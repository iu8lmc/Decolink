# hf-gateway

**Radio HF via internet per Decodium FT2/FT2-Link.** Due stazioni Decodium
fanno QSO reali attraverso internet **senza dipendere dalla propagazione** —
e **senza Tailscale né tool di terzi**: usano un piccolo **server relay
self-hosted** (incluso qui) che gira su un VPS vostro (es. `decolink.ft2.it`).

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

## 1. Gateway sul VPS (una volta sola)

Il server non è più un semplice punto d'incontro: per entrare servono un accesso
approvato e un ruolo. Chi è registrato come **ascoltatore** riceve l'audio ma non
riesce a mandare la radio in trasmissione; **operatore** e **titolare** sì, e ogni
trasmissione viene registrata con nominativo, ora e indirizzo.

Sul VPS con IP pubblico (es. `decolink.ft2.it`):

```bash
sudo mkdir -p /opt/decolink
sudo cp server/decolink_*.py /opt/decolink/
sudo cp server/decolink-relay.service server/decolink-web.service /etc/systemd/system/
sudo useradd --system --home /opt/decolink --shell /usr/sbin/nologin decolink
sudo chown -R decolink:decolink /opt/decolink

sudo -u decolink python3 /opt/decolink/decolink_admin.py init   # primo accesso
sudo ufw allow 5555/udp
sudo systemctl daemon-reload
sudo systemctl enable --now decolink-relay decolink-web
```

Solo Python 3 standard (nessun pip). Il servizio web va messo dietro nginx con
HTTPS, altrimenti le password viaggiano in chiaro.

#### Avviso via email delle richieste (facoltativo)

Le richieste di accesso compaiono nella pagina della stazione, ma nessuno
avvisa il titolare: se non guarda, chi ha chiesto resta in attesa. Con queste
variabili d'ambiente parte una email a ogni richiesta:

```
DECOLINK_SMTP_HOST=smtp.esempio.it     # senza questa, non si manda nulla
DECOLINK_SMTP_PORT=587                 # 587 STARTTLS (predefinito), 465 SSL
DECOLINK_SMTP_USER=decolink@esempio.it
DECOLINK_SMTP_PASS=...
DECOLINK_SMTP_FROM=decolink@esempio.it # se manca, si usa l'utente
DECOLINK_BASE_URL=https://decolink.ft2.it   # per il link al pannello
```

Si mettono nel file del servizio (`Environment=` in `decolink-web.service`).
L'invio gira in un thread a parte e non blocca la registrazione: se il server
di posta non risponde, la richiesta viene registrata lo stesso e in log resta
la riga dell'invio fallito. Senza `DECOLINK_SMTP_HOST` tutto si comporta come
prima.

Istruzioni complete, ruoli, gestione dei membri e note di sicurezza:
**[`server/LEGGIMI.md`](server/LEGGIMI.md)**.

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
scegli input/output dalla lista, il server (`decolink.ft2.it`, invio) e il
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

## Telemetria / diagnostica QSO

Ogni 2 s il gateway mostra: `tx`/`rx` pacchetti, **perdita netta di rete**
(`loss %`, da salti nella sequenza del peer), `underrun` del jitter buffer e le
statistiche **RTT** verso il relay (ultimo / media / max / jitter).

Per registrare tutto su file e analizzare un QSO FT2-Link a posteriori:

```bash
hf-gateway --stats-log              # scrive hfgw_stats.log (CSV)
hf-gateway --stats-log qso1.csv     # nome file a scelta
```

Il CSV ha una riga ogni 2 s (`wallclock,uptime_s,peer,tx,rx,net_lost,loss_pct,`
`buf_lost,underrun,rtt_last_ms,rtt_min_ms,rtt_avg_ms,rtt_max_ms,rtt_jit_ms,`
`in_dbfs,out_dbfs`) piu un riepilogo di sessione alla chiusura (Ctrl+C).
Apribile in Excel/LibreOffice per i grafici RTT/perdita.

---

## Risoluzione problemi

| Problema | Soluzione |
|---|---|
| `[no peer]`, `rtt -1` | il gateway non raggiunge il server: verifica che `hf_relay` giri sul VPS, la porta UDP sia aperta (`ufw`), il nome server sia giusto |
| `[peer OK]` ma nessun audio | controlla i livelli `in`/`out`; su Decodium i cavi virtuali a **48000 Hz**; codice stanza identico sui due lati |
| audio a scatti / underrun | `--jitter-ms 200` (o più su collegamenti instabili) |
| Decodium non decodifica | 48 kHz su tutta la catena; livello `in` del TX a −20…−10 dBFS senza clipping |
| stanza piena | fino a 8 collegati per stazione, ma **un solo gateway**: se un altro PC è già collegato alla stessa radio, staccalo |
| `accesso in attesa di approvazione` | la registrazione c'è ma il titolare non l'ha ancora approvata dal pannello |
| `permesso revocato` a collegamento aperto | il titolare ha tolto l'accesso, oppure la stazione è stata chiusa |
| il PTT non parte, l'audio RX si sente | sei registrato come **ascoltatore**: il ruolo non permette di trasmettere |

## Protocollo

UDP, header 22 byte big-endian (`HFGW` v2: magic, versione, flags, seq,
timestamp ms, sample rate) + payload PCM int16. Flags: AUDIO, PING/PONG,
REGISTER (con il token di accesso), PEERUP, CAT richiesta/risposta, TX audio,
DENIED (rifiuto motivato).

La **v1 non è più accettata**: bastava indovinare il nome di una stanza per
entrare e trasmettere. I client vecchi ricevono un rifiuto che lo spiega e vanno
aggiornati. Dettagli in [`server/LEGGIMI.md`](server/LEGGIMI.md).

## Licenza

MIT — (c) 2026 IU8LMC. Audio: [miniaudio](https://miniaud.io) (public domain/MIT-0).
