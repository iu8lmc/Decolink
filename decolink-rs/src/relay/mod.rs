//! Relay UDP autenticato del gateway Decolink (porting di `server/decolink_relay.py`).
//!
//! Stessa logica, stessi messaggi, stesso database. Il relay non decide nulla da
//! solo: chi puo' entrare e con che poteri sta nel database, riletto ogni pochi
//! secondi. Non guarda dentro i pacchetti audio: inoltra per tipo.

pub mod db;
pub mod token;

use std::collections::{HashMap, HashSet};
use std::net::{SocketAddr, UdpSocket};
use std::path::PathBuf;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

use rusqlite::Connection;

use token::{Dati, TokenError};

// ---------------------------------------------------------------- protocollo

/// Intestazione v2 (registrazione, PING, CAT, audio TX): 22 byte.
pub const V2_HDR: usize = 22;
const V2_MAGIC: &[u8; 4] = b"HFGW";
const V2_VER: u8 = 2;

pub const F_AUDIO: u8 = 0;
pub const F_PING: u8 = 1;
pub const F_PONG: u8 = 2;
pub const F_REGISTER: u8 = 3;
pub const F_PEERUP: u8 = 4;
pub const F_CAT_REQ: u8 = 5;
pub const F_CAT_RSP: u8 = 6;
pub const F_TX_AUDIO: u8 = 7;
pub const F_DENIED: u8 = 8;
pub const F_TX_STATE: u8 = 9;

/// Piano dati v3: intestazione di 10 byte che comincia per 'D'.
const V3_MAGIC: u8 = 0x44;
const V3_VER: u8 = 3;
const V3_HDR: usize = 10;
const V3_AUDIO_RX: u8 = 0;
const V3_AUDIO_TX: u8 = 1;
const V3_CTRL: u8 = 2;
const V3_CAT: u8 = 3;
const V3_NACK: u8 = 4;
const V3_PING: u8 = 5;


const CLIENT_TIMEOUT: f64 = 15.0;
const GRANT_REFRESH: f64 = 5.0;
const TX_IDLE: f64 = 1.5;
const TX_GRACE: f64 = 2.5;
const ROOM_MAX: usize = 8;
const CAT_ROUTE_TTL: f64 = 10.0;
const TX_STATE_EVERY: f64 = 5.0;
const RPRT_REJECTED: &[u8] = b"RPRT -8\n";

/// Comandi CAT che si limitano a leggere. Tutto il resto e' scrittura.
const CAT_LEGGE: &[&str] = &[
    "f", "m", "t", "s", "i", "x", "v", "j", "u", "d", "l", "n", "q", "1",
    "get_freq", "get_mode", "get_ptt", "get_split_vfo", "get_split_freq",
    "get_split_mode", "get_vfo", "get_level", "get_info", "dump_state",
    "chk_vfo", "get_rit", "get_xit", "get_powerstat", "get_dcd", "get_func",
    "get_parm", "get_rig_info",
];

/// 'ptt_on', 'ptt_off', 'scrive' o 'legge' per una riga nel dialetto rigctl.
pub fn classifica_cat(testo: &str) -> &'static str {
    let riga = testo.trim().trim_start_matches('+').trim();
    if riga.is_empty() {
        return "legge";
    }
    let (primo, resto) = match riga.find(' ') {
        Some(i) => (&riga[..i], &riga[i + 1..]),
        None => (riga, ""),
    };
    let lungo = primo.starts_with('\\');
    let cmd = primo.trim_start_matches('\\');
    if cmd == "T" || cmd == "set_ptt" {
        return match resto.split_whitespace().next().and_then(|v| v.parse::<i64>().ok()) {
            Some(v) => {
                if v != 0 { "ptt_on" } else { "ptt_off" }
            }
            None => "scrive",
        };
    }
    if cmd.chars().count() == 1 && !lungo {
        // i comandi corti distinguono le maiuscole: 'f' legge, 'F' scrive
        return if CAT_LEGGE.contains(&cmd) { "legge" } else { "scrive" };
    }
    if CAT_LEGGE.contains(&cmd.to_lowercase().as_str()) { "legge" } else { "scrive" }
}

