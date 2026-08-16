#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decolink_web.py — servizio di accesso del gateway: registrazione, login,
pannello di gestione e API per i client.

E' il "piano di controllo": qui si decide chi puo' collegarsi e con quali
poteri. Il traffico audio non passa da qui — quello resta sul relay UDP, che si
limita a controllare la firma dei token emessi da questo servizio.

    browser  ──HTTP──>  decolink_web  ──scrive──>  decolink.db
                             │                          ▲
                          firma                      rilegge
                          token                     i permessi
                             ▼                          │
    client   ──UDP───>     hf_relay  ────────────────────┘

Uso:
    python3 decolink_web.py [--port 8080] [--host 0.0.0.0]
                            [--cert cert.pem --key key.pem]

TLS: se non si passano cert e key il servizio parla HTTP in chiaro, e va messo
dietro a nginx (o simile) che si occupa di HTTPS. In chiaro e senza reverse
proxy le password viaggerebbero leggibili: il servizio parte lo stesso ma lo
dice a schermo, perche' su una rete locale di prova e' legittimo e altrove no.

Solo libreria standard Python 3.
"""

from __future__ import annotations   # annotazioni come testo: gira anche su Python 3.8

import argparse
import hashlib
import hmac
import html
import json
import os
import re
import secrets
import ssl
import sys
import threading
import time
import urllib.parse
import urllib.request      # serve a chiedere a GitHub qual e' l'ultima release

import traduzioni_sito_fine as ts   # i testi della prima pagina, in sedici lingue
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import decolink_db as db
import decolink_mail as mail
import decolink_token as tok

HERE = os.path.dirname(os.path.abspath(__file__))
SECRET_PATH = os.environ.get("DECOLINK_SECRET") or os.path.join(HERE, "decolink.key")

COOKIE = "dl_session"

# Un token per il relay dura poco: il client lo rinnova da solo quando serve, e
# se nel frattempo qualcuno perde i permessi il danno e' limitato a questo.
API_TOKEN_TTL = 3600

# La chiave di stazione dura trenta giorni: serve ai programmi che non sanno fare
# il login e hanno un solo campo di testo dove incollarla, quindi nessuno puo'
# rinnovarla ogni ora. Resta un token firmato come gli altri — stesso ruolo,
# stessi log, e smette di funzionare entro pochi secondi se si toglie il permesso
# a chi l'ha chiesta.
CHIAVE_TTL = 30 * 24 * 3600

# Freno ai tentativi di login: non e' un antifurto, ma trasforma un attacco a
# dizionario in qualcosa che richiede mesi invece di minuti.
LOGIN_MAX_TRIES = 8
LOGIN_WINDOW = 300.0

_tries: dict = {}     # ip -> [(istante, ...)]

RE_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
RE_CALL = re.compile(r"^[A-Z0-9/]{3,16}$")
RE_SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{1,30}$")

RUOLI_IT = {tok.ROLE_OWNER: "titolare", tok.ROLE_OPERATOR: "operatore",
            tok.ROLE_LISTENER: "ascoltatore"}
STATI_IT = {db.ST_PENDING: "in attesa", db.ST_ACTIVE: "attivo",
            db.ST_SUSPENDED: "sospeso"}

# Tema in linea con gli altri siti FT2 (community.ft2.it): fondo blu notte,
# ciano come accento e verde acqua per le conferme. Gli stessi colori dell'icona
# di Decolink, cosi' il client e il sito si riconoscono come la stessa cosa.
CSS = """
:root {
  color-scheme: dark;
  --fondo:#08111f; --fondo2:#0b1018; --notte:#16213e; --notte2:#1d2c56;
  --bordo:#243b63; --ciano:#00e5ff; --acqua:#36d8ad;
  --testo:#e8edf5; --tenue:#8fb3d9; --giallo:#ffd43b; --rosso:#ff6b6b;
}
* { box-sizing: border-box }
body { margin:0; background:var(--fondo); color:var(--testo);
       font:15px/1.55 system-ui,"Segoe UI","Helvetica Neue",Roboto,sans-serif }
a { color:var(--ciano); text-decoration:none } a:hover { text-decoration:underline }

