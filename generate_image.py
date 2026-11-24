#!/usr/bin/env python3
"""Draw a 1024x1024 newspaper front page summing up world news of
Tuesday 24 November 2026, in six panels. Pure PIL, no network, no
external images. Deterministic: same input always yields same bytes."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (26, 26, 26)
NAVY = (31, 58, 95)
RED = (164, 30, 34)
WHITE = (255, 255, 255)
GREY = (90, 88, 80)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, line_h, fill=INK):
    """Draw wrapped text; returns y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def text_block_height(draw, text, fnt, max_w, line_h):
    return len(wrap(draw, text, fnt, max_w)) * line_h


# ---------------------------------------------------------------- scenes
def scene_zaporizhzhia(d, x, y, w, h):
    """Night sky, apartment block with a damaged corner, fire glow."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 34, 58))
    for sx, sy, r in [(x + 30, y + 22, 2), (x + 90, y + 14, 2),
                      (x + 200, y + 26, 2), (x + 260, y + 16, 2),
                      (x + 150, y + 34, 1)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 220, 200))
    # apartment block
    bx, by, bw, bh = x + 55, y + 55, 200, h - 55
    d.rectangle([bx, by, bx + bw, by + bh], fill=(70, 66, 60))
    # broken top-right corner (dark jagged gap)
    d.polygon([(bx + 150, by), (bx + bw, by), (bx + bw, by + 42),
               (bx + 178, by + 26)], fill=(24, 34, 58))
    # lit windows
    for row in range(3):
        for col in range(5):
            wx = bx + 14 + col * 38
            wy = by + 14 + row * 30
            lit = (row, col) not in [(0, 4), (0, 3)]
            d.rectangle([wx, wy, wx + 18, wy + 16],
                        fill=(255, 214, 120) if lit else (40, 38, 34))
    # fire glow at the damaged corner
    d.ellipse([bx + 158, by - 6, bx + 208, by + 34], fill=(255, 120, 30))
    d.ellipse([bx + 170, by + 2, bx + 196, by + 26], fill=(255, 200, 60))
    # smoke
    d.ellipse([bx + 150, by - 34, bx + 190, by - 6], fill=(120, 120, 115))
    d.ellipse([bx + 180, by - 48, bx + 214, by - 18], fill=(100, 100, 98))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(18, 26, 44))


def scene_gaza(d, x, y, w, h):
    """City skyline at dusk with an explosion burst."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 178, 110))
    d.rectangle([x, y + h - 60, x + w, y + h], fill=(120, 96, 78))
    # skyline blocks
    for bx, bw, bh in [(x + 8, 60, 70), (x + 76, 46, 96),
                       (x + 130, 70, 58), (x + 208, 52, 84),
                       (x + 268, 40, 64)]:
        d.rectangle([bx, y + h - 60 - bh, bx + bw, y + h - 60],
                    fill=(88, 70, 58))
    # explosion burst
    cx, cy = x + 160, y + 62
    for r, col in [(52, (255, 120, 20)), (38, (255, 170, 40)),
                   (24, (255, 225, 120))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    # smoke column (kept inside the scene frame)
    d.ellipse([cx - 26, cy - 56, cx + 6, cy - 26], fill=(90, 80, 74))
    d.ellipse([cx - 6, cy - 60, cx + 30, cy - 34], fill=(70, 62, 58))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(88, 70, 58))


def scene_korea(d, x, y, w, h):
    """Blue sky, two jets, island and sea below, warning triangle."""
    d.rectangle([x, y, x + w, y + h], fill=(158, 198, 232))
    for cx, cy in [(x + 60, y + 30), (x + 250, y + 22), (x + 200, y + 52)]:
        d.ellipse([cx, cy, cx + 34, cy + 10], fill=(255, 255, 255))
    # sea
    d.rectangle([x, y + 118, x + w, y + h], fill=(38, 96, 150))
    d.rectangle([x, y + 118, x + w, y + 122], fill=(220, 235, 245))
    # island
    d.polygon([(x + 40, y + 130), (x + 110, y + 96), (x + 190, y + 96),
               (x + 250, y + 130)], fill=(52, 110, 70))
    d.rectangle([x + 118, y + 78, x + 122, y + 96], fill=(90, 70, 50))
    # jets: simple swept-wing silhouettes
    for jx, jy in [(x + 70, y + 46), (x + 190, y + 66)]:
        d.polygon([(jx, jy), (jx + 46, jy + 8), (jx, jy + 12),
                   (jx + 10, jy + 6)], fill=(40, 44, 52))
        d.polygon([(jx + 30, jy + 2), (jx + 40, jy + 8), (jx + 34, jy + 10)],
                  fill=(40, 44, 52))
    # warning triangle
    tx, ty = x + w - 52, y + h - 44
    d.polygon([(tx + 18, ty), (tx + 36, ty + 32), (tx, ty + 32)],
              fill=(255, 200, 0), outline=(150, 30, 30), width=2)
    d.text((tx + 15, ty + 12), "!", font=font(SANS_BOLD, 18),
           fill=(150, 30, 30))