/// Intestazione v2 con il formato di rete (big-endian).
pub fn hdr(flags: u8, seq: u32, tms: u64, rate: u32) -> [u8; V2_HDR] {
    let mut h = [0u8; V2_HDR];
    h[0..4].copy_from_slice(V2_MAGIC);
    h[4] = V2_VER;
    h[5] = flags;
    h[6..10].copy_from_slice(&seq.to_be_bytes());
    h[10..18].copy_from_slice(&tms.to_be_bytes());
    h[18..22].copy_from_slice(&rate.to_be_bytes());
    h
}

/// Pacchetto di testo: intestazione e testo, troncato a 400 byte come nel Python.
pub fn pkt(flags: u8, testo: &str) -> Vec<u8> {
    let mut v = hdr(flags, 0, 0, 48_000).to_vec();
    let b = testo.as_bytes();
    v.extend_from_slice(&b[..b.len().min(400)]);
    v
}

/// Istante attuale in secondi dall'epoca, come `time.time()` nel Python.
pub fn ora() -> f64 {
    SystemTime::now().duration_since(UNIX_EPOCH).map(|d| d.as_secs_f64()).unwrap_or(0.0)
}

fn latin1(b: &[u8]) -> String {
    b.iter().map(|c| *c as char).collect()
}

// ------------------------------------------------------------------- sessioni

#[derive(Debug, Clone)]
struct Sessione {
    addr: SocketAddr,
    user_id: i64,
    callsign: String,
    station_id: i64,
    role: String,
    jti: String,
    expires: i64,
    is_gw: bool,
    conn_row: Option<i64>,
    tx_row: Option<i64>,
    tx_last: f64,
    last_seen: f64,
}

impl Sessione {
    fn puo_trasmettere(&self) -> bool {
        token::puo_trasmettere(&self.role)
    }

    fn descrizione(&self) -> String {
        format!("{}({})", self.callsign, if self.is_gw { "gw".to_string() } else { self.role.clone() })
    }
}

/// Stato del relay. Il socket UDP e' dentro, cosi' ogni risposta esce dallo stesso punto.
pub struct Relay {
    sock: UdpSocket,
    segreto: Vec<u8>,
    db: Connection,
    sess: HashMap<SocketAddr, Sessione>,
    rooms: HashMap<i64, HashSet<SocketAddr>>,
    tx_holder: HashMap<i64, SocketAddr>,
    cat_route: HashMap<(i64, u16), (SocketAddr, f64)>,
    tx_annunciato: HashMap<i64, (Option<SocketAddr>, f64)>,
    grants: HashMap<(i64, i64), String>,
    revoked: HashSet<String>,
    last_grants: f64,
    pub fwd: u64,
    pub rej: u64,
}

impl Relay {
    pub fn nuovo(sock: UdpSocket, segreto: Vec<u8>, db: Connection) -> Self {
        Relay {
            sock,
            segreto,
            db,
            sess: HashMap::new(),
            rooms: HashMap::new(),
            tx_holder: HashMap::new(),
            cat_route: HashMap::new(),
            tx_annunciato: HashMap::new(),
            grants: HashMap::new(),
            revoked: HashSet::new(),
            last_grants: 0.0,
            fwd: 0,
            rej: 0,
        }
    }

    /// Socket UDP sulla porta data, con timeout di lettura di un secondo.
    pub fn apri_socket(porta: u16) -> std::io::Result<UdpSocket> {
        let s = UdpSocket::bind(("0.0.0.0", porta))?;
        s.set_read_timeout(Some(Duration::from_secs(1)))?;
        Ok(s)
    }

    pub fn numero_sessioni(&self) -> usize {
        self.sess.len()
    }

    pub fn numero_stazioni(&self) -> usize {
        self.rooms.len()
    }

