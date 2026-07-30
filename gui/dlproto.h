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
    PPcm48 = 0,     // 48 kHz int16 grezzo, 808 kbit/s
    PVoce  = 1,     // Opus banda 6 kHz, 32 kbit/s a 40 ms
    PCw    = 2,     // Opus banda 4 kHz, 20 kbit/s a 40 ms
    PDigi  = 3,     // PCM 12 kHz senza perdite, 146 kbit/s
    PEmrg  = 4,     // Codec2 su FreeDV, 0,7 kbit/s
    PCwKey = 5,     // solo gli istanti del tasto, il tono si rigenera all'arrivo
};

enum Flag : quint8 {
    FFec    = 0x1,  // il pacchetto porta la ridondanza del precedente
    FMarker = 0x2,  // primo pacchetto dopo una pausa: azzera il buffer
    FAggr   = 0x4,  // il corpo contiene piu' frame: vedi corpoAggregato()
};

// Capacita' dichiarate nel CTRL/HELLO. Servono a non mandare a un client
// vecchio un formato che non sa leggere: chi non dichiara nulla riceve un frame
// per pacchetto, come prima.
enum Capacita : quint8 {
    CapAggr = 0x1,  // sa leggere i pacchetti con piu' frame
};

// Quanti frame Opus stanno in un datagramma. Non e' una preferenza estetica: su
// un pacchetto da 70 byte le intestazioni IP e UDP sono 28, cioe' il 40% del
// traffico. Raggruppare due frame paga quell'involucro una volta invece di due.
//
//   1 frame  (20 ms)  fonia 39,2 kbit/s   CW 27,2   latenza minima
//   2 frame  (40 ms)  fonia ~32           CW ~20    +20 ms
//   3 frame  (60 ms)  fonia ~30           CW ~18    +40 ms
constexpr int kMaxAggr = 4;

// Il formato del corpo con piu' frame sta piu' sotto, dopo le funzioni di
// lettura e scrittura dei numeri: corpoAggregato() e frameDaCorpo().

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

// Corpo con piu' frame:
//   byte 0        numero di frame (1..kMaxAggr)
//   byte 1..      lunghezze u16 dei primi N-1 frame
//   poi           i frame uno dietro l'altro; l'ultimo prende quel che resta
//
// L'ultima lunghezza non si scrive perche' si ricava: due byte risparmiati su
// ogni pacchetto sono 400 bit/s a 25 pacchetti al secondo, e a questi livelli
// di banda ogni byte conta.
inline QByteArray corpoAggregato(const QList<QByteArray>& frame)
{
    QByteArray corpo;
    corpo.append(char(frame.size()));
    for (int i = 0; i + 1 < frame.size(); ++i) {
        char len[2];
        putU16(len, quint16(frame.at(i).size()));
        corpo.append(len, 2);
    }
    for (QByteArray const& f : frame) corpo.append(f);
    return corpo;
}

// Estrae i frame da un corpo. Con aggregato=false il corpo E' il frame, che e'
// il formato di chi non conosce FAggr. Restituisce una lista vuota se il corpo
// e' incoerente: su UDP arriva anche roba tagliata, e fidarsi delle lunghezze
// dichiarate significherebbe leggere fuori dal pacchetto.
inline QList<QByteArray> frameDaCorpo(const QByteArray& corpo, bool aggregato)
{
    QList<QByteArray> out;
    if (corpo.isEmpty()) return out;
    if (!aggregato) { out.append(corpo); return out; }

    int const n = int(uchar(corpo.at(0)));
    if (n < 1 || n > kMaxAggr) return out;
    int const dati = 1 + 2 * (n - 1);
    if (corpo.size() < dati) return out;

    const uchar* p = reinterpret_cast<const uchar*>(corpo.constData()) + 1;
    QList<int> lunghezze;
    int somma = 0;
    for (int i = 0; i + 1 < n; ++i) {
        int const len = int(getU16(p + 2 * i));
        if (len <= 0 || len > 1500) return out;
        lunghezze.append(len);
        somma += len;
    }
    int const ultimo = corpo.size() - dati - somma;
    if (ultimo <= 0) return out;
    lunghezze.append(ultimo);

    int off = dati;
    for (int len : lunghezze) {
        out.append(corpo.mid(off, len));
        off += len;
    }
    return out;
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
    case PCwKey: return "CW a tasto (solo il ritmo)";
    default:     return "?";
    }
}

} // namespace dl
