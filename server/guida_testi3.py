#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""I testi della guida: catalano, danese, ungherese, rumeno, lettone."""

G3 = {}

G3["ca"] = {
    "titolo": "Decodium Mobile amb Decolink",
    "sottotitolo": "Com portar l'àudio de la ràdio — i el comandament de l'equip — de "
                   "l'ordinador de l'estació al telèfon: a casa dins la mateixa xarxa, o a tot "
                   "arreu passant pel servidor.",
    "meta_app": "Decodium 4.0 Mobile",
    "meta_proto": "Decolink · protocol HFGW v2",
    "meta_data": "16 d'agost de 2026",

    "h_prima": "Abans de començar",
    "s1_t": "A l'ordinador",
    "s1_p": "<strong>Decolink</strong> engegat al costat de la ràdio, amb el CODEC USB de "
            "l'equip connectat. És ell qui envia l'àudio i, si vols, serveix el CAT.",
    "s2_t": "Al telèfon",
    "s2_p": "<strong>Decodium 4 Mobile</strong>. Tot es configura en un sol lloc: l'engranatge "
            "⚙ de dalt, seccions <em>Estació</em>, <em>Àudio</em> i <em>CAT / Rig</em>.",
    "s3_t": "Només per al relé",
    "s3_p": "Un compte aprovat a <code>decolink.ft2.it</code>. En xarxa local no cal: cap "
            "registre, cap dada fora de casa.",

    "h_tre": "Les tres connexions",
    "tre_p": "El Decolink i el Decodium Mobile han d'estar en el <strong>mateix mode</strong>: "
             "és l'error més comú, i no dona missatges clars.",
    "th_modo": "Mode", "th_quando": "Quan", "th_chi": "Qui truca a qui",
    "th_porta": "Port", "th_aprire": "Per obrir",
    "lan": "LAN", "lan_q": "Telèfon i ordinador a la mateixa WiFi",
    "lan_c": "L'ordinador dispara l'àudio a la IP del telèfon", "lan_a": "Res",
    "relay": "Relé", "relay_q": "Fora de casa, també amb dades mòbils",
    "relay_c": "Tots dos surten cap al servidor", "relay_a": "Res",
    "casa": "Casa", "casa_q": "Fora de casa, sense passar pel servidor",
    "casa_c": "El telèfon truca a la teva adreça de casa", "casa_a": "UDP 5555 a l'encaminador",
    "tre_fine": "El <strong>relé</strong> és el que funciona sempre: cap dels dos no ha de ser "
                "accessible des de fora, perquè són ells els qui es fan veure cap al servidor. "
                "És també l'únic que demana un compte.",

    "h_pa": "Camí A · xarxa local",
    "pa1_sigla": "A l'ordinador · Decolink",
    "pa1_h3": "Envia l'àudio a l'adreça del telèfon",
    "pa1_1": '<span class="dove">Àudio ràdio</span> → tria el CODEC USB del transceptor.',
    "pa1_1n": "És l'entrada per on arriba el senyal rebut, no el micròfon de l'ordinador.",
    "pa1_2": '<span class="dove">Modalitat</span> → <code>LAN directa</code>',
    "pa1_3": '<span class="dove">Amfitrió</span> → l\'adreça IP del telèfon a la WiFi de casa.',
    "pa1_3n": "Al telèfon la trobes a Configuració → WiFi → la xarxa a què estàs connectat. "
              "S'assembla a 192.168.1.42.",
    "pa1_4": '<span class="dove">Port</span> → <code>5555</code>',
    "pa1_5": 'Prem <span class="dove">Inicia</span>. El nivell s\'ha de moure al ritme del '
             'soroll de banda.',
    "pa2_sigla": "Al telèfon · Decodium Mobile",
    "pa2_h3": "Posa't a l'escolta",
    "pa2_1": '⚙ → <span class="dove">Estació</span>: indicatiu, locator, informe.',
    "pa2_1n": "Sense indicatiu i locator els missatges no es poden compondre.",
    "pa2_2": '<span class="dove">Àudio → Connexió</span> → <code>LAN</code>',
    "pa2_3": '<span class="dove">Port</span> → <code>5555</code>, el mateix escrit al Decolink',
    "pa2_4": 'Prem <span class="dove">Rep</span>. Apareix <em>«Escoltant al port 5555»</em>: '
             'des d\'aquell moment el waterfall s\'omple tan bon punt l\'ordinador comença a '
             'enviar.',
    "pa_avv_t": "En LAN el telèfon espera, no truca",
    "pa_avv_p": "És l'ordinador qui ha de saber la IP del telèfon. Si l'encaminador reparteix "
                "les adreces per torns, demà aquella IP serà d'algú altre i l'àudio ja no "
                "arribarà: reserva al telèfon una adreça fixa a l'encaminador, o torna a "
                "comprovar el camp <em>Amfitrió</em> a cada sessió.",

    "h_pb": "Camí B · relé al servidor",
    "pb1_sigla": "Una sola vegada · des del navegador",
    "pb1_h3": "Demana l'accés a l'estació",
    "pb1_1": "Obre <code>https://decolink.ft2.it/registrati</code>",
    "pb1_2": "Omple correu, contrasenya, indicatiu i l'estació a què et vols connectar.",
    "pb1_3": "Espera l'aprovació.",
    "pb1_3n": "La sol·licitud queda pendent fins que el titular de l'estació l'accepta: decideix "
              "ell, no és automàtic. També és ell qui estableix el teu paper.",
    "ruolo_tit": "Titular",
    "ruolo_tit_d": 'escolta i transmet <span class="libero">— l\'estació és seva</span>',
    "ruolo_op": "Operador",
    "ruolo_op_d": 'escolta i transmet <span class="libero">— autoritzat pel titular</span>',
    "ruolo_asc": "Oient",
    "ruolo_asc_d": 'només recepció <span class="libero">— la tecla de transmissió resta '
                   'apagada</span>',
    "pb2_sigla": "A l'ordinador · Decolink",
    "pb2_h3": "Porta l'estació dins del relé",
    "pb2_1": '<span class="dove">Servidor</span> → <code>decolink.ft2.it</code>, després correu '
             'i contrasenya, i prem <span class="dove">Accedeix</span>.',
    "pb2_1n": "Si deixes l'estació engegada sola, marca «recorda la contrasenya»: en reiniciar "
              "torna a arrencar sense ningú al teclat.",
    "pb2_2": '<span class="dove">Modalitat</span> → <code>Relé + estació</code>',
    "pb2_3": '<span class="dove">Amfitrió</span> → <code>decolink.ft2.it</code> · '
             '<span class="dove">Port</span> → <code>5555</code>',
    "pb2_4": '<span class="dove">Perfil</span> → <code>PCM 48 kHz</code>',
    "pb2_4n": "Els perfils comprimits consumeixen una cinquena part de l'amplada de banda, però "
              "deixa'ls per després: primer comprova que l'enllaç aguanta així.",
    "pb2_5": 'Prem <span class="dove">Inicia</span>.',
    "pb3_sigla": "Al telèfon · Decodium Mobile",
    "pb3_h3": "Entra amb les teves credencials",
    "pb3_1": '⚙ → <span class="dove">Àudio → Connexió</span> → <code>Relé</code>',
    "pb3_2": 'Omple els camps de l\'accés i prem <span class="dove">Entra</span>.',
    "pb3_3": "Mira la línia d'estat: ha de dir el teu indicatiu, l'estació i el paper.",
    "pb3_3n": "Si hi llegeixes «Has entrat com a oient», reps però no transmets: és el paper, no "
              "una avaria.",
    "pb3_4": '<span class="dove">Port</span> → <code>5555</code>, després '
             '<span class="dove">Rep</span>.',
    "campi_acc": "Accés",
    "campi_email": "Correu", "campi_email_d": "el que vas fer servir en registrar-te",
    "campi_pw": "Contrasenya", "campi_pw_d": "la del compte de Decolink",
    "campi_relay": "Relé", "campi_relay_d": "deixa-ho buit: agafa l'adreça de l'accés",
    "campi_porta": "Port",
    "pb_avv_t": "El permís dura una hora",
    "pb_avv_p": "El servidor lliura un salconduit que caduca al cap de seixanta minuts. Amb "
                "<em>«Recorda la contrasenya»</em> activat l'aplicació el renova sola un minut "
                "abans; sense, al cap d'una hora l'àudio s'atura sense explicacions i cal tornar "
                "a entrar a mà. Al telèfon la contrasenya viu al clauer xifrat del sistema, "
                "fora de les còpies de seguretat.",

    "h_pc": "Camí C · el telèfon truca a casa",
    "pc_p": "Serveix a qui no vol passar pel servidor i té una adreça accessible des de fora. A "
            "canvi cal ficar les mans a l'encaminador.",
    "pc_1": '<span class="dove">A l\'encaminador</span>: redirigeix el port <code>UDP 5555</code> '
            'cap a l\'adreça de l\'ordinador de l\'estació.',
    "pc_2": '<span class="dove">Al Decolink</span>: modalitat <code>El telèfon truca a casa</code>, '
            'port <code>5555</code>. El camp Amfitrió queda buit: és el telèfon qui es fa veure.',
    "pc_3": '<span class="dove">Al telèfon</span>: connexió <code>Casa</code>, al camp de '
            'l\'adreça el teu nom DynDNS (per exemple <code>iu8lmc.ddns.net</code>), port '
            '<code>5555</code>, després <span class="dove">Rep</span>.',
    "pc_fine": "Amb una connexió de casa darrere de CG-NAT — moltes fibres i gairebé totes les "
               "línies mòbils — aquest mode no pot funcionar: ningú de fora no aconsegueix "
               "arribar-hi. És exactament el cas per al qual existeix el relé.",

    "h_cat": "Comandar la ràdio",
    "cat_p": "L'àudio i el CAT són dues coses separades: pots rebre sense CAT, però sense CAT el "
             "telèfon no sap en quina freqüència ets i no pot canviar de banda ni passar a "
             "transmissió.",
    "cat_th1": "Font", "cat_th2": "Com es connecta", "cat_th3": "On funciona",
    "cat_r1": "TCP al PC",
    "cat_r1d": 'Al Decolink marca <em>«Serveix el CAT al telèfon»</em>; al telèfon posa la IP de '
               'l\'ordinador i el port <span class="num">4532</span>',
    "cat_r1w": "Xarxa local",
    "cat_r2": "USB-OTG",
    "cat_r2d": "Cable del telèfon a la ràdio, sense cap ordinador entremig",
    "cat_r2w": "A tot arreu, amb la ràdio a l'abast del cable",
    "cat_r3": "Canal d'àudio",
    "cat_r3d": "Les ordres viatgen dins de l'enllaç d'àudio ja obert",
    "cat_r3w": "A tot arreu — és la tria bona amb Relé o Casa",
    "cat_fine": "Amb el <em>canal d'àudio</em> no cal obrir res més: perquè funcioni s'han de "
                "donar dues condicions — l'àudio de xarxa ja iniciat, i el CAT engegat al "
                "Decolink.",

    "h_guai": "Quan no arriba res",
    "g1_m": "«Escoltant al port 5555 — el PC ha d'enviar aquí l'àudio»",
    "g1_c": "Ets en mode <strong>LAN</strong> però volies el relé. En LAN el telèfon només "
            "espera: no surt cap registre, i et quedes esperant un àudio que ningú no enviarà. "
            "Canvia la connexió a <em>Relé</em>.",
    "g2_m": "«Nom no resolt»",
    "g2_c": "L'adreça escrita no existeix, o el telèfon no té xarxa. Comprova que no hi hagis "
            "posat <code>https://</code> al camp del relé.",
    "g3_m": "«Port 5555 ocupat»",
    "g3_c": "Una altra aplicació té aquell port. Tanca-la, o fes servir-ne un altre — canviant-lo "
            "als dos programes.",
    "g4_m": "«servidor inaccessible»",
    "g4_c": "És un problema de connexió, no de contrasenya: l'aplicació distingeix els dos casos "
            "expressament. Comprova que tens xarxa i torna-ho a provar.",
    "g5_m": "L'àudio arrenca i s'atura al cap de pocs segons",
    "g5_c": "El relé descarta qui es queda callat quinze segons. Si passa contínuament, la xarxa "
            "està perdent paquets: prova un perfil comprimit, que ocupa una cinquena part de "
            "l'amplada de banda.",
    "g6_m": "El waterfall es mou però no descodifica res",
    "g6_c": "Gairebé sempre és el rellotge: els modes digitals s'aguanten o cauen al segon "
            "exacte. Deixa que el telèfon agafi l'hora de la xarxa.",

    "h_demo": "Provar sense ràdio",
    "demo_p": "El botó <strong>Demo</strong>, al costat de <em>Rep</em>, encén una banda fingida "
              "amb cinc estacions i descodificacions que van passant. Serveix per veure com es "
              "comporta l'aplicació abans de connectar res — útil per aprendre on mirar, abans "
              "d'anar a buscar una avaria que no hi és.",

    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — els valors indicats són els "
             "predeterminats dels dos programes a 16 d'agost de 2026.",
}

