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
BOW, BOW_KNOT = "#FF4F9A", "#FFB3D4"
BRAND_PINK, BRAND_PURPLE = "#FF4F9A", "#8E5BE8"


HAIR_LINE = "#CDBBDD"     # outline of the silky coat
STRAND = "#E2D6EE"        # strand lines that make the coat read as long & silky


def hair(d, extra=""):
    return (f'<path d="{d}" fill="url(#hairGrad)" stroke="{HAIR_LINE}" stroke-width="3" '
            f'stroke-linejoin="round"/>{extra}')


def strands(paths, w=2.5):
    return "".join(f'<path d="{d}" stroke="{STRAND}" stroke-width="{w}" fill="none" '
                   f'stroke-linecap="round"/>' for d in paths)


def hem(x0, x1, y, n, depth=16, seed=3):
    """Silky pointed hair tips from x0 to x1 around height y (slightly uneven)."""
    import random
    rnd = random.Random(seed)
    out, step = "", (x1 - x0) / n
    for i in range(n):
        xa, xb = x0 + step * i, x0 + step * (i + 1)
        m, d = (xa + xb) / 2, depth * rnd.uniform(0.7, 1.25)
        out += (f" Q {xa + step*0.2:.1f} {y + d*0.85:.1f} {m:.1f} {y + d:.1f}"
                f" Q {xb - step*0.2:.1f} {y + d*0.85:.1f} {xb:.1f} {y:.1f}")
    return out


def ear(sd, L=130):
    """Long silky ear hair hanging from the side of the head."""
    d = (f"M {sd*52} -52 C {sd*96} -56 {sd*114} -10 {sd*114} 40 "
         f"C {sd*114} {L-50} {sd*122} {L-20} {sd*118} {L}"
         + hem(sd*118, sd*66, L, 3, 18, seed=5 if sd > 0 else 9) +
         f" C {sd*70} {L-40} {sd*66} 40 {sd*64} 10 C {sd*62} -20 {sd*56} -40 {sd*52} -52 Z")
    return hair(d, strands([f"M {sd*70} -40 C {sd*100} -10 {sd*100} 60 {sd*106} {L-4}",
                            f"M {sd*80} -30 C {sd*108} 10 {sd*104} 70 {sd*112} {L-8}",
                            f"M {sd*66} 0 C {sd*84} 30 {sd*80} 80 {sd*86} {L}"], 2.2))


def head_shape():
    """Round furry head, hair parted in the middle and lying sleek."""
    d = "M 0 -96 C 56 -96 92 -56 90 -4 C 88 48 56 82 0 84 C -56 82 -88 48 -90 -4 C -92 -56 -56 -96 0 -96 Z"
    return (hair(d) +
            strands(["M 0 -94 L 0 -64",
                     "M -4 -92 C -34 -88 -60 -72 -72 -46", "M 4 -92 C 34 -88 60 -72 72 -46",
                     "M -6 -80 C -28 -76 -46 -66 -56 -52", "M 6 -80 C 28 -76 46 -66 56 -52"], 2.2) +
            # moustache / muzzle fur
            strands(["M -8 50 C -18 60 -30 62 -40 58", "M 8 50 C 18 60 30 62 40 58",
                     "M -14 44 C -26 50 -36 50 -44 46", "M 14 44 C 26 50 36 50 44 46"], 2) +
            '<path d="M -28 60 Q 0 76 28 60" stroke="#EADFF2" stroke-width="2.5" fill="none" stroke-linecap="round"/>')


def pigtail(sd):
    """Pigtail tied high on the side of the head; the hair falls down softly
    beside the cheek and ends in a little inward curl."""
    d = (f"M {sd*50} -66 C {sd*90} -66 {sd*104} -30 {sd*100} 14 "
         f"C {sd*96} 56 {sd*104} 84 {sd*88} 104 C {sd*80} 112 {sd*70} 106 {sd*74} 96 "
         f"C {sd*82} 84 {sd*76} 60 {sd*76} 30 C {sd*76} -6 {sd*68} -40 {sd*50} -66 Z")
    return hair(d, strands([f"M {sd*62} -56 C {sd*90} -36 {sd*92} 20 {sd*88} 80",
                            f"M {sd*72} -50 C {sd*96} -20 {sd*96} 40 {sd*94} 70"], 2))


def bow(sd):
    cx, cy = sd * 56, -66
    rot = sd * 18
    dots = "".join(f'<circle cx="{dx}" cy="{dy}" r="3.2" fill="#fff" opacity="0.9"/>'
                   for dx, dy in [(-24, -7), (-16, 6), (-30, 4), (24, -7), (16, 6), (30, 4)])
    return (f'<g transform="translate({cx} {cy}) rotate({rot})">'
            f'<path d="M -4 4 L -15 30 L -5 26 Z M 4 4 L 15 30 L 5 26 Z" fill="{BOW}"/>'
            f'<path d="M 0 0 C -46 -38 -50 30 0 0 Z M 0 0 C 46 -38 50 30 0 0 Z" fill="{BOW}" '
            f'stroke="#fff" stroke-width="3" stroke-linejoin="round"/>{dots}'
            f'<circle r="8.5" fill="{BOW_KNOT}" stroke="#fff" stroke-width="2.5"/></g>')


