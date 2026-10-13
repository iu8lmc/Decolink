//! CW a tasto (porting di `gui/cwkey.h`): non si manda audio, si mandano gli
//! istanti in cui il tasto si apre e si chiude, e il tono si rigenera all'arrivo.
//!
//! Il formato del corpo e' sul filo e deve restare identico al C++:
//! ```text
//! byte 0     nota in decine di Hz (70 = 700 Hz)
//! byte 1     numero di eventi
//! poi        u16 per evento: bit 15 = tasto premuto, bit 0-14 = ms dal precedente
//! ```
//! Rilevatore e sintetizzatore sono locali: lavorano in virgola mobile, quindi
//! si verificano con segnali sintetici e non confrontando i campioni.

use std::f64::consts::PI;

/// Risoluzione del rilevatore: un blocco di 5 ms a 48 kHz.
pub const BLOCCO: usize = 240;
pub const MS_PER_BLOCCO: i32 = 5;
/// Banco di note fra 400 e 1000 Hz, a passi di 75 Hz.
const BIN_PRIMO: i32 = 400;
const BIN_PASSO: i32 = 75;
const BIN_NUMERO: i32 = 9;
/// Blocchi di sola osservazione prima di dichiarare qualcosa (100 ms).
const AVVIO: u32 = 20;
/// Stacco minimo fra rumore e picco perche' si creda a un segnale.
const STACCO_MINIMO: f64 = 1.5;

/// Un evento del tasto: il tempo passato dal precedente, e se ora la nota c'e'.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Evento {
    pub delta_ms: u16,
    pub giu: bool,
}

/// Rilevatore con Goertzel su un banco di note.
pub struct Rilevatore {
    acc: Vec<i16>,
    giu: bool,
    rumore: f64,
    picco: f64,
    avvio: u32,
    ms_da_ultimo: i32,
    nota_hz: i32,
    energia_ultima: f64,
}

impl Default for Rilevatore {
    fn default() -> Self {
        Self::new()
    }
}

impl Rilevatore {
    pub fn new() -> Self {
        Rilevatore {
            acc: Vec::new(),
            giu: false,
            rumore: 0.0,
            picco: 0.0,
            avvio: AVVIO,
            ms_da_ultimo: 0,
            nota_hz: 700,
            energia_ultima: 0.0,
        }
    }

    pub fn azzera(&mut self) {
        *self = Rilevatore::new();
    }

    pub fn nota_hz(&self) -> i32 {
        self.nota_hz
    }

    pub fn energia(&self) -> f64 {
        self.energia_ultima
    }

    pub fn premuto(&self) -> bool {
        self.giu
    }

    /// Mangia audio a 48 kHz e restituisce gli eventi maturati.
    pub fn mangia(&mut self, pcm: &[i16]) -> Vec<Evento> {
        let mut fuori = Vec::new();
        self.acc.extend_from_slice(pcm);

        while self.acc.len() >= BLOCCO {
            // Energia in ciascuna nota del banco: si tiene la piu' forte.
            let mut migliore_en = 0.0f64;
            let mut migliore_hz = self.nota_hz;
            for i in 0..BIN_NUMERO {
                let hz = BIN_PRIMO + i * BIN_PASSO;
                let w = 2.0 * PI * f64::from(hz) / 48000.0;
                let coeff = 2.0 * w.cos();
                let (mut s1, mut s2) = (0.0f64, 0.0f64);
                for k in 0..BLOCCO {
                    let s0 = f64::from(self.acc[k]) / 32768.0 + coeff * s1 - s2;
                    s2 = s1;
                    s1 = s0;
                }
                let en = (s1 * s1 + s2 * s2 - coeff * s1 * s2).sqrt();
                if en > migliore_en {
                    migliore_en = en;
                    migliore_hz = hz;
                }
            }
            self.acc.drain(0..BLOCCO);
            self.energia_ultima = migliore_en;

            // Soglia adattiva: rumore e picco si inseguono con costanti diverse.
            if migliore_en < self.rumore {
                self.rumore += (migliore_en - self.rumore) * 0.30;
            } else {
                self.rumore += (migliore_en - self.rumore) * 0.002;
            }
            if migliore_en > self.picco {
                self.picco += (migliore_en - self.picco) * 0.50;
            } else {
                self.picco += (migliore_en - self.picco) * 0.005;
            }

            self.ms_da_ultimo += MS_PER_BLOCCO;

            if self.avvio > 0 {
                self.avvio -= 1;
                continue;
            }

            let salto = self.picco - self.rumore;
            if salto < STACCO_MINIMO {
                // Nessuno trasmette: meglio tasto su che simboli dal fruscio.
                if self.giu {
                    self.giu = false;
                    fuori.push(self.evento(false));
                }
                continue;
            }

            // Isteresi: si accende piu' in alto di quanto si spenga.
            let soglia_su = self.rumore + salto * 0.55;
            let soglia_giu = self.rumore + salto * 0.40;
            let ora_giu = if self.giu {
                migliore_en > soglia_giu
            } else {
                migliore_en > soglia_su
            };
            if ora_giu != self.giu {
                self.giu = ora_giu;
                if self.giu {
                    self.nota_hz = migliore_hz; // la nota si fissa all'attacco
                }
                fuori.push(self.evento(self.giu));
            }
        }
        fuori
    }

