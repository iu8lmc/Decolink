#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quarta parte: il selettore della lingua e i messaggi delle radio in rete.

Le prime quattro sono comparse col menu delle lingue e non erano ancora nel
dizionario. Le altre nascono dal difetto delle radio in rete: quando il
programma che tiene la radio non risponde, chi legge deve capire che il guasto
e' dall'altra parte e non nel proprio computer.
"""

T4 = {}

T4["lingua dell'interfaccia"] = {
 "en": "interface language", "de": "Sprache der Oberfläche",
 "fr": "langue de l'interface", "es": "idioma de la interfaz",
 "pt": "idioma da interface", "nl": "taal van de interface",
 "ca": "idioma de la interfície", "da": "sprog i brugerfladen",
 "hu": "a felület nyelve", "ro": "limba interfeței",
 "lv": "saskarnes valoda", "ru": "язык интерфейса",
 "ja": "画面の言語", "zh": "界面语言", "zh_TW": "介面語言",
}

T4["Lingua"] = {
 "en": "Language", "de": "Sprache", "fr": "Langue", "es": "Idioma",
 "pt": "Idioma", "nl": "Taal", "ca": "Idioma", "da": "Sprog",
 "hu": "Nyelv", "ro": "Limbă", "lv": "Valoda", "ru": "Язык",
 "ja": "言語", "zh": "语言", "zh_TW": "語言",
}

T4["Il collegamento è aperto: la lingua cambia alla prossima apertura del programma."] = {
 "en": "The link is open: the language will change the next time the program starts.",
 "de": "Die Verbindung läuft: die Sprache wechselt beim nächsten Start des Programms.",
 "fr": "La liaison est ouverte : la langue changera au prochain démarrage du programme.",
 "es": "El enlace está abierto: el idioma cambiará la próxima vez que se abra el programa.",
 "pt": "A ligação está aberta: o idioma muda na próxima abertura do programa.",
 "nl": "De verbinding staat open: de taal verandert bij de volgende start van het programma.",
 "ca": "L'enllaç és obert: l'idioma canviarà la propera vegada que s'obri el programa.",
 "da": "Forbindelsen er åben: sproget skifter, næste gang programmet startes.",
 "hu": "A kapcsolat él: a nyelv a program következő indításakor változik meg.",
 "ro": "Legătura este deschisă: limba se schimbă la următoarea pornire a programului.",
 "lv": "Savienojums ir atvērts: valoda mainīsies, nākamreiz palaižot programmu.",
 "ru": "Связь открыта: язык сменится при следующем запуске программы.",
 "ja": "接続中です: 言語は次回の起動時に切り替わります。",
 "zh": "连接正在进行：语言将在下次启动程序时生效。",
 "zh_TW": "連線正在進行：語言將在下次啟動程式時生效。",
}

T4["Decolink si riavvia per cambiare lingua. Procedo?"] = {
 "en": "Decolink will restart to change language. Go ahead?",
 "de": "Decolink startet neu, um die Sprache zu wechseln. Fortfahren?",
 "fr": "Decolink va redémarrer pour changer de langue. Je continue ?",
 "es": "Decolink se reiniciará para cambiar de idioma. ¿Continúo?",
 "pt": "O Decolink vai reiniciar para mudar de idioma. Continuo?",
 "nl": "Decolink start opnieuw op om de taal te wijzigen. Doorgaan?",
 "ca": "El Decolink es reiniciarà per canviar d'idioma. Continuo?",
 "da": "Decolink genstarter for at skifte sprog. Fortsæt?",
 "hu": "A Decolink újraindul a nyelv módosításához. Folytatja?",
 "ro": "Decolink repornește pentru a schimba limba. Continui?",
 "lv": "Decolink pārstartēsies, lai mainītu valodu. Turpināt?",
 "ru": "Decolink перезапустится, чтобы сменить язык. Продолжить?",
 "ja": "言語を変更するため Decolink を再起動します。よろしいですか?",
 "zh": "Decolink 将重启以更改语言。继续吗？",
 "zh_TW": "Decolink 將重新啟動以變更語言。繼續嗎？",
}

T4["qui c'è Decolink stesso: scegli il programma che tiene davvero la radio, "
   "o cambia la porta TCP qui sotto"] = {
 "en": "that is Decolink itself: pick the program that actually holds the radio, "
       "or change the TCP port below",
 "de": "das ist Decolink selbst: wähle das Programm, das das Funkgerät wirklich hält, "
       "oder ändere den TCP-Port unten",
 "fr": "c'est Decolink lui-même : choisissez le programme qui détient vraiment la radio, "
       "ou changez le port TCP ci-dessous",
 "es": "ahí está el propio Decolink: elige el programa que realmente tiene la radio, "
       "o cambia el puerto TCP de abajo",
 "pt": "aí está o próprio Decolink: escolha o programa que detém mesmo o rádio, "
       "ou mude a porta TCP abaixo",
 "nl": "dat is Decolink zelf: kies het programma dat de set werkelijk bezet, "
       "of wijzig de TCP-poort hieronder",
 "ca": "aquí hi ha el mateix Decolink: tria el programa que té realment la ràdio, "
       "o canvia el port TCP de sota",
 "da": "det er Decolink selv: vælg det program, der faktisk har radioen, "
       "eller skift TCP-porten nedenfor",
 "hu": "ez maga a Decolink: válassza azt a programot, amely valóban birtokolja a rádiót, "
       "vagy módosítsa lent a TCP portot",
 "ro": "aici e chiar Decolink: alege programul care ține cu adevărat radioul, "
       "sau schimbă portul TCP de mai jos",
 "lv": "šeit ir pats Decolink: izvēlieties programmu, kas patiešām tur radio, "
       "vai nomainiet TCP portu zemāk",
 "ru": "здесь сам Decolink: выберите программу, которая действительно держит трансивер, "
       "или измените TCP-порт ниже",
 "ja": "これは Decolink 自身です: 実際に無線機を保持しているプログラムを選ぶか、"
       "下の TCP ポートを変更してください",
 "zh": "这里就是 Decolink 自己：请选择真正占用电台的程序，或修改下面的 TCP 端口",
 "zh_TW": "這裡就是 Decolink 自己：請選擇真正占用電台的程式，或修改下面的 TCP 連接埠",
}

T4["il programma che tiene la radio ha smesso di rispondere — "
   "riaccendi il CAT quando è tornato"] = {
 "en": "the program holding the radio stopped answering — turn CAT back on when it is up again",
 "de": "das Programm mit dem Funkgerät antwortet nicht mehr — CAT wieder einschalten, "
       "sobald es zurück ist",
 "fr": "le programme qui détient la radio ne répond plus — rallumez le CAT quand il est revenu",
 "es": "el programa que tiene la radio ha dejado de responder — vuelve a encender el CAT "
       "cuando esté de nuevo activo",
 "pt": "o programa que detém o rádio deixou de responder — volte a ligar o CAT quando regressar",
 "nl": "het programma dat de set bezet antwoordt niet meer — zet CAT weer aan zodra het "
       "terug is",
 "ca": "el programa que té la ràdio ha deixat de respondre — torna a engegar el CAT quan "
       "hagi tornat",
 "da": "programmet med radioen svarer ikke længere — tænd CAT igen, når det er tilbage",
 "hu": "a rádiót birtokló program nem válaszol többé — kapcsolja vissza a CAT-et, ha újra elérhető",
 "ro": "programul care ține radioul a încetat să răspundă — repornește CAT când revine",
 "lv": "programma, kas tur radio, vairs neatbild — ieslēdziet CAT no jauna, kad tā atgriezīsies",
 "ru": "программа, которая держит трансивер, перестала отвечать — включите CAT снова, "
       "когда она вернётся",
 "ja": "無線機を保持しているプログラムが応答しなくなりました — 復帰したら CAT を入れ直してください",
 "zh": "占用电台的程序已停止响应 — 等它恢复后请重新打开 CAT",
 "zh_TW": "占用電台的程式已停止回應 — 等它恢復後請重新開啟 CAT",
}

T4["errore %1 di Hamlib"] = {
 "en": "Hamlib error %1", "de": "Hamlib-Fehler %1", "fr": "erreur Hamlib %1",
 "es": "error %1 de Hamlib", "pt": "erro %1 do Hamlib", "nl": "Hamlib-fout %1",
 "ca": "error %1 de Hamlib", "da": "Hamlib-fejl %1", "hu": "Hamlib-hiba: %1",
 "ro": "eroare Hamlib %1", "lv": "Hamlib kļūda %1", "ru": "ошибка Hamlib %1",
 "ja": "Hamlib エラー %1", "zh": "Hamlib 错误 %1", "zh_TW": "Hamlib 錯誤 %1",
}

T4["indirizzo vuoto"] = {
 "en": "empty address", "de": "leere Adresse", "fr": "adresse vide",
 "es": "dirección vacía", "pt": "endereço vazio", "nl": "leeg adres",
 "ca": "adreça buida", "da": "tom adresse", "hu": "üres cím",
 "ro": "adresă goală", "lv": "tukša adrese", "ru": "пустой адрес",
 "ja": "アドレスが空です", "zh": "地址为空", "zh_TW": "位址為空",
}

T4["nessuna risposta da %1:%2"] = {
 "en": "no answer from %1:%2", "de": "keine Antwort von %1:%2",
 "fr": "aucune réponse de %1:%2", "es": "sin respuesta de %1:%2",
 "pt": "sem resposta de %1:%2", "nl": "geen antwoord van %1:%2",
 "ca": "cap resposta de %1:%2", "da": "intet svar fra %1:%2",
 "hu": "nincs válasz innen: %1:%2", "ro": "niciun răspuns de la %1:%2",
 "lv": "nav atbildes no %1:%2", "ru": "нет ответа от %1:%2",
 "ja": "%1:%2 から応答がありません", "zh": "%1:%2 没有响应", "zh_TW": "%1:%2 沒有回應",
}

# Host, porta e il motivo dato dal sistema: non c'e' niente da tradurre, ma la
# voce deve esserci o la stringa resterebbe segnata come non finita.
T4["%1:%2 — %3"] = {l: "%1:%2 — %3" for l in
                    ["en", "de", "fr", "es", "pt", "nl", "ca", "da", "hu", "ro",
                     "lv", "ru", "ja", "zh", "zh_TW"]}

T4["versione di Decolink"] = {
 "en": "Decolink version", "de": "Decolink-Version", "fr": "version de Decolink",
 "es": "versión de Decolink", "pt": "versão do Decolink", "nl": "versie van Decolink",
 "ca": "versió del Decolink", "da": "Decolink-version", "hu": "a Decolink verziója",
 "ro": "versiunea Decolink", "lv": "Decolink versija", "ru": "версия Decolink",
 "ja": "Decolink のバージョン", "zh": "Decolink 版本", "zh_TW": "Decolink 版本",
}