def eye(cx, cy, sd):
    lash = (f'<path d="M {cx + sd*14} {cy-15} q {sd*8} -5 {sd*13} -11" stroke="{PUPIL}" '
            f'stroke-width="3.2" fill="none" stroke-linecap="round"/>'
            f'<path d="M {cx + sd*17} {cy-8} q {sd*8} -2 {sd*14} -5" stroke="{PUPIL}" '
            f'stroke-width="3.2" fill="none" stroke-linecap="round"/>')
    return (lash + f'<ellipse cx="{cx}" cy="{cy}" rx="17" ry="20" fill="url(#eyeGrad)"/>'
            f'<ellipse cx="{cx+1}" cy="{cy+2}" rx="9.5" ry="11" fill="{PUPIL}"/>'
            f'<circle cx="{cx-5}" cy="{cy-8}" r="6.5" fill="#fff"/>'
            f'<circle cx="{cx+6}" cy="{cy+8}" r="3" fill="#fff"/>')


def face():
    return (eye(-30, 8, -1) + eye(30, 8, 1) +
            f'<ellipse cx="-50" cy="34" rx="12" ry="7.5" fill="{BLUSH}" opacity="0.6"/>'
            f'<ellipse cx="50" cy="34" rx="12" ry="7.5" fill="{BLUSH}" opacity="0.6"/>'
            f'<ellipse cx="0" cy="36" rx="13" ry="9.5" fill="{NOSE}"/>'
            f'<ellipse cx="-4" cy="32.5" rx="4.5" ry="2.6" fill="#fff" opacity="0.65"/>'
            f'<ellipse cx="0" cy="58" rx="6" ry="6" fill="{TONGUE}"/>'
            f'<path d="M 0 45 L 0 51 M -11 52 Q -5.5 59 0 51 Q 5.5 59 11 52" stroke="#3A2A2A" '
            f'stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def head(L=130):
    return (ear(-1, L) + ear(1, L) + head_shape() + pigtail(-1) + pigtail(1) +
            bow(-1) + bow(1) + face())


def puppy_body():
    """Sitting puppy in 3/4 view: chest under the head, body and haunch behind,
    long silky coat to the ground, tail plume curled over the back."""
    g = []
    g.append('<ellipse cx="85" cy="304" rx="185" ry="16" fill="#8FCB9E" opacity="0.45"/>')
    # back leg sits behind the coat; only the lower leg and paw show
    for x in (182, 214):
        g.append(f'<rect x="{x-16}" y="200" width="32" height="100" rx="15" fill="#F7F2FB" '
                 f'stroke="{HAIR_LINE}" stroke-width="3"/>')
        g.append(f'<ellipse cx="{x}" cy="300" rx="20" ry="11" fill="#F7F2FB" stroke="{HAIR_LINE}" stroke-width="3"/>')
    body = ("M -60 80 C -96 130 -98 200 -92 250" + hem(-92, 250, 256, 12, 18, seed=11) +
            " C 256 210 248 170 214 148 C 170 124 100 128 40 96 Z")
    g.append(hair(body, strands([f"M {x} {y} C {x+4} {y+50} {x-2} 200 {x+4} 262"
                                 for x, y in [(-60, 120), (-10, 110), (40, 112), (90, 128), (140, 132),
                                              (190, 142), (228, 168)]])))
    g.append(f'<path d="M 128 196 C 160 176 204 186 216 226" stroke="{STRAND}" stroke-width="3" '
             f'fill="none" stroke-linecap="round"/>')          # haunch
    # front legs + paws peeking out from under the chest hair
    for x in (-42, 6):
        g.append(f'<rect x="{x-17}" y="196" width="34" height="104" rx="16" fill="#fff" '
                 f'stroke="{HAIR_LINE}" stroke-width="3"/>')
        g.append(f'<ellipse cx="{x}" cy="300" rx="22" ry="12" fill="#fff" stroke="{HAIR_LINE}" stroke-width="3"/>')
        g.append(f'<path d="M {x-7} 293 l 0 9 M {x+7} 293 l 0 9" stroke="{HAIR_LINE}" '
                 f'stroke-width="3" stroke-linecap="round"/>')
    bib = "M -88 60 C -100 130 -96 180 -92 218" + hem(-92, 50, 220, 6, 16, seed=4) + " C 58 160 50 110 30 60 Z"
    g.append(hair(bib, strands(["M -60 110 C -62 150 -60 190 -62 222",
                                "M -20 120 C -22 160 -18 200 -22 226", "M 16 110 C 20 150 22 190 20 220"])))
    # tail: plume rising from the rump and curling over the back, silky hair falling off it
    tail = ("M 210 162 C 250 110 222 54 164 52 C 128 52 104 74 110 104 "
            "C 118 126 128 146 120 168 C 140 150 142 122 140 100 C 150 82 178 80 192 100 "
            "C 206 120 204 146 190 176 Z")
    g.append(hair(tail, strands(["M 190 150 C 214 104 186 76 150 76", "M 178 162 C 200 120 176 90 140 92"], 2)))
    return "".join(g)


def molka(x, y, s, full_body=False):
    if full_body:
        return (f'<g transform="translate({x} {y}) scale({s})">{puppy_body()}'
                f'<g transform="rotate(-7)">{head(L=118)}</g></g>')
    return f'<g transform="translate({x} {y}) scale({s})">{head()}</g>'


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
        '<linearGradient id="hairGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/>'
        '<stop offset="1" stop-color="#F2ECF8"/></linearGradient>'
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
               molka(400, 390, 2.15))


def watermark():
    return svg(150, 150, '<circle cx="75" cy="75" r="72" fill="url(#badge)" stroke="#fff" '
                         'stroke-width="5"/>' + molka(75, 72, 0.47))


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
    g.append(molka(690, 618, 0.92, full_body=True))
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
