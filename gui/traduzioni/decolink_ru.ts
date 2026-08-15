<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="ru">
<context>
    <name>Client</name>
    <message>
        <location filename="../main.cpp" line="548" />
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — радиостанция в Decodium Mobile</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="555" />
        <source>LAN diretta</source>
        <translation>Прямая локальная сеть</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="556" />
        <source>Relay + stazione</source>
        <translation>Ретранслятор + станция</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="557" />
        <source>Il telefono chiama casa</source>
        <translation>Телефон звонит домой</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="558" />
        <source>LAN diretta — il telefono è sulla stessa rete: gli si manda l'audio all'indirizzo
Relay + stazione — funziona ovunque, anche su dati mobili: PC e telefono
   escono entrambi verso il relay, quindi non c'è nessun router da configurare
Il telefono chiama casa — porta inoltrata sul router e nome DynDNS</source>
        <translation>Прямая локальная сеть — телефон в той же сети: звук идёт на его адрес
Ретранслятор + станция — работает везде, в том числе в мобильной сети:
   ПК и телефон оба подключаются к ретранслятору, роутер настраивать не нужно
Телефон звонит домой — проброшенный порт на роутере и имя DynDNS</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="565" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>IP телефона или адрес ретранслятора</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="569" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(войдите, чтобы выбрать станцию)</translation>
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
        <translation>Сколько отсчётов в секунду передавать.
48 кГц — 808 кбит/с, 364 МБ в час: безопасно с любой программой
24 кГц — 424 кбит/с, 191 МБ в час
12 кГц — 232 кбит/с, 104 МБ в час: с запасом хватает для SSB,
который занимает всего 2,7 кГц.

