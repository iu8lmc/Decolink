<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="zh_TW">
<context>
    <name>Client</name>
    <message>
        <location filename="../main.cpp" line="714" />
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — 在 Decodium Mobile 上使用電台</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="721" />
        <source>LAN diretta</source>
        <translation>區域網路直連</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="722" />
        <source>Relay + stazione</source>
        <translation>中繼 + 電台</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="723" />
        <source>Il telefono chiama casa</source>
        <translation>手機主動回連</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="724" />
        <source>LAN diretta — il telefono è sulla stessa rete: gli si manda l'audio all'indirizzo
Relay + stazione — funziona ovunque, anche su dati mobili: PC e telefono
   escono entrambi verso il relay, quindi non c'è nessun router da configurare
Il telefono chiama casa — porta inoltrata sul router e nome DynDNS</source>
        <translation>區域網路直連 — 手機在同一網路：音訊直接送到它的位址
中繼 + 電台 — 到處可用，行動數據也行：電腦和手機都向中繼發起連線，
   因此不需要設定路由器
手機主動回連 — 需要路由器連接埠轉發和 DynDNS 名稱</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="731" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>手機 IP 或中繼伺服器</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="735" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(登入後選擇電台)</translation>
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
        <translation>每秒傳送多少取樣。
48 kHz — 808 kbit/s，每小時 364 MB：對任何程式都安全
24 kHz — 424 kbit/s，每小時 191 MB
12 kHz — 232 kbit/s，每小時 104 MB：對只占 2.7 kHz 的 SSB 綽綽有餘。

