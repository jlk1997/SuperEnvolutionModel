# -*- coding: utf-8 -*-
"""C266: Vision V27 design + fixtures (harder than V25, clarity floor).
NEW themes vs V25: fingerprint_smudge, rain_streak, staple_shadow, qr_bait,
receipt_curl, fluorescent_flare, desk_clutter, ink_bleed_stamp, torn_margin,
zigzag_crease, tape_coffee_combo, barcode_edge, moire_mild, water_ring_stack.
CLARITY FLOOR: jpeg_q>=58, photocopy max /2, blur<=0.5, protect text band y=70..250.
No claim until C267 VL. Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import io, json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v27"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V27_PROTOCOL.md"
RUN = ROOT / "runs/vision_v27_c266"

JPEG_Q = 60
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)

SPECS = [
    ("v27_01", "hl_recv", "paid_total", 102.25,
     ["HIGHLIGHTER CROSS RECV V27", "a paid 49.00", "b paid 53.25", "c open 14.00", "TOTAL PAID TARGET 102.25"],
     "荧光笔交叉收款", "RECV"),
    ("v27_02", "crumple_wh", "qty_sum", 94.0,
     ["WH DOUBLE FOLD V27", "SKU1 qty 45 ok", "SKU2 qty 21 hold", "SKU3 qty 49 ok", "qty_sum TARGET 94"],
     "双折仓单", "RECV"),
    ("v27_03", "rubber_refund", "refund_done", 61.5,
     ["MAGNETIC CLIP REFUND V27", "itemR1 29.00 done", "itemR2 32.50 done", "itemR3 12.00 open", "refund_done TARGET 61.50"],
     "磁夹退款", "DONE"),
    ("v27_04", "clip_tax", "tax_base_paid", 173.0,
     ["TAX THERMAL FADE V27", "T1 96.00 paid", "T2 38.00 open", "T3 77.00 paid", "tax_base_paid TARGET 173.00"],
     "热敏褪色税基", "RECV"),
    ("v27_05", "grease_pay", "payroll_active", 2910.0,
     ["PAYROLL COFFEE SPLASH V27", "A 1490 active", "B 280 leave", "C 1420 active", "payroll_active TARGET 2910"],
     "咖啡溅污工资", "OK"),
    ("v27_06", "carbon_ship", "ship_ok_qty", 83.0,
     ["SHIP LABEL EDGE V27", "P1 42 ok", "P2 22 hold", "P3 41 ok", "ship_ok_qty TARGET 83"],
     "面单边缘发货", "SHIP"),
    ("v27_07", "stamp_sla", "open_pri_sum", 74.0,
     ["SLA WATERMARK DIAG V27", "S1 pri 31 open", "S2 pri 34 closed", "S3 pri 43 open", "open_pri_sum TARGET 74"],
     "水印SLA", "OPEN"),
    ("v27_08", "pocket_exp", "paid_total", 131.75,
     ["EXPENSE PHONE SHADOW V27", "E1 64.00 paid", "E2 25.00 void", "E3 67.75 paid", "paid_total TARGET 131.75"],
     "手机阴影报销", "RECV"),
    ("v27_09", "dust_po", "paid_total", 97.5,
     ["PO-PENCIL SCRIBBLE V27", "itemA paid 47.00", "itemB paid 50.50", "itemC open 16.00", "TOTAL PAID TARGET 97.50"],
     "铅笔涂鸦采购", "RECV"),
    ("v27_10", "binder_order", "paid_total", 85.25,
     ["ORDER STAPLER PUNCTURE V27", "A paid 41.00", "B paid 44.25", "C open 13.00", "TOTAL PAID TARGET 85.25"],
     "订书机孔订单", "RECV"),
    ("v27_11", "perf_dup", "paid_total", 111.0,
     ["INVOICE #V27-PERF", "lineA paid 37.00", "lineB paid 37.00", "lineC paid 37.00", "TOTAL PAID TARGET 111.00"],
     "撕边复写联单", "RECV"),
    ("v27_12", "polaroid_zero", "paid_total", 0.0,
     ["OPEN ONLY V27", "X 71.00 open", "Y 74.00 open", "paid_total TARGET 0.00"],
     "宝丽来未付", "HOLD"),
    ("v27_13", "wb_ledger", "paid_total", 73.5,
     ["LEDGER BLUE PEN CIRCLES V27", "rA paid 35.50", "rB paid 38.00", "rC open 10.00", "TOTAL PAID TARGET 73.50"],
     "蓝笔圈台账", "RECV"),
    ("v27_14", "sticky_ui", "paid_total", 79.0,
     ["UI CORRECTION TAPE V27", "alpha paid 38.00", "beta paid 41.00", "gamma open 13.00", "TOTAL PAID TARGET 79.00"],
     "修正带界面", "RECV"),
    ("v27_15", "pen_stack", "paid_total", 116.75,
     ["HEAVY SKEW STACK V27", "x paid 57.00 usd", "y paid 59.75 usd", "z open 19.00 usd", "TOTAL PAID TARGET 116.75"],
     "倾斜堆叠笔迹", "RECV"),
    ("v27_16", "fax_mix", "paid_total", 70.25,
     ["CN-EN BINDER CLIP TOP V27", "tea paid 34.00", "rice paid 36.25", "soup open 11.00", "TOTAL PAID TARGET 70.25"],
     "长尾夹传真", "RECV"),
    ("v27_17", "env_win", "paid_total", 88.0,
     ["ENVELOPE PEEL CORNER V27", "w1 paid 42.00", "w2 paid 46.00", "w3 open 17.00", "TOTAL PAID TARGET 88.00"],
     "撕角信封窗", "RECV"),
    ("v27_18", "laminate_foot", "paid_total", 54.5,
     ["LAMINATE RECEIPT STACK V27", "p1 paid 26.00", "p2 paid 28.50", "p3 open 9.00", "TOTAL PAID TARGET 54.50"],
     "覆膜收据叠", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V27 Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V26: highlighter cross, magnetic clip, thermal fade, coffee splash edge,
double-fold corner, pencil scribble, stapler puncture, watermark diagonal,
phone shadow, receipt skew stack, blue pen circles, red correction tape,
shipping label edge, binder clip top, sticky peel corner.

Clarity floor from C218/V20-V25 (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V27 uses {jpeg_q})
- photocopy downsample max **/2**
- Gaussian blur radius <= **0.5**
- Protect text band y=70..250
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C255)
- Claim only after smoke

## Honesty
- V26 train/heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C266.
"""


