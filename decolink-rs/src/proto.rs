//! Protocollo Decolink v3, piano dati (porting di `gui/dlproto.h`).
//!
//! ```text
//! byte 0     'D'                        riconoscimento veloce
//! byte 1     versione(4) | tipo(4)
//! byte 2     profilo(4)  | flag(4)
//! byte 3     numero di stazione locale
//! byte 4-5   seq u16 (ricircola)
//! byte 6-9   marca temporale u32
//! ```

pub const MAGIC: u8 = b'D';
pub const VER: u8 = 3;
pub const HDR: usize = 10;

/// Tipi di pacchetto del piano dati.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum Tipo {
    AudioRx = 0,
    AudioTx = 1,
    Ctrl = 2,
    Cat = 3,
    Nack = 4,
    Ping = 5,
}

impl Tipo {
    pub fn da_u8(v: u8) -> Option<Tipo> {
        Some(match v {
            0 => Tipo::AudioRx,
            1 => Tipo::AudioTx,
            2 => Tipo::Ctrl,
            3 => Tipo::Cat,
            4 => Tipo::Nack,
            5 => Tipo::Ping,
            _ => return None,
        })
    }
}

/// Profili audio. `Pcm48` e' il punto di caduta per chi non sa altro.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum Profilo {
    Pcm48 = 0,
    Voce = 1,
    Cw = 2,
    Digi = 3,
    Emrg = 4,
    CwKey = 5,
}

impl Profilo {
    pub fn da_u8(v: u8) -> Option<Profilo> {
        Some(match v {
            0 => Profilo::Pcm48,
            1 => Profilo::Voce,
            2 => Profilo::Cw,
            3 => Profilo::Digi,
            4 => Profilo::Emrg,
            5 => Profilo::CwKey,
            _ => return None,
        })
    }

    pub fn nome(self) -> &'static str {
        match self {
            Profilo::Pcm48 => "PCM 48 kHz",
            Profilo::Voce => "voce (Opus)",
            Profilo::Cw => "CW (Opus)",
            Profilo::Digi => "digitali (senza perdite)",
            Profilo::Emrg => "emergenza (Codec2)",
            Profilo::CwKey => "CW a tasto (solo il ritmo)",
        }
    }
}

pub mod flag {
    pub const FEC: u8 = 0x1;
    pub const MARKER: u8 = 0x2;
    pub const AGGR: u8 = 0x4;
}

pub mod capacita {
    /// Sa leggere i pacchetti con piu' frame.
    pub const AGGR: u8 = 0x1;
}

/// Quanti frame Opus stanno in un datagramma.
pub const MAX_AGGR: usize = 4;

/// Sottotipi di `Tipo::Ctrl`: negoziazione in quattro battute.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum Ctrl {
    Hello = 1,
    Offerta = 2,
    Scegli = 3,
    Attivo = 4,
    Report = 5,
}

/// Un pacchetto v3 letto dal filo.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Pacchetto {
    pub tipo: Tipo,
    pub profilo: Profilo,
    pub flag: u8,
    pub stazione: u8,
    pub seq: u16,
    pub tempo: u32,
    pub corpo: Vec<u8>,
}

/// Confeziona un pacchetto v3. Il corpo puo' essere vuoto.
pub fn pacchetto(
    tipo: Tipo,
    profilo: u8,
    flag: u8,
    stazione: u8,
    seq: u16,
    tempo: u32,
    corpo: &[u8],
) -> Vec<u8> {
    let mut p = Vec::with_capacity(HDR + corpo.len());
    p.push(MAGIC);
    p.push((VER << 4) | (tipo as u8 & 0xF));
    p.push(((profilo & 0xF) << 4) | (flag & 0xF));
    p.push(stazione);
    p.extend_from_slice(&seq.to_be_bytes());
    p.extend_from_slice(&tempo.to_be_bytes());
    p.extend_from_slice(corpo);
    p
}

/// Legge un datagramma v3. `None` se non e' v3 o e' troppo corto: su UDP arriva
/// di tutto, anche pacchetti tagliati a meta', e non ci si fida della lunghezza.
pub fn leggi(dg: &[u8]) -> Option<Pacchetto> {
    if dg.len() < HDR || dg[0] != MAGIC || (dg[1] >> 4) != VER {
        return None;
    }
    Some(Pacchetto {
        tipo: Tipo::da_u8(dg[1] & 0xF)?,
        profilo: Profilo::da_u8(dg[2] >> 4)?,
        flag: dg[2] & 0xF,
        stazione: dg[3],
        seq: u16::from_be_bytes([dg[4], dg[5]]),
        tempo: u32::from_be_bytes([dg[6], dg[7], dg[8], dg[9]]),
        corpo: dg[HDR..].to_vec(),
    })
}