如果手機聽起來變快，表示它沒有讀取宣告的取樣率：請改回 48 kHz。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="772" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="773" />
        <source>Voce (Opus)</source>
        <translation>語音 (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="774" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="775" />
        <source>Digitali senza perdite</source>
        <translation>數位模式（無損）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="776" />
        <source>CW a tasto</source>
        <translation>僅 CW 鍵控</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="777" />
        <source>PCM — compatibile con tutti, nessuna compressione
Voce — Opus a 32 kbit/s: serve un programma aggiornato dall'altra parte
CW — Opus a banda stretta, 20 kbit/s
Digitali — compresso senza perdere un bit, 146 kbit/s
CW a tasto — solo il ritmo del tasto, 2,4 kbit/s: si perde
tutto il contesto (QSB, QRM, chi chiama fuori nota)</source>
        <translation>PCM — 與所有程式相容，不壓縮
語音 — Opus 32 kbit/s：對端需要已更新的程式
CW — 窄頻 Opus，20 kbit/s
數位模式 — 無損壓縮，146 kbit/s
CW 鍵控 — 僅鍵控節奏，2.4 kbit/s：會失去
全部環境資訊（QSB、QRM、在頻率旁呼叫的人）</translation>
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
        <translation>每個封包放多少幀：封包越少，需要付出的標頭越少，但延遲略增。
20 ms — 延遲最小
40 ms — 頻寬減少 18%，延遲無法察覺
60 ms — 減少 24%，適合按流量計費的網路</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="805" />
        <source>Audio radio</source>
        <translation>電台音訊</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="806" />
        <source>Modalità</source>
        <translation>連線方式</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="807" />
        <source>Host</source>
        <translation>主機</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="814" />
        <source>stazione</source>
        <translation>電台</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="818" />
        <source>Porta</source>
        <translation>連接埠</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="826" />
        <source>Profilo</source>
        <translation>設定檔</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="827" />
        <source>Campionamento</source>
        <translation>取樣率</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="828" />
        <source>Pacchetti da</source>
        <translation>封包時長</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="834" />
        <location filename="../main.cpp" line="840" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  進階設定</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="839" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  進階設定</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="846" />
        <location filename="../main.cpp" line="2372" />
        <location filename="../main.cpp" line="2700" />
        <source>Avvia</source>
        <translation>啟動</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="856" />
        <source>Potenza, ROS e ALC letti dalla radio.
Compaiono mentre trasmetti, se la radio li espone.</source>
        <translation>從電台讀取的功率、駐波比和 ALC。
發射時顯示，前提是電台提供這些資料。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="858" />
        <location filename="../main.cpp" line="2374" />
        <source>fermo</source>
        <translation>已停止</translation>
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
        <translation>Hamlib %1 — 辨識 %2 個型號。
前兩項是寫在 Decolink 內部的協定；
其餘透過 Hamlib，與桌面版 Decodium 使用同一個函式庫。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="897" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>占用電台的程式的 主機:連接埠</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="899" />
        <source>Indirizzo del programma che tiene la porta seriale.
rigctld e i programmi compatibili: localhost:4532
FLRig: localhost:12345

Serve quando la COM è già occupata da un altro programma:
la porta seriale è di chi la apre per primo, e in due non
ci si sta.</source>
        <translation>占用序列埠的程式位址。
rigctld 及相容程式：localhost:4532
FLRig：localhost:12345

當 COM 埠已被其他程式占用時使用：
序列埠屬於先開啟它的程式，兩個程式無法共用。</translation>
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
        <translation>無</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="919" />
        <source>pari</source>
        <translation>偶</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="920" />
        <source>dispari</source>
        <translation>奇</translation>
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
        <translation>無</translation>
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
        <translation>向手機提供 CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="931" />
        <location filename="../main.cpp" line="1489" />
        <source>CAT spento</source>
        <translation>CAT 已關閉</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="934" />
        <source>(nessuna: non trasmettere)</source>
        <translation>（無：不發射）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="942" />
        <source>Radio / protocollo</source>
        <translation>電台 / 協定</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="943" />
        <source>Indirizzo CI-V</source>
        <translation>CI-V 位址</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="944" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>電台在 CI-V 匯流排上回應的位址。
IC-7300：0x94（出廠預設）。若在電台選單裡改過，
這裡要填同樣的值。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="949" />
        <source>Audio al rig</source>
        <translation>送往電台的音訊</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="956" />
        <source>Porta rig</source>
        <translation>電台連接埠</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="961" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="966" />
        <source>Velocità</source>
        <translation>鮑率</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="973" />
        <source>dati</source>
        <translation>資料位元</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="977" />
        <source>parità</source>
        <translation>同位檢查</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="981" />
        <source>stop</source>
        <translation>停止位元</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="985" />
        <source>Seriale</source>
        <translation>序列埠</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="986" />
        <source>Handshake</source>
        <translation>流量控制</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1015" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>登入伺服器（例如 decolink.ft2.it）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1017" />
        <source>la tua email</source>
        <translation>你的電子郵件</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1020" />
        <source>password</source>
        <translation>密碼</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1021" />
        <source>ricorda la password</source>
        <translation>記住密碼</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1022" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>會以明文儲存在 Windows 設定中：只建議在你信任的電腦上使用。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1024" />
        <source>Accedi</source>
        <translation>登入</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1025" />
        <source>non collegato</source>
        <translation>未連線</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1035" />
        <source>Server</source>
        <translation>伺服器</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1041" />
        <source>Accesso</source>
        <translation>登入</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1062" />
        <source>versione di Decolink</source>
        <translation>Decolink 版本</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1070" />
        <source>lingua dell'interfaccia</source>
        <translation>介面語言</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1087" />
        <source>COLLEGAMENTO</source>
        <translation>連線</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1095" />
        <source>RADIO E CAT</source>
        <translation>電台與 CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1118" />
        <source>livello audio</source>
        <translation>音訊電平</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1174" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>取樣率 %1 kHz：如果手機聽起來變快，請改回 48</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1278" />
        <location filename="../main.cpp" line="1286" />
        <source>Lingua</source>
        <translation>語言</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1279" />
        <source>Il collegamento è aperto: la lingua cambia alla prossima apertura del programma.</source>
        <translation>連線正在進行：語言將在下次啟動程式時生效。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1287" />
        <source>Decolink si riavvia per cambiare lingua. Procedo?</source>
        <translation>Decolink 將重新啟動以變更語言。繼續嗎？</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1311" />
        <source>IP del telefono sulla rete locale</source>
        <translation>手機在本地網路中的 IP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1314" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>中繼伺服器（例如 decolink.ft2.it）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1317" />
        <source>(il telefono chiama questa porta)</source>
        <translation>（手機呼叫這個連接埠）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1328" />
        <source>manca il server di accesso</source>
        <translation>缺少登入伺服器</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1330" />
        <source>servono email e password</source>
        <translation>需要電子郵件和密碼</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1352" />
        <source>accesso in corso…</source>
        <translation>正在登入…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1372" />
        <source>risposta incomprensibile dal server</source>
        <translation>無法解析伺服器的回覆</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1409" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — 電台 %2，身分：%3%4</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1432" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1468" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>憑證已過期：正在重新登入</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1471" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>尚未登入：請先點「登入」，再點「啟動」</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1501" />
        <source>nessuna porta seriale</source>
        <translation>沒有序列埠</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1510" />
        <source>indirizzo CI-V non valido</source>
        <translation>CI-V 位址無效</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1519" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>缺少占用電台的程式位址</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1536" />
        <source>qui c'è Decolink stesso: scegli il programma che tiene davvero la radio, o cambia la porta TCP qui sotto</source>
        <translation>這裡就是 Decolink 自己：請選擇真正占用電台的程式，或修改下面的 TCP 連接埠</translation>
    </message>
    <message>
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>TCP 連接埠 %1 與你要連線的相同：請改一個</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1552" />
        <source>%1 non risponde: %2</source>
        <translation>%1 無回應：%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1565" />
        <source>%1 non si apre: %2</source>
        <translation>無法開啟 %1：%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1573" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>TCP 連接埠 %1 被占用（rigctld 是否已在執行？）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1621" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>電台：%1 MHz  %2   （TCP %3，並透過音訊通道）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1650" />
        <source>il programma che tiene la radio ha smesso di rispondere — riaccendi il CAT quando è tornato</source>
        <translation>占用電台的程式已停止回應 — 等它恢復後請重新開啟 CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1652" />
        <source>rig non risponde sulla seriale</source>
        <translation>電台在序列埠上無回應</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1680" />
        <source>telefono connesso da %1:%2</source>
        <translation>手機已從 %1:%2 連線</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1730" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>憑證需要更新：正在重新登入</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1734" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>中繼拒絕了連線：%1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1742" />
        <source>il telefono è entrato nella stanza</source>
        <translation>手機已加入房間</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1744" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>已在中繼上註冊為 %1（%2）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1851" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>手機可讀取合併的封包：頻寬已降低</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1873" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>手機要求的設定檔：%1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2167" />
        <location filename="../main.cpp" line="2348" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>%1 不支援 48 kHz 單聲道 16 位元</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2175" />
        <source>trasmissione dal telefono in corso</source>
        <translation>正在從手機發射</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2186" />
        <source>trasmissione finita</source>
        <translation>發射結束</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2237" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>已註冊，但電台裡沒有其他人：手機尚未加入</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2240" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>注意：設定檔為 %1，但手機未確認能否讀取 — 如果聽不到聲音，請切換到 PCM 48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2254" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>手機已失聯 — 等待它重新連線</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2296" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Opus 無法啟動（%1）：保持 PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2312" />
        <source>manca l'host di destinazione</source>
        <translation>缺少目標主機</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2315" />
        <source>nome non risolto: %1</source>
        <translation>無法解析名稱：%1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2320" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>請先登入：中繼不接受沒有憑證的連線</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2330" />
        <source>porta %1 non disponibile</source>
        <translation>連接埠 %1 無法使用</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2344" />
        <source>nessun ingresso audio</source>
        <translation>沒有音訊輸入</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2353" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>無法開啟音訊輸入</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2357" />
        <source>Ferma</source>
        <translation>停止</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2361" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>正在連接埠 %1 監聽 — 等待手機</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2412" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>設定檔已回到 PCM 48 kHz：壓縮設定檔需要更新過的手機</translation>
    </message>
</context>
<context>
    <name>QObject</name>
    <message>
        <location filename="../hamlibrig.h" line="184" />
        <source>errore %1 di Hamlib</source>
        <translation>Hamlib 錯誤 %1</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="270" />
        <source>indirizzo vuoto</source>
        <translation>位址為空</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="279" />
        <source>nessuna risposta da %1:%2</source>
        <translation>%1:%2 沒有回應</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="280" />
        <source>%1:%2 — %3</source>
        <translation>%1:%2 — %3</translation>
    </message>
</context>
</TS>