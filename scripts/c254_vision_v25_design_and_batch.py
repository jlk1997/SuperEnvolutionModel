# -*- coding: utf-8 -*-
"""C254: Vision V25 design + fixtures (harder than V24, clarity floor).
NEW themes vs V24: fingerprint_smudge, rain_streak, staple_shadow, qr_bait,
receipt_curl, fluorescent_flare, desk_clutter, ink_bleed_stamp, torn_margin,
zigzag_crease, tape_coffee_combo, barcode_edge, moire_mild, water_ring_stack.
CLARITY FLOOR: jpeg_q>=58, photocopy max /2, blur<=0.5, protect text band y=70..250.
No claim until C255 VL. Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import io, json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v25"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V25_PROTOCOL.md"
RUN = ROOT / "runs/vision_v25_c254"

JPEG_Q = 60
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)

SPECS = [
    ("v25_01", "fp_recv", "paid_total", 82.0,
     ["FINGERPRINT RECV V25", "a paid 40.00", "b paid 42.00", "c open 12.00", "TOTAL PAID TARGET 82.00"],
     "指纹污收据", "RECV"),
    ("v25_02", "rain_wh", "qty_sum", 73.0,
     ["WH RAIN STREAK V25", "SKU1 qty 35 ok", "SKU2 qty 16 hold", "SKU3 qty 38 ok", "qty_sum TARGET 73"],
     "雨痕仓单", "RECV"),
    ("v25_03", "staple_refund", "refund_done", 44.25,
     ["STAPLE SHADOW REFUND V25", "itemR1 20.00 done", "itemR2 24.25 done", "itemR3 9.00 open", "refund_done TARGET 44.25"],
     "订书影退款", "DONE"),
    ("v25_04", "qr_tax", "tax_base_paid", 139.0,
     ["TAX QR BAIT V25", "T1 78.00 paid", "T2 31.00 open", "T3 61.00 paid", "tax_base_paid TARGET 139.00"],
     "二维码税基", "RECV"),
    ("v25_05", "curl_pay", "payroll_active", 2450.0,
     ["PAYROLL CURL EDGE V25", "A 1260 active", "B 240 leave", "C 1190 active", "payroll_active TARGET 2450"],
     "卷边工资", "OK"),
    ("v25_06", "flare_ship", "ship_ok_qty", 62.0,
     ["SHIP FLUOR FLARE V25", "P1 31 ok", "P2 17 hold", "P3 31 ok", "ship_ok_qty TARGET 62"],
     "荧光发货", "SHIP"),
    ("v25_07", "clutter_sla", "open_pri_sum", 58.0,
     ["SLA DESK CLUTTER V25", "S1 pri 25 open", "S2 pri 29 closed", "S3 pri 33 open", "open_pri_sum TARGET 58"],
     "桌面杂SLA", "OPEN"),
    ("v25_08", "ink_exp", "paid_total", 103.5,
     ["EXPENSE INK BLEED V25", "E1 51.00 paid", "E2 19.00 void", "E3 52.50 paid", "paid_total TARGET 103.50"],
     "印泥报销", "RECV"),
    ("v25_09", "torn_po", "paid_total", 81.0,
     ["PO-TORN MARGIN V25", "itemA paid 39.00", "itemB paid 42.00", "itemC open 14.00", "TOTAL PAID TARGET 81.00"],
     "撕边采购", "RECV"),
    ("v25_10", "zig_order", "paid_total", 70.25,
     ["ORDER ZIGZAG CREASE V25", "A paid 34.00", "B paid 36.25", "C open 11.00", "TOTAL PAID TARGET 70.25"],
     "折痕订单", "RECV"),
    ("v25_11", "combo_dup", "paid_total", 90.0,
     ["INVOICE #V25-COMBO", "line paid 30.00", "line paid 30.00", "line paid 30.00", "TOTAL PAID TARGET 90.00"],
     "胶带咖啡重复", "RECV"),
    ("v25_12", "barcode_zero", "paid_total", 0.0,
     ["OPEN ONLY V25", "X 58.00 open", "Y 61.00 open", "paid_total TARGET 0.00"],
     "条码未付", "HOLD"),
    ("v25_13", "moire_ledger", "paid_total", 59.75,
     ["LEDGER MOIRE MILD V25", "rA paid 29.00", "rB paid 30.75", "rC open 8.00", "TOTAL PAID TARGET 59.75"],
     "轻摩尔台账", "RECV"),
    ("v25_14", "rings_ui", "paid_total", 63.0,
     ["UI WATER RINGS V25", "alpha paid 30.50", "beta paid 32.50", "gamma open 11.00", "TOTAL PAID TARGET 63.00"],
     "水环窗口", "RECV"),
    ("v25_15", "fp_stack", "paid_total", 95.5,
     ["HEAVY FP STACK V25", "x paid 47.00 usd", "y paid 48.50 usd", "z open 17.00 usd", "TOTAL PAID TARGET 95.50"],
     "指纹堆单", "RECV"),
    ("v25_16", "rain_mix", "paid_total", 57.5,
     ["CN-EN RAIN MIX V25", "tea paid 28.00", "rice paid 29.50", "soup open 9.00", "TOTAL PAID TARGET 57.50"],
     "中英雨痕", "RECV"),
    ("v25_17", "staple_win", "paid_total", 72.0,
     ["STAPLE WIN V25", "w1 paid 35.00", "w2 paid 37.00", "w3 open 15.00", "TOTAL PAID TARGET 72.00"],
     "订书双窗", "RECV"),
    ("v25_18", "curl_foot", "paid_total", 42.25,
     ["CURL FOOT V25", "p1 paid 20.00", "p2 paid 22.25", "p3 open 7.00", "TOTAL PAID TARGET 42.25"],
     "卷边脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V25 Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V24: fingerprint smudge, rain streak, staple shadow, QR bait,
receipt curl, fluorescent flare, desk clutter, ink bleed stamp, torn margin,
zigzag crease, tape+coffee combo, barcode edge, mild moire, water ring stack.
Clarity floor from C218/V20-V24 (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V25 uses {jpeg_q})
- photocopy downsample max **/2**
- Gaussian blur radius <= **0.5**
- Protect text band y=70..250
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C255)
- Claim only after smoke

## Honesty
- V24 train/heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C254.
"""


