# hf-gateway

**Radio HF via internet per Decodium FT2/FT2-Link.** Tool standalone (un solo
eseguibile, zero dipendenze) che emula il percorso audio di una radio HF tra
due stazioni Decodium collegate via internet — per sperimentare FT2-Link
quando la propagazione non aiuta.

```
[Decodium A]                                          [Decodium B]
 TX → cavo virt. 1 → hf-gateway ══ UDP/internet ══ hf-gateway → cavo virt. 2 → RX
 RX ← cavo virt. 2 ← hf-gateway ══ UDP/internet ══ hf-gateway ← cavo virt. 1 ← TX
```

- **PCM raw 48 kHz int16 mono** (~790 kbit/s per direzione): niente codec —
  AGC/compressione dei tool voce (Discord/Zoom) distruggono i modi digitali.
- Simulazione **canale HF** opzionale: rumore AWGN, attenuazione, QSB
  (spenta di default = pass-through pulito).
- Configurazione **guidata al primo avvio** (scegli i device, inserisci l'IP
  del peer) — salvata in `hfgw.cfg`, gli avvii successivi partono da soli.
- Latenza internet (30–100 ms) irrilevante per i DT di FT2/FT2-Link.

## Download / compilazione

**Windows**: scarica `hf-gateway.exe` dalle [Releases](../../releases) —
eseguibile singolo, nessuna installazione.

**macOS** (o build da sorgente):
```bash
git clone https://github.com/iu8lmc/hf-gateway.git
cd hf-gateway
cmake -B build && cmake --build build
./build/hf-gateway
```
(serve solo Xcode command-line tools + cmake: `xcode-select --install`,
`brew install cmake`)

## Preparazione (una volta sola)

1. **Cavi audio virtuali** (2 per lato):
   - Windows: [VB-Cable A+B](https://vb-audio.com/Cable/)
   - macOS: [BlackHole 2ch](https://existential.audio/blackhole/) ×2 istanze
2. **[Tailscale](https://tailscale.com/)** su entrambi i PC (gratis): VPN
   privata con IP fissi `100.x.y.z`, senza aprire porte sul router.
3. **Decodium** (profilo dedicato consigliato): output audio TX → cavo 1,
   input audio RX ← cavo 2, CAT **None** (non serve una radio).

## Uso

Doppio click (o `./hf-gateway`). Al primo avvio:

```
=== configurazione guidata ===
Dispositivi di CATTURA (input - dove arriva il TX audio di Decodium):
  [0] CABLE-A Output (VB-Audio ...)
  ...
Scegli l'INPUT (numero): 0
Scegli l'OUTPUT (numero): 3
IP del gateway remoto (es. 100.64.1.2 di Tailscale): 100.101.102.103
Porta del peer [5550]:
Porta locale di ascolto [5550]:
```

Fatto: dagli avvii successivi parte direttamente con la config salvata
(`--reconfigure` per rifarla).

**Primo collaudo senza Decodium**: un lato lancia con `--tone-test`
(trasmette un tono a 1500 Hz), l'altro deve vedere il tono sul waterfall
di Decodium e il livello `out` salire nelle statistiche.

Le statistiche (ogni 2 s) mostrano frame tx/rx, persi, underrun, **RTT** e
livelli **in/out in dBFS**.

## Canale HF simulato (opzionale)

Applicato al segnale ricevuto; ogni lato controlla il proprio canale RX.

```bash
hf-gateway --noise-dbfs -30                 # pavimento di rumore a -30 dBFS
hf-gateway --attenuate-db 20                # segnale ricevuto -20 dB
hf-gateway --qsb-depth-db 6 --qsb-period 15 # fading 6 dB ogni 15 s
```

Combinando attenuazione e rumore si ottiene qualsiasi SNR — perfetto per
testare i rate W2300 (WEAK/DEEP/ULTRA) a condizioni controllate e ripetibili.
Per prove pulite di protocollo (QSY, BBS, mail) lasciare tutto spento.

## Risoluzione problemi

| Problema | Soluzione |
|---|---|
| `rtt -1`, `rx 0` | i pacchetti non passano: verifica firewall (UDP sulla porta di ascolto), IP peer, Tailscale attivo |
| audio a scatti / underrun | `--jitter-ms 200` (o più su collegamenti instabili) |
| Decodium non decodifica | tutta la catena a 48 kHz (pannello audio Windows: proprietà dei cavi → 48000 Hz); livello `in` del TX a −20…−10 dBFS senza clipping |
| entrambi TX insieme | collisione, realistico come in HF simplex — FT2-Link ritenta da solo |

## Protocollo

UDP, header 22 byte big-endian (`HFGW` v1: magic, versione, flags, seq,
timestamp ms, sample rate) + payload PCM int16 little-endian, frame 10 ms.
Compatibile con il tool Python `tools/hf-gateway` nel repo Decodium.

## Licenza

MIT — (c) 2026 IU8LMC. Audio: [miniaudio](https://miniaud.io) (public domain/MIT-0).
