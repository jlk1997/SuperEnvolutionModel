# -*- coding: utf-8 -*-
"""C197: Vision V16 design + fixtures (harder than V15).
Hardening: double exposure, LED banding, rain streaks, crumpled shadow,
postage stamp stack, plastic wrap glare, highlighter bleed, torn barcode,
microwave moire, dust speckle, sepia age, jpeg_q36 (plus residual V15 cues).
Gate 0.6. Gate2/3 untouched. gen11 HOLD. No claim until real VL smoke.
"""
from __future__ import annotations
import io, json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v16"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V16_PROTOCOL.md"
RUN = ROOT / "runs/vision_v16_c197"

SPECS = [
    ("v16_01", "dbl_receipt", "paid_total", 63.5,
     ["DBL EXPOSURE V16", "a paid 31.00", "b paid 32.50", "c open 9.00", "TOTAL PAID TARGET 63.50"],
     "双重曝光收据", "RECV"),
    ("v16_02", "led_wh", "qty_sum", 53.0,
     ["WH LED BAND V16", "SKU1 qty 27 ok", "SKU2 qty 12 hold", "SKU3 qty 26 ok", "qty_sum TARGET 53"],
     "灯带仓单", "RECV"),
    ("v16_03", "rain_refund", "refund_done", 29.25,
     ["RAIN REFUND V16", "itemR1 14.00 done", "itemR2 15.25 done", "itemR3 6.00 open", "refund_done TARGET 29.25"],
     "雨痕退款", "DONE"),
    ("v16_04", "crumple_tax", "tax_base_paid", 96.0,
     ["TAX CRUMPLE V16", "T1 52.00 paid", "T2 20.00 open", "T3 44.00 paid", "tax_base_paid TARGET 96.00"],
     "褶皱税联", "RECV"),
    ("v16_05", "postage_pay", "payroll_active", 1680.0,
     ["PAYROLL POSTAGE V16", "A 900 active", "B 140 leave", "C 780 active", "payroll_active TARGET 1680"],
     "邮戳薪资", "OK"),
    ("v16_06", "wrap_ship", "ship_ok_qty", 39.0,
     ["SHIP WRAP V16", "P1 20 ok", "P2 12 hold", "P3 19 ok", "ship_ok_qty TARGET 39"],
     "保鲜膜发货", "SHIP"),
    ("v16_07", "hl_sla", "open_pri_sum", 36.0,
     ["SLA HIGHLIGHT V16", "S1 pri 16 open", "S2 pri 22 closed", "S3 pri 20 open", "open_pri_sum TARGET 36"],
     "荧光笔SLA", "OPEN"),
    ("v16_08", "torn_exp", "paid_total", 71.25,
     ["EXPENSE TORNBC V16", "E1 36.00 paid", "E2 14.00 void", "E3 35.25 paid", "paid_total TARGET 71.25"],
     "撕条码报销", "RECV"),
    ("v16_09", "mw_po", "paid_total", 61.0,
     ["PO-MICROWAVE V16", "itemA paid 30.50", "itemB paid 30.50", "itemC open 11.00", "TOTAL PAID TARGET 61.00"],
     "微波采购", "RECV"),
    ("v16_10", "dust_order", "paid_total", 48.75,
     ["ORDER DUST V16", "A paid 24.00", "B paid 24.75", "C open 8.00", "TOTAL PAID TARGET 48.75"],
     "尘斑订单", "RECV"),
    ("v16_11", "sepia_dup", "paid_total", 57.0,
     ["INVOICE #V16-DUP", "line paid 19.00", "line paid 19.00", "line paid 19.00", "TOTAL PAID TARGET 57.00"],
     "泛黄重复", "RECV"),
    ("v16_12", "rain_zero", "paid_total", 0.0,
     ["OPEN ONLY V16", "X 41.00 open", "Y 44.00 open", "paid_total TARGET 0.00"],
     "雨痕未付", "HOLD"),
    ("v16_13", "dbl_ledger", "paid_total", 39.25,
     ["LEDGER DBL V16", "rA paid 19.50", "rB paid 19.75", "rC open 5.50", "TOTAL PAID TARGET 39.25"],
     "双重账本", "RECV"),
    ("v16_14", "led_ui", "paid_total", 46.5,
     ["UI LED V16", "alpha paid 23.00", "beta paid 23.50", "gamma open 7.50", "TOTAL PAID TARGET 46.50"],
     "灯带界面", "RECV"),
    ("v16_15", "wrap_stack", "paid_total", 66.0,
     ["HEAVY WRAP V16", "x paid 33.00 usd", "y paid 33.00 usd", "z open 14.00 usd", "TOTAL PAID TARGET 66.00"],
     "保鲜膜叠窗", "RECV"),
    ("v16_16", "hl_mix", "paid_total", 40.25,
     ["CN-EN HL MIX V16", "tea paid 18.00", "rice paid 22.25", "soup open 6.00", "TOTAL PAID TARGET 40.25"],
     "中英荧光笔", "RECV"),
    ("v16_17", "crumple_win", "paid_total", 55.0,
     ["CRUMPLE WIN V16", "w1 paid 27.00", "w2 paid 28.00", "w3 open 13.00", "TOTAL PAID TARGET 55.00"],
     "褶皱双窗", "RECV"),
    ("v16_18", "postage_foot", "paid_total", 28.5,
     ["POSTAGE FOOT V16", "p1 paid 14.00", "p2 paid 14.50", "p3 open 5.00", "TOTAL PAID TARGET 28.50"],
     "邮戳脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V16 Protocol — Double / LED / Rain / Crumple / Postage / Wrap / Highlight / Dust / Sepia

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V15: **double exposure**, **LED banding**, **rain streaks**,
**crumpled shadow**, **postage stamp stack**, **plastic wrap glare**,
**highlighter bleed**, **torn barcode**, **microwave moire**, **dust speckle**,
**sepia age**, **jpeg_q36**. Still scoped office OCR+atom. Mild-readable TARGET.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke (C198)

## Honesty
- V15 train/heldout retained when claimed
- Gate2/3 untouched. gen11 HOLD. No fake VL scores here.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v16") & 0xFFFFFFFF)
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
    d.text((10, 718), "V16 Dbl|LED|Rain|Crumple|Postage|Wrap|HL|Dust|Sepia  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)

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
    img = ImageEnhance.Contrast(img).enhance(0.82)
    img = ImageEnhance.Brightness(img).enhance(0.72)

    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.06, -20, 0.022, 1, -7),
        resample=Image.BICUBIC, fillcolor=(188, 182, 172),
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=1.05))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=36)
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
            "double_exposure", "led_banding", "rain_streaks", "crumpled_shadow",
            "postage_stamp_stack", "plastic_wrap_glare", "highlighter_bleed",
            "torn_barcode", "microwave_moire", "dust_speckle", "sepia_age", "jpeg_q36",
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
        "version": "v16", "n": len(items), "gate": GATE,
        "theme": "dbl_led_rain_crumple_postage_wrap_hl_dust_sepia",
        "harder_than": "v15",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C197",
        "theme": "vision_v16_design_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "harder_than": "v15",
        "pass": len(items) >= 16,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "Fixtures only; claim deferred to C198 smoke",
    }
    J(DOC / "C197_V16_DESIGN_BATCH.json", out)
    RUN.mkdir(parents=True, exist_ok=True)
    J(RUN / "design.json", out)
    print(json.dumps({"cycle": "C197", "n": len(items), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
