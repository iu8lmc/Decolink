#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decolink_db.py — database del gateway: utenti, stazioni, permessi, log.

SQLite e non un database vero perche' qui si parla di decine o centinaia di
soci, non di milioni: sta in un file, non ha un servizio da tenere in piedi ed
e' nella libreria standard come il resto del progetto. Il file viene aperto sia
dal servizio web (che scrive) sia dal relay (che legge i permessi ogni pochi
secondi), quindi si usa la modalita' WAL: senza, il relay resterebbe bloccato
ogni volta che qualcuno si registra dal pannello.

Modello dei dati, in breve:

    utente ──< membership >── stazione
                  │
                ruolo (titolare / operatore / ascoltatore)

Un utente puo' avere ruoli diversi su stazioni diverse: operatore sulla radio
del club, semplice ascoltatore su quella di un socio. La stazione ha sempre un
titolare, che e' il responsabile di cio' che va in aria sotto quel nominativo.

Tutte le date sono interi (secondi UNIX): confronti banali e nessuna sorpresa
di fuso orario.
"""

from __future__ import annotations   # annotazioni come testo: gira anche su Python 3.8

import hashlib
import os
import secrets
import sqlite3
import time

from decolink_token import ROLE_LISTENER, ROLE_OPERATOR, ROLE_OWNER, ROLES

# Stati dell'utente. 'pending' e' lo stato in cui si nasce: ci si registra e si
# aspetta che il titolare guardi la domanda. Nessuno arriva alla radio da solo.
ST_PENDING = "pending"
ST_ACTIVE = "active"
ST_SUSPENDED = "suspended"

# Parametri scrypt. Con questi una verifica costa ~100 ms su un VPS modesto:
# impercettibile al login, molto pesante per chi provasse un dizionario.
_SCRYPT_N, _SCRYPT_R, _SCRYPT_P = 2 ** 14, 8, 1

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT    NOT NULL UNIQUE COLLATE NOCASE,
    callsign      TEXT    NOT NULL COLLATE NOCASE,
    name          TEXT    NOT NULL DEFAULT '',
    pwd           TEXT    NOT NULL,
    status        TEXT    NOT NULL DEFAULT 'pending',
    is_admin      INTEGER NOT NULL DEFAULT 0,
    note          TEXT    NOT NULL DEFAULT '',
    created_at    INTEGER NOT NULL,
    last_login    INTEGER
);

CREATE TABLE IF NOT EXISTS stations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    slug          TEXT    NOT NULL UNIQUE COLLATE NOCASE,
    name          TEXT    NOT NULL DEFAULT '',
    callsign      TEXT    NOT NULL DEFAULT '',
    owner_id      INTEGER NOT NULL REFERENCES users(id),
    enabled       INTEGER NOT NULL DEFAULT 1,
    created_at    INTEGER NOT NULL
);

-- Il permesso di un utente su una stazione. Senza una riga qui, per quella
-- stazione l'utente non esiste: nessun accesso, nemmeno in ascolto.
CREATE TABLE IF NOT EXISTS memberships (
    user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    station_id    INTEGER NOT NULL REFERENCES stations(id) ON DELETE CASCADE,
    role          TEXT    NOT NULL,
    granted_by    INTEGER REFERENCES users(id),
    granted_at    INTEGER NOT NULL,
    PRIMARY KEY (user_id, station_id)
);

-- Sessioni del pannello web (cookie). Si conserva solo l'hash: se qualcuno
-- legge il database non ottiene cookie utilizzabili.
CREATE TABLE IF NOT EXISTS web_sessions (
    token_hash    TEXT    PRIMARY KEY,
    user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at    INTEGER NOT NULL,
    expires_at    INTEGER NOT NULL
);

-- Token di accesso al relay buttati via prima della scadenza (disconnessione
-- forzata di una singola sessione). Si tengono finche' non scadono da soli:
-- dopo, la firma non vale piu' comunque e la riga diventa inutile.
CREATE TABLE IF NOT EXISTS revoked_tokens (
    jti           TEXT    PRIMARY KEY,
    expires_at    INTEGER NOT NULL,
    revoked_at    INTEGER NOT NULL,
    reason        TEXT    NOT NULL DEFAULT ''
);

-- Chi si e' collegato al relay e quando. Serve a rispondere alla domanda
-- "chi c'era in stazione quel giorno".
CREATE TABLE IF NOT EXISTS connections (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER,
    callsign      TEXT    NOT NULL DEFAULT '',
    station_id    INTEGER,
    role          TEXT    NOT NULL DEFAULT '',
    addr          TEXT    NOT NULL DEFAULT '',
    joined_at     INTEGER NOT NULL,
    left_at       INTEGER
);

-- Registro delle trasmissioni. Chi opera da remoto trasmette sotto il
-- nominativo del titolare della stazione: senza questo registro non ci sarebbe
-- modo di dire chi ha premuto il PTT, che e' esattamente cio' che il titolare
-- deve poter dimostrare.
CREATE TABLE IF NOT EXISTS tx_log (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER,
    callsign      TEXT    NOT NULL DEFAULT '',
    station_id    INTEGER,
    started_at    INTEGER NOT NULL,
    ended_at      INTEGER,
    addr          TEXT    NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_memb_station ON memberships(station_id);
CREATE INDEX IF NOT EXISTS idx_conn_joined  ON connections(joined_at);
CREATE INDEX IF NOT EXISTS idx_tx_started   ON tx_log(started_at);
"""


