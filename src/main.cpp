// hf-gateway — radio HF via internet per Decodium FT2/FT2-Link
//
// Tool standalone senza dipendenze. Emula il percorso audio di una radio HF
// tra due stazioni Decodium collegate via internet, usando un server relay
// self-hosted (server/hf_relay.py su un VPS, es. community.ft2.it): i due
// gateway entrano nella stessa "stanza" (room code) e il server inoltra
// l'audio. Nessun Tailscale, nessuno scambio di IP, funziona con ogni NAT.
//
// PCM raw int16 mono 48 kHz, frame 10 ms — niente codec (AGC/compressione
// dei tool voce distruggono i modi digitali). Protocollo HFGW v1.
//
// Windows:  g++ -O2 -std=c++17 src/main.cpp -o hf-gateway.exe -static -lws2_32 -lole32
// macOS:    cmake -B build && cmake --build build
//
// (c) 2026 IU8LMC — MIT License

#ifdef _WIN32
// winsock2 PRIMA di windows.h (incluso da miniaudio)
#include <winsock2.h>
#include <ws2tcpip.h>
typedef int socklen_t;
#define CLOSESOCK closesocket
#endif

#define MINIAUDIO_IMPLEMENTATION
#include "../third_party/miniaudio.h"

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#ifndef _WIN32
#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
typedef int SOCKET;
#define INVALID_SOCKET (-1)
#define CLOSESOCK close
#endif
#ifdef _WIN32
#include <ws2tcpip.h>  // getaddrinfo
#endif

#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <deque>
#include <fstream>
#include <iostream>
#include <map>
#include <mutex>
#include <random>
#include <string>
#include <thread>
#include <vector>
#include <csignal>
#include <cstdlib>
#include <ctime>
#include <iomanip>

// ---------------------------------------------------------------- protocollo
static const char MAGIC[4] = {'H', 'F', 'G', 'W'};
static const uint8_t VERSION = 1;
enum : uint8_t { FLAG_AUDIO = 0, FLAG_PING = 1, FLAG_PONG = 2, FLAG_REGISTER = 3, FLAG_PEERUP = 4 };
static const int HDR_SIZE = 22;

static uint64_t now_ms() {
    using namespace std::chrono;
    return duration_cast<milliseconds>(steady_clock::now().time_since_epoch()).count();
}
static void put_u32(uint8_t* p, uint32_t v) { p[0]=v>>24; p[1]=v>>16; p[2]=v>>8; p[3]=v; }
static void put_u64(uint8_t* p, uint64_t v) { for (int i=0;i<8;i++) p[i]=uint8_t(v>>(56-8*i)); }
static uint32_t get_u32(const uint8_t* p) { return (uint32_t(p[0])<<24)|(uint32_t(p[1])<<16)|(uint32_t(p[2])<<8)|p[3]; }
static uint64_t get_u64(const uint8_t* p) { uint64_t v=0; for (int i=0;i<8;i++) v=(v<<8)|p[i]; return v; }

// ---------------------------------------------------------------- config
struct Config {
    std::string inName, outName;
    std::string serverHost = "community.ft2.it";
    int serverPort = 5555;
    std::string room = "";
    int listenPort = 0;      // 0 = porta locale effimera (va bene: usciamo verso il server)
    int rate = 48000;
    int jitterMs = 120;
    bool toneTest = false;
    double noiseDbfs = -999.0, attenDb = 0.0, qsbDepthDb = 0.0, qsbPeriod = 20.0;
    std::string statsLog = "";   // file telemetria (opzionale, opt-in)
};

static std::string cfg_path() { return "hfgw.cfg"; }

static bool load_cfg(Config& c) {
    std::ifstream f(cfg_path());
    if (!f) return false;
    std::string line;
    while (std::getline(f, line)) {
        auto eq = line.find('=');
        if (eq == std::string::npos) continue;
        std::string k = line.substr(0, eq), v = line.substr(eq + 1);
        if (!v.empty() && v.back() == '\r') v.pop_back();
        if (k == "in") c.inName = v;
        else if (k == "out") c.outName = v;
        else if (k == "server_host") c.serverHost = v;
        else if (k == "server_port") c.serverPort = std::stoi(v);
        else if (k == "room") c.room = v;
        else if (k == "jitter_ms") c.jitterMs = std::stoi(v);
    }
    return !c.inName.empty() && !c.outName.empty() && !c.room.empty();
}

