//! Compatibilita' bit per bit con `gui/resample.h`: il decimatore a 12 kHz deve
//! produrre gli stessi campioni del C++ su due blocchi consecutivi (storia inclusa).

use decolink_rs::resample::Decimatore;

fn da_hex_u16(s: &str) -> Vec<i16> {
    (0..s.len())
        .step_by(4)
        .map(|i| u16::from_str_radix(&s[i..i + 4], 16).expect("hex") as i16)
        .collect()
}

#[test]
fn decimatore_identico_al_cpp() {
    let testo = include_str!("vettori_resample.txt");
    let mut d = Decimatore::digi();
    let mut casi = 0;
    for riga in testo.lines().filter(|l| !l.starts_with('#') && !l.trim().is_empty()) {
        let campi: Vec<&str> = riga.split_whitespace().collect();
        assert_eq!(campi.len(), 4, "riga malformata: {riga}");
        let ingresso = da_hex_u16(campi[2]);
        let atteso = da_hex_u16(campi[3]);
        assert_eq!(ingresso.len(), campi[1].parse::<usize>().unwrap());
        let ottenuto = d.giu(&ingresso);
        assert_eq!(ottenuto, atteso, "{}: decimazione diversa dal C++", campi[0]);
        casi += 1;
    }
    assert_eq!(casi, 2);
}
