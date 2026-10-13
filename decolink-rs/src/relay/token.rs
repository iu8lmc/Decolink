//! Token di accesso al relay (porting di `server/decolink_token.py`).
//!
//! Formato: `dl1.<payload>.<firma>`. Il payload e' JSON compatto (chiavi ordinate)
//! in base64url senza padding; la firma e' HMAC-SHA256 troncato a 16 byte. Token
//! emessi dal Python e verificati qui devono passare, e viceversa.

use base64::engine::general_purpose::URL_SAFE_NO_PAD;
use base64::Engine;
use hmac::{Hmac, Mac};
use sha2::Sha256;
use std::path::Path;

pub const PREFIX: &str = "dl1";
pub const RUOLO_PROPRIETARIO: &str = "own";
pub const RUOLO_OPERATORE: &str = "opr";
pub const RUOLO_ASCOLTATORE: &str = "lst";
pub const RUOLI: [&str; 3] = [RUOLO_PROPRIETARIO, RUOLO_OPERATORE, RUOLO_ASCOLTATORE];

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TokenError(pub String);

impl std::fmt::Display for TokenError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}

/// Dati di un token verificato.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Dati {
    pub user_id: i64,
    pub callsign: String,
    pub station_id: i64,
    pub role: String,
    pub expires: i64,
    pub jti: String,
}

/// Il ruolo puo' mandare la radio in aria.
pub fn puo_trasmettere(ruolo: &str) -> bool {
    ruolo == RUOLO_PROPRIETARIO || ruolo == RUOLO_OPERATORE
}

/// Legge la chiave di firma, creandola al primo avvio (48 byte casuali, senza
/// spazi ai bordi, come nel Python).
pub fn carica_segreto(percorso: &Path) -> Result<Vec<u8>, TokenError> {
    if percorso.exists() {
        let raw = std::fs::read(percorso).map_err(|e| TokenError(e.to_string()))?;
        let raw: Vec<u8> = trim_spazi(&raw).to_vec();
        if raw.len() >= 32 {
            return Ok(raw);
        }
        return Err(TokenError(format!("chiave di firma troppo corta in {}", percorso.display())));
    }
    let mut raw = casuali(48)?;
    while raw.first().map_or(false, |b| b.is_ascii_whitespace())
        || raw.last().map_or(false, |b| b.is_ascii_whitespace())
    {
        raw = casuali(48)?;
    }
    if let Some(dir) = percorso.parent() {
        std::fs::create_dir_all(dir).map_err(|e| TokenError(e.to_string()))?;
    }
    // create_new: non si sovrascrive mai una chiave esistente
    use std::io::Write;
    let mut f = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(percorso)
        .map_err(|e| TokenError(e.to_string()))?;
    f.write_all(&raw).map_err(|e| TokenError(e.to_string()))?;
    Ok(raw)
}

fn trim_spazi(b: &[u8]) -> &[u8] {
    let inizio = b.iter().position(|c| !c.is_ascii_whitespace()).unwrap_or(b.len());
    let fine = b.iter().rposition(|c| !c.is_ascii_whitespace()).map_or(inizio, |p| p + 1);
    &b[inizio..fine.max(inizio)]
}

fn casuali(n: usize) -> Result<Vec<u8>, TokenError> {
    let mut v = vec![0u8; n];
    getrandom::getrandom(&mut v).map_err(|e| TokenError(e.to_string()))?;
    Ok(v)
}

fn firma(segreto: &[u8], corpo: &str) -> Vec<u8> {
    let mut m = Hmac::<Sha256>::new_from_slice(segreto).expect("HMAC accetta chiavi di ogni lunghezza");
    m.update(corpo.as_bytes());
    m.finalize().into_bytes()[..16].to_vec()
}

/// Confronto a tempo costante, come `hmac.compare_digest`.
fn uguali(a: &[u8], b: &[u8]) -> bool {
    a.len() == b.len() && a.iter().zip(b).fold(0u8, |acc, (x, y)| acc | (x ^ y)) == 0
}