static void save_cfg(const Config& c) {
    std::ofstream f(cfg_path());
    f << "in=" << c.inName << "\nout=" << c.outName
      << "\nserver_host=" << c.serverHost << "\nserver_port=" << c.serverPort
      << "\nroom=" << c.room << "\njitter_ms=" << c.jitterMs << "\n";
    std::cout << "configurazione salvata in " << cfg_path() << "\n";
}

// ---------------------------------------------------------------- canale HF
struct HfChannel {
    double noiseLin = 0.0, gainLin = 1.0, qsbDepthDb = 0.0, qsbPeriod = 20.0;
    int rate = 48000;
    uint64_t t = 0;
    std::mt19937 rng{std::random_device{}()};
    std::normal_distribution<double> gauss{0.0, 1.0};
    void setup(const Config& c) {
        rate = c.rate;
        if (c.noiseDbfs > -900) noiseLin = std::pow(10.0, c.noiseDbfs / 20.0);
        gainLin = std::pow(10.0, -c.attenDb / 20.0);
        qsbDepthDb = c.qsbDepthDb;
        qsbPeriod = std::max(c.qsbPeriod, 1.0);
    }
    bool active() const { return noiseLin > 0 || gainLin != 1.0 || qsbDepthDb > 0; }
    void process(int16_t* x, int n) {
        for (int i = 0; i < n; i++) {
            double s = x[i] / 32768.0 * gainLin;
            if (qsbDepthDb > 0) {
                double tt = double(t + i) / rate;
                double fadeDb = -0.5 * qsbDepthDb * (1.0 + std::sin(2 * M_PI * tt / qsbPeriod));
                s *= std::pow(10.0, fadeDb / 20.0);
            }
            if (noiseLin > 0) s += gauss(rng) * noiseLin;
            s = std::max(-1.0, std::min(1.0, s));
            x[i] = int16_t(s * 32767.0);
        }
        t += n;
    }
};

// ---------------------------------------------------------------- gateway
struct Gateway {
    Config cfg;
    HfChannel channel;
    SOCKET sock = INVALID_SOCKET;
    sockaddr_in server{};            // destinazione: il relay
    int frame = 480;
    int jitterFrames = 12;

    std::atomic<bool> stop{false};
    std::atomic<uint32_t> seqTx{0};
    std::mutex mx;
    std::map<uint32_t, std::vector<int16_t>> rxBuf;
    bool haveNext = false;
    uint32_t rxNext = 0;
    bool prebuffering = true;

    std::vector<int16_t> inAcc;
    std::deque<int16_t> outAcc;
    double tonePhase = 0.0;

    std::atomic<uint64_t> sent{0}, recvd{0}, lost{0}, late{0}, underrun{0};
    std::atomic<int64_t> rttMs{-1};
    std::atomic<double> inRms{0.0}, outRms{0.0};
    std::atomic<bool> peerUp{false};

    // --- telemetria di rete per diagnosi QSO FT2-Link su internet ---
    std::atomic<uint64_t> netRecv{0};        // pacchetti AUDIO ricevuti dal peer (pre jitter-buffer)
    std::mutex netMx;
    bool haveRxFirst = false;
    uint32_t rxFirstSeq = 0, rxHighSeq = 0;  // per perdita netta da salti di sequenza
    std::mutex rttMx;
    std::deque<int64_t> rttHist;             // ultimi campioni RTT (ms)

