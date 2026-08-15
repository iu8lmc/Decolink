# Le traduzioni di Decolink

Decolink parla sedici lingue. L'italiano è quello scritto nel sorgente: le
`tr("…")` in `main.cpp` contengono direttamente il testo italiano, senza chiavi
astratte in mezzo. Le altre quindici stanno nei cataloghi `.qm` che finiscono
dentro l'eseguibile, quindi copiando il solo `decolink.exe` su un'altra macchina
le traduzioni vanno con lui.

| | |
|---|---|
| Italiano | il sorgente |
| Inglese, tedesco, francese, spagnolo, portoghese, olandese, catalano, danese, ungherese, rumeno, lettone, russo, giapponese, cinese semplificato, cinese tradizionale | `decolink_<codice>.qm` |

Alla prima apertura non si chiede niente: si prende la lingua di Windows. Chi ha
il sistema in tedesco trova Decolink in tedesco. Il selettore in alto a destra
serve a cambiarla, e ogni voce è scritta nella propria lingua — chi apre il
programma in una lingua che non capisce deve poter riconoscere la sua senza
saper leggere le altre.

## Come si aggiorna una traduzione

Le traduzioni non si scrivono nei `.ts` a mano: quei file li riscrive `lupdate`
ogni volta che il sorgente cambia, e le modifiche fatte a mano sopravvivono solo
finché nessuno tocca `main.cpp`. Il testo vero sta nei tre dizionari Python, che
sono la fonte.

```
dizionario.py    etichette, voci dei menu a tendina, pulsanti
dizionario2.py   messaggi di stato (quelli che si leggono quando qualcosa non va)
dizionario3.py   i suggerimenti lunghi
```

Il giro completo, dopo aver aggiunto o cambiato una `tr()` nel sorgente:

```sh
# 1. raccoglie le stringhe nuove dal sorgente
lupdate decolink.pro

# 2. riversa i dizionari nei .ts e dice cosa manca ancora
cd traduzioni && python genera.py

# 3. i .qm li rifà da solo il build, ma volendo:
lrelease decolink_de.ts
```

`genera.py` stampa la copertura lingua per lingua e, in coda, l'elenco delle
stringhe ancora senza traduzione. Quelle vanno aggiunte a uno dei tre dizionari
e il passo 2 si ripete. Con `--stretto` esce con errore se una lingua è sotto il
90%, che è il modo di accorgersene in una build automatica invece che a video.

Quello che il dizionario non traduce resta marcato `unfinished` nel `.ts`: in Qt
Linguist si vede in rosso. Non ci si mette il testo italiano al posto della
traduzione mancante, perché poi nessuno distingue più un buco da una scelta.

Le sigle e i numeri stanno nella lista `UGUALI` di `dizionario.py` e passano
identici in tutte le lingue: `48 kHz`, `115200`, `TCP`, `RTS/CTS`. Tradurli
sarebbe un danno.

## Come si prova

```sh
decolink.exe --lingue          # controlla che i quindici cataloghi carichino e traducano
decolink.exe --lingua=de       # apre in tedesco una volta sola, senza salvare niente
```

`--lingue` esiste perché un `.qm` che non si carica non dà nessun errore:
l'interfaccia resta semplicemente in italiano, e sembra una svista invece di un
file mancante.

## Il tedesco e il layout

Il tedesco allunga le stringhe di circa un terzo rispetto all'italiano, il
cinese le dimezza. Dopo aver aggiunto etichette nuove conviene aprire una volta
con `--lingua=de` e guardare che niente venga tagliato: è la lingua che mette
alla prova i bordi.
