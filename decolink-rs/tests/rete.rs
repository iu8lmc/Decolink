//! Macchina a stati del lato radio: si prova senza rete, passando datagrammi
//! direttamente da una funzione all'altra.

use std::net::SocketAddr;
use std::time::{Duration, Instant};

use decolink_rs::cwkey;
use decolink_rs::lossless;
use decolink_rs::proto::{self as dl, Ctrl, Profilo, Tipo};
use decolink_rs::rete::{v2, v2_leggi, v2_pacchetto, Evento, Gateway, Invio, KEEPALIVE};

fn addr(s: &str) -> SocketAddr {
    s.parse().unwrap()
}

fn nessun_cat(_: &str) -> String {
    panic!("il CAT non doveva essere chiamato")
}

fn cat_fisso(risposta: &'static str) -> impl FnMut(&str) -> String {
    move |_| risposta.to_string()
}

#[test]
fn intestazione_v2_andata_e_ritorno() {
    let p = v2_pacchetto(v2::AUDIO, 0x01020304, 0x1122334455, 48_000, b"ab");
    assert_eq!(p.len(), 24);
    assert_eq!(&p[0..4], b"HFGW");
    let (h, corpo) = v2_leggi(&p).expect("v2");
    assert_eq!(h.flags, v2::AUDIO);
    assert_eq!(h.seq, 0x01020304);
    assert_eq!(h.tempo_ms, 0x1122334455);
    assert_eq!(h.rate, 48_000);
    assert_eq!(corpo, b"ab");
    assert!(v2_leggi(b"HFGW\x03").is_none());
}

#[test]
fn registrazione_e_keepalive_verso_il_relay() {
    let mut gw = Gateway::new();
    let relay = addr("198.51.100.7:5555");
    gw.imposta_destinazione(Some(relay));
    let t0 = Instant::now();

    let r = gw.registrazione("TOKEN", t0).expect("registrazione");
    assert_eq!(r.verso, relay);
    let (h, corpo) = v2_leggi(&r.dati).unwrap();
    assert_eq!(h.flags, v2::REGISTER);
    assert_eq!(corpo, b"gw TOKEN");

    // prima del periodo non si rinnova; dopo, si'
    assert!(gw.tick("TOKEN", t0 + Duration::from_secs(1)).is_empty());
    let dopo = gw.tick("TOKEN", t0 + KEEPALIVE + Duration::from_millis(10));
    assert_eq!(dopo.len(), 1);
}

#[test]
fn risposte_del_relay_registrato_e_rifiutato() {
    let mut gw = Gateway::new();
    let relay = addr("198.51.100.7:5555");
    let (_, ev) = gw.ricevi(&v2_pacchetto(v2::REGISTER, 1, 0, 48_000, &[]), relay, 0, &mut nessun_cat);
    assert_eq!(ev, vec![Evento::Registrato]);

    let (_, ev) = gw.ricevi(&v2_pacchetto(v2::DENIED, 2, 0, 48_000, b"token scaduto"), relay, 0, &mut nessun_cat);
    assert_eq!(ev, vec![Evento::Rifiutato("token scaduto".into())]);
}

#[test]
fn ping_v2_e_v3_hanno_il_pong_con_lo_stesso_seq() {
    let mut gw = Gateway::new();
    let da = addr("203.0.113.9:4000");
    let (inv, _) = gw.ricevi(&v2_pacchetto(v2::PING, 77, 0, 48_000, &[]), da, 0, &mut nessun_cat);
    let (h, _) = v2_leggi(&inv[0].dati).unwrap();
    assert_eq!((h.flags, h.seq), (v2::PONG, 77));

    let ping = dl::pacchetto(Tipo::Ping, 0, 0, 0, 1234, 99, &[]);
    let (inv, _) = gw.ricevi(&ping, da, 0, &mut nessun_cat);
    let p = dl::leggi(&inv[0].dati).unwrap();
    assert_eq!((p.tipo, p.seq, p.tempo), (Tipo::Ping, 1234, 99));
}

