#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prima pagina: spagnolo, portoghese, olandese, catalano, danese, ungherese."""

T2 = {}

T2["es"] = {
    "html": "es",
    "claim": "Lleva tu radio a Decodium Mobile",
    "sotto": "El audio recibido y el control del equipo viajan por internet, de casa al "
             "teléfono, esté donde esté. Basta con la tarjeta de sonido de la radio: ni "
             "cable OTG, ni Hamlib que instalar en el teléfono.",
    "scarica": "Descargar para Windows",
    "peso": "{versione} — {peso} MB, se descomprime y se arranca",
    "vai_github": "Ir a GitHub",
    "senza_ver": "Las versiones están en GitHub",
    "h_cosa": "Qué hace",
    "p_cosa": "Manda al teléfono el audio del CODEC USB de la radio y le hace de "
              "rigctld: frecuencia, modo y PTT sin instalar nada más.",
    "h_serve": "Qué hace falta",
    "p_serve": "Windows de 64 bits, la radio conectada por USB y un acceso a esta "
               "pasarela. Nada que instalar: se descomprime y se arranca.",
    "h_ovunque": "Funciona en cualquier sitio",
    "p_ovunque": "También con datos móviles: el PC y el teléfono salen los dos hacia el "
                 "relé, así que no hay ningún router que configurar.",
    "h_parte": "Cómo empezar",
    "passo1": "Descarga el archivo y descomprímelo donde quieras, también en un pendrive.",
    "passo2_no": "Hace falta un acceso aprobado: <a href=\"/registrati\">pídelo aquí</a> "
                 "indicando tu indicativo y la estación.",
    "passo2_si": "Hace falta un acceso aprobado: ya lo tienes.",
    "passo3": "Arranca <b>Decolink.exe</b>, escribe <b>{host}</b> como servidor de "
              "acceso, entra con tus credenciales y elige la estación.",
    "passo4": "Elige la entrada de audio de la radio, pulsa <b>Iniciar</b> y en el "
              "teléfono pon Conexión = Relé.",
    "h_come": "Cómo funciona",
    "p_come": "Decolink toma el audio que la radio manda al ordenador y lo envía al "
              "teléfono, que lo reproduce. Por el mismo enlace pasan los mandos del "
              "equipo, así que desde el teléfono se cambia frecuencia y modo. El "
              "teléfono puede estar en la habitación de al lado o al otro lado del "
              "mundo: solo cambia la forma en que los dos se encuentran.",
    "m1_t": "LAN directa",
    "m1_p": "El teléfono está en el mismo WiFi: el audio va directo a su dirección. Es "
            "el camino más corto, pero solo vale dentro de casa.",
    "m2_t": "Relé y estación",
    "m2_p": "Funciona en cualquier sitio, también con datos móviles. El ordenador y el "
            "teléfono salen los dos hacia el relé, así que no hay router que abrir. Es "
            "la única manera que funciona siempre.",
    "m3_t": "El teléfono llama a casa",
    "m3_p": "Un puerto redirigido en el router y un nombre DynDNS. Para quien quiere "
            "prescindir del relé y sabe configurar su router.",
    "h_banda": "Cuánto consume",
    "p_banda": "Se elige cuánto ocupar: desde PCM a 48 kHz, que va con todo, hasta "
               "32 kbit/s para la voz y 2,4 kbit/s para solo el ritmo del manipulador "
               "en CW. Para un SSB, que ocupa 2,7 kHz, sobra con muestrear a 12 kHz.",
    "h_lingue": "Dieciséis idiomas",
    "p_lingue": "Decolink toma el idioma de Windows la primera vez que se abre, y se "
                "cambia desde el menú de arriba a la derecha. Italiano, inglés, alemán, "
                "francés, español, portugués, neerlandés, catalán, danés, húngaro, "
                "rumano, letón, ruso, japonés, chino simplificado y tradicional.",
    "accedi": "Acceder",
    "registrati": "Pedir un acceso",
    "gia": "¿Ya tienes un acceso?",
    "sorgente": "Código fuente e historial de versiones:",
    "lingua_et": "Idioma",
}

