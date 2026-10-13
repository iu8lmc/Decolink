//! Compatibilita' bit per bit con il wrapper C++ `gui/opusvoce.h`.
//!
//! `vettori_opus.txt` contiene i pacchetti prodotti dal C++ con la stessa
//! libopus. Il segnale e' intero (dente di sega modulato): il test ricostruisce
//! gli stessi frame e controlla che i pacchetti siano identici byte per byte.

#![cfg(feature = "opus")]

use decolink_rs::opus::{OpusVoce, FRAME};

fn da_hex(s: &str) -> Vec<u8> {
    (0..s.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&s[i..i + 2], 16).expect("hex"))
        .collect()
}

/// Stesso segnale del generatore C++: frame `f` del caso.
fn frame(f: usize) -> Vec<i16> {
    (0..FRAME)
        .map(|i| {
            let t = (f * FRAME + i) as i64;
            let dente = (t * 37) % 2000 - 1000;
            let quadra = if (t / 50) % 2 == 1 { 4000 } else { -4000 };
            (dente * 12 + quadra) as i16
        })
        .collect()
}

#[test]
fn pacchetti_identici_al_cpp() {
    let testo = include_str!("vettori_opus.txt");
    let mut casi = 0;
    for riga in testo.lines().filter(|l| !l.starts_with('#') && !l.trim().is_empty()) {
        let campi: Vec<&str> = riga.split_whitespace().collect();
        assert_eq!(campi.len(), 4, "riga malformata: {riga}");
        let (nome, f): (&str, usize) = (campi[0], campi[1].parse().unwrap());
        let lunghezza: usize = campi[2].parse().unwrap();
        let atteso = da_hex(campi[3]);
        assert_eq!(atteso.len(), lunghezza, "{nome}/{f}: lunghezza dichiarata");

        let (bitrate, banda) = match nome {
            "voce24k6k" => (24_000, 6_000),
            "cw12k4k" => (12_000, 4_000),
            altro => panic!("caso sconosciuto {altro}"),
        };
        let mut o = OpusVoce::default();
        o.apri(bitrate, banda).expect("apertura");
        // I frame di un caso vanno codificati in ordine dallo stesso codificatore.
        let mut ultimo = None;
        for k in 0..=f {
            ultimo = o.codifica(&frame(k));
        }
        assert_eq!(ultimo.expect("codifica"), atteso, "{nome} frame {f}: pacchetto diverso dal C++");
        casi += 1;
    }
    assert_eq!(casi, 12, "numero di vettori inatteso");
}
