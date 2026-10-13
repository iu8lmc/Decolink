//! Audio di ingresso e uscita con cpal (WASAPI su Windows).
//!
//! Il motore lavora a 48 kHz mono int16, come il C++. Se la scheda non lo
//! supporta si prende il suo formato di default, si fa il downmix a mono e si
//! ricampiona. Il ricampionamento e' lineare: piu' povero del filtro del C++
//! (`resample.h`), e va migliorato prima di usarlo per la decodifica FT8.

#![cfg(feature = "audio")]

use std::collections::VecDeque;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::mpsc::{channel, Receiver, Sender};
use std::sync::{Arc, Mutex};

use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use cpal::{Sample, SampleFormat, SampleRate, Stream, StreamConfig};

/// Frequenza del motore.
pub const RATE: u32 = 48_000;

/// Ricampionamento lineare, con stato fra un blocco e il successivo.
pub struct Ricampiona {
    passo: f64,
    prev: f32,
    pos: f64,
}

impl Ricampiona {
    /// `da` e `a` sono le frequenze di campionamento.
    pub fn new(da: u32, a: u32) -> Self {
        Ricampiona {
            passo: f64::from(da) / f64::from(a),
            prev: 0.0,
            pos: 1.0,
        }
    }

    /// Converte un blocco. Il numero di campioni in uscita varia di poco da un
    /// blocco all'altro, ma la fase si conserva e non si perde niente al bordo.
    pub fn processa(&mut self, input: &[f32]) -> Vec<f32> {
        let mut buf = Vec::with_capacity(input.len() + 1);
        buf.push(self.prev);
        buf.extend_from_slice(input);
        let mut out = Vec::with_capacity((input.len() as f64 / self.passo) as usize + 2);
        let mut i = self.pos;
        loop {
            let k = i.floor() as usize;
            if k + 1 >= buf.len() {
                break;
            }
            let frac = (i - k as f64) as f32;
            out.push(buf[k] + (buf[k + 1] - buf[k]) * frac);
            i += self.passo;
        }
        let ultimo = buf.len() - 1;
        self.prev = buf[ultimo];
        self.pos = i - ultimo as f64;
        out
    }
}

/// Converte un campione in f32 normalizzato a [-1, 1].
fn in_f32<T: Sample>(s: T) -> f32
where
    f32: cpal::FromSample<T>,
{
    f32::from_sample(s)
}

/// Converte f32 normalizzato in int16, con saturazione.
fn in_i16(v: f32) -> i16 {
    (v.clamp(-1.0, 1.0) * 32767.0) as i16
}

/// Chiama `$f::<T>` con il tipo di campione corrispondente al formato del dispositivo.
macro_rules! per_formato {
    ($formato:expr, $t:ident => $f:expr) => {
        match $formato {
            SampleFormat::F32 => { type $t = f32; $f }
            SampleFormat::F64 => { type $t = f64; $f }
            SampleFormat::I8 => { type $t = i8; $f }
            SampleFormat::I16 => { type $t = i16; $f }
            SampleFormat::I32 => { type $t = i32; $f }
            SampleFormat::U8 => { type $t = u8; $f }
            SampleFormat::U16 => { type $t = u16; $f }
            SampleFormat::U32 => { type $t = u32; $f }
            altro => Err(format!("formato di campionamento non gestito: {altro:?}")),
        }
    };
}

/// Dispositivi visibili, per il menu della GUI e per la CLI.
pub fn dispositivi() -> (Vec<String>, Vec<String>) {
    let host = cpal::default_host();
    let ingressi = host
        .input_devices()
        .map(|it| it.filter_map(|d| d.name().ok()).collect())
        .unwrap_or_default();
    let uscite = host
        .output_devices()
        .map(|it| it.filter_map(|d| d.name().ok()).collect())
        .unwrap_or_default();
    (ingressi, uscite)
}