def in_text_band(yy):
    y0, y1 = TEXT_BAND
    return y0 <= yy <= y1


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v25c254") & 0xFFFFFFFF)
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

    # staple shadow top-left
    d.ellipse([48, 28, 78, 48], fill=(90, 90, 100))
    d.ellipse([52, 32, 74, 44], fill=(60, 60, 70))

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
    d.text((8, 1), "SCAN DESK V25  bait 333.00  PAGE 01", fill=(70, 70, 70), font=f_fax)

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
        f"V25 C254 clarity floor jpeg_q{JPEG_Q} photo/{PHOTOCOPY_DIV}  FP|Rain|Staple|QR|Curl|Flare|Clutter|Ink|Torn|Zig|Combo|Barcode|Moire|Rings",
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
            "fingerprint_smudge", "rain_streak", "staple_shadow", "qr_bait",
            "receipt_curl", "fluorescent_flare", "desk_clutter", "ink_bleed_stamp",
            "torn_margin", "zigzag_crease", "tape_coffee_combo", "barcode_edge",
            "moire_mild", "water_ring_stack",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c254_clarity_floor",
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
        "version": "v25",
        "n": len(items),
        "gate": GATE,
        "theme": "fp_rain_staple_qr_curl_flare_clutter_ink_torn_zig_combo_barcode_moire_rings",
        "harder_than": "v24_coffee_binder_tape_pen_c248",
        "clarity_floor": {
            "jpeg_q_min": 58,
            "jpeg_q": JPEG_Q,
            "photocopy_div_max": 2,
            "photocopy_div": PHOTOCOPY_DIV,
            "blur_max": 0.5,
            "blur": BLUR_R,
            "text_band_y": list(TEXT_BAND),
            "lesson": "C218 crush + C236 soft_affine; V25 keeps floor",
        },
        "items": items,
        "timestamp": ts(),
        "claim": False,
        "note": "fixtures only; claim deferred to C255 VL smoke",
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C254",
        "theme": "vision_v25_design_and_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "clarity_floor": man["clarity_floor"],
        "vl_gate_v25_claim": False,
        "pass": True,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "C254 design+fixtures; no VL claim",
    }
    J(DOC / "C254_VISION_V25_DESIGN.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
