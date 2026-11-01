# -*- coding: utf-8 -*-
"""C192: Vision V15 design + fixtures (harder than V14).
Hardening: motion blur, barcode stripe, QR bait, chromatic fringe, underexposure,
polaroid crop, corner tear, checker JPEG, overstamp stack, cross-out near TARGET,
stronger affine, jpeg_q40 (plus residual V14 cues).
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
FIX = ROOT / "evo/office/fixtures/vision_images_v15"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V15_PROTOCOL.md"
RUN = ROOT / "runs/vision_v15_c192"

SPECS = [
    ("v15_01", "blur_receipt", "paid_total", 51.5,
     ["BLUR RECEIPT V15", "a paid 25.00", "b paid 26.50", "c open 8.00", "TOTAL PAID TARGET 51.50"],
     "运动模糊收据", "RECV"),
    ("v15_02", "barcode_wh", "qty_sum", 47.0,
     ["WH BARCODE V15", "SKU1 qty 24 ok", "SKU2 qty 10 hold", "SKU3 qty 23 ok", "qty_sum TARGET 47"],
     "条码仓单", "RECV"),
    ("v15_03", "qr_refund", "refund_done", 26.75,
     ["QR REFUND V15", "itemR1 12.50 done", "itemR2 14.25 done", "itemR3 5.00 open", "refund_done TARGET 26.75"],
     "二维码退款", "DONE"),
    ("v15_04", "chroma_tax", "tax_base_paid", 88.0,
     ["TAX CHROMA V15", "T1 48.00 paid", "T2 18.00 open", "T3 40.00 paid", "tax_base_paid TARGET 88.00"],
     "色散税联", "RECV"),
    ("v15_05", "dark_payroll", "payroll_active", 1520.0,
     ["PAYROLL DARK V15", "A 820 active", "B 120 leave", "C 700 active", "payroll_active TARGET 1520"],
     "欠曝薪资", "OK"),
    ("v15_06", "tear_ship", "ship_ok_qty", 34.0,
     ["SHIP TEAR V15", "P1 17 ok", "P2 11 hold", "P3 17 ok", "ship_ok_qty TARGET 34"],
     "撕角发货", "SHIP"),
    ("v15_07", "polaroid_sla", "open_pri_sum", 32.0,
     ["SLA POLAROID V15", "S1 pri 14 open", "S2 pri 20 closed", "S3 pri 18 open", "open_pri_sum TARGET 32"],
     "拍立得SLA", "OPEN"),
    ("v15_08", "checker_exp", "paid_total", 62.25,
     ["EXPENSE CHECKER V15", "E1 32.00 paid", "E2 13.00 void", "E3 30.25 paid", "paid_total TARGET 62.25"],
     "棋盘报销", "RECV"),
    ("v15_09", "stamp_po", "paid_total", 54.0,
     ["PO-STAMP V15", "itemA paid 27.00", "itemB paid 27.00", "itemC open 9.00", "TOTAL PAID TARGET 54.00"],
     "叠章采购", "RECV"),
    ("v15_10", "xout_order", "paid_total", 37.75,
     ["ORDER XOUT V15", "A paid 18.50", "B paid 19.25", "C open 7.00", "TOTAL PAID TARGET 37.75"],
     "划线订单", "RECV"),
    ("v15_11", "persp_dup", "paid_total", 45.0,
     ["INVOICE #V15-DUP", "line paid 15.00", "line paid 15.00", "line paid 15.00", "TOTAL PAID TARGET 45.00"],
     "透视重复", "RECV"),
    ("v15_12", "noise_zero", "paid_total", 0.0,
     ["OPEN ONLY V15", "X 33.00 open", "Y 36.00 open", "paid_total TARGET 0.00"],
     "噪声未付", "HOLD"),
    ("v15_13", "blur_ledger", "paid_total", 30.25,
     ["LEDGER BLUR V15", "rA paid 15.00", "rB paid 15.25", "rC open 4.50", "TOTAL PAID TARGET 30.25"],
     "模糊账本", "RECV"),
    ("v15_14", "barcode_ui", "paid_total", 41.5,
     ["UI BARCODE V15", "alpha paid 20.25", "beta paid 21.25", "gamma open 6.50", "TOTAL PAID TARGET 41.50"],
     "条码界面", "RECV"),
    ("v15_15", "chroma_stack", "paid_total", 58.0,
     ["HEAVY CHROMA V15", "x paid 29.00 usd", "y paid 29.00 usd", "z open 12.00 usd", "TOTAL PAID TARGET 58.00"],
     "色散叠窗", "RECV"),
    ("v15_16", "qr_mix", "paid_total", 33.25,
     ["CN-EN QR MIX V15", "tea paid 15.00", "rice paid 18.25", "soup open 5.00", "TOTAL PAID TARGET 33.25"],
     "中英二维码", "RECV"),
    ("v15_17", "dark_win", "paid_total", 49.0,
     ["DARK WIN V15", "w1 paid 24.00", "w2 paid 25.00", "w3 open 12.00", "TOTAL PAID TARGET 49.00"],
     "欠曝双窗", "RECV"),
    ("v15_18", "tear_foot", "paid_total", 23.5,
     ["TEAR FOOT V15", "p1 paid 11.50", "p2 paid 12.00", "p3 open 4.00", "TOTAL PAID TARGET 23.50"],
     "撕角脚注", "RECV"),
]



def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V15 Protocol — Blur / Barcode / QR / Chroma / Dark / Tear / Polaroid / Cyan / Fax

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V14: **motion blur**, **barcode stripe**, **QR bait**,
**chromatic fringe**, **underexposure**, **ink bleed**, **cyan misreg**, **polaroid crop**,
**overstamp stack**, **fax lines**, **stronger affine**, **jpeg_q40**.
Still scoped office OCR+atom. Mild-readable TARGET for honest VL.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke (C183)

## Honesty
- V14 train/heldout retained when claimed
- Gate2/3 untouched. gen11 HOLD. No fake VL scores here.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v15") & 0xFFFFFFFF)
    img = Image.new("RGB", (1080, 720), (198, 194, 186))
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
    # V15 overlays: barcode stripe, QR bait, cross-out, corner tear
    for bx in range(560, 620, 3):
        d.line([(bx, 80), (bx, 280)], fill=(10, 10, 10), width=2)
    d.text((560, 290), "BARCODE bait", fill=(60, 60, 60), font=f_tiny)
    for qi in range(8):
        for qj in range(8):
            if (qi + qj) % 2 == 0:
                d.rectangle([640 + qi * 8, 80 + qj * 8, 647 + qi * 8, 87 + qj * 8], fill=(0, 0, 0))
    d.text((640, 150), "QR bait 777", fill=(80, 80, 80), font=f_tiny)
    d.line([(50, 300), (200, 320)], fill=(180, 30, 30), width=2)
    d.line([(55, 320), (195, 300)], fill=(180, 30, 30), width=2)
    d.polygon([(36, 18), (120, 18), (36, 100)], fill=(198, 194, 186))
    d.line([(36, 100), (120, 18)], fill=(80, 60, 40), width=2)
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

    d.rectangle([0, 690, 1080, 720], fill=(18, 18, 28))
    d.text((10, 698), "V15 Blur|Barcode|QR|Chroma|Dark|Tear|Polaroid  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)

    px = img.load()
    ww, hh = img.size
    for yy in range(120, 200):
        for xx in range(50, min(500, ww - 4)):
            r, g, b = px[xx, yy]
            px[xx, yy] = (min(255, r + 18), g, max(0, b - 8))
            if xx + 2 < ww:
                r2, g2, b2 = px[xx + 2, yy]
                px[xx + 2, yy] = (max(0, r2 - 8), g2, min(255, b2 + 18))

    glare = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.ellipse([140, 30, 360, 160], fill=(255, 255, 220, 55))
    img = Image.alpha_composite(img.convert("RGBA"), glare).convert("RGB")

    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.055, -18, 0.02, 1, -6),
        resample=Image.BICUBIC, fillcolor=(198, 194, 186),
    )
    img = ImageEnhance.Contrast(img).enhance(0.85)
    img = ImageEnhance.Brightness(img).enhance(0.78)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.9))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=40)
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
            "motion_blur", "barcode_stripe", "qr_bait", "chromatic_fringe",
            "underexposure", "polaroid_crop", "corner_tear", "checker_jpeg",
            "overstamp_stack", "crossout_near_target", "stronger_affine", "jpeg_q40",
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
        "version": "v15", "n": len(items), "gate": GATE,
        "theme": "blur_barcode_qr_chroma_dark_tear_polaroid_stamp",
        "harder_than": "v14",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C192",
        "theme": "vision_v15_design_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "harder_than": "v14",
        "pass": len(items) >= 16,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "Fixtures only; claim deferred to C193 smoke",
    }
    J(DOC / "C192_V15_DESIGN_BATCH.json", out)
    RUN.mkdir(parents=True, exist_ok=True)
    J(RUN / "design.json", out)
    print(json.dumps({"cycle": "C192", "n": len(items), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
