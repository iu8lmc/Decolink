//! Relay UDP di Decolink (porting di `server/decolink_relay.py`).
//!
//! ```text
//! decolink-relay [PORTA]          (predefinita 5555)
//! ```
//! Chiave di firma e database stanno accanto all'eseguibile, come nel Python
//! accanto allo script; `DECOLINK_SECRET` e `DECOLINK_DB` li spostano.

use std::process::ExitCode;
use std::time::Instant;

use decolink_rs::relay::{db, ora, percorso_segreto, token, Relay};

fn cartella_eseguibile() -> std::path::PathBuf {
    std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|d| d.to_path_buf()))
        .unwrap_or_else(|| std::path::PathBuf::from("."))
}

fn main() -> ExitCode {
    let porta: u16 = match std::env::args().nth(1) {
        Some(p) => match p.parse() {
            Ok(v) => v,
            Err(_) => {
                eprintln!("porta non valida: {p}");
                return ExitCode::from(2);
            }
        },
        None => 5555,
    };
    let cartella = cartella_eseguibile();
    let segreto = match token::carica_segreto(&percorso_segreto(&cartella)) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("chiave di firma: {e}");
            return ExitCode::from(1);
        }
    };
    let percorso_db = db::percorso_predefinito(&cartella);
    let conn = match db::apri(&percorso_db) {
        Ok(c) => c,
        Err(e) => {
            eprintln!("database {}: {e}", percorso_db.display());
            return ExitCode::from(1);
        }
    };
    let sock = match Relay::apri_socket(porta) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("porta UDP {porta}: {e}");
            return ExitCode::from(1);
        }
    };

    let mut relay = Relay::nuovo(sock, segreto, conn);
    relay.aggiorna_permessi(ora(), true);
    println!("Decolink relay in ascolto su UDP {porta} — protocollo HFGW v2");
    println!("  chiave di firma: {}", percorso_segreto(&cartella).display());
    println!("  permessi caricati: {} (rilettura ogni 5 s)", relay.permessi());

    let mut buf = [0u8; 8192];
    let mut ultima_pulizia = ora();
    let mut ultima_stat = ora();
    let _ = Instant::now();
    loop {
        let now = ora();
        match relay.ricevi(&mut buf) {
            Ok((n, addr)) => relay.gestisci(&buf[..n], addr, now),
            Err(e) if matches!(e.kind(), std::io::ErrorKind::WouldBlock | std::io::ErrorKind::TimedOut) => {}
            // come nel Python: un errore del socket salta la manutenzione di questo giro
            Err(_) => continue,
        }
        relay.aggiorna_permessi(now, false);
        if now - ultima_pulizia > 2.0 {
            relay.pulisci(now);
            ultima_pulizia = now;
        }
        if now - ultima_stat > 30.0 {
            relay.statistiche();
            ultima_stat = now;
        }
    }
}