    fn evento(&mut self, giu: bool) -> Evento {
        let e = Evento {
            delta_ms: self.ms_da_ultimo.min(32000) as u16,
            giu,
        };
        self.ms_da_ultimo = 0;
        e
    }
}

/// Corpo del pacchetto CW-KEY. Al massimo 255 eventi, come nel C++.
pub fn corpo_cw(nota_hz: i32, ev: &[Evento]) -> Vec<u8> {
    let mut c = Vec::with_capacity(2 + 2 * ev.len().min(255));
    c.push((nota_hz / 10).clamp(0, 255) as u8);
    c.push(ev.len().min(255) as u8);
    for e in ev.iter().take(255) {
        let v = (if e.giu { 0x8000u16 } else { 0 }) | (e.delta_ms & 0x7FFF);
        c.extend_from_slice(&v.to_be_bytes());
    }
    c
}

/// Legge un corpo CW-KEY. `None` se e' tagliato rispetto al numero di eventi.
pub fn leggi_corpo_cw(c: &[u8]) -> Option<(i32, Vec<Evento>)> {
    if c.len() < 2 {
        return None;
    }
    let nota = i32::from(c[0]) * 10;
    let n = usize::from(c[1]);
    if c.len() < 2 + 2 * n {
        return None;
    }
    let ev = (0..n)
        .map(|i| {
            let v = u16::from_be_bytes([c[2 + 2 * i], c[3 + 2 * i]]);
            Evento {
                delta_ms: v & 0x7FFF,
                giu: v & 0x8000 != 0,
            }
        })
        .collect();
    Some((nota, ev))
}

/// Rigenera il tono dagli eventi, con attacco e rilascio di 5 ms per non fare
/// clic a banda larga.
pub struct Sintetizzatore {
    coda: std::collections::VecDeque<Evento>,
    fase: f64,
    amp: f64,
    giu: bool,
    nota_hz: i32,
    attesa: i64,
}

impl Default for Sintetizzatore {
    fn default() -> Self {
        Self::new()
    }
}

impl Sintetizzatore {
    pub fn new() -> Self {
        Sintetizzatore {
            coda: std::collections::VecDeque::new(),
            fase: 0.0,
            amp: 0.0,
            giu: false,
            nota_hz: 700,
            attesa: 0,
        }
    }

    pub fn azzera(&mut self) {
        *self = Sintetizzatore::new();
    }

    pub fn nota(&mut self, hz: i32) {
        if (200..=2500).contains(&hz) {
            self.nota_hz = hz;
        }
    }

    /// Il `delta_ms` di un evento e' il tempo che passa PRIMA di applicarlo: se
    /// la coda era vuota si arma l'attesa del primo.
    pub fn aggiungi(&mut self, ev: &[Evento]) {
        let era_vuota = self.coda.is_empty();
        self.coda.extend(ev.iter().copied());
        if era_vuota && !self.coda.is_empty() && self.attesa <= 0 {
            self.attesa = i64::from(self.coda[0].delta_ms) * 48;
        }
    }

    pub fn in_attesa(&self) -> bool {
        !self.coda.is_empty()
    }