    struct RttStat { int64_t last = -1, mn = -1, mx = -1; double avg = -1.0, jit = -1.0; };
    RttStat rtt_stats() {
        RttStat s; s.last = rttMs.load();
        std::lock_guard<std::mutex> lk(rttMx);
        if (rttHist.empty()) return s;
        int64_t sum = 0, mn = rttHist[0], mx = rttHist[0], jsum = 0; size_t jn = 0;
        for (size_t i = 0; i < rttHist.size(); i++) {
            int64_t v = rttHist[i]; sum += v;
            if (v < mn) mn = v;
            if (v > mx) mx = v;
            if (i) { jsum += std::llabs(v - rttHist[i-1]); jn++; }
        }
        s.mn = mn; s.mx = mx; s.avg = double(sum) / double(rttHist.size());
        s.jit = jn ? double(jsum) / double(jn) : 0.0;
        return s;
    }
    // perdita netta di rete (%): pacchetti AUDIO mancanti nella sequenza del peer
    double net_loss_pct(uint64_t& netLostOut) {
        std::lock_guard<std::mutex> lk(netMx);
        netLostOut = 0;
        if (!haveRxFirst) return 0.0;
        uint64_t expected = uint64_t(rxHighSeq - rxFirstSeq) + 1;
        uint64_t got = netRecv.load();
        uint64_t lost = expected > got ? expected - got : 0;
        netLostOut = lost;
        return expected ? 100.0 * double(lost) / double(expected) : 0.0;
    }

    bool resolve_server() {
        addrinfo hints{}, *res = nullptr;
        hints.ai_family = AF_INET;
        hints.ai_socktype = SOCK_DGRAM;
        std::string portStr = std::to_string(cfg.serverPort);
        if (getaddrinfo(cfg.serverHost.c_str(), portStr.c_str(), &hints, &res) != 0 || !res) {
            std::cout << "ERRORE: impossibile risolvere il server '" << cfg.serverHost << "'\n";
            return false;
        }
        std::memcpy(&server, res->ai_addr, sizeof(sockaddr_in));
        freeaddrinfo(res);
        char ip[64]; inet_ntop(AF_INET, &server.sin_addr, ip, sizeof(ip));
        std::cout << "server relay: " << cfg.serverHost << " (" << ip << ":" << cfg.serverPort << ")\n";
        return true;
    }

