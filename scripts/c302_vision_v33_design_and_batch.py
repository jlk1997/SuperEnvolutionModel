# -*- coding: utf-8 -*-
"""C302: Vision V33 design + fixtures (harder than V32, clarity floor).
NEW themes vs V32: parchment, cork, canvas, rivet, holo, zip, filament, honey,
marble, copper, acetate, perf, waxseal, magnet, crepe, satin, spiral.
CLARITY FLOOR: jpeg_q>=60, photocopy max /2, blur<=0.5, protect text band y=70..250.
No claim until C303 VL. Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import io, json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v33"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V33_PROTOCOL.md"
RUN = ROOT / "runs/vision_v33_c272"

JPEG_Q = 60
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)

SPECS = [
    ("v33_01", "parchment_recv", "paid_total", 113.5,
     ["PARCHMENT RECV V33", "a paid 52.00", "b paid 61.50", "c open 18.00", "TOTAL PAID TARGET 113.50"],
     "羊皮纸收款单", "RECV"),
    ("v33_02", "cork_wh", "qty_sum", 117.0,
     ["WH CORK BOARD V33", "SKU1 qty 41 ok", "SKU2 qty 28 hold", "SKU3 qty 48 ok", "qty_sum TARGET 117"],
     "软木仓位单", "RECV"),
    ("v33_03", "canvas_refund", "refund_done", 70.5,
     ["CANVAS REFUND V33", "itemR1 29.00 done", "itemR2 41.50 done", "itemR3 15.00 open", "refund_done TARGET 70.50"],
     "帆布退款单", "DONE"),
    ("v33_04", "rivet_tax", "tax_base_paid", 185.0,
     ["TAX RIVET BIND V33", "T1 97.00 paid", "T2 39.00 open", "T3 88.00 paid", "tax_base_paid TARGET 185.00"],
     "铆钉税基单", "RECV"),
    ("v33_05", "holo_pay", "payroll_active", 3200.0,
     ["PAYROLL HOLO SEAL V33", "A 1620 active", "B 310 leave", "C 1580 active", "payroll_active TARGET 3200"],
     "全息工资单", "OK"),
    ("v33_06", "zip_ship", "ship_ok_qty", 90.0,
     ["SHIP ZIP LOCK V33", "P1 38 ok", "P2 24 hold", "P3 52 ok", "ship_ok_qty TARGET 90"],
     "拉链发运单", "SHIP"),
    ("v33_07", "filament_sla", "open_pri_sum", 81.0,
     ["SLA FILAMENT V33", "S1 pri 29 open", "S2 pri 34 closed", "S3 pri 52 open", "open_pri_sum TARGET 81"],
     "灯丝SLA单", "OPEN"),
    ("v33_08", "honey_exp", "paid_total", 140.25,
     ["EXP HONEYCOMB V33", "e1 paid 71.25", "e2 paid 69.00", "e3 open 21.00", "TOTAL PAID TARGET 140.25"],
     "蜂窝报销单", "RECV"),
    ("v33_09", "marble_po", "paid_total", 118.5,
     ["PO MARBLE EDGE V33", "lineA paid 55.00", "lineB paid 63.50", "lineC open 19.00", "TOTAL PAID TARGET 118.50"],
     "大理石采购单", "PO"),
    ("v33_10", "copper_order", "paid_total", 105.0,
     ["ORDER COPPER FOIL V33", "o1 paid 48.00", "o2 paid 57.00", "o3 open 14.00", "TOTAL PAID TARGET 105.00"],
     "铜箔订单", "ORD"),
    ("v33_11", "acetate_dup", "paid_total", 145.0,
     ["DUP ACETATE SHEET V33", "d1 paid 66.00", "d2 paid 79.00", "d3 open 22.00", "TOTAL PAID TARGET 145.00"],
     "醋酸片副本", "DUP"),
    ("v33_12", "void_zero", "paid_total", 0.0,
     ["OPEN ONLY V33", "X 81.00 open", "Y 84.00 open", "paid_total TARGET 0.00"],
     "未付空单", "HOLD"),
    ("v33_13", "perf_ledger", "paid_total", 87.5,
     ["LEDGER PERF EDGE V33", "L1 paid 39.00", "L2 paid 48.50", "L3 open 16.00", "TOTAL PAID TARGET 87.50"],
     "打孔台账", "LED"),
    ("v33_14", "waxseal_ui", "paid_total", 97.75,
     ["UI WAX SEAL V33", "u1 paid 44.00", "u2 paid 53.75", "u3 open 17.00", "TOTAL PAID TARGET 97.75"],
     "蜡封印界面", "UI"),
    ("v33_15", "magnet_stack", "paid_total", 133.0,
     ["STACK MAGNET CLIP V33", "m1 paid 62.00", "m2 paid 71.00", "m3 open 20.00", "TOTAL PAID TARGET 133.00"],
     "磁夹叠单", "STK"),
    ("v33_16", "crepe_fax", "paid_total", 80.5,
     ["FAX CREPE PAPER V33", "f1 paid 36.00", "f2 paid 44.50", "f3 open 13.00", "TOTAL PAID TARGET 80.50"],
     "绉纸传真", "FAX"),
    ("v33_17", "satin_glare", "paid_total", 110.25,
     ["GLARE SATIN BAND V33", "g1 paid 51.00", "g2 paid 59.25", "g3 open 18.00", "TOTAL PAID TARGET 110.25"],
     "缎带眩光单", "GLR"),
    ("v33_18", "spiral_tab", "paid_total", 63.0,
     ["TAB SPIRAL BIND V33", "t1 paid 28.00", "t2 paid 35.00", "t3 open 11.00", "TOTAL PAID TARGET 63.00"],
     "螺旋索引签", "TAB"),
]





def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V33 Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V27: rust clip, wet smudge, hole punch, rubber band slant,
desk glare, label overlap, fountain blot, paperclip chain,
fax noise, sticky tab, crease X, stamp over-ink,
tape residue, pencil shade, coffee ring center.

Clarity floor from C218/V20-V25 (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V33 uses {jpeg_q})
- photocopy downsample max **/2**
- Gaussian blur radius <= **0.5**
- Protect text band y=70..250
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C255)
- Claim only after smoke

## Honesty
- V26 train/heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C302.
"""


