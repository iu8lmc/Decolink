# hf-gateway

**Radio HF via internet per Decodium FT2/FT2-Link.** Due stazioni Decodium
fanno QSO reali attraverso internet **senza dipendere dalla propagazione** —
e **senza Tailscale né tool di terzi**: usano un piccolo **server relay
self-hosted** (incluso qui) che gira su un VPS vostro (es. `community.ft2.it`).

```
[Decodium tu]                                              [Decodium Salvatore]
 TX → cavo virt.1 → hf-gateway ─┐                     ┌─ hf-gateway → cavo virt.2 → RX
 RX ← cavo virt.2 ← hf-gateway ←┤   VPS: hf_relay.py  ├→ hf-gateway ← cavo virt.1 ← TX
                                └──── stessa STANZA ───┘
```

Entrambi i gateway **escono** verso il VPS (nessun NAT da bucare, niente porte
da aprire sui router di casa) ed entrano nella stessa *stanza* (un codice
condiviso): il server inoltra l'audio tra i due. Funziona con qualsiasi
router/provider.

- **PCM raw 48 kHz int16 mono**, frame 10 ms: niente codec — AGC/compressione
  dei tool voce distruggono i modi digitali.
- Simulazione **canale HF** opzionale (rumore/SNR, QSB, attenuazione).
- Nessuno scambio di IP: solo un **codice stanza** concordato a voce.

---

## 1. Server relay (una volta sola, sul VPS)

Sul VPS con IP pubblico (es. `community.ft2.it`):

```bash
sudo mkdir -p /opt/hf-relay
sudo cp server/hf_relay.py /opt/hf-relay/
sudo cp server/hf-relay.service /etc/systemd/system/
sudo ufw allow 5555/udp                 # apri la porta UDP sul firewall
sudo systemctl daemon-reload
sudo systemctl enable --now hf-relay
journalctl -u hf-relay -f               # log: chi entra nelle stanze
```

Solo Python 3 standard (nessun pip). Per una prova al volo, senza systemd:
`python3 server/hf_relay.py 5555`.

---

## 2. Gateway (tu e Salvatore, ognuno sul proprio PC)

### Download / compilazione
- **Windows**: scarica `hf-gateway.exe` dalle [Releases](../../releases) —
  eseguibile singolo, nessuna installazione.
- **macOS**: `git clone` poi `cmake -B build && cmake --build build`
  (serve `xcode-select --install` + `brew install cmake`).

### Cavi audio virtuali (2 per lato)
- **Windows**: [VB-Cable A+B](https://vb-audio.com/Cable/)
- **macOS**: [BlackHole 2ch](https://existential.audio/blackhole/) ×2 istanze

### Decodium (profilo dedicato consigliato)
- Output audio **TX** → cavo virtuale 1
- Input audio **RX** ← cavo virtuale 2
- CAT: **None** (non serve una radio; la frequenza è cosmetica)

### Avvio
Doppio click (o `./hf-gateway`). Al **primo avvio**, configurazione guidata:
scegli input/output dalla lista, il server (`community.ft2.it`, invio) e il
**codice stanza** — lo **stesso** su entrambe le stazioni (es.
`iu8lmc-elisir80`). Salvato in `hfgw.cfg`; gli avvii dopo partono da soli
(`--reconfigure` per rifare).

Quando il peer entra nella stessa stanza, il gateway stampa
`>>> peer connesso` e le statistiche passano a `[peer OK]`.

**Primo collaudo senza Decodium**: un lato avvia con `--tone-test`
(trasmette un tono 1500 Hz), l'altro deve vederlo sul waterfall di Decodium
e vedere `out` salire di livello.

---

## Canale HF simulato (opzionale)

Applicato al segnale ricevuto; ogni lato regola il proprio canale RX.

```bash
hf-gateway --noise-dbfs -30                  # rumore AWGN a -30 dBFS
hf-gateway --attenuate-db 20                 # segnale ricevuto -20 dB
hf-gateway --qsb-depth-db 6 --qsb-period 15  # fading 6 dB ogni 15 s
```

Combinando attenuazione e rumore ottieni qualsiasi SNR — ideale per testare i
rate W2300 (WEAK/DEEP/ULTRA) a condizioni ripetibili. Prove pulite di
protocollo (QSY, BBS, mail): lascia tutto spento.

---

## Risoluzione problemi

| Problema | Soluzione |
|---|---|
| `[no peer]`, `rtt -1` | il gateway non raggiunge il server: verifica che `hf_relay` giri sul VPS, la porta UDP sia aperta (`ufw`), il nome server sia giusto |
| `[peer OK]` ma nessun audio | controlla i livelli `in`/`out`; su Decodium i cavi virtuali a **48000 Hz**; codice stanza identico sui due lati |
| audio a scatti / underrun | `--jitter-ms 200` (o più su collegamenti instabili) |
| Decodium non decodifica | 48 kHz su tutta la catena; livello `in` del TX a −20…−10 dBFS senza clipping |
| stanza piena | il relay accoppia **2** stazioni per stanza; usate un codice diverso per un'altra coppia |

## Protocollo

UDP, header 22 byte big-endian (`HFGW` v1: magic, versione, flags, seq,
timestamp ms, sample rate) + payload PCM int16. Flags: AUDIO, PING/PONG,
REGISTER (entra in stanza), PEERUP. Compatibile col tool Python
`tools/hf-gateway` nel repo Decodium.

## Licenza

MIT — (c) 2026 IU8LMC. Audio: [miniaudio](https://miniaud.io) (public domain/MIT-0).