    pub fn permessi(&self) -> usize {
        self.grants.len()
    }

    fn invia(&self, dati: &[u8], a: SocketAddr) {
        let _ = self.sock.send_to(dati, a);
    }

    // ------------------------------------------------------------ permessi

    /// Rilegge dal database chi ha diritto a cosa. Se il database non risponde
    /// si tiene la fotografia precedente.
    pub fn aggiorna_permessi(&mut self, now: f64, forza: bool) {
        if !forza && now - self.last_grants < GRANT_REFRESH {
            return;
        }
        self.last_grants = now;
        let (g, r) = match (db::permessi_attivi(&self.db), db::revocati(&self.db)) {
            (Ok(g), Ok(r)) => (g, r),
            (Err(e), _) | (_, Err(e)) => {
                println!("  [attenzione] permessi non rileggibili: {e}");
                return;
            }
        };
        self.grants = g;
        self.revoked = r;
        let indirizzi: Vec<SocketAddr> = self.sess.keys().copied().collect();
        for addr in indirizzi {
            let Some(s) = self.sess.get(&addr).cloned() else { continue };
            let ruolo = self.grants.get(&(s.user_id, s.station_id)).cloned();
            if self.revoked.contains(&s.jti) {
                self.espelli(addr, "sessione revocata");
            } else if ruolo.is_none() {
                self.espelli(addr, "permesso revocato");
            } else if let Some(r) = ruolo {
                if r != s.role {
                    println!("  ~ {} passa a '{}'", s.descrizione(), r);
                    if let Some(x) = self.sess.get_mut(&addr) {
                        x.role = r.clone();
                    }
                    if !token::puo_trasmettere(&r) {
                        self.fine_tx(addr, now);
                    }
                }
            }
        }
    }

    fn verifica(&self, token_txt: &str, now: f64) -> Result<Dati, TokenError> {
        let mut dati = token::verifica(&self.segreto, token_txt, now)?;
        if self.revoked.contains(&dati.jti) {
            return Err(TokenError("sessione revocata".into()));
        }
        let ruolo = self
            .grants
            .get(&(dati.user_id, dati.station_id))
            .ok_or_else(|| TokenError("permesso non piu' valido".into()))?;
        dati.role = ruolo.clone();
        Ok(dati)
    }

    // ------------------------------------------------------------ sessioni

    fn gateway_di(&self, station: i64) -> Option<Sessione> {
        self.rooms.get(&station)?.iter().filter_map(|a| self.sess.get(a)).find(|s| s.is_gw).cloned()
    }

