// resample.h — da 48 kHz a 12 kHz e ritorno, per il profilo dei modi digitali.
//
// Perche' 12 kHz e non un numero a caso: e' la frequenza a cui campiona WSJT-X.
// Mandando 12 kHz si consegna al decodificatore esattamente il formato che
// userebbe se la radio fosse sul tavolo, senza conversioni ulteriori. E 6 kHz di
// banda coprono con abbondanza tutto quello che sta in un passband SSB, dove i
// modi digitali vivono: FT8 sta sotto i 3 kHz.
//
// Ridurre a un quarto senza filtrare prima sarebbe un errore da manuale: tutto
// quello che sta sopra i 6 kHz tornerebbe indietro ripiegato dentro la banda
// utile (aliasing), mettendo righe false proprio dove il decodificatore cerca i
// segnali. Quindi si filtra, con un FIR a fase lineare: la fase lineare conta,
// perche' un filtro che sfasa in modo diverso le varie frequenze deformerebbe i
// simboli.
//
// Costo: 64 moltiplicazioni per campione prodotto, cioe' 768.000 al secondo.
// Nulla per qualunque PC, e in cambio il segnale resta quello che era.

#pragma once

#include <QByteArray>
#include <QMap>
#include <QVector>

#include <cmath>
#include <cstring>

namespace dl {

constexpr int kDigiRate = 12000;          // come WSJT-X
constexpr int kDigiRapporto = 48000 / kDigiRate;
constexpr int kFirTap = 65;               // dispari: il ritardo e' un numero intero di campioni

// Il collegamento d'emergenza lavora a 8 kHz, che e' la frequenza di FreeDV, e
// taglia a 3,4 kHz: banda telefonica, tutto quello che serve al parlato.
constexpr int kEmrgRate = 8000;
constexpr int kEmrgRapporto = 48000 / kEmrgRate;
constexpr double kEmrgTaglio = 3400.0;

// Coefficienti del passa-basso per una data frequenza di taglio. Si calcolano
// una volta per ciascun taglio richiesto e si tengono da parte: servono a 5,4 kHz
// per i digitali e a 3,4 kHz per il collegamento d'emergenza, che lavora a 8 kHz.
//
// Il taglio si mette sempre sotto Nyquist con margine, perche' la banda di
// transizione di un filtro reale non e' verticale: senza margine qualcosa
// passerebbe oltre e tornerebbe ripiegato dentro.
inline const QVector<double>& firCoeff(double taglioHz = 5400.0)
{
    static QMap<int, QVector<double>> cache;
    int const chiave = int(taglioHz);
    auto const it = cache.constFind(chiave);
    if (it != cache.constEnd()) return it.value();

    QVector<double> h(kFirTap);
    double const fc = taglioHz / 48000.0;   // frequenza di taglio normalizzata
    int const meta = kFirTap / 2;
    double somma = 0;
    for (int i = 0; i < kFirTap; ++i) {
        int const n = i - meta;
        double const sinc = (n == 0) ? 2.0 * fc
                                     : std::sin(2.0 * M_PI * fc * n) / (M_PI * n);
        // Finestra di Blackman: attenuazione fuori banda oltre i 70 dB, che e'
        // quello che serve per non far rientrare nulla dall'aliasing.
        double const w = 0.42 - 0.5 * std::cos(2.0 * M_PI * i / (kFirTap - 1))
                         + 0.08 * std::cos(4.0 * M_PI * i / (kFirTap - 1));
        h[i] = sinc * w;
        somma += h[i];
    }
    for (double& v : h) v /= somma;       // guadagno unitario in continua
    return cache.insert(chiave, h).value();
}

// 48 kHz -> 12 kHz. Tiene la storia fra un blocco e il successivo: azzerarla
// ogni volta produrrebbe uno scatto ogni 40 ms, esattamente al passo dei
// pacchetti.
class Decimatore
{
public:
    // rapporto 4 per i digitali (48->12 kHz), 6 per l'emergenza (48->8 kHz).
    explicit Decimatore(int rapporto = kDigiRapporto, double taglioHz = 5400.0)
        : m_rapporto(rapporto), m_taglio(taglioHz) { m_storia.fill(0, kFirTap); }

    void azzera() { m_storia.fill(0, kFirTap); m_fase = 0; }

    // Restituisce i campioni ridotti prodotti da questo blocco a 48 kHz.
    QVector<qint16> giu(const qint16* pcm, int n)
    {
        QVector<qint16> out;
        out.reserve(n / m_rapporto + 2);
        QVector<double> const& h = firCoeff(m_taglio);
        for (int i = 0; i < n; ++i) {
            // scorrimento della finestra
            std::memmove(m_storia.data(), m_storia.constData() + 1,
                         size_t(kFirTap - 1) * sizeof(double));
            m_storia[kFirTap - 1] = double(pcm[i]);
            if (++m_fase < m_rapporto) continue;
            m_fase = 0;
            // Si calcola solo per i campioni che si tengono: gli altri
            // verrebbero buttati, e sarebbe lavoro speso per niente.
            double acc = 0;
            for (int k = 0; k < kFirTap; ++k) acc += m_storia[k] * h[kFirTap - 1 - k];
            out.append(qint16(qBound(-32768.0, acc, 32767.0)));
        }
        return out;
    }

private:
    int m_rapporto;
    double m_taglio;
    QVector<double> m_storia;
    int m_fase {0};
};

// 12 kHz -> 48 kHz, per l'audio che il telefono manda da trasmettere: la scheda
// del rig vuole 48 kHz. Si inseriscono tre zeri fra i campioni e si filtra; il
// guadagno si recupera moltiplicando per il rapporto, che e' l'energia persa
// mettendo gli zeri.
class Interpolatore
{
public:
    explicit Interpolatore(int rapporto = kDigiRapporto, double taglioHz = 5400.0)
        : m_rapporto(rapporto), m_taglio(taglioHz) { m_storia.fill(0, kFirTap); }

    void azzera() { m_storia.fill(0, kFirTap); }

    QVector<qint16> su(const qint16* pcm, int n)
    {
        QVector<qint16> out;
        out.reserve(n * m_rapporto);
        QVector<double> const& h = firCoeff(m_taglio);
        for (int i = 0; i < n; ++i) {
            for (int z = 0; z < m_rapporto; ++z) {
                std::memmove(m_storia.data(), m_storia.constData() + 1,
                             size_t(kFirTap - 1) * sizeof(double));
                m_storia[kFirTap - 1] = (z == 0) ? double(pcm[i]) : 0.0;
                double acc = 0;
                for (int k = 0; k < kFirTap; ++k) acc += m_storia[k] * h[kFirTap - 1 - k];
                out.append(qint16(qBound(-32768.0, acc * m_rapporto, 32767.0)));
            }
        }
        return out;
    }

private:
    int m_rapporto;
    double m_taglio;
    QVector<double> m_storia;
};

} // namespace dl