fn trova(nome: Option<&str>, input: bool) -> Result<cpal::Device, String> {
    let host = cpal::default_host();
    match nome {
        None => {
            let d = if input { host.default_input_device() } else { host.default_output_device() };
            d.ok_or_else(|| "nessun dispositivo audio predefinito".to_string())
        }
        Some(n) => {
            let mut it = if input { host.input_devices() } else { host.output_devices() }
                .map_err(|e| e.to_string())?;
            it.find(|d| d.name().map(|x| x == n).unwrap_or(false))
                .ok_or_else(|| format!("dispositivo «{n}» non trovato"))
        }
    }
}

/// Ingresso a 48 kHz mono: i campioni arrivano con `ricevi`.
pub struct Ingresso {
    _stream: Stream,
    rx: Receiver<Vec<i16>>,
    pub rate_scheda: u32,
}

impl Ingresso {
    /// Apre l'ingresso. `None` per il dispositivo predefinito.
    pub fn apri(nome: Option<&str>) -> Result<Self, String> {
        let dev = trova(nome, true)?;
        let supportata = dev
            .supported_input_configs()
            .map_err(|e| e.to_string())?
            .find(|c| c.channels() == 1 && c.min_sample_rate().0 <= RATE && c.max_sample_rate().0 >= RATE);
        let (cfg, formato) = match supportata {
            Some(c) => (c.with_sample_rate(SampleRate(RATE)).config(), c.sample_format()),
            None => {
                let d = dev.default_input_config().map_err(|e| e.to_string())?;
                (d.config(), d.sample_format())
            }
        };
        let canali = usize::from(cfg.channels);
        let rate_scheda = cfg.sample_rate.0;
        let (tx, rx) = channel();
        let err = |e| eprintln!("ingresso audio: {e}");
        let stream = per_formato!(formato, T => costruisci_in::<T>(&dev, &cfg, canali, rate_scheda, tx, err))?;
        stream.play().map_err(|e| e.to_string())?;
        Ok(Ingresso { _stream: stream, rx, rate_scheda })
    }

    /// Tutto l'audio arrivato finora, senza bloccare.
    pub fn ricevi(&self) -> Vec<i16> {
        let mut out = Vec::new();
        while let Ok(blocco) = self.rx.try_recv() {
            out.extend(blocco);
        }
        out
    }
}

fn costruisci_in<T>(
    dev: &cpal::Device,
    cfg: &StreamConfig,
    canali: usize,
    rate_scheda: u32,
    tx: Sender<Vec<i16>>,
    err: impl FnMut(cpal::StreamError) + Send + 'static,
) -> Result<Stream, String>
where
    T: cpal::SizedSample + Send + 'static,
    f32: cpal::FromSample<T>,
{
    let mut ric = Ricampiona::new(rate_scheda, RATE);
    dev.build_input_stream(
        cfg,
        move |dati: &[T], _: &cpal::InputCallbackInfo| {
            // downmix a mono: media dei canali di ciascun fotogramma
            let mono: Vec<f32> = dati
                .chunks(canali)
                .map(|f| f.iter().map(|s| in_f32(*s)).sum::<f32>() / canali as f32)
                .collect();
            let pronto = if rate_scheda == RATE { mono } else { ric.processa(&mono) };
            let _ = tx.send(pronto.into_iter().map(in_i16).collect());
        },
        err,
        None,
    )
    .map_err(|e| e.to_string())
}

/// Uscita a 48 kHz mono. `scrivi` accoda i campioni; il dispositivo li prende
/// quando serve, e dove mancano scrive silenzio e conta il sottoscorrimento.
pub struct Uscita {
    _stream: Stream,
    coda: Arc<Mutex<VecDeque<i16>>>,
    sottoscorrimenti: Arc<AtomicU64>,
    ric: Ricampiona,
    rate_scheda: u32,
}

