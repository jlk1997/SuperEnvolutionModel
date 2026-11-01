# -*- coding: utf-8 -*-
"""C182: Vision V13 design + fixtures (harder than V12).
Hardening: crumpled wrinkles, highlighter wash, sticky occlusion, fold crease,
coffee stain, ink bleed stamp, cyan misreg, fluorescent glare, punch holes,
fax line noise, CONFIDENTIAL watermark, carbon-copy fade.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v13"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V13_PROTOCOL.md"
RUN = ROOT / "runs/vision_v13_c182"

SPECS = [
    ("v13_01", "crumple_receipt", "paid_total", 32.25,
     ["CRUMPLE RECEIPT V13", "a paid 15.00", "b paid 17.25", "c open 4.50", "TOTAL PAID TARGET 32.25"],
     "皱纸收据", "RECV"),
    ("v13_02", "highlight_wh", "qty_sum", 31.0,
     ["WH HIGHLIGHT V13", "SKU1 qty 17 ok", "SKU2 qty 5 hold", "SKU3 qty 14 ok", "qty_sum TARGET 31"],
     "荧光笔仓单", "RECV"),
    ("v13_03", "sticky_refund", "refund_done", 14.5,
     ["STICKY REFUND V13", "itemR1 6.25 done", "itemR2 8.25 done", "itemR3 2.00 open", "refund_done TARGET 14.50"],
     "便利贴退款", "DONE"),
    ("v13_04", "fold_tax", "tax_base_paid", 49.0,
     ["TAX FOLD V13", "T1 26.00 paid", "T2 10.00 open", "T3 23.00 paid", "tax_base_paid TARGET 49.00"],
     "折痕税联", "RECV"),
    ("v13_05", "coffee_payroll", "payroll_active", 1120.0,
     ["PAYROLL COFFEE V13", "A 600 active", "B 80 leave", "C 520 active", "payroll_active TARGET 1120"],
     "咖啡渍薪资", "OK"),
    ("v13_06", "bleed_ship", "ship_ok_qty", 27.0,
     ["SHIP BLEED V13", "P1 13 ok", "P2 5 hold", "P3 14 ok", "ship_ok_qty TARGET 27"],
     "洇墨发货", "SHIP"),
    ("v13_07", "cyan_sla", "open_pri_sum", 17.0,
     ["SLA CYAN V13", "S1 pri 8 open", "S2 pri 13 closed", "S3 pri 9 open", "open_pri_sum TARGET 17"],
     "套色SLA", "OPEN"),
    ("v13_08", "fluoro_exp", "paid_total", 48.75,
     ["EXPENSE FLUORO V13", "E1 26.50 paid", "E2 9.00 void", "E3 22.25 paid", "paid_total TARGET 48.75"],
     "荧光报销", "RECV"),
    ("v13_09", "punch_po", "paid_total", 39.5,
     ["PO-PUNCH V13", "itemA paid 20.00", "itemB paid 19.50", "itemC open 7.00", "TOTAL PAID TARGET 39.50"],
     "打孔采购", "RECV"),
    ("v13_10", "fax_order", "paid_total", 30.25,
     ["ORDER FAX V13", "A paid 15.50", "B paid 14.75", "C open 5.00", "TOTAL PAID TARGET 30.25"],
     "传真订单", "RECV"),
    ("v13_11", "wm_dup", "paid_total", 36.0,
     ["INVOICE #V13-DUP", "line paid 12.00", "line paid 12.00", "line paid 12.00", "TOTAL PAID TARGET 36.00"],
     "水印重复", "RECV"),
    ("v13_12", "carbon_zero", "paid_total", 0.0,
     ["OPEN ONLY V13", "X 18.00 open", "Y 21.00 open", "paid_total TARGET 0.00"],
     "复写未付", "HOLD"),
    ("v13_13", "crumple_ledger", "paid_total", 21.5,
     ["LEDGER CRUMPLE V13", "rA paid 10.75", "rB paid 10.75", "rC open 3.00", "TOTAL PAID TARGET 21.50"],
     "皱纸账本", "RECV"),
    ("v13_14", "sticky_ui", "paid_total", 25.0,
     ["UI STICKY V13", "alpha paid 12.00", "beta paid 13.00", "gamma open 4.00", "TOTAL PAID TARGET 25.00"],
     "便利贴界面", "RECV"),
    ("v13_15", "coffee_stack", "paid_total", 42.5,
     ["HEAVY COFFEE V13", "x paid 21.25 usd", "y paid 21.25 usd", "z open 8.00 usd", "TOTAL PAID TARGET 42.50"],
     "咖啡叠窗", "RECV"),
    ("v13_16", "fax_mix", "paid_total", 27.25,
     ["CN-EN FAX MIX V13", "tea paid 12.50", "rice paid 14.75", "soup open 3.50", "TOTAL PAID TARGET 27.25"],
     "中英传真", "RECV"),
    ("v13_17", "fold_win", "paid_total", 43.0,
     ["FOLD WIN V13", "w1 paid 21.00", "w2 paid 22.00", "w3 open 10.00", "TOTAL PAID TARGET 43.00"],
     "折痕双窗", "RECV"),
    ("v13_18", "bleed_foot", "paid_total", 17.5,
     ["BLEED FOOT V13", "p1 paid 8.50", "p2 paid 9.00", "p3 open 2.50", "TOTAL PAID TARGET 17.50"],
     "洇墨脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V13 Protocol — Crumple / Highlight / Sticky / Fold / Coffee / Bleed / Cyan / Fax

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V12: **crumpled wrinkles**, **highlighter wash**, **sticky occlusion**,
**fold crease**, **coffee stain**, **ink bleed**, **cyan misreg**, **fluorescent glare**,
**punch holes**, **fax lines**, **CONFIDENTIAL watermark**, **carbon fade**.
Still scoped office OCR+atom. Mild-readable TARGET for honest VL.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke (C183)

## Honesty
- V12 train/heldout retained when claimed
- Gate2/3 untouched. gen11 HOLD. No fake VL scores here.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v13") & 0xFFFFFFFF)
    img = Image.new("RGB", (1040, 680), (210, 205, 195))
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

    d.rectangle([36, 18, 540, 580], fill=(242, 236, 226), outline=(35, 35, 35), width=2)
    for _ in range(14):
        x0 = rng.randint(40, 500)
        y0 = rng.randint(40, 540)
        d.arc([x0, y0, x0 + rng.randint(40, 120), y0 + rng.randint(20, 60)], 0, 180, fill=(200, 195, 185), width=1)
    d.rectangle([50, 95, 500, 118], fill=(255, 255, 120))
    d.rectangle([50, 160, 420, 182], fill=(180, 255, 180))
    d.rectangle([360, 200, 520, 280], fill=(255, 250, 120), outline=(180, 160, 40), width=2)
    d.text((370, 210), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((370, 235), "bait 888.00", fill=(80, 60, 20), font=f_tiny)
    d.text((370, 255), "IGNORE", fill=(80, 60, 20), font=f_tiny)
    d.line([(40, 40), (520, 560)], fill=(180, 175, 165), width=2)
    d.line([(42, 38), (522, 558)], fill=(230, 225, 215), width=1)

    coffee = Image.new("RGBA", img.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(coffee)
    cd.ellipse([80, 400, 220, 540], outline=(120, 70, 30, 90), width=10)
    cd.ellipse([100, 420, 200, 520], fill=(140, 80, 40, 40))
    img = Image.alpha_composite(img.convert("RGBA"), coffee).convert("RGB")
    d = ImageDraw.Draw(img)

    for hy in (60, 200, 340, 480):
        d.ellipse([18, hy, 34, hy + 16], fill=(210, 205, 195), outline=(40, 40, 40), width=1)
    for fy in range(30, 570, 7):
        if rng.random() > 0.35:
            d.line([(40, fy), (540, fy)], fill=(195, 190, 185), width=1)

    d.text((80, 320), "CONFIDENTIAL", fill=(220, 210, 200), font=f_wm)
    d.text((100, 450), "COPY bait 777", fill=(225, 218, 208), font=f_sm)

    d.rectangle([46, 26, 330, 56], fill=(25, 45, 65))
    d.text((52, 30), (cn_title or kind)[:20], fill=(240, 240, 240), font=f_title)
    y = 70
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((55, y), ln[:54], fill=(8, 8, 8), font=font)
        y += 22

    for (cx, cy, label, col) in [(390, 140, stamp, (180, 30, 30)), (280, 250, "作废", (140, 50, 50)), (430, 300, "VOID", (150, 40, 40))]:
        d.ellipse([cx - 46, cy - 22, cx + 40, cy + 26], outline=col, width=3)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)
        d.ellipse([cx - 50, cy - 26, cx + 44, cy + 30], outline=col, width=1)

    d.rectangle([740, 200, 1020, 420], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((750, 210), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((750, 245), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((750, 280), "do not parse", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 650, 1040, 680], fill=(18, 18, 28))
    d.text((10, 658), "V13 Crumple|Highlight|Sticky|Fold|Coffee|Bleed|Fax  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)

    px = img.load()
    ww, hh = img.size
    for yy in range(120, 200):
        for xx in range(50, min(500, ww - 3)):
            r, g, b = px[xx, yy]
            px[xx, yy] = (r, g, min(255, b + 18))

    glare = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.ellipse([140, 30, 360, 160], fill=(255, 255, 220, 55))
    img = Image.alpha_composite(img.convert("RGBA"), glare).convert("RGB")

    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.025, -10, 0.01, 1, -3),
        resample=Image.BICUBIC, fillcolor=(210, 205, 195),
    )
    img = ImageEnhance.Contrast(img).enhance(0.92)
    img = ImageEnhance.Brightness(img).enhance(0.94)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=55)
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
            "crumple_wrinkles", "highlighter_wash", "sticky_occlusion", "fold_crease",
            "coffee_stain", "ink_bleed_stamp", "cyan_misreg", "fluorescent_glare",
            "punch_holes", "fax_lines", "confidential_wm", "carbon_fade", "jpeg_q55",
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
        "version": "v13", "n": len(items), "gate": GATE,
        "theme": "crumple_highlight_sticky_fold_coffee_bleed_cyan_fax",
        "harder_than": "v12",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C182",
        "theme": "vision_v13_design_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "harder_than": "v12",
        "pass": len(items) >= 16,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "Fixtures only; claim deferred to C183 smoke",
    }
    J(DOC / "C182_V13_DESIGN_BATCH.json", out)
    RUN.mkdir(parents=True, exist_ok=True)
    J(RUN / "design.json", out)
    print(json.dumps({"cycle": "C182", "n": len(items), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