G3["da"] = {
    "titolo": "Decodium Mobile over Decolink",
    "sottotitolo": "Sådan får du radioens lyd — og betjeningen af den — fra shackens computer "
                   "over på telefonen: hjemme på samme net, eller hvor som helst via serveren.",
    "meta_app": "Decodium 4.0 Mobile",
    "meta_proto": "Decolink · protokol HFGW v2",
    "meta_data": "16. august 2026",

    "h_prima": "Før du går i gang",
    "s1_t": "På computeren",
    "s1_p": "<strong>Decolink</strong> kørende ved siden af radioen, med radioens USB-CODEC "
            "tilsluttet. Det er den, der sender lyden og om nødvendigt leverer CAT.",
    "s2_t": "På telefonen",
    "s2_p": "<strong>Decodium 4 Mobile</strong>. Alt sættes op ét sted: tandhjulet ⚙ øverst, "
            "afsnittene <em>Station</em>, <em>Lyd</em> og <em>CAT / Rig</em>.",
    "s3_t": "Kun til relæet",
    "s3_p": "En godkendt adgang på <code>decolink.ft2.it</code>. På lokalnettet er den ikke "
            "nødvendig: ingen registrering, intet forlader huset.",

    "h_tre": "De tre forbindelser",
    "tre_p": "Decolink og Decodium Mobile skal stå på <strong>samme tilstand</strong>: det er "
             "den hyppigste fejl, og den giver ingen tydelig besked.",
    "th_modo": "Tilstand", "th_quando": "Hvornår", "th_chi": "Hvem ringer til hvem",
    "th_porta": "Port", "th_aprire": "Skal åbnes",
    "lan": "LAN", "lan_q": "Telefon og computer på samme WiFi",
    "lan_c": "Computeren skyder lyden mod telefonens IP", "lan_a": "Intet",
    "relay": "Relæ", "relay_q": "Ude af huset, også på mobildata",
    "relay_c": "Begge går ud mod serveren", "relay_a": "Intet",
    "casa": "Hjem", "casa_q": "Ude af huset, uden om serveren",
    "casa_c": "Telefonen ringer til din hjemmeadresse", "casa_a": "UDP 5555 på routeren",
    "tre_fine": "<strong>Relæet</strong> er det, der altid virker: ingen af de to behøver at "
                "kunne nås udefra, for de melder sig begge selv hos serveren. Det er også det "
                "eneste, der kræver en adgang.",

    "h_pa": "Vej A · lokalnet",
    "pa1_sigla": "På computeren · Decolink",
    "pa1_h3": "Send lyden til telefonens adresse",
    "pa1_1": '<span class="dove">Radiolyd</span> → vælg transceiverens USB-CODEC.',
    "pa1_1n": "Det er indgangen, hvor det modtagne signal kommer ind, ikke computerens mikrofon.",
    "pa1_2": '<span class="dove">Tilstand</span> → <code>Direkte LAN</code>',
    "pa1_3": '<span class="dove">Vært</span> → telefonens IP-adresse på hjemmets WiFi.',
    "pa1_3n": "På telefonen finder du den under Indstillinger → WiFi → det net, du er forbundet "
              "til. Den ligner 192.168.1.42.",
    "pa1_4": '<span class="dove">Port</span> → <code>5555</code>',
    "pa1_5": 'Tryk <span class="dove">Start</span>. Niveauet skal bevæge sig i takt med '
             'båndstøjen.',
    "pa2_sigla": "På telefonen · Decodium Mobile",
    "pa2_h3": "Gå på lytning",
    "pa2_1": '⚙ → <span class="dove">Station</span>: kaldesignal, locator, rapport.',
    "pa2_1n": "Uden kaldesignal og locator kan meddelelserne ikke sættes sammen.",
    "pa2_2": '<span class="dove">Lyd → Forbindelse</span> → <code>LAN</code>',
    "pa2_3": '<span class="dove">Port</span> → <code>5555</code>, den samme som i Decolink',
    "pa2_4": 'Tryk <span class="dove">Modtag</span>. Der står <em>»Lytter på port 5555«</em>: '
             'fra da af fyldes vandfaldet, så snart computeren begynder at sende.',
    "pa_avv_t": "På LAN venter telefonen, den ringer ikke",
    "pa_avv_p": "Det er computeren, der skal kende telefonens IP. Deler routeren adresserne ud "
                "på skift, tilhører den IP i morgen en anden, og lyden kommer ikke frem: "
                "reservér telefonen en fast adresse i routeren, eller tjek feltet <em>Vært</em> "
                "hver gang.",

    "h_pb": "Vej B · relæ på serveren",
    "pb1_sigla": "Én gang · fra browseren",
    "pb1_h3": "Bed om adgang til stationen",
    "pb1_1": "Åbn <code>https://decolink.ft2.it/registrati</code>",
    "pb1_2": "Udfyld e-mail, adgangskode, kaldesignal og den station, du vil forbinde til.",
    "pb1_3": "Vent på godkendelsen.",
    "pb1_3n": "Anmodningen står åben, indtil stationens indehaver accepterer den: han bestemmer, "
              "det sker ikke automatisk. Han fastsætter også din rolle.",
    "ruolo_tit": "Indehaver",
    "ruolo_tit_d": 'lytter og sender <span class="libero">— det er hans station</span>',
    "ruolo_op": "Operatør",
    "ruolo_op_d": 'lytter og sender <span class="libero">— godkendt af indehaveren</span>',
    "ruolo_asc": "Lytter",
    "ruolo_asc_d": 'kun modtagelse <span class="libero">— sendetasten forbliver slukket</span>',
    "pb2_sigla": "På computeren · Decolink",
    "pb2_h3": "Før stationen ind i relæet",
    "pb2_1": '<span class="dove">Server</span> → <code>decolink.ft2.it</code>, derefter e-mail '
             'og adgangskode, og tryk <span class="dove">Log ind</span>.',
    "pb2_1n": "Lader du stationen køre alene, så sæt flueben i »husk adgangskoden«: efter en "
              "genstart kommer den op igen uden nogen ved tastaturet.",
    "pb2_2": '<span class="dove">Tilstand</span> → <code>Relæ + station</code>',
    "pb2_3": '<span class="dove">Vært</span> → <code>decolink.ft2.it</code> · '
             '<span class="dove">Port</span> → <code>5555</code>',
    "pb2_4": '<span class="dove">Profil</span> → <code>PCM 48 kHz</code>',
    "pb2_4n": "De komprimerede profiler bruger en femtedel af båndbredden, men gem dem til "
              "senere: se først, om forbindelsen holder sådan.",
    "pb2_5": 'Tryk <span class="dove">Start</span>.',
    "pb3_sigla": "På telefonen · Decodium Mobile",
    "pb3_h3": "Log ind med dine oplysninger",
    "pb3_1": '⚙ → <span class="dove">Lyd → Forbindelse</span> → <code>Relæ</code>',
    "pb3_2": 'Udfyld loginfelterne og tryk <span class="dove">Log ind</span>.',
    "pb3_3": "Se på statuslinjen: der skal stå dit kaldesignal, stationen og rollen.",
    "pb3_3n": "Står der »Du er inde som lytter«, modtager du, men sender ikke: det er rollen, "
              "ikke en fejl.",
    "pb3_4": '<span class="dove">Port</span> → <code>5555</code>, derefter '
             '<span class="dove">Modtag</span>.',
    "campi_acc": "Login",
    "campi_email": "E-mail", "campi_email_d": "den, du registrerede dig med",
    "campi_pw": "Adgangskode", "campi_pw_d": "den til din Decolink-adgang",
    "campi_relay": "Relæ", "campi_relay_d": "lad stå tom: den tager loginadressen",
    "campi_porta": "Port",
    "pb_avv_t": "Tilladelsen varer en time",
    "pb_avv_p": "Serveren udsteder et adgangsbevis, der udløber efter tres minutter. Med "
                "<em>»Husk adgangskoden«</em> slået til forny­er appen det selv et minut før; "
                "uden stopper lyden efter en time uden forklaring, og du skal logge ind i hånden "
                "igen. På telefonen ligger adgangskoden i systemets krypterede nøglering, uden "
                "for sikkerhedskopierne.",

    "h_pc": "Vej C · telefonen ringer hjem",
    "pc_p": "Til dem, der helst vil uden om serveren og har en adresse, der kan nås udefra. Til "
            "gengæld skal man have fingrene ned i routeren.",
    "pc_1": '<span class="dove">På routeren</span>: videresend porten <code>UDP 5555</code> til '
            'shackcomputerens adresse.',
    "pc_2": '<span class="dove">I Decolink</span>: tilstand <code>Telefonen ringer hjem</code>, '
            'port <code>5555</code>. Feltet Vært står tomt: det er telefonen, der melder sig.',
    "pc_3": '<span class="dove">På telefonen</span>: forbindelse <code>Hjem</code>, i adressefeltet '
            'dit DynDNS-navn (for eksempel <code>iu8lmc.ddns.net</code>), port <code>5555</code>, '
            'derefter <span class="dove">Modtag</span>.',
    "pc_fine": "Med en hjemmeforbindelse bag CG-NAT — mange fiberlinjer og næsten alle mobile — "
               "kan denne tilstand ikke virke: ingen udefra når frem til dig. Det er præcis den "
               "situation, relæet findes til.",

    "h_cat": "At styre radioen",
    "cat_p": "Lyd og CAT er to forskellige ting: du kan modtage uden CAT, men uden CAT ved "
             "telefonen ikke, hvilken frekvens du er på, og kan hverken skifte bånd eller sende.",
    "cat_th1": "Kilde", "cat_th2": "Sådan forbinder den", "cat_th3": "Hvor det virker",
    "cat_r1": "TCP til pc'en",
    "cat_r1d": 'Sæt flueben i <em>»Lever CAT til telefonen«</em> i Decolink; på telefonen '
               'indtast computerens IP og port <span class="num">4532</span>',
    "cat_r1w": "Lokalnet",
    "cat_r2": "USB-OTG",
    "cat_r2d": "Kabel fra telefon til radio, ingen computer imellem",
    "cat_r2w": "Overalt, med radioen inden for kabellængde",
    "cat_r3": "Lydkanal",
    "cat_r3d": "Kommandoerne løber med i den lydforbindelse, der allerede er åben",
    "cat_r3w": "Overalt — det rigtige valg med Relæ eller Hjem",
    "cat_fine": "Med <em>lydkanalen</em> er der ikke mere at åbne: to ting skal passe — "
                "netlyden er allerede startet, og CAT er tændt i Decolink.",

    "h_guai": "Når der ikke kommer noget",
    "g1_m": "»Lytter på port 5555 — pc'en skal sende lyden hertil«",
    "g1_c": "Du står i <strong>LAN</strong>-tilstand, men ville have relæet. På LAN venter "
            "telefonen bare: der går ingen registrering ud, og du sidder og venter på lyd, som "
            "ingen sender. Skift forbindelsen til <em>Relæ</em>.",
    "g2_m": "»Navnet kunne ikke slås op«",
    "g2_c": "Adressen i feltet findes ikke, eller telefonen er uden net. Tjek, at du ikke har "
            "skrevet <code>https://</code> i relæfeltet.",
    "g3_m": "»Port 5555 optaget«",
    "g3_c": "En anden app holder den port. Luk den, eller brug en anden — og skift den i begge "
            "programmer.",
    "g4_m": "»serveren kan ikke nås«",
    "g4_c": "Det er et forbindelsesproblem, ikke et adgangskodeproblem: appen skelner med vilje "
            "mellem de to. Tjek, at du har net, og prøv igen.",
    "g5_m": "Lyden går i gang og stopper efter få sekunder",
    "g5_c": "Relæet smider den ud, der er tavs i femten sekunder. Sker det hele tiden, taber "
            "nettet pakker: prøv en komprimeret profil, der fylder en femtedel af båndbredden.",
    "g6_m": "Vandfaldet bevæger sig, men intet dekodes",
    "g6_c": "Næsten altid er det uret: de digitale tilstande står og falder med det præcise "
            "sekund. Lad telefonen hente tiden fra nettet.",

    "h_demo": "Prøve uden radio",
    "demo_p": "Knappen <strong>Demo</strong> ved siden af <em>Modtag</em> tænder et opdigtet "
              "bånd med fem stationer og dekodninger, der ruller forbi. Den viser, hvordan "
              "appen opfører sig, før noget som helst er tilsluttet — god til at lære, hvor man "
              "skal kigge, før man går ud og leder efter en fejl, der ikke er der.",

    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — de nævnte værdier er de to programmers "
             "standardindstillinger pr. 16. august 2026.",
}

