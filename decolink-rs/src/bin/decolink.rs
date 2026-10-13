//! Decolink da riga di comando: il motore senza la GUI.
//!
//! ```text
//! decolink dispositivi
//! decolink avvia --email UTENTE --stazione SLUG --relay HOST:PORTA
//!                [--ingresso NOME] [--uscita NOME]
//!                [--rig-modello N --rig-porta COM3 --rig-baud 19200] [--ascolto]
//! ```
//! La password si legge dalla variabile d'ambiente `DECOLINK_PASSWORD`, non dalla
//! riga di comando, cosi' non finisce nella cronologia.

use std::collections::HashMap;
use std::process::ExitCode;
use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};

use decolink_rs::accesso::{self, Errore};
use decolink_rs::audio::{self, Ingresso, Ricampiona, Uscita};
use decolink_rs::collegamento::Collegamento;
use decolink_rs::cwkey::Sintetizzatore;
use decolink_rs::hamlib::Radio;
use decolink_rs::rete::Evento;

fn opzioni(args: &[String]) -> HashMap<String, String> {
    let mut m = HashMap::new();
    let mut i = 0;
    while i < args.len() {
        if let Some(k) = args[i].strip_prefix("--") {
            let v = if i + 1 < args.len() && !args[i + 1].starts_with("--") {
                i += 1;
                args[i].clone()
            } else {
                "1".to_string()
            };
            m.insert(k.to_string(), v);
        }
        i += 1;
    }
    m
}

fn ora_ms() -> u64 {
    SystemTime::now().duration_since(UNIX_EPOCH).map(|d| d.as_millis() as u64).unwrap_or(0)
}

/// Risponde ai comandi rigctl che il telefono usa, sulla radio aperta.
fn comando_cat(radio: &mut Option<Radio>, riga: &str) -> String {
    let Some(r) = radio.as_mut() else {
        return "RPRT -1\n".to_string();
    };
    let mut parti = riga.trim().trim_start_matches(['\\', '+']).split_whitespace();
    let cmd = parti.next().unwrap_or("");
    let arg = parti.next();
    let esito = |e: Result<(), String>| if e.is_ok() { "RPRT 0\n".to_string() } else { "RPRT -1\n".to_string() };
    match cmd {
        "f" | "get_freq" => r.frequenza().map(|hz| format!("{hz:.0}\n")).unwrap_or("RPRT -1\n".into()),
        "F" | "set_freq" => match arg.and_then(|a| a.parse::<f64>().ok()) {
            Some(hz) => esito(r.imposta_frequenza(hz)),
            None => "RPRT -1\n".into(),
        },
        "m" | "get_mode" => match r.modo() {
            Ok(m) => format!("{m}\n3000\n"),
            Err(_) => "RPRT -1\n".into(),
        },
        "M" | "set_mode" => match arg {
            Some(m) => esito(r.imposta_modo(m)),
            None => "RPRT -1\n".into(),
        },
        "t" | "get_ptt" => r.ptt().map(|p| format!("{}\n", u8::from(p))).unwrap_or("RPRT -1\n".into()),
        "T" | "set_ptt" => match arg {
            Some("1") => esito(r.imposta_ptt(true)),
            Some("0") => esito(r.imposta_ptt(false)),
            _ => "RPRT -1\n".into(),
        },
        _ => "RPRT -1\n".into(),
    }
}