    bool init_net() {
#ifdef _WIN32
        WSADATA wsa; WSAStartup(MAKEWORD(2, 2), &wsa);
#endif
        if (!resolve_server()) return false;
        sock = socket(AF_INET, SOCK_DGRAM, 0);
        if (sock == INVALID_SOCKET) return false;
        sockaddr_in local{};
        local.sin_family = AF_INET;
        local.sin_addr.s_addr = INADDR_ANY;
        local.sin_port = htons(uint16_t(cfg.listenPort));  // 0 = effimera
        if (bind(sock, (sockaddr*)&local, sizeof(local)) != 0) {
            std::cout << "ERRORE: bind socket UDP fallito\n";
            return false;
        }
#ifdef _WIN32
        DWORD tv = 500; setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof(tv));
#else
        timeval tv{0, 500000}; setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
#endif
        return true;
    }

    void send_to_server(uint8_t flags, const uint8_t* payload, int plen, uint32_t seq, uint64_t tms) {
        uint8_t buf[HDR_SIZE + 4096];
        memcpy(buf, MAGIC, 4);
        buf[4] = VERSION; buf[5] = flags;
        put_u32(buf + 6, seq);
        put_u64(buf + 10, tms);
        put_u32(buf + 18, uint32_t(cfg.rate));
        int len = HDR_SIZE;
        if (payload && plen > 0) { memcpy(buf + HDR_SIZE, payload, plen); len += plen; }
        sendto(sock, (const char*)buf, len, 0, (sockaddr*)&server, sizeof(server));
    }

    void rx_loop() {
        uint8_t buf[8192];
        while (!stop) {
            sockaddr_in from{}; socklen_t fl = sizeof(from);
            int n = recvfrom(sock, (char*)buf, sizeof(buf), 0, (sockaddr*)&from, &fl);
            if (n < HDR_SIZE || memcmp(buf, MAGIC, 4) != 0 || buf[4] != VERSION) continue;
            uint8_t flags = buf[5];
            uint32_t seq = get_u32(buf + 6);
            uint64_t tms = get_u64(buf + 10);
            uint32_t rate = get_u32(buf + 18);
            if (flags == FLAG_PONG) {
                int64_t r = int64_t(now_ms() - tms);
                rttMs = r;
                std::lock_guard<std::mutex> lk(rttMx);
                rttHist.push_back(r);
                if (rttHist.size() > 64) rttHist.pop_front();
                continue;
            }
            if (flags == FLAG_PEERUP) { if (!peerUp.exchange(true)) std::cout << ">>> peer connesso nella stanza\n"; continue; }
            if (flags == FLAG_REGISTER) { continue; }  // ack registrazione
            if (flags != FLAG_AUDIO) continue;
            if (int(rate) != cfg.rate) { late++; continue; }
            int samples = (n - HDR_SIZE) / 2;
            if (samples != frame) continue;
            netRecv++;
            {
                std::lock_guard<std::mutex> lk(netMx);
                if (!haveRxFirst) { haveRxFirst = true; rxFirstSeq = seq; rxHighSeq = seq; }
                else if (seq > rxHighSeq) rxHighSeq = seq;
            }
            std::vector<int16_t> pcm(frame);
            memcpy(pcm.data(), buf + HDR_SIZE, frame * 2);
            std::lock_guard<std::mutex> lk(mx);
            if (!haveNext) { haveNext = true; rxNext = seq; }
            if (seq < rxNext) { late++; continue; }
            rxBuf[seq] = std::move(pcm);
            recvd++;
            while (rxBuf.size() > size_t(4 * jitterFrames)) {
                auto it = rxBuf.begin();
                rxNext = std::max(rxNext, it->first + 1);
                rxBuf.erase(it);
            }
        }
    }

    // registrazione periodica alla stanza + ping RTT (mantiene aperta la mappatura NAT)
    void keepalive_loop() {
        const std::vector<uint8_t> room(cfg.room.begin(), cfg.room.end());
        while (!stop) {
            send_to_server(FLAG_REGISTER, room.data(), int(room.size()), 0, 0);
            send_to_server(FLAG_PING, nullptr, 0, seqTx.load(), now_ms());
            for (int i = 0; i < 20 && !stop; i++)
                std::this_thread::sleep_for(std::chrono::milliseconds(100));  // 2 s
        }
    }

    void audio_cb(int16_t* out, const int16_t* in, uint32_t frames) {
        double acc = 0;
        if (cfg.toneTest) {
            for (uint32_t i = 0; i < frames; i++) {
                double s = 0.5 * std::sin(2 * M_PI * 1500.0 * (tonePhase + i) / cfg.rate);
                inAcc.push_back(int16_t(s * 32767)); acc += s * s;
            }
            tonePhase += frames;
        } else {
            for (uint32_t i = 0; i < frames; i++) {
                inAcc.push_back(in ? in[i] : 0);
                double s = (in ? in[i] : 0) / 32768.0; acc += s * s;
            }
        }
        inRms = std::sqrt(acc / std::max(1u, frames));
        while (inAcc.size() >= size_t(frame)) {
            send_to_server(FLAG_AUDIO, (const uint8_t*)inAcc.data(), frame * 2, seqTx++, now_ms());
            sent++;
            inAcc.erase(inAcc.begin(), inAcc.begin() + frame);
        }
        {
            std::lock_guard<std::mutex> lk(mx);
            if (prebuffering && int(rxBuf.size()) >= jitterFrames) prebuffering = false;
            while (!prebuffering && haveNext && outAcc.size() < frames) {
                auto it = rxBuf.find(rxNext);
                if (it != rxBuf.end()) {
                    auto& f = it->second;
                    if (channel.active()) channel.process(f.data(), frame);
                    outAcc.insert(outAcc.end(), f.begin(), f.end());
                    rxBuf.erase(it); rxNext++;
                } else if (!rxBuf.empty()) {
                    lost++; outAcc.insert(outAcc.end(), frame, 0); rxNext++;
                } else { underrun++; prebuffering = true; break; }
            }
        }
        double oacc = 0;
        for (uint32_t i = 0; i < frames; i++) {
            int16_t s = 0;
            if (!outAcc.empty()) { s = outAcc.front(); outAcc.pop_front(); }
            out[i] = s; double v = s / 32768.0; oacc += v * v;
        }
        outRms = std::sqrt(oacc / std::max(1u, frames));
    }
};

static Gateway* g_gw = nullptr;
static std::atomic<bool> g_quit{false};
static void on_signal(int) { g_quit.store(true); }
static void ma_callback(ma_device* dev, void* out, const void* in, ma_uint32 frames) {
    (void)dev; g_gw->audio_cb((int16_t*)out, (const int16_t*)in, frames);
}

