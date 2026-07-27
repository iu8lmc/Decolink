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
#include <QLabel>
#include <QLineEdit>
#include <QMediaDevices>
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

#include <cmath>

namespace {

constexpr int kRate      = 48000;
constexpr int kFrame     = kRate / 100;   // 480 campioni = 10 ms
constexpr int kHdrSize   = 22;
constexpr quint8 kFlagAudio = 0, kFlagPing = 1, kFlagPong = 2,
                 kFlagRegister = 3, kFlagPeerUp = 4,
                 kFlagCatReq = 5, kFlagCatRsp = 6,   // comandi CAT sullo stesso canale
                 kFlagTxAudio = 7;                   // audio che il telefono vuole trasmettere

void putU32(char* p, quint32 v) { p[0]=char(v>>24); p[1]=char(v>>16); p[2]=char(v>>8); p[3]=char(v); }
void putU64(char* p, quint64 v) { for (int i = 0; i < 8; ++i) p[i] = char(v >> (56 - 8*i)); }
quint32 getU32(const uchar* p) { return (quint32(p[0])<<24)|(quint32(p[1])<<16)|(quint32(p[2])<<8)|p[3]; }

QByteArray hfgwPacket(quint8 flags, quint32 seq, const char* payload, int len)
{
    QByteArray pkt(kHdrSize + qMax(0, len), Qt::Uninitialized);
    char* p = pkt.data();
    std::memcpy(p, "HFGW", 4);
    p[4] = 1; p[5] = char(flags);
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
        m_room = new QLineEdit;
        m_room->setPlaceholderText(QStringLiteral("codice stanza condiviso col telefono"));

        auto* form = new QFormLayout;
        form->addRow(QStringLiteral("Audio della radio"), m_device);
        form->addRow(QStringLiteral("Modalità"), m_mode);
        form->addRow(QStringLiteral("Host"), m_host);
        form->addRow(QStringLiteral("Porta"), m_port);
        form->addRow(QStringLiteral("Stanza"), m_room);

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

        auto* box = new QGroupBox(QStringLiteral("Stato"));
        auto* bl = new QVBoxLayout(box);
        bl->addWidget(m_status);
        bl->addWidget(m_stats);

        auto* lay = new QVBoxLayout(this);
        lay->addLayout(form);
        lay->addLayout(row);
        lay->addWidget(catBox);
        lay->addWidget(box);
        setMinimumWidth(520);

        connect(m_start, &QPushButton::clicked, this, [this]{ m_running ? stop() : start(); });
        connect(m_mode, &QComboBox::currentIndexChanged, this, &Client::syncFields);
        connect(m_catOn, &QCheckBox::toggled, this, &Client::toggleCat);
        m_catPoll.setInterval(2000);
        connect(&m_catPoll, &QTimer::timeout, this, &Client::refreshCatState);

        // registrazione periodica alla stanza / keepalive verso casa
        m_keepAlive.setInterval(5000);
        connect(&m_keepAlive, &QTimer::timeout, this, &Client::sendRegister);
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
        // per lasciarlo acceso in stazione senza doverci tornare sopra.
        if (args.contains(QStringLiteral("--start")))
            QTimer::singleShot(300, this, [this] { if (!m_running) start(); });
    }

    ~Client() override { saveSettings(); }

private slots:
    void syncFields()
    {
        int const m = m_mode->currentIndex();
        m_host->setEnabled(m != ModeListen);
        m_room->setEnabled(m == ModeRelay);
        switch (m) {
        case ModeLan:
            m_host->setPlaceholderText(QStringLiteral("IP del telefono sulla rete locale"));
            break;
        case ModeRelay:
            m_host->setPlaceholderText(QStringLiteral("host del relay (es. community.ft2.it)"));
            break;
        default:
            m_host->setPlaceholderText(QStringLiteral("(il telefono chiama questa porta)"));
            break;
        }
    }

    void sendRegister()
    {
        if (!m_running || !m_sock) return;
        if (m_mode->currentIndex() != ModeRelay) return;
        QByteArray const room = m_room->text().trimmed().toUtf8();
        m_sock->writeDatagram(hfgwPacket(kFlagRegister, 0, room.constData(), room.size()),
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
            if (flags == kFlagPeerUp) {
                setStatus(QStringLiteral("il telefono è entrato nella stanza"));
            } else if (flags == kFlagRegister) {
                setStatus(QStringLiteral("registrato sul relay"));
            }
        }
    }

    void onAudioReady()
    {
        if (!m_audioIo) return;
        m_acc += m_audioIo->readAll();
        int const frameBytes = kFrame * 2;
        while (m_acc.size() >= frameBytes) {
            QByteArray const frame = m_acc.left(frameBytes);
            m_acc.remove(0, frameBytes);

            // livello (RMS) per la barra
            const short* s = reinterpret_cast<const short*>(frame.constData());
            double sum = 0;
            for (int i = 0; i < kFrame; ++i) { double v = s[i] / 32768.0; sum += v * v; }
            m_rms = 0.8 * m_rms + 0.2 * std::sqrt(sum / kFrame);

            if (!targetReady()) continue;      // nessun destinatario: non spedisco
            m_sock->writeDatagram(hfgwPacket(kFlagAudio, m_seq++, frame.constData(), frame.size()),
                                  m_dstAddr, m_dstPort);
            ++m_sent;
        }
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
        m_stats->setText(QStringLiteral("pacchetti inviati: %1   (%2 al secondo attesi: 100)")
                             .arg(m_sent).arg(m_seq ? QStringLiteral("in corso") : QStringLiteral("in attesa")));
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
        if (m == ModeRelay && m_room->text().trimmed().isEmpty()) {
            setStatus(QStringLiteral("manca il codice stanza")); return;
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
        if (on) syncFields(); else { m_host->setEnabled(false); m_room->setEnabled(false); }
    }

    void loadSettings()
    {
        QSettings s(QStringLiteral("it.ft2"), QStringLiteral("Decolink"));
        m_mode->setCurrentIndex(s.value(QStringLiteral("mode"), 0).toInt());
        m_host->setText(s.value(QStringLiteral("host")).toString());
        m_port->setValue(s.value(QStringLiteral("port"), 5555).toInt());
        m_room->setText(s.value(QStringLiteral("room")).toString());
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
        s.setValue(QStringLiteral("room"), m_room->text());
        s.setValue(QStringLiteral("device"), m_device->currentText());
        s.setValue(QStringLiteral("catPort"), m_catPort->currentText().section(QLatin1Char(' '), 0, 0));
        s.setValue(QStringLiteral("catBaud"), m_catBaud->currentText());
        s.setValue(QStringLiteral("catTcpPort"), m_catTcpPort->value());
        s.setValue(QStringLiteral("catOn"), m_catOn->isChecked());
        s.setValue(QStringLiteral("rigOut"), m_rigOut->currentText());
    }

    QComboBox *m_device, *m_mode;
    QLineEdit *m_host, *m_room;
    QSpinBox* m_port;
    QPushButton* m_start;
    QProgressBar* m_level;
    QLabel *m_status, *m_stats;

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
