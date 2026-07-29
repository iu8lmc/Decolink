#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decolink_mail.py — avviso al titolare quando qualcuno chiede l'accesso.

Le richieste comparivano soltanto nella pagina della stazione: se il titolare
non andava a guardare, il richiedente restava in attesa senza che nessuno lo
sapesse. Qui parte una email, e basta.

Configurazione, tutta da variabili d'ambiente (come DECOLINK_SECRET):

    DECOLINK_SMTP_HOST   server di posta; se manca, non si manda nulla
    DECOLINK_SMTP_PORT   587 con STARTTLS (predefinito), 465 con SSL diretto
    DECOLINK_SMTP_USER   utente, se il server lo richiede
    DECOLINK_SMTP_PASS   password
    DECOLINK_SMTP_FROM   mittente (predefinito: l'utente SMTP)
    DECOLINK_BASE_URL    indirizzo pubblico, per il link al pannello

Senza DECOLINK_SMTP_HOST il modulo resta zitto e il servizio si comporta come
prima: la posta e' un di piu', non un requisito per far girare il gateway.

Solo libreria standard Python 3.
"""

from __future__ import annotations

import os
import smtplib
import ssl
import threading
from email.message import EmailMessage

HOST = os.environ.get("DECOLINK_SMTP_HOST", "").strip()
PORT = int(os.environ.get("DECOLINK_SMTP_PORT", "587"))
USER = os.environ.get("DECOLINK_SMTP_USER", "").strip()
PASS = os.environ.get("DECOLINK_SMTP_PASS", "")
FROM = os.environ.get("DECOLINK_SMTP_FROM", "").strip() or USER
BASE_URL = os.environ.get("DECOLINK_BASE_URL", "").strip().rstrip("/")

TIMEOUT = 15.0          # s: un server di posta lento non deve bloccare il sito


def attiva() -> bool:
    """Vero se c'e' abbastanza configurazione per provarci."""
    return bool(HOST and FROM)


def _spedisci(msg: EmailMessage) -> None:
    """Invio vero e proprio. Gira in un thread: la registrazione non aspetta."""
    try:
        if PORT == 465:
            with smtplib.SMTP_SSL(HOST, PORT, timeout=TIMEOUT,
                                  context=ssl.create_default_context()) as s:
                if USER:
                    s.login(USER, PASS)
                s.send_message(msg)
        else:
            with smtplib.SMTP(HOST, PORT, timeout=TIMEOUT) as s:
                s.ehlo()
                try:
                    s.starttls(context=ssl.create_default_context())
                    s.ehlo()
                except smtplib.SMTPException:
                    # server senza TLS: si prosegue solo se non ci sono
                    # credenziali da esporre in chiaro
                    if USER:
                        raise
                if USER:
                    s.login(USER, PASS)
                s.send_message(msg)
        print(f"  @ avviso spedito a {msg['To']}")
    except Exception as err:      # noqa: BLE001 — la posta non deve mai far cadere il sito
        print(f"  ! avviso non spedito a {msg['To']}: {err}")


def invia(a: str, oggetto: str, testo: str) -> None:
    if not attiva() or not a:
        return
    msg = EmailMessage()
    msg["From"] = FROM
    msg["To"] = a
    msg["Subject"] = oggetto
    msg.set_content(testo)
    threading.Thread(target=_spedisci, args=(msg,), daemon=True).start()


def avvisa_richiesta(titolare_email: str, *, callsign: str, email: str,
                     nome: str = "", stazione: str = "", nota: str = "") -> None:
    """Avvisa il titolare che c'e' una richiesta da approvare."""
    if not titolare_email:
        return
    chi = f"{callsign} ({nome})" if nome else callsign
    dove = f"/stazione/{stazione}" if stazione else "/"
    link = f"{BASE_URL}{dove}" if BASE_URL else f"...{dove}"
    corpo = [
        f"{chi} ha chiesto l'accesso" + (f" alla stazione {stazione}." if stazione else "."),
        "",
        f"  nominativo : {callsign}",
        f"  email      : {email}",
    ]
    if nota:
        corpo += [f"  nota       : {nota}"]
    corpo += [
        "",
        "Finche' non la approvi, la richiesta resta in attesa e chi l'ha fatta",
        "non puo' collegarsi.",
        "",
        f"Pannello: {link}",
    ]
    invia(titolare_email,
          f"Decolink: {callsign} chiede l'accesso"
          + (f" a {stazione}" if stazione else ""),
          "\n".join(corpo))
