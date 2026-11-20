import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1024, 1024
canvas = Image.new("RGBA", (W, H))
draw = ImageDraw.Draw(canvas)

# Gradient stops: (position, RGB)
stops = [
    (0.0, (43, 16, 85)),
    (0.42, (214, 36, 159)),
    (0.72, (255, 140, 66)),
    (1.0, (255, 209, 102)),
]

def interpolate_color(t, stops):
    if t <= stops[0][0]:
        return stops[0][1]
    if t >= stops[-1][0]:
        return stops[-1][1]
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        if p0 <= t <= p1:
            factor = (t - p0) / (p1 - p0)
            r = int(round(c0[0] + factor * (c1[0] - c0[0])))
            g = int(round(c0[1] + factor * (c1[1] - c0[1])))
            b = int(round(c0[2] + factor * (c1[2] - c0[2])))
            return (r, g, b, 255)
    return (*stops[-1][1], 255)

# Draw vertical sunset gradient
for y in range(H):
    t = y / (H - 1)
    color = interpolate_color(t, stops)
    draw.line([(0, y), (W, y)], fill=color)

# Soft sun
sun_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sun_draw = ImageDraw.Draw(sun_layer)
sun_draw.ellipse([W // 2 - 140, 330, W // 2 + 140, 610], fill=(255, 236, 179, 220))
sun_layer = sun_layer.filter(ImageFilter.GaussianBlur(3))
canvas.paste(sun_layer, (0, 0), sun_layer)

# Fonts
FONTS_DIR = "C:/Windows/Fonts"

def get_font(filename, size):
    full_path = os.path.join(FONTS_DIR, filename)
    if os.path.exists(full_path):
        return ImageFont.truetype(full_path, size)
    try:
        return ImageFont.truetype(filename, size)
    except Exception:
        return ImageFont.load_default()

font_headline = get_font("arialbd.ttf", 60)
font_header_title = get_font("arialbd.ttf", 42)
font_header_sub = get_font("arialbd.ttf", 22)
font_photo_lbl = get_font("consola.ttf", 19)
font_photo_sub = get_font("consola.ttf", 18)
font_field_label = get_font("consola.ttf", 20)
font_name = get_font("arialbd.ttf", 34)
font_dob = get_font("consolab.ttf", 28)
font_class = get_font("arialbd.ttf", 34)
font_issued = get_font("consolab.ttf", 28)
font_expires = get_font("arialbd.ttf", 30)
font_restrictions = get_font("arialbd.ttf", 27)
font_stamp_title = get_font("arialbd.ttf", 40)
font_stamp_mid = get_font("arial.ttf", 26)
font_stamp_sub = get_font("arialbd.ttf", 34)
font_footer_dmv = get_font("consola.ttf", 21)
font_footer_mf = get_font("arialbd.ttf", 26)

# Centered-text helper
def draw_centered_text(draw_obj, y, text, font, fill, stroke_width=0, stroke_fill=None):
    bbox = draw_obj.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    text_w = bbox[2] - bbox[0]
    x = (W - text_w) // 2
    draw_obj.text((x, y), text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)

# Headline centered at y=48
draw_centered_text(draw, 48, "13 YEARS. ONE LICENSE.", font_headline, "#ffffff", stroke_width=3, stroke_fill="#2b1055")

# License card coordinates
cx0, cy0, cx1, cy1 = 64, 158, 960, 902

# Drop shadow
shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow_layer)
shadow_draw.rounded_rectangle([cx0 + 10, cy0 + 14, cx1 + 10, cy1 + 14], radius=30, fill=(0, 0, 0, 120))
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(11))
canvas.paste(shadow_layer, (0, 0), shadow_layer)

# Card body
draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=30, fill="#f7f3e9", outline="#1a1a1a", width=5)

