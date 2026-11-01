# -*- coding: utf-8 -*-
"""C217: Vision V19 design + fixtures (harder than V18).
Hardening: coffee_ring, highlighter_bleed, barcode_strip, ghost_double_exposure,
rubber_stamp_bleed, torn_edge, bic_pen_underline, photocopy_gen, jpeg_q22
(+ residual V18 cues: punch/clip/redact/halftone light). Gate 0.6.
Gate2/3 untouched. gen11 HOLD. No claim until real VL smoke (C218).
"""
from __future__ import annotations
import io, json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v19"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V19_PROTOCOL.md"
RUN = ROOT / "runs/vision_v19_c217"

SPECS = [
    ("v19_01", "coffee_receipt", "paid_total", 93.5,
     ["COFFEE RING V19", "a paid 46.00", "b paid 47.50", "c open 12.00", "TOTAL PAID TARGET 93.50"],
     "咖啡环收据", "RECV"),
    ("v19_02", "hl_wh", "qty_sum", 78.0,
     ["WH HIGHLIGHT V19", "SKU1 qty 41 ok", "SKU2 qty 19 hold", "SKU3 qty 37 ok", "qty_sum TARGET 78"],
     "荧光笔仓", "RECV"),
    ("v19_03", "barcode_refund", "refund_done", 44.75,
     ["BARCODE REFUND V19", "itemR1 21.25 done", "itemR2 23.50 done", "itemR3 9.00 open", "refund_done TARGET 44.75"],
     "条码退款", "DONE"),
    ("v19_04", "ghost_tax", "tax_base_paid", 147.0,
     ["TAX GHOST V19", "T1 82.00 paid", "T2 30.00 open", "T3 65.00 paid", "tax_base_paid TARGET 147.00"],
     "重影税基", "RECV"),
    ("v19_05", "stamp_pay", "payroll_active", 2480.0,
     ["PAYROLL STAMP V19", "A 1310 active", "B 220 leave", "C 1170 active", "payroll_active TARGET 2480"],
     "印泥工资", "OK"),
    ("v19_06", "torn_ship", "ship_ok_qty", 63.0,
     ["SHIP TORN V19", "P1 32 ok", "P2 17 hold", "P3 31 ok", "ship_ok_qty TARGET 63"],
     "撕边发货", "SHIP"),
    ("v19_07", "pen_sla", "open_pri_sum", 55.0,
     ["SLA PEN V19", "S1 pri 24 open", "S2 pri 31 closed", "S3 pri 31 open", "open_pri_sum TARGET 55"],
     "圆珠笔SLA", "OPEN"),
    ("v19_08", "photo_exp", "paid_total", 102.25,
     ["EXPENSE PHOTOCOPY V19", "E1 51.00 paid", "E2 22.00 void", "E3 51.25 paid", "paid_total TARGET 102.25"],
     "复印报销", "RECV"),
    ("v19_09", "coffee_po", "paid_total", 88.0,
     ["PO-COFFEE V19", "itemA paid 43.75", "itemB paid 44.25", "itemC open 15.00", "TOTAL PAID TARGET 88.00"],
     "咖啡环采购", "RECV"),
    ("v19_10", "hl_order", "paid_total", 71.5,
     ["ORDER HIGHLIGHT V19", "A paid 35.50", "B paid 36.00", "C open 11.00", "TOTAL PAID TARGET 71.50"],
     "荧光笔订单", "RECV"),
    ("v19_11", "barcode_dup", "paid_total", 84.0,
     ["INVOICE #V19-DUP", "line paid 28.00", "line paid 28.00", "line paid 28.00", "TOTAL PAID TARGET 84.00"],
     "条码重复", "RECV"),
    ("v19_12", "ghost_zero", "paid_total", 0.0,
     ["OPEN ONLY V19", "X 61.00 open", "Y 64.00 open", "paid_total TARGET 0.00"],
     "重影未付", "HOLD"),
    ("v19_13", "stamp_ledger", "paid_total", 58.75,
     ["LEDGER STAMP V19", "rA paid 29.25", "rB paid 29.50", "rC open 8.00", "TOTAL PAID TARGET 58.75"],
     "印泥台账", "RECV"),
    ("v19_14", "torn_ui", "paid_total", 66.5,
     ["UI TORN V19", "alpha paid 33.00", "beta paid 33.50", "gamma open 10.50", "TOTAL PAID TARGET 66.50"],
     "撕边面板", "RECV"),
    ("v19_15", "pen_stack", "paid_total", 96.0,
     ["HEAVY PEN V19", "x paid 48.00 usd", "y paid 48.00 usd", "z open 19.00 usd", "TOTAL PAID TARGET 96.00"],
     "笔迹堆单", "RECV"),
    ("v19_16", "photo_mix", "paid_total", 61.25,
     ["CN-EN PHOTO MIX V19", "tea paid 29.00", "rice paid 32.25", "soup open 9.00", "TOTAL PAID TARGET 61.25"],
     "中英复印", "RECV"),
    ("v19_17", "coffee_win", "paid_total", 79.0,
     ["COFFEE WIN V19", "w1 paid 39.00", "w2 paid 40.00", "w3 open 16.00", "TOTAL PAID TARGET 79.00"],
     "咖啡环双窗", "RECV"),
    ("v19_18", "hl_foot", "paid_total", 42.5,
     ["HIGHLIGHT FOOT V19", "p1 paid 21.00", "p2 paid 21.50", "p3 open 7.00", "TOTAL PAID TARGET 42.50"],
     "荧光笔脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V19 Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V18: coffee ring, highlighter bleed, barcode strip, ghost double-exposure,
rubber stamp bleed, torn edge, bic pen underline, photocopy generation, jpeg_q22.
Mild-readable TARGET. Scoped office OCR+atom.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke (C218)

## Honesty
- V18 train/heldout retained when claimed
- Gate2/3 untouched. gen11 HOLD. No fake VL scores here.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v19") & 0xFFFFFFFF)
    img = Image.new("RGB", (1100, 740), (195, 190, 180))
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 15)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 13)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 36)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = f_wm = ImageFont.load_default()

    # main card
    d.rectangle([40, 20, 560, 600], fill=(248, 244, 232), outline=(40, 40, 40), width=2)
    # residual V18 wrinkles + LED
    for _ in range(12):
        x0 = rng.randint(45, 520)
        y0 = rng.randint(40, 560)
        d.arc([x0, y0, x0 + rng.randint(40, 120), y0 + rng.randint(20, 60)], 0, 180, fill=(180, 175, 165), width=2)
    for by in range(30, 580, 14):
        d.rectangle([40, by, 560, by + 1], fill=(215, 220, 230))
    # sticky bait
    d.rectangle([370, 210, 540, 300], fill=(255, 248, 100), outline=(180, 160, 40), width=2)
    d.text((380, 220), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((380, 245), "bait 99.99", fill=(80, 60, 20), font=f_tiny)
    d.text((380, 268), "IGNORE", fill=(80, 60, 20), font=f_tiny)

    # punch holes (light residual)
    for (hx, hy) in [(70, 50), (70, 350)]:
        d.ellipse([hx - 10, hy - 10, hx + 10, hy + 10], fill=(195, 190, 180), outline=(60, 60, 60), width=2)

    # binder clip residual
    d.rectangle([250, 8, 340, 32], fill=(40, 40, 50))

    # highlighter bleed bands (yellow/pink over body, not wiping TARGET contrast)
    d.rectangle([55, 95, 520, 118], fill=(255, 255, 80))
    d.rectangle([55, 140, 480, 162], fill=(255, 140, 220))
    d.rectangle([55, 185, 500, 206], fill=(255, 255, 100))

    # barcode strip (right of card left edge)
    bx0 = 548
    for i in range(40):
        w = 1 if rng.random() < 0.55 else 2
        col = (10, 10, 10) if rng.random() < 0.7 else (240, 240, 240)
        d.rectangle([bx0 + i * 2, 80, bx0 + i * 2 + w, 280], fill=col)
    d.text((bx0, 290), "||BAR|| bait 777", fill=(30, 30, 30), font=f_tiny)

    # coffee ring
    for r in range(70, 95, 3):
        d.ellipse([160 - r, 320 - r, 160 + r, 320 + r], outline=(120, 80, 40), width=2)
    d.ellipse([120, 280, 200, 360], fill=(140, 95, 50, ) if False else (210, 175, 130))

    # rubber stamp bleed circles
    for (cx, cy, label, col) in [
        (430, 130, stamp, (180, 30, 30)),
        (300, 260, "作废", (140, 50, 50)),
        (470, 340, "VOID", (150, 40, 40)),
        (200, 480, "COPY", (60, 60, 160)),
    ]:
        d.ellipse([cx - 48, cy - 24, cx + 42, cy + 28], outline=col, width=4)
        d.text((cx - 16, cy - 6), label[:4], fill=col, font=f_stamp)

    # bic pen underlines through amount lines
    for uy in (100, 122, 144, 166, 188, 210):
        d.line([(58, uy + 14), (500, uy + 16)], fill=(20, 40, 160), width=2)

    # ghost double-exposure: faint shifted duplicate of title area later after text

    # redaction residual on void win
    d.rectangle([780, 80, 1040, 110], fill=(10, 10, 10))
    d.text((790, 120), "REDACTED bait 555", fill=(40, 40, 40), font=f_tiny)

    d.text((90, 330), "CONFIDENTIAL", fill=(230, 225, 215), font=f_wm)
    d.rectangle([50, 28, 340, 58], fill=(30, 50, 70))
    d.text((56, 32), (cn_title or kind)[:20], fill=(240, 240, 240), font=f_title)
    y = 72
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        # ghost (shifted faint)
        d.text((62, y + 3), ln[:54], fill=(190, 185, 175), font=font)
        d.text((58 + 2, y + 1), ln[:54], fill=(210, 205, 195), font=font)
        d.text((58, y), ln[:54], fill=(8, 8, 8), font=font)
        y += 22

    # void win decoy
    d.rectangle([760, 220, 1060, 450], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((770, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 265), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 300), "do not parse", fill=(20, 20, 20), font=f_sm)
    d.rectangle([0, 710, 1100, 740], fill=(18, 18, 28))
    d.text((10, 718), "V19 Coffee|HL|Barcode|Ghost|Stamp|Torn|Pen|Photocopy q22  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)

    # torn edge: chew left/bottom of card
    px = img.load()
    ww, hh = img.size
    for yy in range(20, 600):
        tear = int(8 + 6 * ((yy // 17) % 3) + rng.randint(0, 5))
        for xx in range(40, 40 + tear):
            if 0 <= xx < ww and 0 <= yy < hh:
                px[xx, yy] = (195, 190, 180)
    for xx in range(40, 560):
        tear = int(4 + 5 * ((xx // 23) % 2) + rng.randint(0, 4))
        for yy in range(600 - tear, 610):
            if 0 <= xx < ww and 0 <= yy < hh:
                px[xx, yy] = (195, 190, 180)

    # light residual halftone
    for y0 in range(40, 600, 6):
        for x0 in range(50, 540, 6):
            if rng.random() < 0.22:
                v = rng.randint(20, 70)
                if x0 < ww and y0 < hh:
                    r, g, b = px[x0, y0]
                    px[x0, y0] = (max(0, r - v), max(0, g - v), max(0, b - v))

    # coffee stain blotches
    for _ in range(5):
        cx, cy = rng.randint(80, 480), rng.randint(100, 500)
        for dy in range(-25, 26):
            for dx in range(-25, 26):
                if dx * dx + dy * dy < 25 * 25 and rng.random() < 0.55:
                    xx, yy = cx + dx, cy + dy
                    if 0 <= xx < ww and 0 <= yy < hh:
                        r, g, b = px[xx, yy]
                        px[xx, yy] = (max(0, r - 35), max(0, g - 45), max(0, b - 55))

    # dust
    for _ in range(2200):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)

    img = ImageEnhance.Color(img).enhance(0.45)
    img = ImageEnhance.Contrast(img).enhance(0.68)
    img = ImageEnhance.Brightness(img).enhance(0.64)
    # photocopy generation: downscale then upscale
    w, h = img.size
    small = img.resize((w // 3, h // 3), Image.BILINEAR)
    img = small.resize((w, h), Image.BILINEAR)
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.11, -36, 0.04, 1, -14),
        resample=Image.BICUBIC, fillcolor=(195, 190, 180),
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=1.35))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=22)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    img = img.filter(ImageFilter.SMOOTH)
    outp = FIX / f"{fid}_{kind}.png"
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "hardening": [
            "coffee_ring", "highlighter_bleed", "barcode_strip", "ghost_double_exposure",
            "rubber_stamp_bleed", "torn_edge", "bic_pen_underline", "photocopy_gen",
            "jpeg_q22",
        ],
    }


def main():
    PROTO.write_text(PROTOCOL.format(ts=ts()), encoding="utf-8")
    if FIX.exists():
        for p in FIX.glob("*.png"):
            p.unlink()
    items = []
    for fid, kind, metric, expected, lines, cn, stamp in SPECS:
        items.append(make_fixture(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v19", "n": len(items), "gate": GATE,
        "theme": "coffee_hl_barcode_ghost_stamp_torn_pen_photocopy",
        "harder_than": "v18",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C217",
        "theme": "vision_v19_design_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "harder_than": "v18",
        "pass": len(items) >= 16,
        "claim": False,
        "note": "fixtures only; claim deferred to C218 VL smoke",
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C217_V19_DESIGN_BATCH.json", out)
    J(RUN / "batch.json", out)
    print(json.dumps({"cycle": "C217", "n": len(items), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
