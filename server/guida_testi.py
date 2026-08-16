#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""I testi della guida: italiano, inglese, tedesco.

L'italiano e' l'originale, da cui vengono tutte le altre. I tag dentro le frasi
— <strong>, <em>, <code> — fanno parte del testo e vanno riportati anche nelle
traduzioni: cadono in punti diversi a seconda della lingua, e spezzarli fuori
renderebbe le frasi illeggibili a chi le traduce.
"""

G = {}

G["it"] = {
    "titolo": "Decodium Mobile su Decolink",
    "sottotitolo": "Come portare l'audio della radio — e il comando del rig — dal computer "
                   "di stazione al telefono: in casa sulla stessa rete, oppure ovunque "
                   "passando dal server.",
    "meta_app": "Decodium 4.0 Mobile",
    "meta_proto": "Decolink · protocollo HFGW v2",
    "meta_data": "16 agosto 2026",

    "h_prima": "Prima di cominciare",
    "s1_t": "Sul computer",
    "s1_p": "<strong>Decolink</strong> acceso accanto alla radio, con il CODEC USB del rig "
            "collegato. È lui che manda l'audio e, se vuoi, serve il CAT.",
    "s2_t": "Sul telefono",
    "s2_p": "<strong>Decodium 4 Mobile</strong>. Tutto si configura in un posto solo: "
            "l'ingranaggio ⚙ in alto, sezioni <em>Stazione</em>, <em>Audio</em> e "
            "<em>CAT / Rig</em>.",
    "s3_t": "Solo per il relay",
    "s3_p": "Un account approvato su <code>decolink.ft2.it</code>. In rete locale non serve: "
            "nessuna registrazione, nessun dato fuori da casa.",

    "h_tre": "I tre collegamenti",
    "tre_p": "Decolink e Decodium Mobile devono stare sullo <strong>stesso modo</strong>: "
             "è l'errore più comune, e non dà messaggi chiari.",
    "th_modo": "Modo", "th_quando": "Quando", "th_chi": "Chi chiama chi",
    "th_porta": "Porta", "th_aprire": "Da aprire",
    "lan": "LAN", "lan_q": "Telefono e computer sulla stessa WiFi",
    "lan_c": "Il computer spara l'audio all'IP del telefono", "lan_a": "Niente",
    "relay": "Relay", "relay_q": "Fuori casa, anche su dati mobili",
    "relay_c": "Tutti e due escono verso il server", "relay_a": "Niente",
    "casa": "Casa", "casa_q": "Fuori casa, senza passare dal server",
    "casa_c": "Il telefono chiama il tuo indirizzo di casa", "casa_a": "UDP 5555 sul router",
    "tre_fine": "Il <strong>relay</strong> è quello che funziona sempre: nessuno dei due deve "
                "essere raggiungibile dall'esterno, perché sono entrambi a farsi vivi verso "
                "il server. È anche l'unico che richiede un account.",

    "h_pa": "Percorso A · rete locale",
    "pa1_sigla": "Sul computer · Decolink",
    "pa1_h3": "Manda l'audio all'indirizzo del telefono",
    "pa1_1": '<span class="dove">Audio radio</span> → scegli il CODEC USB del ricetrasmettitore.',
    "pa1_1n": "È l'ingresso da cui arriva il segnale ricevuto, non il microfono del computer.",
    "pa1_2": '<span class="dove">Modalità</span> → <code>LAN diretta</code>',
    "pa1_3": '<span class="dove">Host</span> → l\'indirizzo IP del telefono sulla WiFi di casa.',
    "pa1_3n": "Sul telefono lo leggi in Impostazioni → WiFi → la rete a cui sei collegato. "
              "Somiglia a 192.168.1.42.",
    "pa1_4": '<span class="dove">Porta</span> → <code>5555</code>',
    "pa1_5": 'Premi <span class="dove">Avvia</span>. Il livello deve muoversi al ritmo del '
             'rumore di banda.',
    "pa2_sigla": "Sul telefono · Decodium Mobile",
    "pa2_h3": "Mettiti in ascolto",
    "pa2_1": '⚙ → <span class="dove">Stazione</span>: nominativo, locatore, report.',
    "pa2_1n": "Senza nominativo e locatore i messaggi non si possono comporre.",
    "pa2_2": '<span class="dove">Audio → Collegamento</span> → <code>LAN</code>',
    "pa2_3": '<span class="dove">Porta</span> → <code>5555</code>, la stessa scritta su Decolink',
    "pa2_4": 'Premi <span class="dove">Ricevi</span>. Compare <em>«In ascolto sulla porta '
             '5555»</em>: da quel momento il waterfall si popola appena il computer comincia '
             'a mandare.',
    "pa_avv_t": "In LAN il telefono aspetta, non chiama",
    "pa_avv_p": "È il computer che deve conoscere l'IP del telefono. Se il router assegna gli "
                "indirizzi a rotazione, domani quell'IP sarà di qualcun altro e l'audio non "
                "arriverà più: riserva al telefono un indirizzo fisso nel router, oppure "
                "ricontrolla il campo <em>Host</em> a ogni sessione.",

    "h_pb": "Percorso B · relay sul server",
    "pb1_sigla": "Una volta sola · dal browser",
    "pb1_h3": "Chiedi l'accesso alla stazione",
    "pb1_1": "Apri <code>https://decolink.ft2.it/registrati</code>",
    "pb1_2": "Compila email, password, nominativo e la stazione a cui vuoi collegarti.",
    "pb1_3": "Aspetta l'approvazione.",
    "pb1_3n": "La richiesta resta in attesa finché il titolare della stazione non la accetta: "
              "decide lui, non è automatico. È lui che stabilisce anche il tuo ruolo.",
    "ruolo_tit": "Titolare",
    "ruolo_tit_d": 'ascolta e trasmette <span class="libero">— è la stazione sua</span>',
    "ruolo_op": "Operatore",
    "ruolo_op_d": 'ascolta e trasmette <span class="libero">— autorizzato dal titolare</span>',
    "ruolo_asc": "Ascoltatore",
    "ruolo_asc_d": 'solo ricezione <span class="libero">— il tasto di trasmissione resta '
                   'spento</span>',
    "pb2_sigla": "Sul computer · Decolink",
    "pb2_h3": "Porta la stazione dentro il relay",
    "pb2_1": '<span class="dove">Server</span> → <code>decolink.ft2.it</code>, poi email e '
             'password, e premi <span class="dove">Accedi</span>.',
    "pb2_1n": "Se lasci la stazione accesa da sola, spunta «ricorda la password»: al riavvio "
              "riparte senza nessuno alla tastiera.",
    "pb2_2": '<span class="dove">Modalità</span> → <code>Relay + stazione</code>',
    "pb2_3": '<span class="dove">Host</span> → <code>decolink.ft2.it</code> · '
             '<span class="dove">Porta</span> → <code>5555</code>',
    "pb2_4": '<span class="dove">Profilo</span> → <code>PCM 48 kHz</code>',
    "pb2_4n": "I profili compressi consumano un quinto della banda, ma tienili per dopo: "
              "prima verifica che il collegamento regga così.",
    "pb2_5": 'Premi <span class="dove">Avvia</span>.',
    "pb3_sigla": "Sul telefono · Decodium Mobile",
    "pb3_h3": "Entra con le tue credenziali",
    "pb3_1": '⚙ → <span class="dove">Audio → Collegamento</span> → <code>Relay</code>',
    "pb3_2": 'Compila i campi dell\'accesso e premi <span class="dove">Entra</span>.',
    "pb3_3": "Controlla la riga di stato: deve dire il tuo nominativo, la stazione e il ruolo.",
    "pb3_3n": "Se leggi «Sei entrato come ascoltatore», ricevi ma non trasmetti: è il ruolo, "
              "non un guasto.",
    "pb3_4": '<span class="dove">Porta</span> → <code>5555</code>, poi '
             '<span class="dove">Ricevi</span>.',
    "campi_acc": "Accesso",
    "campi_email": "Email", "campi_email_d": "quella con cui ti sei registrato",
    "campi_pw": "Password", "campi_pw_d": "quella dell'account Decolink",
    "campi_relay": "Relay", "campi_relay_d": "lascia vuoto: prende l'indirizzo dell'accesso",
    "campi_porta": "Porta",
    "pb_avv_t": "Il permesso dura un'ora",
    "pb_avv_p": "Il server rilascia un lasciapassare che scade dopo sessanta minuti. Con "
                "<em>«Ricorda la password»</em> attivo l'app lo rinnova da sola un minuto "
                "prima; senza, dopo un'ora l'audio si ferma senza spiegazioni e devi rientrare "
                "a mano. Sul telefono la password sta nel portachiavi cifrato del sistema, "
                "fuori dai backup.",

    "h_pc": "Percorso C · il telefono chiama casa",
    "pc_p": "Serve a chi non vuole passare dal server e ha un indirizzo raggiungibile da fuori. "
            "In cambio bisogna mettere le mani nel router.",
    "pc_1": '<span class="dove">Sul router</span>: inoltra la porta <code>UDP 5555</code> '
            'verso l\'indirizzo del computer di stazione.',
    "pc_2": '<span class="dove">Su Decolink</span>: modalità <code>Il telefono chiama casa</code>, '
            'porta <code>5555</code>. Il campo Host resta vuoto: è il telefono a farsi vivo.',
    "pc_3": '<span class="dove">Sul telefono</span>: collegamento <code>Casa</code>, nel campo '
            'indirizzo il tuo nome DynDNS (per esempio <code>iu8lmc.ddns.net</code>), porta '
            '<code>5555</code>, poi <span class="dove">Ricevi</span>.',
    "pc_fine": "Con una connessione di casa dietro CG-NAT — molte fibre e quasi tutte le linee "
               "mobili — questo modo non può funzionare: nessuno da fuori riesce a "
               "raggiungerti. È esattamente il caso in cui esiste il relay.",

    "h_cat": "Comandare la radio",
    "cat_p": "L'audio e il CAT sono due cose separate: puoi ricevere senza CAT, ma senza CAT "
             "il telefono non sa su che frequenza sei e non può cambiare banda né mandare in "
             "trasmissione.",
    "cat_th1": "Sorgente", "cat_th2": "Come si collega", "cat_th3": "Dove funziona",
    "cat_r1": "TCP al PC",
    "cat_r1d": 'Su Decolink spunta <em>«Servi il CAT al telefono»</em>; sul telefono metti '
               'l\'IP del computer e la porta <span class="num">4532</span>',
    "cat_r1w": "Rete locale",
    "cat_r2": "USB-OTG",
    "cat_r2d": "Cavo dal telefono alla radio, nessun computer di mezzo",
    "cat_r2w": "Ovunque, con la radio a portata di cavo",
    "cat_r3": "Canale audio",
    "cat_r3d": "I comandi viaggiano dentro il collegamento audio già aperto",
    "cat_r3w": "Ovunque — è la scelta giusta con Relay o Casa",
    "cat_fine": "Con il <em>canale audio</em> non serve aprire nulla in più: perché funzioni "
                "devono essere veri due presupposti — l'audio di rete già avviato, e il CAT "
                "acceso su Decolink.",

    "h_guai": "Quando non arriva niente",
    "g1_m": "«In ascolto sulla porta 5555 — il PC deve mandare qui l'audio»",
    "g1_c": "Sei in modo <strong>LAN</strong> ma volevi il relay. In LAN il telefono aspetta e "
            "basta: nessuna registrazione parte, e resti ad aspettare un audio che nessuno "
            "manderà. Cambia il collegamento in <em>Relay</em>.",
    "g2_m": "«Nome non risolto»",
    "g2_c": "L'indirizzo scritto nel campo non esiste o il telefono è senza rete. Controlla di "
            "non aver incluso <code>https://</code> nel campo del relay.",
    "g3_m": "«Porta 5555 occupata»",
    "g3_c": "Un'altra app tiene quella porta. Chiudila, oppure usane un'altra — cambiandola in "
            "tutti e due i programmi.",
    "g4_m": "«server non raggiungibile»",
    "g4_c": "È un problema di collegamento, non di password: l'app distingue i due casi apposta. "
            "Verifica di avere rete e riprova.",
    "g5_m": "L'audio parte e si ferma dopo pochi secondi",
    "g5_c": "Il relay scarta chi resta zitto per quindici secondi. Se succede di continuo, la "
            "rete sta perdendo pacchetti: prova un profilo compresso, che occupa un quinto "
            "della banda.",
    "g6_m": "Il waterfall si muove ma non decodifica nulla",
    "g6_c": "Quasi sempre è l'orologio: i modi digitali stanno o cadono sul secondo esatto. "
            "Lascia che il telefono prenda l'ora dalla rete.",

    "h_demo": "Provare senza radio",
    "demo_p": "Il tasto <strong>Demo</strong>, accanto a <em>Ricevi</em>, accende una banda "
              "finta con cinque stazioni e decodifiche che scorrono. Serve a vedere come si "
              "comporta l'app prima di collegare qualsiasi cosa — utile per capire dove "
              "guardare, prima di andare a cercare un guasto che non c'è.",

    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — i valori indicati sono quelli predefiniti "
             "dei due programmi al 16 agosto 2026.",
}

G["en"] = {
    "titolo": "Decodium Mobile over Decolink",
    "sottotitolo": "How to bring the radio's audio — and rig control — from the shack computer "
                   "to your phone: at home on the same network, or anywhere at all through "
                   "the server.",
    "meta_app": "Decodium 4.0 Mobile",
    "meta_proto": "Decolink · HFGW v2 protocol",
    "meta_data": "16 August 2026",

    "h_prima": "Before you start",
    "s1_t": "On the computer",
    "s1_p": "<strong>Decolink</strong> running next to the radio, with the rig's USB CODEC "
            "connected. It sends the audio and, if you want, serves the CAT.",
    "s2_t": "On the phone",
    "s2_p": "<strong>Decodium 4 Mobile</strong>. Everything is set in one place: the ⚙ gear at "
            "the top, sections <em>Station</em>, <em>Audio</em> and <em>CAT / Rig</em>.",
    "s3_t": "Only for the relay",
    "s3_p": "An approved account on <code>decolink.ft2.it</code>. On a local network you don't "
            "need one: no registration, nothing leaves the house.",

    "h_tre": "The three connections",
    "tre_p": "Decolink and Decodium Mobile must be on the <strong>same mode</strong>: it is the "
             "commonest mistake, and it gives no clear message.",
    "th_modo": "Mode", "th_quando": "When", "th_chi": "Who calls whom",
    "th_porta": "Port", "th_aprire": "To open",
    "lan": "LAN", "lan_q": "Phone and computer on the same WiFi",
    "lan_c": "The computer fires the audio at the phone's IP", "lan_a": "Nothing",
    "relay": "Relay", "relay_q": "Away from home, mobile data included",
    "relay_c": "Both reach out to the server", "relay_a": "Nothing",
    "casa": "Home", "casa_q": "Away from home, without the server",
    "casa_c": "The phone calls your home address", "casa_a": "UDP 5555 on the router",
    "tre_fine": "The <strong>relay</strong> is the one that always works: neither side has to "
                "be reachable from outside, because both are the ones making contact with the "
                "server. It is also the only one that needs an account.",

    "h_pa": "Route A · local network",
    "pa1_sigla": "On the computer · Decolink",
    "pa1_h3": "Send the audio to the phone's address",
    "pa1_1": '<span class="dove">Radio audio</span> → pick the transceiver\'s USB CODEC.',
    "pa1_1n": "It is the input the received signal arrives on, not the computer's microphone.",
    "pa1_2": '<span class="dove">Mode</span> → <code>Direct LAN</code>',
    "pa1_3": '<span class="dove">Host</span> → the phone\'s IP address on your home WiFi.',
    "pa1_3n": "On the phone you find it in Settings → WiFi → the network you are connected to. "
              "It looks like 192.168.1.42.",
    "pa1_4": '<span class="dove">Port</span> → <code>5555</code>',
    "pa1_5": 'Press <span class="dove">Start</span>. The level should move with the band noise.',
    "pa2_sigla": "On the phone · Decodium Mobile",
    "pa2_h3": "Start listening",
    "pa2_1": '⚙ → <span class="dove">Station</span>: callsign, locator, report.',
    "pa2_1n": "Without callsign and locator the messages cannot be composed.",
    "pa2_2": '<span class="dove">Audio → Connection</span> → <code>LAN</code>',
    "pa2_3": '<span class="dove">Port</span> → <code>5555</code>, the same one set in Decolink',
    "pa2_4": 'Press <span class="dove">Receive</span>. <em>“Listening on port 5555”</em> '
             'appears: from then on the waterfall fills up as soon as the computer starts '
             'sending.',
    "pa_avv_t": "On LAN the phone waits, it does not call",
    "pa_avv_p": "It is the computer that has to know the phone's IP. If the router hands out "
                "addresses in rotation, tomorrow that IP will belong to someone else and the "
                "audio will not arrive: reserve a fixed address for the phone in the router, "
                "or check the <em>Host</em> field every session.",

    "h_pb": "Route B · relay on the server",
    "pb1_sigla": "Once only · from the browser",
    "pb1_h3": "Request access to the station",
    "pb1_1": "Open <code>https://decolink.ft2.it/registrati</code>",
    "pb1_2": "Fill in email, password, callsign and the station you want to connect to.",
    "pb1_3": "Wait for approval.",
    "pb1_3n": "The request stays pending until the station owner accepts it: they decide, it is "
              "not automatic. They also set your role.",
    "ruolo_tit": "Owner",
    "ruolo_tit_d": 'listens and transmits <span class="libero">— it is their station</span>',
    "ruolo_op": "Operator",
    "ruolo_op_d": 'listens and transmits <span class="libero">— authorised by the owner</span>',
    "ruolo_asc": "Listener",
    "ruolo_asc_d": 'receive only <span class="libero">— the transmit button stays off</span>',
    "pb2_sigla": "On the computer · Decolink",
    "pb2_h3": "Bring the station into the relay",
    "pb2_1": '<span class="dove">Server</span> → <code>decolink.ft2.it</code>, then email and '
             'password, and press <span class="dove">Sign in</span>.',
    "pb2_1n": "If you leave the station running on its own, tick “remember the password”: after "
              "a restart it comes back with nobody at the keyboard.",
    "pb2_2": '<span class="dove">Mode</span> → <code>Relay + station</code>',
    "pb2_3": '<span class="dove">Host</span> → <code>decolink.ft2.it</code> · '
             '<span class="dove">Port</span> → <code>5555</code>',
    "pb2_4": '<span class="dove">Profile</span> → <code>PCM 48 kHz</code>',
    "pb2_4n": "Compressed profiles use a fifth of the bandwidth, but save them for later: first "
              "make sure the link holds up like this.",
    "pb2_5": 'Press <span class="dove">Start</span>.',
    "pb3_sigla": "On the phone · Decodium Mobile",
    "pb3_h3": "Sign in with your credentials",
    "pb3_1": '⚙ → <span class="dove">Audio → Connection</span> → <code>Relay</code>',
    "pb3_2": 'Fill in the sign-in fields and press <span class="dove">Enter</span>.',
    "pb3_3": "Check the status line: it should give your callsign, the station and the role.",
    "pb3_3n": "If it says “You are in as a listener”, you receive but do not transmit: that is "
              "the role, not a fault.",
    "pb3_4": '<span class="dove">Port</span> → <code>5555</code>, then '
             '<span class="dove">Receive</span>.',
    "campi_acc": "Sign-in",
    "campi_email": "Email", "campi_email_d": "the one you registered with",
    "campi_pw": "Password", "campi_pw_d": "the one for your Decolink account",
    "campi_relay": "Relay", "campi_relay_d": "leave empty: it takes the sign-in address",
    "campi_porta": "Port",
    "pb_avv_t": "The permit lasts an hour",
    "pb_avv_p": "The server issues a pass that expires after sixty minutes. With "
                "<em>“Remember the password”</em> on, the app renews it by itself a minute "
                "before; without it, after an hour the audio stops with no explanation and you "
                "have to sign in again by hand. On the phone the password lives in the system's "
                "encrypted keychain, out of the backups.",

    "h_pc": "Route C · the phone calls home",
    "pc_p": "For those who would rather not go through the server and have an address reachable "
            "from outside. In exchange you have to get your hands into the router.",
    "pc_1": '<span class="dove">On the router</span>: forward port <code>UDP 5555</code> to the '
            'shack computer\'s address.',
    "pc_2": '<span class="dove">In Decolink</span>: mode <code>The phone calls home</code>, port '
            '<code>5555</code>. The Host field stays empty: it is the phone that makes contact.',
    "pc_3": '<span class="dove">On the phone</span>: connection <code>Home</code>, in the address '
            'field your DynDNS name (for example <code>iu8lmc.ddns.net</code>), port '
            '<code>5555</code>, then <span class="dove">Receive</span>.',
    "pc_fine": "With a home connection behind CG-NAT — many fibre lines and nearly every mobile "
               "one — this mode cannot work: nobody outside can reach you. That is exactly the "
               "case the relay exists for.",

    "h_cat": "Commanding the radio",
    "cat_p": "Audio and CAT are two separate things: you can receive without CAT, but without "
             "CAT the phone does not know what frequency you are on and cannot change band or "
             "key the transmitter.",
    "cat_th1": "Source", "cat_th2": "How it connects", "cat_th3": "Where it works",
    "cat_r1": "TCP to the PC",
    "cat_r1d": 'In Decolink tick <em>“Serve the CAT to the phone”</em>; on the phone put the '
               'computer\'s IP and port <span class="num">4532</span>',
    "cat_r1w": "Local network",
    "cat_r2": "USB-OTG",
    "cat_r2d": "A cable from phone to radio, no computer in between",
    "cat_r2w": "Anywhere, with the radio within cable reach",
    "cat_r3": "Audio channel",
    "cat_r3d": "The commands travel inside the audio link that is already open",
    "cat_r3w": "Anywhere — the right choice with Relay or Home",
    "cat_fine": "With the <em>audio channel</em> there is nothing extra to open: for it to work "
                "two things must be true — the network audio already started, and CAT switched "
                "on in Decolink.",

    "h_guai": "When nothing arrives",
    "g1_m": "“Listening on port 5555 — the PC must send the audio here”",
    "g1_c": "You are in <strong>LAN</strong> mode but you wanted the relay. On LAN the phone "
            "just waits: no registration goes out, and you sit waiting for audio nobody will "
            "send. Change the connection to <em>Relay</em>.",
    "g2_m": "“Name not resolved”",
    "g2_c": "The address in the field does not exist, or the phone has no network. Check you "
            "have not included <code>https://</code> in the relay field.",
    "g3_m": "“Port 5555 busy”",
    "g3_c": "Another app is holding that port. Close it, or use a different one — changing it "
            "in both programs.",
    "g4_m": "“server unreachable”",
    "g4_c": "This is a connection problem, not a password one: the app tells the two apart on "
            "purpose. Check you have network and try again.",
    "g5_m": "The audio starts and stops after a few seconds",
    "g5_c": "The relay drops anyone silent for fifteen seconds. If it keeps happening, the "
            "network is losing packets: try a compressed profile, which takes a fifth of the "
            "bandwidth.",
    "g6_m": "The waterfall moves but nothing decodes",
    "g6_c": "Nearly always it is the clock: digital modes stand or fall on the exact second. "
            "Let the phone take the time from the network.",

    "h_demo": "Trying it without a radio",
    "demo_p": "The <strong>Demo</strong> button, next to <em>Receive</em>, lights up a made-up "
              "band with five stations and decodes scrolling by. It is there to show how the "
              "app behaves before connecting anything — useful for learning where to look, "
              "before going hunting for a fault that isn't there.",

    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — the values given are the two programs' "
             "defaults as of 16 August 2026.",
}

G["de"] = {
    "titolo": "Decodium Mobile über Decolink",
    "sottotitolo": "Wie das Audio des Funkgeräts — und die Gerätesteuerung — vom Shack-Rechner "
                   "aufs Telefon kommt: zu Hause im selben Netz oder überall sonst über den "
                   "Server.",
    "meta_app": "Decodium 4.0 Mobile",
    "meta_proto": "Decolink · Protokoll HFGW v2",
    "meta_data": "16. August 2026",

    "h_prima": "Bevor es losgeht",
    "s1_t": "Am Rechner",
    "s1_p": "<strong>Decolink</strong> läuft neben dem Funkgerät, mit angeschlossenem "
            "USB-CODEC des Geräts. Es schickt das Audio und stellt auf Wunsch das CAT bereit.",
    "s2_t": "Am Telefon",
    "s2_p": "<strong>Decodium 4 Mobile</strong>. Alles wird an einer Stelle eingestellt: das "
            "Zahnrad ⚙ oben, Abschnitte <em>Station</em>, <em>Audio</em> und <em>CAT / Rig</em>.",
    "s3_t": "Nur für das Relay",
    "s3_p": "Ein freigegebener Zugang auf <code>decolink.ft2.it</code>. Im lokalen Netz braucht "
            "es keinen: keine Anmeldung, nichts verlässt das Haus.",

    "h_tre": "Die drei Verbindungen",
    "tre_p": "Decolink und Decodium Mobile müssen auf derselben <strong>Betriebsart</strong> "
             "stehen: das ist der häufigste Fehler, und er meldet sich nicht deutlich.",
    "th_modo": "Art", "th_quando": "Wann", "th_chi": "Wer ruft wen",
    "th_porta": "Port", "th_aprire": "Zu öffnen",
    "lan": "LAN", "lan_q": "Telefon und Rechner im selben WLAN",
    "lan_c": "Der Rechner schickt das Audio an die IP des Telefons", "lan_a": "Nichts",
    "relay": "Relay", "relay_q": "Unterwegs, auch im Mobilfunk",
    "relay_c": "Beide verbinden sich zum Server", "relay_a": "Nichts",
    "casa": "Zuhause", "casa_q": "Unterwegs, ohne den Server",
    "casa_c": "Das Telefon ruft deine Heimadresse an", "casa_a": "UDP 5555 im Router",
    "tre_fine": "Das <strong>Relay</strong> ist die Art, die immer funktioniert: keine der "
                "beiden Seiten muss von außen erreichbar sein, denn beide melden sich von "
                "selbst beim Server. Es ist auch die einzige, die einen Zugang braucht.",

    "h_pa": "Weg A · lokales Netz",
    "pa1_sigla": "Am Rechner · Decolink",
    "pa1_h3": "Schick das Audio an die Adresse des Telefons",
    "pa1_1": '<span class="dove">Funkgerät-Audio</span> → den USB-CODEC des Transceivers wählen.',
    "pa1_1n": "Das ist der Eingang, an dem das empfangene Signal ankommt, nicht das Mikrofon "
              "des Rechners.",
    "pa1_2": '<span class="dove">Betriebsart</span> → <code>Direktes LAN</code>',
    "pa1_3": '<span class="dove">Host</span> → die IP-Adresse des Telefons im heimischen WLAN.',
    "pa1_3n": "Am Telefon steht sie unter Einstellungen → WLAN → das verbundene Netz. Sie sieht "
              "aus wie 192.168.1.42.",
    "pa1_4": '<span class="dove">Port</span> → <code>5555</code>',
    "pa1_5": 'Auf <span class="dove">Start</span> drücken. Der Pegel muss sich im Takt des '
             'Bandrauschens bewegen.',
    "pa2_sigla": "Am Telefon · Decodium Mobile",
    "pa2_h3": "Auf Empfang gehen",
    "pa2_1": '⚙ → <span class="dove">Station</span>: Rufzeichen, Locator, Rapport.',
    "pa2_1n": "Ohne Rufzeichen und Locator lassen sich die Meldungen nicht zusammensetzen.",
    "pa2_2": '<span class="dove">Audio → Verbindung</span> → <code>LAN</code>',
    "pa2_3": '<span class="dove">Port</span> → <code>5555</code>, derselbe wie in Decolink',
    "pa2_4": 'Auf <span class="dove">Empfangen</span> drücken. Es erscheint <em>„Höre auf Port '
             '5555“</em>: von da an füllt sich der Wasserfall, sobald der Rechner zu senden '
             'beginnt.',
    "pa_avv_t": "Im LAN wartet das Telefon, es ruft nicht an",
    "pa_avv_p": "Der Rechner muss die IP des Telefons kennen. Vergibt der Router die Adressen "
                "reihum, gehört diese IP morgen jemand anderem und das Audio kommt nicht mehr "
                "an: reserviere dem Telefon im Router eine feste Adresse, oder prüfe das Feld "
                "<em>Host</em> vor jeder Sitzung.",

    "h_pb": "Weg B · Relay auf dem Server",
    "pb1_sigla": "Einmalig · im Browser",
    "pb1_h3": "Zugang zur Station beantragen",
    "pb1_1": "<code>https://decolink.ft2.it/registrati</code> öffnen",
    "pb1_2": "E-Mail, Passwort, Rufzeichen und die gewünschte Station eintragen.",
    "pb1_3": "Auf die Freigabe warten.",
    "pb1_3n": "Der Antrag bleibt offen, bis der Stationsinhaber ihn annimmt: er entscheidet, "
              "automatisch geht das nicht. Er legt auch deine Rolle fest.",
    "ruolo_tit": "Inhaber",
    "ruolo_tit_d": 'hört und sendet <span class="libero">— es ist seine Station</span>',
    "ruolo_op": "Operator",
    "ruolo_op_d": 'hört und sendet <span class="libero">— vom Inhaber berechtigt</span>',
    "ruolo_asc": "Zuhörer",
    "ruolo_asc_d": 'nur Empfang <span class="libero">— die Sendetaste bleibt aus</span>',
    "pb2_sigla": "Am Rechner · Decolink",
    "pb2_h3": "Bring die Station ins Relay",
    "pb2_1": '<span class="dove">Server</span> → <code>decolink.ft2.it</code>, dann E-Mail und '
             'Passwort, und auf <span class="dove">Anmelden</span> drücken.',
    "pb2_1n": "Bleibt die Station allein in Betrieb, „Passwort merken“ ankreuzen: nach einem "
              "Neustart läuft sie wieder an, ohne dass jemand an der Tastatur sitzt.",
    "pb2_2": '<span class="dove">Betriebsart</span> → <code>Relay + Station</code>',
    "pb2_3": '<span class="dove">Host</span> → <code>decolink.ft2.it</code> · '
             '<span class="dove">Port</span> → <code>5555</code>',
    "pb2_4": '<span class="dove">Profil</span> → <code>PCM 48 kHz</code>',
    "pb2_4n": "Die komprimierten Profile brauchen ein Fünftel der Bandbreite, aber hebe sie dir "
              "auf: prüfe erst, ob die Verbindung so trägt.",
    "pb2_5": 'Auf <span class="dove">Start</span> drücken.',
    "pb3_sigla": "Am Telefon · Decodium Mobile",
    "pb3_h3": "Mit deinen Zugangsdaten anmelden",
    "pb3_1": '⚙ → <span class="dove">Audio → Verbindung</span> → <code>Relay</code>',
    "pb3_2": 'Die Anmeldefelder ausfüllen und auf <span class="dove">Anmelden</span> drücken.',
    "pb3_3": "Die Statuszeile prüfen: dort müssen dein Rufzeichen, die Station und die Rolle "
             "stehen.",
    "pb3_3n": "Steht dort „Du bist als Zuhörer drin“, empfängst du, sendest aber nicht: das ist "
              "die Rolle, kein Fehler.",
    "pb3_4": '<span class="dove">Port</span> → <code>5555</code>, dann '
             '<span class="dove">Empfangen</span>.',
    "campi_acc": "Anmeldung",
    "campi_email": "E-Mail", "campi_email_d": "die, mit der du dich registriert hast",
    "campi_pw": "Passwort", "campi_pw_d": "das deines Decolink-Zugangs",
    "campi_relay": "Relay", "campi_relay_d": "leer lassen: es nimmt die Adresse der Anmeldung",
    "campi_porta": "Port",
    "pb_avv_t": "Die Erlaubnis gilt eine Stunde",
    "pb_avv_p": "Der Server gibt einen Ausweis aus, der nach sechzig Minuten abläuft. Ist "
                "<em>„Passwort merken“</em> aktiv, erneuert die App ihn eine Minute vorher von "
                "selbst; ohne bleibt das Audio nach einer Stunde ohne Erklärung stehen und du "
                "musst dich von Hand neu anmelden. Auf dem Telefon liegt das Passwort im "
                "verschlüsselten Schlüsselbund des Systems, außerhalb der Sicherungen.",

    "h_pc": "Weg C · das Telefon ruft zu Hause an",
    "pc_p": "Für alle, die den Server umgehen wollen und eine von außen erreichbare Adresse "
            "haben. Dafür muss man in den Router hinein.",
    "pc_1": '<span class="dove">Im Router</span>: den Port <code>UDP 5555</code> an die Adresse '
            'des Shack-Rechners weiterleiten.',
    "pc_2": '<span class="dove">In Decolink</span>: Betriebsart <code>Das Telefon ruft zu Hause '
            'an</code>, Port <code>5555</code>. Das Feld Host bleibt leer: das Telefon meldet '
            'sich.',
    "pc_3": '<span class="dove">Am Telefon</span>: Verbindung <code>Zuhause</code>, im '
            'Adressfeld dein DynDNS-Name (zum Beispiel <code>iu8lmc.ddns.net</code>), Port '
            '<code>5555</code>, dann <span class="dove">Empfangen</span>.',
    "pc_fine": "Bei einem Hausanschluss hinter CG-NAT — viele Glasfaseranschlüsse und fast alle "
               "Mobilfunkleitungen — kann diese Art nicht funktionieren: von außen erreicht "
               "dich niemand. Genau dafür gibt es das Relay.",

    "h_cat": "Das Funkgerät steuern",
    "cat_p": "Audio und CAT sind zwei getrennte Dinge: empfangen geht auch ohne CAT, aber ohne "
             "CAT weiß das Telefon nicht, auf welcher Frequenz du bist, und kann weder das Band "
             "wechseln noch auf Sendung gehen.",
    "cat_th1": "Quelle", "cat_th2": "Wie es sich verbindet", "cat_th3": "Wo es geht",
    "cat_r1": "TCP zum PC",
    "cat_r1d": 'In Decolink <em>„CAT ans Telefon liefern“</em> ankreuzen; am Telefon die IP des '
               'Rechners und Port <span class="num">4532</span> eintragen',
    "cat_r1w": "Lokales Netz",
    "cat_r2": "USB-OTG",
    "cat_r2d": "Kabel vom Telefon zum Funkgerät, kein Rechner dazwischen",
    "cat_r2w": "Überall, solange das Funkgerät in Kabellänge steht",
    "cat_r3": "Audiokanal",
    "cat_r3d": "Die Befehle laufen in der bereits offenen Audioverbindung mit",
    "cat_r3w": "Überall — die richtige Wahl bei Relay oder Zuhause",
    "cat_fine": "Beim <em>Audiokanal</em> ist nichts weiter zu öffnen: damit er funktioniert, "
                "müssen zwei Dinge stimmen — das Netz-Audio läuft bereits, und CAT ist in "
                "Decolink eingeschaltet.",

    "h_guai": "Wenn nichts ankommt",
    "g1_m": "„Höre auf Port 5555 — der PC muss das Audio hierher schicken“",
    "g1_c": "Du bist in der Betriebsart <strong>LAN</strong>, wolltest aber das Relay. Im LAN "
            "wartet das Telefon nur: es meldet sich nirgends an, und du wartest auf Audio, das "
            "niemand schickt. Stell die Verbindung auf <em>Relay</em>.",
    "g2_m": "„Name nicht aufgelöst“",
    "g2_c": "Die eingetragene Adresse gibt es nicht, oder das Telefon hat kein Netz. Prüfe, ob "
            "im Relay-Feld versehentlich <code>https://</code> steht.",
    "g3_m": "„Port 5555 belegt“",
    "g3_c": "Eine andere App hält diesen Port. Schließe sie, oder nimm einen anderen — und "
            "ändere ihn in beiden Programmen.",
    "g4_m": "„Server nicht erreichbar“",
    "g4_c": "Das ist ein Verbindungsproblem, kein Passwortproblem: die App unterscheidet beides "
            "mit Absicht. Prüfe, ob du Netz hast, und versuch es noch einmal.",
    "g5_m": "Das Audio läuft an und bricht nach wenigen Sekunden ab",
    "g5_c": "Das Relay wirft hinaus, wer fünfzehn Sekunden lang stumm bleibt. Passiert das "
            "andauernd, verliert das Netz Pakete: versuch ein komprimiertes Profil, das ein "
            "Fünftel der Bandbreite braucht.",
    "g6_m": "Der Wasserfall läuft, aber nichts wird dekodiert",
    "g6_c": "Fast immer ist es die Uhr: die digitalen Betriebsarten stehen und fallen mit der "
            "exakten Sekunde. Lass das Telefon die Zeit aus dem Netz holen.",

    "h_demo": "Ohne Funkgerät ausprobieren",
    "demo_p": "Die Taste <strong>Demo</strong> neben <em>Empfangen</em> schaltet ein erfundenes "
              "Band mit fünf Stationen und durchlaufenden Dekodierungen ein. Sie zeigt, wie "
              "sich die App verhält, bevor irgendetwas angeschlossen ist — gut, um zu lernen, "
              "wohin man schaut, bevor man einen Fehler sucht, den es nicht gibt.",

    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — die genannten Werte sind die "
             "Voreinstellungen der beiden Programme, Stand 16. August 2026.",
}
