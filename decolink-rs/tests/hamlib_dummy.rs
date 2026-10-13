//! Giro completo attraverso libhamlib con il backend `Dummy` (modello 1): nessuna
//! radio e nessuna rete. Verifica che apertura, frequenza, modo e PTT passino
//! davvero per Hamlib e tornino indietro col valore scritto.

#![cfg(feature = "hamlib")]

use decolink_rs::hamlib::Radio;

const MODEL_DUMMY: i32 = 1;

#[test]
fn dummy_legge_quello_che_ha_scritto() {
    let mut radio = Radio::apri(MODEL_DUMMY, "", 9600, 8, 1, "n").expect("apertura Dummy");
    assert!(!radio.per_rete());

    radio.imposta_frequenza(14_074_000.0).expect("scrittura frequenza");
    assert_eq!(radio.frequenza().expect("lettura frequenza"), 14_074_000.0);

    radio.imposta_modo("CW").expect("scrittura modo");
    assert_eq!(radio.modo().expect("lettura modo"), "CW");

    radio.imposta_modo("USB").expect("scrittura modo");
    assert_eq!(radio.modo().expect("lettura modo"), "USB");

    radio.imposta_ptt(true).expect("ptt on");
    assert!(radio.ptt().expect("lettura ptt"));
    radio.imposta_ptt(false).expect("ptt off");
    assert!(!radio.ptt().expect("lettura ptt"));
}

#[test]
fn modo_sconosciuto_e_rifiutato() {
    let mut radio = Radio::apri(MODEL_DUMMY, "", 9600, 8, 1, "n").expect("apertura Dummy");
    assert!(radio.imposta_modo("NONESISTE").is_err());
}

#[test]
fn modello_inesistente_da_errore_senza_crash() {
    assert!(Radio::apri(-42, "", 9600, 8, 1, "n").is_err());
}
