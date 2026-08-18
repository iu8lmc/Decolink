<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="lv">
<context>
    <name>Client</name>
    <message>
        <location filename="../main.cpp" line="714" />
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — radio Decodium Mobile lietotnē</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="721" />
        <source>LAN diretta</source>
        <translation>Tiešs LAN</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="722" />
        <source>Relay + stazione</source>
        <translation>Relejs + stacija</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="723" />
        <source>Il telefono chiama casa</source>
        <translation>Telefons zvana uz mājām</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="724" />
        <source>LAN diretta — il telefono è sulla stessa rete: gli si manda l'audio all'indirizzo
Relay + stazione — funziona ovunque, anche su dati mobili: PC e telefono
   escono entrambi verso il relay, quindi non c'è nessun router da configurare
Il telefono chiama casa — porta inoltrata sul router e nome DynDNS</source>
        <translation>Tiešs LAN — telefons ir tajā pašā tīklā: audio tiek sūtīts uz tā adresi
Relejs + stacija — darbojas visur, arī mobilajos datos: dators un telefons
   abi savienojas ar releju, tāpēc nav jākonfigurē neviens maršrutētājs
Telefons zvana uz mājām — pāradresēts ports maršrutētājā un DynDNS vārds</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="731" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>Telefona IP vai releja resursdators</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="735" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(piesakieties, lai izvēlētos staciju)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="759" />
        <source>48 kHz</source>
        <translation>48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="760" />
        <source>24 kHz</source>
        <translation>24 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="761" />
        <source>12 kHz</source>
        <translation>12 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="762" />
        <source>Quanti campioni al secondo mandare.
48 kHz — 808 kbit/s, 364 MB l'ora: sicuro con qualunque programma
24 kHz — 424 kbit/s, 191 MB l'ora
12 kHz — 232 kbit/s, 104 MB l'ora: basta e avanza per un SSB,
che di banda ne occupa 2,7 kHz.

Se il telefono lo sente accelerato, non legge la frequenza
dichiarata: torna a 48 kHz.</source>
        <translation>Cik paraugu sekundē sūtīt.
48 kHz — 808 kbit/s, 364 MB stundā: droši ar jebkuru programmu
24 kHz — 424 kbit/s, 191 MB stundā
12 kHz — 232 kbit/s, 104 MB stundā: pilnīgi pietiek SSB,
kas aizņem tikai 2,7 kHz.

