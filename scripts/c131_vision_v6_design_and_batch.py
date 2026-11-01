# -*- coding: utf-8 -*-
"""C131: Vision V6 protocol + harder noisy UI / multi-window / CN+EN fixtures.
Smoke deferred to C132. Gate 0.6. No Gate2/3. gen11 HOLD.
"""
from __future__ import annotations
import json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs/r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v6"
PROTO = ROOT / "docs" / "蚁算视_VL_GATE_V6_PROTOCOL.md"
RUN = ROOT / "runs/vision_v6_c131"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL_MD = """# 蚁算-视 VL Gate V6 Protocol — Noisy UI / Multi-Window / CN+EN

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V5: **noisy UI chrome**, **multi-window panels**, and **Chinese+English mixed**
office sheets. Tests OCR + atom under distractors (not open-domain VQA).

## Gate
- Numeric gate: **0.6**
- n ≥ **12** fixtures
- Per item: `ocr_ok` AND `atom_ok`
- `rate = n_ok / n` ≥ 0.6 to PASS
- Claim: `vl_gate_v6_claim=true` only if PASS + real VL (C132)

## Hardening vs V5
- Three windows (WIN-A gold / WIN-B noise / WIN-C chrome)
- Fake taskbar + red badges + overlapping labels
- Mixed CN titles with EN metrics (`订单` / `发票` + paid/open)
- Smaller fonts, more distractor numbers (999 / void / DRAFT)
- Desktop blend noise retained

## Honesty
- Real VL only. No synthetic OCR pretending to be VL.
- Prior V0–V5 claims untouched. Gate2/3 untouched. gen11 HOLD.
- Claim only when rate≥0.6.

## Fixtures
- Path: `evo/office/fixtures/vision_images_v6`
- Manifest: `manifest.json`
"""


def make_fixture(i, kind, lines, metric, expected, cn_title=None):
    from PIL import Image, ImageDraw, ImageFont, ImageGrab
    FIX.mkdir(parents=True, exist_ok=True)
    try:
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        bg = shot.crop((0, 0, min(1100, w), min(720, h))).convert("RGB").resize((900, 560))
        img = Image.blend(bg, Image.new("RGB", (900, 560), (248, 248, 252)), 0.48)
        capture = True
    except Exception:
        img = Image.new("RGB", (900, 560), (240, 240, 245))
        capture = False
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 16)
        f = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 13)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 11)
        f_en = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 13)
    except Exception:
        try:
            f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 16)
            f = f_en = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 13)
            f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 11)
        except Exception:
            f_title = f = f_sm = f_en = ImageFont.load_default()

    # fake taskbar
    d.rectangle([0, 530, 900, 560], fill=(30, 30, 40))
    d.text((8, 536), "Start | Mail | Sheets | Chat  [3]", fill=(220, 220, 220), font=f_sm)
    d.ellipse([860, 536, 888, 554], fill=(200, 40, 40))
    d.text((866, 538), "9", fill=(255, 255, 255), font=f_sm)

    # WIN-A gold (left)
    d.rectangle([12, 12, 430, 500], outline=(0, 90, 180), width=3)
    d.rectangle([12, 12, 430, 44], fill=(0, 90, 180))
    title = cn_title or f"V6 WIN-A {kind}"
    d.text((20, 16), title[:28], fill=(255, 255, 255), font=f_title)
    y = 54
    for ln in lines:
        d.text((22, y), ln[:40], fill=(0, 0, 0), font=f_en if ln.isascii() else f)
        y += 22

    # WIN-B noise (right upper)
    d.rectangle([450, 12, 880, 250], outline=(120, 120, 120), width=2)
    d.rectangle([450, 12, 880, 40], fill=(90, 90, 90))
    d.text((458, 16), "WIN-B DRAFT / IGNORE", fill=(255, 255, 200), font=f_sm)
    noise = [
        "old total 999.00",
        "status=void  invoice#OLD",
        "CN: 草稿勿用 / EN: void",
        f"marker V6-{i:02d}",
        "badge alerts: 3 unread",
        "overlap label TOTAL 888",
    ]
    y = 50
    for ln in noise:
        d.text((458, y), ln, fill=(70, 70, 70), font=f_sm)
        y += 18

    # WIN-C chrome (right lower) — overlapping fake window
    d.rectangle([470, 270, 890, 500], outline=(60, 60, 140), width=2)
    d.rectangle([470, 270, 890, 298], fill=(60, 60, 140))
    d.text((478, 274), "WIN-C chat / unrelated UI", fill=(255, 255, 255), font=f_sm)
    chrome = ["hey can you check?", "re: lunch", "FYI total was 42 (wrong)", "emoji 🙂", "关闭窗口"]
    y = 310
    for ln in chrome:
        d.text((478, y), ln, fill=(40, 40, 80), font=f_sm)
        y += 18

    # overlapping badge on WIN-A
    d.ellipse([400, 8, 428, 36], fill=(220, 30, 30))
    d.text((408, 12), "!", fill=(255, 255, 255), font=f_sm)

    name = f"v6_{i:02d}_{kind}.png"
    path = FIX / name
    img.save(path)
    return {
        "id": f"v6_{i:02d}",
        "file": name,
        "kind": kind,
        "metric": metric,
        "expected": expected,
        "lines": lines,
        "cn_title": cn_title,
        "capture_blend": capture,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
    }


