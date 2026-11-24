#!/usr/bin/env python3
"""Render the rev2 news-image entry: one 1024x1024 PNG summing up the world
news of Tuesday, 24 November 2026 — 50 stories across 9 regions.

Run:  python3 render.py            (writes entry.png beside this file)
The entry itself is shipped as entry.png; main.py only copies it to the
output directory, so this renderer never runs inside the grader.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 14

PAPER = (246, 243, 236)
INK = (25, 25, 25)
GREY = (96, 94, 88)
CARD = (255, 255, 255)
CARD_EDGE = (216, 210, 194)
HAIRLINE = (227, 222, 208)
ACCENT = (158, 43, 37)          # deep red for the kicker
DARK_BAND = (31, 41, 55)        # slate band behind the top story
AMBER = (245, 158, 11)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked(draw, xy, text, fnt, fill, tracking=2):
    """Draw text with extra letter spacing; returns the width used."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x - xy[0] - tracking


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# (region name, colour, [headlines])
REGIONS = [
    ("NORTH AMERICA", (31, 78, 121), [
        "Nvidia brings back Jensen Huang as chief executive",
        "Court clears Army to detonate toxic explosives in Iowa",
        "Abrego Garcia to leave US voluntarily after deportation fight",
        "US consumer confidence jumps to near two-year high",
        "Microsoft declares 'Code Red' after historic outage",
        "Trump team poised to unveil new tariffs after capacity probe",
    ]),
    ("LATIN AMERICA", (180, 83, 9), [
        "Car bomb destroys buildings in Villavicencio, Colombia",
        "Gunmen hold 25 hostage in Cartagena supermarket",
        "WHO chief visits Cuba as health system breaks down",
        "Lula backs second fiscal package to curb spending",
        "Mexico to try 'El Chapo Isidro' despite US extradition bid",
    ]),
    ("EUROPE", (91, 33, 182), [
        "Lukashenko offers to fly with Zelenskiy to Moscow for talks",
        "Russian strikes on Kyiv region kill at least 14",
        "Moscow warns Estonia acts verge on 'open war'",
        "Spain's top court amnesties ex-leader Puigdemont",
        "UK recognises Rohingya genocide, sanctions Myanmar generals",
        "UK disability benefit review: system 'not fit for purpose'",
    ]),
    ("MIDDLE EAST", (185, 28, 28), [
        "Eisenkot seals first coalition deal in bid to form government",
        "Riyadh finance-district tower hit in 'terrorist attack'",
        "Houthis advance to 60 km from Aden; army says city will hold",
        "Israeli strikes kill Hamas security chief in Gaza",
        "US weighs military training for Syrian forces",
        "Deadly coach crash in Ras Al Khaimah, UAE",
    ]),
    ("AFRICA", (21, 128, 61), [
        "About 175 migrants missing after boat leaves Senegal",
        "Libya demands answers from Kyiv over strike off Benghazi",
        "Drones hit homes and UN building in Sudan",
        "Amnesty: Tigray strikes may be war crimes",
        "CAS reinstates Senegal as Africa Cup winners",
        "Nigerian monarch, 92, suspended after alleged assault",
    ]),
    ("SOUTH ASIA", (190, 24, 93), [
        "Bangladesh garment workers clash with police in pay protests",
        "Ex-PM Hasina plans December 16 return to Bangladesh",
        "Magnitude 5.6 quake strikes Nepal near China border",
        "Truck crash kills 7 in Punjab, Pakistan",
        "Lahore remains world's most polluted city as smog worsens",
    ]),
    ("EAST ASIA", (14, 116, 144), [
        "China investigates Politburo member Chen Jining",
        "China sentences official to death for spying",
        "Huawei guilty of stealing trade secrets in US trial",
        "China to fly first foreign astronaut to Tiangong station",
        "Russian jets enter South Korea's air-defence zone",
        "Japan to fund ICC in full after US sanctions",
    ]),
    ("SOUTHEAST ASIA", (101, 163, 13), [
        "Hot-pot restaurant blast kills 6 in Hanoi",
        "Indonesia seizes 405 tonnes of missile chemical",
        "Malaysia to repatriate 6,500 Myanmar migrants",
        "Malaysia tells data centres to cut US-blacklisted links",
        "Indonesia charges ex-police chief with treason",
    ]),
    ("OCEANIA", (3, 105, 161), [
        "Cyclone Xavier relief reaches Cook Islands",
        "Solomon Islands to drop China security pact",
        "Australian opposition blocks Vanuatu treaty",
        "Pacific dismay as COP31 ends without a deal",
        "Fiji shuts schools as El Niño drought deepens",
    ]),
]

TOP_STORY = ("Nvidia reinstates Jensen Huang as chief executive; "
             "shares slide 6% as the comeback rally fades")

