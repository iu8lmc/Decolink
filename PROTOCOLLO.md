# Protocollo Decolink v3 — progetto

Documento di progetto, non di cronaca: descrive dove si vuole arrivare e
perché. Il protocollo in funzione oggi è la v2 (audio PCM grezzo, accesso
autenticato), descritta in [`server/LEGGIMI.md`](server/LEGGIMI.md).

## 1. Il problema, in numeri

Oggi Decolink manda 100 pacchetti al secondo da 982 byte:

```
  22 byte di header + 960 byte di PCM (480 campioni int16 a 48 kHz)
  ×100 al secondo  =  98,2 kB/s  =  786 kbit/s
  con le intestazioni IP e UDP (28 byte per pacchetto):  808 kbit/s  =  364 MB l'ora
```

Su una connessione di casa non si nota. Su dati mobili è mezzo giga per un
pomeriggio di ascolto, e su una linea lenta non ci sta.

Il consumo non nasce dal non aver scelto un codec: nasce dal **mandare 48 kHz di
banda audio per un segnale che ne occupa 2,7** in SSB, 0,2 in CW e 0,05 in FT8.
Stiamo trasportando 24 kHz di spettro per ascoltarne il 6%, con la fedeltà di un
CD applicata al fruscio di una radio.

Da qui il principio della v3:

> Non esiste un profilo giusto per tutto. Esiste il profilo giusto per **quello
> che stai facendo adesso**, negoziato all'apertura e adattato mentre la rete
> cambia.

## 2. I quattro profili

| profilo | banda audio | codifica | banda di rete | latenza | stato |
|---|---|---|---|---|---|
| `VOCE` | 6 kHz | Opus VoIP 24 kbit/s | **39,2 kbit/s** | 60–120 ms | **fatto** |
| `VOCE` rete lenta | 6 kHz | Opus 16 kbit/s | **31,2 kbit/s** | 60–120 ms | **fatto** |
| `CW` | 4 kHz | Opus 12 kbit/s | **27,2 kbit/s** | 40–80 ms | **fatto** |
| `DIGI` | 6 kHz | PCM 12 kHz lossless | ~110–150 kbit/s | 0,5–3 s | da fare |
| `EMRG` | 1,6 kHz | Codec2 700C su FreeDV | 0,7 kbit/s | 1–2 s | da fare |

