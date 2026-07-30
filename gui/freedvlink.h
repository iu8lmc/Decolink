// freedvlink.h — il collegamento che non passa da internet.
//
// Quando la linea cade — non perche' manca la propagazione, ma perche' manca
// internet — il trasporto diventa la radio. Qui dentro c'e' FreeDV: modem OFDM e
// voce Codec2, entrambi da libcodec2, senza programmi di terze parti.
//
// Numeri veri, per capire di cosa si sta parlando:
//
//   voce FreeDV 700E   700 bit/s, ~1,1 kHz occupati, robusto sul fading
//   voce FreeDV 700D   700 bit/s, un po' meno robusto ma piu' sensibile
//   dati DATAC3        ~320 bit/s, per i comandi al rig
//
// Settecento bit al secondo sono mille volte meno del PCM. La voce che ne esce e'
// intelligibile, non bella: si capisce un nominativo e un rapporto, non si
// riconosce chi parla. E' il compromesso che rende possibile comandare una
// stazione quando l'alternativa e' niente.
//
// LE DUE COSE CHE NON SI POSSONO AGGIRARE
//
// 1. Serve un secondo apparato, da entrambi i lati. La radio che si sta
//    remotizzando non puo' fare contemporaneamente da modem per il collegamento
//    che la comanda: mentre trasmette i dati del link non e' disponibile per
//    operare. In pratica: un QRP su una banda diversa.
//
// 2. Il canale e' uno solo e half-duplex, come qualunque collegamento radio: o si
//    parla, o si comandano. Non c'e' modo di far stare voce e dati insieme in 700
//    bit/s, e nessuna compressione lo cambiera'.
//
// I modi digitali via HF non ci stanno affatto: FT8 dentro questa banda e'
// impossibile. In emergenza si comanda la radio e si parla.

#pragma once

#include <QByteArray>
#include <QString>
#include <QVector>

extern "C" {
#include <codec2/freedv_api.h>
}

namespace dl {

// Cosa sta facendo il collegamento in questo momento. Il canale e' uno solo,
// quindi lo stato e' esclusivo: e' questo che rende il profilo half-duplex.
enum class UsoEmrg { Voce, Dati };

class FreeDvLink
{
public:
    ~FreeDvLink() { chiudi(); }

    // modoVoce: FREEDV_MODE_700E (robusto, consigliato) o 700D.
    // modoDati: FREEDV_MODE_DATAC3 per i comandi, lento ma tiene con poca S/N.
    bool apri(int modoVoce = FREEDV_MODE_700E, int modoDati = FREEDV_MODE_DATAC3)
    {
        chiudi();
        m_voce = freedv_open(modoVoce);
        if (!m_voce) { m_errore = QStringLiteral("FreeDV: modo voce non disponibile"); return false; }
        m_dati = freedv_open(modoDati);
        if (!m_dati) {
            m_errore = QStringLiteral("FreeDV: modo dati non disponibile");
            chiudi();
            return false;
        }
        // Limitare l'ampiezza in trasmissione: un modem che satura l'ingresso
        // del rig produce prodotti di intermodulazione e sporca la banda dei
        // vicini, che in emergenza sono le persone che ti stanno aiutando.
        freedv_set_clip(m_voce, true);
        freedv_set_tx_bpf(m_voce, 1);
        freedv_set_clip(m_dati, true);
        freedv_set_tx_bpf(m_dati, 1);
        // Un burst per volta: i comandi sono brevi e conviene che ognuno stia in
        // piedi da solo, cosi' se uno si perde si ripete quello e non la sequenza.
        freedv_set_frames_per_burst(m_dati, 1);
        return true;
    }

    void chiudi()
    {
        if (m_voce) { freedv_close(m_voce); m_voce = nullptr; }
        if (m_dati) { freedv_close(m_dati); m_dati = nullptr; }
    }

    bool pronto() const { return m_voce && m_dati; }
    QString errore() const { return m_errore; }