Ja telefonā skan paātrināti, tas ignorē norādīto iztveršanas
frekvenci: atgriezieties uz 48 kHz.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="772" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="773" />
        <source>Voce (Opus)</source>
        <translation>Balss (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="774" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="775" />
        <source>Digitali senza perdite</source>
        <translation>Digitālie režīmi, bez zudumiem</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="776" />
        <source>CW a tasto</source>
        <translation>Tikai CW manipulācija</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="777" />
        <source>PCM — compatibile con tutti, nessuna compressione
Voce — Opus a 32 kbit/s: serve un programma aggiornato dall'altra parte
CW — Opus a banda stretta, 20 kbit/s
Digitali — compresso senza perdere un bit, 146 kbit/s
CW a tasto — solo il ritmo del tasto, 2,4 kbit/s: si perde
tutto il contesto (QSB, QRM, chi chiama fuori nota)</source>
        <translation>PCM — darbojas ar visu, bez saspiešanas
Balss — Opus ar 32 kbit/s: otrā pusē vajadzīga atjaunināta programma
CW — šaurjoslas Opus, 20 kbit/s
Digitālie — saspiests, nezaudējot nevienu bitu, 146 kbit/s
CW manipulācija — tikai ritms, 2,4 kbit/s: zūd viss
konteksts (QSB, QRM, kas sauc blakus frekvencei)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="788" />
        <source>20 ms</source>
        <translation>20 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="789" />
        <source>40 ms</source>
        <translation>40 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="790" />
        <source>60 ms</source>
        <translation>60 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="792" />
        <source>Quanti frame mettere in un pacchetto: meno pacchetti, meno
intestazioni da pagare, ma un po' più di ritardo.
20 ms — latenza minima
40 ms — 18% di banda in meno, ritardo impercettibile
60 ms — 24% in meno, per reti a consumo</source>
        <translation>Cik kadru likt vienā paketē: mazāk pakešu nozīmē mazāk galvenu,
par ko maksāt, bet nedaudz lielāku aizturi.
20 ms — mazākā aizture
40 ms — par 18% mazāks joslas platums, nemanāma aizture
60 ms — par 24% mazāk, savienojumiem ar datu ierobežojumu</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="805" />
        <source>Audio radio</source>
        <translation>Radio audio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="806" />
        <source>Modalità</source>
        <translation>Režīms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="807" />
        <source>Host</source>
        <translation>Resursdators</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="814" />
        <source>stazione</source>
        <translation>stacija</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="818" />
        <source>Porta</source>
        <translation>Ports</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="826" />
        <source>Profilo</source>
        <translation>Profils</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="827" />
        <source>Campionamento</source>
        <translation>Iztveršanas frekvence</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="828" />
        <source>Pacchetti da</source>
        <translation>Pakešu garums</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="834" />
        <location filename="../main.cpp" line="840" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  Papildu iestatījumi</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="839" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  Papildu iestatījumi</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="846" />
        <location filename="../main.cpp" line="2372" />
        <location filename="../main.cpp" line="2700" />
        <source>Avvia</source>
        <translation>Sākt</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="856" />
        <source>Potenza, ROS e ALC letti dalla radio.
Compaiono mentre trasmetti, se la radio li espone.</source>
        <translation>No radio nolasītā jauda, SVK un ALC.
Tie parādās pārraides laikā, ja radio tos sniedz.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="858" />
        <location filename="../main.cpp" line="2374" />
        <source>fermo</source>
        <translation>apturēts</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="861" />
        <location filename="../main.cpp" line="2193" />
        <source>—</source>
        <translation>—</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="871" />
        <source>Yaesu — comandi nativi</source>
        <translation>Yaesu — comandi nativi</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="872" />
        <source>Icom IC-7300 — CI-V nativo</source>
        <translation>Icom IC-7300 — CI-V nativo</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="888" />
        <source>Hamlib %1 — %2 modelli riconosciuti.
I primi due sono i protocolli scritti dentro Decolink;
gli altri passano da Hamlib, la stessa libreria che usa
Decodium sul desktop.</source>
        <translation>Hamlib %1 — %2 atpazīti modeļi.
Pirmie divi ir Decolink iekšpusē rakstītie protokoli;
pārējie iet caur Hamlib — to pašu bibliotēku, ko lieto
Decodium uz datora.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="897" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>resursdators:ports programmai, kas tur radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="899" />
        <source>Indirizzo del programma che tiene la porta seriale.
rigctld e i programmi compatibili: localhost:4532
FLRig: localhost:12345

Serve quando la COM è già occupata da un altro programma:
la porta seriale è di chi la apre per primo, e in due non
ci si sta.</source>
        <translation>Programmas adrese, kas tur seriālo portu.
rigctld un saderīgas programmas: localhost:4532
FLRig: localhost:12345

Vajadzīga, kad COM portu jau aizņēmusi cita programma:
seriālais ports pieder tam, kas to atver pirmais, un divi neietilpst.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="912" />
        <source>115200</source>
        <translation>115200</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="914" />
        <source>7</source>
        <translation>7</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="915" />
        <location filename="../main.cpp" line="916" />
        <source>8</source>
        <translation>8</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="918" />
        <source>nessuna</source>
        <translation>nav</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="919" />
        <source>pari</source>
        <translation>pāra</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="920" />
        <source>dispari</source>
        <translation>nepāra</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="922" />
        <source>1</source>
        <translation>1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="923" />
        <source>2</source>
        <translation>2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="926" />
        <source>nessuno</source>
        <translation>nav</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="927" />
        <source>RTS/CTS</source>
        <translation>RTS/CTS</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="928" />
        <source>XON/XOFF</source>
        <translation>XON/XOFF</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="930" />
        <source>Servi il CAT al telefono</source>
        <translation>Nodrošināt CAT telefonam</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="931" />
        <location filename="../main.cpp" line="1489" />
        <source>CAT spento</source>
        <translation>CAT izslēgts</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="934" />
        <source>(nessuna: non trasmettere)</source>
        <translation>(nav: nepārraidīt)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="942" />
        <source>Radio / protocollo</source>
        <translation>Radio / protokols</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="943" />
        <source>Indirizzo CI-V</source>
        <translation>CI-V adrese</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="944" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>Adrese, ar kuru radio atbild CI-V kopnē.
IC-7300: 0x94 (rūpnīcas noklusējums). Ja tā mainīta radio
izvēlnēs, šeit jāieraksta tā pati vērtība.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="949" />
        <source>Audio al rig</source>
        <translation>Audio uz radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="956" />
        <source>Porta rig</source>
        <translation>Radio ports</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="961" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="966" />
        <source>Velocità</source>
        <translation>Ātrums</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="973" />
        <source>dati</source>
        <translation>dati</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="977" />
        <source>parità</source>
        <translation>paritāte</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="981" />
        <source>stop</source>
        <translation>stop</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="985" />
        <source>Seriale</source>
        <translation>Seriālais</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="986" />
        <source>Handshake</source>
        <translation>Rokasspiediens</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1015" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>pieteikšanās serveris (piem., decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1017" />
        <source>la tua email</source>
        <translation>tava e-pasta adrese</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1020" />
        <source>password</source>
        <translation>parole</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1021" />
        <source>ricorda la password</source>
        <translation>atcerēties paroli</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1022" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>Tiek saglabāta atklātā tekstā Windows iestatījumos: tikai datorā, kuram uzticies.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1024" />
        <source>Accedi</source>
        <translation>Pieteikties</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1025" />
        <source>non collegato</source>
        <translation>nav savienots</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1035" />
        <source>Server</source>
        <translation>Serveris</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1041" />
        <source>Accesso</source>
        <translation>Pieteikšanās</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1062" />
        <source>versione di Decolink</source>
        <translation>Decolink versija</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1070" />
        <source>lingua dell'interfaccia</source>
        <translation>saskarnes valoda</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1087" />
        <source>COLLEGAMENTO</source>
        <translation>SAVIENOJUMS</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1095" />
        <source>RADIO E CAT</source>
        <translation>RADIO UN CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1118" />
        <source>livello audio</source>
        <translation>audio līmenis</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1174" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>iztveršana ar %1 kHz: ja telefonā skan paātrināti, atgriezieties uz 48</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1278" />
        <location filename="../main.cpp" line="1286" />
        <source>Lingua</source>
        <translation>Valoda</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1279" />
        <source>Il collegamento è aperto: la lingua cambia alla prossima apertura del programma.</source>
        <translation>Savienojums ir atvērts: valoda mainīsies, nākamreiz palaižot programmu.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1287" />
        <source>Decolink si riavvia per cambiare lingua. Procedo?</source>
        <translation>Decolink pārstartēsies, lai mainītu valodu. Turpināt?</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1311" />
        <source>IP del telefono sulla rete locale</source>
        <translation>telefona IP vietējā tīklā</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1314" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>releja resursdators (piem., decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1317" />
        <source>(il telefono chiama questa porta)</source>
        <translation>(telefons zvana uz šo portu)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1328" />
        <source>manca il server di accesso</source>
        <translation>trūkst pieteikšanās servera</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1330" />
        <source>servono email e password</source>
        <translation>nepieciešams e-pasts un parole</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1352" />
        <source>accesso in corso…</source>
        <translation>notiek pieteikšanās…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1372" />
        <source>risposta incomprensibile dal server</source>
        <translation>nesaprotama servera atbilde</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1409" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — stacija %2, kā %3%4</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1432" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1468" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>pieteikšanās dati beigušies: pieteikšos vēlreiz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1471" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>nav pieteicies: nospiediet Pieteikties, tad Sākt</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1501" />
        <source>nessuna porta seriale</source>
        <translation>nav seriālā porta</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1510" />
        <source>indirizzo CI-V non valido</source>
        <translation>nederīga CI-V adrese</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1519" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>trūkst programmas adreses, kas tur radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1536" />
        <source>qui c'è Decolink stesso: scegli il programma che tiene davvero la radio, o cambia la porta TCP qui sotto</source>
        <translation>šeit ir pats Decolink: izvēlieties programmu, kas patiešām tur radio, vai nomainiet TCP portu zemāk</translation>
    </message>
    <message>
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>TCP ports %1 ir tas pats, kuram pieslēdzaties: nomainiet vienu no tiem</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1552" />
        <source>%1 non risponde: %2</source>
        <translation>%1 neatbild: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1565" />
        <source>%1 non si apre: %2</source>
        <translation>%1 neatveras: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1573" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>TCP ports %1 ir aizņemts (vai rigctld jau darbojas?)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1621" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>radio: %1 MHz  %2   (TCP %3, un pa audio kanālu)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1650" />
        <source>il programma che tiene la radio ha smesso di rispondere — riaccendi il CAT quando è tornato</source>
        <translation>programma, kas tur radio, vairs neatbild — ieslēdziet CAT no jauna, kad tā atgriezīsies</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1652" />
        <source>rig non risponde sulla seriale</source>
        <translation>radio neatbild uz seriālā porta</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1680" />
        <source>telefono connesso da %1:%2</source>
        <translation>telefons savienots no %1:%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1730" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>jāatjauno pieteikšanās dati: pieteikšos vēlreiz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1734" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>relejs noraidīja savienojumu: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1742" />
        <source>il telefono è entrato nella stanza</source>
        <translation>telefons ir pievienojies telpai</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1744" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>reģistrēts relejā kā %1 (%2)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1851" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>telefons lasa grupētās paketes: samazināts joslas platums</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1873" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>telefona pieprasītais profils: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2167" />
        <location filename="../main.cpp" line="2348" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>%1 neatbalsta 48 kHz mono 16 bitu</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2175" />
        <source>trasmissione dal telefono in corso</source>
        <translation>notiek pārraide no telefona</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2186" />
        <source>trasmissione finita</source>
        <translation>pārraide beigusies</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2237" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>reģistrēts, bet stacijā nav neviena cita: telefons vēl nav pievienojies</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2240" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>uzmanību: profils %1, bet telefons nav apstiprinājis, ka prot to nolasīt — ja neko nedzirdat, pārejiet uz PCM 48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2254" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>telefons vairs nav sasniedzams — gaidu, kad tas atzvanīs</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2296" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Opus nesāk darboties (%1): palieku uz PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2312" />
        <source>manca l'host di destinazione</source>
        <translation>trūkst mērķa resursdatora</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2315" />
        <source>nome non risolto: %1</source>
        <translation>vārds nav atrisināts: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2320" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>vispirms piesakieties: relejs nepieņem savienojumus bez pieteikšanās datiem</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2330" />
        <source>porta %1 non disponibile</source>
        <translation>ports %1 nav pieejams</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2344" />
        <source>nessun ingresso audio</source>
        <translation>nav audio ievades</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2353" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>nevar atvērt audio ievadi</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2357" />
        <source>Ferma</source>
        <translation>Apturēt</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2361" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>klausos portā %1 — gaidu telefonu</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2412" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>profils atgriezts uz PCM 48 kHz: saspiestajiem profiliem vajadzīgs atjaunināts telefons</translation>
    </message>
</context>
<context>
    <name>QObject</name>
    <message>
        <location filename="../hamlibrig.h" line="184" />
        <source>errore %1 di Hamlib</source>
        <translation>Hamlib kļūda %1</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="270" />
        <source>indirizzo vuoto</source>
        <translation>tukša adrese</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="279" />
        <source>nessuna risposta da %1:%2</source>
        <translation>nav atbildes no %1:%2</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="280" />
        <source>%1:%2 — %3</source>
        <translation>%1:%2 — %3</translation>
    </message>
</context>
</TS>