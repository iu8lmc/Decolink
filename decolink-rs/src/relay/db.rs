//! Database condiviso con il servizio web (porting delle funzioni di
//! `server/decolink_db.py` che usa il relay). Stesso file SQLite, stesso schema.

use std::collections::{HashMap, HashSet};
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};

use rusqlite::{params, Connection, OptionalExtension};

/// Lo schema e' quello del Python, estratto tale e quale.
const SCHEMA: &str = include_str!("schema.sql");

/// Dove sta il database se nessuno dice altrimenti: accanto all'eseguibile,
/// come `default_path` nel Python accanto allo script. `DECOLINK_DB` ha la precedenza.
pub fn percorso_predefinito(cartella: &Path) -> PathBuf {
    match std::env::var_os("DECOLINK_DB") {
        Some(p) => PathBuf::from(p),
        None => cartella.join("decolink.db"),
    }
}

pub fn apri(percorso: &Path) -> rusqlite::Result<Connection> {
    let c = Connection::open(percorso)?;
    c.busy_timeout(std::time::Duration::from_secs(10))?;
    c.pragma_update(None, "journal_mode", "WAL")?;
    c.pragma_update(None, "foreign_keys", "ON")?;
    c.execute_batch(SCHEMA)?;
    Ok(c)
}

pub fn adesso() -> i64 {
    SystemTime::now().duration_since(UNIX_EPOCH).map(|d| d.as_secs() as i64).unwrap_or(0)
}

/// Fotografia dei permessi validi: (utente, stazione) -> ruolo.
pub fn permessi_attivi(c: &Connection) -> rusqlite::Result<HashMap<(i64, i64), String>> {
    let mut st = c.prepare(
        "SELECT m.user_id, m.station_id, m.role FROM memberships m \
         JOIN users u ON u.id = m.user_id \
         JOIN stations s ON s.id = m.station_id \
         WHERE u.status = 'active' AND s.enabled = 1",
    )?;
    let righe = st.query_map([], |r| {
        Ok(((r.get::<_, i64>(0)?, r.get::<_, i64>(1)?), r.get::<_, String>(2)?))
    })?;
    righe.collect()
}

/// I token buttati via che non sono ancora scaduti da soli.
pub fn revocati(c: &Connection) -> rusqlite::Result<HashSet<String>> {
    c.execute("DELETE FROM revoked_tokens WHERE expires_at < ?1", params![adesso()])?;
    let mut st = c.prepare("SELECT jti FROM revoked_tokens")?;
    let righe = st.query_map([], |r| r.get::<_, String>(0))?;
    righe.collect()
}

pub fn registra_ingresso(
    c: &Connection,
    utente: i64,
    nominativo: &str,
    stazione: i64,
    ruolo: &str,
    indirizzo: &str,
) -> rusqlite::Result<i64> {
    c.execute(
        "INSERT INTO connections (user_id, callsign, station_id, role, addr, joined_at) \
         VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
        params![utente, nominativo, stazione, ruolo, indirizzo, adesso()],
    )?;
    Ok(c.last_insert_rowid())
}

pub fn registra_uscita(c: &Connection, id: i64) -> rusqlite::Result<()> {
    c.execute(
        "UPDATE connections SET left_at = ?1 WHERE id = ?2 AND left_at IS NULL",
        params![adesso(), id],
    )?;
    Ok(())
}

pub fn inizia_trasmissione(
    c: &Connection,
    utente: i64,
    nominativo: &str,
    stazione: i64,
    indirizzo: &str,
) -> rusqlite::Result<i64> {
    c.execute(
        "INSERT INTO tx_log (user_id, callsign, station_id, started_at, addr) VALUES (?1, ?2, ?3, ?4, ?5)",
        params![utente, nominativo, stazione, adesso(), indirizzo],
    )?;
    Ok(c.last_insert_rowid())
}

pub fn finisci_trasmissione(c: &Connection, id: i64) -> rusqlite::Result<()> {
    c.execute(
        "UPDATE tx_log SET ended_at = ?1 WHERE id = ?2 AND ended_at IS NULL",
        params![adesso(), id],
    )?;
    Ok(())
}

/// Solo per i test: legge un valore singolo.
pub fn scalare_i64(c: &Connection, sql: &str) -> rusqlite::Result<Option<i64>> {
    c.query_row(sql, [], |r| r.get(0)).optional()
}