    // ---- misure dichiarate dalla libreria, non stimate da noi ----
    int campioniVoce() const { return m_voce ? freedv_get_n_speech_samples(m_voce) : 0; }
    int campioniModem() const { return m_voce ? freedv_get_n_nom_modem_samples(m_voce) : 0; }
    int frequenzaModem() const { return m_voce ? freedv_get_modem_sample_rate(m_voce) : 8000; }
    int frequenzaVoce() const { return m_voce ? freedv_get_speech_sample_rate(m_voce) : 8000; }
    int bitPerFrameDati() const { return m_dati ? freedv_get_bits_per_modem_frame(m_dati) : 0; }
    int bytePerFrameDati() const { return bitPerFrameDati() / 8; }
    // Gli ultimi due byte del frame dati sono il CRC che la libreria verifica: i
    // byte utili sono quelli che restano. Ignorarlo era il motivo per cui i
    // comandi partivano e non arrivava niente — venivano scartati all'arrivo
    // perche' il controllo non tornava.
    int byteUtiliDati() const { return qMax(0, bytePerFrameDati() - 2); }

    // freedv_get_rx_status dice piu' cose di freedv_get_sync: distingue "sono
    // agganciato" da "ho consegnato dei bit", e la seconda e' quella che conta.
    bool sincronizzato() const
    {
        return m_voce && (freedv_get_rx_status(m_voce) & FREEDV_RX_SYNC) != 0;
    }
    bool haConsegnatoVoce() const
    {
        return m_voce && (freedv_get_rx_status(m_voce) & FREEDV_RX_BITS) != 0;
    }
    bool sincronizzatoDati() const
    {
        return m_dati && (freedv_get_rx_status(m_dati) & FREEDV_RX_SYNC) != 0;
    }

    // ---- voce ----

    // Un frame di voce a 8 kHz diventa audio da mandare alla radio del link.
    QVector<qint16> vocePerRadio(const qint16* voce8k)
    {
        QVector<qint16> out;
        if (!m_voce) return out;
        out.resize(freedv_get_n_nom_modem_samples(m_voce));
        freedv_tx(m_voce, out.data(), const_cast<short*>(voce8k));
        return out;
    }

    // Audio ricevuto dalla radio del link -> voce. Restituisce i campioni
    // ottenuti: vuoto finche' il modem non si e' agganciato, ed e' normale che
    // ci voglia qualche decimo di secondo.
    QVector<qint16> voceDaRadio(const qint16* modem, int n)
    {
        QVector<qint16> out;
        if (!m_voce || n <= 0) return out;
        m_coda.append(reinterpret_cast<const char*>(modem), n * 2);

        int const maxVoce = freedv_get_n_speech_samples(m_voce);
        while (true) {
            int const servono = freedv_nin(m_voce);
            if (servono <= 0 || m_coda.size() < servono * 2) break;
            QVector<qint16> pezzo(maxVoce);
            int const resi = freedv_rx(m_voce, pezzo.data(),
                                       reinterpret_cast<short*>(m_coda.data()));
            m_coda.remove(0, servono * 2);
            if (resi > 0) {
                pezzo.resize(resi);
                out.append(pezzo);
            }
        }
        return out;
    }

    // ---- dati: comandi al rig e stato della stazione ----

