# -*- coding: utf-8 -*-
"""C143: Vision V7 protocol + fixtures harder than V6.
Hardening: occlusion bands, tiny fonts, stamped receipts.
Smoke deferred to C144. Gate 0.6. No Gate2/3. gen11 HOLD.
"""
from __future__ import annotations
import json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs/r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v7"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V7_PROTOCOL.md"
RUN = ROOT / "runs/vision_v7_c143"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL_MD = """# 蚁算-视 VL Gate V7 Protocol — Occlusion / Tiny Font / Stamped Receipt

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V6: **occlusion** (stamps, bands), **tiny fonts** on line items,
and **stamped receipt** chrome. Still scoped office OCR+atom (not open-domain VQA).

## Gate
- Numeric gate: **0.6**
- n ≥ **14** fixtures
- Per item: `ocr_ok` AND `atom_ok`
- `rate = n_ok / n` ≥ 0.6 to PASS
- Claim: `vl_gate_v7_claim=true` only if PASS + real VL (C144)

## Hardening vs V6
- Line-item fonts ~9–10pt; TARGET kept readable but smaller than V6
- Red circular RECEIVED/PAID stamps overlapping mid-panel
- Semi-transparent occlusion bands & coffee-stain ellipses
- Receipt stub chrome + torn-edge noise
- Retain multi-window distractors (WIN-B void / WIN-C chat)

## Honesty
- Real VL only. No synthetic OCR pretending to be VL.
- Prior V0–V6 claims untouched. Gate2/3 untouched. gen11 HOLD.
- Claim only when rate≥0.6.

## Fixtures
- Path: `evo/office/fixtures/vision_images_v7`
- Manifest: `manifest.json`
"""


