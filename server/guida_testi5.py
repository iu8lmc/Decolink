#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggiornamento della guida al protocollo v3.

La guida descriveva la v2: un solo formato, PCM a 48 kHz, 808 kbit/s per tutti.
La v3 lascia scegliere quanto occupare, e la differenza fra un profilo e
l'altro non e' un dettaglio: da 808 kbit/s a 2,4 kbit/s ci sono tre ordini di
grandezza, e cambia quali collegamenti sono possibili.

Questo file contiene le voci nuove (la tabella dei profili) e quelle che la v2
diceva in modo ormai sbagliato — «un quinto della banda» era vero per nessun
profilo: Opus in fonia occupa un venticinquesimo.

I numeri sono quelli misurati in PROTOCOLLO.md, non stimati.
"""

G5 = {}

G5["it"] = {
    "banda_cwkey": "2,4 kbit/s",
    "meta_proto": "Decolink · protocollo v3",
    "meta_data": "17 agosto 2026",
    "h_prof": "Quanta banda occupa",
    "prof_p": "Il profilo si sceglie su Decolink e vale per tutto il collegamento. Fra il primo "
              "e l'ultimo ci sono tre ordini di grandezza, e non è un dettaglio: decide quali "
              "collegamenti sono possibili.",
    "prof_th1": "Profilo", "prof_th2": "Banda", "prof_th3": "Quando",
    "pr1": "PCM 48 kHz", "pr1_q": "Compatibile con tutto, nessuna compressione. È il punto di "
                                  "partenza: 364 MB l'ora.",
    "pr2": "PCM 12 kHz", "pr2_q": "Basta e avanza per un SSB, che di banda ne occupa 2,7 kHz. "
                                  "Se il telefono lo sente accelerato, torna a 48.",
    "pr3": "Voce (Opus)", "pr3_q": "Fonia: venticinque volte meno del PCM. Serve un telefono "
                                   "aggiornato dall'altra parte.",
    "pr4": "CW (Opus)", "pr4_q": "Telegrafia a banda stretta: quaranta volte meno del PCM.",
    "pr5": "Digitali", "pr5_q": "Compresso senza perdere un bit: FT8 e simili decodificano "
                                "come sul PCM, perché è lo stesso segnale.",
    "pr6": "CW a tasto", "pr6_q": "Solo gli istanti del tasto. Si perde tutto il contesto — "
                                  "QSB, QRM, chi chiama fuori nota — ma passa su qualunque cosa.",
    "prof_fine": "Sotto i 20 kbit/s l'involucro pesa più del contenuto: ogni pacchetto porta 28 "
                 "byte di intestazioni IP e UDP, e abbassare ancora il codec smette di servire. "
                 "Per questo si raggruppano più frame in un pacchetto: a 40 ms di pacchetto si "
                 "risparmia il 18% della banda, e il ritardo in più non si sente.",
    "pb2_4n": "I profili compressi arrivano a occupare venticinque volte meno, ma tienili per "
              "dopo: prima verifica che il collegamento regga così. La tabella qui sotto dice "
              "quanto costa ciascuno.",
    "g5_c": "Il relay scarta chi resta zitto per quindici secondi. Se succede di continuo, la "
            "rete sta perdendo pacchetti: passa al profilo Voce, che occupa venticinque volte "
            "meno del PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — i valori indicati sono quelli predefiniti "
             "dei due programmi al 17 agosto 2026; le bande sono misurate, non stimate.",
}

G5["en"] = {
    "banda_cwkey": "2.4 kbit/s",
    "meta_proto": "Decolink · v3 protocol",
    "meta_data": "17 August 2026",
    "h_prof": "How much bandwidth it takes",
    "prof_p": "The profile is chosen in Decolink and applies to the whole link. Between the "
              "first and the last there are three orders of magnitude, and that is no detail: "
              "it decides which links are possible at all.",
    "prof_th1": "Profile", "prof_th2": "Bandwidth", "prof_th3": "When",
    "pr1": "PCM 48 kHz", "pr1_q": "Works with everything, no compression. It is the starting "
                                  "point: 364 MB per hour.",
    "pr2": "PCM 12 kHz", "pr2_q": "Plenty for SSB, which only occupies 2.7 kHz. If the phone "
                                  "plays it sped up, go back to 48.",
    "pr3": "Voice (Opus)", "pr3_q": "Phone: twenty-five times less than PCM. Needs an updated "
                                    "phone at the other end.",
    "pr4": "CW (Opus)", "pr4_q": "Narrow-band telegraphy: forty times less than PCM.",
    "pr5": "Digital", "pr5_q": "Compressed without losing a bit: FT8 and the like decode just "
                               "as they do on PCM, because it is the same signal.",
    "pr6": "CW keying", "pr6_q": "Only the keying instants. You lose all the context — QSB, "
                                 "QRM, anyone calling off frequency — but it goes through "
                                 "anything.",
    "prof_fine": "Below 20 kbit/s the wrapper weighs more than the contents: every packet "
                 "carries 28 bytes of IP and UDP headers, and lowering the codec further stops "
                 "helping. That is why several frames are grouped into one packet: at 40 ms per "
                 "packet you save 18% of the bandwidth, and the extra delay cannot be felt.",
    "pb2_4n": "Compressed profiles get down to twenty-five times less, but save them for later: "
              "first make sure the link holds up like this. The table below says what each one "
              "costs.",
    "g5_c": "The relay drops anyone silent for fifteen seconds. If it keeps happening, the "
            "network is losing packets: switch to the Voice profile, which takes twenty-five "
            "times less than PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — the values given are the two programs' "
             "defaults as of 17 August 2026; the bandwidths are measured, not estimated.",
}

G5["de"] = {
    "banda_cwkey": "2,4 kbit/s",
    "meta_proto": "Decolink · Protokoll v3",
    "meta_data": "17. August 2026",
    "h_prof": "Wie viel Bandbreite es braucht",
    "prof_p": "Das Profil wird in Decolink gewählt und gilt für die ganze Verbindung. Zwischen "
              "dem ersten und dem letzten liegen drei Größenordnungen, und das ist kein "
              "Detail: es entscheidet, welche Verbindungen überhaupt möglich sind.",
    "prof_th1": "Profil", "prof_th2": "Bandbreite", "prof_th3": "Wann",
    "pr1": "PCM 48 kHz", "pr1_q": "Funktioniert mit allem, keine Kompression. Der Ausgangspunkt: "
                                  "364 MB pro Stunde.",
    "pr2": "PCM 12 kHz", "pr2_q": "Reichlich für SSB, das nur 2,7 kHz belegt. Klingt es am "
                                  "Telefon zu schnell, zurück auf 48.",
    "pr3": "Sprache (Opus)", "pr3_q": "Fonie: fünfundzwanzigmal weniger als PCM. Erfordert ein "
                                      "aktuelles Telefon auf der Gegenseite.",
    "pr4": "CW (Opus)", "pr4_q": "Schmalbandige Telegrafie: vierzigmal weniger als PCM.",
    "pr5": "Digimodes", "pr5_q": "Verlustfrei komprimiert: FT8 und ähnliche dekodieren wie auf "
                                 "PCM, denn es ist dasselbe Signal.",
    "pr6": "CW-Tastung", "pr6_q": "Nur die Tastzeitpunkte. Der ganze Kontext geht verloren — "
                                  "QSB, QRM, wer neben der Frequenz ruft — dafür kommt es überall "
                                  "durch.",
    "prof_fine": "Unter 20 kbit/s wiegt die Hülle mehr als der Inhalt: jedes Paket trägt 28 Byte "
                 "IP- und UDP-Kopfdaten, und den Codec weiter zu senken bringt nichts mehr. "
                 "Darum werden mehrere Frames in ein Paket gebündelt: bei 40 ms Paketlänge spart "
                 "man 18% der Bandbreite, und die zusätzliche Verzögerung merkt man nicht.",
    "pb2_4n": "Die komprimierten Profile kommen auf ein Fünfundzwanzigstel herunter, aber hebe "
              "sie dir auf: prüfe erst, ob die Verbindung so trägt. Die Tabelle unten sagt, was "
              "jedes kostet.",
    "g5_c": "Das Relay wirft hinaus, wer fünfzehn Sekunden lang stumm bleibt. Passiert das "
            "andauernd, verliert das Netz Pakete: wechsle auf das Profil Sprache, das "
            "fünfundzwanzigmal weniger braucht als PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — die genannten Werte sind die "
             "Voreinstellungen der beiden Programme, Stand 17. August 2026; die Bandbreiten "
             "sind gemessen, nicht geschätzt.",
}

G5["fr"] = {
    "banda_cwkey": "2,4 kbit/s",
    "meta_proto": "Decolink · protocole v3",
    "meta_data": "17 août 2026",
    "h_prof": "Ce que ça consomme",
    "prof_p": "Le profil se choisit dans Decolink et vaut pour toute la liaison. Entre le "
              "premier et le dernier il y a trois ordres de grandeur, et ce n'est pas un "
              "détail : cela décide quelles liaisons sont possibles.",
    "prof_th1": "Profil", "prof_th2": "Bande", "prof_th3": "Quand",
    "pr1": "PCM 48 kHz", "pr1_q": "Passe avec tout, aucune compression. C'est le point de "
                                  "départ : 364 Mo par heure.",
    "pr2": "PCM 12 kHz", "pr2_q": "Largement suffisant pour la BLU, qui n'occupe que 2,7 kHz. "
                                  "Si le téléphone l'entend accéléré, revenez à 48.",
    "pr3": "Voix (Opus)", "pr3_q": "Phonie : vingt-cinq fois moins que le PCM. Nécessite un "
                                   "téléphone à jour en face.",
    "pr4": "CW (Opus)", "pr4_q": "Télégraphie à bande étroite : quarante fois moins que le PCM.",
    "pr5": "Numérique", "pr5_q": "Compressé sans perdre un bit : FT8 et consorts décodent comme "
                                 "en PCM, puisque c'est le même signal.",
    "pr6": "Manipulation CW", "pr6_q": "Seulement les instants de manipulation. On perd tout le "
                                       "contexte — QSB, QRM, ceux qui appellent hors fréquence — "
                                       "mais ça passe partout.",
    "prof_fine": "Sous 20 kbit/s l'emballage pèse plus que le contenu : chaque paquet porte "
                 "28 octets d'en-têtes IP et UDP, et baisser encore le codec ne sert plus. C'est "
                 "pourquoi on regroupe plusieurs trames par paquet : à 40 ms de paquet on "
                 "économise 18% de la bande, et le retard supplémentaire ne s'entend pas.",
    "pb2_4n": "Les profils compressés descendent jusqu'à vingt-cinq fois moins, mais gardez-les "
              "pour plus tard : vérifiez d'abord que la liaison tient comme ça. Le tableau "
              "ci-dessous dit ce que coûte chacun.",
    "g5_c": "Le relais écarte ceux qui restent muets quinze secondes. Si cela se répète, le "
            "réseau perd des paquets : passez au profil Voix, qui occupe vingt-cinq fois moins "
            "que le PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — les valeurs indiquées sont celles par "
             "défaut des deux programmes au 17 août 2026 ; les bandes sont mesurées, non "
             "estimées.",
}

G5["es"] = {
    "banda_cwkey": "2,4 kbit/s",
    "meta_proto": "Decolink · protocolo v3",
    "meta_data": "17 de agosto de 2026",
    "h_prof": "Cuánto ancho de banda ocupa",
    "prof_p": "El perfil se elige en Decolink y vale para todo el enlace. Entre el primero y el "
              "último hay tres órdenes de magnitud, y no es un detalle: decide qué enlaces son "
              "posibles.",
    "prof_th1": "Perfil", "prof_th2": "Banda", "prof_th3": "Cuándo",
    "pr1": "PCM 48 kHz", "pr1_q": "Va con todo, sin compresión. Es el punto de partida: 364 MB "
                                  "por hora.",
    "pr2": "PCM 12 kHz", "pr2_q": "De sobra para un SSB, que ocupa 2,7 kHz. Si el teléfono lo "
                                  "oye acelerado, vuelve a 48.",
    "pr3": "Voz (Opus)", "pr3_q": "Fonía: veinticinco veces menos que el PCM. Hace falta un "
                                  "teléfono actualizado al otro lado.",
    "pr4": "CW (Opus)", "pr4_q": "Telegrafía de banda estrecha: cuarenta veces menos que el PCM.",
    "pr5": "Digitales", "pr5_q": "Comprimido sin perder un bit: FT8 y similares decodifican "
                                 "igual que en PCM, porque es la misma señal.",
    "pr6": "Manipulación CW", "pr6_q": "Solo los instantes del manipulador. Se pierde todo el "
                                       "contexto — QSB, QRM, quien llama fuera de frecuencia — "
                                       "pero pasa por cualquier cosa.",
    "prof_fine": "Por debajo de 20 kbit/s el envoltorio pesa más que el contenido: cada paquete "
                 "lleva 28 bytes de cabeceras IP y UDP, y bajar más el códec deja de servir. Por "
                 "eso se agrupan varias tramas en un paquete: con 40 ms de paquete se ahorra el "
                 "18% del ancho de banda, y el retardo añadido no se nota.",
    "pb2_4n": "Los perfiles comprimidos llegan a ocupar veinticinco veces menos, pero déjalos "
              "para después: primero comprueba que el enlace aguanta así. La tabla de abajo dice "
              "lo que cuesta cada uno.",
    "g5_c": "El relé descarta a quien se queda callado quince segundos. Si pasa continuamente, "
            "la red está perdiendo paquetes: pasa al perfil Voz, que ocupa veinticinco veces "
            "menos que el PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — los valores indicados son los "
             "predeterminados de los dos programas a 17 de agosto de 2026; los anchos de banda "
             "están medidos, no estimados.",
}

G5["pt"] = {
    "banda_cwkey": "2,4 kbit/s",
    "meta_proto": "Decolink · protocolo v3",
    "meta_data": "17 de agosto de 2026",
    "h_prof": "Quanta largura de banda ocupa",
    "prof_p": "O perfil escolhe-se no Decolink e vale para toda a ligação. Entre o primeiro e o "
              "último há três ordens de grandeza, e não é um pormenor: decide que ligações são "
              "possíveis.",
    "prof_th1": "Perfil", "prof_th2": "Banda", "prof_th3": "Quando",
    "pr1": "PCM 48 kHz", "pr1_q": "Funciona com tudo, sem compressão. É o ponto de partida: "
                                  "364 MB por hora.",
    "pr2": "PCM 12 kHz", "pr2_q": "Mais do que suficiente para um SSB, que ocupa 2,7 kHz. Se o "
                                  "telemóvel o ouvir acelerado, volte a 48.",
    "pr3": "Voz (Opus)", "pr3_q": "Fonia: vinte e cinco vezes menos do que o PCM. Exige um "
                                  "telemóvel atualizado do outro lado.",
    "pr4": "CW (Opus)", "pr4_q": "Telegrafia de banda estreita: quarenta vezes menos do que o PCM.",
    "pr5": "Digitais", "pr5_q": "Comprimido sem perder um bit: o FT8 e afins descodificam como "
                                "em PCM, porque é o mesmo sinal.",
    "pr6": "Manipulação CW", "pr6_q": "Só os instantes do manipulador. Perde-se todo o contexto "
                                      "— QSB, QRM, quem chama fora de frequência — mas passa por "
                                      "qualquer coisa.",
    "prof_fine": "Abaixo dos 20 kbit/s o invólucro pesa mais do que o conteúdo: cada pacote leva "
                 "28 bytes de cabeçalhos IP e UDP, e baixar mais o codec deixa de servir. Por "
                 "isso agrupam-se várias tramas num pacote: com 40 ms de pacote poupa-se 18% da "
                 "largura de banda, e o atraso acrescentado não se nota.",
    "pb2_4n": "Os perfis comprimidos chegam a ocupar vinte e cinco vezes menos, mas guarde-os "
              "para depois: verifique primeiro que a ligação aguenta assim. A tabela abaixo diz "
              "quanto custa cada um.",
    "g5_c": "O relé descarta quem fica calado quinze segundos. Se acontece a toda a hora, a rede "
            "está a perder pacotes: passe ao perfil Voz, que ocupa vinte e cinco vezes menos do "
            "que o PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — os valores indicados são os predefinidos "
             "dos dois programas a 17 de agosto de 2026; as larguras de banda são medidas, não "
             "estimadas.",
}

G5["nl"] = {
    "banda_cwkey": "2,4 kbit/s",
    "meta_proto": "Decolink · protocol v3",
    "meta_data": "17 augustus 2026",
    "h_prof": "Hoeveel bandbreedte het kost",
    "prof_p": "Het profiel kies je in Decolink en het geldt voor de hele verbinding. Tussen het "
              "eerste en het laatste zitten drie ordes van grootte, en dat is geen detail: het "
              "bepaalt welke verbindingen überhaupt mogelijk zijn.",
    "prof_th1": "Profiel", "prof_th2": "Bandbreedte", "prof_th3": "Wanneer",
    "pr1": "PCM 48 kHz", "pr1_q": "Werkt met alles, geen compressie. Het vertrekpunt: 364 MB per "
                                  "uur.",
    "pr2": "PCM 12 kHz", "pr2_q": "Ruim genoeg voor SSB, dat maar 2,7 kHz beslaat. Klinkt het op "
                                  "de telefoon versneld, ga terug naar 48.",
    "pr3": "Spraak (Opus)", "pr3_q": "Fonie: vijfentwintig keer minder dan PCM. Vereist een "
                                     "bijgewerkte telefoon aan de andere kant.",
    "pr4": "CW (Opus)", "pr4_q": "Smalbandige telegrafie: veertig keer minder dan PCM.",
    "pr5": "Digitaal", "pr5_q": "Verliesvrij gecomprimeerd: FT8 en soortgenoten decoderen net "
                                "als op PCM, want het is hetzelfde signaal.",
    "pr6": "CW-seinen", "pr6_q": "Alleen de seinmomenten. Alle context gaat verloren — QSB, QRM, "
                                 "wie naast de frequentie roept — maar het komt overal doorheen.",
    "prof_fine": "Onder de 20 kbit/s weegt de verpakking zwaarder dan de inhoud: elk pakket "
                 "draagt 28 bytes aan IP- en UDP-headers, en de codec verder verlagen helpt niet "
                 "meer. Daarom worden meerdere frames in één pakket gebundeld: bij 40 ms per "
                 "pakket bespaar je 18% bandbreedte, en de extra vertraging hoor je niet.",
    "pb2_4n": "De gecomprimeerde profielen komen tot vijfentwintig keer minder, maar bewaar ze "
              "voor later: kijk eerst of de verbinding het zo houdt. De tabel hieronder zegt wat "
              "elk profiel kost.",
    "g5_c": "De relay gooit eruit wie vijftien seconden stil blijft. Gebeurt het steeds, dan "
            "verliest het netwerk pakketten: schakel over op het profiel Spraak, dat "
            "vijfentwintig keer minder gebruikt dan PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — de genoemde waarden zijn de "
             "standaardinstellingen van beide programma's op 17 augustus 2026; de bandbreedtes "
             "zijn gemeten, niet geschat.",
}

G5["ca"] = {
    "banda_cwkey": "2,4 kbit/s",
    "meta_proto": "Decolink · protocol v3",
    "meta_data": "17 d'agost de 2026",
    "h_prof": "Quanta amplada de banda ocupa",
    "prof_p": "El perfil es tria al Decolink i val per a tot l'enllaç. Entre el primer i l'últim "
              "hi ha tres ordres de magnitud, i no és cap detall: decideix quins enllaços són "
              "possibles.",
    "prof_th1": "Perfil", "prof_th2": "Banda", "prof_th3": "Quan",
    "pr1": "PCM 48 kHz", "pr1_q": "Va amb tot, sense compressió. És el punt de partida: 364 MB "
                                  "per hora.",
    "pr2": "PCM 12 kHz", "pr2_q": "De sobres per a un SSB, que ocupa 2,7 kHz. Si el telèfon el "
                                  "sent accelerat, torna a 48.",
    "pr3": "Veu (Opus)", "pr3_q": "Fonia: vint-i-cinc vegades menys que el PCM. Cal un telèfon "
                                  "actualitzat a l'altra banda.",
    "pr4": "CW (Opus)", "pr4_q": "Telegrafia de banda estreta: quaranta vegades menys que el PCM.",
    "pr5": "Digitals", "pr5_q": "Comprimit sense perdre cap bit: l'FT8 i companyia descodifiquen "
                                "igual que en PCM, perquè és el mateix senyal.",
    "pr6": "Manipulació CW", "pr6_q": "Només els instants del manipulador. Es perd tot el context "
                                      "— QSB, QRM, qui crida fora de freqüència — però passa per "
                                      "qualsevol cosa.",
    "prof_fine": "Per sota dels 20 kbit/s l'embolcall pesa més que el contingut: cada paquet "
                 "porta 28 bytes de capçaleres IP i UDP, i abaixar més el còdec deixa de servir. "
                 "Per això s'agrupen diverses trames en un paquet: amb 40 ms de paquet s'estalvia "
                 "el 18% de l'amplada de banda, i el retard afegit no se sent.",
    "pb2_4n": "Els perfils comprimits arriben a ocupar vint-i-cinc vegades menys, però deixa'ls "
              "per després: primer comprova que l'enllaç aguanta així. La taula de sota diu què "
              "costa cadascun.",
    "g5_c": "El relé descarta qui es queda callat quinze segons. Si passa contínuament, la xarxa "
            "està perdent paquets: passa al perfil Veu, que ocupa vint-i-cinc vegades menys que "
            "el PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — els valors indicats són els predeterminats "
             "dels dos programes a 17 d'agost de 2026; les amplades de banda són mesurades, no "
             "estimades.",
}

G5["da"] = {
    "banda_cwkey": "2,4 kbit/s",
    "meta_proto": "Decolink · protokol v3",
    "meta_data": "17. august 2026",
    "h_prof": "Hvor meget båndbredde det bruger",
    "prof_p": "Profilen vælges i Decolink og gælder hele forbindelsen. Mellem den første og den "
              "sidste er der tre størrelsesordener, og det er ikke en detalje: det afgør, hvilke "
              "forbindelser der overhovedet er mulige.",
    "prof_th1": "Profil", "prof_th2": "Båndbredde", "prof_th3": "Hvornår",
    "pr1": "PCM 48 kHz", "pr1_q": "Virker med alt, ingen komprimering. Udgangspunktet: 364 MB i "
                                  "timen.",
    "pr2": "PCM 12 kHz", "pr2_q": "Rigeligt til SSB, der kun fylder 2,7 kHz. Lyder det for "
                                  "hurtigt på telefonen, så gå tilbage til 48.",
    "pr3": "Tale (Opus)", "pr3_q": "Fone: femogtyve gange mindre end PCM. Kræver en opdateret "
                                   "telefon i den anden ende.",
    "pr4": "CW (Opus)", "pr4_q": "Smalbåndet telegrafi: fyrre gange mindre end PCM.",
    "pr5": "Digitale", "pr5_q": "Komprimeret uden at miste en bit: FT8 og lignende dekoder som "
                                "på PCM, for det er det samme signal.",
    "pr6": "CW-nøgling", "pr6_q": "Kun nøgleøjeblikkene. Hele konteksten går tabt — QSB, QRM, "
                                  "dem der kalder ved siden af frekvensen — til gengæld kommer "
                                  "det igennem alt.",
    "prof_fine": "Under 20 kbit/s vejer indpakningen mere end indholdet: hver pakke bærer 28 byte "
                 "IP- og UDP-headere, og at sænke codec'et yderligere hjælper ikke længere. "
                 "Derfor samles flere frames i én pakke: ved 40 ms pr. pakke sparer man 18% af "
                 "båndbredden, og den ekstra forsinkelse kan ikke høres.",
    "pb2_4n": "De komprimerede profiler kommer helt ned på en femogtyvendedel, men gem dem til "
              "senere: se først, om forbindelsen holder sådan. Tabellen nedenfor siger, hvad hver "
              "enkelt koster.",
    "g5_c": "Relæet smider den ud, der er tavs i femten sekunder. Sker det hele tiden, taber "
            "nettet pakker: skift til profilen Tale, der fylder femogtyve gange mindre end PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — de nævnte værdier er de to programmers "
             "standardindstillinger pr. 17. august 2026; båndbredderne er målt, ikke skønnet.",
}

G5["hu"] = {
    "banda_cwkey": "2,4 kbit/s",
    "meta_proto": "Decolink · v3 protokoll",
    "meta_data": "2026. augusztus 17.",
    "h_prof": "Mennyi sávszélességet foglal",
    "prof_p": "A profilt a Decolinkben választod, és az egész kapcsolatra érvényes. Az első és "
              "az utolsó között három nagyságrend a különbség, és ez nem részletkérdés: ez dönti "
              "el, mely kapcsolatok lehetségesek egyáltalán.",
    "prof_th1": "Profil", "prof_th2": "Sávszélesség", "prof_th3": "Mikor",
    "pr1": "PCM 48 kHz", "pr1_q": "Mindennel működik, tömörítés nélkül. Ez a kiindulópont: "
                                  "óránként 364 MB.",
    "pr2": "PCM 12 kHz", "pr2_q": "Bőven elég az SSB-hez, amely csak 2,7 kHz-et foglal. Ha a "
                                  "telefonon felgyorsítva szól, térj vissza 48-ra.",
    "pr3": "Beszéd (Opus)", "pr3_q": "Fónia: huszonötször kevesebb, mint a PCM. A túloldalon "
                                     "frissített telefon kell hozzá.",
    "pr4": "CW (Opus)", "pr4_q": "Keskeny sávú távíró: negyvenszer kevesebb, mint a PCM.",
    "pr5": "Digitális", "pr5_q": "Bitpontosan tömörítve: az FT8 és társai ugyanúgy dekódolnak, "
                                 "mint PCM-en, mert ugyanaz a jel.",
    "pr6": "CW-billentyűzés", "pr6_q": "Csak a billentyűzés pillanatai. Elvész a teljes környezet "
                                       "— QSB, QRM, aki a frekvencia mellett hív —, cserébe "
                                       "bármin átmegy.",
    "prof_fine": "20 kbit/s alatt a csomagolás többet nyom, mint a tartalom: minden csomag 28 "
                 "bájt IP- és UDP-fejlécet visz, és a kodek további csökkentése már nem segít. "
                 "Ezért kerül több keret egy csomagba: 40 ms-os csomagnál 18% sávszélesség "
                 "spórolható, és a többletkésleltetés nem hallható.",
    "pb2_4n": "A tömörített profilok akár huszonötödére csökkentik a forgalmat, de tartogasd "
              "őket későbbre: előbb győződj meg róla, hogy a kapcsolat így elbírja. Az alábbi "
              "táblázat megmondja, melyik mennyibe kerül.",
    "g5_c": "A relé kidobja azt, aki tizenöt másodpercig néma marad. Ha folyton előfordul, a "
            "hálózat csomagokat veszít: válts a Beszéd profilra, amely huszonötször kevesebbet "
            "foglal, mint a PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — a megadott értékek a két program "
             "alapbeállításai 2026. augusztus 17-én; a sávszélességek mértek, nem becsültek.",
}

G5["ro"] = {
    "banda_cwkey": "2,4 kbit/s",
    "meta_proto": "Decolink · protocol v3",
    "meta_data": "17 august 2026",
    "h_prof": "Cât consumă",
    "prof_p": "Profilul se alege în Decolink și e valabil pentru toată legătura. Între primul și "
              "ultimul sunt trei ordine de mărime, și nu e un amănunt: el hotărăște ce legături "
              "sunt cu putință.",
    "prof_th1": "Profil", "prof_th2": "Bandă", "prof_th3": "Când",
    "pr1": "PCM 48 kHz", "pr1_q": "Merge cu orice, fără compresie. E punctul de plecare: 364 MB "
                                  "pe oră.",
    "pr2": "PCM 12 kHz", "pr2_q": "Mai mult decât suficient pentru un SSB, care ocupă 2,7 kHz. "
                                  "Dacă telefonul îl aude accelerat, revino la 48.",
    "pr3": "Voce (Opus)", "pr3_q": "Fonie: de douăzeci și cinci de ori mai puțin decât PCM. "
                                   "Necesită un telefon actualizat de cealaltă parte.",
    "pr4": "CW (Opus)", "pr4_q": "Telegrafie în bandă îngustă: de patruzeci de ori mai puțin "
                                 "decât PCM.",
    "pr5": "Digitale", "pr5_q": "Comprimat fără a pierde un bit: FT8 și celelalte decodează ca "
                                "pe PCM, fiindcă e același semnal.",
    "pr6": "Manipulare CW", "pr6_q": "Doar momentele manipulatorului. Se pierde tot contextul — "
                                     "QSB, QRM, cine cheamă lângă frecvență — dar trece prin "
                                     "orice.",
    "prof_fine": "Sub 20 kbit/s ambalajul cântărește mai mult decât conținutul: fiecare pachet "
                 "duce 28 de octeți de antete IP și UDP, iar coborârea codecului nu mai ajută. "
                 "De aceea se grupează mai multe cadre într-un pachet: la 40 ms de pachet se "
                 "economisește 18% din bandă, iar întârzierea în plus nu se simte.",
    "pb2_4n": "Profilurile comprimate ajung să ocupe de douăzeci și cinci de ori mai puțin, dar "
              "păstrează-le pentru mai târziu: întâi verifică dacă legătura ține așa. Tabelul de "
              "mai jos spune cât costă fiecare.",
    "g5_c": "Releul îl scoate afară pe cine tace cincisprezece secunde. Dacă se întâmplă mereu, "
            "rețeaua pierde pachete: treci la profilul Voce, care ocupă de douăzeci și cinci de "
            "ori mai puțin decât PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — valorile indicate sunt cele implicite ale "
             "celor două programe la 17 august 2026; benzile sunt măsurate, nu estimate.",
}

G5["lv"] = {
    "banda_cwkey": "2,4 kbit/s",
    "meta_proto": "Decolink · protokols v3",
    "meta_data": "2026. gada 17. augusts",
    "h_prof": "Cik daudz joslas platuma aizņem",
    "prof_p": "Profilu izvēlas Decolink, un tas attiecas uz visu savienojumu. Starp pirmo un "
              "pēdējo ir trīs kārtas, un tas nav sīkums: tas nosaka, kuri savienojumi vispār ir "
              "iespējami.",
    "prof_th1": "Profils", "prof_th2": "Josla", "prof_th3": "Kad",
    "pr1": "PCM 48 kHz", "pr1_q": "Der visam, bez saspiešanas. Tas ir sākumpunkts: 364 MB stundā.",
    "pr2": "PCM 12 kHz", "pr2_q": "Pilnīgi pietiek SSB, kas aizņem tikai 2,7 kHz. Ja telefonā "
                                  "skan paātrināti, atgriezies uz 48.",
    "pr3": "Balss (Opus)", "pr3_q": "Fonija: divdesmit piecas reizes mazāk nekā PCM. Otrā pusē "
                                    "vajadzīgs atjaunināts telefons.",
    "pr4": "CW (Opus)", "pr4_q": "Šaurjoslas telegrāfs: četrdesmit reizes mazāk nekā PCM.",
    "pr5": "Digitālie", "pr5_q": "Saspiests, nezaudējot nevienu bitu: FT8 un tamlīdzīgie dekodē "
                                 "tāpat kā uz PCM, jo tas ir tas pats signāls.",
    "pr6": "CW manipulācija", "pr6_q": "Tikai manipulatora brīži. Zūd viss konteksts — QSB, QRM, "
                                       "kas sauc blakus frekvencei —, toties tas iziet cauri "
                                       "jebkam.",
    "prof_fine": "Zem 20 kbit/s iesaiņojums sver vairāk nekā saturs: katra pakete nes 28 baitus "
                 "IP un UDP galvenu, un kodeka tālāka samazināšana vairs nepalīdz. Tāpēc vairāki "
                 "kadri tiek grupēti vienā paketē: ar 40 ms paketi ietaupa 18% joslas platuma, "
                 "un papildu aizturi nav dzirdama.",
    "pb2_4n": "Saspiestie profili nokāpj līdz divdesmit piecām reizēm mazāk, bet atstāj tos "
              "vēlākam: vispirms pārliecinies, ka savienojums tā notur. Tabula zemāk saka, cik "
              "katrs maksā.",
    "g5_c": "Relejs izmet to, kas piecpadsmit sekundes klusē. Ja tas notiek nemitīgi, tīkls "
            "zaudē paketes: pārej uz profilu Balss, kas aizņem divdesmit piecas reizes mazāk "
            "nekā PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — norādītās vērtības ir abu programmu "
             "noklusējumi 2026. gada 17. augustā; joslas platumi ir mērīti, nevis lēsti.",
}

G5["ru"] = {
    "banda_cwkey": "2,4 kbit/s",
    "meta_proto": "Decolink · протокол v3",
    "meta_data": "17 августа 2026",
    "h_prof": "Сколько полосы занимает",
    "prof_p": "Профиль выбирается в Decolink и действует на всю связь. Между первым и последним "
              "три порядка величины, и это не мелочь: именно он решает, какие соединения вообще "
              "возможны.",
    "prof_th1": "Профиль", "prof_th2": "Полоса", "prof_th3": "Когда",
    "pr1": "PCM 48 кГц", "pr1_q": "Работает со всем, без сжатия. Это точка отсчёта: 364 МБ в час.",
    "pr2": "PCM 12 кГц", "pr2_q": "С запасом хватает для SSB, который занимает 2,7 кГц. Если на "
                                  "телефоне звук ускорен, вернитесь на 48.",
    "pr3": "Голос (Opus)", "pr3_q": "Телефония: в двадцать пять раз меньше PCM. На той стороне "
                                    "нужна обновлённая программа.",
    "pr4": "CW (Opus)", "pr4_q": "Узкополосный телеграф: в сорок раз меньше PCM.",
    "pr5": "Цифровые", "pr5_q": "Сжатие без потери единого бита: FT8 и прочие декодируют так же, "
                                "как на PCM, — это тот же самый сигнал.",
    "pr6": "Манипуляция CW", "pr6_q": "Только моменты нажатия ключа. Теряется весь контекст — "
                                      "QSB, QRM, кто зовёт рядом по частоте, — зато проходит "
                                      "через что угодно.",
    "prof_fine": "Ниже 20 кбит/с обёртка весит больше содержимого: каждый пакет несёт 28 байт "
                 "заголовков IP и UDP, и дальше понижать кодек уже бесполезно. Поэтому несколько "
                 "кадров складывают в один пакет: при 40 мс на пакет экономится 18% полосы, а "
                 "добавленная задержка не слышна.",
    "pb2_4n": "Сжатые профили доходят до двадцати пяти раз меньше, но отложите их на потом: "
              "сначала убедитесь, что связь держится и так. Таблица ниже говорит, во сколько "
              "обходится каждый.",
    "g5_c": "Ретранслятор отбрасывает того, кто молчит пятнадцать секунд. Если это повторяется "
            "постоянно, сеть теряет пакеты: перейдите на профиль Голос, который занимает в "
            "двадцать пять раз меньше PCM.",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — приведённые значения — заводские настройки "
             "обеих программ на 17 августа 2026 года; полосы измерены, а не оценены.",
}

G5["ja"] = {
    "banda_cwkey": "2.4 kbit/s",
    "meta_proto": "Decolink · プロトコル v3",
    "meta_data": "2026年8月17日",
    "h_prof": "どれくらいの帯域を使うか",
    "prof_p": "プロファイルは Decolink で選び、接続全体に適用されます。最初と最後では 3 桁の差があり、"
              "これは細かい話ではありません。どんな接続が成り立つかを決めるのはここです。",
    "prof_th1": "プロファイル", "prof_th2": "帯域", "prof_th3": "使いどころ",
    "pr1": "PCM 48 kHz", "pr1_q": "すべてと互換、圧縮なし。基準となる設定で、1 時間あたり 364 MB。",
    "pr2": "PCM 12 kHz", "pr2_q": "帯域 2.7 kHz の SSB には十分すぎます。"
                                  "スマートフォンで速く聞こえる場合は 48 に戻してください。",
    "pr3": "音声 (Opus)", "pr3_q": "フォーン: PCM の 25 分の 1。相手側に更新されたプログラムが必要です。",
    "pr4": "CW (Opus)", "pr4_q": "狭帯域の電信: PCM の 40 分の 1。",
    "pr5": "デジタル", "pr5_q": "1 ビットも失わない圧縮。FT8 なども PCM と同じようにデコードできます。"
                              "同じ信号だからです。",
    "pr6": "CW キーイング", "pr6_q": "打鍵のタイミングだけ。周囲の状況 (QSB、QRM、周波数の外で呼ぶ局) は"
                                  "すべて失われますが、どんな回線でも通ります。",
    "prof_fine": "20 kbit/s を下回ると、中身より包みのほうが重くなります。パケットごとに IP と UDP の"
                 "ヘッダーが 28 バイト付くため、コーデックをさらに下げても効果がなくなるのです。"
                 "そこで複数のフレームを 1 つのパケットにまとめます。パケット長 40 ms なら帯域が "
                 "18% 減り、増える遅延は感じられません。",
    "pb2_4n": "圧縮プロファイルは最大で 25 分の 1 まで下がりますが、まずは後回しに。"
              "この設定で接続が保つことを先に確かめてください。下の表に各プロファイルの負担があります。",
    "g5_c": "リレーは 15 秒間無音の相手を切り離します。何度も起きるならネットワークがパケットを"
            "落としています。PCM の 25 分の 1 で済む音声プロファイルに切り替えてください。",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — 記載の値は 2026年8月17日時点の両プログラムの"
             "初期値です。帯域は推定ではなく実測値です。",
}

G5["zh"] = {
    "banda_cwkey": "2.4 kbit/s",
    "meta_proto": "Decolink · v3 协议",
    "meta_data": "2026 年 8 月 17 日",
    "h_prof": "占用多少带宽",
    "prof_p": "配置在 Decolink 中选择，对整条链路生效。第一项和最后一项之间相差三个数量级，"
              "这不是细节：它决定了哪些连接根本能不能成立。",
    "prof_th1": "配置", "prof_th2": "带宽", "prof_th3": "适用场景",
    "pr1": "PCM 48 kHz", "pr1_q": "与所有程序兼容，不压缩。这是基准：每小时 364 MB。",
    "pr2": "PCM 12 kHz", "pr2_q": "对只占 2.7 kHz 的 SSB 绰绰有余。"
                                  "如果手机听起来变快，请改回 48。",
    "pr3": "语音 (Opus)", "pr3_q": "话务：只有 PCM 的二十五分之一。对端需要已更新的程序。",
    "pr4": "CW (Opus)", "pr4_q": "窄带电报：只有 PCM 的四十分之一。",
    "pr5": "数字模式", "pr5_q": "无损压缩：FT8 等模式的解码效果与 PCM 一致，因为就是同一个信号。",
    "pr6": "CW 键控", "pr6_q": "只传键控的时刻。全部环境信息都会失去 —— QSB、QRM、"
                              "在频率旁呼叫的人 —— 但它能通过任何链路。",
    "prof_fine": "低于 20 kbit/s 时，外包装比内容还重：每个数据包都要带 28 字节的 IP 和 UDP 包头，"
                 "再压低编码器已经没有意义。因此会把多帧合并成一个包：包长 40 ms 可省下 18% 的带宽，"
                 "而多出的延迟察觉不到。",
    "pb2_4n": "压缩配置最低可以降到二十五分之一，但先放一放：先确认这样连接能稳住。"
              "下面的表格列出了每种配置的代价。",
    "g5_c": "中继会踢掉沉默十五秒的一方。如果反复出现，说明网络在丢包："
            "改用语音配置，它只占 PCM 的二十五分之一。",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC —— 文中数值为两个程序在 "
             "2026 年 8 月 17 日的默认设置；带宽为实测值，而非估算。",
}

G5["zh_TW"] = {
    "banda_cwkey": "2.4 kbit/s",
    "meta_proto": "Decolink · v3 協定",
    "meta_data": "2026 年 8 月 17 日",
    "h_prof": "占用多少頻寬",
    "prof_p": "設定檔在 Decolink 中選擇，對整條連線生效。第一項和最後一項之間相差三個數量級，"
              "這不是細節：它決定了哪些連線根本能不能成立。",
    "prof_th1": "設定檔", "prof_th2": "頻寬", "prof_th3": "適用場景",
    "pr1": "PCM 48 kHz", "pr1_q": "與所有程式相容，不壓縮。這是基準：每小時 364 MB。",
    "pr2": "PCM 12 kHz", "pr2_q": "對只占 2.7 kHz 的 SSB 綽綽有餘。"
                                  "如果手機聽起來變快，請改回 48。",
    "pr3": "語音 (Opus)", "pr3_q": "話務：只有 PCM 的二十五分之一。對端需要已更新的程式。",
    "pr4": "CW (Opus)", "pr4_q": "窄頻電報：只有 PCM 的四十分之一。",
    "pr5": "數位模式", "pr5_q": "無損壓縮：FT8 等模式的解碼效果與 PCM 一致，因為就是同一個訊號。",
    "pr6": "CW 鍵控", "pr6_q": "只傳鍵控的時刻。全部環境資訊都會失去 —— QSB、QRM、"
                              "在頻率旁呼叫的人 —— 但它能通過任何連線。",
    "prof_fine": "低於 20 kbit/s 時，外包裝比內容還重：每個封包都要帶 28 位元組的 IP 和 UDP 標頭，"
                 "再壓低編碼器已經沒有意義。因此會把多幀合併成一個封包：封包長 40 ms 可省下 18% 的"
                 "頻寬，而多出的延遲察覺不到。",
    "pb2_4n": "壓縮設定檔最低可以降到二十五分之一，但先放一放：先確認這樣連線能穩住。"
              "下面的表格列出了每種設定檔的代價。",
    "g5_c": "中繼會踢掉沉默十五秒的一方。如果反覆出現，表示網路在掉封包："
            "改用語音設定檔，它只占 PCM 的二十五分之一。",
    "piede": "Decodium 4 Mobile · Decolink · IU8LMC —— 文中數值為兩個程式在 "
             "2026 年 8 月 17 日的預設設定；頻寬為實測值，而非估算。",
}
