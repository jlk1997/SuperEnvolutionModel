# -*- coding: utf-8 -*-
"""C160: Vision V9 design + fixtures (smoke deferred).
Harder than V8: torn edge, barcode distractor, multi-currency confuse,
rotated stamp, faint carbon second page ghost, QR noise block.
Gate 0.6. Gate2/3 untouched. gen11 HOLD. No claim until real VL.
"""
from __future__ import annotations
import json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v9"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V9_PROTOCOL.md"
RUN = ROOT / "runs/vision_v9_c160"

SPECS = [
    ("v9_01", "torn_receipt", "paid_total", 19.25,
     ["TORN RECEIPT V9", "a paid 8.25", "b paid 11.00", "c open 2.50", "TOTAL PAID TARGET 19.25"],
     "撕边收据", "RECV"),
    ("v9_02", "barcode_wh", "qty_sum", 21.0,
     ["WH BARCODE V9", "SKU1 qty 13 ok", "SKU2 qty 4 hold", "SKU3 qty 8 ok", "qty_sum TARGET 21"],
     "条码仓单", "RECV"),
    ("v9_03", "fx_refund", "refund_done", 9.75,
     ["FX REFUND V9", "itemR1 4.25 done", "itemR2 5.50 done", "itemR3 3.00 open", "refund_done TARGET 9.75"],
     "多币退款", "DONE"),
    ("v9_04", "ghost_tax", "tax_base_paid", 26.0,
     ["TAX GHOST V9", "T1 14.00 paid", "T2 7.00 open", "T3 12.00 paid", "tax_base_paid TARGET 26.00"],
     "鬼影税联", "RECV"),
    ("v9_05", "qr_payroll", "payroll_active", 860.0,
     ["PAYROLL QR V9", "A 450 active", "B 80 leave", "C 410 active", "payroll_active TARGET 860"],
     "二维码薪资", "OK"),
    ("v9_06", "rot_ship", "ship_ok_qty", 13.0,
     ["SHIP ROT V9", "P1 7 ok", "P2 5 hold", "P3 6 ok", "ship_ok_qty TARGET 13"],
     "旋转发货", "SHIP"),
    ("v9_07", "multi_sla", "open_pri_sum", 10.0,
     ["SLA MULTI V9", "S1 pri 5 open", "S2 pri 9 closed", "S3 pri 5 open", "open_pri_sum TARGET 10"],
     "多章SLA", "OPEN"),
    ("v9_08", "torn_exp", "paid_total", 37.5,
     ["EXPENSE TORN V9", "E1 21.00 paid", "E2 10.00 void", "E3 16.50 paid", "paid_total TARGET 37.50"],
     "撕边报销", "RECV"),
    ("v9_09", "fx_po", "paid_total", 30.0,
     ["PO-FX V9", "itemA paid 16.00", "itemB paid 14.00", "itemC open 5.00", "TOTAL PAID TARGET 30.00"],
     "多币采购", "RECV"),
    ("v9_10", "ghost_order", "paid_total", 22.5,
     ["ORDER GHOST V9", "A paid 12.00", "B paid 10.50", "C open 3.25", "TOTAL PAID TARGET 22.50"],
     "鬼影订单", "RECV"),
    ("v9_11", "dup_barcode", "paid_total", 15.0,
     ["INVOICE #V9-DUP", "line paid 5.00", "line paid 5.00", "line paid 5.00", "TOTAL PAID TARGET 15.00"],
     "条码重复", "RECV"),
    ("v9_12", "edge_zero_fx", "paid_total", 0.0,
     ["OPEN ONLY V9", "X 9.00 open", "Y 13.00 open", "paid_total TARGET 0.00"],
     "未付多币", "HOLD"),
    ("v9_13", "qr_ledger", "paid_total", 14.75,
     ["LEDGER QR V9", "rA paid 7.25", "rB paid 7.50", "rC open 1.50", "TOTAL PAID TARGET 14.75"],
     "二维码账本", "RECV"),
    ("v9_14", "rot_ui", "paid_total", 11.25,
     ["UI ROT V9", "alpha paid 4.75", "beta paid 6.50", "gamma open 2.00", "TOTAL PAID TARGET 11.25"],
     "旋转界面", "RECV"),
    ("v9_15", "torn_stack", "paid_total", 27.0,
     ["HEAVY TORN V9", "x paid 15.00 usd", "y paid 12.00 usd", "z open 4.00 usd", "TOTAL PAID TARGET 27.00"],
     "撕边重章", "RECV"),
    ("v9_16", "mix_fx", "paid_total", 14.0,
     ["CN-EN FX MIX V9", "tea paid 6.00", "rice paid 8.00", "soup open 2.50", "TOTAL PAID TARGET 14.00"],
     "中英多币", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V9 Protocol — Torn / Barcode / FX / Ghost / QR

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V8 heldout-solid: **torn paper edge**, **barcode distractor band**,
**multi-currency ($/€/¥) confuse labels**, **rotated stamp**, **carbon ghost page**,
**QR noise block**. Still scoped office OCR+atom.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke (deferred)

## Honesty
- V8 train 1.0 / heldout 0.9375 retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores here.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v9") & 0xFFFFFFFF)
    try:
        from PIL import ImageGrab
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        bg = shot.crop((0, 0, min(1100, w), min(720, h))).convert("RGB").resize((920, 580))
        paper = Image.new("RGB", (920, 580), (208, 202, 192))
        img = Image.blend(bg, paper, 0.7)
        capture = True
    except Exception:
        img = Image.new("RGB", (920, 580), (208, 202, 192))
        capture = False
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 14)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 11)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 11)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 10)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 15)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 44)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 9)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_wm = f_tiny = ImageFont.load_default()

    d.rectangle([10, 10, 450, 545], fill=(228, 222, 212), outline=(85, 85, 85), width=2)
    # torn edge jagged
    for i in range(12):
        y0 = 20 + i * 40
        d.polygon([(8, y0), (18, y0 + 12), (8, y0 + 28)], fill=(180, 175, 165))
    # barcode distractor
    bx = 30
    for i in range(40):
        wbar = 1 if rng.random() < 0.5 else 2
        d.rectangle([bx, 480, bx + wbar, 530], fill=(30, 30, 30))
        bx += wbar + 1
    d.text((30, 532), "BARCODE IGNORE 4729183", fill=(60, 60, 60), font=f_tiny)
    # FX confuse
    d.text((300, 500), "$999 €888 ¥777", fill=(170, 165, 155), font=f_sm)
    # watermarks
    d.text((90, 210), "777", fill=(200, 195, 185), font=f_wm)
    d.text((210, 330), "666", fill=(198, 193, 183), font=f_wm)
    # ghost second page
    d.text((40, 300), "GHOST PAGE copy TOTAL 42", fill=(200, 195, 188), font=f_tiny)
    # QR-ish noise block
    for yy in range(400, 460, 3):
        for xx in range(360, 430, 3):
            if rng.random() < 0.45:
                d.rectangle([xx, yy, xx + 2, yy + 2], fill=(40, 40, 40))

    d.rectangle([18, 18, 440, 48], fill=(50, 65, 85))
    d.text((24, 22), (cn_title or kind)[:28], fill=(230, 230, 230), font=f_title)
    y = 58
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((26, y), ln[:56], fill=(30, 30, 30), font=font)
        y += 18
    d.rectangle([50, 125, 410, 141], fill=(175, 165, 145))
    d.text((54, 127), "~~ torn fold ~~", fill=(100, 90, 75), font=f_tiny)
    # rotated-ish stamp (offset oval)
    for (cx, cy, label, col) in [(350, 155, stamp, (190, 40, 40)), (290, 205, "VOID", (150, 55, 55))]:
        d.ellipse([cx - 55, cy - 24, cx + 45, cy + 32], outline=col, width=3)
        d.text((cx - 20, cy - 6), label[:6], fill=col, font=f_stamp)

    d.rectangle([480, 40, 900, 280], fill=(245, 245, 248), outline=(60, 60, 60), width=2)
    d.rectangle([480, 40, 900, 68], fill=(70, 70, 95))
    d.text((490, 46), "WIN-B VOID / IGNORE", fill=(255, 220, 220), font=f_sm)
    d.text((490, 80), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((490, 100), "tiny distractor 888.00", fill=(20, 20, 20), font=f_sm)
    d.text((490, 120), "FX bait $777.00", fill=(20, 20, 20), font=f_sm)
    d.text((490, 150), f"{fid} status=void invoice#OLD", fill=(40, 40, 40), font=f_tiny)
    d.rectangle([0, 550, 920, 580], fill=(25, 25, 32))
    d.text((10, 556), "Start | Torn | POS | Chat  [V9]", fill=(200, 200, 200), font=f_tiny)
    px = img.load()
    for _ in range(1600):
        x, y = rng.randint(0, 919), rng.randint(0, 579)
        v = rng.randint(0, 40)
        r, g, b = px[x, y]
        px[x, y] = (max(0, r - v), max(0, g - v), max(0, b - v))
    img = ImageEnhance.Contrast(img).enhance(0.88)
    img = img.filter(ImageFilter.SMOOTH)
    outp = FIX / f"{fid}_{kind}.png"
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "capture_blend": capture,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "hardening": [
            "torn_edge", "barcode_distract", "fx_confuse", "ghost_page",
            "qr_noise", "rotated_stamp", "watermark_666",
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
        "version": "v9", "n": len(items), "gate": GATE,
        "theme": "torn_barcode_fx_ghost_qr",
        "harder_than": "v8",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C160",
        "theme": "vision_v9_design_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "harder_than": "v8",
        "hardening": man["theme"],
        "smoke_deferred_to": "C163+",
        "v8_train_rate": 1.0,
        "v8_heldout_rate": 0.9375,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "pass": len(items) >= 16,
        "claim": False,
        "note": "V9 fixtures ready; claim only after real VL smoke >=0.6",
    }
    J(DOC / "C160_V9_DESIGN_BATCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C160", "n": len(items), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
