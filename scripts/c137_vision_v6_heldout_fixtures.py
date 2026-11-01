# -*- coding: utf-8 -*-
"""C137: Vision V6 HELDOUT fixtures — disjoint IDs/files/amounts vs train V6.
Smoke deferred to C138. Gate 0.6. No Gate2/3. gen11 HOLD.
"""
from __future__ import annotations
import hashlib, json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs/r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v6_heldout"
PRIOR = ROOT / "evo/office/fixtures/vision_images_v6"
RUN = ROOT / "runs/vision_v6_heldout_c137"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def file_hash(p: Path) -> str:
    if not p.is_file():
        return ""
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def make_fixture(i, kind, lines, metric, expected, cn_title=None):
    from PIL import Image, ImageDraw, ImageFont, ImageGrab
    FIX.mkdir(parents=True, exist_ok=True)
    try:
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        ox, oy = min(160, max(0, w - 1100)), min(100, max(0, h - 720))
        bg = shot.crop((ox, oy, min(1100 + ox, w), min(720 + oy, h))).convert("RGB").resize((900, 560))
        img = Image.blend(bg, Image.new("RGB", (900, 560), (250, 248, 255)), 0.45)
        capture = True
    except Exception:
        img = Image.new("RGB", (900, 560), (245, 242, 250))
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

    # fake taskbar (same chrome language as V6, different badge)
    d.rectangle([0, 530, 900, 560], fill=(28, 28, 38))
    d.text((8, 536), "Start | Mail | Sheets | Chat  [2]", fill=(220, 220, 220), font=f_sm)
    d.ellipse([860, 536, 888, 554], fill=(40, 140, 200))
    d.text((866, 538), "H", fill=(255, 255, 255), font=f_sm)

    # WIN-A gold
    d.rectangle([12, 12, 430, 500], outline=(0, 120, 90), width=3)
    d.rectangle([12, 12, 430, 44], fill=(0, 120, 90))
    title = cn_title or f"V6H WIN-A {kind}"
    d.text((20, 16), title[:28], fill=(255, 255, 255), font=f_title)
    y = 54
    for ln in lines:
        d.text((22, y), ln[:40], fill=(0, 0, 0), font=f_en if ln.isascii() else f)
        y += 22

    # WIN-B noise
    d.rectangle([450, 12, 880, 250], outline=(120, 120, 120), width=2)
    d.rectangle([450, 12, 880, 40], fill=(80, 80, 90))
    d.text((458, 16), "WIN-B HELDOUT / IGNORE", fill=(255, 255, 200), font=f_sm)
    noise = [
        "old total 777.00",
        "status=void  invoice#OLD-H",
        "CN: 草稿勿用 / EN: void",
        f"marker V6H-{i:02d}",
        "badge alerts: 2 unread",
        "overlap label TOTAL 666",
    ]
    y = 50
    for ln in noise:
        d.text((458, y), ln, fill=(70, 70, 70), font=f_sm)
        y += 18

    # WIN-C chrome
    d.rectangle([470, 270, 890, 500], outline=(90, 50, 140), width=2)
    d.rectangle([470, 270, 890, 298], fill=(90, 50, 140))
    d.text((478, 274), "WIN-C chat / unrelated UI", fill=(255, 255, 255), font=f_sm)
    chrome = ["ping?", "re: coffee", "FYI total was 33 (wrong)", "emoji 🙂", "关闭窗口"]
    y = 310
    for ln in chrome:
        d.text((478, y), ln, fill=(40, 40, 80), font=f_sm)
        y += 18

    d.ellipse([400, 8, 428, 36], fill=(30, 140, 200))
    d.text((406, 12), "H", fill=(255, 255, 255), font=f_sm)

    name = f"v6h_{i:02d}_{kind}.png"
    path = FIX / name
    img.save(path)
    return {
        "id": f"v6h_{i:02d}",
        "file": name,
        "kind": kind,
        "metric": metric,
        "expected": expected,
        "lines": lines,
        "cn_title": cn_title,
        "capture_blend": capture,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha16": file_hash(path),
    }


