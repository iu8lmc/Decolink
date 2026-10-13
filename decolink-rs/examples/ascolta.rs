//! Prova a mano dell'audio: elenca i dispositivi e cattura due secondi dall'ingresso.
//! cargo run --example ascolta --features audio
use decolink_rs::audio::{dispositivi, Ingresso};
use std::time::{Duration, Instant};

fn main() {
    let (ing, usc) = dispositivi();
    println!("ingressi:");
    for n in &ing { println!("  {n}"); }
    println!("uscite:");
    for n in &usc { println!("  {n}"); }

    let ingresso = match Ingresso::apri(None) {
        Ok(i) => i,
        Err(e) => { println!("ingresso non aperto: {e}"); return; }
    };
    println!("scheda a {} Hz", ingresso.rate_scheda);
    let mut pcm = Vec::new();
    let fine = Instant::now() + Duration::from_secs(2);
    while Instant::now() < fine {
        std::thread::sleep(Duration::from_millis(50));
        pcm.extend(ingresso.ricevi());
    }
    let picco = pcm.iter().map(|s| s.unsigned_abs()).max().unwrap_or(0);
    let rms = (pcm.iter().map(|s| (*s as f64).powi(2)).sum::<f64>() / pcm.len().max(1) as f64).sqrt();
    println!("campioni a 48 kHz: {} (attesi circa 96000)", pcm.len());
    println!("picco {picco}, RMS {rms:.1}");
}
