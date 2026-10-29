#!/usr/bin/env python3
"""Render the CARD: shots in scenes.json as 1920x1080 PNGs with real Devanagari type.

Card prompts look like "rule — नियम ४: text", "title — text" or "end — text".
Rules: the "नियम N" label in the warning red, the rule below it in off-white.
Run from the toolkit root: uv run projects/belghati-halt/make_cards.py
"""
import json
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).parent
W, H = 1920, 1080
FONT = "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Bold.ttf"
PAL = json.load(open(HERE / "config.json"))["palette"]


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, layout_engine=ImageFont.Layout.RAQM)


def wrap(draw: ImageDraw.ImageDraw, text: str, f, max_w: int) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def background(seed: int) -> Image.Image:
    """Near-black paper with a faint red glow and film grain."""
    rnd = random.Random(seed)
    img = Image.new("RGB", (W, H), PAL["ink"])
    glow = Image.new("RGB", (W, H), PAL["ink"])
    ImageDraw.Draw(glow).ellipse((W * 0.15, H * 0.1, W * 0.85, H * 0.95), fill=PAL["accent1"])
    img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(260)), 0.35)
    px = img.load()
    for _ in range(W * H // 12):
        x, y = rnd.randrange(W), rnd.randrange(H)
        r, g, b = px[x, y]
        d = rnd.randint(-14, 14)
        px[x, y] = (max(0, min(255, r + d)), max(0, min(255, g + d)), max(0, min(255, b + d)))
    return img


def centered(draw, lines, f, y, fill, gap=1.25):
    lh = f.size * gap
    for line in lines:
        w = draw.textlength(line, font=f)
        draw.text(((W - w) / 2, y), line, font=f, fill=fill)
        y += lh
    return y


def card(kind: str, text: str, seed: int) -> Image.Image:
    img = background(seed)
    d = ImageDraw.Draw(img)
    if kind == "rule" and ":" in text:
        label, rule = (s.strip() for s in text.split(":", 1))
        fl, fr = font(150), font(78)
        lines = wrap(d, rule, fr, 1720)
        total = fl.size * 1.3 + 40 + len(lines) * fr.size * 1.3
        y = (H - total) / 2
        y = centered(d, [label], fl, y, PAL["warn"], 1.3) + 40
        d.line((W / 2 - 120, y - 25, W / 2 + 120, y - 25), fill=PAL["slate"], width=3)
        centered(d, lines, fr, y, PAL["white"], 1.3)
    else:
        f = font(130 if kind == "title" else 110)
        lines = wrap(d, text, f, 1600)
        y = (H - len(lines) * f.size * 1.3) / 2
        centered(d, lines, f, y, PAL["white"] if kind == "title" else PAL["warn"], 1.3)
    return img


def main() -> None:
    scenes = json.load(open(HERE / "scenes.json"))["scenes"]
    n = 0
    for s in scenes:
        assets = s["asset"] if isinstance(s["asset"], list) else [s["asset"]]
        for path, shot in zip(assets, s["shots"]):
            if shot["kind"] != "card":
                continue
            kind, _, text = shot["prompt"].partition(" — ")
            out = HERE / path
            out.parent.mkdir(parents=True, exist_ok=True)
            card(kind.strip(), text.strip(), int(s["id"])).save(out)
            n += 1
            print(out.name)
    print(f"{n} cards")


if __name__ == "__main__":
    main()
