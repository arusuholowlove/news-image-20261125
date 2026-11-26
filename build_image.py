"""Draw the front page for 25 November 2026 and save it as entry.png.

A newspaper front page, 1024x1024: masthead, one lead story (the Strait
of Hormuz tanker mines) and six smaller stories from six regions, plus a
ticker of three more items. Every picture is drawn from flat shapes so
the file renders the same on any machine; nothing is fetched, nothing is
random, and the output is byte-identical on every run.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (179, 38, 30)
SEA = (46, 95, 122)
SEA_DARK = (28, 66, 88)
SKY = (191, 217, 232)
SAND = (226, 205, 160)
GREY = (120, 120, 116)
FLAME = (232, 116, 30)
FLAME_Y = (244, 190, 60)
SMOKE = (90, 90, 88)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped text, return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def flame(draw, cx, base, w, h):
    """A small stylised flame: outer orange, inner yellow."""
    draw.polygon(
        [(cx - w, base), (cx - w * 0.55, base - h * 0.62),
         (cx - w * 0.15, base - h * 0.42), (cx, base - h),
         (cx + w * 0.2, base - h * 0.45), (cx + w * 0.6, base - h * 0.6),
         (cx + w, base)],
        fill=FLAME,
    )
    draw.polygon(
        [(cx - w * 0.45, base), (cx - w * 0.2, base - h * 0.5),
         (cx, base - h * 0.72), (cx + w * 0.25, base - h * 0.42),
         (cx + w * 0.45, base)],
        fill=FLAME_Y,
    )


def smoke(draw, cx, top, w):
    """Three grey puffs rising above a fire."""
    for i, (dx, dy, r) in enumerate([(-w, 6, 15), (0, -6, 19), (w, 4, 14)]):
        draw.ellipse([cx + dx - r, top + dy - r, cx + dx + r, top + dy + r],
                     fill=SMOKE if i != 1 else (110, 110, 108))


def tanker(draw, x, y, w, h, hull=(40, 44, 48)):
    """A side-on oil tanker: dark hull, deck, bridge tower, funnel."""
    draw.rectangle([x, y, x + w, y + h], fill=hull)
    draw.rectangle([x, y - 8, x + w, y], fill=(70, 74, 78))
    draw.rectangle([x + w - 52, y - 34, x + w - 14, y - 8], fill=(210, 210, 205))
    for fy in (y - 30, y - 22, y - 14):
        draw.rectangle([x + w - 48, fy, x + w - 18, fy + 4], fill=INK)
    draw.rectangle([x + 12, y - 26, x + 30, y - 8], fill=RED)
    draw.rectangle([x + 8, y + h - 10, x + w - 8, y + h], fill=(24, 28, 32))


def mine(draw, cx, cy, r):
    """A spiked naval mine."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 52, 50))
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),
                   (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)]:
        x2, y2 = cx + dx * (r + 9), cy + dy * (r + 9)
        draw.line([(cx + dx * r * 0.7, cy + dy * r * 0.7), (x2, y2)],
                  fill=(52, 52, 50), width=3)


def scene_hormuz(draw, x, y, w, h):
    """Two tankers on a strait, one ablaze, mines in the water."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h * 0.55, x + w, y + h], fill=SEA)
    draw.rectangle([x, y + h * 0.55, x + w, y + h * 0.55 + 4], fill=SEA_DARK)
    for wx in range(x + 10, x + w - 10, 46):
        draw.line([(wx, y + h * 0.72), (wx + 22, y + h * 0.72)],
                  fill=(140, 190, 210), width=2)
        draw.line([(wx + 8, y + h * 0.86), (wx + 30, y + h * 0.86)],
                  fill=(140, 190, 210), width=2)
    tanker(draw, x + 24, y + h * 0.42, 150, 30)
    tanker(draw, x + w - 190, y + h * 0.46, 160, 32)
    flame(draw, x + 95, y + h * 0.42, 26, 62)
    flame(draw, x + w - 110, y + h * 0.46, 30, 74)
    smoke(draw, x + 95, y + h * 0.42 - 62, 16)
    smoke(draw, x + w - 110, y + h * 0.46 - 74, 18)
    mine(draw, x + 215, y + h * 0.8, 11)
    mine(draw, x + w - 60, y + h * 0.88, 9)


def scene_refinery(draw, x, y, w, h):
    """Oil refinery towers with a fire at the base."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 214, 176))
    for tx, tw, th in [(x + 18, 34, 78), (x + 62, 26, 64),
                       (x + 100, 40, 88), (x + 152, 28, 70)]:
        draw.rectangle([tx, y + h - th, tx + tw, y + h], fill=(96, 96, 92))
        draw.rectangle([tx - 3, y + h - th - 8, tx + tw + 3, y + h - th],
                       fill=(70, 70, 66))
    draw.rectangle([x + 200, y + h - 46, x + w - 16, y + h], fill=(70, 70, 66))
    draw.line([(x + 200, y + h - 46), (x + 236, y + 22)], fill=(70, 70, 66),
              width=5)
    flame(draw, x + 130, y + h - 4, 30, 66)
    smoke(draw, x + 130, y + h - 70, 15)


