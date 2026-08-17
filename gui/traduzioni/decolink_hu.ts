<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="hu">
<context>
    <name>Client</name>
    <message>
        <location filename="../main.cpp" line="695" />
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — a rádió a Decodium Mobile-on</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="702" />
        <source>LAN diretta</source>
        <translation>Közvetlen LAN</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="703" />
        <source>Relay + stazione</source>
        <translation>Relé + állomás</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="704" />
        <source>Il telefono chiama casa</source>
        <translation>A telefon hívja az otthont</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="705" />
        <source>LAN diretta — il telefono è sulla stessa rete: gli si manda l'audio all'indirizzo
Relay + stazione — funziona ovunque, anche su dati mobili: PC e telefono
   escono entrambi verso il relay, quindi non c'è nessun router da configurare
Il telefono chiama casa — porta inoltrata sul router e nome DynDNS</source>
        <translation>Közvetlen LAN — a telefon ugyanazon a hálózaton van: a hang a címére megy
Relé + állomás — mindenhol működik, mobilneten is: a PC és a telefon
   egyaránt a reléhez csatlakozik, így nincs router, amit beállítani kell
A telefon hívja az otthont — átirányított port a routeren és DynDNS-név</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="712" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>A telefon IP-címe vagy a relé kiszolgálója</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="716" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(jelentkezzen be az állomás kiválasztásához)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="740" />
        <source>48 kHz</source>
        <translation>48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="741" />
        <source>24 kHz</source>
        <translation>24 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="742" />
        <source>12 kHz</source>
        <translation>12 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="743" />
        <source>Quanti campioni al secondo mandare.
48 kHz — 808 kbit/s, 364 MB l'ora: sicuro con qualunque programma
24 kHz — 424 kbit/s, 191 MB l'ora
12 kHz — 232 kbit/s, 104 MB l'ora: basta e avanza per un SSB,
che di banda ne occupa 2,7 kHz.

Se il telefono lo sente accelerato, non legge la frequenza
dichiarata: torna a 48 kHz.</source>
        <translation>Hány mintát küldjön másodpercenként.
48 kHz — 808 kbit/s, 364 MB óránként: minden programmal biztonságos
24 kHz — 424 kbit/s, 191 MB óránként
12 kHz — 232 kbit/s, 104 MB óránként: bőven elég az SSB-hez,
amely csak 2,7 kHz-et foglal.

