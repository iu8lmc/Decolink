<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE TS>
<TS version="2.1" language="zh">
<context>
    <name>Client</name>
    <message>
        <location filename="../main.cpp" line="571" />
        <source>Decolink — la radio su Decodium Mobile</source>
        <translation>Decolink — 在 Decodium Mobile 上使用电台</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="578" />
        <source>LAN diretta</source>
        <translation>局域网直连</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="579" />
        <source>Relay + stazione</source>
        <translation>中继 + 电台</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="580" />
        <source>Il telefono chiama casa</source>
        <translation>手机主动回连</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="581" />
        <source>LAN diretta — il telefono è sulla stessa rete: gli si manda l'audio all'indirizzo
Relay + stazione — funziona ovunque, anche su dati mobili: PC e telefono
   escono entrambi verso il relay, quindi non c'è nessun router da configurare
Il telefono chiama casa — porta inoltrata sul router e nome DynDNS</source>
        <translation>局域网直连 — 手机在同一网络：音频直接发到它的地址
中继 + 电台 — 到处可用，移动数据也行：电脑和手机都向中继发起连接，
   因此不需要配置路由器
手机主动回连 — 需要路由器端口转发和 DynDNS 名称</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="588" />
        <source>IP del telefono, oppure host del relay</source>
        <translation>手机 IP 或中继服务器</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="592" />
        <source>(accedi per scegliere la stazione)</source>
        <translation>(登录后选择电台)</translation>
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
        <translation>每秒发送多少采样。
48 kHz — 808 kbit/s，每小时 364 MB：对任何程序都安全
24 kHz — 424 kbit/s，每小时 191 MB
12 kHz — 232 kbit/s，每小时 104 MB：对只占 2.7 kHz 的 SSB 绰绰有余。

