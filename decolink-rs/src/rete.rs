//! Lato radio del protocollo di rete (porting della parte di `gui/main.cpp` che
//! parla col relay e coi telefoni).
//!
//! È una macchina a stati senza I/O: riceve datagrammi e restituisce i datagrammi
//! da spedire e gli eventi per il resto del programma. Così si prova senza rete.
//!
//! Non fa (per ora): il login HTTPS sul servizio di accesso, l'invio DIGI (serve
//! il filtro di decimazione di `resample.h`), la ritrasmissione NACK lato invio, e
//! il report di perdita che adatta il bitrate. Il relay resta quello Python sul VPS.

use std::net::SocketAddr;
use std::time::Duration;

use std::collections::BTreeMap;

use crate::cwkey;
use crate::lossless;
use crate::resample::Decimatore;
use crate::proto::{self as dl, Ctrl, Profilo, Tipo};

/// Intestazione del protocollo v2 (PCM e registrazione): 22 byte.
pub const V2_HDR: usize = 22;
const V2_VER: u8 = 2;
/// Periodo del keepalive di registrazione verso il relay, come nel C++.
pub const KEEPALIVE: Duration = Duration::from_secs(5);
/// Campioni di un frame Opus (20 ms a 48 kHz) e di un blocco PCM (10 ms).
pub const FRAME_OPUS: usize = 960;
pub const FRAME_PCM: usize = 480;
/// 40 ms a 48 kHz: il blocco DIGI, che a 12 kHz sono 480 campioni.
pub const FRAME_DIGI: usize = 1920;
/// Quanto si conservano i pacchetti DIGI per una ritrasmissione.
const FINESTRA_MS: u64 = 3000;
const FINESTRA_MAX: usize = 200;

pub mod v2 {
    pub const AUDIO: u8 = 0;
    pub const PING: u8 = 1;
    pub const PONG: u8 = 2;
    pub const REGISTER: u8 = 3;
    pub const PEERUP: u8 = 4;
    pub const CATREQ: u8 = 5;
    pub const CATRSP: u8 = 6;
    pub const TXAUDIO: u8 = 7;
    pub const DENIED: u8 = 8;
    /// Chi ha il PTT della stazione: "tx free", "tx you" o "tx busy <nominativo>".
    pub const TXSTATE: u8 = 9;
}

/// Un datagramma da spedire.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Invio {
    pub verso: SocketAddr,
    pub dati: Vec<u8>,
}

/// Cose che il resto del programma deve sapere.
#[derive(Debug, Clone, PartialEq)]
pub enum Evento {
    /// Il relay ha accettato la registrazione.
    Registrato,
    /// Il relay ha rifiutato, con il motivo.
    Rifiutato(String),
    /// Il telefono si e' presentato (modalita' ascolto).
    TelefonoConnesso(SocketAddr),
    /// Audio da riprodurre sulla scheda del rig, a `rate` Hz.
    Audio { pcm: Vec<i16>, rate: u32 },
    /// Tasto CW da rigenerare: nota e istanti.
    CwKey { nota_hz: i32, eventi: Vec<cwkey::Evento> },
    /// Il profilo attivo e' cambiato per richiesta del telefono.
    Profilo(Profilo),
    /// Stato del PTT della stazione, dal relay.
    StatoTx(String),
}

/// Intestazione v2 letta.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct IntestazioneV2 {
    pub flags: u8,
    pub seq: u32,
    pub tempo_ms: u64,
    pub rate: u32,
}

/// Confeziona un pacchetto v2. `rate` va nell'intestazione, `payload` e' il corpo.
pub fn v2_pacchetto(flags: u8, seq: u32, tempo_ms: u64, rate: u32, payload: &[u8]) -> Vec<u8> {
    let mut p = Vec::with_capacity(V2_HDR + payload.len());
    p.extend_from_slice(b"HFGW");
    p.push(V2_VER);
    p.push(flags);
    p.extend_from_slice(&seq.to_be_bytes());
    p.extend_from_slice(&tempo_ms.to_be_bytes());
    p.extend_from_slice(&rate.to_be_bytes());
    p.extend_from_slice(payload);
    p
}