    /// Registrazione v2: `gw <token>`, `op <token>`, o il token da solo.
    pub fn registra(&mut self, addr: SocketAddr, payload: &str, seq: u32, now: f64) {
        let payload = payload.trim();
        let (tipo, resto) = match payload.find(' ') {
            Some(i) => (payload[..i].trim().to_lowercase(), &payload[i + 1..]),
            None => (payload.trim().to_lowercase(), ""),
        };
        let (tipo, token_txt) = if tipo == "gw" || tipo == "op" {
            (tipo, resto.trim().to_string())
        } else if payload.starts_with(token::PREFIX) && payload[token::PREFIX.len()..].starts_with('.') {
            ("op".to_string(), payload.to_string())
        } else {
            let mostra: String = payload.chars().take(24).collect::<String>().replace('\n', " ");
            let mostra = if mostra.is_empty() { "(vuoto)".to_string() } else { mostra };
            println!(
                "  ? {}:{} si presenta con «{}»{} ({} caratteri)",
                addr.ip(),
                addr.port(),
                mostra,
                if payload.chars().count() > 24 { "…" } else { "" },
                payload.chars().count()
            );
            self.rifiuta(
                addr,
                "serve una chiave di accesso: aggiorna il programma, oppure incolla la chiave di stazione al posto della stanza",
            );
            return;
        };
        if token_txt.is_empty() {
            self.rifiuta(addr, "chiave di accesso mancante");
            return;
        }
        let dati = match self.verifica(&token_txt, now) {
            Ok(d) => d,
            Err(e) => {
                self.rifiuta(addr, &e.0);
                return;
            }
        };

        if let Some(vecchia) = self.sess.get_mut(&addr) {
            // keepalive: il client rimanda il REGISTER ogni 5 secondi
            if vecchia.jti == dati.jti {
                vecchia.last_seen = now;
                self.invia(&hdr(F_REGISTER, seq, 0, 48_000), addr);
                return;
            }
            self.chiudi(addr, "nuova registrazione");
        }

        let is_gw = tipo == "gw";
        if is_gw && !token::puo_trasmettere(&dati.role) {
            self.rifiuta(addr, "serve il ruolo di operatore per fare da gateway");
            return;
        }

        let station = dati.station_id;
        let n_membri = self.rooms.entry(station).or_default().len();
        if is_gw {
            if let Some(altro) = self.gateway_di(station) {
                self.rifiuta(addr, &format!("la stazione ha gia' un gateway ({})", altro.callsign));
                return;
            }
        } else if n_membri >= ROOM_MAX {
            self.rifiuta(addr, "stazione al completo");
            return;
        }

        let riga = match db::registra_ingresso(&self.db, dati.user_id, &dati.callsign, station, &dati.role,
                                               &format!("{}:{}", addr.ip(), addr.port())) {
            Ok(id) => Some(id),
            Err(e) => {
                println!("  [attenzione] collegamento non registrato: {e}");
                None
            }
        };

        let s = Sessione {
            addr,
            user_id: dati.user_id,
            callsign: dati.callsign.clone(),
            station_id: station,
            role: dati.role.clone(),
            jti: dati.jti.clone(),
            expires: dati.expires,
            is_gw,
            conn_row: riga,
            tx_row: None,
            tx_last: 0.0,
            last_seen: now,
        };
        println!(
            "  + {} entra sulla stazione {} da {}:{} ({}/{})",
            s.descrizione(),
            station,
            addr.ip(),
            addr.port(),
            n_membri + 1,
            ROOM_MAX
        );
        self.sess.insert(addr, s);
        self.rooms.entry(station).or_default().insert(addr);
        self.invia(&hdr(F_REGISTER, seq, 0, 48_000), addr);

        let membri: Vec<SocketAddr> = self.rooms.get(&station).map(|m| m.iter().copied().collect()).unwrap_or_default();
        if self.gateway_di(station).is_some() && membri.len() >= 2 {
            for a in &membri {
                self.invia(&hdr(F_PEERUP, 0, 0, 48_000), *a);
            }
        }
        self.annuncia_tx(station, now, true);
    }

    /// Dice al client perche' non entra, cosi' puo' mostrarlo.
    fn rifiuta(&mut self, addr: SocketAddr, motivo: &str) {
        self.rej += 1;
        println!("  ! {}:{} respinto: {}", addr.ip(), addr.port(), motivo);
        self.invia(&pkt(F_DENIED, motivo), addr);
    }

    fn espelli(&mut self, addr: SocketAddr, motivo: &str) {
        self.invia(&pkt(F_DENIED, motivo), addr);
        self.chiudi(addr, motivo);
    }

    fn chiudi(&mut self, addr: SocketAddr, motivo: &str) {
        let Some(s) = self.sess.remove(&addr) else { return };
        self.fine_tx_campi(addr, s.station_id, s.tx_row, &s.callsign, ora());
        let vuota = {
            let membri = self.rooms.entry(s.station_id).or_default();
            membri.remove(&addr);
            membri.is_empty()
        };
        if vuota {
            self.rooms.remove(&s.station_id);
            self.tx_holder.remove(&s.station_id);
        }
        if let Some(id) = s.conn_row {
            let _ = db::registra_uscita(&self.db, id);
        }
        let extra = if motivo.is_empty() { String::new() } else { format!(" ({motivo})") };
        println!("  - {} lascia la stazione {}{}", s.descrizione(), s.station_id, extra);
    }

