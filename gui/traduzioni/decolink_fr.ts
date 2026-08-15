<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="fr">
<context>
    <name>Client</name>
    <message>
        <location filename="../main.cpp" line="548" />
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — la radio sur Decodium Mobile</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="555" />
        <source>LAN diretta</source>
        <translation>LAN direct</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="556" />
        <source>Relay + stazione</source>
        <translation>Relais + station</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="557" />
        <source>Il telefono chiama casa</source>
        <translation>Le téléphone appelle la maison</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="558" />
        <source>LAN diretta — il telefono è sulla stessa rete: gli si manda l'audio all'indirizzo
Relay + stazione — funziona ovunque, anche su dati mobili: PC e telefono
   escono entrambi verso il relay, quindi non c'è nessun router da configurare
Il telefono chiama casa — porta inoltrata sul router e nome DynDNS</source>
        <translation>LAN direct — le téléphone est sur le même réseau : l'audio va à son adresse
Relais + station — fonctionne partout, même en données mobiles : PC et
   téléphone sortent tous deux vers le relais, aucun routeur à configurer
Le téléphone appelle la maison — port redirigé sur le routeur et nom DynDNS</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="565" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>IP du téléphone, ou hôte du relais</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="569" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(connectez-vous pour choisir la station)</translation>
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
        <translation>Combien d'échantillons par seconde envoyer.
48 kHz — 808 kbit/s, 364 Mo par heure : sûr avec tout programme
24 kHz — 424 kbit/s, 191 Mo par heure
12 kHz — 232 kbit/s, 104 Mo par heure : largement suffisant pour la BLU,
qui n'occupe que 2,7 kHz.

