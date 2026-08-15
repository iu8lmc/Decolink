#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prima pagina: rumeno, lettone, russo, giapponese, cinese semplificato e tradizionale."""

T3 = {}

T3["ro"] = {
    "html": "ro",
    "claim": "Adu-ți stația pe Decodium Mobile",
    "sotto": "Audio recepționat și comanda stației călătoresc prin internet, de acasă "
             "pe telefon, oriunde ar fi. E de ajuns placa de sunet a stației: fără "
             "cablu OTG, fără Hamlib de instalat pe telefon.",
    "scarica": "Descarcă pentru Windows",
    "peso": "{versione} — {peso} MB, se dezarhivează și pornește",
    "vai_github": "Mergi pe GitHub",
    "senza_ver": "Versiunile sunt pe GitHub",
    "h_cosa": "Ce face",
    "p_cosa": "Trimite pe telefon audio de la CODEC-ul USB al stației și îi ține loc de "
              "rigctld: frecvență, mod și PTT fără să instalezi altceva.",
    "h_serve": "Ce îți trebuie",
    "p_serve": "Windows pe 64 de biți, stația conectată prin USB și un acces la acest "
               "gateway. Nimic de instalat: se dezarhivează și pornește.",
    "h_ovunque": "Merge oriunde",
    "p_ovunque": "Inclusiv pe date mobile: PC-ul și telefonul ies amândouă spre releu, "
                 "așa că nu e niciun router de configurat.",
    "h_parte": "Cum începi",
    "passo1": "Descarcă arhiva și dezarhiveaz-o unde vrei, chiar și pe un stick USB.",
    "passo2_no": "Îți trebuie un acces aprobat: <a href=\"/registrati\">cere-l aici</a>, "
                 "indicând indicativul și stația.",
    "passo2_si": "Îți trebuie un acces aprobat: îl ai deja.",
    "passo3": "Pornește <b>Decolink.exe</b>, scrie <b>{host}</b> ca server de "
              "autentificare, intră cu datele tale și alege stația.",
    "passo4": "Alege intrarea audio a stației, apasă <b>Pornește</b>, iar pe telefon "
              "pune Conexiune = Releu.",
    "h_come": "Cum funcționează",
    "p_come": "Decolink ia sunetul pe care stația îl trimite calculatorului și îl duce "
              "mai departe pe telefon, care îl redă. Pe aceeași legătură trec comenzile "
              "stației, așa că de pe telefon se schimbă frecvența și modul. Telefonul "
              "poate fi în camera de alături sau la celălalt capăt al lumii: se schimbă "
              "doar felul în care cei doi se găsesc.",
    "m1_t": "LAN direct",
    "m1_p": "Telefonul e pe același WiFi: sunetul merge direct la adresa lui. E drumul "
            "cel mai scurt, dar merge doar în casă.",
    "m2_t": "Releu și stație",
    "m2_p": "Merge oriunde, inclusiv pe date mobile. Calculatorul și telefonul ies "
            "amândouă spre releu, deci nu e niciun router de deschis. E singurul mod "
            "care merge întotdeauna.",
    "m3_t": "Telefonul sună acasă",
    "m3_p": "Un port redirecționat pe router și un nume DynDNS. Pentru cine vrea să se "
            "lipsească de releu și știe să-și configureze routerul.",
    "h_banda": "Cât consumă",
    "p_banda": "Alegi cât să ocupe: de la PCM la 48 kHz, care merge cu orice, până la "
               "32 kbit/s pentru voce și 2,4 kbit/s doar pentru ritmul manipulatorului "
               "în CW. Pentru un SSB, care ocupă 2,7 kHz, ajunge cu prisosință o "
               "eșantionare la 12 kHz.",
    "h_lingue": "Șaisprezece limbi",
    "p_lingue": "Decolink preia limba din Windows la prima deschidere, iar schimbarea "
                "se face din meniul din dreapta sus. Italiană, engleză, germană, "
                "franceză, spaniolă, portugheză, neerlandeză, catalană, daneză, "
                "maghiară, română, letonă, rusă, japoneză, chineză simplificată și "
                "tradițională.",
    "accedi": "Autentificare",
    "registrati": "Cere un acces",
    "gia": "Ai deja un acces?",
    "sorgente": "Cod sursă și istoricul versiunilor:",
    "lingua_et": "Limba",
}