def default_path() -> str:
    """Dove sta il database se nessuno dice altrimenti.

    Accanto agli script: su un VPS il servizio gira dalla sua cartella e cosi'
    backup e ispezione non richiedono di ricordarsi un percorso.
    """
    return os.environ.get("DECOLINK_DB") or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "decolink.db")


def connect(path: str | None = None) -> sqlite3.Connection:
    """Apre il database, creando le tabelle se mancano.

    Una connessione per thread (SQLite non ama essere condiviso): aprirla costa
    poco, quindi il server web ne apre una per richiesta invece di gestire un
    pool.
    """
    path = path or default_path()
    conn = sqlite3.connect(path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")     # relay e web insieme senza bloccarsi
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


# ---------------------------------------------------------------- password

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    dk = hashlib.scrypt(password.encode("utf-8"), salt=salt,
                        n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P, dklen=32)
    return f"scrypt${_SCRYPT_N}${_SCRYPT_R}${_SCRYPT_P}${salt.hex()}${dk.hex()}"


def check_password(password: str, stored: str) -> bool:
    try:
        algo, n, r, p, salt_hex, want_hex = stored.split("$")
        if algo != "scrypt":
            return False
        dk = hashlib.scrypt(password.encode("utf-8"), salt=bytes.fromhex(salt_hex),
                            n=int(n), r=int(r), p=int(p), dklen=len(want_hex) // 2)
    except Exception:
        return False
    return secrets.compare_digest(dk.hex(), want_hex)


# ------------------------------------------------------------------ utenti

def create_user(conn, email: str, callsign: str, password: str, *,
                name: str = "", status: str = ST_PENDING, is_admin: bool = False) -> int:
    """Registra un utente. Nasce 'pending': puo' entrare nel pannello e vedere
    la propria domanda in attesa, ma il relay non lo fa passare."""
    cur = conn.execute(
        "INSERT INTO users (email, callsign, name, pwd, status, is_admin, created_at)"
        " VALUES (?,?,?,?,?,?,?)",
        (email.strip(), callsign.strip().upper(), name.strip(),
         hash_password(password), status, 1 if is_admin else 0, int(time.time())))
    conn.commit()
    return int(cur.lastrowid)


def user_by_email(conn, email: str):
    return conn.execute("SELECT * FROM users WHERE email = ?", (email.strip(),)).fetchone()


def user_by_id(conn, user_id: int):
    return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def authenticate(conn, email: str, password: str):
    """Restituisce l'utente se le credenziali sono giuste, altrimenti None.

    La password si verifica anche per gli utenti sospesi o in attesa: cosi' chi
    aspetta l'approvazione riceve "in attesa di approvazione" invece di
    "credenziali errate", che lo manderebbe a cercare un problema che non c'e'.
    Sta a chi chiama guardare lo stato prima di far passare qualcuno.
    """
    row = user_by_email(conn, email)
    if not row or not check_password(password, row["pwd"]):
        return None
    conn.execute("UPDATE users SET last_login = ? WHERE id = ?", (int(time.time()), row["id"]))
    conn.commit()
    return row


def set_user_status(conn, user_id: int, status: str) -> None:
    if status not in (ST_PENDING, ST_ACTIVE, ST_SUSPENDED):
        raise ValueError(f"stato sconosciuto: {status}")
    conn.execute("UPDATE users SET status = ? WHERE id = ?", (status, user_id))
    conn.commit()


def set_password(conn, user_id: int, password: str) -> None:
    conn.execute("UPDATE users SET pwd = ? WHERE id = ?", (hash_password(password), user_id))
    conn.commit()


def list_users(conn, status: str | None = None):
    if status:
        return conn.execute("SELECT * FROM users WHERE status = ? ORDER BY created_at DESC",
                            (status,)).fetchall()
    return conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()


# ---------------------------------------------------------------- stazioni

def create_station(conn, slug: str, owner_id: int, *, name: str = "", callsign: str = "") -> int:
    """Crea una stazione e ne fa titolare l'utente indicato.

    Il titolare riceve subito la membership da 'own': senza, il proprietario
    della radio non potrebbe collegarsi alla propria stazione, che sarebbe
    assurdo.
    """
    now = int(time.time())
    cur = conn.execute(
        "INSERT INTO stations (slug, name, callsign, owner_id, created_at) VALUES (?,?,?,?,?)",
        (slug.strip().lower(), name.strip(), callsign.strip().upper(), owner_id, now))
    station_id = int(cur.lastrowid)
    conn.execute(
        "INSERT OR REPLACE INTO memberships (user_id, station_id, role, granted_by, granted_at)"
        " VALUES (?,?,?,?,?)", (owner_id, station_id, ROLE_OWNER, owner_id, now))
    conn.commit()
    return station_id


def station_by_slug(conn, slug: str):
    return conn.execute("SELECT * FROM stations WHERE slug = ?", (slug.strip().lower(),)).fetchone()


def station_by_id(conn, station_id: int):
    return conn.execute("SELECT * FROM stations WHERE id = ?", (station_id,)).fetchone()


def list_stations(conn, owner_id: int | None = None):
    if owner_id is not None:
        return conn.execute("SELECT * FROM stations WHERE owner_id = ? ORDER BY slug",
                            (owner_id,)).fetchall()
    return conn.execute("SELECT * FROM stations ORDER BY slug").fetchall()


def set_station_enabled(conn, station_id: int, enabled: bool) -> None:
    """Chiude o riapre una stazione: con enabled=0 nessuno vi si collega piu',
    utile quando la radio e' in manutenzione o il titolare e' assente."""
    conn.execute("UPDATE stations SET enabled = ? WHERE id = ?",
                 (1 if enabled else 0, station_id))
    conn.commit()


# ------------------------------------------------------------- permessi

def grant(conn, user_id: int, station_id: int, role: str, granted_by: int | None = None) -> None:
    if role not in ROLES:
        raise ValueError(f"ruolo sconosciuto: {role}")
    conn.execute(
        "INSERT INTO memberships (user_id, station_id, role, granted_by, granted_at)"
        " VALUES (?,?,?,?,?)"
        " ON CONFLICT(user_id, station_id) DO UPDATE SET role=excluded.role,"
        " granted_by=excluded.granted_by, granted_at=excluded.granted_at",
        (user_id, station_id, role, granted_by, int(time.time())))
    conn.commit()


def revoke(conn, user_id: int, station_id: int) -> None:
    conn.execute("DELETE FROM memberships WHERE user_id = ? AND station_id = ?",
                 (user_id, station_id))
    conn.commit()


def role_of(conn, user_id: int, station_id: int) -> str | None:
    row = conn.execute("SELECT role FROM memberships WHERE user_id = ? AND station_id = ?",
                       (user_id, station_id)).fetchone()
    return row["role"] if row else None


def members_of(conn, station_id: int):
    return conn.execute(
        "SELECT m.role, m.granted_at, u.* FROM memberships m JOIN users u ON u.id = m.user_id"
        " WHERE m.station_id = ? ORDER BY m.role, u.callsign", (station_id,)).fetchall()


def stations_of(conn, user_id: int):
    """Le stazioni a cui l'utente ha accesso, col ruolo. E' quello che il client
    mostra dopo il login per far scegliere dove collegarsi."""
    return conn.execute(
        "SELECT s.*, m.role FROM memberships m JOIN stations s ON s.id = m.station_id"
        " WHERE m.user_id = ? AND s.enabled = 1 ORDER BY s.slug", (user_id,)).fetchall()


def active_grants(conn) -> dict:
    """Fotografia dei permessi validi in questo momento: (user_id, station_id) -> ruolo.

    E' quello che il relay ricarica ogni pochi secondi. Un token firmato dice
    quel che era vero quando e' stato emesso; questa mappa dice quel che e' vero
    adesso, e in caso di disaccordo vince questa. Cosi' togliere il permesso a
    qualcuno ha effetto entro pochi secondi anche se ha in mano un token ancora
    valido, senza dover interrogare il database a ogni pacchetto.
    """
    rows = conn.execute(
        "SELECT m.user_id, m.station_id, m.role FROM memberships m"
        " JOIN users u ON u.id = m.user_id"
        " JOIN stations s ON s.id = m.station_id"
        " WHERE u.status = 'active' AND s.enabled = 1").fetchall()
    return {(int(r["user_id"]), int(r["station_id"])): r["role"] for r in rows}


# -------------------------------------------------------------- revoche

def revoke_token(conn, jti: str, expires_at: int, reason: str = "") -> None:
    conn.execute(
        "INSERT OR REPLACE INTO revoked_tokens (jti, expires_at, revoked_at, reason)"
        " VALUES (?,?,?,?)", (jti, int(expires_at), int(time.time()), reason))
    conn.commit()


def revoked_ids(conn) -> set:
    """I token buttati via che non sono ancora scaduti da soli."""
    now = int(time.time())
    conn.execute("DELETE FROM revoked_tokens WHERE expires_at < ?", (now,))
    conn.commit()
    return {r["jti"] for r in conn.execute("SELECT jti FROM revoked_tokens").fetchall()}


# ----------------------------------------------------------- sessioni web

def new_web_session(conn, user_id: int, ttl: int = 12 * 3600) -> str:
    token = secrets.token_urlsafe(32)
    now = int(time.time())
    conn.execute("INSERT INTO web_sessions (token_hash, user_id, created_at, expires_at)"
                 " VALUES (?,?,?,?)",
                 (hashlib.sha256(token.encode()).hexdigest(), user_id, now, now + ttl))
    conn.execute("DELETE FROM web_sessions WHERE expires_at < ?", (now,))
    conn.commit()
    return token


def web_session_user(conn, token: str):
    if not token:
        return None
    row = conn.execute(
        "SELECT u.* FROM web_sessions w JOIN users u ON u.id = w.user_id"
        " WHERE w.token_hash = ? AND w.expires_at > ?",
        (hashlib.sha256(token.encode()).hexdigest(), int(time.time()))).fetchone()
    return row


def drop_web_session(conn, token: str) -> None:
    if token:
        conn.execute("DELETE FROM web_sessions WHERE token_hash = ?",
                     (hashlib.sha256(token.encode()).hexdigest(),))
        conn.commit()


# ------------------------------------------------------------------- log

def log_join(conn, *, user_id, callsign, station_id, role, addr) -> int:
    cur = conn.execute(
        "INSERT INTO connections (user_id, callsign, station_id, role, addr, joined_at)"
        " VALUES (?,?,?,?,?,?)",
        (user_id, callsign, station_id, role, addr, int(time.time())))
    conn.commit()
    return int(cur.lastrowid)


def log_leave(conn, conn_id: int) -> None:
    conn.execute("UPDATE connections SET left_at = ? WHERE id = ? AND left_at IS NULL",
                 (int(time.time()), conn_id))
    conn.commit()


def log_tx_start(conn, *, user_id, callsign, station_id, addr) -> int:
    cur = conn.execute(
        "INSERT INTO tx_log (user_id, callsign, station_id, started_at, addr) VALUES (?,?,?,?,?)",
        (user_id, callsign, station_id, int(time.time()), addr))
    conn.commit()
    return int(cur.lastrowid)


def log_tx_end(conn, tx_id: int) -> None:
    conn.execute("UPDATE tx_log SET ended_at = ? WHERE id = ? AND ended_at IS NULL",
                 (int(time.time()), tx_id))
    conn.commit()


def recent_tx(conn, station_id: int | None = None, limit: int = 100):
    if station_id is not None:
        return conn.execute("SELECT * FROM tx_log WHERE station_id = ?"
                            " ORDER BY started_at DESC LIMIT ?", (station_id, limit)).fetchall()
    return conn.execute("SELECT * FROM tx_log ORDER BY started_at DESC LIMIT ?",
                        (limit,)).fetchall()


def recent_connections(conn, station_id: int | None = None, limit: int = 100):
    if station_id is not None:
        return conn.execute("SELECT * FROM connections WHERE station_id = ?"
                            " ORDER BY joined_at DESC LIMIT ?", (station_id, limit)).fetchall()
    return conn.execute("SELECT * FROM connections ORDER BY joined_at DESC LIMIT ?",
                        (limit,)).fetchall()