impl Uscita {
    pub fn apri(nome: Option<&str>) -> Result<Self, String> {
        let dev = trova(nome, false)?;
        let d = dev.default_output_config().map_err(|e| e.to_string())?;
        let formato = d.sample_format();
        let cfg = d.config();
        let canali = usize::from(cfg.channels);
        let rate_scheda = cfg.sample_rate.0;
        let coda = Arc::new(Mutex::new(VecDeque::<i16>::new()));
        let sottoscorrimenti = Arc::new(AtomicU64::new(0));
        let err = |e| eprintln!("uscita audio: {e}");
        let stream = per_formato!(formato, T => costruisci_out::<T>(&dev, &cfg, canali, rate_scheda, coda.clone(), sottoscorrimenti.clone(), err))?;
        stream.play().map_err(|e| e.to_string())?;
        Ok(Uscita {
            _stream: stream,
            coda,
            sottoscorrimenti,
            ric: Ricampiona::new(RATE, rate_scheda),
            rate_scheda,
        })
    }

    /// Accoda audio a 48 kHz mono.
    pub fn scrivi(&mut self, pcm: &[i16]) {
        let pronto: Vec<i16> = if self.rate_scheda == RATE {
            pcm.to_vec()
        } else {
            let f: Vec<f32> = pcm.iter().map(|s| f32::from(*s) / 32768.0).collect();
            self.ric.processa(&f).into_iter().map(in_i16).collect()
        };
        if let Ok(mut c) = self.coda.lock() {
            c.extend(pronto);
        }
    }

    /// Quante volte il dispositivo ha trovato la coda vuota.
    pub fn sottoscorrimenti(&self) -> u64 {
        self.sottoscorrimenti.load(Ordering::Relaxed)
    }
}

fn costruisci_out<T>(
    dev: &cpal::Device,
    cfg: &StreamConfig,
    canali: usize,
    rate_scheda: u32,
    coda: Arc<Mutex<VecDeque<i16>>>,
    sottoscorrimenti: Arc<AtomicU64>,
    err: impl FnMut(cpal::StreamError) + Send + 'static,
) -> Result<Stream, String>
where
    T: cpal::SizedSample + cpal::FromSample<f32> + Send + 'static,
{
    let _ = rate_scheda;
    dev.build_output_stream(
        cfg,
        move |dati: &mut [T], _: &cpal::OutputCallbackInfo| {
            let mut c = match coda.lock() {
                Ok(c) => c,
                Err(_) => return,
            };
            for fotogramma in dati.chunks_mut(canali) {
                let v = match c.pop_front() {
                    Some(s) => f32::from(s) / 32768.0,
                    None => {
                        sottoscorrimenti.fetch_add(1, Ordering::Relaxed);
                        0.0
                    }
                };
                for canale in fotogramma.iter_mut() {
                    *canale = T::from_sample(v);
                }
            }
        },
        err,
        None,
    )
    .map_err(|e| e.to_string())
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn ricampionamento_dimezza_il_numero_di_campioni() {
        let mut r = Ricampiona::new(48_000, 24_000);
        let input = vec![0.5f32; 960];
        let mut tot = 0;
        for _ in 0..4 {
            tot += r.processa(&input).len();
        }
        // 3840 campioni a 48 kHz -> circa 1920 a 24 kHz (tolleranza di un blocco)
        assert!((tot as i64 - 1920).abs() <= 2, "{tot}");
    }

    #[test]
    fn ricampionamento_conserva_la_continuita_fra_blocchi() {
        // Una rampa lineare deve restare lineare anche attraverso il confine dei blocchi.
        let mut r = Ricampiona::new(48_000, 48_000 / 2);
        let rampa: Vec<f32> = (0..200).map(|i| i as f32).collect();
        let mut out = Vec::new();
        for blocco in rampa.chunks(20) {
            out.extend(r.processa(blocco));
        }
        for w in out.windows(2).skip(2) {
            assert!((w[1] - w[0] - 2.0).abs() < 1e-3, "salto a {w:?}");
        }
    }

    #[test]
    fn saturazione_in_i16() {
        assert_eq!(in_i16(2.0), 32767);
        assert_eq!(in_i16(-2.0), -32767);
        assert_eq!(in_i16(0.0), 0);
    }

    #[test]
    fn elenco_dispositivi_non_va_in_panico() {
        let (_i, _u) = dispositivi();
    }
}