T3["lv"] = {
    "html": "lv",
    "claim": "Aizved savu radio uz Decodium Mobile",
    "sotto": "Uztvertais skaņas signāls un radio vadība ceļo pa internetu — no mājām uz "
             "telefonu, lai kur tas būtu. Pietiek ar radio skaņas karti: nav vajadzīgs "
             "OTG kabelis, nav jāinstalē Hamlib telefonā.",
    "scarica": "Lejupielādēt Windows videi",
    "peso": "{versione} — {peso} MB, izpako un palaid",
    "vai_github": "Uz GitHub",
    "senza_ver": "Versijas ir GitHub",
    "h_cosa": "Ko tas dara",
    "p_cosa": "Nosūta uz telefonu radio USB CODEC skaņu un darbojas kā rigctld: "
              "frekvence, režīms un PTT, neko citu neinstalējot.",
    "h_serve": "Kas nepieciešams",
    "p_serve": "64 bitu Windows, ar USB pieslēgts radio un piekļuve šim vārtejai. Nekas "
               "nav jāinstalē: izpako un palaid.",
    "h_ovunque": "Darbojas visur",
    "p_ovunque": "Arī mobilajos datos: dators un telefons abi savienojas ar releju, "
                 "tāpēc nav jākonfigurē neviens maršrutētājs.",
    "h_parte": "Kā sākt",
    "passo1": "Lejupielādē arhīvu un izpako to, kur vēlies — kaut vai USB atmiņā.",
    "passo2_no": "Vajadzīga apstiprināta piekļuve: <a href=\"/registrati\">pieprasi to "
                 "šeit</a>, norādot savu izsaukuma signālu un staciju.",
    "passo2_si": "Vajadzīga apstiprināta piekļuve: tā tev jau ir.",
    "passo3": "Palaid <b>Decolink.exe</b>, ieraksti <b>{host}</b> kā pieteikšanās "
              "serveri, piesakies ar saviem datiem un izvēlies staciju.",
    "passo4": "Izvēlies radio audio ieeju, nospied <b>Sākt</b>, bet telefonā iestati "
              "Savienojums = Relejs.",
    "h_come": "Kā tas darbojas",
    "p_come": "Decolink paņem skaņu, ko radio sūta datoram, un nodod to telefonam, kas "
              "to atskaņo. Pa to pašu savienojumu iet radio komandas, tāpēc frekvenci "
              "un režīmu var mainīt no telefona. Telefons var būt blakus istabā vai "
              "otrā pasaules malā: mainās tikai tas, kā abi viens otru atrod.",
    "m1_t": "Tiešs LAN",
    "m1_p": "Telefons ir tajā pašā WiFi: skaņa iet tieši uz tā adresi. Īsākais ceļš, "
            "bet derīgs tikai mājās.",
    "m2_t": "Relejs un stacija",
    "m2_p": "Darbojas visur, arī mobilajos datos. Dators un telefons abi savienojas ar "
            "releju, tāpēc nav jāatver neviens maršrutētājs. Tas ir vienīgais veids, "
            "kas darbojas vienmēr.",
    "m3_t": "Telefons zvana uz mājām",
    "m3_p": "Pāradresēts ports maršrutētājā un DynDNS vārds. Tiem, kas grib iztikt bez "
            "releja un prot konfigurēt savu maršrutētāju.",
    "h_banda": "Cik daudz patērē",
    "p_banda": "Tu izvēlies, cik daudz: no PCM ar 48 kHz, kas der visam, līdz "
               "32 kbit/s balsij un 2,4 kbit/s tikai CW manipulācijas ritmam. SSB, kas "
               "aizņem 2,7 kHz, ar 12 kHz iztveršanu pietiek ar uzviju.",
    "h_lingue": "Sešpadsmit valodas",
    "p_lingue": "Decolink pirmajā palaišanas reizē pārņem Windows valodu, un to var "
                "mainīt izvēlnē augšējā labajā stūrī. Itāļu, angļu, vācu, franču, "
                "spāņu, portugāļu, holandiešu, katalāņu, dāņu, ungāru, rumāņu, latviešu, "
                "krievu, japāņu, vienkāršotā un tradicionālā ķīniešu.",
    "accedi": "Pieteikties",
    "registrati": "Pieprasīt piekļuvi",
    "gia": "Jau ir piekļuve?",
    "sorgente": "Pirmkods un versiju vēsture:",
    "lingua_et": "Valoda",
}

