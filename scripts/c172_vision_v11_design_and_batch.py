# -*- coding: utf-8 -*-
"""C172: Vision V11 design + fixtures (harder than V10).
Hardening: glare, skew shear, handwriting overlay, redaction bars,
night low-contrast, mosaic patches, stamp-over-digits, dual-FX bait,
excel grid crosstalk, partial TARGET crop.
Gate 0.6. Gate2/3 untouched. gen11 HOLD. No claim until real VL smoke.
"""
from __future__ import annotations
import json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v11"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V11_PROTOCOL.md"
RUN = ROOT / "runs/vision_v11_c172"

SPECS = [
    ("v11_01", "glare_receipt", "paid_total", 24.25,
     ["GLARE RECEIPT V11", "a paid 11.00", "b paid 13.25", "c open 5.00", "TOTAL PAID TARGET 24.25"],
     "眩光收据", "RECV"),
    ("v11_02", "skew_wh", "qty_sum", 31.0,
     ["WH SKEW V11", "SKU1 qty 17 ok", "SKU2 qty 4 hold", "SKU3 qty 14 ok", "qty_sum TARGET 31"],
     "斜切仓单", "RECV"),
    ("v11_03", "hand_refund", "refund_done", 13.75,
     ["HAND REFUND V11", "itemR1 5.25 done", "itemR2 8.50 done", "itemR3 2.00 open", "refund_done TARGET 13.75"],
     "手写干扰退款", "DONE"),
    ("v11_04", "redact_tax", "tax_base_paid", 41.0,
     ["TAX REDACT V11", "T1 22.00 paid", "T2 10.00 open", "T3 19.00 paid", "tax_base_paid TARGET 41.00"],
     "涂黑税联", "RECV"),
    ("v11_05", "night_payroll", "payroll_active", 970.0,
     ["PAYROLL NIGHT V11", "A 510 active", "B 120 leave", "C 460 active", "payroll_active TARGET 970"],
     "夜色薪资", "OK"),
    ("v11_06", "mosaic_ship", "ship_ok_qty", 21.0,
     ["SHIP MOSAIC V11", "P1 12 ok", "P2 7 hold", "P3 9 ok", "ship_ok_qty TARGET 21"],
     "马赛克发货", "SHIP"),
    ("v11_07", "stampdig_sla", "open_pri_sum", 15.0,
     ["SLA STAMPDIG V11", "S1 pri 8 open", "S2 pri 12 closed", "S3 pri 7 open", "open_pri_sum TARGET 15"],
     "盖章压字SLA", "OPEN"),
    ("v11_08", "fx_exp", "paid_total", 44.5,
     ["EXPENSE FX V11", "E1 25.00 paid", "E2 8.50 void", "E3 19.50 paid", "paid_total TARGET 44.50"],
     "双币报销", "RECV"),
    ("v11_09", "excel_po", "paid_total", 38.25,
     ["PO-EXCEL V11", "itemA paid 20.00", "itemB paid 18.25", "itemC open 7.00", "TOTAL PAID TARGET 38.25"],
     "表格串扰采购", "RECV"),
    ("v11_10", "crop_order", "paid_total", 27.5,
     ["ORDER CROP V11", "A paid 15.25", "B paid 12.25", "C open 4.00", "TOTAL PAID TARGET 27.50"],
     "裁切订单", "RECV"),
    ("v11_11", "glare_dup", "paid_total", 30.0,
     ["INVOICE #V11-DUP", "line paid 10.00", "line paid 10.00", "line paid 10.00", "TOTAL PAID TARGET 30.00"],
     "眩光重复", "RECV"),
    ("v11_12", "night_zero", "paid_total", 0.0,
     ["OPEN ONLY V11", "X 14.00 open", "Y 16.00 open", "paid_total TARGET 0.00"],
     "夜色未付", "HOLD"),
    ("v11_13", "hand_ledger", "paid_total", 17.5,
     ["LEDGER HAND V11", "rA paid 8.75", "rB paid 8.75", "rC open 3.00", "TOTAL PAID TARGET 17.50"],
     "手写账本", "RECV"),
    ("v11_14", "skew_ui", "paid_total", 19.0,
     ["UI SKEW V11", "alpha paid 9.00", "beta paid 10.00", "gamma open 4.50", "TOTAL PAID TARGET 19.00"],
     "斜切界面", "RECV"),
    ("v11_15", "mosaic_stack", "paid_total", 34.0,
     ["HEAVY MOSAIC V11", "x paid 18.00 usd", "y paid 16.00 usd", "z open 6.00 usd", "TOTAL PAID TARGET 34.00"],
     "马赛克重章", "RECV"),
    ("v11_16", "fx_mix", "paid_total", 22.5,
     ["CN-EN FX MIX V11", "tea paid 10.50", "rice paid 12.00", "soup open 3.50", "TOTAL PAID TARGET 22.50"],
     "中英双币", "RECV"),
    ("v11_17", "excel_win", "paid_total", 33.75,
     ["EXCEL WIN V11", "w1 paid 16.00", "w2 paid 17.75", "w3 open 8.00", "TOTAL PAID TARGET 33.75"],
     "表格多窗", "RECV"),
    ("v11_18", "redact_foot", "paid_total", 15.25,
     ["REDACT FOOT V11", "p1 paid 7.50", "p2 paid 7.75", "p3 open 2.00", "TOTAL PAID TARGET 15.25"],
     "涂黑脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V11 Protocol — Glare / Skew / Hand / Redact / Night / Mosaic

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V10: **glare**, **skew shear**, **handwriting overlay**, **redaction bars**,
**night low-contrast**, **mosaic patches**, **stamp-over-digits**, **dual-FX bait**,
**excel grid crosstalk**, **partial TARGET crop**. Still scoped office OCR+atom.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke (C173)

## Honesty
- V10 train/heldout retained when claimed
- Gate2/3 untouched. gen11 HOLD. No fake VL scores here.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageTransform
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v11") & 0xFFFFFFFF)
    try:
        from PIL import ImageGrab
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        bg = shot.crop((0, 0, min(1200, w), min(780, h))).convert("RGB").resize((1000, 640))
        paper = Image.new("RGB", (1000, 640), (205, 200, 190))
        img = Image.blend(bg, paper, 0.66)
        capture = True
    except Exception:
        img = Image.new("RGB", (1000, 640), (205, 200, 190))
        capture = False
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 14)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 11)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 11)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 10)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 15)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 42)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 9)
        f_hand = ImageFont.truetype(r"C:\\Windows\\Fonts\\comic.ttf", 13)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_wm = f_tiny = f_hand = ImageFont.load_default()

    # Main paper
    d.rectangle([18, 18, 480, 560], fill=(228, 222, 212), outline=(60, 60, 60), width=2)
    # excel grid crosstalk (right of paper edge bleed)
    for gx in range(490, 700, 28):
        d.line([(gx, 40), (gx, 280)], fill=(180, 190, 200), width=1)
    for gy in range(40, 280, 22):
        d.line([(490, gy), (700, gy)], fill=(180, 190, 200), width=1)
    d.text((500, 48), "SHEET bait 888.00", fill=(90, 90, 110), font=f_sm)
    d.text((500, 72), "cell Z99 = 777.00", fill=(90, 90, 110), font=f_sm)

    # redaction bars (non-critical areas)
    d.rectangle([30, 300, 200, 318], fill=(20, 20, 20))
    d.rectangle([250, 340, 420, 358], fill=(20, 20, 20))

    # handwriting overlay
    d.text((40, 380), "ok check ~ignore~", fill=(30, 80, 160), font=f_hand)
    d.text((60, 410), "sign: X.Y.", fill=(30, 80, 160), font=f_hand)

    # mosaic patch
    for yy in range(430, 500, 6):
        for xx in range(300, 400, 6):
            col = (rng.randint(40, 200),) * 3
            d.rectangle([xx, yy, xx + 5, yy + 5], fill=col)

    # watermarks / FX bait
    d.text((90, 220), "777", fill=(200, 195, 185), font=f_wm)
    d.text((200, 320), "¥666 $555", fill=(185, 180, 170), font=f_sm)
    d.text((40, 260), "GHOST FX convert 999", fill=(195, 190, 183), font=f_tiny)

    d.rectangle([26, 26, 310, 54], fill=(40, 55, 75))
    d.text((32, 30), (cn_title or kind)[:22], fill=(230, 230, 230), font=f_title)
    y = 64
    for i, ln in enumerate(lines):
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        # night-ish lower contrast on later lines
        fill = (25, 25, 25) if y < 150 else (55, 55, 55) if y < 190 else (85, 85, 85)
        # partial crop: last TARGET line shifted slightly off (still mostly visible)
        xoff = 30 if "TARGET" not in ln.upper() else 26
        d.text((xoff, y), ln[:52], fill=fill, font=font)
        y += 18

    # stamp over digits region (partial)
    for (cx, cy, label, col) in [(360, 150, stamp, (190, 40, 40)), (280, 210, "VOID", (150, 55, 55))]:
        d.ellipse([cx - 52, cy - 24, cx + 42, cy + 30], outline=col, width=3)
        d.text((cx - 18, cy - 6), label[:6], fill=col, font=f_stamp)

    # chat / void windows
    d.rectangle([720, 30, 980, 260], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.rectangle([720, 30, 980, 58], fill=(70, 50, 100))
    d.text((730, 36), "VOID WIN IGNORE", fill=(255, 220, 220), font=f_sm)
    d.text((730, 70), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((730, 95), "FX bait $444.00", fill=(20, 20, 20), font=f_sm)
    d.text((730, 120), f"{fid} void#OLD", fill=(40, 40, 40), font=f_tiny)

    d.rectangle([720, 290, 980, 540], fill=(240, 250, 240), outline=(40, 90, 40), width=2)
    d.text((730, 300), "CAL bait 666.00", fill=(20, 20, 20), font=f_sm)
    d.text((730, 330), "do not parse", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 600, 1000, 640], fill=(18, 18, 28))
    d.text((10, 610), "Start | Glare | Skew | Night | Excel | POS  [V11]", fill=(200, 200, 200), font=f_tiny)

    # glare ellipse (bright overlay)
    glare = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.ellipse([120, 40, 320, 180], fill=(255, 255, 240, 90))
    img = Image.alpha_composite(img.convert("RGBA"), glare).convert("RGB")

    # mild skew via affine transform
    w, h = img.size
    dx = 18
    img = img.transform(
        (w, h),
        Image.AFFINE,
        (1, 0.04, -dx, 0.01, 1, -4),
        resample=Image.BICUBIC,
        fillcolor=(205, 200, 190),
    )

    # night low contrast + noise
    img = ImageEnhance.Brightness(img).enhance(0.82)
    img = ImageEnhance.Contrast(img).enhance(0.78)
    px = img.load()
    ww, hh = img.size
    for _ in range(2800):
        x, y = rng.randint(0, ww - 1), rng.randint(0, hh - 1)
        v = rng.randint(0, 50)
        r, g, b = px[x, y]
        px[x, y] = (max(0, r - v), max(0, g - v), max(0, b - v))
    img = img.filter(ImageFilter.SMOOTH)
    outp = FIX / f"{fid}_{kind}.png"
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "capture_blend": capture,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "hardening": [
            "glare", "skew_shear", "handwriting", "redaction", "night_contrast",
            "mosaic", "stamp_over_digits", "dual_fx_bait", "excel_grid", "partial_crop",
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
        "version": "v11", "n": len(items), "gate": GATE,
        "theme": "glare_skew_hand_redact_night_mosaic",
        "harder_than": "v10",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C172",
        "theme": "vision_v11_design_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "harder_than": "v10",
        "hardening": man["theme"],
        "smoke_deferred_to": "C173",
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "pass": len(items) >= 16,
        "claim": False,
        "note": "V11 fixtures ready; claim only after real VL smoke >=0.6",
    }
    J(DOC / "C172_V11_DESIGN_BATCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C172", "n": len(items), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
