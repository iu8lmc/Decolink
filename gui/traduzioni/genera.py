#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Riempie i file .ts di Qt con le traduzioni del dizionario.

I .ts li crea lupdate leggendo il sorgente; qui si mettono dentro le traduzioni
e si marca come 'unfinished' quello che manca ancora, che e' esattamente come
Qt Linguist segnala il lavoro da fare.

    python genera.py            riempie i .ts e stampa la copertura
    python genera.py --stretto  esce con errore se una lingua e' sotto il 90%
"""

import os
import re
import sys
import xml.etree.ElementTree as ET

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)

from dizionario import LINGUE, UGUALI, T          # noqa: E402
from dizionario2 import T2                        # noqa: E402
from dizionario3 import T3                        # noqa: E402

TUTTE = dict(T)
TUTTE.update(T2)
TUTTE.update(T3)


def traduzione(fonte: str, lingua: str):
    """La traduzione di una stringa, o None se non c'e' ancora."""
    if fonte in UGUALI:
        return fonte                 # numeri e sigle restano com'erano
    voce = TUTTE.get(fonte)
    if not voce:
        return None
    return voce.get(lingua)


def riempi(percorso: str, lingua: str):
    albero = ET.parse(percorso)
    radice = albero.getroot()
    radice.set("language", lingua)

    totale = tradotte = 0
    mancanti = []
    for messaggio in radice.iter("message"):
        fonte = messaggio.find("source")
        if fonte is None or fonte.text is None:
            continue
        totale += 1
        testo = traduzione(fonte.text, lingua)
        nodo = messaggio.find("translation")
        if nodo is None:
            nodo = ET.SubElement(messaggio, "translation")
        if testo:
            nodo.text = testo
            if "type" in nodo.attrib:
                del nodo.attrib["type"]
            tradotte += 1
        else:
            # Qt Linguist mostra in rosso quelle non finite: e' il modo giusto
            # di dire "manca", invece di lasciare il testo italiano che poi
            # nessuno distingue da una traduzione vera.
            nodo.set("type", "unfinished")
            nodo.text = ""
            mancanti.append(fonte.text)

    albero.write(percorso, encoding="utf-8", xml_declaration=True)
    # Qt vuole il DOCTYPE, che ElementTree non scrive
    with open(percorso, encoding="utf-8") as f:
        testo = f.read()
    if "<!DOCTYPE TS>" not in testo:
        testo = testo.replace("?>", "?>\n<!DOCTYPE TS>", 1)
        with open(percorso, "w", encoding="utf-8") as f:
            f.write(testo)
    return totale, tradotte, mancanti


def main():
    stretto = "--stretto" in sys.argv
    print(f"  {len(TUTTE)} stringhe nel dizionario, {len(LINGUE)} lingue\n")
    peggiore = 100.0
    tutti_mancanti = {}
    for lingua in LINGUE:
        percorso = os.path.join(QUI, f"decolink_{lingua}.ts")
        if not os.path.exists(percorso):
            print(f"  {lingua}: file assente (lancia prima lupdate)")
            continue
        totale, fatte, mancanti = riempi(percorso, lingua)
        perc = 100.0 * fatte / max(1, totale)
        peggiore = min(peggiore, perc)
        for m in mancanti:
            tutti_mancanti.setdefault(m, 0)
            tutti_mancanti[m] += 1
        barra = "#" * int(perc / 5) + "." * (20 - int(perc / 5))
        print(f"  {lingua:<6} {barra} {fatte:3}/{totale}  {perc:5.1f}%")

    if tutti_mancanti:
        print(f"\n  stringhe ancora senza traduzione: {len(tutti_mancanti)}")
        for s, quante in sorted(tutti_mancanti.items(), key=lambda x: -x[1])[:12]:
            testo = s.replace("\n", " / ")
            print(f"    ({quante} lingue) {testo[:66]}")

    print(f"\n  copertura minima: {peggiore:.1f}%")
    if stretto and peggiore < 90:
        print("  sotto la soglia richiesta")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