T3["ru"] = {
    "html": "ru",
    "claim": "Возьмите свой трансивер в Decodium Mobile",
    "sotto": "Принятый звук и управление трансивером идут через интернет — из дома на "
             "телефон, где бы он ни был. Достаточно звуковой карты трансивера: без "
             "кабеля OTG и без установки Hamlib на телефон.",
    "scarica": "Скачать для Windows",
    "peso": "{versione} — {peso} МБ, распаковать и запустить",
    "vai_github": "Перейти на GitHub",
    "senza_ver": "Версии лежат на GitHub",
    "h_cosa": "Что он делает",
    "p_cosa": "Передаёт на телефон звук с USB-кодека трансивера и работает как rigctld: "
              "частота, вид излучения и PTT — больше ничего ставить не нужно.",
    "h_serve": "Что нужно",
    "p_serve": "64-разрядная Windows, трансивер, подключённый по USB, и учётная запись "
               "на этом шлюзе. Устанавливать нечего: распаковать и запустить.",
    "h_ovunque": "Работает везде",
    "p_ovunque": "И в мобильной сети: компьютер и телефон оба подключаются к "
                 "ретранслятору, поэтому роутер настраивать не нужно.",
    "h_parte": "С чего начать",
    "passo1": "Скачайте архив и распакуйте куда угодно — хоть на флешку.",
    "passo2_no": "Нужен одобренный доступ: <a href=\"/registrati\">запросите его "
                 "здесь</a>, указав позывной и станцию.",
    "passo2_si": "Нужен одобренный доступ: он у вас уже есть.",
    "passo3": "Запустите <b>Decolink.exe</b>, впишите <b>{host}</b> как сервер входа, "
              "войдите со своими данными и выберите станцию.",
    "passo4": "Выберите звуковой вход трансивера, нажмите <b>Пуск</b>, а на телефоне "
              "поставьте Подключение = Ретранслятор.",
    "h_come": "Как это работает",
    "p_come": "Decolink берёт звук, который трансивер отдаёт компьютеру, и передаёт его "
              "на телефон, который его воспроизводит. По той же связи идут команды "
              "трансиверу, так что частоту и вид излучения можно менять с телефона. "
              "Телефон может стоять в соседней комнате или на другом конце света: "
              "меняется только то, как эти двое находят друг друга.",
    "m1_t": "Прямая локальная сеть",
    "m1_p": "Телефон в той же сети Wi-Fi: звук идёт прямо на его адрес. Самый короткий "
            "путь, но только дома.",
    "m2_t": "Ретранслятор и станция",
    "m2_p": "Работает везде, в том числе в мобильной сети. Компьютер и телефон оба "
            "подключаются к ретранслятору, поэтому роутер открывать не нужно. Это "
            "единственный способ, который работает всегда.",
    "m3_t": "Телефон звонит домой",
    "m3_p": "Проброшенный порт на роутере и имя DynDNS. Для тех, кто хочет обойтись без "
            "ретранслятора и умеет настроить свой роутер.",
    "h_banda": "Сколько расходует",
    "p_banda": "Вы выбираете, сколько занимать: от PCM 48 кГц, который работает со "
               "всем, до 32 кбит/с для голоса и 2,4 кбит/с для одного лишь ритма ключа "
               "в CW. Для SSB, который занимает 2,7 кГц, с запасом хватает "
               "дискретизации 12 кГц.",
    "h_lingue": "Шестнадцать языков",
    "p_lingue": "При первом запуске Decolink берёт язык Windows, а сменить его можно в "
                "меню справа вверху. Итальянский, английский, немецкий, французский, "
                "испанский, португальский, нидерландский, каталанский, датский, "
                "венгерский, румынский, латышский, русский, японский, китайский "
                "упрощённый и традиционный.",
    "accedi": "Войти",
    "registrati": "Запросить доступ",
    "gia": "Доступ уже есть?",
    "sorgente": "Исходный код и история версий:",
    "lingua_et": "Язык",
}