/// Legge un datagramma v2. `None` se non e' v2 o e' troppo corto.
pub fn v2_leggi(dg: &[u8]) -> Option<(IntestazioneV2, &[u8])> {
    if dg.len() < V2_HDR || &dg[0..4] != b"HFGW" || dg[4] != V2_VER {
        return None;
    }
    let h = IntestazioneV2 {
        flags: dg[5],
        seq: u32::from_be_bytes([dg[6], dg[7], dg[8], dg[9]]),
        tempo_ms: u64::from_be_bytes(dg[10..18].try_into().ok()?),
        rate: u32::from_be_bytes([dg[18], dg[19], dg[20], dg[21]]),
    };
    Some((h, &dg[V2_HDR..]))
}

/// PCM int16 in ordine little-endian, come lo mandano il C++ e il telefono.
fn pcm_da_byte(b: &[u8]) -> Vec<i16> {
    b.chunks_exact(2).map(|c| i16::from_le_bytes([c[0], c[1]])).collect()
}

fn pcm_in_byte(pcm: &[i16]) -> Vec<u8> {
    let mut out = Vec::with_capacity(pcm.len() * 2);
    for s in pcm {
        out.extend_from_slice(&s.to_le_bytes());
    }
    out
}

/// Stato del lato radio verso relay e telefoni.
pub struct Gateway {
    /// Dove spedire l'audio: il relay, o il telefono in modalita' ascolto.
    dst: Option<SocketAddr>,
    /// Modalita' ascolto: il telefono si presenta da solo con REGISTER/PING.
    ascolto: bool,
    /// Il telefono ha mai parlato in v3: solo allora il profilo conta.
    peer_ha_parlato: bool,
    /// Il telefono sa leggere i pacchetti con piu' frame.
    peer_aggr: bool,
    profilo: Profilo,
    aggr: usize,
    seq_v2: u32,
    seq_v3: u16,
    tempo: u32,
    acc: Vec<i16>,
    #[cfg(feature = "opus")]
    da_spedire: Vec<Vec<u8>>,
    #[cfg(feature = "opus")]
    seq_tx_atteso: Option<u16>,
    ultima_registrazione: Option<std::time::Instant>,
    dec: Decimatore,
    /// Pacchetti DIGI mandati, per rispondere ai NACK del telefono.
    finestra: BTreeMap<u16, (Vec<u8>, u64)>,
    /// Sequenze DIGI ricevute dal telefono, per chiedere quelle che mancano.
    arrivati: BTreeMap<u16, u64>,
    ultimo_rx: Option<u16>,
    #[cfg(feature = "opus")]
    opus_out: crate::opus::OpusVoce,
    #[cfg(feature = "opus")]
    opus_in: crate::opus::OpusVoce,
}

impl Default for Gateway {
    fn default() -> Self {
        Self::new()
    }
}

impl Gateway {
    pub fn new() -> Self {
        Gateway {
            dst: None,
            ascolto: false,
            peer_ha_parlato: false,
            peer_aggr: false,
            profilo: Profilo::Pcm48,
            aggr: 2,
            seq_v2: 0,
            seq_v3: 0,
            tempo: 0,
            acc: Vec::new(),
            #[cfg(feature = "opus")]
            da_spedire: Vec::new(),
            #[cfg(feature = "opus")]
            seq_tx_atteso: None,
            ultima_registrazione: None,
            dec: Decimatore::digi(),
            finestra: BTreeMap::new(),
            arrivati: BTreeMap::new(),
            ultimo_rx: None,
            #[cfg(feature = "opus")]
            opus_out: Default::default(),
            #[cfg(feature = "opus")]
            opus_in: Default::default(),
        }
    }

    pub fn profilo(&self) -> Profilo {
        self.profilo
    }

    pub fn imposta_destinazione(&mut self, dove: Option<SocketAddr>) {
        self.dst = dove;
    }

    pub fn modalita_ascolto(&mut self, on: bool) {
        self.ascolto = on;
    }

    /// Profili che il lato radio sa offrire. Senza Opus resta solo il PCM.
    pub fn offerta(&self) -> Vec<Profilo> {
        if cfg!(feature = "opus") {
            vec![Profilo::Voce, Profilo::Cw, Profilo::Pcm48]
        } else {
            vec![Profilo::Pcm48]
        }
    }