G3["hu"] = {
    "titolo": "Decodium Mobile a Decolinken át",
    "sottotitolo": "Hogyan jut a rádió hangja — és a rádió vezérlése — az állomás gépéről a "
                   "telefonra: otthon ugyanazon a hálózaton, vagy bárhonnan a kiszolgálón "
                   "keresztül.",
    "meta_app": "Decodium 4.0 Mobile",
    "meta_proto": "Decolink · HFGW v2 protokoll",
    "meta_data": "2026. augusztus 16.",

    "h_prima": "Mielőtt nekikezdesz",
    "s1_t": "A számítógépen",
    "s1_p": "<strong>Decolink</strong> fut a rádió mellett, a rádió USB-CODEC-je csatlakoztatva. "
            "Ő küldi a hangot, és ha kéred, ő szolgálja ki a CAT-et.",
    "s2_t": "A telefonon",
    "s2_p": "<strong>Decodium 4 Mobile</strong>. Minden egy helyen állítható: a ⚙ fogaskerék "
            "fent, az <em>Állomás</em>, <em>Hang</em> és <em>CAT / Rig</em> szakaszok.",
    "s3_t": "Csak a reléhez",
    "s3_p": "Egy jóváhagyott hozzáférés a <code>decolink.ft2.it</code> címen. Helyi hálózaton "
            "nem kell: nincs regisztráció, semmi nem hagyja el a házat.",

    "h_tre": "A három kapcsolat",
    "tre_p": "A Decolinknek és a Decodium Mobile-nak <strong>ugyanabban a módban</strong> kell "
             "lennie: ez a leggyakoribb hiba, és nem ad világos üzenetet.",
    "th_modo": "Mód", "th_quando": "Mikor", "th_chi": "Ki hívja kit",
    "th_porta": "Port", "th_aprire": "Kinyitandó",
    "lan": "LAN", "lan_q": "Telefon és gép ugyanazon a WiFin",
    "lan_c": "A gép a telefon IP-címére lövi a hangot", "lan_a": "Semmi",
    "relay": "Relé", "relay_q": "Házon kívül, mobilneten is",
    "relay_c": "Mindkettő a kiszolgáló felé indul", "relay_a": "Semmi",
    "casa": "Otthon", "casa_q": "Házon kívül, a kiszolgáló nélkül",
    "casa_c": "A telefon hívja az otthoni címedet", "casa_a": "UDP 5555 a routeren",
    "tre_fine": "A <strong>relé</strong> az, ami mindig működik: egyiknek sem kell kívülről "
                "elérhetőnek lennie, mert mindketten maguk keresik a kiszolgálót. Ez az egyetlen "
                "is, amelyhez hozzáférés kell.",

    "h_pa": "A útvonal · helyi hálózat",
    "pa1_sigla": "A számítógépen · Decolink",
    "pa1_h3": "Küldd a hangot a telefon címére",
    "pa1_1": '<span class="dove">Rádió hangja</span> → válaszd a transceiver USB-CODEC-jét.',
    "pa1_1n": "Ez az a bemenet, ahol a vett jel érkezik, nem a gép mikrofonja.",
    "pa1_2": '<span class="dove">Mód</span> → <code>Közvetlen LAN</code>',
    "pa1_3": '<span class="dove">Kiszolgáló</span> → a telefon IP-címe az otthoni WiFin.',
    "pa1_3n": "A telefonon a Beállítások → WiFi → a hálózat, amelyhez csatlakozol menüpont alatt "
              "látod. Ilyesmi: 192.168.1.42.",
    "pa1_4": '<span class="dove">Port</span> → <code>5555</code>',
    "pa1_5": 'Nyomd meg az <span class="dove">Indítás</span> gombot. A szintnek együtt kell '
             'mozognia a sávzajjal.',
    "pa2_sigla": "A telefonon · Decodium Mobile",
    "pa2_h3": "Állj vételre",
    "pa2_1": '⚙ → <span class="dove">Állomás</span>: hívójel, lokátor, riport.',
    "pa2_1n": "Hívójel és lokátor nélkül az üzenetek nem állíthatók össze.",
    "pa2_2": '<span class="dove">Hang → Kapcsolat</span> → <code>LAN</code>',
    "pa2_3": '<span class="dove">Port</span> → <code>5555</code>, ugyanaz, mint a Decolinkben',
    "pa2_4": 'Nyomd meg a <span class="dove">Vétel</span> gombot. Megjelenik: <em>„Figyelés az '
             '5555-ös porton”</em> — onnantól a vízesés megtelik, amint a gép küldeni kezd.',
    "pa_avv_t": "LAN-on a telefon vár, nem hív",
    "pa_avv_p": "A gépnek kell ismernie a telefon IP-címét. Ha a router sorban osztja a címeket, "
                "holnap az az IP már másé lesz, és a hang nem érkezik meg: foglalj a telefonnak "
                "állandó címet a routerben, vagy ellenőrizd a <em>Kiszolgáló</em> mezőt minden "
                "alkalommal.",

    "h_pb": "B útvonal · relé a kiszolgálón",
    "pb1_sigla": "Egyszer · a böngészőből",
    "pb1_h3": "Kérj hozzáférést az állomáshoz",
    "pb1_1": "Nyisd meg: <code>https://decolink.ft2.it/registrati</code>",
    "pb1_2": "Töltsd ki az e-mail-címet, a jelszót, a hívójelet és az állomást, amelyhez "
             "csatlakozni szeretnél.",
    "pb1_3": "Várd meg a jóváhagyást.",
    "pb1_3n": "A kérés addig függőben marad, míg az állomás tulajdonosa el nem fogadja: ő dönt, "
              "nem automatikus. A szerepedet is ő szabja meg.",
    "ruolo_tit": "Tulajdonos",
    "ruolo_tit_d": 'hallgat és ad <span class="libero">— az ő állomása</span>',
    "ruolo_op": "Kezelő",
    "ruolo_op_d": 'hallgat és ad <span class="libero">— a tulajdonos engedélyével</span>',
    "ruolo_asc": "Hallgató",
    "ruolo_asc_d": 'csak vétel <span class="libero">— az adásgomb sötét marad</span>',
    "pb2_sigla": "A számítógépen · Decolink",
    "pb2_h3": "Vidd be az állomást a relébe",
    "pb2_1": '<span class="dove">Kiszolgáló</span> → <code>decolink.ft2.it</code>, majd e-mail '
             'és jelszó, és nyomd meg a <span class="dove">Belépés</span> gombot.',
    "pb2_1n": "Ha az állomást magára hagyod bekapcsolva, jelöld be a „jelszó megjegyzése” "
              "lehetőséget: újraindítás után magától elindul, senki nem ül a billentyűzetnél.",
    "pb2_2": '<span class="dove">Mód</span> → <code>Relé + állomás</code>',
    "pb2_3": '<span class="dove">Kiszolgáló</span> → <code>decolink.ft2.it</code> · '
             '<span class="dove">Port</span> → <code>5555</code>',
    "pb2_4": '<span class="dove">Profil</span> → <code>PCM 48 kHz</code>',
    "pb2_4n": "A tömörített profilok a sávszélesség ötödét fogyasztják, de tartogasd őket "
              "későbbre: előbb győződj meg róla, hogy a kapcsolat így elbírja.",
    "pb2_5": 'Nyomd meg az <span class="dove">Indítás</span> gombot.',
    "pb3_sigla": "A telefonon · Decodium Mobile",
    "pb3_h3": "Lépj be a hitelesítő adataiddal",
    "pb3_1": '⚙ → <span class="dove">Hang → Kapcsolat</span> → <code>Relé</code>',
    "pb3_2": 'Töltsd ki a belépési mezőket, és nyomd meg a <span class="dove">Belépés</span> '
             'gombot.',
    "pb3_3": "Nézd meg az állapotsort: a hívójeledet, az állomást és a szerepet kell mutatnia.",
    "pb3_3n": "Ha azt olvasod, hogy „Hallgatóként léptél be”, akkor veszel, de nem adsz: ez a "
              "szerep, nem hiba.",
    "pb3_4": '<span class="dove">Port</span> → <code>5555</code>, majd '
             '<span class="dove">Vétel</span>.',
    "campi_acc": "Belépés",
    "campi_email": "E-mail", "campi_email_d": "amivel regisztráltál",
    "campi_pw": "Jelszó", "campi_pw_d": "a Decolink-fiókodé",
    "campi_relay": "Relé", "campi_relay_d": "hagyd üresen: a belépés címét veszi át",
    "campi_porta": "Port",
    "pb_avv_t": "Az engedély egy óráig él",
    "pb_avv_p": "A kiszolgáló olyan belépőt ad, amely hatvan perc múlva lejár. Ha a "
                "<em>„Jelszó megjegyzése”</em> be van kapcsolva, az alkalmazás egy perccel "
                "előbb magától megújítja; enélkül egy óra múlva a hang magyarázat nélkül "
                "elhallgat, és kézzel kell újra belépni. A telefonon a jelszó a rendszer "
                "titkosított kulcstartójában van, a biztonsági mentéseken kívül.",

    "h_pc": "C útvonal · a telefon hívja az otthont",
    "pc_p": "Annak való, aki nem akar a kiszolgálón át menni, és van kívülről elérhető címe. "
            "Cserébe bele kell nyúlni a routerbe.",
    "pc_1": '<span class="dove">A routeren</span>: irányítsd át az <code>UDP 5555</code> portot '
            'az állomás gépének címére.',
    "pc_2": '<span class="dove">A Decolinkben</span>: mód <code>A telefon hívja az otthont</code>, '
            'port <code>5555</code>. A Kiszolgáló mező üresen marad: a telefon jelentkezik be.',
    "pc_3": '<span class="dove">A telefonon</span>: kapcsolat <code>Otthon</code>, a cím mezőbe '
            'a DynDNS-neved (például <code>iu8lmc.ddns.net</code>), port <code>5555</code>, '
            'majd <span class="dove">Vétel</span>.',
    "pc_fine": "CG-NAT mögötti otthoni kapcsolattal — sok optikai és szinte minden mobilvonal "
               "ilyen — ez a mód nem működhet: kívülről senki nem ér el. Pontosan erre az esetre "
               "van a relé.",

    "h_cat": "A rádió vezérlése",
    "cat_p": "A hang és a CAT két külön dolog: CAT nélkül is lehet venni, de CAT nélkül a "
             "telefon nem tudja, milyen frekvencián vagy, és nem tud sem sávot váltani, sem "
             "adásba kapcsolni.",
    "cat_th1": "Forrás", "cat_th2": "Hogyan csatlakozik", "cat_th3": "Hol működik",
    "cat_r1": "TCP a géphez",
    "cat_r1d": 'A Decolinkben jelöld be: <em>„CAT kiszolgálása a telefonnak”</em>; a telefonon '
               'add meg a gép IP-címét és a <span class="num">4532</span> portot',
    "cat_r1w": "Helyi hálózat",
    "cat_r2": "USB-OTG",
    "cat_r2d": "Kábel a telefontól a rádióig, gép nélkül",
    "cat_r2w": "Bárhol, ahol a rádió kábelnyi távolságban van",
    "cat_r3": "Hangcsatorna",
    "cat_r3d": "A parancsok a már megnyitott hangkapcsolatban utaznak",
    "cat_r3w": "Bárhol — Relé vagy Otthon mellett ez a helyes választás",
    "cat_fine": "A <em>hangcsatornánál</em> nincs mit külön megnyitni: két dolognak kell "
                "teljesülnie — a hálózati hang már fut, és a CAT be van kapcsolva a Decolinkben.",

    "h_guai": "Amikor semmi nem érkezik",
    "g1_m": "„Figyelés az 5555-ös porton — a gépnek ide kell küldenie a hangot”",
    "g1_c": "<strong>LAN</strong> módban vagy, pedig a relét akartad. LAN-on a telefon csak vár: "
            "semmilyen regisztráció nem indul, és olyan hangra vársz, amit senki nem küld. Állítsd "
            "a kapcsolatot <em>Relé</em> értékre.",
    "g2_m": "„A név nem oldható fel”",
    "g2_c": "A beírt cím nem létezik, vagy a telefonnak nincs hálózata. Ellenőrizd, hogy nem "
            "került-e <code>https://</code> a relé mezőbe.",
    "g3_m": "„Az 5555-ös port foglalt”",
    "g3_c": "Egy másik alkalmazás tartja azt a portot. Zárd be, vagy válassz másikat — mindkét "
            "programban megváltoztatva.",
    "g4_m": "„a kiszolgáló nem érhető el”",
    "g4_c": "Ez kapcsolati gond, nem jelszóprobléma: az alkalmazás szándékosan különbözteti meg "
            "a kettőt. Nézd meg, van-e hálózatod, és próbáld újra.",
    "g5_m": "A hang elindul, majd pár másodperc múlva megáll",
    "g5_c": "A relé kidobja azt, aki tizenöt másodpercig néma marad. Ha folyton előfordul, a "
            "hálózat csomagokat veszít: próbálj tömörített profilt, az a sávszélesség ötödét "
            "foglalja.",
    "g6_m": "A vízesés mozog, de semmi nem dekódolódik",
    "g6_c": "Majdnem mindig az óra: a digitális módok a pontos másodpercen állnak vagy buknak. "
            "Hagyd, hogy a telefon a hálózatról vegye az időt.",

    "h_demo": "Kipróbálás rádió nélkül",
    "demo_p": "A <strong>Demó</strong> gomb a <em>Vétel</em> mellett kitalált sávot kapcsol be "
              "öt állomással és futó dekódolásokkal. Azt mutatja meg, hogyan viselkedik az "
              "alkalmazás, mielőtt bármit is csatlakoztatnál — jó arra, hogy megtanuld, hová "
              "kell nézni, mielőtt olyan hibát keresel, ami nincs is.",

    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — a megadott értékek a két program "
             "alapbeállításai 2026. augusztus 16-án.",
}

