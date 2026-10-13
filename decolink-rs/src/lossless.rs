//! Compressione senza perdite dell'audio per i modi digitali (porting di
//! `gui/lossless.h`).
//!
//! Il formato di blocco deve restare identico a quello del C++: il telefono lo
//! decodifica con gli stessi conti, bit per bit. Per questo la predizione vive
//! in aritmetica intera, e i coefficienti LPC si calcolano in virgola mobile
//! ma si usano quantizzati.
//!
//! Blocco:
//! ```text
//! u16  numero di campioni (big-endian)
//! u8   ordine (bit 0-3) | 0x80 se predittore adattivo
//! u8   k di Rice (bit 0-3) | spostamento dei coefficienti (bit 4-7)
//! i16  x ordine: i campioni iniziali
//! i16  x ordine: i coefficienti, solo col predittore adattivo
//! bit  residui in codifica di Rice
//! ```

const LPC_MAX_ORDINE: usize = 8;
const LPC_PRECISIONE: u32 = 14;

// ---- scrittura e lettura dei bit ------------------------------------------

struct BitOut<'a> {
    out: &'a mut Vec<u8>,
    acc: u64,
    usati: u32,
}

impl<'a> BitOut<'a> {
    fn new(out: &'a mut Vec<u8>) -> Self {
        BitOut { out, acc: 0, usati: 0 }
    }

    /// Scrive gli `n` bit bassi di `v`, dal più significativo.
    fn bit(&mut self, v: u32, mut n: u32) {
        while n > 0 {
            let quanti = n.min(64 - self.usati);
            let maschera = (1u64 << quanti) - 1;
            self.acc = (self.acc << quanti) | ((u64::from(v) >> (n - quanti)) & maschera);
            self.usati += quanti;
            n -= quanti;
            while self.usati >= 8 {
                self.usati -= 8;
                self.out.push(((self.acc >> self.usati) & 0xFF) as u8);
            }
        }
    }

    /// Unario: `q` zeri e un uno.
    fn unario(&mut self, mut q: u32) {
        while q >= 32 {
            self.bit(0, 32);
            q -= 32;
        }
        if q > 0 {
            self.bit(0, q);
        }
        self.bit(1, 1);
    }

    fn chiudi(&mut self) {
        if self.usati > 0 {
            self.out.push(((self.acc << (8 - self.usati)) & 0xFF) as u8);
            self.usati = 0;
        }
    }
}

struct BitIn<'a> {
    d: &'a [u8],
    pos: usize,
    esaurito: bool,
}

impl<'a> BitIn<'a> {
    fn new(d: &'a [u8]) -> Self {
        BitIn { d, pos: 0, esaurito: false }
    }

    /// Legge `n` bit. Oltre la fine restituisce zeri e alza il flag.
    fn bit(&mut self, n: u32) -> u32 {
        let mut v = 0u32;
        for i in 0..n {
            if self.pos >= self.d.len() * 8 {
                self.esaurito = true;
                return v << (n - i);
            }
            let byte = self.d[self.pos >> 3];
            let off = 7 - (self.pos & 7);
            v = (v << 1) | u32::from((byte >> off) & 1);
            self.pos += 1;
        }
        v
    }

    fn unario(&mut self) -> u32 {
        let mut q = 0u32;
        loop {
            if self.pos >= self.d.len() * 8 {
                self.esaurito = true;
                return q;
            }
            let byte = self.d[self.pos >> 3];
            let off = 7 - (self.pos & 7);
            let uno = (byte >> off) & 1 == 1;
            self.pos += 1;
            if uno {
                return q;
            }
            q += 1;
            if q > 1 << 20 {
                // dati assurdi
                self.esaurito = true;
                return q;
            }
        }
    }
}

// ---- conversioni ----------------------------------------------------------

/// Da intero con segno a senza segno alternando i segni (0, -1, 1, -2, 2...).
pub fn zigzag(v: i32) -> u32 {
    ((v << 1) ^ (v >> 31)) as u32
}

pub fn unzigzag(v: u32) -> i32 {
    ((v >> 1) as i32) ^ ((v & 1) as i32).wrapping_neg()
}

// ---- predittore adattivo (LPC) --------------------------------------------

