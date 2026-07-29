#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decolink_relay.py — relay UDP autenticato del gateway Decolink.

Sostituisce hf_relay.py, che accoppiava due chiunque entrassero nella stessa
stanza. Qui per entrare serve un token firmato dal servizio di accesso
(decolink_web.py), e il ruolo scritto nel token decide che cosa si puo' fare:
ascoltare e basta, oppure mandare la radio in aria.

Protocollo HFGW v2 — incompatibile con la v1, che non aveva alcun controllo.

    REGISTER (flag 3)  payload:  "gw <token>"   il PC collegato alla radio
                                 "op <token>"   chi ascolta o opera da remoto

La stanza non e' piu' una parola scelta a caso ma la stazione scritta dentro al
token: due utenti finiscono insieme se e solo se il servizio di accesso ha
detto che appartengono alla stessa stazione.

Chi parla con chi, dentro una stanza:

    gateway ──audio RX (flag 0)──> tutti gli operatori
    gateway <──audio TX (flag 7)── un solo operatore per volta
    gateway <──comando CAT (5)──── operatori abilitati alla trasmissione
    gateway ──risposta CAT (6)───> chi aveva chiesto

Un ascoltatore che provasse a mandare TX o CAT viene semplicemente ignorato: i
pacchetti non vengono inoltrati e la radio non se ne accorge nemmeno.

Uso:
    python3 decolink_relay.py [porta]        # default 5555
    # apri la porta UDP sul firewall del VPS:  sudo ufw allow 5555/udp
    # avvio persistente: vedi server/decolink-relay.service

Solo libreria standard Python 3.
"""

from __future__ import annotations   # annotazioni come testo: gira anche su Python 3.8

import os
import socket
import struct
import sys
import time

import decolink_db as db
import decolink_token as tok

MAGIC = b"HFGW"
VER = 2                       # v1 = senza autenticazione, non piu' accettata
HDR = struct.Struct("!4sBBIQI")   # magic, ver, flags, seq, t_ms, rate = 22 byte

F_AUDIO, F_PING, F_PONG, F_REGISTER, F_PEERUP = 0, 1, 2, 3, 4
F_CAT_REQ, F_CAT_RSP = 5, 6
F_TX_AUDIO = 7
F_DENIED = 8                  # nuovo in v2: "non entri, ed ecco perche'"

HERE = os.path.dirname(os.path.abspath(__file__))
SECRET_PATH = os.environ.get("DECOLINK_SECRET") or os.path.join(HERE, "decolink.key")

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5555
CLIENT_TIMEOUT = 15.0         # s senza pacchetti -> sessione chiusa
GRANT_REFRESH = 5.0           # s fra due riletture dei permessi dal database
TX_IDLE = 1.5                 # s di silenzio dopo cui il PTT si considera mollato
ROOM_MAX = 8                  # partecipanti per stazione (1 gateway + ascoltatori)
CAT_ROUTE_TTL = 10.0          # s per cui si ricorda chi ha fatto una domanda CAT


def hdr(flags, seq=0, tms=0, rate=48000):
    return HDR.pack(MAGIC, VER, flags, seq, tms, rate)


def pkt(flags, testo=""):
    return hdr(flags) + testo.encode("utf-8")[:400]


class Sessione:
    """Un partecipante collegato: chi e', su quale stazione, con che poteri."""

    __slots__ = ("addr", "user_id", "callsign", "station_id", "role", "is_gw",
                 "jti", "expires", "last_seen", "conn_row", "tx_row", "tx_last")

    def __init__(self, addr, dati, is_gw, conn_row):
        self.addr = addr
        self.user_id = dati["user_id"]
        self.callsign = dati["callsign"]
        self.station_id = dati["station_id"]
        self.role = dati["role"]
        self.jti = dati["jti"]
        self.expires = dati["expires"]
        self.is_gw = is_gw
        self.conn_row = conn_row     # riga nel registro dei collegamenti
        self.tx_row = None           # riga aperta nel registro delle trasmissioni
        self.tx_last = 0.0
        self.last_seen = time.time()

    @property
    def puo_trasmettere(self) -> bool:
        return tok.can_transmit(self.role)

    def __str__(self):
        return f"{self.callsign}({'gw' if self.is_gw else self.role})"