def make_fixture(i, kind, lines, metric, expected, cn_title=None, stamp="PAID"):
    from PIL import Image, ImageDraw, ImageFont, ImageGrab
    FIX.mkdir(parents=True, exist_ok=True)
    try:
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        bg = shot.crop((0, 0, min(1100, w), min(720, h))).convert("RGB").resize((920, 580))
        img = Image.blend(bg, Image.new("RGB", (920, 580), (250, 248, 242)), 0.55)
        capture = True
    except Exception:
        img = Image.new("RGB", (920, 580), (250, 248, 242))
        capture = False
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 9)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 10)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 18)
    except Exception:
        try:
            f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 14)
            f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 9)
            f_sm = f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
            f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 16)
        except Exception:
            f_title = f_tiny = f_sm = f_tgt = f_stamp = ImageFont.load_default()

    # receipt paper
    d.rectangle([8, 8, 440, 540], fill=(255, 252, 245), outline=(40, 40, 40), width=2)
    # torn edge ticks
    for y in range(20, 520, 18):
        d.line([(8, y), (14, y + 6)], fill=(180, 180, 180), width=1)

    # taskbar noise
    d.rectangle([0, 550, 920, 580], fill=(28, 28, 36))
    d.text((10, 556), "Start | Mail | POS | Chat  [7]", fill=(210, 210, 210), font=f_tiny)

    # WIN-A receipt body
    d.rectangle([16, 16, 430, 48], fill=(30, 80, 140))
    title = cn_title or f"V7 RECEIPT {kind}"
    d.text((22, 20), title[:30], fill=(255, 255, 255), font=f_title)
    y = 56
    for idx, ln in enumerate(lines):
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_tiny
        d.text((24, y), ln[:48], fill=(10, 10, 10), font=font)
        y += 16 if font is f_tiny else 18

    # occlusion band across mid lines
    d.rectangle([40, 120, 400, 138], fill=(220, 200, 160))
    d.text((44, 122), "~~ fold crease ~~", fill=(120, 100, 80), font=f_tiny)

    # coffee stain
    d.ellipse([300, 200, 390, 270], outline=(160, 110, 70), width=3)
    d.ellipse([310, 210, 380, 260], fill=(200, 160, 110))

    # red stamp overlapping amounts zone
    cx, cy = 320, 160
    d.ellipse([cx - 55, cy - 35, cx + 55, cy + 35], outline=(200, 30, 30), width=4)
    d.text((cx - 38, cy - 12), stamp[:8], fill=(200, 30, 30), font=f_stamp)

    # second faint stamp
    d.ellipse([60, 300, 160, 360], outline=(180, 60, 60), width=2)
    d.text((72, 320), "RECEIVED", fill=(180, 60, 60), font=f_tiny)

    # WIN-B noise
    d.rectangle([460, 16, 900, 260], outline=(110, 110, 110), width=2)
    d.rectangle([460, 16, 900, 42], fill=(90, 90, 90))
    d.text((468, 20), "WIN-B VOID / IGNORE 999", fill=(255, 255, 180), font=f_sm)
    noise = [
        "old total 999.00 stamped",
        "status=void invoice#OLD",
        "CN draft / EN void",
        f"marker V7-{i:02d}",
        "tiny distractor 888.00",
        "occlusion copy TOTAL 42",
    ]
    y = 52
    for ln in noise:
        d.text((468, y), ln, fill=(60, 60, 60), font=f_tiny)
        y += 16

    # WIN-C chat chrome
    d.rectangle([480, 280, 900, 520], outline=(50, 50, 130), width=2)
    d.rectangle([480, 280, 900, 306], fill=(50, 50, 130))
    d.text((488, 284), "WIN-C chat / stamped spam", fill=(255, 255, 255), font=f_tiny)
    chrome = ["re: lunch total 42?", "stamp preview", "ignore DRAFT 777", "emoji ??", "关闭窗口"]
    y = 316
    for ln in chrome:
        d.text((488, y), ln, fill=(40, 40, 90), font=f_tiny)
        y += 16

    # badge
    d.ellipse([400, 10, 428, 38], fill=(220, 30, 30))
    d.text((408, 14), "!", fill=(255, 255, 255), font=f_tiny)

    name = f"v7_{i:02d}_{kind}.png"
    path = FIX / name
    img.save(path)
    return {
        "id": f"v7_{i:02d}",
        "file": name,
        "kind": kind,
        "metric": metric,
        "expected": expected,
        "lines": lines,
        "cn_title": cn_title,
        "stamp": stamp,
        "capture_blend": capture,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "hardening": ["occlusion", "tiny_font", "stamped_receipt"],
    }