/// Coefficienti ottimali per il blocco, con Levinson-Durbin. `None` se il
/// segnale non ha struttura da sfruttare. Il vettore restituito ha lunghezza
/// `ordine + 1` e l'indice 0 non si usa, come nel C++.
fn lpc_coeff(x: &[i16], ordine: usize) -> Option<Vec<f64>> {
    let n = x.len();
    if n <= ordine * 2 || ordine < 1 || ordine > LPC_MAX_ORDINE {
        return None;
    }

    let mut r = vec![0.0f64; ordine + 1];
    for (lag, rl) in r.iter_mut().enumerate() {
        let mut acc = 0.0;
        for i in lag..n {
            acc += f64::from(x[i]) * f64::from(x[i - lag]);
        }
        *rl = acc;
    }
    if r[0] <= 0.0 {
        return None;
    }

    let mut a = vec![0.0f64; ordine + 1];
    let mut err = r[0];
    for i in 1..=ordine {
        let mut acc = r[i];
        for j in 1..i {
            acc -= a[j] * r[i - j];
        }
        let k = acc / err;
        if !k.is_finite() || k.abs() >= 1.0 {
            // Il predittore diventerebbe instabile: si tiene l'ordine raggiunto.
            return if i > 1 { Some(a) } else { None };
        }
        let mut nuovo = a.clone();
        nuovo[i] = k;
        for j in 1..i {
            nuovo[j] = a[j] - k * a[i - j];
        }
        a = nuovo;
        err *= 1.0 - k * k;
        if err <= 0.0 {
            return if i > 1 { Some(a) } else { None };
        }
    }
    Some(a)
}

// ---- compressione ---------------------------------------------------------

/// Comprime un blocco di campioni int16 mono. Vuoto se `campioni` è vuoto o
/// troppo lungo per l'intestazione.
pub fn comprimi(campioni: &[i16]) -> Vec<u8> {
    let n = campioni.len();
    if n == 0 || n > 65535 {
        return Vec::new();
    }
    let c = |i: usize| i32::from(campioni[i]);

    // Si provano gli ordini 0..=3 e si tiene quello con i residui più piccoli.
    let mut ordine_migliore = 0usize;
    let mut costo_migliore: i64 = -1;
    let mut migliori: Vec<i32> = Vec::new();
    for ordine in 0..=3usize {
        if ordine >= n {
            break;
        }
        let mut residui = vec![0i32; n];
        let mut somma: i64 = 0;
        for i in 0..n {
            let r = if i < ordine {
                0
            } else {
                let r = match ordine {
                    0 => c(i),
                    1 => c(i) - c(i - 1),
                    2 => c(i) - 2 * c(i - 1) + c(i - 2),
                    _ => c(i) - 3 * c(i - 1) + 3 * c(i - 2) - c(i - 3),
                };
                somma += i64::from(r.abs());
                r
            };
            residui[i] = r;
        }
        if costo_migliore < 0 || somma < costo_migliore {
            costo_migliore = somma;
            ordine_migliore = ordine;
            migliori = residui;
        }
    }

    // Predittore adattivo: si tiene il migliore dei due.
    let mut usa_lpc = false;
    let mut ordine_lpc = 0usize;
    let mut shift: u32 = 0;
    let mut coeff_q: Vec<i32> = Vec::new();
    let mut residui_lpc: Vec<i32> = Vec::new();
    let ordine_prova = LPC_MAX_ORDINE.min(n / 8);
    if ordine_prova >= 2 {
        if let Some(a) = lpc_coeff(campioni, ordine_prova) {
            let ordine = a.len() - 1;
            let massimo = a[1..].iter().fold(0.0f64, |m, v| m.max(v.abs()));
            if massimo > 0.0 {
                shift = LPC_PRECISIONE - 1;
                while shift > 0
                    && massimo * f64::from(1i32 << shift) > f64::from((1i32 << (LPC_PRECISIONE - 1)) - 1)
                {
                    shift -= 1;
                }
                coeff_q = vec![0i32; ordine + 1];
                for i in 1..=ordine {
                    coeff_q[i] = (a[i] * f64::from(1i32 << shift)).round() as i32;
                }

                // Residui con i coefficienti quantizzati, in intero: il
                // decodificatore deve rifare gli stessi conti.
                residui_lpc = vec![0i32; n];
                let mut costo: i64 = 0;
                let mut ok = true;
                for i in ordine..n {
                    let mut pred: i64 = 0;
                    for j in 1..=ordine {
                        pred += i64::from(coeff_q[j]) * i64::from(campioni[i - j]);
                    }
                    let res = i64::from(campioni[i]) - (pred >> shift);
                    if res > 0x7FFF_FFFF || res < -0x8000_0000 {
                        ok = false;
                        break;
                    }
                    residui_lpc[i] = res as i32;
                    costo += res.abs();
                }
                let utili_lpc = n - ordine;
                // Ai coefficienti serve spazio nell'intestazione: si usa il
                // predittore adattivo solo se li ripaga.
                if ok && utili_lpc > 0 && costo + (ordine as i64) * 2 * 8 < costo_migliore {
                    usa_lpc = true;
                    ordine_lpc = ordine;
                    costo_migliore = costo;
                }
            }
        }
    }

    let ordine = if usa_lpc { ordine_lpc } else { ordine_migliore };
    let res: &[i32] = if usa_lpc { &residui_lpc } else { &migliori };

    // k di Rice dalla media dei residui.
    let utili = n - ordine;
    let media = if utili > 0 { costo_migliore as f64 / utili as f64 } else { 1.0 };
    let mut k: u32 = 0;
    while k < 15 && f64::from(1u32 << k) < media {
        k += 1;
    }

    let mut out = Vec::with_capacity(4 + 2 * ordine * 2 + n / 2);
    out.push(((n >> 8) & 0xFF) as u8);
    out.push((n & 0xFF) as u8);
    out.push((ordine as u8 & 0xF) | if usa_lpc { 0x80 } else { 0 });
    // Lo spostamento si scrive anche senza LPC: e' cio' che fa il C++.
    out.push((k as u8 & 0xF) | ((shift as u8 & 0xF) << 4));
    for &s in &campioni[..ordine] {
        out.extend_from_slice(&(s as u16).to_be_bytes());
    }
    if usa_lpc {
        for &q in &coeff_q[1..=ordine] {
            out.extend_from_slice(&(q as i16 as u16).to_be_bytes());
        }
    }

    let mut bo = BitOut::new(&mut out);
    for &r in &res[ordine..n] {
        let z = zigzag(r);
        bo.unario(z >> k);
        if k > 0 {
            bo.bit(z & ((1u32 << k) - 1), k);
        }
    }
    bo.chiudi();
    out
}

