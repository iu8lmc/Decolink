//! Accesso al servizio della stazione (porting di `Client::login` in `gui/main.cpp`).
//!
//! POST JSON a `<host>/api/login` con email, password e, se serve, la stazione.
//! Senza schema nell'indirizzo si assume HTTPS: la password non deve viaggiare in
//! chiaro per distrazione. TLS con `rustls`, cioe' in Rust, senza OpenSSL.

use std::time::Duration;

/// Stazione elencata dal servizio quando l'utente ne ha piu' di una.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Stazione {
    pub slug: String,
    pub nome: String,
}

/// Accesso riuscito: il token per il relay e i dati della stazione.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Accesso {
    pub token: String,
    pub stazione: String,
    pub nominativo: String,
    pub ruolo: String,
    pub puo_trasmettere: bool,
    /// Secondi di validita' del token.
    pub scade_tra: u64,
}

/// Perche' l'accesso non e' riuscito.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Errore {
    /// Il servizio non risponde o la risposta non e' JSON.
    NonRaggiungibile(String),
    /// Credenziali o stazione sbagliate. `stazioni` elenca quelle disponibili.
    Rifiutato { motivo: String, stazioni: Vec<Stazione>, serve_stazione: bool },
}

impl std::fmt::Display for Errore {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Errore::NonRaggiungibile(e) => write!(f, "server di accesso non raggiungibile: {e}"),
            Errore::Rifiutato { motivo, .. } => write!(f, "{motivo}"),
        }
    }
}

/// Indirizzo completo dell'endpoint di login. Senza schema si mette https.
pub fn endpoint(host: &str) -> String {
    let base = if host.contains("://") { host.to_string() } else { format!("https://{host}") };
    format!("{}/api/login", base.trim_end_matches('/'))
}

/// Interpreta la risposta JSON del servizio. Separato dalla rete per poterlo provare.
pub fn interpreta(corpo: &str) -> Result<Accesso, Errore> {
    let v: serde_json::Value = serde_json::from_str(corpo)
        .map_err(|_| Errore::NonRaggiungibile("risposta incomprensibile".into()))?;
    let stazioni: Vec<Stazione> = v["stations"]
        .as_array()
        .map(|a| {
            a.iter()
                .map(|s| Stazione {
                    slug: s["slug"].as_str().unwrap_or("").to_string(),
                    nome: s["name"].as_str().unwrap_or("").to_string(),
                })
                .collect()
        })
        .unwrap_or_default();

    if v["ok"].as_bool() != Some(true) {
        return Err(Errore::Rifiutato {
            motivo: v["error"].as_str().unwrap_or("accesso rifiutato").to_string(),
            stazioni,
            serve_stazione: v["need_station"].as_bool().unwrap_or(false),
        });
    }
    Ok(Accesso {
        token: v["token"].as_str().unwrap_or("").to_string(),
        stazione: v["station"].as_str().unwrap_or("").to_string(),
        nominativo: v["callsign"].as_str().unwrap_or("").to_string(),
        ruolo: v["role"].as_str().unwrap_or("").to_string(),
        puo_trasmettere: v["can_transmit"].as_bool().unwrap_or(false),
        scade_tra: v["expires_in"].as_u64().unwrap_or(3600),
    })
}