Если на телефоне звук ускорен, он не читает объявленную частоту
дискретизации: вернитесь на 48 кГц.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="606" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="607" />
        <source>Voce (Opus)</source>
        <translation>Голос (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="608" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="609" />
        <source>Digitali senza perdite</source>
        <translation>Цифровые виды, без потерь</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="610" />
        <source>CW a tasto</source>
        <translation>Только манипуляция CW</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="611" />
        <source>PCM — compatibile con tutti, nessuna compressione
Voce — Opus a 32 kbit/s: serve un programma aggiornato dall'altra parte
CW — Opus a banda stretta, 20 kbit/s
Digitali — compresso senza perdere un bit, 146 kbit/s
CW a tasto — solo il ritmo del tasto, 2,4 kbit/s: si perde
tutto il contesto (QSB, QRM, chi chiama fuori nota)</source>
        <translation>PCM — работает со всем, без сжатия
Голос — Opus 32 кбит/с: на той стороне нужна обновлённая программа
CW — узкополосный Opus, 20 кбит/с
Цифровые — сжатие без потери единого бита, 146 кбит/с
Манипуляция CW — только ритм, 2,4 кбит/с: теряется
весь контекст (QSB, QRM, кто зовёт рядом по частоте)</translation>
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
        <translation>Сколько кадров класть в один пакет: меньше пакетов — меньше
заголовков, но чуть больше задержки.
20 мс — наименьшая задержка
40 мс — на 18% меньше полосы, задержка незаметна
60 мс — на 24% меньше, для тарифов с лимитом</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="639" />
        <source>Audio radio</source>
        <translation>Звук с трансивера</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="640" />
        <source>Modalità</source>
        <translation>Режим</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="641" />
        <source>Host</source>
        <translation>Адрес</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="648" />
        <source>stazione</source>
        <translation>станция</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="652" />
        <source>Porta</source>
        <translation>Порт</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="660" />
        <source>Profilo</source>
        <translation>Профиль</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="661" />
        <source>Campionamento</source>
        <translation>Частота дискретизации</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="662" />
        <source>Pacchetti da</source>
        <translation>Длина пакета</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="668" />
        <location filename="../main.cpp" line="674" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  Дополнительные настройки</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="673" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  Дополнительные настройки</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="680" />
        <location filename="../main.cpp" line="2067" />
        <source>Avvia</source>
        <translation>Пуск</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="686" />
        <location filename="../main.cpp" line="2069" />
        <source>fermo</source>
        <translation>остановлено</translation>
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
        <translation>Hamlib %1 — распознано моделей: %2.
Первые две строки — протоколы, написанные внутри Decolink;
остальные идут через Hamlib, ту же библиотеку, что использует
Decodium на компьютере.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="725" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>адрес:порт программы, которая держит трансивер</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="727" />
        <source>Indirizzo del programma che tiene la porta seriale.
rigctld e i programmi compatibili: localhost:4532
FLRig: localhost:12345

Serve quando la COM è già occupata da un altro programma:
la porta seriale è di chi la apre per primo, e in due non
ci si sta.</source>
        <translation>Адрес программы, которая держит последовательный порт.
rigctld и совместимые программы: localhost:4532
FLRig: localhost:12345

Нужен, когда COM-порт уже занят другой программой:
порт принадлежит тому, кто открыл его первым, и вдвоём туда не поместиться.</translation>
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
        <translation>нет</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="747" />
        <source>pari</source>
        <translation>чётная</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="748" />
        <source>dispari</source>
        <translation>нечётная</translation>
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
        <translation>нет</translation>
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
        <translation>Отдавать CAT телефону</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="759" />
        <location filename="../main.cpp" line="1238" />
        <source>CAT spento</source>
        <translation>CAT выключен</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="762" />
        <source>(nessuna: non trasmettere)</source>
        <translation>(нет: не передавать)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="770" />
        <source>Radio / protocollo</source>
        <translation>Трансивер / протокол</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="771" />
        <source>Indirizzo CI-V</source>
        <translation>Адрес CI-V</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="772" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>Адрес, по которому трансивер отвечает на шине CI-V.
IC-7300: 0x94 (заводское значение). Если его меняли в меню
трансивера, впишите здесь то же самое.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="777" />
        <source>Audio al rig</source>
        <translation>Звук на трансивер</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="784" />
        <source>Porta rig</source>
        <translation>Порт трансивера</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="789" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="794" />
        <source>Velocità</source>
        <translation>Скорость</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="801" />
        <source>dati</source>
        <translation>данные</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="805" />
        <source>parità</source>
        <translation>чётность</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="809" />
        <source>stop</source>
        <translation>стоп</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="813" />
        <source>Seriale</source>
        <translation>Последовательный порт</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="814" />
        <source>Handshake</source>
        <translation>Управление потоком</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="843" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>сервер входа (например, decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="845" />
        <source>la tua email</source>
        <translation>ваша почта</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="848" />
        <source>password</source>
        <translation>пароль</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="849" />
        <source>ricorda la password</source>
        <translation>запомнить пароль</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="850" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>Хранится в открытом виде в настройках Windows: имеет смысл только на доверенном компьютере.</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="852" />
        <source>Accedi</source>
        <translation>Войти</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="853" />
        <source>non collegato</source>
        <translation>не подключено</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="863" />
        <source>Server</source>
        <translation>Сервер</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="869" />
        <source>Accesso</source>
        <translation>Вход</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="891" />
        <source>COLLEGAMENTO</source>
        <translation>СОЕДИНЕНИЕ</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="899" />
        <source>RADIO E CAT</source>
        <translation>ТРАНСИВЕР И CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="922" />
        <source>livello audio</source>
        <translation>уровень звука</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="977" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>дискретизация %1 кГц: если на телефоне звук ускорен, вернитесь на 48</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1060" />
        <source>IP del telefono sulla rete locale</source>
        <translation>IP телефона в локальной сети</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1063" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>адрес ретранслятора (например, decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1066" />
        <source>(il telefono chiama questa porta)</source>
        <translation>(телефон звонит на этот порт)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1077" />
        <source>manca il server di accesso</source>
        <translation>не указан сервер входа</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1079" />
        <source>servono email e password</source>
        <translation>нужны почта и пароль</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1101" />
        <source>accesso in corso…</source>
        <translation>выполняется вход…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1121" />
        <source>risposta incomprensibile dal server</source>
        <translation>непонятный ответ сервера</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1158" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — станция %2, как %3%4</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1181" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1217" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>срок действия учётных данных истёк: вхожу заново</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1220" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>вход не выполнен: нажмите Войти, затем Пуск</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1250" />
        <source>nessuna porta seriale</source>
        <translation>нет последовательного порта</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1259" />
        <source>indirizzo CI-V non valido</source>
        <translation>неверный адрес CI-V</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1268" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>не указан адрес программы, которая держит трансивер</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1280" />
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>TCP-порт %1 совпадает с тем, к которому вы подключаетесь: измените один из них</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1296" />
        <source>%1 non risponde: %2</source>
        <translation>%1 не отвечает: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1309" />
        <source>%1 non si apre: %2</source>
        <translation>%1 не открывается: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1317" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>TCP-порт %1 занят (rigctld уже запущен?)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1345" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>трансивер: %1 МГц  %2   (TCP %3, и по звуковому каналу)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1375" />
        <source>telefono connesso da %1:%2</source>
        <translation>телефон подключён с %1:%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1425" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>нужно обновить учётные данные: вхожу заново</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1429" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>ретранслятор отклонил подключение: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1437" />
        <source>il telefono è entrato nella stanza</source>
        <translation>телефон вошёл в комнату</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1439" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>зарегистрирован на ретрансляторе как %1 (%2)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1546" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>телефон читает сгруппированные пакеты: полоса снижена</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1568" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>профиль по запросу телефона: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1862" />
        <location filename="../main.cpp" line="2043" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>%1 не поддерживает 48 кГц моно 16 бит</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1870" />
        <source>trasmissione dal telefono in corso</source>
        <translation>идёт передача с телефона</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1881" />
        <source>trasmissione finita</source>
        <translation>передача окончена</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1932" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>зарегистрирован, но на станции больше никого нет: телефон ещё не вошёл</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1935" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>внимание: профиль %1, но телефон не подтвердил, что умеет его читать — если ничего не слышно, переключитесь на PCM 48 кГц</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1949" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>телефон больше недоступен — жду, когда он выйдет на связь</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1991" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Opus не запускается (%1): остаюсь на PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2007" />
        <source>manca l'host di destinazione</source>
        <translation>не указан адрес назначения</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2010" />
        <source>nome non risolto: %1</source>
        <translation>имя не разрешено: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2015" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>сначала войдите: ретранслятор не принимает подключения без учётных данных</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2025" />
        <source>porta %1 non disponibile</source>
        <translation>порт %1 недоступен</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2039" />
        <source>nessun ingresso audio</source>
        <translation>нет звукового входа</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2048" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>не удаётся открыть звуковой вход</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2052" />
        <source>Ferma</source>
        <translation>Стоп</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2056" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>слушаю порт %1 — жду телефон</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2107" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>профиль возвращён на PCM 48 кГц: сжатые профили требуют обновлённого телефона</translation>
    </message>
</context>
</TS>