G3["ro"] = {
    "titolo": "Decodium Mobile prin Decolink",
    "sottotitolo": "Cum duci sunetul stației — și comanda ei — de la calculatorul din shack pe "
                   "telefon: acasă, în aceeași rețea, sau de oriunde, trecând prin server.",
    "meta_app": "Decodium 4.0 Mobile",
    "meta_proto": "Decolink · protocol HFGW v2",
    "meta_data": "16 august 2026",

    "h_prima": "Înainte de a începe",
    "s1_t": "Pe calculator",
    "s1_p": "<strong>Decolink</strong> pornit lângă stație, cu CODEC-ul USB al acesteia "
            "conectat. El trimite sunetul și, dacă vrei, servește CAT-ul.",
    "s2_t": "Pe telefon",
    "s2_p": "<strong>Decodium 4 Mobile</strong>. Totul se configurează într-un singur loc: "
            "rotița ⚙ de sus, secțiunile <em>Stație</em>, <em>Audio</em> și <em>CAT / Rig</em>.",
    "s3_t": "Doar pentru releu",
    "s3_p": "Un cont aprobat pe <code>decolink.ft2.it</code>. În rețea locală nu e nevoie: fără "
            "înregistrare, nimic nu iese din casă.",

    "h_tre": "Cele trei legături",
    "tre_p": "Decolink și Decodium Mobile trebuie să fie pe <strong>același mod</strong>: e "
             "greșeala cea mai frecventă, și nu dă mesaje clare.",
    "th_modo": "Mod", "th_quando": "Când", "th_chi": "Cine pe cine sună",
    "th_porta": "Port", "th_aprire": "De deschis",
    "lan": "LAN", "lan_q": "Telefon și calculator pe același WiFi",
    "lan_c": "Calculatorul trimite sunetul spre IP-ul telefonului", "lan_a": "Nimic",
    "relay": "Releu", "relay_q": "În afara casei, inclusiv pe date mobile",
    "relay_c": "Amândouă ies spre server", "relay_a": "Nimic",
    "casa": "Acasă", "casa_q": "În afara casei, fără server",
    "casa_c": "Telefonul sună adresa ta de acasă", "casa_a": "UDP 5555 pe router",
    "tre_fine": "<strong>Releul</strong> este cel care merge întotdeauna: niciunul dintre cei "
                "doi nu trebuie să fie accesibil din exterior, pentru că amândoi ies singuri "
                "spre server. Este și singurul care cere un cont.",

    "h_pa": "Traseul A · rețea locală",
    "pa1_sigla": "Pe calculator · Decolink",
    "pa1_h3": "Trimite sunetul la adresa telefonului",
    "pa1_1": '<span class="dove">Audio radio</span> → alege CODEC-ul USB al transceiverului.',
    "pa1_1n": "Este intrarea pe care sosește semnalul recepționat, nu microfonul calculatorului.",
    "pa1_2": '<span class="dove">Mod</span> → <code>LAN direct</code>',
    "pa1_3": '<span class="dove">Gazdă</span> → adresa IP a telefonului pe WiFi-ul de acasă.',
    "pa1_3n": "Pe telefon o găsești în Setări → WiFi → rețeaua la care ești conectat. Arată cam "
              "așa: 192.168.1.42.",
    "pa1_4": '<span class="dove">Port</span> → <code>5555</code>',
    "pa1_5": 'Apasă <span class="dove">Pornește</span>. Nivelul trebuie să se miște în ritmul '
             'zgomotului de bandă.',
    "pa2_sigla": "Pe telefon · Decodium Mobile",
    "pa2_h3": "Pune-te pe recepție",
    "pa2_1": '⚙ → <span class="dove">Stație</span>: indicativ, locator, raport.',
    "pa2_1n": "Fără indicativ și locator mesajele nu se pot compune.",
    "pa2_2": '<span class="dove">Audio → Conexiune</span> → <code>LAN</code>',
    "pa2_3": '<span class="dove">Port</span> → <code>5555</code>, același scris în Decolink',
    "pa2_4": 'Apasă <span class="dove">Recepție</span>. Apare <em>„Ascult pe portul 5555”</em>: '
             'de atunci cascada se umple de îndată ce calculatorul începe să trimită.',
    "pa_avv_t": "În LAN telefonul așteaptă, nu sună",
    "pa_avv_p": "Calculatorul este cel care trebuie să știe IP-ul telefonului. Dacă routerul dă "
                "adresele pe rând, mâine acel IP va fi al altcuiva și sunetul nu mai ajunge: "
                "rezervă telefonului o adresă fixă în router, sau verifică din nou câmpul "
                "<em>Gazdă</em> la fiecare sesiune.",

    "h_pb": "Traseul B · releu pe server",
    "pb1_sigla": "O singură dată · din browser",
    "pb1_h3": "Cere accesul la stație",
    "pb1_1": "Deschide <code>https://decolink.ft2.it/registrati</code>",
    "pb1_2": "Completează email, parolă, indicativ și stația la care vrei să te conectezi.",
    "pb1_3": "Așteaptă aprobarea.",
    "pb1_3n": "Cererea rămâne în așteptare până când titularul stației o acceptă: el decide, nu "
              "e automat. Tot el îți stabilește și rolul.",
    "ruolo_tit": "Titular",
    "ruolo_tit_d": 'ascultă și transmite <span class="libero">— e stația lui</span>',
    "ruolo_op": "Operator",
    "ruolo_op_d": 'ascultă și transmite <span class="libero">— autorizat de titular</span>',
    "ruolo_asc": "Ascultător",
    "ruolo_asc_d": 'doar recepție <span class="libero">— tasta de emisie rămâne stinsă</span>',
    "pb2_sigla": "Pe calculator · Decolink",
    "pb2_h3": "Adu stația în releu",
    "pb2_1": '<span class="dove">Server</span> → <code>decolink.ft2.it</code>, apoi email și '
             'parolă, și apasă <span class="dove">Autentificare</span>.',
    "pb2_1n": "Dacă lași stația pornită singură, bifează „ține minte parola”: la repornire "
              "pleacă din nou fără nimeni la tastatură.",
    "pb2_2": '<span class="dove">Mod</span> → <code>Releu + stație</code>',
    "pb2_3": '<span class="dove">Gazdă</span> → <code>decolink.ft2.it</code> · '
             '<span class="dove">Port</span> → <code>5555</code>',
    "pb2_4": '<span class="dove">Profil</span> → <code>PCM 48 kHz</code>',
    "pb2_4n": "Profilurile comprimate consumă o cincime din bandă, dar păstrează-le pentru mai "
              "târziu: întâi verifică dacă legătura ține așa.",
    "pb2_5": 'Apasă <span class="dove">Pornește</span>.',
    "pb3_sigla": "Pe telefon · Decodium Mobile",
    "pb3_h3": "Intră cu datele tale",
    "pb3_1": '⚙ → <span class="dove">Audio → Conexiune</span> → <code>Releu</code>',
    "pb3_2": 'Completează câmpurile de autentificare și apasă <span class="dove">Intră</span>.',
    "pb3_3": "Uită-te la linia de stare: trebuie să spună indicativul tău, stația și rolul.",
    "pb3_3n": "Dacă scrie „Ai intrat ca ascultător”, recepționezi dar nu transmiți: e rolul, nu "
              "o defecțiune.",
    "pb3_4": '<span class="dove">Port</span> → <code>5555</code>, apoi '
             '<span class="dove">Recepție</span>.',
    "campi_acc": "Autentificare",
    "campi_email": "Email", "campi_email_d": "cel cu care te-ai înregistrat",
    "campi_pw": "Parolă", "campi_pw_d": "cea a contului Decolink",
    "campi_relay": "Releu", "campi_relay_d": "lasă gol: ia adresa autentificării",
    "campi_porta": "Port",
    "pb_avv_t": "Permisul ține o oră",
    "pb_avv_p": "Serverul eliberează un permis care expiră după șaizeci de minute. Cu "
                "<em>„Ține minte parola”</em> activ aplicația îl reînnoiește singură cu un minut "
                "înainte; fără el, după o oră sunetul se oprește fără explicații și trebuie să "
                "reintri manual. Pe telefon parola stă în inelul de chei criptat al sistemului, "
                "în afara copiilor de rezervă.",

    "h_pc": "Traseul C · telefonul sună acasă",
    "pc_p": "E pentru cine nu vrea să treacă prin server și are o adresă accesibilă din afară. "
            "În schimb trebuie să umbli în router.",
    "pc_1": '<span class="dove">Pe router</span>: redirecționează portul <code>UDP 5555</code> '
            'către adresa calculatorului din shack.',
    "pc_2": '<span class="dove">În Decolink</span>: mod <code>Telefonul sună acasă</code>, port '
            '<code>5555</code>. Câmpul Gazdă rămâne gol: telefonul e cel care se anunță.',
    "pc_3": '<span class="dove">Pe telefon</span>: conexiune <code>Acasă</code>, în câmpul de '
            'adresă numele tău DynDNS (de exemplu <code>iu8lmc.ddns.net</code>), port '
            '<code>5555</code>, apoi <span class="dove">Recepție</span>.',
    "pc_fine": "Cu o conexiune de acasă în spatele unui CG-NAT — multe fibre și aproape toate "
               "liniile mobile — acest mod nu poate funcționa: nimeni din afară nu ajunge la "
               "tine. Exact pentru asta există releul.",

    "h_cat": "Comanda stației",
    "cat_p": "Sunetul și CAT-ul sunt două lucruri separate: poți recepționa fără CAT, dar fără "
             "CAT telefonul nu știe pe ce frecvență ești și nu poate nici schimba banda, nici "
             "trece pe emisie.",
    "cat_th1": "Sursă", "cat_th2": "Cum se conectează", "cat_th3": "Unde merge",
    "cat_r1": "TCP spre PC",
    "cat_r1d": 'În Decolink bifează <em>„Servește CAT-ul telefonului”</em>; pe telefon pune '
               'IP-ul calculatorului și portul <span class="num">4532</span>',
    "cat_r1w": "Rețea locală",
    "cat_r2": "USB-OTG",
    "cat_r2d": "Cablu de la telefon la stație, fără calculator la mijloc",
    "cat_r2w": "Oriunde, cu stația la distanță de cablu",
    "cat_r3": "Canal audio",
    "cat_r3d": "Comenzile călătoresc în legătura audio deja deschisă",
    "cat_r3w": "Oriunde — e alegerea potrivită cu Releu sau Acasă",
    "cat_fine": "Cu <em>canalul audio</em> nu e nimic în plus de deschis: ca să meargă trebuie "
                "să fie adevărate două lucruri — sunetul de rețea deja pornit, și CAT-ul aprins "
                "în Decolink.",

    "h_guai": "Când nu ajunge nimic",
    "g1_m": "„Ascult pe portul 5555 — PC-ul trebuie să trimită sunetul aici”",
    "g1_c": "Ești în modul <strong>LAN</strong>, dar voiai releul. În LAN telefonul doar "
            "așteaptă: nu pleacă nicio înregistrare, și aștepți un sunet pe care nu îl va trimite "
            "nimeni. Schimbă legătura pe <em>Releu</em>.",
    "g2_m": "„Nume nerezolvat”",
    "g2_c": "Adresa scrisă nu există, sau telefonul e fără rețea. Verifică să nu fi pus "
            "<code>https://</code> în câmpul releului.",
    "g3_m": "„Portul 5555 e ocupat”",
    "g3_c": "O altă aplicație ține acel port. Închide-o, sau folosește altul — schimbându-l în "
            "amândouă programele.",
    "g4_m": "„serverul nu răspunde”",
    "g4_c": "E o problemă de legătură, nu de parolă: aplicația le deosebește dinadins. Verifică "
            "dacă ai rețea și încearcă din nou.",
    "g5_m": "Sunetul pornește și se oprește după câteva secunde",
    "g5_c": "Releul îl scoate afară pe cine tace cincisprezece secunde. Dacă se întâmplă mereu, "
            "rețeaua pierde pachete: încearcă un profil comprimat, care ocupă o cincime din "
            "bandă.",
    "g6_m": "Cascada se mișcă, dar nu decodează nimic",
    "g6_c": "Aproape întotdeauna e ceasul: modurile digitale stau sau cad pe secunda exactă. "
            "Lasă telefonul să ia ora din rețea.",

    "h_demo": "De încercat fără stație",
    "demo_p": "Butonul <strong>Demo</strong>, lângă <em>Recepție</em>, aprinde o bandă "
              "închipuită cu cinci stații și decodări care se derulează. Arată cum se poartă "
              "aplicația înainte de a conecta ceva — bun ca să înveți unde să te uiți, înainte "
              "de a căuta o defecțiune care nu există.",

    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — valorile indicate sunt cele implicite ale "
             "celor două programe la 16 august 2026.",
}

