# SMN Uzaktan Yardım ikon ve logo üretici (metinler vektör yola çevrilir)
import sys, math, io, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import re
from playwright.sync_api import sync_playwright
_pw = sync_playwright().start()
_br = _pw.chromium.launch()
_pg = _br.new_page()
def _render(svgtxt, w, h):
    svgtxt = re.sub(r'width="[0-9.]+" height="[0-9.]+"', f'width="{w}" height="{h}"', svgtxt, count=1)
    _pg.set_viewport_size({"width": w, "height": h})
    _pg.set_content(f'<html><body style="margin:0;background:transparent">{svgtxt}</body></html>')
    return _pg.screenshot(omit_background=True, clip={"x":0,"y":0,"width":w,"height":h})
from PIL import Image

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
TURUNCU, KOMUR, BEYAZ = "#F28C1A", "#2F3337", "#FFFFFF"
BOLD = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
SEMI = "/usr/share/fonts/truetype/google-fonts/Poppins-SemiBold.ttf"
if not os.path.exists(SEMI): SEMI = BOLD

def text_path(text, font_path, size, x, y, fill, anchor="start"):
    f = TTFont(font_path); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    upm = f["head"].unitsPerEm; sc = size / upm
    width = sum(f["hmtx"][cmap[ord(c)]][0] for c in text) * sc
    if anchor == "middle": x -= width / 2
    out, cx = [], x
    for c in text:
        g = cmap[ord(c)]; pen = SVGPathPen(gs); gs[g].draw(pen)
        d = pen.getCommands()
        if d:
            out.append(f'<path fill="{fill}" transform="translate({cx:.2f},{y:.2f}) scale({sc:.5f},{-sc:.5f})" d="{d}"/>')
        cx += f["hmtx"][g][0] * sc
    return "".join(out), width

def hexagon(cx, cy, r, rot=30):
    pts = [(cx + r*math.cos(math.radians(60*i+rot)), cy + r*math.sin(math.radians(60*i+rot))) for i in range(6)]
    return " ".join(f"{a:.2f},{b:.2f}" for a, b in pts)

def emblem(cx, cy, r):
    # dış turuncu altıgen, içte kömür altıgen, beyaz SMN
    s = f'<polygon points="{hexagon(cx,cy,r)}" fill="{TURUNCU}"/>'
    s += f'<polygon points="{hexagon(cx,cy,r*0.80)}" fill="{KOMUR}"/>'
    t, _ = text_path("SMN", BOLD, r*0.62, cx, cy + r*0.22, BEYAZ, "middle")
    # alt turuncu çizgi: bağlantı/uzaktan yardım vurgusu
    s += t + f'<rect x="{cx-r*0.38:.2f}" y="{cy+r*0.36:.2f}" width="{r*0.76:.2f}" height="{r*0.08:.2f}" rx="{r*0.04:.2f}" fill="{TURUNCU}"/>'
    return s

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'

icon_svg = svg(256, 256, emblem(128, 128, 126))
open(f"{OUT}/icon.svg", "w").write(icon_svg)

def png(svgtxt, w, h=None):
    return Image.open(io.BytesIO(_render(svgtxt, w, h or w))).convert("RGBA")

for s in (32, 64, 128): png(icon_svg, s).save(f"{OUT}/{s}x{s}.png")
png(icon_svg, 256).save(f"{OUT}/128x128@2x.png")
png(icon_svg, 512).save(f"{OUT}/icon.png")
png(icon_svg, 1024).save(f"{OUT}/mac-icon.png")
big = png(icon_svg, 256)
big.save(f"{OUT}/icon.ico", sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
big.save(f"{OUT}/app_icon.ico", sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
png(icon_svg, 32).save(f"{OUT}/tray-icon.ico", sizes=[(16,16),(32,32)])

# yatay logo (uygulama üst başlığı, 300x60 alana sığar; 2x çözünürlük)
def logo(text_color):
    W, H = 600, 120
    body = emblem(60, 60, 56)
    t1, _ = text_path("SMN Bilişim", BOLD, 46, 132, 58, text_color)
    t2, _ = text_path("Uzaktan Yardım", SEMI, 34, 133, 102, TURUNCU)
    return svg(W, H, body + t1 + t2)
png(logo(KOMUR), 600, 120).save(f"{OUT}/logo.png")
png(logo(KOMUR), 600, 120).save(f"{OUT}/logo_light.png")
png(logo(BEYAZ), 600, 120).save(f"{OUT}/logo_dark.png")
open(f"{OUT}/logo.svg", "w").write(logo(KOMUR))

# taşınabilir paket açılış etiketi (96x32)
lab = svg(192, 64, emblem(32, 32, 30) + text_path("SMN", BOLD, 30, 70, 44, KOMUR)[0])
png(lab, 96, 32).save(f"{OUT}/label.png")
print("ok")
