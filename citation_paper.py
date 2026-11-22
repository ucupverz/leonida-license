from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops


W, H = 1024, 1280
PAPER_W, PAPER_H = 900, 1210
MARGIN = 66
INK = (24, 23, 26)
GREY = (108, 104, 100)
RED = (176, 34, 30)
MAGENTA = (198, 26, 132)
ROOT = Path(__file__).resolve().parent


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def fitting_font(draw: ImageDraw.ImageDraw, text: str, name: str, start: int, max_width: int) -> ImageFont.FreeTypeFont:
    size = start
    while size > 16:
        candidate = font(name, size)
        if draw.textbbox((0, 0), text, font=candidate)[2] <= max_width:
            return candidate
        size -= 1
    candidate = font(name, 16)
    if draw.textbbox((0, 0), text, font=candidate)[2] > max_width:
        raise SystemExit(f"text does not fit at 16 px: {text}")
    return candidate


def tracked_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str,
                 face: ImageFont.FreeTypeFont, fill: tuple[int, ...], extra: int = 3) -> tuple[int, int, int, int]:
    x, y = xy
    start = x
    for char in text:
        draw.text((x, y), char, font=face, fill=fill)
        x += draw.textlength(char, font=face) + extra
    return (start, y, int(x - extra), y + face.size + 4)


def make_background() -> Image.Image:
    rng = np.random.default_rng()
    low = rng.normal(0, 1, (80, 64)).astype(np.float32)
    low = ((low - low.min()) / max(float(np.ptp(low)), 1e-6) * 255).astype(np.uint8)
    texture = Image.fromarray(low, "L").filter(ImageFilter.GaussianBlur(1.2)).resize((W, H), Image.Resampling.BICUBIC)
    noise = np.asarray(texture, dtype=np.float32) * 26.0 / 255.0
    base = np.empty((H, W, 3), dtype=np.float32)
    base[:] = (30, 28, 34)
    base += noise[:, :, None]
    yy, xx = np.mgrid[0:H, 0:W]
    for cx, cy, radius, color in ((60, 300, 620, (236, 62, 148)), (980, 1080, 560, (56, 190, 214))):
        dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        falloff = np.clip(1.0 - dist / radius, 0.0, 1.0) ** 2.4
        base += falloff[:, :, None] * np.asarray(color, dtype=np.float32) * 0.42
    bg = Image.fromarray(np.uint8(np.clip(base, 0, 255)), "RGB")

    spots = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(spots)
    random.seed()
    for _ in range(26):
        x, y = random.randrange(W), random.randrange(H)
        radius = random.randint(6, 22)
        sd.ellipse((x - radius, y - radius, x + radius, y + radius), fill=random.randint(100, 230))
    spots = spots.filter(ImageFilter.GaussianBlur(13))
    mask = np.asarray(spots, dtype=np.float32)[:, :, None] / 255.0 * 0.30
    mag = np.asarray((236, 62, 148), dtype=np.float32)
    cyan = np.asarray((56, 190, 214), dtype=np.float32)
    tint = 0.60 * mag + 0.40 * cyan
    arr = np.asarray(bg, dtype=np.float32) + mask * tint

    radial = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    vignette = np.clip(1.0 - 0.42 * np.minimum(radial ** 2 / 2.0, 1.0), 0.0, 1.0)
    arr *= vignette[:, :, None]
    return Image.fromarray(np.uint8(np.clip(arr, 0, 255)), "RGB")


