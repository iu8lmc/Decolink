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

#include <QList>
#include <QString>
#include <QStringList>

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
        QByteArray const p = porta.toLocal8Bit();
        std::strncpy(m_rig->state.rigport.pathname, p.constData(), HAMLIB_FILPATHLEN - 1);
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
            m_errore = QString::fromLatin1(rigerror(err));
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