    // --------------------------------------------------------- trasmissione

    /// Chiede il PTT per questa sessione. False se ce l'ha un altro.
    fn inizio_tx(&mut self, addr: SocketAddr, now: f64) -> bool {
        let Some(s) = self.sess.get(&addr).cloned() else { return false };
        let station = s.station_id;
        if let Some(attuale) = self.tx_holder.get(&station).copied() {
            if attuale != addr {
                if let Some(altro) = self.sess.get(&attuale).cloned() {
                    if now - altro.tx_last < TX_IDLE {
                        return false;
                    }
                    self.fine_tx(attuale, now);
                }
            }
        }

        if self.tx_holder.get(&station) != Some(&addr) {
            self.tx_holder.insert(station, addr);
            let indirizzo = format!("{}:{}", addr.ip(), addr.port());
            match db::inizia_trasmissione(&self.db, s.user_id, &s.callsign, station, &indirizzo) {
                Ok(id) => {
                    if let Some(x) = self.sess.get_mut(&addr) {
                        x.tx_row = Some(id);
                    }
                }
                Err(e) => println!("  [attenzione] trasmissione non registrata: {e}"),
            }
            println!("  TX {} sulla stazione {}", s.callsign, station);
            if let Some(x) = self.sess.get_mut(&addr) {
                x.tx_last = now;
            }
            self.annuncia_tx(station, now, false);
        }
        if let Some(x) = self.sess.get_mut(&addr) {
            x.tx_last = now;
        }
        true
    }

    /// Chi ha il PTT adesso, se e' ancora in trasmissione.
    fn titolare_tx(&self, station: i64, now: f64) -> Option<SocketAddr> {
        let addr = *self.tx_holder.get(&station)?;
        let s = self.sess.get(&addr)?;
        if now - s.tx_last < TX_IDLE { Some(addr) } else { None }
    }

    /// Se un comando CAT puo' arrivare alla radio. Come MultiFLEX: primo arrivato, primo servito.
    fn arbitra_cat(&mut self, addr: SocketAddr, testo: &str, now: f64) -> bool {
        let genere = classifica_cat(testo);
        if genere == "legge" {
            return true;
        }
        let station = match self.sess.get(&addr) {
            Some(s) => s.station_id,
            None => return false,
        };
        let altro = self.titolare_tx(station, now).filter(|a| *a != addr);
        if genere == "ptt_on" {
            if !self.inizio_tx(addr, now) {
                return false;
            }
            // il primo audio arriva dopo l'anticipo dichiarato: si concede un po'
            if let Some(x) = self.sess.get_mut(&addr) {
                x.tx_last = now + TX_GRACE;
            }
            return true;
        }
        altro.is_none()
    }

    /// Dice a ognuno nella stanza chi ha il PTT, dal suo punto di vista.
    fn annuncia_tx(&mut self, station: i64, now: f64, forza: bool) {
        let membri: Vec<SocketAddr> = self.rooms.get(&station).map(|m| m.iter().copied().collect()).unwrap_or_default();
        let titolare = self.titolare_tx(station, now);
        if !forza {
            if let Some((chiave, _)) = self.tx_annunciato.get(&station) {
                if *chiave == titolare {
                    return;
                }
            }
        }
        self.tx_annunciato.insert(station, (titolare, now));
        let nominativo = titolare.and_then(|a| self.sess.get(&a)).map(|s| s.callsign.clone());
        for a in membri {
            if !self.sess.contains_key(&a) {
                continue;
            }
            let testo = match (titolare, &nominativo) {
                (None, _) => "tx free".to_string(),
                (Some(t), _) if t == a => "tx you".to_string(),
                (Some(_), Some(n)) => format!("tx busy {n}"),
                (Some(_), None) => "tx free".to_string(),
            };
            self.invia(&pkt(F_TX_STATE, &testo), a);
        }
    }

