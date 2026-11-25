#!/usr/bin/env python3
"""rev4: draw the 24 Nov 2026 world-news summary image, 1024x1024 PNG.

Deterministic: no timestamps, no randomness. Run twice -> identical bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (246, 243, 236)
NAVY = (20, 38, 63)
AMBER = (217, 158, 43)
INK = (24, 28, 34)
MUTED = (96, 100, 108)
CARD = (255, 255, 255)
BORDER = (205, 200, 188)
WHITE = (255, 255, 255)

F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width. Returns list of lines."""
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


REGIONS = [
    ("NORTH AMERICA", 6, (31, 90, 140), [
        "Nvidia shares fall 7% as Huang's return rally fades a day after +31% surge",
        "US jury convicts Huawei of trade-secret conspiracy and bank fraud",
        "Democrats clinch largest House majority in decades — 259 seats",
        "Abrego Garcia to leave US voluntarily for Spain after deportation fight",
        "Trump set to unveil new tariffs after probe of excess factory capacity",
        "Pennsylvania measles outbreak claims 9th death across 46 counties",
    ]),
    ("LATIN AMERICA", 4, (150, 74, 32), [
        "Car bomb hits government HQ in Villavicencio, Colombia",
        "Drones strike police command in Cucuta, Colombia; 3 hurt, 60 homes damaged",
        "Mexico to try 'El Chapo Isidro' itself despite US extradition request",
        "WHO chief visits Cuba as health system deteriorates",
    ]),
    ("EUROPE", 7, (42, 92, 66), [
        "Lukashenko offers to fly with Zelenskiy to Moscow for peace talks",
        "Moscow accuses Estonia of acts 'on verge of triggering open war'",
        "Spain's top court grants amnesty to ex-Catalan leader Puigdemont",
        "UK sanctions five Myanmar generals over Rohingya genocide",
        "School shooting in Serbia wounds two; teenage suspect arrested",
        "UK logs record 5,258 heat-related deaths in 2026",
        "Germany first to access Ukraine's Delta battlefield system",
    ]),
    ("MIDDLE EAST", 6, (146, 44, 44), [
        "Houthi strike hits Riyadh's tallest tower; 11 injured — second hit in days",
        "Iran says 4th tanker hit by naval mine in Strait of Hormuz",
        "Iran rules out US talks until seven conditions are met",
        "Israeli strikes in Gaza kill 7, incl. Hamas security chief, despite ceasefire",
        "Eisenkot clinches first coalition deal in bid to form Israeli government",
        "UK sanctions Houthis and four officials over renewed aggression",
    ]),
    ("AFRICA", 5, (120, 84, 16), [
        "~175 migrants missing after contact lost with boat from Senegal",
        "Zambia opposition leader Mundubile charged with treason",
        "Sudan RSF defectors join army in Khartoum",
        "Fighting in DR Congo's Ituri traps Ebola responders near hospital",
        "21 killed in cattle-camp attack in South Sudan's Tonj East",
    ]),
    ("SOUTH ASIA", 6, (106, 44, 110), [
        "Bangladesh begins typhoid vaccination drive for 50m children",
        "Bangladesh rejects Hasina's plea to return: 'arrive as prisoner in handcuffs'",
        "Magnitude 5.6 quake strikes Nepal near China border",
        "Mobs hit ~100 Grameen Bank branches; Nobel laureate Yunus appeals for help",
        "Awami League clashes in Bangladesh injure 30; four crude bombs detonated",
        "Lahore world's most polluted major city as AQI hits 538",
    ]),
    ("EAST ASIA", 5, (16, 110, 118), [
        "China investigates Politburo member Chen Jining, Shanghai party chief",
        "China extends suspension of some US export curbs on critical minerals",
        "China opens Tiangong station to first foreign astronaut — Pakistan's Zeeshan Ali",
        "South Korea warns after Russian jets enter its air defence zone",
        "US blacklists Alibaba unit and Megaspeed in Nvidia chip scandal",
    ]),
    ("SOUTHEAST ASIA", 4, (30, 118, 74), [
        "Indonesia seizes 405 tonnes of missile chemical from China-bound ship",
        "Thai-Cambodia border fighting on hold after truce",
        "14 nations back ICJ ruling on Myanmar's Rohingya genocide",
        "Singapore investigates Megaspeed after US blacklisting",
    ]),
    ("OCEANIA", 3, (60, 74, 128), [
        "Solomon Islands to swap China security pact for Australia treaty",
        "Australia warns US-China rivalry straining conflict safeguards",
        "Nauru among states exiting ICC as Tajikistan starts withdrawal",
    ]),
]

