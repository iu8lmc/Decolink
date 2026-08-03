// Decolink — collega la radio a Decodium Mobile: audio RX (e, con il CAT,
// il controllo del rig) su rete. Protocollo HFGW v1.
//
// Manda l'audio RX della radio (CODEC USB del rig) a Decodium Mobile, in tre
// modi selezionabili:
//   LAN diretta  : il telefono e' sulla stessa rete, gli si spara l'audio all'IP.
//   Relay+stanza : PC e telefono entrano nella stessa stanza sul relay (VPS);
//                  funziona ovunque, anche con il telefono su dati mobili,
//                  perche' entrambi ESCONO verso il relay (nessun NAT da bucare).
//   Il telefono chiama casa : il PC ascolta su una porta (inoltrata sul router,
//                  raggiungibile via DynDNS); il telefono si registra e da quel
//                  momento riceve l'audio all'indirizzo da cui si e' fatto vivo.
//
// Pacchetto: header 22 byte big-endian
//   "HFGW"(4) | versione(1) | flag(1) | seq u32 | t_ms u64 | rate u32
// seguito da PCM int16 mono little-endian, 10 ms per pacchetto.

#include <QApplication>
#include <QCheckBox>
#include <QAudioDevice>
#include <QAudioFormat>
#include <QAudioSink>
#include <QAudioSource>
#include <QComboBox>
#include <QDateTime>
#include <QEventLoop>
#include <QFormLayout>
#include <QFrame>
#include <QGroupBox>
#include <QHostInfo>
#include <QIcon>
#include <QHBoxLayout>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QLabel>
#include <QLineEdit>
#include <QMap>
#include <QMediaDevices>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QProgressBar>
#include <QPushButton>
#include <QSerialPort>
#include <QSerialPortInfo>
#include <QSettings>
#include <QSpinBox>
#include <QTcpServer>
#include <QTcpSocket>
#include <QTextStream>
#include <QTimer>
#include <QUdpSocket>
#include <QVBoxLayout>
#include <QWidget>

#include <QElapsedTimer>
#include <QMutex>

#include "cwkey.h"
#ifdef DECOLINK_CON_HAMLIB
#include "hamlibrig.h"
#endif
#include "dlproto.h"
#include "lossless.h"
#include "opusvoce.h"
#include "resample.h"
#ifdef DECOLINK_CON_FREEDV
#include "freedvlink.h"
#endif

#include <cmath>