/// Controlla firma e scadenza. Non tocca il database: revoca e permessi li
/// controlla chi chiama.
pub fn verifica(segreto: &[u8], token: &str, ora: f64) -> Result<Dati, TokenError> {
    if token.is_empty() {
        return Err(TokenError("token assente".into()));
    }
    let parti: Vec<&str> = token.split('.').collect();
    if parti.len() != 3 || parti[0] != PREFIX {
        return Err(TokenError("formato del token non riconosciuto".into()));
    }
    let (payload, sig) = (parti[1], parti[2]);
    let atteso = firma(segreto, &format!("{PREFIX}.{payload}"));
    let dato = URL_SAFE_NO_PAD
        .decode(sig.trim_end_matches('='))
        .map_err(|_| TokenError("firma illeggibile".into()))?;
    if !uguali(&atteso, &dato) {
        return Err(TokenError("firma non valida".into()));
    }
    let raw = URL_SAFE_NO_PAD
        .decode(payload.trim_end_matches('='))
        .map_err(|_| TokenError("contenuto del token illeggibile".into()))?;
    let v: serde_json::Value =
        serde_json::from_slice(&raw).map_err(|_| TokenError("contenuto del token illeggibile".into()))?;

    let x = v["x"].as_f64().unwrap_or(0.0);
    if x < ora {
        return Err(TokenError("token scaduto".into()));
    }
    let r = v["r"].as_str().unwrap_or("");
    if !RUOLI.contains(&r) {
        return Err(TokenError("ruolo sconosciuto nel token".into()));
    }
    Ok(Dati {
        user_id: v["u"].as_i64().ok_or_else(|| TokenError("contenuto del token illeggibile".into()))?,
        callsign: v["c"].as_str().unwrap_or("").to_string(),
        station_id: v["s"].as_i64().ok_or_else(|| TokenError("contenuto del token illeggibile".into()))?,
        role: r.to_string(),
        expires: x as i64,
        jti: v["i"].as_str().unwrap_or("").to_string(),
    })
}

/// Firma un token, come `issue` nel Python. Serve al web e ai test.
pub fn emetti(
    segreto: &[u8],
    user_id: i64,
    nominativo: &str,
    station_id: i64,
    ruolo: &str,
    ttl: i64,
    ora: f64,
) -> Result<String, TokenError> {
    if !RUOLI.contains(&ruolo) {
        return Err(TokenError(format!("ruolo sconosciuto: {ruolo}")));
    }
    let id = URL_SAFE_NO_PAD.encode(casuali(9)?);
    // Chiavi in ordine alfabetico, senza spazi: come json.dumps(sort_keys=True, separators)
    let c: String = nominativo.to_uppercase().chars().take(16).collect();
    let corpo = format!(
        "{{\"c\":{},\"i\":\"{}\",\"r\":\"{}\",\"s\":{},\"u\":{},\"x\":{}}}",
        serde_json::Value::String(c),
        id,
        ruolo,
        station_id,
        user_id,
        (ora + ttl as f64) as i64
    );
    let payload = URL_SAFE_NO_PAD.encode(corpo.as_bytes());
    let sig = URL_SAFE_NO_PAD.encode(firma(segreto, &format!("{PREFIX}.{payload}")));
    Ok(format!("{PREFIX}.{payload}.{sig}"))
}

#[cfg(test)]
mod test {
    use super::*;

    const SEGRETO: &[u8] = b"segreto-di-prova-lungo-abbastanza-per-il-test-0123456789";

    #[test]
    fn andata_e_ritorno() {
        let t = emetti(SEGRETO, 7, "ik0aaa", 3, RUOLO_OPERATORE, 3600, 1000.0).unwrap();
        let d = verifica(SEGRETO, &t, 1500.0).unwrap();
        assert_eq!((d.user_id, d.station_id, d.role.as_str()), (7, 3, "opr"));
        assert_eq!(d.callsign, "IK0AAA");
        assert_eq!(d.expires, 4600);
        assert!(!d.jti.is_empty());
    }

    #[test]
    fn firma_manomessa_e_scaduta() {
        let t = emetti(SEGRETO, 7, "IK0AAA", 3, RUOLO_OPERATORE, 60, 1000.0).unwrap();
        assert_eq!(verifica(SEGRETO, &t, 2000.0).unwrap_err().0, "token scaduto");
        let mut m = t.clone();
        m.push('A');
        assert!(verifica(SEGRETO, &m, 1000.0).is_err());
        assert_eq!(verifica(b"altra-chiave-sbagliata-di-almeno-32-byte!", &t, 1000.0).unwrap_err().0,
                   "firma non valida");
        assert_eq!(verifica(SEGRETO, "", 0.0).unwrap_err().0, "token assente");
        assert!(verifica(SEGRETO, "dl1.x", 0.0).is_err());
    }

    #[test]
    fn ruoli_che_trasmettono() {
        assert!(puo_trasmettere(RUOLO_PROPRIETARIO));
        assert!(puo_trasmettere(RUOLO_OPERATORE));
        assert!(!puo_trasmettere(RUOLO_ASCOLTATORE));
    }
}
