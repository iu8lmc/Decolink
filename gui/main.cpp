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
#include <QGroupBox>
#include <QHostInfo>
#include <QIcon>
#include <QHBoxLayout>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QLabel>
#include <QLineEdit>
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

#include "dlproto.h"
#include "opusvoce.h"

#include <cmath>

namespace {

constexpr int kRate      = 48000;
constexpr int kFrame     = kRate / 100;   // 480 campioni = 10 ms
constexpr int kHdrSize   = 22;
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

QByteArray hfgwPacket(quint8 flags, quint32 seq, const char* payload, int len)
{
    QByteArray pkt(kHdrSize + qMax(0, len), Qt::Uninitialized);
    char* p = pkt.data();
    std::memcpy(p, "HFGW", 4);
    p[4] = char(kProtoVer); p[5] = char(flags);
    putU32(p + 6, seq);
    putU64(p + 10, quint64(QDateTime::currentMSecsSinceEpoch()));
    putU32(p + 18, kRate);
    if (payload && len > 0) std::memcpy(p + kHdrSize, payload, size_t(len));
    return pkt;
}

enum Mode { ModeLan = 0, ModeRelay = 1, ModeListen = 2 };

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

    bool open(const QString& portName, int baud)
    {
        close();
        m_port = new QSerialPort(portName, this);
        m_port->setBaudRate(baud);
        m_port->setDataBits(QSerialPort::Data8);
        m_port->setParity(QSerialPort::NoParity);
        m_port->setStopBits(QSerialPort::OneStop);
        m_port->setFlowControl(QSerialPort::NoFlowControl);
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
    }