// ---------------------------------------------------------------- device utils
struct Devices {
    ma_context ctx;
    ma_device_info* capture = nullptr;  ma_uint32 nCapture = 0;
    ma_device_info* playback = nullptr; ma_uint32 nPlayback = 0;
    bool ok = false;
    Devices() {
        if (ma_context_init(nullptr, 0, nullptr, &ctx) != MA_SUCCESS) return;
        if (ma_context_get_devices(&ctx, &playback, &nPlayback, &capture, &nCapture) != MA_SUCCESS) return;
        ok = true;
    }
    ~Devices() { if (ok) ma_context_uninit(&ctx); }
    void list() const {
        std::cout << "\nDispositivi di CATTURA (input — dove arriva il TX audio di Decodium):\n";
        for (ma_uint32 i = 0; i < nCapture; i++) std::cout << "  [" << i << "] " << capture[i].name << "\n";
        std::cout << "\nDispositivi di RIPRODUZIONE (output — alimenta l'RX di Decodium):\n";
        for (ma_uint32 i = 0; i < nPlayback; i++) std::cout << "  [" << i << "] " << playback[i].name << "\n";
    }
    int find_capture(const std::string& n) const {
        for (ma_uint32 i = 0; i < nCapture; i++) if (n == capture[i].name) return int(i);
        return -1;
    }
    int find_playback(const std::string& n) const {
        for (ma_uint32 i = 0; i < nPlayback; i++) if (n == playback[i].name) return int(i);
        return -1;
    }
};

static int ask_int(const std::string& prompt, int lo, int hi, int def = -1) {
    while (true) {
        std::cout << prompt;
        std::string s; std::getline(std::cin, s);
        if (s.empty() && def >= 0) return def;
        try { int v = std::stoi(s); if (v >= lo && v <= hi) return v; } catch (...) {}
        std::cout << "  valore non valido (" << lo << "-" << hi << ")\n";
    }
}
static std::string ask_str(const std::string& prompt, const std::string& def = "") {
    std::cout << prompt; std::string s; std::getline(std::cin, s);
    if (s.empty()) return def;
    return s;
}

static bool interactive_setup(Config& c, const Devices& d) {
    std::cout << "\n=== configurazione guidata ===\n";
    d.list();
    if (d.nCapture == 0 || d.nPlayback == 0) {
        std::cout << "ERRORE: nessun dispositivo audio. Installa i cavi virtuali (VB-Cable / BlackHole).\n";
        return false;
    }
    int ci = ask_int("\nScegli l'INPUT (numero): ", 0, int(d.nCapture) - 1);
    int pi = ask_int("Scegli l'OUTPUT (numero): ", 0, int(d.nPlayback) - 1);
    c.inName = d.capture[ci].name;
    c.outName = d.playback[pi].name;
    c.serverHost = ask_str("Server relay [community.ft2.it]: ", "community.ft2.it");
    c.serverPort = ask_int("Porta del server [5555]: ", 1, 65535, 5555);
    std::cout << "Codice stanza (lo STESSO su entrambe le stazioni, es. iu8lmc-elisir80): ";
    std::getline(std::cin, c.room);
    while (c.room.empty()) { std::cout << "  il codice stanza e' obbligatorio: "; std::getline(std::cin, c.room); }
    save_cfg(c);
    return true;
}

