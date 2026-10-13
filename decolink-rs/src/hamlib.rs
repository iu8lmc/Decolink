//! Radio via Hamlib (porting di `gui/hamlibrig.h`), con FFI diretta a libhamlib.
//!
//! Il C++ scrive direttamente in `rig->state.rigport`. Qui non si ha bindgen, quindi
//! gli offset delle strutture sono costanti verificate contro il layout che il
//! compilatore C calcola sulle intestazioni installate (`tests/hamlib_offsets.txt`).
//! Se cambia la versione di Hamlib, il test di compatibilita' se ne accorge.

#![cfg(feature = "hamlib")]

use std::ffi::{c_char, c_int, c_long, c_void, CStr};
use std::sync::{Mutex, Once};
use std::net::{TcpStream, ToSocketAddrs};
use std::time::Duration;

// ---- costanti verificate contro hamlib 4.x (vedi tests/hamlib_offsets.txt)

const VFO_CURR: u32 = 536_870_912;
const RIG_OK: c_int = 0;
const PTT_OFF: c_int = 0;
const PTT_ON: c_int = 1;
const PORT_NETWORK: c_int = 2;
const PORT_UDP_NETWORK: c_int = 10;
const PARITY_NONE: c_int = 0;
const HANDSHAKE_NONE: c_int = 0;
const HANDSHAKE_XONXOFF: c_int = 1;
const HANDSHAKE_HARDWARE: c_int = 2;
const DEBUG_NONE: c_int = 0;
const PASSBAND_NORMAL: c_long = 0;
/// Il modello `netrigctl`: parla il protocollo di rigctld.
pub const MODEL_NETRIGCTL: i32 = 2;

pub const LEVEL_SWR: u64 = 268_435_456;
pub const LEVEL_ALC: u64 = 536_870_912;
pub const LEVEL_STRENGTH: u64 = 1_073_741_824;
pub const LEVEL_RFPOWER_METER: u64 = 4_294_967_296;
pub const LEVEL_RFPOWER_METER_WATTS: u64 = 549_755_813_888;

// Offset in byte dentro `struct s_rig`, `struct rig_caps` e `hamlib_port_t`.
const OFF_CAPS: usize = 0;
const OFF_STATE: usize = 16_328;
const OFF_RIGPORT_IN_STATE: usize = 14_200;
const OFF_CAPS_PORT_TYPE: usize = 56;
const OFF_HAS_GET_LEVEL_IN_STATE: usize = 7_128;
const OFF_TIMEOUT: usize = 32;
const OFF_RETRY: usize = 36;
const OFF_PATHNAME: usize = 40;
const OFF_SERIAL_RATE: usize = 552;
const OFF_SERIAL_DATA_BITS: usize = 556;
const OFF_SERIAL_STOP_BITS: usize = 560;
const OFF_SERIAL_PARITY: usize = 564;
const OFF_SERIAL_HANDSHAKE: usize = 568;
const PATHNAME_LEN: usize = 512;
/// Timeout delle letture in rete, come `kTimeoutRete` nel C++.
pub const TIMEOUT_RETE_MS: i32 = 1000;

/// `value_t` di Hamlib: unione da 16 byte. Il membro `f` sta in testa.
#[repr(C)]
pub struct ValueT([u8; 16]);

#[link(name = "hamlib")]
extern "C" {
    fn rig_set_debug(livello: c_int) -> c_int;
    fn rig_load_all_backends() -> c_int;
    fn rig_init(modello: i32) -> *mut c_void;
    fn rig_cleanup(rig: *mut c_void) -> c_int;
    fn rig_open(rig: *mut c_void) -> c_int;
    fn rig_close(rig: *mut c_void) -> c_int;
    fn rig_get_freq(rig: *mut c_void, vfo: u32, freq: *mut f64) -> c_int;
    fn rig_set_freq(rig: *mut c_void, vfo: u32, freq: f64) -> c_int;
    fn rig_get_mode(rig: *mut c_void, vfo: u32, mode: *mut u64, larghezza: *mut c_long) -> c_int;
    fn rig_set_mode(rig: *mut c_void, vfo: u32, mode: u64, larghezza: c_long) -> c_int;
    fn rig_get_ptt(rig: *mut c_void, vfo: u32, ptt: *mut c_int) -> c_int;
    fn rig_set_ptt(rig: *mut c_void, vfo: u32, ptt: c_int) -> c_int;
    fn rig_get_level(rig: *mut c_void, vfo: u32, livello: u64, valore: *mut ValueT) -> c_int;
    fn rig_strrmode(mode: u64) -> *const c_char;
    fn rig_parse_mode(nome: *const c_char) -> u64;
    fn rigerror(errore: c_int) -> *const c_char;
}

