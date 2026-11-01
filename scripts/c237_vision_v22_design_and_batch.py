# -*- coding: utf-8 -*-
"""C237: Vision V22 design + fixtures (harder than V21, clarity floor).
NEW themes vs V21: coffee_stain, binder_ring, tape_edge, blue_pen_annotate,
crumple_fold, carbon_fade, sticky_overlap, fax_banding, grease_smudge, contrast_scan.
CLARITY FLOOR: jpeg_q>=58, photocopy max /2, blur<=0.5, protect text band y=70..250.
No claim until C238 VL. Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import io, json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v22"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V22_PROTOCOL.md"
RUN = ROOT / "runs/vision_v22_c237"

JPEG_Q = 60
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)

SPECS = [
    ("v22_01", "coffee_receipt", "paid_total", 87.5,
     ["COFFEE STAIN V22", "a paid 42.00", "b paid 45.50", "c open 11.00", "TOTAL PAID TARGET 87.50"],
     "咖啡渍收据", "RECV"),
    ("v22_02", "binder_wh", "qty_sum", 69.0,
     ["WH BINDER V22", "SKU1 qty 33 ok", "SKU2 qty 14 hold", "SKU3 qty 36 ok", "qty_sum TARGET 69"],
     "活页仓单", "RECV"),
    ("v22_03", "tape_refund", "refund_done", 38.5,
     ["TAPE REFUND V22", "itemR1 18.00 done", "itemR2 20.50 done", "itemR3 8.00 open", "refund_done TARGET 38.50"],
     "胶带退款", "DONE"),
    ("v22_04", "pen_tax", "tax_base_paid", 129.0,
     ["TAX BLUE PEN V22", "T1 71.00 paid", "T2 28.00 open", "T3 58.00 paid", "tax_base_paid TARGET 129.00"],
     "蓝笔税基", "RECV"),
    ("v22_05", "crumple_pay", "payroll_active", 2210.0,
     ["PAYROLL CRUMPLE V22", "A 1160 active", "B 210 leave", "C 1050 active", "payroll_active TARGET 2210"],
     "皱折工资", "OK"),
    ("v22_06", "carbon_ship", "ship_ok_qty", 57.0,
     ["SHIP CARBON V22", "P1 29 ok", "P2 15 hold", "P3 28 ok", "ship_ok_qty TARGET 57"],
     "复写发运", "SHIP"),
    ("v22_07", "sticky_sla", "open_pri_sum", 48.0,
     ["SLA STICKY V22", "S1 pri 21 open", "S2 pri 27 closed", "S3 pri 27 open", "open_pri_sum TARGET 48"],
     "便签SLA", "OPEN"),
    ("v22_08", "fax_exp", "paid_total", 91.25,
     ["EXPENSE FAXBAND V22", "E1 45.00 paid", "E2 17.00 void", "E3 46.25 paid", "paid_total TARGET 91.25"],
     "传真报销", "RECV"),
    ("v22_09", "grease_po", "paid_total", 74.0,
     ["PO-GREASE V22", "itemA paid 36.50", "itemB paid 37.50", "itemC open 13.00", "TOTAL PAID TARGET 74.00"],
     "油渍采购", "RECV"),
    ("v22_10", "contrast_order", "paid_total", 61.5,
     ["ORDER CONTRAST V22", "A paid 30.00", "B paid 31.50", "C open 9.00", "TOTAL PAID TARGET 61.50"],
     "对比扫描", "RECV"),
    ("v22_11", "coffee_dup", "paid_total", 72.0,
     ["INVOICE #V22-DUP", "line paid 24.00", "line paid 24.00", "line paid 24.00", "TOTAL PAID TARGET 72.00"],
     "咖啡重复", "RECV"),
    ("v22_12", "binder_zero", "paid_total", 0.0,
     ["OPEN ONLY V22", "X 51.00 open", "Y 54.00 open", "paid_total TARGET 0.00"],
     "活页未付", "HOLD"),
    ("v22_13", "tape_ledger", "paid_total", 49.75,
     ["LEDGER TAPE V22", "rA paid 24.50", "rB paid 25.25", "rC open 7.00", "TOTAL PAID TARGET 49.75"],
     "胶带台账", "RECV"),
    ("v22_14", "pen_ui", "paid_total", 55.5,
     ["UI BLUE PEN V22", "alpha paid 27.50", "beta paid 28.00", "gamma open 9.50", "TOTAL PAID TARGET 55.50"],
     "蓝笔界面", "RECV"),
    ("v22_15", "crumple_stack", "paid_total", 86.0,
     ["HEAVY CRUMPLE V22", "x paid 43.00 usd", "y paid 43.00 usd", "z open 16.00 usd", "TOTAL PAID TARGET 86.00"],
     "皱折堆单", "RECV"),
    ("v22_16", "carbon_mix", "paid_total", 52.25,
     ["CN-EN CARBON MIX V22", "tea paid 25.00", "rice paid 27.25", "soup open 8.00", "TOTAL PAID TARGET 52.25"],
     "中英复写", "RECV"),
    ("v22_17", "sticky_win", "paid_total", 66.0,
     ["STICKY WIN V22", "w1 paid 32.00", "w2 paid 34.00", "w3 open 14.00", "TOTAL PAID TARGET 66.00"],
     "便签双窗", "RECV"),
    ("v22_18", "grease_foot", "paid_total", 36.5,
     ["GREASE FOOT V22", "p1 paid 18.00", "p2 paid 18.50", "p3 open 6.00", "TOTAL PAID TARGET 36.50"],
     "油渍脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V22 Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V21: coffee stain, binder rings, tape edge, blue pen annotate,
crumple fold, carbon fade, sticky overlap, fax banding, grease smudge, contrast scan.
Clarity floor from C218/V20/V21 (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V22 uses {jpeg_q})
- photocopy downsample max **/2**
- Gaussian blur radius <= **0.5**
- Protect text band y=70..250
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C238)
- Claim only after smoke

## Honesty
- V21 train refresh (C236) / heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C237.
"""