def make_paper() -> Image.Image:
    rng = np.random.default_rng()
    yy, xx = np.mgrid[0:PAPER_H, 0:PAPER_W]
    gradient = (xx / (PAPER_W - 1) + yy / (PAPER_H - 1)) / 2.0
    grain = rng.normal(0.0, 3.0, (PAPER_H, PAPER_W, 1))
    arr = np.empty((PAPER_H, PAPER_W, 3), dtype=np.float32)
    arr[:] = (250, 247, 240)
    arr += grain
    arr += gradient[:, :, None] * np.asarray((9, 5, -4), dtype=np.float32)
    paper = Image.fromarray(np.uint8(np.clip(arr, 0, 255)), "RGB")
    draw = ImageDraw.Draw(paper)
    boxes: list[tuple[str, tuple[int, int, int, int]]] = []
    cursor = 42
    x0, x1 = MARGIN, PAPER_W - MARGIN
    inner = x1 - x0

    def record(name: str, box: tuple[int, int, int, int]) -> None:
        boxes.append((name, tuple(map(int, box))))

    def text(name: str, xy: tuple[int, int], value: str, face: ImageFont.FreeTypeFont,
             fill: tuple[int, ...] = INK, anchor: str | None = None) -> tuple[int, int, int, int]:
        draw.text(xy, value, font=face, fill=fill, anchor=anchor)
        bbox = draw.textbbox(xy, value, font=face, anchor=anchor)
        record(name, bbox)
        return bbox

    def rule(name: str, y: int, width: int) -> None:
        draw.rectangle((x0, y, x1, y + width - 1), fill=INK)
        record(name, (x0, y, x1, y + width))

    # Header row
    header_face = font("arial.ttf", 23)
    tracked = tracked_text(draw, (x0, cursor), "CITY OF VICE CITY", header_face, GREY)
    record("city header", tracked)
    form = "FORM 4-B"
    form_face = font("arial.ttf", 23)
    form_w = draw.textlength(form, font=form_face)
    text("form label", (x1 - form_w, cursor), form, form_face, GREY)
    cursor += 38

    rule("top rule", cursor, 3)
    cursor += 21

    title = "PARKING CITATION"
    title_face = fitting_font(draw, title, "arialbd.ttf", 60, inner)
    text("title", (x0, cursor), title, title_face)
    cursor += 78

    rule("title divider", cursor, 2)
    cursor += 22

    # Two aligned columns, one reserved block.
    col_gap = 34
    col_w = (inner - col_gap) // 2
    label_face = font("arial.ttf", 20)
    left_x, right_x = x0, x0 + col_w + col_gap
    text("issued label", (left_x, cursor), "ISSUED", label_face, GREY)
    text("location label", (right_x, cursor), "LOCATION", label_face, GREY)
    cursor += 30
    issued_face = fitting_font(draw, "17 SEP 2013", "arialbd.ttf", 44, col_w)
    location_face = fitting_font(draw, "OCEAN DRIVE", "arialbd.ttf", 44, col_w)
    text("issued value", (left_x, cursor), "17 SEP 2013", issued_face)
    text("location value", (right_x, cursor), "OCEAN DRIVE", location_face)
    cursor += 61

    text("vehicle label", (x0, cursor), "VEHICLE", label_face, GREY)
    cursor += 30
    vehicle = "WHITE INFERNUS · PLATE LUCIA-6"
    vehicle_face = fitting_font(draw, vehicle, "arialbd.ttf", 40, inner)
    text("vehicle value", (x0, cursor), vehicle, vehicle_face)
    cursor += 60

    rule("vehicle divider", cursor, 2)
    cursor += 20

    # Fee rows; dotted leaders are individual tracked rectangles.
    fee_face = font("consolab.ttf", 28)
    fee_rows = (("4,813 DAYS OVERTIME @ $0.25", "$1,203.25"),
                ("PENALTIES, FEES & STORAGE", "$822.75"))
    for idx, (description, price) in enumerate(fee_rows, start=1):
        desc_w = draw.textlength(description, font=fee_face)
        price_w = draw.textlength(price, font=fee_face)
        desc_x = x0
        price_x = x1 - price_w
        dots_start = int(desc_x + desc_w + 10)
        dots_end = int(price_x - 10)
        if dots_end - dots_start < 18:
            raise SystemExit(f"fee row {idx} has no room for dotted leader")
        text(f"fee {idx} description", (desc_x, cursor), description, fee_face)
        text(f"fee {idx} price", (price_x, cursor), price, fee_face)
        dot_y = cursor + 16
        for dx in range(dots_start, dots_end - 2, 9):
            draw.rectangle((dx, dot_y, dx + 2, dot_y + 2), fill=GREY)
            record(f"fee {idx} leader {dx}", (dx, dot_y, dx + 3, dot_y + 3))
        cursor += 43

    rule("total rule", cursor, 4)
    cursor += 19

    total_label_face = font("arial.ttf", 34)
    total_value = "$2,026.00"
    total_value_face = fitting_font(draw, total_value, "arialbd.ttf", 112, inner - 250)
    text("total due label", (x0, cursor + 20), "TOTAL DUE", total_label_face, GREY)
    total_w = draw.textlength(total_value, font=total_value_face)
    text("total due value", (x1 - total_w, cursor), total_value, total_value_face)
    cursor += 126

    # Red distressed stamp, centered across the sheet.
    stamp = Image.new("RGBA", (620, 146), (0, 0, 0, 0))
    stamp_draw = ImageDraw.Draw(stamp)
    stamp_draw.rounded_rectangle((4, 4, 616, 142), radius=14, outline=RED + (255,), width=6)
    stamp_draw.rounded_rectangle((15, 15, 605, 131), radius=9, outline=RED + (255,), width=3)
    stamp_text = "13 YEARS UNPAID"
    stamp_face = fitting_font(stamp_draw, stamp_text, "arialbd.ttf", 70, 560)
    stamp_bbox = stamp_draw.textbbox((0, 0), stamp_text, font=stamp_face)
    stamp_x = (620 - (stamp_bbox[2] - stamp_bbox[0])) // 2 - stamp_bbox[0]
    stamp_y = (146 - (stamp_bbox[3] - stamp_bbox[1])) // 2 - stamp_bbox[1]
    stamp_draw.text((stamp_x, stamp_y), stamp_text, font=stamp_face, fill=RED + (255,))
    stamp_arr = np.asarray(stamp).copy()
    alpha = stamp_arr[:, :, 3]
    distress = np.random.default_rng().random(alpha.shape) < 0.16
    factors = np.random.default_rng().uniform(0.05, 0.5, alpha.shape)
    alpha[distress] = (alpha[distress].astype(np.float32) * factors[distress]).astype(np.uint8)
    stamp_arr[:, :, 3] = alpha
    stamp = Image.fromarray(stamp_arr, "RGBA").rotate(-7, resample=Image.Resampling.BICUBIC, expand=True)
    stamp_x = (PAPER_W - stamp.width) // 2
    paper_rgba = paper.convert("RGBA")
    paper_rgba.alpha_composite(stamp, (stamp_x, cursor))
    record("rubber stamp", (stamp_x, cursor, stamp_x + stamp.width, cursor + stamp.height))
    cursor += stamp.height + 18

    punch = "THE CAR NEVER MOVED."
    punch_face = fitting_font(draw, punch, "arialbd.ttf", 72, inner)
    text("punchline", (x0, cursor), punch, punch_face)
    cursor += 86

    kicker = "PARKED THE DAY GTA V CAME OUT."
    kicker_face = fitting_font(draw, kicker, "arialbd.ttf", 34, inner)
    text("kicker", (x0, cursor), kicker, kicker_face, MAGENTA)
    cursor += 52

    rule("footer divider", cursor, 2)
    cursor += 18

    mark_path = ROOT / "assets" / "mark-1024.png"
    if not mark_path.is_file():
        raise SystemExit(f"required logo asset missing: {mark_path}")
    logo = Image.open(mark_path).convert("RGBA").resize((64, 64), Image.Resampling.LANCZOS)
    paper_rgba.alpha_composite(logo, (x0, cursor))
    record("ghost logo", (x0, cursor, x0 + 64, cursor + 64))
    footer_x = x0 + 80
    paid_face = font("arialbd.ttf", 27)
    settled_face = font("arial.ttf", 20)
    url_face = font("consola.ttf", 18)
    text("paid line", (footer_x, cursor + 2), "PAID BY MY AI AGENT", paid_face)
    text("settled line", (footer_x, cursor + 36), "settled with a bounty payout from make.fun", settled_face, GREY)
    text("bounty url", (x0, cursor + 73), "make.fun/bounty/gta6-meme-x-01", url_face, GREY)
    cursor += 103

    if cursor > PAPER_H - 30:
        raise SystemExit(f"content overflow: bottom {cursor} exceeds {PAPER_H - 30}")
    for i, (name_a, a) in enumerate(boxes):
        for name_b, b in boxes[i + 1:]:
            if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                raise SystemExit(f"layout collision: {name_a} overlaps {name_b}")
    return paper_rgba.convert("RGB")