// ---- decompressione -------------------------------------------------------

/// Decomprime un blocco. `None` se è incoerente o tagliato: un pacchetto guasto
/// deve dare un errore, non audio inventato.
pub fn decomprimi(blocco: &[u8]) -> Option<Vec<i16>> {
    if blocco.len() < 4 {
        return None;
    }
    let n = (usize::from(blocco[0]) << 8) | usize::from(blocco[1]);
    let lpc = blocco[2] & 0x80 != 0;
    let ordine = usize::from(blocco[2] & 0xF);
    let k = u32::from(blocco[3] & 0xF);
    let shift = u32::from(blocco[3] >> 4);
    if n == 0 || ordine > if lpc { LPC_MAX_ORDINE } else { 3 } || (lpc && ordine < 1) || n < ordine {
        return None;
    }

    let testa = 4 + 2 * ordine + if lpc { 2 * ordine } else { 0 };
    if blocco.len() < testa {
        return None;
    }

    let mut out = vec![0i16; n];
    for (i, s) in out.iter_mut().enumerate().take(ordine) {
        *s = i16::from_be_bytes([blocco[4 + 2 * i], blocco[5 + 2 * i]]);
    }

    let mut coeff = vec![0i64; ordine + 1];
    if lpc {
        let base = 4 + 2 * ordine;
        for i in 1..=ordine {
            let p = base + 2 * (i - 1);
            coeff[i] = i64::from(i16::from_be_bytes([blocco[p], blocco[p + 1]]));
        }
    }

    let mut bi = BitIn::new(&blocco[testa..]);
    for i in ordine..n {
        let q = bi.unario();
        let r = if k > 0 { bi.bit(k) } else { 0 };
        if bi.esaurito {
            return None;
        }
        let res = i64::from(unzigzag((q << k) | r));
        let v = if lpc {
            // Gli stessi conti interi dell'encoder, nello stesso ordine.
            let mut pred: i64 = 0;
            for j in 1..=ordine {
                pred += coeff[j] * i64::from(out[i - j]);
            }
            res + (pred >> shift)
        } else {
            let p1 = |j: usize| i64::from(out[i - j]);
            match ordine {
                0 => res,
                1 => res + p1(1),
                2 => res + 2 * p1(1) - p1(2),
                _ => res + 3 * p1(1) - 3 * p1(2) + p1(3),
            }
        };
        out[i] = v as i16;
    }
    Some(out)
}