# Magenta header band
draw.rounded_rectangle([cx0, cy0, cx1, cy0 + 98], radius=30, fill="#d6249f")
draw.rectangle([cx0, cy0 + 52, cx1, cy0 + 98], fill="#d6249f")
# Preserve card outline
draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=30, outline="#1a1a1a", width=5)

# Header text
draw_centered_text(draw, cy0 + 16, "STATE OF LEONIDA", font_header_title, "#ffffff")
draw_centered_text(draw, cy0 + 62, "D R I V E R   L I C E N S E", font_header_sub, "#ffe3f3")

# Licensee photo box
px0, py0, px1, py1 = cx0 + 34, cy0 + 130, cx0 + 300, cy0 + 452
draw.rectangle([px0, py0, px1, py1], fill="#dfe6ee", outline="#1a1a1a", width=4)

if os.path.exists("assets/mark-1024.png"):
    photo = Image.open("assets/mark-1024.png").convert("RGBA")
    box_w = px1 - px0
    box_h = py1 - py0
    photo.thumbnail((box_w - 44, box_h - 44), Image.Resampling.LANCZOS)
    pw, ph = photo.size
    paste_x = px0 + (box_w - pw) // 2
    paste_y = py0 + (box_h - ph) // 2
    canvas.paste(photo, (paste_x, paste_y), photo)

# Under the photo
draw.text((px0 + 4, py1 + 8), "LICENSEE PHOTO", font=font_photo_lbl, fill="#555555")
draw.text((px0 + 4, py1 + 32), "VICE CITY · LEONIDA", font=font_photo_sub, fill="#555555")

# Data fields helper
fx = cx0 + 336
def draw_field(x, y, label, value, val_font, val_color="#1a1a1a"):
    draw.text((x, y), label, font=font_field_label, fill="#8a8a8a")
    draw.text((x, y + 24), value, font=val_font, fill=val_color)

draw_field(fx, cy0 + 128, "NAME", "EVERY GTA FAN", font_name, "#1a1a1a")
draw_field(fx, cy0 + 214, "DOB", "09 / 17 / 2013", font_dob, "#1a1a1a")
draw_field(fx + 252, cy0 + 214, "CLASS", "VI", font_class, "#d6249f")
draw_field(fx, cy0 + 296, "ISSUED", "11 / 19 / 2026", font_issued, "#1a1a1a")
draw_field(fx + 252, cy0 + 296, "EXPIRES", "NEVER", font_expires, "#c0392b")
draw_field(fx, cy0 + 380, "RESTRICTIONS", "13 YEARS OF PATIENCE", font_restrictions, "#1a1a1a")

# Rotated "PAID IN FULL" stamp
stamp = Image.new("RGBA", (470, 168), (0, 0, 0, 0))
s_draw = ImageDraw.Draw(stamp)
s_draw.rounded_rectangle([6, 6, 464, 162], radius=14, fill=(247, 243, 233, 255), outline=(214, 36, 159, 255), width=7)
s_draw.text((30, 26), "PAID IN FULL", font=font_stamp_title, fill=(214, 36, 159, 255))
s_draw.text((30, 80), "my AI agent earned it on", font=font_stamp_mid, fill=(150, 20, 110, 255))
s_draw.text((30, 114), "make.fun", font=font_stamp_sub, fill=(214, 36, 159, 255))

rotated_stamp = stamp.rotate(-9, expand=True, resample=Image.Resampling.BICUBIC)
canvas.paste(rotated_stamp, (cx1 - 512, cy1 - 306), rotated_stamp)

# Footer (strengthened contrast for enhanced print/screen legibility)
draw.text((cx0 + 40, cy1 - 70), "LEONIDA DMV  ·  GTA VI  ·  EST. 2013", font=font_footer_dmv, fill="#2a2a2a")
draw.text((cx0 + 40, cy1 - 44), "make.fun", font=font_footer_mf, fill="#b51a83")

# Save meme.png and print size
canvas.save("meme.png")
print(f"Saved meme.png ({canvas.width}x{canvas.height})")
