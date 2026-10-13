//! Riduzione di frequenza per i digitali (porting di `gui/resample.h`):
//! 48 kHz -> 12 kHz con un FIR a 65 tap, finestra di Blackman, taglio a 5400 Hz.
//!
//! Il filtro e' quello del C++: il decodificatore del telefono riceve gli stessi
//! campioni che WSJT-X riceverebbe da una radio sul tavolo.

use std::f64::consts::PI;

pub const DIGI_RATE: u32 = 12_000;
pub const DIGI_RAPPORTO: usize = 4;
/// Dispari: il ritardo del filtro e' un numero intero di campioni.
pub const FIR_TAP: usize = 65;
pub const TAGLIO_DIGI_HZ: f64 = 5400.0;

/// Coefficienti del passa-basso FIR, a guadagno unitario in continua.
pub fn fir_coeff(taglio_hz: f64) -> Vec<f64> {
    let fc = taglio_hz / 48_000.0;
    let meta = (FIR_TAP / 2) as f64;
    let mut h = vec![0.0f64; FIR_TAP];
    let mut somma = 0.0;
    for (i, hi) in h.iter_mut().enumerate() {
        let n = i as f64 - meta;
        let sinc = if n == 0.0 { 2.0 * fc } else { (2.0 * PI * fc * n).sin() / (PI * n) };
        // Finestra di Blackman: attenuazione fuori banda oltre i 70 dB.
        let x = i as f64 / (FIR_TAP as f64 - 1.0);
        let w = 0.42 - 0.5 * (2.0 * PI * x).cos() + 0.08 * (4.0 * PI * x).cos();
        *hi = sinc * w;
        somma += *hi;
    }
    for v in &mut h {
        *v /= somma;
    }
    h
}

/// Riduce la frequenza tenendo la storia fra un blocco e il successivo: azzerarla
/// ogni volta produrrebbe uno scatto a ogni pacchetto.
pub struct Decimatore {
    rapporto: usize,
    h: Vec<f64>,
    storia: [f64; FIR_TAP],
    fase: usize,
}

impl Decimatore {
    pub fn new(rapporto: usize, taglio_hz: f64) -> Self {
        Decimatore { rapporto, h: fir_coeff(taglio_hz), storia: [0.0; FIR_TAP], fase: 0 }
    }

    /// Digitali: 48 -> 12 kHz con il taglio del C++.
    pub fn digi() -> Self {
        Self::new(DIGI_RAPPORTO, TAGLIO_DIGI_HZ)
    }

    pub fn azzera(&mut self) {
        self.storia = [0.0; FIR_TAP];
        self.fase = 0;
    }

    /// Campioni ridotti prodotti da questo blocco a 48 kHz.
    pub fn giu(&mut self, pcm: &[i16]) -> Vec<i16> {
        let mut out = Vec::with_capacity(pcm.len() / self.rapporto + 2);
        for &x in pcm {
            self.storia.rotate_left(1);
            self.storia[FIR_TAP - 1] = f64::from(x);
            self.fase += 1;
            if self.fase < self.rapporto {
                continue;
            }
            self.fase = 0;
            // Si calcola solo per i campioni che si tengono.
            let acc: f64 = (0..FIR_TAP).map(|k| self.storia[k] * self.h[FIR_TAP - 1 - k]).sum();
            out.push(acc.clamp(-32768.0, 32767.0) as i16);
        }
        out
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn guadagno_unitario_in_continua() {
        let h = fir_coeff(TAGLIO_DIGI_HZ);
        assert!((h.iter().sum::<f64>() - 1.0).abs() < 1e-9);
        assert_eq!(h.len(), FIR_TAP);
    }

    #[test]
    fn continua_passa_e_l_alta_frequenza_no() {
        // Un segnale in continua deve restare costante dopo il transitorio...
        let mut d = Decimatore::digi();
        let out = d.giu(&vec![1000i16; 4000]);
        let coda = &out[out.len() - 100..];
        assert!(coda.iter().all(|v| (i32::from(*v) - 1000).abs() <= 2), "{coda:?}");

        // ...e un segnale a 20 kHz (sopra il taglio) deve sparire.
        let mut d = Decimatore::digi();
        let alto: Vec<i16> = (0..4800)
            .map(|i| (20000.0 * (2.0 * PI * 20_000.0 * i as f64 / 48_000.0).sin()) as i16)
            .collect();
        let out = d.giu(&alto);
        let picco = out[200..].iter().map(|v| v.unsigned_abs()).max().unwrap_or(0);
        assert!(picco < 300, "picco residuo {picco}");
    }

    #[test]
    fn storia_conservata_fra_blocchi() {
        // Spezzare lo stesso segnale in blocchi non deve cambiare il risultato.
        let segnale: Vec<i16> = (0..960).map(|i| ((i * 37) % 2000 - 1000) as i16).collect();
        let intero = Decimatore::digi().giu(&segnale);
        let mut a = Decimatore::digi();
        let mut spezzato = a.giu(&segnale[..480]);
        spezzato.extend(a.giu(&segnale[480..]));
        assert_eq!(intero, spezzato);
    }
}
