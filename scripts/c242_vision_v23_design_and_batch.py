# -*- coding: utf-8 -*-
"""C242: Vision V23 design + fixtures (harder than V21, clarity floor).
NEW themes vs V22: highlighter_bleed, paperclip_shadow, hole_punch,
rubber_stamp_overlap, folded_corner, thermal_fade, dust_speckle,
red_ink_bleed, laminated_glare, stapler_dent, margin_crop, barcode_occlusion.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v23"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V23_PROTOCOL.md"
RUN = ROOT / "runs/vision_v23_c242"

JPEG_Q = 60
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)

SPECS = [
    ("v23_01", "hl_receipt", "paid_total", 93.5,
     ["HIGHLIGHTER BLEED V23", "a paid 46.00", "b paid 47.50", "c open 12.00", "TOTAL PAID TARGET 93.50"],
     "荧光笔收据", "RECV"),
    ("v23_02", "clip_wh", "qty_sum", 78.0,
     ["WH PAPERCLIP V23", "SKU1 qty 37 ok", "SKU2 qty 16 hold", "SKU3 qty 41 ok", "qty_sum TARGET 78"],
     "回形针仓单", "RECV"),
    ("v23_03", "punch_refund", "refund_done", 44.75,
     ["HOLE PUNCH REFUND V23", "itemR1 21.00 done", "itemR2 23.75 done", "itemR3 9.00 open", "refund_done TARGET 44.75"],
     "打孔退款", "DONE"),
    ("v23_04", "stamp_tax", "tax_base_paid", 141.0,
     ["TAX RUBBER STAMP V23", "T1 79.00 paid", "T2 31.00 open", "T3 62.00 paid", "tax_base_paid TARGET 141.00"],
     "橡皮章税基", "RECV"),
    ("v23_05", "fold_pay", "payroll_active", 2480.0,
     ["PAYROLL FOLD V23", "A 1280 active", "B 240 leave", "C 1200 active", "payroll_active TARGET 2480"],
     "折角工资", "OK"),
    ("v23_06", "thermal_ship", "ship_ok_qty", 63.0,
     ["SHIP THERMAL V23", "P1 32 ok", "P2 17 hold", "P3 31 ok", "ship_ok_qty TARGET 63"],
     "热敏发运", "SHIP"),
    ("v23_07", "dust_sla", "open_pri_sum", 55.0,
     ["SLA DUST V23", "S1 pri 24 open", "S2 pri 29 closed", "S3 pri 31 open", "open_pri_sum TARGET 55"],
     "粉尘SLA", "OPEN"),
    ("v23_08", "redink_exp", "paid_total", 102.25,
     ["EXPENSE RED INK V23", "E1 51.00 paid", "E2 19.00 void", "E3 51.25 paid", "paid_total TARGET 102.25"],
     "红墨报销", "RECV"),
    ("v23_09", "glare_po", "paid_total", 81.0,
     ["PO-LAMINATE GLARE V23", "itemA paid 40.00", "itemB paid 41.00", "itemC open 14.00", "TOTAL PAID TARGET 81.00"],
     "覆膜眩光采购", "RECV"),
    ("v23_10", "staple_order", "paid_total", 68.5,
     ["ORDER STAPLER V23", "A paid 33.50", "B paid 35.00", "C open 10.00", "TOTAL PAID TARGET 68.50"],
     "订书机订单", "RECV"),
    ("v23_11", "hl_dup", "paid_total", 84.0,
     ["INVOICE #V23-DUP", "line paid 28.00", "line paid 28.00", "line paid 28.00", "TOTAL PAID TARGET 84.00"],
     "荧光笔重复", "RECV"),
    ("v23_12", "clip_zero", "paid_total", 0.0,
     ["OPEN ONLY V23", "X 58.00 open", "Y 61.00 open", "paid_total TARGET 0.00"],
     "回形针未付", "HOLD"),
    ("v23_13", "crop_ledger", "paid_total", 57.75,
     ["LEDGER MARGIN CROP V23", "rA paid 28.50", "rB paid 29.25", "rC open 8.00", "TOTAL PAID TARGET 57.75"],
     "裁边台账", "RECV"),
    ("v23_14", "barcode_ui", "paid_total", 59.5,
     ["UI BARCODE OCCLUSION V23", "alpha paid 29.50", "beta paid 30.00", "gamma open 11.50", "TOTAL PAID TARGET 59.50"],
     "条码遮挡界面", "RECV"),
    ("v23_15", "fold_stack", "paid_total", 98.0,
     ["HEAVY FOLD STACK V23", "x paid 49.00 usd", "y paid 49.00 usd", "z open 18.00 usd", "TOTAL PAID TARGET 98.00"],
     "折角堆单", "RECV"),
    ("v23_16", "thermal_mix", "paid_total", 58.25,
     ["CN-EN THERMAL MIX V23", "tea paid 28.00", "rice paid 30.25", "soup open 9.00", "TOTAL PAID TARGET 58.25"],
     "中英热敏", "RECV"),
    ("v23_17", "dust_win", "paid_total", 73.0,
     ["DUST WIN V23", "w1 paid 36.00", "w2 paid 37.00", "w3 open 15.00", "TOTAL PAID TARGET 73.00"],
     "粉尘双窗", "RECV"),
    ("v23_18", "glare_foot", "paid_total", 41.5,
     ["GLARE FOOT V23", "p1 paid 20.50", "p2 paid 21.00", "p3 open 7.00", "TOTAL PAID TARGET 41.50"],
     "眩光脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V23 Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V22: highlighter bleed, paperclip shadow, hole punch,
rubber stamp overlap, folded corner, thermal fade, dust speckle,
red ink bleed, laminated glare, stapler dent, margin crop, barcode occlusion.
Clarity floor from C218/V20/V21 (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V23 uses {jpeg_q})
- photocopy downsample max **/2**
- Gaussian blur radius <= **0.5**
- Protect text band y=70..250
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C238)
- Claim only after smoke

## Honesty
- V21 train refresh (C236) / heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C242.
"""


