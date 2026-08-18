<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="de">
<context>
    <name>Client</name>
    <message>
        <location filename="../main.cpp" line="714" />
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — das Funkgerät auf Decodium Mobile</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="721" />
        <source>LAN diretta</source>
        <translation>Direktes LAN</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="722" />
        <source>Relay + stazione</source>
        <translation>Relay + Station</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="723" />
        <source>Il telefono chiama casa</source>
        <translation>Das Telefon ruft zu Hause an</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="724" />
        <source>LAN diretta — il telefono è sulla stessa rete: gli si manda l'audio all'indirizzo
Relay + stazione — funziona ovunque, anche su dati mobili: PC e telefono
   escono entrambi verso il relay, quindi non c'è nessun router da configurare
Il telefono chiama casa — porta inoltrata sul router e nome DynDNS</source>
        <translation>Direktes LAN — das Telefon ist im selben Netz: Audio geht an seine Adresse
Relay + Station — funktioniert überall, auch mobil: PC und Telefon
   verbinden sich beide zum Relay, also kein Router zu konfigurieren
Das Telefon ruft zu Hause an — Portweiterleitung im Router und DynDNS-Name</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="731" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>IP des Telefons oder Relay-Host</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="735" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(anmelden, um die Station zu wählen)</translation>
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
        <translation>Wie viele Abtastwerte pro Sekunde gesendet werden.
48 kHz — 808 kbit/s, 364 MB pro Stunde: sicher mit jedem Programm
24 kHz — 424 kbit/s, 191 MB pro Stunde
12 kHz — 232 kbit/s, 104 MB pro Stunde: reichlich für SSB,
das nur 2,7 kHz belegt.

