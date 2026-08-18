// misuratori.h — potenza, ROS e ALC, disegnati.
//
// Le tre misure c'erano gia' e finivano in una riga di testo che compariva solo
// mentre la radio trasmetteva: chi guardava la finestra non vedeva niente, e
// non aveva modo di sapere se il collegamento con la radio le stesse portando
// davvero. Un misuratore deve vedersi anche quando segna zero.
//
// Tre barrette, disegnate a mano invece che con tre QProgressBar: servono
// colori che cambiano col valore — il ROS che diventa rosso quando l'antenna
// non risponde e' l'unica cosa che si guarda davvero — e una scala che per il
// ROS non e' lineare.
#pragma once

#include <QLabel>
#include <QPainter>
#include <QWidget>

namespace dl {

class Misuratori final : public QWidget
{
public:
    explicit Misuratori(QWidget* parent = nullptr) : QWidget(parent)
    {
        setFixedHeight(34);
        setMinimumWidth(240);
    }

    // Le tre misure. Un valore negativo vuol dire «non lo so»: la radio non
    // espone quel misuratore, oppure non sta trasmettendo. E' diverso da zero,
    // e va mostrato in modo diverso — zero su un rosmetro vorrebbe dire
    // antenna perfetta.
    void aggiorna(double watt, double ros, double alcPercento)
    {
        m_watt = watt; m_ros = ros; m_alc = alcPercento;
        update();
    }

    void spegni() { aggiorna(-1, -1, -1); }

    // Quanti watt segna la radio al massimo, per dare una scala alla barra.
    // Cento e' il fondo scala di quasi tutti i ricetrasmettitori da stazione.
    void setPotenzaMassima(double w) { m_wattMax = w > 1 ? w : 100.0; update(); }

protected:
    void paintEvent(QPaintEvent*) override
    {
        QPainter p(this);
        p.setRenderHint(QPainter::Antialiasing, true);

        int const n = 3;
        int const spazio = 10;
        int const larg = (width() - spazio * (n - 1)) / n;

        disegna(p, 0 * (larg + spazio), larg, QStringLiteral("POT"),
                m_watt, m_watt >= 0 ? m_watt / m_wattMax : -1,
                m_watt >= 0 ? QStringLiteral("%1 W").arg(m_watt, 0, 'f', 0) : QString(),
                QColor(0, 229, 255));

        // Il ROS non e' lineare: da 1,0 a 3,0 c'e' tutto quello che interessa,
        // e sopra 3 la barra e' piena perche' oltre non cambia il consiglio —
        // smetti di trasmettere e guarda l'antenna.
        double const frazioneRos = m_ros >= 1.0 ? qBound(0.0, (m_ros - 1.0) / 2.0, 1.0) : -1;
        QColor coloreRos(54, 216, 173);
        if (m_ros >= 2.0) coloreRos = QColor(233, 176, 92);
        if (m_ros >= 2.5) coloreRos = QColor(255, 107, 107);
        disegna(p, 1 * (larg + spazio), larg, QStringLiteral("ROS"),
                m_ros, frazioneRos,
                m_ros >= 1.0 ? QStringLiteral("%1").arg(m_ros, 0, 'f', 1) : QString(),
                coloreRos);

        // L'ALC oltre il fondo scala vuol dire che si sta sovrapilotando: e' il
        // modo piu' comune di sporcare un segnale senza accorgersene.
        QColor coloreAlc(54, 216, 173);
        if (m_alc > 60) coloreAlc = QColor(233, 176, 92);
        if (m_alc > 85) coloreAlc = QColor(255, 107, 107);
        disegna(p, 2 * (larg + spazio), larg, QStringLiteral("ALC"),
                m_alc, m_alc >= 0 ? m_alc / 100.0 : -1,
                m_alc >= 0 ? QStringLiteral("%1%").arg(m_alc, 0, 'f', 0) : QString(),
                coloreAlc);
    }

private:
    void disegna(QPainter& p, int x, int larg, QString const& nome,
                 double valore, double frazione, QString const& testo,
                 QColor const& colore)
    {
        Q_UNUSED(valore);
        QFont f = font();
        f.setPointSizeF(7.5);
        p.setFont(f);

        // etichetta a sinistra, valore a destra, barra sotto
        p.setPen(QColor(0x5d, 0x7b, 0xa3));
        p.drawText(QRect(x, 0, larg, 13), Qt::AlignLeft | Qt::AlignVCenter, nome);
        if (testo.isEmpty()) {
            p.setPen(QColor(0x3a, 0x50, 0x6b));
            p.drawText(QRect(x, 0, larg, 13), Qt::AlignRight | Qt::AlignVCenter,
                       QStringLiteral("—"));
        } else {
            p.setPen(QColor(0xe8, 0xed, 0xf5));
            QFont g = f; g.setBold(true); p.setFont(g);
            p.drawText(QRect(x, 0, larg, 13), Qt::AlignRight | Qt::AlignVCenter, testo);
            p.setFont(f);
        }

        QRect const letto(x, 17, larg, 7);
        p.setPen(Qt::NoPen);
        p.setBrush(QColor(0x0b, 0x10, 0x18));
        p.drawRoundedRect(letto, 3, 3);
        p.setBrush(QColor(0x24, 0x3b, 0x63));
        p.drawRoundedRect(letto.adjusted(0, 0, 0, 0), 3, 3);

        if (frazione >= 0) {
            int const w = int(letto.width() * qBound(0.0, frazione, 1.0));
            if (w > 2) {
                p.setBrush(colore);
                p.drawRoundedRect(QRect(letto.left(), letto.top(), w, letto.height()), 3, 3);
            }
        }
    }

    double m_watt {-1}, m_ros {-1}, m_alc {-1};
    double m_wattMax {100.0};
};

} // namespace dl