def build_batch():
    specs = [
        ("receipt_paid", ["RECEIPT #V7-01", "latte paid 4.50", "sandwich paid 12.00", "juice open 3.00", "TOTAL PAID TARGET 16.50"], "paid_total", 16.50, "收据 Receipt", "PAID"),
        ("stamp_wh", ["WH TICKET V7", "BOLT qty 12 ok", "NUT qty 8 hold", "WASH qty 5 ok", "qty_sum TARGET 17"], "qty_sum", 17.0, "仓收据 Warehouse", "RECV"),
        ("tiny_refund", ["REFUND STUB", "R1 3.25 done", "R2 5.00 open", "R3 1.75 done", "refund_done TARGET 5.00"], "refund_done", 5.00, "退款小票 Refund", "DONE"),
        ("tax_stamp", ["TAX SLIP", "T1 7.00 paid", "T2 4.50 open", "T3 9.00 paid", "tax_base_paid TARGET 16.00"], "tax_base_paid", 16.00, "税联 Tax", "PAID"),
        ("payroll_tiny", ["PAYROLL SLIP", "A 450 active", "B 80 leave", "C 350 active", "payroll_active TARGET 800"], "payroll_active", 800.0, "薪资条 Payroll", "OK"),
        ("ship_occlude", ["SHIP RECEIPT", "P1 4 ok", "P2 9 hold", "P3 3 ok", "ship_ok_qty TARGET 7"], "ship_ok_qty", 7.0, "发货单 Ship", "SHIP"),
        ("sla_stamp", ["SLA TICKET", "S1 pri 2 open", "S2 pri 8 closed", "S3 pri 5 open", "open_pri_sum TARGET 7"], "open_pri_sum", 7.0, "服务单 SLA", "OPEN"),
        ("expense_tiny", ["EXPENSE STUB", "E1 18.00 paid", "E2 9.00 void", "E3 7.50 paid", "paid_total TARGET 25.50"], "paid_total", 25.50, "报销小票 Expense", "PAID"),
        ("po_stamp", ["PO-77 STAMPED", "line1 paid 5.50", "line2 paid 9.50", "line3 open 2.00", "TOTAL PAID TARGET 15.00"], "paid_total", 15.00, "采购联 PO", "RECV"),
        ("order_mix", ["ORDER OFFICE", "A paid 6.25", "B paid 8.75", "C open 1.00", "TOTAL PAID TARGET 15.00"], "paid_total", 15.00, "订单 Order", "PAID"),
        ("dup_stamp", ["INVOICE #V7-DUP", "paid 2.00", "paid 3.50", "paid 4.50", "TOTAL PAID TARGET 10.00"], "paid_total", 10.00, "重复盖章 Dup", "PAID"),
        ("edge_zero", ["OPEN ONLY STUB", "X 11.00 open", "Y 19.00 open", "paid_total TARGET 0.00"], "paid_total", 0.0, "未付 Open", "HOLD"),
        ("occlude_mid", ["LEDGER V7", "row1 paid 2.75", "row2 paid 5.25", "row3 open 0.50", "TOTAL PAID TARGET 8.00"], "paid_total", 8.00, "遮挡账本 Ledger", "PAID"),
        ("ui_stamp", ["UI RECEIPT", "alpha paid 1.50", "beta paid 6.50", "gamma open 4.00", "TOTAL PAID TARGET 8.00"], "paid_total", 8.00, "界面小票 UI", "PAID"),
        ("stamp_heavy", ["HEAVY STAMP", "x paid 10.00", "y paid 5.00", "z open 2.00", "TOTAL PAID TARGET 15.00"], "paid_total", 15.00, "重章 Heavy", "PAID"),
        ("tiny_cn", ["中英小票 MIX", "甲 paid 3.00", "乙 paid 7.00", "丙 open 2.00", "TOTAL PAID TARGET 10.00"], "paid_total", 10.00, "中英盖章 Mix", "验讫"),
    ]
    items = []
    for i, (kind, lines, metric, expected, cn_title, stamp) in enumerate(specs, 1):
        items.append(make_fixture(i, kind, lines, metric, expected, cn_title=cn_title, stamp=stamp))
    man = {
        "version": "v7",
        "n": len(items),
        "gate": GATE,
        "theme": "occlusion_tiny_font_stamped_receipt",
        "harder_than": "v6",
        "items": items,
        "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    return man


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    if FIX.exists():
        shutil.rmtree(FIX)
    PROTO.write_text(PROTOCOL_MD.format(ts=ts()), encoding="utf-8")
    man = build_batch()
    out = {
        "cycle": "C143",
        "theme": "v7_design_occlusion_tiny_stamped",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "fixtures_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "n_fixtures": man["n"],
        "manifest": str((FIX / "manifest.json").relative_to(ROOT)).replace("\\", "/"),
        "harder_than_v6": True,
        "pass": man["n"] >= 14 and PROTO.is_file(),
        "claim": False,
        "vl_gate_v7_claim": False,
        "note": "V7 protocol+fixtures landed. Claim deferred to C144 smoke with real VL.",
    }
    J(DOC / "C143_V7_DESIGN_BATCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C143",
        "n_fixtures": man["n"],
        "pass": out["pass"],
        "claim": False,
    }, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