T3["ja"] = {
    "html": "ja",
    "claim": "無線機を Decodium Mobile へ",
    "sotto": "受信音も無線機の操作もインターネットを通り、自宅からスマートフォンへ、"
             "どこにいても届きます。必要なのは無線機のサウンドカードだけ。OTG ケーブルも、"
             "スマートフォンへの Hamlib のインストールも要りません。",
    "scarica": "Windows 版をダウンロード",
    "peso": "{versione} — {peso} MB、展開して起動するだけ",
    "vai_github": "GitHub へ",
    "senza_ver": "各バージョンは GitHub にあります",
    "h_cosa": "できること",
    "p_cosa": "無線機の USB CODEC の音声をスマートフォンへ送り、rigctld として働きます。"
              "周波数、モード、PTT を、ほかに何も入れずに操作できます。",
    "h_serve": "必要なもの",
    "p_serve": "64 ビット版 Windows、USB でつないだ無線機、そしてこのゲートウェイの"
               "アカウント。インストールは不要で、展開して起動するだけです。",
    "h_ovunque": "どこでも使えます",
    "p_ovunque": "モバイル回線でも同じです。パソコンもスマートフォンもリレーへ発信するので、"
                 "ルーターの設定は要りません。",
    "h_parte": "使いはじめ方",
    "passo1": "アーカイブをダウンロードし、好きな場所に展開します。USB メモリでも構いません。",
    "passo2_no": "承認されたアカウントが必要です。<a href=\"/registrati\">こちらから申請</a>"
                 "し、コールサインと局を記入してください。",
    "passo2_si": "承認されたアカウントが必要です。すでにお持ちです。",
    "passo3": "<b>Decolink.exe</b> を起動し、ログインサーバーに <b>{host}</b> と入力、"
              "認証情報でログインして局を選びます。",
    "passo4": "無線機の音声入力を選び、<b>開始</b> を押して、スマートフォン側で"
              "「接続 = リレー」に設定します。",
    "h_come": "しくみ",
    "p_come": "Decolink は無線機がパソコンへ送る音声を受け取り、スマートフォンへ中継して"
              "鳴らします。同じ回線を無線機のコマンドも通るので、周波数もモードも"
              "スマートフォンから変えられます。スマートフォンは隣の部屋にあっても"
              "地球の裏側にあっても構いません。変わるのは、二台がどう出会うかだけです。",
    "m1_t": "LAN 直結",
    "m1_p": "スマートフォンが同じ Wi-Fi 上にある場合、音声はその IP へ直接届きます。"
            "最短経路ですが、家の中でしか使えません。",
    "m2_t": "リレーと局",
    "m2_p": "モバイル回線を含め、どこでも動きます。パソコンもスマートフォンもリレーへ"
            "発信するため、ルーターを開ける必要がありません。常に使える唯一の方法です。",
    "m3_t": "スマートフォンから接続",
    "m3_p": "ルーターのポート転送と DynDNS 名を使います。リレーを使わずに済ませたい、"
            "自分でルーターを設定できる方向けです。",
    "h_banda": "通信量",
    "p_banda": "どれだけ使うかは選べます。すべてに対応する 48 kHz の PCM から、"
               "音声用の 32 kbit/s、CW の打鍵リズムだけなら 2.4 kbit/s まで。"
               "帯域 2.7 kHz の SSB なら、12 kHz のサンプリングで十分すぎます。",
    "h_lingue": "16 の言語",
    "p_lingue": "Decolink は初回起動時に Windows の言語をそのまま使い、右上のメニューで"
                "変更できます。イタリア語、英語、ドイツ語、フランス語、スペイン語、"
                "ポルトガル語、オランダ語、カタルーニャ語、デンマーク語、ハンガリー語、"
                "ルーマニア語、ラトビア語、ロシア語、日本語、簡体字中国語、繁体字中国語。",
    "accedi": "ログイン",
    "registrati": "アカウントを申請",
    "gia": "すでにアカウントをお持ちですか?",
    "sorgente": "ソースコードとバージョン履歴:",
    "lingua_et": "言語",
}