/// Corpo con piu' frame: byte 0 = numero di frame; poi le lunghezze u16 dei
/// primi N-1 frame; poi i frame. L'ultima lunghezza si ricava.
pub fn corpo_aggregato(frame: &[&[u8]]) -> Vec<u8> {
    let mut corpo = vec![frame.len() as u8];
    for f in &frame[..frame.len().saturating_sub(1)] {
        corpo.extend_from_slice(&(f.len() as u16).to_be_bytes());
    }
    for f in frame {
        corpo.extend_from_slice(f);
    }
    corpo
}

/// Estrae i frame da un corpo. Senza `aggregato` il corpo e' gia' un frame.
/// Lista vuota se il corpo e' incoerente: non ci si fida delle lunghezze dichiarate.
pub fn frame_da_corpo(corpo: &[u8], aggregato: bool) -> Vec<Vec<u8>> {
    if corpo.is_empty() {
        return Vec::new();
    }
    if !aggregato {
        return vec![corpo.to_vec()];
    }
    let n = corpo[0] as usize;
    if n < 1 || n > MAX_AGGR {
        return Vec::new();
    }
    let dati = 1 + 2 * (n - 1);
    if corpo.len() < dati {
        return Vec::new();
    }
    let mut lunghezze = Vec::with_capacity(n);
    let mut somma = 0usize;
    for i in 0..n - 1 {
        let len = u16::from_be_bytes([corpo[1 + 2 * i], corpo[2 + 2 * i]]) as usize;
        if len == 0 || len > 1500 {
            return Vec::new();
        }
        lunghezze.push(len);
        somma += len;
    }
    if corpo.len() <= dati + somma {
        return Vec::new();
    }
    lunghezze.push(corpo.len() - dati - somma);

    let mut out = Vec::with_capacity(n);
    let mut off = dati;
    for len in lunghezze {
        out.push(corpo[off..off + len].to_vec());
        off += len;
    }
    out
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn intestazione_di_dieci_byte() {
        let p = pacchetto(Tipo::AudioRx, 1, flag::FEC, 7, 0x1234, 0xAABBCCDD, &[9, 9]);
        assert_eq!(p.len(), HDR + 2);
        assert_eq!(p[0], b'D');
        assert_eq!(p[1], (3 << 4) | 0);
        assert_eq!(p[2], (1 << 4) | 1);
        assert_eq!(p[3], 7);
        assert_eq!(&p[4..6], &[0x12, 0x34]);
        assert_eq!(&p[6..10], &[0xAA, 0xBB, 0xCC, 0xDD]);
    }

    #[test]
    fn andata_e_ritorno() {
        let corpo = [1u8, 2, 3, 4];
        let p = pacchetto(Tipo::Ctrl, 2, 0, 3, 65535, 42, &corpo);
        let l = leggi(&p).expect("v3");
        assert_eq!(l.tipo, Tipo::Ctrl);
        assert_eq!(l.profilo, Profilo::Cw);
        assert_eq!(l.stazione, 3);
        assert_eq!(l.seq, 65535);
        assert_eq!(l.tempo, 42);
        assert_eq!(l.corpo, corpo);
    }

    #[test]
    fn rifiuta_il_non_v3_e_il_tagliato() {
        assert!(leggi(b"HFGW\x03\x00").is_none());
        assert!(leggi(&[b'D', 0x30, 0, 0, 0, 0, 0, 0, 0]).is_none()); // 9 byte
        let mut v2 = pacchetto(Tipo::AudioRx, 0, 0, 0, 0, 0, &[]);
        v2[1] = 2 << 4; // versione sbagliata
        assert!(leggi(&v2).is_none());
    }

    #[test]
    fn corpo_aggregato_tre_frame() {
        let a = [1u8; 5];
        let b = [2u8; 7];
        let c = [3u8; 3];
        let corpo = corpo_aggregato(&[&a, &b, &c]);
        assert_eq!(corpo[0], 3);
        // due lunghezze da 2 byte, nessuna per l'ultimo
        assert_eq!(&corpo[1..5], &[0, 5, 0, 7]);
        let fr = frame_da_corpo(&corpo, true);
        assert_eq!(fr, vec![a.to_vec(), b.to_vec(), c.to_vec()]);
    }

    #[test]
    fn corpo_incoerente_non_legge_fuori() {
        assert!(frame_da_corpo(&[], true).is_empty());
        assert!(frame_da_corpo(&[0], true).is_empty()); // zero frame
        assert!(frame_da_corpo(&[5, 0, 1], true).is_empty()); // piu' di MAX_AGGR
        assert!(frame_da_corpo(&[2, 0, 9, 1, 2], true).is_empty()); // dichiarati 9, ce ne sono 2
        assert!(frame_da_corpo(&[2, 0, 2, 1, 2], true).is_empty()); // nessun byte per l'ultimo
        assert_eq!(frame_da_corpo(&[9, 9], false), vec![vec![9, 9]]);
    }
}