    /// Pacchetto di registrazione sul relay: `gw <token>`.
    pub fn registrazione(&mut self, token: &str, ora: std::time::Instant) -> Option<Invio> {
        let verso = self.dst?;
        self.ultima_registrazione = Some(ora);
        let corpo = format!("gw {token}");
        Some(Invio {
            verso,
            dati: v2_pacchetto(v2::REGISTER, self.prossimo_v2(), 0, 48_000, corpo.as_bytes()),
        })
    }

    /// Da chiamare a ogni giro: rinnova la registrazione ogni `KEEPALIVE`.
    pub fn tick(&mut self, token: &str, ora: std::time::Instant) -> Vec<Invio> {
        let scaduta = self
            .ultima_registrazione
            .map_or(true, |t| ora.duration_since(t) >= KEEPALIVE);
        if !scaduta || self.dst.is_none() || self.ascolto {
            return Vec::new();
        }
        self.registrazione(token, ora).into_iter().collect()
    }

    fn prossimo_v2(&mut self) -> u32 {
        self.seq_v2 = self.seq_v2.wrapping_add(1);
        self.seq_v2
    }

    fn prossimo_v3(&mut self) -> u16 {
        self.seq_v3 = self.seq_v3.wrapping_add(1);
        self.seq_v3
    }

    /// Audio ricevuto dalla radio (48 kHz mono): lo si codifica secondo il profilo
    /// attivo e si restituiscono i datagrammi pronti. Senza destinazione non si
    /// spedisce niente: il campione si butta, come nel C++.
    pub fn invia_audio(&mut self, pcm: &[i16], ora_ms: u64) -> Vec<Invio> {
        let Some(verso) = self.dst else {
            self.acc.clear();
            return Vec::new();
        };
        self.acc.extend_from_slice(pcm);
        let blocco = match self.profilo {
            Profilo::Pcm48 => FRAME_PCM,
            Profilo::Digi => FRAME_DIGI,
            _ => FRAME_OPUS,
        };
        let mut out = Vec::new();
        while self.acc.len() >= blocco {
            let frame: Vec<i16> = self.acc.drain(0..blocco).collect();
            match self.profilo {
                Profilo::Pcm48 => {
                    let seq = self.prossimo_v2();
                    out.push(Invio {
                        verso,
                        dati: v2_pacchetto(v2::AUDIO, seq, ora_ms, 48_000, &pcm_in_byte(&frame)),
                    });
                }
                #[cfg(feature = "opus")]
                Profilo::Voce | Profilo::Cw => {
                    let Some(p) = self.opus_out.codifica(&frame) else { continue };
                    self.tempo = self.tempo.wrapping_add(FRAME_OPUS as u32);
                    self.da_spedire.push(p);
                    if self.da_spedire.len() < self.aggr_attivo() {
                        continue;
                    }
                    out.push(self.pacchetto_audio(verso));
                }
                Profilo::Digi => {
                    let giu = self.dec.giu(&frame);
                    if giu.is_empty() {
                        continue;
                    }
                    let blocco = lossless::comprimi(&giu);
                    let seq = self.prossimo_v3();
                    let dati = dl::pacchetto(Tipo::AudioRx, Profilo::Digi as u8, 0, 0, seq, self.tempo, &blocco);
                    self.tempo = self.tempo.wrapping_add(giu.len() as u32);
                    self.ricorda(seq, &dati, ora_ms);
                    out.push(Invio { verso, dati });
                }
                _ => {}
            }
        }
        out
    }

    /// Conserva un pacchetto mandato, per rimandarlo se il telefono lo chiede.
    fn ricorda(&mut self, seq: u16, dati: &[u8], ora_ms: u64) {
        self.finestra.insert(seq, (dati.to_vec(), ora_ms));
        if self.finestra.len() > FINESTRA_MAX {
            self.finestra.retain(|_, (_, t)| ora_ms.saturating_sub(*t) <= FINESTRA_MS);
        }
    }

    /// Il telefono chiede indietro dei pacchetti: si rimandano quelli ancora in finestra.
    fn rimanda(&self, corpo: &[u8], da: SocketAddr, inv: &mut Vec<Invio>) {
        if corpo.len() < 2 {
            return;
        }
        let quanti = usize::from(corpo[1]);
        for i in 0..quanti {
            let Some(b) = corpo.get(2 + 2 * i..4 + 2 * i) else { break };
            let seq = u16::from_be_bytes([b[0], b[1]]);
            if let Some((dati, _)) = self.finestra.get(&seq) {
                inv.push(Invio { verso: da, dati: dati.clone() });
            }
        }
    }

