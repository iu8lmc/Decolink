//! Opus per la voce e la CW (porting di `gui/opusvoce.h`), con FFI diretta a
//! libopus: nessun crate esterno, e le impostazioni sono quelle del C++.
//!
//! Parametri per la radio, non per la musica: VoIP, 48 kHz, frame di 20 ms,
//! banda massima 6 kHz (4 kHz per il CW), FEC in banda con perdita dichiarata
//! al 5%, DTX spento: il rumore di fondo e' informazione su una radio.

#![cfg(feature = "opus")]

use std::ffi::{c_char, c_int, CStr};

/// 48 kHz, frame da 20 ms: 960 campioni, come nel C++.
pub const RATE: i32 = 48_000;
pub const FRAME: usize = 960;
/// Pacchetto Opus piu' grande possibile.
pub const MAX_PACCHETTO: usize = 1275;

const OK: c_int = 0;
const APPLICATION_VOIP: c_int = 2048;
const BANDWIDTH_NARROWBAND: c_int = 1101;
const BANDWIDTH_MEDIUMBAND: c_int = 1102;
const BANDWIDTH_WIDEBAND: c_int = 1103;
const SET_BITRATE: c_int = 4002;
const SET_MAX_BANDWIDTH: c_int = 4004;
const SET_COMPLEXITY: c_int = 4010;
const SET_INBAND_FEC: c_int = 4012;
const SET_PACKET_LOSS_PERC: c_int = 4014;
const SET_DTX: c_int = 4016;
const SET_SIGNAL: c_int = 4024;
const SIGNAL_VOICE: c_int = 3001;

#[repr(C)]
pub struct Encoder {
    _privato: [u8; 0],
}
#[repr(C)]
pub struct Decoder {
    _privato: [u8; 0],
}

extern "C" {
    fn opus_encoder_create(fs: i32, canali: c_int, applicazione: c_int, errore: *mut c_int) -> *mut Encoder;
    fn opus_encoder_destroy(st: *mut Encoder);
    fn opus_encoder_ctl(st: *mut Encoder, richiesta: c_int, ...) -> c_int;
    fn opus_encode(st: *mut Encoder, pcm: *const i16, frame: c_int, dati: *mut u8, max: i32) -> i32;
    fn opus_decoder_create(fs: i32, canali: c_int, errore: *mut c_int) -> *mut Decoder;
    fn opus_decoder_destroy(st: *mut Decoder);
    fn opus_decode(st: *mut Decoder, dati: *const u8, len: i32, pcm: *mut i16, frame: c_int, fec: c_int) -> c_int;
    fn opus_strerror(errore: c_int) -> *const c_char;
    fn opus_get_version_string() -> *const c_char;
}

fn testo_errore(e: c_int) -> String {
    // SAFETY: opus_strerror restituisce una stringa statica terminata da NUL.
    unsafe { CStr::from_ptr(opus_strerror(e)) }.to_string_lossy().into_owned()
}

/// Versione di libopus collegata.
pub fn versione() -> String {
    // SAFETY: stringa statica di libopus.
    unsafe { CStr::from_ptr(opus_get_version_string()) }.to_string_lossy().into_owned()
}

/// Coppia codificatore e decodificatore, come `dl::OpusVoce`.
pub struct OpusVoce {
    enc: *mut Encoder,
    dec: *mut Decoder,
    bitrate: i32,
    banda: i32,
}

// SAFETY: libopus non tiene stato condiviso fra thread; uno stesso OpusVoce
// si usa da un solo thread alla volta (non e' Sync).
unsafe impl Send for OpusVoce {}

impl Default for OpusVoce {
    fn default() -> Self {
        OpusVoce {
            enc: std::ptr::null_mut(),
            dec: std::ptr::null_mut(),
            bitrate: 24_000,
            banda: 6_000,
        }
    }
}

impl OpusVoce {
    /// `banda_hz`: 4000 per il CW, 6000 per la fonia. `bitrate` in bit/s.
    pub fn apri(&mut self, bitrate: i32, banda_hz: i32) -> Result<(), String> {
        self.chiudi();
        let mut err: c_int = 0;
        // SAFETY: parametri validi; il puntatore d'errore e' un c_int locale.
        let enc = unsafe { opus_encoder_create(RATE, 1, APPLICATION_VOIP, &mut err) };
        if err != OK || enc.is_null() {
            return Err(testo_errore(err));
        }
        // SAFETY: come sopra.
        let dec = unsafe { opus_decoder_create(RATE, 1, &mut err) };
        if err != OK || dec.is_null() {
            // SAFETY: enc e' valido e non ancora condiviso.
            unsafe { opus_encoder_destroy(enc) };
            return Err(testo_errore(err));
        }
        self.enc = enc;
        self.dec = dec;

        let banda = if banda_hz <= 4000 {
            BANDWIDTH_NARROWBAND
        } else if banda_hz <= 6000 {
            BANDWIDTH_MEDIUMBAND
        } else {
            BANDWIDTH_WIDEBAND
        };
        self.ctl(SET_BITRATE, bitrate);
        self.ctl(SET_MAX_BANDWIDTH, banda);
        self.ctl(SET_SIGNAL, SIGNAL_VOICE);
        self.ctl(SET_COMPLEXITY, 8);
        self.ctl(SET_INBAND_FEC, 1);
        self.ctl(SET_PACKET_LOSS_PERC, 5);
        self.ctl(SET_DTX, 0);
        self.bitrate = bitrate;
        self.banda = banda_hz;
        Ok(())
    }

