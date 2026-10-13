//! Compatibilita' bit per bit con `gui/lossless.h`.
//!
//! `vettori_lossless.txt` e' prodotto dal C++ originale (vedi il commento in
//! testa al file): per ogni segnale riporta il blocco che il C++ scrive. Il
//! porting Rust deve produrre gli stessi byte, e decodificarli nello stesso
//! segnale. Non e' un test di round-trip: e' il contratto col telefono.

use decolink_rs::lossless::{comprimi, decomprimi};

fn da_hex(s: &str) -> Vec<u8> {
    (0..s.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&s[i..i + 2], 16).expect("hex"))
        .collect()
}

#[test]
fn blocchi_identici_al_cpp() {
    let testo = include_str!("vettori_lossless.txt");
    let mut casi = 0;
    for riga in testo.lines().filter(|l| !l.starts_with('#') && !l.trim().is_empty()) {
        let campi: Vec<&str> = riga.split_whitespace().collect();
        assert_eq!(campi.len(), 5, "riga malformata: {riga}");
        let nome = campi[0];
        let n: usize = campi[1].parse().unwrap();
        let campioni_be = da_hex(campi[2]);
        let blocco_cpp = da_hex(campi[3]);
        let ok_cpp = campi[4] == "1";

        let campioni: Vec<i16> = campioni_be
            .chunks(2)
            .map(|c| i16::from_be_bytes([c[0], c[1]]))
            .collect();
        assert_eq!(campioni.len(), n, "{nome}: lunghezza");

        let blocco_rs = comprimi(&campioni);
        assert_eq!(blocco_rs, blocco_cpp, "{nome}: il blocco Rust differisce dal C++");

        let decodificato = decomprimi(&blocco_cpp).expect("il blocco C++ deve decodificarsi");
        assert_eq!(decodificato, campioni, "{nome}: decodifica diversa dal segnale");
        assert!(ok_cpp, "{nome}: il C++ stesso non ha superato il round-trip");
        casi += 1;
    }
    assert_eq!(casi, 11, "numero di vettori inatteso");
}
