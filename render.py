#!/usr/bin/env python3
"""Render the 18 November 2026 world-news poster to entry.png.

Editorial front-page poster, 1024x1024, drawn entirely with Pillow
primitives and DejaVu fonts. No network, no downloaded assets, no
randomness: the same script always produces the same bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (246, 241, 230)
INK = (26, 26, 26)
NAVY = (16, 38, 63)
NAVY_DARK = (10, 26, 44)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
TEAL = (18, 92, 96)
CARD = (255, 255, 255)
BORDER = (200, 192, 172)
GREY = (90, 86, 76)
SEA = (23, 68, 104)
SKY = (214, 228, 238)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(path, text, max_w, start):
    size = start
    while size > 10:
        f = font(path, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 2
    return font(path, size)


def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, f, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def star_points(cx, cy, r_out, r_in, n=10):
    import math
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_explosion(d, box):
    """Jet + explosion burst over a dark sea."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=NAVY_DARK)
    # sky band
    d.rectangle([x0, y0, x1, y0 + 108], fill=SKY)
    # sun
    d.ellipse([x0 + 300, y0 + 22, x0 + 344, y0 + 66], fill=(240, 196, 84))
    # sea
    d.rectangle([x0, y0 + 108, x1, y1], fill=SEA)
    for wy in (y0 + 150, y0 + 196, y0 + 238):
        for wx in range(x0 + 8, x1 - 30, 62):
            d.arc([wx, wy, wx + 44, wy + 14], 200, 340, fill=(255, 255, 255), width=3)
    # jet silhouette (simple delta)
    jx, jy = x0 + 96, y0 + 62
    d.polygon([(jx, jy), (jx + 66, jy + 10), (jx + 10, jy + 16),
               (jx + 30, jy + 26), (jx + 2, jy + 20)], fill=(40, 40, 48))
    # explosion burst
    cx, cy = x0 + 250, y0 + 178
    d.polygon(star_points(cx, cy, 74, 34, 10), fill=(245, 179, 1))
    d.polygon(star_points(cx, cy, 48, 22, 10), fill=(232, 116, 16))
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(255, 236, 160))
    # smoke
    for sx, sy, sr in ((cx - 62, cy - 52, 16), (cx + 58, cy - 44, 13),
                       (cx - 48, cy + 56, 14), (cx + 66, cy + 52, 17)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 118))


