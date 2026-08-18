// hamlibrig.h — il rig comandato attraverso Hamlib, cioe' quasi tutte le radio.
//
// Fino a ieri qui dentro c'erano due protocolli scritti a mano: i comandi Yaesu
// e il CI-V degli Icom. Funzionano, ma coprono due marche. Hamlib ne conosce
// oltre trecento modelli, e li conosce meglio di quanto potremmo fare noi: sa
// quali comandi accetta ciascun apparato, come si comporta sul VFO, quali
// stranezze ha il singolo modello.
//
// E' la stessa libreria che usa Decodium sul desktop (Transceiver/HamlibTransceiver
// e src/radio/HamlibTransceiverLite): stessa versione, stesso modo di aprirla,
// stessi nomi dei modi. Chi ha gia' fatto funzionare la radio con Decodium
// ritrova qui gli stessi numeri.
//
// I due protocolli nativi restano: su un FT-991 o un IC-7300 gia' collaudati non
// c'e' motivo di aggiungere uno strato, e chi non ha Hamlib installato continua
// ad avere un programma che funziona.

#pragma once

#include <QElapsedTimer>
#include <QHostAddress>
#include <QHostInfo>
#include <QList>
#include <QPair>
#include <QString>
#include <QNetworkInterface>
#include <QStringList>
#include <QTcpSocket>

#include <cstring>

extern "C" {
#include <hamlib/rig.h>
}

namespace dl {

// Un modello, come lo elenca Hamlib.
struct ModelloRig {
    int numero;
    QString costruttore;
    QString modello;
    QString stato;        // "stabile", "beta", "alfa", "non funzionante"
    // Vero se si raggiunge per rete invece che sulla seriale. Sono i modelli che
    // permettono di condividere la radio: uno solo tiene la porta fisica — un
    // rigctld, FLRig, un altro programma — e tutti gli altri parlano con lui.
    // Senza, due programmi sulla stessa COM non ci stanno: la porta e' di chi
    // arriva primo.
    bool rete {false};
};

class HamlibRig
{
public:
    ~HamlibRig() { chiudi(); }

    // Tutti i modelli conosciuti, ordinati per costruttore. Il caricamento dei
    // backend avviene una volta sola: costa qualche decina di millisecondi e
    // farlo a ogni apertura della tendina si sentirebbe.
    static QList<ModelloRig> modelli()
    {
        static QList<ModelloRig> cache;
        if (!cache.isEmpty()) return cache;

        rig_set_debug(RIG_DEBUG_NONE);      // niente chiacchiere sullo standard error
        rig_load_all_backends();
        rig_list_foreach(&raccogli, &cache);

        std::sort(cache.begin(), cache.end(), [](ModelloRig const& a, ModelloRig const& b) {
            if (a.costruttore != b.costruttore) return a.costruttore < b.costruttore;
            return a.modello < b.modello;
        });
        return cache;
    }