#[test]
fn negoziazione_offre_e_conferma_il_profilo() {
    let mut gw = Gateway::new();
    let tel = addr("203.0.113.9:4000");

    // HELLO con la capacita' di raggruppare
    let hello = dl::pacchetto(Tipo::Ctrl, 0, 0, 0, 0, 0, &[Ctrl::Hello as u8, dl::capacita::AGGR]);
    let (inv, _) = gw.ricevi(&hello, tel, 0, &mut nessun_cat);
    let offerta = dl::leggi(&inv[0].dati).unwrap();
    assert_eq!(offerta.corpo[0], Ctrl::Offerta as u8);
    assert_eq!(offerta.corpo[4], Profilo::Pcm48 as u8, "profilo attivo");
    assert_eq!(offerta.corpo[5], dl::capacita::AGGR);

    // SCEGLI: il telefono chiede la voce compressa, offerta da entrambi i lati solo con Opus
    let scegli = dl::pacchetto(Tipo::Ctrl, 0, 0, 0, 0, 0, &[Ctrl::Scegli as u8, Profilo::Voce as u8]);
    let (inv, ev) = gw.ricevi(&scegli, tel, 0, &mut nessun_cat);
    let attivo = dl::leggi(&inv[0].dati).unwrap();
    assert_eq!(attivo.corpo[0], Ctrl::Attivo as u8);
    if cfg!(feature = "opus") {
        assert_eq!(gw.profilo(), Profilo::Voce);
        assert_eq!(ev, vec![Evento::Profilo(Profilo::Voce)]);
        assert_eq!(attivo.corpo[1], Profilo::Voce as u8);
    } else {
        assert_eq!(gw.profilo(), Profilo::Pcm48, "senza Opus la voce non e' in offerta");
        assert!(ev.is_empty());
    }
}

#[test]
fn un_profilo_non_offerto_non_cambia_nulla() {
    let mut gw = Gateway::new();
    let tel = addr("203.0.113.9:4000");
    let scegli = dl::pacchetto(Tipo::Ctrl, 0, 0, 0, 0, 0, &[Ctrl::Scegli as u8, Profilo::Emrg as u8]);
    let (inv, ev) = gw.ricevi(&scegli, tel, 0, &mut nessun_cat);
    assert!(ev.is_empty());
    assert_eq!(gw.profilo(), Profilo::Pcm48);
    assert_eq!(dl::leggi(&inv[0].dati).unwrap().corpo[1], Profilo::Pcm48 as u8);
}

#[test]
fn cat_v3_passa_al_rig_e_la_risposta_torna_con_lo_stesso_seq() {
    let mut gw = Gateway::new();
    let tel = addr("203.0.113.9:4000");
    let req = dl::pacchetto(Tipo::Cat, 0, 0, 0, 555, 42, b"f");
    let (inv, ev) = gw.ricevi(&req, tel, 0, &mut cat_fisso("14074000\n"));
    assert!(ev.is_empty());
    let r = dl::leggi(&inv[0].dati).unwrap();
    assert_eq!((r.tipo, r.seq, r.tempo), (Tipo::Cat, 555, 42));
    assert_eq!(r.corpo, b"14074000\n");
}

#[test]
fn cat_v2_passa_al_rig() {
    let mut gw = Gateway::new();
    let tel = addr("203.0.113.9:4000");
    let (inv, _) = gw.ricevi(&v2_pacchetto(v2::CATREQ, 9, 0, 48_000, b"m"), tel, 0, &mut cat_fisso("USB\n3000\n"));
    let (h, corpo) = v2_leggi(&inv[0].dati).unwrap();
    assert_eq!((h.flags, h.seq), (v2::CATRSP, 9));
    assert_eq!(corpo, b"USB\n3000\n");
}

