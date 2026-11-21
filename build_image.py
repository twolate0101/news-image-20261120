"""Build the news-image entry v2: a 1024x1024 newspaper front page
summing up Friday 20 November 2026, drawn with Pillow only.
Run: python3 build_image.py  -> writes entry.png (<= 1 MiB).
Six featured stories + eight briefs = 14 stories. All facts were
checked against Reuters / CNN / Al Jazeera / NDTV / The Hindu search
results on 21 Nov 2026; 19 Nov events are labelled as such.
"""
from PIL import Image, ImageDraw, ImageFont

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
    draw.rounded_rectangle(box, radius=12, fill=fill, outline=border, width=3)


def headline(draw, x, y, w, text, size, color=INK, fnt=SANSB):
    f = font(fnt, size)
    lines = wrap(draw, text, f, w)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=color)
        y += size + 5
    return y


def body(draw, x, y, w, text, size=20, color=INK):
    f = font(SANS, size)
    for ln in wrap(draw, text, f, w):
        draw.text((x, y), ln, font=f, fill=color)
        y += size + 6
    return y


def kicker(draw, x, y, text, color, size=18):
    f = font(SANSB, size)
    draw.text((x, y), text, font=f, fill=color)
    return y + size + 9


def brief(draw, x, y, w, tag, head, text):
    # One compact brief: coloured tag, bold headline, one body line.
    f_tag = font(SANSB, 14)
    d_tag = draw.textlength(tag + "  ", font=f_tag)
    draw.text((x, y), tag, font=f_tag, fill=RED)
    f_h = font(SANSB, 17)
    for ln in wrap(draw, head, f_h, w - d_tag):
        draw.text((x + d_tag, y), ln, font=f_h, fill=INK)
        y += 21
        break  # headline: one line only
    f_b = font(SANS, 15)
    for ln in wrap(draw, text, f_b, w):
        draw.text((x, y), ln, font=f_b, fill=(60, 60, 60))
        y += 19
        break  # body: one line only
    return y


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    m = 34
    # Masthead
    d.text((m, 22), "THE WORLD IN ONE DAY", font=font(SERIF, 48), fill=INK)
    d.text((m, 82), "FRIDAY  20  NOVEMBER  2026", font=font(SANSB, 32), fill=RED)
    d.line([(m, 128), (W - m, 128)], fill=RED, width=5)
    d.text((m, 136), "Fourteen stories that defined the day  •  All 20 Nov 2026 unless noted",
           font=font(SANS, 19), fill=(90, 90, 90))

    # 1. GTA VI lead panel, neon Vice City gradient
    x0, y0, x1, y1 = m, 166, W - m, 356
    for i in range(y1 - y0):
        t = i / (y1 - y0)
        r = int(90 + 140 * t)
        g = int(30 + 60 * (1 - t))
        b = int(140 + 40 * t)
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=(r, g, b))
    d.rounded_rectangle([x0, y0, x1, y1], radius=12, outline=INK, width=3)
    d.ellipse([x1 - 170, y0 + 22, x1 - 56, y0 + 136], fill=(255, 190, 60))
    d.text((x0 + 22, y0 + 14), "ENTERTAINMENT  •  BIGGEST LAUNCH EVER",
           font=font(SANSB, 19), fill=(255, 220, 120))
    d.text((x0 + 22, y0 + 42), "$3.79BN IN A DAY", font=font(SANSB, 56), fill=(255, 255, 255))
    y = headline(d, x0 + 22, y0 + 108, x1 - x0 - 44,
                 "GTA VI SMASHES THE LAUNCH RECORD", 30, (255, 255, 255))
    body(d, x0 + 22, y + 2, x1 - x0 - 44,
         "Rockstar: 32.5m copies sold before release, first new GTA in 13 years.",
         20, (240, 240, 255))

    # Row 2: Kyiv | Nasdaq
    ry, rh = 372, 138
    panel(d, [m, ry, 498, ry + rh], (232, 238, 245))
    kicker(d, m + 18, ry + 10, "WAR  •  UKRAINE", (30, 60, 120), 17)
    headline(d, m + 18, ry + 36, 424, "KYIV BRIDGES HIT", 27)
    body(d, m + 18, ry + 72, 424,
         "Russia fires 400+ drones, 110+ missiles; 8 killed. Missiles land in Poland.", 18)
    panel(d, [526, ry, W - m, ry + rh], (250, 225, 225))
    kicker(d, 544, ry + 10, "MARKETS  •  AI SELL-OFF", RED, 17)
    headline(d, 544, ry + 36, 424, "NASDAQ  -5.3%", 27)
    body(d, 544, ry + 72, 424,
         "2026 gains wiped out. Nvidia -14%, Anthropic -8.5% to $88.91.", 18)

    # Row 3: Summit | COP31
    ry, rh = 526, 138
    panel(d, [m, ry, 498, ry + rh], (238, 232, 222))
    kicker(d, m + 18, ry + 10, "DIPLOMACY  •  19 NOV SUMMIT", (120, 70, 20), 17)
    headline(d, m + 18, ry + 36, 424, "TRUMP, XI, PUTIN", 27)
    body(d, m + 18, ry + 72, 424,
         "Shenzhen 'peace declaration': 'Nuclear war cannot be won.' No Ukraine deal.", 18)
    panel(d, [526, ry, W - m, ry + rh], (225, 240, 225))
    kicker(d, 544, ry + 10, "CLIMATE  •  ANTALYA", (30, 110, 50), 17)
    headline(d, 544, ry + 36, 424, "COP31 IN OVERTIME", 27)
    body(d, 544, ry + 72, 424,
         "Draft deal drops all fossil-fuel mentions; $120bn adaptation fund cut.", 18)

    # ICJ strip
    ry, rh = 680, 56
    panel(d, [m, ry, W - m, ry + rh], (235, 230, 245))
    d.text((m + 18, ry + 8), "LAW  •  19 NOV VERDICT",
           font=font(SANSB, 16), fill=(70, 40, 110))
    d.text((m + 18, ry + 30),
           "ICJ: MYANMAR GUILTY OF GENOCIDE — first state ever, 9-6, reparations ordered.",
           font=font(SANSB, 19), fill=INK)

    # The day in brief: 8 verified stories, 2 columns x 4 rows
    d.text((m, 752), "THE DAY IN BRIEF", font=font(SANSB, 22), fill=RED)
    d.line([(m, 782), (W - m, 782)], fill=INK, width=3)
    # All eight briefs were verified by me against search results:
    # Akvan, Kerch, Trump-Iran, PIF Tower, Bukele, EU-UK reset,
    # TSMC/Samsung curbs, and Malik's Delhi visit (Dawn, 20 Nov).
    briefs = [
        ("CYCLONE", "AKVAN HITS ODISHA",
         "Landfall near Gopalpur; 372,000 evacuated, no deaths."),
        ("UKRAINE", "KERCH BRIDGE ROAD SPAN FALLS",
         "Strikes 17-19 Nov collapse road deck; Neptune hit halts rail."),
        ("IRAN", "TRUMP PUSHES DECISION TO 2027",
         "'I'll talk to you about it after the beginning of the year.'"),
        ("RIYADH", "HOUTHI MISSILE HITS PIF TOWER",
         "19 Nov: windows out on 7-8 floors, no injuries."),
        ("EL SALVADOR", "BUKELE SEEKS THIRD TERM",
         "Registers 19 Nov for 28 Feb 2027 vote; term limits gone."),
        ("EU-UK", "BREXIT RESET DEAL SEALED",
         "Food checks scrapped; youth mobility for 100,000."),
        ("CHIPS", "TSMC, SAMSUNG HALT CHINA ORDERS",
         "US rule, 19 Nov: 16nm and below need export licences."),
        ("SOUTH ASIA", "PAKISTAN MINISTER IN DELHI",
         "First Pakistani minister in India since 2023, for SCO forum."),
    ]
    col_w = 462
    for i, (tag, head, text) in enumerate(briefs):
        col = i % 2
        row = i // 2
        x = m + col * (col_w + 28)
        y = 796 + row * 56
        brief(d, x, y, col_w, tag, head, text)
        if row < 3:
            d.line([(x, y + 46), (x + col_w, y + 46)], fill=(200, 195, 185), width=1)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
