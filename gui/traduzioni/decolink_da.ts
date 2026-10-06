<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="da">
<context>
    <name>Client</name>
    <message>
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — radioen på Decodium Mobile</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="753" />
        <source>LAN diretta</source>
        <translation>Direkte LAN</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="754" />
        <source>Relay + stazione</source>
        <translation>Relæ + station</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="755" />
        <source>Il telefono chiama casa</source>
        <translation>Telefonen ringer hjem</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="756" />
        <source>LAN diretta — il telefono è sulla stessa rete: gli si manda l'audio all'indirizzo
Relay + stazione — funziona ovunque, anche su dati mobili: PC e telefono
   escono entrambi verso il relay, quindi non c'è nessun router da configurare
Il telefono chiama casa — porta inoltrata sul router e nome DynDNS</source>
        <translation>Direkte LAN — telefonen er på samme net: lyden sendes til dens adresse
Relæ + station — virker overalt, også på mobildata: pc og telefon går
   begge ud til relæet, så der er ingen router at sætte op
Telefonen ringer hjem — videresendt port på routeren og et DynDNS-navn</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="763" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>Telefonens IP eller relæ-vært</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="767" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(log ind for at vælge station)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="791" />
        <source>48 kHz</source>
        <translation>48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="792" />
        <source>24 kHz</source>
        <translation>24 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="793" />
        <source>12 kHz</source>
        <translation>12 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="794" />
        <source>Quanti campioni al secondo mandare.
48 kHz — 808 kbit/s, 364 MB l'ora: sicuro con qualunque programma
24 kHz — 424 kbit/s, 191 MB l'ora
12 kHz — 232 kbit/s, 104 MB l'ora: basta e avanza per un SSB,
che di banda ne occupa 2,7 kHz.

Se il telefono lo sente accelerato, non legge la frequenza
dichiarata: torna a 48 kHz.</source>
        <translation>Hvor mange samples i sekundet der sendes.
48 kHz — 808 kbit/s, 364 MB i timen: sikkert med ethvert program
24 kHz — 424 kbit/s, 191 MB i timen
12 kHz — 232 kbit/s, 104 MB i timen: rigeligt til SSB,
der kun fylder 2,7 kHz.

