import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Set deterministic random seed
random.seed(2026)

WIDTH, HEIGHT = 1024, 1024

# Palette
C_DEEP_PURPLE = (43, 16, 85)
C_MID_MAGENTA = (214, 36, 159)
C_ORANGE = (255, 140, 66)

C_CARD_BG = (255, 253, 247)      # #FFFDF7
C_HEADER_BLACK = (20, 20, 20)    # #141414
C_MAGENTA = (214, 33, 156)       # #D6219C
C_GOLD = (255, 209, 102)         # #FFD166
C_RED_STAMP = (226, 59, 46)      # #E23B2E
C_NAVY = (27, 42, 74)            # #1B2A4A
C_GRAY_LABEL = (138, 138, 138)   # #8A8A8A
C_BODY_DARK = (18, 18, 20)
C_WHITE = (255, 255, 255)

FONT_DIR = "C:/Windows/Fonts"
f_header_title = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 55)
f_header_sub = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 21)
f_class_lbl = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 13)
f_class_val = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 40)

f_pill_serving = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 15)
f_take_number = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 14)

f_microcap = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 12)
f_date_val = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 21)
f_checkbox = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 14)

f_stamp_main = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 46)
f_stamp_sub = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 19)

f_fee_text = ImageFont.truetype(f"{FONT_DIR}/consolab.ttf", 22)
f_fee_price = ImageFont.truetype(f"{FONT_DIR}/consolab.ttf", 22)

f_total_lbl = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 40)
f_total_val = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 54)

f_microprint = ImageFont.truetype(f"{FONT_DIR}/consola.ttf", 13)
f_barcode_sub = ImageFont.truetype(f"{FONT_DIR}/consola.ttf", 11)
f_clerk = ImageFont.truetype(f"{FONT_DIR}/arial.ttf", 13)

f_footer_h = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 26)
f_footer_p = ImageFont.truetype(f"{FONT_DIR}/arial.ttf", 17)
f_pill_brand = ImageFont.truetype(f"{FONT_DIR}/arialbd.ttf", 24)

def draw_letterspaced(draw, pos, text, font, fill, spacing=2):
    x, y = pos
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        bbox = font.getbbox(char)
        char_w = (bbox[2] - bbox[0]) if bbox else 8
        x += char_w + spacing

def make_background():
    max_s = (WIDTH - 1) + (HEIGHT - 1)
    lut = []
    for s in range(max_s + 1):
        t = s / max_s
        if t <= 0.5:
            r = t / 0.5
            cr = int(round(C_DEEP_PURPLE[0] + (C_MID_MAGENTA[0] - C_DEEP_PURPLE[0]) * r))
            cg = int(round(C_DEEP_PURPLE[1] + (C_MID_MAGENTA[1] - C_DEEP_PURPLE[1]) * r))
            cb = int(round(C_DEEP_PURPLE[2] + (C_MID_MAGENTA[2] - C_DEEP_PURPLE[2]) * r))
        else:
            r = (t - 0.5) / 0.5
            cr = int(round(C_MID_MAGENTA[0] + (C_ORANGE[0] - C_MID_MAGENTA[0]) * r))
            cg = int(round(C_MID_MAGENTA[1] + (C_ORANGE[1] - C_MID_MAGENTA[1]) * r))
            cb = int(round(C_MID_MAGENTA[2] + (C_ORANGE[2] - C_MID_MAGENTA[2]) * r))
        lut.append(bytes([cr, cg, cb]))
    raw = b''.join(b''.join(lut[x + y] for x in range(WIDTH)) for y in range(HEIGHT))
    return Image.frombytes("RGB", (WIDTH, HEIGHT), raw)

def make_stamp():
    sw, sh = 420, 116
    stamp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(stamp)
    
    # Rounded rectangular border
    d.rounded_rectangle([4, 4, sw - 5, sh - 5], radius=14, outline=C_RED_STAMP, width=5)
    
    # 13 YEARS LATE
    t1 = "13 YEARS LATE"
    b1 = f_stamp_main.getbbox(t1)
    w1 = b1[2] - b1[0]
    x1 = (sw - w1) // 2
    d.text((x1, 14), t1, font=f_stamp_main, fill=C_RED_STAMP)
    
    # 4,811 DAYS IN QUEUE
    t2 = "4,811 DAYS IN QUEUE"
    b2 = f_stamp_sub.getbbox(t2)
    w2 = b2[2] - b2[0]
    x2 = (sw - w2) // 2
    d.text((x2, 68), t2, font=f_stamp_sub, fill=C_RED_STAMP)
    
    # Distressed stamp texture
    pixels = stamp.load()
    for py in range(sh):
        for px in range(sw):
            r, g, b, a = pixels[px, py]
            if a > 0:
                if random.random() < 0.12:
                    pixels[px, py] = (r, g, b, int(a * random.uniform(0.1, 0.6)))
                elif random.random() < 0.05:
                    pixels[px, py] = (r, g, b, 0)
    
    rotated = stamp.rotate(-8, resample=Image.Resampling.BICUBIC, expand=True)
    return rotated

