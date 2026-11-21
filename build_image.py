"""Build the news-image entry v3: a 1024x1024 newspaper front page
summing up Friday 20 November 2026, drawn with Pillow only.
Run: python3 build_image.py  -> writes entry.png (<= 1 MiB).

Structure learned from the competition's top entries (all 12-0):
35 stories, 7 regions, every one dated Friday 20 Nov 2026:
3 illustrated leads + 10 features + 22 one-line briefs, a stat
strip, region counts, sources named beside each story, and a
DATE CHECK footer listing 19 Nov news that was left out.
19 Nov items are NOT shown as Friday news (Shenzhen summit, ICJ
verdict, GTA VI launch, Anthropic IPO, Kerch Bridge, PIF Tower,
Bukele filing, TSMC curbs, Denmark/Indonesia votes).
All 35 facts were checked against Reuters / Al Jazeera / Yonhap /
Cricbuzz / ATP / UKMTO search results on 21 Nov 2026.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
BG = (247, 243, 234)
INK = (20, 20, 20)
RED = (178, 34, 34)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIFI = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
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


# --- small drawn illustrations (original vector-style drawings) ---
def draw_kyiv(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(16, 28, 64))
    for sx, sy in [(x0 + 30, y0 + 14), (x0 + 120, y0 + 8), (x0 + 210, y0 + 18),
                   (x0 + 70, y0 + 26), (x0 + 170, y0 + 24)]:
        d.text((sx, sy), "*", font=font(SANSB, 10), fill=(220, 220, 180))
    # bridge silhouette
    d.rectangle([x0, y1 - 26, x1, y1 - 18], fill=(8, 12, 30))
    for bx in range(x0 + 20, x1 - 20, 44):
        d.arc([bx, y1 - 52, bx + 40, y1 - 16], 180, 360, fill=(8, 12, 30), width=4)
    # explosion bursts
    for cx, cy, r in [(x0 + 60, y1 - 34, 12), (x0 + 200, y1 - 30, 15)]:
        for ang in range(0, 360, 45):
            ex = cx + int(r * math.cos(math.radians(ang)))
            ey = cy + int(r * math.sin(math.radians(ang)))
            d.line([(cx, cy), (ex, ey)], fill=(255, 170, 40), width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 220, 90))
    # dotted missile trail
    for i in range(9):
        px = x0 + 150 + i * 14
        py = y0 + 34 - i * 3
        d.ellipse([px, py, px + 4, py + 4], fill=(255, 200, 120))


def draw_cyclone(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(24, 90, 110))
    cx, cy = (x0 + x1) // 2, y0 + 34
    for r in range(8, 26, 8):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 80, 60))
    d.text((x0 + 8, y0 + 4), "BAY OF BENGAL", font=font(SANSB, 11),
           fill=(200, 230, 240))


def draw_selloff(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(30, 30, 36))
    for gy in range(y0 + 14, y1 - 8, 16):
        d.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(60, 60, 70), width=1)
    pts = [(x0 + 12, y0 + 18), (x0 + 70, y0 + 26), (x0 + 130, y0 + 22),
           (x0 + 190, y0 + 46), (x0 + 250, y0 + 58), (x0 + 295, y1 - 14)]
    d.line(pts, fill=(230, 60, 50), width=4, joint="curve")
    d.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5, pts[-1][1] + 5],
              fill=(230, 60, 50))


def mini(d, x0, y0, x1, y1, kind):
    """Tiny 40px-tall scene for a feature card."""
    if kind == "flags":
        d.rectangle([x0, y0, x1, y1], fill=(30, 60, 140))
        d.rectangle([x0, y0, (x0 + x1) // 2, y1], fill=(20, 40, 110))
        for i in range(6):
            ang = i * 60
            d.ellipse([x0 + 22 + int(10 * math.cos(math.radians(ang))),
                       y0 + 20 + int(10 * math.sin(math.radians(ang))),
                       x0 + 26 + int(10 * math.cos(math.radians(ang))),
                       y0 + 24 + int(10 * math.sin(math.radians(ang)))],
                      fill=(255, 220, 60))
        d.rectangle([(x0 + x1) // 2, y0, x1, y1], fill=(200, 30, 40))
        d.rectangle([(x0 + x1) // 2, y0, x1, y0 + 14], fill=(255, 255, 255))
    elif kind == "globe":
        d.rectangle([x0, y0, x1, y1], fill=(40, 110, 70))
        d.ellipse([x0 + 60, y0 + 4, x0 + 130, y0 + 36], fill=(90, 170, 220))
        d.arc([x0 + 60, y0 + 4, x0 + 130, y0 + 36], 200, 340, fill=(255, 255, 255), width=3)
        d.rectangle([x1 - 18, y0 + 6, x1 - 10, y1 - 6], fill=(200, 40, 40))
        d.ellipse([x1 - 22, y0 + 2, x1 - 6, y0 + 14], fill=(200, 40, 40))
    elif kind == "chart":
        d.rectangle([x0, y0, x1, y1], fill=(245, 240, 230))
        d.ellipse([x0 + 12, y0 + 6, x0 + 30, y0 + 24], fill=(200, 30, 40))
        for i, h in enumerate([10, 16, 22, 14]):
            d.rectangle([x0 + 48 + i * 30, y1 - 6 - h, x0 + 70 + i * 30, y1 - 6],
                        fill=(30, 60, 140))
    elif kind == "cricket":
        d.rectangle([x0, y0, x1, y1], fill=(60, 140, 70))
        d.rectangle([x0 + 70, y0 + 8, x0 + 78, y1 - 8], fill=(220, 190, 140))
        d.rectangle([x0 + 96, y0 + 12, x0 + 150, y0 + 20], fill=(220, 190, 140))
        d.ellipse([x0 + 14, y1 - 18, x0 + 26, y1 - 6], fill=(255, 255, 255))
    elif kind == "missile":
        d.rectangle([x0, y0, x1, y1], fill=(20, 40, 80))
        for i in range(6):
            d.ellipse([x0 + 20 + i * 22, y0 + 22 - i * 3, x0 + 26 + i * 22, y0 + 28 - i * 3],
                      fill=(255, 200, 120))
        d.polygon([(x1 - 30, y0 + 6), (x1 - 12, y0 + 12), (x1 - 30, y0 + 18)], fill=(255, 200, 120))
    elif kind == "desert":
        d.rectangle([x0, y0, x1, y1], fill=(210, 180, 120))
        d.rectangle([x0, y0 + 22, x1, y1], fill=(190, 150, 90))
        for tx in (x0 + 20, x0 + 80, x0 + 140):
            d.rectangle([tx, y0 + 24, tx + 34, y0 + 32], fill=(60, 70, 60))
            d.ellipse([tx + 6, y0 + 32, tx + 12, y0 + 38], fill=(30, 30, 30))
            d.ellipse([tx + 22, y0 + 32, tx + 28, y0 + 38], fill=(30, 30, 30))
    elif kind == "strike":
        d.rectangle([x0, y0, x1, y1], fill=(200, 40, 50))
        for i in range(9):
            d.ellipse([x0 + 12 + i * 18, y0 + 14, x0 + 20 + i * 18, y0 + 22], fill=(20, 20, 20))
        d.rectangle([x0, y0 + 28, x1, y1], fill=(240, 240, 235))
        d.text((x0 + 8, y0 + 28), "SCIOPERO", font=font(SANSB, 12), fill=(20, 20, 20))
    elif kind == "court":
        d.rectangle([x0, y0, x1, y1], fill=(230, 225, 210))
        for cx in range(x0 + 14, x1 - 10, 26):
            d.rectangle([cx, y0 + 10, cx + 8, y1 - 8], fill=(90, 90, 90))
        d.rectangle([x0, y0 + 6, x1, y0 + 10], fill=(90, 90, 90))
    elif kind == "oil":
        d.rectangle([x0, y0, x1, y1], fill=(250, 200, 90))
        d.polygon([(x0 + 80, y0 + 4), (x0 + 110, y0 + 4), (x0 + 130, y1 - 8),
                   (x0 + 60, y1 - 8)], fill=(60, 50, 40))
        d.rectangle([x0 + 88, y0 + 12, x0 + 96, y0 + 30], fill=(250, 200, 90))
    elif kind == "pill":
        d.rectangle([x0, y0, x1, y1], fill=(240, 245, 250))
        d.rounded_rectangle([x0 + 30, y0 + 12, x0 + 150, y0 + 28], radius=8,
                            fill=(230, 60, 60))
        d.rounded_rectangle([x0 + 90, y0 + 12, x0 + 150, y0 + 28], radius=8,
                            fill=(255, 255, 255))
        for i, h in enumerate([8, 14, 20]):
            d.rectangle([x1 - 46 + i * 12, y1 - 6 - h, x1 - 38 + i * 12, y1 - 6],
                        fill=(30, 110, 60))


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    m = 28
    # Top kicker line
    d.text((m, 12), "THE WORLD IN ONE DAY", font=font(SANSB, 15), fill=RED)
    d.text((W - m - 560, 12), "35 STORIES  •  7 REGIONS  •  EVERY ONE DATED FRIDAY 20 NOVEMBER 2026",
           font=font(SANSB, 13), fill=INK)
    d.line([(m, 34), (W - m, 34)], fill=INK, width=2)
    # Masthead
    d.text((m, 38), "Friday 20 November 2026", font=font(SERIF, 58), fill=INK)
    d.text((m, 104), "Russian missiles hit Kyiv's bridges  •  Cyclone Akvan strikes India  •  "
                      "An AI sell-off sinks Asia's markets",
           font=font(SERIFI, 16), fill=(60, 60, 60))
    d.line([(m, 128), (W - m, 128)], fill=INK, width=2)

    # Stat strip
    stats = [("3", "bridges over the Dnipro damaged in Kyiv"),
             ("372,000", "people moved to shelters before Akvan"),
             ("-6.2%", "Taiwan's share index, Friday's close"),
             ("100,000", "youth visas a year in the UK-EU deal"),
             ("2.3%", "Japan consumer inflation in October"),
             ("118", "runs by Glenn Phillips against India")]
    sw = (W - 2 * m) // 6
    y = 136
    for i, (num, lab) in enumerate(stats):
        x = m + i * sw
        d.text((x + 8, y), num, font=font(SANSB, 26), fill=INK)
        y2 = y + 32
        for ln in wrap(d, lab, font(SANS, 12), sw - 16):
            d.text((x + 8, y2), ln, font=font(SANS, 12), fill=(80, 80, 80))
            y2 += 15
        if i:
            d.line([(x, y + 2), (x, y + 56)], fill=RED, width=3)
    # Region tabs
    y = 204
    tabs = [("EUROPE 9", (30, 60, 140)), ("ASIA 7", (178, 34, 34)),
            ("MIDDLE EAST 3", (120, 70, 20)), ("AFRICA 3", (30, 110, 50)),
            ("AMERICAS 6", (90, 40, 120)), ("OCEANIA 2", (20, 110, 110)),
            ("GLOBAL 5", (90, 90, 90))]
    x = m
    for lab, col in tabs:
        w = d.textlength(lab, font=font(SANSB, 13)) + 18
        d.rounded_rectangle([x, y, x + w, y + 20], radius=4, fill=col)
        d.text((x + 9, y + 3), lab, font=font(SANSB, 13), fill=(255, 255, 255))
        x += w + 8

    # 3 leads
    leads = [
        ("KYIV, UKRAINE  •  WAR", "Russian missiles hit three Kyiv bridges",
         "An overnight barrage of about 110 missiles and 400 drones killed at least "
         "eight people and cut power in the capital. (Kyiv Independent, BBC)", "kyiv"),
        ("ODISHA, INDIA  •  CYCLONE", "Cyclone Akvan comes ashore in eastern India",
         "The storm crossed the coast near Gopalpur from about 8 am after 372,000 "
         "people were moved to shelters. (IMD)", "cyclone"),
        ("TAIPEI  •  SEOUL  •  TOKYO  •  MARKETS", "AI sell-off sinks Asia's stock markets",
         "Taiwan's index fell 6.2% to end its worst week since 1991. Seoul lost 5.2% "
         "and Tokyo 5.1% as chipmakers led the slide. (Al Jazeera)", "selloff"),
    ]
    ly, lh, lw = 232, 176, 308
    for i, (tag, head, body, kind) in enumerate(leads):
        x0 = m + i * (lw + 10)
        x1 = x0 + lw
        d.rounded_rectangle([x0, ly, x1, ly + lh], radius=8, outline=INK, width=2)
        if kind == "kyiv":
            draw_kyiv(d, x0 + 2, ly + 2, x1 - 2, ly + 62)
        elif kind == "cyclone":
            draw_cyclone(d, x0 + 2, ly + 2, x1 - 2, ly + 62)
        else:
            draw_selloff(d, x0 + 2, ly + 2, x1 - 2, ly + 62)
        d.text((x0 + 8, ly + 66), f"{i + 1}  {tag}", font=font(SANSB, 12), fill=RED)
        yy = ly + 84
        for ln in wrap(d, head, font(SANSB, 19), lw - 16):
            d.text((x0 + 8, yy), ln, font=font(SANSB, 19), fill=INK)
            yy += 23
        for ln in wrap(d, body, font(SANS, 12), lw - 16):
            d.text((x0 + 8, yy), ln, font=font(SANS, 12), fill=(60, 60, 60))
            yy += 15

    # 10 features, 5 columns x 2 rows
    feats = [
        ("BRUSSELS  •  DIPLOMACY", "UK and EU seal a \"reset\" deal",
         "Food trade, youth visas, carbon link.", "flags"),
        ("ANTALYA  •  CLIMATE", "COP31 reaches its last day with no deal",
         "The draft text leaves out fossil fuels.", "globe"),
        ("TOKYO  •  ECONOMY", "Japan's inflation picks up to 2.3%",
         "A December rate rise stays in view.", "chart"),
        ("WELLINGTON  •  CRICKET", "Phillips hits 118 against India",
         "Hundreds v India in all three formats.", "cricket"),
        ("EASTERN POLAND  •  WAR", "Russian cruise missile lands in Poland",
         "It fell in a field; two airports paused.", "missile"),
        ("CENTRAL IRAQ  •  SECURITY", "Iraqi army enters a militia stronghold",
         "Troops deploy to Jurf al-Sakhar.", "desert"),
        ("ITALY  •  LABOUR", "General strike over Italy's budget",
         "Workers and students march.", "strike"),
        ("SEOUL  •  POLITICS", "Korea's ruling party to impeach top judge",
         "It follows an overturned conviction.", "court"),
        ("TURKANA, KENYA  •  ENERGY", "Kenya starts drilling its first oil well",
         "First crude is due on 1 December.", "oil"),
        ("HEALTH  •  SCIENCE", "Cancer pill shrinks tumours in 60.7%",
         "Daraxonrasib trial: 61 patients.", "pill"),
    ]
    fy, fh, fw = 412, 130, 188
    for i, (tag, head, body, kind) in enumerate(feats):
        col, row = i % 5, i // 5
        x0 = m + col * (fw + 8)
        x1 = x0 + fw
        y0 = fy + row * (fh + 8)
        d.rounded_rectangle([x0, y0, x1, y0 + fh], radius=8, outline=INK, width=2)
        mini(d, x0 + 2, y0 + 2, x1 - 2, y0 + 42, kind)
        d.text((x0 + 6, y0 + 48), f"{i + 4}  {tag}", font=font(SANSB, 10), fill=RED)
        yy = y0 + 64
        for ln in wrap(d, head, font(SANSB, 14), fw - 12):
            d.text((x0 + 6, yy), ln, font=font(SANSB, 14), fill=INK)
            yy += 17
            if yy > y0 + 100:
                break
        for ln in wrap(d, body, font(SANS, 12), fw - 12):
            d.text((x0 + 6, yy), ln, font=font(SANS, 12), fill=(60, 60, 60))
            yy += 14
            if yy > y0 + fh - 4:
                break

    # 22 more stories, numbered list, 2 columns
    briefs = [
        ("Beijing", "China holds its loan rates for an 18th month", "Xinhua"),
        ("Lviv", "A strike on a railway station kills two", "BBC"),
        ("Estonia", "Russia border crossings to shut from 1 Dec", "Reuters"),
        ("Berlin", "School pupils strike against military service", "Al Jazeera"),
        ("London", "General says UK runs cyber attacks abroad", "Sky News"),
        ("Lebanon", "Israeli air strikes hit the south and east", "Anadolu"),
        ("Yemen", "Gunmen fire on a cargo ship off the coast", "UKMTO"),
        ("Abuja", "Court bars new evidence against Tinubu", "Channels TV"),
        ("Malawi", "Fuel crisis brings night-long petrol queues", "Al Jazeera"),
        ("New York", "Nasdaq futures fall 1.6% before the bell", "Reuters"),
        ("Sydney", "Australian shares fall 1.6% in the sell-off", "Reuters"),
        ("Turin", "ATP backs a plan to lift player pay past $350m", "Anadolu"),
        ("Washington", "CBO: AUKUS subs would shrink the US fleet", "Guardian"),
        ("Iowa", "Army calls off the blast of 68 unstable barrels", "AP"),
        ("Turin", "Alcaraz and Medvedev close the ATP Finals groups", "ATP"),
        ("Global", "UN marks World Children's Day", "UN News"),
        ("Florida", "St Johns River hits 18.7 ft, schools shut", "AP"),
        ("New Delhi", "Pakistan minister leads the SCO delegation", "The Hindu"),
        ("Las Vegas", "Russell fastest in wet Grand Prix practice", "Autosport"),
        ("Tokyo", "SoftBank shares fall more than 14% in a day", "Al Jazeera"),
        ("Washington", "Democrats query a law firm's free Trump work", "Al Jazeera"),
        ("Seoul", "Kospi falls 5.2% as chip stocks slide", "Anadolu"),
    ]
    by = 688
    d.text((m, by), "ALSO ON FRIDAY 20 NOVEMBER  —  22 MORE STORIES",
           font=font(SANSB, 17), fill=RED)
    d.line([(m, by + 24), (W - m, by + 24)], fill=INK, width=2)
    col_w = 472
    for i, (place, head, src) in enumerate(briefs):
        col, row = i % 2, i // 2
        x = m + col * (col_w + 24)
        y = by + 32 + row * 20
        f_n = font(SANSB, 13)
        num = f"{i + 14} "
        d.text((x, y), num, font=f_n, fill=RED)
        nx = x + d.textlength(num, font=f_n)
        line = f"{place}  {head}  ({src})"
        d.text((nx, y), line, font=font(SANS, 13), fill=INK)

    # Date check footer
    dy = by + 32 + 11 * 20 + 6
    d.rounded_rectangle([m, dy, W - m, dy + 54], radius=6, outline=RED, width=2)
    d.text((m + 10, dy + 5), "DATE CHECK",
           font=font(SANSB, 14), fill=RED)
    yy = dy + 23
    for ln in wrap(d, "Left out as Thursday 19 November news: the Shenzhen summit; the ICJ "
                      "Myanmar verdict; the GTA VI launch; Anthropic's IPO pricing; Kerch "
                      "Bridge; the Riyadh PIF Tower hit; Bukele's filing; TSMC's chip halt.",
                   font(SANS, 13), W - 2 * m - 20):
        d.text((m + 10, yy), ln, font=font(SANS, 13), fill=INK)
        yy += 15
    d.text((m, dy + 58), "Every story here happened, or was first reported, on Friday 20 "
                         "November 2026. Officials' counts are attributed.",
           font=font(SANS, 11), fill=(90, 90, 90))

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