    // Apre la radio. handshake: "nessuno", "hardware", "software".
    bool apri(int modello, const QString& porta, int baud,
              int bitDati = 8, int bitStop = 1, const QString& handshake = QString())
    {
        chiudi();
        rig_set_debug(RIG_DEBUG_NONE);
        rig_load_all_backends();

        m_rig = rig_init(rig_model_t(modello));
        if (!m_rig) { m_errore = QStringLiteral("modello %1 sconosciuto a Hamlib").arg(modello); return false; }

        // I parametri della porta si scrivono nella struttura prima di aprire:
        // Hamlib usa i suoi valori predefiniti per il modello, e vanno
        // sovrascritti solo se l'utente ha chiesto qualcosa di diverso.
        // Per i modelli di rete il "percorso" e' un indirizzo: localhost:4532
        // per un rigctld, oppure host:porta di FLRig. I parametri della seriale
        // non c'entrano niente e non vanno toccati.
        m_perRete = (m_rig->caps->port_type == RIG_PORT_NETWORK
                     || m_rig->caps->port_type == RIG_PORT_UDP_NETWORK);

        // Con una radio in rete si bussa prima, e con un'attesa decisa da noi:
        // rig_open su un indirizzo che non risponde tiene fermo il programma
        // ventuno secondi, e chi guarda vede una finestra morta.
        //
        // Vale solo per il TCP: l'UDP non si connette, non c'e' porta a cui
        // bussare, e un tentativo andrebbe a vuoto sempre.
        if (m_perRete && m_rig->caps->port_type == RIG_PORT_NETWORK) {
            QString perche;
            if (!rispondeQualcuno(porta, kAttesaRete, &perche)) {
                m_errore = perche;
                rig_cleanup(m_rig);
                m_rig = nullptr;
                return false;
            }
        }

        QByteArray const p = porta.toLocal8Bit();
        std::strncpy(m_rig->state.rigport.pathname, p.constData(), HAMLIB_FILPATHLEN - 1);
        if (m_perRete) {
            // Sulle letture il tempo lo si puo' accorciare, e conviene: dopo
            // l'apertura il client interroga la radio ogni due secondi, sempre
            // dal thread dell'interfaccia. Con i valori di fabbrica una radio
            // che smette di rispondere blocca la finestra a ogni giro.
            m_rig->state.rigport.timeout = kTimeoutRete;
            m_rig->state.rigport.retry = 1;
        }
        if (!m_perRete && baud > 0) {
            m_rig->state.rigport.parm.serial.rate = baud;
            m_rig->state.rigport.parm.serial.data_bits = bitDati;
            m_rig->state.rigport.parm.serial.stop_bits = bitStop;
            m_rig->state.rigport.parm.serial.parity = RIG_PARITY_NONE;
            m_rig->state.rigport.parm.serial.handshake =
                handshake.startsWith(QLatin1Char('h'), Qt::CaseInsensitive) ? RIG_HANDSHAKE_HARDWARE
                : handshake.startsWith(QLatin1Char('s'), Qt::CaseInsensitive) ? RIG_HANDSHAKE_XONXOFF
                                                                             : RIG_HANDSHAKE_NONE;
        }

        int const err = rig_open(m_rig);
        if (err != RIG_OK) {
            m_errore = spiega(err);
            rig_cleanup(m_rig);
            m_rig = nullptr;
            return false;
        }
        m_nome = QString::fromLatin1(m_rig->caps->mfg_name) + QLatin1Char(' ')
                 + QString::fromLatin1(m_rig->caps->model_name);
        return true;
    }

    void chiudi()
    {
        if (m_rig) { rig_close(m_rig); rig_cleanup(m_rig); m_rig = nullptr; }
    }

    bool aperto() const { return m_rig != nullptr; }
    bool perRete() const { return m_perRete; }
    QString errore() const { return m_errore; }
    QString nome() const { return m_nome; }

    // Se il modello indicato si raggiunge per rete. Serve all'interfaccia per
    // chiedere un indirizzo invece di una porta COM.
    static bool modelloPerRete(int numero)
    {
        for (ModelloRig const& r : modelli())
            if (r.numero == numero) return r.rete;
        return false;
    }

    // La porta su cui parla un rigctld quando non se ne indica una: e' quella
    // che usa Hamlib se l'indirizzo e' scritto senza i due punti.
    static constexpr quint16 kPortaRigctld = 4532;

    // Quanto si aspetta un programma che tiene la radio. Un rigctld sulla stessa
    // macchina risponde in un millesimo; uno in casa, sul WiFi, in qualche
    // decina. Un secondo e mezzo e' larghissimo per entrambi e non congela
    // niente se dall'altra parte non c'e' nessuno.
    static constexpr int kAttesaRete = 1500;
    static constexpr int kTimeoutRete = 1000;   // sulle letture, dopo l'apertura