    /// Chiude la trasmissione di una sessione presente nella tabella.
    fn fine_tx(&mut self, addr: SocketAddr, now: f64) {
        let Some(s) = self.sess.get_mut(&addr) else { return };
        let (station, riga, nome) = (s.station_id, s.tx_row.take(), s.callsign.clone());
        self.fine_tx_campi(addr, station, riga, &nome, now);
    }

    fn fine_tx_campi(&mut self, addr: SocketAddr, station: i64, riga: Option<i64>, nome: &str, now: f64) {
        if self.tx_holder.get(&station) == Some(&addr) {
            self.tx_holder.remove(&station);
            self.annuncia_tx(station, now, false);
        }
        if let Some(id) = riga {
            let _ = db::finisci_trasmissione(&self.db, id);
            println!("  TX {nome} finita");
        }
    }

    // ------------------------------------------------------------ inoltro

    fn membri_altri(&self, station: i64, da: SocketAddr) -> Vec<SocketAddr> {
        self.rooms.get(&station).map(|m| m.iter().copied().filter(|a| *a != da).collect()).unwrap_or_default()
    }

    /// Inoltro dei pacchetti v3, con le stesse regole della v2.
    fn inoltra_v3(&mut self, addr: SocketAddr, tipo: u8, seq: u16, data: &[u8], now: f64) {
        let Some(s) = self.sess.get(&addr).cloned() else { return };
        let station = s.station_id;

        match tipo {
            V3_AUDIO_RX => {
                if !s.is_gw {
                    return;
                }
                for a in self.membri_altri(station, addr) {
                    self.invia(data, a);
                    self.fwd += 1;
                }
            }
            V3_AUDIO_TX | V3_CAT | V3_NACK => {
                if s.is_gw {
                    // il gateway risponde a CAT e NACK: tornano a chi ha chiesto
                    if tipo == V3_CAT || tipo == V3_NACK {
                        if let Some((dest, _)) = self.cat_route.remove(&(station, seq)) {
                            self.invia(data, dest);
                            self.fwd += 1;
                        } else {
                            for a in self.membri_altri(station, addr) {
                                self.invia(data, a);
                                self.fwd += 1;
                            }
                        }
                    }
                    return;
                }
                if !s.puo_trasmettere() {
                    self.rej += 1;
                    return;
                }
                let Some(gw) = self.gateway_di(station) else { return };
                if tipo == V3_AUDIO_TX && !self.inizio_tx(addr, now) {
                    return;
                }
                let mut testo_cat = String::new();
                if tipo == V3_CAT {
                    testo_cat = latin1(&data[V3_HDR.min(data.len())..]);
                    if !self.arbitra_cat(addr, &testo_cat, now) {
                        println!("  x {} rifiutato per PTT occupato: {}", s.descrizione(),
                                 testo_cat.trim().chars().take(24).collect::<String>());
                        let mut r = data[..V3_HDR.min(data.len())].to_vec();
                        r.extend_from_slice(RPRT_REJECTED);
                        self.invia(&r, addr);
                        self.rej += 1;
                        return;
                    }
                }
                if tipo == V3_CAT || tipo == V3_NACK {
                    self.cat_route.insert((station, seq), (addr, now));
                }
                self.invia(data, gw.addr);
                self.fwd += 1;
                if tipo == V3_CAT && classifica_cat(&testo_cat) == "ptt_off" {
                    self.fine_tx(addr, now);
                }
            }
            V3_CTRL => {
                // negoziazione e report: il relay li passa senza leggerli
                if s.is_gw {
                    for a in self.membri_altri(station, addr) {
                        self.invia(data, a);
                        self.fwd += 1;
                    }
                } else if let Some(gw) = self.gateway_di(station) {
                    self.invia(data, gw.addr);
                    self.fwd += 1;
                }
            }
            V3_PING => self.invia(data, addr),
            _ => {}
        }
    }