def build_batch():
    # Distinct from V6 train: new IDs, amounts, titles, kinds where possible
    specs = [
        ("retail_mix", ["INVOICE #V6H-01", "item A paid 9.25", "item B open 5.00", "item C paid 12.75", "TOTAL PAID TARGET 22.00"], "paid_total", 22.00, "零售 Invoice V6H"),
        ("lab_cn", ["LAB PICK V6H", "VIAL qty 12 ok", "KIT qty 8 hold", "PAD qty 9 ok", "qty_sum TARGET 29"], "qty_sum", 29.0, "实验室拣货 Lab"),
        ("refund_h", ["REFUND LOG H", "R1 3.50 done", "R2 9.00 open", "R3 5.50 done", "refund_done TARGET 9.00"], "refund_done", 9.00, "退款 Refund H"),
        ("vat_cn", ["VAT BASE H", "V1 7.00 paid", "V2 11.00 open", "V3 9.25 paid", "tax_base_paid TARGET 16.25"], "tax_base_paid", 16.25, "增值税 Tax H"),
        ("payroll_h", ["PAYROLL H", "A 650 active", "B 200 leave", "C 550 active", "payroll_active TARGET 1200"], "payroll_active", 1200.0, "工资单 Payroll H"),
        ("ship_h", ["SHIP QTY H", "P1 4 ok", "P2 9 hold", "P3 8 ok", "ship_ok_qty TARGET 12"], "ship_ok_qty", 12.0, "发货 Ship H"),
        ("sla_h", ["SLA OPEN H", "S1 pri 2 open", "S2 pri 8 closed", "S3 pri 6 open", "open_pri_sum TARGET 8"], "open_pri_sum", 8.0, "服务单 SLA H"),
        ("expense_h", ["EXPENSE H", "E1 22.00 paid", "E2 15.00 void", "E3 18.75 paid", "paid_total TARGET 40.75"], "paid_total", 40.75, "报销 Expense H"),
        ("po_h", ["PO-H77", "line1 paid 6.50", "line2 paid 11.50", "line3 open 3.00", "TOTAL PAID TARGET 18.00"], "paid_total", 18.00, "采购单 PO H"),
        ("order_h", ["订单 OFFICE H", "A paid 8.25", "B paid 10.75", "C open 1.50", "TOTAL PAID TARGET 19.00"], "paid_total", 19.00, "订单 Order H"),
        ("dup_h", ["INVOICE #V6H-DUP", "paid 2.25", "paid 4.75", "paid 9.00", "TOTAL PAID TARGET 16.00"], "paid_total", 16.00, "重复噪声 Dup H"),
        ("edge_zero_h", ["OPEN ONLY H", "X 18.00 open", "Y 27.00 open", "paid_total TARGET 0.00"], "paid_total", 0.0, "仅未付 Open Only H"),
        ("multi_h", ["WIN-A LEDGER H", "row1 paid 4.50", "row2 paid 5.50", "row3 open 2.00", "TOTAL PAID TARGET 10.00"], "paid_total", 10.00, "多窗口 Multi H"),
        ("ui_h", ["UI SHEET H", "alpha paid 3.25", "beta paid 7.75", "gamma open 6.00", "TOTAL PAID TARGET 11.00"], "paid_total", 11.00, "界面噪声 UI H"),
    ]
    items = []
    for i, (kind, lines, metric, expected, cn_title) in enumerate(specs, 1):
        items.append(make_fixture(i, kind, lines, metric, expected, cn_title=cn_title))
    man = {
        "version": "v6_heldout",
        "n": len(items),
        "gate": GATE,
        "theme": "noisy_ui_multi_window_cn_en_heldout",
        "items": items,
        "timestamp": ts(),
        "prior_train": str(PRIOR.relative_to(ROOT)).replace("\\", "/") if PRIOR.is_dir() else None,
    }
    J(FIX / "manifest.json", man)
    return man


def overlap_check(man):
    prior_path = PRIOR / "manifest.json"
    if not prior_path.is_file():
        return {"checked": False, "reason": "no_prior"}
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    train_ids = {it["id"] for it in prior.get("items", [])}
    train_files = {it.get("file") for it in prior.get("items", [])}
    train_expected = {(it.get("kind"), float(it.get("expected"))) for it in prior.get("items", [])}
    train_sha = {it.get("sha16") for it in prior.get("items", []) if it.get("sha16")}
    hold_ids = {it["id"] for it in man["items"]}
    hold_files = {it["file"] for it in man["items"]}
    hold_sha = {it.get("sha16") for it in man["items"] if it.get("sha16")}
    id_overlap = sorted(train_ids & hold_ids)
    file_overlap = sorted(x for x in (train_files & hold_files) if x)
    sha_overlap = sorted(x for x in (train_sha & hold_sha) if x)
    kind_exp_overlap = []
    for it in man["items"]:
        key = (it["kind"], float(it["expected"]))
        if key in train_expected:
            kind_exp_overlap.append({"id": it["id"], "kind": it["kind"], "expected": it["expected"]})
    return {
        "checked": True,
        "id_overlap": id_overlap,
        "file_overlap": file_overlap,
        "sha_overlap": sha_overlap,
        "kind_expected_soft_overlap": kind_exp_overlap,
        "disjoint_ids": len(id_overlap) == 0,
        "disjoint_files": len(file_overlap) == 0,
        "disjoint_sha": len(sha_overlap) == 0,
    }


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    if FIX.exists():
        shutil.rmtree(FIX)
    man = build_batch()
    ov = overlap_check(man)
    out = {
        "cycle": "C137",
        "theme": "vision_v6_heldout_fixtures_disjoint",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "n_fixtures": man["n"],
        "fixtures_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "manifest": str((FIX / "manifest.json").relative_to(ROOT)).replace("\\", "/"),
        "overlap": ov,
        "pass": (
            man["n"] >= 12
            and ov.get("disjoint_ids", False)
            and ov.get("disjoint_files", False)
            and ov.get("disjoint_sha", True)
            and len(ov.get("kind_expected_soft_overlap", [])) == 0
        ),
        "claim": False,
        "note": "Heldout fixtures only; claim deferred to C138 smoke. Soft overlap on (kind,expected) must be empty.",
    }
    J(DOC / "C137_VISION_V6_HELDOUT_FIXTURES.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C137", "n": man["n"], "pass": out["pass"],
        "id_overlap": ov.get("id_overlap"), "soft_overlap": ov.get("kind_expected_soft_overlap"),
    }, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