    bool isOpen() const { return m_port && m_port->isOpen(); }
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
            send(QStringLiteral("FA%1;").arg(hz, 9, 10, QChar('0')));
            return QStringLiteral("RPRT 0\n");
        }
        if (cmd.startsWith(QLatin1String("T "))) {
            bool const on = cmd.mid(2).trimmed().toInt() != 0;
            send(on ? QStringLiteral("TX1;") : QStringLiteral("TX0;"));
            return QStringLiteral("RPRT 0\n");
        }
        if (cmd == QLatin1String("t")) {
            QString const r = query(QStringLiteral("TX;"), QStringLiteral("TX"));
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
        if (cmd.startsWith(QLatin1String("M "))) return QStringLiteral("RPRT 0\n");   // modo: lo imposta l'operatore
        return QStringLiteral("RPRT 0\n");
    }

    qint64 readFreq()
    {
        QString const r = query(QStringLiteral("FA;"), QStringLiteral("FA"));
        if (r.size() < 11) return 0;
        return r.mid(2, 9).toLongLong();
    }

    QString readMode()
    {
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
        m_mode->addItem(QStringLiteral("LAN diretta — indirizzo del telefono"));
        m_mode->addItem(QStringLiteral("Relay + stanza — funziona ovunque"));
        m_mode->addItem(QStringLiteral("Il telefono chiama casa — DynDNS/porta inoltrata"));

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
        m_profile = new QComboBox;
        m_profile->addItem(QStringLiteral("Voce — Opus, 39 kbit/s (consigliato)"), dl::PVoce);
        m_profile->addItem(QStringLiteral("CW — Opus banda stretta, 27 kbit/s"), dl::PCw);
        m_profile->addItem(QStringLiteral("PCM 48 kHz — 808 kbit/s, per client vecchi"), dl::PPcm48);

        // Quanti frame per pacchetto. Piu' se ne raggruppano, meno volte si paga
        // l'involucro IP/UDP, ma piu' latenza si aggiunge.
        m_aggr = new QComboBox;
        m_aggr->addItem(QStringLiteral("20 ms — latenza minima"), 1);
        m_aggr->addItem(QStringLiteral("40 ms — 18% di banda in meno (consigliato)"), 2);
        m_aggr->addItem(QStringLiteral("60 ms — 24% in meno, per reti a consumo"), 3);
        m_aggr->setCurrentIndex(1);

        auto* form = new QFormLayout;
        form->addRow(QStringLiteral("Audio della radio"), m_device);
        form->addRow(QStringLiteral("Modalità"), m_mode);
        form->addRow(QStringLiteral("Host"), m_host);
        form->addRow(QStringLiteral("Porta"), m_port);
        form->addRow(QStringLiteral("Stazione"), m_station);
        form->addRow(QStringLiteral("Profilo audio"), m_profile);
        form->addRow(QStringLiteral("Pacchetti da"), m_aggr);

        m_start = new QPushButton(QStringLiteral("Avvia"));
        m_start->setMinimumHeight(34);
        m_level = new QProgressBar; m_level->setRange(0, 100); m_level->setTextVisible(false);
        m_level->setFixedHeight(14);
        m_status = new QLabel(QStringLiteral("fermo"));
        m_stats  = new QLabel(QStringLiteral("—"));
        m_stats->setStyleSheet(QStringLiteral("color:#666"));

        auto* row = new QHBoxLayout;
        row->addWidget(m_start);
        row->addWidget(new QLabel(QStringLiteral("livello")));
        row->addWidget(m_level, 1);

        // ---- CAT: controllo del rig sulla seriale, servito al telefono ----
        m_catPort = new QComboBox;
        for (QSerialPortInfo const& pi : QSerialPortInfo::availablePorts())
            m_catPort->addItem(pi.portName() + "  " + pi.description());
        m_catBaud = new QComboBox;
        for (int b : {4800, 9600, 19200, 38400, 57600, 115200}) m_catBaud->addItem(QString::number(b));
        m_catBaud->setCurrentText(QStringLiteral("38400"));
        m_catTcpPort = new QSpinBox; m_catTcpPort->setRange(1, 65535); m_catTcpPort->setValue(4532);
        m_catOn = new QCheckBox(QStringLiteral("Servi il CAT al telefono"));
        m_catState = new QLabel(QStringLiteral("CAT spento"));

        m_rigOut = new QComboBox;
        m_rigOut->addItem(QStringLiteral("(nessuna: non trasmettere)"));
        for (QAudioDevice const& d : QMediaDevices::audioOutputs())
            m_rigOut->addItem(d.description());

        auto* catForm = new QFormLayout;
        catForm->addRow(QStringLiteral("Audio verso il rig (TX)"), m_rigOut);
        catForm->addRow(QStringLiteral("Porta del rig"), m_catPort);
        catForm->addRow(QStringLiteral("Velocità"), m_catBaud);
        catForm->addRow(QStringLiteral("Porta TCP (LAN)"), m_catTcpPort);
        auto* catBox = new QGroupBox(QStringLiteral("CAT — controllo della radio"));
        auto* catLay = new QVBoxLayout(catBox);
        catLay->addLayout(catForm);
        catLay->addWidget(m_catOn);
        catLay->addWidget(m_catState);

        // ---- accesso: chi sei, e che cosa ti lasciano fare ----
        m_authHost = new QLineEdit;
        m_authHost->setPlaceholderText(QStringLiteral("server di accesso (es. decolink.ft2.it)"));
        m_email = new QLineEdit;
        m_email->setPlaceholderText(QStringLiteral("la tua email"));
        m_password = new QLineEdit;
        m_password->setEchoMode(QLineEdit::Password);
        m_password->setPlaceholderText(QStringLiteral("password"));
        m_remember = new QCheckBox(QStringLiteral("Ricorda la password (salvata in chiaro fra le impostazioni)"));
        m_login = new QPushButton(QStringLiteral("Accedi"));
        m_authState = new QLabel(QStringLiteral("non collegato"));
        m_authState->setWordWrap(true);
        m_authState->setStyleSheet(QStringLiteral("color:#666"));

        auto* authForm = new QFormLayout;
        authForm->addRow(QStringLiteral("Server di accesso"), m_authHost);
        authForm->addRow(QStringLiteral("Email"), m_email);
        authForm->addRow(QStringLiteral("Password"), m_password);
        auto* authBox = new QGroupBox(QStringLiteral("Accesso"));
        auto* authLay = new QVBoxLayout(authBox);
        authLay->addLayout(authForm);
        authLay->addWidget(m_remember);
        authLay->addWidget(m_login);
        authLay->addWidget(m_authState);

        auto* box = new QGroupBox(QStringLiteral("Stato"));
        auto* bl = new QVBoxLayout(box);
        bl->addWidget(m_status);
        bl->addWidget(m_stats);

        auto* lay = new QVBoxLayout(this);
        lay->addWidget(authBox);
        lay->addLayout(form);
        lay->addLayout(row);
        lay->addWidget(catBox);
        lay->addWidget(box);
        setMinimumWidth(520);

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
        // prossimo keepalive senza interrompere l'audio.
        if (m_running) sendRegister();
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
        if (!m_rig.open(port, m_catBaud->currentText().toInt())) {
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
                feedTx(dg.mid(kHdrSize));
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
                if (motivo.contains(QStringLiteral("scaduto")) && !m_password->text().isEmpty()) {
                    setStatus(QStringLiteral("token scaduto: lo rinnovo"));
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
        // cambiare il passo ai client che la parlano.
        quint8 const prof = profiloAttivo();
        int const campioni = (prof == dl::PPcm48) ? kFrame : dl::kOpusFrame;
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
                pkt = hfgwPacket(kFlagAudio, m_seq++, frame.constData(), frame.size());
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
        if (scelto == dl::PPcm48) return dl::PPcm48;
        return m_opusOut.pronto() ? scelto : dl::PPcm48;
    }

    // Quanti frame raggruppare adesso: quello scelto, ma uno solo se dall'altra
    // parte c'e' qualcuno che non ha dichiarato di saper leggere i pacchetti
    // aggregati. Risparmiare banda mandando un formato incomprensibile
    // significa non mandare niente.
    int aggrAttivo() const
    {
        if (!m_peerSaAggr) return 1;
        return qBound(1, m_aggr->currentData().toInt(), dl::kMaxAggr);
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
        if (prof != dl::PPcm48) {
            testo += QStringLiteral("   Opus %1 kbit/s").arg(m_opusOut.bitrate() / 1000);
            int const n = aggrAttivo();
            testo += (n > 1) ? QStringLiteral("   pacchetti da %1 ms").arg(n * 20)
                             : QStringLiteral("   un frame per pacchetto");
        }
        if (m_perditaVista > 0)
            testo += QStringLiteral("   perdita segnalata %1%").arg(m_perditaVista);
        m_stats->setText(testo);
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
        int const pi = m_profile->findData(s.value(QStringLiteral("profile"), dl::PVoce).toUInt());
        if (pi >= 0) m_profile->setCurrentIndex(pi);
        int const ai = m_aggr->findData(s.value(QStringLiteral("aggr"), 2).toInt());
        if (ai >= 0) m_aggr->setCurrentIndex(ai);
        m_catBaud->setCurrentText(s.value(QStringLiteral("catBaud"), QStringLiteral("38400")).toString());
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
        if (m_remember->isChecked())
            s.setValue(QStringLiteral("password"), m_password->text());
        else
            s.remove(QStringLiteral("password"));
        // Il token non si salva: dura un'ora e si riottiene al volo. Scriverlo
        // sul disco allungherebbe soltanto la vita a una credenziale rubata.
        s.setValue(QStringLiteral("device"), m_device->currentText());
        s.setValue(QStringLiteral("catPort"), m_catPort->currentText().section(QLatin1Char(' '), 0, 0));
        s.setValue(QStringLiteral("catBaud"), m_catBaud->currentText());
        s.setValue(QStringLiteral("catTcpPort"), m_catTcpPort->value());
        s.setValue(QStringLiteral("catOn"), m_catOn->isChecked());
        s.setValue(QStringLiteral("rigOut"), m_rigOut->currentText());
    }

    QComboBox *m_device, *m_mode, *m_station, *m_profile, *m_aggr;
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

    QComboBox *m_catPort, *m_catBaud;
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
    QList<QByteArray> m_daSpedire;   // frame in attesa di partire insieme
    // Si parte dal presupposto che l'altro capo non sappia leggere i pacchetti
    // raggruppati, e lo si scopre dal suo HELLO: meglio consumare piu' banda che
    // mandare a un client vecchio un formato che non capisce.
    bool m_peerSaAggr {false};

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

        out << "\nNota: non si riporta un rapporto segnale/rumore fra originale e\n"
               "ricostruito. Opus e' un codificatore percettivo e sposta la fase:\n"
               "un confronto campione per campione darebbe un numero pessimo anche\n"
               "quando l'audio e' ottimo, quindi sarebbe una misura falsa.\n"
               "La qualita' in fonia si giudica ascoltando; la banda si misura, ed e'\n"
               "quella che vedi qui sopra.\n";
        out.flush();
        return 0;
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
        if (!rig.open(port, baud)) { out << "apertura fallita: " << rig.error() << "\n"; out.flush(); return 6; }
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
