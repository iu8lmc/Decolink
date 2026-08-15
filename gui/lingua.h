// lingua.h — la lingua dell'interfaccia
//
// Decolink nasce in italiano, e l'italiano resta la lingua di partenza: le
// stringhe nel sorgente sono quelle, senza un catalogo intermedio. Le altre
// quindici arrivano dai .qm dentro l'eseguibile, quindi non c'e' una cartella
// da portarsi dietro quando si copia il solo .exe su un'altra macchina.
//
// La prima volta la lingua non si chiede: si prende quella del sistema. Chi ha
// Windows in tedesco trova Decolink in tedesco senza toccare niente, e se non
// gli va la cambia dal selettore in alto.
#pragma once

#include <QApplication>
#include <QLibraryInfo>
#include <QLocale>
#include <QSettings>
#include <QString>
#include <QStringList>
#include <QTranslator>
#include <QVector>

namespace dl {

struct Lingua {
    char const* codice;   // quello che finisce nelle impostazioni e nel nome del .qm
    char const* nome;     // scritto nella lingua stessa: chi la cerca la riconosce
};

// Le quindici di Decodium piu' il portoghese. L'italiano non ha .qm perche' e'
// gia' dentro il sorgente.
inline QVector<Lingua> const& lingue()
{
    static QVector<Lingua> const v = {
        {"it",    "Italiano"},
        {"en",    "English"},
        {"de",    "Deutsch"},
        {"fr",    "Français"},
        {"es",    "Español"},
        {"pt",    "Português"},
        {"nl",    "Nederlands"},
        {"ca",    "Català"},
        {"da",    "Dansk"},
        {"hu",    "Magyar"},
        {"ro",    "Română"},
        {"lv",    "Latviešu"},
        {"ru",    "Русский"},
        {"ja",    "日本語"},
        {"zh",    "简体中文"},
        {"zh_TW", "繁體中文"},
    };
    return v;
}

inline bool conosciuta(QString const& codice)
{
    for (Lingua const& l : lingue())
        if (codice == QLatin1String(l.codice)) return true;
    return false;
}

// La lingua del sistema ridotta a una che abbiamo. Windows dice "de_AT"; a noi
// basta "de". Il cinese e' il caso che va guardato per intero, perche' fra
// semplificato e tradizionale non e' questione di regione ma di scrittura.
inline QString linguaDiSistema()
{
    QLocale const sistema;
    QString const nome = sistema.name();                 // p.es. "de_AT", "zh_TW"
    if (conosciuta(nome)) return nome;

    if (nome.startsWith(QLatin1String("zh"))) {
        // zh_Hant_*, zh_HK, zh_MO, zh_TW: tradizionale. Il resto semplificato.
        QString const scritt = QLocale::scriptToString(sistema.script());
        if (scritt.contains(QLatin1String("Traditional"), Qt::CaseInsensitive))
            return QStringLiteral("zh_TW");
        QString const regione = nome.mid(3);
        if (regione == QLatin1String("TW") || regione == QLatin1String("HK")
            || regione == QLatin1String("MO"))
            return QStringLiteral("zh_TW");
        return QStringLiteral("zh");
    }

    QString const breve = nome.left(2);
    if (conosciuta(breve)) return breve;
    return QStringLiteral("en");   // meglio l'inglese dell'italiano, per chi capita da fuori
}

// Le stesse chiavi del resto delle impostazioni: la lingua sta con host, porta
// e profilo, non in un angolo suo.
inline QSettings impostazioni()
{
    return QSettings(QStringLiteral("it.ft2"), QStringLiteral("Decolink"));
}

// Quella scelta dall'utente, o quella del sistema la prima volta.
inline QString linguaScelta()
{
    QSettings imp = impostazioni();
    QString const salvata = imp.value(QStringLiteral("lingua")).toString();
    if (conosciuta(salvata)) return salvata;
    return linguaDiSistema();
}

inline void salvaLingua(QString const& codice)
{
    QSettings imp = impostazioni();
    imp.setValue(QStringLiteral("lingua"), codice);
    imp.sync();
}

// Carica i cataloghi. Ne servono due: il nostro e quello di Qt, che traduce i
// pulsanti delle finestre di sistema (Annulla, Sfoglia, Sì/No). Senza il
// secondo l'interfaccia e' tradotta ma le finestre di dialogo no, e si vede.
//
// I traduttori vanno tenuti vivi per tutta la durata del programma: installarli
// e lasciarli morire e' un errore che non da' errori, solo testo non tradotto.
inline void installaTraduttori(QApplication& app, QString const& codice)
{
    if (codice == QLatin1String("it")) return;   // e' gia' la lingua del sorgente

    static QTranslator nostro, diQt;

    if (nostro.load(QStringLiteral(":/traduzioni/%1.qm").arg(codice)))
        app.installTranslator(&nostro);

    // Qt non usa i nostri stessi codici: il portoghese lo spedisce come pt_BR,
    // il cinese semplificato come zh_CN, e per il rumeno non c'e' catalogo. Chi
    // sceglie il rumeno avra' l'interfaccia in rumeno e i pulsanti delle
    // finestre di sistema in inglese: e' quello che Qt mette a disposizione.
    QString suo = codice.left(2);
    if (codice == QLatin1String("pt"))    suo = QStringLiteral("pt_BR");
    if (codice == QLatin1String("zh"))    suo = QStringLiteral("zh_CN");
    if (codice == QLatin1String("zh_TW")) suo = QStringLiteral("zh_TW");

    // Due posti: accanto all'eseguibile, che e' dove finiscono nel pacchetto
    // distribuito, e dove li tiene l'installazione di Qt, che e' il caso di chi
    // compila da sorgente.
    QStringList const posti = {
        QApplication::applicationDirPath() + QStringLiteral("/translations"),
        QLibraryInfo::path(QLibraryInfo::TranslationsPath),
    };
    for (QString const& dove : posti) {
        if (diQt.load(QStringLiteral("qtbase_%1").arg(suo), dove)
            || diQt.load(QStringLiteral("qt_%1").arg(suo), dove)) {
            app.installTranslator(&diQt);
            break;
        }
    }
}

} // namespace dl