fn avvia(o: &HashMap<String, String>) -> Result<(), String> {
    let email = o.get("email").ok_or("manca --email")?;
    let password = std::env::var("DECOLINK_PASSWORD").map_err(|_| "manca la variabile DECOLINK_PASSWORD")?;
    let relay_str = o.get("relay").ok_or("manca --relay HOST:PORTA")?;
    let host_accesso = o.get("accesso").map(String::as_str).unwrap_or("decolink.ft2.it");
    let stazione = o.get("stazione").map(String::as_str);

    let mut accesso = accesso::accedi(host_accesso, email, &password, stazione).map_err(|e| match e {
        Errore::Rifiutato { motivo, stazioni, serve_stazione } if serve_stazione => {
            let elenco: Vec<String> = stazioni.iter().map(|s| format!("  {} — {}", s.slug, s.nome)).collect();
            format!("{motivo}\nstazioni disponibili:\n{}", elenco.join("\n"))
        }
        altro => altro.to_string(),
    })?;
    eprintln!("accesso: {} — stazione {}, {}", accesso.nominativo, accesso.stazione,
              if accesso.puo_trasmettere { "puo' trasmettere" } else { "solo ascolto" });

    let relay = relay_str
        .parse::<std::net::SocketAddr>()
        .or_else(|_| {
            use std::net::ToSocketAddrs;
            relay_str.to_socket_addrs().ok().and_then(|mut i| i.next()).ok_or(())
        })
        .map_err(|_| format!("relay non valido: {relay_str}"))?;

    let mut col = Collegamento::apri("0.0.0.0:0", &accesso.token).map_err(|e| e.to_string())?;
    col.gw.imposta_destinazione(Some(relay));
    col.gw.modalita_ascolto(o.contains_key("ascolto"));

    let ingresso = Ingresso::apri(o.get("ingresso").map(String::as_str)).map_err(|e| format!("ingresso: {e}"))?;
    let mut uscita = Uscita::apri(o.get("uscita").map(String::as_str)).map_err(|e| format!("uscita: {e}"))?;

    let mut radio: Option<Radio> = match o.get("rig-modello") {
        Some(m) => {
            let modello: i32 = m.parse().map_err(|_| "rig-modello non numerico")?;
            let porta = o.get("rig-porta").map(String::as_str).unwrap_or("");
            let baud = o.get("rig-baud").and_then(|b| b.parse().ok()).unwrap_or(19200);
            let r = Radio::apri(modello, porta, baud, 8, 1, "n").map_err(|e| format!("radio: {e}"))?;
            eprintln!("radio aperta (modello {modello})");
            Some(r)
        }
        None => None,
    };

    let mut sint = Sintetizzatore::new();
    let mut ric_tx: HashMap<u32, Ricampiona> = HashMap::new();
    eprintln!("in ascolto: relay {relay}, Ctrl-C per fermare");

    let mut ultimo_rinnovo = Instant::now();
    let mut ultimo_profilo = col.gw.profilo();
    loop {
        // Audio della radio verso il telefono
        let pcm = ingresso.ricevi();
        if !pcm.is_empty() {
            col.invia_audio(&pcm, ora_ms()).map_err(|e| e.to_string())?;
        }

        // Eventi dal telefono o dal relay
        let ora = Instant::now();
        let eventi = col
            .passo(ora, ora_ms(), &mut |riga| comando_cat(&mut radio, riga))
            .map_err(|e| e.to_string())?;
        for e in eventi {
            match e {
                Evento::Registrato => eprintln!("relay: registrato"),
                Evento::Rifiutato(m) => eprintln!("relay: rifiutato: {m}"),
                Evento::TelefonoConnesso(a) => eprintln!("telefono connesso da {a}"),
                Evento::Profilo(p) => eprintln!("profilo: {}", p.nome()),
                Evento::StatoTx(s) => eprintln!("PTT: {s}"),
                Evento::Audio { pcm, rate } => {
                    let v = if rate == audio::RATE {
                        pcm
                    } else {
                        let r = ric_tx.entry(rate).or_insert_with(|| Ricampiona::new(rate, audio::RATE));
                        let f: Vec<f32> = pcm.iter().map(|s| f32::from(*s) / 32768.0).collect();
                        r.processa(&f).into_iter().map(|v| (v.clamp(-1.0, 1.0) * 32767.0) as i16).collect()
                    };
                    uscita.scrivi(&v);
                }
                Evento::CwKey { nota_hz, eventi } => {
                    sint.nota(nota_hz);
                    sint.aggiungi(&eventi);
                }
            }
        }
        // Il tasto CW rigenerato va alla scheda, un blocco alla volta
        if sint.in_attesa() {
            uscita.scrivi(&sint.genera(480));
        }

        // Cambio di profilo: si dice in chiaro, utile quando si guarda il log
        if col.gw.profilo() != ultimo_profilo {
            ultimo_profilo = col.gw.profilo();
        }

        // Il token dura un'ora: si rinnova qualche minuto prima
        if ultimo_rinnovo.elapsed() > Duration::from_secs(accesso.scade_tra.saturating_sub(300).max(60)) {
            match accesso::accedi(host_accesso, email, &password, Some(&accesso.stazione)) {
                Ok(nuovo) => {
                    col.imposta_token(&nuovo.token);
                    accesso = nuovo;
                    eprintln!("token rinnovato");
                }
                Err(e) => eprintln!("rinnovo del token fallito: {e}"),
            }
            ultimo_rinnovo = Instant::now();
        }

        std::thread::sleep(Duration::from_millis(10));
    }
}

fn principale() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let Some(comando) = args.first() else {
        eprintln!("uso: decolink dispositivi | decolink avvia --email U --relay H:P [...]");
        return ExitCode::from(2);
    };
    let o = opzioni(&args[1..]);
    let esito = match comando.as_str() {
        "dispositivi" => {
            let (ing, usc) = audio::dispositivi();
            println!("ingressi:");
            for n in ing { println!("  {n}"); }
            println!("uscite:");
            for n in usc { println!("  {n}"); }
            Ok(())
        }
        "avvia" => avvia(&o),
        altro => Err(format!("comando sconosciuto: {altro}")),
    };
    match esito {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("decolink: {e}");
            ExitCode::from(1)
        }
    }
}

fn main() -> ExitCode {
    principale()
}