def build_batch():
    specs = [
        ("invoice_mix", ["INVOICE #V6-01", "item A paid 15.00", "item B open 6.00", "item C paid 10.50", "TOTAL PAID TARGET 25.50"], "paid_total", 25.50, "发票 Invoice V6"),
        ("warehouse_cn", ["WH PICK V6", "BOLT qty 25 ok", "NUT qty 15 hold", "WASH qty 10 ok", "qty_sum TARGET 35"], "qty_sum", 35.0, "仓库拣货 Warehouse"),
        ("refund_mix", ["REFUND LOG", "R1 4.25 done", "R2 8.00 open", "R3 2.75 done", "refund_done TARGET 7.00"], "refund_done", 7.00, "退款 Refund"),
        ("tax_cn", ["TAX BASE", "T1 12.00 paid", "T2 9.50 open", "T3 8.00 paid", "tax_base_paid TARGET 20.00"], "tax_base_paid", 20.00, "税务底 Tax Base"),
        ("payroll", ["PAYROLL", "A 800 active", "B 150 leave", "C 700 active", "payroll_active TARGET 1500"], "payroll_active", 1500.0, "工资单 Payroll"),
        ("ship_mix", ["SHIP QTY", "P1 5 ok", "P2 7 hold", "P3 6 ok", "ship_ok_qty TARGET 11"], "ship_ok_qty", 11.0, "发货 Ship"),
        ("sla_cn", ["SLA OPEN", "S1 pri 4 open", "S2 pri 9 closed", "S3 pri 3 open", "open_pri_sum TARGET 7"], "open_pri_sum", 7.0, "服务单 SLA"),
        ("expense", ["EXPENSE", "E1 30.00 paid", "E2 12.00 void", "E3 25.50 paid", "paid_total TARGET 55.50"], "paid_total", 55.50, "报销 Expense"),
        ("po_mix", ["PO-88", "line1 paid 7.00", "line2 paid 13.00", "line3 open 4.00", "TOTAL PAID TARGET 20.00"], "paid_total", 20.00, "采购单 PO"),
        ("order_cn", ["订单 OFFICE", "A paid 11.00", "B paid 9.50", "C open 2.00", "TOTAL PAID TARGET 20.50"], "paid_total", 20.50, "订单 Order 中英"),
        ("dup_noise", ["INVOICE #V6-DUP", "paid 5.00", "paid 6.00", "paid 7.00", "TOTAL PAID TARGET 18.00"], "paid_total", 18.00, "重复噪声 Dup"),
        ("edge_zero", ["OPEN ONLY", "X 15.00 open", "Y 22.00 open", "paid_total TARGET 0.00"], "paid_total", 0.0, "仅未付 Open Only"),
        ("multi_win", ["WIN-A LEDGER", "row1 paid 3.25", "row2 paid 6.75", "row3 open 1.00", "TOTAL PAID TARGET 10.00"], "paid_total", 10.00, "多窗口 Multi-Win"),
        ("ui_noise", ["UI SHEET", "alpha paid 2.00", "beta paid 8.00", "gamma open 9.00", "TOTAL PAID TARGET 10.00"], "paid_total", 10.00, "界面噪声 UI Noise"),
    ]
    items = []
    for i, (kind, lines, metric, expected, cn_title) in enumerate(specs, 1):
        items.append(make_fixture(i, kind, lines, metric, expected, cn_title=cn_title))
    man = {
        "version": "v6",
        "n": len(items),
        "gate": GATE,
        "theme": "noisy_ui_multi_window_cn_en",
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
        "cycle": "C131",
        "theme": "v6_design_noisy_ui_multiwindow_cn_en",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "fixtures_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "n_fixtures": man["n"],
        "manifest": str((FIX / "manifest.json").relative_to(ROOT)).replace("\\", "/"),
        "pass": man["n"] >= 12 and PROTO.is_file(),
        "claim": False,
        "vl_gate_v6_claim": False,
        "note": "V6 protocol+fixtures landed. Claim deferred to C132 smoke with real VL.",
    }
    J(DOC / "C131_V6_DESIGN_BATCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C131",
        "n_fixtures": man["n"],
        "pass": out["pass"],
        "claim": False,
    }, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
