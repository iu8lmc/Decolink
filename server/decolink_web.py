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
import html
import json
import os
import re
import secrets
import ssl
import sys
import time
import urllib.parse
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

CSS = """
:root { color-scheme: dark }
* { box-sizing: border-box }
body { margin:0; background:#12151a; color:#dfe4ea; font:15px/1.5 system-ui,Segoe UI,sans-serif }
a { color:#5fd08a; text-decoration:none } a:hover { text-decoration:underline }
header { background:#0d1014; border-bottom:1px solid #232a33; padding:14px 22px;
         display:flex; align-items:center; gap:16px; flex-wrap:wrap }
header .logo { font-weight:700; letter-spacing:.5px; color:#5fd08a }
header .sp { flex:1 }
main { max-width:960px; margin:0 auto; padding:22px }
h1 { font-size:21px; margin:0 0 4px } h2 { font-size:17px; margin:26px 0 10px; color:#9fb0c0 }
.sub { color:#7d8b99; margin:0 0 20px }
.card { background:#171b21; border:1px solid #232a33; border-radius:10px; padding:18px; margin-bottom:18px }
label { display:block; margin:12px 0 5px; color:#9fb0c0; font-size:13px }
input,select { width:100%; padding:9px 11px; background:#0f1216; color:#dfe4ea;
               border:1px solid #2c3542; border-radius:7px; font-size:15px }
input:focus,select:focus { outline:none; border-color:#5fd08a }
button { background:#5fd08a; color:#0d1014; border:0; border-radius:7px; padding:9px 16px;
         font-size:15px; font-weight:600; cursor:pointer; margin-top:14px }
button:hover { background:#74dc9c }
button.ghost { background:transparent; color:#9fb0c0; border:1px solid #2c3542; font-weight:400 }
button.danger { background:#c9553f; color:#fff }
button.small { padding:5px 10px; font-size:13px; margin:0 }
table { width:100%; border-collapse:collapse; margin-top:8px }
th,td { text-align:left; padding:8px 10px; border-bottom:1px solid #232a33; font-size:14px }
th { color:#7d8b99; font-weight:500; font-size:12px; text-transform:uppercase; letter-spacing:.4px }
.tag { display:inline-block; padding:2px 8px; border-radius:20px; font-size:12px }
.own { background:#2d4a63; color:#b3d9f5 } .opr { background:#2c5340; color:#9ee6b8 }
.lst { background:#3a3a44; color:#c3c3cf }
.pending { background:#5c4a22; color:#f0d190 } .active { background:#2c5340; color:#9ee6b8 }
.suspended { background:#5b2b2b; color:#f0a9a9 }
.msg { padding:11px 14px; border-radius:8px; margin-bottom:16px }
.err { background:#3a1f1f; border:1px solid #6b3232; color:#f0b4b4 }
.ok  { background:#1c3527; border:1px solid #2f5c42; color:#a6e8c1 }
.mono { font-family:Consolas,monospace; font-size:13px; word-break:break-all;
        background:#0f1216; padding:10px; border-radius:6px; border:1px solid #2c3542 }
.inline { display:inline } .row { display:flex; gap:8px; align-items:center; flex-wrap:wrap }
footer { color:#5a6673; font-size:12px; text-align:center; padding:24px }
"""


def e(s) -> str:
    """Testo pronto per finire dentro l'HTML. Ogni valore che arriva da un
    utente passa di qui: e' l'unica difesa contro chi si registra con un
    nominativo pieno di tag."""
    return html.escape("" if s is None else str(s), quote=True)


def page(titolo: str, corpo: str, utente=None, msg: str = "", errore: str = "") -> bytes:
    nav = ""
    if utente:
        nav = (f'<span>{e(utente["callsign"])}</span>'
               f'<a href="/">stazioni</a>')
        if utente["is_admin"]:
            nav += '<a href="/admin">amministrazione</a>'
        nav += ('<form method="post" action="/esci" class="inline">'
                '<button class="ghost small">esci</button></form>')
    avviso = ""
    if errore:
        avviso += f'<div class="msg err">{e(errore)}</div>'
    if msg:
        avviso += f'<div class="msg ok">{e(msg)}</div>'
    doc = f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titolo)} — Decolink</title><style>{CSS}</style></head><body>
<header><span class="logo">DECOLINK</span><span class="sp"></span>{nav}</header>
<main>{avviso}{corpo}</main>
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
            if percorso == "/":
                return self.pagina_home(conn, utente)
            if percorso == "/accedi":
                return self._send(200, self.form_accesso())
            if percorso == "/registrati":
                return self._send(200, self.form_registrazione(conn))
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

            utente = self._utente(conn)
            if not utente:
                return self._redirect("/accedi")
            if not self._csrf_ok(conn, utente, dati):
                return self._send(400, page("errore", "<h1>Richiesta non valida</h1>"
                                            "<p class='sub'>Ricarica la pagina e riprova.</p>", utente))
            if percorso == "/esci":
                db.drop_web_session(conn, self._cookie(COOKIE))
                return self._redirect("/accedi", [("Set-Cookie", f"{COOKIE}=; Max-Age=0; Path=/")])
            if percorso == "/membro":
                return self.post_membro(conn, utente, dati)
            if percorso == "/stato-utente":
                return self.post_stato_utente(conn, utente, dati)
            if percorso == "/stazione-nuova":
                return self.post_stazione_nuova(conn, utente, dati)
            if percorso == "/stazione-stato":
                return self.post_stazione_stato(conn, utente, dati)
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
<p style="margin-top:18px;color:#7d8b99">Non hai un accesso?
<a href="/registrati">Richiedilo</a>.</p></div>"""
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
            return self._send(200, self.form_accesso())
        if utente["status"] != db.ST_ACTIVE:
            corpo = f"""<div class="card"><h1>Accesso in attesa</h1>
<p class="sub">La richiesta di <b>{e(utente['callsign'])}</b> è stata registrata
ma non è ancora stata approvata. Fino ad allora non è possibile collegarsi ad
alcuna stazione.</p></div>"""
            return self._send(200, page("in attesa", corpo, utente))

        righe = ""
        for s in db.stations_of(conn, utente["id"]):
            gestisci = (f'<a href="/stazione/{e(s["slug"])}">gestisci</a>'
                        if s["role"] == tok.ROLE_OWNER or utente["is_admin"] else "")
            righe += (f'<tr><td><b>{e(s["slug"])}</b></td><td>{e(s["name"])}</td>'
                      f'<td>{e(s["callsign"])}</td>'
                      f'<td><span class="tag {e(s["role"])}">{e(RUOLI_IT[s["role"]])}</span></td>'
                      f'<td>{gestisci}</td></tr>')
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
<div class="mono">{e(self.headers.get('Host', ''))}</div></div>"""
        return self._send(200, page("stazioni", corpo, utente))

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
<tr><th>entrato</th><th>chi</th><th>ruolo</th><th>uscito</th><th>indirizzo</th></tr>{cn}</table></div>"""
        return self._send(200, page(f"stazione {slug}", corpo, utente))

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