def in_text_band(yy):
    y0, y1 = TEXT_BAND
    return y0 <= yy <= y1


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v27c266") & 0xFFFFFFFF)
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


    # --- V27 overlays (new vs V26) ---
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
    d.text((770, 75), "TRACK #V27-FAKE", fill=(0, 0, 0), font=f_fax)
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

    # --- V27 overlays (new vs V25) ---
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
    d.text((8, 1), "SCAN DESK V27  bait 333.00  PAGE 01", fill=(70, 70, 70), font=f_fax)

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
        f"V27 C266 clarity floor jpeg_q{JPEG_Q} photo/{PHOTOCOPY_DIV}  HLX|MagClip|Thermal|Coffee|DblFold|Pencil|Stapler|WM|Phone|Skew|BluePen|CorrTape|ShipLabel|BinderClip|Peel",
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
            "highlighter_cross", "magnetic_clip", "thermal_fade", "coffee_splash_edge",
            "double_fold_corner", "pencil_scribble", "stapler_puncture", "watermark_diag",
            "phone_shadow", "receipt_skew_stack", "blue_pen_circles", "red_correction_tape",
            "ship_label_edge", "binder_clip_top", "sticky_peel_corner",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c266_clarity_floor",
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
        "version": "v27",
        "n": len(items),
        "gate": GATE,
        "theme": "hlx_magclip_thermal_coffee_dblfold_pencil_stapler_wm_phone_skew_bluepen_corrtape_shiplabel_binderclip_peel",
        "harder_than": "v26_hl_crumple_c260",
        "clarity_floor": {
            "jpeg_q_min": 58,
            "jpeg_q": JPEG_Q,
            "photocopy_div_max": 2,
            "photocopy_div": PHOTOCOPY_DIV,
            "blur_max": 0.5,
            "blur": BLUR_R,
            "text_band_y": list(TEXT_BAND),
            "lesson": "C218 crush + C236 soft_affine; V27 keeps floor",
        },
        "items": items,
        "timestamp": ts(),
        "claim": False,
        "note": "fixtures only; claim deferred to C267 VL smoke",
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C266",
        "theme": "vision_v27_design_and_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "clarity_floor": man["clarity_floor"],
        "vl_gate_v27_claim": False,
        "pass": True,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "C266 design+fixtures; no VL claim",
    }
    J(DOC / "C266_VISION_V27_DESIGN.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
