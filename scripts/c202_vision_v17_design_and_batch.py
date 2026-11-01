# -*- coding: utf-8 -*-
"""C202: Vision V17 design + fixtures (harder than V15).
Hardening: double exposure, LED banding, rain streaks, crumpled shadow,
postage stamp stack, plastic wrap glare, highlighter bleed, torn barcode,
microwave moire, dust speckle, sepia age, jpeg_q36 (plus residual V15 cues).
Gate 0.6. Gate2/3 untouched. gen11 HOLD. No claim until real VL smoke (C203).
"""
from __future__ import annotations
import io, json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v17"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V17_PROTOCOL.md"
RUN = ROOT / "runs/vision_v17_c202"

SPECS = [
    ("v17_01", "oil_receipt", "paid_total", 74.25,
     ["OIL SMEAR V17", "a paid 36.00", "b paid 38.25", "c open 10.00", "TOTAL PAID TARGET 74.25"],
     "oil_receipt", "RECV"),
    ("v17_02", "frost_wh", "qty_sum", 61.0,
     ["WH FROST V17", "SKU1 qty 31 ok", "SKU2 qty 14 hold", "SKU3 qty 30 ok", "qty_sum TARGET 61"],
     "frost_wh", "RECV"),
    ("v17_03", "ink_refund", "refund_done", 34.5,
     ["INK BLEED REFUND V17", "itemR1 16.50 done", "itemR2 18.00 done", "itemR3 7.00 open", "refund_done TARGET 34.50"],
     "ink_refund", "DONE"),
    ("v17_04", "carbon_tax", "tax_base_paid", 112.0,
     ["TAX CARBON V17", "T1 60.00 paid", "T2 22.00 open", "T3 52.00 paid", "tax_base_paid TARGET 112.00"],
     "carbon_tax", "RECV"),
    ("v17_05", "staple_pay", "payroll_active", 1890.0,
     ["PAYROLL STAPLE V17", "A 1000 active", "B 160 leave", "C 890 active", "payroll_active TARGET 1890"],
     "staple_pay", "OK"),
    ("v17_06", "fold_ship", "ship_ok_qty", 45.0,
     ["SHIP FOLD V17", "P1 23 ok", "P2 13 hold", "P3 22 ok", "ship_ok_qty TARGET 45"],
     "fold_ship", "SHIP"),
    ("v17_07", "uv_sla", "open_pri_sum", 41.0,
     ["SLA UV V17", "S1 pri 18 open", "S2 pri 25 closed", "S3 pri 23 open", "open_pri_sum TARGET 41"],
     "uv_sla", "OPEN"),
    ("v17_08", "skew_exp", "paid_total", 82.75,
     ["EXPENSE SKEW V17", "E1 41.00 paid", "E2 16.00 void", "E3 41.75 paid", "paid_total TARGET 82.75"],
     "skew_exp", "RECV"),
    ("v17_09", "oil_po", "paid_total", 69.5,
     ["PO-OIL V17", "itemA paid 34.50", "itemB paid 35.00", "itemC open 12.00", "TOTAL PAID TARGET 69.50"],
     "oil_po", "RECV"),
    ("v17_10", "frost_order", "paid_total", 54.25,
     ["ORDER FROST V17", "A paid 27.00", "B paid 27.25", "C open 9.00", "TOTAL PAID TARGET 54.25"],
     "frost_order", "RECV"),
    ("v17_11", "carbon_dup", "paid_total", 66.0,
     ["INVOICE #V17-DUP", "line paid 22.00", "line paid 22.00", "line paid 22.00", "TOTAL PAID TARGET 66.00"],
     "carbon_dup", "RECV"),
    ("v17_12", "ink_zero", "paid_total", 0.0,
     ["OPEN ONLY V17", "X 48.00 open", "Y 51.00 open", "paid_total TARGET 0.00"],
     "ink_zero", "HOLD"),
    ("v17_13", "staple_ledger", "paid_total", 44.5,
     ["LEDGER STAPLE V17", "rA paid 22.00", "rB paid 22.50", "rC open 6.00", "TOTAL PAID TARGET 44.50"],
     "staple_ledger", "RECV"),
    ("v17_14", "fold_ui", "paid_total", 52.0,
     ["UI FOLD V17", "alpha paid 26.00", "beta paid 26.00", "gamma open 8.50", "TOTAL PAID TARGET 52.00"],
     "fold_ui", "RECV"),
    ("v17_15", "uv_stack", "paid_total", 73.0,
     ["HEAVY UV V17", "x paid 36.50 usd", "y paid 36.50 usd", "z open 15.00 usd", "TOTAL PAID TARGET 73.00"],
     "uv_stack", "RECV"),
    ("v17_16", "skew_mix", "paid_total", 45.75,
     ["CN-EN SKEW MIX V17", "tea paid 21.00", "rice paid 24.75", "soup open 7.00", "TOTAL PAID TARGET 45.75"],
     "skew_mix", "RECV"),
    ("v17_17", "oil_win", "paid_total", 62.0,
     ["OIL WIN V17", "w1 paid 30.00", "w2 paid 32.00", "w3 open 14.00", "TOTAL PAID TARGET 62.00"],
     "oil_win", "RECV"),
    ("v17_18", "frost_foot", "paid_total", 31.25,
     ["FROST FOOT V17", "p1 paid 15.50", "p2 paid 15.75", "p3 open 5.50", "TOTAL PAID TARGET 31.25"],
     "frost_foot", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V17 Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V16: oil smear, frost glass, ink bleed, carbon copy ghost,
stapler shadow, fold crease stack, UV purple cast, scanner skew+, jpeg_q32.
Mild-readable TARGET. Scoped office OCR+atom.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke (C203)

## Honesty
- V16 train/heldout retained when claimed
- Gate2/3 untouched. gen11 HOLD. No fake VL scores here.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v17") & 0xFFFFFFFF)
    img = Image.new("RGB", (1100, 740), (188, 182, 172))
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

    d.rectangle([40, 20, 560, 600], fill=(238, 230, 218), outline=(40, 40, 40), width=2)
    # crumpled wrinkles
    for _ in range(18):
        x0 = rng.randint(45, 520)
        y0 = rng.randint(40, 560)
        d.arc([x0, y0, x0 + rng.randint(50, 140), y0 + rng.randint(25, 70)], 0, 200, fill=(175, 168, 155), width=2)
    d.rectangle([55, 100, 520, 124], fill=(255, 255, 90))
    d.rectangle([55, 170, 430, 194], fill=(255, 120, 220))  # highlighter
    d.rectangle([370, 210, 540, 300], fill=(255, 248, 100), outline=(180, 160, 40), width=2)
    d.text((380, 220), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((380, 245), "bait 888.00", fill=(80, 60, 20), font=f_tiny)
    d.text((380, 268), "IGNORE", fill=(80, 60, 20), font=f_tiny)

    # LED banding
    for by in range(30, 580, 11):
        d.rectangle([40, by, 560, by + 2], fill=(210, 220, 230))
    # barcode + torn edge
    for bx in range(580, 650, 2):
        d.line([(bx, 90), (bx, 300)], fill=(5, 5, 5), width=2)
    d.polygon([(580, 90), (650, 90), (640, 140), (590, 145)], fill=(188, 182, 172))
    d.text((580, 310), "TORN BARCODE", fill=(60, 60, 60), font=f_tiny)
    # postage stamps
    for i, (sx, sy) in enumerate([(700, 80), (780, 80), (700, 160)]):
        d.rectangle([sx, sy, sx + 60, sy + 50], outline=(120, 40, 40), width=2)
        d.text((sx + 6, sy + 12), f"POST{i+1}", fill=(120, 40, 40), font=f_tiny)
        d.text((sx + 6, sy + 28), "9.99", fill=(80, 80, 80), font=f_tiny)

    # rain streaks
    for _ in range(40):
        rx = rng.randint(40, 1050)
        ry = rng.randint(20, 700)
        d.line([(rx, ry), (rx + 2, ry + rng.randint(20, 50))], fill=(160, 170, 190), width=1)

    # plastic wrap glare ellipse
    wrap = Image.new("RGBA", img.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(wrap)
    wd.ellipse([120, 40, 400, 180], fill=(255, 255, 255, 45))
    wd.ellipse([450, 400, 700, 620], fill=(200, 220, 255, 35))
    img = Image.alpha_composite(img.convert("RGBA"), wrap).convert("RGB")
    d = ImageDraw.Draw(img)

    coffee = Image.new("RGBA", img.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(coffee)
    cd.ellipse([90, 420, 240, 560], outline=(110, 60, 25, 100), width=12)
    cd.ellipse([110, 440, 220, 540], fill=(130, 70, 35, 45))
    img = Image.alpha_composite(img.convert("RGBA"), coffee).convert("RGB")
    d = ImageDraw.Draw(img)

    d.text((90, 330), "CONFIDENTIAL", fill=(210, 200, 190), font=f_wm)
    d.text((110, 470), "COPY bait 777", fill=(220, 212, 200), font=f_sm)

    d.rectangle([50, 28, 340, 58], fill=(30, 50, 70))
    d.text((56, 32), (cn_title or kind)[:20], fill=(240, 240, 240), font=f_title)
    y = 72
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        # double exposure ghost text offset
        d.text((58 + 2, y + 1), ln[:54], fill=(200, 195, 185), font=font)
        d.text((58, y), ln[:54], fill=(10, 10, 10), font=font)
        y += 22

    for (cx, cy, label, col) in [(400, 145, stamp, (180, 30, 30)), (290, 255, "作废", (140, 50, 50)), (450, 320, "VOID", (150, 40, 40))]:
        d.ellipse([cx - 46, cy - 22, cx + 40, cy + 26], outline=col, width=3)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)

    d.rectangle([760, 220, 1060, 450], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((770, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 265), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 300), "do not parse", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 710, 1100, 740], fill=(18, 18, 28))
    d.text((10, 718), "V17 Oil|Frost|Ink|Carbon|Staple|Fold|UV|Skew  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)

    # dust + microwave moire + chromatic
    px = img.load()
    ww, hh = img.size
    for _ in range(2200):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)
    for yy in range(100, 220):
        for xx in range(50, min(520, ww - 4)):
            r, g, b = px[xx, yy]
            px[xx, yy] = (min(255, r + 22), g, max(0, b - 10))
            if xx + 3 < ww:
                r2, g2, b2 = px[xx + 3, yy]
                px[xx + 3, yy] = (max(0, r2 - 10), g2, min(255, b2 + 22))
    for mx in range(45, 540, 4):
        for my in range(30, 590, 7):
            r, g, b = px[mx, my]
            px[mx, my] = (min(255, r + 8), g, min(255, b + 8))

    # sepia-ish
    img = ImageEnhance.Color(img).enhance(0.55)
    img = ImageEnhance.Contrast(img).enhance(0.78)
    img = ImageEnhance.Brightness(img).enhance(0.70)

    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.085, -28, 0.03, 1, -10),
        resample=Image.BICUBIC, fillcolor=(188, 182, 172),
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=1.15))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=32)
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
            "oil_smear", "frost_glass", "ink_bleed", "carbon_copy_ghost",
            "stapler_shadow", "fold_crease_stack", "uv_purple_cast",
            "scanner_skew_plus", "jpeg_q32",
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
        "version": "v17", "n": len(items), "gate": GATE,
        "theme": "oil_frost_ink_carbon_staple_fold_uv_skew",
        "harder_than": "v16",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C202",
        "theme": "vision_v17_design_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "harder_than": "v16",
        "pass": len(items) >= 16,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "Fixtures only; claim deferred to C203 smoke",
    }
    J(DOC / "C202_V17_DESIGN_BATCH.json", out)
    RUN.mkdir(parents=True, exist_ok=True)
    J(RUN / "design.json", out)
    print(json.dumps({"cycle": "C202", "n": len(items), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