def draw_bridge(d, box):
    """Arch bridge with its middle span broken and falling."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(226, 232, 236))
    # water
    d.rectangle([x0, y1 - 34, x1, y1], fill=(58, 110, 150))
    for wx in range(x0 + 6, x1 - 24, 40):
        d.arc([wx, y1 - 26, wx + 30, y1 - 14], 200, 340, fill=(255, 255, 255), width=2)
    # pylons
    d.rectangle([x0 + 8, y0 + 26, x0 + 20, y1 - 34], fill=(70, 76, 84))
    d.rectangle([x1 - 20, y0 + 26, x1 - 8, y1 - 34], fill=(70, 76, 84))
    # arch
    d.arc([x0 + 6, y0 + 30, x1 - 6, y0 + 150], 180, 360, fill=(70, 76, 84), width=6)
    # deck, left and right of the gap
    mid = (x0 + x1) // 2
    d.rectangle([x0, y0 + 66, mid - 26, y0 + 76], fill=(70, 76, 84))
    d.rectangle([mid + 26, y0 + 66, x1, y0 + 76], fill=(70, 76, 84))
    # broken ends, tilted
    d.polygon([(mid - 26, y0 + 66), (mid - 8, y0 + 66), (mid - 16, y0 + 92),
               (mid - 30, y0 + 88)], fill=(70, 76, 84))
    d.polygon([(mid + 26, y0 + 66), (mid + 8, y0 + 66), (mid + 16, y0 + 94),
               (mid + 30, y0 + 90)], fill=(70, 76, 84))
    # falling debris + smoke in the gap
    for dx, dy, dr in ((mid - 6, y0 + 104, 5), (mid + 10, y0 + 116, 4),
                       (mid + 2, y0 + 128, 3)):
        d.ellipse([dx - dr, dy - dr, dx + dr, dy + dr], fill=(90, 90, 88))
    d.ellipse([mid - 24, y0 + 78, mid + 4, y0 + 104], fill=(150, 150, 148))
    d.ellipse([mid + 2, y0 + 84, mid + 26, y0 + 106], fill=(170, 170, 168))


def draw_flags(d, box):
    """Three small flags: United States, China, Russia."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(238, 238, 234))
    fw, fh = 44, 30
    gap = 8
    total = fw * 3 + gap * 2
    sx = x0 + (x1 - x0 - total) // 2
    sy = y0 + (y1 - y0 - fh) // 2
    # USA: stripes + canton
    ux = sx
    for i in range(7):
        d.rectangle([ux, sy + i * (fh // 7), ux + fw, sy + (i + 1) * (fh // 7)],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([ux, sy, ux + 20, sy + 16], fill=(60, 59, 110))
    for dx in (4, 11):
        for dy in (4, 11):
            d.ellipse([ux + dx, sy + dy, ux + dx + 2, sy + dy + 2], fill=(255, 255, 255))
    # China: red + stars
    cx = sx + fw + gap
    d.rectangle([cx, sy, cx + fw, sy + fh], fill=(222, 41, 16))
    d.polygon(star_points(cx + 11, sy + 9, 6, 2.5, 5), fill=(255, 222, 0))
    for px, py in ((cx + 24, sy + 6), (cx + 30, sy + 11), (cx + 30, sy + 17),
                   (cx + 24, sy + 21)):
        d.polygon(star_points(px, py, 3, 1.4, 5), fill=(255, 222, 0))
    # Russia: white / blue / red tricolor
    rx = sx + 2 * (fw + gap)
    d.rectangle([rx, sy, rx + fw, sy + 10], fill=(255, 255, 255))
    d.rectangle([rx, sy + 10, rx + fw, sy + 20], fill=(0, 57, 166))
    d.rectangle([rx, sy + 20, rx + fw, sy + fh], fill=(213, 0, 50))
    for fx in (ux, cx, rx):
        d.rectangle([fx, sy, fx + fw, sy + fh], outline=(120, 120, 120), width=1)


def draw_virus(d, box):
    """Spiky virus particle (Ebola)."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(250, 226, 222))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    import math
    for k in range(12):
        a = math.pi * 2 * k / 12
        x2, y2 = cx + 52 * math.cos(a), cy + 52 * math.sin(a)
        x3, y3 = cx + 62 * math.cos(a), cy + 62 * math.sin(a)
        d.line([x2, y2, x3, y3], fill=(150, 30, 30), width=4)
        d.ellipse([x3 - 5, y3 - 5, x3 + 5, y3 + 5], fill=(150, 30, 30))
    d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=(178, 34, 34))
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(205, 60, 50))
    for px, py, pr in ((cx - 18, cy - 12, 7), (cx + 14, cy + 8, 9), (cx + 4, cy - 20, 5)):
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(232, 120, 110))


def draw_thermometer(d, box):
    """Thermometer with high red mercury (measles fever)."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(226, 240, 246))
    cx = (x0 + x1) // 2
    # stem
    d.rounded_rectangle([cx - 13, y0 + 12, cx + 13, y1 - 34], radius=13,
                        fill=(255, 255, 255), outline=(90, 90, 90), width=2)
    # mercury
    d.rectangle([cx - 7, y0 + 30, cx + 7, y1 - 44], fill=(200, 40, 40))
    # bulb
    d.ellipse([cx - 24, y1 - 52, cx + 24, y1 - 4], fill=(200, 40, 40),
              outline=(90, 90, 90), width=2)
    d.ellipse([cx - 24, y1 - 52, cx + 24, y1 - 4], outline=(90, 90, 90), width=2)
    # tick marks
    for ty in (y0 + 34, y0 + 54, y0 + 74):
        d.line([cx + 13, ty, cx + 22, ty], fill=(90, 90, 90), width=2)
    # red spots (rash) around
    for px, py, pr in ((x0 + 18, y0 + 26, 6), (x1 - 20, y0 + 44, 5),
                       (x0 + 24, y1 - 30, 5), (x1 - 26, y1 - 22, 6)):
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(200, 40, 40))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.rectangle([0, 150, W, 156], fill=GOLD)
    f_kicker = font(SANS_B, 26)
    kick = "T H E   W O R L D   I N   O N E   D A Y"
    d.text(((W - f_kicker.getlength(kick)) / 2, 16), kick, font=f_kicker,
           fill=(200, 210, 225))
    f_date = fit_font(SERIF_B, "WEDNESDAY 18 NOVEMBER 2026", W - 48, 66)
    d.text(((W - f_date.getlength("WEDNESDAY 18 NOVEMBER 2026")) / 2, 52),
           "WEDNESDAY 18 NOVEMBER 2026", font=f_date, fill=(255, 255, 255))
    f_sub = font(SANS, 20)
    sub = "Five stories that defined the day  •  World news, Wednesday 18 November 2026"
    d.text(((W - f_sub.getlength(sub)) / 2, 122), sub, font=f_sub, fill=GOLD)

    # ---- Lead story: Gulf ------------------------------------------
    d.rectangle([24, 172, 1000, 452], fill=CARD, outline=BORDER, width=2)
    d.rectangle([24, 172, 30, 452], fill=RED)
    draw_explosion(d, (30, 172, 420, 452))
    tx = 448
    f_tag = font(SANS_B, 20)
    d.text((tx, 190), "MIDDLE EAST  •  CONFLICT", font=f_tag, fill=RED)
    f_h1 = font(SANS_B, 36)
    lead_head = "U.S. hits Iran's Qeshm Island; Iran drones strike Bahrain and Kuwait"
    lines = wrap(d, lead_head, f_h1, 1000 - tx - 24)
    y = text_block(d, tx, 222, lines, f_h1, INK, 43)
    f_body = font(SANS, 22)
    lead_body = ("U.S. jets hit a Revolutionary Guard missile site on Qeshm "
                 "Island. Tehran answered with drone attacks in Bahrain "
                 "and Kuwait.")
    lines = wrap(d, lead_body, f_body, 1000 - tx - 24)
    text_block(d, tx, y + 8, lines, f_body, (60, 58, 52), 28)

    # ---- 2x2 grid ---------------------------------------------------
    cards = [
        ("EUROPE  •  WAR", "Ukraine hits Kerch Bridge again",
         "Part of the road span to Crimea collapses into the strait.",
         draw_bridge),
        ("ASIA  •  DIPLOMACY", "APEC opens; Quad meets in Manila",
         "Trump, Xi and Putin meet tomorrow in Shenzhen, at the first "
         "trilateral summit.",
         draw_flags),
        ("AFRICA  •  HEALTH", "Ebola in DR Congo more than doubles",
         "11,000+ cases, 5,400 deaths, the UN says. Seven in ten "
         "infected under-fives die.",
         draw_virus),
        ("AMERICAS  •  HEALTH", "U.S. loses measles-free status",
         "More than 5,400 cases and 10 deaths end 26 years of measles "
         "elimination status.",
         draw_thermometer),
    ]
    gx = (24, 524)
    gy = (470, 676)
    cw, ch = 476, 190
    f_ctag = font(SANS_B, 18)
    f_chead = font(SANS_B, 27)
    f_cbody = font(SANS, 20)
    for i, (tag, head, body, icon) in enumerate(cards):
        x0 = gx[i % 2]
        y0 = gy[i // 2]
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD, outline=BORDER, width=2)
        icon(d, (x0 + 2, y0 + 2, x0 + 132, y0 + ch - 2))
        d.line([x0 + 134, y0 + 10, x0 + 134, y0 + ch - 10], fill=BORDER, width=2)
        tx2 = x0 + 150
        d.text((tx2, y0 + 12), tag, font=f_ctag, fill=TEAL)
        lines = wrap(d, head, f_chead, x0 + cw - tx2 - 14)
        y = text_block(d, tx2, y0 + 38, lines, f_chead, INK, 32)
        lines = wrap(d, body, f_cbody, x0 + cw - tx2 - 14)
        text_block(d, tx2, y + 6, lines, f_cbody, (60, 58, 52), 26)

    # ---- Also today --------------------------------------------------
    d.rectangle([24, 884, 1000, 950], fill=NAVY)
    f_also = font(SANS_B, 20)
    d.text((44, 900), "ALSO TODAY", font=f_also, fill=GOLD)
    f_a = font(SANS, 20)
    also = ("Cyclone Xavier slams the Cook Islands  •  Russian military plane "
            "crash kills 19 in Siberia  •  Peltola wins Alaska Senate seat; "
            "Democrats reach 56")
    lines = wrap(d, also, f_a, 1000 - 44 - 200)
    text_block(d, 220, 888, lines, f_a, (255, 255, 255), 26)

    # ---- Footer -------------------------------------------------------
    f_foot = font(SANS, 17)
    foot = "All stories happened or were first reported on Wednesday 18 November 2026"
    d.text(((W - f_foot.getlength(foot)) / 2, 966), foot, font=f_foot, fill=GREY)

    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
