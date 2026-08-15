<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="da">
<context>
    <name>Client</name>
    <message>
        <location filename="../main.cpp" line="548" />
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — radioen på Decodium Mobile</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="555" />
        <source>LAN diretta</source>
        <translation>Direkte LAN</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="556" />
        <source>Relay + stazione</source>
        <translation>Relæ + station</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="557" />
        <source>Il telefono chiama casa</source>
        <translation>Telefonen ringer hjem</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="558" />
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
        <location filename="../main.cpp" line="565" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>Telefonens IP eller relæ-vært</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="569" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(log ind for at vælge station)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="593" />
        <source>48 kHz</source>
        <translation>48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="594" />
        <source>24 kHz</source>
        <translation>24 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="595" />
        <source>12 kHz</source>
        <translation>12 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="596" />
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
        <location filename="../main.cpp" line="606" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="607" />
        <source>Voce (Opus)</source>
        <translation>Tale (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="608" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="609" />
        <source>Digitali senza perdite</source>
        <translation>Digitale modes, tabsfri</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="610" />
        <source>CW a tasto</source>
        <translation>Kun CW-nøgling</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="611" />
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
        <location filename="../main.cpp" line="622" />
        <source>20 ms</source>
        <translation>20 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="623" />
        <source>40 ms</source>
        <translation>40 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="624" />
        <source>60 ms</source>
        <translation>60 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="626" />
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
        <location filename="../main.cpp" line="639" />
        <source>Audio radio</source>
        <translation>Radiolyd</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="640" />
        <source>Modalità</source>
        <translation>Tilstand</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="641" />
        <source>Host</source>
        <translation>Vært</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="648" />
        <source>stazione</source>
        <translation>station</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="652" />
        <source>Porta</source>
        <translation>Port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="660" />
        <source>Profilo</source>
        <translation>Profil</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="661" />
        <source>Campionamento</source>
        <translation>Samplerate</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="662" />
        <source>Pacchetti da</source>
        <translation>Pakkelængde</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="668" />
        <location filename="../main.cpp" line="674" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  Avancerede indstillinger</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="673" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  Avancerede indstillinger</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="680" />
        <location filename="../main.cpp" line="2067" />
        <source>Avvia</source>
        <translation>Start</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="686" />
        <location filename="../main.cpp" line="2069" />
        <source>fermo</source>
        <translation>stoppet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="689" />
        <location filename="../main.cpp" line="1888" />
        <source>—</source>
        <translation>—</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="699" />
        <source>Yaesu — comandi nativi</source>
        <translation>Yaesu — comandi nativi</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="700" />
        <source>Icom IC-7300 — CI-V nativo</source>
        <translation>Icom IC-7300 — CI-V nativo</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="716" />
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
        <location filename="../main.cpp" line="725" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>vært:port for programmet der har radioen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="727" />
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
        <location filename="../main.cpp" line="740" />
        <source>115200</source>
        <translation>115200</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="742" />
        <source>7</source>
        <translation>7</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="743" />
        <location filename="../main.cpp" line="744" />
        <source>8</source>
        <translation>8</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="746" />
        <source>nessuna</source>
        <translation>ingen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="747" />
        <source>pari</source>
        <translation>lige</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="748" />
        <source>dispari</source>
        <translation>ulige</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="750" />
        <source>1</source>
        <translation>1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="751" />
        <source>2</source>
        <translation>2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="754" />
        <source>nessuno</source>
        <translation>ingen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="755" />
        <source>RTS/CTS</source>
        <translation>RTS/CTS</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="756" />
        <source>XON/XOFF</source>
        <translation>XON/XOFF</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="758" />
        <source>Servi il CAT al telefono</source>
        <translation>Stil CAT til rådighed for telefonen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="759" />
        <location filename="../main.cpp" line="1238" />
        <source>CAT spento</source>
        <translation>CAT slukket</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="762" />
        <source>(nessuna: non trasmettere)</source>
        <translation>(ingen: send ikke)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="770" />
        <source>Radio / protocollo</source>
        <translation>Radio / protokol</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="771" />
        <source>Indirizzo CI-V</source>
        <translation>CI-V-adresse</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="772" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>Adressen som radioen svarer på over CI-V-bussen.
IC-7300: 0x94 (fabriksindstilling). Er den ændret i radioens
menuer, skal samme værdi skrives her.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="777" />
        <source>Audio al rig</source>
        <translation>Lyd til radioen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="784" />
        <source>Porta rig</source>
        <translation>Radioens port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="789" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="794" />
        <source>Velocità</source>
        <translation>Hastighed</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="801" />
        <source>dati</source>
        <translation>data</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="805" />
        <source>parità</source>
        <translation>paritet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="809" />
        <source>stop</source>
        <translation>stop</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="813" />
        <source>Seriale</source>
        <translation>Seriel</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="814" />
        <source>Handshake</source>
        <translation>Handshake</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="843" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>loginserver (f.eks. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="845" />
        <source>la tua email</source>
        <translation>din e-mail</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="848" />
        <source>password</source>
        <translation>adgangskode</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="849" />
        <source>ricorda la password</source>
        <translation>husk adgangskoden</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="850" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>Gemmes i klartekst i Windows-indstillingerne: kun værd på en computer du stoler på.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="852" />
        <source>Accedi</source>
        <translation>Log ind</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="853" />
        <source>non collegato</source>
        <translation>ikke forbundet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="863" />
        <source>Server</source>
        <translation>Server</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="869" />
        <source>Accesso</source>
        <translation>Login</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="891" />
        <source>COLLEGAMENTO</source>
        <translation>FORBINDELSE</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="899" />
        <source>RADIO E CAT</source>
        <translation>RADIO OG CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="922" />
        <source>livello audio</source>
        <translation>lydniveau</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="977" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>sampling ved %1 kHz: lyder det hurtigt på telefonen, gå tilbage til 48</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1060" />
        <source>IP del telefono sulla rete locale</source>
        <translation>telefonens IP på det lokale net</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1063" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>relæ-vært (f.eks. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1066" />
        <source>(il telefono chiama questa porta)</source>
        <translation>(telefonen ringer til denne port)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1077" />
        <source>manca il server di accesso</source>
        <translation>loginserveren mangler</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1079" />
        <source>servono email e password</source>
        <translation>e-mail og adgangskode kræves</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1101" />
        <source>accesso in corso…</source>
        <translation>logger ind…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1121" />
        <source>risposta incomprensibile dal server</source>
        <translation>uforståeligt svar fra serveren</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1158" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — station %2, som %3%4</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1181" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1217" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>loginoplysninger udløbet: logger ind igen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1220" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>ikke logget ind: tryk Log ind og derefter Start</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1250" />
        <source>nessuna porta seriale</source>
        <translation>ingen seriel port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1259" />
        <source>indirizzo CI-V non valido</source>
        <translation>ugyldig CI-V-adresse</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1268" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>adressen på programmet der har radioen mangler</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1280" />
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>TCP-port %1 er den samme, du forbinder til: skift en af dem</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1296" />
        <source>%1 non risponde: %2</source>
        <translation>%1 svarer ikke: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1309" />
        <source>%1 non si apre: %2</source>
        <translation>%1 kan ikke åbnes: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1317" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>TCP-port %1 optaget (kører rigctld allerede?)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1345" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>radio: %1 MHz  %2   (TCP %3, og via lydkanalen)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1375" />
        <source>telefono connesso da %1:%2</source>
        <translation>telefon forbundet fra %1:%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1425" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>loginoplysninger skal fornys: logger ind igen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1429" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>relæet afviste forbindelsen: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1437" />
        <source>il telefono è entrato nella stanza</source>
        <translation>telefonen er kommet ind i rummet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1439" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>registreret på relæet som %1 (%2)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1546" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>telefonen læser grupperede pakker: reduceret båndbredde</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1568" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>profil ønsket af telefonen: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1862" />
        <location filename="../main.cpp" line="2043" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>%1 understøtter ikke 48 kHz mono 16 bit</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1870" />
        <source>trasmissione dal telefono in corso</source>
        <translation>sender fra telefonen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1881" />
        <source>trasmissione finita</source>
        <translation>udsendelse afsluttet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1932" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>registreret, men der er ingen andre i stationen: telefonen er ikke kommet ind endnu</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1935" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>bemærk: profil %1, men telefonen har ikke bekræftet at den kan læse det — hører du intet, skift til PCM 48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1949" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>telefonen kan ikke længere nås — venter på at den ringer igen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1991" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Opus starter ikke (%1): bliver på PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2007" />
        <source>manca l'host di destinazione</source>
        <translation>målværten mangler</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2010" />
        <source>nome non risolto: %1</source>
        <translation>navnet kunne ikke slås op: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2015" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>log ind først: relæet accepterer ikke forbindelser uden loginoplysninger</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2025" />
        <source>porta %1 non disponibile</source>
        <translation>port %1 er ikke tilgængelig</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2039" />
        <source>nessun ingresso audio</source>
        <translation>ingen lydindgang</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2048" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>kan ikke åbne lydindgangen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2052" />
        <source>Ferma</source>
        <translation>Stop</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2056" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>lytter på port %1 — venter på telefonen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2107" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>profil sat tilbage til PCM 48 kHz: komprimerede profiler kræver en opdateret telefon</translation>
    </message>
</context>
</TS>