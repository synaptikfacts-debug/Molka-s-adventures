#!/usr/bin/env python3
"""Build Molka's Adventures channel branding (avatar, banner, watermark).

Molka is drawn from code so she is identical everywhere (HARD RULE A1).
Outputs go to channel/brand/: SVG sources + upload-ready PNGs.

Usage: python3 scripts/build_brand.py
Needs: rsvg-convert, Pillow, Inter font (OFL).
"""
import math
import subprocess
from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "channel" / "brand"

# ---- Locked palette (mirrors bible/SERIES_BIBLE.md) -------------------------
FUR = "#FFFFFF"
FUR_SHADE = "#F3ECF8"
OUTLINE = "#B9A3CF"        # soft lavender-grey so white fur never disappears
EYE_OUT, EYE_IN, PUPIL = "#4A2611", "#8A4B26", "#22110A"
NOSE = "#1E1E1E"
BLUSH = "#FF9DC0"
TONGUE = "#FF7FA6"
PAD_PINK, PAD_BLACK = "#FF8FB8", "#2A2A2A"
BOW_LEFT, BOW_RIGHT, BOW_KNOT = "#FF4F9A", "#A66BFF", "#FFD24A"
BRAND_PINK, BRAND_PURPLE = "#FF4F9A", "#8E5BE8"


def fluff(circles, fill=FUR, outline=OUTLINE, w=5):
    """Scalloped fluffy shape: outline layer of bigger circles under fill circles."""
    under = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + w:.1f}" fill="{outline}"/>'
                    for x, y, r in circles)
    over = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"/>'
                   for x, y, r in circles)
    return under + over


def chain(p0, p1, r0, r1, n):
    return [(p0[0] + (p1[0] - p0[0]) * i / (n - 1),
             p0[1] + (p1[1] - p0[1]) * i / (n - 1),
             r0 + (r1 - r0) * i / (n - 1)) for i in range(n)]


def head_circles():
    c = [(0, 0, 92)]
    for k in range(12):
        a = math.radians(k * 30 + 15)
        c.append((math.cos(a) * 92, math.sin(a) * 82, 26))
    return c


def ear(side):
    s = side
    return fluff(chain((s * 78, -30), (s * 104, 128), 38, 30, 7), fill=FUR_SHADE)


def pigtail(side):
    s = side
    # short fountain-style tufts that splay outwards and droop at the tips,
    # so they read as pigtails, not ears
    pts = [(s * 46, -98, 24), (s * 66, -122, 22), (s * 90, -138, 20),
           (s * 114, -142, 18), (s * 134, -134, 16), (s * 146, -118, 13)]
    return fluff(pts)


def bow(side):
    s = side
    color = BOW_LEFT if s < 0 else BOW_RIGHT
    cx, cy = s * 50, -104
    loops = (f'<path d="M {cx} {cy} C {cx-48} {cy-40}, {cx-52} {cy+30}, {cx} {cy} Z" '
             f'fill="{color}" stroke="#ffffff" stroke-width="3" stroke-linejoin="round"/>'
             f'<path d="M {cx} {cy} C {cx+48} {cy-40}, {cx+52} {cy+30}, {cx} {cy} Z" '
             f'fill="{color}" stroke="#ffffff" stroke-width="3" stroke-linejoin="round"/>')
    tails = (f'<path d="M {cx-4} {cy+4} L {cx-16} {cy+30} L {cx-6} {cy+26} Z" fill="{color}"/>'
             f'<path d="M {cx+4} {cy+4} L {cx+16} {cy+30} L {cx+6} {cy+26} Z" fill="{color}"/>')
    dots = "".join(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="3.2" fill="#ffffff" opacity="0.9"/>'
                   for dx, dy in [(-26, -8), (-18, 6), (-32, 4), (24, -8), (18, 6), (32, 4)])
    knot = f'<circle cx="{cx}" cy="{cy}" r="9" fill="{BOW_KNOT}" stroke="#ffffff" stroke-width="2.5"/>'
    return tails + loops + dots + knot


