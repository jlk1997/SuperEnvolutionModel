# -*- coding: utf-8 -*-
"""C224: Vision V20 design + fixtures (harder than V19 mild).
NEW themes vs V19: crease_grid, tape_glare, carbon_blue, halftone_dot,
fold_corner, edge_wet, thermal_stripe, fax_header, fingerprint_edge,
clip_shadow (+ residual V19 coffee/HL/barcode/stamp light).
CLARITY FLOOR (learn C218 crush): jpeg_q>=58, photocopy max /2, blur<=0.5,
protect text band y=70..240 from glyph-wiping overlays. No claim until C225 VL.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import io, json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v20"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V20_PROTOCOL.md"
RUN = ROOT / "runs/vision_v20_c224"

# clarity floor constants (C218 lesson)
JPEG_Q = 60
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)  # y protect

SPECS = [
    ("v20_01", "crease_receipt", "paid_total", 87.5,
     ["CREASE GRID V20", "a paid 42.00", "b paid 45.50", "c open 11.00", "TOTAL PAID TARGET 87.50"],
     "折痕收据", "RECV"),
    ("v20_02", "tape_wh", "qty_sum", 69.0,
     ["WH TAPE GLARE V20", "SKU1 qty 33 ok", "SKU2 qty 14 hold", "SKU3 qty 36 ok", "qty_sum TARGET 69"],
     "胶带仓单", "RECV"),
    ("v20_03", "carbon_refund", "refund_done", 38.5,
     ["CARBON REFUND V20", "itemR1 18.25 done", "itemR2 20.25 done", "itemR3 8.00 open", "refund_done TARGET 38.50"],
     "复写退款", "DONE"),
    ("v20_04", "halftone_tax", "tax_base_paid", 133.0,
     ["TAX HALFTONE V20", "T1 74.00 paid", "T2 28.00 open", "T3 59.00 paid", "tax_base_paid TARGET 133.00"],
     "网点税基", "RECV"),
    ("v20_05", "fold_pay", "payroll_active", 2210.0,
     ["PAYROLL FOLD V20", "A 1180 active", "B 210 leave", "C 1030 active", "payroll_active TARGET 2210"],
     "折角工资", "OK"),
    ("v20_06", "wet_ship", "ship_ok_qty", 57.0,
     ["SHIP WET EDGE V20", "P1 29 ok", "P2 15 hold", "P3 28 ok", "ship_ok_qty TARGET 57"],
     "湿边发运", "SHIP"),
    ("v20_07", "thermal_sla", "open_pri_sum", 48.0,
     ["SLA THERMAL V20", "S1 pri 21 open", "S2 pri 27 closed", "S3 pri 27 open", "open_pri_sum TARGET 48"],
     "热敏SLA", "OPEN"),
    ("v20_08", "fax_exp", "paid_total", 94.25,
     ["EXPENSE FAX V20", "E1 47.00 paid", "E2 18.00 void", "E3 47.25 paid", "paid_total TARGET 94.25"],
     "传真报销", "RECV"),
    ("v20_09", "fp_po", "paid_total", 76.0,
     ["PO-FINGERPRINT V20", "itemA paid 37.75", "itemB paid 38.25", "itemC open 13.00", "TOTAL PAID TARGET 76.00"],
     "指纹采购", "RECV"),
    ("v20_10", "clip_order", "paid_total", 64.5,
     ["ORDER CLIP V20", "A paid 32.00", "B paid 32.50", "C open 9.00", "TOTAL PAID TARGET 64.50"],
     "夹影订单", "RECV"),
    ("v20_11", "crease_dup", "paid_total", 75.0,
     ["INVOICE #V20-DUP", "line paid 25.00", "line paid 25.00", "line paid 25.00", "TOTAL PAID TARGET 75.00"],
     "折痕重复", "RECV"),
    ("v20_12", "carbon_zero", "paid_total", 0.0,
     ["OPEN ONLY V20", "X 55.00 open", "Y 58.00 open", "paid_total TARGET 0.00"],
     "复写未付", "HOLD"),
    ("v20_13", "tape_ledger", "paid_total", 52.75,
     ["LEDGER TAPE V20", "rA paid 26.25", "rB paid 26.50", "rC open 7.00", "TOTAL PAID TARGET 52.75"],
     "胶带台账", "RECV"),
    ("v20_14", "halftone_ui", "paid_total", 59.5,
     ["UI HALFTONE V20", "alpha paid 29.50", "beta paid 30.00", "gamma open 9.50", "TOTAL PAID TARGET 59.50"],
     "网点界面", "RECV"),
    ("v20_15", "fold_stack", "paid_total", 88.0,
     ["HEAVY FOLD V20", "x paid 44.00 usd", "y paid 44.00 usd", "z open 17.00 usd", "TOTAL PAID TARGET 88.00"],
     "折角堆单", "RECV"),
    ("v20_16", "wet_mix", "paid_total", 55.25,
     ["CN-EN WET MIX V20", "tea paid 26.00", "rice paid 29.25", "soup open 8.00", "TOTAL PAID TARGET 55.25"],
     "中英湿边", "RECV"),
    ("v20_17", "thermal_win", "paid_total", 71.0,
     ["THERMAL WIN V20", "w1 paid 35.00", "w2 paid 36.00", "w3 open 14.00", "TOTAL PAID TARGET 71.00"],
     "热敏双窗", "RECV"),
    ("v20_18", "fax_foot", "paid_total", 39.5,
     ["FAX FOOT V20", "p1 paid 19.50", "p2 paid 20.00", "p3 open 6.00", "TOTAL PAID TARGET 39.50"],
     "传真脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V20 Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V19 mild: crease grid, tape glare, carbon blue, halftone dots,
fold corner, wet edge, thermal stripe, fax header, fingerprint edge, clip shadow.
Clarity floor from C218 lesson (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V20 uses {jpeg_q})
- photocopy downsample max **/2** (not /3)
- Gaussian blur radius <= **0.5**
- Protect text band y≈70–250 from glyph-wiping overlays
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C225)
- Claim only after smoke

## Honesty
- V19 train/heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C224.
"""