    /// Inoltro dei pacchetti v2 (audio RX, CAT, audio TX).
    fn inoltra(&mut self, addr: SocketAddr, flags: u8, seq: u32, data: &[u8], now: f64) {
        let Some(s) = self.sess.get(&addr).cloned() else { return };
        let station = s.station_id;

        match flags {
            F_AUDIO => {
                if !s.is_gw {
                    return;
                }
                for a in self.membri_altri(station, addr) {
                    self.invia(data, a);
                    self.fwd += 1;
                }
            }
            F_TX_AUDIO | F_CAT_REQ => {
                if s.is_gw {
                    return;
                }
                if !s.puo_trasmettere() {
                    self.rej += 1;
                    return;
                }
                let Some(gw) = self.gateway_di(station) else { return };
                if flags == F_TX_AUDIO && !self.inizio_tx(addr, now) {
                    return;
                }
                let mut testo = String::new();
                if flags == F_CAT_REQ {
                    testo = latin1(&data[V2_HDR.min(data.len())..]);
                    if !self.arbitra_cat(addr, &testo, now) {
                        println!("  x {} rifiutato per PTT occupato: {}", s.descrizione(),
                                 testo.trim().chars().take(24).collect::<String>());
                        let mut r = hdr(F_CAT_RSP, seq, 0, 48_000).to_vec();
                        r.extend_from_slice(RPRT_REJECTED);
                        self.invia(&r, addr);
                        self.rej += 1;
                        return;
                    }
                    self.cat_route.insert((station, seq as u16), (addr, now));
                }
                self.invia(data, gw.addr);
                self.fwd += 1;
                if flags == F_CAT_REQ && classifica_cat(&testo) == "ptt_off" {
                    self.fine_tx(addr, now);
                }
            }
            F_CAT_RSP => {
                if !s.is_gw {
                    return;
                }
                if let Some((dest, _)) = self.cat_route.remove(&(station, seq as u16)) {
                    self.invia(data, dest);
                    self.fwd += 1;
                } else {
                    for a in self.membri_altri(station, addr) {
                        self.invia(data, a);
                        self.fwd += 1;
                    }
                }
            }
            _ => {}
        }
    }

    // ---------------------------------------------------------- manutenzione

    pub fn pulisci(&mut self, now: f64) {
        let indirizzi: Vec<SocketAddr> = self.sess.keys().copied().collect();
        for addr in indirizzi {
            let Some(s) = self.sess.get(&addr).cloned() else { continue };
            if now - s.last_seen > CLIENT_TIMEOUT {
                self.chiudi(addr, "silenzio");
            } else if (s.expires as f64) < now {
                // token scaduto: il client ne chiede uno nuovo e si ripresenta
                self.espelli(addr, "token scaduto, rinnovalo");
            } else if s.tx_row.is_some() && now - s.tx_last > TX_IDLE {
                self.fine_tx(addr, now);
            }
        }
        let stazioni: Vec<i64> = self.rooms.keys().copied().collect();
        for sid in stazioni {
            let rinnova = match self.tx_annunciato.get(&sid) {
                None => true,
                Some((_, quando)) => now - quando >= TX_STATE_EVERY,
            };
            self.annuncia_tx(sid, now, rinnova);
        }
        self.cat_route.retain(|_, (_, quando)| now - *quando <= CAT_ROUTE_TTL);
    }

