# -*- coding: utf-8 -*-
"""C187: Vision V14 design + fixtures (harder than V13).
Hardening: salt-pepper, moire scanlines, double-ghost text, tape strips,
redaction bars, wet smear, low-contrast fade, mesh screen, fingerprint oil,
thermal stripes, stronger skew, hail noise.
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
FIX = ROOT / "evo/office/fixtures/vision_images_v14"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V14_PROTOCOL.md"
RUN = ROOT / "runs/vision_v14_c187"

SPECS = [
    ("v14_01", "salt_receipt", "paid_total", 34.75,
     ["SALT RECEIPT V14", "a paid 16.50", "b paid 18.25", "c open 5.50", "TOTAL PAID TARGET 34.75"],
     "椒盐收据", "RECV"),
    ("v14_02", "moire_wh", "qty_sum", 36.0,
     ["WH MOIRE V14", "SKU1 qty 19 ok", "SKU2 qty 7 hold", "SKU3 qty 17 ok", "qty_sum TARGET 36"],
     "摩尔仓单", "RECV"),
    ("v14_03", "ghost_refund", "refund_done", 18.0,
     ["GHOST REFUND V14", "itemR1 8.00 done", "itemR2 10.00 done", "itemR3 3.50 open", "refund_done TARGET 18.00"],
     "重影退款", "DONE"),
    ("v14_04", "tape_tax", "tax_base_paid", 61.0,
     ["TAX TAPE V14", "T1 33.00 paid", "T2 12.00 open", "T3 28.00 paid", "tax_base_paid TARGET 61.00"],
     "胶带税联", "RECV"),
    ("v14_05", "redact_payroll", "payroll_active", 1310.0,
     ["PAYROLL REDACT V14", "A 700 active", "B 90 leave", "C 610 active", "payroll_active TARGET 1310"],
     "涂黑薪资", "OK"),
    ("v14_06", "wet_ship", "ship_ok_qty", 29.0,
     ["SHIP WET V14", "P1 14 ok", "P2 8 hold", "P3 15 ok", "ship_ok_qty TARGET 29"],
     "水渍发货", "SHIP"),
    ("v14_07", "fade_sla", "open_pri_sum", 21.0,
     ["SLA FADE V14", "S1 pri 10 open", "S2 pri 15 closed", "S3 pri 11 open", "open_pri_sum TARGET 21"],
     "淡墨SLA", "OPEN"),
    ("v14_08", "mesh_exp", "paid_total", 53.25,
     ["EXPENSE MESH V14", "E1 28.00 paid", "E2 11.00 void", "E3 25.25 paid", "paid_total TARGET 53.25"],
     "网纹报销", "RECV"),
    ("v14_09", "oil_po", "paid_total", 45.5,
     ["PO-OIL V14", "itemA paid 23.00", "itemB paid 22.50", "itemC open 8.00", "TOTAL PAID TARGET 45.50"],
     "指纹采购", "RECV"),
    ("v14_10", "thermal_order", "paid_total", 33.25,
     ["ORDER THERMAL V14", "A paid 17.00", "B paid 16.25", "C open 6.00", "TOTAL PAID TARGET 33.25"],
     "热敏订单", "RECV"),
    ("v14_11", "skew_dup", "paid_total", 39.0,
     ["INVOICE #V14-DUP", "line paid 13.00", "line paid 13.00", "line paid 13.00", "TOTAL PAID TARGET 39.00"],
     "强斜重复", "RECV"),
    ("v14_12", "hail_zero", "paid_total", 0.0,
     ["OPEN ONLY V14", "X 22.00 open", "Y 25.00 open", "paid_total TARGET 0.00"],
     "雹点未付", "HOLD"),
    ("v14_13", "salt_ledger", "paid_total", 26.5,
     ["LEDGER SALT V14", "rA paid 13.25", "rB paid 13.25", "rC open 4.00", "TOTAL PAID TARGET 26.50"],
     "椒盐账本", "RECV"),
    ("v14_14", "tape_ui", "paid_total", 31.0,
     ["UI TAPE V14", "alpha paid 15.00", "beta paid 16.00", "gamma open 5.00", "TOTAL PAID TARGET 31.00"],
     "胶带界面", "RECV"),
    ("v14_15", "mesh_stack", "paid_total", 48.0,
     ["HEAVY MESH V14", "x paid 24.00 usd", "y paid 24.00 usd", "z open 9.00 usd", "TOTAL PAID TARGET 48.00"],
     "网纹叠窗", "RECV"),
    ("v14_16", "ghost_mix", "paid_total", 29.75,
     ["CN-EN GHOST MIX V14", "tea paid 13.50", "rice paid 16.25", "soup open 4.00", "TOTAL PAID TARGET 29.75"],
     "中英重影", "RECV"),
    ("v14_17", "wet_win", "paid_total", 47.0,
     ["WET WIN V14", "w1 paid 23.00", "w2 paid 24.00", "w3 open 11.00", "TOTAL PAID TARGET 47.00"],
     "水渍双窗", "RECV"),
    ("v14_18", "oil_foot", "paid_total", 19.5,
     ["OIL FOOT V14", "p1 paid 9.50", "p2 paid 10.00", "p3 open 3.00", "TOTAL PAID TARGET 19.50"],
     "指纹脚注", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V14 Protocol — Salt / Moire / Ghost / Tape / Redact / Wet / Mesh

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V13: **salt-pepper**, **moire scanlines**, **double-ghost**, **tape strips**,
**redaction bars**, **wet smear**, **low-contrast fade**, **mesh screen**, **fingerprint oil**,
**thermal stripes**, **stronger skew**, **hail noise**.
Still scoped office OCR+atom. Mild-readable TARGET for honest VL.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke (C188)

## Honesty
- V13 train/heldout retained when claimed
- Gate2/3 untouched. gen11 HOLD. No fake VL scores here.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v14") & 0xFFFFFFFF)
    img = Image.new("RGB", (1060, 700), (205, 200, 190))
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 15)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 13)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 34)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = f_wm = ImageFont.load_default()

    # main panel
    d.rectangle([34, 16, 550, 590], fill=(244, 238, 228), outline=(30, 30, 30), width=2)

    # crumple arcs (retain V13)
    for _ in range(12):
        x0 = rng.randint(40, 500)
        y0 = rng.randint(40, 540)
        d.arc([x0, y0, x0 + rng.randint(40, 120), y0 + rng.randint(20, 60)], 0, 180, fill=(195, 190, 180), width=1)

    # highlighter + sticky bait
    d.rectangle([48, 100, 510, 122], fill=(255, 255, 110))
    d.rectangle([370, 210, 530, 295], fill=(255, 248, 110), outline=(170, 150, 30), width=2)
    d.text((380, 220), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((380, 245), "bait 888.00", fill=(80, 60, 20), font=f_tiny)
    d.text((380, 268), "IGNORE", fill=(80, 60, 20), font=f_tiny)

    # tape strips (away from TARGET lines)
    d.rectangle([60, 300, 200, 322], fill=(240, 220, 140, ) if False else (240, 220, 140))
    d.rectangle([420, 420, 540, 445], fill=(235, 210, 130))

    # redaction bars (bait region only — not covering TARGET text block)
    d.rectangle([560, 80, 720, 110], fill=(10, 10, 10))
    d.rectangle([560, 130, 700, 155], fill=(10, 10, 10))
    d.text((560, 165), "REDACT bait", fill=(80, 80, 80), font=f_tiny)

    # coffee / wet smear
    wet = Image.new("RGBA", img.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(wet)
    wd.ellipse([70, 430, 240, 580], outline=(100, 60, 30, 100), width=12)
    wd.ellipse([95, 455, 215, 555], fill=(130, 75, 40, 45))
    wd.ellipse([300, 500, 420, 620], fill=(90, 110, 140, 35))
    img = Image.alpha_composite(img.convert("RGBA"), wet).convert("RGB")
    d = ImageDraw.Draw(img)

    # punch holes + fax lines
    for hy in (50, 180, 320, 460):
        d.ellipse([16, hy, 32, hy + 14], fill=(205, 200, 190), outline=(40, 40, 40), width=1)
    for fy in range(28, 580, 6):
        if rng.random() > 0.4:
            d.line([(36, fy), (548, fy)], fill=(190, 185, 180), width=1)

    # moire / mesh
    for mx in range(40, 540, 5):
        d.line([(mx, 20), (mx + 8, 580)], fill=(200, 198, 192), width=1)

    # thermal stripes
    for ty in range(40, 560, 18):
        d.rectangle([36, ty, 548, ty + 2], fill=(230, 225, 215))

    # double ghost bait text
    d.text((90, 340), "GHOST bait 666.00", fill=(228, 222, 214), font=f_sm)
    d.text((92, 342), "GHOST bait 666.00", fill=(215, 208, 200), font=f_sm)
    d.text((70, 380), "CONFIDENTIAL", fill=(218, 210, 200), font=f_wm)

    # title + body lines (readable TARGET)
    d.rectangle([44, 24, 340, 54], fill=(20, 40, 60))
    d.text((50, 28), (cn_title or kind)[:20], fill=(240, 240, 240), font=f_title)
    y = 68
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((52, y), ln[:54], fill=(6, 6, 6), font=font)
        y += 22

    # stamps
    for (cx, cy, label, col) in [(400, 130, stamp, (175, 25, 25)), (270, 260, "作废", (135, 45, 45)), (450, 330, "VOID", (145, 35, 35))]:
        d.ellipse([cx - 46, cy - 22, cx + 40, cy + 26], outline=col, width=3)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)

    # void window bait
    d.rectangle([760, 210, 1040, 430], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((770, 220), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 255), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 290), "do not parse", fill=(20, 20, 20), font=f_sm)

    # footer
    d.rectangle([0, 670, 1060, 700], fill=(16, 16, 26))
    d.text((10, 678), "V14 Salt|Moire|Ghost|Tape|Redact|Wet|Mesh|Oil|Thermal  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)

    # salt-pepper + hail
    px = img.load()
    ww, hh = img.size
    for _ in range(1800):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        v = 0 if rng.random() < 0.5 else 255
        px[xx, yy] = (v, v, v)

    # cyan misreg on a band
    for yy in range(130, 200):
        for xx in range(48, min(520, ww - 3)):
            r, g, b = px[xx, yy]
            px[xx, yy] = (r, g, min(255, b + 20))

    # fingerprint oil blob
    oil = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(oil)
    od.ellipse([480, 480, 580, 580], fill=(90, 70, 40, 50))
    for i in range(5):
        od.arc([485 + i, 485 + i, 575 - i, 575 - i], 0, 270, fill=(60, 40, 20, 40), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), oil).convert("RGB")

    # glare
    glare = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.ellipse([150, 20, 380, 150], fill=(255, 255, 230, 50))
    img = Image.alpha_composite(img.convert("RGBA"), glare).convert("RGB")

    # stronger skew
    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.04, -14, 0.015, 1, -4),
        resample=Image.BICUBIC, fillcolor=(205, 200, 190),
    )
    img = ImageEnhance.Contrast(img).enhance(0.88)
    img = ImageEnhance.Brightness(img).enhance(0.92)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=48)
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
            "salt_pepper", "moire_scanlines", "double_ghost", "tape_strips",
            "redaction_bars", "wet_smear", "low_contrast_fade", "mesh_screen",
            "fingerprint_oil", "thermal_stripes", "stronger_skew", "hail_noise",
            "cyan_misreg", "jpeg_q48",
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
        "version": "v14", "n": len(items), "gate": GATE,
        "theme": "salt_moire_ghost_tape_redact_wet_mesh_oil_thermal",
        "harder_than": "v13",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C187",
        "theme": "vision_v14_design_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "harder_than": "v13",
        "pass": len(items) >= 16,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "Fixtures only; claim deferred to C188 smoke",
    }
    J(DOC / "C187_V14_DESIGN_BATCH.json", out)
    RUN.mkdir(parents=True, exist_ok=True)
    J(RUN / "design.json", out)
    print(json.dumps({"cycle": "C187", "n": len(items), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
