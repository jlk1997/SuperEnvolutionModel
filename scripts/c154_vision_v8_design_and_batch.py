# -*- coding: utf-8 -*-
"""C154: Vision V8 protocol + fixtures harder than V7.
Hardening: low-contrast, fax/carbon noise, multi-stamp stack, skew bands,
watermark money distractors, handwritten scribble overlays.
Smoke deferred to C155. Gate 0.6. No Gate2/3. gen11 HOLD.
"""
from __future__ import annotations
import json, math, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs/r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v8"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V8_PROTOCOL.md"
RUN = ROOT / "runs/vision_v8_c154"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL_MD = """# 蚁算-视 VL Gate V8 Protocol — Low-contrast / Fax / Multi-stamp / Watermark

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V7: **low-contrast paper**, **fax/carbon scan noise**, **stacked stamps**,
**skew/fold bands**, **watermark money distractors**, **handwritten scribble**.
Still scoped office OCR+atom (not open-domain VQA).

## Gate
- Numeric gate: **0.6**
- n ≥ **16** fixtures
- Per item: `ocr_ok` AND `atom_ok`
- `rate = n_ok / n` ≥ 0.6 to PASS
- Claim: `vl_gate_v8_claim=true` only if PASS + real VL (C155)

## Hardening vs V7
- Paper fill ~ (210,205,195) on noisy bg; ink ~ (45,45,45) (lower contrast)
- Speckle + horizontal fax lines
- Two overlapping circular stamps (PAID + VOID ghost)
- Watermark big digits (777/666) behind line items — must be ignored
- Diagonal scribble lines simulating pen marks
- Tiny 8–9pt fonts; TARGET still present but muted
- Retain occlusion fold + coffee stain from V7 vocabulary

## Honesty
- Real VL only. No synthetic OCR pretending to be VL.
- Prior V0–V7 claims untouched. Gate2/3 untouched. gen11 HOLD.
- Claim only when rate≥0.6.

## Fixtures
- Path: `evo/office/fixtures/vision_images_v8`
- Manifest: `manifest.json`
"""


