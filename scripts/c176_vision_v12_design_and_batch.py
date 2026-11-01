# -*- coding: utf-8 -*-
"""C176: Vision V12 design + fixtures (harder than V11).
Hardening: torn edges, barcode noise, perspective warp, QR bait,
thermal fade, shadow cast, JPEG blocking, dense bilingual stamp,
double-exposure ghost, low-res downsample.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v12"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V12_PROTOCOL.md"
RUN = ROOT / "runs/vision_v12_c176"

SPECS = [
    ("v12_01", "torn_receipt", "paid_total", 28.75,
     ["TORN RECEIPT V12", "a paid 13.50", "b paid 15.25", "c open 4.00", "TOTAL PAID TARGET 28.75"],
     "撕边收据", "RECV"),
    ("v12_02", "barcode_wh", "qty_sum", 34.0,
     ["WH BARCODE V12", "SKU1 qty 18 ok", "SKU2 qty 3 hold", "SKU3 qty 16 ok", "qty_sum TARGET 34"],
     "条码仓单", "RECV"),
    ("v12_03", "persp_refund", "refund_done", 15.5,
     ["PERSP REFUND V12", "itemR1 6.00 done", "itemR2 9.50 done", "itemR3 2.50 open", "refund_done TARGET 15.50"],
     "透视退款", "DONE"),
    ("v12_04", "qr_tax", "tax_base_paid", 47.0,
     ["TAX QR V12", "T1 25.00 paid", "T2 11.00 open", "T3 22.00 paid", "tax_base_paid TARGET 47.00"],
     "二维码税联", "RECV"),
    ("v12_05", "thermal_payroll", "payroll_active", 1050.0,
     ["PAYROLL THERMAL V12", "A 560 active", "B 90 leave", "C 490 active", "payroll_active TARGET 1050"],
     "热敏薪资", "OK"),
    ("v12_06", "shadow_ship", "ship_ok_qty", 26.0,
     ["SHIP SHADOW V12", "P1 14 ok", "P2 6 hold", "P3 12 ok", "ship_ok_qty TARGET 26"],
     "阴影发货", "SHIP"),
    ("v12_07", "jpeg_sla", "open_pri_sum", 18.0,
     ["SLA JPEG V12", "S1 pri 9 open", "S2 pri 14 closed", "S3 pri 9 open", "open_pri_sum TARGET 18"],
     "压缩SLA", "OPEN"),
    ("v12_08", "stamp_exp", "paid_total", 51.25,
     ["EXPENSE STAMP V12", "E1 28.00 paid", "E2 10.00 void", "E3 23.25 paid", "paid_total TARGET 51.25"],
     "密章报销", "RECV"),
    ("v12_09", "ghost_po", "paid_total", 40.5,
     ["PO-GHOST V12", "itemA paid 21.00", "itemB paid 19.50", "itemC open 8.00", "TOTAL PAID TARGET 40.50"],
     "重影采购", "RECV"),
    ("v12_10", "lores_order", "paid_total", 29.0,
     ["ORDER LORES V12", "A paid 16.00", "B paid 13.00", "C open 5.50", "TOTAL PAID TARGET 29.00"],
     "低清订单", "RECV"),
    ("v12_11", "torn_dup", "paid_total", 33.0,
     ["INVOICE #V12-DUP", "line paid 11.00", "line paid 11.00", "line paid 11.00", "TOTAL PAID TARGET 33.00"],
     "撕边重复", "RECV"),
    ("v12_12", "thermal_zero", "paid_total", 0.0,
     ["OPEN ONLY V12", "X 17.00 open", "Y 19.00 open", "paid_total TARGET 0.00"],
     "热敏未付", "HOLD"),
    ("v12_13", "persp_ledger", "paid_total", 18.5,
     ["LEDGER PERSP V12", "rA paid 9.25", "rB paid 9.25", "rC open 4.00", "TOTAL PAID TARGET 18.50"],
     "透视账本", "RECV"),
    ("v12_14", "barcode_ui", "paid_total", 23.75,
     ["UI BARCODE V12", "alpha paid 11.25", "beta paid 12.50", "gamma open 3.00", "TOTAL PAID TARGET 23.75"],
     "条码界面", "RECV"),
    ("v12_15", "shadow_stack", "paid_total", 37.0,
     ["HEAVY SHADOW V12", "x paid 19.00 usd", "y paid 18.00 usd", "z open 7.00 usd", "TOTAL PAID TARGET 37.00"],
     "阴影叠窗", "RECV"),
    ("v12_16", "qr_mix", "paid_total", 24.5,
     ["CN-EN QR MIX V12", "tea paid 11.00", "rice paid 13.50", "soup open 2.50", "TOTAL PAID TARGET 24.50"],
     "中英二维码", "RECV"),
    ("v12_17", "jpeg_win", "paid_total", 41.25,
     ["JPEG WIN V12", "w1 paid 20.00", "w2 paid 21.25", "w3 open 9.00", "TOTAL PAID TARGET 41.25"],
     "压缩双窗", "RECV"),
    ("v12_18", "ghost_foot", "paid_total", 16.75,
     ["GHOST FOOT V12", "p1 paid 8.00", "p2 paid 8.75", "p3 open 3.00", "TOTAL PAID TARGET 16.75"],
     "重影脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V12 Protocol — Torn / Barcode / Perspective / QR / Thermal / Shadow / JPEG / Ghost

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V11: **torn edges**, **barcode noise**, **perspective warp**, **QR bait**,
**thermal fade**, **shadow cast**, **JPEG blocking**, **dense bilingual stamp**,
**double-exposure ghost**, **low-res downsample**. Still scoped office OCR+atom.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke (C177)

## Honesty
- V11 train/heldout retained when claimed
- Gate2/3 untouched. gen11 HOLD. No fake VL scores here.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v12") & 0xFFFFFFFF)
    try:
        from PIL import ImageGrab
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        bg = shot.crop((0, 0, min(1200, w), min(780, h))).convert("RGB").resize((1020, 660))
        paper = Image.new("RGB", (1020, 660), (200, 195, 185))
        img = Image.blend(bg, paper, 0.64)
        capture = True
    except Exception:
        img = Image.new("RGB", (1020, 660), (200, 195, 185))
        capture = False
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 14)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 11)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 11)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 10)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 40)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 9)
        f_cn = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 12)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_wm = f_tiny = f_cn = ImageFont.load_default()

    # Main paper with torn edge zig-zag left
    d.rectangle([40, 20, 500, 560], fill=(230, 224, 214), outline=(55, 55, 55), width=2)
    for ty in range(20, 560, 18):
        d.polygon([(40, ty), (28, ty + 9), (40, ty + 18)], fill=(200, 195, 185))

    # barcode noise strip
    bx0, by0 = 520, 40
    for i in range(60):
        bw = rng.randint(1, 3)
        d.rectangle([bx0 + i * 3, by0, bx0 + i * 3 + bw, by0 + 70], fill=(10, 10, 10))
    d.text((520, 115), "BARCODE bait 888.88 IGNORE", fill=(80, 80, 80), font=f_tiny)

    # QR bait (fake modules)
    qx, qy = 760, 40
    d.rectangle([qx, qy, qx + 90, qy + 90], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    for yy in range(qy + 4, qy + 86, 6):
        for xx in range(qx + 4, qx + 86, 6):
            if rng.random() > 0.45:
                d.rectangle([xx, yy, xx + 4, yy + 4], fill=(0, 0, 0))
    d.text((qx, qy + 95), "QR=999.00 bait", fill=(120, 40, 40), font=f_tiny)

    # ghost / double exposure faint duplicate of bait totals
    d.text((80, 300), "GHOST paid 777.00", fill=(210, 205, 198), font=f_wm)
    d.text((120, 380), "OLD TOTAL 666.00", fill=(205, 200, 193), font=f_sm)

    d.rectangle([48, 28, 330, 56], fill=(35, 50, 70))
    d.text((54, 32), (cn_title or kind)[:22], fill=(230, 230, 230), font=f_title)
    y = 70
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        fill = (20, 20, 20) if y < 160 else (50, 50, 50) if y < 200 else (90, 90, 90)
        d.text((55, y), ln[:52], fill=fill, font=font)
        y += 18

    # dense bilingual stamps
    for (cx, cy, label, col) in [
        (380, 140, stamp, (190, 40, 40)),
        (300, 220, "作废", (150, 55, 55)),
        (420, 280, "VOID", (160, 40, 40)),
        (250, 160, "已核", (40, 100, 40)),
    ]:
        d.ellipse([cx - 48, cy - 22, cx + 38, cy + 26], outline=col, width=3)
        d.text((cx - 16, cy - 6), label[:4], fill=col, font=f_stamp)

    # chat void window
    d.rectangle([720, 200, 1000, 420], fill=(248, 248, 255), outline=(50, 50, 80), width=2)
    d.rectangle([720, 200, 1000, 228], fill=(70, 50, 100))
    d.text((730, 206), "VOID WIN IGNORE", fill=(255, 220, 220), font=f_sm)
    d.text((730, 240), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((730, 265), "QR fee 444.00", fill=(20, 20, 20), font=f_sm)
    d.text((730, 290), f"{fid} void#OLD", fill=(40, 40, 40), font=f_tiny)

    d.rectangle([720, 450, 1000, 620], fill=(240, 250, 240), outline=(40, 90, 40), width=2)
    d.text((730, 460), "CAL bait 666.00", fill=(20, 20, 20), font=f_sm)
    d.text((730, 490), "do not parse", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 630, 1020, 660], fill=(15, 15, 25))
    d.text((10, 638), "Start | Torn | Barcode | QR | Thermal | Shadow | JPEG  [V12]", fill=(200, 200, 200), font=f_tiny)

    # shadow cast (dark gradient blob)
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([60, 400, 420, 580], fill=(0, 0, 0, 70))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")

    # perspective-ish affine warp
    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.06, -22, 0.02, 1, -6),
        resample=Image.BICUBIC, fillcolor=(200, 195, 185),
    )

    # thermal fade (low contrast + slight yellow)
    img = ImageEnhance.Brightness(img).enhance(0.88)
    img = ImageEnhance.Contrast(img).enhance(0.72)
    img = ImageEnhance.Color(img).enhance(0.85)

    # low-res downsample then up
    if "lores" in kind or rng.random() > 0.55:
        small = img.resize((w // 3, h // 3), Image.BILINEAR)
        img = small.resize((w, h), Image.NEAREST)

    # JPEG blocking
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=28)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")

    # noise
    px = img.load()
    ww, hh = img.size
    for _ in range(3200):
        x, y = rng.randint(0, ww - 1), rng.randint(0, hh - 1)
        v = rng.randint(0, 55)
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
            "torn_edges", "barcode_noise", "perspective_warp", "qr_bait",
            "thermal_fade", "shadow_cast", "jpeg_blocking", "dense_bilingual_stamp",
            "double_exposure_ghost", "lowres_downsample",
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
        "version": "v12", "n": len(items), "gate": GATE,
        "theme": "torn_barcode_persp_qr_thermal_shadow_jpeg_ghost",
        "harder_than": "v11",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C176",
        "theme": "vision_v12_design_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "harder_than": "v11",
        "hardening": man["theme"],
        "smoke_deferred_to": "C177",
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "pass": len(items) >= 16,
        "claim": False,
        "note": "V12 fixtures ready; claim only after real VL smoke >=0.6",
    }
    J(DOC / "C176_V12_DESIGN_BATCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C176", "n": len(items), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