#[cfg(test)]
mod test {
    use super::*;

    fn rumore(seme: &mut u32, ampiezza: i32) -> i16 {
        *seme = seme.wrapping_mul(1_664_525).wrapping_add(1_013_904_223);
        let v = (*seme >> 16) as i32 - 32768;
        ((v * ampiezza) / 32768).clamp(-32768, 32767) as i16
    }

    fn tono(n: usize, hz: f64, fs: f64, ampiezza: f64) -> Vec<i16> {
        (0..n)
            .map(|i| (ampiezza * (2.0 * std::f64::consts::PI * hz * i as f64 / fs).sin()).round() as i16)
            .collect()
    }

    fn roundtrip(campioni: &[i16]) {
        let b = comprimi(campioni);
        let back = decomprimi(&b).expect("blocco valido");
        assert_eq!(back, campioni, "round-trip di {} campioni", campioni.len());
    }

    #[test]
    fn zigzag_e_inverso() {
        for v in [0, -1, 1, -2, 2, i32::MAX, i32::MIN + 1, -32768, 32767] {
            assert_eq!(unzigzag(zigzag(v)), v);
        }
        assert_eq!(zigzag(0), 0);
        assert_eq!(zigzag(-1), 1);
        assert_eq!(zigzag(1), 2);
    }

    #[test]
    fn blocchi_di_ogni_lunghezza() {
        let mut seme = 1u32;
        for n in [1usize, 2, 3, 4, 15, 16, 17, 64, 480] {
            let v: Vec<i16> = (0..n).map(|_| rumore(&mut seme, 3000)).collect();
            roundtrip(&v);
        }
    }

    #[test]
    fn silenzio_tono_e_rumore() {
        roundtrip(&vec![0i16; 480]);
        roundtrip(&vec![-32768i16; 480]);
        roundtrip(&tono(480, 1500.0, 12000.0, 20000.0));
        let mut seme = 7u32;
        let v: Vec<i16> = (0..480).map(|_| rumore(&mut seme, 32767)).collect();
        roundtrip(&v);
    }

    #[test]
    fn estremi_e_alternanza() {
        let v: Vec<i16> = (0..480).map(|i| if i % 2 == 0 { 32767 } else { -32768 }).collect();
        roundtrip(&v);
        let m: Vec<i16> = (0..480).map(|i| if i % 3 == 0 { -32768 } else { 32767 }).collect();
        roundtrip(&m);
    }

    #[test]
    fn il_tono_comprime_meglio_del_rumore() {
        let t = comprimi(&tono(480, 1500.0, 12000.0, 20000.0));
        let mut seme = 3u32;
        let r: Vec<i16> = (0..480).map(|_| rumore(&mut seme, 32767)).collect();
        assert!(t.len() < comprimi(&r).len());
        // Il C++ misura il 53% sul tono puro: si tiene quella stessa soglia.
        assert!(t.len() * 100 < 960 * 60, "un tono puro deve scendere sotto il 60%");
    }

    #[test]
    fn blocco_tagliato_o_incoerente_non_legge_fuori() {
        assert!(decomprimi(&[]).is_none());
        assert!(decomprimi(&[0, 0, 0, 0]).is_none()); // zero campioni
        assert!(decomprimi(&[0, 5, 0x83, 0]).is_none()); // lpc con ordine 3
        assert!(decomprimi(&[0, 5, 0x05, 0]).is_none()); // ordine 5 senza lpc
        assert!(decomprimi(&[0, 1, 0x02, 0, 0, 0]).is_none()); // piu' campioni iniziali che campioni
        let mut seme = 9u32;
        let v: Vec<i16> = (0..480).map(|_| rumore(&mut seme, 32767)).collect();
        let b = comprimi(&v);
        assert!(decomprimi(&b[..b.len() / 2]).is_none());
    }
}