SPECS = [
    ("v8_01", "fax_receipt", "paid_total", 21.5,
     ["RECEIPT #V8-01", "tea paid 6.50", "bun paid 15.00", "soup open 4.00", "TOTAL PAID TARGET 21.50"],
     "传真收据 Fax", "PAID"),
    ("v8_02", "carbon_wh", "qty_sum", 19.0,
     ["WH TICKET V8", "SCREW qty 11 ok", "WASHER qty 6 hold", "PIN qty 8 ok", "qty_sum TARGET 19"],
     "复写仓单 Carbon", "RECV"),
    ("v8_03", "lowcon_refund", "refund_done", 6.25,
     ["REFUND STUB V8", "R1 2.00 done", "R2 4.25 done", "R3 9.00 open", "refund_done TARGET 6.25"],
     "低对比退款", "DONE"),
    ("v8_04", "watermark_tax", "tax_base_paid", 22.0,
     ["TAX SLIP V8", "T1 10.00 paid", "T2 5.00 open", "T3 12.00 paid", "tax_base_paid TARGET 22.00"],
     "水印税联", "PAID"),
    ("v8_05", "scribble_pay", "payroll_active", 920.0,
     ["PAYROLL V8", "A 500 active", "B 90 leave", "C 420 active", "payroll_active TARGET 920"],
     "涂鸦薪资", "OK"),
    ("v8_06", "fax_ship", "ship_ok_qty", 11.0,
     ["SHIP RECEIPT V8", "P1 6 ok", "P2 4 hold", "P3 5 ok", "ship_ok_qty TARGET 11"],
     "传真发货", "SHIP"),
    ("v8_07", "stampstack_sla", "open_pri_sum", 9.0,
     ["SLA TICKET V8", "S1 pri 3 open", "S2 pri 7 closed", "S3 pri 6 open", "open_pri_sum TARGET 9"],
     "叠章 SLA", "OPEN"),
    ("v8_08", "carbon_exp", "paid_total", 33.75,
     ["EXPENSE V8", "E1 20.25 paid", "E2 11.00 void", "E3 13.50 paid", "paid_total TARGET 33.75"],
     "复写报销", "PAID"),
    ("v8_09", "po_watermark", "paid_total", 27.0,
     ["PO-88 V8", "itemA paid 12.00", "itemB paid 15.00", "itemC open 3.50", "TOTAL PAID TARGET 27.00"],
     "水印采购", "RECV"),
    ("v8_10", "skew_order", "paid_total", 18.5,
     ["ORDER V8", "A paid 7.25", "B paid 11.25", "C open 2.00", "TOTAL PAID TARGET 18.50"],
     "倾斜订单", "PAID"),
    ("v8_11", "dup_fax", "paid_total", 14.0,
     ["INVOICE #V8-DUP", "paid 4.00", "paid 5.00", "paid 5.00", "TOTAL PAID TARGET 14.00"],
     "传真重复", "PAID"),
    ("v8_12", "edge_zero_lc", "paid_total", 0.0,
     ["OPEN ONLY V8", "X 14.00 open", "Y 22.00 open", "paid_total TARGET 0.00"],
     "低对比未付", "HOLD"),
    ("v8_13", "ledger_scribble", "paid_total", 12.5,
     ["LEDGER V8", "rA paid 4.50", "rB paid 8.00", "rC open 1.25", "TOTAL PAID TARGET 12.50"],
     "涂鸦账本", "PAID"),
    ("v8_14", "ui_fax", "paid_total", 9.75,
     ["UI RECEIPT V8", "alpha paid 2.25", "beta paid 7.50", "gamma open 3.00", "TOTAL PAID TARGET 9.75"],
     "界面传真", "PAID"),
    ("v8_15", "heavy_stack", "paid_total", 24.0,
     ["HEAVY STACK V8", "x paid 16.00", "y paid 8.00", "z open 4.00", "TOTAL PAID TARGET 24.00"],
     "重章叠印", "PAID"),
    ("v8_16", "mix_cn_fax", "paid_total", 13.0,
     ["中英传真 MIX", "甲 paid 5.00", "乙 paid 8.00", "丙 open 3.00", "TOTAL PAID TARGET 13.00"],
     "中英传真", "验讫"),
    ("v8_17", "noise_inv", "paid_total", 31.0,
     ["INVENTORY PAY V8", "lot1 paid 19.00", "lot2 paid 12.00", "lot3 open 6.00", "TOTAL PAID TARGET 31.00"],
     "噪声库存付", "PAID"),
    ("v8_18", "carbon_mix", "paid_total", 16.8,
     ["CARBON MIX V8", "m1 paid 9.30", "m2 paid 7.50", "m3 void 4.00", "TOTAL PAID TARGET 16.80"],
     "复写混合", "PAID"),
]


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid) & 0xFFFFFFFF)
    try:
        from PIL import ImageGrab
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        bg = shot.crop((0, 0, min(1100, w), min(720, h))).convert("RGB").resize((920, 580))
        paper = Image.new("RGB", (920, 580), (210, 205, 195))
        img = Image.blend(bg, paper, 0.72)
        capture = True
    except Exception:
        img = Image.new("RGB", (920, 580), (210, 205, 195))
        capture = False
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 13)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 8)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 9)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 16)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 48)
    except Exception:
        try:
            f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 13)
            f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 8)
            f_sm = f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 9)
            f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 14)
            f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 40)
        except Exception:
            f_title = f_tiny = f_sm = f_tgt = f_stamp = f_wm = ImageFont.load_default()

    # receipt paper low contrast
    d.rectangle([10, 10, 450, 545], fill=(225, 220, 210), outline=(90, 90, 90), width=2)
    # fax horizontal lines
    for y in range(20, 540, 7):
        if rng.random() < 0.55:
            d.line([(12, y), (448, y)], fill=(190, 185, 175), width=1)
    # watermark distractor digits
    d.text((80, 200), "777", fill=(200, 195, 185), font=f_wm)
    d.text((200, 320), "666", fill=(198, 193, 183), font=f_wm)

    d.rectangle([18, 18, 440, 48], fill=(55, 70, 90))
    d.text((24, 22), (cn_title or kind)[:28], fill=(230, 230, 230), font=f_title)
    y = 58
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_tiny
        ink = (50, 50, 50) if font is f_tiny else (35, 35, 35)
        d.text((26, y), ln[:52], fill=ink, font=font)
        y += 15 if font is f_tiny else 17

    # fold occlusion
    d.rectangle([50, 115, 410, 132], fill=(180, 170, 150))
    d.text((54, 117), "~~ fax fold ~~", fill=(110, 100, 85), font=f_tiny)
    # coffee
    d.ellipse([310, 210, 400, 285], outline=(150, 100, 60), width=2)
    d.ellipse([320, 220, 390, 275], fill=(185, 150, 105))

    # stacked stamps
    for (cx, cy, label, col) in [
        (340, 150, stamp, (190, 40, 40)),
        (300, 190, "VOID", (160, 60, 60)),
    ]:
        d.ellipse([cx - 50, cy - 28, cx + 50, cy + 28], outline=col, width=3)
        d.text((cx - 22, cy - 8), label[:6], fill=col, font=f_stamp)

    # handwritten scribble
    for _ in range(6):
        x0, y0 = rng.randint(30, 400), rng.randint(60, 480)
        x1, y1 = x0 + rng.randint(-40, 80), y0 + rng.randint(-20, 40)
        d.line([(x0, y0), (x1, y1)], fill=(40, 40, 120), width=1)

    # WIN-B distractor
    d.rectangle([480, 40, 900, 260], fill=(245, 245, 248), outline=(60, 60, 60), width=2)
    d.rectangle([480, 40, 900, 68], fill=(80, 80, 100))
    d.text((490, 46), "WIN-B VOID / IGNORE", fill=(255, 220, 220), font=f_sm)
    d.text((490, 80), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((490, 100), "tiny distractor 888.00", fill=(20, 20, 20), font=f_sm)
    d.text((490, 120), "occlusion copy TOTAL 42", fill=(20, 20, 20), font=f_sm)
    d.text((490, 150), f"{fid} status=void invoice#OLD", fill=(40, 40, 40), font=f_tiny)

    # taskbar
    d.rectangle([0, 550, 920, 580], fill=(25, 25, 32))
    d.text((10, 556), "Start | Fax | POS | Chat  [V8]", fill=(200, 200, 200), font=f_tiny)

    # speckle noise
    px = img.load()
    for _ in range(1800):
        x, y = rng.randint(0, 919), rng.randint(0, 579)
        v = rng.randint(0, 40)
        r, g, b = px[x, y]
        px[x, y] = (max(0, r - v), max(0, g - v), max(0, b - v))

    img = ImageEnhance.Contrast(img).enhance(0.85)
    img = img.filter(ImageFilter.SMOOTH)
    out = FIX / f"{fid}_{kind}.png"
    img.save(out)
    return {
        "id": fid,
        "file": out.name,
        "kind": kind,
        "metric": metric,
        "expected": expected,
        "lines": lines,
        "cn_title": cn_title,
        "stamp": stamp,
        "capture_blend": capture,
        "path": str(out.relative_to(ROOT)).replace("\\", "/"),
        "hardening": [
            "low_contrast", "fax_carbon_noise", "multi_stamp", "watermark_distract",
            "hand_scribble", "tiny_font", "occlusion",
        ],
    }


def main():
    PROTO.write_text(PROTOCOL_MD.format(ts=ts()), encoding="utf-8")
    if FIX.exists():
        for p in FIX.glob("*.png"):
            p.unlink()
    items = []
    for fid, kind, metric, expected, lines, cn, stamp in SPECS:
        items.append(make_fixture(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v8",
        "n": len(items),
        "gate": GATE,
        "theme": "low_contrast_fax_multistamp_watermark_scribble",
        "harder_than": "v7",
        "items": items,
        "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C154",
        "theme": "vision_v8_design_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "harder_than": "v7",
        "hardening": man["theme"],
        "smoke_deferred_to": "C155",
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "pass": len(items) >= 16,
        "claim": False,
        "note": "V8 fixtures ready; claim only after real VL smoke ≥0.6",
    }
    J(DOC / "C154_V8_DESIGN_BATCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C154", "n": len(items), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
