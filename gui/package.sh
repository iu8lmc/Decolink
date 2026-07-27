#!/usr/bin/env bash
# Crea il pacchetto autonomo di HF Gateway (cartella copiabile su qualsiasi PC
# Windows, senza Qt installato). Da eseguire nella shell MSYS2/Git Bash.
#
#   bash gui/package.sh            -> dist/HF-Gateway
#
# windeployqt copia le librerie Qt ma NON il runtime MinGW ne' le dipendenze
# transitive: qui si risolvono con ldd finche' non ne restano. Alla fine si
# tolgono i codec video di ffmpeg, che pesano ma non servono all'audio.
set -e

MINGW=/c/msys64/mingw64
SRC=/c/hf-gateway/gui
OUT=/c/hf-gateway/dist/HF-Gateway

[ -f "$SRC/build/hfgw-client.exe" ] || { echo "manca build/hfgw-client.exe: esegui prima gui/build.bat"; exit 1; }

rm -rf "$OUT"; mkdir -p "$OUT"
cp "$SRC/build/hfgw-client.exe" "$OUT/HF-Gateway.exe"
cp "$SRC/hfgw.ico" "$OUT/"

"$MINGW/bin/windeployqt6.exe" --release --no-translations --no-system-d3d-compiler --no-opengl-sw "$OUT/HF-Gateway.exe" >/dev/null

# dipendenze mancanti: ldd le segnala per nome, si copiano finche' non ne restano
cd "$OUT"
for i in 1 2 3 4 5 6; do
  miss=$(for f in HF-Gateway.exe *.dll */*.dll; do ldd "$f" 2>/dev/null; done \
         | grep -i "not found" | awk '{print $1}' | sort -u | grep -vi "^api-ms-win" || true)
  n=0
  for b in $miss; do
    if [ ! -f "$b" ] && [ -f "$MINGW/bin/$b" ]; then cp "$MINGW/bin/$b" .; n=$((n+1)); fi
  done
  [ "$n" -eq 0 ] && break
done

# codec video di ffmpeg: il backend multimediale li carica solo per il video,
# qui si cattura solo audio. Toglierli dimezza il pacchetto.
for pat in x264 x265 aom SvtAv1 rav1e vpx dav1d theora jxl rsvg shaderc \
           openh264 zimg webp openjp gsm ass fribidi harfbuzz-subset placebo dovi vulkan spirv; do
  rm -f -- *"$pat"*.dll
done

# relay per il VPS (serve solo se si usa la modalita' Relay + stanza)
mkdir -p "$OUT/server"
cp /c/hf-gateway/server/hf_relay.py "$OUT/server/" 2>/dev/null || true
cp /c/hf-gateway/server/hf-relay.service "$OUT/server/" 2>/dev/null || true

echo "pacchetto pronto: $OUT  ($(du -sm "$OUT" | cut -f1) MB, $(find "$OUT" -type f | wc -l) file)"