fn errore_hamlib(e: c_int) -> String {
    // SAFETY: rig_strerror restituisce una stringa statica.
    unsafe { CStr::from_ptr(rigerror(e)) }.to_string_lossy().into_owned()
}

/// Hamlib carica i backend in modo globale: farlo due volte in parallelo fa
/// crollare il processo. Si inizializza una volta sola, e le aperture e le
/// chiusure passano da un solo lock.
static INIZIO: Once = Once::new();
static CICLO_VITA: Mutex<()> = Mutex::new(());

/// Radio aperta. Si chiude da sola quando va fuori scope.
pub struct Radio {
    rig: *mut c_void,
    per_rete: bool,
}

impl Radio {
    /// Apre una radio. `percorso` e' la porta seriale (`COM3`) oppure `host:porta`
    /// per una radio condivisa in rete. Per la seriale servono baud, bit e handshake
    /// (`"n"`, `"h"` o `"s"`), come nel C++.
    pub fn apri(
        modello: i32,
        percorso: &str,
        baud: i32,
        bit_dati: i32,
        bit_stop: i32,
        handshake: &str,
    ) -> Result<Self, String> {
        INIZIO.call_once(|| {
            // SAFETY: inizializzazione globale di libhamlib, eseguita una volta sola.
            unsafe {
                rig_set_debug(DEBUG_NONE);
                rig_load_all_backends();
            }
        });
        let _lock = CICLO_VITA.lock().unwrap_or_else(|e| e.into_inner());
        // SAFETY: rig_init restituisce un puntatore valido o nullo.
        let rig = unsafe { rig_init(modello) };
        if rig.is_null() {
            return Err(format!("modello {modello} non disponibile in questa Hamlib"));
        }
        // SAFETY: il primo campo di s_rig e' il puntatore a rig_caps.
        let caps = unsafe { *(rig as *const *const u8).add(OFF_CAPS) };
        // SAFETY: caps punta a una rig_caps valida; port_type e' un int.
        let tipo = unsafe { *(caps.add(OFF_CAPS_PORT_TYPE) as *const c_int) };
        let per_rete = tipo == PORT_NETWORK || tipo == PORT_UDP_NETWORK;

        if per_rete && tipo == PORT_NETWORK {
            // Si bussa alla porta prima di chiamare Hamlib: rig_open, se nessuno
            // risponde, puo' restare fermo per decine di secondi (vedi il C++).
            sonda_rete(percorso)?;
        }

        let porta = porta_di(rig);
        scrivi_stringa(porta, OFF_PATHNAME, percorso, PATHNAME_LEN);
        if per_rete {
            scrivi_i32(porta, OFF_TIMEOUT, TIMEOUT_RETE_MS);
            scrivi_i16(porta, OFF_RETRY, 1);
        } else {
            scrivi_i32(porta, OFF_SERIAL_RATE, baud);
            scrivi_i32(porta, OFF_SERIAL_DATA_BITS, bit_dati);
            scrivi_i32(porta, OFF_SERIAL_STOP_BITS, bit_stop);
            scrivi_i32(porta, OFF_SERIAL_PARITY, PARITY_NONE);
            let hs = match handshake.chars().next().map(|c| c.to_ascii_lowercase()) {
                Some('h') => HANDSHAKE_HARDWARE,
                Some('s') => HANDSHAKE_XONXOFF,
                _ => HANDSHAKE_NONE,
            };
            scrivi_i32(porta, OFF_SERIAL_HANDSHAKE, hs);
        }

        // SAFETY: rig e' un rig_init valido.
        let e = unsafe { rig_open(rig) };
        if e != RIG_OK {
            let msg = errore_hamlib(e);
            // SAFETY: rig valido, non ancora usato altrove.
            unsafe { rig_cleanup(rig) };
            return Err(msg);
        }
        Ok(Radio { rig, per_rete })
    }

    pub fn per_rete(&self) -> bool {
        self.per_rete
    }

    pub fn frequenza(&mut self) -> Result<f64, String> {
        let mut f = 0.0f64;
        // SAFETY: rig aperto, f valido per la scrittura.
        let e = unsafe { rig_get_freq(self.rig, VFO_CURR, &mut f) };
        if e == RIG_OK { Ok(f) } else { Err(errore_hamlib(e)) }
    }

