#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Piu' operatori sulla stessa radio: un solo PTT, primo arrivato primo servito.

Come MultiFLEX di FlexRadio: tutti possono ascoltare e guardare la radio, ma
finche' uno trasmette gli altri non possono alzare il PTT, abbassarglielo ne'
cambiare frequenza o modo. Il relay lo fa rispettare sia sull'audio da
trasmettere sia sui comandi CAT, e dice a ciascuno chi ha il PTT.
"""
import os
import socket
import struct
import subprocess
import sys
import time

SRV = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRV)
TMP = os.path.join(SRV, "_prova_multiop")
os.makedirs(TMP, exist_ok=True)
DB, KEY = os.path.join(TMP, "m.db"), os.path.join(TMP, "m.key")
PORT = 5698
for f in (DB, KEY, DB + "-wal", DB + "-shm"):
    if os.path.exists(f):
        os.remove(f)
env = dict(os.environ, DECOLINK_DB=DB, DECOLINK_SECRET=KEY, PYTHONIOENCODING="utf-8")
import decolink_db as db          # noqa: E402
import decolink_token as tok      # noqa: E402
import decolink_relay as rl       # noqa: E402

ok = err = 0


def verifica(nome, cond, extra=""):
    global ok, err
    if cond:
        ok += 1
        print(f"  OK   {nome}")
    else:
        err += 1
        print(f"  FALLITO  {nome}  {extra}")


print("== come il relay legge i comandi CAT ==")
tabella = [
    ("f", "legge"), ("m\n", "legge"), ("t", "legge"), ("l STRENGTH", "legge"), ("s", "legge"),
    ("\\get_freq", "legge"), ("\\dump_state", "legge"),
    ("F 14074000", "scrive"), ("M PKTUSB 0", "scrive"), ("S 1 VFOB", "scrive"),
    ("I 14080000", "scrive"), ("L RFPOWER 0.5", "scrive"), ("w BY;", "scrive"),
    ("\\set_freq 7074000", "scrive"), ("\\send_cmd TX1;", "scrive"),
    ("T 1", "ptt_on"), ("T 3", "ptt_on"), ("T 0", "ptt_off"),
    ("\\set_ptt 1", "ptt_on"), ("\\set_ptt 0", "ptt_off"), ("+T 1", "ptt_on"),
    ("T", "scrive"), ("T x", "scrive"), ("", "legge"),
]
for riga, atteso in tabella:
    verifica(f"{riga!r} -> {atteso}", rl.classifica_cat(riga) == atteso, rl.classifica_cat(riga))

# Un titolare, due operatori, un ascoltatore.
c = db.connect(DB)
own = db.create_user(c, "own@t.it", "IU8LMC", "provaprova", status=db.ST_ACTIVE, is_admin=True)
ua = db.create_user(c, "a@t.it", "K1ABC", "provaprova", status=db.ST_ACTIVE)
ub = db.create_user(c, "b@t.it", "DL1XYZ", "provaprova", status=db.ST_ACTIVE)
ul = db.create_user(c, "l@t.it", "F4MXE", "provaprova", status=db.ST_ACTIVE)
st = db.create_station(c, "shack", own, name="Shack")
db.grant(c, ua, st, "opr", own)
db.grant(c, ub, st, "opr", own)
db.grant(c, ul, st, "lst", own)
c.close()
seg = tok.load_secret(KEY)
t_gw = tok.issue(seg, user_id=own, callsign="IU8LMC", station_id=st, role="own")
t_a = tok.issue(seg, user_id=ua, callsign="K1ABC", station_id=st, role="opr")
t_b = tok.issue(seg, user_id=ub, callsign="DL1XYZ", station_id=st, role="opr")
t_l = tok.issue(seg, user_id=ul, callsign="F4MXE", station_id=st, role="lst")

relay = subprocess.Popen([sys.executable, "decolink_relay.py", str(PORT)], cwd=SRV, env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                         encoding="utf-8", errors="replace")
time.sleep(2)

H = struct.Struct("!4sBBIQI")
F_AUDIO, F_REGISTER, F_PEERUP, F_CATREQ, F_CATRSP, F_TX, F_DENIED, F_TXSTATE = 0, 3, 4, 5, 6, 7, 8, 9


def v2(flags, payload=b"", seq=0):
    return H.pack(b"HFGW", 2, flags, seq, 0, 48000) + payload


def v3cat(testo, seq=1):
    return bytes([0x44, (3 << 4) | 3, 0, 0, seq >> 8, seq & 255, 0, 0, 0, 0]) + testo.encode()


def apri():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.3)
    return s


def manda(s, d):
    s.sendto(d, ("127.0.0.1", PORT))


def tutti(s, attesa=0.5):
    """Tutto quel che arriva entro `attesa` secondi: lista di (flag, corpo)."""
    out = []
    s.settimeout(attesa)
    while True:
        try:
            d, _ = s.recvfrom(8192)
        except socket.timeout:
            break
        if d[:4] == b"HFGW":
            out.append((d[5], d[22:]))
        else:
            out.append(("v3", d))
        s.settimeout(0.15)
    return out


def stati(lista):
    return [c.decode() for f, c in lista if f == F_TXSTATE]


gw, a, b, l = apri(), apri(), apri(), apri()
manda(gw, v2(F_REGISTER, f"gw {t_gw}".encode()))
manda(a, v2(F_REGISTER, f"op {t_a}".encode()))
manda(b, v2(F_REGISTER, f"op {t_b}".encode()))
manda(l, v2(F_REGISTER, f"op {t_l}".encode()))
for s in (gw, a, b, l):
    tutti(s, 0.8)

print("\n== chi entra vede la stazione libera ==")
c2 = apri()
manda(c2, v2(F_REGISTER, f"op {t_b}".encode()))      # nuova sessione dello stesso utente: sostituisce la vecchia
r = tutti(c2, 0.8)
verifica("il nuovo operatore riceve 'tx free'", "tx free" in stati(r), r)
b.close()
b = c2
tutti(a, 0.4)

print("\n== il primo che alza il PTT lo ottiene ==")
manda(a, v2(F_CATREQ, b"T 1\n", seq=11))
r_gw = tutti(gw)
verifica("il comando T 1 di K1ABC arriva alla radio", any(f == F_CATREQ and c.strip() == b"T 1" for f, c in r_gw), r_gw)
verifica("anche il gateway sa chi trasmette ('tx busy K1ABC')", "tx busy K1ABC" in stati(r_gw), r_gw)
r_a, r_b = tutti(a), tutti(b)
verifica("K1ABC vede 'tx you'", "tx you" in stati(r_a), r_a)
verifica("DL1XYZ vede 'tx busy K1ABC'", "tx busy K1ABC" in stati(r_b), r_b)

print("\n== gli altri guardano ma non toccano ==")
manda(b, v2(F_CATREQ, b"T 1\n", seq=21))
r_b, r_gw = tutti(b), tutti(gw)
verifica("DL1XYZ non puo' alzare il PTT: risposta RPRT -8",
         any(f == F_CATRSP and c.startswith(b"RPRT -8") for f, c in r_b), r_b)
verifica("e la radio non sente niente", not r_gw, r_gw)

manda(b, v2(F_CATREQ, b"F 7074000\n", seq=22))
r_b, r_gw = tutti(b), tutti(gw)
verifica("DL1XYZ non puo' cambiare frequenza mentre K1ABC trasmette",
         any(f == F_CATRSP and c.startswith(b"RPRT -8") for f, c in r_b) and not r_gw, (r_b, r_gw))

manda(b, v2(F_CATREQ, b"M USB 0\n", seq=23))
r_b, r_gw = tutti(b), tutti(gw)
verifica("ne' modo", any(f == F_CATRSP and c.startswith(b"RPRT -8") for f, c in r_b) and not r_gw, (r_b, r_gw))

manda(b, v2(F_CATREQ, b"T 0\n", seq=24))
r_b, r_gw = tutti(b), tutti(gw)
verifica("e non puo' abbassare il PTT a chi sta trasmettendo",
         any(f == F_CATRSP and c.startswith(b"RPRT -8") for f, c in r_b) and not r_gw, (r_b, r_gw))

manda(b, v2(F_CATREQ, b"f\n", seq=25))
manda(b, v2(F_CATREQ, b"l STRENGTH\n", seq=26))
r_gw = tutti(gw)
verifica("puo' invece leggere frequenza e S-meter",
         sum(1 for f, c in r_gw if f == F_CATREQ) == 2, r_gw)

manda(b, v2(F_TX, b"\x01" * 240))
r_gw = tutti(gw)
verifica("il suo audio da trasmettere non passa", not any(f == F_TX for f, c in r_gw), r_gw)
manda(a, v2(F_TX, b"\x02" * 240))
r_gw = tutti(gw)
verifica("quello di chi ha il PTT si", any(f == F_TX for f, c in r_gw), r_gw)

print("\n== lo stesso vale con il protocollo v3 ==")
manda(b, v3cat("F 14074000\n", 31))
r_b, r_gw = tutti(b), tutti(gw)
verifica("comando di scrittura v3 rifiutato con RPRT -8",
         any(f == "v3" and c[10:].startswith(b"RPRT -8") for f, c in r_b) and not r_gw, (r_b, r_gw))
manda(b, v3cat("t\n", 32))
r_gw = tutti(gw)
verifica("lettura v3 inoltrata", any(f == "v3" and c[10:].startswith(b"t") for f, c in r_gw), r_gw)

print("\n== ascoltatore: ne' PTT ne' comandi ==")
manda(l, v2(F_CATREQ, b"T 1\n", seq=41))
r_l, r_gw = tutti(l), tutti(gw)
verifica("l'ascoltatore e' ignorato", not r_gw and not any(f == F_CATRSP and c.startswith(b"RPRT 0") for f, c in r_l), (r_l, r_gw))

print("\n== chi finisce libera la stazione ==")
manda(a, v2(F_CATREQ, b"T 0\n", seq=51))
r_gw = tutti(gw)
verifica("il T 0 di K1ABC arriva alla radio", any(f == F_CATREQ and c.strip() == b"T 0" for f, c in r_gw), r_gw)
verifica("il gateway vede 'tx free'", "tx free" in stati(r_gw), r_gw)
r_a, r_b = tutti(a), tutti(b)
verifica("tutti vedono 'tx free'", "tx free" in stati(r_a) and "tx free" in stati(r_b), (r_a, r_b))

manda(b, v2(F_CATREQ, b"T 1\n", seq=61))
r_gw = tutti(gw)
verifica("ora DL1XYZ lo ottiene", any(f == F_CATREQ and c.strip() == b"T 1" for f, c in r_gw), r_gw)
r_a = tutti(a)
verifica("K1ABC vede 'tx busy DL1XYZ'", "tx busy DL1XYZ" in stati(r_a), r_a)

print("\n== chi sparisce senza lasciare il PTT non blocca la stazione ==")
manda(a, v2(F_CATREQ, b"T 1\n", seq=71))
r_a = tutti(a)
verifica("subito dopo, K1ABC e' ancora respinto", any(f == F_CATRSP and c.startswith(b"RPRT -8") for f, c in r_a), r_a)
tutti(gw)
time.sleep(rl.TX_IDLE + rl.TX_GRACE + 0.8)       # DL1XYZ non manda piu' audio e non abbassa il PTT
manda(a, v2(F_CATREQ, b"T 1\n", seq=72))
r_gw = tutti(gw)
verifica("scaduto il periodo di grazia K1ABC lo ottiene",
         any(f == F_CATREQ and c.strip() == b"T 1" for f, c in r_gw), r_gw)

for s in (gw, a, b, l):
    s.close()
relay.terminate()
try:
    log, _ = relay.communicate(timeout=5)
except subprocess.TimeoutExpired:
    relay.kill()
    log = ""
print(f"\n=== {ok} verifiche superate, {err} fallite ===")
if err:
    print(log[-1500:])
for f in (DB, KEY, DB + "-wal", DB + "-shm"):
    if os.path.exists(f):
        try:
            os.remove(f)
        except OSError:
            pass
try:
    os.rmdir(TMP)
except OSError:
    pass
sys.exit(1 if err else 0)