FOOTER = ("Sources: Reuters · AP · AFP · BBC · Al Jazeera · The Straits Times · CNA"
          " — All stories reported Tuesday, 24 November 2026")


def draw_panel(draw, x, y, w, h, name, colour, stories):
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=CARD, outline=CARD_EDGE)
    draw.rectangle([x, y, x + w - 1, y + 4], fill=colour)
    head_f = font(SANS_BOLD, 16)
    count_f = font(SANS, 12)
    draw.text((x + 12, y + 14), name, font=head_f, fill=colour)
    count = f"{len(stories)} stories"
    draw.text((x + w - 12 - draw.textlength(count, font=count_f), y + 17),
              count, font=count_f, fill=GREY)
    draw.line([x + 12, y + 38, x + w - 12, y + 38], fill=HAIRLINE)

    body_f = font(SANS, 13)
    num_f = font(SANS_BOLD, 13)
    text_x = x + 34
    text_w = w - 34 - 12
    leading = 15.5
    wrapped = [wrap(draw, s, body_f, text_w) for s in stories]
    for lines in wrapped:
        if len(lines) > 2:
            raise SystemExit(f"OVERFLOW: headline needs {len(lines)} lines: "
                             f"{' '.join(lines)[:60]}")
    heights = [len(lines) * leading for lines in wrapped]
    area_top = y + 44
    area_h = h - 44 - 8
    n = len(stories)
    total_text = sum(heights)
    gap = (area_h - total_text) / (n - 1) if n > 1 else 0
    if gap < 6:
        raise SystemExit(f"OVERFLOW: {name} gap {gap:.1f}px "
                         f"(text {total_text}px in {area_h}px)")
    sy = area_top
    for i, lines in enumerate(wrapped):
        draw.text((x + 12, sy), f"{i + 1}", font=num_f, fill=colour)
        ly = sy
        for line in lines:
            draw.text((text_x, ly), line, font=body_f, fill=INK)
            ly += leading
        sy += heights[i] + gap
    return n, max(len(lines) for lines in wrapped)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # thin outer frame
    draw.rectangle([5, 5, W - 6, H - 6], outline=(207, 200, 180))

    # ---- header ----
    tracked(draw, (MARGIN + 2, 24), "THE WORLD IN ONE PAGE",
            font(SANS_BOLD, 14), ACCENT, tracking=3)
    draw.text((MARGIN + 2, 44), "Tuesday, 24 November 2026",
              font=font(SERIF_BOLD, 36), fill=INK)
    draw.text((MARGIN + 2, 90),
              "The day's world news, region by region",
              font=font(SANS, 14), fill=GREY)
    # right badge: story count
    badge = "50 STORIES  ·  9 REGIONS"
    bf = font(SANS_BOLD, 15)
    bw = draw.textlength(badge, font=bf) + 28
    bx = W - MARGIN - bw
    draw.rectangle([bx, 26, bx + bw, 62], outline=INK, width=2)
    draw.text((bx + 14, 37), badge, font=bf, fill=INK)
    # double rule under the header
    draw.line([MARGIN, 110, W - MARGIN, 110], fill=INK, width=2)
    draw.line([MARGIN, 114, W - MARGIN, 114], fill=INK, width=1)

    # ---- top-story strip ----
    draw.rectangle([MARGIN, 124, W - MARGIN, 150], fill=DARK_BAND)
    strip_f = font(SANS, 14)
    label_f = font(SANS_BOLD, 14)
    lx = MARGIN + 12
    draw.text((lx, 131), "TOP STORY", font=label_f, fill=AMBER)
    lx += draw.textlength("TOP STORY", font=label_f) + 10
    draw.text((lx, 131), "—  " + TOP_STORY, font=strip_f, fill=(255, 255, 255))

    # ---- region grid: 3 x 3 ----
    grid_top = 160
    gutter = 12
    pw = (W - 2 * MARGIN - 2 * gutter) // 3
    ph = 272
    total_stories = 0
    max_lines = 0
    for idx, (name, colour, stories) in enumerate(REGIONS):
        col, row = idx % 3, idx // 3
        x = MARGIN + col * (pw + gutter)
        y = grid_top + row * (ph + gutter)
        n, ml = draw_panel(draw, x, y, pw, ph, name, colour, stories)
        total_stories += n
        max_lines = max(max_lines, ml)

    # ---- footer ----
    foot_f = font(SANS, 12)
    fw = draw.textlength(FOOTER, font=foot_f)
    draw.text(((W - fw) / 2, 1008), FOOTER, font=foot_f, fill=GREY)

    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    print(f"wrote {out}  stories={total_stories}  max_lines_per_story={max_lines}")
    print(f"size={os.path.getsize(out)} bytes  dimensions={img.size}")


if __name__ == "__main__":
    main()