Lyder det for hurtigt på telefonen, ignorerer den den angivne
samplerate: gå tilbage til 48 kHz.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="804" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="805" />
        <source>Voce (Opus)</source>
        <translation>Tale (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="806" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="807" />
        <source>Digitali senza perdite</source>
        <translation>Digitale modes, tabsfri</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="808" />
        <source>CW a tasto</source>
        <translation>Kun CW-nøgling</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="809" />
        <source>PCM — compatibile con tutti, nessuna compressione
Voce — Opus a 32 kbit/s: serve un programma aggiornato dall'altra parte
CW — Opus a banda stretta, 20 kbit/s
Digitali — compresso senza perdere un bit, 146 kbit/s
CW a tasto — solo il ritmo del tasto, 2,4 kbit/s: si perde
tutto il contesto (QSB, QRM, chi chiama fuori nota)</source>
        <translation>PCM — virker med alt, ingen komprimering
Tale — Opus ved 32 kbit/s: kræver et opdateret program i den anden ende
CW — smalbåndet Opus, 20 kbit/s
Digitale — komprimeret uden at miste en bit, 146 kbit/s
CW-nøgling — kun rytmen, 2,4 kbit/s: hele konteksten går tabt
(QSB, QRM, dem der kalder ved siden af frekvensen)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="820" />
        <source>20 ms</source>
        <translation>20 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="821" />
        <source>40 ms</source>
        <translation>40 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="822" />
        <source>60 ms</source>
        <translation>60 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="824" />
        <source>Quanti frame mettere in un pacchetto: meno pacchetti, meno
intestazioni da pagare, ma un po' più di ritardo.
20 ms — latenza minima
40 ms — 18% di banda in meno, ritardo impercettibile
60 ms — 24% in meno, per reti a consumo</source>
        <translation>Hvor mange frames der lægges i én pakke: færre pakker betyder færre
headere at betale for, men lidt mere forsinkelse.
20 ms — laveste latenstid
40 ms — 18% mindre båndbredde, umærkelig forsinkelse
60 ms — 24% mindre, til forbindelser med datagrænse</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="837" />
        <source>Audio radio</source>
        <translation>Radiolyd</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="838" />
        <source>Modalità</source>
        <translation>Tilstand</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="839" />
        <source>Host</source>
        <translation>Vært</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="846" />
        <source>stazione</source>
        <translation>station</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="850" />
        <source>Porta</source>
        <translation>Port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="858" />
        <source>Profilo</source>
        <translation>Profil</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="859" />
        <source>Campionamento</source>
        <translation>Samplerate</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="860" />
        <source>Pacchetti da</source>
        <translation>Pakkelængde</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="866" />
        <location filename="../main.cpp" line="872" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  Avancerede indstillinger</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="871" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  Avancerede indstillinger</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="878" />
        <location filename="../main.cpp" line="2431" />
        <location filename="../main.cpp" line="2759" />
        <source>Avvia</source>
        <translation>Start</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="888" />
        <source>Potenza, ROS e ALC letti dalla radio.
Compaiono mentre trasmetti, se la radio li espone.</source>
        <translation>Effekt, SWR og ALC aflæst fra radioen.
De vises, mens du sender, hvis radioen giver dem.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="890" />
        <location filename="../main.cpp" line="2433" />
        <source>fermo</source>
        <translation>stoppet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="896" />
        <location filename="../main.cpp" line="2251" />
        <source>—</source>
        <translation>—</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="906" />
        <source>Yaesu — comandi nativi</source>
        <translation>Yaesu — comandi nativi</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="907" />
        <source>Icom IC-7300 — CI-V nativo</source>
        <translation>Icom IC-7300 — CI-V nativo</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="923" />
        <source>Hamlib %1 — %2 modelli riconosciuti.
I primi due sono i protocolli scritti dentro Decolink;
gli altri passano da Hamlib, la stessa libreria che usa
Decodium sul desktop.</source>
        <translation>Hamlib %1 — %2 genkendte modeller.
De to første er protokollerne skrevet i Decolink;
de øvrige går gennem Hamlib, samme bibliotek som Decodium
bruger på computeren.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="932" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>vært:port for programmet der har radioen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="934" />
        <source>Indirizzo del programma che tiene la porta seriale.
rigctld e i programmi compatibili: localhost:4532
FLRig: localhost:12345

Serve quando la COM è già occupata da un altro programma:
la porta seriale è di chi la apre per primo, e in due non
ci si sta.</source>
        <translation>Adressen på programmet der har den serielle port.
rigctld og kompatible programmer: localhost:4532
FLRig: localhost:12345

Bruges når COM-porten allerede er optaget af et andet program:
den serielle port tilhører den der åbner den først, og der er
ikke plads til to.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="947" />
        <source>115200</source>
        <translation>115200</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="949" />
        <source>7</source>
        <translation>7</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="950" />
        <location filename="../main.cpp" line="951" />
        <source>8</source>
        <translation>8</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="953" />
        <source>nessuna</source>
        <translation>ingen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="954" />
        <source>pari</source>
        <translation>lige</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="955" />
        <source>dispari</source>
        <translation>ulige</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="957" />
        <source>1</source>
        <translation>1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="958" />
        <source>2</source>
        <translation>2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="961" />
        <source>nessuno</source>
        <translation>ingen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="962" />
        <source>RTS/CTS</source>
        <translation>RTS/CTS</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="963" />
        <source>XON/XOFF</source>
        <translation>XON/XOFF</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="965" />
        <source>Servi il CAT al telefono</source>
        <translation>Stil CAT til rådighed for telefonen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="966" />
        <location filename="../main.cpp" line="1532" />
        <source>CAT spento</source>
        <translation>CAT slukket</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="969" />
        <source>(nessuna: non trasmettere)</source>
        <translation>(ingen: send ikke)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="977" />
        <source>Radio / protocollo</source>
        <translation>Radio / protokol</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="978" />
        <source>Indirizzo CI-V</source>
        <translation>CI-V-adresse</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="979" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>Adressen som radioen svarer på over CI-V-bussen.
IC-7300: 0x94 (fabriksindstilling). Er den ændret i radioens
menuer, skal samme værdi skrives her.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="984" />
        <source>Audio al rig</source>
        <translation>Lyd til radioen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="991" />
        <source>Porta rig</source>
        <translation>Radioens port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="996" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1001" />
        <source>Velocità</source>
        <translation>Hastighed</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1008" />
        <source>dati</source>
        <translation>data</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1012" />
        <source>parità</source>
        <translation>paritet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1016" />
        <source>stop</source>
        <translation>stop</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1020" />
        <source>Seriale</source>
        <translation>Seriel</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1021" />
        <source>Handshake</source>
        <translation>Handshake</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1050" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>loginserver (f.eks. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1052" />
        <source>la tua email</source>
        <translation>din e-mail</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1055" />
        <source>password</source>
        <translation>adgangskode</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1056" />
        <source>ricorda la password</source>
        <translation>husk adgangskoden</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1057" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>Gemmes i klartekst i Windows-indstillingerne: kun værd på en computer du stoler på.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1059" />
        <source>Accedi</source>
        <translation>Log ind</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1060" />
        <source>non collegato</source>
        <translation>ikke forbundet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1070" />
        <source>Server</source>
        <translation>Server</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1076" />
        <source>Accesso</source>
        <translation>Login</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1097" />
        <source>versione di Decolink</source>
        <translation>Decolink-version</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1105" />
        <source>lingua dell'interfaccia</source>
        <translation>sprog i brugerfladen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1128" />
        <source>COLLEGAMENTO</source>
        <translation>FORBINDELSE</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1136" />
        <source>RADIO E CAT</source>
        <translation>RADIO OG CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1159" />
        <source>livello audio</source>
        <translation>lydniveau</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1217" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>sampling ved %1 kHz: lyder det hurtigt på telefonen, gå tilbage til 48</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1321" />
        <location filename="../main.cpp" line="1329" />
        <source>Lingua</source>
        <translation>Sprog</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1322" />
        <source>Il collegamento è aperto: la lingua cambia alla prossima apertura del programma.</source>
        <translation>Forbindelsen er åben: sproget skifter, næste gang programmet startes.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1330" />
        <source>Decolink si riavvia per cambiare lingua. Procedo?</source>
        <translation>Decolink genstarter for at skifte sprog. Fortsæt?</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1354" />
        <source>IP del telefono sulla rete locale</source>
        <translation>telefonens IP på det lokale net</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1357" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>relæ-vært (f.eks. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1360" />
        <source>(il telefono chiama questa porta)</source>
        <translation>(telefonen ringer til denne port)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1371" />
        <source>manca il server di accesso</source>
        <translation>loginserveren mangler</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1373" />
        <source>servono email e password</source>
        <translation>e-mail og adgangskode kræves</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1395" />
        <source>accesso in corso…</source>
        <translation>logger ind…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1415" />
        <source>risposta incomprensibile dal server</source>
        <translation>uforståeligt svar fra serveren</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1452" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — station %2, som %3%4</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1475" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1511" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>loginoplysninger udløbet: logger ind igen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1514" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>ikke logget ind: tryk Log ind og derefter Start</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1544" />
        <source>nessuna porta seriale</source>
        <translation>ingen seriel port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1553" />
        <source>indirizzo CI-V non valido</source>
        <translation>ugyldig CI-V-adresse</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1562" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>adressen på programmet der har radioen mangler</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1579" />
        <source>qui c'è Decolink stesso: scegli il programma che tiene davvero la radio, o cambia la porta TCP qui sotto</source>
        <translation>det er Decolink selv: vælg det program, der faktisk har radioen, eller skift TCP-porten nedenfor</translation>
    </message>
    <message>
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>TCP-port %1 er den samme, du forbinder til: skift en af dem</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1595" />
        <source>%1 non risponde: %2</source>
        <translation>%1 svarer ikke: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1608" />
        <source>%1 non si apre: %2</source>
        <translation>%1 kan ikke åbnes: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1616" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>TCP-port %1 optaget (kører rigctld allerede?)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1664" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>radio: %1 MHz  %2   (TCP %3, og via lydkanalen)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1693" />
        <source>il programma che tiene la radio ha smesso di rispondere — riaccendi il CAT quando è tornato</source>
        <translation>programmet med radioen svarer ikke længere — tænd CAT igen, når det er tilbage</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1695" />
        <source>rig non risponde sulla seriale</source>
        <translation>radioen svarer ikke på den serielle port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1723" />
        <source>telefono connesso da %1:%2</source>
        <translation>telefon forbundet fra %1:%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1773" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>loginoplysninger skal fornys: logger ind igen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1777" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>relæet afviste forbindelsen: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1789" />
        <source>PTT: trasmette %1</source>
        <translation>PTT: %1 sender</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1792" />
        <source>PTT: libero</source>
        <translation>PTT: ledig</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1800" />
        <source>il telefono è entrato nella stanza</source>
        <translation>telefonen er kommet ind i rummet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1802" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>registreret på relæet som %1 (%2)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1909" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>telefonen læser grupperede pakker: reduceret båndbredde</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1931" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>profil ønsket af telefonen: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2225" />
        <location filename="../main.cpp" line="2406" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>%1 understøtter ikke 48 kHz mono 16 bit</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2233" />
        <source>trasmissione dal telefono in corso</source>
        <translation>sender fra telefonen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2244" />
        <source>trasmissione finita</source>
        <translation>udsendelse afsluttet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2295" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>registreret, men der er ingen andre i stationen: telefonen er ikke kommet ind endnu</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2298" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>bemærk: profil %1, men telefonen har ikke bekræftet at den kan læse det — hører du intet, skift til PCM 48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2312" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>telefonen kan ikke længere nås — venter på at den ringer igen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2354" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Opus starter ikke (%1): bliver på PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2370" />
        <source>manca l'host di destinazione</source>
        <translation>målværten mangler</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2373" />
        <source>nome non risolto: %1</source>
        <translation>navnet kunne ikke slås op: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2378" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>log ind først: relæet accepterer ikke forbindelser uden loginoplysninger</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2388" />
        <source>porta %1 non disponibile</source>
        <translation>port %1 er ikke tilgængelig</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2402" />
        <source>nessun ingresso audio</source>
        <translation>ingen lydindgang</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2411" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>kan ikke åbne lydindgangen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2415" />
        <source>Ferma</source>
        <translation>Stop</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2419" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>lytter på port %1 — venter på telefonen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2471" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>profil sat tilbage til PCM 48 kHz: komprimerede profiler kræver en opdateret telefon</translation>
    </message>
</context>
<context>
    <name>QObject</name>
    <message>
        <location filename="../hamlibrig.h" line="204" />
        <source>errore %1 di Hamlib</source>
        <translation>Hamlib-fejl %1</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="290" />
        <source>indirizzo vuoto</source>
        <translation>tom adresse</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="299" />
        <source>nessuna risposta da %1:%2</source>
        <translation>intet svar fra %1:%2</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="300" />
        <source>%1:%2 — %3</source>
        <translation>%1:%2 — %3</translation>
    </message>
</context>
</TS>