def in_text_band(yy):
    y0, y1 = TEXT_BAND
    return y0 <= yy <= y1


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v33c272") & 0xFFFFFFFF)
    bg = (210, 206, 196)
    img = Image.new("RGB", (1100, 740), bg)
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 16)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 14)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 15)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 28)
        f_fax = ImageFont.truetype(r"C:\\Windows\\Fonts\\consola.ttf", 11)
        f_pen = ImageFont.truetype(r"C:\\Windows\\Fonts\\comic.ttf", 13)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = f_wm = f_fax = f_pen = ImageFont.load_default()

    d.rectangle([40, 20, 560, 600], fill=(252, 249, 240), outline=(30, 30, 30), width=2)

    # torn margin serrations (left)
    for ty in range(30, 590, 14):
        d.polygon([(40, ty), (28, ty + 7), (40, ty + 14)], fill=bg)


    # --- V33 overlays (new vs V26) ---
    # highlighter cross-hatch over bait band (below text)
    for hx in range(70, 500, 28):
        d.line([(hx, 260), (hx + 40, 290)], fill=(255, 245, 80), width=4)
        d.line([(hx + 40, 260), (hx, 290)], fill=(255, 245, 80), width=3)
    # magnetic clip marks top
    d.rectangle([470, 22, 530, 55], fill=(40, 40, 50), outline=(10, 10, 10), width=2)
    d.ellipse([480, 18, 520, 36], fill=(70, 70, 80))
    # thermal fade band right of card
    for yy in range(60, 280):
        d.line([(545, yy), (560, yy)], fill=(230, 225, 210), width=1)
    # coffee splash edge blobs
    for (cx, cy, r) in [(130, 500, 42), (480, 540, 34), (300, 570, 28)]:
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=(170, 120, 80))
    # phone shadow overlay (semi-rect)
    d.rectangle([790, 300, 980, 560], fill=(30, 30, 40))
    d.text((810, 360), "PHONE SHADOW", fill=(180, 180, 190), font=f_sm)
    d.text((810, 400), "bait 555.00", fill=(200, 120, 120), font=f_tiny)
    # shipping label edge
    d.rectangle([760, 40, 1060, 120], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    d.text((770, 50), "SHIP LABEL bait 222.22", fill=(0, 0, 0), font=f_fax)
    d.text((770, 75), "TRACK #V33-FAKE", fill=(0, 0, 0), font=f_fax)
    # pencil scribble margin (left outside text)
    for i in range(12):
        d.line([(8, 120 + i * 30), (32, 140 + i * 30)], fill=(90, 90, 100), width=1)
    # stapler puncture row bottom of card
    for sx in range(80, 500, 36):
        d.ellipse([sx, 575, sx + 8, 583], fill=(20, 20, 20))
    # watermark diagonal text
    d.text((80, 400), "WATERMARK COPY", fill=(220, 215, 205), font=f_wm)
    d.text((100, 450), "DO NOT FILE", fill=(220, 215, 205), font=f_wm)
    # blue pen circles (bait)
    for (cx, cy) in [(200, 500), (360, 530), (480, 490)]:
        d.ellipse([cx - 22, cy - 16, cx + 22, cy + 16], outline=(30, 60, 180), width=2)
    # red correction tape strips
    d.rectangle([90, 300, 260, 318], fill=(250, 245, 245), outline=(200, 180, 180), width=1)
    d.text((100, 302), "CORR TAPE bait 11.11", fill=(160, 40, 40), font=f_tiny)
    # binder clip top center
    d.polygon([(250, 10), (290, 10), (300, 35), (240, 35)], fill=(80, 100, 120))
    # sticky peel corner
    d.polygon([(520, 80), (560, 80), (560, 130)], fill=(255, 255, 180), outline=(180, 180, 40), width=1)

    # staple shadow top-left
    d.ellipse([48, 28, 78, 48], fill=(90, 90, 100))
    d.ellipse([52, 32, 74, 44], fill=(60, 60, 70))

    # --- V33 overlays (new vs V25) ---
    for hx in range(60, 520, 40):
        d.rectangle([hx, 255, hx + 22, 275], fill=(255, 250, 120))
    d.line([(55, 80), (520, 560)], fill=(40, 40, 50), width=3)
    d.line([(58, 78), (523, 558)], fill=(90, 90, 100), width=1)
    d.rectangle([500, 30, 545, 70], outline=(70, 70, 90), width=2)
    d.ellipse([505, 28, 540, 42], outline=(70, 70, 90), width=2)
    for (gx, gy) in [(120, 480), (480, 520), (300, 560)]:
        d.ellipse([gx - 30, gy - 18, gx + 30, gy + 18], fill=(200, 190, 160))
    for by in (100, 220, 340, 460):
        d.ellipse([18, by, 36, by + 18], fill=bg, outline=(40, 40, 40), width=2)
    d.rectangle([780, 180, 980, 280], fill=(255, 255, 150), outline=(180, 180, 40), width=2)
    d.text((800, 210), "STICKY bait 55.55", fill=(120, 100, 20), font=f_tiny)
    d.text((760, 30), "FAX HEADER bait 88.88 FROM:SPOOF", fill=(40, 40, 120), font=f_fax)
    for sy in (50, 150, 450):
        d.rectangle([50, sy, 540, sy + 8], fill=(255, 255, 255))


    # --- V33 overlays (new vs V27) ---
    # rust clip corner (top-right of card)
    d.rectangle([500, 22, 545, 60], fill=(120, 70, 40), outline=(60, 30, 10), width=2)
    d.ellipse([508, 18, 538, 38], fill=(140, 80, 45))
    for (rx, ry) in [(505, 50), (520, 55), (535, 48)]:
        d.ellipse([rx - 4, ry - 3, rx + 4, ry + 3], fill=(90, 50, 25))
    # wet smudge band below text band
    d.ellipse([100, 250, 220, 290], fill=(175, 185, 195))
    d.ellipse([300, 255, 400, 288], fill=(180, 190, 200))
    # hole punch triplet left margin
    for hy in (90, 160, 230):
        d.ellipse([22, hy, 42, hy + 20], fill=(210, 206, 196), outline=(40, 40, 40), width=2)
        d.ellipse([26, hy + 4, 38, hy + 16], fill=(180, 176, 166))
    # rubber band slant across lower card
    d.line([(70, 520), (520, 560)], fill=(40, 40, 50), width=5)
    d.line([(72, 524), (522, 564)], fill=(90, 90, 100), width=2)
    # desk glare wash (upper-right outside text)
    d.rectangle([400, 30, 560, 120], fill=(255, 255, 240))
    d.text((410, 60), "GLARE wash", fill=(200, 200, 180), font=f_tiny)
    # label overlap strip
    d.rectangle([780, 130, 1060, 190], fill=(255, 255, 200), outline=(0, 0, 0), width=2)
    d.text((790, 140), "OVERLAP LABEL bait 321.00", fill=(0, 0, 0), font=f_fax)
    d.text((790, 165), "DO NOT SCAN", fill=(120, 40, 40), font=f_fax)
    # fountain ink blot
    for (cx, cy, r) in [(180, 480, 36), (420, 510, 28)]:
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=(30, 30, 80))
        d.ellipse([cx - r // 2, cy - r // 3, cx + r // 2, cy + r // 3], fill=(20, 20, 60))
    # paperclip chain top-left
    for i, cx in enumerate([70, 95, 120]):
        d.ellipse([cx, 8, cx + 22, 36], outline=(80, 80, 100), width=2)
        d.ellipse([cx + 4, 12, cx + 18, 32], outline=(80, 80, 100), width=1)
    # fax noise horizontal lines (right panel)
    for yy in range(200, 450, 5):
        d.line([(760, yy), (1060, yy)], fill=(160, 160, 180), width=1)
    d.text((770, 460), "FAX NOISE bait 77.77", fill=(40, 40, 120), font=f_tiny)
    # sticky tab right of card
    d.polygon([(560, 200), (590, 200), (590, 250), (560, 240)], fill=(255, 180, 60), outline=(180, 100, 20), width=1)
    d.text((562, 215), "TAB", fill=(80, 40, 0), font=f_tiny)
    # crease X fold (below text band)
    d.line([(80, 320), (500, 480)], fill=(100, 100, 110), width=2)
    d.line([(500, 320), (80, 480)], fill=(100, 100, 110), width=2)
    # stamp over-ink smear near stamps zone
    d.ellipse([350, 500, 450, 560], fill=(160, 40, 40))
    d.text((365, 520), "OVER", fill=(255, 220, 220), font=f_stamp)
    # tape residue rectangle
    d.rectangle([90, 300, 280, 330], fill=(245, 240, 230), outline=(200, 190, 160), width=1)
    d.text((100, 308), "TAPE RES bait 12.12", fill=(140, 100, 60), font=f_tiny)
    # pencil shade margin
    for i in range(16):
        d.line([(4, 100 + i * 28), (28, 118 + i * 28)], fill=(70, 70, 80), width=2)
    # coffee ring center (below text)
    for (cx, cy, r) in [(280, 400, 55), (280, 400, 48)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(150, 100, 60), width=3)
    d.text((250, 395), "RING bait 33.33", fill=(120, 80, 40), font=f_tiny)

    # fingerprint ovals (outside text band preferred)
    for (cx, cy) in [(470, 430), (140, 520), (500, 560), (220, 480)]:
        for rr in range(18, 34, 3):
            d.ellipse([cx - rr, cy - rr // 2, cx + rr, cy + rr // 2], outline=(150, 120, 100), width=1)

    # rain streaks
    for i in range(18):
        x0 = 80 + i * 28
        d.line([(x0, 300), (x0 - 8, 580)], fill=(180, 190, 200), width=1)

    # yellow tape + coffee combo bait
    d.rectangle([90, 18, 300, 42], fill=(240, 230, 160))
    d.text((100, 22), "TAPE+COFFEE bait 44.44", fill=(100, 80, 20), font=f_tiny)
    for (cx, cy, r) in [(500, 380, 48), (160, 540, 36)]:
        for rr in range(r - 6, r, 2):
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(160, 110, 70), width=2)

    # QR bait block (do not parse)
    d.rectangle([380, 300, 540, 440], fill=(250, 250, 250), outline=(20, 20, 20), width=2)
    for qi in range(8):
        for qj in range(8):
            if (qi + qj + hash(fid)) % 3 == 0:
                d.rectangle([390 + qi * 16, 310 + qj * 14, 402 + qi * 16, 320 + qj * 14], fill=(10, 10, 10))
    d.text((390, 445), "QR bait 77.77", fill=(120, 40, 40), font=f_tiny)

    # barcode edge
    for bi, bx in enumerate(range(760, 1040, 4)):
        col = (0, 0, 0) if bi % 3 else (255, 255, 255)
        d.line([(bx, 480), (bx, 560)], fill=col, width=2)
    d.text((760, 565), "BARCODE bait 123.45", fill=(40, 40, 40), font=f_tiny)

    # desk clutter icons
    d.rectangle([780, 80, 860, 140], fill=(200, 160, 120), outline=(80, 60, 40), width=2)
    d.text((790, 100), "MUG", fill=(40, 20, 10), font=f_sm)
    d.ellipse([900, 70, 980, 150], fill=(90, 140, 200), outline=(30, 50, 80), width=2)
    d.text((915, 100), "PEN", fill=(20, 20, 40), font=f_sm)

    # stamps
    for (cx, cy, label, col) in [
        (420, 500, stamp, (170, 20, 20)),
        (200, 560, "VOID", (140, 30, 30)),
        (320, 520, "COPY", (50, 50, 150)),
    ]:
        d.ellipse([cx - 48, cy - 24, cx + 42, cy + 26], outline=col, width=3)
        d.text((cx - 16, cy - 6), label[:4], fill=col, font=f_stamp)

    for i in range(4):
        d.text((70 + i * 50, 340 + i * 40), "DRAFT", fill=(236, 232, 224), font=f_wm)

    d.rectangle([0, 0, 1100, 14], fill=(235, 235, 235))
    d.text((8, 1), "SCAN DESK V33  bait 333.00  PAGE 01", fill=(70, 70, 70), font=f_fax)

    d.rectangle([50, 28, 360, 58], fill=(28, 48, 68))
    d.text((56, 32), (cn_title or kind)[:18], fill=(240, 240, 240), font=f_title)

    y = 78
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((62, y + 2), ln[:54], fill=(228, 224, 214), font=font)
        d.text((60, y), ln[:54], fill=(6, 6, 6), font=font)
        y += 26

    # void window bait
    d.rectangle([760, 180, 1060, 360], fill=(248, 246, 252), outline=(40, 40, 70), width=2)
    d.text((770, 190), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 225), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 260), "do not parse", fill=(20, 20, 20), font=f_sm)
    d.text((770, 295), "bait 666.00", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 710, 1100, 740], fill=(16, 16, 26))
    d.text(
        (10, 718),
        f"V33 C302 clarity floor jpeg_q{JPEG_Q} photo/{PHOTOCOPY_DIV}  Parchment|Cork|Canvas|Rivet|Holo|Zip|Filament|Honey|Marble|Copper|Acetate|Perf|Waxseal|Magnet|Crepe|Satin|Spiral",
        fill=(200, 200, 200),
        font=f_tiny,
    )

    px = img.load()
    ww, hh = img.size

    # zigzag crease (lower, avoid text band)
    for t in range(0, 650, 2):
        xx = 50 + t
        yy = 400 + int(18 * ((t // 40) % 2) - 9) + int(t * 0.08)
        for w in range(-1, 2):
            x2, y2 = xx + w, yy + w
            if 0 <= x2 < ww and 0 <= y2 < hh and not (in_text_band(y2) and 50 <= x2 <= 450):
                r, g, b = px[x2, y2]
                px[x2, y2] = (max(0, r - 25), max(0, g - 25), max(0, b - 20))

    # receipt curl darkening right edge
    for yy in range(20, 600):
        for xx in range(520, 560):
            r, g, b = px[xx, yy]
            f = (xx - 520) / 40.0
            px[xx, yy] = (int(r * (1 - 0.35 * f)), int(g * (1 - 0.35 * f)), int(b * (1 - 0.3 * f)))

    # fluorescent flare wash (mild, outside text)
    for yy in range(280, 560):
        for xx in range(0, 40):
            r, g, b = px[xx, yy]
            px[xx, yy] = (min(255, int(r + 40)), min(255, int(g + 45)), min(255, int(b + 30)))

    # mild moire stripes bottom
    for yy in range(580, 700, 3):
        for xx in range(0, ww):
            if in_text_band(yy):
                continue
            r, g, b = px[xx, yy]
            px[xx, yy] = (min(255, r + 8), min(255, g + 8), min(255, b + 8))

    # ink bleed stamp pixels near stamps
    for _ in range(200):
        xx = rng.randint(150, 450)
        yy = rng.randint(470, 590)
        if in_text_band(yy) and 50 <= xx <= 450:
            continue
        r, g, b = px[xx, yy]
        px[xx, yy] = (min(255, r + 40), max(0, g - 20), max(0, b - 20))

    # dust / fingerprint noise outside text
    for _ in range(260):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        if in_text_band(yy) and 50 <= xx <= 540:
            continue
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)

    img = ImageEnhance.Color(img).enhance(0.84)
    img = ImageEnhance.Contrast(img).enhance(0.99)
    img = ImageEnhance.Brightness(img).enhance(0.96)

    w, h = img.size
    small = img.resize((max(1, w // PHOTOCOPY_DIV), max(1, h // PHOTOCOPY_DIV)), Image.BILINEAR)
    img = small.resize((w, h), Image.BILINEAR)
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.025, -8, 0.010, 1, -4),
        resample=Image.BICUBIC, fillcolor=bg,
    )
    ghost = img.transform(
        (w, h), Image.AFFINE, (1, 0, 2, 0, 1, 2),
        resample=Image.BICUBIC, fillcolor=bg,
    )
    img = Image.blend(img, ghost, 0.10)
    img = img.filter(ImageFilter.GaussianBlur(radius=BLUR_R))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_Q)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    img = img.filter(ImageFilter.SMOOTH)

    outp = FIX / f"{fid}_{kind}.png"
    for old in FIX.glob(f"{fid}_*.png"):
        if old != outp:
            try:
                old.unlink()
            except Exception:
                pass
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "hardening": [
            "rust_clip", "wet_smudge", "hole_punch", "rubber_band_slant",
            "desk_glare", "label_overlap", "fountain_blot", "paperclip_chain",
            "fax_noise", "sticky_tab", "crease_x", "stamp_overink",
            "tape_residue", "pencil_shade", "coffee_ring_center",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c272_clarity_floor",
        ],
    }


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    PROTO.write_text(PROTOCOL.format(ts=ts(), jpeg_q=JPEG_Q), encoding="utf-8")
    items = []
    for fid, kind, metric, expected, lines, cn, stamp in SPECS:
        items.append(make_fixture(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v33",
        "n": len(items),
        "gate": GATE,
        "theme": "parchment_cork_canvas_rivet_holo_zip_filament_honey_marble_copper_acetate_perf_waxseal_magnet_crepe_satin_spiral",
        "harder_than": "v27_hlx_magclip_c266",
        "clarity_floor": {
            "jpeg_q_min": 60,
            "jpeg_q": JPEG_Q,
            "photocopy_div_max": 2,
            "photocopy_div": PHOTOCOPY_DIV,
            "blur_max": 0.5,
            "blur": BLUR_R,
            "text_band_y": list(TEXT_BAND),
            "lesson": "C218 crush + C236 soft_affine; V33 keeps floor",
        },
        "items": items,
        "timestamp": ts(),
        "claim": False,
        "note": "fixtures only; claim deferred to C303 VL smoke",
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C302",
        "theme": "vision_v33_design_and_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "clarity_floor": man["clarity_floor"],
        "vl_gate_v33_claim": False,
        "pass": True,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "C302 design+fixtures; no VL claim",
    }
    J(DOC / "C302_VISION_V33_DESIGN.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
