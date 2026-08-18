<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="ja">
<context>
    <name>Client</name>
    <message>
        <location filename="../main.cpp" line="714" />
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — Decodium Mobile で無線機を操作</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="721" />
        <source>LAN diretta</source>
        <translation>LAN 直結</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="722" />
        <source>Relay + stazione</source>
        <translation>リレー + 局</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="723" />
        <source>Il telefono chiama casa</source>
        <translation>スマートフォンから接続</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="724" />
        <source>LAN diretta — il telefono è sulla stessa rete: gli si manda l'audio all'indirizzo
Relay + stazione — funziona ovunque, anche su dati mobili: PC e telefono
   escono entrambi verso il relay, quindi non c'è nessun router da configurare
Il telefono chiama casa — porta inoltrata sul router e nome DynDNS</source>
        <translation>LAN 直結 — スマートフォンが同じネットワーク上: その IP へ音声を送ります
リレー + 局 — どこでも動作し、モバイル回線でも可: PC もスマートフォンも
   リレーへ発信するので、ルーターの設定は不要です
スマートフォンから接続 — ルーターのポート転送と DynDNS 名が必要</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="731" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>スマートフォンの IP、またはリレーのホスト</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="735" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(ログインして局を選択)</translation>
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
        <translation>1 秒あたり何サンプル送るか。
48 kHz — 808 kbit/s、1 時間 364 MB: どのプログラムでも安全
24 kHz — 424 kbit/s、1 時間 191 MB
12 kHz — 232 kbit/s、1 時間 104 MB: 帯域 2.7 kHz の SSB には十分すぎます。

