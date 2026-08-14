#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Decolink deve poter usare una radio tenuta da un altro programma, senza
aprire la porta seriale.

Qui si finge di essere quel programma — un server che parla come rigctld, cioe'
come farebbero rigctld, FLRig o Decodium — e si lascia che Decolink ci si
colleghi davvero.
"""
import os
import socket
import subprocess
import sys
import threading

PORTA = 4599          # non la 4532, per non pestare un rigctld vero
FREQ = [14074000]
MODO = ["USB"]
PTT = [0]
richieste = []


def servi(conn):
    resto = b""
    while True:
        try:
            d = conn.recv(1024)
        except OSError:
            return
        if not d:
            return
        resto += d
        while b"\n" in resto:
            riga, resto = resto.split(b"\n", 1)
            c = riga.decode("utf-8", "ignore").strip()
            if not c:
                continue
            richieste.append(c)
            if c == "f":
                conn.sendall(f"{FREQ[0]}\n".encode())
            elif c.startswith("F "):
                FREQ[0] = int(float(c[2:].strip()))
                conn.sendall(b"RPRT 0\n")
            elif c == "m":
                conn.sendall(f"{MODO[0]}\n2400\n".encode())
            elif c.startswith("M "):
                MODO[0] = c[2:].strip().split()[0]
                conn.sendall(b"RPRT 0\n")
            elif c == "t":
                conn.sendall(f"{PTT[0]}\n".encode())
            elif c.startswith("T "):
                PTT[0] = int(c[2:].strip())
                conn.sendall(b"RPRT 0\n")
            elif c.startswith("\\dump_state"):
                # Il formato lo pretende Hamlib all'apertura: versione del
                # protocollo, modello, regione ITU, le gamme in ricezione e
                # trasmissione chiuse da una riga di zeri, i passi di sintonia,
                # i filtri, e infine i limiti e le funzioni disponibili.
                stato = "\n".join([
                    "0",                       # versione del protocollo
                    "2",                       # modello (NET rigctl)
                    "2",                       # regione ITU
                    "150000.000000 30000000.000000 0x1ff -1 -1 0x1 0x0",
                    "0 0 0 0 0 0 0",           # fine delle gamme in ricezione
                    "1800000.000000 2000000.000000 0x1ff 5000 100000 0x1 0x0",
                    "0 0 0 0 0 0 0",           # fine delle gamme in trasmissione
                    "0x1ff 1", "0 0",          # passi di sintonia
                    "0x1ff 2400", "0 0",       # filtri
                    "0", "0", "0", "0",        # rit, xit, spostamento FI, annunci
                    "0", "0",                  # preamplificatore, attenuatore
                    "0x0", "0x0",              # funzioni leggibili / impostabili
                    "0x0", "0x0",              # livelli leggibili / impostabili
                    "0x0", "0x0",              # parametri leggibili / impostabili
                ]) + "\n"
                conn.sendall(stato.encode())
            elif c.startswith("\\chk_vfo"):
                conn.sendall(b"CHKVFO 0\n")
            elif c.startswith("\\get_powerstat"):
                conn.sendall(b"1\n")
            else:
                conn.sendall(b"RPRT 0\n")


def ascolta(srv):
    while True:
        try:
            conn, _ = srv.accept()
        except OSError:
            return
        threading.Thread(target=servi, args=(conn,), daemon=True).start()


srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("127.0.0.1", PORTA))
srv.listen(5)
threading.Thread(target=ascolta, args=(srv,), daemon=True).start()
print(f"  un altro programma tiene la radio e la offre su 127.0.0.1:{PORTA}")
print("  (nessuna porta COM aperta da Decolink)\n")

env = dict(os.environ, PATH="C:\\msys64\\mingw64\\bin;" + os.environ.get("PATH", ""))
r = subprocess.run(["C:\\hf-gateway\\gui\\build\\decolink.exe", "--hamlibtest",
                    f"127.0.0.1:{PORTA}"],
                   capture_output=True, text=True, timeout=120, env=env)

for riga in r.stdout.splitlines():
    t = riga.strip()
    if t.startswith(("radio condivisa", "collegato", "legge", "cambia", "alza", "abbassa",
                     "la radio", "non risponde", "QUALCOSA")):
        print("  " + t)

esito = "la radio condivisa funziona" in r.stdout
print(f"\n  comandi ricevuti da chi tiene la radio: {len(richieste)}")
if richieste:
    verbi = sorted({c.split()[0] for c in richieste})
    print(f"  verbi usati: {' '.join(verbi[:10])}")
print(f"  stato finale del server finto: {FREQ[0]} Hz, {MODO[0]}, PTT={PTT[0]}")
srv.close()
print("\n=== " + ("prova superata" if esito else "PROVA FALLITA") + " ===")
sys.exit(0 if esito else 1)
