
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

-- Le chiavi di stazione emesse. Una chiave e' un token firmato che vive
-- trenta giorni fuori dal nostro controllo, incollato dentro un'applicazione
-- che non sa fare l'accesso: se non si tiene nota di averla emessa, non c'e'
-- modo di annullarla prima della scadenza, perche' per revocarla serve il suo
-- identificativo e quello lo si vede una volta sola, al momento di emetterla.
--
-- La riga resta anche dopo la revoca: chi guarda deve poter vedere che una
-- chiave c'e' stata e che e' stata annullata, non trovare il vuoto.
CREATE TABLE IF NOT EXISTS issued_keys (
    jti           TEXT    PRIMARY KEY,
    user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    station_id    INTEGER NOT NULL REFERENCES stations(id) ON DELETE CASCADE,
    role          TEXT    NOT NULL DEFAULT '',
    issued_at     INTEGER NOT NULL,
    expires_at    INTEGER NOT NULL,
    revoked_at    INTEGER
);
CREATE INDEX IF NOT EXISTS idx_keys_user ON issued_keys(user_id);
CREATE INDEX IF NOT EXISTS idx_keys_station ON issued_keys(station_id);

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
