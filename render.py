import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 1. Deterministic seed
random.seed(2026)

CANVAS_SIZE = 1024

# 2. Diagonal gradient background
# Deep purple (43,16,85) at top-left -> magenta (214,36,159) middle -> warm orange (255,140,66) bottom-right
c0 = (43, 16, 85)
c1 = (214, 36, 159)
c2 = (255, 140, 66)

lut = []
max_d = 2046.0
for d in range(2047):
    t = d / max_d
    if t <= 0.5:
        u = t / 0.5
        r = int(round((1.0 - u) * c0[0] + u * c1[0]))
        g = int(round((1.0 - u) * c0[1] + u * c1[1]))
        b = int(round((1.0 - u) * c0[2] + u * c1[2]))
    else:
        u = (t - 0.5) / 0.5
        r = int(round((1.0 - u) * c1[0] + u * c2[0]))
        g = int(round((1.0 - u) * c1[1] + u * c2[1]))
        b = int(round((1.0 - u) * c1[2] + u * c2[2]))
    lut.append(bytes([r, g, b]))

raw_bg = b"".join(lut[x + y] for y in range(CANVAS_SIZE) for x in range(CANVAS_SIZE))
canvas = Image.frombytes("RGB", (CANVAS_SIZE, CANVAS_SIZE), raw_bg)

# 3. Soft blurred dark drop shadow behind the card
card_box = [56, 40, 968, 984]
corner_radius = 26

shadow_layer = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow_layer)
shadow_offset_y = 12
shadow_draw.rounded_rectangle(
    [card_box[0] - 2, card_box[1] + shadow_offset_y, card_box[2] + 2, card_box[3] + shadow_offset_y],
    radius=corner_radius + 2,
    fill=(15, 5, 25, 120)
)
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=18))
canvas.paste(shadow_layer, (0, 0), shadow_layer)

# 4. Fonts from C:/Windows/Fonts
font_dmv = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 56)
font_receipt = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
font_class_lbl = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 14)
font_class_val = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 42)

font_queue_pill = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)
font_take_num = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 17)

font_date_lbl = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
font_date_val = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 24)

font_stamp_main = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 50)
font_stamp_sub = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)

font_check = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)

font_fee = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 24)

font_total_lbl = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 42)
font_total_val = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 62)

font_micro = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 17)
font_barcode_cap = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
font_clerk = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)

font_agent_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 28)
font_agent_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 19)
font_makefun_pill = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)

# 5. Build card surface (RGBA)
card_img = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
card_draw = ImageDraw.Draw(card_img)

# Cream paper fill: (255, 253, 247)
card_draw.rectangle([56, 40, 968, 984], fill=(255, 253, 247, 255))

# Header zone 1: Black bar (y 40..176), fill (20,20,20)
card_draw.rectangle([56, 40, 968, 176], fill=(20, 20, 20, 255))

# Queue zone 2: Magenta strip (y 176..228), fill (214,33,156)
card_draw.rectangle([56, 176, 968, 228], fill=(214, 33, 156, 255))

# Footer zone 4: Magenta footer band (y 852..984), fill (214,33,156)
card_draw.rectangle([56, 852, 968, 984], fill=(214, 33, 156, 255))

# --- HEADER BAR CONTENT ---
# Left ID-card icon
icon_x = 82
icon_y = 66
icon_w = 52
icon_h = 36
card_draw.rounded_rectangle(
    [icon_x, icon_y, icon_x + icon_w, icon_y + icon_h],
    radius=5,
    outline=(255, 255, 255, 255),
    width=2
)
# Mini photo box on left of ID card
card_draw.rectangle([icon_x + 5, icon_y + 5, icon_x + 17, icon_y + 23], outline=(200, 200, 200, 255), width=1)
card_draw.ellipse([icon_x + 8, icon_y + 8, icon_x + 14, icon_y + 14], fill=(255, 255, 255, 255))
card_draw.pieslice([icon_x + 6, icon_y + 14, icon_x + 16, icon_y + 23], 180, 360, fill=(255, 255, 255, 255))

# Text lines on right of ID card (one gold)
card_draw.line([(icon_x + 22, icon_y + 9), (icon_x + 44, icon_y + 9)], fill=(255, 209, 102, 255), width=2)
card_draw.line([(icon_x + 22, icon_y + 15), (icon_x + 42, icon_y + 15)], fill=(255, 255, 255, 255), width=2)
card_draw.line([(icon_x + 22, icon_y + 21), (icon_x + 38, icon_y + 21)], fill=(255, 255, 255, 255), width=2)
card_draw.line([(icon_x + 5, icon_y + 29), (icon_x + 44, icon_y + 29)], fill=(160, 160, 160, 255), width=2)

