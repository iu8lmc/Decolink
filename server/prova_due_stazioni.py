#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Due stazioni devono essere due stanze separate: niente audio ne' comandi
che passino dall'una all'altra."""
import os
import socket
import struct
import subprocess
import sys
import time

SRV = r"C:\hf-gateway\server"
TMP = os.path.dirname(os.path.abspath(__file__))
DB, KEY = os.path.join(TMP, "due.db"), os.path.join(TMP, "due.key")
PORT = 5597
for f in (DB, KEY, DB + "-wal", DB + "-shm"):
    if os.path.exists(f):
        os.remove(f)
env = dict(os.environ, DECOLINK_DB=DB, DECOLINK_SECRET=KEY, PYTHONIOENCODING="utf-8")
sys.path.insert(0, SRV)
import decolink_db as db          # noqa: E402
import decolink_token as tok      # noqa: E402

ok = err = 0


def verifica(nome, cond, extra=""):
    global ok, err
    if cond:
        ok += 1
        print(f"  OK   {nome}")
    else:
        err += 1
        print(f"  FALLITO  {nome}  {extra}")


# Due operatori, due radio, due stazioni: come Caserta e Malta.
c = db.connect(DB)
u_it = db.create_user(c, "it@t.it", "IU8LMC", "provaprova", status=db.ST_ACTIVE, is_admin=True)
u_mt = db.create_user(c, "mt@t.it", "9H1SR", "provaprova", status=db.ST_ACTIVE)
s_it = db.create_station(c, "decodium", u_it, name="Caserta")
s_mt = db.create_station(c, "9h1sr-malta", u_mt, name="Malta")
c.close()

seg = tok.load_secret(KEY)
gw_it = tok.issue(seg, user_id=u_it, callsign="IU8LMC", station_id=s_it, role="own")
op_it = tok.issue(seg, user_id=u_it, callsign="IU8LMC", station_id=s_it, role="own")
gw_mt = tok.issue(seg, user_id=u_mt, callsign="9H1SR", station_id=s_mt, role="own")
op_mt = tok.issue(seg, user_id=u_mt, callsign="9H1SR", station_id=s_mt, role="own")

relay = subprocess.Popen([sys.executable, "decolink_relay.py", str(PORT)], cwd=SRV, env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                         encoding="utf-8", errors="replace")
time.sleep(2)

H = struct.Struct("!4sBBIQI")
F_AUDIO, F_REGISTER, F_CATREQ, F_CATRSP, F_TX, F_DENIED = 0, 3, 5, 6, 7, 8


def v2(flags, payload=b""):
    return H.pack(b"HFGW", 2, flags, 0, 0, 48000) + payload


def apri():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2.0)
    return s


def manda(s, d):
    s.sendto(d, ("127.0.0.1", PORT))


def leggi(s):
    try:
        d, _ = s.recvfrom(8192)
        return d[5], d[22:]
    except socket.timeout:
        return None, b""


def svuota(*socks):
    for s in socks:
        s.settimeout(0.4)
        while leggi(s)[0] is not None:
            pass
        s.settimeout(2.0)


radio_it, app_it = apri(), apri()
radio_mt, app_mt = apri(), apri()

print("\n== ognuno entra nella propria stazione ==")
manda(radio_it, v2(F_REGISTER, f"gw {gw_it}".encode()))
verifica("la radio di Caserta entra", leggi(radio_it)[0] == F_REGISTER)
manda(app_it, v2(F_REGISTER, f"op {op_it}".encode()))
verifica("l'app di Caserta entra", leggi(app_it)[0] == F_REGISTER)
manda(radio_mt, v2(F_REGISTER, f"gw {gw_mt}".encode()))
verifica("la radio di Malta entra", leggi(radio_mt)[0] == F_REGISTER)
manda(app_mt, v2(F_REGISTER, f"op {op_mt}".encode()))
verifica("l'app di Malta entra", leggi(app_mt)[0] == F_REGISTER)
svuota(radio_it, app_it, radio_mt, app_mt)

print("\n== due radio insieme: prima era impossibile, ora sono stanze diverse ==")
verifica("due gateway coesistono, uno per stazione", True)

print("\n== l'audio resta nella sua stazione ==")
manda(radio_it, v2(F_AUDIO, b"\xaa" * 480))
f, corpo = leggi(app_it)
verifica("l'app di Caserta sente la sua radio", f == F_AUDIO and len(corpo) == 480, (f, len(corpo)))
f, _ = leggi(app_mt)
verifica("l'app di Malta NON sente la radio di Caserta", f is None, f)

manda(radio_mt, v2(F_AUDIO, b"\xbb" * 480))
f, corpo = leggi(app_mt)
verifica("l'app di Malta sente la sua radio", f == F_AUDIO and len(corpo) == 480, (f, len(corpo)))
f, _ = leggi(app_it)
verifica("l'app di Caserta NON sente la radio di Malta", f is None, f)

print("\n== i comandi restano nella loro stazione ==")
svuota(radio_it, app_it, radio_mt, app_mt)
# Malta cambia frequenza: e' il caso segnalato
manda(app_mt, v2(F_CATREQ, b"F 14074000\n"))
f, corpo = leggi(radio_mt)
verifica("il comando di Malta arriva alla radio di Malta",
         f == F_CATREQ and b"14074000" in corpo, (f, corpo))
f, corpo = leggi(radio_it)
verifica("e NON arriva alla radio di Caserta", f is None, (f, corpo))
f, corpo = leggi(app_it)
verifica("e NON si vede sull'app di Caserta", f is None, (f, corpo))

print("\n== la risposta torna solo a chi ha chiesto ==")
manda(radio_mt, v2(F_CATRSP, b"RPRT 0\n"))
f, corpo = leggi(app_mt)
verifica("la risposta arriva all'app di Malta", f == F_CATRSP, (f, corpo))
f, _ = leggi(app_it)
verifica("l'app di Caserta non vede la risposta altrui", f is None, f)

print("\n== l'audio da trasmettere non attraversa le stazioni ==")
svuota(radio_it, app_it, radio_mt, app_mt)
manda(app_mt, v2(F_TX, b"\xcc" * 480))
f, _ = leggi(radio_mt)
verifica("la trasmissione di Malta va alla sua radio", f == F_TX, f)
f, _ = leggi(radio_it)
verifica("e non tocca la radio di Caserta", f is None, f)

for s in (radio_it, app_it, radio_mt, app_mt):
    s.close()
relay.terminate()
try:
    relay.communicate(timeout=5)
except subprocess.TimeoutExpired:
    relay.kill()
print(f"\n=== {ok} verifiche superate, {err} fallite ===")
for f in (DB, KEY, DB + "-wal", DB + "-shm"):
    if os.path.exists(f):
        try:
            os.remove(f)
        except OSError:
            pass
sys.exit(1 if err else 0)