I numeri dei profili già fatti sono **misurati** con `decolink.exe --codectest` su
30 secondi di parlato simulato, e comprendono l'header v3 e le intestazioni
IP/UDP. Contro gli 808 kbit/s del PCM (anch'essi con IP/UDP): **20,6× in meno**
in fonia, **29,8×** in CW.

### L'intestazione IP/UDP che nessuno conta

La prima misura ha smentito la prima stesura di questo documento, che prometteva
28 kbit/s in fonia e 15 in CW. Quei numeri contavano solo il payload UDP. Ma ogni
datagramma paga **28 byte di intestazioni IP e UDP**, e con pacchetti da 70 byte
sono il 40% del traffico:

```
  Opus 24 kbit/s, frame da 20 ms:
     60 byte di audio + 10 di header v3 + 28 di IP/UDP = 98 byte
     ×50 al secondo = 39,2 kbit/s     (il 29% non è audio)

  Opus 12 kbit/s (CW), frame da 20 ms:
     30 byte di audio + 10 + 28 = 68 byte
     ×50 al secondo = 27,2 kbit/s     (il 56% non è audio!)
```

Sotto i 20 kbit/s di codifica **l'involucro pesa più del contenuto**, e ridurre il
bitrate del codec smette di servire: da 24 a 12 kbit/s di Opus la banda vera
scende solo da 39 a 27.

La cura è mandare più frame per datagramma: con 40 ms (due frame Opus) la fonia
scende a ~31 kbit/s e il CW a ~19; con 60 ms il CW arriva a ~17. Si paga in
latenza — 40 ms in più sono accettabili in fonia, meno in CW dove il ritmo conta.
È il primo lavoro in coda dopo questo passo, ed è un guadagno del 20–35% che non
costa nulla in qualità.

### Perché i digitali restano lossless

Opus è un codec percettivo: butta via ciò che l'orecchio non sente. Su FT8 a
−24 dB di rapporto segnale/rumore, quello che l'orecchio non sente **è il
segnale**. In pratica Opus a 48 kbit/s decodifica quasi tutto, ma "quasi" è la
parola sbagliata quando si sta inseguendo una stazione al limite: il gateway non
deve essere il motivo per cui una decodifica manca.

Quindi sui digitali si comprime **senza perdere niente**: PCM a 12 kHz — che
copre l'intero passband dei modi digitali con margine — compresso con FLAC, che
sull'audio di una radio rende il 55–65%. Sono 110–150 kbit/s: cinque volte meno
di oggi, con l'audio identico bit per bit a quello che esce dal rig.

### Perché il CW ha un profilo suo

Un segnale CW sta in 200 Hz. Trasportarne 3 kHz è sprecare il 93% della banda
per sentire il rumore accanto. Il profilo `CW` filtra a 800 Hz — abbastanza per
sentire chi chiama poco fuori nota, che è ciò che serve davvero.

Per chi ha una connessione al limite è previsto `CW-KEY`, che non manda audio
affatto: il gateway riconosce l'inviluppo della nota e trasmette gli istanti di
apertura e chiusura del tasto, ~50 bit/s. Il client risintetizza una nota
pulita. Si perde il contesto (QSB, interferenze, gli altri sulla frequenza),
quindi resta un'opzione dichiarata, non un'astuzia silenziosa.

## 3. Latenza: la distinzione che cambia tutto

Le due esigenze sono incompatibili e vanno separate, non mediate.

**In fonia e CW conta la latenza.** Un ritardo sopra i 150 ms rende impossibile
il ritmo di un QSO. Quindi: nessuna ritrasmissione, buffer corto, e le perdite si
tappano con gli strumenti di Opus — FEC inband (le informazioni per ricostruire
il pacchetto precedente viaggiano dentro il successivo) e mascheramento delle
perdite. Si accetta un artefatto, non si accetta di aspettare.

**Nei modi digitali la latenza non conta affatto.** FT8 lavora a fette di 15
secondi: il decodificatore parte quando la fetta è finita. Se un pacchetto si
perde, **c'è tempo per richiederlo di nuovo** — un secondo o due di ritardo non
li nota nessuno, mentre un buco nell'audio rovina la decodifica di tutta la
fetta.

Quindi il profilo `DIGI` usa ritrasmissione selettiva: il ricevente tiene una
finestra di 3 secondi, si accorge dei numeri di sequenza mancanti e li richiede.
L'audio consegnato al decodificatore è **completo o dichiarato incompleto**, mai
silenziosamente bucato.

È la ragione per cui un flusso solo non basta e quattro profili sì: la stessa
rete, con le stesse perdite, va gestita in modo opposto a seconda del modo.

## 4. Formato dei pacchetti

L'header v2 è di 22 byte: con Opus a 24 kbit/s il payload è di 60 byte, quindi
l'intestazione peserebbe il 27% del traffico. Va ridotta.

### Header dati v3 — 10 byte

```
 byte  0     'D' (0x44)                      riconoscimento veloce
 byte  1     ver(4 bit) | tipo(4 bit)        ver=3
 byte  2     profilo(4 bit) | flag(4 bit)    flag: FEC, ultimo-di-slot, ridondante, marker
 byte  3     numero di stazione locale       distingue i flussi in una stanza
 byte  4-5   seq (u16, ricircola)            per perdite e riordino
 byte  6-9   marca temporale in campioni     u32, nell'orologio del profilo
```

Il tipo di pacchetto sostituisce i "flag" della v2 e cresce con ordine:

| tipo | nome | direzione |
|---|---|---|
| 0 | `AUDIO_RX` | gateway → operatori |
| 1 | `AUDIO_TX` | operatore → gateway |
| 2 | `CTRL` | in entrambi i versi (sottotipo nel payload) |
| 3 | `CAT` | operatore ↔ gateway |
| 4 | `NACK` | ricevente → mittente (sequenze mancanti) |
| 5 | `PING` / `PONG` | misura del percorso |

Overhead: 10 byte su 60 di payload Opus = 14%. In `DIGI`, con blocchi da 40 ms
(circa 500 byte compressi), scende al 2%.

### Perché non RTP

RTP sarebbe lo standard di settore e darebbe l'interoperabilità con Wireshark,
ffmpeg e gstreamer. Si è scelto di non adottarlo: l'header è di 12 byte contro
10, ma soprattutto RTP porta con sé aspettative — RTCP per i report, SDP per la
negoziazione, SRTP per la cifratura — e adottarne solo l'intestazione darebbe
l'apparenza della compatibilità senza la sostanza. Decolink ha già un piano di
controllo autenticato che fa quel lavoro.

Resta previsto un profilo `RTP/Opus` come uscita futura verso strumenti terzi,
dichiarato per quello che è: un ponte, non il trasporto nativo.

## 5. Negoziazione

Il profilo lo chiede **chi ascolta**, perché è chi conosce la propria rete e sa
cosa sta facendo; il gateway concede quello che sa fare.

```
  operatore → gateway   CTRL/HELLO      profili che so gestire, in ordine di preferenza
  gateway  → operatore  CTRL/OFFERTA    profili disponibili, parametri, capacità del rig
  operatore → gateway   CTRL/SCEGLI     profilo scelto + banda massima accettata
  gateway  → operatore  CTRL/ATTIVO     profilo in vigore da questa sequenza in poi
```

Un cambio di profilo a collegamento aperto è la stessa cosa: `SCEGLI` seguito da
`ATTIVO`, e il flusso cambia al pacchetto indicato senza interruzione. Passare da
fonia a FT8 non deve richiedere di staccare e riattaccare.

Il **relay non guarda dentro**. Continua a inoltrare per tipo di pacchetto e
resta trasparente al codec: aggiungere un profilo domani non richiede di
aggiornare il server, che è ciò che permette al gateway e al client di evolvere
senza fermare la stazione di nessun altro.

## 6. Adattamento

Ogni 2 secondi il ricevente manda `CTRL/REPORT`: pacchetti attesi, ricevuti,
riordinati, jitter, occupazione del buffer. Il mittente reagisce:

| condizione | reazione |
|---|---|
| perdita > 2% | attiva la FEC inband di Opus (+25% di banda) |
| perdita > 8% | scende di bitrate: 24 → 16 → 12 kbit/s |
| perdita > 20% | propone all'utente `CW-KEY` o `EMRG` |
| stabile per 30 s | risale di un gradino |
| jitter in crescita | allarga il buffer, 60 → 200 ms |

Le decisioni si scrivono nel registro della stazione: quando qualcuno dirà "si
sentiva male", ci sarà una riga che dice se era la rete e cosa ha fatto il
gateway.

## 7. Il canale d'emergenza

Quando internet non c'è — non perché manca la propagazione, ma perché è caduta
la linea — il trasporto diventa la radio stessa. Con `EMRG` il collegamento
passa su **FreeDV**: modem OFDM e voce Codec2 a 700 bit/s, entrambi già dentro
libcodec2, senza programmi di terze parti.

```
  operatore                                          stazione remota
  [Decolink] ──audio──> [radio HF QRP] ))) ((( [radio HF] <──audio── [Decolink]
              Codec2 700C + modem FreeDV OFDM, ~1 kHz occupati
```

Cosa passa, in ordine di priorità:

1. **Comandi CAT e stato** — frequenza, modo, PTT, ROS, alimentazione: decine di
   byte, che arrivano anche con propagazione mediocre.
2. **Voce digitale** a 700–1600 bit/s: intelligibile, non bella.
3. **Messaggi brevi** di servizio fra operatore e stazione.

Cosa **non** passa, e va detto subito: l'audio dei modi digitali. FT8 dentro un
canale da 700 bit/s non ci sta, e nessuna compressione lo farà entrare. In
emergenza si comanda la radio e si parla, non si fa FT8 remoto.

### Il vincolo che non si può aggirare

Serve **un secondo apparato**, da entrambi i lati. La radio che si sta
remotizzando non può fare contemporaneamente da modem per il collegamento che la
comanda: mentre trasmette i dati del link non è disponibile per operare. Chi
prevede l'uso in emergenza deve mettere in conto una seconda radio, tipicamente
un QRP su una banda diversa.

È il genere di dettaglio che in un dépliant si omette. Qui sta al punto 7 perché
chi organizza una stazione d'emergenza deve saperlo prima di contarci.

## 8. Compatibilità

La v3 **si affianca** alla v2, non la sostituisce di colpo. Il gateway annuncia
entrambe; un client v2 continua a collegarsi con PCM grezzo e riceve nel
`CTRL/OFFERTA` l'indicazione che esistono profili migliori. Il relay inoltra
entrambe le versioni, perché non guarda dentro i pacchetti.

Nessuna rottura come quella fra v1 e v2: quella era necessaria perché mancava
l'autenticazione, qui si tratta solo di efficienza, e rompere per efficienza è
un lusso che si paga in stazioni che smettono di funzionare.

## 9. Come si misura se funziona

Un progetto che si dichiara "professionale" deve dire in anticipo come verrà
smentito. Le prove:

| misura | strumento | obiettivo |
|---|---|---|
| banda reale per profilo | contatori nel client, 60 s di flusso | entro il 10% della tabella §2 |
| decodifiche FT8 conservate | 30 min di registrazione, decodifica in locale e via `DIGI` | **identiche** (il profilo è lossless) |
| intelligibilità in fonia | ascolto in doppio cieco, `VOCE` contro PCM | indistinguibile su segnali forti |
| tenuta alle perdite | perdita indotta al 5/10/20% | fonia comprensibile, `DIGI` senza buchi |
| latenza andata e ritorno | marca temporale nei PING | < 150 ms in fonia sulla stessa nazione |
| `EMRG` su canale vero | due radio, banda 40 m, sera | CAT affidabile, voce comprensibile |

Sui digitali il criterio è severo e volutamente binario: se una sola decodifica
si perde rispetto all'ascolto locale, il profilo non va bene.

## 10. Ordine dei lavori

1. ~~**Fonia con Opus**~~ — **fatto**: 39,2 kbit/s misurati, 20,6× meno del PCM.
2. ~~**Header v3 e negoziazione**~~ — **fatto**: header da 10 byte, quattro
   battute di negoziazione, la v2 continua a funzionare accanto.
3. ~~**`CW` con Opus a banda stretta**~~ — **fatto**: 27,2 kbit/s.
4. ~~**Adattamento dai report**~~ — **fatto**: la perdita segnalata regola la
   ridondanza di Opus e fa scendere il bitrate.
5. **Più frame per datagramma** — 20–35% di banda in meno senza perdere qualità,
   vedi §2. È il prossimo passo perché è il guadagno più economico che resta.
6. **`DIGI` lossless con ritrasmissione** — il profilo che deve dimostrare zero
   decodifiche perse.
7. **`CW-KEY`** — solo inviluppo del tasto, ~50 bit/s.
8. **`EMRG` su FreeDV** — per ultimo, perché richiede due radio per essere
   provato seriamente, non un banco di prova.

Ogni passo è utile da solo: fermandosi qui, la fonia consuma già venti volte
meno di prima.

## 11. Quello che questo protocollo non farà

- **Non rende riservato l'audio.** L'accesso stabilisce chi può usare la radio;
  il contenuto di un segnale che è già pubblico via etere non ha bisogno di
  essere cifrato, e fingere il contrario sarebbe teatro.
- **Non elimina la latenza della rete.** Nessun codec accorcia la distanza fisica.
- **Non fa passare i digitali via radio HF.** Vedi §7.
- **Non sostituisce la propagazione con internet, né viceversa.** Sono due
  trasporti con caratteristiche diverse: il protocollo li rende scambiabili
  quando ha senso, non equivalenti.