Ha a telefonon felgyorsítva szól, figyelmen kívül hagyja a megadott
mintavételezést: térjen vissza 48 kHz-re.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="753" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="754" />
        <source>Voce (Opus)</source>
        <translation>Beszéd (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="755" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="756" />
        <source>Digitali senza perdite</source>
        <translation>Digitális módok, veszteségmentes</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="757" />
        <source>CW a tasto</source>
        <translation>Csak CW-billentyűzés</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="758" />
        <source>PCM — compatibile con tutti, nessuna compressione
Voce — Opus a 32 kbit/s: serve un programma aggiornato dall'altra parte
CW — Opus a banda stretta, 20 kbit/s
Digitali — compresso senza perdere un bit, 146 kbit/s
CW a tasto — solo il ritmo del tasto, 2,4 kbit/s: si perde
tutto il contesto (QSB, QRM, chi chiama fuori nota)</source>
        <translation>PCM — mindennel működik, tömörítés nélkül
Beszéd — Opus 32 kbit/s-en: frissített programot igényel a túloldalon
CW — keskeny sávú Opus, 20 kbit/s
Digitális — bitpontosan tömörítve, 146 kbit/s
CW-billentyűzés — csak a ritmus, 2,4 kbit/s: elvész
a teljes környezet (QSB, QRM, aki a frekvencia mellett hív)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="769" />
        <source>20 ms</source>
        <translation>20 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="770" />
        <source>40 ms</source>
        <translation>40 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="771" />
        <source>60 ms</source>
        <translation>60 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="773" />
        <source>Quanti frame mettere in un pacchetto: meno pacchetti, meno
intestazioni da pagare, ma un po' più di ritardo.
20 ms — latenza minima
40 ms — 18% di banda in meno, ritardo impercettibile
60 ms — 24% in meno, per reti a consumo</source>
        <translation>Hány keret kerüljön egy csomagba: kevesebb csomag kevesebb fejlécet
jelent, de kicsit több késleltetést.
20 ms — legkisebb késleltetés
40 ms — 18%-kal kevesebb sávszélesség, észrevehetetlen késleltetés
60 ms — 24%-kal kevesebb, korlátos kapcsolatokhoz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="786" />
        <source>Audio radio</source>
        <translation>Rádió hangja</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="787" />
        <source>Modalità</source>
        <translation>Üzemmód</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="788" />
        <source>Host</source>
        <translation>Kiszolgáló</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="795" />
        <source>stazione</source>
        <translation>állomás</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="799" />
        <source>Porta</source>
        <translation>Port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="807" />
        <source>Profilo</source>
        <translation>Profil</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="808" />
        <source>Campionamento</source>
        <translation>Mintavételezés</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="809" />
        <source>Pacchetti da</source>
        <translation>Csomaghossz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="815" />
        <location filename="../main.cpp" line="821" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  Speciális beállítások</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="820" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  Speciális beállítások</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="827" />
        <location filename="../main.cpp" line="2336" />
        <location filename="../main.cpp" line="2663" />
        <source>Avvia</source>
        <translation>Indítás</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="833" />
        <location filename="../main.cpp" line="2338" />
        <source>fermo</source>
        <translation>leállítva</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="836" />
        <location filename="../main.cpp" line="2157" />
        <source>—</source>
        <translation>—</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="846" />
        <source>Yaesu — comandi nativi</source>
        <translation>Yaesu — comandi nativi</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="847" />
        <source>Icom IC-7300 — CI-V nativo</source>
        <translation>Icom IC-7300 — CI-V nativo</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="863" />
        <source>Hamlib %1 — %2 modelli riconosciuti.
I primi due sono i protocolli scritti dentro Decolink;
gli altri passano da Hamlib, la stessa libreria che usa
Decodium sul desktop.</source>
        <translation>Hamlib %1 — %2 felismert modell.
Az első kettő a Decolinkba írt protokoll;
a többi a Hamlibon keresztül megy, ugyanazon a könyvtáron,
amit a Decodium használ asztali gépen.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="872" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>a rádiót birtokló program kiszolgálója:portja</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="874" />
        <source>Indirizzo del programma che tiene la porta seriale.
rigctld e i programmi compatibili: localhost:4532
FLRig: localhost:12345

Serve quando la COM è già occupata da un altro programma:
la porta seriale è di chi la apre per primo, e in due non
ci si sta.</source>
        <translation>A soros portot birtokló program címe.
rigctld és kompatibilis programok: localhost:4532
FLRig: localhost:12345

Akkor kell, ha a COM portot már elfoglalta egy másik program:
a soros port azé, aki elsőként megnyitja, és ketten nem férnek el.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="887" />
        <source>115200</source>
        <translation>115200</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="889" />
        <source>7</source>
        <translation>7</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="890" />
        <location filename="../main.cpp" line="891" />
        <source>8</source>
        <translation>8</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="893" />
        <source>nessuna</source>
        <translation>nincs</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="894" />
        <source>pari</source>
        <translation>páros</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="895" />
        <source>dispari</source>
        <translation>páratlan</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="897" />
        <source>1</source>
        <translation>1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="898" />
        <source>2</source>
        <translation>2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="901" />
        <source>nessuno</source>
        <translation>nincs</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="902" />
        <source>RTS/CTS</source>
        <translation>RTS/CTS</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="903" />
        <source>XON/XOFF</source>
        <translation>XON/XOFF</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="905" />
        <source>Servi il CAT al telefono</source>
        <translation>CAT szolgáltatása a telefonnak</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="906" />
        <location filename="../main.cpp" line="1463" />
        <source>CAT spento</source>
        <translation>CAT kikapcsolva</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="909" />
        <source>(nessuna: non trasmettere)</source>
        <translation>(nincs: ne adjon)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="917" />
        <source>Radio / protocollo</source>
        <translation>Rádió / protokoll</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="918" />
        <source>Indirizzo CI-V</source>
        <translation>CI-V cím</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="919" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>A cím, amelyen a rádió válaszol a CI-V buszon.
IC-7300: 0x94 (gyári alapérték). Ha a rádió menüjében
megváltoztatták, ugyanazt az értéket kell ide írni.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="924" />
        <source>Audio al rig</source>
        <translation>Hang a rádió felé</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="931" />
        <source>Porta rig</source>
        <translation>Rádió portja</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="936" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="941" />
        <source>Velocità</source>
        <translation>Sebesség</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="948" />
        <source>dati</source>
        <translation>adat</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="952" />
        <source>parità</source>
        <translation>paritás</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="956" />
        <source>stop</source>
        <translation>stop</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="960" />
        <source>Seriale</source>
        <translation>Soros</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="961" />
        <source>Handshake</source>
        <translation>Kézfogás</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="990" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>bejelentkezési kiszolgáló (pl. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="992" />
        <source>la tua email</source>
        <translation>az e-mail-címed</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="995" />
        <source>password</source>
        <translation>jelszó</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="996" />
        <source>ricorda la password</source>
        <translation>jelszó megjegyzése</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="997" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>Titkosítatlanul tárolódik a Windows beállításai közt: csak megbízható gépen érdemes.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="999" />
        <source>Accedi</source>
        <translation>Belépés</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1000" />
        <source>non collegato</source>
        <translation>nincs kapcsolat</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1010" />
        <source>Server</source>
        <translation>Kiszolgáló</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1016" />
        <source>Accesso</source>
        <translation>Belépés</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1037" />
        <source>versione di Decolink</source>
        <translation>a Decolink verziója</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1045" />
        <source>lingua dell'interfaccia</source>
        <translation>a felület nyelve</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1062" />
        <source>COLLEGAMENTO</source>
        <translation>KAPCSOLAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1070" />
        <source>RADIO E CAT</source>
        <translation>RÁDIÓ ÉS CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1093" />
        <source>livello audio</source>
        <translation>hangszint</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1148" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>mintavételezés %1 kHz-en: ha a telefonon felgyorsítva szól, térjen vissza 48-ra</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1252" />
        <location filename="../main.cpp" line="1260" />
        <source>Lingua</source>
        <translation>Nyelv</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1253" />
        <source>Il collegamento è aperto: la lingua cambia alla prossima apertura del programma.</source>
        <translation>A kapcsolat él: a nyelv a program következő indításakor változik meg.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1261" />
        <source>Decolink si riavvia per cambiare lingua. Procedo?</source>
        <translation>A Decolink újraindul a nyelv módosításához. Folytatja?</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1285" />
        <source>IP del telefono sulla rete locale</source>
        <translation>a telefon IP-címe a helyi hálózaton</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1288" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>a relé kiszolgálója (pl. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1291" />
        <source>(il telefono chiama questa porta)</source>
        <translation>(a telefon ezt a portot hívja)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1302" />
        <source>manca il server di accesso</source>
        <translation>hiányzik a bejelentkezési kiszolgáló</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1304" />
        <source>servono email e password</source>
        <translation>e-mail-cím és jelszó szükséges</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1326" />
        <source>accesso in corso…</source>
        <translation>belépés folyamatban…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1346" />
        <source>risposta incomprensibile dal server</source>
        <translation>értelmezhetetlen válasz a kiszolgálótól</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1383" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — %2 állomás, mint %3%4</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1406" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1442" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>a hitelesítő adatok lejártak: újra belépek</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1445" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>nincs belépve: nyomja meg a Belépés, majd az Indítás gombot</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1475" />
        <source>nessuna porta seriale</source>
        <translation>nincs soros port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1484" />
        <source>indirizzo CI-V non valido</source>
        <translation>érvénytelen CI-V cím</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1493" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>hiányzik a rádiót birtokló program címe</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1510" />
        <source>qui c'è Decolink stesso: scegli il programma che tiene davvero la radio, o cambia la porta TCP qui sotto</source>
        <translation>ez maga a Decolink: válassza azt a programot, amely valóban birtokolja a rádiót, vagy módosítsa lent a TCP portot</translation>
    </message>
    <message>
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>a(z) %1 TCP port ugyanaz, amelyhez csatlakozik: változtassa meg az egyiket</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1526" />
        <source>%1 non risponde: %2</source>
        <translation>%1 nem válaszol: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1539" />
        <source>%1 non si apre: %2</source>
        <translation>%1 nem nyitható meg: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1547" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>a(z) %1 TCP port foglalt (fut már a rigctld?)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1595" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>rádió: %1 MHz  %2   (TCP %3, és a hangcsatornán)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1614" />
        <source>il programma che tiene la radio ha smesso di rispondere — riaccendi il CAT quando è tornato</source>
        <translation>a rádiót birtokló program nem válaszol többé — kapcsolja vissza a CAT-et, ha újra elérhető</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1616" />
        <source>rig non risponde sulla seriale</source>
        <translation>a rádió nem válaszol a soros porton</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1644" />
        <source>telefono connesso da %1:%2</source>
        <translation>a telefon csatlakozott innen: %1:%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1694" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>a hitelesítő adatokat meg kell újítani: újra belépek</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1698" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>a relé elutasította a kapcsolatot: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1706" />
        <source>il telefono è entrato nella stanza</source>
        <translation>a telefon belépett a szobába</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1708" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>regisztrálva a relén mint %1 (%2)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1815" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>a telefon olvassa a csoportosított csomagokat: csökkentett sávszélesség</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1837" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>a telefon által kért profil: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2131" />
        <location filename="../main.cpp" line="2312" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>a(z) %1 nem támogatja a 48 kHz mono 16 bitet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2139" />
        <source>trasmissione dal telefono in corso</source>
        <translation>adás a telefonról folyamatban</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2150" />
        <source>trasmissione finita</source>
        <translation>az adás véget ért</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2201" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>regisztrálva, de rajtad kívül nincs senki az állomáson: a telefon még nem lépett be</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2204" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>figyelem: %1 profil, de a telefon nem erősítette meg, hogy tudja olvasni — ha nem hall semmit, váltson PCM 48 kHz-re</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2218" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>a telefon már nem érhető el — várom, hogy visszahívjon</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2260" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Az Opus nem indul (%1): marad a PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2276" />
        <source>manca l'host di destinazione</source>
        <translation>hiányzik a cél kiszolgáló</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2279" />
        <source>nome non risolto: %1</source>
        <translation>a név nem oldható fel: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2284" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>előbb lépjen be: a relé nem fogad kapcsolatot hitelesítő adatok nélkül</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2294" />
        <source>porta %1 non disponibile</source>
        <translation>a(z) %1 port nem érhető el</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2308" />
        <source>nessun ingresso audio</source>
        <translation>nincs hangbemenet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2317" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>a hangbemenet nem nyitható meg</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2321" />
        <source>Ferma</source>
        <translation>Leállítás</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2325" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>figyelés a(z) %1 porton — várom a telefont</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2376" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>a profil visszaállt PCM 48 kHz-re: a tömörített profilokhoz frissített telefon kell</translation>
    </message>
</context>
<context>
    <name>QObject</name>
    <message>
        <location filename="../hamlibrig.h" line="184" />
        <source>errore %1 di Hamlib</source>
        <translation>Hamlib-hiba: %1</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="270" />
        <source>indirizzo vuoto</source>
        <translation>üres cím</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="279" />
        <source>nessuna risposta da %1:%2</source>
        <translation>nincs válasz innen: %1:%2</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="280" />
        <source>%1:%2 — %3</source>
        <translation>%1:%2 — %3</translation>
    </message>
</context>
</TS>