"""OG image + touch icon for The Flip: an original sampler drawn in code - LCD with a chopped break, sixteen pads. No brand marks."""
import os, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("FLIP_OUT", "/home/claude/flip")
T = lambda n, s: ImageFont.truetype(f"{H}/ttf/{n}.ttf", s)
W, Hh = 1200, 630
BG, INK, RED, CASE, CASE2, PAD, LCD, LCDINK, MUTED = (216, 212, 200), (23, 24, 27), (212, 44, 31), (30, 32, 36), (42, 45, 51), (139, 142, 150), (183, 199, 90), (28, 39, 16), (93, 94, 98)
im = Image.new("RGB", (W, Hh), BG)
# the machine
mx, my, mw, mh = 690, 50, 460, 530
sh = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([mx + 6, my + 22, mx + mw + 6, my + mh + 22], 22, fill=(0, 0, 0, 120))
im = im.convert("RGBA"); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
d = ImageDraw.Draw(im)
d.rounded_rectangle([mx, my, mx + mw, my + mh], 20, fill=CASE)
d.rounded_rectangle([mx, my, mx + mw, my + 120], 20, fill=CASE2); d.rectangle([mx, my + 60, mx + mw, my + 130], fill=CASE)
d.text((mx + 26, my + 22), "FLIP", font=T("archivo-latin-900-italic", 30), fill=(241, 237, 226)); d.text((mx + 108, my + 22), "60", font=T("archivo-latin-900-italic", 30), fill=RED)
d.rectangle([mx + 24, my + 62, mx + mw - 24, my + 64], fill=RED)
# lcd
lx0, ly0, lx1, ly1 = mx + 24, my + 80, mx + mw - 24, my + 190
d.rounded_rectangle([lx0, ly0, lx1, ly1], 8, fill=LCD, outline=(0, 0, 0), width=2)
d.text((lx0 + 12, ly0 + 8), "SEQ 01", font=T("silkscreen-latin-400-normal", 13), fill=LCDINK); d.text((lx1 - 12, ly0 + 8), "CHOP 8", font=T("silkscreen-latin-400-normal", 13), fill=LCDINK, anchor="ra")
rnd = random.Random(7); n = 96; env = 0; cyy = ly0 + 66; bw = (lx1 - lx0 - 24) / n
for i in range(n):
    hit = i % 12 == 0
    env = 1.0 if hit else env * rnd.uniform(.78, .93)
    h = max(2, env * rnd.uniform(.55, 1) * 30)
    x = lx0 + 12 + i * bw
    d.rectangle([x, cyy - h, x + bw * .6, cyy + h], fill=LCDINK)
    if hit:
        for y in range(ly0 + 28, ly1 - 6, 6):
            d.line([(x - 2, y), (x - 2, y + 3)], fill=LCDINK, width=1)
# pads
gx, gy, gap = mx + 24, my + 212, 12
ps = (mw - 48 - 3 * gap) / 4
for r in range(4):
    for c in range(4):
        x, y = gx + c * (ps + gap), gy + r * (ps * .7 + gap)
        hot = (r, c) == (1, 2)
        d.rounded_rectangle([x, y + 4, x + ps, y + ps * .7 + 4], 9, fill=(0, 0, 0))
        d.rounded_rectangle([x, y, x + ps, y + ps * .7], 9, fill=RED if hot else PAD)
        d.text((x + 9, y + 7), f"PAD {r * 4 + c + 1:02d}", font=T("silkscreen-latin-400-normal", 9), fill=(255, 245, 238) if hot else (16, 17, 20))
if True:
    glow = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); x, y = gx + 2 * (ps + gap), gy + 1 * (ps * .7 + gap)
    ImageDraw.Draw(glow).rounded_rectangle([x - 8, y - 8, x + ps + 8, y + ps * .7 + 8], 14, fill=(226, 58, 44, 90))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(14))); d = ImageDraw.Draw(im)
    d.rounded_rectangle([x, y, x + ps, y + ps * .7], 9, fill=RED); d.text((x + 9, y + 7), "PAD 07", font=T("silkscreen-latin-400-normal", 9), fill=(255, 245, 238))
# words
n_src = sys.argv[1] if len(sys.argv) > 1 else ""
d.text((60, 96), "COLD.FYI DEEP DIVE NO. 11", font=T("ibm-plex-mono-latin-600-normal", 20), fill=MUTED)
d.text((52, 130), "THE", font=T("archivo-latin-900-italic", 150), fill=INK)
d.text((52, 262), "FLIP", font=T("archivo-latin-900-italic", 150), fill=RED)
d.text((60, 442), "How sampling works: the breaks, the", font=T("source-serif-4-latin-400-italic", 30), fill=INK)
d.text((60, 482), "machines, the law and the money.", font=T("source-serif-4-latin-400-italic", 30), fill=INK)
d.text((60, 552), "FLIP.COLD.FYI" + (f"  ·  {n_src} SOURCES" if n_src else ""), font=T("ibm-plex-mono-latin-600-normal", 20), fill=MUTED)
d.rectangle([0, Hh - 10, W, Hh], fill=RED)
im.convert("RGB").save(f"{OUT}/og.png", optimize=True)
ic = Image.new("RGB", (180, 180), CASE); z = ImageDraw.Draw(ic)
for r in range(4):
    for c in range(4):
        z.rounded_rectangle([18 + c * 38, 18 + r * 38, 48 + c * 38, 48 + r * 38], 6, fill=RED if (r, c) == (1, 2) else PAD)
ic.save(f"{OUT}/apple-touch-icon.png")
print("og ok")