T3["zh"] = {
    "html": "zh-Hans",
    "claim": "把你的电台带进 Decodium Mobile",
    "sotto": "接收到的音频和电台控制都通过互联网传输，从家里送到手机上，无论手机在哪里。"
             "只需要电台的声卡：不用 OTG 线，也不用在手机上安装 Hamlib。",
    "scarica": "下载 Windows 版",
    "peso": "{versione} — {peso} MB，解压即用",
    "vai_github": "前往 GitHub",
    "senza_ver": "各版本在 GitHub 上",
    "h_cosa": "它做什么",
    "p_cosa": "把电台 USB CODEC 的音频送到手机，并充当 rigctld：频率、模式和 PTT，"
              "无需再装别的东西。",
    "h_serve": "需要什么",
    "p_serve": "64 位 Windows、通过 USB 连接的电台，以及本网关的一个账号。"
               "无需安装：解压即可运行。",
    "h_ovunque": "到处都能用",
    "p_ovunque": "移动数据也一样：电脑和手机都主动连向中继，因此不需要配置任何路由器。",
    "h_parte": "如何开始",
    "passo1": "下载压缩包，解压到任意位置，U 盘也可以。",
    "passo2_no": "需要一个已批准的账号：<a href=\"/registrati\">在此申请</a>，"
                 "填写你的呼号和电台。",
    "passo2_si": "需要一个已批准的账号：你已经有了。",
    "passo3": "运行 <b>Decolink.exe</b>，把 <b>{host}</b> 填为登录服务器，"
              "用你的凭据登录并选择电台。",
    "passo4": "选择电台的音频输入，点击 <b>启动</b>，并在手机上把“连接”设为“中继”。",
    "h_come": "工作原理",
    "p_come": "Decolink 把电台送给电脑的音频接过来，转发到手机上播放。电台的控制命令"
              "走同一条链路，所以在手机上就能改频率和模式。手机可以在隔壁房间，"
              "也可以在地球另一端：变的只是两者如何找到彼此。",
    "m1_t": "局域网直连",
    "m1_p": "手机在同一个 Wi-Fi 上：音频直接发到它的地址。这是最短的路径，但只在家里有效。",
    "m2_t": "中继与电台",
    "m2_p": "到处都能用，移动数据也行。电脑和手机都主动连向中继，因此不用开放路由器端口。"
            "这是唯一始终可用的方式。",
    "m3_t": "手机主动回连",
    "m3_p": "路由器上的端口转发加一个 DynDNS 名称。适合想不用中继、又能配置自己路由器的人。",
    "h_banda": "占用多少流量",
    "p_banda": "占用多少由你决定：从兼容一切的 48 kHz PCM，到语音的 32 kbit/s，"
               "再到只传键控节奏的 2.4 kbit/s。对于只占 2.7 kHz 的 SSB，"
               "12 kHz 采样绰绰有余。",
    "h_lingue": "十六种语言",
    "p_lingue": "Decolink 首次打开时采用 Windows 的语言，可以在右上角的菜单里更改。"
                "意大利语、英语、德语、法语、西班牙语、葡萄牙语、荷兰语、加泰罗尼亚语、"
                "丹麦语、匈牙利语、罗马尼亚语、拉脱维亚语、俄语、日语、简体中文和繁体中文。",
    "accedi": "登录",
    "registrati": "申请账号",
    "gia": "已经有账号了？",
    "sorgente": "源代码与版本历史：",
    "lingua_et": "语言",
}