def render_meme():
    bg = make_background()
    
    # Soft drop shadow under the card
    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([64, 76, 960, 972], radius=28, fill=(18, 6, 28, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    
    bg_rgba = bg.convert("RGBA")
    bg_rgba.alpha_composite(shadow)
    
    # Card surface
    card = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    
    # Card background
    cd.rectangle([64, 64, 960, 960], fill=C_CARD_BG)
    
    # ZONE 1: Black header bar (y: 64 -> 208)
    cd.rectangle([64, 64, 960, 208], fill=C_HEADER_BLACK)
    
    # ID Card Silhouette Icon (drawn with shapes)
    cd.rounded_rectangle([104, 108, 148, 138], radius=4, outline=C_WHITE, width=2)
    cd.rectangle([110, 114, 122, 128], outline=C_WHITE, width=1)
    cd.ellipse([114, 116, 118, 120], fill=C_WHITE)
    cd.arc([112, 122, 120, 130], 180, 360, fill=C_WHITE)
    cd.line([(126, 117), (142, 117)], fill=C_WHITE, width=2)
    cd.line([(126, 122), (139, 122)], fill=C_WHITE, width=2)
    cd.line([(126, 127), (135, 127)], fill=C_GOLD, width=2)
    
    # LEONIDA DMV
    cd.text((160, 88), "LEONIDA DMV", font=f_header_title, fill=C_WHITE)
    # LICENSE RENEWAL RECEIPT
    draw_letterspaced(cd, (162, 154), "LICENSE RENEWAL RECEIPT", f_header_sub, C_GOLD, spacing=3)
    
    # Right side: CLASS above V -> VI
    cd.text((865, 102), "CLASS", font=f_class_lbl, fill=C_GRAY_LABEL)
    cd.text((800, 122), "V \u2192 VI", font=f_class_val, fill=C_WHITE)
    
    # ZONE 1b: Thin magenta band (y: 208 -> 254)
    cd.rectangle([64, 208, 960, 254], fill=C_MAGENTA)
    cd.rounded_rectangle([104, 216, 290, 246], radius=15, fill=C_WHITE)
    cd.text((120, 222), "NOW SERVING #2013", font=f_pill_serving, fill=C_MAGENTA)
    draw_letterspaced(cd, (772, 224), "TAKE A NUMBER", f_take_number, C_WHITE, spacing=2)
    
    # ZONE 2: Receipt body (y: 254 -> 842)
    # SUBMITTED
    draw_letterspaced(cd, (104, 274), "SUBMITTED", f_microcap, C_GRAY_LABEL, spacing=2)
    cd.text((104, 292), "LOS SANTOS \u00B7 SEP 17, 2013", font=f_date_val, fill=C_BODY_DARK)
    
    # PROCESSED
    draw_letterspaced(cd, (104, 328), "PROCESSED", f_microcap, C_GRAY_LABEL, spacing=2)
    cd.text((104, 346), "VICE CITY \u00B7 NOV 19, 2026", font=f_date_val, fill=C_BODY_DARK)
    
    # Checkbox row
    cd.text((104, 388), "FILED AS:", font=f_checkbox, fill=C_GRAY_LABEL)
    # Box 1: ON TIME (empty)
    cd.rectangle([184, 388, 200, 404], outline=C_GRAY_LABEL, width=2)
    cd.text((208, 387), "ON TIME", font=f_checkbox, fill=(100, 100, 100))
    # Box 2: LATE RETURN (checked with red checkmark)
    cd.rectangle([300, 388, 316, 404], outline=C_RED_STAMP, width=2)
    cd.line([(302, 396), (307, 402)], fill=C_RED_STAMP, width=3)
    cd.line([(307, 402), (318, 388)], fill=C_RED_STAMP, width=3)
    cd.text((324, 387), "LATE RETURN", font=f_checkbox, fill=C_RED_STAMP)
    
    # Red Rubber Stamp (Distressed, rotated)
    stamp_img = make_stamp()
    card.alpha_composite(stamp_img, (500, 266))
    
    # Thin divider line
    cd.line([(104, 428), (920, 428)], fill=(225, 222, 214), width=1)
    
    # Five itemized fee lines
    fee_items = [
        ("Late renewal \u2014 13 years @ $100/yr", "$1,300"),
        ("Class upgrade: V \u2192 VI", "$600"),
        ("Photo retake \u2014 subject aged 13 yrs", "$40"),
        ("Address change: Los Santos \u2192 Vice City", "$60"),
        ("Restriction VI: chronic patience", "$26")
    ]
    
    start_y = 448
    line_h = 35
    for i, (desc, price) in enumerate(fee_items):
        cur_y = start_y + i * line_h
        cd.text((104, cur_y), desc, font=f_fee_text, fill=C_BODY_DARK)
        desc_bbox = f_fee_text.getbbox(desc)
        desc_w = desc_bbox[2] - desc_bbox[0]
        
        price_bbox = f_fee_price.getbbox(price)
        price_w = price_bbox[2] - price_bbox[0]
        price_x = 920 - price_w
        cd.text((price_x, cur_y), price, font=f_fee_price, fill=C_BODY_DARK)
        
        # Dotted leader line
        dot_start_x = 104 + desc_w + 12
        dot_end_x = price_x - 12
        dot_y = cur_y + 16
        for dot_x in range(dot_start_x, dot_end_x, 8):
            cd.rectangle([dot_x, dot_y, dot_x + 2, dot_y + 2], fill=(160, 160, 160))
            
    # Magenta horizontal rule
    cd.line([(104, 630), (920, 630)], fill=C_MAGENTA, width=4)
    
    # TOTAL DUE
    cd.text((104, 646), "TOTAL DUE", font=f_total_lbl, fill=C_NAVY)
    
    total_str = "$2,026"
    tot_bbox = f_total_val.getbbox(total_str)
    tot_w = tot_bbox[2] - tot_bbox[0]
    cd.text((920 - tot_w, 638), total_str, font=f_total_val, fill=C_MAGENTA)
    
    # Microprint line
    micro_str = "the total is the release year. obviously. \u00B7 no refunds \u00B7 PC version: still waiting \u00B7 Jason & Lucia approved"
    micro_bbox = f_microprint.getbbox(micro_str)
    micro_w = micro_bbox[2] - micro_bbox[0]
    cd.text(((WIDTH - micro_w) // 2, 712), micro_str, font=f_microprint, fill=(110, 110, 110))
    
    # Barcode
    bx = 104
    by = 744
    bh = 46
    bar_pattern = [
        3, 1, 1, 2, 4, 1, 2, 1, 3, 2, 1, 4, 1, 2, 3, 1, 1, 3, 2, 1, 4,
        2, 1, 3, 1, 2, 4, 1, 1, 2, 3, 1, 4, 2, 1, 3, 2, 1, 1, 4, 2, 1,
        3, 1, 2, 4, 1, 3, 1, 2, 1, 4, 2, 1, 3, 1, 2, 3, 1, 4, 1, 2, 3
    ]
    cur_bx = bx
    for idx, w in enumerate(bar_pattern):
        if idx % 2 == 0:
            cd.rectangle([cur_bx, by, cur_bx + w - 1, by + bh], fill=(20, 20, 20))
        cur_bx += w
    cd.text((104, 796), "* 2013-2026-LEONIDA-DMV-VI *", font=f_barcode_sub, fill=(100, 100, 100))
    
    # Signature line
    cd.line([(450, 790), (920, 790)], fill=(180, 180, 180), width=1)
    cd.text((450, 796), "Clerk: make.fun agent", font=f_clerk, fill=C_GRAY_LABEL)
    
    # Handwritten signature scrawl
    sig_points = [
        (470, 778), (485, 762), (495, 782), (510, 758), (525, 775),
        (540, 765), (555, 780), (580, 760), (610, 775), (650, 770), (700, 784)
    ]
    for sp in range(len(sig_points) - 1):
        cd.line([sig_points[sp], sig_points[sp+1]], fill=(25, 45, 95), width=2)
    cd.arc([465, 776, 715, 792], 0, 180, fill=(25, 45, 95), width=2)
    
    # ZONE 3: Magenta footer band (y: 842 -> 960)
    cd.rectangle([64, 842, 960, 960], fill=C_MAGENTA)
    
    # Mascot
    if os.path.exists("assets/mark-1024.png"):
        mascot = Image.open("assets/mark-1024.png").convert("RGBA")
        mascot = mascot.resize((92, 92), Image.Resampling.LANCZOS)
        card.alpha_composite(mascot, (104, 855))
        
    # Text next to mascot
    cd.text((214, 866), "PAID BY MY AI AGENT", font=f_footer_h, fill=C_WHITE)
    cd.text((214, 902), "with a bounty payout it earned on", font=f_footer_p, fill=C_WHITE)
    
    # Pill with wordmark
    cd.rounded_rectangle([755, 878, 920, 924], radius=23, fill=C_WHITE)
    cd.text((782, 886), "make.fun", font=f_pill_brand, fill=C_MAGENTA)
    
    # Rounded rectangle mask for entire card
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([64, 64, 960, 960], radius=28, fill=255)
    
    final_img = Image.composite(card, bg_rgba, mask)
    
    final_rgb = final_img.convert("RGB")
    final_rgb.save("meme.png", "PNG")
    print("Saved meme.png")
    
    img_480 = final_rgb.resize((480, 480), Image.Resampling.LANCZOS)
    img_480.save("meme_480.png", "PNG")
    print("Saved meme_480.png")

if __name__ == "__main__":
    render_meme()