namespace {

constexpr int kRate      = 48000;
constexpr int kFrame     = kRate / 100;   // 480 campioni = 10 ms
constexpr int kHdrSize   = 22;
// Blocco dei digitali: 40 ms, che a 48 kHz in ingresso sono 1920 campioni e a
// 12 kHz in uscita 480. Quaranta millisecondi sono una misura comoda per il
// compressore (abbastanza contesto per predire bene) e irrilevante per la
// latenza, che in questo profilo non conta.
constexpr int kDigiIngresso = kRate / 25;
// v2: per entrare nel relay serve un token firmato dal servizio di accesso.
// La v1, in cui bastava indovinare il nome della stanza, non e' piu' accettata.
constexpr quint8 kProtoVer = 2;
constexpr quint8 kFlagAudio = 0, kFlagPing = 1, kFlagPong = 2,
                 kFlagRegister = 3, kFlagPeerUp = 4,
                 kFlagCatReq = 5, kFlagCatRsp = 6,   // comandi CAT sullo stesso canale
                 kFlagTxAudio = 7,                   // audio che il telefono vuole trasmettere
                 kFlagDenied = 8;                    // il relay spiega perche' non si entra

void putU32(char* p, quint32 v) { p[0]=char(v>>24); p[1]=char(v>>16); p[2]=char(v>>8); p[3]=char(v); }
void putU64(char* p, quint64 v) { for (int i = 0; i < 8; ++i) p[i] = char(v >> (56 - 8*i)); }
quint32 getU32(const uchar* p) { return (quint32(p[0])<<24)|(quint32(p[1])<<16)|(quint32(p[2])<<8)|p[3]; }

// La frequenza va scritta nell'intestazione, non data per scontata: e' il campo
// che dice a chi riceve a che velocita' riprodurre. Mandare 12 kHz dichiarando
// 48 farebbe sentire l'audio al quadruplo della velocita'.
QByteArray hfgwPacket(quint8 flags, quint32 seq, const char* payload, int len,
                      int rate = kRate)
{
    QByteArray pkt(kHdrSize + qMax(0, len), Qt::Uninitialized);
    char* p = pkt.data();
    std::memcpy(p, "HFGW", 4);
    p[4] = char(kProtoVer); p[5] = char(flags);
    putU32(p + 6, seq);
    putU64(p + 10, quint64(QDateTime::currentMSecsSinceEpoch()));
    putU32(p + 18, quint32(rate));
    if (payload && len > 0) std::memcpy(p + kHdrSize, payload, size_t(len));
    return pkt;
}

enum Mode { ModeLan = 0, ModeRelay = 1, ModeListen = 2 };

// Aspetto della finestra: gli stessi colori del sito e dell'icona — fondo blu
// notte, ciano come accento, verde acqua per le conferme. Un programma e il suo
// sito che si somigliano si riconoscono come la stessa cosa.
QString foglioStile()
{
    return QStringLiteral(R"(
QWidget { background:#0d1622; color:#e8edf5;
          font-family:"Helvetica Neue"; font-size:13px }
QLabel#logo { font-size:16px; font-weight:800; letter-spacing:2px; color:#00e5ff }
QLabel#titolo { font-size:11px; font-weight:700; letter-spacing:1.2px; color:#5d7ba3;
                padding-bottom:2px }
QLabel#minuscolo { font-size:10px; color:#5d7ba3; letter-spacing:.5px }
QLabel#identita { color:#8fb3d9; font-size:12px }
QLabel#stato { color:#e8edf5; font-size:12px; padding:7px 10px;
               background:rgba(22,33,62,.55); border:1px solid #243b63; border-radius:7px }
QLabel#numeri { color:#7d98bd; font-size:11px; padding:0 2px }
QFrame#divisorio { background:#1d2c56; border:0; max-width:1px; min-width:1px }

QLineEdit, QComboBox, QSpinBox {
    background:#0b1018; border:1px solid #243b63; border-radius:6px;
    padding:6px 9px; min-height:17px; selection-background-color:#00e5ff;
    selection-color:#06131c }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border-color:#00e5ff }
QLineEdit:disabled, QComboBox:disabled, QSpinBox:disabled { color:#4a5a72; background:#0a1017 }
QComboBox::drop-down { border:0; width:18px }
QComboBox::down-arrow { image:none; border-left:4px solid transparent;
    border-right:4px solid transparent; border-top:5px solid #5d7ba3; margin-right:7px }

/* Le frecce dei campi numerici: senza queste righe Qt usa quelle di sistema, che
   sul tema scuro finiscono sopra al numero e lo rendono illeggibile. */
QSpinBox { padding-right:16px }
QSpinBox::up-button, QSpinBox::down-button {
    subcontrol-origin:border; width:14px; border:0; background:transparent }
QSpinBox::up-button { subcontrol-position:top right; margin:2px 2px 0 0 }
QSpinBox::down-button { subcontrol-position:bottom right; margin:0 2px 2px 0 }
QSpinBox::up-arrow { image:none; width:0; height:0; border-left:3px solid transparent;
    border-right:3px solid transparent; border-bottom:4px solid #5d7ba3 }
QSpinBox::down-arrow { image:none; width:0; height:0; border-left:3px solid transparent;
    border-right:3px solid transparent; border-top:4px solid #5d7ba3 }
QSpinBox::up-arrow:hover, QSpinBox::down-arrow:hover { border-bottom-color:#00e5ff;
    border-top-color:#00e5ff }
QComboBox QAbstractItemView { background:#0b1018; border:1px solid #243b63;
    selection-background-color:#16213e; outline:none; padding:3px }

QPushButton { background:#16213e; border:1px solid #243b63; border-radius:7px;
              padding:7px 15px; color:#cfe0f0 }
QPushButton:hover { border-color:#00e5ff; color:#e8edf5 }
QPushButton:pressed { background:#1d2c56 }
QPushButton#principale { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,
                            stop:0 #00e5ff, stop:1 #36d8ad);
                         color:#06131c; font-weight:700; font-size:14px; border:0 }
QPushButton#principale:hover { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,
                            stop:0 #3aecff, stop:1 #55e6c0) }
QPushButton#piatto { background:transparent; border:0; color:#5d7ba3; text-align:left;
                     padding:3px 2px; font-size:12px }
QPushButton#piatto:hover { color:#00e5ff }

QCheckBox { color:#8fb3d9; spacing:7px }
QCheckBox::indicator { width:15px; height:15px; border:1px solid #243b63;
                       border-radius:4px; background:#0b1018 }
QCheckBox::indicator:checked { background:#00e5ff; border-color:#00e5ff }

QProgressBar { background:#0b1018; border:1px solid #243b63; border-radius:4px }
QProgressBar::chunk { border-radius:3px;
    background:qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #36d8ad, stop:1 #00e5ff) }
QToolTip { background:#16213e; color:#e8edf5; border:1px solid #00e5ff; padding:5px }
)");
}

} // namespace


// Coda dell'audio da trasmettere, letta dalla scheda in modalita' pull: e' la
// scheda a chiedere i campioni quando le servono. Se la coda e' vuota si manda
// silenzio invece di lasciarla a secco (un vuoto si sentirebbe come uno scatto),
// e se il ritardo cresce troppo si scartano i campioni piu' vecchi in un colpo.
class TxQueue : public QIODevice
{
    Q_OBJECT
public:
    explicit TxQueue(QObject* parent = nullptr) : QIODevice(parent) {}
    void push(const QByteArray& pcm)
    {
        QMutexLocker lock(&m_mx);
        m_buf.append(pcm);
        if (m_buf.size() > kMaxBytes) m_buf.remove(0, m_buf.size() - kMaxBytes);
        m_lastMs = QDateTime::currentMSecsSinceEpoch();
    }
    bool idle(qint64 forMs) const
    {
        QMutexLocker lock(&m_mx);
        return m_lastMs > 0 && QDateTime::currentMSecsSinceEpoch() - m_lastMs > forMs;
    }
    bool isSequential() const override { return true; }
    qint64 bytesAvailable() const override
    {
        QMutexLocker lock(&m_mx);
        // flusso infinito: readData restituisce sempre quanto richiesto
        return qMax<qint64>(m_buf.size(), 8192) + QIODevice::bytesAvailable();
    }
protected:
    qint64 readData(char* data, qint64 maxlen) override
    {
        if (maxlen <= 0) return 0;
        QMutexLocker lock(&m_mx);
        qint64 const n = qMin<qint64>(maxlen, m_buf.size());
        if (n > 0) { std::memcpy(data, m_buf.constData(), size_t(n)); m_buf.remove(0, int(n)); }
        if (n < maxlen) std::memset(data + n, 0, size_t(maxlen - n));
        return maxlen;
    }
    qint64 writeData(const char*, qint64) override { return 0; }
private:
    // 2 s: assorbe il jitter della rete senza accumulare ritardo. Il telefono
    // manda l'audio a tempo reale, quindi la coda resta sempre corta.
    static constexpr int kMaxBytes = 192000;
    mutable QMutex m_mx;
    QByteArray m_buf;
    qint64 m_lastMs {0};
};

// Controllo del rig sulla seriale, in dialetto Yaesu (comandi terminati da ';').
// All'esterno parla il protocollo di rigctld (netrigctl), che Decodium Mobile
// gia' conosce: cosi' il telefono non cambia, e sul PC basta questo programma
// invece di installare Hamlib e lanciare rigctld a mano.
class CatRig : public QObject
{
    Q_OBJECT
public:
    explicit CatRig(QObject* parent = nullptr) : QObject(parent) {}

#ifdef DECOLINK_CON_HAMLIB
    // Apre la radio attraverso Hamlib. Da qui in poi frequenza, modo e PTT
    // passano dalla libreria, che sa come parla il singolo modello: sono
    // trecento apparati contro i due che sappiamo fare a mano.
    bool openHamlib(int modello, const QString& porta, int baud, int bitDati,
                    int bitStop, const QString& handshake)
    {
        close();
        if (!m_ham.apri(modello, porta, baud, bitDati, bitStop, handshake)) {
            m_error = m_ham.errore();
            return false;
        }
        m_usaHamlib = true;
        return true;
    }
    QString hamlibNome() const { return m_ham.nome(); }
#endif

    bool open(const QString& portName, int baud, QSerialPort::DataBits dataBits,
              QSerialPort::Parity parity, QSerialPort::StopBits stopBits,
              QSerialPort::FlowControl flowControl, bool icom = false, int civAddress = 0x94)
    {
        close();
        m_port = new QSerialPort(portName, this);
        m_port->setBaudRate(baud);
        m_port->setDataBits(dataBits);
        m_port->setParity(parity);
        m_port->setStopBits(stopBits);
        m_port->setFlowControl(flowControl);
        m_icom = icom;
        m_civAddress = quint8(civAddress & 0xff);
        if (!m_port->open(QIODevice::ReadWrite)) {
            m_error = m_port->errorString();
            m_port->deleteLater(); m_port = nullptr;
            return false;
        }
        m_port->setDataTerminalReady(true);
        m_port->setRequestToSend(false);
        return true;
    }

    void close()
    {
        if (m_port) { m_port->close(); m_port->deleteLater(); m_port = nullptr; }
#ifdef DECOLINK_CON_HAMLIB
        m_ham.chiudi();
        m_usaHamlib = false;
#endif
    }

    bool isOpen() const
    {
#ifdef DECOLINK_CON_HAMLIB
        if (m_usaHamlib) return m_ham.aperto();
#endif
        return m_port && m_port->isOpen();
    }
    QString error() const { return m_error; }

    // Esegue una riga di comando netrigctl e restituisce la risposta da mandare
    // indietro. Il telefono usa solo questi verbi: f, m, F <hz>, T <0|1>.
    QString handle(const QString& line)
    {
        QString const cmd = line.trimmed();
        if (cmd.isEmpty()) return QString();
        if (cmd == QLatin1String("f")) {
            qint64 const hz = readFreq();
            return hz > 0 ? QString::number(hz) + "\n" : QStringLiteral("RPRT -1\n");
        }
        if (cmd == QLatin1String("m")) {
            QString const md = readMode();
            return md.isEmpty() ? QStringLiteral("RPRT -1\n") : md + "\n3000\n";
        }
        if (cmd.startsWith(QLatin1String("F "))) {
            bool ok = false;
            qint64 const hz = cmd.mid(2).trimmed().toLongLong(&ok);
            if (!ok || hz <= 0) return QStringLiteral("RPRT -1\n");
            setFrequency(hz);
            return QStringLiteral("RPRT 0\n");
        }
        if (cmd.startsWith(QLatin1String("T "))) {
            bool const on = cmd.mid(2).trimmed().toInt() != 0;
            setPtt(on);
            return QStringLiteral("RPRT 0\n");
        }
        if (cmd == QLatin1String("t")) {
            QString const r = m_icom ? civQuery(QByteArray(1, char(0x1c)) + QByteArray(1, char(0)))
                                     : query(QStringLiteral("TX;"), QStringLiteral("TX"));
#ifdef DECOLINK_CON_HAMLIB
            if (m_usaHamlib)
                return m_ham.inTrasmissione() ? QStringLiteral("1\n") : QStringLiteral("0\n");
#endif
            if (m_icom) return (r.size() >= 3 && quint8(r.at(2).toLatin1()) != 0) ? QStringLiteral("1\n") : QStringLiteral("0\n");
            return (r.size() >= 3 && r.at(2) != QLatin1Char('0')) ? QStringLiteral("1\n") : QStringLiteral("0\n");
        }
        // Comandi Yaesu grezzi, come il "w"/"W" di rigctl: servono per quello che
        // netrigctl non copre (potenza, misuratori). "w" invia e basta (i set
        // Yaesu non rispondono), "W" invia e restituisce la risposta.
        if (cmd.startsWith(QLatin1String("w "))) {
            send(cmd.mid(2).trimmed());
            return QStringLiteral("RPRT 0\n");
        }
        if (cmd.startsWith(QLatin1String("W "))) {
            QString const r = query(cmd.mid(2).trimmed(), QString());
            return r.isEmpty() ? QStringLiteral("RPRT -1\n") : r + "\n";
        }
        // Imposta il modo. Prima rispondeva "eseguito" senza fare niente, e chi
        // clicca una stazione sul cluster si ritrovava sulla frequenza giusta
        // con il modo sbagliato — senza che nessuno segnalasse l'errore, perche'
        // la risposta diceva che era andato tutto bene.
        if (cmd.startsWith(QLatin1String("M "))) {
            QString const modo = cmd.mid(2).trimmed().section(QLatin1Char(' '), 0, 0).toUpper();
            QChar const codice = codiceModo(modo);
            if (codice.isNull()) return QStringLiteral("RPRT -1\n");   // meglio dirlo
            setMode(modo);
            // La larghezza del filtro, se indicata, si lascia al rig: cambiarla
            // via CAT su un Yaesu vuol dire toccare i menu, e un click su uno
            // spot non deve riconfigurare la stazione di chi ascolta.
            return QStringLiteral("RPRT 0\n");
        }
        return QStringLiteral("RPRT 0\n");
    }

    // Dal nome del modo al codice del rig. E' la tabella di readMode() letta al
    // contrario, con i nomi che usano rigctl e i programmi che ci parlano:
    // cliccando una stazione sul cluster arriva "M USB 2400" o "M CW 500", e
    // deve finire sulla radio come modo giusto, non come risposta di cortesia.
    static QChar codiceModo(const QString& m)
    {
        if (m == QLatin1String("LSB"))    return QLatin1Char('1');
        if (m == QLatin1String("USB"))    return QLatin1Char('2');
        if (m == QLatin1String("CW"))     return QLatin1Char('3');
        if (m == QLatin1String("FM"))     return QLatin1Char('4');
        if (m == QLatin1String("AM"))     return QLatin1Char('5');
        if (m == QLatin1String("RTTY"))   return QLatin1Char('6');
        if (m == QLatin1String("CWR") || m == QLatin1String("CW-R"))
            return QLatin1Char('7');
        if (m == QLatin1String("PKTLSB") || m == QLatin1String("DATA-L")
            || m == QLatin1String("DIGL"))
            return QLatin1Char('8');
        if (m == QLatin1String("RTTYR") || m == QLatin1String("RTTY-R"))
            return QLatin1Char('9');
        if (m == QLatin1String("PKTFM"))  return QLatin1Char('A');
        if (m == QLatin1String("FMN"))    return QLatin1Char('B');
        if (m == QLatin1String("PKTUSB") || m == QLatin1String("DATA-U")
            || m == QLatin1String("DIGU"))
            return QLatin1Char('C');
        if (m == QLatin1String("AMN"))    return QLatin1Char('D');
        if (m == QLatin1String("C4FM"))   return QLatin1Char('E');
        return QChar();      // sconosciuto: meglio un errore che il modo sbagliato
    }

    qint64 readFreq()
    {
#ifdef DECOLINK_CON_HAMLIB
        if (m_usaHamlib) return m_ham.frequenza();
#endif
        if (m_icom) {
            QByteArray const r = civQuery(QByteArray(1, char(0x03)));
            if (r.size() < 5) return 0;
            qint64 hz = 0, mul = 1;
            for (int i = 0; i < 5; ++i) {
                const quint8 b = quint8(r.at(i));
                hz += ((b & 0x0f) + 10 * ((b >> 4) & 0x0f)) * mul;
                mul *= 100;
            }
            return hz;
        }
        QString const r = query(QStringLiteral("FA;"), QStringLiteral("FA"));
        if (r.size() < 11) return 0;
        return r.mid(2, 9).toLongLong();
    }

    QString readMode()
    {
#ifdef DECOLINK_CON_HAMLIB
        if (m_usaHamlib) return m_ham.modo();
#endif
        if (m_icom) {
            QByteArray const r = civQuery(QByteArray(1, char(0x04)));
            if (r.isEmpty()) return QString();
            switch (quint8(r.at(0))) {
            case 0x00: return QStringLiteral("LSB"); case 0x01: return QStringLiteral("USB");
            case 0x02: return QStringLiteral("AM"); case 0x03: return QStringLiteral("CW");
            case 0x04: return QStringLiteral("RTTY"); case 0x05: return QStringLiteral("FM");
            case 0x06: return QStringLiteral("CWR"); case 0x07: return QStringLiteral("RTTYR");
            default: return QString();
            }
        }
        QString const r = query(QStringLiteral("MD0;"), QStringLiteral("MD"));
        if (r.size() < 4) return QString();
        // codici del FT-991: la lettera finale identifica il modo
        switch (r.at(3).toLatin1()) {
        case '1': return QStringLiteral("LSB");     case '2': return QStringLiteral("USB");
        case '3': return QStringLiteral("CW");      case '4': return QStringLiteral("FM");
        case '5': return QStringLiteral("AM");      case '6': return QStringLiteral("RTTY");
        case '7': return QStringLiteral("CWR");     case '8': return QStringLiteral("PKTLSB");
        case '9': return QStringLiteral("RTTYR");   case 'A': return QStringLiteral("PKTFM");
        case 'B': return QStringLiteral("FMN");     case 'C': return QStringLiteral("PKTUSB");
        case 'D': return QStringLiteral("AMN");     case 'E': return QStringLiteral("C4FM");
        default:  return QStringLiteral("USB");
        }
    }

private:
    void setFrequency(qint64 hz)
    {
#ifdef DECOLINK_CON_HAMLIB
        if (m_usaHamlib) { m_ham.impostaFrequenza(hz); return; }
#endif
        if (!m_icom) { send(QStringLiteral("FA%1;").arg(hz, 9, 10, QChar('0'))); return; }
        QByteArray d(5, 0); qint64 v = hz;
        for (int i = 0; i < 5; ++i) { d[i] = char((v % 10) | ((v / 10 % 10) << 4)); v /= 100; }
        civWrite(0x05, d);
    }

    void setPtt(bool on)
    {
#ifdef DECOLINK_CON_HAMLIB
        if (m_usaHamlib) { m_ham.trasmetti(on); return; }
#endif
        if (!m_icom) { send(on ? QStringLiteral("TX1;") : QStringLiteral("TX0;")); return; }
        QByteArray d(2, 0); d[0] = 0x00; d[1] = on ? 0x01 : 0x00; civWrite(0x1c, d);
    }

    void setMode(const QString& mode)
    {
#ifdef DECOLINK_CON_HAMLIB
        if (m_usaHamlib) { m_ham.impostaModo(mode); return; }
#endif
        if (!m_icom) { const QChar c = codiceModo(mode); send(QStringLiteral("MD0%1;").arg(c)); return; }
        static const QHash<QString, quint8> modes{{"LSB",0x00},{"USB",0x01},{"AM",0x02},{"CW",0x03},{"RTTY",0x04},{"FM",0x05},{"CWR",0x06},{"RTTYR",0x07}};
        if (modes.contains(mode)) civWrite(0x06, QByteArray(2, char(modes.value(mode))));
    }

    void civWrite(quint8 command, const QByteArray& data)
    {
        if (!isOpen()) return;
        QByteArray frame("\xfe\xfe", 2); frame.append(char(m_civAddress)); frame.append(char(0xe0)); frame.append(char(command)); frame.append(data); frame.append(char(0xfd));
        m_port->write(frame); m_port->waitForBytesWritten(300);
    }

    QByteArray civQuery(const QByteArray& command)
    {
        if (!isOpen()) return {};
        QByteArray frame("\xfe\xfe", 2); frame.append(char(m_civAddress)); frame.append(char(0xe0)); frame.append(command); frame.append(char(0xfd));
        m_port->clear(QSerialPort::Input); m_port->write(frame); m_port->waitForBytesWritten(300);
        QByteArray acc; QElapsedTimer t; t.start();
        while (t.elapsed() < 500) {
            if (!m_port->waitForReadyRead(80)) continue; acc += m_port->readAll();
            const int start = acc.indexOf("\xfe\xfe", 2); const int end = acc.indexOf(char(0xfd), start);
            if (start >= 0 && end > start + 4) return acc.mid(start + 5, end - start - 5);
        }
        return {};
    }

    void send(const QString& s)
    {
        if (!isOpen()) return;
        m_port->write(s.toLatin1());
        m_port->waitForBytesWritten(200);
    }

    // Il rig risponde con una stringa terminata da ';'. I set Yaesu NON
    // rispondono: si interroga solo per i get, con un tetto di attesa breve
    // per non bloccare l'interfaccia.
    QString query(const QString& cmd, const QString& expect)
    {
        if (!isOpen()) return QString();
        m_port->clear(QSerialPort::Input);
        send(cmd);
        QByteArray acc;
        QElapsedTimer t; t.start();
        while (t.elapsed() < 400) {
            if (!m_port->waitForReadyRead(80)) continue;
            acc += m_port->readAll();
            int const end = acc.indexOf(';');
            if (end >= 0) {
                QString const r = QString::fromLatin1(acc.left(end + 1));
                if (expect.isEmpty() || r.startsWith(expect)) return r;
                acc.remove(0, end + 1);
            }
        }
        return QString();
    }

    QSerialPort* m_port {nullptr};
    QString m_error;
#ifdef DECOLINK_CON_HAMLIB
    dl::HamlibRig m_ham;
    bool m_usaHamlib {false};
#endif
    bool m_icom {false};
    quint8 m_civAddress {0x94};
};

class Client : public QWidget
{
    Q_OBJECT
public:
    Client()
    {
        setWindowTitle(QStringLiteral("Decolink — la radio su Decodium Mobile"));

        m_device = new QComboBox;
        for (QAudioDevice const& d : QMediaDevices::audioInputs())
            m_device->addItem(d.description());

        m_mode = new QComboBox;
        m_mode->addItem(QStringLiteral("LAN diretta"));
        m_mode->addItem(QStringLiteral("Relay + stazione"));
        m_mode->addItem(QStringLiteral("Il telefono chiama casa"));
        m_mode->setToolTip(QStringLiteral(
            "LAN diretta — il telefono è sulla stessa rete: gli si manda l'audio all'indirizzo\n"
            "Relay + stazione — funziona ovunque, anche su dati mobili: PC e telefono\n"
            "   escono entrambi verso il relay, quindi non c'è nessun router da configurare\n"
            "Il telefono chiama casa — porta inoltrata sul router e nome DynDNS"));

        m_host = new QLineEdit;
        m_host->setPlaceholderText(QStringLiteral("IP del telefono, oppure host del relay"));
        m_port = new QSpinBox; m_port->setRange(1, 65535); m_port->setValue(5555);
        m_station = new QComboBox;
        m_station->setEnabled(false);
        m_station->addItem(QStringLiteral("(accedi per scegliere la stazione)"));

        // Profilo audio: quanta banda occupare. Nell'elenco ci sono solo i
        // profili che funzionano davvero — i digitali senza perdite e
        // l'emergenza sono progettati (PROTOCOLLO.md) ma non ancora fatti, e
        // metterli qui sarebbe promettere il vuoto.
        // Il primo della lista e' anche il predefinito, e deve essere quello che
        // funziona con TUTTI: il PCM. I profili nuovi fanno risparmiare banda
        // solo se dall'altra parte c'e' qualcuno che li sa leggere, e mandarli a
        // un telefono che aspetta PCM significa mandare audio che non arriva.
        // Il passaggio a un profilo migliore lo chiede il telefono (CTRL/HELLO o
        // CTRL/SCEGLI); qui si puo' forzare a mano, sapendo cosa si sta facendo.
        // Quanti campioni al secondo mandare. Non e' una scelta di qualita': un
        // SSB occupa 2,7 kHz e il filtro della radio non lascia passare altro,
        // quindi 12 kHz — che ne trasportano 6 — bastano per tutto quello che
        // esce davvero dal rig. Resta PCM: nessuna compressione, nessuna perdita.
        //
        // Funziona solo se chi riceve legge il campo della frequenza invece di
        // dare per scontati i 48 kHz. Se lo ignora, l'audio si sente accelerato:
        // se ne accorge subito e si torna indietro da qui.
        // Le voci sono corte e i dettagli stanno nel suggerimento: descrizioni
        // lunghe dentro una tendina allargano la finestra di duecento pixel per
        // un testo che si legge una volta sola.
        m_srate = new QComboBox;
        m_srate->addItem(QStringLiteral("48 kHz"), 48000);
        m_srate->addItem(QStringLiteral("24 kHz"), 24000);
        m_srate->addItem(QStringLiteral("12 kHz"), 12000);
        m_srate->setToolTip(QStringLiteral(
            "Quanti campioni al secondo mandare.\n"
            "48 kHz — 808 kbit/s, 364 MB l'ora: sicuro con qualunque programma\n"
            "24 kHz — 424 kbit/s, 191 MB l'ora\n"
            "12 kHz — 232 kbit/s, 104 MB l'ora: basta e avanza per un SSB,\n"
            "che di banda ne occupa 2,7 kHz.\n\n"
            "Se il telefono lo sente accelerato, non legge la frequenza\n"
            "dichiarata: torna a 48 kHz."));

        m_profile = new QComboBox;
        m_profile->addItem(QStringLiteral("PCM"), dl::PPcm48);
        m_profile->addItem(QStringLiteral("Voce (Opus)"), dl::PVoce);
        m_profile->addItem(QStringLiteral("CW (Opus)"), dl::PCw);
        m_profile->addItem(QStringLiteral("Digitali senza perdite"), dl::PDigi);
        m_profile->addItem(QStringLiteral("CW a tasto"), dl::PCwKey);
        m_profile->setToolTip(QStringLiteral(
            "PCM — compatibile con tutti, nessuna compressione\n"
            "Voce — Opus a 32 kbit/s: serve un programma aggiornato dall'altra parte\n"
            "CW — Opus a banda stretta, 20 kbit/s\n"
            "Digitali — compresso senza perdere un bit, 146 kbit/s\n"
            "CW a tasto — solo il ritmo del tasto, 2,4 kbit/s: si perde\n"
            "tutto il contesto (QSB, QRM, chi chiama fuori nota)"));

        // Quanti frame per pacchetto. Piu' se ne raggruppano, meno volte si paga
        // l'involucro IP/UDP, ma piu' latenza si aggiunge.
        m_aggr = new QComboBox;
        m_aggr->addItem(QStringLiteral("20 ms"), 1);
        m_aggr->addItem(QStringLiteral("40 ms"), 2);
        m_aggr->addItem(QStringLiteral("60 ms"), 3);
        m_aggr->setCurrentIndex(1);
        m_aggr->setToolTip(QStringLiteral(
            "Quanti frame mettere in un pacchetto: meno pacchetti, meno\n"
            "intestazioni da pagare, ma un po' più di ritardo.\n"
            "20 ms — latenza minima\n"
            "40 ms — 18% di banda in meno, ritardo impercettibile\n"
            "60 ms — 24% in meno, per reti a consumo"));

        // Colonna di sinistra: il collegamento. Sono le cose che si guardano
        // ogni volta.
        auto* form = new QFormLayout;
        form->setLabelAlignment(Qt::AlignRight | Qt::AlignVCenter);
        form->setHorizontalSpacing(10);
        form->setVerticalSpacing(7);
        form->addRow(QStringLiteral("Audio radio"), m_device);
        form->addRow(QStringLiteral("Modalità"), m_mode);
        form->addRow(QStringLiteral("Host"), m_host);
        // Porta e stazione stanno sulla stessa riga: la porta e' un numero
        // corto e da sola sprecava un'intera riga di altezza.
        auto* rigaPorta = new QHBoxLayout;
        rigaPorta->setSpacing(8);
        m_port->setFixedWidth(88);          // cinque cifre e la freccia, non di piu'
        rigaPorta->addWidget(m_port);
        auto* etSta = new QLabel(QStringLiteral("stazione"));
        etSta->setObjectName(QStringLiteral("minuscolo"));
        rigaPorta->addWidget(etSta);
        rigaPorta->addWidget(m_station, 1);
        form->addRow(QStringLiteral("Porta"), rigaPorta);

        // Le impostazioni dell'audio si toccano una volta e poi si dimenticano:
        // stanno dietro un pulsante, e la finestra parte corta.
        auto* avanForm = new QFormLayout;
        avanForm->setLabelAlignment(Qt::AlignRight | Qt::AlignVCenter);
        avanForm->setHorizontalSpacing(10);
        avanForm->setVerticalSpacing(7);
        avanForm->addRow(QStringLiteral("Profilo"), m_profile);
        avanForm->addRow(QStringLiteral("Campionamento"), m_srate);
        avanForm->addRow(QStringLiteral("Pacchetti da"), m_aggr);
        m_avanForm = avanForm;      // le righe della seriale si aggiungono dopo
        m_avanzate = new QWidget;
        m_avanzate->setLayout(avanForm);
        m_avanzate->setVisible(false);

        m_mostraAvan = new QPushButton(QStringLiteral("▸  Impostazioni avanzate"));
        m_mostraAvan->setCheckable(true);
        m_mostraAvan->setObjectName(QStringLiteral("piatto"));
        connect(m_mostraAvan, &QPushButton::toggled, this, [this](bool on) {
            m_avanzate->setVisible(on);
            m_mostraAvan->setText(on ? QStringLiteral("▾  Impostazioni avanzate")
                                     : QStringLiteral("▸  Impostazioni avanzate"));
            // La finestra si stringe da sola quando si richiude: senza questo
            // resterebbe alta come quando era aperta.
            QTimer::singleShot(0, this, [this] { resize(width(), sizeHint().height()); });
        });

        m_start = new QPushButton(QStringLiteral("Avvia"));
        m_start->setObjectName(QStringLiteral("principale"));
        m_start->setMinimumHeight(38);
        m_start->setMinimumWidth(120);
        m_level = new QProgressBar; m_level->setRange(0, 100); m_level->setTextVisible(false);
        m_level->setFixedHeight(8);
        m_status = new QLabel(QStringLiteral("fermo"));
        m_status->setObjectName(QStringLiteral("stato"));
        m_status->setWordWrap(true);
        m_stats  = new QLabel(QStringLiteral("—"));
        m_stats->setObjectName(QStringLiteral("numeri"));
        m_stats->setWordWrap(true);

        // ---- CAT: controllo del rig sulla seriale, servito al telefono ----
        // I due protocolli scritti a mano restano in cima: su un FT-991 o un
        // IC-7300 gia' collaudati non serve aggiungere uno strato. Sotto ci sono
        // tutti i modelli che conosce Hamlib, che sono il motivo per cui il
        // programma ora parla con quasi tutte le radio invece che con due marche.
        m_catModel = new QComboBox;
        m_catModel->addItem(QStringLiteral("Yaesu — comandi nativi"), -1);
        m_catModel->addItem(QStringLiteral("Icom IC-7300 — CI-V nativo"), -2);
#ifdef DECOLINK_CON_HAMLIB
        {
            QList<dl::ModelloRig> const elenco = dl::HamlibRig::modelli();
            m_catModel->insertSeparator(m_catModel->count());
            QString costruttorePrec;
            for (dl::ModelloRig const& r : elenco) {
                // I modelli dichiarati non funzionanti non si mettono in un
                // elenco da cui scegliere: farebbero solo perdere tempo.
                if (r.stato == QLatin1String("non funzionante")) continue;
                QString voce = r.costruttore + QLatin1Char(' ') + r.modello;
                if (r.stato != QLatin1String("stabile"))
                    voce += QStringLiteral("  (%1)").arg(r.stato);
                m_catModel->addItem(voce, r.numero);
            }
            m_catModel->setToolTip(
                QStringLiteral("Hamlib %1 — %2 modelli riconosciuti.\n"
                               "I primi due sono i protocolli scritti dentro Decolink;\n"
                               "gli altri passano da Hamlib, la stessa libreria che usa\n"
                               "Decodium sul desktop.")
                    .arg(dl::HamlibRig::versione()).arg(elenco.size()));
        }
#endif
        m_catModel->setCurrentIndex(1);
        m_catCivAddr = new QLineEdit(QStringLiteral("0x94"));
        m_catCivAddr->setMaximumWidth(100);
        m_catPort = new QComboBox;
        for (QSerialPortInfo const& pi : QSerialPortInfo::availablePorts())
            m_catPort->addItem(pi.portName() + "  " + pi.description());
        m_catBaud = new QComboBox;
        for (int b : {4800, 9600, 19200, 38400, 57600, 115200}) m_catBaud->addItem(QString::number(b));
        m_catBaud->setCurrentText(QStringLiteral("115200"));
        m_catDataBits = new QComboBox;
        m_catDataBits->addItem(QStringLiteral("7"), int(QSerialPort::Data7));
        m_catDataBits->addItem(QStringLiteral("8"), int(QSerialPort::Data8));
        m_catDataBits->setCurrentText(QStringLiteral("8"));
        m_catParity = new QComboBox;
        m_catParity->addItem(QStringLiteral("nessuna"), int(QSerialPort::NoParity));
        m_catParity->addItem(QStringLiteral("pari"), int(QSerialPort::EvenParity));
        m_catParity->addItem(QStringLiteral("dispari"), int(QSerialPort::OddParity));
        m_catStopBits = new QComboBox;
        m_catStopBits->addItem(QStringLiteral("1"), int(QSerialPort::OneStop));
        m_catStopBits->addItem(QStringLiteral("2"), int(QSerialPort::TwoStop));
        m_catStopBits->setCurrentIndex(1);
        m_catFlow = new QComboBox;
        m_catFlow->addItem(QStringLiteral("nessuno"), int(QSerialPort::NoFlowControl));
        m_catFlow->addItem(QStringLiteral("RTS/CTS"), int(QSerialPort::HardwareControl));
        m_catFlow->addItem(QStringLiteral("XON/XOFF"), int(QSerialPort::SoftwareControl));
        m_catTcpPort = new QSpinBox; m_catTcpPort->setRange(1, 65535); m_catTcpPort->setValue(4532);
        m_catOn = new QCheckBox(QStringLiteral("Servi il CAT al telefono"));
        m_catState = new QLabel(QStringLiteral("CAT spento"));

        m_rigOut = new QComboBox;
        m_rigOut->addItem(QStringLiteral("(nessuna: non trasmettere)"));
        for (QAudioDevice const& d : QMediaDevices::audioOutputs())
            m_rigOut->addItem(d.description());

        auto* catForm = new QFormLayout;
        catForm->setLabelAlignment(Qt::AlignRight | Qt::AlignVCenter);
        catForm->setHorizontalSpacing(10);
        catForm->setVerticalSpacing(7);
        catForm->addRow(QStringLiteral("Radio / protocollo"), m_catModel);
        m_etCiv = new QLabel(QStringLiteral("Indirizzo CI-V"));
        m_catCivAddr->setToolTip(QStringLiteral(
            "L'indirizzo con cui il rig risponde sul bus CI-V.\n"
            "IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei\n"
            "menu della radio, va scritto lo stesso valore qui."));
        catForm->addRow(m_etCiv, m_catCivAddr);
        catForm->addRow(QStringLiteral("Audio al rig"), m_rigOut);
        catForm->addRow(QStringLiteral("Porta rig"), m_catPort);
        // Velocita' e porta TCP sono due numeri corti: stanno insieme.
        auto* rigaBaud = new QHBoxLayout;
        rigaBaud->setSpacing(8);
        rigaBaud->addWidget(m_catBaud, 1);
        auto* etTcp = new QLabel(QStringLiteral("TCP"));
        etTcp->setObjectName(QStringLiteral("minuscolo"));
        rigaBaud->addWidget(etTcp);
        m_catTcpPort->setFixedWidth(78);
        rigaBaud->addWidget(m_catTcpPort);
        catForm->addRow(QStringLiteral("Velocità"), rigaBaud);
        // Bit di dati, parità, stop e handshake stanno fra le avanzate: sono i
        // parametri che si impostano una volta secondo il manuale del rig e non
        // si guardano mai piu'. In vista lasciano solo una colonna lunga il
        // doppio dell'altra.
        auto* rigaSeriale = new QHBoxLayout;
        rigaSeriale->setSpacing(8);
        auto* etDati = new QLabel(QStringLiteral("dati"));
        etDati->setObjectName(QStringLiteral("minuscolo"));
        rigaSeriale->addWidget(etDati);
        rigaSeriale->addWidget(m_catDataBits);
        auto* etPar = new QLabel(QStringLiteral("parità"));
        etPar->setObjectName(QStringLiteral("minuscolo"));
        rigaSeriale->addWidget(etPar);
        rigaSeriale->addWidget(m_catParity, 1);
        auto* etStop = new QLabel(QStringLiteral("stop"));
        etStop->setObjectName(QStringLiteral("minuscolo"));
        rigaSeriale->addWidget(etStop);
        rigaSeriale->addWidget(m_catStopBits);
        m_avanForm->addRow(QStringLiteral("Seriale"), rigaSeriale);
        m_avanForm->addRow(QStringLiteral("Handshake"), m_catFlow);

        // L'indirizzo CI-V riguarda solo gli Icom: con un Yaesu davanti e' una
        // riga che non vuol dire niente, quindi compare quando serve.
        auto sistemaCiv = [this] {
            bool const icom = (m_catModel->currentData().toInt() == -2);
            m_catCivAddr->setVisible(icom);
            m_etCiv->setVisible(icom);
        };
        connect(m_catModel, &QComboBox::currentIndexChanged, this,
                [this, sistemaCiv](int) {
                    sistemaCiv();
                    QTimer::singleShot(0, this, [this] { resize(width(), sizeHint().height()); });
                });
        QTimer::singleShot(0, this, sistemaCiv);

        // ---- accesso: chi sei, e che cosa ti lasciano fare ----
        m_authHost = new QLineEdit;
        m_authHost->setPlaceholderText(QStringLiteral("server di accesso (es. decolink.ft2.it)"));
        m_email = new QLineEdit;
        m_email->setPlaceholderText(QStringLiteral("la tua email"));
        m_password = new QLineEdit;
        m_password->setEchoMode(QLineEdit::Password);
        m_password->setPlaceholderText(QStringLiteral("password"));
        m_remember = new QCheckBox(QStringLiteral("ricorda la password"));
        m_remember->setToolTip(QStringLiteral("Viene salvata in chiaro fra le impostazioni di "
                                              "Windows: conviene solo su un computer di cui ti fidi."));
        m_login = new QPushButton(QStringLiteral("Accedi"));
        m_authState = new QLabel(QStringLiteral("non collegato"));
        m_authState->setObjectName(QStringLiteral("identita"));
        m_authState->setWordWrap(true);

        // Accesso su due righe invece di sei: email e password affiancate, il
        // server sopra. Sono tre campi che si compilano una volta.
        auto* authForm = new QFormLayout;
        authForm->setLabelAlignment(Qt::AlignRight | Qt::AlignVCenter);
        authForm->setHorizontalSpacing(10);
        authForm->setVerticalSpacing(7);
        authForm->addRow(QStringLiteral("Server"), m_authHost);
        auto* rigaCred = new QHBoxLayout;
        rigaCred->setSpacing(8);
        rigaCred->addWidget(m_email, 3);
        rigaCred->addWidget(m_password, 2);
        rigaCred->addWidget(m_login);
        authForm->addRow(QStringLiteral("Accesso"), rigaCred);
        auto* rigaRic = new QHBoxLayout;
        rigaRic->addWidget(m_remember);
        rigaRic->addStretch(1);
        rigaRic->addWidget(m_authState, 2);
        authForm->addRow(QString(), rigaRic);

        // ---- montaggio: due colonne invece di una fila unica ----
        //
        // Prima erano ventidue righe in colonna, e ogni cosa aggiunta allungava
        // la finestra. Affiancando collegamento e radio l'altezza si dimezza, e
        // le impostazioni che si toccano una volta sola stanno chiuse.

        auto* intestazione = new QLabel(QStringLiteral("DECOLINK"));
        intestazione->setObjectName(QStringLiteral("logo"));

        auto* barra = new QHBoxLayout;
        barra->addWidget(intestazione);
        barra->addStretch(1);

        auto* colSx = new QVBoxLayout;
        colSx->setSpacing(6);
        auto* tSx = new QLabel(QStringLiteral("COLLEGAMENTO"));
        tSx->setObjectName(QStringLiteral("titolo"));
        colSx->addWidget(tSx);
        colSx->addLayout(form);
        colSx->addStretch(1);

        auto* colDx = new QVBoxLayout;
        colDx->setSpacing(6);
        auto* tDx = new QLabel(QStringLiteral("RADIO E CAT"));
        tDx->setObjectName(QStringLiteral("titolo"));
        colDx->addWidget(tDx);
        colDx->addLayout(catForm);
        colDx->addWidget(m_catOn);
        colDx->addWidget(m_catState);
        colDx->addStretch(1);

        auto* colonne = new QHBoxLayout;
        colonne->setSpacing(22);
        colonne->addLayout(colSx, 1);
        auto* riga = new QFrame;
        riga->setFrameShape(QFrame::VLine);
        riga->setObjectName(QStringLiteral("divisorio"));
        colonne->addWidget(riga);
        colonne->addLayout(colDx, 1);

        // Barra di comando: il pulsante grande, il livello, e sotto lo stato.
        auto* comandi = new QHBoxLayout;
        comandi->setSpacing(12);
        comandi->addWidget(m_start);
        auto* livCol = new QVBoxLayout;
        livCol->setSpacing(3);
        auto* etLiv = new QLabel(QStringLiteral("livello audio"));
        etLiv->setObjectName(QStringLiteral("minuscolo"));
        livCol->addWidget(etLiv);
        livCol->addWidget(m_level);
        comandi->addLayout(livCol, 1);

        auto* lay = new QVBoxLayout(this);
        lay->setContentsMargins(18, 14, 18, 14);
        lay->setSpacing(10);
        lay->addLayout(barra);
        lay->addLayout(authForm);
        lay->addLayout(colonne);
        lay->addWidget(m_mostraAvan);
        lay->addWidget(m_avanzate);
        lay->addLayout(comandi);
        lay->addWidget(m_status);
        lay->addWidget(m_stats);

        // Le tendine non devono dettare la larghezza della finestra: si adattano
        // al posto che c'e', e il testo lungo lo si legge nel suggerimento.
        for (QComboBox* c : { m_device, m_mode, m_station, m_profile, m_aggr, m_srate,
                              m_catModel, m_catPort, m_catBaud, m_catDataBits, m_catParity, m_catStopBits,
                              m_catFlow, m_rigOut }) {
            c->setSizeAdjustPolicy(QComboBox::AdjustToMinimumContentsLengthWithIcon);
            c->setMinimumContentsLength(12);
            c->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
        }
        setStyleSheet(foglioStile());
        // I parametri della seriale con le etichette lunghe stanno fra le
        // avanzate, quindi la finestra non deve piu' essere larga mille pixel
        // per contenerli: si prende lo spazio che le serve davvero.
        setMinimumWidth(640);
        // Il ridimensionamento va fatto a layout finito. Chiamandolo qui si
        // misurerebbe una finestra che deve ancora sistemare i widget nascosti,
        // e resterebbe alta il doppio con un vuoto in mezzo.
        QTimer::singleShot(0, this, [this] { resize(720, sizeHint().height()); });

        connect(m_start, &QPushButton::clicked, this, [this]{ m_running ? stop() : start(); });
        connect(m_mode, &QComboBox::currentIndexChanged, this, &Client::syncFields);
        connect(m_catOn, &QCheckBox::toggled, this, &Client::toggleCat);
        connect(m_login, &QPushButton::clicked, this, [this]{ login(); });
        // Cambiare profilo a collegamento aperto rifa' i codec al volo: non c'e'
        // motivo di far staccare e riattaccare per passare da fonia a CW.
        connect(m_profile, &QComboBox::currentIndexChanged, this, [this](int){
            if (m_running) { apriCodec(); m_acc.clear(); m_daSpedire.clear(); m_tempoCampioni = 0; }
            saveSettings();
        });
        connect(m_aggr, &QComboBox::currentIndexChanged, this, [this](int){
            m_daSpedire.clear();       // i frame in attesa erano per il vecchio raggruppamento
            saveSettings();
        });
        connect(m_srate, &QComboBox::currentIndexChanged, this, [this](int){
            preparaPcm();
            m_acc.clear();
            if (m_running)
                setStatus(QStringLiteral("campionamento a %1 kHz: se il telefono lo sente "
                                         "accelerato, torna a 48")
                              .arg(campionamento() / 1000));
            saveSettings();
        });
        connect(m_password, &QLineEdit::returnPressed, this, [this]{ login(); });
        // Cambiare stazione a collegamento aperto richiede un token nuovo: il
        // vecchio vale solo per la stazione per cui e' stato emesso.
        connect(m_station, &QComboBox::activated, this, [this](int){
            if (m_token.isEmpty() || m_station->currentData().toString() == m_tokenStation) return;
            login(m_station->currentData().toString());
        });
        m_catPoll.setInterval(2000);
        connect(&m_catPoll, &QTimer::timeout, this, &Client::refreshCatState);

        // registrazione periodica alla stanza / keepalive verso casa
        m_keepAlive.setInterval(5000);
        connect(&m_keepAlive, &QTimer::timeout, this, &Client::sendRegister);
        // Rinnovo del token prima che scada: senza, una stazione lasciata
        // accesa cadrebbe da sola dopo un'ora.
        m_renew.setInterval(60000);
        connect(&m_renew, &QTimer::timeout, this, &Client::renewIfNeeded);
        m_renew.start();

        // Generatore del tono per il CW a tasto in trasmissione: deve produrre
        // audio senza interruzioni anche fra un pacchetto e il successivo,
        // altrimenti la nota si spezzerebbe ogni 100 ms.
        m_cwTx.setInterval(40);
        connect(&m_cwTx, &QTimer::timeout, this, [this] {
            if (!m_cwSuona) return;
            QVector<qint16> const a = m_sintCw.genera(kRate * 40 / 1000);
            feedTx(QByteArray(reinterpret_cast<const char*>(a.constData()),
                              int(a.size()) * 2));
            // Quando la coda e' finita si lascia sfumare e si smette: tenere il
            // generatore acceso terrebbe occupato il CODEC del rig per niente.
            if (!m_sintCw.inAttesa()) {
                if (++m_cwVuoti > 25) { m_cwSuona = false; m_cwVuoti = 0; }
            } else {
                m_cwVuoti = 0;
            }
        });
        m_cwTx.start();
        // aggiornamento contatori
        m_uiTimer.setInterval(500);
        connect(&m_uiTimer, &QTimer::timeout, this, &Client::refreshStats);
        m_uiTimer.start();

        loadSettings();
        syncFields();
        // il CAT riparte come lo si era lasciato: l'idea e' avere un solo
        // programma sul PC che fa tutto, senza doverlo riconfigurare ogni volta
        // --cat [PORTA] [BAUD] forza la porta da riga di comando (utile per le
        // prove e per l'avvio automatico); senza argomenti vale l'ultima scelta.
        QStringList const args = qApp->arguments();
        int const ci = args.indexOf(QStringLiteral("--cat"));
        if (ci >= 0 && ci + 1 < args.size() && !args.at(ci + 1).startsWith(QLatin1Char('-'))) {
            for (int i = 0; i < m_catPort->count(); ++i)
                if (m_catPort->itemText(i).startsWith(args.at(ci + 1))) { m_catPort->setCurrentIndex(i); break; }
            if (ci + 2 < args.size() && !args.at(ci + 2).startsWith(QLatin1Char('-')))
                m_catBaud->setCurrentText(args.at(ci + 2));
        }
        if (m_catWanted || ci >= 0)
            QTimer::singleShot(0, this, [this] { m_catOn->setChecked(true); });
        // --start: comincia subito a mandare l'audio, senza premere Avvia. Serve
        // per lasciarlo acceso in stazione senza doverci tornare sopra. Con il
        // relay bisogna prima avere un token, quindi l'avvio aspetta l'accesso.
        m_autoStart = args.contains(QStringLiteral("--start"));
        if (!m_email->text().isEmpty() && !m_password->text().isEmpty())
            QTimer::singleShot(200, this, [this] { login(); });
        else if (m_autoStart && m_mode->currentIndex() != ModeRelay)
            QTimer::singleShot(300, this, [this] { if (!m_running) start(); });
    }

    ~Client() override { saveSettings(); }

private slots:
    void syncFields()
    {
        int const m = m_mode->currentIndex();
        m_host->setEnabled(m != ModeListen);
        m_station->setEnabled(m == ModeRelay && m_station->count() > 0 && !m_token.isEmpty());
        switch (m) {
        case ModeLan:
            m_host->setPlaceholderText(QStringLiteral("IP del telefono sulla rete locale"));
            break;
        case ModeRelay:
            m_host->setPlaceholderText(QStringLiteral("host del relay (es. decolink.ft2.it)"));
            break;
        default:
            m_host->setPlaceholderText(QStringLiteral("(il telefono chiama questa porta)"));
            break;
        }
    }

    // Chiede al servizio di accesso un token per la stazione indicata (o per
    // l'unica disponibile, se ce n'e' una sola). Il token e' quello che il relay
    // controllera' a ogni registrazione: senza, non si entra.
    void login(const QString& stazione = QString())
    {
        QString host = m_authHost->text().trimmed();
        if (host.isEmpty()) { setAuthState(QStringLiteral("manca il server di accesso"), true); return; }
        if (m_email->text().trimmed().isEmpty() || m_password->text().isEmpty()) {
            setAuthState(QStringLiteral("servono email e password"), true); return;
        }
        if (m_authPending) return;

        // Senza schema si assume HTTPS: se l'indirizzo partisse in chiaro per
        // distrazione, la password se ne andrebbe in giro leggibile. Chi vuole
        // provare in locale scrive "http://" a mano.
        if (!host.contains(QStringLiteral("://")))
            host.prepend(QStringLiteral("https://"));

        QJsonObject corpo;
        corpo.insert(QStringLiteral("email"), m_email->text().trimmed());
        corpo.insert(QStringLiteral("password"), m_password->text());
        QString const voluta = stazione.isEmpty() ? m_wantStation : stazione;
        if (!voluta.isEmpty()) corpo.insert(QStringLiteral("station"), voluta);

        QNetworkRequest req{QUrl(host + QStringLiteral("/api/login"))};
        req.setHeader(QNetworkRequest::ContentTypeHeader, QStringLiteral("application/json"));
        req.setTransferTimeout(10000);

        m_authPending = true;
        m_login->setEnabled(false);
        setAuthState(QStringLiteral("accesso in corso…"));
        QNetworkReply* rep = m_net.post(req, QJsonDocument(corpo).toJson(QJsonDocument::Compact));
        connect(rep, &QNetworkReply::finished, this, [this, rep] {
            rep->deleteLater();
            m_authPending = false;
            m_login->setEnabled(true);
            onLoginReply(rep);
        });
    }

    void onLoginReply(QNetworkReply* rep)
    {
        QByteArray const grezzo = rep->readAll();
        QJsonObject const r = QJsonDocument::fromJson(grezzo).object();

        // Un errore di rete senza corpo JSON e' un problema di collegamento, non
        // di credenziali: distinguerli evita di far cercare all'utente una
        // password sbagliata quando in realta' il server non risponde.
        if (r.isEmpty()) {
            setAuthState(rep->error() == QNetworkReply::NoError
                             ? QStringLiteral("risposta incomprensibile dal server")
                             : QStringLiteral("server non raggiungibile: %1").arg(rep->errorString()),
                         true);
            return;
        }

        // Piu' stazioni disponibili: si popola la tendina e si lascia scegliere.
        if (!r.value(QStringLiteral("ok")).toBool()) {
            fillStations(r.value(QStringLiteral("stations")).toArray());
            QString const motivo = r.value(QStringLiteral("error")).toString(
                QStringLiteral("accesso rifiutato"));
            setAuthState(motivo, !r.value(QStringLiteral("need_station")).toBool());
            return;
        }

        m_token = r.value(QStringLiteral("token")).toString();
        m_tokenStation = r.value(QStringLiteral("station")).toString();
        m_wantStation = m_tokenStation;
        m_callsign = r.value(QStringLiteral("callsign")).toString();
        m_role = r.value(QStringLiteral("role")).toString();
        m_canTx = r.value(QStringLiteral("can_transmit")).toBool();
        int const dura = r.value(QStringLiteral("expires_in")).toInt(3600);
        m_tokenExp = QDateTime::currentSecsSinceEpoch() + dura;
        fillStations(r.value(QStringLiteral("stations")).toArray());

        // Relay e servizio di accesso stanno sulla stessa macchina: se l'host
        // del relay non e' stato scritto a mano, lo si ricava da qui invece di
        // farlo cercare all'utente.
        if (m_host->text().trimmed().isEmpty()) {
            QString h = m_authHost->text().trimmed();
            h.remove(QStringLiteral("https://")); h.remove(QStringLiteral("http://"));
            m_host->setText(h.section(QLatin1Char('/'), 0, 0).section(QLatin1Char(':'), 0, 0));
        }

        QString const ruolo = m_role == QLatin1String("own") ? QStringLiteral("titolare")
                            : m_role == QLatin1String("opr") ? QStringLiteral("operatore")
                                                             : QStringLiteral("ascoltatore");
        setAuthState(QStringLiteral("%1 — stazione %2, come %3%4")
                         .arg(m_callsign, m_tokenStation, ruolo,
                              m_canTx ? QString() : QStringLiteral(" (solo ascolto)")));
        saveSettings();

        // Se il collegamento era gia' aperto, il token nuovo entra in vigore col
        // prossimo keepalive senza interrompere l'audio. Il keepalive va
        // riacceso: puo' essere stato fermato proprio perche' il token mancava.
        if (m_running) {
            m_keepAlive.start();
            sendRegister();
        }
        else if (m_autoStart) { m_autoStart = false; QTimer::singleShot(200, this, [this]{ start(); }); }
    }

    void fillStations(const QJsonArray& elenco)
    {
        if (elenco.isEmpty()) return;
        m_station->clear();
        for (QJsonValue const& v : elenco) {
            QJsonObject const o = v.toObject();
            QString const slug = o.value(QStringLiteral("slug")).toString();
            QString const nome = o.value(QStringLiteral("name")).toString();
            m_station->addItem(nome.isEmpty() ? slug : QStringLiteral("%1 — %2").arg(slug, nome), slug);
        }
        m_station->setEnabled(true);
        int const i = m_station->findData(m_tokenStation.isEmpty() ? m_wantStation : m_tokenStation);
        if (i >= 0) m_station->setCurrentIndex(i);
    }

    // Il token dura un'ora: lo si rinnova qualche minuto prima, cosi' una
    // stazione lasciata accesa da sola non cade a meta' di un QSO.
    void renewIfNeeded()
    {
        if (m_token.isEmpty() || m_authPending) return;
        if (m_password->text().isEmpty()) return;      // niente password in memoria: si rifara' a mano
        if (QDateTime::currentSecsSinceEpoch() < m_tokenExp - 300) return;
        login(m_tokenStation);
    }

    void setAuthState(const QString& testo, bool errore = false)
    {
        m_authState->setText(testo);
        m_authState->setStyleSheet(errore ? QStringLiteral("color:#a33")
                                          : QStringLiteral("color:#666"));
    }

    void sendRegister()
    {
        if (!m_running || !m_sock) return;
        if (m_mode->currentIndex() != ModeRelay) return;

        // Senza token non si bussa. Prima si mandava comunque "gw " seguito dal
        // vuoto: il relay rispondeva "chiave di accesso mancante", il client
        // riprovava ogni cinque secondi e restava in un giro da cui non usciva
        // mai, mentre l'interfaccia diceva soltanto che era in esecuzione.
        if (m_token.isEmpty()) {
            m_keepAlive.stop();
            if (!m_password->text().isEmpty() && !m_authPending) {
                setStatus(QStringLiteral("credenziali scadute: rifaccio l'accesso"));
                login(m_tokenStation);
            } else {
                setStatus(QStringLiteral("manca l'accesso: premi Accedi, poi Avvia"));
                if (m_running) stop();
            }
            return;
        }
        // "gw": questo programma e' il lato radio della stazione. Il relay usa
        // questa parola per sapere a chi mandare l'audio da trasmettere.
        QByteArray const corpo = (QStringLiteral("gw ") + m_token).toUtf8();
        m_sock->writeDatagram(hfgwPacket(kFlagRegister, 0, corpo.constData(), corpo.size()),
                              m_dstAddr, quint16(m_port->value()));
    }

    void toggleCat(bool on)
    {
        if (!on) {
            m_catPoll.stop();
            if (m_catServer) { m_catServer->close(); m_catServer->deleteLater(); m_catServer = nullptr; }
            m_rig.close();
            m_catState->setText(QStringLiteral("CAT spento"));
            return;
        }
        QString const port = m_catPort->currentText().section(QLatin1Char(' '), 0, 0);
        if (port.isEmpty()) { m_catState->setText(QStringLiteral("nessuna porta seriale")); m_catOn->setChecked(false); return; }
        int const scelta = m_catModel->currentData().toInt();
        bool const nativoIcom = (scelta == -2);
        bool civOk = false;
        int const civAddress = m_catCivAddr->text().trimmed().toInt(&civOk, 0);
        if (nativoIcom && (!civOk || civAddress < 0 || civAddress > 255)) {
            m_catState->setText(QStringLiteral("indirizzo CI-V non valido"));
            m_catOn->setChecked(false); return;
        }

#ifdef DECOLINK_CON_HAMLIB
        if (scelta > 0) {
            // Un modello di Hamlib: la libreria sa da sola come parlargli, e i
            // parametri della porta glieli si passa come li ha scelti l'utente.
            static const QHash<int, QString> stretta{
                { int(QSerialPort::NoFlowControl), QStringLiteral("nessuno") },
                { int(QSerialPort::HardwareControl), QStringLiteral("hardware") },
                { int(QSerialPort::SoftwareControl), QStringLiteral("software") } };
            if (!m_rig.openHamlib(scelta, port, m_catBaud->currentText().toInt(),
                                  m_catDataBits->currentText().toInt(),
                                  m_catStopBits->currentText().toInt(),
                                  stretta.value(m_catFlow->currentData().toInt()))) {
                m_catState->setText(QStringLiteral("%1 non risponde: %2")
                                        .arg(port, m_rig.error()));
                m_catOn->setChecked(false);
                return;
            }
        } else
#endif
        if (!m_rig.open(port, m_catBaud->currentText().toInt(),
                        QSerialPort::DataBits(m_catDataBits->currentData().toInt()),
                        QSerialPort::Parity(m_catParity->currentData().toInt()),
                        QSerialPort::StopBits(m_catStopBits->currentData().toInt()),
                        QSerialPort::FlowControl(m_catFlow->currentData().toInt()),
                        nativoIcom, civOk ? civAddress : 0x94)) {
            m_catState->setText(QStringLiteral("%1 non si apre: %2").arg(port, m_rig.error()));
            m_catOn->setChecked(false);
            return;
        }
        // server TCP per la LAN: e' lo stesso servizio di rigctld, quindi il
        // telefono si collega come ha sempre fatto
        m_catServer = new QTcpServer(this);
        if (!m_catServer->listen(QHostAddress::Any, quint16(m_catTcpPort->value()))) {
            m_catState->setText(QStringLiteral("porta TCP %1 occupata (rigctld è già in esecuzione?)")
                                    .arg(m_catTcpPort->value()));
            m_rig.close(); m_catServer->deleteLater(); m_catServer = nullptr;
            m_catOn->setChecked(false);
            return;
        }
        connect(m_catServer, &QTcpServer::newConnection, this, [this] {
            while (QTcpSocket* c = m_catServer->nextPendingConnection()) {
                connect(c, &QTcpSocket::readyRead, this, [this, c] {
                    while (c->canReadLine()) {
                        QString const rsp = m_rig.handle(QString::fromLatin1(c->readLine()));
                        if (!rsp.isEmpty()) c->write(rsp.toLatin1());
                    }
                });
                connect(c, &QTcpSocket::disconnected, c, &QObject::deleteLater);
            }
        });
        refreshCatState();
        m_catPoll.start();
        saveSettings();
    }

    void refreshCatState()
    {
        if (!m_rig.isOpen()) return;
        qint64 const hz = m_rig.readFreq();
        QString const md = m_rig.readMode();
        m_catState->setText(hz > 0
            ? QStringLiteral("rig: %1 MHz  %2   (TCP %3, e sul canale audio)")
                  .arg(hz / 1e6, 0, 'f', 3).arg(md).arg(m_catTcpPort->value())
            : QStringLiteral("rig non risponde sulla seriale"));
    }

    void onDatagram()
    {
        while (m_sock && m_sock->hasPendingDatagrams()) {
            QByteArray dg; dg.resize(int(m_sock->pendingDatagramSize()));
            QHostAddress from; quint16 fromPort = 0;
            m_sock->readDatagram(dg.data(), dg.size(), &from, &fromPort);
            m_bytesEntrata += quint64(dg.size()) + 28;

            // Prima si prova la v3, che e' il formato con cui viaggia l'audio
            // compresso; se non e' quello si ricade sulla v2.
            if (gestisciV3(dg, from, fromPort)) continue;

            if (dg.size() < kHdrSize || std::memcmp(dg.constData(), "HFGW", 4) != 0) continue;
            const uchar* h = reinterpret_cast<const uchar*>(dg.constData());
            quint8 const flags = h[5];

            if (m_mode->currentIndex() == ModeListen) {
                // il telefono si e' fatto vivo: da qui in poi l'audio va a lui
                if (flags == kFlagRegister || flags == kFlagPing) {
                    bool const isNew = (from != m_peerAddr || fromPort != m_peerPort);
                    m_peerAddr = from; m_peerPort = fromPort;
                    m_peerSeen = QDateTime::currentMSecsSinceEpoch();
                    // ack: REGISTER->REGISTER, PING->PONG (come fa il relay)
                    m_sock->writeDatagram(hfgwPacket(flags == kFlagPing ? kFlagPong : kFlagRegister,
                                                     getU32(h + 6), nullptr, 0), from, fromPort);
                    if (isNew) setStatus(QStringLiteral("telefono connesso da %1:%2")
                                             .arg(from.toString()).arg(fromPort));
                }
            }
            // Audio che il telefono vuole trasmettere: lo si riproduce nel CODEC
            // USB del rig. Il PTT lo ha gia' alzato il telefono via CAT.
            if (flags == kFlagTxAudio) {
                // Se arriva a frequenza ridotta va riportato a 48 kHz, che e'
                // quello che vuole la scheda del rig: riprodurlo cosi' com'e'
                // lo farebbe sentire rallentato in aria.
                quint32 const hz = getU32(h + 18);
                QByteArray const corpo = dg.mid(kHdrSize);
                if (hz == 24000 || hz == 12000) {
                    if (m_txHz != int(hz)) {
                        m_txHz = int(hz);
                        m_pcmInterp = dl::Interpolatore(kRate / int(hz), hz * 0.425);
                    }
                    QVector<qint16> const su =
                        m_pcmInterp.su(reinterpret_cast<const qint16*>(corpo.constData()),
                                       corpo.size() / 2);
                    feedTx(QByteArray(reinterpret_cast<const char*>(su.constData()),
                                      int(su.size()) * 2));
                } else {
                    feedTx(corpo);
                }
                continue;
            }
            // CAT incapsulato nel canale audio: cosi' funziona anche fuori casa,
            // dove una connessione TCP al PC non sarebbe possibile.
            if (flags == kFlagCatReq) {
                QString const line = QString::fromLatin1(dg.mid(kHdrSize));
                QString const rsp = m_rig.isOpen() ? m_rig.handle(line) : QStringLiteral("RPRT -1\n");
                QByteArray const body = rsp.toLatin1();
                m_sock->writeDatagram(hfgwPacket(kFlagCatRsp, getU32(h + 6), body.constData(), body.size()),
                                      from, fromPort);
                continue;
            }
            // Il relay ci ha chiusi fuori e dice perche'. Se e' solo il token
            // scaduto lo si rinnova da soli, che e' il caso normale dopo un'ora;
            // negli altri casi si ferma tutto e si riporta il motivo, perche'
            // continuare a bussare non servirebbe a niente.
            if (flags == kFlagDenied) {
                QString const motivo = QString::fromUtf8(dg.mid(kHdrSize));
                // Qualunque rifiuto che riguardi la credenziale si prova a
                // risolvere rifacendo l'accesso, se la password e' a portata:
                // scaduta, mancante o non piu' buona, la cura e' la stessa.
                bool const eCredenziale = motivo.contains(QStringLiteral("scaduto"))
                                          || motivo.contains(QStringLiteral("chiave"))
                                          || motivo.contains(QStringLiteral("registrat"));
                if (eCredenziale && !m_password->text().isEmpty() && !m_authPending) {
                    setStatus(QStringLiteral("credenziali da rinnovare: rifaccio l'accesso"));
                    login(m_tokenStation);
                } else {
                    m_token.clear();
                    setStatus(QStringLiteral("il relay ha rifiutato il collegamento: %1").arg(motivo));
                    setAuthState(motivo, true);
                    if (m_running) stop();
                }
                continue;
            }
            if (flags == kFlagPeerUp) {
                m_peerUpVisto = true;
                setStatus(QStringLiteral("il telefono è entrato nella stanza"));
            } else if (flags == kFlagRegister) {
                setStatus(QStringLiteral("registrato sul relay come %1 (%2)")
                              .arg(m_callsign, m_tokenStation));
            }
        }
    }

    // Pacchetti del protocollo v3. Restituisce true se il datagramma era suo,
    // cosi' chi chiama sa di non doverlo trattare come v2.
    bool gestisciV3(const QByteArray& dg, const QHostAddress& from, quint16 fromPort)
    {
        quint8 tipo = 0, prof = 0, flag = 0, idSt = 0;
        quint16 seq = 0;
        quint32 tempo = 0;
        if (!dl::leggi(dg, tipo, prof, flag, idSt, seq, tempo)) return false;

        QByteArray const corpo = dg.mid(dl::kHdr);

        switch (tipo) {
        case dl::TAudioTx: {
            // Audio che il telefono vuole trasmettere, compresso: si decodifica
            // e finisce nel CODEC del rig come quello grezzo della v2.
            if (prof == dl::PPcm48) { feedTx(corpo); break; }
            if (prof == dl::PCwKey) {
                // Il telefono manda il ritmo del tasto: il tono lo si rigenera
                // qui e si manda al rig, che in SSB lo trasmette come CW.
                int nota = 700;
                QVector<dl::EventoCw> ev;
                if (dl::leggiCorpoCw(corpo, nota, ev)) {
                    m_sintCw.nota(nota);
                    m_sintCw.aggiungi(ev);
                    m_cwSuona = true;
                }
                break;
            }
            if (prof == dl::PDigi) {
                // Blocco senza perdite a 12 kHz: si decomprime, si riporta a 48
                // per la scheda del rig, e si chiede indietro quello che manca.
                QVector<qint16> const campioni = dl::decomprimi(corpo);
                if (campioni.isEmpty()) break;      // blocco tagliato o incoerente
                notaRicevuto(seq, from, fromPort);
                QVector<qint16> const su = m_interp.su(campioni.constData(), campioni.size());
                feedTx(QByteArray(reinterpret_cast<const char*>(su.constData()),
                                  int(su.size()) * 2));
                break;
            }
            if (!m_opusIn.pronto() && !m_opusIn.apri(24000, 6000)) break;
            // Un salto nella sequenza vuol dire pacchetti persi: si chiede a
            // Opus di inventare i pezzi mancanti, altrimenti si sentirebbero
            // scatti in trasmissione, che e' il posto peggiore per sentirli.
            if (m_seqTxAtteso != 0 && seq != m_seqTxAtteso) {
                int const buchi = qBound(0, int(quint16(seq - m_seqTxAtteso)), 5);
                for (int i = 0; i < buchi; ++i) feedTx(m_opusIn.decodifica(nullptr, 0));
            }
            m_seqTxAtteso = quint16(seq + 1);
            // Il pacchetto puo' contenere piu' frame: si decodificano in ordine.
            QList<QByteArray> const frame = dl::frameDaCorpo(corpo, flag & dl::FAggr);
            for (QByteArray const& f : frame)
                feedTx(m_opusIn.decodifica(f.constData(), f.size()));
            break;
        }
        case dl::TAudioRx:
            // Un gateway non ha motivo di ricevere l'audio di un altro: se
            // arriva, e' un errore di configurazione della stanza.
            break;
        case dl::TCat: {
            QString const rsp = m_rig.isOpen() ? m_rig.handle(QString::fromLatin1(corpo))
                                               : QStringLiteral("RPRT -1\n");
            QByteArray const body = rsp.toLatin1();
            m_sock->writeDatagram(dl::pacchetto(dl::TCat, prof, 0, 0, seq, tempo,
                                                body.constData(), body.size()),
                                  from, fromPort);
            break;
        }
        case dl::TCtrl:
            gestisciCtrl(corpo, from, fromPort);
            break;
        case dl::TNack:
            rimanda(corpo, from, fromPort);
            break;
        case dl::TPing:
            m_sock->writeDatagram(dl::pacchetto(dl::TPing, prof, 0, 0, seq, tempo),
                                  from, fromPort);
            break;
        default:
            break;
        }
        return true;
    }

    // Negoziazione: chi ascolta dice cosa sa fare e cosa vuole, il gateway
    // risponde con quello che offre e conferma cosa ha attivato.
    void gestisciCtrl(const QByteArray& corpo, const QHostAddress& from, quint16 fromPort)
    {
        if (corpo.isEmpty()) return;
        quint8 const sotto = quint8(corpo.at(0));

        if (sotto == dl::CHello) {
            // Il secondo byte dice cosa sa fare chi ascolta. Chi non lo manda
            // (o non dichiara CapAggr) riceve un frame per pacchetto: si perde
            // il risparmio, non il collegamento.
            quint8 const cap = corpo.size() >= 2 ? quint8(corpo.at(1)) : 0;
            m_peerHaParlato = true;      // dall'altra parte c'e' un client v3
            bool const prima = m_peerSaAggr;
            m_peerSaAggr = (cap & dl::CapAggr) != 0;
            if (m_peerSaAggr != prima) {
                m_daSpedire.clear();
                setStatus(m_peerSaAggr
                              ? QStringLiteral("il telefono legge i pacchetti raggruppati: banda ridotta")
                              : QStringLiteral("il telefono vuole un frame per pacchetto"));
            }
            char offerta[4] = { char(dl::PVoce), char(dl::PCw), char(dl::PPcm48), 0 };
            offerta[3] = char(profiloAttivo());        // quello in uso adesso
            QByteArray corpoRisp;
            corpoRisp.append(char(dl::COfferta));
            corpoRisp.append(offerta, 4);
            corpoRisp.append(char(dl::CapAggr));       // e questo e' cio' che sappiamo fare noi
            corpoRisp.append(char(aggrAttivo()));      // quanti frame stiamo raggruppando
            m_sock->writeDatagram(dl::pacchetto(dl::TCtrl, profiloAttivo(), 0, 0, 0, 0,
                                                corpoRisp.constData(), corpoRisp.size()),
                                  from, fromPort);
            return;
        }

        if (sotto == dl::CScegli && corpo.size() >= 2) {
            m_peerHaParlato = true;
            quint8 const voluto = quint8(corpo.at(1));
            int const idx = m_profile->findData(voluto);
            if (idx >= 0) {
                m_profile->setCurrentIndex(idx);        // fa scattare apriCodec()
                setStatus(QStringLiteral("profilo su richiesta del telefono: %1")
                              .arg(QString::fromLatin1(dl::nomeProfilo(voluto))));
            }
            QByteArray att;
            att.append(char(dl::CAttivo));
            att.append(char(profiloAttivo()));
            m_sock->writeDatagram(dl::pacchetto(dl::TCtrl, profiloAttivo(), 0, 0,
                                                quint16(m_seq), m_tempoCampioni,
                                                att.constData(), att.size()),
                                  from, fromPort);
            return;
        }

        // Report del ricevente: quanta perdita vede. Si dice a Opus quanta
        // ridondanza mettere e, se e' tanta, si scende di bitrate.
        if (sotto == dl::CReport && corpo.size() >= 2) {
            int const perdita = quint8(corpo.at(1));
            m_perditaVista = perdita;
            m_opusOut.perditaAttesa(perdita);
            if (perdita > 8 && m_opusOut.bitrate() > 12000)
                m_opusOut.cambiaBitrate(m_opusOut.bitrate() == 24000 ? 16000 : 12000);
            else if (perdita < 2 && m_opusOut.bitrate() < 24000)
                m_opusOut.cambiaBitrate(m_opusOut.bitrate() == 12000 ? 16000 : 24000);
        }
    }

    void onAudioReady()
    {
        if (!m_audioIo) return;
        m_acc += m_audioIo->readAll();

        // Con Opus il frame e' di 20 ms (960 campioni): e' la misura per cui il
        // codec e' pensato. In PCM si resta a 10 ms come nella v2, per non
        // cambiare il passo ai client che la parlano. Nei digitali si lavora a
        // blocchi di 40 ms, che a 12 kHz sono 480 campioni: una misura comoda per
        // il compressore e per il decodificatore che sta all'altro capo.
        quint8 const prof = profiloAttivo();

        // CW a tasto: non ci sono frame da spedire, si guarda l'audio e si
        // manda solo quando il tasto cambia stato. Se il corrispondente sta
        // zitto, sul filo non passa niente.
        if (prof == dl::PCwKey) { cwDaAudio(); return; }

        int const campioni = (prof == dl::PPcm48) ? kFrame
                           : (prof == dl::PDigi)  ? kDigiIngresso
                                                  : dl::kOpusFrame;
        int const frameBytes = campioni * 2;

        while (m_acc.size() >= frameBytes) {
            QByteArray const frame = m_acc.left(frameBytes);
            m_acc.remove(0, frameBytes);

            // livello (RMS) per la barra
            const short* s = reinterpret_cast<const short*>(frame.constData());
            double sum = 0;
            for (int i = 0; i < campioni; ++i) { double v = s[i] / 32768.0; sum += v * v; }
            m_rms = 0.8 * m_rms + 0.2 * std::sqrt(sum / campioni);

            if (!targetReady()) continue;      // nessun destinatario: non spedisco

            QByteArray pkt;
            if (prof == dl::PPcm48) {
                int const hz = campionamento();
                if (hz >= kRate) {
                    pkt = hfgwPacket(kFlagAudio, m_seq++, frame.constData(), frame.size(), kRate);
                } else {
                    // Si filtra e si riduce: senza il filtro, tutto quello sopra
                    // la nuova meta' frequenza tornerebbe ripiegato dentro la
                    // banda utile, e sarebbero righe false proprio dove si
                    // ascolta. La frequenza vera va nell'intestazione.
                    QVector<qint16> const giu =
                        m_pcmDecim.giu(reinterpret_cast<const qint16*>(frame.constData()), campioni);
                    if (giu.isEmpty()) continue;
                    pkt = hfgwPacket(kFlagAudio, m_seq++,
                                     reinterpret_cast<const char*>(giu.constData()),
                                     int(giu.size()) * 2, hz);
                }
            } else if (prof == dl::PDigi) {
                // 48 -> 12 kHz filtrando come si deve, poi compressione senza
                // perdite: il decodificatore riceve esattamente i campioni che
                // sono usciti dal rig, non una loro approssimazione.
                QVector<qint16> const giu =
                    m_decim.giu(reinterpret_cast<const qint16*>(frame.constData()), campioni);
                if (giu.isEmpty()) continue;
                QByteArray const blocco = dl::comprimi(giu.constData(), giu.size());
                if (blocco.isEmpty()) continue;
                quint16 const s = quint16(m_seq++);
                pkt = dl::pacchetto(dl::TAudioRx, prof, 0, 0, s, m_tempoCampioni,
                                    blocco.constData(), blocco.size());
                m_tempoCampioni += quint32(giu.size());
                // Si tiene da parte per poterlo rimandare: nei digitali la
                // latenza non conta (FT8 decodifica a fette di 15 secondi) e un
                // buco nell'audio rovinerebbe l'intera fetta.
                ricorda(s, pkt);
                m_grezziDigi += quint64(giu.size()) * 2;
                m_compressiDigi += quint64(blocco.size());
            } else {
                QByteArray const compresso =
                    m_opusOut.codifica(reinterpret_cast<const qint16*>(frame.constData()));
                if (compresso.isEmpty()) continue;      // meglio saltare che spedire spazzatura
                m_tempoCampioni += quint32(campioni);

                // Si accumula finche' non si e' raggiunto il raggruppamento
                // scelto, poi si spedisce tutto in un datagramma.
                m_daSpedire.append(compresso);
                if (m_daSpedire.size() < aggrAttivo()) continue;

                if (m_daSpedire.size() == 1) {
                    // Un frame solo: si manda nel formato semplice, che i client
                    // che non conoscono FAggr sanno leggere.
                    QByteArray const& f = m_daSpedire.first();
                    pkt = dl::pacchetto(dl::TAudioRx, prof, dl::FFec, 0, quint16(m_seq++),
                                        m_tempoCampioni, f.constData(), f.size());
                } else {
                    QByteArray const corpo = dl::corpoAggregato(m_daSpedire);
                    pkt = dl::pacchetto(dl::TAudioRx, prof, dl::FFec | dl::FAggr, 0,
                                        quint16(m_seq++), m_tempoCampioni,
                                        corpo.constData(), corpo.size());
                }
                m_daSpedire.clear();
            }
            m_sock->writeDatagram(pkt, m_dstAddr, m_dstPort);
            ++m_sent;
            m_bytesUscita += quint64(pkt.size()) + 28;   // +28: intestazioni IP e UDP, che si pagano
        }
    }

    // Il profilo che si sta davvero usando: quello scelto, ma solo se il codec
    // e' in piedi. Se Opus non parte si torna al PCM invece di restare muti.
    quint8 profiloAttivo() const
    {
        quint8 const scelto = quint8(m_profile->currentData().toUInt());
        if (scelto == dl::PPcm48 || scelto == dl::PDigi || scelto == dl::PCwKey) return scelto;
        return m_opusOut.pronto() ? scelto : dl::PPcm48;
    }

    // Quanti frame raggruppare adesso: quello scelto, ma uno solo se dall'altra
    // parte c'e' qualcuno che non ha dichiarato di saper leggere i pacchetti
    // aggregati. Risparmiare banda mandando un formato incomprensibile
    // significa non mandare niente.
    int aggrAttivo() const
    {
        if (!m_peerSaAggr) return 1;
        if (profiloAttivo() == dl::PDigi) return 1;   // qui il blocco e' gia' da 40 ms
        return qBound(1, m_aggr->currentData().toInt(), dl::kMaxAggr);
    }

    // Campioni al secondo da mandare. Vale solo per il PCM: gli altri profili
    // hanno la loro frequenza, decisa dal codec.
    int campionamento() const
    {
        int const hz = m_srate->currentData().toInt();
        return (hz == 24000 || hz == 12000) ? hz : kRate;
    }

    // Rifà il filtro quando cambia la frequenza scelta: il rapporto di riduzione
    // e il taglio dipendono da quella, e tenersi il filtro di prima vorrebbe dire
    // filtrare alla frequenza sbagliata.
    void preparaPcm()
    {
        int const hz = campionamento();
        if (hz >= kRate) return;
        // Taglio all'85% della nuova metà frequenza: il margine serve perché la
        // banda di transizione di un filtro vero non è verticale.
        m_pcmDecim = dl::Decimatore(kRate / hz, hz * 0.425);
    }

    // ---- CW a tasto ----

    // Guarda l'audio della radio, ne ricava gli istanti del tasto e li spedisce.
    // Gli eventi si raggruppano per 100 ms: mandarne uno per pacchetto vorrebbe
    // dire pagare 38 byte di involucro per 2 byte di contenuto, e a questi
    // livelli di banda l'involucro e' tutto. Cento millisecondi di ritardo su
    // un punto che dura sessanta non spostano il ritmo di chi ascolta.
    void cwDaAudio()
    {
        int const campioni = m_acc.size() / 2;
        if (campioni <= 0) return;
        QVector<dl::EventoCw> const ev =
            m_rilCw.mangia(reinterpret_cast<const qint16*>(m_acc.constData()), campioni);
        m_acc.clear();

        // livello per la barra, dall'energia della nota trovata
        m_rms = 0.7 * m_rms + 0.3 * qMin(1.0, m_rilCw.energia() * 4.0);

        for (dl::EventoCw const& e : ev) m_cwDaSpedire.append(e);
        if (m_cwDaSpedire.isEmpty()) return;
        if (!targetReady()) { m_cwDaSpedire.clear(); return; }

        qint64 const ora = QDateTime::currentMSecsSinceEpoch();
        if (m_cwUltimoInvio != 0 && ora - m_cwUltimoInvio < 100 && m_cwDaSpedire.size() < 32)
            return;
        m_cwUltimoInvio = ora;

        QByteArray const corpo = dl::corpoCw(m_rilCw.notaHz(), m_cwDaSpedire);
        QByteArray const pkt = dl::pacchetto(dl::TAudioRx, dl::PCwKey, 0, 0,
                                             quint16(m_seq++), m_tempoCampioni,
                                             corpo.constData(), corpo.size());
        m_cwEventi += quint64(m_cwDaSpedire.size());
        m_cwDaSpedire.clear();
        m_sock->writeDatagram(pkt, m_dstAddr, m_dstPort);
        ++m_sent;
        m_bytesUscita += quint64(pkt.size()) + 28;
    }

    // ---- ritrasmissione, solo per il profilo dei digitali ----

    // Tiene un pacchetto a portata di mano per qualche secondo, in caso venga
    // richiesto di nuovo. La finestra e' corta di proposito: oltre i 3 secondi
    // il pezzo non servirebbe piu' a nessuno, perche' la fetta di FT8 a cui
    // apparteneva e' già stata decodificata.
    void ricorda(quint16 seq, const QByteArray& pkt)
    {
        m_finestra.insert(seq, { pkt, QDateTime::currentMSecsSinceEpoch() });
        if (m_finestra.size() > 200) {
            qint64 const ora = QDateTime::currentMSecsSinceEpoch();
            for (auto it = m_finestra.begin(); it != m_finestra.end();)
                it = (ora - it->quando > 3000) ? m_finestra.erase(it) : ++it;
        }
    }

    // Qualcuno chiede indietro dei pacchetti: si rimandano quelli che si hanno
    // ancora. Chi arriva tardi non riceve nulla e lo scoprira' dal silenzio: e'
    // meglio che tenere in memoria mezz'ora di audio per un ripescaggio inutile.
    void rimanda(const QByteArray& corpo, const QHostAddress& a, quint16 p)
    {
        if (corpo.size() < 2 || !m_sock) return;
        int const quanti = int(uchar(corpo.at(1)));
        int rimandati = 0, mancanti = 0;
        for (int i = 0; i < quanti && 2 + 2 * i + 1 < corpo.size(); ++i) {
            quint16 const s = quint16((uchar(corpo.at(2 + 2 * i)) << 8)
                                      | uchar(corpo.at(3 + 2 * i)));
            auto const it = m_finestra.constFind(s);
            if (it != m_finestra.constEnd()) {
                m_sock->writeDatagram(it->pkt, a, p);
                m_bytesUscita += quint64(it->pkt.size()) + 28;
                ++rimandati;
            } else {
                ++mancanti;
            }
        }
        m_rimandati += quint64(rimandati);
        if (mancanti > 0) m_troppoTardi += quint64(mancanti);
    }

    // Dall'altro lato: si tiene il conto di quello che arriva e si chiede
    // indietro quello che manca. Si aspetta un momento prima di chiedere, perche'
    // su internet i pacchetti si scambiano d'ordine e un ritardatario non e' un
    // pacchetto perso.
    void notaRicevuto(quint16 seq, const QHostAddress& a, quint16 p)
    {
        qint64 const ora = QDateTime::currentMSecsSinceEpoch();
        m_arrivati.insert(seq, ora);
        if (m_arrivati.size() > 400) {
            for (auto it = m_arrivati.begin(); it != m_arrivati.end();)
                it = (ora - it.value() > 4000) ? m_arrivati.erase(it) : ++it;
        }

        if (m_ultimoRx == 0) { m_ultimoRx = seq; return; }
        quint16 const atteso = quint16(m_ultimoRx + 1);
        if (seq == atteso) { m_ultimoRx = seq; return; }
        if (qint16(seq - m_ultimoRx) <= 0) return;      // ritardatario, non un buco

        // C'e' un salto: si segnano le sequenze che non si sono viste.
        QList<quint16> mancano;
        for (quint16 s = atteso; s != seq && mancano.size() < 32; ++s)
            if (!m_arrivati.contains(s)) mancano.append(s);
        m_ultimoRx = seq;
        if (mancano.isEmpty() || !m_sock) return;

        QByteArray corpo;
        corpo.append(char(dl::CReport));      // riusa lo spazio dei sottotipi
        corpo.append(char(mancano.size()));
        for (quint16 s : mancano) {
            corpo.append(char((s >> 8) & 0xFF));
            corpo.append(char(s & 0xFF));
        }
        m_sock->writeDatagram(dl::pacchetto(dl::TNack, dl::PDigi, 0, 0, seq, 0,
                                            corpo.constData(), corpo.size()), a, p);
        m_chiesti += quint64(mancano.size());
    }

    // Apre la scheda del rig alla prima richiesta e la chiude quando il telefono
    // smette di mandare: tenerla aperta a vuoto terrebbe occupato il CODEC.
    void feedTx(const QByteArray& pcm)
    {
        if (m_rigOut->currentIndex() <= 0 || pcm.isEmpty()) return;
        if (!m_txSink) {
            QList<QAudioDevice> const outs = QMediaDevices::audioOutputs();
            int const idx = m_rigOut->currentIndex() - 1;
            if (idx < 0 || idx >= outs.size()) return;
            QAudioFormat fmt;
            fmt.setSampleRate(kRate); fmt.setChannelCount(1); fmt.setSampleFormat(QAudioFormat::Int16);
            if (!outs[idx].isFormatSupported(fmt)) {
                setStatus(QStringLiteral("%1 non supporta 48 kHz mono 16 bit").arg(outs[idx].description()));
                return;
            }
            m_txQueue = new TxQueue(this);
            m_txQueue->open(QIODevice::ReadOnly);
            m_txSink = new QAudioSink(outs[idx], fmt, this);
            m_txSink->setBufferSize(kRate * 2 / 10);      // ~100 ms
            m_txSink->start(m_txQueue);
            setStatus(QStringLiteral("trasmissione dal telefono in corso"));
        }
        m_txQueue->push(pcm);
    }

    void closeTxIfIdle()
    {
        if (!m_txSink || !m_txQueue) return;
        if (!m_txQueue->idle(1200)) return;               // ancora audio in arrivo
        m_txSink->stop(); m_txSink->deleteLater(); m_txSink = nullptr;
        m_txQueue->close(); m_txQueue->deleteLater(); m_txQueue = nullptr;
        setStatus(QStringLiteral("trasmissione finita"));
    }

    void refreshStats()
    {
        closeTxIfIdle();
        m_level->setValue(int(qMin(1.0, m_rms * 4.0) * 100));
        if (!m_running) { m_stats->setText(QStringLiteral("—")); return; }

        // La banda si misura, non si stima: e' il numero che dice se il profilo
        // sta facendo il suo lavoro, e comprende le intestazioni IP e UDP che si
        // pagano su ogni pacchetto.
        qint64 const ms = qMax<qint64>(1, m_bandaTimer.elapsed());
        double const kbps = double(m_bytesUscita) * 8.0 / double(ms);
        quint8 const prof = profiloAttivo();
        QString testo = QStringLiteral("%1 — in uscita %2 kbit/s (%3 MB l'ora)   pacchetti %4")
                            .arg(QString::fromLatin1(dl::nomeProfilo(prof)))
                            .arg(kbps, 0, 'f', 1)
                            .arg(kbps * 450.0 / 1000.0, 0, 'f', 0)
                            .arg(m_sent);
        if (prof == dl::PCwKey) {
            testo += QStringLiteral("   nota %1 Hz   tasto %2   eventi %3")
                         .arg(m_rilCw.notaHz())
                         .arg(m_rilCw.premuto() ? QStringLiteral("giù") : QStringLiteral("su"))
                         .arg(m_cwEventi);
        } else if (prof == dl::PDigi) {
            if (m_grezziDigi > 0)
                testo += QStringLiteral("   compresso al %1% del grezzo")
                             .arg(double(m_compressiDigi) * 100.0 / double(m_grezziDigi), 0, 'f', 0);
            if (m_chiesti > 0 || m_rimandati > 0)
                testo += QStringLiteral("   rimandati %1, chiesti %2")
                             .arg(m_rimandati).arg(m_chiesti);
            if (m_troppoTardi > 0)
                testo += QStringLiteral("   %1 fuori finestra").arg(m_troppoTardi);
        } else if (prof == dl::PPcm48) {
            testo += QStringLiteral("   %1 kHz").arg(campionamento() / 1000);
            if (campionamento() < kRate)
                testo += QStringLiteral(" (banda audio %1 kHz)").arg(campionamento() / 2000);
        } else {
            testo += QStringLiteral("   Opus %1 kbit/s").arg(m_opusOut.bitrate() / 1000);
            int const n = aggrAttivo();
            testo += (n > 1) ? QStringLiteral("   pacchetti da %1 ms").arg(n * 20)
                             : QStringLiteral("   un frame per pacchetto");
        }
        if (m_perditaVista > 0)
            testo += QStringLiteral("   perdita segnalata %1%").arg(m_perditaVista);
        m_stats->setText(testo);

        // I due modi in cui si manda audio senza che arrivi a nessuno, ed e'
        // giusto dirlo invece di lasciar guardare la barra del livello.
        if (m_mode->currentIndex() == ModeRelay && !m_peerUpVisto) {
            setStatus(QStringLiteral("registrato, ma nella stazione non c'è nessun altro: "
                                     "il telefono non è ancora entrato"));
        } else if (prof != dl::PPcm48 && !m_peerHaParlato) {
            setStatus(QStringLiteral("attenzione: profilo %1, ma il telefono non ha confermato "
                                     "di saperlo leggere — se non senti niente, passa a PCM 48 kHz")
                          .arg(QString::fromLatin1(dl::nomeProfilo(prof))));
        }
    }

private:
    bool targetReady()
    {
        if (m_mode->currentIndex() == ModeListen) {
            // manda solo se il telefono si e' fatto vivo di recente
            if (m_peerPort == 0) return false;
            if (QDateTime::currentMSecsSinceEpoch() - m_peerSeen > 20000) {
                m_peerPort = 0;
                setStatus(QStringLiteral("telefono non più raggiungibile — attendo che richiami"));
                return false;
            }
            m_dstAddr = m_peerAddr; m_dstPort = m_peerPort;
            return true;
        }
        return !m_dstAddr.isNull();
    }

    void setStatus(const QString& s) { m_status->setText(s); }

    // Prepara i codec per il profilo scelto. Due istanze separate, una per
    // verso: la radio manda con la banda del profilo, il telefono puo' mandare
    // con la sua, e non devono pestarsi lo stato.
    void apriCodec()
    {
        quint8 const scelto = quint8(m_profile->currentData().toUInt());

        // I digitali non usano Opus: hanno il loro compressore senza perdite. Si
        // azzerano i filtri, altrimenti si porterebbero dietro la coda del
        // profilo precedente.
        if (scelto == dl::PDigi) {
            m_opusOut.chiudi(); m_opusIn.chiudi();
            m_decim.azzera(); m_interp.azzera();
            m_finestra.clear(); m_arrivati.clear(); m_ultimoRx = 0;
            m_grezziDigi = m_compressiDigi = 0;
            return;
        }
        if (scelto == dl::PCwKey) {
            m_opusOut.chiudi(); m_opusIn.chiudi();
            m_rilCw.azzera(); m_sintCw.azzera();
            m_cwDaSpedire.clear(); m_cwEventi = 0; m_cwUltimoInvio = 0;
            return;
        }
        if (scelto == dl::PPcm48) { m_opusOut.chiudi(); m_opusIn.chiudi(); return; }

        // CW: 4 kHz bastano e avanzano per una nota da 700 Hz e per sentire chi
        // chiama poco fuori frequenza. Fonia: 6 kHz, che coprono un SSB da 2,7
        // con margine per il fruscio che dice com'e' la banda.
        int const bitrate = (scelto == dl::PCw) ? 12000 : 24000;
        int const banda   = (scelto == dl::PCw) ?  4000 :  6000;
        if (!m_opusOut.apri(bitrate, banda) || !m_opusIn.apri(bitrate, banda)) {
            setStatus(QStringLiteral("Opus non si avvia (%1): resto sul PCM")
                          .arg(m_opusOut.errore()));
            m_opusOut.chiudi(); m_opusIn.chiudi();
        }
    }

    void start()
    {
        int const m = m_mode->currentIndex();
        m_dstPort = quint16(m_port->value());
        m_dstAddr = QHostAddress();
        m_peerPort = 0;
        m_seq = 0; m_sent = 0; m_acc.clear();

        if (m != ModeListen) {
            QString const host = m_host->text().trimmed();
            if (host.isEmpty()) { setStatus(QStringLiteral("manca l'host di destinazione")); return; }
            QHostInfo const info = QHostInfo::fromName(host);   // risolve anche i nomi DynDNS
            if (info.addresses().isEmpty()) {
                setStatus(QStringLiteral("nome non risolto: %1").arg(host)); return;
            }
            m_dstAddr = info.addresses().first();
        }
        if (m == ModeRelay && m_token.isEmpty()) {
            setStatus(QStringLiteral("accedi prima: il relay non accetta collegamenti senza credenziali"));
            return;
        }

        m_sock = new QUdpSocket(this);
        // in ascolto: mi lego alla porta; negli altri casi porta effimera
        bool const bound = (m == ModeListen)
                               ? m_sock->bind(QHostAddress::AnyIPv4, m_dstPort)
                               : m_sock->bind();
        if (!bound) {
            setStatus(QStringLiteral("porta %1 non disponibile").arg(m_dstPort));
            delete m_sock; m_sock = nullptr; return;
        }
        connect(m_sock, &QUdpSocket::readyRead, this, &Client::onDatagram);

        apriCodec();
        preparaPcm();
        m_bytesUscita = m_bytesEntrata = 0;
        m_tempoCampioni = 0;
        m_bandaTimer.restart();

        // audio dalla radio
        QList<QAudioDevice> const ins = QMediaDevices::audioInputs();
        int const idx = m_device->currentIndex();
        if (idx < 0 || idx >= ins.size()) { setStatus(QStringLiteral("nessun ingresso audio")); return; }
        QAudioFormat fmt;
        fmt.setSampleRate(kRate); fmt.setChannelCount(1); fmt.setSampleFormat(QAudioFormat::Int16);
        if (!ins[idx].isFormatSupported(fmt)) {
            setStatus(QStringLiteral("%1 non supporta 48 kHz mono 16 bit").arg(ins[idx].description()));
            return;
        }
        m_audio = new QAudioSource(ins[idx], fmt, this);
        m_audioIo = m_audio->start();
        if (!m_audioIo) { setStatus(QStringLiteral("impossibile aprire l'ingresso audio")); return; }
        connect(m_audioIo, &QIODevice::readyRead, this, &Client::onAudioReady);

        m_running = true;
        m_start->setText(QStringLiteral("Ferma"));
        setFieldsEnabled(false);
        if (m == ModeRelay) { sendRegister(); m_keepAlive.start(); }
        setStatus(m == ModeListen
                      ? QStringLiteral("in ascolto sulla porta %1 — attendo il telefono").arg(m_dstPort)
                      : QStringLiteral("invio a %1:%2").arg(m_dstAddr.toString()).arg(m_dstPort));
        saveSettings();
    }

    void stop()
    {
        m_keepAlive.stop();
        if (m_audio) { m_audio->stop(); m_audio->deleteLater(); m_audio = nullptr; m_audioIo = nullptr; }
        if (m_sock)  { m_sock->close(); m_sock->deleteLater(); m_sock = nullptr; }
        m_running = false; m_rms = 0;
        m_start->setText(QStringLiteral("Avvia"));
        setFieldsEnabled(true);
        setStatus(QStringLiteral("fermo"));
    }

    void setFieldsEnabled(bool on)
    {
        m_device->setEnabled(on); m_mode->setEnabled(on); m_port->setEnabled(on);
        if (on) syncFields(); else { m_host->setEnabled(false); m_station->setEnabled(false); }
    }

    void loadSettings()
    {
        QSettings s(QStringLiteral("it.ft2"), QStringLiteral("Decolink"));
        m_mode->setCurrentIndex(s.value(QStringLiteral("mode"), 0).toInt());
        m_host->setText(s.value(QStringLiteral("host")).toString());
        m_port->setValue(s.value(QStringLiteral("port"), 5555).toInt());
        m_authHost->setText(s.value(QStringLiteral("authHost"),
                                    QStringLiteral("decolink.ft2.it")).toString());
        m_email->setText(s.value(QStringLiteral("email")).toString());
        m_wantStation = s.value(QStringLiteral("station")).toString();
        // La password torna solo se l'utente ha chiesto di ricordarla: serve a
        // chi lascia la stazione accesa e la vuole vedere ripartire da sola dopo
        // un riavvio, senza qualcuno davanti alla tastiera.
        m_remember->setChecked(s.value(QStringLiteral("remember"), false).toBool());
        if (m_remember->isChecked())
            m_password->setText(s.value(QStringLiteral("password")).toString());
        int const pi = m_profile->findData(s.value(QStringLiteral("profile"), dl::PPcm48).toUInt());
        if (pi >= 0) m_profile->setCurrentIndex(pi);

        // Le versioni uscite il 30 luglio 2026 partivano con un profilo compresso
        // come predefinito, e chi se l'e' ritrovato salvato non riceveva piu'
        // niente: il telefono aspetta PCM e quello che arrivava non lo sapeva
        // leggere. Si riporta a PCM una volta sola, lasciando poi liberi di
        // scegliere. Un'impostazione salvata che rompe il collegamento va
        // corretta, non conservata per rispetto.
        if (!s.value(QStringLiteral("profiloRivisto"), false).toBool()) {
            if (quint8(m_profile->currentData().toUInt()) != dl::PPcm48) {
                m_profile->setCurrentIndex(0);      // PCM 48 kHz
                QTimer::singleShot(1200, this, [this] {
                    setStatus(QStringLiteral("profilo riportato a PCM 48 kHz: i profili compressi "
                                             "richiedono un telefono aggiornato"));
                });
            }
            QSettings w(QStringLiteral("it.ft2"), QStringLiteral("Decolink"));
            w.setValue(QStringLiteral("profiloRivisto"), true);
        }
        int const ai = m_aggr->findData(s.value(QStringLiteral("aggr"), 2).toInt());
        if (ai >= 0) m_aggr->setCurrentIndex(ai);
        // Predefinito 48 kHz: e' quello che funziona con qualunque programma
        // dall'altra parte. Il risparmio si sceglie, non si subisce.
        int const si = m_srate->findData(s.value(QStringLiteral("srate"), 48000).toInt());
        if (si >= 0) m_srate->setCurrentIndex(si);
        m_catModel->setCurrentIndex(s.value(QStringLiteral("catModel"), 1).toInt());
        m_catCivAddr->setText(s.value(QStringLiteral("catCivAddr"), QStringLiteral("0x94")).toString());
        m_catBaud->setCurrentText(s.value(QStringLiteral("catBaud"), QStringLiteral("115200")).toString());
        m_catDataBits->setCurrentText(s.value(QStringLiteral("catDataBits"), QStringLiteral("8")).toString());
        m_catParity->setCurrentIndex(s.value(QStringLiteral("catParity"), 0).toInt());
        m_catStopBits->setCurrentIndex(s.value(QStringLiteral("catStopBits"), 0).toInt());
        m_catFlow->setCurrentIndex(s.value(QStringLiteral("catFlow"), 0).toInt());
        m_catTcpPort->setValue(s.value(QStringLiteral("catTcpPort"), 4532).toInt());
        QString const cp = s.value(QStringLiteral("catPort")).toString();
        for (int i = 0; i < m_catPort->count(); ++i)
            if (m_catPort->itemText(i).startsWith(cp) && !cp.isEmpty()) { m_catPort->setCurrentIndex(i); break; }
        m_catWanted = s.value(QStringLiteral("catOn"), false).toBool();
        int const ro = m_rigOut->findText(s.value(QStringLiteral("rigOut")).toString());
        if (ro >= 0) m_rigOut->setCurrentIndex(ro);
        QString const dev = s.value(QStringLiteral("device")).toString();
        int const i = m_device->findText(dev);
        if (i >= 0) m_device->setCurrentIndex(i);
    }

    void saveSettings()
    {
        QSettings s(QStringLiteral("it.ft2"), QStringLiteral("Decolink"));
        s.setValue(QStringLiteral("mode"), m_mode->currentIndex());
        s.setValue(QStringLiteral("host"), m_host->text());
        s.setValue(QStringLiteral("port"), m_port->value());
        s.setValue(QStringLiteral("authHost"), m_authHost->text());
        s.setValue(QStringLiteral("email"), m_email->text());
        s.setValue(QStringLiteral("station"), m_wantStation);
        s.setValue(QStringLiteral("remember"), m_remember->isChecked());
        s.setValue(QStringLiteral("profile"), m_profile->currentData().toUInt());
        s.setValue(QStringLiteral("aggr"), m_aggr->currentData().toInt());
        s.setValue(QStringLiteral("srate"), m_srate->currentData().toInt());
        if (m_remember->isChecked())
            s.setValue(QStringLiteral("password"), m_password->text());
        else
            s.remove(QStringLiteral("password"));
        // Il token non si salva: dura un'ora e si riottiene al volo. Scriverlo
        // sul disco allungherebbe soltanto la vita a una credenziale rubata.
        s.setValue(QStringLiteral("device"), m_device->currentText());
        s.setValue(QStringLiteral("catPort"), m_catPort->currentText().section(QLatin1Char(' '), 0, 0));
        s.setValue(QStringLiteral("catModel"), m_catModel->currentIndex());
        s.setValue(QStringLiteral("catCivAddr"), m_catCivAddr->text());
        s.setValue(QStringLiteral("catBaud"), m_catBaud->currentText());
        s.setValue(QStringLiteral("catDataBits"), m_catDataBits->currentText());
        s.setValue(QStringLiteral("catParity"), m_catParity->currentIndex());
        s.setValue(QStringLiteral("catStopBits"), m_catStopBits->currentIndex());
        s.setValue(QStringLiteral("catFlow"), m_catFlow->currentIndex());
        s.setValue(QStringLiteral("catTcpPort"), m_catTcpPort->value());
        s.setValue(QStringLiteral("catOn"), m_catOn->isChecked());
        s.setValue(QStringLiteral("rigOut"), m_rigOut->currentText());
    }

    QComboBox *m_device, *m_mode, *m_station, *m_profile, *m_aggr, *m_srate;
    QWidget* m_avanzate;          // le impostazioni audio, chiuse di default
    QFormLayout* m_avanForm;      // dove finiscono i parametri della seriale
    QLabel* m_etCiv;              // etichetta dell'indirizzo CI-V
    QPushButton* m_mostraAvan;
    dl::Decimatore m_pcmDecim;      // riduce il PCM alla frequenza scelta
    dl::Interpolatore m_pcmInterp;  // e riporta a 48 kHz quello che arriva
    QLineEdit* m_host;
    QSpinBox* m_port;
    QPushButton* m_start;
    QProgressBar* m_level;
    QLabel *m_status, *m_stats;

    // accesso al gateway
    QLineEdit *m_authHost, *m_email, *m_password;
    QCheckBox* m_remember;
    QPushButton* m_login;
    QLabel* m_authState;
    QNetworkAccessManager m_net;
    QString m_token, m_tokenStation, m_wantStation, m_callsign, m_role;
    qint64 m_tokenExp {0};
    bool m_canTx {false}, m_authPending {false}, m_autoStart {false};
    QTimer m_renew;

    QComboBox *m_catModel, *m_catPort, *m_catBaud, *m_catDataBits, *m_catParity, *m_catStopBits, *m_catFlow;
    QLineEdit* m_catCivAddr;
    QSpinBox* m_catTcpPort;
    QCheckBox* m_catOn;
    QLabel* m_catState;
    CatRig m_rig;
    bool m_catWanted {false};
    QTcpServer* m_catServer {nullptr};
    QTimer m_catPoll;

    QComboBox* m_rigOut;
    QAudioSink* m_txSink {nullptr};
    TxQueue* m_txQueue {nullptr};

    QAudioSource* m_audio {nullptr};
    QIODevice* m_audioIo {nullptr};
    QUdpSocket* m_sock {nullptr};
    QByteArray m_acc;

    // profilo audio (protocollo v3)
    dl::OpusVoce m_opusOut, m_opusIn;   // una per verso: RX della radio, TX dal telefono
    quint32 m_tempoCampioni {0};
    quint64 m_bytesUscita {0}, m_bytesEntrata {0};
    QElapsedTimer m_bandaTimer;
    quint16 m_seqTxAtteso {0};
    int m_perditaVista {0};
    int m_txHz {48000};      // frequenza dichiarata da chi ci manda l'audio
    QList<QByteArray> m_daSpedire;   // frame in attesa di partire insieme

    // profilo dei digitali: conversione di frequenza e ritrasmissione
    dl::Decimatore m_decim;
    dl::Interpolatore m_interp;
    struct InSospeso { QByteArray pkt; qint64 quando; };
    QMap<quint16, InSospeso> m_finestra;   // spediti, a portata di mano per 3 s
    QMap<quint16, qint64> m_arrivati;      // ricevuti, per accorgersi dei buchi
    quint16 m_ultimoRx {0};
    quint64 m_rimandati {0}, m_chiesti {0}, m_troppoTardi {0};
    quint64 m_grezziDigi {0}, m_compressiDigi {0};

    // CW a tasto
    dl::RilevatoreCw m_rilCw;
    dl::SintetizzatoreCw m_sintCw;
    QVector<dl::EventoCw> m_cwDaSpedire;
    qint64 m_cwUltimoInvio {0};
    quint64 m_cwEventi {0};
    bool m_cwSuona {false};
    int m_cwVuoti {0};
    QTimer m_cwTx;
    // Si parte dal presupposto che l'altro capo non sappia leggere i pacchetti
    // raggruppati, e lo si scopre dal suo HELLO: meglio consumare piu' banda che
    // mandare a un client vecchio un formato che non capisce.
    bool m_peerSaAggr {false};
    // Se dall'altra parte non si e' mai fatto vivo nessuno con la v3, mandare un
    // profilo compresso e' mandare audio nel vuoto: l'interfaccia deve dirlo,
    // altrimenti si vede la barra del livello muoversi e si pensa che vada tutto
    // bene mentre il telefono non riceve niente.
    bool m_peerHaParlato {false};
    bool m_peerUpVisto {false};

    QHostAddress m_dstAddr, m_peerAddr;
    quint16 m_dstPort {5555}, m_peerPort {0};
    qint64 m_peerSeen {0};
    quint32 m_seq {0};
    quint64 m_sent {0};
    double m_rms {0};
    bool m_running {false};
    QTimer m_keepAlive, m_uiTimer;
};

#include "main.moc"

int main(int argc, char** argv)
{
    QApplication app(argc, argv);
    app.setWindowIcon(QIcon(QStringLiteral(":/hfgw.ico")));

    // --devices: elenca gli ingressi audio e esce. Serve a verificare che il
    // backend multimediale funzioni davvero in una copia distribuita (se manca
    // qualcosa la lista esce vuota e il client sarebbe inutilizzabile).
    if (app.arguments().contains(QStringLiteral("--devices"))) {
        QTextStream out(stdout);
        QList<QAudioDevice> const ins = QMediaDevices::audioInputs();
        out << "ingressi audio trovati: " << ins.size() << "\n";
        for (QAudioDevice const& d : ins) out << "  " << d.description() << "\n";
        QList<QAudioDevice> const outs = QMediaDevices::audioOutputs();
        out << "uscite audio trovate: " << outs.size() << "\n";
        for (QAudioDevice const& d : outs) out << "  " << d.description() << "\n";
        out.flush();
        return ins.isEmpty() ? 2 : 0;
    }

    // --codectest: misura quanta banda occupa ogni profilo, senza radio e senza
    // rete. Serve a verificare i numeri dichiarati in PROTOCOLLO.md su questa
    // macchina invece di fidarsi della tabella.
    if (app.arguments().contains(QStringLiteral("--codectest"))) {
        QTextStream out(stdout);
        out << "Decolink — misura dei profili audio\n";
        out << "libopus " << dl::OpusVoce::versione() << "\n\n";

        // Segnale di prova: parlato finto (fondamentale a 150 Hz con qualche
        // armonica, inviluppo a sillabe) sopra un fruscio di fondo. Non e' una
        // voce vera, ma occupa la banda come una voce in SSB, che e' quello che
        // conta per misurare il codificatore.
        int const secondi = 30;
        int const tot = dl::kOpusRate * secondi;
        QVector<qint16> segnale(tot);
        double fase1 = 0, fase2 = 0, fase3 = 0;
        quint32 rnd = 12345;
        for (int i = 0; i < tot; ++i) {
            double const t = double(i) / dl::kOpusRate;
            double const sillaba = 0.5 + 0.5 * std::sin(2 * M_PI * 3.5 * t);   // ~3,5 sillabe/s
            fase1 += 2 * M_PI * 150.0 / dl::kOpusRate;
            fase2 += 2 * M_PI * 900.0 / dl::kOpusRate;
            fase3 += 2 * M_PI * 2100.0 / dl::kOpusRate;
            rnd = rnd * 1103515245u + 12345u;
            double const fruscio = (double(int((rnd >> 16) & 0x7FFF)) / 16384.0 - 1.0) * 0.03;
            double const v = sillaba * (0.35 * std::sin(fase1) + 0.22 * std::sin(fase2)
                                        + 0.12 * std::sin(fase3)) + fruscio;
            segnale[i] = qint16(qBound(-32768.0, v * 26000.0, 32767.0));
        }

        struct Prova { const char* nome; int bitrate; int banda; int aggr; };
        Prova const prove[] = {
            { "voce 24k, pacchetti da 20 ms", 24000, 6000, 1 },
            { "voce 24k, pacchetti da 40 ms", 24000, 6000, 2 },
            { "voce 24k, pacchetti da 60 ms", 24000, 6000, 3 },
            { "voce 16k, pacchetti da 40 ms", 16000, 6000, 2 },
            { "CW   12k, pacchetti da 20 ms", 12000, 4000, 1 },
            { "CW   12k, pacchetti da 40 ms", 12000, 4000, 2 },
            { "CW   12k, pacchetti da 60 ms", 12000, 4000, 3 },
        };

        double const pcmKbps = double(kHdrSize + kFrame * 2 + 28) * 8.0 * 100.0 / 1000.0;
        out << QStringLiteral("%1  %2 kbit/s  %3 MB/ora\n")
                   .arg(QStringLiteral("PCM 48 kHz (v2, riferimento)"), -32)
                   .arg(pcmKbps, 8, 'f', 1).arg(pcmKbps * 0.45, 6, 'f', 0);

        for (Prova const& p : prove) {
            dl::OpusVoce voce;
            if (!voce.apri(p.bitrate, p.banda)) {
                out << "  " << p.nome << ": Opus non si avvia — " << voce.errore() << "\n";
                continue;
            }
            qint64 byte = 0, campioniResi = 0;
            int frame = 0, pacchetti = 0, riletti = 0;
            QList<QByteArray> gruppo;
            QElapsedTimer cron; cron.start();
            for (int i = 0; i + dl::kOpusFrame <= tot; i += dl::kOpusFrame) {
                QByteArray const c = voce.codifica(segnale.constData() + i);
                if (c.isEmpty()) { out << "  errore di codifica\n"; break; }
                ++frame;
                gruppo.append(c);
                if (gruppo.size() < p.aggr) continue;

                // Il pacchetto vero, come finirebbe sul filo: corpo + header v3
                // + IP/UDP.
                QByteArray const corpo = (p.aggr == 1) ? gruppo.first()
                                                       : dl::corpoAggregato(gruppo);
                byte += corpo.size() + dl::kHdr + 28;
                ++pacchetti;

                // Si rilegge come farebbe chi riceve: se il formato aggregato
                // non tornasse indietro identico, il risparmio sarebbe finto.
                QList<QByteArray> const estratti = dl::frameDaCorpo(corpo, p.aggr > 1);
                if (estratti.size() == gruppo.size()) {
                    bool uguali = true;
                    for (int k = 0; k < estratti.size(); ++k)
                        if (estratti.at(k) != gruppo.at(k)) { uguali = false; break; }
                    if (uguali) riletti += estratti.size();
                }
                for (QByteArray const& f : estratti) {
                    QByteArray const d = voce.decodifica(f.constData(), f.size());
                    campioniResi += d.size() / 2;
                }
                gruppo.clear();
            }
            qint64 const ms = qMax<qint64>(1, cron.elapsed());
            double const kbps = double(byte) * 8.0 / double(secondi) / 1000.0;
            out << QStringLiteral("%1  %2 kbit/s  %3 MB/ora   %4× meno del PCM\n")
                       .arg(QString::fromLatin1(p.nome), -32)
                       .arg(kbps, 8, 'f', 1).arg(kbps * 0.45, 6, 'f', 0)
                       .arg(pcmKbps / kbps, 0, 'f', 1);
            out << QStringLiteral("      %1 frame in %2 pacchetti, %3 riletti identici, "
                                  "%4 campioni resi, %5× tempo reale\n")
                       .arg(frame).arg(pacchetti).arg(riletti).arg(campioniResi)
                       .arg(double(secondi) * 1000.0 / double(ms), 0, 'f', 0);
        }

        // ---- PCM a frequenza ridotta: quanto si risparmia e cosa si perde ----
        out << "\n  PCM con campionamento ridotto (nessun codec, solo meno campioni):\n";
        for (int hz : { 48000, 24000, 12000 }) {
            int const campioni = hz / 100;             // 10 ms
            double const kbps = double(kHdrSize + campioni * 2 + 28) * 100.0 * 8.0 / 1000.0;
            out << QStringLiteral("    %1 kHz: %2 byte per pacchetto, %3 kbit/s, "
                                  "%4 MB/ora, banda audio %5 kHz\n")
                       .arg(hz / 1000, 2).arg(kHdrSize + campioni * 2)
                       .arg(kbps, 6, 'f', 1).arg(kbps * 0.45, 4, 'f', 0).arg(hz / 2000);
        }

        // La prova vera: un tono a 1500 Hz — dove stanno SSB e CW — deve uscire
        // dalla riduzione con la stessa ampiezza. Se sopravvive quello,
        // sopravvive tutto quello che una radio produce davvero.
        out << "\n  un tono a 1500 Hz attraverso la riduzione:\n";
        for (int hz : { 24000, 12000 }) {
            dl::Decimatore dec(kRate / hz, hz * 0.425);
            dl::Interpolatore inter(kRate / hz, hz * 0.425);
            QVector<qint16> ingresso(kRate / 2);       // mezzo secondo
            for (int i = 0; i < ingresso.size(); ++i)
                ingresso[i] = qint16(20000 * std::sin(2 * M_PI * 1500.0 * i / kRate));

            QVector<qint16> giu = dec.giu(ingresso.constData(), ingresso.size());
            QVector<qint16> su = inter.su(giu.constData(), giu.size());

            // si confrontano le ampiezze a regime, saltando l'avvio dei filtri
            auto ampiezza = [](const QVector<qint16>& v, int da) {
                double e = 0; int n = 0;
                for (int i = da; i < v.size(); ++i) { e += double(v[i]) * v[i]; ++n; }
                return n ? std::sqrt(e / n) : 0.0;
            };
            double const a0 = ampiezza(ingresso, 2000);
            double const a1 = ampiezza(su, 4000);
            out << QStringLiteral("    %1 kHz: %2 campioni -> %3, ampiezza %4% "
                                  "dell'originale  %5\n")
                       .arg(hz / 1000, 2).arg(ingresso.size()).arg(giu.size())
                       .arg(a1 / qMax(a0, 1.0) * 100.0, 5, 'f', 1)
                       .arg(a1 / qMax(a0, 1.0) > 0.9 ? QStringLiteral("intatto")
                                                     : QStringLiteral("ATTENUATO"));
        }

        // E cosa succede sopra la banda utile: un tono a 8 kHz, che a 12 kHz di
        // campionamento non ci starebbe, deve essere tolto dal filtro e non
        // ripiegarsi dentro la banda buona.
        {
            dl::Decimatore dec(4, 12000 * 0.425);
            dl::Interpolatore inter(4, 12000 * 0.425);
            QVector<qint16> alto(kRate / 2);
            for (int i = 0; i < alto.size(); ++i)
                alto[i] = qint16(20000 * std::sin(2 * M_PI * 8000.0 * i / kRate));
            QVector<qint16> const giu = dec.giu(alto.constData(), alto.size());
            QVector<qint16> const su = inter.su(giu.constData(), giu.size());
            double e = 0; int n = 0;
            for (int i = 4000; i < su.size(); ++i) { e += double(su[i]) * su[i]; ++n; }
            double const resta = n ? std::sqrt(e / n) / 20000.0 * 100.0 : 0;
            out << QStringLiteral("\n    un tono a 8 kHz (fuori dalla banda utile) a 12 kHz: "
                                  "ne resta il %1%  %2\n")
                       .arg(resta, 0, 'f', 2)
                       .arg(resta < 2.0 ? QStringLiteral("tolto dal filtro, niente aliasing")
                                        : QStringLiteral("ATTENZIONE: rientra ripiegato"));
        }

        // ---- profilo dei digitali: la promessa e' che non si perda un bit ----
        out << "\n";
        {
            dl::Decimatore dec;
            qint64 grezzi = 0, compressi = 0, byteRete = 0;
            int blocchi = 0, identici = 0;
            QElapsedTimer cron; cron.start();
            for (int i = 0; i + kDigiIngresso <= tot; i += kDigiIngresso) {
                QVector<qint16> const giu = dec.giu(segnale.constData() + i, kDigiIngresso);
                if (giu.isEmpty()) continue;
                QByteArray const blocco = dl::comprimi(giu.constData(), giu.size());
                QVector<qint16> const torna = dl::decomprimi(blocco);
                ++blocchi;
                grezzi += giu.size() * 2;
                compressi += blocco.size();
                byteRete += blocco.size() + dl::kHdr + 28;
                if (torna == giu) ++identici;      // confronto esatto, campione per campione
            }
            double const kbps = double(byteRete) * 8.0 / double(secondi) / 1000.0;
            out << QStringLiteral("%1  %2 kbit/s  %3 MB/ora   %4× meno del PCM\n")
                       .arg(QStringLiteral("digitali (12 kHz senza perdite)"), -32)
                       .arg(kbps, 8, 'f', 1).arg(kbps * 0.45, 6, 'f', 0)
                       .arg(pcmKbps / kbps, 0, 'f', 1);
            out << QStringLiteral("      %1 blocchi, compressi al %2% del grezzo, "
                                  "%3× tempo reale\n")
                       .arg(blocchi)
                       .arg(double(compressi) * 100.0 / double(qMax<qint64>(1, grezzi)), 0, 'f', 1)
                       .arg(double(secondi) * 1000.0 / double(qMax<qint64>(1, cron.elapsed())), 0, 'f', 0);
            out << QStringLiteral("      ricostruiti identici: %1 su %2  -> %3\n")
                       .arg(identici).arg(blocchi)
                       .arg(identici == blocchi ? QStringLiteral("SENZA PERDITE, confermato")
                                                : QStringLiteral("ATTENZIONE: NON è senza perdite"));
        }

        // Il compressore va provato anche su segnali che in aria capitano: il
        // silenzio, la saturazione e il rumore puro sono i casi in cui un
        // predittore si comporta peggio, ed e' li' che un errore si nasconde.
        {
            out << "\n  prove del compressore su casi difficili:\n";
            struct Caso { const char* nome; int tipo; };
            Caso const casi[] = { {"silenzio", 0}, {"rumore a tutto volume", 1},
                                  {"saturazione ai due estremi", 2},
                                  {"tono puro", 3}, {"gradini bruschi", 4} };
            quint32 r = 999;
            bool tuttoBene = true;
            for (Caso const& c : casi) {
                QVector<qint16> blocco(dl::kDigiRate / 25);
                for (int i = 0; i < blocco.size(); ++i) {
                    r = r * 1103515245u + 12345u;
                    switch (c.tipo) {
                    case 0: blocco[i] = 0; break;
                    case 1: blocco[i] = qint16(int((r >> 16) & 0xFFFF) - 32768); break;
                    case 2: blocco[i] = (i % 2) ? 32767 : -32768; break;
                    case 3: blocco[i] = qint16(30000 * std::sin(2 * M_PI * 1500.0 * i / dl::kDigiRate)); break;
                    default: blocco[i] = (i / 40 % 2) ? 20000 : -20000; break;
                    }
                }
                QByteArray const c1 = dl::comprimi(blocco.constData(), blocco.size());
                QVector<qint16> const c2 = dl::decomprimi(c1);
                bool const uguale = (c2 == blocco);
                if (!uguale) tuttoBene = false;
                out << QStringLiteral("    %1  %2 -> %3 byte (%4%)  %5\n")
                           .arg(QString::fromLatin1(c.nome), -28)
                           .arg(blocco.size() * 2).arg(c1.size())
                           .arg(double(c1.size()) * 100.0 / double(blocco.size() * 2), 0, 'f', 0)
                           .arg(uguale ? QStringLiteral("identico") : QStringLiteral("DIVERSO!"));
            }
            // Un blocco tagliato a metà non deve produrre campioni inventati:
            // meglio niente che dati falsi consegnati a un decodificatore.
            QVector<qint16> pieno(480, 1234);
            QByteArray tagliato = dl::comprimi(pieno.constData(), pieno.size());
            tagliato.truncate(tagliato.size() / 2);
            bool const scartato = dl::decomprimi(tagliato).isEmpty();
            out << QStringLiteral("    %1  %2\n").arg(QStringLiteral("blocco tagliato a metà"), -28)
                       .arg(scartato ? QStringLiteral("scartato, come deve")
                                     : QStringLiteral("ACCETTATO: sbagliato"));
            if (!scartato) tuttoBene = false;
            out << (tuttoBene ? "  tutte le prove passate\n" : "  QUALCOSA NON TORNA\n");
        }

        // ---- CW a tasto: la banda conta poco, conta che il ritmo sopravviva ----
        out << "\n";
        {
            // "CQ DE IU8LMC K" a 20 parole al minuto: il punto dura 60 ms.
            // Costruito con le durate esatte, cosi' si puo' confrontare quello
            // che il rilevatore ha capito con quello che c'era davvero.
            int const punto = 60;
            const char* morse[] = {
                "-.-.", "--.-", " ", "-..", ".", " ",
                "..", "..-", "---.", ".-..", "--", "-.-.", "-...", " ", "-.-"
            };
            struct Tratto { bool giu; int ms; };
            QVector<Tratto> voluti;
            // Mezzo secondo di sola banda prima di cominciare: e' come va nella
            // realta' (si apre il collegamento, si sente il fruscio, poi arriva
            // qualcuno) e da' al rilevatore il tempo di formare le soglie.
            voluti.append({ false, 500 });
            for (const char* lettera : morse) {
                if (lettera[0] == ' ') { voluti.append({ false, punto * 4 }); continue; }
                for (int i = 0; lettera[i]; ++i) {
                    voluti.append({ true, lettera[i] == '.' ? punto : punto * 3 });
                    voluti.append({ false, punto });
                }
                voluti.append({ false, punto * 2 });      // pausa fra lettere
            }

            // Audio: tono a 700 Hz con attacco morbido, piu' un po' di fruscio,
            // perche' un rilevatore che funziona solo sul segnale pulito non
            // serve a niente.
            QVector<qint16> audio;
            double fase = 0, amp = 0;
            quint32 rnd = 4242;
            int msTot = 0;
            for (Tratto const& t : voluti) {
                int const n = t.ms * 48;
                for (int i = 0; i < n; ++i) {
                    amp += t.giu ? 1.0 / 240.0 : -1.0 / 240.0;
                    amp = qBound(0.0, amp, 1.0);
                    fase += 2 * M_PI * 700.0 / 48000.0;
                    rnd = rnd * 1103515245u + 12345u;
                    double const fruscio = (double(int((rnd >> 16) & 0x7FFF)) / 16384.0 - 1.0) * 0.02;
                    audio.append(qint16(qBound(-32768.0,
                                               (amp * 0.55 * std::sin(fase) + fruscio) * 32000.0,
                                               32767.0)));
                }
                msTot += t.ms;
            }

            dl::RilevatoreCw ril;
            QVector<dl::EventoCw> visti;
            qint64 byteRete = 0;
            int pacchetti = 0;
            QVector<dl::EventoCw> gruppo;
            int msDaInvio = 0;
            // Si simula anche il raggruppamento a 100 ms, come fa il client.
            for (int i = 0; i + dl::kCwBlocco <= audio.size(); i += dl::kCwBlocco) {
                QVector<dl::EventoCw> const ev = ril.mangia(audio.constData() + i, dl::kCwBlocco);
                for (dl::EventoCw const& e : ev) { gruppo.append(e); visti.append(e); }
                msDaInvio += dl::kCwMs;
                if (!gruppo.isEmpty() && msDaInvio >= 100) {
                    byteRete += dl::corpoCw(ril.notaHz(), gruppo).size() + dl::kHdr + 28;
                    ++pacchetti;
                    gruppo.clear();
                    msDaInvio = 0;
                }
            }
            if (!gruppo.isEmpty()) {
                byteRete += dl::corpoCw(ril.notaHz(), gruppo).size() + dl::kHdr + 28;
                ++pacchetti;
            }

            double const secondiCw = double(msTot) / 1000.0;
            double const kbps = double(byteRete) * 8.0 / secondiCw / 1000.0;
            out << QStringLiteral("%1  %2 kbit/s  %3 MB/ora   %4× meno del PCM\n")
                       .arg(QStringLiteral("CW a tasto (solo il ritmo)"), -32)
                       .arg(kbps, 8, 'f', 1).arg(kbps * 0.45, 6, 'f', 0)
                       .arg(pcmKbps / kbps, 0, 'f', 0);
            out << QStringLiteral("      %1 s di trasmissione, %2 eventi in %3 pacchetti, nota "
                                  "riconosciuta %4 Hz\n")
                       .arg(secondiCw, 0, 'f', 1).arg(visti.size()).arg(pacchetti).arg(ril.notaHz());

            // La prova vera: le durate riconosciute corrispondono a quelle
            // trasmesse? Prima si fondono i tratti consecutivi con lo stesso
            // stato — le pause fra simboli e fra lettere sono silenzi attaccati,
            // e il rilevatore vede giustamente un solo intervallo.
            QVector<Tratto> fusi;
            for (Tratto const& t : voluti) {
                if (!fusi.isEmpty() && fusi.last().giu == t.giu) fusi.last().ms += t.ms;
                else fusi.append(t);
            }

            // Il deltaMs di un evento e' la durata del tratto che lo precede,
            // quindi visti[i] va confrontato con fusi[i]. Il primo si salta: e'
            // misurato dalla fine del periodo di apprendimento, non dall'inizio
            // dell'audio, e sarebbe un confronto senza senso.
            int confrontati = 0, entro10 = 0, peggiore = 0;
            for (int i = 1; i < visti.size() && i < fusi.size(); ++i) {
                int const errore = std::abs(int(visti[i].deltaMs) - fusi[i].ms);
                ++confrontati;
                if (errore <= 10) ++entro10;
                peggiore = qMax(peggiore, errore);
            }
            out << "      primi tratti (atteso -> misurato):";
            for (int i = 1; i < visti.size() && i < fusi.size() && i <= 6; ++i)
                out << QStringLiteral("  %1%2->%3")
                           .arg(fusi[i].giu ? QStringLiteral("giù ") : QStringLiteral("su "))
                           .arg(fusi[i].ms).arg(visti[i].deltaMs);
            out << "\n";
            out << QStringLiteral("      durate confrontate: %1, entro 10 ms: %2, errore massimo %3 ms\n")
                       .arg(confrontati).arg(entro10).arg(peggiore);
            bool const ritmoOk = confrontati > 20 && entro10 >= confrontati * 9 / 10 && peggiore <= 20;
            out << QStringLiteral("      %1\n")
                       .arg(ritmoOk ? QStringLiteral("il ritmo sopravvive al viaggio")
                                    : QStringLiteral("ATTENZIONE: il ritmo si deforma"));

            // Andata e ritorno: si rigenera il tono dagli eventi e lo si ripassa
            // dal rilevatore. Se il ritmo esce di nuovo uguale, tutta la catena
            // — rilevatore, formato, sintetizzatore — conserva quello che deve
            // conservare. E' una prova piu' onesta del confronto con l'audio di
            // partenza, che sarebbe sensibile a qualche millisecondo di sfasamento
            // senza che questo significhi niente per chi ascolta.
            dl::SintetizzatoreCw sint;
            sint.nota(ril.notaHz());
            sint.aggiungi(visti);
            QVector<qint16> const rifatto = sint.genera(audio.size());

            dl::RilevatoreCw ril2;
            QVector<dl::EventoCw> visti2;
            for (int i = 0; i + dl::kCwBlocco <= rifatto.size(); i += dl::kCwBlocco)
                for (dl::EventoCw const& e : ril2.mangia(rifatto.constData() + i, dl::kCwBlocco))
                    visti2.append(e);

            int rifatti = 0, rifattiOk = 0, peggioreRif = 0;
            for (int i = 1; i < visti.size() && i < visti2.size(); ++i) {
                int const errore = std::abs(int(visti2[i].deltaMs) - int(visti[i].deltaMs));
                ++rifatti;
                if (errore <= 10) ++rifattiOk;
                peggioreRif = qMax(peggioreRif, errore);
            }
            out << QStringLiteral("      andata e ritorno: %1 eventi rigenerati su %2, "
                                  "durate entro 10 ms: %3/%4, errore massimo %5 ms\n")
                       .arg(visti2.size()).arg(visti.size())
                       .arg(rifattiOk).arg(rifatti).arg(peggioreRif);
            out << QStringLiteral("      %1\n")
                       .arg(rifatti > 20 && rifattiOk >= rifatti * 9 / 10 && peggioreRif <= 20
                                ? QStringLiteral("il tono rigenerato ripete lo stesso ritmo")
                                : QStringLiteral("ATTENZIONE: la rigenerazione altera il ritmo"));
        }

        out << "\nNota: non si riporta un rapporto segnale/rumore fra originale e\n"
               "ricostruito. Opus e' un codificatore percettivo e sposta la fase:\n"
               "un confronto campione per campione darebbe un numero pessimo anche\n"
               "quando l'audio e' ottimo, quindi sarebbe una misura falsa.\n"
               "La qualita' in fonia si giudica ascoltando; la banda si misura, ed e'\n"
               "quella che vedi qui sopra.\n";
        out.flush();
        return 0;
    }

    // --hamlibtest: elenca le radio conosciute e prova tutta la catena sulla
    // radio finta di Hamlib, che risponde come una vera senza essere collegata.
    // E' l'unico modo di verificare il percorso — apertura, frequenza, modo,
    // PTT — senza avere trecento apparati sul tavolo.
    if (app.arguments().contains(QStringLiteral("--hamlibtest"))) {
        QTextStream out(stdout);
#ifndef DECOLINK_CON_HAMLIB
        out << "Compilato senza Hamlib: restano i protocolli nativi Yaesu e Icom.\n"
               "Su MSYS2:  pacman -S mingw-w64-x86_64-hamlib\n";
        out.flush();
        return 3;
#else
        QList<dl::ModelloRig> const elenco = dl::HamlibRig::modelli();
        out << dl::HamlibRig::versione() << " — " << elenco.size() << " modelli\n\n";

        QMap<QString, int> perCostruttore;
        int stabili = 0;
        for (dl::ModelloRig const& r : elenco) {
            perCostruttore[r.costruttore]++;
            if (r.stato == QLatin1String("stabile")) ++stabili;
        }
        out << QStringLiteral("  %1 costruttori, %2 modelli dichiarati stabili\n\n")
                   .arg(perCostruttore.size()).arg(stabili);
        out << "  i costruttori con piu' modelli:\n";
        QList<QPair<int, QString>> ordinati;
        for (auto it = perCostruttore.cbegin(); it != perCostruttore.cend(); ++it)
            ordinati.append({ it.value(), it.key() });
        std::sort(ordinati.begin(), ordinati.end(),
                  [](auto const& a, auto const& b) { return a.first > b.first; });
        for (int i = 0; i < qMin(8, ordinati.size()); ++i)
            out << QStringLiteral("    %1  %2\n").arg(ordinati[i].first, 4).arg(ordinati[i].second);

        // Le radio che interessano qui, per vedere che ci siano davvero.
        out << "\n  qualche modello cercato per nome:\n";
        for (QString const& cerca : { QStringLiteral("FT-991"), QStringLiteral("IC-7300"),
                                      QStringLiteral("TS-590"), QStringLiteral("FT-817"),
                                      QStringLiteral("IC-705"), QStringLiteral("FlexRadio") }) {
            bool trovato = false;
            for (dl::ModelloRig const& r : elenco) {
                if (r.modello.contains(cerca, Qt::CaseInsensitive)
                    || r.costruttore.contains(cerca, Qt::CaseInsensitive)) {
                    out << QStringLiteral("    %1 %2  (numero %3, %4)\n")
                               .arg(r.costruttore, r.modello).arg(r.numero).arg(r.stato);
                    trovato = true;
                    break;
                }
            }
            if (!trovato) out << QStringLiteral("    %1: non trovato\n").arg(cerca);
        }

        // La radio finta: risponde ai comandi come una vera, quindi permette di
        // provare l'intero percorso senza hardware.
        out << "\n  prova sulla radio finta di Hamlib:\n";
        dl::HamlibRig finta;
        if (!finta.apri(1, QStringLiteral("/dev/null"), 0)) {
            out << "    non si apre: " << finta.errore() << "\n";
            out.flush();
            return 4;
        }
        out << QStringLiteral("    aperta: %1\n").arg(finta.nome());
        bool tutto = true;
        auto prova = [&](const QString& cosa, bool esito, const QString& letto) {
            out << QStringLiteral("    %1%2  %3\n").arg(cosa, -34)
                       .arg(esito ? QStringLiteral("ok") : QStringLiteral("FALLITO"), -8).arg(letto);
            if (!esito) tutto = false;
        };
        bool const okF = finta.impostaFrequenza(14074000);
        qint64 const letta = finta.frequenza();
        prova(QStringLiteral("imposta 14.074.000 Hz e rileggi"), okF && letta == 14074000,
              QStringLiteral("%1 Hz").arg(letta));
        bool const okM = finta.impostaModo(QStringLiteral("USB"));
        QString const modo = finta.modo();
        prova(QStringLiteral("imposta USB e rileggi"), okM && modo == QLatin1String("USB"), modo);
        bool const okC = finta.impostaModo(QStringLiteral("CW"));
        QString const modo2 = finta.modo();
        prova(QStringLiteral("imposta CW e rileggi"), okC && modo2 == QLatin1String("CW"), modo2);
        bool const okT = finta.trasmetti(true);
        bool const inTx = finta.inTrasmissione();
        prova(QStringLiteral("PTT giù e rileggi"), okT && inTx,
              inTx ? QStringLiteral("in trasmissione") : QStringLiteral("a riposo"));
        finta.trasmetti(false);
        prova(QStringLiteral("PTT su e rileggi"), !finta.inTrasmissione(),
              QStringLiteral("a riposo"));
        bool const modoStrano = finta.impostaModo(QStringLiteral("PIZZA"));
        prova(QStringLiteral("un modo inventato viene rifiutato"), !modoStrano, finta.errore());
        finta.chiudi();
        out << (tutto ? "\n  la catena funziona\n" : "\n  QUALCOSA NON TORNA\n");
        out.flush();
        return tutto ? 0 : 1;
#endif
    }

    // --emrgtest: prova il collegamento d'emergenza al banco, facendo passare
    // voce e comandi attraverso un canale rumoroso simulato. Non sostituisce la
    // prova in aria — servono due radio — ma dice se la catena funziona e a che
    // rapporto segnale/rumore smette di funzionare.
    if (app.arguments().contains(QStringLiteral("--emrgtest"))) {
        QTextStream out(stdout);
#ifndef DECOLINK_CON_FREEDV
        out << "Questa copia e' stata compilata senza libcodec2: il collegamento\n"
               "d'emergenza non c'e'. Su MSYS2:  pacman -S mingw-w64-x86_64-codec2\n";
        out.flush();
        return 3;
#else
        out << "Decolink — collegamento d'emergenza (FreeDV)\n\n";
        dl::FreeDvLink link;
        if (!link.apri()) {
            out << "  " << link.errore() << "\n";
            out.flush();
            return 4;
        }
        int const nVoce = link.campioniVoce();
        int const nModem = link.campioniModem();
        out << QStringLiteral("  voce  %1: %2 campioni per frame a %3 Hz\n")
                   .arg(dl::FreeDvLink::nomeModo(FREEDV_MODE_700E)).arg(nVoce)
                   .arg(link.frequenzaVoce());
        out << QStringLiteral("  modem: %1 campioni per frame a %2 Hz\n")
                   .arg(nModem).arg(link.frequenzaModem());
        out << QStringLiteral("  dati  %1: %2 bit per frame (%3 byte)\n\n")
                   .arg(dl::FreeDvLink::nomeModo(FREEDV_MODE_DATAC3))
                   .arg(link.bitPerFrameDati()).arg(link.bytePerFrameDati());

        // Parlato finto a 8 kHz, come quello di --codectest ma alla frequenza di
        // FreeDV.
        int const secondi = 6;
        int const tot = link.frequenzaVoce() * secondi;
        QVector<qint16> voce(tot);
        double f1 = 0, f2 = 0, f3 = 0;
        for (int i = 0; i < tot; ++i) {
            double const t = double(i) / link.frequenzaVoce();
            double const sillaba = 0.5 + 0.5 * std::sin(2 * M_PI * 3.5 * t);
            f1 += 2 * M_PI * 150.0 / link.frequenzaVoce();
            f2 += 2 * M_PI * 900.0 / link.frequenzaVoce();
            f3 += 2 * M_PI * 2100.0 / link.frequenzaVoce();
            voce[i] = qint16(sillaba * (0.4 * std::sin(f1) + 0.25 * std::sin(f2)
                                       + 0.15 * std::sin(f3)) * 24000.0);
        }

        // Modulazione: la voce diventa audio da mandare al rig del link.
        QVector<qint16> onda;
        for (int i = 0; i + nVoce <= tot; i += nVoce)
            onda.append(link.vocePerRadio(voce.constData() + i));
        double const secondiOnda = double(onda.size()) / link.frequenzaModem();
        out << QStringLiteral("  %1 s di parlato -> %2 campioni di modem (%3 s)\n")
                   .arg(secondi).arg(onda.size()).arg(secondiOnda, 0, 'f', 1);
        out << QStringLiteral("  occupazione sul filo: 700 bit/s, cioe' %1 volte meno del PCM\n\n")
                   .arg(808000.0 / 700.0, 0, 'f', 0);

        // Il canale: rumore bianco a rapporti segnale/rumore decrescenti. Un
        // modem HF si giudica da dove cede, non da come va sul banco pulito.
        // Il rumore si sparge su tutti i 4 kHz del canale, mentre il segnale
        // occupa 1,1 kHz: il rapporto che conta per il modem e' quindi ~5,6 dB
        // migliore di quello scritto qui. Si riporta il valore a banda piena
        // perche' e' quello che si misura su uno strumento, ma il confronto con
        // le tabelle di FreeDV va fatto tenendo conto di questa differenza.
        out << "  attraverso un canale rumoroso (rapporto misurato su tutti i 4 kHz):\n";
        double pot = 0;
        for (qint16 v : onda) pot += double(v) * double(v);
        pot /= qMax(1, onda.size());

        quint32 seme = 777;
        for (double snrDb : { 10.0, 0.0, -6.0, -10.0, -13.0, -16.0, -20.0 }) {
            double const sigma = std::sqrt(pot / std::pow(10.0, snrDb / 10.0));

            // Tre prove con rumore diverso: l'aggancio di un modem e' un
            // fenomeno a soglia, e una prova sola darebbe numeri che ballano di
            // decine di punti da un livello al successivo — come e' capitato
            // nella prima stesura di questa misura.
            double somma = 0;
            for (int prova = 0; prova < 3; ++prova) {
                quint32 rnd = seme + quint32(prova) * 9871;
                QVector<qint16> sporca(onda.size());
                for (int i = 0; i < onda.size(); ++i) {
                    // rumore gaussiano approssimato sommando quattro uniformi
                    double g = 0;
                    for (int k = 0; k < 4; ++k) {
                        rnd = rnd * 1103515245u + 12345u;
                        g += double(int((rnd >> 16) & 0x7FFF)) / 16384.0 - 1.0;
                    }
                    sporca[i] = qint16(qBound(-32768.0, double(onda[i]) + g * sigma * 0.5, 32767.0));
                }

                dl::FreeDvLink rx;
                rx.apri();
                int conBit = 0, blocchi = 0;
                for (int i = 0; i + nModem <= sporca.size(); i += nModem) {
                    rx.voceDaRadio(sporca.constData() + i, nModem);
                    ++blocchi;
                    // Il sync da solo non basta: freedv_rx restituisce campioni
                    // anche quando non ha agganciato, solo che sono silenzio.
                    // Quello che conta e' se ha consegnato dei bit.
                    if (rx.haConsegnatoVoce()) ++conBit;
                }
                somma += blocchi ? 100.0 * conBit / blocchi : 0;
            }
            seme += 31;
            double const perc = somma / 3.0;
            out << QStringLiteral("    S/N %1 dB:  frame con voce %2%  %3\n")
                       .arg(snrDb, 5, 'f', 1).arg(perc, 5, 'f', 1)
                       .arg(perc > 80 ? QStringLiteral("buono")
                            : perc > 40 ? QStringLiteral("faticoso")
                                        : QStringLiteral("non tiene"));
        }

        // I comandi al rig: quelli devono passare anche quando la voce non passa,
        // perche' sono la cosa piu' importante da avere in emergenza.
        out << "\n  comandi al rig sul canale dati:\n";
        QByteArray const comando = QByteArrayLiteral("F 14074000\nM USB 2400\n");
        QVector<qint16> const ondaDati = link.datiPerRadio(comando);
        out << QStringLiteral("    \"%1\" -> %2 campioni (%3 s di trasmissione)\n")
                   .arg(QString::fromLatin1(comando).trimmed().replace('\n', QLatin1String(" | ")))
                   .arg(ondaDati.size())
                   .arg(double(ondaDati.size()) / link.frequenzaModem(), 0, 'f', 1);
        {
            dl::FreeDvLink rxd;
            rxd.apri();
            QByteArray tornato;
            for (int i = 0; i + nModem <= ondaDati.size(); i += nModem)
                tornato.append(rxd.datiDaRadio(ondaDati.constData() + i, nModem));
            QByteArray pulito = tornato;
            while (pulito.endsWith('\0')) pulito.chop(1);
            bool const ok = pulito.startsWith(comando.left(10));
            out << QStringLiteral("    ritornati %1 byte  %2\n")
                       .arg(tornato.size())
                       .arg(ok ? QStringLiteral("comando riconosciuto")
                               : QStringLiteral("(su canale pulito il preambolo può "
                                                "non bastare: si ripete)"));
        }

        out << "\n  Attenzione, e sta scritto anche in PROTOCOLLO.md §7:\n"
               "  serve un SECONDO apparato per lato. La radio che si remotizza non\n"
               "  puo' fare anche da modem per il collegamento che la comanda.\n"
               "  E il canale e' half-duplex: o si parla, o si comanda.\n"
               "  I modi digitali (FT8) in 700 bit/s non ci stanno, e non ci staranno.\n";
        out.flush();
        return 0;
#endif
    }

    // --cattest COM5 38400: interroga solo la seriale del rig ed esce. Serve a
    // distinguere un problema di porta/cablaggio da uno di rete.
    if (app.arguments().contains(QStringLiteral("--cattest"))) {
        QTextStream out(stdout);
        QStringList const a2 = app.arguments();
        int const i = a2.indexOf(QStringLiteral("--cattest"));
        QString const port = (i + 1 < a2.size()) ? a2.at(i + 1) : QStringLiteral("COM5");
        int const baud = (i + 2 < a2.size()) ? a2.at(i + 2).toInt() : 38400;
        out << "porte disponibili:";
        for (QSerialPortInfo const& pi : QSerialPortInfo::availablePorts()) out << " " << pi.portName();
        out << "\napro " << port << " a " << baud << " baud\n";
        CatRig rig;
        if (!rig.open(port, baud, QSerialPort::Data8, QSerialPort::NoParity,
                      QSerialPort::OneStop, QSerialPort::NoFlowControl)) {
            out << "apertura fallita: " << rig.error() << "\n"; out.flush(); return 6;
        }
        qint64 const hz = rig.readFreq();
        QString const md = rig.readMode();
        out << "frequenza letta: " << hz << "\nmodo letto: " << (md.isEmpty() ? QStringLiteral("(nessuna risposta)") : md) << "\n";
        out.flush();
        return hz > 0 ? 0 : 7;
    }

    // --selftest: apre davvero l'ingresso e cattura mezzo secondo. Elencare i
    // dispositivi non basta a dire che una copia distribuita funziona: la
    // cattura carica altre librerie del backend, ed e' li' che si scopre se
    // manca qualcosa.
    if (app.arguments().contains(QStringLiteral("--selftest"))) {
        QTextStream out(stdout);
        QList<QAudioDevice> const ins = QMediaDevices::audioInputs();
        if (ins.isEmpty()) { out << "nessun ingresso audio\n"; out.flush(); return 2; }
        QAudioFormat fmt;
        fmt.setSampleRate(kRate); fmt.setChannelCount(1); fmt.setSampleFormat(QAudioFormat::Int16);
        int idx = 0;
        for (int i = 0; i < ins.size(); ++i)
            if (ins[i].description().contains(QStringLiteral("USB Audio CODEC"))) { idx = i; break; }
        out << "apro: " << ins[idx].description() << "\n";
        if (!ins[idx].isFormatSupported(fmt)) { out << "formato 48k mono 16bit non supportato\n"; out.flush(); return 3; }
        QAudioSource src(ins[idx], fmt);
        QIODevice* io = src.start();
        if (!io) { out << "start() fallito\n"; out.flush(); return 4; }
        qint64 total = 0;
        QEventLoop loop;
        QObject::connect(io, &QIODevice::readyRead, [&] { total += io->readAll().size(); });
        QTimer::singleShot(500, &loop, &QEventLoop::quit);
        loop.exec();
        src.stop();
        out << "catturati " << total << " byte in 0,5 s (attesi ~48000)\n";
        out << (total > 8000 ? "CATTURA OK\n" : "CATTURA INSUFFICIENTE\n");
        out.flush();
        return total > 8000 ? 0 : 5;
    }

    Client w;
    w.show();
    return app.exec();
}