T3["zh_TW"] = {
    "html": "zh-Hant",
    "claim": "把你的電台帶進 Decodium Mobile",
    "sotto": "接收到的音訊和電台控制都透過網際網路傳輸，從家裡送到手機上，無論手機在哪裡。"
             "只需要電台的音效卡：不用 OTG 線，也不用在手機上安裝 Hamlib。",
    "scarica": "下載 Windows 版",
    "peso": "{versione} — {peso} MB，解壓縮即可使用",
    "vai_github": "前往 GitHub",
    "senza_ver": "各版本在 GitHub 上",
    "h_cosa": "它做什麼",
    "p_cosa": "把電台 USB CODEC 的音訊送到手機，並充當 rigctld：頻率、模式和 PTT，"
              "不必再裝別的東西。",
    "h_serve": "需要什麼",
    "p_serve": "64 位元 Windows、透過 USB 連接的電台，以及本閘道的一個帳號。"
               "不必安裝：解壓縮即可執行。",
    "h_ovunque": "到處都能用",
    "p_ovunque": "行動數據也一樣：電腦和手機都主動連向中繼，因此不需要設定任何路由器。",
    "h_parte": "如何開始",
    "passo1": "下載壓縮檔，解壓縮到任意位置，隨身碟也可以。",
    "passo2_no": "需要一個已核准的帳號：<a href=\"/registrati\">在此申請</a>，"
                 "填寫你的呼號和電台。",
    "passo2_si": "需要一個已核准的帳號：你已經有了。",
    "passo3": "執行 <b>Decolink.exe</b>，把 <b>{host}</b> 填為登入伺服器，"
              "用你的憑證登入並選擇電台。",
    "passo4": "選擇電台的音訊輸入，點選 <b>啟動</b>，並在手機上把「連線」設為「中繼」。",
    "h_come": "運作原理",
    "p_come": "Decolink 把電台送給電腦的音訊接過來，轉送到手機上播放。電台的控制命令"
              "走同一條連線，所以在手機上就能改頻率和模式。手機可以在隔壁房間，"
              "也可以在地球另一端：變的只是兩者如何找到彼此。",
    "m1_t": "區域網路直連",
    "m1_p": "手機在同一個 Wi-Fi 上：音訊直接送到它的位址。這是最短的路徑，但只在家裡有效。",
    "m2_t": "中繼與電台",
    "m2_p": "到處都能用，行動數據也行。電腦和手機都主動連向中繼，因此不必開放路由器連接埠。"
            "這是唯一始終可用的方式。",
    "m3_t": "手機主動回連",
    "m3_p": "路由器上的連接埠轉發加一個 DynDNS 名稱。適合想不用中繼、又能設定自己路由器的人。",
    "h_banda": "佔用多少流量",
    "p_banda": "佔用多少由你決定：從相容一切的 48 kHz PCM，到語音的 32 kbit/s，"
               "再到只傳鍵控節奏的 2.4 kbit/s。對於只佔 2.7 kHz 的 SSB，"
               "12 kHz 取樣綽綽有餘。",
    "h_lingue": "十六種語言",
    "p_lingue": "Decolink 首次開啟時採用 Windows 的語言，可以在右上角的選單裡變更。"
                "義大利語、英語、德語、法語、西班牙語、葡萄牙語、荷蘭語、加泰隆尼亞語、"
                "丹麥語、匈牙利語、羅馬尼亞語、拉脫維亞語、俄語、日語、簡體中文和繁體中文。",
    "accedi": "登入",
    "registrati": "申請帳號",
    "gia": "已經有帳號了？",
    "sorgente": "原始碼與版本歷史：",
    "lingua_et": "語言",
}
