# -*- coding: utf-8 -*-
"""C208: Vision V18 design + fixtures (harder than V17).
Hardening: bleach washout, newspaper halftone, crayon scribble, thermal fade,
punch holes, binder-clip shadow, redaction bars, wet fingerprint, jpeg_q28
(plus residual V17 cues). Gate 0.6. Gate2/3 untouched. gen11 HOLD.
No claim until real VL smoke (C209).
"""
from __future__ import annotations
import io, json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v18"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V18_PROTOCOL.md"
RUN = ROOT / "runs/vision_v18_c208"

SPECS = [
    ("v18_01", "bleach_receipt", "paid_total", 81.5,
     ["BLEACH WASHOUT V18", "a paid 40.00", "b paid 41.50", "c open 11.00", "TOTAL PAID TARGET 81.50"],
     "漂白收据", "RECV"),
    ("v18_02", "halftone_wh", "qty_sum", 67.0,
     ["WH HALFTONE V18", "SKU1 qty 34 ok", "SKU2 qty 15 hold", "SKU3 qty 33 ok", "qty_sum TARGET 67"],
     "网点仓库", "RECV"),
    ("v18_03", "crayon_refund", "refund_done", 39.25,
     ["CRAYON REFUND V18", "itemR1 18.75 done", "itemR2 20.50 done", "itemR3 8.00 open", "refund_done TARGET 39.25"],
     "蜡笔退款", "DONE"),
    ("v18_04", "thermal_tax", "tax_base_paid", 128.0,
     ["TAX THERMAL V18", "T1 70.00 paid", "T2 25.00 open", "T3 58.00 paid", "tax_base_paid TARGET 128.00"],
     "热敏税基", "RECV"),
    ("v18_05", "punch_pay", "payroll_active", 2110.0,
     ["PAYROLL PUNCH V18", "A 1120 active", "B 180 leave", "C 990 active", "payroll_active TARGET 2110"],
     "打孔薪资", "OK"),
    ("v18_06", "clip_ship", "ship_ok_qty", 51.0,
     ["SHIP CLIP V18", "P1 26 ok", "P2 14 hold", "P3 25 ok", "ship_ok_qty TARGET 51"],
     "夹影发货", "SHIP"),
    ("v18_07", "redact_sla", "open_pri_sum", 47.0,
     ["SLA REDACT V18", "S1 pri 21 open", "S2 pri 28 closed", "S3 pri 26 open", "open_pri_sum TARGET 47"],
     "涂黑SLA", "OPEN"),
    ("v18_08", "finger_exp", "paid_total", 91.75,
     ["EXPENSE FINGER V18", "E1 45.50 paid", "E2 18.00 void", "E3 46.25 paid", "paid_total TARGET 91.75"],
     "指印报销", "RECV"),
    ("v18_09", "bleach_po", "paid_total", 76.0,
     ["PO-BLEACH V18", "itemA paid 37.75", "itemB paid 38.25", "itemC open 13.00", "TOTAL PAID TARGET 76.00"],
     "漂白采购", "RECV"),
    ("v18_10", "halftone_order", "paid_total", 59.5,
     ["ORDER HALFTONE V18", "A paid 29.50", "B paid 30.00", "C open 10.00", "TOTAL PAID TARGET 59.50"],
     "网点订单", "RECV"),
    ("v18_11", "thermal_dup", "paid_total", 72.0,
     ["INVOICE #V18-DUP", "line paid 24.00", "line paid 24.00", "line paid 24.00", "TOTAL PAID TARGET 72.00"],
     "热敏重复", "RECV"),
    ("v18_12", "crayon_zero", "paid_total", 0.0,
     ["OPEN ONLY V18", "X 55.00 open", "Y 58.00 open", "paid_total TARGET 0.00"],
     "蜡笔未付", "HOLD"),
    ("v18_13", "punch_ledger", "paid_total", 49.25,
     ["LEDGER PUNCH V18", "rA paid 24.50", "rB paid 24.75", "rC open 7.00", "TOTAL PAID TARGET 49.25"],
     "打孔账本", "RECV"),
    ("v18_14", "clip_ui", "paid_total", 57.5,
     ["UI CLIP V18", "alpha paid 28.50", "beta paid 29.00", "gamma open 9.50", "TOTAL PAID TARGET 57.50"],
     "夹影界面", "RECV"),
    ("v18_15", "redact_stack", "paid_total", 80.0,
     ["HEAVY REDACT V18", "x paid 40.00 usd", "y paid 40.00 usd", "z open 16.00 usd", "TOTAL PAID TARGET 80.00"],
     "涂黑堆叠", "RECV"),
    ("v18_16", "finger_mix", "paid_total", 50.25,
     ["CN-EN FINGER MIX V18", "tea paid 23.00", "rice paid 27.25", "soup open 8.00", "TOTAL PAID TARGET 50.25"],
     "中英指印", "RECV"),
    ("v18_17", "bleach_win", "paid_total", 68.0,
     ["BLEACH WIN V18", "w1 paid 33.00", "w2 paid 35.00", "w3 open 15.00", "TOTAL PAID TARGET 68.00"],
     "漂白双窗", "RECV"),
    ("v18_18", "halftone_foot", "paid_total", 34.5,
     ["HALFTONE FOOT V18", "p1 paid 17.00", "p2 paid 17.50", "p3 open 6.00", "TOTAL PAID TARGET 34.50"],
     "网点脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V18 Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V17: bleach washout, newspaper halftone, crayon scribble, thermal fade,
punch holes, binder-clip shadow, redaction bars, wet fingerprint, jpeg_q28.
Mild-readable TARGET. Scoped office OCR+atom.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke (C209)

## Honesty
- V17 train/heldout retained when claimed
- Gate2/3 untouched. gen11 HOLD. No fake VL scores here.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v18") & 0xFFFFFFFF)
    img = Image.new("RGB", (1100, 740), (200, 195, 185))
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

    d.rectangle([40, 20, 560, 600], fill=(245, 240, 230), outline=(40, 40, 40), width=2)
    # residual V17 wrinkles + LED
    for _ in range(14):
        x0 = rng.randint(45, 520)
        y0 = rng.randint(40, 560)
        d.arc([x0, y0, x0 + rng.randint(40, 120), y0 + rng.randint(20, 60)], 0, 180, fill=(180, 175, 165), width=2)
    for by in range(30, 580, 12):
        d.rectangle([40, by, 560, by + 1], fill=(215, 220, 230))
    d.rectangle([55, 100, 520, 124], fill=(255, 255, 90))
    d.rectangle([55, 170, 430, 194], fill=(255, 120, 220))
    d.rectangle([370, 210, 540, 300], fill=(255, 248, 100), outline=(180, 160, 40), width=2)
    d.text((380, 220), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((380, 245), "bait 888.00", fill=(80, 60, 20), font=f_tiny)
    d.text((380, 268), "IGNORE", fill=(80, 60, 20), font=f_tiny)

    # punch holes
    for (hx, hy) in [(70, 50), (70, 200), (70, 350), (70, 500)]:
        d.ellipse([hx - 10, hy - 10, hx + 10, hy + 10], fill=(200, 195, 185), outline=(60, 60, 60), width=2)
        d.ellipse([hx - 4, hy - 4, hx + 4, hy + 4], fill=(120, 120, 120))

    # binder clip shadow top
    d.rectangle([250, 8, 340, 35], fill=(40, 40, 50))
    d.polygon([(250, 35), (340, 35), (320, 55), (270, 55)], fill=(60, 60, 70))

    # redaction bars (not over TARGET region carefully — left side bait)
    d.rectangle([780, 80, 1040, 110], fill=(10, 10, 10))
    d.rectangle([780, 130, 980, 155], fill=(10, 10, 10))
    d.text((790, 165), "REDACTED bait 555", fill=(40, 40, 40), font=f_tiny)

    # crayon scribble
    for _ in range(8):
        pts = [(rng.randint(80, 500), rng.randint(80, 520)) for __ in range(4)]
        d.line(pts, fill=(rng.choice([(220, 40, 40), (40, 80, 220), (40, 180, 60)])), width=3)

    # wet fingerprint
    fp = Image.new("RGBA", img.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(fp)
    for i in range(6):
        fd.ellipse([420 + i, 380 + i, 500 - i, 470 - i], outline=(90, 60, 40, 70), width=2)
    fd.ellipse([440, 400, 480, 450], fill=(100, 70, 50, 35))
    img = Image.alpha_composite(img.convert("RGBA"), fp).convert("RGB")
    d = ImageDraw.Draw(img)

    d.text((90, 330), "CONFIDENTIAL", fill=(220, 215, 205), font=f_wm)
    d.rectangle([50, 28, 340, 58], fill=(30, 50, 70))
    d.text((56, 32), (cn_title or kind)[:20], fill=(240, 240, 240), font=f_title)
    y = 72
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
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
    d.text((10, 718), "V18 Bleach|Halftone|Crayon|Thermal|Punch|Clip|Redact|Finger  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)

    px = img.load()
    ww, hh = img.size
    # newspaper halftone dots
    for y0 in range(40, 600, 5):
        for x0 in range(50, 540, 5):
            if rng.random() < 0.35:
                v = rng.randint(30, 90)
                if x0 < ww and y0 < hh:
                    r, g, b = px[x0, y0]
                    px[x0, y0] = (max(0, r - v), max(0, g - v), max(0, b - v))
    # thermal fade bands
    for yy in range(60, 200):
        for xx in range(50, min(520, ww)):
            r, g, b = px[xx, yy]
            fade = 35 + (yy % 7) * 3
            px[xx, yy] = (min(255, r + fade), min(255, g + fade), min(255, b + fade // 2))
    # bleach washout (raise brightness locally)
    for yy in range(250, 400):
        for xx in range(80, min(480, ww)):
            r, g, b = px[xx, yy]
            px[xx, yy] = (min(255, int(r * 1.15 + 20)), min(255, int(g * 1.15 + 20)), min(255, int(b * 1.1 + 15)))
    # dust
    for _ in range(1800):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)

    img = ImageEnhance.Color(img).enhance(0.50)
    img = ImageEnhance.Contrast(img).enhance(0.72)
    img = ImageEnhance.Brightness(img).enhance(0.68)
    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.095, -32, 0.035, 1, -12),
        resample=Image.BICUBIC, fillcolor=(200, 195, 185),
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=1.25))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=28)
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
            "bleach_washout", "newspaper_halftone", "crayon_scribble", "thermal_fade",
            "punch_holes", "binder_clip_shadow", "redaction_bars", "wet_fingerprint",
            "jpeg_q28",
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
        "version": "v18", "n": len(items), "gate": GATE,
        "theme": "bleach_halftone_crayon_thermal_punch_clip_redact_finger",
        "harder_than": "v17",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C208",
        "theme": "vision_v18_design_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "harder_than": "v17",
        "pass": len(items) >= 16,
        "claim": False,
        "note": "fixtures only; claim deferred to C209 VL smoke",
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(DOC / "C208_V18_DESIGN_BATCH.json", out)
    J(RUN / "batch.json", out)
    print(json.dumps({"cycle": "C208", "n": len(items), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
