#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decolink_admin.py — amministrazione da terminale del gateway.

Il pannello web copre la gestione di tutti i giorni; questo serve per il primo
avvio (quando ancora non esiste nessun accesso con cui entrare nel pannello) e
per le emergenze: password dimenticata dell'amministratore, utente da buttare
fuori subito, controllo di cosa e' andato in aria.

    python3 decolink_admin.py init                      primo amministratore
    python3 decolink_admin.py utenti [--stato pending]
    python3 decolink_admin.py attiva  iu8lmc@esempio.it
    python3 decolink_admin.py sospendi iu8lmc@esempio.it
    python3 decolink_admin.py password iu8lmc@esempio.it
    python3 decolink_admin.py stazioni
    python3 decolink_admin.py stazione-nuova i0abc-hf iu8lmc@esempio.it --nome "HF di sezione"
    python3 decolink_admin.py permesso iu8lmc@esempio.it i0abc-hf operatore
    python3 decolink_admin.py togli    iu8lmc@esempio.it i0abc-hf
    python3 decolink_admin.py log [--stazione i0abc-hf]
"""

import argparse
import getpass
import os
import sys
import time

import decolink_db as db
import decolink_token as tok

HERE = os.path.dirname(os.path.abspath(__file__))
SECRET_PATH = os.environ.get("DECOLINK_SECRET") or os.path.join(HERE, "decolink.key")

# Sulla riga di comando si scrivono i ruoli per esteso: 'opr' e' comodo dentro
# un pacchetto UDP, non davanti a chi amministra alle due di notte.
RUOLI = {"titolare": tok.ROLE_OWNER, "operatore": tok.ROLE_OPERATOR,
         "ascoltatore": tok.ROLE_LISTENER}
RUOLI_INV = {v: k for k, v in RUOLI.items()}


def quando(t) -> str:
    return time.strftime("%d/%m/%Y %H:%M", time.localtime(t)) if t else "—"


def trova_utente(conn, email: str):
    u = db.user_by_email(conn, email)
    if not u:
        sys.exit(f"nessun utente con email '{email}'")
    return u


def trova_stazione(conn, slug: str):
    s = db.station_by_slug(conn, slug)
    if not s:
        sys.exit(f"nessuna stazione '{slug}'")
    return s


def chiedi_password() -> str:
    while True:
        p1 = getpass.getpass("password: ")
        if len(p1) < 8:
            print("  almeno 8 caratteri.")
            continue
        if p1 != getpass.getpass("ripeti:   "):
            print("  le due password non coincidono.")
            continue
        return p1


def cmd_init(conn, args):
    if db.list_users(conn):
        sys.exit("il database ha già degli utenti: usa il pannello web, "
                 "oppure 'password' per rimettere in piedi un accesso.")
    print("Primo amministratore del gateway.\n")
    email = input("email:      ").strip()
    call = input("nominativo: ").strip().upper()
    nome = input("nome:       ").strip()
    pwd = chiedi_password()
    uid = db.create_user(conn, email, call, pwd, name=nome,
                         status=db.ST_ACTIVE, is_admin=True)

    # La chiave di firma va creata adesso e non al primo login: se web e relay
    # partissero insieme senza chiave, potrebbero generarne due diverse e
    # nessun token risulterebbe valido.
    tok.load_secret(SECRET_PATH)

    print(f"\namministratore {call} creato (id {uid}).")
    print(f"chiave di firma: {SECRET_PATH}")
    slug = input("\ncodice della prima stazione (invio per saltare): ").strip().lower()
    if slug:
        nome_st = input("nome della stazione: ").strip()
        call_st = input("nominativo della stazione: ").strip().upper()
        sid = db.create_station(conn, slug, uid, name=nome_st, callsign=call_st)
        print(f"stazione '{slug}' creata (id {sid}), titolare {call}.")
    print("\nAvvia ora il servizio web e il relay:")
    print("    python3 decolink_web.py --port 8080")
    print("    python3 decolink_relay.py 5555")


def cmd_utenti(conn, args):
    righe = db.list_users(conn, args.stato)
    if not righe:
        print("nessun utente.")
        return
    print(f"{'nominativo':<12} {'email':<28} {'stato':<10} {'admin':<6} registrato")
    for u in righe:
        print(f"{u['callsign']:<12} {u['email']:<28} {u['status']:<10} "
              f"{'sì' if u['is_admin'] else '':<6} {quando(u['created_at'])}")
        if u["note"]:
            print(f"             nota: {u['note']}")


def cmd_attiva(conn, args):
    u = trova_utente(conn, args.email)
    db.set_user_status(conn, u["id"], db.ST_ACTIVE)
    print(f"{u['callsign']} è ora attivo.")
    if not db.stations_of(conn, u["id"]):
        print("attenzione: non ha ancora accesso ad alcuna stazione. "
              "Assegnaglielo con 'permesso'.")


def cmd_sospendi(conn, args):
    u = trova_utente(conn, args.email)
    db.set_user_status(conn, u["id"], db.ST_SUSPENDED)
    print(f"{u['callsign']} è sospeso. Se era collegato, il relay lo chiude "
          f"entro pochi secondi.")


def cmd_password(conn, args):
    u = trova_utente(conn, args.email)
    print(f"nuova password per {u['callsign']} <{u['email']}>")
    db.set_password(conn, u["id"], chiedi_password())
    print("fatto.")


def cmd_stazioni(conn, args):
    righe = db.list_stations(conn)
    if not righe:
        print("nessuna stazione.")
        return
    for s in righe:
        titolare = db.user_by_id(conn, s["owner_id"])
        stato = "aperta" if s["enabled"] else "chiusa"
        print(f"{s['slug']:<16} {s['name'] or '—':<28} titolare "
              f"{titolare['callsign'] if titolare else '?':<10} {stato}")
        for m in db.members_of(conn, s["id"]):
            print(f"    {m['callsign']:<12} {RUOLI_INV.get(m['role'], m['role']):<12} "
                  f"{m['status']}")


def cmd_stazione_nuova(conn, args):
    if db.station_by_slug(conn, args.slug):
        sys.exit(f"la stazione '{args.slug}' esiste già")
    u = trova_utente(conn, args.titolare)
    sid = db.create_station(conn, args.slug, u["id"], name=args.nome or "",
                            callsign=args.nominativo or "")
    print(f"stazione '{args.slug}' creata (id {sid}), titolare {u['callsign']}.")


def cmd_permesso(conn, args):
    u = trova_utente(conn, args.email)
    s = trova_stazione(conn, args.stazione)
    ruolo = RUOLI.get(args.ruolo.lower())
    if not ruolo:
        sys.exit(f"ruolo sconosciuto: scegli fra {', '.join(RUOLI)}")
    db.grant(conn, u["id"], s["id"], ruolo)
    print(f"{u['callsign']} è {args.ruolo} sulla stazione '{s['slug']}'.")
    if u["status"] != db.ST_ACTIVE:
        print(f"attenzione: l'accesso di {u['callsign']} è '{u['status']}', "
              f"quindi il permesso non vale ancora. Attivalo con 'attiva'.")


def cmd_togli(conn, args):
    u = trova_utente(conn, args.email)
    s = trova_stazione(conn, args.stazione)
    if u["id"] == s["owner_id"]:
        sys.exit("non si può togliere il titolare dalla propria stazione: "
                 "cambia prima titolare.")
    db.revoke(conn, u["id"], s["id"])
    print(f"{u['callsign']} non ha più accesso a '{s['slug']}'.")


def cmd_log(conn, args):
    sid = trova_stazione(conn, args.stazione)["id"] if args.stazione else None
    print("— trasmissioni —")
    for t in db.recent_tx(conn, sid, args.righe):
        durata = f"{t['ended_at'] - t['started_at']} s" if t["ended_at"] else "in corso"
        print(f"{quando(t['started_at'])}  {t['callsign']:<12} {durata:<10} {t['addr']}")
    print("\n— collegamenti —")
    for c in db.recent_connections(conn, sid, args.righe):
        fine = quando(c["left_at"]) if c["left_at"] else "collegato"
        print(f"{quando(c['joined_at'])}  {c['callsign']:<12} "
              f"{RUOLI_INV.get(c['role'], c['role']):<12} {fine:<18} {c['addr']}")


def main():
    ap = argparse.ArgumentParser(description="Amministrazione del gateway Decolink")
    ap.add_argument("--db", default=db.default_path())
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="crea il primo amministratore").set_defaults(f=cmd_init)

    p = sub.add_parser("utenti", help="elenca gli utenti")
    p.add_argument("--stato", choices=[db.ST_PENDING, db.ST_ACTIVE, db.ST_SUSPENDED])
    p.set_defaults(f=cmd_utenti)

    for nome, fn, aiuto in (("attiva", cmd_attiva, "abilita un accesso"),
                            ("sospendi", cmd_sospendi, "sospende un accesso"),
                            ("password", cmd_password, "cambia la password")):
        p = sub.add_parser(nome, help=aiuto)
        p.add_argument("email")
        p.set_defaults(f=fn)

    sub.add_parser("stazioni", help="elenca stazioni e membri").set_defaults(f=cmd_stazioni)

    p = sub.add_parser("stazione-nuova", help="crea una stazione")
    p.add_argument("slug")
    p.add_argument("titolare", help="email del titolare")
    p.add_argument("--nome", default="")
    p.add_argument("--nominativo", default="")
    p.set_defaults(f=cmd_stazione_nuova)

    p = sub.add_parser("permesso", help="assegna un ruolo su una stazione")
    p.add_argument("email")
    p.add_argument("stazione")
    p.add_argument("ruolo", choices=list(RUOLI))
    p.set_defaults(f=cmd_permesso)

    p = sub.add_parser("togli", help="toglie l'accesso a una stazione")
    p.add_argument("email")
    p.add_argument("stazione")
    p.set_defaults(f=cmd_togli)

    p = sub.add_parser("log", help="registro di trasmissioni e collegamenti")
    p.add_argument("--stazione")
    p.add_argument("--righe", type=int, default=30)
    p.set_defaults(f=cmd_log)

    args = ap.parse_args()
    conn = db.connect(args.db)
    try:
        args.f(conn, args)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