def scene_spacex(d, x, y, w, h):
    """Courthouse pediment and columns beside a rocket."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 222, 232))
    # courthouse
    cx0, cy0 = x + 16, y + 52
    d.polygon([(cx0, cy0), (cx0 + 150, cy0), (cx0 + 75, cy0 - 34)],
              fill=(240, 240, 236))
    d.rectangle([cx0, cy0, cx0 + 150, cy0 + 10], fill=(120, 118, 112))
    for i in range(4):
        px = cx0 + 12 + i * 38
        d.rectangle([px, cy0 + 10, px + 16, cy0 + 92], fill=(245, 245, 240))
    d.rectangle([cx0, cy0 + 92, cx0 + 150, cy0 + 104], fill=(120, 118, 112))
    # rocket
    rx = x + 218
    d.rectangle([rx, y + 30, rx + 34, y + 128], fill=(235, 235, 230),
                outline=(120, 120, 118), width=2)
    d.polygon([(rx, y + 30), (rx + 17, y + 6), (rx + 34, y + 30)],
              fill=(164, 30, 34))
    d.rectangle([rx + 4, y + 62, rx + 12, y + 72], fill=(31, 58, 95))
    d.polygon([(rx, y + 128), (rx - 12, y + 148), (rx, y + 140)],
              fill=(164, 30, 34))
    d.polygon([(rx + 34, y + 128), (rx + 46, y + 148), (rx + 34, y + 140)],
              fill=(164, 30, 34))
    d.polygon([(rx + 12, y + 128), (rx + 22, y + 128), (rx + 17, y + 152)],
              fill=(255, 160, 40))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(120, 118, 112))


def scene_cartagena(d, x, y, w, h):
    """Supermarket storefront with striped awning and glass doors."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 226, 196))
    # shop wall
    d.rectangle([x + 14, y + 30, x + w - 14, y + h - 20], fill=(250, 246, 236),
                outline=(150, 140, 120), width=2)
    # striped awning
    ax0, ay0, aw = x + 14, y + 30, w - 28
    for i in range(8):
        col = (164, 30, 34) if i % 2 == 0 else (250, 246, 236)
        d.rectangle([ax0 + i * aw // 8, ay0, ax0 + (i + 1) * aw // 8, ay0 + 26],
                    fill=col)
    d.rectangle([ax0, ay0 + 26, ax0 + aw, ay0 + 30], fill=(120, 30, 32))
    # glass doors
    d.rectangle([x + 96, y + 76, x + 168, y + h - 20], fill=(170, 205, 225),
                outline=(90, 90, 90), width=2)
    d.rectangle([x + 176, y + 76, x + 218, y + h - 20], fill=(150, 190, 215),
                outline=(90, 90, 90), width=2)
    d.line([x + 132, y + 76, x + 132, y + h - 20], fill=(90, 90, 90), width=2)
    # windows either side
    d.rectangle([x + 30, y + 76, x + 84, y + 120], fill=(170, 205, 225),
                outline=(90, 90, 90), width=2)
    d.rectangle([x + 232, y + 76, x + 286, y + 120], fill=(170, 205, 225),
                outline=(90, 90, 90), width=2)
    # police tape line across the doors
    d.rectangle([x + 14, y + 128, x + w - 14, y + 142], fill=(255, 210, 0))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(120, 112, 100))