    // Il messaggio di Hamlib, ridotto a quello che serve.
    //
    // rigerror() in Hamlib 4.7 non restituisce una frase: restituisce il
    // registro di debug accumulato, venti righe di netrigctl_transaction e
    // read_string_generic con in fondo il motivo vero. Messo in un'etichetta
    // e' un muro di testo che nasconde l'unica riga che l'utente puo' capire.
    static QString spiega(int err)
    {
        QString const tutto = QString::fromLatin1(rigerror(err)).trimmed();
        if (tutto.isEmpty()) return QObject::tr("errore %1 di Hamlib").arg(err);
        // L'ultima riga non vuota e' il motivo; il resto e' il come ci si e'
        // arrivati, che interessa a chi scrive Hamlib e non a chi usa la radio.
        QStringList const righe = tutto.split(QLatin1Char('\n'), Qt::SkipEmptyParts);
        for (int i = righe.size() - 1; i >= 0; --i) {
            QString const r = righe.at(i).trimmed();
            if (r.isEmpty() || r.endsWith(QLatin1Char(')')) || r.contains(QLatin1String("():")))
                continue;
            return r;
        }
        return righe.last().trimmed();
    }

    // Spezza "host:porta" in due. Gestisce anche la forma con le parentesi
    // quadre, [::1]:4532, perche' in un indirizzo IPv6 i due punti ci sono gia'
    // dentro e cercare l'ultimo non basterebbe.
    static QPair<QString, quint16> dividiIndirizzo(const QString& testo,
                                                   quint16 predefinita = kPortaRigctld)
    {
        QString s = testo.trimmed();
        if (s.isEmpty()) return {QString(), predefinita};

        if (s.startsWith(QLatin1Char('['))) {
            int const chiusa = s.indexOf(QLatin1Char(']'));
            if (chiusa > 0) {
                QString const host = s.mid(1, chiusa - 1);
                QString const resto = s.mid(chiusa + 1);
                if (resto.startsWith(QLatin1Char(':'))) {
                    bool ok = false;
                    quint16 const p = quint16(resto.mid(1).toUInt(&ok));
                    return {host, (ok && p) ? p : predefinita};
                }
                return {host, predefinita};
            }
        }
        int const duePunti = s.lastIndexOf(QLatin1Char(':'));
        // Piu' di un due punti senza parentesi quadre: e' un IPv6 nudo, che di
        // porta non ne porta.
        if (duePunti < 0 || s.count(QLatin1Char(':')) > 1) return {s, predefinita};
        bool ok = false;
        quint16 const p = quint16(s.mid(duePunti + 1).toUInt(&ok));
        return {s.left(duePunti), (ok && p) ? p : predefinita};
    }

    // Se questo host e' la macchina su cui stiamo girando.
    //
    // La stessa macchina si scrive in molti modi: localhost, 127.0.0.1, ::1, il
    // nome del computer, un indirizzo della propria scheda di rete. Servono
    // tutti, perche' basta che ne sfugga uno per lasciar partire un
    // collegamento a se stessi — che non fallisce: si pianta.
    static bool indirizzoLocale(const QString& host)
    {
        QString const h = host.trimmed();
        if (h.isEmpty()) return true;      // niente host: e' la macchina locale
        if (h.compare(QLatin1String("localhost"), Qt::CaseInsensitive) == 0) return true;

        QHostAddress ind(h);
        if (!ind.isNull()) {
            if (ind.isLoopback()) return true;
            for (QHostAddress const& mio : QNetworkInterface::allAddresses())
                if (mio.isEqual(ind, QHostAddress::TolerantConversion)) return true;
            return false;
        }
        // Un nome, non un indirizzo: il nostro lo si riconosce senza chiedere al
        // DNS, che qui costerebbe un'attesa per una domanda di cui sappiamo gia'
        // la risposta.
        QString const nostro = QHostInfo::localHostName();
        return !nostro.isEmpty()
               && (h.compare(nostro, Qt::CaseInsensitive) == 0
                   || h.startsWith(nostro + QLatin1Char('.'), Qt::CaseInsensitive));
    }