# Title: "LEONIDA DMV"
card_draw.text((150, 52), "LEONIDA DMV", font=font_dmv, fill=(255, 255, 255, 255))

# Subtitle: "LICENSE RENEWAL RECEIPT" in gold (255,209,102), letter-spaced ~3px
cur_sub_x = 152
sub_text = "LICENSE RENEWAL RECEIPT"
for ch in sub_text:
    card_draw.text((cur_sub_x, 126), ch, font=font_receipt, fill=(255, 209, 102, 255))
    bb = card_draw.textbbox((0, 0), ch, font=font_receipt)
    cur_sub_x += (bb[2] - bb[0]) + 3

# Right side: CLASS label above V → VI
class_val_text = "V → VI"
val_bbox = card_draw.textbbox((0, 0), class_val_text, font=font_class_val)
val_w = val_bbox[2] - val_bbox[0]
val_x = 924 - val_w
val_y = 86
card_draw.text((val_x, val_y), class_val_text, font=font_class_val, fill=(255, 255, 255, 255))

lbl_bbox = card_draw.textbbox((0, 0), "CLASS", font=font_class_lbl)
lbl_w = lbl_bbox[2] - lbl_bbox[0]
lbl_x = 924 - lbl_w
lbl_y = 66
card_draw.text((lbl_x, lbl_y), "CLASS", font=font_class_lbl, fill=(180, 180, 185, 255))