    // Impacchetta un comando in uno o piu' frame dati e restituisce l'audio da
    // trasmettere, preambolo compreso. Il preambolo serve perche' il demodulatore
    // dall'altra parte si agganci: senza, i primi frame andrebbero persi.
    QVector<qint16> datiPerRadio(const QByteArray& testo)
    {
        QVector<qint16> out;
        if (!m_dati) return out;
        int const perFrame = bytePerFrameDati();
        int const utili = byteUtiliDati();
        if (utili <= 0) return out;

        QVector<qint16> pre(qMax(freedv_get_n_tx_preamble_modem_samples(m_dati),
                                 freedv_get_n_tx_modem_samples(m_dati)));
        int const nPre = freedv_rawdatapreambletx(m_dati, pre.data());
        if (nPre > 0) { pre.resize(nPre); out.append(pre); }

        for (int off = 0; off < testo.size(); off += utili) {
            QByteArray blocco = testo.mid(off, utili);
            blocco.append(QByteArray(utili - blocco.size(), '\0'));   // riempimento
            // CRC16 in coda, come lo aspetta il demodulatore.
            quint16 const crc = freedv_gen_crc16(
                reinterpret_cast<unsigned char*>(blocco.data()), utili);
            blocco.append(char((crc >> 8) & 0xFF));
            blocco.append(char(crc & 0xFF));
            Q_ASSERT(blocco.size() == perFrame);

            QVector<qint16> frame(freedv_get_n_tx_modem_samples(m_dati));
            freedv_rawdatatx(m_dati, frame.data(),
                             reinterpret_cast<unsigned char*>(blocco.data()));
            out.append(frame);
        }

        QVector<qint16> post(qMax(freedv_get_n_tx_postamble_modem_samples(m_dati),
                                  freedv_get_n_tx_modem_samples(m_dati)));
        int const nPost = freedv_rawdatapostambletx(m_dati, post.data());
        if (nPost > 0) { post.resize(nPost); out.append(post); }

        // Mezzo secondo di silenzio in coda, e non e' un dettaglio estetico: il
        // decodificatore a correzione d'errore lavora con ritardo, e senza
        // qualcosa da masticare dopo il burst l'ultimo frame gli resta dentro.
        // E' il motivo per cui i comandi partivano e non arrivava niente.
        out.append(QVector<qint16>(freedv_get_modem_sample_rate(m_dati) / 2, 0));
        return out;
    }

    // Audio dalla radio -> byte dei comandi. Restituisce solo i frame arrivati
    // senza errori: il codice a correzione dentro DATAC3 li scarta da solo se
    // sono rotti, e un comando CAT a metà sarebbe peggio di un comando mancante.
    QByteArray datiDaRadio(const qint16* modem, int n)
    {
        QByteArray out;
        if (!m_dati || n <= 0) return out;
        m_codaDati.append(reinterpret_cast<const char*>(modem), n * 2);

        int const perFrame = bytePerFrameDati();
        int const utili = byteUtiliDati();
        if (utili <= 0) return out;
        while (true) {
            int const servono = freedv_nin(m_dati);
            if (servono <= 0 || m_codaDati.size() < servono * 2) break;
            QByteArray blocco(perFrame + 8, '\0');
            int const resi = freedv_rawdatarx(m_dati,
                                              reinterpret_cast<unsigned char*>(blocco.data()),
                                              reinterpret_cast<short*>(m_codaDati.data()));
            m_codaDati.remove(0, servono * 2);
            // Si consegnano solo i byte utili: il CRC ha già fatto il suo lavoro
            // e non serve a chi legge il comando.
            if (resi > 0) out.append(blocco.left(qMin(resi, perFrame)).left(utili));
        }
        return out;
    }

    void azzera()
    {
        m_coda.clear();
        m_codaDati.clear();
        if (m_voce) freedv_set_sync(m_voce, FREEDV_SYNC_UNSYNC);
        if (m_dati) freedv_set_sync(m_dati, FREEDV_SYNC_UNSYNC);
    }

    static QString nomeModo(int modo)
    {
        switch (modo) {
        case FREEDV_MODE_700D: return QStringLiteral("700D");
        case FREEDV_MODE_700E: return QStringLiteral("700E");
        case FREEDV_MODE_700C: return QStringLiteral("700C");
        case FREEDV_MODE_1600: return QStringLiteral("1600");
        case FREEDV_MODE_DATAC3: return QStringLiteral("DATAC3");
        case FREEDV_MODE_DATAC1: return QStringLiteral("DATAC1");
        case FREEDV_MODE_DATAC0: return QStringLiteral("DATAC0");
        default: return QString::number(modo);
        }
    }

private:
    struct freedv* m_voce {nullptr};
    struct freedv* m_dati {nullptr};
    QByteArray m_coda, m_codaDati;
    QString m_errore;
};

} // namespace dl