    /// Produce `n` campioni a 48 kHz consumando la coda degli eventi.
    pub fn genera(&mut self, n: usize) -> Vec<i16> {
        let d_fase = 2.0 * PI * f64::from(self.nota_hz) / 48000.0;
        let passo = 1.0 / 240.0;
        let mut out = Vec::with_capacity(n);
        for _ in 0..n {
            // Il ciclo, non un if: due eventi possono cadere nello stesso campione.
            while self.attesa <= 0 {
                let Some(e) = self.coda.pop_front() else { break };
                self.giu = e.giu;
                self.attesa = self
                    .coda
                    .front()
                    .map_or(0, |p| i64::from(p.delta_ms) * 48);
            }
            if self.attesa > 0 {
                self.attesa -= 1;
            }

            self.amp += if self.giu { passo } else { -passo };
            self.amp = self.amp.clamp(0.0, 1.0);
            self.fase += d_fase;
            if self.fase > 2.0 * PI {
                self.fase -= 2.0 * PI;
            }
            out.push((self.amp * 18000.0 * self.fase.sin()) as i16);
        }
        out
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn corpo_e_inverso() {
        let ev = vec![
            Evento { delta_ms: 0, giu: true },
            Evento { delta_ms: 60, giu: false },
            Evento { delta_ms: 32767, giu: true },
        ];
        let c = corpo_cw(700, &ev);
        assert_eq!(c[0], 70);
        assert_eq!(c[1], 3);
        assert_eq!(&c[2..4], &[0x80, 0x00]);
        assert_eq!(&c[4..6], &[0x00, 60]);
        assert_eq!(&c[6..8], &[0xFF, 0xFF]);
        let (nota, letti) = leggi_corpo_cw(&c).expect("valido");
        assert_eq!(nota, 700);
        assert_eq!(letti, ev);
    }

    #[test]
    fn corpo_tagliato_e_rifiutato() {
        assert!(leggi_corpo_cw(&[]).is_none());
        assert!(leggi_corpo_cw(&[70, 3, 0x80, 0]).is_none());
    }

    #[test]
    fn corpo_con_piu_di_255_eventi_si_tronca() {
        let ev = vec![Evento { delta_ms: 1, giu: false }; 300];
        let c = corpo_cw(700, &ev);
        assert_eq!(c[1], 255);
        assert_eq!(c.len(), 2 + 2 * 255);
    }

    /// Tono di `ms` millisecondi a 700 Hz, ampiezza `amp`.
    fn tono(out: &mut Vec<i16>, ms: usize, amp: f64, fase: &mut f64) {
        for _ in 0..ms * 48 {
            *fase += 2.0 * PI * 700.0 / 48000.0;
            out.push((amp * fase.sin()) as i16);
        }
    }

    fn silenzio_rumoroso(out: &mut Vec<i16>, ms: usize, seme: &mut u32) {
        for _ in 0..ms * 48 {
            *seme = seme.wrapping_mul(1_664_525).wrapping_add(1_013_904_223);
            out.push((((*seme >> 16) as i32 - 32768) * 200 / 32768) as i16);
        }
    }

    #[test]
    fn il_rilevatore_riconosce_punti_e_linee() {
        // 300 ms di fondo, poi punto punto linea con spazi di 60 ms.
        let mut pcm = Vec::new();
        let mut seme = 5u32;
        let mut fase = 0.0;
        silenzio_rumoroso(&mut pcm, 300, &mut seme);
        for &(on, off) in &[(60usize, 60usize), (60, 60), (180, 60)] {
            tono(&mut pcm, on, 10000.0, &mut fase);
            silenzio_rumoroso(&mut pcm, off, &mut seme);
        }
        silenzio_rumoroso(&mut pcm, 300, &mut seme);

        let mut r = Rilevatore::new();
        let mut ev = Vec::new();
        for chunk in pcm.chunks(960) {
            ev.extend(r.mangia(chunk));
        }
        let accensioni: Vec<u16> = ev.iter().filter(|e| e.giu).map(|e| e.delta_ms).collect();
        let spegnimenti: Vec<u16> = ev.iter().filter(|e| !e.giu).map(|e| e.delta_ms).collect();
        assert_eq!(accensioni.len(), 3, "tre simboli: {ev:?}");
        assert_eq!(spegnimenti.len(), 3, "tre rilasci: {ev:?}");
        // Le durate: punto ~60 ms, linea ~180 ms, con tolleranza di 15 ms.
        let durata = |i: usize| spegnimenti[i] as i32;
        assert!((durata(0) - 60).abs() <= 15, "punto: {}", durata(0));
        assert!((durata(1) - 60).abs() <= 15, "punto: {}", durata(1));
        assert!((durata(2) - 180).abs() <= 15, "linea: {}", durata(2));
        assert!((accensioni[0] as i32 - 300).abs() <= 15, "attesa iniziale: {}", accensioni[0]);
    }

    #[test]
    fn il_rilevatore_resta_muto_sul_fruscio() {
        let mut pcm = Vec::new();
        let mut seme = 11u32;
        silenzio_rumoroso(&mut pcm, 3000, &mut seme);
        let mut r = Rilevatore::new();
        let mut ev = Vec::new();
        for chunk in pcm.chunks(960) {
            ev.extend(r.mangia(chunk));
        }
        assert!(ev.is_empty(), "il fruscio non deve produrre simboli: {ev:?}");
    }

    #[test]
    fn il_sintetizzatore_segue_la_coda() {
        let mut s = Sintetizzatore::new();
        // 100 ms di silenzio, poi 100 ms di tasto giu'.
        s.aggiungi(&[
            Evento { delta_ms: 100, giu: true },
            Evento { delta_ms: 100, giu: false },
        ]);
        let pcm = s.genera(48 * 300);
        let ampiezza = |a: usize, b: usize| pcm[a..b].iter().map(|v| v.unsigned_abs()).max().unwrap_or(0);
        assert!(ampiezza(0, 48 * 90) < 50, "prima dell'evento deve essere muto");
        assert!(ampiezza(48 * 150, 48 * 180) > 10000, "tasto giu' deve suonare");
        assert!(ampiezza(48 * 260, 48 * 300) < 50, "dopo il rilascio deve tacere");
        assert!(!s.in_attesa());
    }

    #[test]
    fn il_sintetizzatore_non_va_fuori_tempo_con_eventi_nello_stesso_campione() {
        let mut s = Sintetizzatore::new();
        s.aggiungi(&[
            Evento { delta_ms: 0, giu: true },
            Evento { delta_ms: 0, giu: false },
            Evento { delta_ms: 0, giu: true },
        ]);
        let pcm = s.genera(480);
        assert_eq!(pcm.len(), 480);
        assert!(!s.in_attesa());
    }
}
