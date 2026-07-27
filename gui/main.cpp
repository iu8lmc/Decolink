// hfgw-client — client audio HF con finestra, protocollo HFGW v1.
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
#include <QAudioDevice>
#include <QAudioFormat>
#include <QAudioSource>
#include <QComboBox>
#include <QDateTime>
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
#include <QSettings>
#include <QSpinBox>
#include <QTextStream>
#include <QTimer>
#include <QUdpSocket>
#include <QVBoxLayout>
#include <QWidget>

#include <cmath>

namespace {

constexpr int kRate      = 48000;
constexpr int kFrame     = kRate / 100;   // 480 campioni = 10 ms
constexpr int kHdrSize   = 22;
constexpr quint8 kFlagAudio = 0, kFlagPing = 1, kFlagPong = 2,
                 kFlagRegister = 3, kFlagPeerUp = 4;

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

class Client : public QWidget
{
    Q_OBJECT
public:
    Client()
    {
        setWindowTitle(QStringLiteral("HF Gateway — audio della radio verso Decodium Mobile"));

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

        auto* box = new QGroupBox(QStringLiteral("Stato"));
        auto* bl = new QVBoxLayout(box);
        bl->addWidget(m_status);
        bl->addWidget(m_stats);

        auto* lay = new QVBoxLayout(this);
        lay->addLayout(form);
        lay->addLayout(row);
        lay->addWidget(box);
        setMinimumWidth(520);

        connect(m_start, &QPushButton::clicked, this, [this]{ m_running ? stop() : start(); });
        connect(m_mode, &QComboBox::currentIndexChanged, this, &Client::syncFields);

        // registrazione periodica alla stanza / keepalive verso casa
        m_keepAlive.setInterval(5000);
        connect(&m_keepAlive, &QTimer::timeout, this, &Client::sendRegister);
        // aggiornamento contatori
        m_uiTimer.setInterval(500);
        connect(&m_uiTimer, &QTimer::timeout, this, &Client::refreshStats);
        m_uiTimer.start();

        loadSettings();
        syncFields();
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
            } else if (flags == kFlagPeerUp) {
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

    void refreshStats()
    {
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
        QSettings s(QStringLiteral("it.ft2"), QStringLiteral("hfgw-client"));
        m_mode->setCurrentIndex(s.value(QStringLiteral("mode"), 0).toInt());
        m_host->setText(s.value(QStringLiteral("host")).toString());
        m_port->setValue(s.value(QStringLiteral("port"), 5555).toInt());
        m_room->setText(s.value(QStringLiteral("room")).toString());
        QString const dev = s.value(QStringLiteral("device")).toString();
        int const i = m_device->findText(dev);
        if (i >= 0) m_device->setCurrentIndex(i);
    }

    void saveSettings()
    {
        QSettings s(QStringLiteral("it.ft2"), QStringLiteral("hfgw-client"));
        s.setValue(QStringLiteral("mode"), m_mode->currentIndex());
        s.setValue(QStringLiteral("host"), m_host->text());
        s.setValue(QStringLiteral("port"), m_port->value());
        s.setValue(QStringLiteral("room"), m_room->text());
        s.setValue(QStringLiteral("device"), m_device->currentText());
    }

    QComboBox *m_device, *m_mode;
    QLineEdit *m_host, *m_room;
    QSpinBox* m_port;
    QPushButton* m_start;
    QProgressBar* m_level;
    QLabel *m_status, *m_stats;

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
        out.flush();
        return ins.isEmpty() ? 2 : 0;
    }

    Client w;
    w.show();
    return app.exec();
}