G3["lv"] = {
    "titolo": "Decodium Mobile caur Decolink",
    "sottotitolo": "Kā aizvest radio skaņu — un tā vadību — no stacijas datora uz telefonu: "
                   "mājās tajā pašā tīklā vai jebkur citur caur serveri.",
    "meta_app": "Decodium 4.0 Mobile",
    "meta_proto": "Decolink · protokols HFGW v2",
    "meta_data": "2026. gada 16. augusts",

    "h_prima": "Pirms sākt",
    "s1_t": "Uz datora",
    "s1_p": "<strong>Decolink</strong> darbojas blakus radio, ar pieslēgtu radio USB CODEC. Tas "
            "sūta skaņu un, ja vēlies, nodrošina CAT.",
    "s2_t": "Uz telefona",
    "s2_p": "<strong>Decodium 4 Mobile</strong>. Viss iestatāms vienuviet: zobratiņš ⚙ augšā, "
            "sadaļas <em>Stacija</em>, <em>Audio</em> un <em>CAT / Rig</em>.",
    "s3_t": "Tikai relejam",
    "s3_p": "Apstiprināta piekļuve vietnē <code>decolink.ft2.it</code>. Vietējā tīklā tā nav "
            "vajadzīga: nekādas reģistrācijas, nekas neatstāj māju.",

    "h_tre": "Trīs savienojumi",
    "tre_p": "Decolink un Decodium Mobile jābūt <strong>vienā un tajā pašā režīmā</strong>: tā "
             "ir visbiežākā kļūda, un tā nedod skaidru ziņojumu.",
    "th_modo": "Režīms", "th_quando": "Kad", "th_chi": "Kurš kuru zvana",
    "th_porta": "Ports", "th_aprire": "Jāatver",
    "lan": "LAN", "lan_q": "Telefons un dators vienā WiFi tīklā",
    "lan_c": "Dators raida skaņu uz telefona IP", "lan_a": "Nekas",
    "relay": "Relejs", "relay_q": "Ārpus mājas, arī mobilajos datos",
    "relay_c": "Abi dodas uz serveri", "relay_a": "Nekas",
    "casa": "Mājas", "casa_q": "Ārpus mājas, bez servera",
    "casa_c": "Telefons zvana uz tavu mājas adresi", "casa_a": "UDP 5555 maršrutētājā",
    "tre_fine": "<strong>Relejs</strong> ir tas, kas darbojas vienmēr: nevienam no abiem nav "
                "jābūt sasniedzamam no ārpuses, jo abi paši piesakās serverim. Tas ir arī "
                "vienīgais, kam vajadzīga piekļuve.",

    "h_pa": "A ceļš · vietējais tīkls",
    "pa1_sigla": "Uz datora · Decolink",
    "pa1_h3": "Sūti skaņu uz telefona adresi",
    "pa1_1": '<span class="dove">Radio skaņa</span> → izvēlies uztvērēja-raidītāja USB CODEC.',
    "pa1_1n": "Tā ir ieeja, pa kuru pienāk uztvertais signāls, nevis datora mikrofons.",
    "pa1_2": '<span class="dove">Režīms</span> → <code>Tiešs LAN</code>',
    "pa1_3": '<span class="dove">Resursdators</span> → telefona IP adrese mājas WiFi tīklā.',
    "pa1_3n": "Telefonā to atrodi sadaļā Iestatījumi → WiFi → tīkls, kuram esi pievienojies. "
              "Tā izskatās apmēram šādi: 192.168.1.42.",
    "pa1_4": '<span class="dove">Ports</span> → <code>5555</code>',
    "pa1_5": 'Nospied <span class="dove">Sākt</span>. Līmenim jākustas līdzi joslas troksnim.',
    "pa2_sigla": "Uz telefona · Decodium Mobile",
    "pa2_h3": "Pārej uz klausīšanos",
    "pa2_1": '⚙ → <span class="dove">Stacija</span>: izsaukuma signāls, lokators, atskaite.',
    "pa2_1n": "Bez izsaukuma signāla un lokatora ziņojumus nevar salikt.",
    "pa2_2": '<span class="dove">Audio → Savienojums</span> → <code>LAN</code>',
    "pa2_3": '<span class="dove">Ports</span> → <code>5555</code>, tas pats, kas Decolink',
    "pa2_4": 'Nospied <span class="dove">Uztvert</span>. Parādās <em>«Klausos portā 5555»</em>: '
             'no tā brīža ūdenskritums piepildās, tiklīdz dators sāk sūtīt.',
    "pa_avv_t": "LAN tīklā telefons gaida, tas nezvana",
    "pa_avv_p": "Datoram jāzina telefona IP. Ja maršrutētājs izdala adreses pēc kārtas, rīt tā "
                "IP piederēs kādam citam un skaņa vairs nepienāks: rezervē telefonam "
                "maršrutētājā pastāvīgu adresi vai pārbaudi lauku <em>Resursdators</em> katrā "
                "reizē.",

    "h_pb": "B ceļš · relejs serverī",
    "pb1_sigla": "Vienreiz · no pārlūka",
    "pb1_h3": "Pieprasi piekļuvi stacijai",
    "pb1_1": "Atver <code>https://decolink.ft2.it/registrati</code>",
    "pb1_2": "Aizpildi e-pastu, paroli, izsaukuma signālu un staciju, kurai vēlies pieslēgties.",
    "pb1_3": "Gaidi apstiprinājumu.",
    "pb1_3n": "Pieteikums paliek gaidīšanā, līdz stacijas īpašnieks to pieņem: viņš izlemj, tas "
              "nenotiek automātiski. Viņš nosaka arī tavu lomu.",
    "ruolo_tit": "Īpašnieks",
    "ruolo_tit_d": 'klausās un raida <span class="libero">— tā ir viņa stacija</span>',
    "ruolo_op": "Operators",
    "ruolo_op_d": 'klausās un raida <span class="libero">— ar īpašnieka atļauju</span>',
    "ruolo_asc": "Klausītājs",
    "ruolo_asc_d": 'tikai uztveršana <span class="libero">— raidīšanas taustiņš paliek '
                   'nedzīvs</span>',
    "pb2_sigla": "Uz datora · Decolink",
    "pb2_h3": "Ieved staciju relejā",
    "pb2_1": '<span class="dove">Serveris</span> → <code>decolink.ft2.it</code>, tad e-pasts un '
             'parole, un nospied <span class="dove">Pieteikties</span>.',
    "pb2_1n": "Ja atstāj staciju darbojamies vienu pašu, atzīmē «atcerēties paroli»: pēc "
              "pārstartēšanas tā palaižas atkal, nevienam neesot pie tastatūras.",
    "pb2_2": '<span class="dove">Režīms</span> → <code>Relejs + stacija</code>',
    "pb2_3": '<span class="dove">Resursdators</span> → <code>decolink.ft2.it</code> · '
             '<span class="dove">Ports</span> → <code>5555</code>',
    "pb2_4": '<span class="dove">Profils</span> → <code>PCM 48 kHz</code>',
    "pb2_4n": "Saspiestie profili patērē piekto daļu joslas platuma, bet atstāj tos vēlākam: "
              "vispirms pārliecinies, ka savienojums tā notur.",
    "pb2_5": 'Nospied <span class="dove">Sākt</span>.',
    "pb3_sigla": "Uz telefona · Decodium Mobile",
    "pb3_h3": "Pieteicies ar saviem datiem",
    "pb3_1": '⚙ → <span class="dove">Audio → Savienojums</span> → <code>Relejs</code>',
    "pb3_2": 'Aizpildi pieteikšanās laukus un nospied <span class="dove">Ienākt</span>.',
    "pb3_3": "Paskaties uz stāvokļa rindu: tajā jābūt tavam izsaukuma signālam, stacijai un lomai.",
    "pb3_3n": "Ja tur rakstīts «Esi ienācis kā klausītājs», tu uztver, bet neraidi: tā ir loma, "
              "nevis bojājums.",
    "pb3_4": '<span class="dove">Ports</span> → <code>5555</code>, tad '
             '<span class="dove">Uztvert</span>.',
    "campi_acc": "Pieteikšanās",
    "campi_email": "E-pasts", "campi_email_d": "tas, ar kuru reģistrējies",
    "campi_pw": "Parole", "campi_pw_d": "tava Decolink konta parole",
    "campi_relay": "Relejs", "campi_relay_d": "atstāj tukšu: tiks ņemta pieteikšanās adrese",
    "campi_porta": "Ports",
    "pb_avv_t": "Atļauja der vienu stundu",
    "pb_avv_p": "Serveris izsniedz caurlaidi, kas beidzas pēc sešdesmit minūtēm. Ja ieslēgts "
                "<em>«Atcerēties paroli»</em>, lietotne to atjauno pati minūti iepriekš; bez tā "
                "pēc stundas skaņa apstājas bez paskaidrojuma un jāpiesakās no jauna ar roku. "
                "Telefonā parole glabājas sistēmas šifrētajā atslēgu saišķī, ārpus dublējumiem.",

    "h_pc": "C ceļš · telefons zvana uz mājām",
    "pc_p": "Domāts tiem, kas negrib iet caur serveri un kam ir no ārpuses sasniedzama adrese. "
            "Pretī jāieliek rokas maršrutētājā.",
    "pc_1": '<span class="dove">Maršrutētājā</span>: pāradresē portu <code>UDP 5555</code> uz '
            'stacijas datora adresi.',
    "pc_2": '<span class="dove">Decolink</span>: režīms <code>Telefons zvana uz mājām</code>, '
            'ports <code>5555</code>. Resursdatora lauks paliek tukšs: telefons pats piesakās.',
    "pc_3": '<span class="dove">Telefonā</span>: savienojums <code>Mājas</code>, adreses laukā '
            'tavs DynDNS vārds (piemēram, <code>iu8lmc.ddns.net</code>), ports <code>5555</code>, '
            'tad <span class="dove">Uztvert</span>.',
    "pc_fine": "Ar mājas pieslēgumu aiz CG-NAT — daudzas optiskās un gandrīz visas mobilās "
               "līnijas — šis režīms nevar darboties: neviens no ārpuses tevi nesasniedz. Tieši "
               "šim gadījumam relejs arī pastāv.",

    "h_cat": "Radio vadīšana",
    "cat_p": "Skaņa un CAT ir divas atsevišķas lietas: uztvert var arī bez CAT, taču bez CAT "
             "telefons nezina, kurā frekvencē esi, un nevar ne mainīt joslu, ne pārslēgt "
             "raidīšanā.",
    "cat_th1": "Avots", "cat_th2": "Kā tas savienojas", "cat_th3": "Kur darbojas",
    "cat_r1": "TCP uz datoru",
    "cat_r1d": 'Decolink atzīmē <em>«Nodrošināt CAT telefonam»</em>; telefonā ievadi datora IP '
               'un portu <span class="num">4532</span>',
    "cat_r1w": "Vietējais tīkls",
    "cat_r2": "USB-OTG",
    "cat_r2d": "Vads no telefona uz radio, bez datora pa vidu",
    "cat_r2w": "Jebkur, kur radio ir vada attālumā",
    "cat_r3": "Audio kanāls",
    "cat_r3d": "Komandas ceļo jau atvērtajā audio savienojumā",
    "cat_r3w": "Jebkur — pareizā izvēle ar Releju vai Mājām",
    "cat_fine": "Ar <em>audio kanālu</em> nekas papildus nav jāatver: lai tas darbotos, jābūt "
                "diviem nosacījumiem — tīkla skaņa jau palaista un CAT ieslēgts Decolink.",

    "h_guai": "Kad nekas nepienāk",
    "g1_m": "«Klausos portā 5555 — datoram skaņa jāsūta šurp»",
    "g1_c": "Esi <strong>LAN</strong> režīmā, bet gribēji releju. LAN telefons tikai gaida: "
            "nekāda reģistrācija neaiziet, un tu gaidi skaņu, ko neviens nesūtīs. Nomaini "
            "savienojumu uz <em>Releju</em>.",
    "g2_m": "«Vārds nav atrisināts»",
    "g2_c": "Ierakstītā adrese neeksistē vai telefonam nav tīkla. Pārbaudi, vai releja laukā "
            "nav iekļuvis <code>https://</code>.",
    "g3_m": "«Ports 5555 ir aizņemts»",
    "g3_c": "Kāda cita lietotne tur šo portu. Aizver to vai izmanto citu — nomainot to abās "
            "programmās.",
    "g4_m": "«serveris nav sasniedzams»",
    "g4_c": "Tā ir savienojuma, nevis paroles problēma: lietotne abas ar nolūku nošķir. "
            "Pārbaudi, vai ir tīkls, un mēģini vēlreiz.",
    "g5_m": "Skaņa sākas un pēc dažām sekundēm apstājas",
    "g5_c": "Relejs izmet to, kas piecpadsmit sekundes klusē. Ja tas notiek nemitīgi, tīkls "
            "zaudē paketes: pamēģini saspiestu profilu, kas aizņem piekto daļu joslas platuma.",
    "g6_m": "Ūdenskritums kustas, bet nekas netiek dekodēts",
    "g6_c": "Gandrīz vienmēr vainīgs pulkstenis: digitālie režīmi stāv vai krīt uz precīzas "
            "sekundes. Ļauj telefonam ņemt laiku no tīkla.",

    "h_demo": "Izmēģināt bez radio",
    "demo_p": "Poga <strong>Demo</strong> blakus <em>Uztvert</em> ieslēdz izdomātu joslu ar "
              "piecām stacijām un ritošām dekodēšanām. Tā parāda, kā lietotne uzvedas, pirms "
              "vēl kaut kas ir pieslēgts — noder, lai iemācītos, kur skatīties, pirms doties "
              "meklēt bojājumu, kura nav.",

    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — norādītās vērtības ir abu programmu "
             "noklusējumi 2026. gada 16. augustā.",
}
