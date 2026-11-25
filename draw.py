#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news summary image (1024x1024 PNG).

Reads nothing but the STORIES table below and writes entry.png next to this
file (or to the path in argv[1]). Deterministic: fixed fonts, fixed layout,
no timestamps, no randomness, so repeated runs are byte-identical.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (246, 242, 233)
CARD = (255, 253, 248)
INK = (25, 25, 25)
MUTED = (107, 101, 88)
LINE = (216, 210, 196)
HEADER = (20, 33, 61)
AMBER = (252, 163, 17)
LEAD_GREY = (207, 202, 187)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

# (region, colour, [(headline, source), ...]) — 5 stories each, 9 regions.
REGIONS = [
    ("NORTH AMERICA", (31, 78, 121), [
        ("Huang back at Nvidia HQ as rally fades; shares fall 6%", "Reuters"),
        ("US consumer confidence hits near two-year high", "Reuters"),
        ("Trump taps prosecutor who lost re-election for judgeship", "Reuters"),
        ("Court clears Army to detonate toxic explosives in Iowa", "Reuters"),
        ("Democrats vow to reverse Trump’s food-aid cuts", "Reuters"),
    ]),
    ("LATIN AMERICA", (46, 125, 50), [
        ("Sheinbaum: no US troops in Sinaloa kingpin arrest", "AP"),
        ("Brazil summons Flávio Bolsonaro for “slandering” Lula", "Breitbart"),
        ("Maduro’s first birthday behind bars in US custody", "Breitbart"),
        ("WHO chief pledges $2m for Cuba vaccination drive", "Breitbart"),
        ("FIFA: US, Mexico, Costa Rica, Jamaica host 2031 World Cup", "TOI"),
    ]),
    ("EUROPE", (91, 45, 142), [
        ("NATO vows to defend space after Russian satellite reports", "BBC"),
        ("Germany first to access Ukraine’s Delta system", "Kyiv Independent"),
        ("Seven states back EU push to limit Russian visas", "Kyiv Independent"),
        ("Two held after break-in at Prince William’s Norfolk home", "SCMP"),
        ("COP31 climate talks collapse in Antalya over fossil fuels", "Grist"),
    ]),
    ("MIDDLE EAST", (192, 86, 33), [
        ("Israeli strike kills Hamas security chief in Gaza City", "Reuters"),
        ("US discussing military training for Syrian forces", "Reuters"),
        ("US envoy doubts Trump pledge to end $3.8bn Israel aid", "Reuters"),
        ("Iraq PM orders state to run oilfields in Kurdish areas", "Reuters"),
        ("Saudi condemns “terrorist attack” as Riyadh tower hit twice", "SCMP"),
    ]),
    ("AFRICA", (141, 43, 61), [
        ("Ukraine says drones sank Russian warship off Libya", "Reuters"),
        ("About 175 migrants missing after boat lost from Senegal", "Reuters"),
        ("Fighting traps Ebola responders in DR Congo’s Ituri", "UN News"),
        ("Fire engulfs six Zanzibar hotels; 180 tourists evacuated", "TOI"),
        ("Amnesty: Ethiopia, Tigray strikes may be war crimes", "Reuters"),
    ]),
    ("SOUTH ASIA", (14, 116, 144), [
        ("India invokes 1943 Bengal famine at UN Security Council", "TOI"),
        ("5.3 quake jolts North Bengal and Sikkim", "Shillong Times"),
        ("Hasina plans Dec 16 return; Dhaka vows arrest", "Reuters"),
        ("India gives $1.62bn package to flood-hit Nepal", "SRI"),
        ("Asia Cup Rising Stars: India A, Pakistan A reach semis", "Tribune"),
    ]),
    ("EAST ASIA", (185, 28, 28), [
        ("China probes Shanghai chief Chen Jining, Politburo member", "Xinhua"),
        ("North Korea threatens to shut Swiss office over sanctions", "SCMP"),
        ("Russian jets enter South Korea’s air defence zone", "AP"),
        ("South Korea offers $375,000 to catch AI exam cheats", "WSJ"),
        ("Japan to pay 2027 ICC contribution early, Takaichi says", "Reuters"),
    ]),
    ("SOUTHEAST ASIA", (133, 77, 14), [
        ("US blacklists Singapore cloud firm Megaspeed over chips", "Politico"),
        ("Philippines deports 139 Indonesians in scam raid", "Inquirer"),
        ("Indonesia factory fire toll rises to 26; 28 still missing", "ASEANS"),
        ("Landmine casualties hit five-year high of 7,000", "SCMP"),
        ("US tariff probe names six ASEAN economies among 16 targets", "WSJ"),
    ]),
    ("OCEANIA", (71, 85, 105), [
        ("Australian shares hit six-month low as AI sell-off bites", "Bus. Recorder"),
        ("Australia to treat AI as key foreign-policy issue", "SCMP"),
        ("PNG votes on Bougainville independence", "Evening Report"),
        ("Australia thrash France 92–0 to reach women’s RLWC semis", "BBC"),
        ("Australia pledges $4bn for remote housing", "Evening Report"),
    ]),
]