class Relay:
    def __init__(self, port: int, db_path: str | None = None):
        self.secret = tok.load_secret(SECRET_PATH)
        self.db = db.connect(db_path)
        self.port = port

        self.sess: dict = {}          # addr -> Sessione
        self.rooms: dict = {}         # station_id -> set(addr)
        self.tx_holder: dict = {}     # station_id -> addr che sta trasmettendo
        self.cat_route: dict = {}     # (station_id, seq) -> (addr, istante)

        self.grants = {}              # (user, stazione) -> ruolo, riletti dal DB
        self.revoked = set()
        self.last_grants = 0.0
        self.fwd = self.rej = 0

    # ------------------------------------------------------------ permessi

    def refresh_grants(self, now: float, forza: bool = False) -> None:
        """Rilegge dal database chi ha diritto a cosa.

        Il token dice quel che era vero quando e' stato emesso; questa mappa
        dice quel che e' vero adesso. Se il titolare toglie il permesso a
        qualcuno mentre e' collegato, entro pochi secondi la sessione cade,
        senza aspettare la scadenza del token.

        Se il database non risponde si tiene la fotografia precedente: meglio un
        permesso vecchio di qualche secondo che buttare fuori tutta la stazione
        perche' il disco era occupato.
        """
        if not forza and now - self.last_grants < GRANT_REFRESH:
            return
        self.last_grants = now
        try:
            self.grants = db.active_grants(self.db)
            self.revoked = db.revoked_ids(self.db)
        except Exception as ex:
            print(f"  [attenzione] permessi non rileggibili: {ex}")
            return
        # Chi non e' piu' in regola se ne va adesso, non alla scadenza.
        for addr, s in list(self.sess.items()):
            ruolo = self.grants.get((s.user_id, s.station_id))
            if s.jti in self.revoked:
                self.espelli(addr, "sessione revocata")
            elif ruolo is None:
                self.espelli(addr, "permesso revocato")
            elif ruolo != s.role:
                # Declassato mentre era collegato: non lo si butta fuori, gli si
                # cambiano i poteri. Se perde il diritto di trasmettere e aveva
                # il PTT, glielo si toglie subito.
                print(f"  ~ {s} passa a '{ruolo}'")
                s.role = ruolo
                if not s.puo_trasmettere:
                    self.fine_tx(s, now)

    def verifica(self, token_txt: str, now: float):
        """Controlla un token e restituisce i dati, o solleva TokenError."""
        dati = tok.verify(self.secret, token_txt, now=now)
        if dati["jti"] in self.revoked:
            raise tok.TokenError("sessione revocata")
        ruolo = self.grants.get((dati["user_id"], dati["station_id"]))
        if ruolo is None:
            raise tok.TokenError("permesso non piu' valido")
        dati["role"] = ruolo     # comanda il database, non il foglietto firmato
        return dati

    # ------------------------------------------------------------ sessioni

    def gateway_di(self, station_id):
        for a in self.rooms.get(station_id, ()):
            s = self.sess.get(a)
            if s and s.is_gw:
                return s
        return None

    def registra(self, addr, payload: str, seq, now: float) -> None:
        # payload: "gw <token>" oppure "op <token>"
        tipo, _, token_txt = payload.partition(" ")
        tipo = tipo.strip().lower()
        token_txt = token_txt.strip()
        if tipo not in ("gw", "op") or not token_txt:
            self.rifiuta(addr, "formato della registrazione non valido")
            return

        try:
            dati = self.verifica(token_txt, now)
        except tok.TokenError as ex:
            self.rifiuta(addr, str(ex))
            return

        vecchia = self.sess.get(addr)
        if vecchia:
            # Semplice keepalive: e' il caso piu' frequente, il client rimanda
            # il REGISTER ogni 5 secondi per tenere aperto il buco nel NAT.
            if vecchia.jti == dati["jti"]:
                vecchia.last_seen = now
                self.sock.sendto(hdr(F_REGISTER, seq), addr)
                return
            self.chiudi(addr, "nuova registrazione")

        is_gw = (tipo == "gw")
        if is_gw and not tok.can_transmit(dati["role"]):
            # Il PC attaccato alla radio la fa anche trasmettere: darlo in mano a
            # un ascoltatore vorrebbe dire aggirare il divieto dalla porta di
            # servizio.
            self.rifiuta(addr, "serve il ruolo di operatore per fare da gateway")
            return

        membri = self.rooms.setdefault(dati["station_id"], set())
        if is_gw:
            altro = self.gateway_di(dati["station_id"])
            if altro:
                # Una radio sola, un gateway solo: due sorgenti audio sulla
                # stessa stanza si sovrapporrebbero e nessuno capirebbe piu' nulla.
                self.rifiuta(addr, f"la stazione ha gia' un gateway ({altro.callsign})")
                return
        elif len(membri) >= ROOM_MAX:
            self.rifiuta(addr, "stazione al completo")
            return

        try:
            riga = db.log_join(self.db, user_id=dati["user_id"], callsign=dati["callsign"],
                               station_id=dati["station_id"], role=dati["role"],
                               addr=f"{addr[0]}:{addr[1]}")
        except Exception as ex:
            print(f"  [attenzione] collegamento non registrato: {ex}")
            riga = None

        s = Sessione(addr, dati, is_gw, riga)
        self.sess[addr] = s
        membri.add(addr)
        print(f"  + {s} entra sulla stazione {dati['station_id']} "
              f"da {addr[0]}:{addr[1]} ({len(membri)}/{ROOM_MAX})")

        self.sock.sendto(hdr(F_REGISTER, seq), addr)
        # Avvisa tutti che la stanza ha un gateway e almeno un operatore: e' il
        # segnale con cui i client smettono di aspettare e cominciano.
        if self.gateway_di(dati["station_id"]) and len(membri) >= 2:
            for a in membri:
                self.sock.sendto(hdr(F_PEERUP), a)

    def rifiuta(self, addr, motivo: str) -> None:
        """Dice al client perche' non entra.

        Un rifiuto muto lascerebbe l'utente davanti a una barra che gira: cosi'
        invece Decolink puo' scrivere 'accesso in attesa di approvazione' e la
        differenza fra un permesso mancante e una porta sbagliata e' evidente.
        """
        self.rej += 1
        print(f"  ! {addr[0]}:{addr[1]} respinto: {motivo}")
        try:
            self.sock.sendto(pkt(F_DENIED, motivo), addr)
        except OSError:
            pass

    def espelli(self, addr, motivo: str) -> None:
        try:
            self.sock.sendto(pkt(F_DENIED, motivo), addr)
        except OSError:
            pass
        self.chiudi(addr, motivo)

    def chiudi(self, addr, motivo: str = "") -> None:
        s = self.sess.pop(addr, None)
        if not s:
            return
        self.fine_tx(s, time.time())
        membri = self.rooms.get(s.station_id, set())
        membri.discard(addr)
        if not membri:
            self.rooms.pop(s.station_id, None)
            self.tx_holder.pop(s.station_id, None)
        if s.conn_row:
            try:
                db.log_leave(self.db, s.conn_row)
            except Exception:
                pass
        print(f"  - {s} lascia la stazione {s.station_id}" + (f" ({motivo})" if motivo else ""))

    # --------------------------------------------------------- trasmissione

    def inizio_tx(self, s: Sessione, now: float) -> bool:
        """Chiede il PTT per questa sessione. False se ce l'ha un altro.

        Un solo operatore per volta manda audio alla radio: due che parlano
        insieme non farebbero un QSO a tre, farebbero un pasticcio in aria sotto
        il nominativo del titolare.
        """
        attuale = self.tx_holder.get(s.station_id)
        if attuale is not None and attuale != s.addr:
            altro = self.sess.get(attuale)
            # Chi teneva il PTT ha smesso di mandare: il canale torna libero.
            if altro and now - altro.tx_last < TX_IDLE:
                return False
            if altro:
                self.fine_tx(altro, now)

        if self.tx_holder.get(s.station_id) != s.addr:
            self.tx_holder[s.station_id] = s.addr
            try:
                s.tx_row = db.log_tx_start(self.db, user_id=s.user_id, callsign=s.callsign,
                                           station_id=s.station_id,
                                           addr=f"{s.addr[0]}:{s.addr[1]}")
            except Exception as ex:
                print(f"  [attenzione] trasmissione non registrata: {ex}")
            print(f"  TX {s.callsign} sulla stazione {s.station_id}")
        s.tx_last = now
        return True

    def fine_tx(self, s: Sessione, now: float) -> None:
        if self.tx_holder.get(s.station_id) == s.addr:
            del self.tx_holder[s.station_id]
        if s.tx_row:
            try:
                db.log_tx_end(self.db, s.tx_row)
            except Exception:
                pass
            print(f"  TX {s.callsign} finita")
            s.tx_row = None

    # ------------------------------------------------------------ inoltro

    def inoltra(self, s: Sessione, flags: int, seq: int, data: bytes, now: float) -> None:
        membri = self.rooms.get(s.station_id, ())

        if flags == F_AUDIO:
            # L'audio ricevuto dalla radio ha senso solo dal gateway verso gli
            # altri: se lo mandasse un client sarebbe rumore in casa d'altri.
            if not s.is_gw:
                return
            for a in membri:
                if a != s.addr:
                    self.sock.sendto(data, a)
                    self.fwd += 1
            return

        if flags in (F_TX_AUDIO, F_CAT_REQ):
            if s.is_gw:
                return                       # il gateway non comanda se stesso
            if not s.puo_trasmettere:
                self.rej += 1                # ascoltatore: silenziosamente ignorato
                return
            gw = self.gateway_di(s.station_id)
            if not gw:
                return
            if flags == F_TX_AUDIO and not self.inizio_tx(s, now):
                return                       # il PTT ce l'ha un altro
            if flags == F_CAT_REQ:
                # Si ricorda chi ha chiesto, per far tornare la risposta a lui
                # solo: con piu' operatori collegati, spedirla a tutti
                # significherebbe rispondere a domande che non hanno fatto.
                self.cat_route[(s.station_id, seq)] = (s.addr, now)
            self.sock.sendto(data, gw.addr)
            self.fwd += 1
            return

        if flags == F_CAT_RSP:
            if not s.is_gw:
                return
            dest = self.cat_route.pop((s.station_id, seq), None)
            if dest:
                self.sock.sendto(data, dest[0])
                self.fwd += 1
            else:
                # Risposta senza domanda registrata (o arrivata tardi): va a
                # tutti gli operatori, che scarteranno quel che non aspettano.
                for a in membri:
                    if a != s.addr:
                        self.sock.sendto(data, a)
                        self.fwd += 1

    # ---------------------------------------------------------- manutenzione

    def pulisci(self, now: float) -> None:
        for addr, s in list(self.sess.items()):
            if now - s.last_seen > CLIENT_TIMEOUT:
                self.chiudi(addr, "silenzio")
            elif s.expires < now:
                # Il token e' scaduto: il client ne chiede uno nuovo al servizio
                # web e si ripresenta. Non e' un errore, e' il rinnovo.
                self.espelli(addr, "token scaduto, rinnovalo")
            elif s.tx_row and now - s.tx_last > TX_IDLE:
                self.fine_tx(s, now)
        for chiave, (_, quando) in list(self.cat_route.items()):
            if now - quando > CAT_ROUTE_TTL:
                del self.cat_route[chiave]

    # ---------------------------------------------------------------- ciclo

    def run(self) -> None:
        # Sotto systemd lo stdout non e' un terminale e Python lo bufferizza a
        # blocchi: senza questo, "journalctl -f" resterebbe muto per minuti e poi
        # sputerebbe tutto insieme, proprio mentre si sta guardando chi entra.
        try:
            sys.stdout.reconfigure(line_buffering=True)
        except Exception:
            pass

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1 << 20)
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.settimeout(1.0)
        self.refresh_grants(time.time(), forza=True)

        print(f"Decolink relay in ascolto su UDP {self.port} — protocollo HFGW v{VER}")
        print(f"  chiave di firma: {SECRET_PATH}")
        print(f"  permessi caricati: {len(self.grants)} (rilettura ogni {GRANT_REFRESH:.0f} s)")

        ultima_pulizia = ultima_stat = time.time()
        while True:
            now = time.time()
            try:
                data, addr = self.sock.recvfrom(8192)
                if len(data) >= HDR.size and data[:4] == MAGIC:
                    _, ver, flags, seq, tms, rate = HDR.unpack_from(data)
                    if ver != VER:
                        # Quasi sempre e' un client v1, cioe' senza login: se non
                        # glielo si dicesse, resterebbe a bussare per sempre.
                        if flags == F_REGISTER:
                            self.rifiuta(addr, "versione del protocollo non piu' supportata: "
                                               "aggiorna Decolink")
                    elif flags == F_PING:
                        self.sock.sendto(hdr(F_PONG, seq, tms, rate), addr)
                    elif flags == F_REGISTER:
                        self.registra(addr, data[HDR.size:].decode("utf-8", "ignore")[:600],
                                      seq, now)
                    else:
                        s = self.sess.get(addr)
                        if s:
                            s.last_seen = now
                            self.inoltra(s, flags, seq, data, now)
                        elif flags in (F_AUDIO, F_TX_AUDIO, F_CAT_REQ):
                            # Traffico da chi non si e' registrato: capita dopo un
                            # riavvio del relay, il client deve ripresentarsi.
                            self.rifiuta(addr, "non registrato")
            except socket.timeout:
                pass
            except OSError:
                continue

            self.refresh_grants(now)
            if now - ultima_pulizia > 2:
                self.pulisci(now)
                ultima_pulizia = now
            if now - ultima_stat > 30:
                print(f"  [stat] stazioni attive: {len(self.rooms)}  collegati: {len(self.sess)}  "
                      f"inoltrati: {self.fwd}  respinti: {self.rej}")
                ultima_stat = now


def main():
    relay = Relay(PORT)
    try:
        relay.run()
    except KeyboardInterrupt:
        print("\nrelay chiuso.")
    finally:
        for addr in list(relay.sess):
            relay.chiudi(addr, "relay fermato")
        relay.db.close()


if __name__ == "__main__":
    main()