#[test]
fn audio_pcm_dal_telefono_arriva_come_campioni() {
    let mut gw = Gateway::new();
    let tel = addr("203.0.113.9:4000");
    let campioni: Vec<i16> = vec![1, -2, 300, -32768, 32767];
    let mut corpo = Vec::new();
    for s in &campioni {
        corpo.extend_from_slice(&s.to_le_bytes());
    }
    let p = dl::pacchetto(Tipo::AudioTx, Profilo::Pcm48 as u8, 0, 0, 1, 0, &corpo);
    let (_, ev) = gw.ricevi(&p, tel, 0, &mut nessun_cat);
    assert_eq!(ev, vec![Evento::Audio { pcm: campioni, rate: 48_000 }]);
}

#[test]
fn digi_si_decodifica_senza_perdite() {
    let mut gw = Gateway::new();
    let tel = addr("203.0.113.9:4000");
    let campioni: Vec<i16> = (0..480).map(|i| ((i * 73) % 4000 - 2000) as i16).collect();
    let blocco = lossless::comprimi(&campioni);
    let p = dl::pacchetto(Tipo::AudioTx, Profilo::Digi as u8, 0, 0, 1, 0, &blocco);
    let (_, ev) = gw.ricevi(&p, tel, 0, &mut nessun_cat);
    assert_eq!(ev, vec![Evento::Audio { pcm: campioni, rate: 12_000 }]);
}

#[test]
fn cw_a_tasto_arriva_come_eventi() {
    let mut gw = Gateway::new();
    let tel = addr("203.0.113.9:4000");
    let eventi = vec![
        cwkey::Evento { delta_ms: 100, giu: true },
        cwkey::Evento { delta_ms: 60, giu: false },
    ];
    let corpo = cwkey::corpo_cw(700, &eventi);
    let p = dl::pacchetto(Tipo::AudioTx, Profilo::CwKey as u8, 0, 0, 1, 0, &corpo);
    let (_, ev) = gw.ricevi(&p, tel, 0, &mut nessun_cat);
    assert_eq!(ev, vec![Evento::CwKey { nota_hz: 700, eventi }]);
}

#[test]
fn pacchetti_rotti_o_sconosciuti_non_producono_nulla() {
    let mut gw = Gateway::new();
    let tel = addr("203.0.113.9:4000");
    for dg in [&b""[..], b"D", b"HFGW\x02", b"qualcosa di altro che non e' niente"] {
        let (inv, ev) = gw.ricevi(dg, tel, 0, &mut nessun_cat);
        assert!(inv.is_empty() && ev.is_empty());
    }
}

#[test]
fn modalita_ascolto_si_aggancia_al_telefono_che_chiama() {
    let mut gw = Gateway::new();
    gw.modalita_ascolto(true);
    let tel = addr("203.0.113.9:4000");
    let (inv, ev) = gw.ricevi(&v2_pacchetto(v2::REGISTER, 3, 0, 48_000, &[]), tel, 0, &mut nessun_cat);
    assert_eq!(ev, vec![Evento::TelefonoConnesso(tel)]);
    assert_eq!(inv[0].verso, tel);
    // senza un telefono che chiama, l'audio non va da nessuna parte
    assert_eq!(gw.invia_audio(&[0i16; 480], 0).len(), 1, "un blocco PCM da 10 ms");
}

#[test]
fn senza_destinazione_l_audio_si_butta() {
    let mut gw = Gateway::new();
    assert!(gw.invia_audio(&[0i16; 4800], 0).is_empty());
}

#[test]
fn pcm_in_uscita_e_un_pacchetto_v2_per_blocco() {
    let mut gw = Gateway::new();
    let relay = addr("198.51.100.7:5555");
    gw.imposta_destinazione(Some(relay));
    let pcm: Vec<i16> = (0..480 * 3).map(|i| i as i16).collect();
    let inv: Vec<Invio> = gw.invia_audio(&pcm, 1000);
    assert_eq!(inv.len(), 3);
    let (h, corpo) = v2_leggi(&inv[1].dati).unwrap();
    assert_eq!((h.flags, h.rate), (v2::AUDIO, 48_000));
    assert_eq!(corpo.len(), 480 * 2);
    assert_eq!(i16::from_le_bytes([corpo[0], corpo[1]]), 480);
}