def in_text_band(yy):
    y0, y1 = TEXT_BAND
    return y0 <= yy <= y1


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v22c237") & 0xFFFFFFFF)
    bg = (212, 208, 198)
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

    for hy in (80, 160, 240, 320, 400, 480):
        d.ellipse([8, hy - 10, 36, hy + 10], outline=(60, 60, 70), width=3)
        d.ellipse([14, hy - 4, 30, hy + 4], fill=(180, 180, 190))

    for (cx, cy, r) in [(480, 420, 55), (120, 520, 40), (900, 300, 70)]:
        for rr in range(r - 8, r, 2):
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(160, 110, 70), width=2)
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(170, 120, 80))

    d.rectangle([80, 18, 280, 42], fill=(240, 230, 160))
    d.text((90, 22), "TAPE bait 33.33", fill=(100, 80, 20), font=f_tiny)

    d.line([(470, 90), (540, 200)], fill=(20, 60, 180), width=2)
    d.text((475, 160), "OK?", fill=(20, 60, 180), font=f_pen)
    d.text((475, 185), "bait 66.66", fill=(20, 60, 180), font=f_tiny)

    d.rectangle([380, 300, 540, 380], fill=(255, 250, 120), outline=(180, 160, 40), width=2)
    d.text((390, 310), "STICKY", fill=(70, 50, 10), font=f_sm)
    d.text((390, 335), "bait 88.88", fill=(70, 50, 10), font=f_tiny)
    d.text((390, 355), "IGNORE", fill=(70, 50, 10), font=f_tiny)

    for y in range(290, 560, 7):
        shade = 200 if (y // 7) % 2 == 0 else 230
        d.line([(50, y), (540, y)], fill=(shade, shade, shade), width=1)

    for (cx, cy, label, col) in [
        (420, 450, stamp, (170, 20, 20)),
        (180, 500, "VOID", (140, 30, 30)),
        (300, 550, "COPY", (50, 50, 150)),
    ]:
        d.ellipse([cx - 48, cy - 24, cx + 42, cy + 26], outline=col, width=3)
        d.text((cx - 16, cy - 6), label[:4], fill=col, font=f_stamp)

    for i in range(5):
        d.text((70 + i * 45, 310 + i * 38), "DRAFT", fill=(236, 232, 224), font=f_wm)

    d.rectangle([0, 0, 1100, 14], fill=(235, 235, 235))
    d.text((8, 1), "SCAN DESK V22  bait 222.00  PAGE 01", fill=(70, 70, 70), font=f_fax)

    d.rectangle([50, 28, 360, 58], fill=(28, 48, 68))
    d.text((56, 32), (cn_title or kind)[:18], fill=(240, 240, 240), font=f_title)

    y = 78
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((62, y + 2), ln[:54], fill=(228, 224, 214), font=font)
        d.text((60, y), ln[:54], fill=(6, 6, 6), font=font)
        y += 26

    d.rectangle([760, 220, 1060, 420], fill=(248, 246, 252), outline=(40, 40, 70), width=2)
    d.text((770, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 265), "old total 888.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 300), "do not parse", fill=(20, 20, 20), font=f_sm)
    d.text((770, 335), "bait 555.00", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 710, 1100, 740], fill=(16, 16, 26))
    d.text(
        (10, 718),
        f"V22 C237 clarity floor jpeg_q{JPEG_Q} photo/{PHOTOCOPY_DIV}  Coffee|Binder|Tape|Pen|Crumple|Carbon|Sticky|Fax|Grease|Contrast",
        fill=(200, 200, 200),
        font=f_tiny,
    )

    px = img.load()
    ww, hh = img.size

    for t in range(0, 700, 2):
        xx = 60 + t
        yy = 280 + int(t * 0.35)
        for w in range(-2, 3):
            x2, y2 = xx + w, yy + w
            if 0 <= x2 < ww and 0 <= y2 < hh and not (in_text_band(y2) and 50 <= x2 <= 450):
                r, g, b = px[x2, y2]
                px[x2, y2] = (min(255, r + 18), min(255, g + 16), min(255, b + 12))

    for _ in range(120):
        xx = rng.randint(45, 160)
        yy = rng.randint(420, 580)
        r, g, b = px[xx, yy]
        px[xx, yy] = (max(0, r - 40), max(0, g - 50), max(0, b - 55))

    for yy in range(300, 560):
        for xx in range(500, 560):
            r, g, b = px[xx, yy]
            px[xx, yy] = (int(r * 0.92 + 20), int(g * 0.92 + 20), int(b * 0.92 + 20))

    for _ in range(280):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        if in_text_band(yy) and 50 <= xx <= 540:
            continue
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)

    img = ImageEnhance.Color(img).enhance(0.82)
    img = ImageEnhance.Contrast(img).enhance(0.98)
    img = ImageEnhance.Brightness(img).enhance(0.95)

    w, h = img.size
    small = img.resize((max(1, w // PHOTOCOPY_DIV), max(1, h // PHOTOCOPY_DIV)), Image.BILINEAR)
    img = small.resize((w, h), Image.BILINEAR)
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.025, -8, 0.01, 1, -4),
        resample=Image.BICUBIC, fillcolor=bg,
    )
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
            "coffee_stain", "binder_ring", "tape_edge", "blue_pen",
            "crumple_fold", "carbon_fade", "sticky_overlap", "fax_banding",
            "grease_smudge", "contrast_scan",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c237_clarity_floor",
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
        "version": "v22",
        "n": len(items),
        "gate": GATE,
        "theme": "coffee_binder_tape_pen_crumple_carbon_sticky_fax_grease_contrast",
        "harder_than": "v21_staple_hl_skew_c230",
        "clarity_floor": {
            "jpeg_q_min": 58,
            "jpeg_q": JPEG_Q,
            "photocopy_div_max": 2,
            "photocopy_div": PHOTOCOPY_DIV,
            "blur_max": 0.5,
            "blur": BLUR_R,
            "text_band_y": list(TEXT_BAND),
            "lesson": "C218 crush + C236 soft_affine; V22 keeps floor",
        },
        "items": items,
        "timestamp": ts(),
        "claim": False,
        "note": "fixtures only; claim deferred to C238 VL smoke",
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C237",
        "theme": "vision_v22_design_and_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "clarity_floor": man["clarity_floor"],
        "vl_gate_v22_claim": False,
        "pass": True,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "C237 design+fixtures; no VL claim",
    }
    J(DOC / "C237_VISION_V22_DESIGN.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