def in_text_band(yy, xx=None):
    y0, y1 = TEXT_BAND
    return y0 <= yy <= y1


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v20c224") & 0xFFFFFFFF)
    bg = (218, 214, 204)
    img = Image.new("RGB", (1100, 740), bg)
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 16)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 14)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 15)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 32)
        f_fax = ImageFont.truetype(r"C:\\Windows\\Fonts\\consola.ttf", 11)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = f_wm = f_fax = ImageFont.load_default()

    # main card
    d.rectangle([40, 20, 560, 600], fill=(250, 247, 238), outline=(35, 35, 35), width=2)

    # crease grid (light diagonals) — OUTSIDE / below text band preference
    for i in range(8):
        x0 = 50 + i * 55
        d.line([(x0, 260), (x0 + 80, 560)], fill=(200, 195, 185), width=2)
        d.line([(x0 + 40, 260), (x0 - 20, 560)], fill=(205, 200, 190), width=1)

    # carbon blue tint wash on lower card only
    d.rectangle([42, 320, 558, 598], fill=(230, 238, 248))

    # thermal fade stripes BETWEEN lines below text band
    for ty in range(270, 520, 28):
        d.rectangle([50, ty, 540, ty + 3], fill=(235, 225, 210))

    # tape glare stripe (semi-transparent sim) — right of text, not over digits
    d.rectangle([480, 80, 555, 240], fill=(255, 255, 230))
    d.rectangle([485, 90, 550, 230], outline=(220, 210, 160), width=1)
    d.text((490, 100), "TAPE", fill=(180, 160, 80), font=f_tiny)
    d.text((490, 120), "glare", fill=(180, 160, 80), font=f_tiny)
    d.text((490, 145), "bait 88.88", fill=(160, 140, 60), font=f_tiny)

    # fax header top margin (outside card text)
    d.rectangle([0, 0, 1100, 16], fill=(240, 240, 240))
    d.text((8, 2), "FAX FROM 021-555-0199  2026-10-19 08:15  PAGE 01/01  bait 111.00", fill=(80, 80, 80), font=f_fax)

    # sticky bait NOISE (away from TARGET column start)
    d.rectangle([380, 280, 540, 370], fill=(255, 250, 120), outline=(180, 160, 40), width=2)
    d.text((390, 290), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((390, 315), "bait 99.99", fill=(80, 60, 20), font=f_tiny)
    d.text((390, 338), "IGNORE", fill=(80, 60, 20), font=f_tiny)

    # stamps away from TARGET lines (y>260)
    for (cx, cy, label, col) in [
        (430, 400, stamp, (180, 30, 30)),
        (200, 480, "VOID", (150, 40, 40)),
        (320, 540, "COPY", (60, 60, 160)),
    ]:
        d.ellipse([cx - 42, cy - 20, cx + 36, cy + 22], outline=col, width=3)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)

    # barcode strip far right of card
    bx0 = 545
    for i in range(36):
        w = 1 if rng.random() < 0.55 else 2
        col = (10, 10, 10) if rng.random() < 0.7 else (240, 240, 240)
        d.rectangle([bx0 + i * 2, 300, bx0 + i * 2 + w, 460], fill=col)
    d.text((bx0, 470), "||BAR|| bait 777", fill=(40, 40, 40), font=f_tiny)

    # residual mild coffee ring away from text
    for r in (48, 55, 62):
        d.ellipse([150 - r, 520 - r, 150 + r, 520 + r], outline=(140, 100, 60), width=2)

    # binder clip shadow top
    d.rectangle([250, 6, 340, 28], fill=(40, 40, 50))
    d.ellipse([255, 22, 335, 48], fill=(60, 60, 70))

    # redaction residual right void area
    d.rectangle([780, 80, 1040, 105], fill=(20, 20, 20))
    d.text((790, 115), "REDACTED bait 555", fill=(60, 60, 60), font=f_tiny)

    d.text((100, 560), "CONFIDENTIAL", fill=(232, 228, 218), font=f_wm)
    d.rectangle([50, 28, 360, 58], fill=(30, 50, 70))
    d.text((56, 32), (cn_title or kind)[:18], fill=(240, 240, 240), font=f_title)

    # PRIMARY TEXT — high contrast, protected band
    y = 78
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        # very faint ghost (theme) — must stay low-contrast so digits readable
        d.text((62, y + 2), ln[:54], fill=(230, 226, 216), font=font)
        d.text((60, y), ln[:54], fill=(8, 8, 8), font=font)
        y += 26

    # void win decoy
    d.rectangle([760, 220, 1060, 420], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((770, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 265), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 300), "do not parse", fill=(20, 20, 20), font=f_sm)
    d.text((770, 335), "bait 666.00", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 710, 1100, 740], fill=(18, 18, 28))
    d.text(
        (10, 718),
        f"V20 C224 clarity floor jpeg_q{JPEG_Q} photo/{{PHOTOCOPY_DIV}}  Crease|Tape|Carbon|Halftone|Fold|Wet|Thermal|Fax|FP|Clip",
        fill=(200, 200, 200),
        font=f_tiny,
    )

    px = img.load()
    ww, hh = img.size

    # fold corner chew (top-left outside text)
    for yy in range(20, 90):
        tear = int(2 + (yy - 20) // 8 + rng.randint(0, 2))
        for xx in range(40, 40 + tear):
            if 0 <= xx < ww and 0 <= yy < hh:
                px[xx, yy] = bg

    # wet edge smear bottom/side — skip text band
    for _ in range(4):
        cx = rng.randint(60, 500)
        cy = rng.randint(400, 580)
        for dy in range(-22, 23):
            for dx in range(-22, 23):
                if dx * dx + dy * dy < 22 * 22 and rng.random() < 0.35:
                    xx, yy = cx + dx, cy + dy
                    if 0 <= xx < ww and 0 <= yy < hh and not in_text_band(yy):
                        r, g, b = px[xx, yy]
                        px[xx, yy] = (max(0, r - 20), max(0, g - 15), min(255, b + 10))

    # fingerprint dots near edge (not text)
    for _ in range(80):
        xx = rng.randint(50, 200)
        yy = rng.randint(400, 580)
        if rng.random() < 0.5:
            r, g, b = px[xx, yy]
            px[xx, yy] = (max(0, r - 40), max(0, g - 50), max(0, b - 45))

    # mild halftone dots OUTSIDE text band
    for _ in range(900):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        if in_text_band(yy) and 50 <= xx <= 540:
            continue
        if (xx + yy) % 3 == 0 and rng.random() < 0.4:
            r, g, b = px[xx, yy]
            v = 18 if rng.random() < 0.5 else -12
            px[xx, yy] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v)))

    # light dust outside text
    for _ in range(280):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        if in_text_band(yy) and 50 <= xx <= 540:
            continue
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)

    # carbon / contrast mild
    img = ImageEnhance.Color(img).enhance(0.82)
    img = ImageEnhance.Contrast(img).enhance(0.97)
    img = ImageEnhance.Brightness(img).enhance(0.95)

    # photocopy max /2 (NOT /3 — C218 lesson)
    w, h = img.size
    small = img.resize((max(1, w // PHOTOCOPY_DIV), max(1, h // PHOTOCOPY_DIV)), Image.BILINEAR)
    img = small.resize((w, h), Image.BILINEAR)
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.028, -8, 0.010, 1, -4),
        resample=Image.BICUBIC, fillcolor=bg,
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=BLUR_R))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_Q)  # >=58 clarity floor
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
            "crease_grid", "tape_glare", "carbon_blue", "halftone_dot",
            "fold_corner", "edge_wet", "thermal_stripe", "fax_header",
            "fingerprint_edge", "clip_shadow",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c224_clarity_floor",
        ],
    }


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    PROTO.write_text(
        PROTOCOL.format(ts=ts(), jpeg_q=JPEG_Q),
        encoding="utf-8",
    )
    items = []
    for fid, kind, metric, expected, lines, cn, stamp in SPECS:
        items.append(make_fixture(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v20",
        "n": len(items),
        "gate": GATE,
        "theme": "crease_tape_carbon_halftone_fold_wet_thermal_fax_fp_clip",
        "harder_than": "v19_mild_c219",
        "clarity_floor": {
            "jpeg_q_min": 58,
            "jpeg_q": JPEG_Q,
            "photocopy_div_max": 2,
            "photocopy_div": PHOTOCOPY_DIV,
            "blur_max": 0.5,
            "blur": BLUR_R,
            "text_band_y": list(TEXT_BAND),
            "lesson": "C218 jpeg_q22+photo/3 crushed digits; V20 enforces floor",
        },
        "items": items,
        "timestamp": ts(),
        "claim": False,
        "note": "fixtures only; claim deferred to C225 VL smoke",
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C224",
        "theme": "vision_v20_design_and_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "clarity_floor": man["clarity_floor"],
        "vl_gate_v20_claim": False,
        "pass": True,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "C224 design+fixtures; no VL claim",
    }
    J(DOC / "C224_VISION_V20_DESIGN.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