# --- QUEUE STRIP CONTENT ---
# Left: white rounded pill containing "NOW SERVING #2013" in magenta bold ~18px
pill_text = "NOW SERVING #2013"
pt_bbox = card_draw.textbbox((0, 0), pill_text, font=font_queue_pill)
pt_w = pt_bbox[2] - pt_bbox[0]
pt_h = pt_bbox[3] - pt_bbox[1]
pill_pad_x = 18
pill_w = pt_w + pill_pad_x * 2
pill_h = 36
pill_x = 88
pill_y = 176 + (52 - pill_h) // 2
card_draw.rounded_rectangle(
    [pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
    radius=pill_h // 2,
    fill=(255, 255, 255, 255)
)
card_draw.text(
    (pill_x + pill_pad_x, pill_y + (pill_h - pt_h) // 2 - pt_bbox[1]),
    pill_text,
    font=font_queue_pill,
    fill=(214, 33, 156, 255)
)

# Right: "TAKE A NUMBER" in white bold ~17px, letter-spaced ~2px
take_text = "TAKE A NUMBER"
tn_widths = []
for ch in take_text:
    bb = card_draw.textbbox((0, 0), ch, font=font_take_num)
    tn_widths.append(bb[2] - bb[0])
total_tn_w = sum(tn_widths) + (len(take_text) - 1) * 2
cur_tn_x = 924 - total_tn_w
tn_y = 176 + (52 - 17) // 2
for i, ch in enumerate(take_text):
    card_draw.text((cur_tn_x, tn_y), ch, font=font_take_num, fill=(255, 255, 255, 255))
    cur_tn_x += tn_widths[i] + 2

# --- WHITE PAPER BODY (y 228..852) ---
# Date blocks on left half
# SUBMITTED label + LOS SANTOS · SEP 17, 2013
cur_sub_lbl_x = 88
for ch in "SUBMITTED":
    card_draw.text((cur_sub_lbl_x, 246), ch, font=font_date_lbl, fill=(88, 88, 92, 255))
    bb = card_draw.textbbox((0, 0), ch, font=font_date_lbl)
    cur_sub_lbl_x += (bb[2] - bb[0]) + 3

card_draw.text((88, 268), "LOS SANTOS · SEP 17, 2013", font=font_date_val, fill=(18, 18, 20, 255))

# PROCESSED label + VICE CITY · NOV 19, 2026
cur_proc_lbl_x = 88
for ch in "PROCESSED":
    card_draw.text((cur_proc_lbl_x, 304), ch, font=font_date_lbl, fill=(88, 88, 92, 255))
    bb = card_draw.textbbox((0, 0), ch, font=font_date_lbl)
    cur_proc_lbl_x += (bb[2] - bb[0]) + 3

card_draw.text((88, 326), "VICE CITY · NOV 19, 2026", font=font_date_val, fill=(18, 18, 20, 255))

# Red rubber stamp on upper-RIGHT
stamp_w, stamp_h = 390, 118
stamp_img = Image.new("RGBA", (stamp_w, stamp_h), (0, 0, 0, 0))
sdraw = ImageDraw.Draw(stamp_img)

# Double border in red (226,59,46)
sdraw.rounded_rectangle([4, 4, stamp_w - 4, stamp_h - 4], radius=14, outline=(226, 59, 46, 255), width=4)
sdraw.rounded_rectangle([12, 12, stamp_w - 12, stamp_h - 12], radius=10, outline=(226, 59, 46, 255), width=2)

st_main = "13 YEARS LATE"
bb_m = sdraw.textbbox((0, 0), st_main, font=font_stamp_main)
sdraw.text(((stamp_w - (bb_m[2] - bb_m[0])) // 2, 16), st_main, font=font_stamp_main, fill=(226, 59, 46, 255))

st_sub = "4,811 DAYS IN QUEUE"
bb_s = sdraw.textbbox((0, 0), st_sub, font=font_stamp_sub)
sdraw.text(((stamp_w - (bb_s[2] - bb_s[0])) // 2, 74), st_sub, font=font_stamp_sub, fill=(226, 59, 46, 255))

# Light distressed texture
stamp_pixels = stamp_img.load()
for sy in range(stamp_h):
    for sx in range(stamp_w):
        r, g, b, a = stamp_pixels[sx, sy]
        if a > 0:
            rnd = random.random()
            if rnd < 0.05:
                stamp_pixels[sx, sy] = (r, g, b, 0)
            elif rnd < 0.12:
                stamp_pixels[sx, sy] = (r, g, b, int(a * random.uniform(0.2, 0.6)))

# Rotate about -8 degrees
rotated_stamp = stamp_img.rotate(-8, resample=Image.Resampling.BICUBIC, expand=True)
card_img.paste(rotated_stamp, (530, 236), rotated_stamp)

# Checkbox row below dates (y ~ 372)
card_draw.text((88, 372), "FILED AS:", font=font_check, fill=(88, 88, 92, 255))

# Empty box labeled "ON TIME"
card_draw.rounded_rectangle([186, 372, 206, 392], radius=3, outline=(88, 88, 92, 255), width=2)
card_draw.text((214, 372), "ON TIME", font=font_check, fill=(88, 88, 92, 255))

# Checked box labeled "LATE RETURN" in red (226,59,46)
card_draw.rounded_rectangle([320, 372, 340, 392], radius=3, outline=(226, 59, 46, 255), width=2)
# Draw thick red checkmark
card_draw.line([(323, 381), (328, 388), (338, 371)], fill=(226, 59, 46, 255), width=3)
card_draw.text((348, 372), "LATE RETURN", font=font_check, fill=(226, 59, 46, 255))

# Thin light divider line
card_draw.line([(88, 408), (924, 408)], fill=(220, 220, 224, 255), width=1)

# SIX itemized fee lines
fee_items = [
    ("Late renewal \u2014 13 years @ $100/yr", "$1,300"),
    ("Two delays: Fall 2025, May 2026", "$52"),
    ("Road test: in line since 2013", "$213"),
    ("Photo retake: subject aged 13 yrs", "$137"),
    ("Class upgrade: V \u2192 VI", "$224"),
    ("Address: Los Santos \u2192 Vice City", "$100")
]

fee_start_y = 428
line_spacing = 40
for idx, (desc, price) in enumerate(fee_items):
    y = fee_start_y + idx * line_spacing
    desc_bbox = card_draw.textbbox((88, y), desc, font=font_fee)
    price_bbox = card_draw.textbbox((0, 0), price, font=font_fee)
    price_w = price_bbox[2] - price_bbox[0]
    price_x = 924 - price_w

    card_draw.text((88, y), desc, font=font_fee, fill=(18, 18, 20, 255))
    card_draw.text((price_x, y), price, font=font_fee, fill=(18, 18, 20, 255))

    # Dotted leaders: 2px squares every 8px
    dot_start = desc_bbox[2] + 10
    dot_end = price_x - 10
    dot_y = y + 15
    for dx in range(dot_start, dot_end, 8):
        card_draw.rectangle([dx, dot_y, dx + 2, dot_y + 2], fill=(18, 18, 20, 255))

# Magenta horizontal rule (~4px thick)
card_draw.line([(88, 674), (924, 674)], fill=(214, 33, 156, 255), width=4)

# TOTAL DUE and $2,026
card_draw.text((88, 692), "TOTAL DUE", font=font_total_lbl, fill=(27, 42, 74, 255))

tot_bbox = card_draw.textbbox((0, 0), "$2,026", font=font_total_val)
tot_w = tot_bbox[2] - tot_bbox[0]
tot_x = 924 - tot_w
card_draw.text((tot_x, 678), "$2,026", font=font_total_val, fill=(214, 33, 156, 255))

# Microprint line
micro_text = "Form VI-13 \u00b7 examiners Jason & Lucia \u00b7 214 GB download \u00b7 no refunds \u00b7 PC version pending"
mp_bbox = card_draw.textbbox((0, 0), micro_text, font=font_micro)
mp_w = mp_bbox[2] - mp_bbox[0]
card_draw.text(((CANVAS_SIZE - mp_w) // 2, 756), micro_text, font=font_micro, fill=(70, 70, 74, 255))

# Barcode at lower-left
bc_x = 88
bc_y = 786
bc_h = 36
bar_widths = [3, 2, 1, 2, 4, 1, 2, 3, 1, 2, 4, 2, 1, 3, 2, 1, 4, 2, 2, 1, 3, 2, 1, 3, 4, 1, 2, 3, 1, 2, 4, 1, 2, 3, 2, 1, 4, 2, 1, 3, 2, 1, 3, 2, 4, 1, 2, 3, 1, 4, 2, 1, 3, 2]
cur_bc_x = bc_x
for b_idx, bw in enumerate(bar_widths):
    if b_idx % 2 == 0:
        card_draw.rectangle([cur_bc_x, bc_y, cur_bc_x + bw, bc_y + bc_h], fill=(18, 18, 20, 255))
    cur_bc_x += bw

card_draw.text((88, 828), "* 2013-2026-LEONIDA-DMV-VI *", font=font_barcode_cap, fill=(70, 70, 74, 255))

# Signature line at lower-right
sig_x1 = 700
sig_x2 = 924
sig_y = 824
card_draw.line([(sig_x1, sig_y), (sig_x2, sig_y)], fill=(160, 160, 165, 255), width=2)

# Hand-drawn navy scrawl
sig_points = [
    (710, 814), (722, 794), (728, 818), (738, 802),
    (752, 816), (766, 792), (778, 820), (792, 806),
    (812, 816), (826, 796), (842, 818), (866, 804),
    (892, 816), (918, 808)
]
card_draw.line(sig_points, fill=(27, 42, 74, 255), width=2, joint="curve")
card_draw.arc([712, 790, 736, 814], 180, 360, fill=(27, 42, 74, 255), width=2)

card_draw.text((sig_x1, 828), "Clerk: make.fun agent", font=font_clerk, fill=(70, 70, 74, 255))

# --- FOOTER BAND (y 852..984) ---
# Left: ghost mascot
ghost_path = "assets/mark-1024.png"
if os.path.exists(ghost_path):
    ghost = Image.open(ghost_path).convert("RGBA")
    ghost = ghost.resize((96, 96), Image.Resampling.LANCZOS)
    card_img.paste(ghost, (80, 870), ghost)

card_draw.text((192, 880), "PAID BY MY AI AGENT", font=font_agent_title, fill=(255, 255, 255, 255))
card_draw.text((192, 920), "with a bounty payout it earned on", font=font_agent_sub, fill=(255, 255, 255, 255))

# Right: make.fun pill
mf_pill_w = 160
mf_pill_h = 48
mf_pill_x = 924 - mf_pill_w
mf_pill_y = 892
card_draw.rounded_rectangle(
    [mf_pill_x, mf_pill_y, mf_pill_x + mf_pill_w, mf_pill_y + mf_pill_h],
    radius=mf_pill_h // 2,
    fill=(255, 255, 255, 255)
)
mf_text = "make.fun"
mf_bb = card_draw.textbbox((0, 0), mf_text, font=font_makefun_pill)
mf_w = mf_bb[2] - mf_bb[0]
mf_h = mf_bb[3] - mf_bb[1]
card_draw.text(
    (mf_pill_x + (mf_pill_w - mf_w) // 2, mf_pill_y + (mf_pill_h - mf_h) // 2 - mf_bb[1]),
    mf_text,
    font=font_makefun_pill,
    fill=(214, 33, 156, 255)
)

# 6. Rounded mask composite over gradient
mask = Image.new("L", (CANVAS_SIZE, CANVAS_SIZE), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.rounded_rectangle(card_box, radius=corner_radius, fill=255)

canvas.paste(card_img, (0, 0), mask)

# 7. Save outputs
output_path = "meme.png"
canvas.save(output_path, "PNG")

output_480_path = "meme_480.png"
img_480 = canvas.resize((480, 480), Image.Resampling.LANCZOS)
img_480.save(output_480_path, "PNG")

print(f"Successfully generated {output_path} (1024x1024) and {output_480_path} (480x480).")