    /// Registra una sequenza DIGI ricevuta e, se ne manca qualcuna, restituisce il
    /// NACK da mandare al telefono. Un ritardatario non e' un buco.
    fn nota_ricevuto(&mut self, seq: u16, ora_ms: u64) -> Option<Vec<u8>> {
        self.arrivati.insert(seq, ora_ms);
        if self.arrivati.len() > 400 {
            self.arrivati.retain(|_, t| ora_ms.saturating_sub(*t) <= 4000);
        }
        let Some(ultimo) = self.ultimo_rx else {
            self.ultimo_rx = Some(seq);
            return None;
        };
        let atteso = ultimo.wrapping_add(1);
        if seq == atteso {
            self.ultimo_rx = Some(seq);
            return None;
        }
        if (seq.wrapping_sub(ultimo) as i16) <= 0 {
            return None;
        }
        let mut mancano: Vec<u16> = Vec::new();
        let mut s = atteso;
        while s != seq && mancano.len() < 32 {
            if !self.arrivati.contains_key(&s) {
                mancano.push(s);
            }
            s = s.wrapping_add(1);
        }
        self.ultimo_rx = Some(seq);
        if mancano.is_empty() {
            return None;
        }
        let mut corpo = vec![Ctrl::Report as u8, mancano.len() as u8];
        for m in &mancano {
            corpo.extend_from_slice(&m.to_be_bytes());
        }
        Some(dl::pacchetto(Tipo::Nack, Profilo::Digi as u8, 0, 0, seq, 0, &corpo))
    }

    #[cfg(feature = "opus")]
    fn aggr_attivo(&self) -> usize {
        if self.peer_aggr { self.aggr.clamp(1, dl::MAX_AGGR) } else { 1 }
    }

    #[cfg(feature = "opus")]
    fn pacchetto_audio(&mut self, verso: SocketAddr) -> Invio {
        let seq = self.prossimo_v3();
        let frame: Vec<Vec<u8>> = std::mem::take(&mut self.da_spedire);
        let (flag, corpo) = if frame.len() == 1 {
            (dl::flag::FEC, frame[0].clone())
        } else {
            let rif: Vec<&[u8]> = frame.iter().map(|f| f.as_slice()).collect();
            (dl::flag::FEC | dl::flag::AGGR, dl::corpo_aggregato(&rif))
        };
        Invio {
            verso,
            dati: dl::pacchetto(Tipo::AudioRx, self.profilo as u8, flag, 0, seq, self.tempo, &corpo),
        }
    }

    /// Cambia profilo se il telefono lo ha chiesto e il lato radio lo sa fare.
    fn scegli(&mut self, voluto: Profilo) -> bool {
        // Come nel C++: il telefono puo' chiedere anche i digitali, che non sono nell'offerta.
        if !self.offerta().contains(&voluto) && voluto != Profilo::Digi {
            return false;
        }
        self.profilo = voluto;
        #[cfg(feature = "opus")]
        {
            match voluto {
                Profilo::Voce => {
                    let _ = self.opus_out.apri(24_000, 6_000);
                    let _ = self.opus_in.apri(24_000, 6_000);
                }
                Profilo::Cw => {
                    let _ = self.opus_out.apri(12_000, 4_000);
                    let _ = self.opus_in.apri(12_000, 4_000);
                }
                _ => {}
            }
        }
        true
    }

    /// Un datagramma arrivato. `cat` risponde ai comandi CAT del telefono.
    /// Restituisce i datagrammi da spedire e gli eventi.
    pub fn ricevi(
        &mut self,
        dg: &[u8],
        da: SocketAddr,
        ora_ms: u64,
        cat: &mut dyn FnMut(&str) -> String,
    ) -> (Vec<Invio>, Vec<Evento>) {
        let mut inv = Vec::new();
        let mut ev = Vec::new();
        if let Some(p) = dl::leggi(dg) {
            self.ricevi_v3(p, da, ora_ms, cat, &mut inv, &mut ev);
        } else if let Some((h, corpo)) = v2_leggi(dg) {
            self.ricevi_v2(h, corpo, da, ora_ms, cat, &mut inv, &mut ev);
        }
        (inv, ev)
    }

