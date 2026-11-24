#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261124.

Draws a single 1024x1024 newspaper-style image summing up Tuesday
24 November 2026 world news. Pillow only; run: python3 render.py.
Writes entry.png next to this file. Deterministic: same bytes every run.

Layout budget (1024 tall): masthead 14-116, ticker 122-152,
heroes 160-436, row2 446-640, row3 650-806, bottom 816-1010.
Every text block is wrapped to its panel width and kept short enough
that it cannot reach the tag or the next panel.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (248, 244, 232)
NAVY = (22, 41, 77)
GOLD = (201, 162, 39)
RED = (185, 28, 28)
INK = (26, 26, 26)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
GREEN = (21, 128, 61)
AMBER = (180, 120, 10)
TEAL = (27, 107, 122)
SKY = (127, 179, 213)
ORANGE = (249, 115, 22)
YELLOW = (250, 204, 21)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_fonts = {}


def font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, x, y, w, h, fill=WHITE, outline=NAVY, width=2):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=fill,
                           outline=outline, width=width)


def tag(draw, x, y, kind):
    label = kind.upper()
    fnt = font(BOLD, 12)
    w = int(draw.textlength(label, font=fnt)) + 12
    color = GREEN if kind.upper() == "CONFIRMED" else AMBER
    draw.rounded_rectangle([x, y, x + w, y + 18], radius=9, fill=color)
    draw.text((x + 6, y + 2), label, font=fnt, fill=WHITE)
    return w


# ---------------------------------------------------------------- heroes
def draw_hormuz(draw, x, y, w, h):
    """Strait of Hormuz: water band between land strips, 3 burning tankers, mines."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 90, 110))
    draw.rectangle([x, y, x + w, y + 18], fill=(217, 201, 163))
    draw.rectangle([x, y + h - 18, x + w, y + h], fill=(217, 201, 163))
    draw.text((x + 8, y + 2), "IRAN", font=font(BOLD, 12), fill=(90, 70, 40))
    draw.text((x + w - 52, y + h - 16), "OMAN", font=font(BOLD, 12), fill=(90, 70, 40))
    draw.text((x + 8, y + 24), "STRAIT OF HORMUZ", font=font(BOLD, 14), fill=WHITE)
    for mx, my in [(x + 250, y + 44), (x + 60, y + 70)]:
        for dx, dy in [(0, -7), (0, 7), (-7, 0), (7, 0), (-5, -5), (5, -5), (-5, 5), (5, 5)]:
            draw.line([mx, my, mx + dx, my + dy], fill=(20, 20, 20), width=2)
        draw.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=(20, 20, 20))
    for tx in (x + 30, x + 130, x + 228):
        fx, fy = tx + 22, y + 44
        draw.polygon([(fx - 11, fy + 16), (fx - 4, fy - 2), (fx + 2, fy + 7),
                      (fx + 9, fy - 9), (fx + 13, fy + 16)], fill=ORANGE)
        draw.polygon([(fx - 5, fy + 16), (fx - 1, fy + 4), (fx + 4, fy + 16)],
                     fill=YELLOW)
        draw.rounded_rectangle([tx, y + 60, tx + 46, y + 78], radius=4, fill=(30, 30, 30))
        draw.rectangle([tx + 30, y + 50, tx + 42, y + 60], fill=(30, 30, 30))
        draw.rectangle([tx + 4, y + 64, tx + 42, y + 68], fill=(200, 60, 40))


def draw_huang(draw, x, y, w, h):
    """Nvidia rebound: dark panel, steep green rising chart, chip icon."""
    draw.rectangle([x, y, x + w, y + h], fill=(10, 38, 22))
    for gy in range(y + 22, y + h - 6, 22):
        draw.line([x + 8, gy, x + w - 8, gy], fill=(30, 70, 45), width=1)
    cx, cy = x + 14, y + 10
    draw.rectangle([cx, cy, cx + 32, cy + 32], outline=(34, 197, 94), width=3)
    draw.rectangle([cx + 10, cy + 10, cx + 22, cy + 22], fill=(34, 197, 94))
    for px in (cx + 4, cx + 14, cx + 24):
        draw.line([px, cy - 5, px, cy], fill=(34, 197, 94), width=2)
        draw.line([px, cy + 32, px, cy + 37], fill=(34, 197, 94), width=2)
    draw.text((x + 58, y + 14), "NASDAQ  +REBOUND", font=font(BOLD, 16), fill=(134, 239, 172))
    pts = [(x + 20, y + h - 16), (x + 80, y + h - 36), (x + 130, y + h - 30),
           (x + 190, y + h - 58), (x + 250, y + h - 74), (x + 296, y + 20)]
    draw.line(pts, fill=(34, 197, 94), width=6, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 18, ey + 2), (ex - 4, ey + 16)], fill=(34, 197, 94))


def draw_awacs(draw, x, y, w, h):
    """AWACS over Poland: sky, simplified Poland polygon, bold plane silhouette."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    for cx, cy, cw in [(x + 20, y + 10, 44), (x + 230, y + 16, 52)]:
        draw.ellipse([cx, cy, cx + cw, cy + 16], fill=(255, 255, 255))
    poly = [(x + 60, y + 66), (x + 110, y + 56), (x + 180, y + 60),
            (x + 240, y + 54), (x + 280, y + 70), (x + 262, y + 92),
            (x + 200, y + 98), (x + 130, y + 94), (x + 80, y + 88)]
    draw.polygon(poly, fill=(122, 154, 91), outline=(70, 100, 55))
    draw.text((x + 128, y + 70), "POLAND", font=font(BOLD, 15), fill=(40, 60, 35))
    # AWACS plane: dark-navy silhouette so it reads against the sky
    px, py = x + 56, y + 26
    draw.ellipse([px + 66, py - 12, px + 132, py + 4], fill=NAVY)  # radar dome
    draw.line([px + 99, py + 2, px + 99, py + 8], fill=NAVY, width=5)
    draw.rounded_rectangle([px, py + 6, px + 200, py + 22], radius=8, fill=NAVY)
    draw.polygon([(px + 188, py + 6), (px + 214, py - 12), (px + 214, py + 6)], fill=NAVY)
    draw.polygon([(px + 88, py + 22), (px + 126, py + 36), (px + 148, py + 22)], fill=NAVY)


