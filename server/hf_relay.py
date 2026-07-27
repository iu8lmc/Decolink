#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hf_relay.py — rendez-vous + relay UDP self-hosted per hf-gateway.

Gira su un VPS con IP pubblico (es. community.ft2.it) e accoppia due
gateway che entrano nella stessa "stanza" (room code), inoltrando l'audio
tra loro. Sostituisce la necessità di Tailscale / port-forwarding: i due
gateway escono verso questo server, che fa da ponte. Funziona con qualsiasi
NAT.

Solo libreria standard Python 3 (nessun pip). Protocollo HFGW v1, compatibile con Decolink e con Decodium Mobile.
Inoltra audio (flag 0) e comandi CAT (flag 5/6) fra i membri della stanza.

Uso:
    python3 hf_relay.py [porta]        # default 5555
    # apri la porta UDP sul firewall del VPS, es.:
    #   sudo ufw allow 5555/udp
    # avvio persistente: vedi server/hf-relay.service (systemd)
"""

import socket
import struct
import sys
import time

MAGIC = b"HFGW"
VER = 1
HDR = struct.Struct("!4sBBIQI")  # magic, ver, flags, seq, t_ms, rate = 22 byte
F_AUDIO, F_PING, F_PONG, F_REGISTER, F_PEERUP = 0, 1, 2, 3, 4
# 5/6: comandi CAT e relative risposte. Viaggiano sullo stesso canale
# dell'audio perche' fuori dalla rete locale non c'e' modo di aprire una
# connessione diretta verso il PC della radio (NAT dell'operatore).
F_CAT_REQ, F_CAT_RSP = 5, 6
FORWARDED = (F_AUDIO, F_CAT_REQ, F_CAT_RSP)

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5555
CLIENT_TIMEOUT = 15.0   # s senza pacchetti -> client rimosso
ROOM_MAX = 2            # stazioni per stanza (QSO punto-punto)


def hdr(flags, seq=0, tms=0, rate=48000):
    return HDR.pack(MAGIC, VER, flags, seq, tms, rate)


def main():
    try:
        sys.stdout.reconfigure(line_buffering=True)  # log utili sotto systemd/VPS
    except Exception:
        pass
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1 << 20)
    sock.bind(("0.0.0.0", PORT))
    sock.settimeout(1.0)
    print(f"hf-relay in ascolto su UDP {PORT} — protocollo HFGW v{VER}")

    addr_room: dict[tuple, tuple] = {}   # addr -> (room, last_seen)
    rooms: dict[str, set] = {}           # room -> set(addr)
    fwd = tx = 0
    last_clean = last_stat = time.time()

    def drop(addr):
        info = addr_room.pop(addr, None)
        if info:
            room = info[0]
            rooms.get(room, set()).discard(addr)
            if room in rooms and not rooms[room]:
                del rooms[room]
            print(f"  - {addr[0]}:{addr[1]} lascia la stanza '{room}'")

    while True:
        now = time.time()
        try:
            data, addr = sock.recvfrom(8192)
            if len(data) >= HDR.size and data[:4] == MAGIC:
                _, ver, flags, seq, tms, rate = HDR.unpack_from(data)
                if ver == VER:
                    if flags == F_PING:
                        sock.sendto(hdr(F_PONG, seq, tms, rate), addr)

                    elif flags == F_REGISTER:
                        room = data[HDR.size:].decode("utf-8", "ignore")[:64] or "default"
                        prev = addr_room.get(addr)
                        if prev and prev[0] != room:
                            drop(addr)
                        new_here = addr not in addr_room
                        # limite stanza: rifiuta il 3° arrivato
                        members = rooms.setdefault(room, set())
                        if new_here and len(members) >= ROOM_MAX and addr not in members:
                            # stanza piena: rispondi comunque REGISTER ma non aggiungere
                            sock.sendto(hdr(F_REGISTER, 0, 0, rate), addr)
                        else:
                            members.add(addr)
                            addr_room[addr] = (room, now)
                            if new_here:
                                print(f"  + {addr[0]}:{addr[1]} entra nella stanza "
                                      f"'{room}' ({len(members)}/{ROOM_MAX})")
                            sock.sendto(hdr(F_REGISTER, seq, tms, rate), addr)  # ack
                            if len(members) >= 2:  # avvisa tutti che il peer c'e'
                                for a in members:
                                    sock.sendto(hdr(F_PEERUP, 0, 0, rate), a)

                    elif flags in FORWARDED:
                        info = addr_room.get(addr)
                        if info:
                            room = info[0]
                            addr_room[addr] = (room, now)  # keepalive
                            for a in rooms.get(room, ()):
                                if a != addr:
                                    sock.sendto(data, a)   # inoltra il pacchetto intero
                                    fwd += 1
                            tx += 1
        except socket.timeout:
            pass
        except OSError:
            continue

        if now - last_clean > 3:
            for a in [a for a, (_, t) in addr_room.items() if now - t > CLIENT_TIMEOUT]:
                drop(a)
            last_clean = now
        if now - last_stat > 30:
            print(f"  [stat] stanze attive: {len(rooms)}  client: {len(addr_room)}  "
                  f"pacchetti inoltrati: {fwd}")
            last_stat = now


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nhf-relay chiuso.")