def scene_ituri(d, x, y, w, h):
    """Hospital building with a red cross, hills, dust cloud."""
    d.rectangle([x, y, x + w, y + h], fill=(190, 220, 190))
    # hills
    d.ellipse([x - 40, y + 96, x + 140, y + h + 30], fill=(110, 160, 100))
    d.ellipse([x + 150, y + 106, x + w + 40, y + h + 30], fill=(90, 140, 88))
    # hospital building
    hx, hy = x + 78, y + 52
    d.rectangle([hx, hy, hx + 160, y + h - 24], fill=(245, 245, 240),
                outline=(140, 140, 134), width=2)
    d.rectangle([hx, hy, hx + 160, hy + 14], fill=(31, 58, 95))
    # red cross sign
    cx, cy = hx + 80, hy + 44
    d.rectangle([cx - 8, cy - 20, cx + 8, cy + 20], fill=(200, 30, 30))
    d.rectangle([cx - 20, cy - 8, cx + 20, cy + 8], fill=(200, 30, 30))
    # windows
    for i in range(3):
        d.rectangle([hx + 20 + i * 48, hy + 78, hx + 44 + i * 48, hy + 100],
                    fill=(150, 190, 215), outline=(90, 90, 90), width=1)
    # dust / smoke cloud from fighting at the right
    d.ellipse([x + 236, y + 40, x + 292, y + 88], fill=(200, 180, 140))
    d.ellipse([x + 258, y + 22, x + 306, y + 66], fill=(180, 160, 122))
    # two figures taking cover (simple crouched shapes)
    for fx in (x + 34, x + 56):
        d.ellipse([fx, y + 132, fx + 14, y + 146], fill=(40, 44, 52))
        d.ellipse([fx - 4, y + 144, fx + 18, y + 158], fill=(60, 70, 90))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(90, 140, 88))


# ---------------------------------------------------------------- page
PANELS = [
    ("DEADLY STRIKE HITS ZAPORIZHZHIA",
     "Russian strike on flats kills 2, wounds 40, including 4 children.",
     scene_zaporizhzhia),
    ("HAMAS SECURITY CHIEF KILLED IN GAZA",
     "Israeli strike in Gaza City kills Naeem Abu Nahel and six others.",
     scene_gaza),
    ("RUSSIAN JETS ENTER S. KOREA ZONE",
     "Residents of Ulleung island briefly told to take shelter.",
     scene_korea),
    ("STATES SUE SPACEX OVER GROK IMAGES",
     "Oregon and Virginia sue over sexual images made by Grok.",
     scene_spacex),
    ("25 HOSTAGES SEIZED IN CARTAGENA",
     "Gunmen take 25 hostages at a supermarket in Colombia.",
     scene_cartagena),
    ("EBOLA TEAMS TRAPPED BY FIGHTING",
     "Heavy fighting near a hospital in Ituri, DR Congo, forces teams to take cover.",
     scene_ituri),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    title = "THE WORLD IN ONE IMAGE"
    tf = font(SERIF_BOLD, 56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 26), title, font=tf, fill=NAVY)
    d.line([24, 102, W - 24, 102], fill=INK, width=3)
    d.line([24, 108, W - 24, 108], fill=INK, width=1)

    # Date, large and prominent
    date = "Tuesday 24 November 2026"
    df = font(SANS_BOLD, 40)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 120), date, font=df, fill=RED)
    d.line([24, 172, W - 24, 172], fill=INK, width=2)

    # Grid: 3 x 2, panels 317 x 408
    px = [24, 353, 682]
    py = [186, 606]
    pw, ph = 317, 408
    scene_h = 172
    for i, (headline, caption, scene_fn) in enumerate(PANELS):
        x = px[i % 3]
        y = py[i // 3]
        d.rectangle([x, y, x + pw, y + ph], fill=WHITE,
                    outline=(120, 116, 108), width=2)
        # Draw the scene on its own canvas so nothing can spill past
        # the scene rectangle into the headline area or a neighbour panel.
        scene_img = Image.new("RGB", (pw - 4, scene_h), WHITE)
        scene_d = ImageDraw.Draw(scene_img)
        scene_fn(scene_d, 0, 0, pw - 4, scene_h)
        img.paste(scene_img, (x + 2, y + 2))
        tx = x + 14
        max_w = pw - 28
        hf = font(SANS_BOLD, 23)
        hl_h = text_block_height(d, headline, hf, max_w, 29)
        assert hl_h <= 87, f"headline too tall: {headline}"
        cy = draw_wrapped(d, headline, hf, tx, y + scene_h + 14, max_w, 29)
        cf = font(SANS, 17)
        cap_h = text_block_height(d, caption, cf, max_w, 22)
        assert cy + cap_h <= y + ph - 12, f"caption overflows: {caption}"
        draw_wrapped(d, caption, cf, tx, cy + 8, max_w, 22, fill=(60, 58, 52))

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    build()
    print("wrote entry.png")