    fn ctl(&mut self, richiesta: c_int, valore: c_int) {
        if !self.enc.is_null() {
            // SAFETY: chiamata variadica con un solo intero, come vuole libopus.
            unsafe { opus_encoder_ctl(self.enc, richiesta, valore) };
        }
    }

    pub fn chiudi(&mut self) {
        if !self.enc.is_null() {
            // SAFETY: puntatore creato da opus_encoder_create e ancora valido.
            unsafe { opus_encoder_destroy(self.enc) };
            self.enc = std::ptr::null_mut();
        }
        if !self.dec.is_null() {
            // SAFETY: puntatore creato da opus_decoder_create e ancora valido.
            unsafe { opus_decoder_destroy(self.dec) };
            self.dec = std::ptr::null_mut();
        }
    }

    pub fn pronto(&self) -> bool {
        !self.enc.is_null() && !self.dec.is_null()
    }

    pub fn bitrate(&self) -> i32 {
        self.bitrate
    }

    pub fn banda(&self) -> i32 {
        self.banda
    }

    /// Cambia il bitrate senza ricreare il codificatore (niente scatto nell'audio).
    pub fn cambia_bitrate(&mut self, bitrate: i32) {
        if self.enc.is_null() || bitrate == self.bitrate {
            return;
        }
        self.ctl(SET_BITRATE, bitrate);
        self.bitrate = bitrate;
    }

    /// Perdita da dichiarare a Opus, limitata a 0..=30 come nel C++.
    pub fn perdita_attesa(&mut self, percento: i32) {
        self.ctl(SET_PACKET_LOSS_PERC, percento.clamp(0, 30));
    }

    /// Codifica esattamente `FRAME` campioni. `None` se la lunghezza e' sbagliata
    /// o la codifica fallisce: meglio saltare che mandare spazzatura.
    pub fn codifica(&mut self, pcm: &[i16]) -> Option<Vec<u8>> {
        if self.enc.is_null() || pcm.len() != FRAME {
            return None;
        }
        let mut out = vec![0u8; MAX_PACCHETTO];
        // SAFETY: pcm ha FRAME campioni; out ha MAX_PACCHETTO byte.
        let n = unsafe {
            opus_encode(self.enc, pcm.as_ptr(), FRAME as c_int, out.as_mut_ptr(), MAX_PACCHETTO as i32)
        };
        if n < 0 {
            return None;
        }
        out.truncate(n as usize);
        Some(out)
    }

    /// Decodifica un pacchetto. Senza pacchetto (`None`) Opus inventa il pezzo
    /// mancante: meglio un frammento ricostruito che un buco.
    pub fn decodifica(&mut self, pacchetto: Option<&[u8]>) -> Option<Vec<i16>> {
        if self.dec.is_null() {
            return None;
        }
        let mut pcm = vec![0i16; FRAME];
        let (ptr, len) = match pacchetto {
            Some(p) if !p.is_empty() => (p.as_ptr(), p.len() as i32),
            _ => (std::ptr::null(), 0),
        };
        // SAFETY: pcm ha FRAME campioni; ptr e' nullo oppure punta a p, vivo per la chiamata.
        let n = unsafe { opus_decode(self.dec, ptr, len, pcm.as_mut_ptr(), FRAME as c_int, 0) };
        if n < 0 {
            return None;
        }
        pcm.truncate(n as usize);
        Some(pcm)
    }
}

impl Drop for OpusVoce {
    fn drop(&mut self) {
        self.chiudi();
    }
}

#[cfg(test)]
mod test {
    use super::*;

    fn tono(n: usize, hz: f64, fase: &mut f64, amp: f64) -> Vec<i16> {
        (0..n)
            .map(|_| {
                *fase += 2.0 * std::f64::consts::PI * hz / f64::from(RATE);
                (amp * fase.sin()) as i16
            })
            .collect()
    }

    #[test]
    fn versione_di_libopus() {
        assert!(versione().starts_with("libopus"), "{}", versione());
    }

    #[test]
    fn codifica_e_decodifica_un_frame() {
        let mut o = OpusVoce::default();
        o.apri(24_000, 6_000).expect("apertura");
        assert!(o.pronto());
        let mut fase = 0.0;
        let mut ultimo = Vec::new();
        for _ in 0..10 {
            let f = tono(FRAME, 1000.0, &mut fase, 8000.0);
            let p = o.codifica(&f).expect("codifica");
            assert!(!p.is_empty() && p.len() <= MAX_PACCHETTO);
            ultimo = o.decodifica(Some(&p)).expect("decodifica");
        }
        assert_eq!(ultimo.len(), FRAME);
        let picco = ultimo.iter().map(|v| v.unsigned_abs()).max().unwrap_or(0);
        assert!(picco > 4000, "il tono deve tornare: picco {picco}");
    }

    #[test]
    fn lunghezza_sbagliata_e_rifiutata() {
        let mut o = OpusVoce::default();
        o.apri(24_000, 6_000).expect("apertura");
        assert!(o.codifica(&[0i16; 100]).is_none());
    }

    #[test]
    fn pacchetto_mancante_produce_un_frame() {
        let mut o = OpusVoce::default();
        o.apri(24_000, 6_000).expect("apertura");
        let pcm = o.decodifica(None).expect("mascheramento");
        assert_eq!(pcm.len(), FRAME);
    }

    #[test]
    fn cambio_di_bitrate_a_collegamento_aperto() {
        let mut o = OpusVoce::default();
        o.apri(24_000, 6_000).expect("apertura");
        o.cambia_bitrate(16_000);
        assert_eq!(o.bitrate(), 16_000);
        o.cambia_bitrate(16_000);
        assert_eq!(o.bitrate(), 16_000);
    }
}