# ------------------------------------------------------------- medium icons
def icon_merkury(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(70, 110, 140))
    draw.polygon([(x + 10, y + 30), (x + 48, y + 24), (x + 45, y + 36),
                  (x + 13, y + 40)], fill=(30, 30, 30))
    draw.rectangle([x + 32, y + 14, x + 39, y + 26], fill=(30, 30, 30))
    for wy in (y + 46, y + 52):
        draw.arc([x + 6, wy - 5, x + 26, wy + 5], 0, 180, fill=WHITE, width=3)
        draw.arc([x + 30, wy - 5, x + 50, wy + 5], 0, 180, fill=WHITE, width=3)


def icon_korea(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=RED)
    draw.text((x + s // 2 - 9, y + 6), "!", font=font(BOLD, 46), fill=WHITE)


def icon_fire(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(194, 65, 12))
    cx = x + s // 2
    draw.polygon([(cx - 17, y + 46), (cx - 9, y + 20), (cx - 2, y + 30),
                  (cx + 7, y + 11), (cx + 17, y + 46)], fill=ORANGE)
    draw.polygon([(cx - 8, y + 46), (cx - 2, y + 29), (cx + 8, y + 46)], fill=YELLOW)


def icon_cop(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=TEAL)
    draw.rounded_rectangle([x + 24, y + 8, x + 38, y + 42], radius=7,
                           outline=WHITE, width=3)
    draw.rectangle([x + 28, y + 26, x + 34, y + 40], fill=RED)
    draw.ellipse([x + 20, y + 38, x + 42, y + 54], fill=RED, outline=WHITE, width=2)


# -------------------------------------------------------------- small icons
def sicon(draw, x, y, s, kind):
    colors = {"$": RED, "W": (180, 140, 20), "F": (194, 65, 12), "P": (109, 40, 217)}
    draw.rectangle([x, y, x + s, y + s], fill=colors[kind])
    fnt = font(BOLD, 28)
    tw = draw.textlength(kind, font=fnt)
    draw.text((x + (s - tw) / 2, y + 4), kind, font=fnt, fill=WHITE)


# ------------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([16, 14, W - 16, 116], fill=NAVY)
    d.text((W // 2, 24), "THE WORLD TODAY", font=font(BOLD, 52),
           fill=WHITE, anchor="ma")
    d.text((W // 2, 80), "TUESDAY,  24  NOVEMBER  2026", font=font(BOLD, 28),
           fill=GOLD, anchor="ma")

    # ---- ticker (short, fits)
    d.rectangle([16, 122, W - 16, 152], fill=RED)
    tick = "HORMUZ: 3 TANKERS HIT  •  HUANG BACK AT NVIDIA  •  NATO AWACS TO POLAND"
    d.text((W // 2, 129), tick, font=font(BOLD, 17), fill=WHITE, anchor="ma")

    # ---- heroes (160-436)
    heroes = [
        ("HORMUZ TANKERS HIT",
         "Three oil tankers hit sea mines and burn in the Strait of Hormuz, "
         "the Revolutionary Guard says.",
         "CONFIRMED", draw_hormuz),
        ("HUANG IS BACK",
         "Jensen Huang is reinstated as Nvidia CEO after Trump brokers a "
         "deal with the board; Wall Street rebounds.",
         "CONFIRMED", draw_huang),
        ("NATO AWACS TO POLAND",
         "NATO sends early-warning aircraft to Poland after three Russian "
         "missiles landed on its soil.",
         "CONFIRMED", draw_awacs),
    ]
    hx, hy, hw, hh = 16, 160, 320, 276
    for i, (head, summ, kind, painter) in enumerate(heroes):
        x = hx + i * (hw + 16)
        panel(d, x, hy, hw, hh)
        painter(d, x + 2, hy + 2, hw - 4, 100)
        yy = hy + 110
        for line in wrap(d, head, font(BOLD, 28), hw - 24)[:2]:
            d.text((x + 12, yy), line, font=font(BOLD, 28), fill=NAVY)
            yy += 32
        text_block(d, x + 12, yy + 4,
                   wrap(d, summ, font(REG, 17), hw - 24)[:3],
                   font(REG, 17), INK, leading=20)
        tag(d, x + 12, hy + hh - 26, kind)

    # ---- row 2: medium panels (446-640), icon-top layout
    mids = [
        ("MERKURY SUNK",
         "Ukraine sinks the Russian corvette Merkury in Benghazi, Libya, "
         "with naval drones.",
         "CONFIRMED", icon_merkury),
        ("N. KOREA vs SWISS",
         "Kim Yo Jong threatens to shut the Swiss mission after Bern "
         "imposes sanctions.",
         "REPORTED", icon_korea),
        ("INDONESIA FIRE",
         "A candy factory fire in Banten kills at least 24; rescuers "
         "search for the missing.",
         "CONFIRMED", icon_fire),
        ("COP31 AFTERMATH",
         "Climate talks collapsed over fossil fuels; Australia faces "
         "backlash.",
         "CONFIRMED", icon_cop),
    ]
    mx, my, mw, mh = 16, 446, 236, 194
    for i, (head, summ, kind, painter) in enumerate(mids):
        x = mx + i * (mw + 16)
        panel(d, x, my, mw, mh)
        painter(d, x + 10, my + 10, 56)
        tx = x + 76
        yy = my + 10
        for line in wrap(d, head, font(BOLD, 20), mw - 86)[:2]:
            d.text((tx, yy), line, font=font(BOLD, 20), fill=NAVY)
            yy += 23
        text_block(d, x + 10, my + 76,
                   wrap(d, summ, font(REG, 14), mw - 20)[:3],
                   font(REG, 14), INK, leading=17)
        tag(d, x + 10, my + mh - 26, kind)

    # ---- row 3: small panels (650-806), icon-top layout
    smalls = [
        ("US SANCTIONS IRAN",
         "Treasury sanctions two dozen Iranian exchange houses and front "
         "firms.",
         "CONFIRMED", "$"),
        ("GRAIN DEAL DEAD",
         "Russia tells the UN Security Council it will agree to no new "
         "grain deal.",
         "CONFIRMED", "W"),
        ("SPARTA II ABLAZE",
         "A Russian cargo ship catches fire in the Gulf of Finland after "
         "a drone attack.",
         "REPORTED", "F"),
        ("LISBON PROTESTS",
         "Thousands march in Lisbon against the rising cost of living.",
         "CONFIRMED", "P"),
    ]
    sx, sy, sw, sh = 16, 650, 236, 156
    for i, (head, summ, kind, glyph) in enumerate(smalls):
        x = sx + i * (sw + 16)
        panel(d, x, sy, sw, sh)
        sicon(d, x + 10, sy + 10, 40, glyph)
        tx = x + 60
        yy = sy + 10
        for line in wrap(d, head, font(BOLD, 18), sw - 70)[:2]:
            d.text((tx, yy), line, font=font(BOLD, 18), fill=NAVY)
            yy += 21
        text_block(d, x + 10, sy + 60,
                   wrap(d, summ, font(REG, 13), sw - 20)[:3],
                   font(REG, 13), INK, leading=16)
        tag(d, x + 10, sy + sh - 24, kind)

    # ---- bottom (816-1010)
    by = 816
    d.text((16, by), "ALSO ON", font=font(BOLD, 18), fill=NAVY)
    d.line([16, by + 26, 656, by + 26], fill=NAVY, width=2)
    also = [
        "Alcaraz beats Zverev for his first ATP Finals title.",
        "FIFA confirms the 2031 Women's World Cup in the US, Mexico, Costa Rica and Jamaica; 2035 in the UK.",
        "Verstappen wins the Las Vegas Grand Prix.",
        "India v New Zealand first Test ends in a draw; Pant hits 128.",
        "Modi and Nepal PM Balendra Shah flag off the Saryu-Kamala Express.",
        "Israeli strikes kill three in Gaza, including an UNRWA worker.",
        "Iran flogs a singer and her team — 74 lashes each.",
        "Gukesh begins his World Chess title defence against Sindarov in Geneva.",
    ]
    col_w = 316
    for i, item in enumerate(also):
        col = i // 4
        row = i % 4
        ax = 16 + col * (col_w + 8)
        ay = by + 34 + row * 34
        d.text((ax, ay), "▪", font=font(BOLD, 13), fill=RED)
        text_block(d, ax + 15, ay,
                   wrap(d, item, font(REG, 13), col_w - 15)[:2],
                   font(REG, 13), INK, leading=15)

    # DATE CHECK box
    bx, bw = 672, 336
    panel(d, bx, by, bw, 108, fill=WHITE, outline=NAVY, width=2)
    d.text((bx + 12, by + 8), "DATE CHECK — LEFT OUT ON PURPOSE",
           font=font(BOLD, 13), fill=NAVY)
    dc = [
        "Shenzhen summit (Trump, Putin, Xi) — 23 Nov.",
        "Riemann Hypothesis proof claim — 23 Nov.",
        "COP31 collapse itself — Sunday.",
        "Dymer death toll — 23 Nov.",
    ]
    text_block(d, bx + 12, by + 30, dc, font(REG, 13), INK, leading=17)

    # legend
    ly = by + 118
    for line in wrap(d, "CONFIRMED = 2+ major outlets  •  REPORTED = one major outlet  •  CLAIM = one side's claim.",
                     font(BOLD, 12), bw):
        d.text((bx + 12, ly), line, font=font(BOLD, 12), fill=GREY)
        ly += 15
    d.text((bx + 12, ly + 2), "No hype, no speculation as fact.",
           font=font(BOLD, 12), fill=GREY)

    # footer
    d.line([16, 988, W - 16, 988], fill=GREY, width=1)
    d.text((W // 2, 994),
           "Sources: Reuters, AP, AFP, Al Jazeera, KCNA, IRGC. 24 stories · 5 continents · Tuesday 24 November 2026.",
           font=font(REG, 12), fill=GREY, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
