<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="lv">
<context>
    <name>Client</name>
    <message>
        <location filename="../main.cpp" line="548" />
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — radio Decodium Mobile lietotnē</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="555" />
        <source>LAN diretta</source>
        <translation>Tiešs LAN</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="556" />
        <source>Relay + stazione</source>
        <translation>Relejs + stacija</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="557" />
        <source>Il telefono chiama casa</source>
        <translation>Telefons zvana uz mājām</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="558" />
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
        <location filename="../main.cpp" line="565" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>Telefona IP vai releja resursdators</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="569" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(piesakieties, lai izvēlētos staciju)</translation>
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
        <translation>Cik paraugu sekundē sūtīt.
48 kHz — 808 kbit/s, 364 MB stundā: droši ar jebkuru programmu
24 kHz — 424 kbit/s, 191 MB stundā
12 kHz — 232 kbit/s, 104 MB stundā: pilnīgi pietiek SSB,
kas aizņem tikai 2,7 kHz.

Ja telefonā skan paātrināti, tas ignorē norādīto iztveršanas
frekvenci: atgriezieties uz 48 kHz.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="606" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="607" />
        <source>Voce (Opus)</source>
        <translation>Balss (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="608" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="609" />
        <source>Digitali senza perdite</source>
        <translation>Digitālie režīmi, bez zudumiem</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="610" />
        <source>CW a tasto</source>
        <translation>Tikai CW manipulācija</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="611" />
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
        <translation>Cik kadru likt vienā paketē: mazāk pakešu nozīmē mazāk galvenu,
par ko maksāt, bet nedaudz lielāku aizturi.
20 ms — mazākā aizture
40 ms — par 18% mazāks joslas platums, nemanāma aizture
60 ms — par 24% mazāk, savienojumiem ar datu ierobežojumu</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="639" />
        <source>Audio radio</source>
        <translation>Radio audio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="640" />
        <source>Modalità</source>
        <translation>Režīms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="641" />
        <source>Host</source>
        <translation>Resursdators</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="648" />
        <source>stazione</source>
        <translation>stacija</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="652" />
        <source>Porta</source>
        <translation>Ports</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="660" />
        <source>Profilo</source>
        <translation>Profils</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="661" />
        <source>Campionamento</source>
        <translation>Iztveršanas frekvence</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="662" />
        <source>Pacchetti da</source>
        <translation>Pakešu garums</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="668" />
        <location filename="../main.cpp" line="674" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  Papildu iestatījumi</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="673" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  Papildu iestatījumi</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="680" />
        <location filename="../main.cpp" line="2067" />
        <source>Avvia</source>
        <translation>Sākt</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="686" />
        <location filename="../main.cpp" line="2069" />
        <source>fermo</source>
        <translation>apturēts</translation>
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
        <translation>Hamlib %1 — %2 atpazīti modeļi.
Pirmie divi ir Decolink iekšpusē rakstītie protokoli;
pārējie iet caur Hamlib — to pašu bibliotēku, ko lieto
Decodium uz datora.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="725" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>resursdators:ports programmai, kas tur radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="727" />
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
        <translation>nav</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="747" />
        <source>pari</source>
        <translation>pāra</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="748" />
        <source>dispari</source>
        <translation>nepāra</translation>
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
        <translation>nav</translation>
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
        <translation>Nodrošināt CAT telefonam</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="759" />
        <location filename="../main.cpp" line="1238" />
        <source>CAT spento</source>
        <translation>CAT izslēgts</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="762" />
        <source>(nessuna: non trasmettere)</source>
        <translation>(nav: nepārraidīt)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="770" />
        <source>Radio / protocollo</source>
        <translation>Radio / protokols</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="771" />
        <source>Indirizzo CI-V</source>
        <translation>CI-V adrese</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="772" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>Adrese, ar kuru radio atbild CI-V kopnē.
IC-7300: 0x94 (rūpnīcas noklusējums). Ja tā mainīta radio
izvēlnēs, šeit jāieraksta tā pati vērtība.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="777" />
        <source>Audio al rig</source>
        <translation>Audio uz radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="784" />
        <source>Porta rig</source>
        <translation>Radio ports</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="789" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="794" />
        <source>Velocità</source>
        <translation>Ātrums</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="801" />
        <source>dati</source>
        <translation>dati</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="805" />
        <source>parità</source>
        <translation>paritāte</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="809" />
        <source>stop</source>
        <translation>stop</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="813" />
        <source>Seriale</source>
        <translation>Seriālais</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="814" />
        <source>Handshake</source>
        <translation>Rokasspiediens</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="843" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>pieteikšanās serveris (piem., decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="845" />
        <source>la tua email</source>
        <translation>tava e-pasta adrese</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="848" />
        <source>password</source>
        <translation>parole</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="849" />
        <source>ricorda la password</source>
        <translation>atcerēties paroli</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="850" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>Tiek saglabāta atklātā tekstā Windows iestatījumos: tikai datorā, kuram uzticies.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="852" />
        <source>Accedi</source>
        <translation>Pieteikties</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="853" />
        <source>non collegato</source>
        <translation>nav savienots</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="863" />
        <source>Server</source>
        <translation>Serveris</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="869" />
        <source>Accesso</source>
        <translation>Pieteikšanās</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="891" />
        <source>COLLEGAMENTO</source>
        <translation>SAVIENOJUMS</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="899" />
        <source>RADIO E CAT</source>
        <translation>RADIO UN CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="922" />
        <source>livello audio</source>
        <translation>audio līmenis</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="977" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>iztveršana ar %1 kHz: ja telefonā skan paātrināti, atgriezieties uz 48</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1060" />
        <source>IP del telefono sulla rete locale</source>
        <translation>telefona IP vietējā tīklā</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1063" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>releja resursdators (piem., decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1066" />
        <source>(il telefono chiama questa porta)</source>
        <translation>(telefons zvana uz šo portu)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1077" />
        <source>manca il server di accesso</source>
        <translation>trūkst pieteikšanās servera</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1079" />
        <source>servono email e password</source>
        <translation>nepieciešams e-pasts un parole</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1101" />
        <source>accesso in corso…</source>
        <translation>notiek pieteikšanās…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1121" />
        <source>risposta incomprensibile dal server</source>
        <translation>nesaprotama servera atbilde</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1158" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — stacija %2, kā %3%4</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1181" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1217" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>pieteikšanās dati beigušies: pieteikšos vēlreiz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1220" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>nav pieteicies: nospiediet Pieteikties, tad Sākt</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1250" />
        <source>nessuna porta seriale</source>
        <translation>nav seriālā porta</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1259" />
        <source>indirizzo CI-V non valido</source>
        <translation>nederīga CI-V adrese</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1268" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>trūkst programmas adreses, kas tur radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1280" />
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>TCP ports %1 ir tas pats, kuram pieslēdzaties: nomainiet vienu no tiem</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1296" />
        <source>%1 non risponde: %2</source>
        <translation>%1 neatbild: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1309" />
        <source>%1 non si apre: %2</source>
        <translation>%1 neatveras: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1317" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>TCP ports %1 ir aizņemts (vai rigctld jau darbojas?)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1345" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>radio: %1 MHz  %2   (TCP %3, un pa audio kanālu)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1375" />
        <source>telefono connesso da %1:%2</source>
        <translation>telefons savienots no %1:%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1425" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>jāatjauno pieteikšanās dati: pieteikšos vēlreiz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1429" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>relejs noraidīja savienojumu: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1437" />
        <source>il telefono è entrato nella stanza</source>
        <translation>telefons ir pievienojies telpai</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1439" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>reģistrēts relejā kā %1 (%2)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1546" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>telefons lasa grupētās paketes: samazināts joslas platums</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1568" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>telefona pieprasītais profils: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1862" />
        <location filename="../main.cpp" line="2043" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>%1 neatbalsta 48 kHz mono 16 bitu</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1870" />
        <source>trasmissione dal telefono in corso</source>
        <translation>notiek pārraide no telefona</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1881" />
        <source>trasmissione finita</source>
        <translation>pārraide beigusies</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1932" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>reģistrēts, bet stacijā nav neviena cita: telefons vēl nav pievienojies</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1935" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>uzmanību: profils %1, bet telefons nav apstiprinājis, ka prot to nolasīt — ja neko nedzirdat, pārejiet uz PCM 48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1949" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>telefons vairs nav sasniedzams — gaidu, kad tas atzvanīs</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1991" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Opus nesāk darboties (%1): palieku uz PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2007" />
        <source>manca l'host di destinazione</source>
        <translation>trūkst mērķa resursdatora</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2010" />
        <source>nome non risolto: %1</source>
        <translation>vārds nav atrisināts: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2015" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>vispirms piesakieties: relejs nepieņem savienojumus bez pieteikšanās datiem</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2025" />
        <source>porta %1 non disponibile</source>
        <translation>ports %1 nav pieejams</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2039" />
        <source>nessun ingresso audio</source>
        <translation>nav audio ievades</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2048" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>nevar atvērt audio ievadi</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2052" />
        <source>Ferma</source>
        <translation>Apturēt</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2056" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>klausos portā %1 — gaidu telefonu</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2107" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>profils atgriezts uz PCM 48 kHz: saspiestajiem profiliem vajadzīgs atjaunināts telefons</translation>
    </message>
</context>
</TS>