def eye(cx, cy, side):
    lash = (f'<path d="M {cx + side*17} {cy-16} q {side*9} -6 {side*14} -12" stroke="{PUPIL}" '
            f'stroke-width="3.5" fill="none" stroke-linecap="round"/>'
            f'<path d="M {cx + side*20} {cy-8} q {side*9} -2 {side*15} -6" stroke="{PUPIL}" '
            f'stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    return (lash +
            f'<ellipse cx="{cx}" cy="{cy}" rx="20" ry="24" fill="url(#eyeGrad)"/>'
            f'<ellipse cx="{cx+1}" cy="{cy+2}" rx="11" ry="13" fill="{PUPIL}"/>'
            f'<circle cx="{cx-6}" cy="{cy-9}" r="7.5" fill="#fff"/>'
            f'<circle cx="{cx+7}" cy="{cy+9}" r="3.5" fill="#fff"/>')


def face():
    return (eye(-36, 8, -1) + eye(36, 8, 1) +
            f'<ellipse cx="-63" cy="38" rx="15" ry="9" fill="{BLUSH}" opacity="0.6"/>'
            f'<ellipse cx="63" cy="38" rx="15" ry="9" fill="{BLUSH}" opacity="0.6"/>'
            f'<ellipse cx="0" cy="40" rx="15" ry="11" fill="{NOSE}"/>'
            f'<ellipse cx="-4" cy="36" rx="5" ry="3" fill="#fff" opacity="0.65"/>'
            f'<ellipse cx="0" cy="68" rx="7" ry="7" fill="{TONGUE}"/>'
            f'<path d="M 0 51 L 0 59 M -14 60 Q -7 68 0 59 Q 7 68 14 60" stroke="#3A2A2A" '
            f'stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def paw_pads(cx, cy, k=1.0):
    """Pink main pad, toe beans black-pink-pink-black (locked pattern)."""
    beans = [(-17, -14, PAD_BLACK), (-6, -21, PAD_PINK), (6, -21, PAD_PINK), (17, -14, PAD_BLACK)]
    out = f'<ellipse cx="{cx}" cy="{cy + 6*k}" rx="{15*k}" ry="{12*k}" fill="{PAD_PINK}"/>'
    out += "".join(f'<ellipse cx="{cx + dx*k}" cy="{cy + dy*k}" rx="{6*k}" ry="{7*k}" fill="{c}"/>'
                   for dx, dy, c in beans)
    return out


def body(wave=True):
    parts = []
    # tail (behind body)
    parts.append(fluff([(95, 230, 26), (122, 205, 24), (140, 175, 22), (146, 145, 20),
                        (138, 118, 17)], fill=FUR_SHADE))
    # body blob
    c = [(0, 185, 88)] + [(math.cos(math.radians(a)) * 82, 185 + math.sin(math.radians(a)) * 78, 26)
                          for a in range(0, 360, 30)]
    parts.append(fluff(c))
    # front legs + feet
    for s in (-1, 1) if not wave else (-1,):
        parts.append(fluff(chain((s * 38, 230), (s * 42, 280), 30, 28, 4)))
        parts.append(f'<path d="M {s*42-10} 292 l 0 10 M {s*42+4} 293 l 0 10" stroke="{OUTLINE}" '
                     f'stroke-width="3.5" stroke-linecap="round"/>')
    if wave:
        parts.append(fluff(chain((40, 250), (42, 280), 30, 28, 3)))
        parts.append(f'<path d="M 32 292 l 0 10 M 46 293 l 0 10" stroke="{OUTLINE}" '
                     f'stroke-width="3.5" stroke-linecap="round"/>')
    return "".join(parts)


def waving_arm():
    return (fluff(chain((60, 170), (122, 82), 26, 30, 5)) +
            fluff([(128, 66, 34)]) + paw_pads(128, 66, 1.05))


def molka(x, y, s, full_body=False):
    g = [ear(-1), ear(1)]
    if full_body:
        g.append(body(wave=True))
    g += [pigtail(-1), pigtail(1), fluff(head_circles()), bow(-1), bow(1), face()]
    if full_body:
        g.append(waving_arm())
    return f'<g transform="translate({x} {y}) scale({s})">{"".join(g)}</g>'


def sparkle(x, y, r, color="#FFFFFF", op=1.0):
    q = r * 0.28
    return (f'<path d="M {x} {y-r} Q {x+q} {y-q} {x+r} {y} Q {x+q} {y+q} {x} {y+r} '
            f'Q {x-q} {y+q} {x-r} {y} Q {x-q} {y-q} {x} {y-r} Z" fill="{color}" opacity="{op}"/>')


def heart(x, y, s, color, op=1.0):
    return (f'<path transform="translate({x} {y}) scale({s})" d="M 0 8 C -14 -4 -8 -16 0 -8 '
            f'C 8 -16 14 -4 0 8 Z" fill="{color}" opacity="{op}"/>')


def paw_print(x, y, s, color, op=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{color}" opacity="{op}">'
            '<ellipse cx="0" cy="8" rx="13" ry="11"/><ellipse cx="-14" cy="-8" rx="5.5" ry="7"/>'
            '<ellipse cx="-5" cy="-15" rx="5.5" ry="7"/><ellipse cx="5" cy="-15" rx="5.5" ry="7"/>'
            '<ellipse cx="14" cy="-8" rx="5.5" ry="7"/></g>')


DEFS = (f'<defs><radialGradient id="eyeGrad" cx="45%" cy="40%" r="60%">'
        f'<stop offset="0" stop-color="{EYE_IN}"/><stop offset="1" stop-color="{EYE_OUT}"/>'
        f'</radialGradient>'
        '<radialGradient id="avBg" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#FFF0F7"/>'
        '<stop offset="0.7" stop-color="#FFD3E8"/><stop offset="1" stop-color="#E5CCFF"/></radialGradient>'
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CDE8FF"/>'
        '<stop offset="0.55" stop-color="#F3E4FF"/><stop offset="1" stop-color="#FFE3F0"/></linearGradient>'
        '<linearGradient id="badge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF7DB6"/>'
        '<stop offset="1" stop-color="#B07CFF"/></linearGradient></defs>')


def svg(w, h, body_):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{DEFS}{body_}</svg>')


def avatar():
    deco = "".join([sparkle(170, 230, 26), sparkle(640, 210, 20), sparkle(655, 560, 16, op=0.9),
                    sparkle(150, 560, 14, op=0.9), heart(605, 300, 1.4, "#FF8FC4", 0.8),
                    heart(200, 330, 1.1, "#C9A3FF", 0.8)])
    return svg(800, 800, '<rect width="800" height="800" fill="url(#avBg)"/>' + deco +
               molka(400, 430, 1.55))


def watermark():
    return svg(150, 150, '<circle cx="75" cy="75" r="72" fill="url(#badge)" stroke="#fff" '
                         'stroke-width="5"/>' + molka(75, 84, 0.315))


def banner():
    W, H = 2560, 1440
    g = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    # clouds
    for cx, cy, s in [(300, 300, 1.4), (1150, 220, 1.0), (2200, 330, 1.5), (1900, 160, 0.8),
                      (650, 1150, 0.9)]:
        g.append(f'<g transform="translate({cx} {cy}) scale({s})" fill="#FFFFFF" opacity="0.85">'
                 '<circle cx="0" cy="0" r="60"/><circle cx="70" cy="-25" r="75"/>'
                 '<circle cx="150" cy="0" r="58"/><rect x="0" y="0" width="150" height="58"/></g>')
    # hills (ground line sits just under Molka's feet inside the desktop band)
    g.append('<path d="M 0 960 Q 640 860 1280 940 T 2560 920 L 2560 1440 L 0 1440 Z" fill="#C8EFCF"/>')
    g.append('<path d="M 0 1040 Q 700 960 1400 1030 T 2560 1000 L 2560 1440 L 0 1440 Z" fill="#AEE3BC"/>')
    # flowers
    import random
    rnd = random.Random(7)
    for _ in range(70):
        fx, fy = rnd.uniform(0, W), rnd.uniform(975, 1420)
        col = rnd.choice(["#FF8FC4", "#FFD24A", "#C9A3FF", "#FFFFFF", "#FF6FA8"])
        r = rnd.uniform(7, 13)
        g.append("".join(f'<circle cx="{fx + math.cos(a)*r:.1f}" cy="{fy + math.sin(a)*r:.1f}" '
                         f'r="{r*0.7:.1f}" fill="{col}"/>' for a in [k * math.pi * 2 / 5 for k in range(5)]))
        g.append(f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="{r*0.5:.1f}" fill="#FFF3A6"/>')
    # sparkles, hearts, paw prints across whole canvas (decor only)
    for x, y, r in [(520, 560, 22), (2000, 560, 20), (1300, 480, 16), (2350, 700, 26),
                    (180, 720, 24), (1820, 900, 14), (960, 880, 12), (2450, 480, 18), (90, 450, 16)]:
        g.append(sparkle(x, y, r))
    for x, y, s, c in [(2150, 820, 2.0, "#FF8FC4"), (420, 860, 1.6, "#C9A3FF"), (2380, 1200, 2.4, "#FF8FC4"),
                       (140, 1250, 2.2, "#C9A3FF")]:
        g.append(heart(x, y, s, c, 0.85))
    for i, (x, y) in enumerate([(1980, 1180), (2080, 1130), (2180, 1185), (2280, 1135)]):
        g.append(paw_print(x, y, 1.6, "#FFFFFF", 0.7))
    # Molka inside the safe area (x 507–2053, y 508.5–931.5)
    g.append(molka(720, 680, 0.78, full_body=True))
    # title + tagline inside safe area
    cx = 1490
    title = ('font-family="Inter" font-weight="900" text-anchor="middle" '
             'stroke-linejoin="round" paint-order="stroke"')
    g.append(f'<text x="{cx+8}" y="{690+10}" font-size="128" {title} fill="#C9A3FF" '
             f'stroke="#C9A3FF" stroke-width="26">Molka’s</text>')
    g.append(f'<text x="{cx}" y="690" font-size="128" {title} fill="{BRAND_PINK}" '
             f'stroke="#FFFFFF" stroke-width="26">Molka’s</text>')
    g.append(f'<text x="{cx+8}" y="{815+10}" font-size="112" {title} fill="#C9A3FF" '
             f'stroke="#C9A3FF" stroke-width="24">Adventures</text>')
    g.append(f'<text x="{cx}" y="815" font-size="112" {title} fill="{BRAND_PURPLE}" '
             f'stroke="#FFFFFF" stroke-width="24">Adventures</text>')
    g.append(f'<rect x="{cx-400}" y="852" width="800" height="66" rx="33" fill="#FFFFFF" opacity="0.92"/>')
    g.append(f'<text x="{cx}" y="897" font-size="40" font-family="Inter" font-weight="800" '
             f'text-anchor="middle" fill="{BRAND_PINK}">Tiny puppy. Big adventures!</text>')
    g.append(paw_print(cx - 352, 885, 1.1, BRAND_PINK))
    g.append(paw_print(cx + 352, 885, 1.1, BRAND_PURPLE))
    return svg(W, H, "".join(g))


def safe_zone_preview(png):
    """Overlay of YouTube's display areas, for checking only."""
    from PIL import ImageDraw
    im = Image.open(png).convert("RGB")
    d = ImageDraw.Draw(im)
    for (w, h), col, label in [((2560, 1440), "#000000", "TV 2560x1440"),
                               ((2560, 423), "#0066FF", "Desktop max 2560x423"),
                               ((1855, 423), "#00AA55", "Tablet 1855x423"),
                               ((1546, 423), "#FF0000", "SAFE (all devices) 1546x423")]:
        x0, y0 = (2560 - w) / 2, (1440 - h) / 2
        d.rectangle([x0, y0, x0 + w - 1, y0 + h - 1], outline=col, width=6)
        d.text((x0 + 14, y0 + 10), label, fill=col)
    return im


def render(svg_text, name, w, h):
    src = OUT / f"{name}.svg"
    src.write_text(svg_text, encoding="utf-8")
    png = OUT / f"{name}.png"
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), "-o", str(png), str(src)], check=True)
    return png


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    av = render(avatar(), "avatar_800x800", 800, 800)
    bn = render(banner(), "banner_2560x1440", 2560, 1440)
    wm = render(watermark(), "watermark_150x150", 150, 150)
    # banner: flatten to RGB (no transparency needed) and keep under 6 MB
    Image.open(bn).convert("RGB").save(bn, optimize=True)
    Image.open(av).convert("RGB").save(av, optimize=True)
    safe_zone_preview(bn).save(OUT / "banner_safe_zone_preview.png", optimize=True)
    # circle-crop preview of the avatar as YouTube shows it
    from PIL import ImageDraw
    a = Image.open(av).convert("RGBA")
    mask = Image.new("L", a.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 799, 799], fill=255)
    a.putalpha(mask)
    a.resize((98, 98), Image.LANCZOS).save(OUT / "avatar_preview_98px_circle.png")
    for p in sorted(OUT.glob("*.png")):
        im = Image.open(p)
        print(f"{p.name:34s} {im.size[0]}x{im.size[1]} {im.mode:5s} {p.stat().st_size/1024:8.1f} KB")


if __name__ == "__main__":
    main()
