<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="ro">
<context>
    <name>Client</name>
    <message>
        <location filename="../main.cpp" line="695" />
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — radioul pe Decodium Mobile</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="702" />
        <source>LAN diretta</source>
        <translation>LAN direct</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="703" />
        <source>Relay + stazione</source>
        <translation>Releu + stație</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="704" />
        <source>Il telefono chiama casa</source>
        <translation>Telefonul sună acasă</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="705" />
        <source>LAN diretta — il telefono è sulla stessa rete: gli si manda l'audio all'indirizzo
Relay + stazione — funziona ovunque, anche su dati mobili: PC e telefono
   escono entrambi verso il relay, quindi non c'è nessun router da configurare
Il telefono chiama casa — porta inoltrata sul router e nome DynDNS</source>
        <translation>LAN direct — telefonul e în aceeași rețea: audio merge la adresa lui
Releu + stație — merge oriunde, inclusiv pe date mobile: PC-ul și telefonul
   ies amândouă spre releu, deci nu e niciun router de configurat
Telefonul sună acasă — port redirecționat pe router și nume DynDNS</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="712" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>IP-ul telefonului sau gazda releului</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="716" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(autentifică-te pentru a alege stația)</translation>
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
        <translation>Câte eșantioane pe secundă să trimită.
48 kHz — 808 kbit/s, 364 MB pe oră: sigur cu orice program
24 kHz — 424 kbit/s, 191 MB pe oră
12 kHz — 232 kbit/s, 104 MB pe oră: mai mult decât suficient pentru SSB,
care ocupă doar 2,7 kHz.