def render() -> None:
    background = make_background()
    sheet = make_paper().rotate(-2.1, resample=Image.Resampling.BICUBIC, expand=True)
    scaled_size = (round(sheet.width * 1.14), round(sheet.height * 1.14))
    sheet = sheet.resize(scaled_size, Image.Resampling.LANCZOS)
    sheet = sheet.transform(
        sheet.size,
        Image.Transform.PERSPECTIVE,
        (1, 0, 0, 0, 1, 0, 0.00016, 0.000045),
        resample=Image.Resampling.BICUBIC,
    )
    left = (W - sheet.width) // 2
    top = (H - sheet.height) // 2 + 8
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle((left + 10, top + 18, left + sheet.width + 10, top + sheet.height + 18), fill=(0, 0, 0, 190))
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))
    background = Image.alpha_composite(background.convert("RGBA"), shadow)
    background.alpha_composite(sheet.convert("RGBA"), (left, top))
    image = background.convert("RGB")

    arr = np.asarray(image, dtype=np.float32)
    arr += np.random.default_rng().normal(0.0, 3.6, arr.shape)
    arr *= np.asarray((1.015, 1.0, 0.985), dtype=np.float32)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    red = np.roll(arr[:, :, 0], 2, axis=1).astype(np.float32) * 0.55 + arr[:, :, 0].astype(np.float32) * 0.45
    blue = np.roll(arr[:, :, 2], -2, axis=1).astype(np.float32) * 0.55 + arr[:, :, 2].astype(np.float32) * 0.45
    arr[:, :, 0] = np.clip(red, 0, 255).astype(np.uint8)
    arr[:, :, 2] = np.clip(blue, 0, 255).astype(np.uint8)
    image = Image.fromarray(arr, "RGB").filter(ImageFilter.GaussianBlur(0.4))
    image.save(ROOT / "meme.png", format="PNG")
    image.resize((410, 512), Image.Resampling.LANCZOS).save(ROOT / "meme_480.png", format="PNG")
    print(f"meme.png: {image.size[0]}x{image.size[1]}")
    print("meme_480.png: 410x512")


if __name__ == "__main__":
    render()