Klingt es am Telefon zu schnell, wird die angegebene Abtastrate
ignoriert: zurück auf 48 kHz.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="772" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="773" />
        <source>Voce (Opus)</source>
        <translation>Sprache (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="774" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="775" />
        <source>Digitali senza perdite</source>
        <translation>Digimodes, verlustfrei</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="776" />
        <source>CW a tasto</source>
        <translation>Nur CW-Tastung</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="777" />
        <source>PCM — compatibile con tutti, nessuna compressione
Voce — Opus a 32 kbit/s: serve un programma aggiornato dall'altra parte
CW — Opus a banda stretta, 20 kbit/s
Digitali — compresso senza perdere un bit, 146 kbit/s
CW a tasto — solo il ritmo del tasto, 2,4 kbit/s: si perde
tutto il contesto (QSB, QRM, chi chiama fuori nota)</source>
        <translation>PCM — funktioniert mit allem, keine Kompression
Sprache — Opus mit 32 kbit/s: erfordert ein aktuelles Programm auf der Gegenseite
CW — schmalbandiges Opus, 20 kbit/s
Digimodes — verlustfrei komprimiert, 146 kbit/s
CW-Tastung — nur der Rhythmus, 2,4 kbit/s: der ganze Kontext geht
verloren (QSB, QRM, wer neben der Frequenz ruft)</translation>
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
        <translation>Wie viele Frames in ein Paket kommen: weniger Pakete bedeuten weniger
Kopfdaten, dafür etwas mehr Verzögerung.
20 ms — geringste Latenz
40 ms — 18% weniger Bandbreite, nicht wahrnehmbare Verzögerung
60 ms — 24% weniger, für Verbindungen mit Datenlimit</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="805" />
        <source>Audio radio</source>
        <translation>Funkgerät-Audio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="806" />
        <source>Modalità</source>
        <translation>Betriebsart</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="807" />
        <source>Host</source>
        <translation>Host</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="814" />
        <source>stazione</source>
        <translation>Station</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="818" />
        <source>Porta</source>
        <translation>Port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="826" />
        <source>Profilo</source>
        <translation>Profil</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="827" />
        <source>Campionamento</source>
        <translation>Abtastrate</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="828" />
        <source>Pacchetti da</source>
        <translation>Paketlänge</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="834" />
        <location filename="../main.cpp" line="840" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  Erweiterte Einstellungen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="839" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  Erweiterte Einstellungen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="846" />
        <location filename="../main.cpp" line="2372" />
        <location filename="../main.cpp" line="2700" />
        <source>Avvia</source>
        <translation>Start</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="856" />
        <source>Potenza, ROS e ALC letti dalla radio.
Compaiono mentre trasmetti, se la radio li espone.</source>
        <translation>Leistung, SWR und ALC vom Funkgerät gelesen.
Sie erscheinen beim Senden, sofern das Gerät sie liefert.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="858" />
        <location filename="../main.cpp" line="2374" />
        <source>fermo</source>
        <translation>angehalten</translation>
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
        <translation>Hamlib %1 — %2 erkannte Modelle.
Die ersten beiden sind die in Decolink geschriebenen Protokolle;
die anderen laufen über Hamlib, dieselbe Bibliothek wie bei
Decodium am Desktop.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="897" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>Host:Port des Programms, das das Funkgerät hält</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="899" />
        <source>Indirizzo del programma che tiene la porta seriale.
rigctld e i programmi compatibili: localhost:4532
FLRig: localhost:12345

Serve quando la COM è già occupata da un altro programma:
la porta seriale è di chi la apre per primo, e in due non
ci si sta.</source>
        <translation>Adresse des Programms, das die serielle Schnittstelle hält.
rigctld und kompatible Programme: localhost:4532
FLRig: localhost:12345

Nötig, wenn der COM-Port bereits von einem anderen Programm
belegt ist: die Schnittstelle gehört dem, der sie zuerst öffnet,
und zu zweit passt man nicht hinein.</translation>
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
        <translation>keine</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="919" />
        <source>pari</source>
        <translation>gerade</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="920" />
        <source>dispari</source>
        <translation>ungerade</translation>
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
        <translation>keiner</translation>
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
        <translation>CAT für das Telefon bereitstellen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="931" />
        <location filename="../main.cpp" line="1489" />
        <source>CAT spento</source>
        <translation>CAT aus</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="934" />
        <source>(nessuna: non trasmettere)</source>
        <translation>(keine: nicht senden)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="942" />
        <source>Radio / protocollo</source>
        <translation>Funkgerät / Protokoll</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="943" />
        <source>Indirizzo CI-V</source>
        <translation>CI-V-Adresse</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="944" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>Die Adresse, unter der das Funkgerät am CI-V-Bus antwortet.
IC-7300: 0x94 (Werkseinstellung). Wurde sie in den Menüs des
Geräts geändert, hier denselben Wert eintragen.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="949" />
        <source>Audio al rig</source>
        <translation>Audio zum Funkgerät</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="956" />
        <source>Porta rig</source>
        <translation>Funkgerät-Port</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="961" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="966" />
        <source>Velocità</source>
        <translation>Geschwindigkeit</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="973" />
        <source>dati</source>
        <translation>Daten</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="977" />
        <source>parità</source>
        <translation>Parität</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="981" />
        <source>stop</source>
        <translation>Stopp</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="985" />
        <source>Seriale</source>
        <translation>Seriell</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="986" />
        <source>Handshake</source>
        <translation>Handshake</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1015" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>Anmeldeserver (z. B. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1017" />
        <source>la tua email</source>
        <translation>deine E-Mail</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1020" />
        <source>password</source>
        <translation>Passwort</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1021" />
        <source>ricorda la password</source>
        <translation>Passwort merken</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1022" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>Wird im Klartext in den Windows-Einstellungen gespeichert: nur auf einem Rechner, dem du traust.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1024" />
        <source>Accedi</source>
        <translation>Anmelden</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1025" />
        <source>non collegato</source>
        <translation>nicht verbunden</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1035" />
        <source>Server</source>
        <translation>Server</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1041" />
        <source>Accesso</source>
        <translation>Anmeldung</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1062" />
        <source>versione di Decolink</source>
        <translation>Decolink-Version</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1070" />
        <source>lingua dell'interfaccia</source>
        <translation>Sprache der Oberfläche</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1087" />
        <source>COLLEGAMENTO</source>
        <translation>VERBINDUNG</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1095" />
        <source>RADIO E CAT</source>
        <translation>FUNKGERÄT UND CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1118" />
        <source>livello audio</source>
        <translation>Audiopegel</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1174" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>Abtastung mit %1 kHz: klingt es am Telefon zu schnell, zurück auf 48</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1278" />
        <location filename="../main.cpp" line="1286" />
        <source>Lingua</source>
        <translation>Sprache</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1279" />
        <source>Il collegamento è aperto: la lingua cambia alla prossima apertura del programma.</source>
        <translation>Die Verbindung läuft: die Sprache wechselt beim nächsten Start des Programms.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1287" />
        <source>Decolink si riavvia per cambiare lingua. Procedo?</source>
        <translation>Decolink startet neu, um die Sprache zu wechseln. Fortfahren?</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1311" />
        <source>IP del telefono sulla rete locale</source>
        <translation>IP des Telefons im lokalen Netz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1314" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>Relay-Host (z. B. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1317" />
        <source>(il telefono chiama questa porta)</source>
        <translation>(das Telefon ruft diesen Port an)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1328" />
        <source>manca il server di accesso</source>
        <translation>Der Anmeldeserver fehlt</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1330" />
        <source>servono email e password</source>
        <translation>E-Mail und Passwort werden benötigt</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1352" />
        <source>accesso in corso…</source>
        <translation>Anmeldung läuft…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1372" />
        <source>risposta incomprensibile dal server</source>
        <translation>unverständliche Antwort vom Server</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1409" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — Station %2, als %3%4</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1432" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1468" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>Zugangsdaten abgelaufen: melde mich erneut an</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1471" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>nicht angemeldet: erst Anmelden, dann Start</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1501" />
        <source>nessuna porta seriale</source>
        <translation>keine serielle Schnittstelle</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1510" />
        <source>indirizzo CI-V non valido</source>
        <translation>ungültige CI-V-Adresse</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1519" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>Adresse des Programms fehlt, das das Funkgerät hält</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1536" />
        <source>qui c'è Decolink stesso: scegli il programma che tiene davvero la radio, o cambia la porta TCP qui sotto</source>
        <translation>das ist Decolink selbst: wähle das Programm, das das Funkgerät wirklich hält, oder ändere den TCP-Port unten</translation>
    </message>
    <message>
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>TCP-Port %1 ist derselbe, zu dem du dich verbindest: ändere einen davon</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1552" />
        <source>%1 non risponde: %2</source>
        <translation>%1 antwortet nicht: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1565" />
        <source>%1 non si apre: %2</source>
        <translation>%1 lässt sich nicht öffnen: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1573" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>TCP-Port %1 belegt (läuft rigctld bereits?)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1621" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>Funkgerät: %1 MHz  %2   (TCP %3, und über den Audiokanal)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1650" />
        <source>il programma che tiene la radio ha smesso di rispondere — riaccendi il CAT quando è tornato</source>
        <translation>das Programm mit dem Funkgerät antwortet nicht mehr — CAT wieder einschalten, sobald es zurück ist</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1652" />
        <source>rig non risponde sulla seriale</source>
        <translation>Funkgerät antwortet nicht auf der seriellen Schnittstelle</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1680" />
        <source>telefono connesso da %1:%2</source>
        <translation>Telefon verbunden von %1:%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1730" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>Zugangsdaten müssen erneuert werden: melde mich erneut an</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1734" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>Das Relay hat die Verbindung abgelehnt: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1742" />
        <source>il telefono è entrato nella stanza</source>
        <translation>Das Telefon ist dem Raum beigetreten</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1744" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>am Relay angemeldet als %1 (%2)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1851" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>Das Telefon liest gebündelte Pakete: Bandbreite reduziert</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1873" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>Profil auf Wunsch des Telefons: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2167" />
        <location filename="../main.cpp" line="2348" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>%1 unterstützt kein 48 kHz Mono 16 Bit</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2175" />
        <source>trasmissione dal telefono in corso</source>
        <translation>Sendung vom Telefon läuft</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2186" />
        <source>trasmissione finita</source>
        <translation>Sendung beendet</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2237" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>angemeldet, aber sonst ist niemand in der Station: das Telefon ist noch nicht da</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2240" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>Achtung: Profil %1, aber das Telefon hat nicht bestätigt, dass es das lesen kann — hörst du nichts, wechsle zu PCM 48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2254" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>Telefon nicht mehr erreichbar — warte auf Rückruf</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2296" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Opus startet nicht (%1): bleibe bei PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2312" />
        <source>manca l'host di destinazione</source>
        <translation>Der Ziel-Host fehlt</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2315" />
        <source>nome non risolto: %1</source>
        <translation>Name nicht aufgelöst: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2320" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>erst anmelden: das Relay nimmt keine Verbindungen ohne Zugangsdaten an</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2330" />
        <source>porta %1 non disponibile</source>
        <translation>Port %1 nicht verfügbar</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2344" />
        <source>nessun ingresso audio</source>
        <translation>kein Audioeingang</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2353" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>Audioeingang lässt sich nicht öffnen</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2357" />
        <source>Ferma</source>
        <translation>Stopp</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2361" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>höre auf Port %1 — warte auf das Telefon</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2412" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>Profil auf PCM 48 kHz zurückgesetzt: komprimierte Profile brauchen ein aktuelles Telefon</translation>
    </message>
</context>
<context>
    <name>QObject</name>
    <message>
        <location filename="../hamlibrig.h" line="184" />
        <source>errore %1 di Hamlib</source>
        <translation>Hamlib-Fehler %1</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="270" />
        <source>indirizzo vuoto</source>
        <translation>leere Adresse</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="279" />
        <source>nessuna risposta da %1:%2</source>
        <translation>keine Antwort von %1:%2</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="280" />
        <source>%1:%2 — %3</source>
        <translation>%1:%2 — %3</translation>
    </message>
</context>
</TS>