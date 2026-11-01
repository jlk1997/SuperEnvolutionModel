# -*- coding: utf-8 -*-
"""C125: Vision V5 HELDOUT fixtures — new IDs/numbers vs train V5. No smoke here."""
from __future__ import annotations
import json, hashlib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "evo/office/fixtures/vision_images_v5_heldout"
PRIOR = ROOT / "evo/office/fixtures/vision_images_v5"
DOC = ROOT / "docs/r50"
GATE = 0.6


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def file_hash(p: Path) -> str:
    if not p.is_file():
        return ""
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def make_fixture(i, kind, lines, metric, expected, clutter=True):
    from PIL import Image, ImageDraw, ImageFont, ImageGrab
    FIX.mkdir(parents=True, exist_ok=True)
    try:
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        # offset crop so heldout wallpaper != train crop when possible
        ox, oy = min(120, max(0, w - 1000)), min(80, max(0, h - 700))
        bg = shot.crop((ox, oy, min(1000 + ox, w), min(700 + oy, h))).convert("RGB").resize((800, 520))
        img = Image.blend(bg, Image.new("RGB", (800, 520), (248, 248, 252)), 0.52 if clutter else 0.75)
        capture = True
    except Exception:
        img = Image.new("RGB", (800, 520), (240, 240, 245))
        capture = False
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 18)
        f = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 14)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 12)
    except Exception:
        f_title = f = f_sm = ImageFont.load_default()
    d.rectangle([10, 10, 390, 500], outline=(0, 0, 0), width=2)
    d.rectangle([410, 10, 790, 500], outline=(80, 80, 80), width=1)
    d.rectangle([18, 18, 382, 52], fill=(180, 255, 200), outline=(0, 0, 0))
    d.text((24, 24), f"V5H ZONE-A {kind}", fill=(0, 0, 0), font=f_title)
    y = 60
    for ln in lines:
        d.text((24, y), ln[:42], fill=(0, 0, 0), font=f)
        y += 20
    d.text((420, 24), "ZONE-B noise / heldout", fill=(60, 60, 60), font=f_sm)
    noise = [
        "DRAFT ignore",
        "old total 888.00",
        "status=void",
        f"marker V5H-{i:02d}",
        "backup sheet",
    ]
    y = 60
    for ln in noise:
        d.text((420, y), ln, fill=(90, 90, 90), font=f_sm)
        y += 18
    name = f"v5h_{i:02d}_{kind}.png"
    path = FIX / name
    img.save(path)
    return {
        "id": f"v5h_{i:02d}",
        "file": name,
        "kind": kind,
        "metric": metric,
        "expected": expected,
        "lines": lines,
        "capture_blend": capture,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha16": file_hash(path),
    }


def build_batch():
    # Distinct from V5 train (different IDs, amounts, titles)
    specs = [
        ("retail", ["RETAIL #V5H-A1", "sku X paid 7.25", "sku Y open 3.00", "sku Z paid 11.75", "TOTAL PAID TARGET 19.00"], "paid_total", 19.00),
        ("lab", ["LAB STOCK H", "VIAL qty 8 ok", "KIT qty 14 hold", "PAD qty 6 ok", "qty_sum TARGET 28"], "qty_sum", 28.0),
        ("claim", ["TRAVEL H", "flight 210.00", "hotel 95.00", "blocked 40", "APPROVED TOTAL 305.00"], "approved_total", 305.0),
        ("vat", ["VAT H", "V1 8.00 paid", "V2 12.00 open", "V3 6.50 paid", "tax_base_paid TARGET 14.50"], "tax_base_paid", 14.50),
        ("grn", ["GRN 8801", "recv qty 5", "recv qty 9", "SUM RECV 14", "status OK"], "recv_sum", 14.0),
        ("ship", ["SHIP H", "P1 7 ok", "P2 3 hold", "P3 2 ok", "ship_ok_qty TARGET 9"], "ship_ok_qty", 9.0),
        ("sla", ["SLA H", "S1 pri 4 open", "S2 pri 1 closed", "S3 pri 5 open", "open_pri_sum TARGET 9"], "open_pri_sum", 9.0),
        ("expense", ["EXP H", "E1 13.00 paid", "E2 4.00 void", "E3 17.50 paid", "paid_total TARGET 30.50"], "paid_total", 30.50),
        ("po", ["PO-H91", "line1 paid 4.50", "line2 paid 10.50", "line3 open 8.00", "TOTAL PAID TARGET 15.00"], "paid_total", 15.00),
        ("mixed", ["MIX OFFICE H", "A paid 5.25", "B paid 8.75", "C open 2.00", "TOTAL PAID TARGET 14.00"], "paid_total", 14.00),
        ("dup", ["INVOICE #V5H-DUP", "paid 1.50", "paid 2.50", "paid 6.00", "TOTAL PAID TARGET 10.00"], "paid_total", 10.00),
        ("edge_zero", ["OPEN ONLY H", "X 4.00 open", "Y 6.00 open", "paid_total TARGET 0.00"], "paid_total", 0.0),
    ]
    items = []
    for i, (kind, lines, metric, expected) in enumerate(specs, 1):
        items.append(make_fixture(i, kind, lines, metric, expected, clutter=True))
    man = {
        "version": "v5_heldout",
        "n": len(items),
        "gate": GATE,
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
    train_expected = {(it.get("kind"), it.get("expected")) for it in prior.get("items", [])}
    hold_ids = {it["id"] for it in man["items"]}
    hold_files = {it["file"] for it in man["items"]}
    id_overlap = sorted(train_ids & hold_ids)
    file_overlap = sorted(train_files & hold_files)
    # soft: same (kind, expected) pairs discouraged
    kind_exp_overlap = []
    for it in man["items"]:
        key = (it["kind"], it["expected"])
        if key in train_expected:
            kind_exp_overlap.append({"id": it["id"], "kind": it["kind"], "expected": it["expected"]})
    return {
        "checked": True,
        "id_overlap": id_overlap,
        "file_overlap": file_overlap,
        "kind_expected_soft_overlap": kind_exp_overlap,
        "disjoint_ids": len(id_overlap) == 0,
        "disjoint_files": len(file_overlap) == 0,
    }


def main():
    import shutil
    if FIX.exists():
        shutil.rmtree(FIX)
    man = build_batch()
    ov = overlap_check(man)
    out = {
        "cycle": "C125",
        "theme": "vision_v5_heldout_fixtures",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "n_fixtures": man["n"],
        "fixtures_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "manifest": str((FIX / "manifest.json").relative_to(ROOT)).replace("\\", "/"),
        "overlap": ov,
        "pass": man["n"] >= 10 and ov.get("disjoint_ids", False) and ov.get("disjoint_files", False),
        "claim": False,
        "note": "Heldout fixtures only; claim deferred to C126 smoke.",
    }
    J(DOC / "C125_VISION_V5_HELDOUT_FIXTURES.json", out)
    print(json.dumps({"cycle": "C125", "n": man["n"], "pass": out["pass"], "overlap_ids": ov.get("id_overlap")}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
