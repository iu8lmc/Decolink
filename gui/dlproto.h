// dlproto.h — protocollo Decolink v3, piano dati.
//
// La v2 (header "HFGW" di 22 byte, PCM grezzo) resta in funzione per la
// registrazione e per i client non aggiornati: qui c'e' solo il trasporto
// dell'audio, dove l'intestazione va tagliata all'osso. Con Opus a 24 kbit/s un
// pacchetto di voce pesa 60 byte, e i 22 byte della v2 sarebbero il 27% del
// traffico: i 10 byte della v3 sono il 14%.
//
//   byte 0     'D'                        riconoscimento veloce
//   byte 1     versione(4) | tipo(4)
//   byte 2     profilo(4)  | flag(4)
//   byte 3     numero di stazione locale  distingue i flussi in una stanza
//   byte 4-5   seq u16 (ricircola)        perdite e riordino
//   byte 6-9   marca temporale u32        in campioni dell'orologio del profilo
//
// Il relay inoltra questi pacchetti senza guardarci dentro: aggiungere un
// profilo domani non richiede di aggiornare il server.
//
// Progetto completo e ragioni delle scelte: PROTOCOLLO.md

#pragma once

#include <QByteArray>
#include <cstdint>
#include <cstring>

namespace dl {

constexpr char    kMagic   = 'D';
constexpr quint8  kVer     = 3;
constexpr int     kHdr     = 10;

// Tipi di pacchetto del piano dati.
enum Tipo : quint8 {
    TAudioRx = 0,   // gateway -> operatori: quello che la radio riceve
    TAudioTx = 1,   // operatore -> gateway: quello che vuole trasmettere
    TCtrl    = 2,   // negoziazione e report (sottotipo nel primo byte del corpo)
    TCat     = 3,   // comandi al rig e risposte
    TNack    = 4,   // sequenze mancanti da rimandare (profilo DIGI)
    TPing    = 5,
};

// Profili. PCM48 e' la v2 travestita: serve come punto di caduta quando l'altro
// capo non sa fare altro.
enum Profilo : quint8 {
    PPcm48 = 0,     // 48 kHz int16 grezzo, 786 kbit/s
    PVoce  = 1,     // Opus banda 6 kHz, ~28 kbit/s
    PCw    = 2,     // Opus banda 4 kHz, ~15 kbit/s
    PDigi  = 3,     // PCM 12 kHz senza perdite, ~130 kbit/s
    PEmrg  = 4,     // Codec2 su FreeDV, 0,7 kbit/s
};

enum Flag : quint8 {
    FFec    = 0x1,  // il pacchetto porta la ridondanza del precedente
    FMarker = 0x2,  // primo pacchetto dopo una pausa: azzera il buffer
};

// Sottotipi di TCtrl. La negoziazione e' un dialogo di quattro battute:
// chi ascolta dice cosa sa fare, il gateway offre, chi ascolta scegli, il
// gateway conferma da quale sequenza vale.
enum Ctrl : quint8 {
    CHello   = 1,
    COfferta = 2,
    CScegli  = 3,
    CAttivo  = 4,
    CReport  = 5,
};

inline void putU16(char* p, quint16 v) { p[0] = char(v >> 8); p[1] = char(v); }
inline void putU32(char* p, quint32 v)
{
    p[0] = char(v >> 24); p[1] = char(v >> 16); p[2] = char(v >> 8); p[3] = char(v);
}
inline quint16 getU16(const uchar* p) { return quint16((quint16(p[0]) << 8) | p[1]); }
inline quint32 getU32(const uchar* p)
{
    return (quint32(p[0]) << 24) | (quint32(p[1]) << 16) | (quint32(p[2]) << 8) | p[3];
}

// Confeziona un pacchetto v3. Il corpo puo' essere vuoto (PING, alcuni CTRL).
inline QByteArray pacchetto(quint8 tipo, quint8 profilo, quint8 flag, quint8 idStazione,
                            quint16 seq, quint32 tempo,
                            const char* corpo = nullptr, int len = 0)
{
    QByteArray p(kHdr + (len > 0 ? len : 0), Qt::Uninitialized);
    char* d = p.data();
    d[0] = kMagic;
    d[1] = char((kVer << 4) | (tipo & 0xF));
    d[2] = char(((profilo & 0xF) << 4) | (flag & 0xF));
    d[3] = char(idStazione);
    putU16(d + 4, seq);
    putU32(d + 6, tempo);
    if (corpo && len > 0) std::memcpy(d + kHdr, corpo, size_t(len));
    return p;
}

// Vero se il datagramma e' un pacchetto v3 leggibile. Non si fida della
// lunghezza: su UDP arriva di tutto, anche pacchetti tagliati a metà.
inline bool leggi(const QByteArray& dg, quint8& tipo, quint8& profilo, quint8& flag,
                  quint8& idStazione, quint16& seq, quint32& tempo)
{
    if (dg.size() < kHdr) return false;
    const uchar* d = reinterpret_cast<const uchar*>(dg.constData());
    if (d[0] != uchar(kMagic) || (d[1] >> 4) != kVer) return false;
    tipo       = d[1] & 0xF;
    profilo    = d[2] >> 4;
    flag       = d[2] & 0xF;
    idStazione = d[3];
    seq        = getU16(d + 4);
    tempo      = getU32(d + 6);
    return true;
}

inline const char* nomeProfilo(quint8 p)
{
    switch (p) {
    case PPcm48: return "PCM 48 kHz";
    case PVoce:  return "voce (Opus)";
    case PCw:    return "CW (Opus)";
    case PDigi:  return "digitali (senza perdite)";
    case PEmrg:  return "emergenza (Codec2)";
    default:     return "?";
    }
}

} // namespace dl