T2["pt"] = {
    "html": "pt",
    "claim": "Leve o seu rádio para o Decodium Mobile",
    "sotto": "O áudio recebido e o controlo do rádio viajam pela internet, de casa para "
             "o telemóvel, onde quer que esteja. Basta a placa de som do rádio: sem "
             "cabo OTG, sem Hamlib para instalar no telemóvel.",
    "scarica": "Transferir para Windows",
    "peso": "{versione} — {peso} MB, descompacta-se e arranca",
    "vai_github": "Ir ao GitHub",
    "senza_ver": "As versões estão no GitHub",
    "h_cosa": "O que faz",
    "p_cosa": "Envia para o telemóvel o áudio do CODEC USB do rádio e serve-lhe de "
              "rigctld: frequência, modo e PTT sem mais nada para instalar.",
    "h_serve": "O que é preciso",
    "p_serve": "Windows de 64 bits, o rádio ligado por USB e um acesso a esta gateway. "
               "Nada para instalar: descompacta-se e arranca.",
    "h_ovunque": "Funciona em qualquer lado",
    "p_ovunque": "Mesmo com dados móveis: o PC e o telemóvel saem ambos para o relé, "
                 "por isso não há router para configurar.",
    "h_parte": "Como começar",
    "passo1": "Transfira o arquivo e descompacte-o onde quiser, até numa pen USB.",
    "passo2_no": "É preciso um acesso aprovado: <a href=\"/registrati\">peça-o aqui</a> "
                 "indicando o seu indicativo e a estação.",
    "passo2_si": "É preciso um acesso aprovado: já o tem.",
    "passo3": "Abra o <b>Decolink.exe</b>, escreva <b>{host}</b> como servidor de "
              "acesso, entre com as suas credenciais e escolha a estação.",
    "passo4": "Escolha a entrada de áudio do rádio, carregue em <b>Iniciar</b> e no "
              "telemóvel ponha Ligação = Relé.",
    "h_come": "Como funciona",
    "p_come": "O Decolink pega no áudio que o rádio manda para o computador e "
              "reencaminha-o para o telemóvel, que o faz ouvir. Pela mesma ligação "
              "passam os comandos do rádio, portanto muda-se frequência e modo a partir "
              "do telemóvel. O telemóvel pode estar na sala ao lado ou do outro lado do "
              "mundo: só muda a forma como os dois se encontram.",
    "m1_t": "LAN direta",
    "m1_p": "O telemóvel está no mesmo WiFi: o áudio vai direto para o seu endereço. É "
            "o caminho mais curto, mas só vale dentro de casa.",
    "m2_t": "Relé e estação",
    "m2_p": "Funciona em qualquer lado, dados móveis incluídos. O computador e o "
            "telemóvel saem ambos para o relé, por isso não há router para abrir. É a "
            "única forma que funciona sempre.",
    "m3_t": "O telemóvel liga para casa",
    "m3_p": "Uma porta encaminhada no router e um nome DynDNS. Para quem quer dispensar "
            "o relé e sabe configurar o seu router.",
    "h_banda": "Quanto consome",
    "p_banda": "Escolhe-se quanto ocupar: do PCM a 48 kHz, que funciona com tudo, até "
               "32 kbit/s para a voz e 2,4 kbit/s só para o ritmo do manipulador em CW. "
               "Para um SSB, que ocupa 2,7 kHz, chega e sobra amostrar a 12 kHz.",
    "h_lingue": "Dezasseis línguas",
    "p_lingue": "O Decolink adota a língua do Windows na primeira abertura, e muda-se "
                "no menu ao canto superior direito. Italiano, inglês, alemão, francês, "
                "espanhol, português, neerlandês, catalão, dinamarquês, húngaro, "
                "romeno, letão, russo, japonês, chinês simplificado e tradicional.",
    "accedi": "Entrar",
    "registrati": "Pedir um acesso",
    "gia": "Já tem acesso?",
    "sorgente": "Código-fonte e histórico de versões:",
    "lingua_et": "Língua",
}