// ---------------------------------------------------------------- main
int main(int argc, char** argv) {
    Config cfg;
    bool reconfigure = false, listOnly = false;
    for (int i = 1; i < argc; i++) {
        std::string a = argv[i];
        auto nextd = [&](double& v) { if (i + 1 < argc) v = std::stod(argv[++i]); };
        auto nexts = [&](std::string& v) { if (i + 1 < argc) v = argv[++i]; };
        if (a == "--tone-test") cfg.toneTest = true;
        else if (a == "--reconfigure" || a == "-r") reconfigure = true;
        else if (a == "--list-devices") listOnly = true;
        else if (a == "--room") nexts(cfg.room);
        else if (a == "--server") nexts(cfg.serverHost);
        else if (a == "--noise-dbfs") nextd(cfg.noiseDbfs);
        else if (a == "--attenuate-db") nextd(cfg.attenDb);
        else if (a == "--qsb-depth-db") nextd(cfg.qsbDepthDb);
        else if (a == "--qsb-period") nextd(cfg.qsbPeriod);
        else if (a == "--jitter-ms") { double v = 120; nextd(v); cfg.jitterMs = int(v); }
        else if (a == "--stats-log") {
            if (i + 1 < argc && argv[i + 1][0] != '-') cfg.statsLog = argv[++i];
            else cfg.statsLog = "hfgw_stats.log";
        }
        else if (a == "--help" || a == "-h") {
            std::cout <<
                "hf-gateway — radio HF via internet per Decodium FT2/FT2-Link\n\n"
                "Senza argomenti: config guidata al 1o avvio (salvata in hfgw.cfg), poi automatico.\n"
                "I due gateway usano lo STESSO --room sullo stesso --server: il relay li accoppia.\n\n"
                "  --reconfigure      rifai la configurazione guidata\n"
                "  --list-devices     elenca i dispositivi audio ed esce\n"
                "  --room CODICE      codice stanza condiviso\n"
                "  --server HOST      server relay (default community.ft2.it)\n"
                "  --tone-test        trasmette un tono 1500 Hz (collaudo senza Decodium)\n"
                "  --jitter-ms N      jitter buffer (default 120)\n"
                "  --stats-log [F]    logga telemetria (RTT/perdita) su CSV (default hfgw_stats.log)\n"
                "canale HF (default OFF): --noise-dbfs X  --attenuate-db X  --qsb-depth-db X  --qsb-period X\n";
            return 0;
        }
    }

    std::cout << "=== hf-gateway v1.1 — radio HF via internet (FT2/FT2-Link) ===\n";
    Devices dev;
    if (!dev.ok) { std::cout << "ERRORE: init audio fallita\n"; return 1; }
    if (listOnly) { dev.list(); return 0; }

    bool haveCfg = !reconfigure && load_cfg(cfg);
    if (haveCfg && (dev.find_capture(cfg.inName) < 0 || dev.find_playback(cfg.outName) < 0)) {
        std::cout << "AVVISO: un dispositivo salvato non esiste piu' — riconfiguro.\n";
        haveCfg = false;
    }
    if (haveCfg) {
        std::cout << "config (hfgw.cfg): in='" << cfg.inName << "' out='" << cfg.outName
                  << "' server=" << cfg.serverHost << ":" << cfg.serverPort
                  << " stanza='" << cfg.room << "'\n";
    } else if (!interactive_setup(cfg, dev)) return 1;

    int ci = dev.find_capture(cfg.inName);
    int pi = dev.find_playback(cfg.outName);

    Gateway gw;
    gw.cfg = cfg;
    gw.frame = cfg.rate / 100;
    gw.jitterFrames = std::max(2, cfg.jitterMs / 10);
    gw.channel.setup(cfg);
    if (!gw.init_net()) return 1;
    g_gw = &gw;

    ma_device_config dc = ma_device_config_init(ma_device_type_duplex);
    dc.sampleRate = ma_uint32(cfg.rate);
    dc.capture.pDeviceID = &dev.capture[ci].id;
    dc.capture.format = ma_format_s16;  dc.capture.channels = 1;
    dc.playback.pDeviceID = &dev.playback[pi].id;
    dc.playback.format = ma_format_s16; dc.playback.channels = 1;
    dc.periodSizeInFrames = ma_uint32(gw.frame);
    dc.dataCallback = ma_callback;

    ma_device device;
    if (ma_device_init(&dev.ctx, &dc, &device) != MA_SUCCESS) {
        std::cout << "ERRORE: apertura dispositivi audio fallita (48 kHz mono)\n"; return 1;
    }
    if (ma_device_start(&device) != MA_SUCCESS) {
        std::cout << "ERRORE: avvio stream audio fallito\n"; return 1;
    }

    std::thread trx(&Gateway::rx_loop, &gw);
    std::thread tka(&Gateway::keepalive_loop, &gw);
    std::signal(SIGINT, on_signal);
    std::signal(SIGTERM, on_signal);

    std::ofstream stats;
    if (!cfg.statsLog.empty()) {
        stats.open(cfg.statsLog, std::ios::app);
        if (stats) {
            stats << "# hf-gateway telemetria — stanza=" << cfg.room
                  << " server=" << cfg.serverHost << ":" << cfg.serverPort << "\n";
            stats << "wallclock,uptime_s,peer,tx,rx,net_lost,loss_pct,buf_lost,underrun,"
                     "rtt_last_ms,rtt_min_ms,rtt_avg_ms,rtt_max_ms,rtt_jit_ms,in_dbfs,out_dbfs\n";
            stats.flush();
            std::cout << "telemetria loggata in " << cfg.statsLog << "\n";
        } else {
            std::cout << "AVVISO: impossibile aprire il file telemetria '" << cfg.statsLog << "'\n";
        }
    }

    std::cout << "\ngateway ATTIVO — stanza '" << cfg.room << "' su " << cfg.serverHost << ":" << cfg.serverPort
              << "\ncanale HF: " << (gw.channel.active() ? "ATTIVO" : "pass-through")
              << (cfg.toneTest ? "  [TONO DI TEST 1500 Hz]" : "")
              << "\nin attesa del peer nella stessa stanza... (Ctrl+C per uscire)\n\n";

    auto dbfs = [](double v) {
        char b[16]; snprintf(b, sizeof(b), "%5.1f", 20.0 * std::log10(std::max(v, 1e-9))); return std::string(b);
    };
    auto wallclock = []() {
        std::time_t tt = std::time(nullptr);
        char b[32]; std::strftime(b, sizeof(b), "%Y-%m-%d %H:%M:%S", std::localtime(&tt));
        return std::string(b);
    };
    uint64_t t0 = now_ms();
    while (!g_quit) {
        std::this_thread::sleep_for(std::chrono::seconds(2));
        uint64_t netLost = 0;
        double lossPct = gw.net_loss_pct(netLost);
        Gateway::RttStat rs = gw.rtt_stats();
        double up = double(now_ms() - t0) / 1000.0;
        std::cout << (gw.peerUp ? "[peer OK] " : "[no peer] ")
                  << "tx " << gw.sent << "  rx " << gw.recvd
                  << "  loss " << std::fixed << std::setprecision(1) << lossPct << "% (" << netLost << ")"
                  << "  underrun " << gw.underrun
                  << "  rtt " << rs.last << " ms (avg " << std::setprecision(0) << rs.avg
                  << " max " << rs.mx << " jit " << std::setprecision(1) << rs.jit << ")"
                  << "  in " << dbfs(gw.inRms) << "  out " << dbfs(gw.outRms) << " dBFS\n";
        if (stats) {
            stats << wallclock() << "," << std::fixed << std::setprecision(1) << up << ","
                  << (gw.peerUp ? 1 : 0) << "," << gw.sent << "," << gw.recvd << ","
                  << netLost << "," << lossPct << "," << gw.lost << "," << gw.underrun << ","
                  << rs.last << "," << rs.mn << "," << std::setprecision(1) << rs.avg << ","
                  << rs.mx << "," << rs.jit << ","
                  << dbfs(gw.inRms) << "," << dbfs(gw.outRms) << "\n";
            stats.flush();
        }
    }

    std::cout << "\nchiusura in corso...\n";
    gw.stop = true;
    ma_device_stop(&device);
    if (trx.joinable()) trx.join();
    if (tka.joinable()) tka.join();
    {
        uint64_t netLost = 0;
        double lossPct = gw.net_loss_pct(netLost);
        Gateway::RttStat rs = gw.rtt_stats();
        std::cout << "riepilogo sessione: tx " << gw.sent << "  rx " << gw.recvd
                  << "  perdita " << std::fixed << std::setprecision(1) << lossPct << "% (" << netLost << ")"
                  << "  underrun " << gw.underrun
                  << "  rtt avg " << std::setprecision(0) << rs.avg << " max " << rs.mx << " ms\n";
        if (stats) {
            stats << "# fine sessione — tx " << gw.sent << " rx " << gw.recvd
                  << " loss " << std::setprecision(1) << lossPct << "% rtt_avg " << rs.avg
                  << " rtt_max " << rs.mx << "\n";
            stats.flush(); stats.close();
        }
    }
    ma_device_uninit(&device);
    return 0;
}
