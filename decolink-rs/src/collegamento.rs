//! Collegamento UDP reale attorno alla macchina a stati di `rete`: apre il socket,
//! spedisce quello che la macchina produce e le passa i datagrammi che arrivano.

use std::io;
use std::net::{SocketAddr, UdpSocket};
use std::time::{Duration, Instant};

use crate::rete::{Evento, Gateway, Invio};

/// Socket UDP più stato del lato radio.
pub struct Collegamento {
    sock: UdpSocket,
    pub gw: Gateway,
    token: String,
}

impl Collegamento {
    /// Apre il socket su `locale` (es. `0.0.0.0:0` per una porta libera).
    pub fn apri(locale: &str, token: &str) -> io::Result<Self> {
        let sock = UdpSocket::bind(locale)?;
        sock.set_nonblocking(true)?;
        Ok(Collegamento { sock, gw: Gateway::new(), token: token.to_string() })
    }

    /// Token nuovo dopo un rinnovo di accesso.
    pub fn imposta_token(&mut self, token: &str) {
        self.token = token.to_string();
    }

    pub fn indirizzo_locale(&self) -> io::Result<SocketAddr> {
        self.sock.local_addr()
    }

    fn spedisci(&self, invii: &[Invio]) -> io::Result<()> {
        for i in invii {
            self.sock.send_to(&i.dati, i.verso)?;
        }
        Ok(())
    }

    /// Un giro: legge i datagrammi arrivati, rinnova la registrazione se serve, e
    /// restituisce gli eventi. `cat` risponde ai comandi CAT del telefono.
    pub fn passo(
        &mut self,
        ora: Instant,
        ora_ms: u64,
        cat: &mut dyn FnMut(&str) -> String,
    ) -> io::Result<Vec<Evento>> {
        let mut eventi = Vec::new();
        let mut buf = [0u8; 2048];
        loop {
            match self.sock.recv_from(&mut buf) {
                Ok((n, da)) => {
                    let (invii, ev) = self.gw.ricevi(&buf[..n], da, ora_ms, cat);
                    self.spedisci(&invii)?;
                    eventi.extend(ev);
                }
                Err(e) if e.kind() == io::ErrorKind::WouldBlock => break,
                Err(e) => return Err(e),
            }
        }
        let rinnovi = self.gw.tick(&self.token, ora);
        self.spedisci(&rinnovi)?;
        Ok(eventi)
    }

    /// Audio radio (48 kHz mono) da spedire.
    pub fn invia_audio(&mut self, pcm: &[i16], ora_ms: u64) -> io::Result<()> {
        let invii = self.gw.invia_audio(pcm, ora_ms);
        self.spedisci(&invii)
    }

    /// Attesa breve, per i test e per i cicli senza altro da fare.
    pub fn attesa(&self, d: Duration) {
        std::thread::sleep(d);
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn registrazione_su_socket_veri() {
        // Il "relay" e' un socket UDP che risponde REGISTER al REGISTER ricevuto.
        let relay = UdpSocket::bind("127.0.0.1:0").unwrap();
        relay.set_read_timeout(Some(Duration::from_secs(2))).unwrap();
        let relay_addr = relay.local_addr().unwrap();

        let mut col = Collegamento::apri("127.0.0.1:0", "TOKEN").unwrap();
        col.gw.imposta_destinazione(Some(relay_addr));
        let ora = Instant::now();
        let r = col.gw.registrazione("TOKEN", ora).unwrap();
        col.spedisci(&[r]).unwrap();

        let mut buf = [0u8; 256];
        let (n, da) = relay.recv_from(&mut buf).unwrap();
        assert!(buf[..n].starts_with(b"HFGW"));
        assert!(buf[..n].ends_with(b"gw TOKEN"));

        // risposta del relay: REGISTER di ritorno, con l'intestazione v2
        let ack = crate::rete::v2_pacchetto(crate::rete::v2::REGISTER, 1, 0, 48_000, &[]);
        relay.send_to(&ack, da).unwrap();

        let mut eventi = Vec::new();
        for _ in 0..50 {
            eventi.extend(col.passo(Instant::now(), 0, &mut |_| String::new()).unwrap());
            if !eventi.is_empty() {
                break;
            }
            col.attesa(Duration::from_millis(10));
        }
        assert_eq!(eventi, vec![Evento::Registrato]);
    }
}