T2["nl"] = {
    "html": "nl",
    "claim": "Zet je set op Decodium Mobile",
    "sotto": "Ontvangen audio en bediening van de set gaan over internet, van thuis naar "
             "je telefoon, waar die ook is. De geluidskaart van de set volstaat: geen "
             "OTG-kabel, geen Hamlib op de telefoon.",
    "scarica": "Downloaden voor Windows",
    "peso": "{versione} — {peso} MB, uitpakken en starten",
    "vai_github": "Naar GitHub",
    "senza_ver": "De versies staan op GitHub",
    "h_cosa": "Wat het doet",
    "p_cosa": "Stuurt de audio van de USB-CODEC van de set naar je telefoon en doet "
              "dienst als rigctld: frequentie, mode en PTT zonder verdere installatie.",
    "h_serve": "Wat je nodig hebt",
    "p_serve": "64-bits Windows, de set via USB aangesloten en een account op deze "
               "gateway. Niets te installeren: uitpakken en starten.",
    "h_ovunque": "Werkt overal",
    "p_ovunque": "Ook op mobiele data: de pc en de telefoon gaan allebei naar de relay, "
                 "dus er is geen router in te stellen.",
    "h_parte": "Zo begin je",
    "passo1": "Download het archief en pak het uit waar je wilt, ook op een USB-stick.",
    "passo2_no": "Je hebt een goedgekeurd account nodig: <a href=\"/registrati\">vraag "
                 "het hier aan</a>, met je roepnaam en station.",
    "passo2_si": "Je hebt een goedgekeurd account nodig: dat heb je al.",
    "passo3": "Start <b>Decolink.exe</b>, vul <b>{host}</b> in als aanmeldserver, meld "
              "je aan en kies het station.",
    "passo4": "Kies de audio-ingang van de set, druk op <b>Starten</b> en zet op de "
              "telefoon Verbinding = Relay.",
    "h_come": "Hoe het werkt",
    "p_come": "Decolink neemt de audio die de set naar de computer stuurt en geeft die "
              "door aan de telefoon, die hem hoorbaar maakt. Over dezelfde verbinding "
              "lopen de commando's voor de set, dus je verandert frequentie en mode "
              "vanaf de telefoon. De telefoon mag in de kamer ernaast staan of aan de "
              "andere kant van de wereld: alleen de manier waarop de twee elkaar vinden "
              "verandert.",
    "m1_t": "Direct LAN",
    "m1_p": "De telefoon zit op dezelfde WiFi: de audio gaat rechtstreeks naar zijn "
            "adres. De kortste weg, maar alleen binnenshuis.",
    "m2_t": "Relay en station",
    "m2_p": "Werkt overal, mobiele data inbegrepen. De computer en de telefoon gaan "
            "allebei naar de relay, dus er is geen router open te zetten. Het is de "
            "enige manier die altijd werkt.",
    "m3_t": "De telefoon belt naar huis",
    "m3_p": "Een doorgestuurde poort op de router en een DynDNS-naam. Voor wie zonder "
            "relay wil en zijn eigen router kan instellen.",
    "h_banda": "Hoeveel het verbruikt",
    "p_banda": "Je kiest hoeveel: van PCM op 48 kHz, dat met alles werkt, tot "
               "32 kbit/s voor spraak en 2,4 kbit/s voor alleen het seinritme in CW. "
               "Voor SSB, dat 2,7 kHz beslaat, is bemonstering op 12 kHz ruim genoeg.",
    "h_lingue": "Zestien talen",
    "p_lingue": "Decolink neemt bij de eerste start de taal van Windows over, en je "
                "wijzigt hem via het menu rechtsboven. Italiaans, Engels, Duits, Frans, "
                "Spaans, Portugees, Nederlands, Catalaans, Deens, Hongaars, Roemeens, "
                "Lets, Russisch, Japans, Chinees vereenvoudigd en traditioneel.",
    "accedi": "Aanmelden",
    "registrati": "Account aanvragen",
    "gia": "Heb je al een account?",
    "sorgente": "Broncode en versiegeschiedenis:",
    "lingua_et": "Taal",
}