    #[allow(clippy::too_many_arguments)]
    fn ricevi_v2(
        &mut self,
        h: IntestazioneV2,
        corpo: &[u8],
        da: SocketAddr,
        ora_ms: u64,
        cat: &mut dyn FnMut(&str) -> String,
        inv: &mut Vec<Invio>,
        ev: &mut Vec<Evento>,
    ) {
        match h.flags {
            v2::REGISTER | v2::PING if self.ascolto => {
                // il telefono si e' fatto vivo: da qui in poi l'audio va a lui
                let nuovo = self.dst != Some(da);
                self.dst = Some(da);
                let risposta = if h.flags == v2::PING { v2::PONG } else { v2::REGISTER };
                inv.push(Invio { verso: da, dati: v2_pacchetto(risposta, h.seq, ora_ms, 48_000, &[]) });
                if nuovo {
                    ev.push(Evento::TelefonoConnesso(da));
                }
            }
            v2::PING => {
                inv.push(Invio { verso: da, dati: v2_pacchetto(v2::PONG, h.seq, ora_ms, 48_000, &[]) });
            }
            v2::REGISTER => ev.push(Evento::Registrato),
            v2::DENIED => ev.push(Evento::Rifiutato(String::from_utf8_lossy(corpo).into_owned())),
            v2::PEERUP => {}
            v2::TXSTATE => ev.push(Evento::StatoTx(String::from_utf8_lossy(corpo).trim().to_string())),
            v2::CATREQ => {
                let testo = String::from_utf8_lossy(corpo).into_owned();
                let risposta = cat(&testo);
                inv.push(Invio {
                    verso: da,
                    dati: v2_pacchetto(v2::CATRSP, h.seq, ora_ms, 48_000, risposta.as_bytes()),
                });
            }
            v2::TXAUDIO => {
                // Audio da trasmettere in PCM. A 24 o 12 kHz il chiamante ricampiona.
                ev.push(Evento::Audio { pcm: pcm_da_byte(corpo), rate: h.rate });
            }
            _ => {}
        }
    }

    fn ricevi_v3(
        &mut self,
        p: dl::Pacchetto,
        da: SocketAddr,
        ora_ms: u64,
        cat: &mut dyn FnMut(&str) -> String,
        inv: &mut Vec<Invio>,
        ev: &mut Vec<Evento>,
    ) {
        match p.tipo {
            Tipo::AudioTx => self.audio_tx(&p, da, ora_ms, inv, ev),
            Tipo::Cat => {
                let testo = String::from_utf8_lossy(&p.corpo).into_owned();
                let risposta = cat(&testo);
                inv.push(Invio {
                    verso: da,
                    dati: dl::pacchetto(Tipo::Cat, p.profilo as u8, 0, 0, p.seq, p.tempo, risposta.as_bytes()),
                });
            }
            Tipo::Ctrl => self.ctrl(&p, da, inv, ev),
            Tipo::Ping => {
                inv.push(Invio {
                    verso: da,
                    dati: dl::pacchetto(Tipo::Ping, p.profilo as u8, 0, 0, p.seq, p.tempo, &[]),
                });
            }
            // Il telefono chiede indietro dei pacchetti DIGI che ha perso.
            Tipo::Nack => self.rimanda(&p.corpo, da, inv),
            // Il lato radio non riceve audio RX.
            Tipo::AudioRx => {}
        }
    }

