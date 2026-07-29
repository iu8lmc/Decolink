#!/usr/bin/env bash
# Installa il gateway Decolink su un VPS Debian/Ubuntu.
#
#   sudo bash installa.sh
#
# Va lanciato dalla cartella server/ del repository (o da una copia che
# contenga i decolink_*.py e le due unit systemd). Si puo' rieseguire quando
# si vuole: aggiorna i file e riavvia i servizi senza toccare il database, gli
# utenti o la chiave di firma.
set -e

DEST=/opt/decolink
UTENTE=decolink
PORTA_RELAY=${PORTA_RELAY:-5555}
PORTA_WEB=${PORTA_WEB:-8080}

[ "$(id -u)" = "0" ] || { echo "serve root: usa sudo"; exit 1; }
cd "$(dirname "$0")"
for f in decolink_relay.py decolink_web.py decolink_db.py decolink_token.py decolink_admin.py; do
    [ -f "$f" ] || { echo "manca $f: lancia lo script dalla cartella server/"; exit 1; }
done

python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,8) else 1)' \
    || { echo "serve Python 3.8 o piu' recente"; exit 1; }

# Il vecchio relay senza autenticazione tiene la stessa porta UDP: finche' gira,
# il nuovo non riesce nemmeno ad aprirla. Va fermato consapevolmente, perche'
# chi lo sta usando in questo momento perde il collegamento.
if systemctl is-active --quiet hf-relay 2>/dev/null; then
    echo
    echo "ATTENZIONE: hf-relay (il relay senza autenticazione) e' in funzione"
    echo "sulla porta $PORTA_RELAY/udp. Il nuovo gateway non puo' partire finche'"
    echo "quello vecchio la tiene occupata, e fermarlo scollega chi lo sta usando."
    echo
    read -r -p "Fermo e disabilito hf-relay adesso? [s/N] " risposta
    case "$risposta" in
        s|S|si|SI|y|Y) systemctl disable --now hf-relay; echo "  hf-relay fermato." ;;
        *) echo "  lascio hf-relay attivo: il relay nuovo non partira'."
           echo "  In alternativa rilancia con PORTA_RELAY=5556 per usare un'altra porta." ;;
    esac
fi

id -u "$UTENTE" >/dev/null 2>&1 || \
    useradd --system --home "$DEST" --shell /usr/sbin/nologin "$UTENTE"

mkdir -p "$DEST"
install -m 0644 -o "$UTENTE" -g "$UTENTE" decolink_*.py "$DEST/"
[ -f LEGGIMI.md ] && install -m 0644 -o "$UTENTE" -g "$UTENTE" LEGGIMI.md "$DEST/"
chown "$UTENTE:$UTENTE" "$DEST"
chmod 0750 "$DEST"

# Le porte nelle unit si adeguano a quelle scelte, cosi' chi cambia porta non
# deve ricordarsi di modificare anche i file di servizio.
sed "s|decolink_relay.py 5555|decolink_relay.py $PORTA_RELAY|" \
    decolink-relay.service > /etc/systemd/system/decolink-relay.service
sed "s|--port 8080|--port $PORTA_WEB|" \
    decolink-web.service > /etc/systemd/system/decolink-web.service
systemctl daemon-reload

if command -v ufw >/dev/null 2>&1; then
    ufw allow "$PORTA_RELAY/udp" >/dev/null 2>&1 || true
    echo "  aperta la porta $PORTA_RELAY/udp sul firewall"
fi

# Il primo avvio deve creare amministratore e chiave di firma prima che i
# servizi partano: senza un utente attivo nessuno potrebbe entrare, e web e
# relay creerebbero la chiave per conto loro in ordine imprevedibile.
if [ ! -f "$DEST/decolink.db" ]; then
    echo
    echo "Nessun database: creo il primo amministratore e la prima stazione."
    echo
    sudo -u "$UTENTE" python3 "$DEST/decolink_admin.py" init
fi

systemctl enable --now decolink-relay decolink-web
sleep 1

echo
systemctl --no-pager --lines=0 status decolink-relay decolink-web || true
echo
echo "Fatto. Il servizio web ascolta su 127.0.0.1:$PORTA_WEB e va pubblicato"
echo "con nginx + HTTPS su decolink.ft2.it (esempio dentro decolink-web.service)."
echo "Log:  journalctl -u decolink-relay -f"
