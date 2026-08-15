#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mette insieme i tre blocchi di traduzione e sceglie la lingua di chi legge.

I testi stanno in tre file per non averne uno solo da millecinquecento righe;
qui tornano a essere un dizionario unico, che e' come li usa la pagina.
"""

from traduzioni_sito import LINGUE, CODICI, RIPIEGO, T as _T1
from traduzioni_sito2 import T2 as _T2
from traduzioni_sito3 import T3 as _T3

T = {}
T.update(_T1)
T.update(_T2)
T.update(_T3)

# Se una lingua ha un buco lo si scopre adesso, all'avvio, e non quando un
# visitatore trova un pezzo di pagina vuoto.
_CHIAVI = set(T["it"])
for _c in CODICI:
    if _c not in T:
        raise RuntimeError(f"manca del tutto la lingua {_c}")
    _mancano = _CHIAVI - set(T[_c])
    if _mancano:
        raise RuntimeError(f"lingua {_c}: mancano {sorted(_mancano)}")


def normalizza(codice: str) -> str | None:
    """Da un codice qualsiasi a uno dei nostri, o None.

    I browser mandano roba come 'de-AT', 'pt-BR', 'zh-Hant-HK'. Il cinese va
    guardato per intero, perche' fra semplificato e tradizionale non e'
    questione di regione ma di scrittura.
    """
    if not codice:
        return None
    c = codice.strip().replace("_", "-")
    b = c.split("-")[0].lower()

    if b == "zh":
        resto = c.lower()
        if "hant" in resto or resto.endswith(("-tw", "-hk", "-mo")):
            return "zh_TW"
        return "zh"
    if b in CODICI:
        return b
    return None


def lingua_del_browser(accept_language: str) -> str:
    """La prima lingua gradita al browser fra quelle che abbiamo.

    Accept-Language arriva ordinato per preferenza con i pesi q=: 'it-IT,it;q=0.9,
    en;q=0.8'. Si rispetta quell'ordine invece di prendere la prima e basta,
    altrimenti chi ha l'italiano come terza scelta se lo vedrebbe imposto.
    """
    if not accept_language:
        return RIPIEGO
    voci = []
    for pezzo in accept_language.split(","):
        pezzo = pezzo.strip()
        if not pezzo:
            continue
        q = 1.0
        if ";" in pezzo:
            pezzo, _, param = pezzo.partition(";")
            param = param.strip()
            if param.startswith("q="):
                try:
                    q = float(param[2:])
                except ValueError:
                    q = 0.0
        voci.append((q, pezzo.strip()))
    for _, codice in sorted(voci, key=lambda v: -v[0]):
        n = normalizza(codice)
        if n:
            return n
    return RIPIEGO


def testi(codice: str) -> dict:
    """Il blocco di testi di una lingua, con ripiego se il codice non esiste."""
    return T.get(codice) or T[RIPIEGO]