如果手机听起来变快，说明它没有读取声明的采样率：请改回 48 kHz。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="629" />
        <source>PCM</source>
        <translation>PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="630" />
        <source>Voce (Opus)</source>
        <translation>语音 (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="631" />
        <source>CW (Opus)</source>
        <translation>CW (Opus)</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="632" />
        <source>Digitali senza perdite</source>
        <translation>数字模式（无损）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="633" />
        <source>CW a tasto</source>
        <translation>仅 CW 键控</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="634" />
        <source>PCM — compatibile con tutti, nessuna compressione
Voce — Opus a 32 kbit/s: serve un programma aggiornato dall'altra parte
CW — Opus a banda stretta, 20 kbit/s
Digitali — compresso senza perdere un bit, 146 kbit/s
CW a tasto — solo il ritmo del tasto, 2,4 kbit/s: si perde
tutto il contesto (QSB, QRM, chi chiama fuori nota)</source>
        <translation>PCM — 与所有程序兼容，不压缩
语音 — Opus 32 kbit/s：对端需要已更新的程序
CW — 窄带 Opus，20 kbit/s
数字模式 — 无损压缩，146 kbit/s
CW 键控 — 仅键控节奏，2.4 kbit/s：会失去
全部环境信息（QSB、QRM、在频率旁呼叫的人）</translation>
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
        <translation>每个包放多少帧：包越少，需要付出的包头越少，但延迟略增。
20 ms — 延迟最小
40 ms — 带宽减少 18%，延迟无法察觉
60 ms — 减少 24%，适合按流量计费的网络</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="662" />
        <source>Audio radio</source>
        <translation>电台音频</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="663" />
        <source>Modalità</source>
        <translation>连接方式</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="664" />
        <source>Host</source>
        <translation>主机</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="671" />
        <source>stazione</source>
        <translation>电台</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="675" />
        <source>Porta</source>
        <translation>端口</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="683" />
        <source>Profilo</source>
        <translation>配置</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="684" />
        <source>Campionamento</source>
        <translation>采样率</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="685" />
        <source>Pacchetti da</source>
        <translation>分组时长</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="691" />
        <location filename="../main.cpp" line="697" />
        <source>▸  Impostazioni avanzate</source>
        <translation>▸  高级设置</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="696" />
        <source>▾  Impostazioni avanzate</source>
        <translation>▾  高级设置</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="703" />
        <location filename="../main.cpp" line="2182" />
        <location filename="../main.cpp" line="2442" />
        <source>Avvia</source>
        <translation>启动</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="709" />
        <location filename="../main.cpp" line="2184" />
        <source>fermo</source>
        <translation>已停止</translation>
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
        <translation>Hamlib %1 — 识别 %2 个型号。
前两项是写在 Decolink 内部的协议；
其余通过 Hamlib，与桌面版 Decodium 使用同一个库。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="748" />
        <source>host:porta del programma che tiene la radio</source>
        <translation>占用电台的程序的 主机:端口</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="750" />
        <source>Indirizzo del programma che tiene la porta seriale.
rigctld e i programmi compatibili: localhost:4532
FLRig: localhost:12345

Serve quando la COM è già occupata da un altro programma:
la porta seriale è di chi la apre per primo, e in due non
ci si sta.</source>
        <translation>占用串口的程序地址。
rigctld 及兼容程序：localhost:4532
FLRig：localhost:12345

当 COM 口已被其他程序占用时使用：
串口属于先打开它的程序，两个程序无法共用。</translation>
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
        <translation>无</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="770" />
        <source>pari</source>
        <translation>偶</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="771" />
        <source>dispari</source>
        <translation>奇</translation>
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
        <translation>无</translation>
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
        <translation>向手机提供 CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="782" />
        <location filename="../main.cpp" line="1315" />
        <source>CAT spento</source>
        <translation>CAT 已关闭</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="785" />
        <source>(nessuna: non trasmettere)</source>
        <translation>（无：不发射）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="793" />
        <source>Radio / protocollo</source>
        <translation>电台 / 协议</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="794" />
        <source>Indirizzo CI-V</source>
        <translation>CI-V 地址</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="795" />
        <source>L'indirizzo con cui il rig risponde sul bus CI-V.
IC-7300: 0x94 (predefinito di fabbrica). Se e' stato cambiato nei
menu della radio, va scritto lo stesso valore qui.</source>
        <translation>电台在 CI-V 总线上应答的地址。
IC-7300：0x94（出厂默认）。若在电台菜单里改过，
这里要填同样的值。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="800" />
        <source>Audio al rig</source>
        <translation>送往电台的音频</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="807" />
        <source>Porta rig</source>
        <translation>电台端口</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="812" />
        <source>TCP</source>
        <translation>TCP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="817" />
        <source>Velocità</source>
        <translation>波特率</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="824" />
        <source>dati</source>
        <translation>数据位</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="828" />
        <source>parità</source>
        <translation>校验</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="832" />
        <source>stop</source>
        <translation>停止位</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="836" />
        <source>Seriale</source>
        <translation>串口</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="837" />
        <source>Handshake</source>
        <translation>流控</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="866" />
        <source>server di accesso (es. decolink.ft2.it)</source>
        <translation>登录服务器（例如 decolink.ft2.it）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="868" />
        <source>la tua email</source>
        <translation>你的邮箱</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="871" />
        <source>password</source>
        <translation>密码</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="872" />
        <source>ricorda la password</source>
        <translation>记住密码</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="873" />
        <source>Viene salvata in chiaro fra le impostazioni di Windows: conviene solo su un computer di cui ti fidi.</source>
        <translation>会以明文保存在 Windows 设置中：只建议在你信任的电脑上使用。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="875" />
        <source>Accedi</source>
        <translation>登录</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="876" />
        <source>non collegato</source>
        <translation>未连接</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="886" />
        <source>Server</source>
        <translation>服务器</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="892" />
        <source>Accesso</source>
        <translation>登录</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="914" />
        <source>lingua dell'interfaccia</source>
        <translation>界面语言</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="930" />
        <source>COLLEGAMENTO</source>
        <translation>连接</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="938" />
        <source>RADIO E CAT</source>
        <translation>电台与 CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="961" />
        <source>livello audio</source>
        <translation>音频电平</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1016" />
        <source>campionamento a %1 kHz: se il telefono lo sente accelerato, torna a 48</source>
        <translation>采样率 %1 kHz：如果手机听起来变快，请改回 48</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1104" />
        <location filename="../main.cpp" line="1112" />
        <source>Lingua</source>
        <translation>语言</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1105" />
        <source>Il collegamento è aperto: la lingua cambia alla prossima apertura del programma.</source>
        <translation>连接正在进行：语言将在下次启动程序时生效。</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1113" />
        <source>Decolink si riavvia per cambiare lingua. Procedo?</source>
        <translation>Decolink 将重启以更改语言。继续吗？</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1137" />
        <source>IP del telefono sulla rete locale</source>
        <translation>手机在本地网络中的 IP</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1140" />
        <source>host del relay (es. decolink.ft2.it)</source>
        <translation>中继服务器（例如 decolink.ft2.it）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1143" />
        <source>(il telefono chiama questa porta)</source>
        <translation>（手机呼叫这个端口）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1154" />
        <source>manca il server di accesso</source>
        <translation>缺少登录服务器</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1156" />
        <source>servono email e password</source>
        <translation>需要邮箱和密码</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1178" />
        <source>accesso in corso…</source>
        <translation>正在登录…</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1198" />
        <source>risposta incomprensibile dal server</source>
        <translation>无法解析服务器的回复</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1235" />
        <source>%1 — stazione %2, come %3%4</source>
        <translation>%1 — 电台 %2，身份：%3%4</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1258" />
        <source>%1 — %2</source>
        <translation>%1 — %2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1294" />
        <source>credenziali scadute: rifaccio l'accesso</source>
        <translation>凭据已过期：正在重新登录</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1297" />
        <source>manca l'accesso: premi Accedi, poi Avvia</source>
        <translation>尚未登录：请先点“登录”，再点“启动”</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1327" />
        <source>nessuna porta seriale</source>
        <translation>没有串口</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1336" />
        <source>indirizzo CI-V non valido</source>
        <translation>CI-V 地址无效</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1345" />
        <source>manca l'indirizzo del programma che tiene la radio</source>
        <translation>缺少占用电台的程序地址</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1362" />
        <source>qui c'è Decolink stesso: scegli il programma che tiene davvero la radio, o cambia la porta TCP qui sotto</source>
        <translation>这里就是 Decolink 自己：请选择真正占用电台的程序，或修改下面的 TCP 端口</translation>
    </message>
    <message>
        <source>la porta TCP %1 e' la stessa a cui ti stai collegando: cambiane una</source>
        <translation>TCP 端口 %1 与你要连接的端口相同：请改一个</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1378" />
        <source>%1 non risponde: %2</source>
        <translation>%1 无响应：%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1391" />
        <source>%1 non si apre: %2</source>
        <translation>无法打开 %1：%2</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1399" />
        <source>porta TCP %1 occupata (rigctld è già in esecuzione?)</source>
        <translation>TCP 端口 %1 被占用（rigctld 是否已在运行？）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1447" />
        <source>rig: %1 MHz  %2   (TCP %3, e sul canale audio)</source>
        <translation>电台：%1 MHz  %2   （TCP %3，并通过音频通道）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1460" />
        <source>il programma che tiene la radio ha smesso di rispondere — riaccendi il CAT quando è tornato</source>
        <translation>占用电台的程序已停止响应 — 等它恢复后请重新打开 CAT</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1462" />
        <source>rig non risponde sulla seriale</source>
        <translation>电台在串口上无响应</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1490" />
        <source>telefono connesso da %1:%2</source>
        <translation>手机已从 %1:%2 连接</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1540" />
        <source>credenziali da rinnovare: rifaccio l'accesso</source>
        <translation>凭据需要更新：正在重新登录</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1544" />
        <source>il relay ha rifiutato il collegamento: %1</source>
        <translation>中继拒绝了连接：%1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1552" />
        <source>il telefono è entrato nella stanza</source>
        <translation>手机已加入房间</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1554" />
        <source>registrato sul relay come %1 (%2)</source>
        <translation>已在中继上注册为 %1（%2）</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1661" />
        <source>il telefono legge i pacchetti raggruppati: banda ridotta</source>
        <translation>手机可读取合并的数据包：带宽已降低</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1683" />
        <source>profilo su richiesta del telefono: %1</source>
        <translation>手机请求的配置：%1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1977" />
        <location filename="../main.cpp" line="2158" />
        <source>%1 non supporta 48 kHz mono 16 bit</source>
        <translation>%1 不支持 48 kHz 单声道 16 位</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1985" />
        <source>trasmissione dal telefono in corso</source>
        <translation>正在从手机发射</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="1996" />
        <source>trasmissione finita</source>
        <translation>发射结束</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2047" />
        <source>registrato, ma nella stazione non c'è nessun altro: il telefono non è ancora entrato</source>
        <translation>已注册，但电台里没有其他人：手机尚未加入</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2050" />
        <source>attenzione: profilo %1, ma il telefono non ha confermato di saperlo leggere — se non senti niente, passa a PCM 48 kHz</source>
        <translation>注意：配置为 %1，但手机未确认能否读取 — 如果听不到声音，请切换到 PCM 48 kHz</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2064" />
        <source>telefono non più raggiungibile — attendo che richiami</source>
        <translation>手机已失联 — 等待它重新连接</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2106" />
        <source>Opus non si avvia (%1): resto sul PCM</source>
        <translation>Opus 无法启动（%1）：保持 PCM</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2122" />
        <source>manca l'host di destinazione</source>
        <translation>缺少目标主机</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2125" />
        <source>nome non risolto: %1</source>
        <translation>无法解析名称：%1</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2130" />
        <source>accedi prima: il relay non accetta collegamenti senza credenziali</source>
        <translation>请先登录：中继不接受没有凭据的连接</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2140" />
        <source>porta %1 non disponibile</source>
        <translation>端口 %1 不可用</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2154" />
        <source>nessun ingresso audio</source>
        <translation>没有音频输入</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2163" />
        <source>impossibile aprire l'ingresso audio</source>
        <translation>无法打开音频输入</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2167" />
        <source>Ferma</source>
        <translation>停止</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2171" />
        <source>in ascolto sulla porta %1 — attendo il telefono</source>
        <translation>正在端口 %1 监听 — 等待手机</translation>
    </message>
    <message>
        <location filename="../main.cpp" line="2222" />
        <source>profilo riportato a PCM 48 kHz: i profili compressi richiedono un telefono aggiornato</source>
        <translation>配置已回到 PCM 48 kHz：压缩配置需要更新过的手机</translation>
    </message>
</context>
<context>
    <name>QObject</name>
    <message>
        <location filename="../hamlibrig.h" line="182" />
        <source>errore %1 di Hamlib</source>
        <translation>Hamlib 错误 %1</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="268" />
        <source>indirizzo vuoto</source>
        <translation>地址为空</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="277" />
        <source>nessuna risposta da %1:%2</source>
        <translation>%1:%2 没有响应</translation>
    </message>
    <message>
        <location filename="../hamlibrig.h" line="278" />
        <source>%1:%2 — %3</source>
        <translation>%1:%2 — %3</translation>
    </message>
</context>
</TS>