#[cfg(feature = "opus")]
#[test]
fn opus_in_uscita_torna_leggibile_dall_altro_lato() {
    // Il lato radio codifica con Opus; il ricevitore (qui un secondo Gateway che fa
    // la parte del telefono) decodifica. Il pacchetto di uscita diventa un pacchetto
    // di trasmissione cambiando solo il tipo.
    let relay = addr("198.51.100.7:5555");
    let mut tx = Gateway::new();
    tx.imposta_destinazione(Some(relay));
    let hello = dl::pacchetto(Tipo::Ctrl, 0, 0, 0, 0, 0, &[Ctrl::Hello as u8, dl::capacita::AGGR]);
    let tel = addr("203.0.113.9:4000");
    tx.ricevi(&hello, tel, 0, &mut nessun_cat);
    let scegli = dl::pacchetto(Tipo::Ctrl, 0, 0, 0, 0, 0, &[Ctrl::Scegli as u8, Profilo::Voce as u8]);
    tx.ricevi(&scegli, tel, 0, &mut nessun_cat);

    let mut rx = Gateway::new();
    let frame = 960 * 4;
    let mut fase = 0.0f64;
    let tono: Vec<i16> = (0..frame)
        .map(|_| {
            fase += 2.0 * std::f64::consts::PI * 1000.0 / 48_000.0;
            (8000.0 * fase.sin()) as i16
        })
        .collect();
    let inv = tx.invia_audio(&tono, 0);
    assert!(!inv.is_empty(), "devono uscire pacchetti Opus");

    let mut uscito: Vec<i16> = Vec::new();
    for i in inv {
        let p = dl::leggi(&i.dati).expect("v3");
        assert_eq!(p.profilo, Profilo::Voce);
        // stesso pacchetto, ma di trasmissione
        let dg = dl::pacchetto(Tipo::AudioTx, p.profilo as u8, p.flag, 0, p.seq, p.tempo, &p.corpo);
        let (_, ev) = rx.ricevi(&dg, tel, 0, &mut nessun_cat);
        for e in ev {
            if let Evento::Audio { pcm, rate } = e {
                assert_eq!(rate, 48_000);
                uscito.extend(pcm);
            }
        }
    }
    assert_eq!(uscito.len(), frame, "due pacchetti di due frame ciascuno");
    let rms = |v: &[i16]| (v.iter().map(|s| f64::from(*s).powi(2)).sum::<f64>() / v.len() as f64).sqrt();
    let (a, b) = (rms(&tono), rms(&uscito[960..]));
    assert!(b > a * 0.5 && b < a * 1.5, "energia: ingresso {a:.0}, uscita {b:.0}");
}

fn scegli_digi(gw: &mut Gateway, tel: SocketAddr) {
    let scegli = dl::pacchetto(Tipo::Ctrl, 0, 0, 0, 0, 0, &[Ctrl::Scegli as u8, Profilo::Digi as u8]);
    let (_, ev) = gw.ricevi(&scegli, tel, 0, &mut nessun_cat);
    assert_eq!(ev, vec![Evento::Profilo(Profilo::Digi)]);
}

#[test]
fn digi_in_uscita_e_il_decimato_compresso_senza_perdite() {
    let relay = addr("198.51.100.7:5555");
    let tel = addr("203.0.113.9:4000");
    let mut gw = Gateway::new();
    gw.imposta_destinazione(Some(relay));
    scegli_digi(&mut gw, tel);

    let pcm: Vec<i16> = (0..1920 * 2).map(|i| ((i * 37) % 2000 - 1000) as i16).collect();
    let inv = gw.invia_audio(&pcm, 0);
    assert_eq!(inv.len(), 2, "due blocchi da 40 ms");
    let mut tutti = Vec::new();
    for i in &inv {
        let p = dl::leggi(&i.dati).unwrap();
        assert_eq!(p.profilo, Profilo::Digi);
        let s = lossless::decomprimi(&p.corpo).expect("blocco lossless");
        assert_eq!(s.len(), 480);
        tutti.extend(s);
    }
    // stesso risultato del decimatore fatto a mano, campione per campione
    let atteso = decolink_rs::resample::Decimatore::digi().giu(&pcm);
    assert_eq!(tutti, atteso);
    let (a, b) = (dl::leggi(&inv[0].dati).unwrap().seq, dl::leggi(&inv[1].dati).unwrap().seq);
    assert_eq!(b, a.wrapping_add(1));
}

