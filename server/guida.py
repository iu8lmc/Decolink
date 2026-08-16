#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mette insieme i testi della guida nelle sedici lingue e li controlla.

Il controllo si fa all'avvio, non quando un visitatore ci arriva sopra: una
chiave che manca in una lingua diventerebbe un buco nella pagina, e i buchi in
una lingua che non parliamo non li nota nessuno finche' non scrive qualcuno.
"""

from guida_testi import G as _G1
from guida_testi2 import G2 as _G2
from guida_testi3 import G3 as _G3
from guida_testi4 import G4 as _G4

TESTI = {}
TESTI.update(_G1)
TESTI.update(_G2)
TESTI.update(_G3)
TESTI.update(_G4)

_ATTESE = set(TESTI["it"])
for _cod, _blocco in TESTI.items():
    _mancano = _ATTESE - set(_blocco)
    if _mancano:
        raise RuntimeError(f"guida, lingua {_cod}: mancano {sorted(_mancano)}")
    _vuote = [k for k, v in _blocco.items() if not str(v).strip()]
    if _vuote:
        raise RuntimeError(f"guida, lingua {_cod}: vuote {sorted(_vuote)}")


def testi(codice: str) -> dict:
    """I testi della guida in una lingua, con ripiego sull'inglese."""
    return TESTI.get(codice) or TESTI["en"]


def lingue_pronte() -> list:
    return sorted(TESTI)


# Il richiamo alla guida sulla prima pagina. Sono due frasi sole e stanno qui
# invece che nel corpo della guida, perche' appartengono alla pagina che la
# annuncia, non a quella che la contiene.
INVITO = {
    "it": ("Guida passo passo", "Leggi la guida"),
    "en": ("Step-by-step guide", "Read the guide"),
    "de": ("Anleitung Schritt für Schritt", "Anleitung lesen"),
    "fr": ("Guide pas à pas", "Lire le guide"),
    "es": ("Guía paso a paso", "Leer la guía"),
    "pt": ("Guia passo a passo", "Ler o guia"),
    "nl": ("Stap voor stap", "Lees de handleiding"),
    "ca": ("Guia pas a pas", "Llegeix la guia"),
    "da": ("Trin for trin", "Læs vejledningen"),
    "hu": ("Lépésről lépésre", "Útmutató elolvasása"),
    "ro": ("Ghid pas cu pas", "Citește ghidul"),
    "lv": ("Soli pa solim", "Lasīt pamācību"),
    "ru": ("Пошаговое руководство", "Читать руководство"),
    "ja": ("手順ガイド", "ガイドを読む"),
    "zh": ("分步指南", "阅读指南"),
    "zh_TW": ("分步指南", "閱讀指南"),
}


def invito(codice: str) -> tuple:
    return INVITO.get(codice) or INVITO["en"]
