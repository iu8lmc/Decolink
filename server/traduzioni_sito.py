#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""I testi della prima pagina, nelle sedici lingue del client.

Il client parla sedici lingue e il sito ne parlava una. Chi arrivava da fuori
Italia leggeva le istruzioni in italiano, scaricava un programma che poi gli si
apriva nella sua lingua, e nel mezzo doveva indovinare.

Qui i testi stanno raccolti per lingua e non per chiave: ogni blocco si legge
come una pagina intera, e chi rilegge una traduzione vede il discorso invece di
trenta frasi sciolte.

I segnaposto {peso}, {versione} e {host} restano tali e quali: li riempie chi
costruisce la pagina.
"""

# L'ordine conta: e' quello in cui compaiono nel menu a tendina, e ogni lingua e'
# scritta nella propria lingua perche' chi non capisce le altre riconosca la sua.
LINGUE = [
    ("it",    "Italiano"),
    ("en",    "English"),
    ("de",    "Deutsch"),
    ("fr",    "Français"),
    ("es",    "Español"),
    ("pt",    "Português"),
    ("nl",    "Nederlands"),
    ("ca",    "Català"),
    ("da",    "Dansk"),
    ("hu",    "Magyar"),
    ("ro",    "Română"),
    ("lv",    "Latviešu"),
    ("ru",    "Русский"),
    ("ja",    "日本語"),
    ("zh",    "简体中文"),
    ("zh_TW", "繁體中文"),
]

CODICI = [c for c, _ in LINGUE]

# Lingua di ripiego: chi arriva con un browser che parla una lingua che non
# abbiamo legge l'inglese, non l'italiano. Il sito nasce italiano, ma chi capita
# da fuori ha piu' probabilita' di cavarsela con l'inglese.
RIPIEGO = "en"

T = {}

T["it"] = {
    "html": "it",
    "claim": "Porta la tua radio su Decodium Mobile",
    "sotto": "L'audio ricevuto e il controllo del rig viaggiano su internet, da casa "
             "al telefono, dovunque sia. Basta la scheda audio della radio: niente "
             "cavo OTG, niente Hamlib da installare sul telefono.",
    "scarica": "Scarica per Windows",
    "peso": "{versione} — {peso} MB, si scompatta e si avvia",
    "vai_github": "Vai su GitHub",
    "senza_ver": "Le versioni sono su GitHub",
    "h_cosa": "Che cosa fa",
    "p_cosa": "Manda al telefono l'audio del CODEC USB della radio e le fa da rigctld: "
              "frequenza, modo e PTT senza installare altro.",
    "h_serve": "Che cosa serve",
    "p_serve": "Windows 64 bit, la radio collegata via USB e un accesso a questo "
               "gateway. Niente da installare: si scompatta e si avvia.",
    "h_ovunque": "Funziona ovunque",
    "p_ovunque": "Anche col telefono su dati mobili: il PC e il telefono escono "
                 "entrambi verso il relay, quindi non c'è nessun router da configurare.",
    "h_parte": "Come si parte",
    "passo1": "Scarica l'archivio e scompattalo dove vuoi, anche su una chiavetta.",
    "passo2_no": "Serve un accesso approvato: <a href=\"/registrati\">richiedilo qui</a> "
                 "indicando il tuo nominativo e la stazione.",
    "passo2_si": "Serve un accesso approvato: ce l'hai già.",
    "passo3": "Avvia <b>Decolink.exe</b>, scrivi <b>{host}</b> come server di accesso, "
              "entra con le tue credenziali e scegli la stazione.",
    "passo4": "Scegli l'ingresso audio della radio, premi <b>Avvia</b> e sul telefono "
              "metti Collegamento = Relay.",
    "h_come": "Come funziona",
    "p_come": "Decolink prende l'audio che la radio manda al computer e lo spedisce al "
              "telefono, che lo fa ascoltare. Nello stesso collegamento passano i "
              "comandi del rig, così dal telefono si cambia frequenza e modo. Il "
              "telefono può stare in casa o dall'altra parte del mondo: cambia solo "
              "come i due si trovano.",
    "m1_t": "LAN diretta",
    "m1_p": "Il telefono è sulla stessa rete WiFi: gli si manda l'audio al suo "
            "indirizzo. È la strada più corta, ma vale solo dentro casa.",
    "m2_t": "Relay e stazione",
    "m2_p": "Funziona ovunque, anche su dati mobili. Il computer e il telefono escono "
            "tutti e due verso il relay, quindi non c'è nessun router da aprire. È "
            "l'unico modo che funziona sempre.",
    "m3_t": "Il telefono chiama casa",
    "m3_p": "Porta inoltrata sul router e un nome DynDNS. Serve a chi vuole fare a meno "
            "del relay e ha modo di configurare il proprio router.",
    "h_banda": "Quanto consuma",
    "p_banda": "Si sceglie quanto occupare: dal PCM a 48 kHz, che va con tutto, fino a "
               "32 kbit/s per la voce e 2,4 kbit/s per il solo ritmo del tasto in CW. "
               "Per un SSB, che di banda ne occupa 2,7 kHz, bastano 12 kHz di "
               "campionamento.",
    "h_lingue": "Sedici lingue",
    "p_lingue": "Decolink prende la lingua di Windows alla prima apertura, e si cambia "
                "dal menu in alto a destra. Italiano, inglese, tedesco, francese, "
                "spagnolo, portoghese, olandese, catalano, danese, ungherese, rumeno, "
                "lettone, russo, giapponese, cinese semplificato e tradizionale.",
    "accedi": "Accedi",
    "registrati": "Richiedi un accesso",
    "gia": "Hai già un accesso?",
    "sorgente": "Codice sorgente e cronologia delle versioni:",
    "lingua_et": "Lingua",
}

T["en"] = {
    "html": "en",
    "claim": "Put your radio on Decodium Mobile",
    "sotto": "Received audio and rig control travel over the internet, from home to "
             "your phone, wherever it is. All it takes is the radio's sound card: no "
             "OTG cable, no Hamlib to install on the phone.",
    "scarica": "Download for Windows",
    "peso": "{versione} — {peso} MB, unzip and run",
    "vai_github": "Go to GitHub",
    "senza_ver": "The releases are on GitHub",
    "h_cosa": "What it does",
    "p_cosa": "Sends the audio from the radio's USB CODEC to your phone and acts as "
              "rigctld: frequency, mode and PTT with nothing else to install.",
    "h_serve": "What you need",
    "p_serve": "64-bit Windows, the radio connected over USB and an account on this "
               "gateway. Nothing to install: unzip it and run it.",
    "h_ovunque": "Works anywhere",
    "p_ovunque": "Mobile data included: the PC and the phone both reach out to the "
                 "relay, so there is no router to configure.",
    "h_parte": "Getting started",
    "passo1": "Download the archive and unzip it wherever you like, a USB stick included.",
    "passo2_no": "You need an approved account: <a href=\"/registrati\">request one "
                 "here</a>, giving your callsign and station.",
    "passo2_si": "You need an approved account: you already have one.",
    "passo3": "Run <b>Decolink.exe</b>, type <b>{host}</b> as the sign-in server, sign "
              "in with your credentials and pick the station.",
    "passo4": "Choose the radio's audio input, press <b>Start</b>, and on the phone set "
              "Connection = Relay.",
    "h_come": "How it works",
    "p_come": "Decolink takes the audio the radio sends to the computer and forwards it "
              "to the phone, which plays it. Rig commands travel on the same link, so "
              "you change frequency and mode from the phone. The phone can be in the "
              "next room or on the other side of the world: only the way the two find "
              "each other changes.",
    "m1_t": "Direct LAN",
    "m1_p": "The phone is on the same WiFi: the audio goes straight to its address. "
            "Shortest path, but only inside the house.",
    "m2_t": "Relay and station",
    "m2_p": "Works anywhere, mobile data included. The computer and the phone both "
            "reach out to the relay, so there is no router to open. It is the only way "
            "that always works.",
    "m3_t": "The phone calls home",
    "m3_p": "A forwarded port on the router and a DynDNS name. For those who want to do "
            "without the relay and can configure their own router.",
    "h_banda": "How much it uses",
    "p_banda": "You choose how much: from 48 kHz PCM, which works with everything, down "
               "to 32 kbit/s for voice and 2.4 kbit/s for CW keying alone. For SSB, "
               "which occupies 2.7 kHz, sampling at 12 kHz is plenty.",
    "h_lingue": "Sixteen languages",
    "p_lingue": "Decolink picks up your Windows language the first time it opens, and "
                "you change it from the menu at the top right. Italian, English, "
                "German, French, Spanish, Portuguese, Dutch, Catalan, Danish, "
                "Hungarian, Romanian, Latvian, Russian, Japanese, Chinese simplified "
                "and traditional.",
    "accedi": "Sign in",
    "registrati": "Request an account",
    "gia": "Already have an account?",
    "sorgente": "Source code and version history:",
    "lingua_et": "Language",
}

T["de"] = {
    "html": "de",
    "claim": "Bring dein Funkgerät auf Decodium Mobile",
    "sotto": "Empfangenes Audio und Gerätesteuerung laufen übers Internet, von zu Hause "
             "aufs Telefon, wo immer es ist. Es genügt die Soundkarte des Funkgeräts: "
             "kein OTG-Kabel, kein Hamlib auf dem Telefon.",
    "scarica": "Für Windows herunterladen",
    "peso": "{versione} — {peso} MB, entpacken und starten",
    "vai_github": "Zu GitHub",
    "senza_ver": "Die Versionen liegen auf GitHub",
    "h_cosa": "Was es macht",
    "p_cosa": "Schickt das Audio des USB-CODECs vom Funkgerät aufs Telefon und dient "
              "als rigctld: Frequenz, Betriebsart und PTT, ohne weitere Installation.",
    "h_serve": "Was du brauchst",
    "p_serve": "Windows 64 Bit, das Funkgerät per USB angeschlossen und einen Zugang zu "
               "diesem Gateway. Nichts zu installieren: entpacken und starten.",
    "h_ovunque": "Funktioniert überall",
    "p_ovunque": "Auch mit Mobilfunk: PC und Telefon verbinden sich beide zum Relay, "
                 "also ist kein Router zu konfigurieren.",
    "h_parte": "So geht's los",
    "passo1": "Archiv herunterladen und entpacken, wohin du willst — auch auf einen "
              "USB-Stick.",
    "passo2_no": "Du brauchst einen freigegebenen Zugang: <a href=\"/registrati\">hier "
                 "beantragen</a>, mit Rufzeichen und Station.",
    "passo2_si": "Du brauchst einen freigegebenen Zugang: den hast du bereits.",
    "passo3": "<b>Decolink.exe</b> starten, <b>{host}</b> als Anmeldeserver eintragen, "
              "mit deinen Zugangsdaten anmelden und die Station wählen.",
    "passo4": "Den Audioeingang des Funkgeräts wählen, <b>Start</b> drücken und am "
              "Telefon Verbindung = Relay einstellen.",
    "h_come": "Wie es funktioniert",
    "p_come": "Decolink nimmt das Audio, das das Funkgerät an den Rechner schickt, und "
              "leitet es ans Telefon weiter, das es hörbar macht. Über dieselbe "
              "Verbindung laufen die Gerätebefehle, sodass sich Frequenz und "
              "Betriebsart vom Telefon aus ändern lassen. Das Telefon kann im "
              "Nebenzimmer stehen oder am anderen Ende der Welt: es ändert sich nur, "
              "wie die beiden zueinander finden.",
    "m1_t": "Direktes LAN",
    "m1_p": "Das Telefon ist im selben WLAN: das Audio geht direkt an seine Adresse. "
            "Der kürzeste Weg, gilt aber nur im Haus.",
    "m2_t": "Relay und Station",
    "m2_p": "Funktioniert überall, auch mobil. Rechner und Telefon verbinden sich beide "
            "zum Relay, es ist also kein Router zu öffnen. Der einzige Weg, der immer "
            "funktioniert.",
    "m3_t": "Das Telefon ruft zu Hause an",
    "m3_p": "Portweiterleitung im Router und ein DynDNS-Name. Für alle, die ohne Relay "
            "auskommen wollen und ihren Router selbst konfigurieren können.",
    "h_banda": "Wie viel es braucht",
    "p_banda": "Du wählst, wie viel: von PCM mit 48 kHz, das mit allem läuft, bis "
               "hinunter zu 32 kbit/s für Sprache und 2,4 kbit/s für die reine "
               "CW-Tastung. Für SSB, das 2,7 kHz belegt, reichen 12 kHz Abtastung "
               "reichlich.",
    "h_lingue": "Sechzehn Sprachen",
    "p_lingue": "Decolink übernimmt beim ersten Start die Sprache von Windows, ändern "
                "lässt sie sich oben rechts. Italienisch, Englisch, Deutsch, "
                "Französisch, Spanisch, Portugiesisch, Niederländisch, Katalanisch, "
                "Dänisch, Ungarisch, Rumänisch, Lettisch, Russisch, Japanisch, "
                "Chinesisch vereinfacht und traditionell.",
    "accedi": "Anmelden",
    "registrati": "Zugang beantragen",
    "gia": "Schon einen Zugang?",
    "sorgente": "Quellcode und Versionsgeschichte:",
    "lingua_et": "Sprache",
}

T["fr"] = {
    "html": "fr",
    "claim": "Emmenez votre radio sur Decodium Mobile",
    "sotto": "L'audio reçu et la commande du poste passent par internet, de la maison "
             "au téléphone, où qu'il soit. Il suffit de la carte son de la radio : pas "
             "de câble OTG, pas de Hamlib à installer sur le téléphone.",
    "scarica": "Télécharger pour Windows",
    "peso": "{versione} — {peso} Mo, on décompresse et on lance",
    "vai_github": "Aller sur GitHub",
    "senza_ver": "Les versions sont sur GitHub",
    "h_cosa": "Ce qu'il fait",
    "p_cosa": "Envoie au téléphone l'audio du CODEC USB de la radio et lui sert de "
              "rigctld : fréquence, mode et PTT sans rien d'autre à installer.",
    "h_serve": "Ce qu'il faut",
    "p_serve": "Windows 64 bits, la radio branchée en USB et un accès à cette "
               "passerelle. Rien à installer : on décompresse et on lance.",
    "h_ovunque": "Fonctionne partout",
    "p_ovunque": "Même en données mobiles : le PC et le téléphone sortent tous les deux "
                 "vers le relais, donc aucun routeur à configurer.",
    "h_parte": "Pour démarrer",
    "passo1": "Téléchargez l'archive et décompressez-la où vous voulez, même sur une "
              "clé USB.",
    "passo2_no": "Il faut un accès approuvé : <a href=\"/registrati\">demandez-le "
                 "ici</a> en indiquant votre indicatif et la station.",
    "passo2_si": "Il faut un accès approuvé : vous l'avez déjà.",
    "passo3": "Lancez <b>Decolink.exe</b>, saisissez <b>{host}</b> comme serveur de "
              "connexion, connectez-vous et choisissez la station.",
    "passo4": "Choisissez l'entrée audio de la radio, appuyez sur <b>Démarrer</b>, et "
              "sur le téléphone mettez Connexion = Relais.",
    "h_come": "Comment ça marche",
    "p_come": "Decolink prend l'audio que la radio envoie à l'ordinateur et le "
              "transmet au téléphone, qui le fait entendre. Les commandes du poste "
              "passent par la même liaison, si bien qu'on change fréquence et mode "
              "depuis le téléphone. Le téléphone peut être dans la pièce d'à côté ou à "
              "l'autre bout du monde : seule change la façon dont les deux se trouvent.",
    "m1_t": "LAN direct",
    "m1_p": "Le téléphone est sur le même WiFi : l'audio part droit vers son adresse. "
            "Le chemin le plus court, mais valable seulement à la maison.",
    "m2_t": "Relais et station",
    "m2_p": "Fonctionne partout, données mobiles comprises. L'ordinateur et le "
            "téléphone sortent tous les deux vers le relais, donc aucun routeur à "
            "ouvrir. C'est la seule façon qui marche toujours.",
    "m3_t": "Le téléphone appelle la maison",
    "m3_p": "Un port redirigé sur le routeur et un nom DynDNS. Pour qui veut se passer "
            "du relais et sait configurer son routeur.",
    "h_banda": "Ce que ça consomme",
    "p_banda": "On choisit combien : du PCM à 48 kHz, qui passe avec tout, jusqu'à "
               "32 kbit/s pour la voix et 2,4 kbit/s pour la seule manipulation en CW. "
               "Pour la BLU, qui occupe 2,7 kHz, un échantillonnage à 12 kHz suffit "
               "largement.",
    "h_lingue": "Seize langues",
    "p_lingue": "Decolink prend la langue de Windows au premier lancement, et elle se "
                "change depuis le menu en haut à droite. Italien, anglais, allemand, "
                "français, espagnol, portugais, néerlandais, catalan, danois, hongrois, "
                "roumain, letton, russe, japonais, chinois simplifié et traditionnel.",
    "accedi": "Se connecter",
    "registrati": "Demander un accès",
    "gia": "Vous avez déjà un accès ?",
    "sorgente": "Code source et historique des versions :",
    "lingua_et": "Langue",
}