header { background:linear-gradient(90deg,#0b1018 0%,#16213e 55%,#1d2c56 100%);
         border-bottom:1px solid var(--bordo); padding:14px 22px;
         display:flex; align-items:center; gap:18px; flex-wrap:wrap }
header .logo { font-weight:800; letter-spacing:1.2px; font-size:17px;
               background:linear-gradient(90deg,var(--ciano),var(--acqua));
               -webkit-background-clip:text; background-clip:text; color:transparent }
/* Il logo e' un collegamento alla prima pagina, ma resta scritto col gradiente:
   senza questa riga header a:hover vince per specificita' e lo appiattisce. */
header a.logo:hover { color:transparent }
header .sp { flex:1 }
header a { color:var(--tenue) } header a:hover { color:var(--ciano); text-decoration:none }

main { max-width:960px; margin:0 auto; padding:22px }
h1 { font-size:22px; margin:0 0 4px; letter-spacing:.2px }
h2 { font-size:17px; margin:28px 0 10px; color:var(--tenue); font-weight:600 }
.sub { color:var(--tenue); margin:0 0 20px }
.card { background:rgba(22,33,62,.45); border:1px solid var(--bordo); border-radius:12px;
        padding:18px; margin-bottom:18px }

label { display:block; margin:12px 0 5px; color:var(--tenue); font-size:13px }
input,select { width:100%; padding:10px 12px; background:var(--fondo2); color:var(--testo);
               border:1px solid var(--bordo); border-radius:8px; font-size:15px }
input:focus,select:focus { outline:none; border-color:var(--ciano);
                           box-shadow:0 0 0 3px rgba(0,229,255,.13) }
button { background:linear-gradient(90deg,var(--ciano),var(--acqua)); color:#06131c; border:0;
         border-radius:8px; padding:10px 18px; font-size:15px; font-weight:700;
         cursor:pointer; margin-top:14px; letter-spacing:.2px }
button:hover { filter:brightness(1.12) }
button.ghost { background:transparent; color:var(--tenue); border:1px solid var(--bordo);
               font-weight:500 }
button.ghost:hover { color:var(--ciano); border-color:var(--ciano); filter:none }
button.danger { background:#c9553f; color:#fff }
button.small { padding:6px 11px; font-size:13px; margin:0 }

table { width:100%; border-collapse:collapse; margin-top:8px }
th,td { text-align:left; padding:9px 10px; border-bottom:1px solid rgba(36,59,99,.7); font-size:14px }
th { color:var(--tenue); font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:.5px }
.tag { display:inline-block; padding:2px 9px; border-radius:20px; font-size:12px; font-weight:600 }
.own { background:rgba(0,229,255,.15); color:#7fe9ff }
.opr { background:rgba(54,216,173,.16); color:#6ee7bf }
.lst { background:rgba(143,179,217,.14); color:#a9c4e0 }
.pending { background:rgba(255,212,59,.14); color:var(--giallo) }
.active { background:rgba(54,216,173,.16); color:#6ee7bf }
.suspended { background:rgba(255,107,107,.15); color:var(--rosso) }

.msg { padding:11px 14px; border-radius:8px; margin-bottom:16px }
.err { background:rgba(255,107,107,.1); border:1px solid rgba(255,107,107,.4); color:#ffb4b4 }
.ok  { background:rgba(54,216,173,.1); border:1px solid rgba(54,216,173,.4); color:#8fe8cd }
.mono { font-family:Consolas,ui-monospace,monospace; font-size:13px; word-break:break-all;
        background:var(--fondo2); padding:10px; border-radius:8px; border:1px solid var(--bordo);
        color:#9fe9ff }
.inline { display:inline } .row { display:flex; gap:8px; align-items:center; flex-wrap:wrap }
footer { color:#5d7ba3; font-size:12px; text-align:center; padding:26px }
footer a { color:#5d7ba3 }

/* pagina di scaricamento */
.hero { text-align:center; padding:14px 0 6px }
.hero h1 { font-size:30px; margin-bottom:8px }
.hero .sub { font-size:16px; max-width:620px; margin:0 auto 22px }
.scarica { display:inline-block; background:linear-gradient(90deg,var(--ciano),var(--acqua));
           color:#06131c; font-weight:800; font-size:17px; padding:14px 30px; border-radius:10px }
.scarica:hover { filter:brightness(1.12); text-decoration:none }
.riquadri { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:14px }
.passo { display:flex; gap:12px; margin-bottom:14px }
.passo .n { flex:0 0 26px; height:26px; border-radius:50%; background:rgba(0,229,255,.15);
            color:var(--ciano); font-weight:700; font-size:13px; display:flex;
            align-items:center; justify-content:center }

/* Striscia di scaricamento in cima a ogni pagina. Una riga sola: deve dire
   dove si prende il client senza rubare la pagina a quello che c'e' sotto. */
.banner { display:flex; align-items:center; gap:14px; flex-wrap:wrap;
          background:linear-gradient(90deg,rgba(0,229,255,.10),rgba(54,216,173,.07));
          border:1px solid rgba(0,229,255,.3); border-radius:10px;
          padding:11px 16px; margin-bottom:18px }
.banner .gh { flex:0 0 auto; width:22px; height:22px; fill:var(--ciano) }
.banner .testo { flex:1 1 220px; font-size:14px; color:#c9d8ea; line-height:1.45 }
.banner .testo b { color:#e8edf5 }
.banner .ver { color:var(--ciano); font-weight:700 }
.banner .vai { flex:0 0 auto; background:linear-gradient(90deg,var(--ciano),var(--acqua));
               color:#06131c; font-weight:700; font-size:14px; padding:9px 18px;
               border-radius:8px; white-space:nowrap }
.banner .vai:hover { filter:brightness(1.12); text-decoration:none }
@media (max-width:520px) { .banner .vai { width:100% ; text-align:center } }

/* Selettore delle lingue: un <details>, cosi' non serve JavaScript. */
.lingue { position:relative; display:inline-block }
.lingue summary { list-style:none; cursor:pointer; color:#8fb3d9; font-size:13px;
                  padding:5px 10px; border:1px solid var(--bordo); border-radius:7px;
                  white-space:nowrap }
.lingue summary::-webkit-details-marker { display:none }
.lingue summary::after { content:" ▾"; color:#5d7ba3 }
.lingue summary:hover { border-color:var(--ciano); color:#e8edf5 }
.lingue .tendina { position:absolute; right:0; top:calc(100% + 6px); z-index:20;
                   background:var(--fondo2); border:1px solid var(--bordo);
                   border-radius:9px; padding:6px; min-width:170px;
                   box-shadow:0 12px 30px rgba(0,0,0,.5);
                   display:grid; grid-template-columns:1fr 1fr; gap:2px }
.lingue .tendina a { display:block; padding:6px 9px; border-radius:6px; font-size:13px;
                     color:#c9d8ea; white-space:nowrap }
.lingue .tendina a:hover { background:rgba(0,229,255,.12); text-decoration:none }
.lingue .tendina a.qui { color:var(--ciano); font-weight:700 }

/* Prima pagina */
.prima h1 { font-size:34px; line-height:1.2; margin-bottom:10px }
.prima .claim { font-size:17px; max-width:660px; margin:0 auto 24px; color:#c9d8ea }
.prima .sotto-btn { margin-top:12px; font-size:14px; color:#8fb3d9 }
.prima .gia { margin-top:18px; font-size:14px; color:#8fb3d9 }
.modi { display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:14px }
.modi .card b { color:var(--ciano) }
h2 { font-size:19px; margin:30px 0 12px }
"""


# Da dove si prende il client. Il file non viene copiato sul VPS: la pagina
# mostra il collegamento all'ultima release e il browser scarica da GitHub, che
# ha la banda per farlo e tiene il conto degli scaricamenti.
GITHUB_REPO = os.environ.get("DECOLINK_REPO", "iu8lmc/Decolink")
RELEASE_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
RELEASE_PAGINA = f"https://github.com/{GITHUB_REPO}/releases/latest"
RELEASE_CACHE_TTL = 900.0     # 15 min: GitHub concede 60 richieste l'ora per indirizzo

_release_cache: dict = {"quando": 0.0, "dati": None}


def ultima_release() -> dict | None:
    """L'ultima release pubblicata su GitHub, o None se non si riesce a saperlo.

    Il risultato si tiene in memoria per un quarto d'ora: senza cache, una
    pagina condivisa in chat brucerebbe il limite di richieste di GitHub in
    pochi minuti e resterebbe senza collegamenti proprio quando serve.
    """
    ora = time.time()
    if _release_cache["dati"] is not None and ora - _release_cache["quando"] < RELEASE_CACHE_TTL:
        return _release_cache["dati"]

    try:
        req = urllib.request.Request(RELEASE_API, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Decolink-gateway",
        })
        with urllib.request.urlopen(req, timeout=6) as r:
            grezzo = json.loads(r.read().decode("utf-8"))
        dati = {
            "tag": str(grezzo.get("tag_name", "")),
            "nome": str(grezzo.get("name", "")),
            "data": str(grezzo.get("published_at", ""))[:10],
            "pagina": str(grezzo.get("html_url", RELEASE_PAGINA)),
            "note": str(grezzo.get("body", ""))[:1200],
            "file": [{
                "nome": str(a.get("name", "")),
                "url": str(a.get("browser_download_url", "")),
                "mb": round(int(a.get("size", 0)) / 1048576.0, 1),
                "conta": int(a.get("download_count", 0)),
            } for a in grezzo.get("assets", []) if a.get("browser_download_url")],
        }
        _release_cache.update(quando=ora, dati=dati)
        return dati
    except Exception as ex:
        # Non e' un errore da mostrare: la pagina funziona comunque, con il
        # collegamento diretto a GitHub invece del pulsante preciso.
        print(f"  [attenzione] release non leggibile da GitHub: {ex}")
        _release_cache.update(quando=ora - RELEASE_CACHE_TTL + 60, dati=None)
        return None


# Durata di un collegamento per rimettere la password: un'ora. Il gettone non si
# conserva da nessuna parte, perche' contiene al proprio interno l'impronta della
# password attuale: appena la password cambia, il collegamento smette di valere.
# Cosi' non serve una tabella da svuotare, e un collegamento gia' usato non si
# puo' riusare.
RESET_TTL = 3600


def gettone_reset(utente, scade: int) -> str:
    corpo = f"{utente['id']}:{utente['email']}:{utente['pwd']}:{scade}"
    firma = hmac.new(SECRET, corpo.encode("utf-8"), hashlib.sha256).hexdigest()[:32]
    return f"{utente['id']}-{scade}-{firma}"


def utente_da_gettone(conn, gettone: str):
    """L'utente a cui appartiene il collegamento, o None se non vale (piu')."""
    try:
        uid, scade, firma = gettone.split("-", 2)
        uid, scade = int(uid), int(scade)
    except Exception:
        return None
    if scade < time.time():
        return None
    u = db.user_by_id(conn, uid)
    if not u:
        return None
    atteso = gettone_reset(u, scade).split("-", 2)[2]
    return u if secrets.compare_digest(atteso, firma) else None


def e(s) -> str:
    """Testo pronto per finire dentro l'HTML. Ogni valore che arriva da un
    utente passa di qui: e' l'unica difesa contro chi si registra con un
    nominativo pieno di tag."""
    return html.escape("" if s is None else str(s), quote=True)


# Gettone anti-CSRF della richiesta in corso. Sta in un contenitore per thread
# perche' il server ne serve piu' d'una insieme, e due utenti diversi non devono
# mai vedersi scambiare il proprio.
#
# Serve perche' l'intestazione della pagina contiene il pulsante "esci", che e'
# una POST come le altre e quindi deve portare il gettone. Senza, l'uscita veniva
# respinta come "richiesta non valida": il difetto stava proprio nel punto in cui
# nessuno guarda, perche' l'intestazione la si costruisce una volta e poi la si
# dimentica.
_richiesta = threading.local()


# Il logo di GitHub disegnato dentro la pagina invece che preso da un CDN: e' una
# richiesta in meno, e la striscia non resta monca se il CDN non risponde.
GITHUB_SVG = ('<svg class="gh" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 '
              '3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01'
              '.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08'
              '.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-'
              '3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32'
              '-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82'
              '1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 '
              '2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>')


COOKIE_LINGUA = "dl_lang"


def menu_lingue(codice: str, percorso: str) -> str:
    """Il selettore delle lingue, in HTML e basta.

    Un <details> invece di un <select> con JavaScript: si apre e si chiude da
    solo, funziona anche a script spenti, e ogni voce e' un collegamento vero
    che si puo' condividere. Ogni lingua e' scritta nella propria lingua,
    perche' chi arriva su una pagina che non capisce deve poter riconoscere la
    sua senza saper leggere le altre.
    """
    corrente = dict(ts.LINGUE).get(codice, codice)
    voci = "".join(
        f'<a href="{e(percorso)}?lang={c}"{" class=\'qui\'" if c == codice else ""}>{e(n)}</a>'
        for c, n in ts.LINGUE)
    return (f'<details class="lingue"><summary>{e(corrente)}</summary>'
            f'<div class="tendina">{voci}</div></details>')


def banner_scarica() -> str:
    """La striscia che dice dove si prende il client.

    Sta in cima a tutte le pagine tranne quella di scaricamento, dove
    ripeterebbe quello che c'e' gia' scritto sotto in grande.

    La versione viene da GitHub: se non risponde, la striscia resta e manda alla
    pagina delle release senza dichiarare un numero. Meglio nessun numero che un
    numero vecchio: chi legge "v2.1.0" scarica quella e non sa di aver perso
    l'ultima.
    """
    rel = ultima_release()
    if rel and rel["file"]:
        def peso(f):
            n = f["nome"].lower()
            return (0 if ("win" in n or n.endswith(".zip") or n.endswith(".exe")) else 1, n)
        principale = sorted(rel["file"], key=peso)[0]
        testo = (f'<b>Decolink <span class="ver">{e(rel["tag"])}</span></b> per Windows — '
                 f'{principale["mb"]} MB, si scompatta e si avvia.')
        dove = e(principale["url"])
        etichetta = "Scarica da GitHub"
    else:
        testo = '<b>Decolink per Windows</b> — le versioni sono su GitHub.'
        dove = e(RELEASE_PAGINA)
        etichetta = "Vai su GitHub"
    return (f'<div class="banner">{GITHUB_SVG}<div class="testo">{testo}</div>'
            f'<a class="vai" href="{dove}">{etichetta}</a></div>')



# Informativa privacy dell'app Decodium Mobile (pacchetto it.ft2.decodium).
# Il Play Store esige un indirizzo pubblico che elenchi i dati trattati
# dall'APP: quella di ft2.it riguarda il sito e il forum, e non basta.
# Il testo sorgente sta in decodium-mobile/store/privacy-policy.html: se si
# cambia li', va riportato anche qui.
PRIVACY_APP = """<h1>Decodium 4 — Informativa sulla privacy</h1>
<p class="data">In vigore dal 14 agosto 2026 · applicazione Android <code>it.ft2.decodium</code></p>

<p>Decodium 4 è un'applicazione per radioamatori: decodifica e trasmette i modi
digitali FT8, FT4 e FT2 e comanda una radio via CAT. Questa informativa spiega
quali dati tratta, dove finiscono e cosa puoi decidere tu.</p>

<p>In sintesi: <strong>non c'è pubblicità, non c'è analitica, non c'è
profilazione</strong> e non viene usato alcun identificativo pubblicitario. I dati
restano sul telefono, tranne quelli che tu scegli di mandare in aria o alle reti
radioamatoriali — e tranne quelli dell'account, se decidi di usare il
collegamento remoto.</p>

<h2>L'account per il collegamento remoto</h2>

<p>Per operare da remoto — cioè con il telefono fuori casa, anche su dati mobili —
serve un account sul servizio <strong>decolink.ft2.it</strong>, che è gestito da
chi sviluppa questa app. È l'unico caso in cui dei tuoi dati arrivano a noi.</p>

<p>La registrazione avviene dal browser su
<code>https://decolink.ft2.it/registrati</code> e raccoglie:</p>

<ul>
  <li><strong>indirizzo email</strong> — identifica l'account e serve per accedere;</li>
  <li><strong>password</strong> — conservata sul server in forma cifrata, mai in chiaro;</li>
  <li><strong>nominativo radioamatoriale e stazione</strong> — servono al titolare
      della stazione per decidere se autorizzarti, e per stabilire il tuo ruolo
      (per esempio "solo ascolto").</li>
</ul>

<p>La richiesta resta in attesa finché il titolare della stazione non la approva:
l'approvazione è una scelta sua, non automatica. Il server conserva questi dati
per tutto il tempo in cui l'account esiste, li usa solo per far funzionare il
collegamento e <strong>non li cede a nessuno</strong>. Puoi chiederne in qualsiasi
momento la cancellazione scrivendo all'indirizzo in fondo.</p>

<p><strong>Questo account non serve se operi in rete locale.</strong> Con il
telefono sulla stessa rete WiFi del computer non c'è alcuna registrazione e
nessun dato esce da casa tua: è la modalità che consigliamo a chi non ha bisogno
di collegarsi da fuori.</p>

<h2>Dati trattati e dove restano</h2>

<table>
<tr><th>Dato</th><th>A cosa serve</th><th>Dove va</th></tr>

<tr>
  <td>Nominativo e locatore che inserisci</td>
  <td>Costruire i messaggi radio: senza di essi non si può operare</td>
  <td>Trasmessi <strong>via radio</strong>, quindi pubblici per natura. Inviati
      anche alle reti radioamatoriali elencate sotto, se attivi quelle funzioni</td>
</tr>

<tr>
  <td>Microfono</td>
  <td>Solo per la trasmissione in fonia, mentre tieni premuto il tasto</td>
  <td>Trasmesso in tempo reale alla radio. <strong>Non viene registrato</strong>
      né conservato né inviato allo sviluppatore. Il permesso viene chiesto al
      primo uso della fonia, non all'avvio: chi ascolta soltanto non se lo vede
      mai chiedere</td>
</tr>

<tr>
  <td>Registro dei collegamenti (log ADIF)</td>
  <td>Tenere memoria dei QSO</td>
  <td>Resta sul telefono</td>
</tr>

<tr>
  <td>Credenziali dell'account Decolink</td>
  <td>Accedere al relay per operare da remoto</td>
  <td>Sul telefono restano <strong>solo se lo chiedi</strong> ("ricordami"), nel
      portachiavi cifrato di Android. Vengono inviate a decolink.ft2.it per
      l'accesso, che rilascia un permesso temporaneo rinnovato ogni ora</td>
</tr>

<tr>
  <td>Impostazioni dell'app</td>
  <td>Ritrovare la configurazione</td>
  <td>Restano sul telefono</td>
</tr>
</table>

<h2>Servizi di terze parti</h2>

<p>Sono tutti servizi del mondo radioamatoriale, e ciascuno entra in funzione
solo se lo usi o lo attivi:</p>

<ul>
  <li><strong>PSK Reporter</strong> — se attivi l'invio dei rapporti di ricezione,
      l'app pubblica quali stazioni hai ricevuto, con nominativo, locatore,
      frequenza e orario. È una rete pubblica di propagazione: quei dati diventano
      consultabili da chiunque.</li>
  <li><strong>Cluster DX</strong> — il collegamento avviene con il tuo nominativo,
      come da prassi del servizio.</li>
  <li><strong>QRZ</strong> — consultato per risalire ai dati pubblici di un
      nominativo. Se attivi il logbook QRZ, i collegamenti che chiudi vengono
      caricati sul tuo diario di stazione, usando la chiave che inserisci tu.</li>
  <li><strong>Cloudlog</strong> — stesso discorso del logbook QRZ, verso
      l'indirizzo del tuo Cloudlog: sale lo stesso collegamento che finisce nel
      file locale, e l'indirizzo e la chiave li fornisci tu. Se non li inserisci,
      l'app non contatta nessun diario online.</li>
  <li><strong>Relay Decolink</strong> (<code>decolink.ft2.it</code>, oppure un
      server tuo se ne ospiti uno) — trasporta audio e comandi fra telefono e
      radio quando operi da remoto. Non è un terzo: è il servizio di chi
      sviluppa l'app, e i dati dell'account sono descritti sopra.</li>
  <li><strong>Server NTP</strong> — per l'orario preciso, indispensabile ai modi
      digitali. Non viene inviato alcun dato personale.</li>
</ul>

<p>Questi servizi sono gestiti da terzi e hanno regole proprie: se li usi, valgono
anche le loro condizioni.</p>

<h2>Quello che l'app NON fa</h2>
<ul>
  <li>Non usa la posizione del telefono: nessun permesso di localizzazione. Il
      locatore è quello che digiti tu.</li>
  <li>Non usa la fotocamera, e il permesso non viene nemmeno chiesto: lo
      dichiarava il componente multimediale su cui l'app è costruita, ed è stato
      tolto dal pacchetto perché nessuna funzione lo utilizza.</li>
  <li>Non contiene pubblicità né strumenti di analisi o tracciamento.</li>
  <li>Non condivide né vende dati a nessuno.</li>
</ul>

<h2>Conservazione e cancellazione</h2>
<p>I dati stanno sul tuo dispositivo: disinstallando l'app spariscono con essa,
tranne i file che hai esportato di tua iniziativa (per esempio il log ADIF). Quanto
è già stato pubblicato sulle reti radioamatoriali segue le regole di quei servizi,
ai quali devi rivolgerti direttamente.</p>

<h2>Minori</h2>
<p>L'app si rivolge ai radioamatori titolari di licenza e non è progettata per i
minori di 13 anni.</p>

<h2>Modifiche</h2>
<p>Se questa informativa cambierà, la data in cima verrà aggiornata e la versione
corrente resterà sempre a questo indirizzo.</p>

<h2>Titolare del trattamento e contatti</h2>
<p>Titolare del trattamento: <strong>Martino Merola (IU8LMC)</strong>, lo stesso
indicato nell'informativa del sito <a href="https://www.ft2.it/privacy">ft2.it</a>,
che riguarda invece il sito web e il forum.</p>
<p>Per qualunque domanda, o per esercitare i diritti previsti dal GDPR (accesso,
rettifica, cancellazione, opposizione): <strong>iu8lmc@gmail.com</strong></p>"""

def page(titolo: str, corpo: str, utente=None, msg: str = "", errore: str = "",
         banner: bool = True, lingua: str = "", percorso: str = "") -> bytes:
    nav = '<a href="/scarica">scarica il client</a>'
    if utente:
        csrf = getattr(_richiesta, "csrf", "")
        nav = (f'<span>{e(utente["callsign"])}</span>'
               f'<a href="/">stazioni</a>' + nav)
        if utente["is_admin"]:
            nav += '<a href="/admin">amministrazione</a>'
        nav += '<a href="/password">il tuo accesso</a>'
        nav += ('<form method="post" action="/esci" class="inline">'
                f'<input type="hidden" name="csrf" value="{e(csrf)}">'
                '<button class="ghost small">esci</button></form>')
    avviso = ""
    if errore:
        avviso += f'<div class="msg err">{e(errore)}</div>'
    if msg:
        avviso += f'<div class="msg ok">{e(msg)}</div>'
    striscia = banner_scarica() if banner else ""
    # Il selettore compare solo dove la pagina e' davvero tradotta: metterlo sul
    # pannello prometterebbe un tedesco che li' non c'e'.
    if lingua:
        nav += menu_lingue(lingua, percorso or "/")
    lang_html = ts.testi(lingua)["html"] if lingua else "it"
    doc = f"""<!doctype html><html lang="{lang_html}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titolo)} — Decolink</title><style>{CSS}</style></head><body>
<header><a href="/" class="logo">DECOLINK</a><span class="sp"></span>{nav}</header>
<main>{striscia}{avviso}{corpo}</main>
<footer>Decolink — gateway radio ad accesso controllato</footer></body></html>"""
    return doc.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "Decolink"
    sys_version = ""

    # ------------------------------------------------------------ utilita'

    def log_message(self, fmt, *a):   # una riga per richiesta, non tre
        sys.stdout.write("  %s %s\n" % (self.address_string(), fmt % a))

    def _client_ip(self) -> str:
        # Dietro nginx l'indirizzo del socket e' sempre 127.0.0.1: senza questo
        # il freno ai login varrebbe per tutti insieme invece che per chi bussa.
        fwd = self.headers.get("X-Forwarded-For", "")
        return fwd.split(",")[0].strip() if fwd else self.client_address[0]

    def _send(self, code: int, body: bytes, ctype="text/html; charset=utf-8", extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        # Il pannello non ha nulla da mostrare dentro una cornice altrui, e
        # vietarlo chiude la porta al clickjacking sui pulsanti di revoca.
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        for k, v in (extra or []):
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, code: int, obj: dict):
        self._send(code, json.dumps(obj).encode("utf-8"), "application/json; charset=utf-8")

    def _redirect(self, dove: str, extra=None):
        self.send_response(303)
        self.send_header("Location", dove)
        for k, v in (extra or []):
            self.send_header(k, v)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > 1 << 20:
            return {}
        raw = self.rfile.read(n)
        ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip()
        if ctype == "application/json":
            try:
                d = json.loads(raw)
                return d if isinstance(d, dict) else {}
            except Exception:
                return {}
        return {k: v[0] for k, v in urllib.parse.parse_qs(raw.decode("utf-8", "ignore")).items()}

    def _cookie(self, nome: str) -> str:
        for pezzo in (self.headers.get("Cookie") or "").split(";"):
            k, _, v = pezzo.strip().partition("=")
            if k == nome:
                return v
        return ""

    def _utente(self, conn):
        return db.web_session_user(conn, self._cookie(COOKIE))

    def _csrf(self, conn, utente) -> str:
        """Gettone anti-CSRF derivato dalla sessione.

        Senza, basterebbe una pagina qualsiasi con un form nascosto per far
        revocare a un titolare i propri operatori mentre e' collegato al
        pannello.
        """
        import hashlib
        seme = self._cookie(COOKIE) + str(utente["id"])
        return hashlib.sha256((seme + SECRET.hex()).encode()).hexdigest()[:32]

    def _arma_csrf(self, conn, utente) -> None:
        """Mette il gettone a disposizione di page(), che costruisce il pulsante
        di uscita. Va chiamato appena si sa chi e' l'utente, prima di produrre
        qualunque pagina."""
        _richiesta.csrf = self._csrf(conn, utente) if utente else ""

    def _csrf_ok(self, conn, utente, dati) -> bool:
        atteso = self._csrf(conn, utente)
        return secrets.compare_digest(atteso, str(dati.get("csrf", "")))

    def _freno(self) -> bool:
        """True se questo indirizzo ha esagerato con i tentativi di login."""
        ip, ora = self._client_ip(), time.time()
        recenti = [t for t in _tries.get(ip, []) if ora - t < LOGIN_WINDOW]
        _tries[ip] = recenti
        return len(recenti) >= LOGIN_MAX_TRIES

    def _segna_tentativo(self):
        _tries.setdefault(self._client_ip(), []).append(time.time())

    # -------------------------------------------------------------- rotte

    def do_GET(self):
        percorso = urllib.parse.urlparse(self.path).path.rstrip("/") or "/"
        conn = db.connect(DB_PATH)
        try:
            utente = self._utente(conn)
            self._arma_csrf(conn, utente)
            if percorso == "/":
                return self.pagina_home(conn, utente)
            if percorso == "/accedi":
                return self._send(200, self.form_accesso())
            if percorso == "/registrati":
                return self._send(200, self.form_registrazione(conn))
            if percorso == "/privacy":
                return self._send(200, page("privacy", PRIVACY_APP, utente,
                                            banner=False))
            if percorso in ("/scarica", "/download"):
                return self.pagina_scarica(conn, utente)
            if percorso == "/password":
                return self.pagina_password(conn, utente)
            if percorso == "/recupera":
                return self.pagina_recupera(conn)
            if percorso == "/reimposta":
                q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                return self.pagina_reimposta(conn, (q.get("t") or [""])[0])
            if percorso == "/admin":
                return self.pagina_admin(conn, utente)
            if percorso.startswith("/stazione/"):
                return self.pagina_stazione(conn, utente, percorso.split("/")[2])
            if percorso == "/api/stazioni":
                return self.api_stazioni(conn)
            self._send(404, page("non trovata", "<h1>Pagina inesistente</h1>", utente))
        finally:
            conn.close()

    def do_POST(self):
        percorso = urllib.parse.urlparse(self.path).path.rstrip("/") or "/"
        conn = db.connect(DB_PATH)
        try:
            dati = self._body()
            if percorso == "/api/login":
                return self.api_login(conn, dati)
            if percorso == "/accedi":
                return self.post_accesso(conn, dati)
            if percorso == "/registrati":
                return self.post_registrazione(conn, dati)
            # Recupero e reimpostazione stanno fuori dal controllo anti-CSRF
            # perche' chi li usa non e' collegato e un gettone non ce l'ha: al
            # loro posto valgono il freno sui tentativi e il collegamento firmato.
            if percorso == "/recupera":
                return self.post_recupera(conn, dati)
            if percorso == "/reimposta":
                return self.post_reimposta(conn, dati)

            utente = self._utente(conn)
            self._arma_csrf(conn, utente)
            if not utente:
                return self._redirect("/accedi")
            if not self._csrf_ok(conn, utente, dati):
                return self._send(400, page("errore", "<h1>Richiesta non valida</h1>"
                                            "<p class='sub'>Ricarica la pagina e riprova.</p>", utente))
            if percorso == "/esci":
                db.drop_web_session(conn, self._cookie(COOKIE))
                return self._redirect("/accedi", [("Set-Cookie", f"{COOKIE}=; Max-Age=0; Path=/")])
            if percorso == "/elimina-accesso":
                return self.post_elimina_accesso(conn, utente, dati)
            if percorso == "/membro":
                return self.post_membro(conn, utente, dati)
            if percorso == "/stato-utente":
                return self.post_stato_utente(conn, utente, dati)
            if percorso == "/stazione-nuova":
                return self.post_stazione_nuova(conn, utente, dati)
            if percorso == "/stazione-stato":
                return self.post_stazione_stato(conn, utente, dati)
            if percorso == "/chiave":
                return self.post_chiave(conn, utente, dati)
            if percorso == "/chiave-revoca":
                return self.post_chiave_revoca(conn, utente, dati)
            if percorso == "/utente-cancella":
                return self.post_utente_cancella(conn, utente, dati)
            if percorso == "/password":
                return self.post_password(conn, utente, dati)
            if percorso == "/reimposta-admin":
                return self.post_reimposta_admin(conn, utente, dati)
            self._send(404, page("non trovata", "<h1>Pagina inesistente</h1>", utente))
        finally:
            conn.close()

    # ----------------------------------------------------------- accesso

    def form_accesso(self, errore="", msg=""):
        corpo = """
<div class="card" style="max-width:420px;margin:40px auto">
<h1>Accesso</h1><p class="sub">Entra per collegarti alle stazioni abilitate.</p>
<form method="post" action="/accedi">
<label>Email</label><input name="email" type="email" required autofocus>
<label>Password</label><input name="password" type="password" required>
<button style="width:100%">Entra</button>
</form>
<p style="margin-top:18px;color:#8fb3d9">Non hai un accesso?
<a href="/registrati">Richiedilo</a>. &nbsp;·&nbsp;
<a href="/recupera">Password dimenticata?</a></p>
<p style="margin-top:6px;color:#8fb3d9">Ti serve il programma?
<a href="/scarica">Scarica Decolink</a>.</p></div>"""
        return page("accesso", corpo, None, msg, errore)

    def post_accesso(self, conn, dati):
        if self._freno():
            return self._send(429, self.form_accesso(
                "Troppi tentativi da questo indirizzo. Riprova fra qualche minuto."))
        utente = db.authenticate(conn, str(dati.get("email", "")), str(dati.get("password", "")))
        if not utente:
            self._segna_tentativo()
            return self._send(401, self.form_accesso("Email o password non corretti."))
        if utente["status"] == db.ST_SUSPENDED:
            return self._send(403, self.form_accesso("Questo accesso è sospeso."))
        cookie = db.new_web_session(conn, utente["id"])
        # Secure solo dietro HTTPS: con il flag attivo su una prova in chiaro il
        # browser scarterebbe il cookie e il login sembrerebbe non funzionare.
        flag = "; Secure" if HTTPS else ""
        return self._redirect("/", [("Set-Cookie",
                                     f"{COOKIE}={cookie}; HttpOnly; SameSite=Lax; Path=/{flag}")])

    def form_registrazione(self, conn, errore="", msg="", dati=None):
        dati = dati or {}
        opzioni = "".join(
            f'<option value="{e(s["slug"])}">{e(s["slug"])} — {e(s["name"] or s["callsign"])}</option>'
            for s in db.list_stations(conn) if s["enabled"])
        corpo = f"""
<div class="card" style="max-width:460px;margin:40px auto">
<h1>Richiesta di accesso</h1>
<p class="sub">La domanda viene esaminata dal titolare della stazione: fino ad allora
l'accesso resta in attesa.</p>
<form method="post" action="/registrati">
<label>Nominativo</label><input name="callsign" required value="{e(dati.get('callsign',''))}"
  placeholder="IU8LMC" style="text-transform:uppercase">
<label>Nome</label><input name="name" value="{e(dati.get('name',''))}">
<label>Email</label><input name="email" type="email" required value="{e(dati.get('email',''))}">
<label>Password</label><input name="password" type="password" required minlength="8"
  placeholder="almeno 8 caratteri">
<label>Stazione richiesta</label><select name="station"><option value="">— nessuna, decido dopo —</option>{opzioni}</select>
<label>Due righe su di te (facoltativo)</label><input name="note" value="{e(dati.get('note',''))}"
  placeholder="socio della sezione, licenza dal 2019...">
<button style="width:100%">Invia la richiesta</button>
</form>
<p style="margin-top:18px;color:#7d8b99">Hai già un accesso? <a href="/accedi">Entra</a>.</p></div>"""
        return page("registrazione", corpo, None, msg, errore)

    def post_registrazione(self, conn, dati):
        email = str(dati.get("email", "")).strip()
        call = str(dati.get("callsign", "")).strip().upper()
        pwd = str(dati.get("password", ""))
        slug = str(dati.get("station", "")).strip().lower()

        if not RE_EMAIL.match(email):
            return self._send(400, self.form_registrazione(conn, "Email non valida.", dati=dati))
        if not RE_CALL.match(call):
            return self._send(400, self.form_registrazione(
                conn, "Nominativo non valido: da 3 a 16 caratteri fra lettere, cifre e /.", dati=dati))
        if len(pwd) < 8:
            return self._send(400, self.form_registrazione(
                conn, "La password deve avere almeno 8 caratteri.", dati=dati))
        if db.user_by_email(conn, email):
            return self._send(409, self.form_registrazione(
                conn, "Esiste già un accesso con questa email.", dati=dati))

        uid = db.create_user(conn, email, call, pwd, name=str(dati.get("name", "")),
                             status=db.ST_PENDING)
        if str(dati.get("note", "")).strip():
            conn.execute("UPDATE users SET note = ? WHERE id = ?",
                         (str(dati["note"])[:400], uid))
            conn.commit()
        # La stazione richiesta si registra subito come membership da
        # ascoltatore: non vale niente finche' l'utente e' 'pending', ma fa
        # comparire la domanda nella pagina della stazione giusta, che e' dove
        # il titolare la cerchera'.
        titolare = None
        if slug:
            st = db.station_by_slug(conn, slug)
            if st:
                db.grant(conn, uid, st["id"], tok.ROLE_LISTENER)
                titolare = db.user_by_id(conn, st["owner_id"])
        print(f"  registrazione: {call} <{email}> stazione='{slug or '-'}' — in attesa")
        # Il titolare non ha modo di sapere che c'e' una domanda se non
        # guardando la pagina: se la posta e' configurata, glielo si dice.
        if titolare:
            mail.avvisa_richiesta(titolare["email"], callsign=call, email=email,
                                  nome=str(dati.get("name", "")).strip(),
                                  stazione=slug, nota=str(dati.get("note", "")).strip())
        elif mail.attiva() and not slug:
            print("  ~ nessuna stazione indicata: nessuno da avvisare")
        return self._send(200, self.form_accesso(
            msg="Richiesta inviata. Riceverai l'accesso quando il titolare l'avrà approvata."))

    # ---------------------------------------------------------- pagine

    def pagina_home(self, conn, utente):
        if not utente:
            return self.pagina_prima(conn, utente)
        if utente["status"] != db.ST_ACTIVE:
            corpo = f"""<div class="card"><h1>Accesso in attesa</h1>
<p class="sub">La richiesta di <b>{e(utente['callsign'])}</b> è stata registrata
ma non è ancora stata approvata. Fino ad allora non è possibile collegarsi ad
alcuna stazione.</p></div>"""
            return self._send(200, page("in attesa", corpo, utente))

        csrf = self._csrf(conn, utente)
        righe = ""
        for s in db.stations_of(conn, utente["id"]):
            gestisci = (f'<a href="/stazione/{e(s["slug"])}">gestisci</a> '
                        if s["role"] == tok.ROLE_OWNER or utente["is_admin"] else "")
            chiave = (f'<form method="post" action="/chiave" class="inline">'
                      f'<input type="hidden" name="csrf" value="{e(csrf)}">'
                      f'<input type="hidden" name="station" value="{e(s["slug"])}">'
                      f'<button class="ghost small">chiave</button></form>')
            righe += (f'<tr><td><b>{e(s["slug"])}</b></td><td>{e(s["name"])}</td>'
                      f'<td>{e(s["callsign"])}</td>'
                      f'<td><span class="tag {e(s["role"])}">{e(RUOLI_IT[s["role"]])}</span></td>'
                      f'<td>{gestisci}{chiave}</td></tr>')
        if not righe:
            righe = ('<tr><td colspan="5" style="color:#7d8b99">Nessuna stazione abilitata. '
                     'Chiedi al titolare di aggiungerti.</td></tr>')

        corpo = f"""<h1>Le tue stazioni</h1>
<p class="sub">Nel client Decolink inserisci queste credenziali: il token di
collegamento viene richiesto da solo a ogni avvio.</p>
<div class="card"><table>
<tr><th>stanza</th><th>nome</th><th>nominativo</th><th>ruolo</th><th></th></tr>
{righe}</table></div>
<h2>Impostazioni per il client</h2>
<div class="card"><p class="sub">Server di accesso da indicare in Decolink:</p>
<div class="mono">{e(self.headers.get('Host', ''))}</div>
<p class="sub" style="margin-top:14px;font-size:13px">Il pulsante <b>chiave</b> serve
per i programmi che non sanno fare l'accesso — come le versioni di Decodium Mobile
precedenti al controllo accessi: la chiave si incolla al posto del nome della
stanza. Decolink aggiornato non ne ha bisogno, fa il login da sé.</p></div>
{self._riquadro_chiavi(conn, utente, csrf)}"""
        return self._send(200, page("stazioni", corpo, utente))

    def _riquadro_chiavi(self, conn, utente, csrf: str) -> str:
        """Le chiavi emesse, con il pulsante per annullarle.

        Una chiave vive trenta giorni fuori dal pannello, incollata dentro
        un'applicazione: senza questo elenco, chi ne perde una puo' solo
        aspettare che scada. Qui si vede quante ne sono in giro e si spengono
        una per una.
        """
        chiavi = db.keys_of_user(conn, utente["id"])
        if not chiavi:
            return ""

        righe = ""
        for k in chiavi:
            emessa = time.strftime("%d/%m/%Y", time.localtime(k["issued_at"]))
            scade = time.strftime("%d/%m/%Y", time.localtime(k["expires_at"]))
            if k["revoked_at"] is not None:
                quando = time.strftime("%d/%m/%Y", time.localtime(k["revoked_at"]))
                stato = f'<span class="tag lst">annullata il {e(quando)}</span>'
                azione = ""
            else:
                stato = f'valida fino al <b>{e(scade)}</b>'
                azione = (f'<form method="post" action="/chiave-revoca" class="inline">'
                          f'<input type="hidden" name="csrf" value="{e(csrf)}">'
                          f'<input type="hidden" name="jti" value="{e(k["jti"])}">'
                          f'<button class="small danger">annulla</button></form>')
            righe += (f'<tr><td><b>{e(k["slug"])}</b></td>'
                      f'<td>{e(RUOLI_IT.get(k["role"], k["role"]))}</td>'
                      f'<td class="sub">emessa il {e(emessa)}</td>'
                      f'<td>{stato}</td><td>{azione}</td></tr>')

        return f"""
<h2>Chiavi di stazione emesse</h2>
<div class="card"><table>
<tr><th>stazione</th><th>ruolo</th><th>quando</th><th>stato</th><th></th></tr>
{righe}</table>
<p class="sub" style="margin-top:14px;font-size:13px">Annullare una chiave la ferma
entro pochi secondi, anche se qualcuno la sta usando in quel momento. Non si può
disfare: per tornare a collegarsi con un programma vecchio se ne emette un'altra.
Le chiavi scadute non sono in elenco, non c'è niente da annullare in una chiave
che non vale più.</p></div>"""

    def post_chiave_revoca(self, conn, utente, dati):
        """Annulla una chiave di stazione.

        La può annullare chi l'ha emessa e il titolare della stazione: il primo
        perché è sua, il secondo perché è la sua radio, ed è l'unico che può
        sapere che la chiave di un suo operatore è finita dove non doveva.
        """
        jti = str(dati.get("jti", "")).strip()
        k = db.key_by_jti(conn, jti)
        if not k:
            return self._redirect("/")

        st = db.station_by_id(conn, k["station_id"])
        suo = int(k["user_id"]) == int(utente["id"])
        titolare = bool(st) and self._puo_gestire(conn, utente, st["id"])
        if not (suo or titolare):
            return self._send(403, page("vietato",
                                        "<h1>Questa chiave non è tua</h1>", utente))

        if db.revoke_key(conn, jti, reason=f"annullata da {utente['callsign']}"):
            print(f"  {utente['callsign']} annulla la chiave {jti} "
                  f"su '{st['slug'] if st else '?'}'")
        return self._redirect("/" if suo else f"/stazione/{st['slug']}")

    def _lingua(self) -> tuple[str, bool]:
        """La lingua di chi sta leggendo, e se va scritta nel cookie.

        Nell'ordine: quella chiesta con ?lang=, quella gia' scelta nel cookie,
        quella del browser. Chi arriva da un paese qualsiasi trova la pagina
        nella sua lingua senza cercare niente, ed e' lo stesso comportamento del
        client, che prende la lingua di Windows.
        """
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        chiesta = ts.normalizza((q.get("lang") or [""])[0])
        if chiesta:
            return chiesta, True
        salvata = ts.normalizza(self._cookie(COOKIE_LINGUA))
        if salvata:
            return salvata, False
        return ts.lingua_del_browser(self.headers.get("Accept-Language", "")), False

    def pagina_prima(self, conn, utente):
        """La prima pagina: cos'e' Decolink, come si scarica, come funziona.

        Prima qui c'era il modulo di accesso e basta: chi non aveva un account
        vedeva due caselle e nessuna spiegazione, e il programma da scaricare
        stava dietro una voce di menu. Ora la spiegazione viene prima, e il
        modulo di accesso sta un clic piu' in la' per chi gia' sa cosa fare.
        """
        lingua, da_salvare = self._lingua()
        t = ts.testi(lingua)
        host = self.headers.get("Host", "decolink.ft2.it")
        rel = ultima_release()

        # Chi ha appena eliminato il proprio accesso arriva qui: senza una
        # riga che lo dica, la prima pagina sembrerebbe solo un'uscita mal
        # riuscita invece della conferma che la cosa e' andata a buon fine.
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        avviso = ts.avviso("eliminato", lingua) if q.get("eliminato") else ""

        if rel and rel["file"]:
            def peso(f):
                n = f["nome"].lower()
                return (0 if ("win" in n or n.endswith(".zip") or n.endswith(".exe")) else 1, n)
            principale = sorted(rel["file"], key=peso)[0]
            bottone = (f'<a class="scarica" href="{e(principale["url"])}">{e(t["scarica"])}</a>'
                       f'<div class="sotto-btn">'
                       + e(t["peso"]).format(versione=e(rel["tag"]), peso=principale["mb"])
                       + '</div>')
        else:
            bottone = (f'<a class="scarica" href="{e(RELEASE_PAGINA)}">{e(t["vai_github"])}</a>'
                       f'<div class="sotto-btn">{e(t["senza_ver"])}</div>')

        # I passi contengono <b> e <a> voluti da noi, non testo di chi visita:
        # non vanno passati da e(), o si vedrebbero i tag scritti in chiaro.
        passo2 = t["passo2_si"] if utente else t["passo2_no"]
        corpo = f"""
<div class="hero prima">
<h1>{e(t["claim"])}</h1>
<p class="claim">{e(t["sotto"])}</p>
{bottone}
<div class="gia">{e(t["gia"])} <a href="/accedi">{e(t["accedi"])}</a>
 &nbsp;·&nbsp; <a href="/registrati">{e(t["registrati"])}</a></div>
</div>

<div class="riquadri" style="margin-top:30px">
  <div class="card"><b>{e(t["h_cosa"])}</b><p class="sub" style="margin:8px 0 0">
  {e(t["p_cosa"])}</p></div>
  <div class="card"><b>{e(t["h_serve"])}</b><p class="sub" style="margin:8px 0 0">
  {e(t["p_serve"])}</p></div>
  <div class="card"><b>{e(t["h_ovunque"])}</b><p class="sub" style="margin:8px 0 0">
  {e(t["p_ovunque"])}</p></div>
</div>

<h2>{e(t["h_parte"])}</h2>
<div class="card">
  <div class="passo"><div class="n">1</div><div>{e(t["passo1"])}</div></div>
  <div class="passo"><div class="n">2</div><div>{passo2}</div></div>
  <div class="passo"><div class="n">3</div><div>{t["passo3"].format(host=e(host))}</div></div>
  <div class="passo"><div class="n">4</div><div>{t["passo4"]}</div></div>
</div>

<h2>{e(t["h_come"])}</h2>
<div class="card"><p class="sub" style="margin:0">{e(t["p_come"])}</p></div>
<div class="modi" style="margin-top:14px">
  <div class="card"><b>{e(t["m1_t"])}</b><p class="sub" style="margin:8px 0 0">
  {e(t["m1_p"])}</p></div>
  <div class="card"><b>{e(t["m2_t"])}</b><p class="sub" style="margin:8px 0 0">
  {e(t["m2_p"])}</p></div>
  <div class="card"><b>{e(t["m3_t"])}</b><p class="sub" style="margin:8px 0 0">
  {e(t["m3_p"])}</p></div>
</div>

<h2>{e(t["h_banda"])}</h2>
<div class="card"><p class="sub" style="margin:0">{e(t["p_banda"])}</p></div>

<h2>{e(t["h_lingue"])}</h2>
<div class="card"><p class="sub" style="margin:0">{e(t["p_lingue"])}</p></div>

<p class="sub" style="font-size:13px;margin-top:26px">{e(t["sorgente"])}
<a href="https://github.com/{e(GITHUB_REPO)}">github.com/{e(GITHUB_REPO)}</a></p>"""

        extra = []
        if da_salvare:
            # Un anno: la lingua non e' una sessione, e chi torna fra sei mesi
            # non deve ricominciare dall'italiano.
            extra.append(("Set-Cookie",
                          f"{COOKIE_LINGUA}={lingua}; Max-Age=31536000; Path=/; "
                          f"SameSite=Lax"))
        return self._send(200, page("Decolink", corpo, utente, msg=avviso, banner=False,
                                    lingua=lingua, percorso="/"), extra=extra)

    def pagina_stazione(self, conn, utente, slug):
        if not utente:
            return self._redirect("/accedi")
        st = db.station_by_slug(conn, slug)
        if not st:
            return self._send(404, page("non trovata", "<h1>Stazione inesistente</h1>", utente))
        if not (utente["is_admin"] or st["owner_id"] == utente["id"]):
            return self._send(403, page("vietato", "<h1>Non sei il titolare di questa stazione</h1>",
                                        utente))
        csrf = self._csrf(conn, utente)

        righe = ""
        for m in db.members_of(conn, st["id"]):
            sel = "".join(f'<option value="{r}"{" selected" if m["role"] == r else ""}>'
                          f'{RUOLI_IT[r]}</option>' for r in tok.ROLES)
            azioni = f"""
<form method="post" action="/membro" class="row">
<input type="hidden" name="csrf" value="{e(csrf)}">
<input type="hidden" name="station" value="{e(st['slug'])}">
<input type="hidden" name="user" value="{m['id']}">
<select name="role" style="width:auto">{sel}</select>
<button class="small">salva</button>
<button class="small danger" name="azione" value="revoca">togli</button>
</form>"""
            stato = f'<span class="tag {e(m["status"])}">{e(STATI_IT[m["status"]])}</span>'
            if m["status"] == db.ST_PENDING:
                stato += f"""
<form method="post" action="/stato-utente" class="inline">
<input type="hidden" name="csrf" value="{e(csrf)}">
<input type="hidden" name="user" value="{m['id']}">
<input type="hidden" name="torna" value="/stazione/{e(st['slug'])}">
<button class="small" name="stato" value="active">approva</button></form>"""
            elif m["status"] == db.ST_ACTIVE and m["id"] != utente["id"]:
                stato += f"""
<form method="post" action="/stato-utente" class="inline">
<input type="hidden" name="csrf" value="{e(csrf)}">
<input type="hidden" name="user" value="{m['id']}">
<input type="hidden" name="torna" value="/stazione/{e(st['slug'])}">
<button class="small ghost" name="stato" value="suspended">sospendi</button></form>"""
            note = f'<div style="color:#7d8b99;font-size:13px">{e(m["note"])}</div>' if m["note"] else ""
            righe += (f'<tr><td><b>{e(m["callsign"])}</b>{note}</td><td>{e(m["name"])}</td>'
                      f'<td>{e(m["email"])}</td><td>{stato}</td><td>{azioni}</td></tr>')

        tx = ""
        for t in db.recent_tx(conn, st["id"], 25):
            durata = (f'{t["ended_at"] - t["started_at"]} s' if t["ended_at"] else "in corso")
            tx += (f'<tr><td>{time.strftime("%d/%m %H:%M:%S", time.localtime(t["started_at"]))}</td>'
                   f'<td><b>{e(t["callsign"])}</b></td><td>{durata}</td><td>{e(t["addr"])}</td></tr>')
        tx = tx or '<tr><td colspan="4" style="color:#7d8b99">Nessuna trasmissione registrata.</td></tr>'

        cn = ""
        for c in db.recent_connections(conn, st["id"], 25):
            fine = (time.strftime("%H:%M:%S", time.localtime(c["left_at"]))
                    if c["left_at"] else "collegato")
            cn += (f'<tr><td>{time.strftime("%d/%m %H:%M:%S", time.localtime(c["joined_at"]))}</td>'
                   f'<td><b>{e(c["callsign"])}</b></td>'
                   f'<td>{e(RUOLI_IT.get(c["role"], c["role"]))}</td>'
                   f'<td>{fine}</td><td>{e(c["addr"])}</td></tr>')
        cn = cn or '<tr><td colspan="5" style="color:#7d8b99">Nessun collegamento registrato.</td></tr>'

        stato_st = "aperta" if st["enabled"] else "chiusa"
        corpo = f"""<h1>Stazione {e(st["slug"])}</h1>
<p class="sub">{e(st["name"])} — nominativo {e(st["callsign"] or "non indicato")} — stazione {stato_st}</p>

<div class="card"><form method="post" action="/stazione-stato" class="row">
<input type="hidden" name="csrf" value="{e(csrf)}">
<input type="hidden" name="station" value="{e(st['slug'])}">
<span style="color:#9fb0c0">Chiudendo la stazione nessuno può collegarsi, nemmeno chi è già abilitato.</span>
<button class="small {'danger' if st['enabled'] else ''}" name="enabled"
 value="{0 if st['enabled'] else 1}">{'chiudi' if st['enabled'] else 'riapri'}</button>
</form></div>

<h2>Chi può accedere</h2>
<div class="card"><table>
<tr><th>nominativo</th><th>nome</th><th>email</th><th>stato</th><th>ruolo</th></tr>
{righe}</table>
<p style="color:#7d8b99;font-size:13px;margin-top:14px">
Solo <b>titolare</b> e <b>operatore</b> possono trasmettere e comandare il rig.
L'<b>ascoltatore</b> riceve e basta.</p></div>

<h2>Registro delle trasmissioni</h2>
<div class="card"><table>
<tr><th>quando</th><th>chi</th><th>durata</th><th>indirizzo</th></tr>{tx}</table></div>

<h2>Collegamenti</h2>
<div class="card"><table>
<tr><th>entrato</th><th>chi</th><th>ruolo</th><th>uscito</th><th>indirizzo</th></tr>{cn}</table></div>
{self._chiavi_della_stazione(conn, st, csrf)}"""
        return self._send(200, page(f"stazione {slug}", corpo, utente))

    def _chiavi_della_stazione(self, conn, st, csrf: str) -> str:
        """Le chiavi vive di questa stazione, di chiunque siano.

        Le vede il titolare perche' e' la sua radio: una chiave di un operatore
        finita nelle mani sbagliate opera la stazione a nome suo, e chi ne
        risponde deve poterla spegnere senza chiedere il permesso a nessuno.
        """
        chiavi = db.keys_of_station(conn, st["id"])
        if not chiavi:
            return ""
        righe = ""
        for k in chiavi:
            emessa = time.strftime("%d/%m/%Y", time.localtime(k["issued_at"]))
            scade = time.strftime("%d/%m/%Y", time.localtime(k["expires_at"]))
            if k["revoked_at"] is not None:
                quando = time.strftime("%d/%m/%Y", time.localtime(k["revoked_at"]))
                stato, azione = f'<span class="tag lst">annullata il {e(quando)}</span>', ""
            else:
                stato = f'fino al <b>{e(scade)}</b>'
                azione = (f'<form method="post" action="/chiave-revoca" class="inline">'
                          f'<input type="hidden" name="csrf" value="{e(csrf)}">'
                          f'<input type="hidden" name="jti" value="{e(k["jti"])}">'
                          f'<button class="small danger">annulla</button></form>')
            righe += (f'<tr><td><b>{e(k["callsign"])}</b></td>'
                      f'<td>{e(RUOLI_IT.get(k["role"], k["role"]))}</td>'
                      f'<td class="sub">emessa il {e(emessa)}</td>'
                      f'<td>{stato}</td><td>{azione}</td></tr>')
        return f"""
<h2>Chiavi di stazione in circolazione</h2>
<div class="card"><table>
<tr><th>chi</th><th>ruolo</th><th>quando</th><th>stato</th><th></th></tr>
{righe}</table>
<p class="sub" style="margin-top:14px;font-size:13px">Sono chiavi che operano
questa stazione senza passare dall'accesso, valide fino alla scadenza da
qualunque dispositivo. Annullandone una, chi la sta usando viene chiuso entro
pochi secondi.</p></div>"""

    def pagina_admin(self, conn, utente):
        if not utente:
            return self._redirect("/accedi")
        if not utente["is_admin"]:
            return self._send(403, page("vietato", "<h1>Riservato agli amministratori</h1>", utente))
        csrf = self._csrf(conn, utente)

        ut = ""
        for u in db.list_users(conn):
            azioni = ""
            for stato, etichetta in ((db.ST_ACTIVE, "attiva"), (db.ST_SUSPENDED, "sospendi")):
                if u["status"] != stato and u["id"] != utente["id"]:
                    azioni += f"""
<form method="post" action="/stato-utente" class="inline">
<input type="hidden" name="csrf" value="{e(csrf)}">
<input type="hidden" name="user" value="{u['id']}">
<input type="hidden" name="torna" value="/admin">
<button class="small ghost" name="stato" value="{stato}">{etichetta}</button></form> """
            # La cancellazione non si offre per se stessi: un amministratore che
            # si cancella lascia il pannello senza nessuno che possa entrarci.
            azioni += f"""
<form method="post" action="/reimposta-admin" class="inline"
      onsubmit="return confirm('Rimettere la password di {e(u['callsign'])}?')">
<input type="hidden" name="csrf" value="{e(csrf)}">
<input type="hidden" name="user" value="{u['id']}">
<button class="small ghost">password</button></form> """
            if u["id"] != utente["id"]:
                azioni += f"""
<form method="post" action="/utente-cancella" class="inline"
      onsubmit="return confirm('Cancellare {e(u['callsign'])} definitivamente?')">
<input type="hidden" name="csrf" value="{e(csrf)}">
<input type="hidden" name="user" value="{u['id']}">
<button class="small danger">cancella</button></form> """
            ut += (f'<tr><td><b>{e(u["callsign"])}</b></td><td>{e(u["name"])}</td>'
                   f'<td>{e(u["email"])}</td>'
                   f'<td><span class="tag {e(u["status"])}">{e(STATI_IT[u["status"]])}</span></td>'
                   f'<td>{"sì" if u["is_admin"] else ""}</td><td>{azioni}</td></tr>')

        stz = ""
        for s in db.list_stations(conn):
            titolare = db.user_by_id(conn, s["owner_id"])
            stz += (f'<tr><td><b>{e(s["slug"])}</b></td><td>{e(s["name"])}</td>'
                    f'<td>{e(titolare["callsign"] if titolare else "?")}</td>'
                    f'<td>{"aperta" if s["enabled"] else "chiusa"}</td>'
                    f'<td><a href="/stazione/{e(s["slug"])}">gestisci</a></td></tr>')

        scelte = "".join(f'<option value="{u["id"]}">{e(u["callsign"])} — {e(u["email"])}</option>'
                         for u in db.list_users(conn, db.ST_ACTIVE))
        corpo = f"""<h1>Amministrazione</h1>
<p class="sub">Utenti registrati e stazioni del server.</p>

<h2>Utenti</h2>
<div class="card"><table>
<tr><th>nominativo</th><th>nome</th><th>email</th><th>stato</th><th>admin</th><th></th></tr>
{ut}</table></div>

<h2>Stazioni</h2>
<div class="card"><table>
<tr><th>stanza</th><th>nome</th><th>titolare</th><th>stato</th><th></th></tr>
{stz or '<tr><td colspan="5" style="color:#7d8b99">Nessuna stazione.</td></tr>'}</table></div>

<h2>Nuova stazione</h2>
<div class="card"><form method="post" action="/stazione-nuova">
<input type="hidden" name="csrf" value="{e(csrf)}">
<label>Codice stanza</label><input name="slug" required placeholder="i0abc-hf"
 pattern="[a-z0-9][a-z0-9-]{{1,30}}">
<label>Nome</label><input name="name" placeholder="Stazione HF della sezione">
<label>Nominativo della stazione</label><input name="callsign" placeholder="IQ8XX"
 style="text-transform:uppercase">
<label>Titolare</label><select name="owner" required>{scelte}</select>
<button>Crea la stazione</button></form></div>"""
        return self._send(200, page("amministrazione", corpo, utente))

    # ----------------------------------------------------------- azioni

    def _puo_gestire(self, conn, utente, station_id) -> bool:
        st = db.station_by_id(conn, station_id)
        return bool(st) and (utente["is_admin"] or st["owner_id"] == utente["id"])

    def post_membro(self, conn, utente, dati):
        st = db.station_by_slug(conn, str(dati.get("station", "")))
        if not st or not self._puo_gestire(conn, utente, st["id"]):
            return self._send(403, page("vietato", "<h1>Non puoi gestire questa stazione</h1>", utente))
        try:
            uid = int(dati.get("user", 0))
        except ValueError:
            return self._redirect(f"/stazione/{st['slug']}")

        if str(dati.get("azione", "")) == "revoca":
            # Il titolare non puo' togliersi da solo: resterebbe una stazione
            # senza nessuno che possa amministrarla.
            if uid == st["owner_id"]:
                return self._redirect(f"/stazione/{st['slug']}")
            db.revoke(conn, uid, st["id"])
            print(f"  {utente['callsign']} toglie l'utente {uid} da '{st['slug']}'")
        else:
            ruolo = str(dati.get("role", tok.ROLE_LISTENER))
            if ruolo not in tok.ROLES:
                return self._redirect(f"/stazione/{st['slug']}")
            if uid == st["owner_id"] and ruolo != tok.ROLE_OWNER:
                return self._redirect(f"/stazione/{st['slug']}")
            db.grant(conn, uid, st["id"], ruolo, utente["id"])
            print(f"  {utente['callsign']} assegna '{ruolo}' all'utente {uid} su '{st['slug']}'")
        return self._redirect(f"/stazione/{st['slug']}")

    def post_stato_utente(self, conn, utente, dati):
        try:
            uid = int(dati.get("user", 0))
        except ValueError:
            return self._redirect("/")
        stato = str(dati.get("stato", ""))
        torna = str(dati.get("torna", "/"))
        if not torna.startswith("/"):
            torna = "/"        # niente redirect verso l'esterno
        if uid == utente["id"]:
            return self._redirect(torna)

        # Puo' approvare o sospendere un amministratore, oppure il titolare di
        # una stazione di cui l'utente e' (o chiede di essere) membro.
        permesso = utente["is_admin"]
        if not permesso:
            for s in db.list_stations(conn, owner_id=utente["id"]):
                if db.role_of(conn, uid, s["id"]):
                    permesso = True
                    break
        if not permesso:
            return self._send(403, page("vietato", "<h1>Non puoi cambiare questo accesso</h1>", utente))

        db.set_user_status(conn, uid, stato)
        # Sospendere qualcuno mentre e' collegato deve buttarlo fuori subito: il
        # relay se ne accorge al prossimo rinfresco dei permessi, entro pochi
        # secondi, perche' active_grants() salta gli utenti non attivi.
        print(f"  {utente['callsign']} porta l'utente {uid} allo stato '{stato}'")
        return self._redirect(torna)

    def post_stazione_nuova(self, conn, utente, dati):
        if not utente["is_admin"]:
            return self._send(403, page("vietato", "<h1>Riservato agli amministratori</h1>", utente))
        slug = str(dati.get("slug", "")).strip().lower()
        if not RE_SLUG.match(slug):
            return self._send(400, page("errore", "<h1>Codice stanza non valido</h1>"
                                        "<p class='sub'>Lettere minuscole, cifre e trattini.</p>"
                                        "<p><a href='/admin'>torna</a></p>", utente))
        if db.station_by_slug(conn, slug):
            return self._send(409, page("errore", "<h1>Questo codice stanza esiste già</h1>"
                                        "<p><a href='/admin'>torna</a></p>", utente))
        try:
            owner = int(dati.get("owner", 0))
        except ValueError:
            return self._redirect("/admin")
        if not db.user_by_id(conn, owner):
            return self._redirect("/admin")
        db.create_station(conn, slug, owner, name=str(dati.get("name", "")),
                          callsign=str(dati.get("callsign", "")))
        print(f"  {utente['callsign']} crea la stazione '{slug}'")
        return self._redirect(f"/stazione/{slug}")

    def post_stazione_stato(self, conn, utente, dati):
        st = db.station_by_slug(conn, str(dati.get("station", "")))
        if not st or not self._puo_gestire(conn, utente, st["id"]):
            return self._send(403, page("vietato", "<h1>Non puoi gestire questa stazione</h1>", utente))
        db.set_station_enabled(conn, st["id"], str(dati.get("enabled", "1")) == "1")
        return self._redirect(f"/stazione/{st['slug']}")

    def post_utente_cancella(self, conn, utente, dati):
        """Cancella un utente. Solo gli amministratori, e mai se stessi."""
        if not utente["is_admin"]:
            return self._send(403, page("vietato", "<h1>Riservato agli amministratori</h1>", utente))
        try:
            uid = int(dati.get("user", 0))
        except ValueError:
            return self._redirect("/admin")
        if uid == utente["id"]:
            return self._redirect("/admin")
        vittima = db.user_by_id(conn, uid)
        if not vittima:
            return self._redirect("/admin")
        try:
            db.delete_user(conn, uid)
        except ValueError as ex:
            return self._send(409, page("non si può", f"<h1>Impossibile cancellare "
                                        f"{e(vittima['callsign'])}</h1>"
                                        f"<p class='sub'>{e(str(ex))}.</p>"
                                        f"<p><a href='/admin'>torna</a></p>", utente))
        print(f"  {utente['callsign']} cancella l'utente {vittima['callsign']} "
              f"<{vittima['email']}>")
        return self._redirect("/admin")

    def post_chiave(self, conn, utente, dati):
        """Emette una chiave di stazione per i programmi che non sanno accedere.

        Serve a chi ha un'app con un solo campo di testo al posto del login: la
        chiave si incolla dove andava il nome della stanza. Vale trenta giorni
        perche' nessuno puo' reincollarla ogni ora, ed e' l'unico modo per far
        entrare un programma vecchio senza riaprire le stanze a chiunque.
        """
        if utente["status"] != db.ST_ACTIVE:
            return self._send(403, page("vietato", "<h1>Accesso non attivo</h1>", utente))
        slug = str(dati.get("station", "")).strip().lower()
        st = db.station_by_slug(conn, slug)
        if not st:
            return self._redirect("/")
        ruolo = db.role_of(conn, utente["id"], st["id"])
        if not ruolo:
            return self._send(403, page("vietato",
                                        "<h1>Non hai accesso a questa stazione</h1>", utente))

        chiave = tok.issue(SECRET, user_id=utente["id"], callsign=utente["callsign"],
                           station_id=st["id"], role=ruolo, ttl=CHIAVE_TTL)
        # L'identificativo si rilegge dal token appena firmato invece di
        # fabbricarlo qui: e' l'unico modo per essere certi di annotare quello
        # che c'e' davvero dentro alla chiave che si sta consegnando.
        dati_chiave = tok.verify(SECRET, chiave)
        db.record_key(conn, dati_chiave["jti"], utente["id"], st["id"], ruolo,
                      dati_chiave["expires"])
        scade = time.strftime("%d/%m/%Y", time.localtime(time.time() + CHIAVE_TTL))
        print(f"  chiave di stazione per {utente['callsign']} su '{st['slug']}' "
              f"({ruolo}), scade il {scade}")

        corpo = f"""<h1>Chiave per {e(st['slug'])}</h1>
<p class="sub">Da usare nei programmi che non sanno fare l'accesso, come le versioni
di Decodium Mobile precedenti al controllo accessi.</p>

<div class="card">
<p><b>Incolla questa chiave al posto del nome della stanza</b>, nel campo
<i>Stanza</i> dell'applicazione. Lascia l'host come è
(<span class="mono" style="display:inline;padding:2px 6px">{e(self.headers.get('Host', ''))}</span>).</p>
<div class="mono">{e(chiave)}</div>
<p class="sub" style="margin-top:14px">Vale come <b>{e(RUOLI_IT.get(ruolo, ruolo))}</b>
fino al <b>{e(scade)}</b>. Ogni collegamento e ogni trasmissione restano registrati
a nome tuo.</p>
</div>

<div class="msg err">
<b>Trattala come una password.</b> Chi ce l'ha può operare la stazione come te,
fino alla scadenza, da qualunque dispositivo. Se la perdi o non ti serve più,
annullala dalla <a href="/">pagina delle tue stazioni</a>: smette di funzionare
entro pochi secondi, anche per chi la sta usando in quel momento.
</div>

<p><a href="/">← torna alle stazioni</a></p>"""
        return self._send(200, page("chiave di stazione", corpo, utente))

    # -------------------------------------------------------------- API

    def api_login(self, conn, dati):
        """Login dei client: credenziali in cambio di un token per il relay.

        Risponde sempre con l'elenco delle stazioni abilitate, cosi' il client
        puo' proporle senza una seconda chiamata. Se la stazione non viene
        indicata e ce n'e' una sola, si sceglie quella: e' il caso di gran lunga
        piu' comune e risparmia un passaggio all'utente.
        """
        if self._freno():
            return self._json(429, {"ok": False, "error": "troppi tentativi, riprova più tardi"})
        utente = db.authenticate(conn, str(dati.get("email", "")), str(dati.get("password", "")))
        if not utente:
            self._segna_tentativo()
            return self._json(401, {"ok": False, "error": "email o password non corretti"})
        if utente["status"] == db.ST_PENDING:
            return self._json(403, {"ok": False, "error": "accesso in attesa di approvazione"})
        if utente["status"] != db.ST_ACTIVE:
            return self._json(403, {"ok": False, "error": "accesso sospeso"})

        stazioni = db.stations_of(conn, utente["id"])
        elenco = [{"slug": s["slug"], "name": s["name"], "callsign": s["callsign"],
                   "role": s["role"]} for s in stazioni]
        if not elenco:
            return self._json(403, {"ok": False, "error": "nessuna stazione abilitata per questo utente",
                                    "stations": []})

        voluta = str(dati.get("station", "")).strip().lower()
        scelta = None
        if voluta:
            scelta = next((s for s in stazioni if s["slug"] == voluta), None)
            if not scelta:
                return self._json(403, {"ok": False, "stations": elenco,
                                        "error": f"nessun permesso sulla stazione '{voluta}'"})
        elif len(stazioni) == 1:
            scelta = stazioni[0]
        else:
            return self._json(200, {"ok": False, "need_station": True, "stations": elenco,
                                    "error": "indica su quale stazione collegarti"})

        token = tok.issue(SECRET, user_id=utente["id"], callsign=utente["callsign"],
                          station_id=scelta["id"], role=scelta["role"], ttl=API_TOKEN_TTL)
        print(f"  token per {utente['callsign']} su '{scelta['slug']}' ({scelta['role']})")
        return self._json(200, {
            "ok": True, "token": token, "expires_in": API_TOKEN_TTL,
            "callsign": utente["callsign"], "station": scelta["slug"],
            "station_name": scelta["name"], "role": scelta["role"],
            "can_transmit": tok.can_transmit(scelta["role"]), "stations": elenco,
        })

    def pagina_scarica(self, conn, utente):
        """Pagina pubblica di scaricamento del client.

        Sta fuori dal login perche' il client serve prima di averne uno: chi
        arriva qui deve poter scaricare, vedere che gli occorre un accesso e
        chiederlo, in quest'ordine.
        """
        rel = ultima_release()

        if rel and rel["file"]:
            # Prima l'eseguibile o l'archivio per Windows, che e' quello che
            # cerca il 99% di chi arriva su questa pagina.
            def peso(f):
                n = f["nome"].lower()
                return (0 if ("win" in n or n.endswith(".zip") or n.endswith(".exe")) else 1, n)
            fs = sorted(rel["file"], key=peso)
            principale = fs[0]
            scaricato = sum(f["conta"] for f in rel["file"])
            bottone = (f'<a class="scarica" href="{e(principale["url"])}">'
                       f'Scarica Decolink {e(rel["tag"])}</a>'
                       f'<div class="sub" style="margin-top:12px;font-size:14px">'
                       f'{e(principale["nome"])} — {principale["mb"]} MB'
                       + (f' — pubblicato il {e(rel["data"])}' if rel["data"] else "")
                       + (f' — {scaricato} scaricamenti' if scaricato else "") + '</div>')
            altri = ""
            if len(fs) > 1:
                voci = "".join(
                    f'<li><a href="{e(f["url"])}">{e(f["nome"])}</a> '
                    f'<span style="color:#8fb3d9">({f["mb"]} MB)</span></li>' for f in fs[1:])
                altri = (f'<h2>Altri file di questa versione</h2>'
                         f'<div class="card"><ul style="margin:0;padding-left:20px">{voci}</ul></div>')
            note = ""
            if rel["note"]:
                note = (f'<h2>Novità di {e(rel["tag"])}</h2>'
                        f'<div class="card" style="white-space:pre-wrap;color:#c9d8ea">'
                        f'{e(rel["note"])}</div>')
        else:
            # GitHub non risponde, oppure non e' ancora stata pubblicata una
            # release: si manda comunque la gente nel posto giusto.
            bottone = (f'<a class="scarica" href="{e(RELEASE_PAGINA)}">Vai agli scaricamenti</a>'
                       f'<div class="sub" style="margin-top:12px;font-size:14px">'
                       f'l\'elenco delle versioni è su GitHub</div>')
            altri = note = ""

        corpo = f"""
<div class="hero">
<h1>Decolink</h1>
<p class="sub">Porta la tua radio su Decodium Mobile: l'audio ricevuto e il
controllo del rig viaggiano su internet, da casa al telefono, dovunque sia.</p>
{bottone}
</div>

<div class="riquadri" style="margin-top:26px">
  <div class="card"><b>Che cosa fa</b><p class="sub" style="margin:8px 0 0">
  Manda al telefono l'audio del CODEC USB della radio e le fa da rigctld:
  frequenza, modo e PTT senza installare Hamlib.</p></div>
  <div class="card"><b>Che cosa serve</b><p class="sub" style="margin:8px 0 0">
  Windows 64 bit, la radio collegata via USB e un accesso a questo gateway.
  Niente da installare: si scompatta e si avvia.</p></div>
  <div class="card"><b>Funziona ovunque</b><p class="sub" style="margin:8px 0 0">
  Anche col telefono su dati mobili: PC e telefono escono verso il relay, quindi
  non c'è nessun router da configurare.</p></div>
</div>

<h2>Come si parte</h2>
<div class="card">
  <div class="passo"><div class="n">1</div><div>Scarica l'archivio e scompattalo
    dove vuoi, anche su una chiavetta.</div></div>
  <div class="passo"><div class="n">2</div><div>Serve un accesso approvato:
    {'ce l\'hai già.' if utente else '<a href="/registrati">richiedilo qui</a> indicando il tuo nominativo e la stazione.'}
    </div></div>
  <div class="passo"><div class="n">3</div><div>Avvia <span class="mono"
    style="display:inline;padding:2px 6px">Decolink.exe</span>, scrivi
    <b>{e(self.headers.get('Host', 'decolink.ft2.it'))}</b> come server di accesso,
    entra con le tue credenziali e scegli la stazione.</div></div>
  <div class="passo"><div class="n">4</div><div>Scegli l'ingresso audio della
    radio, premi <b>Avvia</b> e sul telefono metti Collegamento = Relay.</div></div>
</div>
{note}
{altri}
<p class="sub" style="font-size:13px">Codice sorgente e cronologia delle versioni:
<a href="https://github.com/{e(GITHUB_REPO)}">github.com/{e(GITHUB_REPO)}</a></p>"""
        return self._send(200, page("scarica", corpo, utente, banner=False))

    # ------------------------------------------------------- password

    def pagina_password(self, conn, utente, errore="", msg=""):
        if not utente:
            return self._redirect("/accedi")
        csrf = self._csrf(conn, utente)
        corpo = f"""
<div class="card" style="max-width:460px">
<h1>Cambia la password</h1>
<p class="sub">Vale per il pannello e per il client Decolink: sono lo stesso accesso.</p>
<form method="post" action="/password">
<input type="hidden" name="csrf" value="{e(csrf)}">
<label>Password attuale</label><input name="vecchia" type="password" required autofocus>
<label>Nuova password</label><input name="nuova" type="password" required minlength="8"
  placeholder="almeno 8 caratteri">
<label>Ripeti la nuova</label><input name="ripeti" type="password" required minlength="8">
<button style="width:100%">Cambia</button>
</form>
<p class="sub" style="margin-top:16px;font-size:13px">Cambiando la password, le
<b>chiavi di stazione</b> già emesse continuano a valere fino alla loro scadenza:
sono firmate a parte e non dipendono da questa.</p>
</div>

{self._riquadro_elimina(conn, utente, csrf)}"""
        return self._send(200, page("il tuo accesso", corpo, utente, msg, errore))

    def _riquadro_elimina(self, conn, utente, csrf: str) -> str:
        """Il riquadro per cancellare il proprio accesso.

        Chi vuole andarsene deve poterlo fare da solo, senza chiedere il
        permesso a un amministratore. Ma e' irreversibile, quindi si chiedono
        due conferme di natura diversa: la password dice che sei tu, il
        nominativo scritto a mano dice che l'hai voluto. Un pulsante solo lo si
        preme per sbaglio; queste due cose no.
        """
        possedute = db.owned_stations(conn, utente["id"])
        if possedute:
            elenco = ", ".join(f'<b>{e(s["slug"])}</b>' for s in possedute)
            return f"""
<div class="card" style="max-width:460px;margin-top:20px;border-color:rgba(255,107,107,.35)">
<h2 style="margin-top:0">Elimina il tuo accesso</h2>
<p class="sub">Sei titolare di {elenco}. Finché lo sei non puoi cancellarti:
resterebbe una stazione che nessuno può amministrare.</p>
<p class="sub" style="font-size:13px">Passa la titolarità a un altro operatore
dalla pagina della stazione, oppure chiedi a un amministratore di eliminarla.
Poi torna qui.</p></div>"""

        ultimo_admin = utente["is_admin"] and db.count_admins(conn) <= 1
        if ultimo_admin:
            return """
<div class="card" style="max-width:460px;margin-top:20px;border-color:rgba(255,107,107,.35)">
<h2 style="margin-top:0">Elimina il tuo accesso</h2>
<p class="sub">Sei l'unico amministratore rimasto. Se te ne vai non resta
nessuno ad approvare le registrazioni, e per rimediare bisognerebbe entrare nel
server a mano.</p>
<p class="sub" style="font-size:13px">Nomina prima un altro amministratore dal
pannello, poi torna qui.</p></div>"""

        return f"""
<div class="card" style="max-width:460px;margin-top:20px;border-color:rgba(255,107,107,.35)">
<h2 style="margin-top:0">Elimina il tuo accesso</h2>
<p class="sub">Sparisce l'accesso, le abilitazioni sulle stazioni degli altri e
le sessioni aperte. Se in questo momento sei collegato a una stazione, il relay
chiude entro pochi secondi.</p>
<p class="sub" style="font-size:13px">Restano i registri dei collegamenti e delle
trasmissioni, col nominativo scritto dentro: servono a dire chi ha operato la
radio, e cancellarli insieme all'accesso vorrebbe dire poter far sparire le
proprie tracce. Non si torna indietro: per rientrare bisogna registrarsi di
nuovo e farsi riapprovare.</p>
<form method="post" action="/elimina-accesso">
<input type="hidden" name="csrf" value="{e(csrf)}">
<label>La tua password</label><input name="password" type="password" required>
<label>Scrivi <b>{e(utente["callsign"])}</b> per confermare</label>
<input name="conferma" required autocomplete="off" placeholder="{e(utente["callsign"])}">
<button class="danger" style="width:100%">Elimina il mio accesso</button>
</form></div>"""

    def post_password(self, conn, utente, dati):
        vecchia = str(dati.get("vecchia", ""))
        nuova = str(dati.get("nuova", ""))
        ripeti = str(dati.get("ripeti", ""))
        if not db.check_password(vecchia, utente["pwd"]):
            return self.pagina_password(conn, utente, "La password attuale non è corretta.")
        if len(nuova) < 8:
            return self.pagina_password(conn, utente, "La nuova password deve avere almeno 8 caratteri.")
        if nuova != ripeti:
            return self.pagina_password(conn, utente, "Le due password non coincidono.")
        db.set_password(conn, utente["id"], nuova)
        print(f"  {utente['callsign']} ha cambiato la propria password")
        # Si resta collegati: il cookie di sessione e' indipendente dalla
        # password, e buttare fuori qualcuno che ha appena fatto la cosa giusta
        # sarebbe solo scortese.
        return self.pagina_password(conn, db.user_by_id(conn, utente["id"]),
                                    msg="Password cambiata.")

    def post_elimina_accesso(self, conn, utente, dati):
        """Cancellazione del proprio accesso, chiesta dall'interessato.

        Tutti i controlli si rifanno qui e non ci si fida di quelli fatti
        mostrando il modulo: fra il momento in cui la pagina e' stata aperta e
        quello in cui arriva la POST possono essere passate ore, e nel frattempo
        l'utente puo' essere diventato titolare di una stazione o essere rimasto
        l'unico amministratore.
        """
        if not utente:
            return self._redirect("/accedi")

        if not db.check_password(str(dati.get("password", "")), utente["pwd"]):
            return self.pagina_password(conn, utente, "La password non è corretta.")

        # Confronto senza distinguere maiuscole e spazi ai lati: chi scrive
        # " iu8lmc " intendeva il proprio nominativo, non un altro.
        scritto = str(dati.get("conferma", "")).strip().upper()
        if scritto != str(utente["callsign"]).strip().upper():
            return self.pagina_password(
                conn, utente, "Per confermare devi scrivere esattamente il tuo nominativo.")

        if db.owned_stations(conn, utente["id"]):
            return self.pagina_password(
                conn, utente, "Sei titolare di una stazione: passa prima la titolarità.")

        if utente["is_admin"] and db.count_admins(conn) <= 1:
            return self.pagina_password(
                conn, utente, "Sei l'unico amministratore: nominane un altro prima di andartene.")

        try:
            db.delete_user(conn, utente["id"])
        except ValueError as ex:
            return self.pagina_password(conn, utente, str(ex).capitalize() + ".")

        # Nel registro resta scritto chi se n'e' andato e quando: e' un evento
        # che non si puo' ricostruire da nessun'altra parte, visto che la riga
        # dell'utente non c'e' piu'.
        print(f"  {utente['callsign']} <{utente['email']}> ha eliminato il proprio accesso")

        # Il cookie va spento qui: le sessioni sono sparite col database, ma un
        # browser che continua a mandare un cookie morto vedrebbe la prima
        # pagina come un anonimo qualunque senza capire perche'.
        return self._redirect("/?eliminato=1", [
            ("Set-Cookie", f"{COOKIE}=; Max-Age=0; Path=/")])

    def pagina_recupera(self, conn, errore="", msg=""):
        corpo = f"""
<div class="card" style="max-width:440px;margin:40px auto">
<h1>Password dimenticata</h1>
<p class="sub">Scrivi la tua email: se l'indirizzo è registrato ti arriva un
collegamento per rimetterla, valido un'ora.</p>
<form method="post" action="/recupera">
<label>Email</label><input name="email" type="email" required autofocus>
<button style="width:100%">Mandami il collegamento</button>
</form>
<p class="sub" style="margin-top:16px;font-size:13px">
Se la posta non è configurata su questo server, il collegamento non può partire:
in quel caso chiedi a un amministratore della stazione di rimettertela dal
pannello.</p>
<p style="margin-top:14px"><a href="/accedi">← torna all'accesso</a></p></div>"""
        return self._send(200, page("password dimenticata", corpo, None, msg, errore))

    def post_recupera(self, conn, dati):
        if self._freno():
            return self._send(429, page("troppi tentativi",
                                        "<h1>Troppe richieste</h1>"
                                        "<p class='sub'>Riprova fra qualche minuto.</p>"))
        self._segna_tentativo()
        email = str(dati.get("email", "")).strip()
        u = db.user_by_email(conn, email)

        # La risposta e' la stessa che l'indirizzo esista o no: dire "questa
        # email non risulta" permetterebbe a chiunque di scoprire chi ha un
        # accesso a questo gateway.
        risposta = ("Se l'indirizzo è registrato, il collegamento per rimettere "
                    "la password è appena partito. Controlla la posta.")

        if u:
            scade = int(time.time()) + RESET_TTL
            base = mail.BASE_URL or f"https://{self.headers.get('Host', '')}"
            link = f"{base}/reimposta?t={urllib.parse.quote(gettone_reset(u, scade))}"
            if mail.attiva():
                mail.invia(u["email"], "Decolink: rimetti la tua password",
                           f"Per rimettere la password di {u['callsign']} apri questo "
                           f"collegamento entro un'ora:\n\n{link}\n\n"
                           f"Se non hai chiesto tu di cambiarla, ignora questo messaggio: "
                           f"la password attuale resta valida.")
                print(f"  collegamento di recupero spedito a {u['callsign']}")
            else:
                # Senza posta configurata il collegamento non puo' partire. Si
                # scrive nel registro del servizio, cosi' chi amministra la
                # macchina puo' prenderlo e consegnarlo a mano: e' l'unico modo
                # onesto di non lasciare la gente chiusa fuori.
                print(f"  [posta non configurata] collegamento di recupero per "
                      f"{u['callsign']} <{u['email']}>:\n      {link}")
        return self._send(200, self.form_accesso(msg=risposta))

    def pagina_reimposta(self, conn, gettone, errore=""):
        u = utente_da_gettone(conn, gettone)
        if not u:
            corpo = """<div class="card" style="max-width:440px;margin:40px auto">
<h1>Collegamento non più valido</h1>
<p class="sub">È scaduto, è già stato usato, oppure la password è stata cambiata
nel frattempo. Chiedine un altro.</p>
<p><a href="/recupera">← richiedi un nuovo collegamento</a></p></div>"""
            return self._send(400, page("non valido", corpo))
        corpo = f"""
<div class="card" style="max-width:440px;margin:40px auto">
<h1>Nuova password</h1>
<p class="sub">Per <b>{e(u['callsign'])}</b> &lt;{e(u['email'])}&gt;</p>
<form method="post" action="/reimposta">
<input type="hidden" name="t" value="{e(gettone)}">
<label>Nuova password</label><input name="nuova" type="password" required minlength="8"
  autofocus placeholder="almeno 8 caratteri">
<label>Ripeti</label><input name="ripeti" type="password" required minlength="8">
<button style="width:100%">Imposta</button>
</form></div>"""
        return self._send(200, page("nuova password", corpo, None, "", errore))

    def post_reimposta(self, conn, dati):
        gettone = str(dati.get("t", ""))
        u = utente_da_gettone(conn, gettone)
        if not u:
            return self.pagina_reimposta(conn, gettone)
        nuova, ripeti = str(dati.get("nuova", "")), str(dati.get("ripeti", ""))
        if len(nuova) < 8:
            return self.pagina_reimposta(conn, gettone, "Almeno 8 caratteri.")
        if nuova != ripeti:
            return self.pagina_reimposta(conn, gettone, "Le due password non coincidono.")
        db.set_password(conn, u["id"], nuova)
        print(f"  {u['callsign']} ha rimesso la password con un collegamento di recupero")
        return self._send(200, self.form_accesso(
            msg="Password impostata. Ora puoi entrare."))

    def post_reimposta_admin(self, conn, utente, dati):
        """Un amministratore rimette la password di qualcun altro.

        Serve quando la posta non e' configurata, che e' la condizione normale di
        un gateway appena messo in piedi: senza questo, chi dimentica la password
        resta fuori e l'unico rimedio sarebbe entrare nel server.
        """
        if not utente["is_admin"]:
            return self._send(403, page("vietato", "<h1>Riservato agli amministratori</h1>", utente))
        try:
            uid = int(dati.get("user", 0))
        except ValueError:
            return self._redirect("/admin")
        u = db.user_by_id(conn, uid)
        if not u:
            return self._redirect("/admin")
        nuova = secrets.token_urlsafe(9)
        db.set_password(conn, uid, nuova)
        print(f"  {utente['callsign']} rimette la password di {u['callsign']}")
        corpo = f"""<h1>Password rimessa per {e(u['callsign'])}</h1>
<div class="card"><p>Consegnala a mano e falla cambiare al primo accesso:</p>
<div class="mono">{e(nuova)}</div></div>
<div class="msg err">Vale finché non la cambia. Se il messaggio con cui gliela
mandi resta in giro, resta in giro anche l'accesso.</div>
<p><a href="/admin">← torna all'amministrazione</a></p>"""
        return self._send(200, page("password rimessa", corpo, utente))

    def api_stazioni(self, conn):
        """Elenco pubblico delle stazioni: serve solo a popolare la tendina
        della registrazione, quindi non espone nulla oltre al nome."""
        return self._json(200, {"stations": [
            {"slug": s["slug"], "name": s["name"], "callsign": s["callsign"]}
            for s in db.list_stations(conn) if s["enabled"]]})


def main():
    ap = argparse.ArgumentParser(description="Servizio di accesso di Decolink")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--db", default=db.default_path())
    ap.add_argument("--cert", help="certificato TLS (con --key serve HTTPS direttamente)")
    ap.add_argument("--key", help="chiave privata TLS")
    args = ap.parse_args()

    # Log riga per riga: sotto systemd lo stdout e' un tubo, non un terminale, e
    # senza questo "journalctl -f" non mostrerebbe niente in tempo reale.
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    global SECRET, DB_PATH, HTTPS
    DB_PATH = args.db
    SECRET = tok.load_secret(SECRET_PATH)
    HTTPS = bool(args.cert and args.key)

    conn = db.connect(DB_PATH)
    n_utenti = len(db.list_users(conn))
    conn.close()

    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    if HTTPS:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(args.cert, args.key)
        srv.socket = ctx.wrap_socket(srv.socket, server_side=True)

    schema = "https" if HTTPS else "http"
    print(f"Decolink — servizio di accesso su {schema}://{args.host}:{args.port}")
    print(f"  database: {DB_PATH}  ({n_utenti} utenti)")
    print(f"  chiave di firma: {SECRET_PATH}")
    if not HTTPS:
        print("  ATTENZIONE: HTTP in chiaro. Mettilo dietro nginx con HTTPS,")
        print("              altrimenti le password viaggiano leggibili.")
    if n_utenti == 0:
        print("  Nessun utente: crea il primo amministratore con")
        print("      python3 decolink_admin.py init")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nservizio chiuso.")


if __name__ == "__main__":
    main()
