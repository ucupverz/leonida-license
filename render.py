import os
import random
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_receipt():
    # Deterministic seed as specified
    random.seed(2026)

    width = 1024
    height = 1024

    # 1. Background gradient
    # Deep purple (43,16,85) at top-left -> magenta (214,36,159) middle -> warm orange (255,140,66) bottom-right
    c_purple = (43, 16, 85)
    c_magenta = (214, 36, 159)
    c_orange = (255, 140, 66)

    max_diag = 1023 + 1023  # 2046
    color_table = []
    for d in range(max_diag + 1):
        t = d / float(max_diag)
        if t <= 0.5:
            f = t * 2.0
            r = int(c_purple[0] + (c_magenta[0] - c_purple[0]) * f + 0.5)
            g = int(c_purple[1] + (c_magenta[1] - c_purple[1]) * f + 0.5)
            b = int(c_purple[2] + (c_magenta[2] - c_purple[2]) * f + 0.5)
        else:
            f = (t - 0.5) * 2.0
            r = int(c_magenta[0] + (c_orange[0] - c_magenta[0]) * f + 0.5)
            g = int(c_magenta[1] + (c_orange[1] - c_magenta[1]) * f + 0.5)
            b = int(c_magenta[2] + (c_orange[2] - c_magenta[2]) * f + 0.5)
        color_table.append((r, g, b))

    buf = bytearray(width * height * 3)
    idx = 0
    for y in range(height):
        for x in range(width):
            c = color_table[x + y]
            buf[idx] = c[0]
            buf[idx + 1] = c[1]
            buf[idx + 2] = c[2]
            idx += 3

    bg = Image.frombytes("RGB", (width, height), bytes(buf))

    # Fonts
    font_arialbd = lambda size: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", size)
    font_arial = lambda size: ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)
    font_monobd = lambda size: ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", size)
    font_mono = lambda size: ImageFont.truetype("C:/Windows/Fonts/consola.ttf", size)

    # Helper for letter-spaced text
    def draw_spaced_text(d, pos, text, font, fill, spacing=3):
        cur_x, cur_y = pos
        for ch in text:
            d.text((cur_x, cur_y), ch, font=font, fill=fill)
            w = font.getlength(ch)
            cur_x += w + spacing

    # 2. Card layer
    card = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)

    # Base sections of the card
    # Section 1: Black header bar (64..208)
    draw.rectangle([64, 64, 960, 208], fill=(20, 20, 20))

    # Section 2: Magenta strip (208..254)
    draw.rectangle([64, 208, 960, 254], fill=(214, 33, 156))

    # Section 3: Paper body (254..842)
    draw.rectangle([64, 254, 960, 842], fill=(255, 253, 247))

    # Section 4: Magenta footer band (842..960)
    draw.rectangle([64, 842, 960, 960], fill=(214, 33, 156))

    # --- Section 1: Black Header Bar Details ---
    # ID card icon
    # Rounded rectangle card outline
    draw.rounded_rectangle([96, 96, 164, 174], radius=7, outline=(255, 255, 255), width=2)
    # Head circle
    draw.ellipse([108, 108, 126, 126], fill=(255, 255, 255))
    # Body arc / shoulders
    draw.chord([103, 130, 131, 152], start=180, end=0, fill=(255, 255, 255))
    # Text lines
    draw.line([(135, 116), (155, 116)], fill=(255, 255, 255), width=2)
    draw.line([(135, 126), (155, 126)], fill=(255, 209, 102), width=2)  # gold line
    draw.line([(135, 136), (148, 136)], fill=(255, 255, 255), width=2)

    # Header text
    f_dmv = font_arialbd(55)
    draw.text((182, 90), "LEONIDA DMV", font=f_dmv, fill=(255, 255, 255))

    f_sub = font_arialbd(21)
    draw_spaced_text(draw, (185, 158), "LICENSE RENEWAL RECEIPT", f_sub, fill=(255, 209, 102), spacing=3)

    # Class label and value on right
    f_class_lbl = font_arial(13)
    f_class_val = font_arialbd(40)
    class_val_str = "V \u2192 VI"
    val_w = f_class_val.getlength(class_val_str)
    draw.text((920 - val_w, 118), class_val_str, font=f_class_val, fill=(255, 255, 255))

    lbl_w = f_class_lbl.getlength("CLASS")
    draw.text((920 - lbl_w, 98), "CLASS", font=f_class_lbl, fill=(160, 160, 160))

    # --- Section 2: Magenta Strip Details ---
    # White rounded pill: "NOW SERVING #2013"
    f_pill = font_arialbd(15)
    pill_text = "NOW SERVING #2013"
    pill_text_w = f_pill.getlength(pill_text)
    pill_pad_x = 14
    pill_w = pill_text_w + pill_pad_x * 2
    draw.rounded_rectangle([96, 217, 96 + pill_w, 245], radius=14, fill=(255, 255, 255))
    draw.text((96 + pill_pad_x, 222), pill_text, font=f_pill, fill=(214, 33, 156))

    # Right: "TAKE A NUMBER" letter-spaced
    f_tan = font_arialbd(14)
    tan_text = "TAKE A NUMBER"
    tan_spacing = 2
    tan_w = sum(f_tan.getlength(c) + tan_spacing for c in tan_text) - tan_spacing
    draw_spaced_text(draw, (920 - tan_w, 223), tan_text, f_tan, fill=(255, 255, 255), spacing=tan_spacing)

    # --- Section 3: White Paper Body Details ---
    # SUBMITTED label + value
    f_meta_lbl = font_arialbd(12)
    f_meta_val = font_arialbd(21)
    draw_spaced_text(draw, (96, 274), "SUBMITTED", f_meta_lbl, fill=(130, 130, 135), spacing=1)
    draw.text((96, 292), "LOS SANTOS \u00b7 SEP 17, 2013", font=f_meta_val, fill=(18, 18, 20))

    # PROCESSED label + value
    draw_spaced_text(draw, (96, 328), "PROCESSED", f_meta_lbl, fill=(130, 130, 135), spacing=1)
    draw.text((96, 346), "VICE CITY \u00b7 NOV 19, 2026", font=f_meta_val, fill=(18, 18, 20))

    # Checkbox row
    f_chk = font_arialbd(14)
    draw.text((96, 388), "FILED AS:", font=f_chk, fill=(130, 130, 135))

    # Empty box "ON TIME"
    draw.rectangle([186, 388, 202, 404], outline=(150, 150, 155), width=2)
    draw.text((210, 388), "ON TIME", font=f_chk, fill=(140, 140, 145))

    # Checked box "LATE RETURN"
    draw.rectangle([300, 388, 316, 404], outline=(226, 59, 46), width=2)
    draw.line([(303, 396), (307, 401)], fill=(226, 59, 46), width=2)
    draw.line([(307, 401), (314, 391)], fill=(226, 59, 46), width=2)
    draw.text((324, 388), "LATE RETURN", font=f_chk, fill=(226, 59, 46))

    # Red rubber stamp overlapping upper-right of body
    stamp_w, stamp_h = 390, 135
    stamp_img = Image.new("RGBA", (stamp_w, stamp_h), (0, 0, 0, 0))
    stamp_draw = ImageDraw.Draw(stamp_img)
    stamp_red = (226, 59, 46)

    # Double border
    stamp_draw.rounded_rectangle([4, 4, stamp_w - 4, stamp_h - 4], radius=15, outline=stamp_red, width=4)
    stamp_draw.rounded_rectangle([13, 13, stamp_w - 13, stamp_h - 13], radius=10, outline=stamp_red, width=2)

    # Stamp text
    f_stamp_hdr = font_arialbd(48)
    f_stamp_sub = font_arialbd(20)

    t1 = "13 YEARS LATE"
    w_t1 = f_stamp_hdr.getlength(t1)
    stamp_draw.text(((stamp_w - w_t1) / 2, 22), t1, font=f_stamp_hdr, fill=stamp_red)

    t2 = "4,811 DAYS IN QUEUE"
    w_t2 = f_stamp_sub.getlength(t2)
    stamp_draw.text(((stamp_w - w_t2) / 2, 82), t2, font=f_stamp_sub, fill=stamp_red)

    # Light distressed texture
    stamp_pix = stamp_img.load()
    for sy in range(stamp_h):
        for sx in range(stamp_w):
            r, g, b, a = stamp_pix[sx, sy]
            if a > 0:
                rv = random.random()
                if rv < 0.08:
                    stamp_pix[sx, sy] = (r, g, b, 0)
                elif rv < 0.22:
                    stamp_pix[sx, sy] = (r, g, b, int(a * 0.45))
                elif rv < 0.35:
                    stamp_pix[sx, sy] = (r, g, b, int(a * 0.75))

    stamp_rot = stamp_img.rotate(-8, resample=Image.BICUBIC, expand=True)
    card.alpha_composite(stamp_rot, (530, 260))

    # Divider line
    draw.line([(96, 428), (920, 428)], fill=(220, 220, 225), width=1)

    # Six itemized fee lines
    fee_lines = [
        ("Late renewal \u2014 13 years @ $100/yr", "$1,300"),
        ("Two delays: Fall 2025, May 2026", "$52"),
        ("Road test: in line since 2013", "$213"),
        ("Photo retake: subject aged 13 yrs", "$137"),
        ("Class upgrade: V \u2192 VI", "$224"),
        ("Address: Los Santos \u2192 Vice City", "$100"),
    ]

    f_fee = font_monobd(22)
    start_y = 448
    spacing_y = 35

    for i, (desc, price) in enumerate(fee_lines):
        line_y = start_y + i * spacing_y
        draw.text((96, line_y), desc, font=f_fee, fill=(18, 18, 20))

        pw = f_fee.getlength(price)
        px = 920 - pw
        draw.text((px, line_y), price, font=f_fee, fill=(18, 18, 20))

        # Dotted leader lines: 2px squares every 8px
        desc_w = f_fee.getlength(desc)
        dot_start = int(96 + desc_w + 12)
        dot_end = int(px - 10)
        dot_y = line_y + 15
        for dx in range(dot_start, dot_end, 8):
            draw.rectangle([dx, dot_y, dx + 2, dot_y + 2], fill=(160, 160, 165))

    # Magenta horizontal rule (~4px thick)
    draw.line([(96, 664), (920, 664)], fill=(214, 33, 156), width=4)

    # TOTAL DUE row
    f_total_lbl = font_arialbd(40)
    f_total_val = font_arialbd(64)
    draw.text((96, 696), "TOTAL DUE", font=f_total_lbl, fill=(27, 42, 74))

    val_str = "$2,026"
    val_w = f_total_val.getlength(val_str)
    draw.text((920 - val_w, 674), val_str, font=f_total_val, fill=(214, 33, 156))

    # Microprint line
    f_micro = font_mono(13)
    micro_text = "Form VI-13 \u00b7 examiners Jason & Lucia \u00b7 214 GB download required \u00b7 no refunds \u00b7 PC version pending"
    micro_w = f_micro.getlength(micro_text)
    draw.text(((width - micro_w) / 2, 752), micro_text, font=f_micro, fill=(110, 110, 110))

    # Barcode at lower-left
    bar_widths = [3, 1, 2, 1, 4, 2, 1, 3, 2, 1, 1, 3, 2, 4, 1, 2, 3, 1, 2, 2, 1, 3, 1, 4, 2, 1, 3, 2, 1, 2, 3, 1, 1, 4, 2, 1, 3, 2]
    bar_gaps   = [2, 1, 2, 3, 1, 2, 2, 1, 3, 2, 1, 2, 1, 3, 2, 1, 2, 3, 1, 2, 1, 2, 3, 1, 2, 2, 1, 3, 2, 1, 2, 1, 3, 2, 1, 2, 1, 2]

    bx = 96
    for bw, bgap in zip(bar_widths, bar_gaps):
        draw.rectangle([bx, 772, bx + bw, 808], fill=(20, 20, 20))
        bx += bw + bgap

    f_barcode_cap = font_mono(11)
    draw.text((96, 814), "* 2013-2026-LEONIDA-DMV-VI *", font=f_barcode_cap, fill=(120, 120, 120))

    # Signature line at lower-right
    draw.line([(680, 808), (920, 808)], fill=(180, 180, 185), width=1)

    # Scrawl signature
    scrawl_points = [
        (700, 802), (712, 788), (722, 778), (728, 796), (734, 802),
        (744, 786), (754, 782), (760, 800), (772, 788), (784, 785),
        (796, 802), (802, 792), (814, 780), (822, 778), (828, 800),
        (836, 802), (850, 794), (866, 792), (886, 790), (902, 788), (914, 798)
    ]
    for i in range(len(scrawl_points) - 1):
        draw.line([scrawl_points[i], scrawl_points[i + 1]], fill=(27, 42, 74), width=2)

    f_clerk = font_arial(13)
    draw.text((680, 814), "Clerk: make.fun agent", font=f_clerk, fill=(120, 120, 120))

    # --- Section 4: Magenta Footer Band Details ---
    # Mascot on left
    mascot_path = "assets/mark-1024.png"
    if os.path.exists(mascot_path):
        mascot = Image.open(mascot_path).convert("RGBA")
        mascot = mascot.resize((92, 92), Image.LANCZOS)
        card.alpha_composite(mascot, (96, 855))

    f_foot_hdr = font_arialbd(26)
    f_foot_sub = font_arial(17)
    draw.text((206, 864), "PAID BY MY AI AGENT", font=f_foot_hdr, fill=(255, 255, 255))
    draw.text((206, 902), "with a bounty payout it earned on", font=f_foot_sub, fill=(255, 255, 255))

    # White pill with make.fun on right
    pill_mf_w = 160
    pill_mf_h = 48
    pill_mf_x1 = 920 - pill_mf_w
    pill_mf_y1 = 878
    draw.rounded_rectangle([pill_mf_x1, pill_mf_y1, 920, pill_mf_y1 + pill_mf_h], radius=24, fill=(255, 255, 255))

    f_mf = font_arialbd(24)
    mf_text = "make.fun"
    mf_w = f_mf.getlength(mf_text)
    draw.text((pill_mf_x1 + (pill_mf_w - mf_w) / 2, pill_mf_y1 + 10), mf_text, font=f_mf, fill=(214, 33, 156))

    # 3. Soft blurred dark drop shadow
    shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle([64, 74, 960, 970], radius=28, fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=18))

    # 4. Rounded corner mask for the card
    mask = Image.new("L", (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([64, 64, 960, 960], radius=28, fill=255)

    # 5. Composite card over gradient
    final_canvas = bg.copy().convert("RGBA")
    final_canvas.alpha_composite(shadow)
    final_canvas.paste(card, (0, 0), mask)

    final_rgb = final_canvas.convert("RGB")
    final_rgb.save("meme.png", "PNG")
    print("Saved meme.png (1024x1024)")

    # Downscaled 480x480 version
    img_480 = final_rgb.resize((480, 480), Image.LANCZOS)
    img_480.save("meme_480.png", "PNG")
    print("Saved meme_480.png (480x480)")

if __name__ == "__main__":
    create_receipt()