    fn ctrl(&mut self, p: &dl::Pacchetto, da: SocketAddr, inv: &mut Vec<Invio>, ev: &mut Vec<Evento>) {
        self.peer_ha_parlato = true;
        let Some(&sotto) = p.corpo.first() else { return };
        match sotto {
            x if x == Ctrl::Hello as u8 => {
                let cap = p.corpo.get(1).copied().unwrap_or(0);
                self.peer_aggr = cap & dl::capacita::AGGR != 0;
                let mut corpo = vec![Ctrl::Offerta as u8];
                let mut offerta: Vec<u8> = self.offerta().iter().map(|x| *x as u8).collect();
                offerta.resize(3, 0);
                corpo.extend_from_slice(&offerta);
                corpo.push(self.profilo as u8);
                corpo.push(dl::capacita::AGGR);
                corpo.push(self.aggr as u8);
                inv.push(Invio {
                    verso: da,
                    dati: dl::pacchetto(Tipo::Ctrl, self.profilo as u8, 0, 0, 0, 0, &corpo),
                });
            }
            x if x == Ctrl::Report as u8 => {
                if let Some(&perdita) = p.corpo.get(1) {
                    self.adatta_bitrate(i32::from(perdita));
                }
            }
            x if x == Ctrl::Scegli as u8 => {
                let Some(&voluto) = p.corpo.get(1) else { return };
                if let Some(prof) = Profilo::da_u8(voluto) {
                    if self.scegli(prof) {
                        ev.push(Evento::Profilo(prof));
                    }
                }
                let seq = self.prossimo_v3();
                inv.push(Invio {
                    verso: da,
                    dati: dl::pacchetto(Tipo::Ctrl, self.profilo as u8, 0, 0, seq, self.tempo,
                                        &[Ctrl::Attivo as u8, self.profilo as u8]),
                });
            }
            _ => {}
        }
    }

    /// Il report di perdita del telefono: piu' perdita, piu' ridondanza e meno bitrate.
    #[cfg(feature = "opus")]
    fn adatta_bitrate(&mut self, perdita: i32) {
        self.opus_out.perdita_attesa(perdita);
        let b = self.opus_out.bitrate();
        if perdita > 8 && b > 12_000 {
            self.opus_out.cambia_bitrate(if b == 24_000 { 16_000 } else { 12_000 });
        } else if perdita < 2 && b < 24_000 {
            self.opus_out.cambia_bitrate(if b == 12_000 { 16_000 } else { 24_000 });
        }
    }

    #[cfg(not(feature = "opus"))]
    fn adatta_bitrate(&mut self, _perdita: i32) {}

    /// Bitrate attuale dell'Opus in uscita, se Opus e' compilato.
    #[cfg(feature = "opus")]
    pub fn bitrate(&self) -> i32 {
        self.opus_out.bitrate()
    }

    fn audio_tx(
        &mut self,
        p: &dl::Pacchetto,
        da: SocketAddr,
        ora_ms: u64,
        inv: &mut Vec<Invio>,
        ev: &mut Vec<Evento>,
    ) {
        self.peer_ha_parlato = true;
        match p.profilo {
            Profilo::Pcm48 => ev.push(Evento::Audio { pcm: pcm_da_byte(&p.corpo), rate: 48_000 }),
            Profilo::CwKey => {
                if let Some((nota_hz, eventi)) = cwkey::leggi_corpo_cw(&p.corpo) {
                    ev.push(Evento::CwKey { nota_hz, eventi });
                }
            }
            Profilo::Digi => {
                if let Some(pcm) = lossless::decomprimi(&p.corpo) {
                    ev.push(Evento::Audio { pcm, rate: 12_000 });
                }
                if let Some(nack) = self.nota_ricevuto(p.seq, ora_ms) {
                    inv.push(Invio { verso: da, dati: nack });
                }
            }
            #[cfg(feature = "opus")]
            Profilo::Voce | Profilo::Cw => self.audio_tx_opus(p, ev),
            _ => {}
        }
    }

    #[cfg(feature = "opus")]
    fn audio_tx_opus(&mut self, p: &dl::Pacchetto, ev: &mut Vec<Evento>) {
        if !self.opus_in.pronto() && self.opus_in.apri(24_000, 6_000).is_err() {
            return;
        }
        // Un salto nella sequenza vuol dire pacchetti persi: Opus inventa fino a
        // cinque frame, altrimenti in trasmissione si sentirebbero scatti.
        if let Some(atteso) = self.seq_tx_atteso {
            if p.seq != atteso {
                let buchi = usize::from(p.seq.wrapping_sub(atteso)).min(5);
                for _ in 0..buchi {
                    if let Some(pcm) = self.opus_in.decodifica(None) {
                        ev.push(Evento::Audio { pcm, rate: 48_000 });
                    }
                }
            }
        }
        self.seq_tx_atteso = Some(p.seq.wrapping_add(1));
        let frame = dl::frame_da_corpo(&p.corpo, p.flag & dl::flag::AGGR != 0);
        for f in frame {
            if let Some(pcm) = self.opus_in.decodifica(Some(&f)) {
                ev.push(Evento::Audio { pcm, rate: 48_000 });
            }
        }
    }
}
