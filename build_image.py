"""Build the news-image entry: a 1024x1024 newspaper front page
summing up Friday 20 November 2026, drawn with Pillow only.
Run: python3 build_image.py  -> writes entry.png (<= 1 MiB).
All facts were checked against Reuters / CNN / Al Jazeera / ISW
search results on 21 Nov 2026; 19 Nov events are labelled as such.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

W = H = 1024
BG = (247, 243, 234)
INK = (20, 20, 20)
RED = (178, 34, 34)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def panel(draw, box, fill, border=INK):
    draw.rounded_rectangle(box, radius=14, fill=fill, outline=border, width=3)


def headline(draw, x, y, w, text, size, color=INK, fnt=SANSB):
    f = font(fnt, size)
    lines = wrap(draw, text, f, w)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=color)
        y += size + 6
    return y


def body(draw, x, y, w, text, size=21, color=INK):
    f = font(SANS, size)
    for ln in wrap(draw, text, f, w):
        draw.text((x, y), ln, font=f, fill=color)
        y += size + 7
    return y


def kicker(draw, x, y, text, color):
    f = font(SANSB, 19)
    draw.text((x, y), text, font=f, fill=color)
    return y + 28


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    m = 36
    # Masthead
    d.text((m, 28), "THE WORLD IN ONE DAY", font=font(SERIF, 52), fill=INK)
    d.text((m, 92), "FRIDAY  20  NOVEMBER  2026", font=font(SANSB, 34), fill=RED)
    d.line([(m, 140), (W - m, 140)], fill=RED, width=5)
    d.text((m, 150), "Six stories that defined the day  •  All events 20 Nov 2026 unless noted",
           font=font(SANS, 20), fill=(90, 90, 90))

    # 1. GTA VI lead panel, neon Vice City gradient
    x0, y0, x1, y1 = m, 182, W - m, 452
    for i in range(y1 - y0):
        t = i / (y1 - y0)
        r = int(90 + 140 * t)
        g = int(30 + 60 * (1 - t))
        b = int(140 + 40 * t)
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=(r, g, b))
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, outline=INK, width=3)
    d.ellipse([x1 - 190, y0 + 30, x1 - 60, y0 + 160], fill=(255, 190, 60))
    d.text((x0 + 24, y0 + 18), "ENTERTAINMENT  •  BIGGEST LAUNCH EVER",
           font=font(SANSB, 20), fill=(255, 220, 120))
    d.text((x0 + 24, y0 + 52), "$3.79BN IN A DAY", font=font(SANSB, 64), fill=(255, 255, 255))
    y = headline(d, x0 + 24, y0 + 128, x1 - x0 - 48,
                 "GTA VI SMASHES THE LAUNCH RECORD", 34, (255, 255, 255))
    body(d, x0 + 24, y + 4, x1 - x0 - 48,
         "Rockstar: 32.5m copies sold before release, first new GTA in 13 years.",
         22, (240, 240, 255))

    # Row 2: Kyiv | Nasdaq
    ry, rh = 472, 196
    panel(d, [m, ry, 498, ry + rh], (232, 238, 245))
    kicker(d, m + 20, ry + 14, "WAR  •  UKRAINE", (30, 60, 120))
    headline(d, m + 20, ry + 44, 420, "KYIV BRIDGES HIT", 30)
    body(d, m + 20, ry + 88, 420,
         "Russia fires 400+ drones, 110+ missiles; 8 killed. Missiles land in Poland.", 20)
    panel(d, [526, ry, W - m, ry + rh], (250, 225, 225))
    kicker(d, 546, ry + 14, "MARKETS  •  AI SELL-OFF", RED)
    headline(d, 546, ry + 44, 420, "NASDAQ  -5.3%", 30)
    body(d, 546, ry + 88, 420,
         "2026 gains wiped out. Nvidia -14%, Anthropic -8.5% to $88.91.", 20)

    # Row 3: Summit | COP31
    ry, rh = 688, 196
    panel(d, [m, ry, 498, ry + rh], (238, 232, 222))
    kicker(d, m + 20, ry + 14, "DIPLOMACY  •  19 NOV SUMMIT", (120, 70, 20))
    headline(d, m + 20, ry + 44, 420, "TRUMP, XI, PUTIN", 30)
    body(d, m + 20, ry + 88, 420,
         "Shenzhen 'peace declaration': 'Nuclear war cannot be won.' No Ukraine deal.", 20)
    panel(d, [526, ry, W - m, ry + rh], (225, 240, 225))
    kicker(d, 546, ry + 14, "CLIMATE  •  ANTALYA", (30, 110, 50))
    headline(d, 546, ry + 44, 420, "COP31 IN OVERTIME", 30)
    body(d, 546, ry + 88, 420,
         "Draft deal drops all fossil-fuel mentions; $120bn adaptation fund cut.", 20)

    # Row 4: ICJ full width
    ry, rh = 904, 84
    panel(d, [m, ry, W - m, ry + rh], (235, 230, 245))
    d.text((m + 20, ry + 10), "LAW  •  19 NOV VERDICT, REACTION 20 NOV",
           font=font(SANSB, 18), fill=(70, 40, 110))
    headline(d, m + 20, ry + 36, W - m - 40,
             "ICJ: MYANMAR GUILTY OF GENOCIDE — first state ever, 9-6, reparations ordered.",
             20)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