スマートフォンで速く聞こえる場合、宣言したサンプリング周波数を
読んでいません: 48 kHz に戻してください。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="772" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="773" />
        <source>Voce (Opus)</source>
        <translation>音声 (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="774" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="775" />
        <source>Digitali senza perdite</source>
        <translation>デジタルモード (可逆圧縮)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="776" />
        <source>CW a tasto</source>
        <translation>CW キーイングのみ</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="777" />
        <source>PCM — compatibile con tutti, nessuna compressione
Voce — Opus a 32 kbit/s: serve un programma aggiornato dall'altra parte
CW — Opus a banda stretta, 20 kbit/s
Digitali — compresso senza perdere un bit, 146 kbit/s
CW a tasto — solo il ritmo del tasto, 2,4 kbit/s: si perde
tutto il contesto (QSB, QRM, chi chiama fuori nota)</source>
        <translation>PCM — すべてと互換、圧縮なし
音声 — Opus 32 kbit/s: 相手側に更新されたプログラムが必要
CW — 狭帯域 Opus、20 kbit/s
デジタル — 1 ビットも失わない圧縮、146 kbit/s
CW キーイング — 打鍵のリズムのみ、2.4 kbit/s: 周囲の状況
(QSB、QRM、周波数の外で呼ぶ局) はすべて失われます</translation>
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
        <translation>1 パケットに何フレーム入れるか: パケットが少ないほどヘッダーの
負担が減りますが、遅延が少し増えます。
20 ms — 遅延最小
40 ms — 帯域 18% 減、遅延は感じられません
60 ms — 24% 減、従量制の回線向け</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="805" />
        <source>Audio radio</source>
        <translation>無線機の音声</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="806" />
        <source>Modalità</source>
        <translation>接続方式</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="807" />
        <source>Host</source>
        <translation>ホスト</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="814" />
        <source>stazione</source>
        <translation>局</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="818" />
        <source>Porta</source>
        <translation>ポート</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="826" />
        <source>Profilo</source>
        <translation>プロファイル</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="827" />
        <source>Campionamento</source>
        <translation>サンプリング</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="828" />
        <source>Pacchetti da</source>
        <translation>パケット長</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="834" />
        <location filename="../main.cpp" line="840" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  詳細設定</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="839" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  詳細設定</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="846" />
        <location filename="../main.cpp" line="2372" />
        <location filename="../main.cpp" line="2700" />
        <source>Avvia</source>
        <translation>開始</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="856" />
        <source>Potenza, ROS e ALC letti dalla radio.
Compaiono mentre trasmetti, se la radio li espone.</source>
        <translation>無線機から読み取った電力、SWR、ALC。
無線機が対応していれば、送信中に表示されます。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="858" />
        <location filename="../main.cpp" line="2374" />
        <source>fermo</source>
        <translation>停止中</translation>
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
        <translation>Hamlib %1 — %2 機種に対応。
最初の 2 つは Decolink 内に書かれたプロトコルです。
それ以外は Hamlib 経由で、デスクトップ版 Decodium と
同じライブラリを使います。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="897" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>無線機を保持しているプログラムの ホスト:ポート</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="899" />
        <source>Indirizzo del programma che tiene la porta seriale.
rigctld e i programmi compatibili: localhost:4532
FLRig: localhost:12345

Serve quando la COM è già occupata da un altro programma:
la porta seriale è di chi la apre per primo, e in due non
ci si sta.</source>
        <translation>シリアルポートを保持しているプログラムのアドレス。
rigctld および互換プログラム: localhost:4532
FLRig: localhost:12345

COM ポートが別のプログラムに占有されている場合に使います。
シリアルポートは先に開いた側のもので、2 つは同居できません。</translation>
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
        <translation>なし</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="919" />
        <source>pari</source>
        <translation>偶数</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="920" />
        <source>dispari</source>
        <translation>奇数</translation>
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
        <translation>なし</translation>
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
        <translation>CAT をスマートフォンに提供</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="931" />
        <location filename="../main.cpp" line="1489" />
        <source>CAT spento</source>
        <translation>CAT オフ</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="934" />
        <source>(nessuna: non trasmettere)</source>
        <translation>(なし: 送信しない)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="942" />
        <source>Radio / protocollo</source>
        <translation>無線機 / プロトコル</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="943" />
        <source>Indirizzo CI-V</source>
        <translation>CI-V アドレス</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="944" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>CI-V バス上で無線機が応答するアドレス。
IC-7300: 0x94 (工場出荷時)。無線機のメニューで変更した
場合は、同じ値をここに入力します。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="949" />
        <source>Audio al rig</source>
        <translation>無線機への音声</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="956" />
        <source>Porta rig</source>
        <translation>無線機のポート</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="961" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="966" />
        <source>Velocità</source>
        <translation>通信速度</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="973" />
        <source>dati</source>
        <translation>データ</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="977" />
        <source>parità</source>
        <translation>パリティ</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="981" />
        <source>stop</source>
        <translation>ストップ</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="985" />
        <source>Seriale</source>
        <translation>シリアル</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="986" />
        <source>Handshake</source>
        <translation>フロー制御</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1015" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>ログインサーバー (例: decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1017" />
        <source>la tua email</source>
        <translation>メールアドレス</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1020" />
        <source>password</source>
        <translation>パスワード</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1021" />
        <source>ricorda la password</source>
        <translation>パスワードを保存</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1022" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>Windows の設定に平文で保存されます: 信頼できるパソコンでのみ使ってください。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1024" />
        <source>Accedi</source>
        <translation>ログイン</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1025" />
        <source>non collegato</source>
        <translation>未接続</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1035" />
        <source>Server</source>
        <translation>サーバー</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1041" />
        <source>Accesso</source>
        <translation>ログイン</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1062" />
        <source>versione di Decolink</source>
        <translation>Decolink のバージョン</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1070" />
        <source>lingua dell'interfaccia</source>
        <translation>画面の言語</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1087" />
        <source>COLLEGAMENTO</source>
        <translation>接続</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1095" />
        <source>RADIO E CAT</source>
        <translation>無線機と CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1118" />
        <source>livello audio</source>
        <translation>音声レベル</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1174" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>サンプリング %1 kHz: スマートフォンで速く聞こえる場合は 48 に戻してください</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1278" />
        <location filename="../main.cpp" line="1286" />
        <source>Lingua</source>
        <translation>言語</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1279" />
        <source>Il collegamento è aperto: la lingua cambia alla prossima apertura del programma.</source>
        <translation>接続中です: 言語は次回の起動時に切り替わります。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1287" />
        <source>Decolink si riavvia per cambiare lingua. Procedo?</source>
        <translation>言語を変更するため Decolink を再起動します。よろしいですか?</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1311" />
        <source>IP del telefono sulla rete locale</source>
        <translation>ローカルネットワーク上のスマートフォンの IP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1314" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>リレーのホスト (例: decolink.ft2.it)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1317" />
        <source>(il telefono chiama questa porta)</source>
        <translation>(スマートフォンがこのポートに接続します)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1328" />
        <source>manca il server di accesso</source>
        <translation>ログインサーバーが未設定です</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1330" />
        <source>servono email e password</source>
        <translation>メールアドレスとパスワードが必要です</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1352" />
        <source>accesso in corso…</source>
        <translation>ログイン中…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1372" />
        <source>risposta incomprensibile dal server</source>
        <translation>サーバーの応答を解釈できません</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1409" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — 局 %2、%3%4 として</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1432" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1468" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>認証情報の期限切れ: 再ログインします</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1471" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>未ログインです: ログイン してから 開始 を押してください</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1501" />
        <source>nessuna porta seriale</source>
        <translation>シリアルポートがありません</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1510" />
        <source>indirizzo CI-V non valido</source>
        <translation>CI-V アドレスが不正です</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1519" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>無線機を保持しているプログラムのアドレスが未設定です</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1536" />
        <source>qui c'è Decolink stesso: scegli il programma che tiene davvero la radio, o cambia la porta TCP qui sotto</source>
        <translation>これは Decolink 自身です: 実際に無線機を保持しているプログラムを選ぶか、下の TCP ポートを変更してください</translation>
    </message>
    <message>
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>TCP ポート %1 は接続先と同じです: どちらかを変更してください</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1552" />
        <source>%1 non risponde: %2</source>
        <translation>%1 が応答しません: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1565" />
        <source>%1 non si apre: %2</source>
        <translation>%1 を開けません: %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1573" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>TCP ポート %1 は使用中です (rigctld が既に動作中?)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1621" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>無線機: %1 MHz  %2   (TCP %3、音声チャンネル経由)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1650" />
        <source>il programma che tiene la radio ha smesso di rispondere — riaccendi il CAT quando è tornato</source>
        <translation>無線機を保持しているプログラムが応答しなくなりました — 復帰したら CAT を入れ直してください</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1652" />
        <source>rig non risponde sulla seriale</source>
        <translation>無線機がシリアルポートで応答しません</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1680" />
        <source>telefono connesso da %1:%2</source>
        <translation>スマートフォンが %1:%2 から接続しました</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1730" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>認証情報の更新が必要です: 再ログインします</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1734" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>リレーが接続を拒否しました: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1742" />
        <source>il telefono è entrato nella stanza</source>
        <translation>スマートフォンが部屋に入りました</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1744" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>リレーに %1 (%2) として登録しました</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1851" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>スマートフォンがまとめたパケットを読めます: 帯域を削減しました</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1873" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>スマートフォンの要求によるプロファイル: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2167" />
        <location filename="../main.cpp" line="2348" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>%1 は 48 kHz モノラル 16 ビットに対応していません</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2175" />
        <source>trasmissione dal telefono in corso</source>
        <translation>スマートフォンから送信中</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2186" />
        <source>trasmissione finita</source>
        <translation>送信終了</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2237" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>登録済みですが、局には他に誰もいません: スマートフォンがまだ入っていません</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2240" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>注意: プロファイル %1 ですが、スマートフォンが読めると確認していません — 何も聞こえない場合は PCM 48 kHz に切り替えてください</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2254" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>スマートフォンに接続できません — 再接続を待っています</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2296" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Opus を開始できません (%1): PCM のままにします</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2312" />
        <source>manca l'host di destinazione</source>
        <translation>接続先ホストが未設定です</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2315" />
        <source>nome non risolto: %1</source>
        <translation>名前を解決できません: %1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2320" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>先にログインしてください: リレーは認証情報なしの接続を受け付けません</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2330" />
        <source>porta %1 non disponibile</source>
        <translation>ポート %1 は使用できません</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2344" />
        <source>nessun ingresso audio</source>
        <translation>音声入力がありません</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2353" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>音声入力を開けません</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2357" />
        <source>Ferma</source>
        <translation>停止</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2361" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>ポート %1 で待ち受け中 — スマートフォンを待っています</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2412" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>プロファイルを PCM 48 kHz に戻しました: 圧縮プロファイルには更新されたスマートフォンが必要です</translation>
    </message>
</context>
<context>
    <name>QObject</name>
    <message>
        <location filename="../hamlibrig.h" line="184" />
        <source>errore %1 di Hamlib</source>
        <translation>Hamlib エラー %1</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="270" />
        <source>indirizzo vuoto</source>
        <translation>アドレスが空です</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="279" />
        <source>nessuna risposta da %1:%2</source>
        <translation>%1:%2 から応答がありません</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="280" />
        <source>%1:%2 — %3</source>
        <translation>%1:%2 — %3</translation>
    </message>
</context>
</TS>