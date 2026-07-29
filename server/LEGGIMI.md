# Decolink — gateway per stazioni remote ad accesso controllato

Questa cartella contiene la parte che gira sul VPS: il **servizio di accesso**
(utenti, stazioni, permessi) e il **relay** che porta audio e comandi CAT fra la
radio e chi opera da lontano.

La differenza rispetto alle versioni precedenti è che non basta più conoscere il
nome di una stanza. Per entrare serve un accesso approvato, e il ruolo assegnato
decide che cosa si può fare: chi ascolta e basta non riesce a mandare la radio in
trasmissione, nemmeno provandoci.

```
   browser  ──HTTPS──>  decolink_web  ──scrive──>  decolink.db
   (registrazione,           │                         ▲
    login, pannello)      firma i                   rilegge i
                          token                     permessi
                             ▼                         │
   Decolink  ───UDP────>  decolink_relay ───────────────┘
   Decodium Mobile        (audio + CAT)
```

Serve solo Python 3 (da 3.8 in su), nessun pacchetto da installare.

## I ruoli

| ruolo | ascolta | trasmette e comanda il rig | gestisce i membri |
|---|---|---|---|
| **titolare** | sì | sì | sì |
| **operatore** | sì | sì | no |
| **ascoltatore** | sì | **no** | no |

Il titolare è il responsabile di ciò che va in aria sotto il nominativo della
stazione. Per questo ogni trasmissione finisce nel registro con nominativo, ora e
indirizzo di chi l'ha fatta: è la traccia che permette di dire chi ha operato.

## Installazione sul VPS

Dalla cartella `server/` del repository, sul VPS:

```bash
sudo bash installa.sh
```

Lo script fa tutto: utente di sistema, copia dei file, unit systemd, apertura
della porta sul firewall e creazione del primo amministratore. Si può rieseguire
per aggiornare i file senza toccare database, utenti e chiave di firma.

Se sulla macchina gira ancora `hf-relay` (il relay senza autenticazione, che
tiene la stessa porta UDP) lo script se ne accorge e chiede se fermarlo, perché
farlo scollega chi lo sta usando in quel momento. Per affiancarlo invece di
sostituirlo: `sudo PORTA_RELAY=5556 bash installa.sh`.

### A mano, se si preferisce

```bash
sudo mkdir -p /opt/decolink
sudo cp decolink_*.py /opt/decolink/
sudo cp decolink-relay.service decolink-web.service /etc/systemd/system/
sudo useradd --system --home /opt/decolink --shell /usr/sbin/nologin decolink
sudo chown -R decolink:decolink /opt/decolink

# primo amministratore e prima stazione (interattivo)
sudo -u decolink python3 /opt/decolink/decolink_admin.py init

sudo ufw allow 5555/udp
sudo systemctl daemon-reload
sudo systemctl enable --now decolink-relay decolink-web
```

Il comando `init` crea anche `decolink.key`, la chiave con cui i token vengono
firmati. **Web e relay devono leggere lo stesso file**: se ne usassero due
diversi, ogni token risulterebbe falso e nessuno riuscirebbe a collegarsi.

### HTTPS

Il servizio web ascolta su `127.0.0.1:8080` e va messo dietro nginx con un
certificato (l'esempio è dentro `decolink-web.service`). In chiaro le password
viaggerebbero leggibili: il servizio parte lo stesso, ma lo scrive nei log a ogni
avvio.

Per una prova in rete locale, senza nginx:

```bash
python3 decolink_web.py --host 0.0.0.0 --port 8080
python3 decolink_relay.py 5555
```

e nel client si scrive `http://indirizzo:8080` (con lo schema esplicito, perché
altrimenti Decolink assume HTTPS).

## Uso quotidiano

Dal pannello web, il titolare di una stazione:

- vede le richieste di accesso in attesa e le approva;
- assegna a ciascuno il ruolo di operatore o di ascoltatore;
- toglie l'accesso a chi non deve più averlo — chi è collegato in quel momento
  cade entro pochi secondi, non alla scadenza del token;
- chiude la stazione quando la radio non è disponibile;
- consulta il registro delle trasmissioni e dei collegamenti.

Chi si registra indica il proprio nominativo e la stazione a cui chiede accesso,
poi resta in attesa: nessuno arriva alla radio da solo.

## Da terminale

Il pannello copre la gestione normale; la riga di comando serve al primo avvio e
alle emergenze.

```bash
python3 decolink_admin.py utenti --stato pending      # chi aspetta
python3 decolink_admin.py attiva  ik0aaa@esempio.it
python3 decolink_admin.py permesso ik0aaa@esempio.it prova-hf operatore
python3 decolink_admin.py sospendi ik0aaa@esempio.it  # buttalo fuori adesso
python3 decolink_admin.py log --stazione prova-hf     # chi ha trasmesso
python3 decolink_admin.py password admin@esempio.it   # password dimenticata
```

## Come funziona l'accesso

Il client manda email e password a `POST /api/login` e riceve un **token
firmato** che dice chi è, su quale stazione e con che ruolo. Da quel momento
presenta il token al relay a ogni registrazione.

Il relay controlla solo la firma, che gli costa una hash: non può interrogare il
database per ognuno dei cento pacchetti al secondo che riceve. In compenso
rilegge i permessi ogni cinque secondi, e in caso di disaccordo **vince il
database**: chi è stato sospeso o declassato se ne accorge subito, senza aspettare
la scadenza.

Il token dura un'ora e il client lo rinnova da solo. Non viene mai scritto su
disco.

### Quello che il gateway non protegge

L'audio sul canale UDP viaggia **in chiaro**, come nella versione precedente: chi
può intercettare il traffico fra client e VPS può ascoltarlo. L'autenticazione
stabilisce *chi può usare la radio*, non rende la conversazione riservata — cosa
che del resto avrebbe poco senso per un segnale che è già pubblico via etere.

Le password sul disco del server sono conservate con scrypt e salt, quindi un
furto del database non le rivela. Il file `decolink.key`, invece, va protetto come
una chiave privata: chi lo legge può fabbricarsi un token da titolare.

## Protocollo HFGW v2

Header UDP di 22 byte, big-endian: `HFGW` | versione | flag | seq | t_ms | rate,
seguito dal payload.

| flag | significato | chi lo manda |
|---|---|---|
| 0 | audio ricevuto dalla radio | il gateway → tutti |
| 1 / 2 | ping / pong | chiunque |
| 3 | registrazione: `"gw <token>"` o `"op <token>"` | chiunque entri |
| 4 | la stanza è pronta | il relay |
| 5 / 6 | comando CAT e risposta | operatori ↔ gateway |
| 7 | audio da trasmettere | un operatore per volta → gateway |
| 8 | rifiuto, col motivo in chiaro | il relay |

La v1 non è più accettata: chi si presenta con la vecchia versione riceve un
rifiuto che glielo dice, invece di restare a bussare senza capire.

Un solo gateway per stazione (una radio sola non può avere due sorgenti audio) e
un solo trasmittente per volta: se due operatori premono il PTT insieme, passa il
primo e il secondo viene ignorato finché il canale non si libera.
