// cwkey.h — il profilo che non trasmette audio, ma il gesto del tasto.
//
// Un segnale CW porta pochissima informazione: la nota c'e' o non c'e'. Tutto il
// resto — l'altezza del tono, il fruscio intorno, la forma dell'inviluppo — al
// ricevitore non serve per capire cosa si stia dicendo. Quindi invece di
// mandare l'audio si mandano gli istanti in cui il tasto si apre e si chiude, e
// il tono lo si rigenera all'arrivo.
//
// Cosa si guadagna: un ordine di grandezza sotto il profilo CW con Opus, e un
// flusso che sta dentro un canale radio HF.
//
// Cosa si perde, e va detto chiaro: **tutto il contesto**. Non si sente piu' chi
// chiama poco fuori nota, non si sente il QSB, non si sente il QRM che copre il
// corrispondente, non si sente se c'e' un'altra stazione sulla frequenza. Si
// sente un tono pulito, generato da un computer, che ripete il ritmo di quello
// che il rilevatore ha creduto di vedere. Per leggere un nominativo in una banda
// pulita e' perfetto; per operare in un contest e' inutilizzabile.
//
// Per questo resta un profilo che si chiede esplicitamente, non un'astuzia che
// scatta da sola quando la rete peggiora.

#pragma once

#include <QByteArray>
#include <QVector>

#include <cmath>
#include <cstdint>

namespace dl {

// Risoluzione temporale del rilevatore: 5 ms. A 20 parole al minuto un punto
// dura 60 ms, quindi 5 ms di grana sono un errore inferiore al 10% sul simbolo
// piu' corto — impercettibile all'orecchio, che sul ritmo del CW e' tollerante
// ai millisecondi ma non alle decine.
constexpr int kCwBlocco = 240;              // campioni a 48 kHz = 5 ms
constexpr int kCwMs = 5;

// Banco di note in cui cercare il segnale: il CW si ascolta fra i 400 e i 1000
// Hz, e cercare piu' in largo vorrebbe dire raccogliere rumore.
constexpr int kCwBinPrimo = 400;
constexpr int kCwBinPasso = 75;
constexpr int kCwBin = 9;                   // 400..1000 Hz

// Blocchi di sola osservazione all'inizio, prima di dichiarare qualcosa: 100 ms
// bastano perche' le soglie si formino sul segnale vero.
constexpr int kCwAvvio = 20;
// Stacco minimo fra rumore e picco per credere che qualcuno stia trasmettendo.
// Il valore e' in unita' di energia del rilevatore, con l'audio normalizzato a 1.
constexpr double kCwStaccoMinimo = 1.5;

// Un evento del tasto: quanto tempo e' passato dal precedente, e se ora la nota
// c'e' o no.
struct EventoCw {
    quint16 deltaMs;
    bool giu;
};

// ---------------------------------------------------------------- rilevatore

// Trova la nota e decide se il tasto e' premuto. Il metodo e' quello di
// Goertzel: costa due moltiplicazioni per campione per ciascuna frequenza
// cercata, molto meno di una trasformata completa, e qui servono nove frequenze.
class RilevatoreCw
{
public:
    RilevatoreCw() { azzera(); }

    void azzera()
    {
        m_coda.clear();
        m_giu = false;
        // Si parte da zero e si impara dal segnale. Partire da valori inventati
        // e' esattamente l'errore che rendeva il rilevatore sordo ai punti brevi:
        // con un picco iniziale troppo alto la soglia restava tarata su un
        // segnale che non c'era, e serviva un quarto d'ora perche' scendesse.
        m_rumore = 0.0;
        m_picco = 0.0;
        m_avvio = kCwAvvio;
        m_msDaUltimo = 0;
        m_acc.clear();
        m_notaHz = 700;
        m_energiaUltima = 0;
    }

    int notaHz() const { return m_notaHz; }
    double energia() const { return m_energiaUltima; }
    bool premuto() const { return m_giu; }

