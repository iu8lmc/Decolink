// opusvoce.h — codifica e decodifica della voce con Opus.
//
// Perche' Opus e non un resampling a mano: gli si passano i campioni a 48 kHz
// cosi' come escono dalla scheda del rig e si dice fino a quale banda ci
// interessa arrivare (OPUS_SET_MAX_BANDWIDTH). Il filtraggio e la riduzione li
// fa lui, con filtri fatti come si deve; scriverli a mano vorrebbe dire
// rifarli peggio.
//
// Parametri scelti per la radio, non per la musica:
//
//   APPLICATION_VOIP     ottimizzato per il parlato, non per un'orchestra
//   MAX_BANDWIDTH 6 kHz  un SSB occupa 2,7 kHz: oltre si trasporta fruscio
//   SIGNAL_VOICE         dice a Opus che tipo di segnale aspettarsi
//   INBAND_FEC + LOSS    la ridondanza del pacchetto precedente viaggia dentro
//                        il successivo, cosi' una perdita isolata si ricostruisce
//                        senza chiedere niente a nessuno
//   frame da 20 ms       compromesso solito fra latenza e resa: 50 pacchetti al
//                        secondo, ~60 byte l'uno a 24 kbit/s
//
// Il DTX (smettere di trasmettere nel silenzio) resta spento di proposito: su
// una radio il rumore di fondo E' informazione — dice che il collegamento c'e' e
// com'e' la banda. Un silenzio digitale perfetto sembrerebbe un guasto.

#pragma once

#include <QByteArray>
#include <opus.h>

#include <cstdint>

namespace dl {

constexpr int kOpusRate  = 48000;
constexpr int kOpusFrame = kOpusRate / 50;   // 960 campioni = 20 ms
constexpr int kOpusMax   = 1275;             // pacchetto Opus piu' grande possibile

class OpusVoce
{
public:
    ~OpusVoce() { chiudi(); }

    // bandaHz: 4000 per il CW, 6000 per la fonia. bitrate in bit/s.
    bool apri(int bitrate = 24000, int bandaHz = 6000)
    {
        chiudi();
        int err = 0;
        m_enc = opus_encoder_create(kOpusRate, 1, OPUS_APPLICATION_VOIP, &err);
        if (err != OPUS_OK || !m_enc) { m_errore = opus_strerror(err); return false; }
        m_dec = opus_decoder_create(kOpusRate, 1, &err);
        if (err != OPUS_OK || !m_dec) { m_errore = opus_strerror(err); chiudi(); return false; }

        int const banda = bandaHz <= 4000 ? OPUS_BANDWIDTH_NARROWBAND
                        : bandaHz <= 6000 ? OPUS_BANDWIDTH_MEDIUMBAND
                                          : OPUS_BANDWIDTH_WIDEBAND;
        opus_encoder_ctl(m_enc, OPUS_SET_BITRATE(bitrate));
        opus_encoder_ctl(m_enc, OPUS_SET_MAX_BANDWIDTH(banda));
        opus_encoder_ctl(m_enc, OPUS_SET_SIGNAL(OPUS_SIGNAL_VOICE));
        opus_encoder_ctl(m_enc, OPUS_SET_COMPLEXITY(8));
        opus_encoder_ctl(m_enc, OPUS_SET_INBAND_FEC(1));
        opus_encoder_ctl(m_enc, OPUS_SET_PACKET_LOSS_PERC(5));
        opus_encoder_ctl(m_enc, OPUS_SET_DTX(0));
        m_bitrate = bitrate;
        m_banda = bandaHz;
        return true;
    }

    void chiudi()
    {
        if (m_enc) { opus_encoder_destroy(m_enc); m_enc = nullptr; }
        if (m_dec) { opus_decoder_destroy(m_dec); m_dec = nullptr; }
    }

    bool pronto() const { return m_enc && m_dec; }
    QString errore() const { return m_errore; }
    int bitrate() const { return m_bitrate; }
    int banda() const { return m_banda; }

    // Cambia il bitrate a collegamento aperto: e' quello che fa l'adattamento
    // quando la rete peggiora, senza ricreare il codificatore (ricrearlo
    // produrrebbe uno scatto nell'audio).
    void cambiaBitrate(int bitrate)
    {
        if (m_enc && bitrate != m_bitrate) {
            opus_encoder_ctl(m_enc, OPUS_SET_BITRATE(bitrate));
            m_bitrate = bitrate;
        }
    }

    // Quanta perdita dichiarare a Opus: piu' e' alta, piu' ridondanza mette
    // dentro i pacchetti (e piu' banda usa). Si aggiorna dai report del ricevente.
    void perditaAttesa(int percento)
    {
        if (m_enc) opus_encoder_ctl(m_enc, OPUS_SET_PACKET_LOSS_PERC(qBound(0, percento, 30)));
    }

    // pcm: esattamente kOpusFrame campioni int16 mono. Vuoto se la codifica
    // fallisce, cosi' chi chiama non manda spazzatura in rete.
    QByteArray codifica(const qint16* pcm)
    {
        if (!m_enc) return {};
        QByteArray out(kOpusMax, Qt::Uninitialized);
        int const n = opus_encode(m_enc, pcm, kOpusFrame,
                                  reinterpret_cast<unsigned char*>(out.data()), kOpusMax);
        if (n < 0) { m_errore = opus_strerror(n); return {}; }
        out.resize(n);
        return out;
    }

    // Decodifica un pacchetto. Passando un pacchetto vuoto si chiede a Opus di
    // inventare il pezzo mancante (mascheramento della perdita): meglio un
    // frammento ricostruito che un buco, che si sentirebbe come uno scatto.
    QByteArray decodifica(const char* dati, int len)
    {
        if (!m_dec) return {};
        QByteArray pcm(kOpusFrame * 2, Qt::Uninitialized);
        int const n = opus_decode(m_dec,
                                  (dati && len > 0) ? reinterpret_cast<const unsigned char*>(dati) : nullptr,
                                  (dati && len > 0) ? len : 0,
                                  reinterpret_cast<qint16*>(pcm.data()), kOpusFrame, 0);
        if (n < 0) { m_errore = opus_strerror(n); return {}; }
        pcm.resize(n * 2);
        return pcm;
    }

    static QString versione() { return QString::fromLatin1(opus_get_version_string()); }

private:
    OpusEncoder* m_enc {nullptr};
    OpusDecoder* m_dec {nullptr};
    QString m_errore;
    int m_bitrate {24000};
    int m_banda {6000};
};

} // namespace dl