TOP = [
    ("1  NVIDIA RALLY FADES",
     "Shares fall 7% a day after Huang's return sent them +31%; Huawei convicted in US court."),
    ("2  RIYADH TOWER STRUCK",
     "Houthi attack hits the capital's tallest tower — 11 injured, the second strike in days."),
    ("3  TANKERS HIT IN HORMUZ",
     "Iran says a 4th tanker struck a naval mine; Tehran rules out US talks until 7 conditions met."),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header band ----
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.rectangle([0, 96, W, 100], fill=AMBER)
    f_title = font(F_BOLD, 40)
    d.text((18, 12), "THE WORLD IN ONE PAGE", font=f_title, fill=WHITE)
    f_date = font(F_BOLD, 21)
    d.text((18, 62), "TUESDAY, 24 NOVEMBER 2026", font=f_date, fill=AMBER)
    f_sub = font(F_REG, 13)
    d.text((560, 66), "46 stories  ·  9 regions  ·  All dated 24 Nov 2026",
           font=f_sub, fill=(205, 210, 220))

    # ---- top stories strip ----
    f_top_label = font(F_BOLD, 12)
    d.text((18, 112), "TOP STORIES", font=f_top_label, fill=(146, 44, 44))
    strip_y, strip_h, strip_w, gap = 132, 62, 322, 10
    f_top_head = font(F_BOLD, 13)
    f_top_body = font(F_REG, 11.5)
    for i, (head, body) in enumerate(TOP):
        x = 18 + i * (strip_w + gap)
        d.rectangle([x, strip_y, x + strip_w, strip_y + strip_h], fill=CARD,
                    outline=BORDER, width=1)
        d.rectangle([x, strip_y, x + 4, strip_y + strip_h], fill=AMBER)
        d.text((x + 12, strip_y + 5), head, font=f_top_head, fill=INK)
        lines = wrap(d, body, f_top_body, strip_w - 24)
        y = strip_y + 24
        for ln in lines[:2]:
            d.text((x + 12, y), ln, font=f_top_body, fill=(52, 56, 64))
            y += 15

    # ---- region grid 3x3 ----
    grid_y, card_w, card_h, gx, gy = 206, 322, 258, 10, 8
    f_region = font(F_BOLD, 14)
    f_count = font(F_BOLD, 12)
    f_bullet = font(F_REG, 11.5)
    max_lines = 0
    for idx, (name, count, color, stories) in enumerate(REGIONS):
        r, c = divmod(idx, 3)
        x = 18 + c * (card_w + gx)
        y = grid_y + r * (card_h + gy)
        d.rectangle([x, y, x + card_w, y + card_h], fill=CARD,
                    outline=BORDER, width=1)
        d.rectangle([x, y, x + card_w, y + 28], fill=color)
        d.text((x + 10, y + 6), name, font=f_region, fill=WHITE)
        cnt = f"{count} stories"
        cw = d.textlength(cnt, font=f_count)
        d.text((x + card_w - cw - 10, y + 7), cnt, font=f_count, fill=(235, 235, 235))
        by = y + 36
        for s in stories:
            lines = wrap(d, s, f_bullet, card_w - 30)
            assert len(lines) <= 2, f"bullet needs {len(lines)} lines: {s}"
            max_lines = max(max_lines, len(lines))
            d.text((x + 10, by), "•", font=f_bullet, fill=color)
            ly = by
            for ln in lines:
                d.text((x + 24, ly), ln, font=f_bullet, fill=INK)
                ly += 14
            by = ly + 3
        assert by <= y + card_h - 4, f"card overflow: {name} ends at {by}, card ends {y + card_h}"

    # ---- footer ----
    f_foot = font(F_REG, 11)
    d.text((18, 998),
           "Sources: Reuters · AP · AFP · BBC · Al Jazeera · Anadolu · Just Security — "
           "events happened or were first reported on 24 November 2026.",
           font=f_foot, fill=MUTED)

    img.save("entry.png", format="PNG", optimize=True)
    total = sum(len(ss) for _, _, _, ss in REGIONS)
    print(f"saved entry.png  stories={total}  max_bullet_lines={max_lines}")


if __name__ == "__main__":
    main()
