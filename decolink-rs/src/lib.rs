//! Decolink, motore in Rust.
//!
//! Porting graduale di `gui/dlproto.h`, `lossless.h`, `cwkey.h`, `hamlibrig.h`
//! e della parte di rete di `gui/main.cpp`. Questo primo passo copre solo il
//! protocollo v3: il piano dati, senza codec né hardware.

pub mod proto;
pub mod lossless;
pub mod cwkey;
#[cfg(feature = "opus")]
pub mod opus;
#[cfg(feature = "audio")]
pub mod audio;
#[cfg(feature = "hamlib")]
pub mod hamlib;
pub mod rete;
pub mod collegamento;
#[cfg(feature = "login")]
pub mod accesso;
pub mod resample;
#[cfg(feature = "relay")]
pub mod relay;