    pub fn imposta_frequenza(&mut self, hz: f64) -> Result<(), String> {
        // SAFETY: rig aperto.
        let e = unsafe { rig_set_freq(self.rig, VFO_CURR, hz) };
        if e == RIG_OK { Ok(()) } else { Err(errore_hamlib(e)) }
    }

    /// Modo come nome (`USB`, `CW`, ...) e larghezza di banda.
    pub fn modo(&mut self) -> Result<String, String> {
        let mut m: u64 = 0;
        let mut larg: c_long = 0;
        // SAFETY: rig aperto, puntatori validi.
        let e = unsafe { rig_get_mode(self.rig, VFO_CURR, &mut m, &mut larg) };
        if e != RIG_OK {
            return Err(errore_hamlib(e));
        }
        // SAFETY: rig_strrmode restituisce una stringa statica.
        Ok(unsafe { CStr::from_ptr(rig_strrmode(m)) }.to_string_lossy().into_owned())
    }

    /// Imposta il modo per nome, con la banda passante scelta da Hamlib.
    pub fn imposta_modo(&mut self, nome: &str) -> Result<(), String> {
        let c = std::ffi::CString::new(nome).map_err(|e| e.to_string())?;
        // SAFETY: c e' una stringa NUL-terminata viva per la chiamata.
        let m = unsafe { rig_parse_mode(c.as_ptr()) };
        if m == 0 {
            return Err(format!("modo sconosciuto: {nome}"));
        }
        // SAFETY: rig aperto.
        let e = unsafe { rig_set_mode(self.rig, VFO_CURR, m, PASSBAND_NORMAL) };
        if e == RIG_OK { Ok(()) } else { Err(errore_hamlib(e)) }
    }

    pub fn ptt(&mut self) -> Result<bool, String> {
        let mut p: c_int = PTT_OFF;
        // SAFETY: rig aperto, p valido.
        let e = unsafe { rig_get_ptt(self.rig, VFO_CURR, &mut p) };
        if e == RIG_OK { Ok(p != PTT_OFF) } else { Err(errore_hamlib(e)) }
    }

    pub fn imposta_ptt(&mut self, on: bool) -> Result<(), String> {
        // SAFETY: rig aperto.
        let e = unsafe { rig_set_ptt(self.rig, VFO_CURR, if on { PTT_ON } else { PTT_OFF }) };
        if e == RIG_OK { Ok(()) } else { Err(errore_hamlib(e)) }
    }

    /// Un livello in virgola mobile (misuratori). `None` se la radio non lo espone.
    pub fn livello(&mut self, quale: u64) -> Option<f32> {
        let mut v = ValueT([0; 16]);
        // SAFETY: rig aperto, v e' una value_t di 16 byte.
        let e = unsafe { rig_get_level(self.rig, VFO_CURR, quale, &mut v) };
        if e != RIG_OK {
            return None;
        }
        Some(f32::from_le_bytes([v.0[0], v.0[1], v.0[2], v.0[3]]))
    }

    /// Dichiara i misuratori a un server in rete che non li annuncia da solo.
    pub fn aggiungi_misuratori(&mut self) {
        if !self.per_rete {
            return;
        }
        let misuratori = LEVEL_SWR | LEVEL_ALC | LEVEL_STRENGTH | LEVEL_RFPOWER_METER | LEVEL_RFPOWER_METER_WATTS;
        let p = self.rig as *mut u8;
        // SAFETY: l'offset e' dentro s_rig, verificato dal test di compatibilita'.
        unsafe {
            let campo = p.add(OFF_STATE + OFF_HAS_GET_LEVEL_IN_STATE) as *mut u64;
            *campo |= misuratori;
        }
    }
}

impl Drop for Radio {
    fn drop(&mut self) {
        if !self.rig.is_null() {
            let _lock = CICLO_VITA.lock().unwrap_or_else(|e| e.into_inner());
            // SAFETY: rig aperto e mai liberato.
            unsafe {
                rig_close(self.rig);
                rig_cleanup(self.rig);
            }
            self.rig = std::ptr::null_mut();
        }
    }
}

fn porta_di(rig: *mut c_void) -> *mut u8 {
    // SAFETY: l'offset e' dentro s_rig.
    unsafe { (rig as *mut u8).add(OFF_STATE + OFF_RIGPORT_IN_STATE) }
}

fn scrivi_i32(base: *mut u8, off: usize, v: i32) {
    // SAFETY: offset dentro hamlib_port_t, verificato.
    unsafe { (base.add(off) as *mut i32).write_unaligned(v) }
}

fn scrivi_i16(base: *mut u8, off: usize, v: i16) {
    // SAFETY: offset dentro hamlib_port_t, verificato.
    unsafe { (base.add(off) as *mut i16).write_unaligned(v) }
}