/// Accede al servizio. `stazione` e' facoltativa: serve quando l'utente ne ha piu' di una.
pub fn accedi(
    host: &str,
    email: &str,
    password: &str,
    stazione: Option<&str>,
) -> Result<Accesso, Errore> {
    let mut corpo = serde_json::json!({ "email": email, "password": password });
    if let Some(s) = stazione.filter(|s| !s.is_empty()) {
        corpo["station"] = serde_json::Value::String(s.to_string());
    }
    let agente = ureq::AgentBuilder::new().timeout(Duration::from_secs(10)).build();
    let risposta = agente
        .post(&endpoint(host))
        .set("Content-Type", "application/json")
        .send_string(&corpo.to_string());
    // Il servizio risponde con JSON anche quando rifiuta (HTTP 4xx): si legge il corpo.
    let testo = match risposta {
        Ok(r) => r.into_string(),
        Err(ureq::Error::Status(_, r)) => r.into_string(),
        Err(e) => return Err(Errore::NonRaggiungibile(e.to_string())),
    }
    .map_err(|e| Errore::NonRaggiungibile(e.to_string()))?;
    interpreta(&testo)
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn senza_schema_si_usa_https() {
        assert_eq!(endpoint("decolink.ft2.it"), "https://decolink.ft2.it/api/login");
        assert_eq!(endpoint("http://127.0.0.1:8080/"), "http://127.0.0.1:8080/api/login");
    }

    #[test]
    fn risposta_positiva() {
        let a = interpreta(
            r#"{"ok":true,"token":"T1","station":"prova","callsign":"IK0AAA","role":"own","can_transmit":true,"expires_in":3600,"stations":[]}"#,
        )
        .unwrap();
        assert_eq!(a.token, "T1");
        assert_eq!(a.stazione, "prova");
        assert!(a.puo_trasmettere);
        assert_eq!(a.scade_tra, 3600);
    }

    #[test]
    fn rifiuto_con_stazioni_da_scegliere() {
        let e = interpreta(
            r#"{"ok":false,"error":"scegli una stazione","need_station":true,"stations":[{"slug":"a","name":"Alfa"},{"slug":"b","name":"Beta"}]}"#,
        )
        .unwrap_err();
        match e {
            Errore::Rifiutato { motivo, stazioni, serve_stazione } => {
                assert_eq!(motivo, "scegli una stazione");
                assert!(serve_stazione);
                assert_eq!(stazioni.len(), 2);
                assert_eq!(stazioni[1].nome, "Beta");
            }
            altro => panic!("{altro:?}"),
        }
    }

    #[test]
    fn corpo_che_non_e_json() {
        assert!(matches!(interpreta("<html>"), Err(Errore::NonRaggiungibile(_))));
    }

    /// Legge una richiesta HTTP intera, fino al corpo dichiarato da Content-Length.
    fn leggi_richiesta(s: &mut std::net::TcpStream) -> String {
        use std::io::Read;
        let mut dati: Vec<u8> = Vec::new();
        let mut buf = [0u8; 1024];
        loop {
            let n = s.read(&mut buf).unwrap();
            if n == 0 {
                break;
            }
            dati.extend_from_slice(&buf[..n]);
            if let Some(fine) = dati.windows(4).position(|w| w == b"\r\n\r\n") {
                let testa = String::from_utf8_lossy(&dati[..fine]).to_lowercase();
                let lungh: usize = testa
                    .lines()
                    .find_map(|l| l.strip_prefix("content-length:"))
                    .and_then(|v| v.trim().parse().ok())
                    .unwrap_or(0);
                if dati.len() >= fine + 4 + lungh {
                    break;
                }
            }
        }
        String::from_utf8_lossy(&dati).into_owned()
    }

    /// Un servizio finto su socket locale: verifica la richiesta e la risposta
    /// senza TLS (`http://`).
    #[test]
    fn accesso_contro_un_servizio_locale() {
        use std::io::Write;
        let l = std::net::TcpListener::bind("127.0.0.1:0").unwrap();
        let porta = l.local_addr().unwrap().port();
        let srv = std::thread::spawn(move || {
            let (mut s, _) = l.accept().unwrap();
            let richiesta = leggi_richiesta(&mut s);
            let corpo = r#"{"ok":true,"token":"XYZ","station":"prova","callsign":"IK0AAA","role":"opr","can_transmit":false,"expires_in":60}"#;
            let r = format!(
                "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
                corpo.len(),
                corpo
            );
            s.write_all(r.as_bytes()).unwrap();
            richiesta
        });
        let a = accedi(&format!("http://127.0.0.1:{porta}"), "ik0@x.it", "segreta", Some("prova")).unwrap();
        let richiesta = srv.join().unwrap();
        assert!(richiesta.starts_with("POST /api/login"));
        assert!(richiesta.contains(r#""station":"prova""#));
        assert_eq!(a.token, "XYZ");
        assert!(!a.puo_trasmettere);
    }
}
