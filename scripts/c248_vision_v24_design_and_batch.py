# -*- coding: utf-8 -*-
"""C248: Vision V24 design + fixtures (harder than V21, clarity floor).
NEW themes vs V22: highlighter_bleed, paperclip_shadow, hole_punch,
rubber_stamp_overlap, folded_corner, thermal_fade, dust_speckle,
red_ink_bleed, laminated_glare, stapler_dent, margin_crop, barcode_occlusion.
CLARITY FLOOR: jpeg_q>=58, photocopy max /2, blur<=0.5, protect text band y=70..250.
No claim until C249 VL. Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import io, json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v24"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V24_PROTOCOL.md"
RUN = ROOT / "runs/vision_v24_c248"

JPEG_Q = 60
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)

SPECS = [
    ("v24_01", "coffee_recv", "paid_total", 88.5,
     ["COFFEE RING RECV V24", "a paid 43.00", "b paid 45.50", "c open 11.00", "TOTAL PAID TARGET 88.50"],
     "咖啡渍收据", "RECV"),
    ("v24_02", "binder_wh", "qty_sum", 69.0,
     ["WH BINDER TEETH V24", "SKU1 qty 32 ok", "SKU2 qty 14 hold", "SKU3 qty 37 ok", "qty_sum TARGET 69"],
     "活页夹仓单", "RECV"),
    ("v24_03", "tape_refund", "refund_done", 39.5,
     ["YELLOW TAPE REFUND V24", "itemR1 18.00 done", "itemR2 21.50 done", "itemR3 8.00 open", "refund_done TARGET 39.50"],
     "黄胶带退款", "DONE"),
    ("v24_04", "pen_tax", "tax_base_paid", 127.0,
     ["TAX PEN SCRIBBLE V24", "T1 71.00 paid", "T2 28.00 open", "T3 56.00 paid", "tax_base_paid TARGET 127.00"],
     "笔迹税基", "RECV"),
    ("v24_05", "crumple_pay", "payroll_active", 2210.0,
     ["PAYROLL CRUMPLE X V24", "A 1140 active", "B 210 leave", "C 1070 active", "payroll_active TARGET 2210"],
     "皱折工资", "OK"),
    ("v24_06", "carbon_ship", "ship_ok_qty", 55.0,
     ["SHIP CARBON GHOST V24", "P1 28 ok", "P2 15 hold", "P3 27 ok", "ship_ok_qty TARGET 55"],
     "复写发货", "SHIP"),
    ("v24_07", "sticky_sla", "open_pri_sum", 49.0,
     ["SLA STICKY STACK V24", "S1 pri 21 open", "S2 pri 26 closed", "S3 pri 28 open", "open_pri_sum TARGET 49"],
     "便利贴SLA", "OPEN"),
    ("v24_08", "fax_exp", "paid_total", 91.75,
     ["EXPENSE FAX STREAK V24", "E1 45.00 paid", "E2 17.00 void", "E3 46.75 paid", "paid_total TARGET 91.75"],
     "传真条纹报销", "RECV"),
    ("v24_09", "grease_po", "paid_total", 74.0,
     ["PO-GREASE BLOT V24", "itemA paid 36.00", "itemB paid 38.00", "itemC open 13.00", "TOTAL PAID TARGET 74.00"],
     "油渍采购", "RECV"),
    ("v24_10", "gray_order", "paid_total", 61.5,
     ["ORDER GRAY FADE V24", "A paid 30.00", "B paid 31.50", "C open 9.00", "TOTAL PAID TARGET 61.50"],
     "低对比订单", "RECV"),
    ("v24_11", "coffee_dup", "paid_total", 75.0,
     ["INVOICE #V24-DUP", "line paid 25.00", "line paid 25.00", "line paid 25.00", "TOTAL PAID TARGET 75.00"],
     "咖啡渍重复", "RECV"),
    ("v24_12", "binder_zero", "paid_total", 0.0,
     ["OPEN ONLY V24", "X 52.00 open", "Y 55.00 open", "paid_total TARGET 0.00"],
     "活页未付", "HOLD"),
    ("v24_13", "skew_ledger", "paid_total", 52.25,
     ["LEDGER SKEW MILD V24", "rA paid 25.50", "rB paid 26.75", "rC open 7.00", "TOTAL PAID TARGET 52.25"],
     "轻斜台账", "RECV"),
    ("v24_14", "ghost_ui", "paid_total", 54.5,
     ["UI GHOST DOUBLE V24", "alpha paid 26.50", "beta paid 28.00", "gamma open 10.50", "TOTAL PAID TARGET 54.50"],
     "重影窗口", "RECV"),
    ("v24_15", "crumple_stack", "paid_total", 87.0,
     ["HEAVY CRUMPLE STACK V24", "x paid 43.00 usd", "y paid 44.00 usd", "z open 16.00 usd", "TOTAL PAID TARGET 87.00"],
     "皱折堆单", "RECV"),
    ("v24_16", "carbon_mix", "paid_total", 51.25,
     ["CN-EN CARBON MIX V24", "tea paid 25.00", "rice paid 26.25", "soup open 8.00", "TOTAL PAID TARGET 51.25"],
     "中英复写", "RECV"),
    ("v24_17", "fax_win", "paid_total", 66.0,
     ["FAX WIN V24", "w1 paid 32.00", "w2 paid 34.00", "w3 open 14.00", "TOTAL PAID TARGET 66.00"],
     "传真双窗", "RECV"),
    ("v24_18", "grease_foot", "paid_total", 37.5,
     ["GREASE FOOT V24", "p1 paid 18.00", "p2 paid 19.50", "p3 open 6.00", "TOTAL PAID TARGET 37.50"],
     "油渍脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V24 Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V23: coffee ring, binder teeth, yellow tape, pen scribble,
crumple X, carbon ghost, sticky stack, fax streak, grease blot, gray fade,
mild skew, double-exposure ghost.
Clarity floor from C218/V20/V21 (no jpeg crush).

## Clarity floor (mandatory)
- jpeg quality >= **58** (V24 uses {jpeg_q})
- photocopy downsample max **/2**
- Gaussian blur radius <= **0.5**
- Protect text band y=70..250
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL (C238)
- Claim only after smoke

## Honesty
- V21 train refresh (C236) / heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C248.
"""