T2["ca"] = {
    "html": "ca",
    "claim": "Porta la teva ràdio a Decodium Mobile",
    "sotto": "L'àudio rebut i el control de l'equip viatgen per internet, de casa al "
             "telèfon, sigui on sigui. Amb la targeta de so de la ràdio n'hi ha prou: "
             "sense cable OTG, sense Hamlib per instal·lar al telèfon.",
    "scarica": "Baixa per a Windows",
    "peso": "{versione} — {peso} MB, es descomprimeix i s'engega",
    "vai_github": "Vés a GitHub",
    "senza_ver": "Les versions són a GitHub",
    "h_cosa": "Què fa",
    "p_cosa": "Envia al telèfon l'àudio del CODEC USB de la ràdio i li fa de rigctld: "
              "freqüència, mode i PTT sense instal·lar res més.",
    "h_serve": "Què cal",
    "p_serve": "Windows de 64 bits, la ràdio connectada per USB i un accés a aquesta "
               "passarel·la. Res per instal·lar: es descomprimeix i s'engega.",
    "h_ovunque": "Funciona a tot arreu",
    "p_ovunque": "També amb dades mòbils: el PC i el telèfon surten tots dos cap al "
                 "relé, així no hi ha cap encaminador a configurar.",
    "h_parte": "Com començar",
    "passo1": "Baixa l'arxiu i descomprimeix-lo on vulguis, també en un llapis USB.",
    "passo2_no": "Cal un accés aprovat: <a href=\"/registrati\">demana'l aquí</a> "
                 "indicant el teu indicatiu i l'estació.",
    "passo2_si": "Cal un accés aprovat: ja el tens.",
    "passo3": "Engega <b>Decolink.exe</b>, escriu <b>{host}</b> com a servidor d'accés, "
              "entra amb les teves credencials i tria l'estació.",
    "passo4": "Tria l'entrada d'àudio de la ràdio, prem <b>Inicia</b> i al telèfon posa "
              "Connexió = Relé.",
    "h_come": "Com funciona",
    "p_come": "El Decolink agafa l'àudio que la ràdio envia a l'ordinador i el fa "
              "arribar al telèfon, que el fa sentir. Pel mateix enllaç hi passen les "
              "ordres de l'equip, així que des del telèfon es canvia freqüència i mode. "
              "El telèfon pot ser a l'habitació del costat o a l'altra punta del món: "
              "només canvia com es troben tots dos.",
    "m1_t": "LAN directa",
    "m1_p": "El telèfon és a la mateixa WiFi: l'àudio va directe a la seva adreça. És "
            "el camí més curt, però només val dins de casa.",
    "m2_t": "Relé i estació",
    "m2_p": "Funciona a tot arreu, també amb dades mòbils. L'ordinador i el telèfon "
            "surten tots dos cap al relé, així no hi ha cap encaminador a obrir. És "
            "l'única manera que funciona sempre.",
    "m3_t": "El telèfon truca a casa",
    "m3_p": "Un port redirigit a l'encaminador i un nom DynDNS. Per a qui vol prescindir "
            "del relé i sap configurar el seu encaminador.",
    "h_banda": "Quant consumeix",
    "p_banda": "Es tria quant ocupar: des del PCM a 48 kHz, que va amb tot, fins a "
               "32 kbit/s per a la veu i 2,4 kbit/s només per al ritme del manipulador "
               "en CW. Per a un SSB, que ocupa 2,7 kHz, amb mostrejar a 12 kHz en va de "
               "sobres.",
    "h_lingue": "Setze llengües",
    "p_lingue": "El Decolink agafa la llengua del Windows la primera vegada que s'obre, "
                "i es canvia des del menú de dalt a la dreta. Italià, anglès, alemany, "
                "francès, espanyol, portuguès, neerlandès, català, danès, hongarès, "
                "romanès, letó, rus, japonès, xinès simplificat i tradicional.",
    "accedi": "Accedeix",
    "registrati": "Demana un accés",
    "gia": "Ja tens accés?",
    "sorgente": "Codi font i historial de versions:",
    "lingua_et": "Llengua",
}