def scene_rocket(draw, x, y, w, h):
    """A rocket climbing past stars toward a small station arc."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 34, 58))
    for sx, sy in [(x + 20, y + 18), (x + 70, y + 40), (x + 150, y + 14),
                   (x + 220, y + 46), (x + 270, y + 20), (x + 110, y + 70),
                   (x + 250, y + 76)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(240, 240, 230))
    bx, by = x + w // 2, y + h - 34
    draw.polygon([(bx - 16, by), (bx - 16, by - 62), (bx, by - 84),
                  (bx + 16, by - 62), (bx + 16, by)], fill=(225, 225, 220))
    draw.polygon([(bx - 16, by - 62), (bx, by - 84), (bx, by - 62)],
                 fill=RED)
    draw.rectangle([bx - 26, by - 30, bx - 16, by - 6], fill=RED)
    draw.rectangle([bx + 16, by - 30, bx + 26, by - 6], fill=RED)
    flame(draw, bx, by + 2, 12, 30)
    draw.ellipse([x + w - 52, y + 16, x + w - 16, y + 52], outline=(200, 200, 190),
                 width=3)
    draw.rectangle([x + w - 62, y + 30, x + w - 52, y + 38], fill=(200, 200, 190))
    draw.rectangle([x + w - 16, y + 30, x + w - 6, y + 38], fill=(200, 200, 190))


def scene_court(draw, x, y, w, h):
    """Courthouse columns, a gavel and a chip."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 206, 188))
    draw.polygon([(x + 20, y + 26), (x + w // 2, y + 6),
                  (x + w - 20, y + 26)], fill=(120, 112, 96))
    for cx in (x + 44, x + w // 2 - 10, x + w - 64):
        draw.rectangle([cx, y + 30, cx + 20, y + h - 14], fill=(240, 236, 224))
    draw.rectangle([x + 16, y + h - 14, x + w - 16, y + h - 6],
                   fill=(120, 112, 96))
    draw.rectangle([x + w - 96, y + h - 62, x + w - 36, y + h - 22],
                   fill=(40, 44, 48))
    for gy in range(y + h - 56, y + h - 26, 8):
        draw.line([(x + w - 90, gy), (x + w - 42, gy)], fill=(150, 160, 170),
                  width=2)
    draw.rectangle([x + 34, y + h - 40, x + 84, y + h - 30], fill=(120, 84, 48))
    draw.rectangle([x + 52, y + h - 62, x + 66, y + h - 40], fill=(120, 84, 48))


def scene_island(draw, x, y, w, h):
    """A Pacific island, two flagpoles and a rising sun."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.ellipse([x + w - 66, y + 12, x + w - 22, y + 56], fill=FLAME_Y)
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    draw.polygon([(x + 40, y + h * 0.62), (x + 130, y + h * 0.34),
                  (x + 230, y + h * 0.62)], fill=(96, 140, 84))
    draw.polygon([(x + 150, y + h * 0.62), (x + 220, y + h * 0.44),
                  (x + w - 30, y + h * 0.62)], fill=(74, 116, 66))
    for fx, col in [(x + 60, (0, 40, 90)), (x + 250, (0, 60, 40))]:
        draw.line([(fx, y + 18), (fx, y + h * 0.62)], fill=INK, width=3)
        draw.polygon([(fx, y + 18), (fx + 34, y + 28), (fx, y + 38)],
                     fill=col)
    draw.rectangle([x + 96, y + h * 0.3, x + 102, y + h * 0.44], fill=(90, 60, 30))
    draw.ellipse([x + 84, y + h * 0.22, x + 118, y + h * 0.32], fill=(46, 110, 58))


def scene_city(draw, x, y, w, h):
    """A city skyline at dusk with one blast and a candle below."""
    draw.rectangle([x, y, x + w, y + h], fill=(52, 48, 66))
    for bx, bw, bh in [(x + 12, 44, 66), (x + 64, 36, 88), (x + 108, 52, 58),
                       (x + 170, 40, 96), (x + 218, 46, 72), (x + 272, 34, 60)]:
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(30, 28, 40))
        for wy in range(y + h - bh + 8, y + h - 8, 14):
            for wx in range(bx + 6, bx + bw - 6, 14):
                draw.rectangle([wx, wy, wx + 5, wy + 6], fill=FLAME_Y)
    cx, cy = x + 150, y + 34
    for dx, dy in [(0, -26), (0, 26), (-26, 0), (26, 0),
                   (-18, -18), (18, -18), (-18, 18), (18, 18)]:
        draw.line([(cx, cy), (cx + dx, cy + dy)], fill=FLAME, width=5)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=FLAME_Y)


def scene_drone(draw, x, y, w, h):
    """A quadcopter drone over flat-roofed houses in dry country."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 222, 190))
    draw.ellipse([x + w - 70, y + 10, x + w - 26, y + 54], fill=FLAME_Y)
    for hx, hw in [(x + 16, 70), (x + 96, 84), (x + 190, 76), (x + 268, 56)]:
        draw.rectangle([hx, y + h - 52, hx + hw, y + h - 10], fill=(172, 138, 96))
        draw.rectangle([hx - 4, y + h - 58, hx + hw + 4, y + h - 52],
                       fill=(140, 108, 74))
        draw.rectangle([hx + hw // 2 - 8, y + h - 40, hx + hw // 2 + 8,
                        y + h - 10], fill=(90, 66, 44))
    cx, cy = x + w // 2, y + 30
    draw.rectangle([cx - 22, cy - 8, cx + 22, cy + 8], fill=(52, 52, 50))
    for sx in (-34, 34):
        draw.ellipse([cx + sx - 16, cy - 18, cx + sx + 16, cy + 2],
                     outline=(52, 52, 50), width=2)
    draw.line([(cx - 22, cy), (cx - 50, cy - 8)], fill=(52, 52, 50), width=2)
    draw.line([(cx + 22, cy), (cx + 50, cy - 8)], fill=(52, 52, 50), width=2)


SCENES = {
    "hormuz": scene_hormuz,
    "refinery": scene_refinery,
    "rocket": scene_rocket,
    "court": scene_court,
    "island": scene_island,
    "city": scene_city,
    "drone": scene_drone,
}

STORIES = [
    ("MIDDLE EAST", "refinery", "Houthis hit Saudi refinery",
     "Ras Tanura ablaze after a Houthi strike; a Riyadh tower attack "
     "hurt 11."),
    ("SPACE", "rocket", "Pakistan's first astronaut",
     "Shenzhou-24 lifts off with Muhammad Zeeshan Ali, the first "
     "Pakistani bound for Tiangong."),
    ("TECH", "court", "Huawei convicted",
     "A US jury finds Huawei guilty of stealing trade secrets and bank "
     "fraud; racketeering fails."),
    ("PACIFIC", "island", "No foreign bases",
     "Solomon Islands and Australia sign a treaty barring any foreign "
     "military base on the islands."),
    ("EUROPE", "city", "Odesa hit; toll nears 500,000",
     "A Russian strike kills two in Odesa; leaked figures count "
     "490,334 Russian soldiers dead."),
    ("AFRICA", "drone", "19 killed in Sudan",
     "Rapid Support Forces drone strikes hit two cities, killing 19 "
     "civilians and wounding 20."),
]


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=1)

    # Masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 26), title, font=tf,
           fill=INK)
    rule(d, 30, 104, W - 30, 2)
    date = "WEDNESDAY  ·  25 NOVEMBER 2026"
    df = font(SANS_B, 27)
    d.text(((W - d.textlength(date, font=df)) / 2, 112), date, font=df,
           fill=RED)
    sub = "The world's news of one day, in one picture  —  seven stories"
    sf = font(SERIF, 21)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 148), sub, font=sf,
           fill=INK)
    rule(d, 30, 180, W - 30, 2)

    # Lead story: Hormuz
    kick = font(SANS_B, 18)
    d.text((30, 194), "LEAD  ·  THE IRAN WAR", font=kick, fill=RED)
    head = font(SERIF_B, 46)
    y = para(d, 30, 220, "Mines in the Strait", head, 430, 52)
    deck = font(SERIF, 21)
    y = para(d, 30, y + 6,
             "Two oil tankers struck, ablaze in Hormuz, as the war widens "
             "to shipping and Saudi oil.", deck, 430, 27)
    SCENES["hormuz"](d, 500, 194, 494, 208)
    d.rectangle([500, 194, 994, 402], outline=INK, width=2)
    rule(d, 30, 420, W - 30, 2)

    # Six stories, three across and two down
    cell_w, cell_h = 308, 250
    gap_x, gap_y = 14, 12
    x0, y0 = 30, 436
    for i, (kicker, scene, headline, summary) in enumerate(STORIES):
        cx = x0 + (i % 3) * (cell_w + gap_x)
        cy = y0 + (i // 3) * (cell_h + gap_y)
        d.text((cx, cy), kicker, font=kick, fill=RED)
        SCENES[scene](d, cx, cy + 26, cell_w, 108)
        d.rectangle([cx, cy + 26, cx + cell_w, cy + 134], outline=INK,
                    width=1)
        hf = font(SERIF_B, 23)
        y = para(d, cx, cy + 142, headline, hf, cell_w, 26)
        bf = font(SANS, 16)
        para(d, cx, y + 2, summary, bf, cell_w, 20)
        if i % 3 != 2:
            d.line([(cx + cell_w + 7, cy), (cx + cell_w + 7, cy + cell_h)],
                   fill=GREY, width=1)

    # Footer ticker (shortened until it fits one line)
    rule(d, 30, 962, W - 30, 2)
    ticker = ("ALSO TODAY · Tariffs up to 20% on China, EU + 12 · "
              "Villavicencio bomb injures 23 · CIA breached")
    tick = font(SANS_B, 16)
    if d.textlength(ticker, font=tick) > W - 60:
        tick = font(SANS_B, 15)
    d.text((30, 972), ticker, font=tick, fill=INK)

    img.save(path, "PNG", optimize=True)


if __name__ == "__main__":
    build("entry.png")