def in_text_band(yy):
    y0, y1 = TEXT_BAND
    return y0 <= yy <= y1


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v24c248") & 0xFFFFFFFF)
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
    d.text((8, 1), "SCAN DESK V24  bait 222.00  PAGE 01", fill=(70, 70, 70), font=f_fax)

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
        f"V24 C248 clarity floor jpeg_q{JPEG_Q} photo/{PHOTOCOPY_DIV}  Coffee|Binder|Tape|Pen|Crumple|Carbon|Sticky|Fax|Grease|Gray|Skew|Ghost",
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
        (w, h), Image.AFFINE, (1, 0.028, -10, 0.012, 1, -5),
        resample=Image.BICUBIC, fillcolor=bg,
    )
    ghost = img.transform(
        (w, h), Image.AFFINE, (1, 0, 3, 0, 1, 2),
        resample=Image.BICUBIC, fillcolor=bg,
    )
    img = Image.blend(img, ghost, 0.12)
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
            "coffee_ring", "binder_teeth", "yellow_tape", "pen_scribble",
            "crumple_x", "carbon_ghost", "sticky_stack", "fax_streak",
            "grease_blot", "gray_fade", "skew_mild", "ghost_double",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c248_clarity_floor",
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
        "version": "v24",
        "n": len(items),
        "gate": GATE,
        "theme": "coffee_binder_tape_pen_crumple_carbon_sticky_fax_grease_gray_skew_ghost",
        "harder_than": "v23_hl_clip_punch_stamp_fold_c242",
        "clarity_floor": {
            "jpeg_q_min": 58,
            "jpeg_q": JPEG_Q,
            "photocopy_div_max": 2,
            "photocopy_div": PHOTOCOPY_DIV,
            "blur_max": 0.5,
            "blur": BLUR_R,
            "text_band_y": list(TEXT_BAND),
            "lesson": "C218 crush + C236 soft_affine; V24 keeps floor",
        },
        "items": items,
        "timestamp": ts(),
        "claim": False,
        "note": "fixtures only; claim deferred to C249 VL smoke",
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C248",
        "theme": "vision_v24_design_and_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "clarity_floor": man["clarity_floor"],
        "vl_gate_v24_claim": False,
        "pass": True,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "C248 design+fixtures; no VL claim",
    }
    J(DOC / "C248_VISION_V24_DESIGN.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
