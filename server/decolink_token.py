#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decolink_token.py — token di accesso firmati, condivisi fra il servizio web e
il relay.

Perche' un token firmato e non una ricerca nel database: il relay riceve
centinaia di pacchetti al secondo per ogni collegamento e non puo' permettersi
una query per stabilire chi sia il mittente. Il servizio web (che il database
ce l'ha) firma un foglietto di carta che dice "questo e' Tizio, sulla stazione
3, come operatore, fino alle 18:40"; il relay controlla solo la firma, che gli
costa una hash, e si fida per tutta la durata.

Il prezzo di questa scelta e' che un token resta valido fino alla scadenza
anche se nel frattempo l'utente viene sospeso. Per questo la durata e' breve
(il client lo rinnova da solo) e il relay tiene comunque una lista di revoche
che ricontrolla ogni pochi secondi: vedi decolink_db.revoked_ids().

Solo libreria standard. Chiave e formato devono restare identici fra web e
relay, quindi questo file e' l'unico posto dove si toccano.
"""

from __future__ import annotations   # annotazioni come testo: gira anche su Python 3.8

import base64
import hashlib
import hmac
import json
import os
import secrets
import time

# Sigla di versione in testa al token: se un domani cambia il formato, i token
# vecchi vengono rifiutati subito invece di fallire in modo oscuro sulla firma.
PREFIX = "dl1"

# Ruoli, dal piu' potente al piu' innocuo. Sono stringhe corte perche' finiscono
# dentro un pacchetto UDP.
ROLE_OWNER = "own"       # titolare della stazione: opera e amministra i membri
ROLE_OPERATOR = "opr"    # puo' trasmettere: TX audio e comandi CAT
ROLE_LISTENER = "lst"    # solo ascolto: niente PTT, niente CAT
ROLES = (ROLE_OWNER, ROLE_OPERATOR, ROLE_LISTENER)

# Chi puo' mandare la radio in aria. Il relay usa esattamente questo insieme per
# decidere se inoltrare TX audio e comandi CAT.
TX_ROLES = frozenset({ROLE_OWNER, ROLE_OPERATOR})

DEFAULT_TTL = 3600  # 1 h: abbastanza per non disturbare, poco per limitare i danni


class TokenError(Exception):
    """Token assente, scaduto, manomesso o di formato sconosciuto."""


def _b64e(raw: bytes) -> str:
    # Senza padding: il token viaggia in un datagramma, ogni byte e' spazio tolto
    # all'audio, e i '=' finali non aggiungono informazione.
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64d(txt: str) -> bytes:
    return base64.urlsafe_b64decode(txt + "=" * (-len(txt) % 4))


def load_secret(path: str) -> bytes:
    """Legge la chiave di firma, creandola al primo avvio.

    Va creata una volta sola e condivisa fra servizio web e relay: se i due
    processi usassero chiavi diverse, ogni token risulterebbe falso e nessuno
    riuscirebbe piu' a collegarsi. Il file viene scritto con permessi 0600
    perche' chi lo legge puo' fabbricarsi un token da titolare di stazione.
    """
    if os.path.exists(path):
        with open(path, "rb") as f:
            raw = f.read().strip()
        if len(raw) >= 32:
            return raw
        # Un file troppo corto e' quasi certamente un residuo di una prova
        # andata male: meglio fermarsi che firmare con una chiave debole.
        raise TokenError(f"chiave di firma troppo corta in {path}")

    raw = secrets.token_bytes(48)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, raw)
    finally:
        os.close(fd)
    return raw


def issue(secret: bytes, *, user_id: int, callsign: str, station_id: int,
          role: str, ttl: int = DEFAULT_TTL, now: float | None = None) -> str:
    """Firma un token per un utente su una stazione.

    Il nominativo viaggia dentro al token perche' il relay lo scrive nei log
    delle trasmissioni: chi ha operato la radio deve risultare senza dover
    interrogare nessuno, anche a distanza di tempo.
    """
    if role not in ROLES:
        raise TokenError(f"ruolo sconosciuto: {role}")
    now = time.time() if now is None else now
    body = {
        "u": int(user_id),
        "c": callsign.upper()[:16],
        "s": int(station_id),
        "r": role,
        "x": int(now + ttl),
        "i": _b64e(secrets.token_bytes(9)),   # identificativo, serve alle revoche
    }
    raw = json.dumps(body, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload = _b64e(raw)
    sig = hmac.new(secret, f"{PREFIX}.{payload}".encode("ascii"), hashlib.sha256).digest()
    # Meta' firma: 16 byte sono fuori portata per un attacco a forza bruta e
    # risparmiano spazio nel datagramma.
    return f"{PREFIX}.{payload}.{_b64e(sig[:16])}"


def verify(secret: bytes, token: str, *, now: float | None = None) -> dict:
    """Controlla firma e scadenza e restituisce i dati del token.

    Solleva TokenError in ogni caso storto. Non tocca il database: la revoca e'
    un controllo separato, a carico di chi chiama.
    """
    if not token:
        raise TokenError("token assente")
    parts = token.split(".")
    if len(parts) != 3 or parts[0] != PREFIX:
        raise TokenError("formato del token non riconosciuto")

    _, payload, sig = parts
    atteso = hmac.new(secret, f"{PREFIX}.{payload}".encode("ascii"), hashlib.sha256).digest()[:16]
    try:
        dato = _b64d(sig)
    except Exception:
        raise TokenError("firma illeggibile")
    # compare_digest e non ==: il confronto normale esce al primo byte diverso e
    # il tempo che ci mette racconta quanto ci si e' avvicinati alla firma giusta.
    if not hmac.compare_digest(atteso, dato):
        raise TokenError("firma non valida")

    try:
        body = json.loads(_b64d(payload))
    except Exception:
        raise TokenError("contenuto del token illeggibile")

    now = time.time() if now is None else now
    if float(body.get("x", 0)) < now:
        raise TokenError("token scaduto")
    if body.get("r") not in ROLES:
        raise TokenError("ruolo sconosciuto nel token")

    return {
        "user_id": int(body["u"]),
        "callsign": str(body.get("c", "")),
        "station_id": int(body["s"]),
        "role": str(body["r"]),
        "expires": int(body["x"]),
        "jti": str(body.get("i", "")),
    }


def can_transmit(role: str) -> bool:
    """Se questo ruolo puo' mandare la radio in aria."""
    return role in TX_ROLES