    // Mangia audio a 48 kHz e restituisce gli eventi maturati.
    QVector<EventoCw> mangia(const qint16* pcm, int n)
    {
        QVector<EventoCw> fuori;
        m_acc.append(reinterpret_cast<const char*>(pcm), n * 2);

        while (m_acc.size() >= kCwBlocco * 2) {
            const qint16* b = reinterpret_cast<const qint16*>(m_acc.constData());

            // Energia in ciascuna nota del banco, e si tiene la piu' forte:
            // e' la nota su cui il corrispondente sta trasmettendo.
            double miglioreEn = 0;
            int miglioreHz = m_notaHz;
            for (int i = 0; i < kCwBin; ++i) {
                int const hz = kCwBinPrimo + i * kCwBinPasso;
                double const w = 2.0 * M_PI * hz / 48000.0;
                double const coeff = 2.0 * std::cos(w);
                double s0 = 0, s1 = 0, s2 = 0;
                for (int k = 0; k < kCwBlocco; ++k) {
                    s0 = double(b[k]) / 32768.0 + coeff * s1 - s2;
                    s2 = s1;
                    s1 = s0;
                }
                double const en = std::sqrt(s1 * s1 + s2 * s2 - coeff * s1 * s2);
                if (en > miglioreEn) { miglioreEn = en; miglioreHz = hz; }
            }
            m_acc.remove(0, kCwBlocco * 2);
            m_energiaUltima = miglioreEn;

            // Soglia che si adatta: si inseguono il livello del rumore e quello
            // del picco, e si decide a meta' strada. Una soglia fissa
            // funzionerebbe solo con un livello di ingresso e una banda.
            //
            // Le costanti di tempo sono asimmetriche perche' i due livelli si
            // muovono in modo diverso: il picco deve salire subito quando arriva
            // un simbolo e scendere in circa un secondo se il corrispondente
            // smette; il rumore deve seguire i minimi ma non farsi trascinare dai
            // segnali. Sbagliare queste quattro costanti significa perdere i
            // punti brevi, che sono la meta' del CW.
            if (miglioreEn < m_rumore) m_rumore += (miglioreEn - m_rumore) * 0.30;
            else                       m_rumore += (miglioreEn - m_rumore) * 0.002;
            if (miglioreEn > m_picco)  m_picco  += (miglioreEn - m_picco) * 0.50;
            else                       m_picco  += (miglioreEn - m_picco) * 0.005;

            m_msDaUltimo += kCwMs;

            // Primi 100 ms: si guarda e si impara, senza dichiarare niente.
            // Emettere eventi con soglie non ancora formate produrrebbe una
            // raffica di transizioni inventate all'apertura del collegamento.
            if (m_avvio > 0) { --m_avvio; continue; }

            double const salto = m_picco - m_rumore;
            // Se fra rumore e picco non c'e' stacco, non c'e' nessuno che
            // trasmette: meglio tasto su che inventarsi simboli dal fruscio.
            if (salto < kCwStaccoMinimo) {
                if (m_giu) {
                    m_giu = false;
                    fuori.append({ quint16(qMin(m_msDaUltimo, 32000)), false });
                    m_msDaUltimo = 0;
                }
                continue;
            }

            // Isteresi: si accende piu' in alto di quanto si spenga, altrimenti
            // sul bordo di un simbolo il tasto sfarfallerebbe.
            double const sogliaSu  = m_rumore + salto * 0.55;
            double const sogliaGiu = m_rumore + salto * 0.40;

            bool const oraGiu = m_giu ? (miglioreEn > sogliaGiu) : (miglioreEn > sogliaSu);
            if (oraGiu != m_giu) {
                m_giu = oraGiu;
                if (m_giu) m_notaHz = miglioreHz;      // la nota si fissa all'attacco
                fuori.append({ quint16(qMin(m_msDaUltimo, 32000)), m_giu });
                m_msDaUltimo = 0;
            }
        }
        return fuori;
    }

private:
    QByteArray m_acc;
    QVector<EventoCw> m_coda;
    bool m_giu {false};
    double m_rumore {0.0}, m_picco {0.0}, m_energiaUltima {0};
    int m_avvio {kCwAvvio};
    int m_msDaUltimo {0};
    int m_notaHz {700};
};

// Corpo del pacchetto CW-KEY:
//   byte 0     nota in decine di Hz (70 = 700 Hz)
//   byte 1     numero di eventi
//   poi        u16 per evento: bit 15 = tasto premuto, bit 0-14 = ms dal precedente
//
// Due byte per evento: a 20 parole al minuto sono una decina di eventi al
// secondo, cioe' 160 bit/s di informazione vera.
inline QByteArray corpoCw(int notaHz, const QVector<EventoCw>& ev)
{
    QByteArray c;
    c.append(char(qBound(0, notaHz / 10, 255)));
    c.append(char(qMin(ev.size(), 255)));
    for (int i = 0; i < ev.size() && i < 255; ++i) {
        quint16 const v = quint16((ev[i].giu ? 0x8000 : 0) | (ev[i].deltaMs & 0x7FFF));
        c.append(char((v >> 8) & 0xFF));
        c.append(char(v & 0xFF));
    }
    return c;
}

inline bool leggiCorpoCw(const QByteArray& c, int& notaHz, QVector<EventoCw>& ev)
{
    ev.clear();
    if (c.size() < 2) return false;
    notaHz = int(uchar(c.at(0))) * 10;
    int const n = int(uchar(c.at(1)));
    if (c.size() < 2 + 2 * n) return false;
    for (int i = 0; i < n; ++i) {
        quint16 const v = quint16((uchar(c.at(2 + 2 * i)) << 8) | uchar(c.at(3 + 2 * i)));
        ev.append({ quint16(v & 0x7FFF), (v & 0x8000) != 0 });
    }
    return true;
}

// ------------------------------------------------------------ sintetizzatore

// Rigenera il tono dagli eventi. L'attacco e il rilascio sono smussati su 5 ms:
// accendere e spegnere di netto una sinusoide produce un clic a banda larga —
// il difetto che in aria si chiama "key click" — e ascoltarlo per un'ora
// stanca piu' del rumore che si voleva togliere.
class SintetizzatoreCw
{
public:
    void azzera()
    {
        m_coda.clear();
        m_fase = 0;
        m_amp = 0;
        m_giu = false;
        m_attesa = 0;
    }