T2["da"] = {
    "html": "da",
    "claim": "Tag din radio med på Decodium Mobile",
    "sotto": "Modtaget lyd og betjening af radioen går over internettet, hjemmefra til "
             "telefonen, hvor den end er. Radioens lydkort er nok: intet OTG-kabel, "
             "ingen Hamlib at installere på telefonen.",
    "scarica": "Hent til Windows",
    "peso": "{versione} — {peso} MB, pakkes ud og startes",
    "vai_github": "Gå til GitHub",
    "senza_ver": "Versionerne ligger på GitHub",
    "h_cosa": "Hvad den gør",
    "p_cosa": "Sender lyden fra radioens USB-CODEC til telefonen og fungerer som "
              "rigctld: frekvens, modulation og PTT uden at installere andet.",
    "h_serve": "Hvad der skal til",
    "p_serve": "64-bit Windows, radioen tilsluttet via USB og en adgang til denne "
               "gateway. Intet at installere: pak ud og start.",
    "h_ovunque": "Virker overalt",
    "p_ovunque": "Også på mobildata: pc og telefon går begge ud til relæet, så der er "
                 "ingen router at sætte op.",
    "h_parte": "Sådan kommer du i gang",
    "passo1": "Hent arkivet og pak det ud, hvor du vil — også på en USB-nøgle.",
    "passo2_no": "Der skal en godkendt adgang til: <a href=\"/registrati\">bed om den "
                 "her</a> med dit kaldesignal og stationen.",
    "passo2_si": "Der skal en godkendt adgang til: den har du allerede.",
    "passo3": "Start <b>Decolink.exe</b>, skriv <b>{host}</b> som loginserver, log ind "
              "med dine oplysninger og vælg stationen.",
    "passo4": "Vælg radioens lydindgang, tryk <b>Start</b>, og sæt på telefonen "
              "Forbindelse = Relæ.",
    "h_come": "Sådan virker det",
    "p_come": "Decolink tager den lyd, radioen sender til computeren, og videresender "
              "den til telefonen, der afspiller den. Over samme forbindelse går "
              "kommandoerne til radioen, så du skifter frekvens og modulation fra "
              "telefonen. Telefonen kan stå i næste rum eller på den anden side af "
              "jorden: kun måden, de to finder hinanden på, ændrer sig.",
    "m1_t": "Direkte LAN",
    "m1_p": "Telefonen er på samme WiFi: lyden sendes direkte til dens adresse. Den "
            "korteste vej, men kun inden døre.",
    "m2_t": "Relæ og station",
    "m2_p": "Virker overalt, mobildata inklusive. Computer og telefon går begge ud til "
            "relæet, så der er ingen router at åbne. Det er den eneste måde, der altid "
            "virker.",
    "m3_t": "Telefonen ringer hjem",
    "m3_p": "En videresendt port på routeren og et DynDNS-navn. For dem, der vil undvære "
            "relæet og selv kan sætte deres router op.",
    "h_banda": "Hvor meget den bruger",
    "p_banda": "Du vælger hvor meget: fra PCM ved 48 kHz, der virker med alt, ned til "
               "32 kbit/s for tale og 2,4 kbit/s for ren CW-nøgling. Til SSB, der fylder "
               "2,7 kHz, er 12 kHz sampling rigeligt.",
    "h_lingue": "Seksten sprog",
    "p_lingue": "Decolink tager sproget fra Windows første gang, den åbnes, og det "
                "skiftes fra menuen øverst til højre. Italiensk, engelsk, tysk, fransk, "
                "spansk, portugisisk, hollandsk, catalansk, dansk, ungarsk, rumænsk, "
                "lettisk, russisk, japansk, kinesisk forenklet og traditionelt.",
    "accedi": "Log ind",
    "registrati": "Bed om adgang",
    "gia": "Har du allerede adgang?",
    "sorgente": "Kildekode og versionshistorik:",
    "lingua_et": "Sprog",
}