#[test]
fn nack_per_il_buco_e_ritrasmissione_del_pacchetto_perso() {
    let relay = addr("198.51.100.7:5555");
    let tel = addr("203.0.113.9:4000");
    let pcm: Vec<i16> = (0..1920 * 3).map(|i| ((i * 37) % 2000 - 1000) as i16).collect();

    // lato radio: tre pacchetti DIGI verso il telefono
    let mut tx = Gateway::new();
    tx.imposta_destinazione(Some(relay));
    scegli_digi(&mut tx, tel);
    let inviati = tx.invia_audio(&pcm, 0);
    assert_eq!(inviati.len(), 3);

    // il telefono riceve il primo e il terzo, perde il secondo
    let come_tx = |dati: &[u8]| {
        let p = dl::leggi(dati).unwrap();
        dl::pacchetto(Tipo::AudioTx, p.profilo as u8, p.flag, 0, p.seq, p.tempo, &p.corpo)
    };
    let mut tel_gw = Gateway::new();
    let (_, _) = tel_gw.ricevi(&come_tx(&inviati[0].dati), tel, 0, &mut nessun_cat);
    let (nack, _) = tel_gw.ricevi(&come_tx(&inviati[2].dati), tel, 0, &mut nessun_cat);
    assert_eq!(nack.len(), 1, "un NACK per la sequenza mancante");
    assert_eq!(nack[0].verso, tel);
    let pn = dl::leggi(&nack[0].dati).unwrap();
    assert_eq!(pn.tipo, Tipo::Nack);
    assert_eq!(pn.corpo, vec![Ctrl::Report as u8, 1, 0, dl::leggi(&inviati[1].dati).unwrap().seq as u8]);

    // il lato radio riceve il NACK e rimanda il pacchetto perso, identico
    let (rit, _) = tx.ricevi(&nack[0].dati, tel, 0, &mut nessun_cat);
    assert_eq!(rit.len(), 1);
    assert_eq!(rit[0].dati, inviati[1].dati);
}

#[cfg(feature = "opus")]
#[test]
fn report_di_perdita_abbassa_e_rialza_il_bitrate() {
    let tel = addr("203.0.113.9:4000");
    let mut gw = Gateway::new();
    let hello = dl::pacchetto(Tipo::Ctrl, 0, 0, 0, 0, 0, &[Ctrl::Hello as u8, dl::capacita::AGGR]);
    gw.ricevi(&hello, tel, 0, &mut nessun_cat);
    let scegli = dl::pacchetto(Tipo::Ctrl, 0, 0, 0, 0, 0, &[Ctrl::Scegli as u8, Profilo::Voce as u8]);
    gw.ricevi(&scegli, tel, 0, &mut nessun_cat);
    assert_eq!(gw.bitrate(), 24_000);

    let perde = dl::pacchetto(Tipo::Ctrl, 0, 0, 0, 0, 0, &[Ctrl::Report as u8, 10]);
    gw.ricevi(&perde, tel, 0, &mut nessun_cat);
    assert_eq!(gw.bitrate(), 16_000);

    let sana = dl::pacchetto(Tipo::Ctrl, 0, 0, 0, 0, 0, &[Ctrl::Report as u8, 1]);
    gw.ricevi(&sana, tel, 0, &mut nessun_cat);
    assert_eq!(gw.bitrate(), 24_000);
}

#[test]
fn stato_ptt_arriva_dal_relay() {
    let relay = addr("198.51.100.7:5555");
    let mut gw = Gateway::new();
    let (_, ev) = gw.ricevi(&v2_pacchetto(v2::TXSTATE, 1, 0, 48_000, b"tx busy IK0AAA"), relay, 0, &mut nessun_cat);
    assert_eq!(ev, vec![Evento::StatoTx("tx busy IK0AAA".into())]);
}