    void nota(int hz) { if (hz >= 200 && hz <= 2500) m_notaHz = hz; }

    void aggiungi(const QVector<EventoCw>& ev)
    {
        // Il deltaMs di un evento e' il tempo che passa PRIMA di applicarlo. Se
        // la coda era vuota bisogna quindi armare l'attesa del primo: ignorarla
        // manderebbe fuori tempo tutto il messaggio, che e' l'unica cosa che
        // questo profilo deve trasportare bene.
        bool const eraVuota = m_coda.isEmpty();
        for (EventoCw const& e : ev) m_coda.append(e);
        if (eraVuota && !m_coda.isEmpty() && m_attesa <= 0)
            m_attesa = qint64(m_coda.first().deltaMs) * 48;
    }

    // Produce n campioni a 48 kHz consumando la coda degli eventi.
    QVector<qint16> genera(int n)
    {
        QVector<qint16> out(n);
        double const dFase = 2.0 * M_PI * m_notaHz / 48000.0;
        // Rampa di 5 ms: 240 campioni per passare da zero a pieno.
        double const passo = 1.0 / 240.0;

        for (int i = 0; i < n; ++i) {
            // Scaduta l'attesa si applica l'evento e si arma quella del
            // successivo. Il ciclo, e non un semplice if, perche' due eventi
            // possono cadere nello stesso campione.
            while (!m_coda.isEmpty() && m_attesa <= 0) {
                m_giu = m_coda.takeFirst().giu;
                m_attesa = m_coda.isEmpty() ? 0 : qint64(m_coda.first().deltaMs) * 48;
            }
            if (m_attesa > 0) --m_attesa;

            m_amp += m_giu ? passo : -passo;
            m_amp = qBound(0.0, m_amp, 1.0);
            m_fase += dFase;
            if (m_fase > 2 * M_PI) m_fase -= 2 * M_PI;
            out[i] = qint16(m_amp * 18000.0 * std::sin(m_fase));
        }
        return out;
    }

    bool inAttesa() const { return !m_coda.isEmpty(); }

private:
    QVector<EventoCw> m_coda;
    double m_fase {0}, m_amp {0};
    bool m_giu {false};
    int m_notaHz {700};
    qint64 m_attesa {0};
};

} // namespace dl