fn scrivi_stringa(base: *mut u8, off: usize, s: &str, max: usize) {
    let b = s.as_bytes();
    let n = b.len().min(max - 1);
    // SAFETY: il campo ha `max` byte; si scrive al massimo max-1 piu' il NUL.
    unsafe {
        let dst = base.add(off);
        std::ptr::copy_nonoverlapping(b.as_ptr(), dst, n);
        *dst.add(n) = 0;
    }
}

/// Bussa alla porta di rete con un tempo massimo, come fa il C++ prima di rig_open.
fn sonda_rete(indirizzo: &str) -> Result<(), String> {
    let mut it = indirizzo
        .to_socket_addrs()
        .map_err(|e| format!("indirizzo {indirizzo}: {e}"))?;
    let addr = it.next().ok_or_else(|| format!("indirizzo {indirizzo} senza risultati"))?;
    TcpStream::connect_timeout(&addr, Duration::from_millis(1500))
        .map(|_| ())
        .map_err(|_| format!("nessuno risponde su {indirizzo}"))
}

#[cfg(test)]
mod test {
    use super::*;

    /// Il file generato dal compilatore C deve coincidere con le costanti del modulo.
    #[test]
    fn offset_come_il_compilatore_c() {
        let testo = include_str!("../tests/hamlib_offsets.txt");
        let mut mappa = std::collections::HashMap::new();
        for riga in testo.lines() {
            let mut it = riga.split_whitespace();
            if let (Some(k), Some(v)) = (it.next(), it.next()) {
                mappa.insert(k.to_string(), v.parse::<u64>().unwrap());
            }
        }
        let attesi = [
            ("rig.caps", OFF_CAPS as u64),
            ("rig.state", OFF_STATE as u64),
            ("state.rigport", OFF_RIGPORT_IN_STATE as u64),
            ("caps.port_type", OFF_CAPS_PORT_TYPE as u64),
            ("state.has_get_level", OFF_HAS_GET_LEVEL_IN_STATE as u64),
            ("rigport.timeout", OFF_TIMEOUT as u64),
            ("rigport.retry", OFF_RETRY as u64),
            ("rigport.pathname", OFF_PATHNAME as u64),
            ("rigport.serial_rate", OFF_SERIAL_RATE as u64),
            ("rigport.serial_data_bits", OFF_SERIAL_DATA_BITS as u64),
            ("rigport.serial_stop_bits", OFF_SERIAL_STOP_BITS as u64),
            ("rigport.serial_parity", OFF_SERIAL_PARITY as u64),
            ("rigport.serial_handshake", OFF_SERIAL_HANDSHAKE as u64),
            ("value.f", 0),
        ];
        for (nome, valore) in attesi {
            assert_eq!(mappa.get(nome), Some(&valore), "offset di {nome}");
        }
        assert_eq!(mappa.get("RIG_LEVEL_SWR"), Some(&LEVEL_SWR));
        assert_eq!(mappa.get("RIG_LEVEL_ALC"), Some(&LEVEL_ALC));
        assert_eq!(mappa.get("RIG_LEVEL_STRENGTH"), Some(&LEVEL_STRENGTH));
        assert_eq!(mappa.get("RIG_LEVEL_RFPOWER_METER"), Some(&LEVEL_RFPOWER_METER));
        assert_eq!(mappa.get("RIG_LEVEL_RFPOWER_METER_WATTS"), Some(&LEVEL_RFPOWER_METER_WATTS));
        assert_eq!(mappa.get("RIG_VFO_CURR"), Some(&(VFO_CURR as u64)));
        assert_eq!(mappa.get("RIG_MODEL_NETRIGCTL"), Some(&(MODEL_NETRIGCTL as u64)));
        assert_eq!(mappa.get("RIG_PORT_NETWORK"), Some(&(PORT_NETWORK as u64)));
        assert_eq!(mappa.get("RIG_PORT_UDP_NETWORK"), Some(&(PORT_UDP_NETWORK as u64)));
    }

    #[test]
    fn percorso_troppo_lungo_si_tronca() {
        let mut buf = vec![0u8; 16];
        scrivi_stringa(buf.as_mut_ptr(), 0, "0123456789abcdefXYZ", 16);
        assert_eq!(buf[15], 0);
        assert_eq!(&buf[..15], b"0123456789abcde");
    }

    #[test]
    fn sonda_non_trova_nessuno() {
        // porta quasi certamente chiusa in locale
        assert!(sonda_rete("127.0.0.1:1").is_err());
    }
}