    // Bussa alla porta prima di chiamare Hamlib.
    //
    // Serve perche' rig_open, se dall'altra parte non risponde nessuno, resta
    // fermo ventuno secondi: e' il tempo che Windows impiega a rinunciare a un
    // TCP che non risponde, e Hamlib non lo puo' accorciare — timeout e retry
    // della sua struttura valgono sulle letture, non sulla connessione. Ventuno
    // secondi dentro il thread dell'interfaccia sono una finestra ghiacciata e
    // Windows che propone di chiudere il programma: da fuori si vede un crash.
    //
    // Qui il tempo lo decidiamo noi, e se non c'e' nessuno si rinuncia subito.
    static bool rispondeQualcuno(const QString& indirizzo, int msAttesa, QString* perche)
    {
        QPair<QString, quint16> const dove = dividiIndirizzo(indirizzo);
        if (dove.first.isEmpty()) {
            if (perche) *perche = QObject::tr("indirizzo vuoto");
            return false;
        }
        QTcpSocket prova;
        prova.connectToHost(dove.first, dove.second);
        if (!prova.waitForConnected(msAttesa)) {
            if (perche) {
                *perche = (prova.error() == QAbstractSocket::SocketTimeoutError
                           || prova.state() == QAbstractSocket::ConnectingState)
                    ? QObject::tr("nessuna risposta da %1:%2").arg(dove.first).arg(dove.second)
                    : QObject::tr("%1:%2 — %3").arg(dove.first).arg(dove.second)
                          .arg(prova.errorString());
            }
            prova.abort();
            return false;
        }
        prova.disconnectFromHost();
        return true;
    }

    qint64 frequenza()
    {
        if (!m_rig) return 0;
        freq_t f = 0;
        int const err = rig_get_freq(m_rig, RIG_VFO_CURR, &f);
        if (err != RIG_OK) { m_errore = QString::fromLatin1(rigerror(err)); return 0; }
        return qint64(f);
    }

    bool impostaFrequenza(qint64 hz)
    {
        if (!m_rig) return false;
        int const err = rig_set_freq(m_rig, RIG_VFO_CURR, freq_t(hz));
        if (err != RIG_OK) { m_errore = QString::fromLatin1(rigerror(err)); return false; }
        return true;
    }

    // I nomi dei modi sono quelli di Hamlib, che sono anche quelli che usano
    // rigctl e i programmi che ci parlano: USB, LSB, CW, CWR, RTTY, PKTUSB...
    QString modo()
    {
        if (!m_rig) return QString();
        rmode_t m = RIG_MODE_NONE;
        pbwidth_t larghezza = 0;
        int const err = rig_get_mode(m_rig, RIG_VFO_CURR, &m, &larghezza);
        if (err != RIG_OK) { m_errore = QString::fromLatin1(rigerror(err)); return QString(); }
        m_larghezza = qint64(larghezza);
        return QString::fromLatin1(rig_strrmode(m));
    }

    qint64 larghezza() const { return m_larghezza; }

    bool impostaModo(const QString& nome, qint64 larghezzaHz = 0)
    {
        if (!m_rig) return false;
        rmode_t const m = rig_parse_mode(nome.toLatin1().constData());
        if (m == RIG_MODE_NONE) {
            m_errore = QStringLiteral("modo sconosciuto: %1").arg(nome);
            return false;
        }
        // Larghezza non indicata significa "quella normale per questo modo su
        // questa radio", che e' RIG_PASSBAND_NORMAL: la sceglie Hamlib, che sa
        // cosa accetta il singolo apparato.
        //
        // Non NOCHANGE: con una radio condivisa in rete quel valore fa cadere il
        // comando per strada — il modo non arrivava affatto, e nessuno se ne
        // accorgeva perche' la chiamata tornava senza errore.
        int const err = rig_set_mode(m_rig, RIG_VFO_CURR, m,
                                     larghezzaHz > 0 ? pbwidth_t(larghezzaHz)
                                                     : RIG_PASSBAND_NORMAL);
        if (err != RIG_OK) { m_errore = QString::fromLatin1(rigerror(err)); return false; }
        return true;
    }

