# Genera l'icona del client (hfgw.ico), stile Decodium: fondo scuro,
# antenna con onde in ciano e la traccia audio che viaggia. Multi-risoluzione,
# disegnata a 512 e ridotta, cosi' resta leggibile anche a 16 px.
import os

from PIL import Image, ImageDraw

S = 512
BG1, BG2 = (14, 26, 36), (8, 11, 16)      # gradiente scuro
CYAN     = (53, 184, 240)
BRIGHT   = (127, 214, 255)
GREEN    = (94, 240, 138)

img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# fondo: quadrato arrotondato con gradiente verticale
bg = Image.new("RGB", (1, S))
for y in range(S):
    t = y / (S - 1)
    bg.putpixel((0, y), tuple(int(BG1[i] + (BG2[i] - BG1[i]) * t) for i in range(3)))
bg = bg.resize((S, S))
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=255)
img.paste(bg, (0, 0), mask)

# antenna: palo verticale + base
cx, top, bot = int(S * 0.34), int(S * 0.22), int(S * 0.78)
d.line([(cx, top), (cx, bot)], fill=BRIGHT, width=int(S * 0.045))
d.line([(cx - int(S * 0.10), bot), (cx + int(S * 0.10), bot)], fill=BRIGHT, width=int(S * 0.04))

# onde che partono dall'antenna verso destra (tre archi crescenti)
for i, r in enumerate((0.16, 0.27, 0.38)):
    rr = int(S * r)
    box = [cx - rr, int(S * 0.40) - rr, cx + rr, int(S * 0.40) + rr]
    d.arc(box, start=-62, end=62, fill=CYAN if i < 2 else BRIGHT, width=int(S * 0.035))

# traccia audio in basso: il segnale che scorre verso il telefono
y0 = int(S * 0.74)
pts = []
import math
for x in range(int(S * 0.16), int(S * 0.86)):
    t = (x - S * 0.16) / (S * 0.70)
    amp = int(S * 0.055) * math.sin(t * math.pi * 5.0) * (0.35 + 0.65 * t)
    pts.append((x, y0 + amp))
d.line(pts, fill=GREEN, width=int(S * 0.028), joint="curve")

sizes = [16, 24, 32, 48, 64, 128, 256]
# Accanto a questo file, non a un percorso assoluto: l'icona deve finire nella
# cartella del progetto ovunque essa sia.
qui = os.path.dirname(os.path.abspath(__file__))
img.save(os.path.join(qui, "hfgw.ico"), sizes=[(s, s) for s in sizes])
img.resize((256, 256), Image.LANCZOS).save(os.path.join(qui, "hfgw.png"))
print("icona creata: hfgw.ico (%s) + hfgw.png" % ", ".join(str(s) for s in sizes))