T2["hu"] = {
    "html": "hu",
    "claim": "Vidd a rádiódat a Decodium Mobile-ra",
    "sotto": "A vett hang és a rádió vezérlése az interneten utazik, otthonról a "
             "telefonra, bárhol is legyen. Elég hozzá a rádió hangkártyája: nincs "
             "OTG-kábel, nincs telefonra telepítendő Hamlib.",
    "scarica": "Letöltés Windowsra",
    "peso": "{versione} — {peso} MB, kicsomagolni és indítani",
    "vai_github": "Tovább a GitHubra",
    "senza_ver": "A verziók a GitHubon vannak",
    "h_cosa": "Mit csinál",
    "p_cosa": "A rádió USB-CODEC-jének hangját a telefonra küldi, és rigctld-ként "
              "szolgál: frekvencia, üzemmód és PTT minden további telepítés nélkül.",
    "h_serve": "Mi kell hozzá",
    "p_serve": "64 bites Windows, USB-n csatlakoztatott rádió és hozzáférés ehhez az "
               "átjáróhoz. Nincs mit telepíteni: kicsomagolni és indítani.",
    "h_ovunque": "Mindenhol működik",
    "p_ovunque": "Mobilneten is: a számítógép és a telefon egyaránt a reléhez "
                 "csatlakozik, így nincs router, amit be kellene állítani.",
    "h_parte": "Így kezdj hozzá",
    "passo1": "Töltsd le az archívumot, és csomagold ki, ahová akarod — akár pendrive-ra.",
    "passo2_no": "Jóváhagyott hozzáférés kell: <a href=\"/registrati\">kérd itt</a>, "
                 "megadva a hívójeledet és az állomást.",
    "passo2_si": "Jóváhagyott hozzáférés kell: már megvan.",
    "passo3": "Indítsd el a <b>Decolink.exe</b>-t, írd be a <b>{host}</b> címet "
              "bejelentkezési kiszolgálónak, lépj be, és válaszd ki az állomást.",
    "passo4": "Válaszd ki a rádió hangbemenetét, nyomd meg az <b>Indítás</b> gombot, a "
              "telefonon pedig állítsd a Kapcsolatot Relére.",
    "h_come": "Hogyan működik",
    "p_come": "A Decolink veszi a hangot, amit a rádió a számítógépnek küld, és "
              "továbbítja a telefonra, amely megszólaltatja. Ugyanazon a kapcsolaton "
              "mennek a rádió parancsai is, így a telefonról állítható a frekvencia és "
              "az üzemmód. A telefon lehet a szomszéd szobában vagy a világ másik "
              "felén: csak az változik, ahogy a kettő egymásra talál.",
    "m1_t": "Közvetlen LAN",
    "m1_p": "A telefon ugyanazon a WiFin van: a hang egyenesen a címére megy. A "
            "legrövidebb út, de csak házon belül.",
    "m2_t": "Relé és állomás",
    "m2_p": "Mindenhol működik, mobilneten is. A számítógép és a telefon egyaránt a "
            "reléhez csatlakozik, így nincs routert nyitogatni. Ez az egyetlen mód, "
            "ami mindig működik.",
    "m3_t": "A telefon hívja az otthont",
    "m3_p": "Átirányított port a routeren és egy DynDNS-név. Annak, aki a relé nélkül "
            "boldogul, és be tudja állítani a saját routerét.",
    "h_banda": "Mennyit fogyaszt",
    "p_banda": "Te választod meg: a 48 kHz-es PCM-től, ami mindennel megy, egészen "
               "32 kbit/s-ig beszédre és 2,4 kbit/s-ig a puszta CW-billentyűzésre. Az "
               "SSB-hez, ami 2,7 kHz-et foglal, a 12 kHz-es mintavétel bőven elég.",
    "h_lingue": "Tizenhat nyelv",
    "p_lingue": "A Decolink első indításkor a Windows nyelvét veszi át, és a jobb felső "
                "menüből lehet megváltoztatni. Olasz, angol, német, francia, spanyol, "
                "portugál, holland, katalán, dán, magyar, román, lett, orosz, japán, "
                "egyszerűsített és hagyományos kínai.",
    "accedi": "Belépés",
    "registrati": "Hozzáférés kérése",
    "gia": "Van már hozzáférésed?",
    "sorgente": "Forráskód és verziótörténet:",
    "lingua_et": "Nyelv",
}