Si le téléphone l'entend accéléré, il ignore la fréquence déclarée :
revenez à 48 kHz.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="606" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="607" />
        <source>Voce (Opus)</source>
        <translation>Voix (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="608" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="609" />
        <source>Digitali senza perdite</source>
        <translation>Modes numériques, sans perte</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="610" />
        <source>CW a tasto</source>
        <translation>Manipulation CW seule</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="611" />
        <source>PCM — compatibile con tutti, nessuna compressione
Voce — Opus a 32 kbit/s: serve un programma aggiornato dall'altra parte
CW — Opus a banda stretta, 20 kbit/s
Digitali — compresso senza perdere un bit, 146 kbit/s
CW a tasto — solo il ritmo del tasto, 2,4 kbit/s: si perde
tutto il contesto (QSB, QRM, chi chiama fuori nota)</source>
        <translation>PCM — fonctionne avec tout, aucune compression
Voix — Opus à 32 kbit/s : nécessite un programme à jour en face
CW — Opus à bande étroite, 20 kbit/s
Numérique — compressé sans perdre un bit, 146 kbit/s
Manipulation CW — seulement le rythme, 2,4 kbit/s : on perd
tout le contexte (QSB, QRM, ceux qui appellent hors fréquence)</translation>
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
        <translation>Combien de trames par paquet : moins de paquets, moins d'en-têtes
à payer, mais un peu plus de retard.
20 ms — latence minimale
40 ms — 18% de bande passante en moins, retard imperceptible
60 ms — 24% en moins, pour les forfaits limités</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="639" />
        <source>Audio radio</source>
        <translation>Audio radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="640" />
        <source>Modalità</source>
        <translation>Mode</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="641" />
        <source>Host</source>
        <translation>Hôte</translation>
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
        <translation>Échantillonnage</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="662" />
        <source>Pacchetti da</source>
        <translation>Durée des paquets</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="668" />
        <location filename="../main.cpp" line="674" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  Réglages avancés</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="673" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  Réglages avancés</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="680" />
        <location filename="../main.cpp" line="2067" />
        <source>Avvia</source>
        <translation>Démarrer</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="686" />
        <location filename="../main.cpp" line="2069" />
        <source>fermo</source>
        <translation>arrêté</translation>
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
        <translation>Hamlib %1 — %2 modèles reconnus.
Les deux premiers sont les protocoles écrits dans Decolink ;
les autres passent par Hamlib, la même bibliothèque qu'utilise
Decodium sur le bureau.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="725" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>hôte:port du programme qui détient la radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="727" />
        <source>Indirizzo del programma che tiene la porta seriale.
rigctld e i programmi compatibili: localhost:4532
FLRig: localhost:12345

Serve quando la COM è già occupata da un altro programma:
la porta seriale è di chi la apre per primo, e in due non
ci si sta.</source>
        <translation>Adresse du programme qui détient le port série.
rigctld et programmes compatibles : localhost:4532
FLRig : localhost:12345

Utile quand le port COM est déjà pris par un autre programme :
le port série appartient à celui qui l'ouvre en premier, et on
n'y tient pas à deux.</translation>
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
        <translation>aucune</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="747" />
        <source>pari</source>
        <translation>paire</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="748" />
        <source>dispari</source>
        <translation>impaire</translation>
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
        <translation>aucun</translation>
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
        <translation>Fournir le CAT au téléphone</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="759" />
        <location filename="../main.cpp" line="1238" />
        <source>CAT spento</source>
        <translation>CAT désactivé</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="762" />
        <source>(nessuna: non trasmettere)</source>
        <translation>(aucune : ne pas émettre)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="770" />
        <source>Radio / protocollo</source>
        <translation>Radio / protocole</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="771" />
        <source>Indirizzo CI-V</source>
        <translation>Adresse CI-V</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="772" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>L'adresse à laquelle la radio répond sur le bus CI-V.
IC-7300 : 0x94 (valeur d'usine). Si elle a été modifiée dans
les menus de la radio, indiquez la même valeur ici.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="777" />
        <source>Audio al rig</source>
        <translation>Audio vers la radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="784" />
        <source>Porta rig</source>
        <translation>Port de la radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="789" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="794" />
        <source>Velocità</source>
        <translation>Vitesse</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="801" />
        <source>dati</source>
        <translation>données</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="805" />
        <source>parità</source>
        <translation>parité</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="809" />
        <source>stop</source>
        <translation>stop</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="813" />
        <source>Seriale</source>
        <translation>Série</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="814" />
        <source>Handshake</source>
        <translation>Contrôle de flux</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="843" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>serveur de connexion (ex. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="845" />
        <source>la tua email</source>
        <translation>votre e-mail</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="848" />
        <source>password</source>
        <translation>mot de passe</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="849" />
        <source>ricorda la password</source>
        <translation>retenir le mot de passe</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="850" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>Enregistré en clair dans les réglages de Windows : à faire seulement sur un ordinateur de confiance.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="852" />
        <source>Accedi</source>
        <translation>Se connecter</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="853" />
        <source>non collegato</source>
        <translation>non connecté</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="863" />
        <source>Server</source>
        <translation>Serveur</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="869" />
        <source>Accesso</source>
        <translation>Connexion</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="891" />
        <source>COLLEGAMENTO</source>
        <translation>CONNEXION</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="899" />
        <source>RADIO E CAT</source>
        <translation>RADIO ET CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="922" />
        <source>livello audio</source>
        <translation>niveau audio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="977" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>échantillonnage à %1 kHz : si le téléphone l'entend accéléré, revenez à 48</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1060" />
        <source>IP del telefono sulla rete locale</source>
        <translation>IP du téléphone sur le réseau local</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1063" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>hôte du relais (ex. decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1066" />
        <source>(il telefono chiama questa porta)</source>
        <translation>(le téléphone appelle ce port)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1077" />
        <source>manca il server di accesso</source>
        <translation>il manque le serveur de connexion</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1079" />
        <source>servono email e password</source>
        <translation>e-mail et mot de passe sont requis</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1101" />
        <source>accesso in corso…</source>
        <translation>connexion en cours…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1121" />
        <source>risposta incomprensibile dal server</source>
        <translation>réponse incompréhensible du serveur</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1158" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — station %2, en tant que %3%4</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1181" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1217" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>identifiants expirés : je me reconnecte</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1220" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>non connecté : appuyez sur Se connecter, puis Démarrer</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1250" />
        <source>nessuna porta seriale</source>
        <translation>aucun port série</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1259" />
        <source>indirizzo CI-V non valido</source>
        <translation>adresse CI-V non valide</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1268" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>adresse manquante du programme qui détient la radio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1280" />
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>le port TCP %1 est celui auquel vous vous connectez : changez-en un</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1296" />
        <source>%1 non risponde: %2</source>
        <translation>%1 ne répond pas : %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1309" />
        <source>%1 non si apre: %2</source>
        <translation>%1 ne s'ouvre pas : %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1317" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>port TCP %1 occupé (rigctld est-il déjà lancé ?)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1345" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>radio : %1 MHz  %2   (TCP %3, et sur le canal audio)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1375" />
        <source>telefono connesso da %1:%2</source>
        <translation>téléphone connecté depuis %1:%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1425" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>identifiants à renouveler : je me reconnecte</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1429" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>le relais a refusé la connexion : %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1437" />
        <source>il telefono è entrato nella stanza</source>
        <translation>le téléphone a rejoint la salle</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1439" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>enregistré sur le relais en tant que %1 (%2)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1546" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>le téléphone lit les paquets groupés : bande passante réduite</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1568" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>profil demandé par le téléphone : %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1862" />
        <location filename="../main.cpp" line="2043" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>%1 ne prend pas en charge 48 kHz mono 16 bits</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1870" />
        <source>trasmissione dal telefono in corso</source>
        <translation>émission depuis le téléphone en cours</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1881" />
        <source>trasmissione finita</source>
        <translation>émission terminée</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1932" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>enregistré, mais personne d'autre dans la station : le téléphone n'est pas encore entré</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1935" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>attention : profil %1, mais le téléphone n'a pas confirmé qu'il sait le lire — si vous n'entendez rien, passez à PCM 48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1949" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>téléphone injoignable — j'attends qu'il rappelle</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1991" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Opus ne démarre pas (%1) : je reste en PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2007" />
        <source>manca l'host di destinazione</source>
        <translation>l'hôte de destination manque</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2010" />
        <source>nome non risolto: %1</source>
        <translation>nom non résolu : %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2015" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>connectez-vous d'abord : le relais n'accepte pas de connexion sans identifiants</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2025" />
        <source>porta %1 non disponibile</source>
        <translation>port %1 non disponible</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2039" />
        <source>nessun ingresso audio</source>
        <translation>aucune entrée audio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2048" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>impossible d'ouvrir l'entrée audio</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2052" />
        <source>Ferma</source>
        <translation>Arrêter</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2056" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>à l'écoute sur le port %1 — j'attends le téléphone</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2107" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>profil ramené à PCM 48 kHz : les profils compressés exigent un téléphone à jour</translation>
    </message>
</context>
</TS>