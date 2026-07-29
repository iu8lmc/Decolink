#!/usr/bin/env bash
# Crea il pacchetto autonomo di HF Gateway (cartella copiabile su qualsiasi PC
# Windows, senza Qt installato) e VERIFICA che funzioni con un ambiente pulito.
#
#   bash gui/package.sh            -> dist/Decolink
#
# Perche' la verifica e' dentro lo script: provando il pacchetto da una shell
# che ha MSYS2 nel PATH sembra funzionare anche se mancano delle librerie,
# perche' Windows le ripesca da li'. Su un altro PC darebbe "errore di
# libreria" all'avvio. Qui si prova con il PATH ripulito, che e' la condizione
# vera dell'utente finale.
set -e

MINGW=/c/msys64/mingw64
# Percorsi ricavati da dove sta questo script, non scritti a mano: la cartella
# del progetto ha gia' cambiato nome una volta e gli script erano rimasti a
# puntare al vecchio, senza dirlo.
SRC=$(cd "$(dirname "$0")" && pwd)
RADICE=$(cd "$SRC/.." && pwd)
OUT=$RADICE/dist/Decolink

[ -f "$SRC/build/decolink.exe" ] || { echo "manca build/decolink.exe: esegui prima gui/build.bat"; exit 1; }

rm -rf "$OUT"; mkdir -p "$OUT"
cp "$SRC/build/decolink.exe" "$OUT/Decolink.exe"
cp "$SRC/hfgw.ico" "$OUT/"
[ -f "$SRC/LEGGIMI.txt" ] && cp "$SRC/LEGGIMI.txt" "$OUT/"

"$MINGW/bin/windeployqt6.exe" --release --no-translations --no-system-d3d-compiler --no-opengl-sw "$OUT/Decolink.exe" >/dev/null

# windeployqt NON copia il runtime del compilatore: senza questi l'exe non
# parte proprio (errore di libreria prima ancora del main).
for b in libgcc_s_seh-1.dll libstdc++-6.dll libwinpthread-1.dll; do
    cp "$MINGW/bin/$b" "$OUT/"
done

# Dipendenze transitive. Attenzione: ldd le risolve usando il PATH, quindi
# quelle presenti in MSYS2 le riporta col percorso /mingw64/bin (NON come
# "not found"): vanno prese in ENTRAMBI i modi, altrimenti il pacchetto sembra
# completo qui e da' errore di libreria su un altro PC.
# Fra queste ci sono i codec di ffmpeg, importati da avcodec all'avvio: senza
# di loro il backend multimediale non si carica e l'elenco dispositivi resta
# vuoto. Per questo non si sfoltiscono.
cd "$OUT"
for i in $(seq 1 10); do
  refs=$(for f in Decolink.exe *.dll */*.dll; do ldd "$f" 2>/dev/null; done)
  names=$( { echo "$refs" | grep -io "/mingw64/bin/[a-z0-9_.+-]*\.dll" | xargs -r -n1 basename
             echo "$refs" | grep -i "not found" | awk '{print $1}'; }            | sort -u | grep -vi "^api-ms-win" || true)
  n=0
  for b in $names; do
    if [ ! -f "$b" ] && [ -f "$MINGW/bin/$b" ]; then cp "$MINGW/bin/$b" .; n=$((n+1)); fi
  done
  [ "$n" -eq 0 ] && break
done

# Parte server: serve a chi ospita il gateway sul proprio VPS. Si copia tutto il
# gruppo (relay, servizio di accesso, amministrazione) perche' i pezzi non
# funzionano separati: il relay senza il servizio web non ha token da verificare.
mkdir -p "$OUT/server"
for f in decolink_relay.py decolink_web.py decolink_db.py decolink_token.py \
         decolink_admin.py decolink-relay.service decolink-web.service \
         nginx-decolink.conf installa.sh LEGGIMI.md; do
    cp "$RADICE/server/$f" "$OUT/server/" 2>/dev/null || true
done

# ---- verifica in ambiente pulito (senza MSYS2 nel PATH) ----
echo "verifica con PATH ripulito..."
set +e
out=$(powershell -NoProfile -ExecutionPolicy Bypass -File "$(cygpath -w "$SRC/verify.ps1")" -Exe "$(cygpath -w "$OUT/Decolink.exe")" 2>&1)
rc=$?
set -e
echo "$out" | sed 's/^/    /'
if [ $rc -ne 0 ]; then
  echo "PACCHETTO NON VALIDO (codice $rc): manca qualcosa, non distribuirlo."
  exit 1
fi
echo "pacchetto pronto e verificato: $OUT  ($(du -sm "$OUT" | cut -f1) MB, $(find "$OUT" -type f | wc -l) file)"