    /// Un giro di ricezione: smista il datagramma. Ritorna false se non e' un pacchetto da trattare.
    pub fn gestisci(&mut self, data: &[u8], addr: SocketAddr, now: f64) {
        if data.len() >= V3_HDR && data[0] == V3_MAGIC && (data[1] >> 4) == V3_VER {
            if let Some(s) = self.sess.get_mut(&addr) {
                s.last_seen = now;
                let tipo = data[1] & 0xF;
                let seq = u16::from_be_bytes([data[4], data[5]]);
                self.inoltra_v3(addr, tipo, seq, data, now);
            } else {
                self.rifiuta(addr, "non registrato");
            }
            return;
        }
        if data.len() >= V2_HDR && &data[0..4] == V2_MAGIC {
            let ver = data[4];
            let flags = data[5];
            let seq = u32::from_be_bytes([data[6], data[7], data[8], data[9]]);
            let tms = u64::from_be_bytes(data[10..18].try_into().unwrap());
            let rate = u32::from_be_bytes([data[18], data[19], data[20], data[21]]);
            if ver != V2_VER {
                if flags == F_REGISTER {
                    self.rifiuta(addr, "versione del protocollo non piu' supportata: aggiorna Decolink");
                }
            } else if flags == F_PING {
                self.invia(&hdr(F_PONG, seq, tms, rate), addr);
            } else if flags == F_REGISTER {
                let testo: String = String::from_utf8_lossy(&data[V2_HDR..]).chars().take(600).collect();
                self.registra(addr, &testo, seq, now);
            } else if let Some(s) = self.sess.get_mut(&addr) {
                s.last_seen = now;
                self.inoltra(addr, flags, seq, data, now);
            } else if flags == F_AUDIO || flags == F_TX_AUDIO || flags == F_CAT_REQ {
                self.rifiuta(addr, "non registrato");
            }
        }
    }

    /// Attende un datagramma (fino al timeout del socket).
    pub fn ricevi(&mut self, buf: &mut [u8]) -> std::io::Result<(usize, SocketAddr)> {
        self.sock.recv_from(buf)
    }

    /// Stampa le statistiche, come ogni 30 secondi nel Python.
    pub fn statistiche(&self) {
        println!(
            "  [stat] stazioni attive: {}  collegati: {}  inoltrati: {}  respinti: {}",
            self.rooms.len(),
            self.sess.len(),
            self.fwd,
            self.rej
        );
    }
}

/// Percorso della chiave di firma: `DECOLINK_SECRET`, o `decolink.key` accanto all'eseguibile.
pub fn percorso_segreto(cartella: &std::path::Path) -> PathBuf {
    match std::env::var_os("DECOLINK_SECRET") {
        Some(p) => PathBuf::from(p),
        None => cartella.join("decolink.key"),
    }
}


#[cfg(test)]
mod test {
    use super::*;

    /// Gli stessi casi della tabella di `prova_multioperatore.py`.
    #[test]
    fn classificazione_cat_come_il_python() {
        let tabella = [
            ("f", "legge"), ("m\n", "legge"), ("t", "legge"), ("l STRENGTH", "legge"), ("s", "legge"),
            ("\\get_freq", "legge"), ("\\dump_state", "legge"),
            ("F 14074000", "scrive"), ("M PKTUSB 0", "scrive"), ("S 1 VFOB", "scrive"),
            ("I 14080000", "scrive"), ("L RFPOWER 0.5", "scrive"), ("w BY;", "scrive"),
            ("\\set_freq 7074000", "scrive"), ("\\send_cmd TX1;", "scrive"),
            ("T 1", "ptt_on"), ("T 3", "ptt_on"), ("T 0", "ptt_off"),
            ("\\set_ptt 1", "ptt_on"), ("\\set_ptt 0", "ptt_off"), ("+T 1", "ptt_on"),
            ("T", "scrive"), ("T x", "scrive"), ("", "legge"),
        ];
        for (riga, atteso) in tabella {
            assert_eq!(classifica_cat(riga), atteso, "{riga:?}");
        }
    }

    #[test]
    fn intestazione_v2_in_rete() {
        let h = hdr(F_REGISTER, 0x0102_0304, 0, 48_000);
        assert_eq!(&h[0..4], b"HFGW");
        assert_eq!(h[4], 2);
        assert_eq!(h[5], F_REGISTER);
        assert_eq!(&h[6..10], &[1, 2, 3, 4]);
        assert_eq!(&h[18..22], &48_000u32.to_be_bytes());
    }
}