def in_text_band(yy):
    y0, y1 = TEXT_BAND
    return y0 <= yy <= y1


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v23c242") & 0xFFFFFFFF)
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
    d.text((8, 1), "SCAN DESK V23  bait 222.00  PAGE 01", fill=(70, 70, 70), font=f_fax)

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
        f"V23 C242 clarity floor jpeg_q{JPEG_Q} photo/{PHOTOCOPY_DIV}  HL|Clip|Punch|Stamp|Fold|Thermal|Dust|RedInk|Glare|Staple|Crop|Barcode",
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
            "highlighter_bleed", "paperclip_shadow", "hole_punch",
            "rubber_stamp_overlap", "folded_corner", "thermal_fade",
            "dust_speckle", "red_ink_bleed", "laminated_glare",
            "stapler_dent", "margin_crop", "barcode_occlusion",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c242_clarity_floor",
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
        "version": "v23",
        "n": len(items),
        "gate": GATE,
        "theme": "hl_clip_punch_stamp_fold_thermal_dust_redink_glare_staple_crop_barcode",
        "harder_than": "v22_coffee_binder_tape_pen_c237",
        "clarity_floor": {
            "jpeg_q_min": 58,
            "jpeg_q": JPEG_Q,
            "photocopy_div_max": 2,
            "photocopy_div": PHOTOCOPY_DIV,
            "blur_max": 0.5,
            "blur": BLUR_R,
            "text_band_y": list(TEXT_BAND),
            "lesson": "C218 crush + C236 soft_affine; V23 keeps floor",
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
        "cycle": "C242",
        "theme": "vision_v23_design_and_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "clarity_floor": man["clarity_floor"],
        "vl_gate_v23_claim": False,
        "pass": True,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "C242 design+fixtures; no VL claim",
    }
    J(DOC / "C242_VISION_V23_DESIGN.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