TITLE = "THE WORLD IN ONE DAY"
DATE_LINE = "TUESDAY, 24 NOVEMBER 2026"
DATE_TAIL = "  ·  45 STORIES  ·  9 REGIONS"
LEAD = ("Lead: Huang back at Nvidia HQ as rally fades  ·  COP31 talks collapse  ·  "
        "Ukraine says it sank a Russian warship off Libya")
FOOTER = ("Sources: Reuters · AP · BBC · SCMP · Al Jazeera · Inquirer · Kyiv Independent · "
          "WSJ · NYT · Politico · Grist · TOI — All stories first reported on "
          "Tuesday, 24 November 2026")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines, each within max_w."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if fnt.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_story(text, source, max_w):
    """Pick the largest size (14, 13.5, 13) whose wrap fits in 2 lines."""
    full = "%s (%s)" % (text, source)
    for size in (14, 13.5, 13):
        fnt = font(BOLD, size)
        lines = wrap(full, fnt, max_w)
        if len(lines) <= 2:
            return fnt, lines, size, False
    fnt = font(BOLD, 13)
    lines = wrap(full, fnt, max_w)[:2]
    # hard-truncate the second line with an ellipsis
    while len(lines) == 2 and fnt.getlength(lines[1] + " …") > max_w:
        cut = lines[1].rsplit(" ", 1)[0]
        if cut == lines[1]:
            lines[1] = lines[1][:-1]
        else:
            lines[1] = cut
    lines[1] = lines[1] + " …"
    return fnt, lines, 13, True


def draw_line_with_source(draw, x, y, line, fnt, colour):
    """Draw one wrapped line; the trailing (Source) parenthetical in colour."""
    words = line.split(" ")
    src_idx = None
    for i, w in enumerate(words):
        if w.startswith("("):
            src_idx = i
            break
    if src_idx is None:
        draw.text((x, y), line, font=fnt, fill=INK)
        return
    head = " ".join(words[:src_idx])
    tail = " ".join(words[src_idx:])
    draw.text((x, y), head, font=fnt, fill=INK)
    draw.text((x + fnt.getlength(head + " "), y), tail, font=fnt, fill=colour)


def draw_card(draw, x, y, w, h, name, colour, stories):
    draw.rounded_rectangle([x, y, x + w - 1, y + h - 1], radius=4,
                           fill=CARD, outline=LINE, width=1)
    # region header band
    draw.rounded_rectangle([x, y, x + w - 1, y + 30], radius=4, fill=colour)
    draw.rectangle([x, y + 20, x + w - 1, y + 30], fill=colour)
    draw.rectangle([x, y, x + 6, y + 30], fill=colour)
    hf = font(BOLD, 15)
    draw.text((x + 12, y + 7), name, font=hf, fill=(255, 255, 255))
    cf = font(BOLD, 11)
    tag = "5 STORIES"
    draw.text((x + w - 12 - cf.getlength(tag), y + 9), tag, font=cf,
              fill=(255, 255, 255))
    # stories
    text_w = w - 24 - 12
    story_y = y + 38
    line_h = 19
    gap = 9
    report = []
    for text, source in stories:
        fnt, lines, size, truncated = fit_story(text, source, text_w)
        report.append((text, size, len(lines), truncated))
        draw.rectangle([x + 12, story_y + 6, x + 18, story_y + 12], fill=colour)
        for i, ln in enumerate(lines):
            draw_line_with_source(draw, x + 24, story_y + i * line_h, ln,
                                  fnt, colour)
        story_y += 2 * line_h + gap
    return report


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # header band
    d.rectangle([0, 0, W - 1, 111], fill=HEADER)
    d.rectangle([0, 111, W - 1, 114], fill=AMBER)
    d.text((24, 12), TITLE, font=font(BOLD, 38), fill=(255, 255, 255))
    d.text((24, 58), DATE_LINE, font=font(BOLD, 22), fill=AMBER)
    dw = font(BOLD, 22).getlength(DATE_LINE)
    d.text((24 + dw, 60), DATE_TAIL, font=font(REG, 17), fill=(255, 255, 255))
    d.text((24, 88), LEAD, font=font(REG, 14), fill=LEAD_GREY)

    # 3x3 grid of region cards
    margin, gap = 24, 12
    cw = (W - 2 * margin - 2 * gap) // 3
    ch = 282
    top = 124
    report = []
    for i, (name, colour, stories) in enumerate(REGIONS):
        cx = margin + (i % 3) * (cw + gap)
        cy = top + (i // 3) * (ch + gap)
        report += draw_card(d, cx, cy, cw, ch, name, colour, stories)

    # footer
    ff = font(REG, 12)
    fw = ff.getlength(FOOTER)
    d.text(((W - fw) / 2, 1004), FOOTER, font=ff, fill=MUTED)

    img.save(out, "PNG")
    data = open(out, "rb").read()
    print("stories:", sum(len(r[2]) for r in REGIONS))
    print("regions:", len(REGIONS))
    print("bytes:", len(data))
    print("sha256:", hashlib.sha256(data).hexdigest())
    bad = [r for r in report if r[3] or r[2] > 2]
    small = [r for r in report if r[1] < 14]
    print("truncated/overflowing:", len(bad))
    for r in bad:
        print("  OVERFLOW:", r)
    print("shrunk below 14px:", len(small))
    for r in small:
        print("  SHRUNK:", r)


if __name__ == "__main__":
    main()
