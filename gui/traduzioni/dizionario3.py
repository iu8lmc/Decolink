#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Terza parte: i suggerimenti lunghi.

Sono quelli che spiegano le scelte — quanta banda costa un profilo, perche' la
porta seriale non si condivide, cosa si perde con il CW a solo ritmo. Tradurli
male vale meno che non tradurli, perche' e' li' che l'utente decide.

Gli a capo vanno rispettati: in un suggerimento sono la formattazione.
"""

T3 = {}

_MODI = {
 "en": ("Direct LAN — the phone is on the same network: audio goes to its address\n"
        "Relay + station — works anywhere, mobile data included: PC and phone\n"
        "   both reach out to the relay, so there is no router to configure\n"
        "The phone calls home — forwarded port on the router and a DynDNS name"),
 "de": ("Direktes LAN — das Telefon ist im selben Netz: Audio geht an seine Adresse\n"
        "Relay + Station — funktioniert überall, auch mobil: PC und Telefon\n"
        "   verbinden sich beide zum Relay, also kein Router zu konfigurieren\n"
        "Das Telefon ruft zu Hause an — Portweiterleitung im Router und DynDNS-Name"),
 "fr": ("LAN direct — le téléphone est sur le même réseau : l'audio va à son adresse\n"
        "Relais + station — fonctionne partout, même en données mobiles : PC et\n"
        "   téléphone sortent tous deux vers le relais, aucun routeur à configurer\n"
        "Le téléphone appelle la maison — port redirigé sur le routeur et nom DynDNS"),
 "es": ("LAN directa — el teléfono está en la misma red: el audio va a su dirección\n"
        "Relé + estación — funciona en cualquier sitio, también con datos móviles:\n"
        "   PC y teléfono salen hacia el relé, no hay router que configurar\n"
        "El teléfono llama a casa — puerto redirigido en el router y nombre DynDNS"),
 "pt": ("LAN direta — o telemóvel está na mesma rede: o áudio vai para o seu endereço\n"
        "Relé + estação — funciona em qualquer lado, mesmo em dados móveis: PC e\n"
        "   telemóvel saem ambos para o relé, não há router para configurar\n"
        "O telemóvel liga para casa — porta encaminhada no router e nome DynDNS"),
 "nl": ("Direct LAN — de telefoon zit op hetzelfde netwerk: audio gaat naar zijn adres\n"
        "Relay + station — werkt overal, ook op mobiele data: pc en telefoon gaan\n"
        "   allebei naar de relay, dus geen router om in te stellen\n"
        "De telefoon belt naar huis — doorgestuurde poort op de router en DynDNS-naam"),
 "ca": ("LAN directa — el telèfon és a la mateixa xarxa: l'àudio va a la seva adreça\n"
        "Relé + estació — funciona a tot arreu, també amb dades mòbils: PC i telèfon\n"
        "   surten tots dos cap al relé, així no hi ha cap encaminador a configurar\n"
        "El telèfon truca a casa — port redirigit a l'encaminador i nom DynDNS"),
 "da": ("Direkte LAN — telefonen er på samme net: lyden sendes til dens adresse\n"
        "Relæ + station — virker overalt, også på mobildata: pc og telefon går\n"
        "   begge ud til relæet, så der er ingen router at sætte op\n"
        "Telefonen ringer hjem — videresendt port på routeren og et DynDNS-navn"),
 "hu": ("Közvetlen LAN — a telefon ugyanazon a hálózaton van: a hang a címére megy\n"
        "Relé + állomás — mindenhol működik, mobilneten is: a PC és a telefon\n"
        "   egyaránt a reléhez csatlakozik, így nincs router, amit beállítani kell\n"
        "A telefon hívja az otthont — átirányított port a routeren és DynDNS-név"),
 "ro": ("LAN direct — telefonul e în aceeași rețea: audio merge la adresa lui\n"
        "Releu + stație — merge oriunde, inclusiv pe date mobile: PC-ul și telefonul\n"
        "   ies amândouă spre releu, deci nu e niciun router de configurat\n"
        "Telefonul sună acasă — port redirecționat pe router și nume DynDNS"),
 "lv": ("Tiešs LAN — telefons ir tajā pašā tīklā: audio tiek sūtīts uz tā adresi\n"
        "Relejs + stacija — darbojas visur, arī mobilajos datos: dators un telefons\n"
        "   abi savienojas ar releju, tāpēc nav jākonfigurē neviens maršrutētājs\n"
        "Telefons zvana uz mājām — pāradresēts ports maršrutētājā un DynDNS vārds"),
 "ru": ("Прямая локальная сеть — телефон в той же сети: звук идёт на его адрес\n"
        "Ретранслятор + станция — работает везде, в том числе в мобильной сети:\n"
        "   ПК и телефон оба подключаются к ретранслятору, роутер настраивать не нужно\n"
        "Телефон звонит домой — проброшенный порт на роутере и имя DynDNS"),
 "ja": ("LAN 直結 — スマートフォンが同じネットワーク上: その IP へ音声を送ります\n"
        "リレー + 局 — どこでも動作し、モバイル回線でも可: PC もスマートフォンも\n"
        "   リレーへ発信するので、ルーターの設定は不要です\n"
        "スマートフォンから接続 — ルーターのポート転送と DynDNS 名が必要"),
 "zh": ("局域网直连 — 手机在同一网络：音频直接发到它的地址\n"
        "中继 + 电台 — 到处可用，移动数据也行：电脑和手机都向中继发起连接，\n"
        "   因此不需要配置路由器\n"
        "手机主动回连 — 需要路由器端口转发和 DynDNS 名称"),
 "zh_TW": ("區域網路直連 — 手機在同一網路：音訊直接送到它的位址\n"
           "中繼 + 電台 — 到處可用，行動數據也行：電腦和手機都向中繼發起連線，\n"
           "   因此不需要設定路由器\n"
           "手機主動回連 — 需要路由器連接埠轉發和 DynDNS 名稱"),
}
T3["LAN diretta — il telefono è sulla stessa rete: gli si manda l'audio all'indirizzo\n"
   "Relay + stazione — funziona ovunque, anche su dati mobili: PC e telefono\n"
   "   escono entrambi verso il relay, quindi non c'è nessun router da configurare\n"
   "Il telefono chiama casa — porta inoltrata sul router e nome DynDNS"] = _MODI

_CAMP = {
 "en": ("How many samples per second to send.\n"
        "48 kHz — 808 kbit/s, 364 MB per hour: safe with any program\n"
        "24 kHz — 424 kbit/s, 191 MB per hour\n"
        "12 kHz — 232 kbit/s, 104 MB per hour: plenty for SSB,\n"
        "which only occupies 2.7 kHz.\n\n"
        "If the phone plays it sped up, it is ignoring the declared\n"
        "sample rate: go back to 48 kHz."),
 "de": ("Wie viele Abtastwerte pro Sekunde gesendet werden.\n"
        "48 kHz — 808 kbit/s, 364 MB pro Stunde: sicher mit jedem Programm\n"
        "24 kHz — 424 kbit/s, 191 MB pro Stunde\n"
        "12 kHz — 232 kbit/s, 104 MB pro Stunde: reichlich für SSB,\n"
        "das nur 2,7 kHz belegt.\n\n"
        "Klingt es am Telefon zu schnell, wird die angegebene Abtastrate\n"
        "ignoriert: zurück auf 48 kHz."),
 "fr": ("Combien d'échantillons par seconde envoyer.\n"
        "48 kHz — 808 kbit/s, 364 Mo par heure : sûr avec tout programme\n"
        "24 kHz — 424 kbit/s, 191 Mo par heure\n"
        "12 kHz — 232 kbit/s, 104 Mo par heure : largement suffisant pour la BLU,\n"
        "qui n'occupe que 2,7 kHz.\n\n"
        "Si le téléphone l'entend accéléré, il ignore la fréquence déclarée :\n"
        "revenez à 48 kHz."),
 "es": ("Cuántas muestras por segundo enviar.\n"
        "48 kHz — 808 kbit/s, 364 MB por hora: seguro con cualquier programa\n"
        "24 kHz — 424 kbit/s, 191 MB por hora\n"
        "12 kHz — 232 kbit/s, 104 MB por hora: de sobra para SSB,\n"
        "que solo ocupa 2,7 kHz.\n\n"
        "Si el teléfono lo oye acelerado, está ignorando el muestreo\n"
        "declarado: vuelve a 48 kHz."),
 "pt": ("Quantas amostras por segundo enviar.\n"
        "48 kHz — 808 kbit/s, 364 MB por hora: seguro com qualquer programa\n"
        "24 kHz — 424 kbit/s, 191 MB por hora\n"
        "12 kHz — 232 kbit/s, 104 MB por hora: mais do que suficiente para SSB,\n"
        "que só ocupa 2,7 kHz.\n\n"
        "Se o telemóvel o ouvir acelerado, está a ignorar a amostragem\n"
        "declarada: volte a 48 kHz."),
 "nl": ("Hoeveel samples per seconde verzonden worden.\n"
        "48 kHz — 808 kbit/s, 364 MB per uur: veilig met elk programma\n"
        "24 kHz — 424 kbit/s, 191 MB per uur\n"
        "12 kHz — 232 kbit/s, 104 MB per uur: ruim genoeg voor SSB,\n"
        "dat maar 2,7 kHz beslaat.\n\n"
        "Klinkt het op de telefoon versneld, dan negeert die de opgegeven\n"
        "bemonstering: ga terug naar 48 kHz."),
 "ca": ("Quantes mostres per segon enviar.\n"
        "48 kHz — 808 kbit/s, 364 MB per hora: segur amb qualsevol programa\n"
        "24 kHz — 424 kbit/s, 191 MB per hora\n"
        "12 kHz — 232 kbit/s, 104 MB per hora: de sobres per a SSB,\n"
        "que només ocupa 2,7 kHz.\n\n"
        "Si el telèfon el sent accelerat, ignora el mostreig declarat:\n"
        "torna a 48 kHz."),
 "da": ("Hvor mange samples i sekundet der sendes.\n"
        "48 kHz — 808 kbit/s, 364 MB i timen: sikkert med ethvert program\n"
        "24 kHz — 424 kbit/s, 191 MB i timen\n"
        "12 kHz — 232 kbit/s, 104 MB i timen: rigeligt til SSB,\n"
        "der kun fylder 2,7 kHz.\n\n"
        "Lyder det for hurtigt på telefonen, ignorerer den den angivne\n"
        "samplerate: gå tilbage til 48 kHz."),
 "hu": ("Hány mintát küldjön másodpercenként.\n"
        "48 kHz — 808 kbit/s, 364 MB óránként: minden programmal biztonságos\n"
        "24 kHz — 424 kbit/s, 191 MB óránként\n"
        "12 kHz — 232 kbit/s, 104 MB óránként: bőven elég az SSB-hez,\n"
        "amely csak 2,7 kHz-et foglal.\n\n"
        "Ha a telefonon felgyorsítva szól, figyelmen kívül hagyja a megadott\n"
        "mintavételezést: térjen vissza 48 kHz-re."),
 "ro": ("Câte eșantioane pe secundă să trimită.\n"
        "48 kHz — 808 kbit/s, 364 MB pe oră: sigur cu orice program\n"
        "24 kHz — 424 kbit/s, 191 MB pe oră\n"
        "12 kHz — 232 kbit/s, 104 MB pe oră: mai mult decât suficient pentru SSB,\n"
        "care ocupă doar 2,7 kHz.\n\n"
        "Dacă telefonul îl aude accelerat, ignoră eșantionarea declarată:\n"
        "revino la 48 kHz."),
 "lv": ("Cik paraugu sekundē sūtīt.\n"
        "48 kHz — 808 kbit/s, 364 MB stundā: droši ar jebkuru programmu\n"
        "24 kHz — 424 kbit/s, 191 MB stundā\n"
        "12 kHz — 232 kbit/s, 104 MB stundā: pilnīgi pietiek SSB,\n"
        "kas aizņem tikai 2,7 kHz.\n\n"
        "Ja telefonā skan paātrināti, tas ignorē norādīto iztveršanas\n"
        "frekvenci: atgriezieties uz 48 kHz."),
 "ru": ("Сколько отсчётов в секунду передавать.\n"
        "48 кГц — 808 кбит/с, 364 МБ в час: безопасно с любой программой\n"
        "24 кГц — 424 кбит/с, 191 МБ в час\n"
        "12 кГц — 232 кбит/с, 104 МБ в час: с запасом хватает для SSB,\n"
        "который занимает всего 2,7 кГц.\n\n"
        "Если на телефоне звук ускорен, он не читает объявленную частоту\n"
        "дискретизации: вернитесь на 48 кГц."),
 "ja": ("1 秒あたり何サンプル送るか。\n"
        "48 kHz — 808 kbit/s、1 時間 364 MB: どのプログラムでも安全\n"
        "24 kHz — 424 kbit/s、1 時間 191 MB\n"
        "12 kHz — 232 kbit/s、1 時間 104 MB: 帯域 2.7 kHz の SSB には十分すぎます。\n\n"
        "スマートフォンで速く聞こえる場合、宣言したサンプリング周波数を\n"
        "読んでいません: 48 kHz に戻してください。"),
 "zh": ("每秒发送多少采样。\n"
        "48 kHz — 808 kbit/s，每小时 364 MB：对任何程序都安全\n"
        "24 kHz — 424 kbit/s，每小时 191 MB\n"
        "12 kHz — 232 kbit/s，每小时 104 MB：对只占 2.7 kHz 的 SSB 绰绰有余。\n\n"
        "如果手机听起来变快，说明它没有读取声明的采样率：请改回 48 kHz。"),
 "zh_TW": ("每秒傳送多少取樣。\n"
           "48 kHz — 808 kbit/s，每小時 364 MB：對任何程式都安全\n"
           "24 kHz — 424 kbit/s，每小時 191 MB\n"
           "12 kHz — 232 kbit/s，每小時 104 MB：對只占 2.7 kHz 的 SSB 綽綽有餘。\n\n"
           "如果手機聽起來變快，表示它沒有讀取宣告的取樣率：請改回 48 kHz。"),
}
T3["Quanti campioni al secondo mandare.\n"
   "48 kHz — 808 kbit/s, 364 MB l'ora: sicuro con qualunque programma\n"
   "24 kHz — 424 kbit/s, 191 MB l'ora\n"
   "12 kHz — 232 kbit/s, 104 MB l'ora: basta e avanza per un SSB,\n"
   "che di banda ne occupa 2,7 kHz.\n\n"
   "Se il telefono lo sente accelerato, non legge la frequenza\n"
   "dichiarata: torna a 48 kHz."] = _CAMP

_PROF = {
 "en": ("PCM — works with everything, no compression\n"
        "Voice — Opus at 32 kbit/s: needs an updated program at the other end\n"
        "CW — narrow-band Opus, 20 kbit/s\n"
        "Digital — compressed without losing a bit, 146 kbit/s\n"
        "CW keying — only the keying rhythm, 2.4 kbit/s: you lose\n"
        "all the context (QSB, QRM, anyone calling off frequency)"),
 "de": ("PCM — funktioniert mit allem, keine Kompression\n"
        "Sprache — Opus mit 32 kbit/s: erfordert ein aktuelles Programm auf der Gegenseite\n"
        "CW — schmalbandiges Opus, 20 kbit/s\n"
        "Digimodes — verlustfrei komprimiert, 146 kbit/s\n"
        "CW-Tastung — nur der Rhythmus, 2,4 kbit/s: der ganze Kontext geht\n"
        "verloren (QSB, QRM, wer neben der Frequenz ruft)"),
 "fr": ("PCM — fonctionne avec tout, aucune compression\n"
        "Voix — Opus à 32 kbit/s : nécessite un programme à jour en face\n"
        "CW — Opus à bande étroite, 20 kbit/s\n"
        "Numérique — compressé sans perdre un bit, 146 kbit/s\n"
        "Manipulation CW — seulement le rythme, 2,4 kbit/s : on perd\n"
        "tout le contexte (QSB, QRM, ceux qui appellent hors fréquence)"),
 "es": ("PCM — funciona con todo, sin compresión\n"
        "Voz — Opus a 32 kbit/s: hace falta un programa actualizado al otro lado\n"
        "CW — Opus de banda estrecha, 20 kbit/s\n"
        "Digitales — comprimido sin perder un bit, 146 kbit/s\n"
        "Manipulación CW — solo el ritmo, 2,4 kbit/s: se pierde\n"
        "todo el contexto (QSB, QRM, quien llama fuera de frecuencia)"),
 "pt": ("PCM — funciona com tudo, sem compressão\n"
        "Voz — Opus a 32 kbit/s: exige um programa atualizado do outro lado\n"
        "CW — Opus de banda estreita, 20 kbit/s\n"
        "Digitais — comprimido sem perder um bit, 146 kbit/s\n"
        "Manipulação CW — só o ritmo, 2,4 kbit/s: perde-se\n"
        "todo o contexto (QSB, QRM, quem chama fora de frequência)"),
 "nl": ("PCM — werkt met alles, geen compressie\n"
        "Spraak — Opus op 32 kbit/s: vereist een bijgewerkt programma aan de andere kant\n"
        "CW — smalbandige Opus, 20 kbit/s\n"
        "Digitaal — verliesvrij gecomprimeerd, 146 kbit/s\n"
        "CW-seinen — alleen het ritme, 2,4 kbit/s: alle context gaat\n"
        "verloren (QSB, QRM, wie naast de frequentie roept)"),
 "ca": ("PCM — funciona amb tot, sense compressió\n"
        "Veu — Opus a 32 kbit/s: cal un programa actualitzat a l'altra banda\n"
        "CW — Opus de banda estreta, 20 kbit/s\n"
        "Digitals — comprimit sense perdre cap bit, 146 kbit/s\n"
        "Manipulació CW — només el ritme, 2,4 kbit/s: es perd\n"
        "tot el context (QSB, QRM, qui crida fora de freqüència)"),
 "da": ("PCM — virker med alt, ingen komprimering\n"
        "Tale — Opus ved 32 kbit/s: kræver et opdateret program i den anden ende\n"
        "CW — smalbåndet Opus, 20 kbit/s\n"
        "Digitale — komprimeret uden at miste en bit, 146 kbit/s\n"
        "CW-nøgling — kun rytmen, 2,4 kbit/s: hele konteksten går tabt\n"
        "(QSB, QRM, dem der kalder ved siden af frekvensen)"),
 "hu": ("PCM — mindennel működik, tömörítés nélkül\n"
        "Beszéd — Opus 32 kbit/s-en: frissített programot igényel a túloldalon\n"
        "CW — keskeny sávú Opus, 20 kbit/s\n"
        "Digitális — bitpontosan tömörítve, 146 kbit/s\n"
        "CW-billentyűzés — csak a ritmus, 2,4 kbit/s: elvész\n"
        "a teljes környezet (QSB, QRM, aki a frekvencia mellett hív)"),
 "ro": ("PCM — merge cu orice, fără compresie\n"
        "Voce — Opus la 32 kbit/s: necesită un program actualizat de cealaltă parte\n"
        "CW — Opus în bandă îngustă, 20 kbit/s\n"
        "Digitale — comprimat fără a pierde un bit, 146 kbit/s\n"
        "Manipulare CW — doar ritmul, 2,4 kbit/s: se pierde\n"
        "tot contextul (QSB, QRM, cine cheamă lângă frecvență)"),
 "lv": ("PCM — darbojas ar visu, bez saspiešanas\n"
        "Balss — Opus ar 32 kbit/s: otrā pusē vajadzīga atjaunināta programma\n"
        "CW — šaurjoslas Opus, 20 kbit/s\n"
        "Digitālie — saspiests, nezaudējot nevienu bitu, 146 kbit/s\n"
        "CW manipulācija — tikai ritms, 2,4 kbit/s: zūd viss\n"
        "konteksts (QSB, QRM, kas sauc blakus frekvencei)"),
 "ru": ("PCM — работает со всем, без сжатия\n"
        "Голос — Opus 32 кбит/с: на той стороне нужна обновлённая программа\n"
        "CW — узкополосный Opus, 20 кбит/с\n"
        "Цифровые — сжатие без потери единого бита, 146 кбит/с\n"
        "Манипуляция CW — только ритм, 2,4 кбит/с: теряется\n"
        "весь контекст (QSB, QRM, кто зовёт рядом по частоте)"),
 "ja": ("PCM — すべてと互換、圧縮なし\n"
        "音声 — Opus 32 kbit/s: 相手側に更新されたプログラムが必要\n"
        "CW — 狭帯域 Opus、20 kbit/s\n"
        "デジタル — 1 ビットも失わない圧縮、146 kbit/s\n"
        "CW キーイング — 打鍵のリズムのみ、2.4 kbit/s: 周囲の状況\n"
        "(QSB、QRM、周波数の外で呼ぶ局) はすべて失われます"),
 "zh": ("PCM — 与所有程序兼容，不压缩\n"
        "语音 — Opus 32 kbit/s：对端需要已更新的程序\n"
        "CW — 窄带 Opus，20 kbit/s\n"
        "数字模式 — 无损压缩，146 kbit/s\n"
        "CW 键控 — 仅键控节奏，2.4 kbit/s：会失去\n"
        "全部环境信息（QSB、QRM、在频率旁呼叫的人）"),
 "zh_TW": ("PCM — 與所有程式相容，不壓縮\n"
           "語音 — Opus 32 kbit/s：對端需要已更新的程式\n"
           "CW — 窄頻 Opus，20 kbit/s\n"
           "數位模式 — 無損壓縮，146 kbit/s\n"
           "CW 鍵控 — 僅鍵控節奏，2.4 kbit/s：會失去\n"
           "全部環境資訊（QSB、QRM、在頻率旁呼叫的人）"),
}
T3["PCM — compatibile con tutti, nessuna compressione\n"
   "Voce — Opus a 32 kbit/s: serve un programma aggiornato dall'altra parte\n"
   "CW — Opus a banda stretta, 20 kbit/s\n"
   "Digitali — compresso senza perdere un bit, 146 kbit/s\n"
   "CW a tasto — solo il ritmo del tasto, 2,4 kbit/s: si perde\n"
   "tutto il contesto (QSB, QRM, chi chiama fuori nota)"] = _PROF

_PACC = {
 "en": ("How many frames to put in one packet: fewer packets means fewer\n"
        "headers to pay for, but a little more delay.\n"
        "20 ms — lowest latency\n"
        "40 ms — 18% less bandwidth, imperceptible delay\n"
        "60 ms — 24% less, for metered connections"),
 "de": ("Wie viele Frames in ein Paket kommen: weniger Pakete bedeuten weniger\n"
        "Kopfdaten, dafür etwas mehr Verzögerung.\n"
        "20 ms — geringste Latenz\n"
        "40 ms — 18% weniger Bandbreite, nicht wahrnehmbare Verzögerung\n"
        "60 ms — 24% weniger, für Verbindungen mit Datenlimit"),
 "fr": ("Combien de trames par paquet : moins de paquets, moins d'en-têtes\n"
        "à payer, mais un peu plus de retard.\n"
        "20 ms — latence minimale\n"
        "40 ms — 18% de bande passante en moins, retard imperceptible\n"
        "60 ms — 24% en moins, pour les forfaits limités"),
 "es": ("Cuántas tramas poner en un paquete: menos paquetes, menos cabeceras\n"
        "que pagar, pero un poco más de retardo.\n"
        "20 ms — latencia mínima\n"
        "40 ms — 18% menos de ancho de banda, retardo imperceptible\n"
        "60 ms — 24% menos, para conexiones con límite de datos"),
 "pt": ("Quantas tramas colocar num pacote: menos pacotes, menos cabeçalhos\n"
        "a pagar, mas um pouco mais de atraso.\n"
        "20 ms — latência mínima\n"
        "40 ms — menos 18% de largura de banda, atraso impercetível\n"
        "60 ms — menos 24%, para ligações com limite de dados"),
 "nl": ("Hoeveel frames in één pakket: minder pakketten betekent minder\n"
        "headers te betalen, maar iets meer vertraging.\n"
        "20 ms — laagste latentie\n"
        "40 ms — 18% minder bandbreedte, onmerkbare vertraging\n"
        "60 ms — 24% minder, voor verbindingen met datalimiet"),
 "ca": ("Quantes trames posar en un paquet: menys paquets, menys capçaleres\n"
        "a pagar, però una mica més de retard.\n"
        "20 ms — latència mínima\n"
        "40 ms — 18% menys d'amplada de banda, retard imperceptible\n"
        "60 ms — 24% menys, per a connexions amb límit de dades"),
 "da": ("Hvor mange frames der lægges i én pakke: færre pakker betyder færre\n"
        "headere at betale for, men lidt mere forsinkelse.\n"
        "20 ms — laveste latenstid\n"
        "40 ms — 18% mindre båndbredde, umærkelig forsinkelse\n"
        "60 ms — 24% mindre, til forbindelser med datagrænse"),
 "hu": ("Hány keret kerüljön egy csomagba: kevesebb csomag kevesebb fejlécet\n"
        "jelent, de kicsit több késleltetést.\n"
        "20 ms — legkisebb késleltetés\n"
        "40 ms — 18%-kal kevesebb sávszélesség, észrevehetetlen késleltetés\n"
        "60 ms — 24%-kal kevesebb, korlátos kapcsolatokhoz"),
 "ro": ("Câte cadre să pună într-un pachet: mai puține pachete înseamnă mai\n"
        "puține antete de plătit, dar puțin mai multă întârziere.\n"
        "20 ms — latență minimă\n"
        "40 ms — cu 18% mai puțină lățime de bandă, întârziere imperceptibilă\n"
        "60 ms — cu 24% mai puțin, pentru conexiuni cu trafic limitat"),
 "lv": ("Cik kadru likt vienā paketē: mazāk pakešu nozīmē mazāk galvenu,\n"
        "par ko maksāt, bet nedaudz lielāku aizturi.\n"
        "20 ms — mazākā aizture\n"
        "40 ms — par 18% mazāks joslas platums, nemanāma aizture\n"
        "60 ms — par 24% mazāk, savienojumiem ar datu ierobežojumu"),
 "ru": ("Сколько кадров класть в один пакет: меньше пакетов — меньше\n"
        "заголовков, но чуть больше задержки.\n"
        "20 мс — наименьшая задержка\n"
        "40 мс — на 18% меньше полосы, задержка незаметна\n"
        "60 мс — на 24% меньше, для тарифов с лимитом"),
 "ja": ("1 パケットに何フレーム入れるか: パケットが少ないほどヘッダーの\n"
        "負担が減りますが、遅延が少し増えます。\n"
        "20 ms — 遅延最小\n"
        "40 ms — 帯域 18% 減、遅延は感じられません\n"
        "60 ms — 24% 減、従量制の回線向け"),
 "zh": ("每个包放多少帧：包越少，需要付出的包头越少，但延迟略增。\n"
        "20 ms — 延迟最小\n"
        "40 ms — 带宽减少 18%，延迟无法察觉\n"
        "60 ms — 减少 24%，适合按流量计费的网络"),
 "zh_TW": ("每個封包放多少幀：封包越少，需要付出的標頭越少，但延遲略增。\n"
           "20 ms — 延遲最小\n"
           "40 ms — 頻寬減少 18%，延遲無法察覺\n"
           "60 ms — 減少 24%，適合按流量計費的網路"),
}
T3["Quanti frame mettere in un pacchetto: meno pacchetti, meno\n"
   "intestazioni da pagare, ma un po' più di ritardo.\n"
   "20 ms — latenza minima\n"
   "40 ms — 18% di banda in meno, ritardo impercettibile\n"
   "60 ms — 24% in meno, per reti a consumo"] = _PACC

_HAM = {
 "en": ("Hamlib %1 — %2 models recognised.\nThe first two are the protocols written inside "
        "Decolink;\nthe others go through Hamlib, the same library used by\nDecodium on the desktop."),
 "de": ("Hamlib %1 — %2 erkannte Modelle.\nDie ersten beiden sind die in Decolink geschriebenen "
        "Protokolle;\ndie anderen laufen über Hamlib, dieselbe Bibliothek wie bei\nDecodium am Desktop."),
 "fr": ("Hamlib %1 — %2 modèles reconnus.\nLes deux premiers sont les protocoles écrits dans "
        "Decolink ;\nles autres passent par Hamlib, la même bibliothèque qu'utilise\nDecodium sur le bureau."),
 "es": ("Hamlib %1 — %2 modelos reconocidos.\nLos dos primeros son los protocolos escritos dentro "
        "de Decolink;\nlos demás pasan por Hamlib, la misma biblioteca que usa\nDecodium en el escritorio."),
 "pt": ("Hamlib %1 — %2 modelos reconhecidos.\nOs dois primeiros são os protocolos escritos dentro "
        "do Decolink;\nos outros passam pelo Hamlib, a mesma biblioteca que o\nDecodium usa no computador."),
 "nl": ("Hamlib %1 — %2 herkende modellen.\nDe eerste twee zijn de protocollen in Decolink zelf;\n"
        "de rest loopt via Hamlib, dezelfde bibliotheek die Decodium\nop de desktop gebruikt."),
 "ca": ("Hamlib %1 — %2 models reconeguts.\nEls dos primers són els protocols escrits dins del "
        "Decolink;\nla resta passen per Hamlib, la mateixa biblioteca que fa servir\nel Decodium a l'escriptori."),
 "da": ("Hamlib %1 — %2 genkendte modeller.\nDe to første er protokollerne skrevet i Decolink;\n"
        "de øvrige går gennem Hamlib, samme bibliotek som Decodium\nbruger på computeren."),
 "hu": ("Hamlib %1 — %2 felismert modell.\nAz első kettő a Decolinkba írt protokoll;\n"
        "a többi a Hamlibon keresztül megy, ugyanazon a könyvtáron,\namit a Decodium használ asztali gépen."),
 "ro": ("Hamlib %1 — %2 modele recunoscute.\nPrimele două sunt protocoalele scrise în Decolink;\n"
        "celelalte trec prin Hamlib, aceeași bibliotecă folosită de\nDecodium pe desktop."),
 "lv": ("Hamlib %1 — %2 atpazīti modeļi.\nPirmie divi ir Decolink iekšpusē rakstītie protokoli;\n"
        "pārējie iet caur Hamlib — to pašu bibliotēku, ko lieto\nDecodium uz datora."),
 "ru": ("Hamlib %1 — распознано моделей: %2.\nПервые две строки — протоколы, написанные внутри "
        "Decolink;\nостальные идут через Hamlib, ту же библиотеку, что использует\nDecodium на компьютере."),
 "ja": ("Hamlib %1 — %2 機種に対応。\n最初の 2 つは Decolink 内に書かれたプロトコルです。\n"
        "それ以外は Hamlib 経由で、デスクトップ版 Decodium と\n同じライブラリを使います。"),
 "zh": ("Hamlib %1 — 识别 %2 个型号。\n前两项是写在 Decolink 内部的协议；\n"
        "其余通过 Hamlib，与桌面版 Decodium 使用同一个库。"),
 "zh_TW": ("Hamlib %1 — 辨識 %2 個型號。\n前兩項是寫在 Decolink 內部的協定；\n"
           "其餘透過 Hamlib，與桌面版 Decodium 使用同一個函式庫。"),
}
T3["Hamlib %1 — %2 modelli riconosciuti.\nI primi due sono i protocolli scritti dentro Decolink;\n"
   "gli altri passano da Hamlib, la stessa libreria che usa\nDecodium sul desktop."] = _HAM

_RETE = {
 "en": ("Address of the program that holds the serial port.\nrigctld and compatible programs: "
        "localhost:4532\nFLRig: localhost:12345\n\nUse this when the COM port is already taken by "
        "another program:\nthe serial port belongs to whoever opens it first, and two\nprograms do not fit."),
 "de": ("Adresse des Programms, das die serielle Schnittstelle hält.\nrigctld und kompatible Programme: "
        "localhost:4532\nFLRig: localhost:12345\n\nNötig, wenn der COM-Port bereits von einem anderen "
        "Programm\nbelegt ist: die Schnittstelle gehört dem, der sie zuerst öffnet,\nund zu zweit passt man nicht hinein."),
 "fr": ("Adresse du programme qui détient le port série.\nrigctld et programmes compatibles : "
        "localhost:4532\nFLRig : localhost:12345\n\nUtile quand le port COM est déjà pris par un autre "
        "programme :\nle port série appartient à celui qui l'ouvre en premier, et on\nn'y tient pas à deux."),
 "es": ("Dirección del programa que tiene el puerto serie.\nrigctld y programas compatibles: "
        "localhost:4532\nFLRig: localhost:12345\n\nHace falta cuando el puerto COM ya lo ocupa otro "
        "programa:\nel puerto serie es de quien lo abre primero, y no caben dos."),
 "pt": ("Endereço do programa que detém a porta série.\nrigctld e programas compatíveis: "
        "localhost:4532\nFLRig: localhost:12345\n\nÉ preciso quando a porta COM já está ocupada por outro "
        "programa:\na porta série é de quem a abre primeiro, e não cabem dois."),
 "nl": ("Adres van het programma dat de seriële poort bezet.\nrigctld en compatibele programma's: "
        "localhost:4532\nFLRig: localhost:12345\n\nNodig als de COM-poort al door een ander programma "
        "bezet is:\nde seriële poort is van wie hem het eerst opent, en met z'n\ntweeën past het niet."),
 "ca": ("Adreça del programa que té el port sèrie.\nrigctld i programes compatibles: "
        "localhost:4532\nFLRig: localhost:12345\n\nCal quan el port COM ja l'ocupa un altre programa:\n"
        "el port sèrie és de qui l'obre primer, i no hi caben dos."),
 "da": ("Adressen på programmet der har den serielle port.\nrigctld og kompatible programmer: "
        "localhost:4532\nFLRig: localhost:12345\n\nBruges når COM-porten allerede er optaget af et andet "
        "program:\nden serielle port tilhører den der åbner den først, og der er\nikke plads til to."),
 "hu": ("A soros portot birtokló program címe.\nrigctld és kompatibilis programok: "
        "localhost:4532\nFLRig: localhost:12345\n\nAkkor kell, ha a COM portot már elfoglalta egy másik "
        "program:\na soros port azé, aki elsőként megnyitja, és ketten nem férnek el."),
 "ro": ("Adresa programului care deține portul serial.\nrigctld și programele compatibile: "
        "localhost:4532\nFLRig: localhost:12345\n\nEste necesară când portul COM e deja ocupat de alt "
        "program:\nportul serial e al celui care îl deschide primul, iar doi nu încap."),
 "lv": ("Programmas adrese, kas tur seriālo portu.\nrigctld un saderīgas programmas: "
        "localhost:4532\nFLRig: localhost:12345\n\nVajadzīga, kad COM portu jau aizņēmusi cita programma:\n"
        "seriālais ports pieder tam, kas to atver pirmais, un divi neietilpst."),
 "ru": ("Адрес программы, которая держит последовательный порт.\nrigctld и совместимые программы: "
        "localhost:4532\nFLRig: localhost:12345\n\nНужен, когда COM-порт уже занят другой программой:\n"
        "порт принадлежит тому, кто открыл его первым, и вдвоём туда не поместиться."),
 "ja": ("シリアルポートを保持しているプログラムのアドレス。\nrigctld および互換プログラム: "
        "localhost:4532\nFLRig: localhost:12345\n\nCOM ポートが別のプログラムに占有されている場合に使います。\n"
        "シリアルポートは先に開いた側のもので、2 つは同居できません。"),
 "zh": ("占用串口的程序地址。\nrigctld 及兼容程序：localhost:4532\nFLRig：localhost:12345\n\n"
        "当 COM 口已被其他程序占用时使用：\n串口属于先打开它的程序，两个程序无法共用。"),
 "zh_TW": ("占用序列埠的程式位址。\nrigctld 及相容程式：localhost:4532\nFLRig：localhost:12345\n\n"
           "當 COM 埠已被其他程式占用時使用：\n序列埠屬於先開啟它的程式，兩個程式無法共用。"),
}
T3["Indirizzo del programma che tiene la porta seriale.\nrigctld e i programmi compatibili: "
   "localhost:4532\nFLRig: localhost:12345\n\nServe quando la COM è già occupata da un altro programma:\n"
   "la porta seriale è di chi la apre per primo, e in due non\nci si sta."] = _RETE

_CIV = {
 "en": ("The address the rig answers to on the CI-V bus.\nIC-7300: 0x94 (factory default). If it was "
        "changed in the\nradio's menus, write the same value here."),
 "de": ("Die Adresse, unter der das Funkgerät am CI-V-Bus antwortet.\nIC-7300: 0x94 (Werkseinstellung). "
        "Wurde sie in den Menüs des\nGeräts geändert, hier denselben Wert eintragen."),
 "fr": ("L'adresse à laquelle la radio répond sur le bus CI-V.\nIC-7300 : 0x94 (valeur d'usine). Si elle "
        "a été modifiée dans\nles menus de la radio, indiquez la même valeur ici."),
 "es": ("La dirección con la que la radio responde en el bus CI-V.\nIC-7300: 0x94 (valor de fábrica). Si "
        "se cambió en los menús\nde la radio, escribe aquí el mismo valor."),
 "pt": ("O endereço com que o rádio responde no barramento CI-V.\nIC-7300: 0x94 (predefinição de fábrica). "
        "Se foi alterado nos\nmenus do rádio, escreva aqui o mesmo valor."),
 "nl": ("Het adres waarmee de set antwoordt op de CI-V-bus.\nIC-7300: 0x94 (fabrieksinstelling). Is het in "
        "de menu's van de\nradio gewijzigd, vul hier dezelfde waarde in."),
 "ca": ("L'adreça amb què la ràdio respon al bus CI-V.\nIC-7300: 0x94 (valor de fàbrica). Si s'ha canviat "
        "als menús\nde la ràdio, escriu-hi el mateix valor."),
 "da": ("Adressen som radioen svarer på over CI-V-bussen.\nIC-7300: 0x94 (fabriksindstilling). Er den "
        "ændret i radioens\nmenuer, skal samme værdi skrives her."),
 "hu": ("A cím, amelyen a rádió válaszol a CI-V buszon.\nIC-7300: 0x94 (gyári alapérték). Ha a rádió "
        "menüjében\nmegváltoztatták, ugyanazt az értéket kell ide írni."),
 "ro": ("Adresa la care radioul răspunde pe magistrala CI-V.\nIC-7300: 0x94 (valoare din fabrică). Dacă a "
        "fost schimbată în\nmeniurile radioului, scrie aici aceeași valoare."),
 "lv": ("Adrese, ar kuru radio atbild CI-V kopnē.\nIC-7300: 0x94 (rūpnīcas noklusējums). Ja tā mainīta "
        "radio\nizvēlnēs, šeit jāieraksta tā pati vērtība."),
 "ru": ("Адрес, по которому трансивер отвечает на шине CI-V.\nIC-7300: 0x94 (заводское значение). Если его "
        "меняли в меню\nтрансивера, впишите здесь то же самое."),
 "ja": ("CI-V バス上で無線機が応答するアドレス。\nIC-7300: 0x94 (工場出荷時)。無線機のメニューで変更した\n場合は、同じ値をここに入力します。"),
 "zh": ("电台在 CI-V 总线上应答的地址。\nIC-7300：0x94（出厂默认）。若在电台菜单里改过，\n这里要填同样的值。"),
 "zh_TW": ("電台在 CI-V 匯流排上回應的位址。\nIC-7300：0x94（出廠預設）。若在電台選單裡改過，\n這裡要填同樣的值。"),
}
T3["L'indirizzo con cui il rig risponde sul bus CI-V.\nIC-7300: 0x94 (predefinito di fabbrica). Se e' stato "
   "cambiato nei\nmenu della radio, va scritto lo stesso valore qui."] = _CIV

T3["Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi."] = {
 "en": "Stored in plain text among the Windows settings: only worth it on a computer you trust.",
 "de": "Wird im Klartext in den Windows-Einstellungen gespeichert: nur auf einem Rechner, dem du traust.",
 "fr": "Enregistré en clair dans les réglages de Windows : à faire seulement sur un ordinateur de confiance.",
 "es": "Se guarda en texto plano en los ajustes de Windows: solo conviene en un ordenador de confianza.",
 "pt": "Guardada em texto simples nas definições do Windows: só vale a pena num computador de confiança.",
 "nl": "Wordt onversleuteld bewaard bij de Windows-instellingen: alleen doen op een pc die je vertrouwt.",
 "ca": "Es desa en clar a la configuració de Windows: només val la pena en un ordinador de confiança.",
 "da": "Gemmes i klartekst i Windows-indstillingerne: kun værd på en computer du stoler på.",
 "hu": "Titkosítatlanul tárolódik a Windows beállításai közt: csak megbízható gépen érdemes.",
 "ro": "Se salvează în clar în setările Windows: merită doar pe un calculator în care ai încredere.",
 "lv": "Tiek saglabāta atklātā tekstā Windows iestatījumos: tikai datorā, kuram uzticies.",
 "ru": "Хранится в открытом виде в настройках Windows: имеет смысл только на доверенном компьютере.",
 "ja": "Windows の設定に平文で保存されます: 信頼できるパソコンでのみ使ってください。",
 "zh": "会以明文保存在 Windows 设置中：只建议在你信任的电脑上使用。",
 "zh_TW": "會以明文儲存在 Windows 設定中：只建議在你信任的電腦上使用。",
}

T3["IP del telefono sulla rete locale"] = {
 "en": "phone IP on the local network", "de": "IP des Telefons im lokalen Netz",
 "fr": "IP du téléphone sur le réseau local", "es": "IP del teléfono en la red local",
 "pt": "IP do telemóvel na rede local", "nl": "IP van de telefoon op het lokale netwerk",
 "ca": "IP del telèfon a la xarxa local", "da": "telefonens IP på det lokale net",
 "hu": "a telefon IP-címe a helyi hálózaton", "ro": "IP-ul telefonului în rețeaua locală",
 "lv": "telefona IP vietējā tīklā", "ru": "IP телефона в локальной сети",
 "ja": "ローカルネットワーク上のスマートフォンの IP", "zh": "手机在本地网络中的 IP",
 "zh_TW": "手機在本地網路中的 IP",
}

T3["host del relay (es. decolink.ft2.it)"] = {
 "en": "relay host (e.g. decolink.ft2.it)", "de": "Relay-Host (z. B. decolink.ft2.it)",
 "fr": "hôte du relais (ex. decolink.ft2.it)", "es": "host del relé (p. ej. decolink.ft2.it)",
 "pt": "servidor do relé (ex.: decolink.ft2.it)", "nl": "relay-host (bijv. decolink.ft2.it)",
 "ca": "amfitrió del relé (p. ex. decolink.ft2.it)", "da": "relæ-vært (f.eks. decolink.ft2.it)",
 "hu": "a relé kiszolgálója (pl. decolink.ft2.it)", "ro": "gazda releului (ex. decolink.ft2.it)",
 "lv": "releja resursdators (piem., decolink.ft2.it)", "ru": "адрес ретранслятора (например, decolink.ft2.it)",
 "ja": "リレーのホスト (例: decolink.ft2.it)", "zh": "中继服务器（例如 decolink.ft2.it）",
 "zh_TW": "中繼伺服器（例如 decolink.ft2.it）",
}

T3["(il telefono chiama questa porta)"] = {
 "en": "(the phone calls this port)", "de": "(das Telefon ruft diesen Port an)",
 "fr": "(le téléphone appelle ce port)", "es": "(el teléfono llama a este puerto)",
 "pt": "(o telemóvel liga para esta porta)", "nl": "(de telefoon belt deze poort)",
 "ca": "(el telèfon truca a aquest port)", "da": "(telefonen ringer til denne port)",
 "hu": "(a telefon ezt a portot hívja)", "ro": "(telefonul sună la acest port)",
 "lv": "(telefons zvana uz šo portu)", "ru": "(телефон звонит на этот порт)",
 "ja": "(スマートフォンがこのポートに接続します)", "zh": "（手机呼叫这个端口）",
 "zh_TW": "（手機呼叫這個連接埠）",
}

T3["%1 — stazione %2, come %3%4"] = {
 "en": "%1 — station %2, as %3%4", "de": "%1 — Station %2, als %3%4",
 "fr": "%1 — station %2, en tant que %3%4", "es": "%1 — estación %2, como %3%4",
 "pt": "%1 — estação %2, como %3%4", "nl": "%1 — station %2, als %3%4",
 "ca": "%1 — estació %2, com a %3%4", "da": "%1 — station %2, som %3%4",
 "hu": "%1 — %2 állomás, mint %3%4", "ro": "%1 — stația %2, ca %3%4",
 "lv": "%1 — stacija %2, kā %3%4", "ru": "%1 — станция %2, как %3%4",
 "ja": "%1 — 局 %2、%3%4 として", "zh": "%1 — 电台 %2，身份：%3%4",
 "zh_TW": "%1 — 電台 %2，身分：%3%4",
}

T3["%1 — %2"] = {l: "%1 — %2" for l in
                 ["en", "de", "fr", "es", "pt", "nl", "ca", "da", "hu", "ro", "lv", "ru", "ja", "zh", "zh_TW"]}
T3["—"] = {l: "—" for l in
           ["en", "de", "fr", "es", "pt", "nl", "ca", "da", "hu", "ro", "lv", "ru", "ja", "zh", "zh_TW"]}

T3["attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, "
   "passa a PCM 48 kHz"] = {
 "en": "warning: profile %1, but the phone has not confirmed it can read it — if you hear nothing, switch to PCM 48 kHz",
 "de": "Achtung: Profil %1, aber das Telefon hat nicht bestätigt, dass es das lesen kann — hörst du nichts, wechsle zu PCM 48 kHz",
 "fr": "attention : profil %1, mais le téléphone n'a pas confirmé qu'il sait le lire — si vous n'entendez rien, passez à PCM 48 kHz",
 "es": "atención: perfil %1, pero el teléfono no ha confirmado que sepa leerlo — si no oyes nada, cambia a PCM 48 kHz",
 "pt": "atenção: perfil %1, mas o telemóvel não confirmou que o sabe ler — se não ouvir nada, mude para PCM 48 kHz",
 "nl": "let op: profiel %1, maar de telefoon heeft niet bevestigd dat hij het kan lezen — hoor je niets, schakel over naar PCM 48 kHz",
 "ca": "atenció: perfil %1, però el telèfon no ha confirmat que el sàpiga llegir — si no sents res, passa a PCM 48 kHz",
 "da": "bemærk: profil %1, men telefonen har ikke bekræftet at den kan læse det — hører du intet, skift til PCM 48 kHz",
 "hu": "figyelem: %1 profil, de a telefon nem erősítette meg, hogy tudja olvasni — ha nem hall semmit, váltson PCM 48 kHz-re",
 "ro": "atenție: profilul %1, dar telefonul nu a confirmat că îl poate citi — dacă nu auzi nimic, treci la PCM 48 kHz",
 "lv": "uzmanību: profils %1, bet telefons nav apstiprinājis, ka prot to nolasīt — ja neko nedzirdat, pārejiet uz PCM 48 kHz",
 "ru": "внимание: профиль %1, но телефон не подтвердил, что умеет его читать — если ничего не слышно, переключитесь на PCM 48 кГц",
 "ja": "注意: プロファイル %1 ですが、スマートフォンが読めると確認していません — 何も聞こえない場合は PCM 48 kHz に切り替えてください",
 "zh": "注意：配置为 %1，但手机未确认能否读取 — 如果听不到声音，请切换到 PCM 48 kHz",
 "zh_TW": "注意：設定檔為 %1，但手機未確認能否讀取 — 如果聽不到聲音，請切換到 PCM 48 kHz",
}