Dacă telefonul îl aude accelerat, ignoră eșantionarea declarată:
revino la 48 kHz.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="753" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="754" />
        <source>Voce (Opus)</source>
        <translation>Voce (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="755" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="756" />
        <source>Digitali senza perdite</source>
        <translation>Moduri digitale, fără pierderi</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="757" />
        <source>CW a tasto</source>
        <translation>Doar manipulare CW</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="758" />
        <source>PCM — compatibile con tutti, nessuna compressione
Voce — Opus a 32 kbit/s: serve un programma aggiornato dall'altra parte
CW — Opus a banda stretta, 20 kbit/s
Digitali — compresso senza perdere un bit, 146 kbit/s
CW a tasto — solo il ritmo del tasto, 2,4 kbit/s: si perde
tutto il contesto (QSB, QRM, chi chiama fuori nota)</source>
        <translation>PCM — merge cu orice, fără compresie
Voce — Opus la 32 kbit/s: necesită un program actualizat de cealaltă parte
CW — Opus în bandă îngustă, 20 kbit/s
Digitale — comprimat fără a pierde un bit, 146 kbit/s
Manipulare CW — doar ritmul, 2,4 kbit/s: se pierde
tot contextul (QSB, QRM, cine cheamă lângă frecvență)</translation>
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
        <translation>Câte cadre să pună într-un pachet: mai puține pachete înseamnă mai
puține antete de plătit, dar puțin mai multă întârziere.
20 ms — latență minimă
40 ms — cu 18% mai puțină lățime de bandă, întârziere imperceptibilă
60 ms — cu 24% mai puțin, pentru conexiuni cu trafic limitat</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="786" />
        <source>Audio radio</source>
        <translation>Audio radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="787" />
        <source>Modalità</source>
        <translation>Mod</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="788" />
        <source>Host</source>
        <translation>Gazdă</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="795" />
        <source>stazione</source>
        <translation>stație</translation>
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
        <translation>Eșantionare</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="809" />
        <source>Pacchetti da</source>
        <translation>Durata pachetului</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="815" />
        <location filename="../main.cpp" line="821" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  Setări avansate</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="820" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  Setări avansate</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="827" />
        <location filename="../main.cpp" line="2336" />
        <location filename="../main.cpp" line="2663" />
        <source>Avvia</source>
        <translation>Pornește</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="833" />
        <location filename="../main.cpp" line="2338" />
        <source>fermo</source>
        <translation>oprit</translation>
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
        <translation>Hamlib %1 — %2 modele recunoscute.
Primele două sunt protocoalele scrise în Decolink;
celelalte trec prin Hamlib, aceeași bibliotecă folosită de
Decodium pe desktop.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="872" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>gazdă:port al programului care deține radioul</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="874" />
        <source>Indirizzo del programma che tiene la porta seriale.
rigctld e i programmi compatibili: localhost:4532
FLRig: localhost:12345

Serve quando la COM è già occupata da un altro programma:
la porta seriale è di chi la apre per primo, e in due non
ci si sta.</source>
        <translation>Adresa programului care deține portul serial.
rigctld și programele compatibile: localhost:4532
FLRig: localhost:12345

Este necesară când portul COM e deja ocupat de alt program:
portul serial e al celui care îl deschide primul, iar doi nu încap.</translation>
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
        <translation>niciuna</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="894" />
        <source>pari</source>
        <translation>pară</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="895" />
        <source>dispari</source>
        <translation>impară</translation>
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
        <translation>niciunul</translation>
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
        <translation>Oferă CAT telefonului</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="906" />
        <location filename="../main.cpp" line="1463" />
        <source>CAT spento</source>
        <translation>CAT oprit</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="909" />
        <source>(nessuna: non trasmettere)</source>
        <translation>(niciuna: nu transmite)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="917" />
        <source>Radio / protocollo</source>
        <translation>Radio / protocol</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="918" />
        <source>Indirizzo CI-V</source>
        <translation>Adresă CI-V</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="919" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>Adresa la care radioul răspunde pe magistrala CI-V.
IC-7300: 0x94 (valoare din fabrică). Dacă a fost schimbată în
meniurile radioului, scrie aici aceeași valoare.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="924" />
        <source>Audio al rig</source>
        <translation>Audio către radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="931" />
        <source>Porta rig</source>
        <translation>Portul radioului</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="936" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="941" />
        <source>Velocità</source>
        <translation>Viteză</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="948" />
        <source>dati</source>
        <translation>date</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="952" />
        <source>parità</source>
        <translation>paritate</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="956" />
        <source>stop</source>
        <translation>stop</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="960" />
        <source>Seriale</source>
        <translation>Serial</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="961" />
        <source>Handshake</source>
        <translation>Control flux</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="990" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>server de autentificare (ex. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="992" />
        <source>la tua email</source>
        <translation>emailul tău</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="995" />
        <source>password</source>
        <translation>parolă</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="996" />
        <source>ricorda la password</source>
        <translation>reține parola</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="997" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>Se salvează în clar în setările Windows: merită doar pe un calculator în care ai încredere.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="999" />
        <source>Accedi</source>
        <translation>Autentificare</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1000" />
        <source>non collegato</source>
        <translation>neconectat</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1010" />
        <source>Server</source>
        <translation>Server</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1016" />
        <source>Accesso</source>
        <translation>Autentificare</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1037" />
        <source>versione di Decolink</source>
        <translation>versiunea Decolink</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1045" />
        <source>lingua dell'interfaccia</source>
        <translation>limba interfeței</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1062" />
        <source>COLLEGAMENTO</source>
        <translation>CONEXIUNE</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1070" />
        <source>RADIO E CAT</source>
        <translation>RADIO ȘI CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1093" />
        <source>livello audio</source>
        <translation>nivel audio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1148" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>eșantionare la %1 kHz: dacă telefonul îl aude accelerat, revino la 48</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1252" />
        <location filename="../main.cpp" line="1260" />
        <source>Lingua</source>
        <translation>Limbă</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1253" />
        <source>Il collegamento è aperto: la lingua cambia alla prossima apertura del programma.</source>
        <translation>Legătura este deschisă: limba se schimbă la următoarea pornire a programului.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1261" />
        <source>Decolink si riavvia per cambiare lingua. Procedo?</source>
        <translation>Decolink repornește pentru a schimba limba. Continui?</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1285" />
        <source>IP del telefono sulla rete locale</source>
        <translation>IP-ul telefonului în rețeaua locală</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1288" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>gazda releului (ex. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1291" />
        <source>(il telefono chiama questa porta)</source>
        <translation>(telefonul sună la acest port)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1302" />
        <source>manca il server di accesso</source>
        <translation>lipsește serverul de autentificare</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1304" />
        <source>servono email e password</source>
        <translation>sunt necesare emailul și parola</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1326" />
        <source>accesso in corso…</source>
        <translation>se autentifică…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1346" />
        <source>risposta incomprensibile dal server</source>
        <translation>răspuns neinteligibil de la server</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1383" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — stația %2, ca %3%4</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1406" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1442" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>credențiale expirate: mă autentific din nou</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1445" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>neautentificat: apasă Autentificare, apoi Pornește</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1475" />
        <source>nessuna porta seriale</source>
        <translation>niciun port serial</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1484" />
        <source>indirizzo CI-V non valido</source>
        <translation>adresă CI-V nevalidă</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1493" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>lipsește adresa programului care deține radioul</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1510" />
        <source>qui c'è Decolink stesso: scegli il programma che tiene davvero la radio, o cambia la porta TCP qui sotto</source>
        <translation>aici e chiar Decolink: alege programul care ține cu adevărat radioul, sau schimbă portul TCP de mai jos</translation>
    </message>
    <message>
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>portul TCP %1 este același la care te conectezi: schimbă-l pe unul</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1526" />
        <source>%1 non risponde: %2</source>
        <translation>%1 nu răspunde: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1539" />
        <source>%1 non si apre: %2</source>
        <translation>%1 nu se deschide: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1547" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>portul TCP %1 este ocupat (rulează deja rigctld?)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1595" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>radio: %1 MHz  %2   (TCP %3, și pe canalul audio)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1614" />
        <source>il programma che tiene la radio ha smesso di rispondere — riaccendi il CAT quando è tornato</source>
        <translation>programul care ține radioul a încetat să răspundă — repornește CAT când revine</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1616" />
        <source>rig non risponde sulla seriale</source>
        <translation>radioul nu răspunde pe portul serial</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1644" />
        <source>telefono connesso da %1:%2</source>
        <translation>telefon conectat de la %1:%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1694" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>credențialele trebuie reînnoite: mă autentific din nou</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1698" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>releul a refuzat conexiunea: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1706" />
        <source>il telefono è entrato nella stanza</source>
        <translation>telefonul a intrat în cameră</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1708" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>înregistrat pe releu ca %1 (%2)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1815" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>telefonul citește pachetele grupate: lățime de bandă redusă</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1837" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>profil cerut de telefon: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2131" />
        <location filename="../main.cpp" line="2312" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>%1 nu acceptă 48 kHz mono 16 biți</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2139" />
        <source>trasmissione dal telefono in corso</source>
        <translation>se transmite de pe telefon</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2150" />
        <source>trasmissione finita</source>
        <translation>transmisie încheiată</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2201" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>înregistrat, dar nu mai e nimeni în stație: telefonul încă nu a intrat</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2204" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>atenție: profilul %1, dar telefonul nu a confirmat că îl poate citi — dacă nu auzi nimic, treci la PCM 48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2218" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>telefonul nu mai este accesibil — aștept să sune din nou</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2260" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Opus nu pornește (%1): rămân pe PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2276" />
        <source>manca l'host di destinazione</source>
        <translation>lipsește gazda de destinație</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2279" />
        <source>nome non risolto: %1</source>
        <translation>nume nerezolvat: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2284" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>autentifică-te mai întâi: releul nu acceptă conexiuni fără credențiale</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2294" />
        <source>porta %1 non disponibile</source>
        <translation>portul %1 nu este disponibil</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2308" />
        <source>nessun ingresso audio</source>
        <translation>nicio intrare audio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2317" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>nu se poate deschide intrarea audio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2321" />
        <source>Ferma</source>
        <translation>Oprește</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2325" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>ascult pe portul %1 — aștept telefonul</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2376" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>profil readus la PCM 48 kHz: profilurile comprimate necesită un telefon actualizat</translation>
    </message>
</context>
<context>
    <name>QObject</name>
    <message>
        <location filename="../hamlibrig.h" line="184" />
        <source>errore %1 di Hamlib</source>
        <translation>eroare Hamlib %1</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="270" />
        <source>indirizzo vuoto</source>
        <translation>adresă goală</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="279" />
        <source>nessuna risposta da %1:%2</source>
        <translation>niciun răspuns de la %1:%2</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="280" />
        <source>%1:%2 — %3</source>
        <translation>%1:%2 — %3</translation>
    </message>
</context>
</TS>