    bool inTrasmissione()
    {
        if (!m_rig) return false;
        ptt_t p = RIG_PTT_OFF;
        if (rig_get_ptt(m_rig, RIG_VFO_CURR, &p) != RIG_OK) return false;
        return p != RIG_PTT_OFF;
    }

    bool trasmetti(bool on)
    {
        if (!m_rig) return false;
        int const err = rig_set_ptt(m_rig, RIG_VFO_CURR, on ? RIG_PTT_ON : RIG_PTT_OFF);
        if (err != RIG_OK) { m_errore = QString::fromLatin1(rigerror(err)); return false; }
        return true;
    }

    // ------------------------------------------------------------ misuratori
    //
    // ALC, ROS e potenza sono quello che si guarda mentre si trasmette, ed e'
    // proprio quello che manca a chi opera da remoto: senza, si manda in aria
    // una radio di cui non si vede ne' quanto sta erogando ne' se l'antenna
    // sta rispondendo.
    //
    // Hamlib li chiama «livelli» e non tutte le radio li hanno: si chiede prima
    // se questo apparato sa rispondere, invece di interrogarlo e prendersi un
    // errore per qualcosa che non ha mai avuto.
    bool haLivello(setting_t quale) const
    {
        if (!m_rig) return false;
        if (rig_has_get_level(m_rig, quale)) return true;
        // Con una radio in rete l'elenco delle capacita' arriva dal
        // \dump_state di chi sta dall'altra parte, e non tutti lo compilano:
        // un server che dimentica di dichiarare i misuratori li rende
        // invisibili, anche quando risponderebbe benissimo. Meglio provare a
        // chiedere e prendersi un rifiuto — costa una domanda — che dare per
        // scontato un «non ce l'ho» che nessuno ha davvero detto.
        return m_perRete;
    }

    // Il valore grezzo di un livello. Torna false se la radio non lo espone o
    // se la lettura fallisce: chi chiama deve poter distinguere «zero» da
    // «non lo so», che su un misuratore sono due cose diverse.
    bool livello(setting_t quale, float& fuori)
    {
        if (!m_rig || !haLivello(quale)) return false;
        value_t v;
        std::memset(&v, 0, sizeof(v));
        int const err = rig_get_level(m_rig, RIG_VFO_CURR, quale, &v);
        if (err != RIG_OK) { m_errore = spiega(err); return false; }
        // I livelli dei misuratori sono float; STRENGTH e' l'eccezione, e la
        // gestisce chi la chiede.
        fuori = v.f;
        return true;
    }

    bool livelloIntero(setting_t quale, int& fuori)
    {
        if (!m_rig || !haLivello(quale)) return false;
        value_t v;
        std::memset(&v, 0, sizeof(v));
        int const err = rig_get_level(m_rig, RIG_VFO_CURR, quale, &v);
        if (err != RIG_OK) { m_errore = spiega(err); return false; }
        fuori = v.i;
        return true;
    }

    static QString versione() { return QString::fromLatin1(hamlib_version); }

private:
    static int raccogli(const struct rig_caps* c, void* dove)
    {
        auto* elenco = static_cast<QList<ModelloRig>*>(dove);
        QString stato;
        switch (c->status) {
        case RIG_STATUS_STABLE:  stato = QStringLiteral("stabile"); break;
        case RIG_STATUS_BETA:    stato = QStringLiteral("beta"); break;
        case RIG_STATUS_ALPHA:   stato = QStringLiteral("alfa"); break;
        case RIG_STATUS_UNTESTED: stato = QStringLiteral("mai provato"); break;
        default:                 stato = QStringLiteral("non funzionante"); break;
        }
        bool const perRete = (c->port_type == RIG_PORT_NETWORK
                              || c->port_type == RIG_PORT_UDP_NETWORK);
        elenco->append({ int(c->rig_model),
                         QString::fromLatin1(c->mfg_name),
                         QString::fromLatin1(c->model_name),
                         stato, perRete });
        return 1;   // continua a scorrere
    }

    RIG* m_rig {nullptr};
    QString m_errore, m_nome;
    qint64 m_larghezza {0};
    bool m_perRete {false};
};

} // namespace dl
