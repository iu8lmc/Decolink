<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="hu">
<context>
    <name>Client</name>
    <message>
        <location filename="../main.cpp" line="571" />
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — a rádió a Decodium Mobile-on</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="578" />
        <source>LAN diretta</source>
        <translation>Közvetlen LAN</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="579" />
        <source>Relay + stazione</source>
        <translation>Relé + állomás</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="580" />
        <source>Il telefono chiama casa</source>
        <translation>A telefon hívja az otthont</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="581" />
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
        <location filename="../main.cpp" line="588" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>A telefon IP-címe vagy a relé kiszolgálója</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="592" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(jelentkezzen be az állomás kiválasztásához)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="616" />
        <source>48 kHz</source>
        <translation>48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="617" />
        <source>24 kHz</source>
        <translation>24 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="618" />
        <source>12 kHz</source>
        <translation>12 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="619" />
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
        <location filename="../main.cpp" line="629" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="630" />
        <source>Voce (Opus)</source>
        <translation>Beszéd (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="631" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="632" />
        <source>Digitali senza perdite</source>
        <translation>Digitális módok, veszteségmentes</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="633" />
        <source>CW a tasto</source>
        <translation>Csak CW-billentyűzés</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="634" />
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
        <location filename="../main.cpp" line="645" />
        <source>20 ms</source>
        <translation>20 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="646" />
        <source>40 ms</source>
        <translation>40 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="647" />
        <source>60 ms</source>
        <translation>60 ms</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="649" />
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
        <location filename="../main.cpp" line="662" />
        <source>Audio radio</source>
        <translation>Rádió hangja</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="663" />
        <source>Modalità</source>
        <translation>Üzemmód</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="664" />
        <source>Host</source>
        <translation>Kiszolgáló</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="671" />
        <source>stazione</source>
        <translation>állomás</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="675" />
        <source>Porta</source>
        <translation>Port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="683" />
        <source>Profilo</source>
        <translation>Profil</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="684" />
        <source>Campionamento</source>
        <translation>Mintavételezés</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="685" />
        <source>Pacchetti da</source>
        <translation>Csomaghossz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="691" />
        <location filename="../main.cpp" line="697" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  Speciális beállítások</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="696" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  Speciális beállítások</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="703" />
        <location filename="../main.cpp" line="2182" />
        <location filename="../main.cpp" line="2442" />
        <source>Avvia</source>
        <translation>Indítás</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="709" />
        <location filename="../main.cpp" line="2184" />
        <source>fermo</source>
        <translation>leállítva</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="712" />
        <location filename="../main.cpp" line="2003" />
        <source>—</source>
        <translation>—</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="722" />
        <source>Yaesu — comandi nativi</source>
        <translation>Yaesu — comandi nativi</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="723" />
        <source>Icom IC-7300 — CI-V nativo</source>
        <translation>Icom IC-7300 — CI-V nativo</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="739" />
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
        <location filename="../main.cpp" line="748" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>a rádiót birtokló program kiszolgálója:portja</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="750" />
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
        <location filename="../main.cpp" line="763" />
        <source>115200</source>
        <translation>115200</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="765" />
        <source>7</source>
        <translation>7</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="766" />
        <location filename="../main.cpp" line="767" />
        <source>8</source>
        <translation>8</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="769" />
        <source>nessuna</source>
        <translation>nincs</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="770" />
        <source>pari</source>
        <translation>páros</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="771" />
        <source>dispari</source>
        <translation>páratlan</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="773" />
        <source>1</source>
        <translation>1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="774" />
        <source>2</source>
        <translation>2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="777" />
        <source>nessuno</source>
        <translation>nincs</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="778" />
        <source>RTS/CTS</source>
        <translation>RTS/CTS</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="779" />
        <source>XON/XOFF</source>
        <translation>XON/XOFF</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="781" />
        <source>Servi il CAT al telefono</source>
        <translation>CAT szolgáltatása a telefonnak</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="782" />
        <location filename="../main.cpp" line="1315" />
        <source>CAT spento</source>
        <translation>CAT kikapcsolva</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="785" />
        <source>(nessuna: non trasmettere)</source>
        <translation>(nincs: ne adjon)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="793" />
        <source>Radio / protocollo</source>
        <translation>Rádió / protokoll</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="794" />
        <source>Indirizzo CI-V</source>
        <translation>CI-V cím</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="795" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>A cím, amelyen a rádió válaszol a CI-V buszon.
IC-7300: 0x94 (gyári alapérték). Ha a rádió menüjében
megváltoztatták, ugyanazt az értéket kell ide írni.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="800" />
        <source>Audio al rig</source>
        <translation>Hang a rádió felé</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="807" />
        <source>Porta rig</source>
        <translation>Rádió portja</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="812" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="817" />
        <source>Velocità</source>
        <translation>Sebesség</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="824" />
        <source>dati</source>
        <translation>adat</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="828" />
        <source>parità</source>
        <translation>paritás</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="832" />
        <source>stop</source>
        <translation>stop</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="836" />
        <source>Seriale</source>
        <translation>Soros</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="837" />
        <source>Handshake</source>
        <translation>Kézfogás</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="866" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>bejelentkezési kiszolgáló (pl. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="868" />
        <source>la tua email</source>
        <translation>az e-mail-címed</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="871" />
        <source>password</source>
        <translation>jelszó</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="872" />
        <source>ricorda la password</source>
        <translation>jelszó megjegyzése</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="873" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>Titkosítatlanul tárolódik a Windows beállításai közt: csak megbízható gépen érdemes.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="875" />
        <source>Accedi</source>
        <translation>Belépés</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="876" />
        <source>non collegato</source>
        <translation>nincs kapcsolat</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="886" />
        <source>Server</source>
        <translation>Kiszolgáló</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="892" />
        <source>Accesso</source>
        <translation>Belépés</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="914" />
        <source>lingua dell'interfaccia</source>
        <translation>a felület nyelve</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="930" />
        <source>COLLEGAMENTO</source>
        <translation>KAPCSOLAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="938" />
        <source>RADIO E CAT</source>
        <translation>RÁDIÓ ÉS CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="961" />
        <source>livello audio</source>
        <translation>hangszint</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1016" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>mintavételezés %1 kHz-en: ha a telefonon felgyorsítva szól, térjen vissza 48-ra</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1104" />
        <location filename="../main.cpp" line="1112" />
        <source>Lingua</source>
        <translation>Nyelv</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1105" />
        <source>Il collegamento è aperto: la lingua cambia alla prossima apertura del programma.</source>
        <translation>A kapcsolat él: a nyelv a program következő indításakor változik meg.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1113" />
        <source>Decolink si riavvia per cambiare lingua. Procedo?</source>
        <translation>A Decolink újraindul a nyelv módosításához. Folytatja?</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1137" />
        <source>IP del telefono sulla rete locale</source>
        <translation>a telefon IP-címe a helyi hálózaton</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1140" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>a relé kiszolgálója (pl. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1143" />
        <source>(il telefono chiama questa porta)</source>
        <translation>(a telefon ezt a portot hívja)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1154" />
        <source>manca il server di accesso</source>
        <translation>hiányzik a bejelentkezési kiszolgáló</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1156" />
        <source>servono email e password</source>
        <translation>e-mail-cím és jelszó szükséges</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1178" />
        <source>accesso in corso…</source>
        <translation>belépés folyamatban…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1198" />
        <source>risposta incomprensibile dal server</source>
        <translation>értelmezhetetlen válasz a kiszolgálótól</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1235" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — %2 állomás, mint %3%4</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1258" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1294" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>a hitelesítő adatok lejártak: újra belépek</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1297" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>nincs belépve: nyomja meg a Belépés, majd az Indítás gombot</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1327" />
        <source>nessuna porta seriale</source>
        <translation>nincs soros port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1336" />
        <source>indirizzo CI-V non valido</source>
        <translation>érvénytelen CI-V cím</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1345" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>hiányzik a rádiót birtokló program címe</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1362" />
        <source>qui c'è Decolink stesso: scegli il programma che tiene davvero la radio, o cambia la porta TCP qui sotto</source>
        <translation>ez maga a Decolink: válassza azt a programot, amely valóban birtokolja a rádiót, vagy módosítsa lent a TCP portot</translation>
    </message>
    <message>
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>a(z) %1 TCP port ugyanaz, amelyhez csatlakozik: változtassa meg az egyiket</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1378" />
        <source>%1 non risponde: %2</source>
        <translation>%1 nem válaszol: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1391" />
        <source>%1 non si apre: %2</source>
        <translation>%1 nem nyitható meg: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1399" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>a(z) %1 TCP port foglalt (fut már a rigctld?)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1447" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>rádió: %1 MHz  %2   (TCP %3, és a hangcsatornán)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1460" />
        <source>il programma che tiene la radio ha smesso di rispondere — riaccendi il CAT quando è tornato</source>
        <translation>a rádiót birtokló program nem válaszol többé — kapcsolja vissza a CAT-et, ha újra elérhető</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1462" />
        <source>rig non risponde sulla seriale</source>
        <translation>a rádió nem válaszol a soros porton</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1490" />
        <source>telefono connesso da %1:%2</source>
        <translation>a telefon csatlakozott innen: %1:%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1540" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>a hitelesítő adatokat meg kell újítani: újra belépek</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1544" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>a relé elutasította a kapcsolatot: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1552" />
        <source>il telefono è entrato nella stanza</source>
        <translation>a telefon belépett a szobába</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1554" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>regisztrálva a relén mint %1 (%2)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1661" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>a telefon olvassa a csoportosított csomagokat: csökkentett sávszélesség</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1683" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>a telefon által kért profil: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1977" />
        <location filename="../main.cpp" line="2158" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>a(z) %1 nem támogatja a 48 kHz mono 16 bitet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1985" />
        <source>trasmissione dal telefono in corso</source>
        <translation>adás a telefonról folyamatban</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1996" />
        <source>trasmissione finita</source>
        <translation>az adás véget ért</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2047" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>regisztrálva, de rajtad kívül nincs senki az állomáson: a telefon még nem lépett be</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2050" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>figyelem: %1 profil, de a telefon nem erősítette meg, hogy tudja olvasni — ha nem hall semmit, váltson PCM 48 kHz-re</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2064" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>a telefon már nem érhető el — várom, hogy visszahívjon</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2106" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Az Opus nem indul (%1): marad a PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2122" />
        <source>manca l'host di destinazione</source>
        <translation>hiányzik a cél kiszolgáló</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2125" />
        <source>nome non risolto: %1</source>
        <translation>a név nem oldható fel: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2130" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>előbb lépjen be: a relé nem fogad kapcsolatot hitelesítő adatok nélkül</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2140" />
        <source>porta %1 non disponibile</source>
        <translation>a(z) %1 port nem érhető el</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2154" />
        <source>nessun ingresso audio</source>
        <translation>nincs hangbemenet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2163" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>a hangbemenet nem nyitható meg</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2167" />
        <source>Ferma</source>
        <translation>Leállítás</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2171" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>figyelés a(z) %1 porton — várom a telefont</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2222" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>a profil visszaállt PCM 48 kHz-re: a tömörített profilokhoz frissített telefon kell</translation>
    </message>
</context>
<context>
    <name>QObject</name>
    <message>
        <location filename="../hamlibrig.h" line="182" />
        <source>errore %1 di Hamlib</source>
        <translation>Hamlib-hiba: %1</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="268" />
        <source>indirizzo vuoto</source>
        <translation>üres cím</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="277" />
        <source>nessuna risposta da %1:%2</source>
        <translation>nincs válasz innen: %1:%2</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="278" />
        <source>%1:%2 — %3</source>
        <translation>%1:%2 — %3</translation>
    </message>
</context>
</TS>