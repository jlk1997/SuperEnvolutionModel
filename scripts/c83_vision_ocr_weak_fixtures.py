# -*- coding: utf-8 -*-
"""C83: Weak OCR domain fixtures — train + disjoint test.
Hard for bare VL: small font, low contrast, clutter. domain=ocr_weak.
"""
from __future__ import annotations
import hashlib, json
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
TRAIN = ROOT / "evo/office/fixtures/vision_images_ocr_weak_train"
TEST = ROOT / "evo/office/fixtures/vision_images_ocr_weak_test"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def font(size, bold=False):
    p = Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf")
    if not p.is_file():
        p = Path(r"C:\Windows\Fonts\consola.ttf")
    return ImageFont.truetype(str(p), size=size)


def save(out: Path, img, name, meta):
    out.mkdir(parents=True, exist_ok=True)
    png = out / f"{name}.png"
    img.save(png, format="PNG")
    digest = hashlib.sha256(png.read_bytes()).hexdigest()
    meta = {
        **meta,
        "id": name,
        "sha256": digest,
        "domain": "ocr_weak",
        "task": "ocr",
        "drawn_for_vl": True,
        "synthetic_not_vl": False,
        "weak_domain": True,
        "source": "c83_vision_ocr_weak_fixtures",
        "timestamp": ts(),
        "gold": meta.get("gold") or "",
    }
    (out / f"{name}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"id": name, "png_bytes": png.stat().st_size, "gold": meta["gold"], "split": meta.get("split")}


def make_receipt(code: str, total: str, date: str, clutter: bool = True) -> Image.Image:
    # low-contrast gray-on-gray + tiny font + distractors
    img = Image.new("RGB", (520, 360), (198, 198, 198))
    d = ImageDraw.Draw(img)
    if clutter:
        for i in range(0, 520, 40):
            d.line([(i, 0), (i, 360)], fill=(190, 190, 190), width=1)
        d.text((12, 8), "INTERNAL DRAFT DO NOT FILE COPY COPY COPY", fill=(175, 175, 175), font=font(11))
        d.text((12, 330), "watermark watermark watermark", fill=(180, 180, 180), font=font(10))
    d.text((18, 40), f"RCPT {code}", fill=(120, 120, 120), font=font(13, bold=True))
    d.text((18, 70), f"AMT {total}", fill=(115, 115, 115), font=font(12))
    d.text((18, 95), f"DATE {date}", fill=(115, 115, 115), font=font(12))
    d.text((18, 130), "SKU MIX NOISE AAA BBB CCC", fill=(170, 170, 170), font=font(11))
    d.text((18, 155), "ref noise 999 junk line", fill=(170, 170, 170), font=font(11))
    # slight blur to hurt bare OCR
    img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    return img


def main():
    train_specs = [
        ("owt-rcpt-001", "RX-1001", "12.50", "2026-09-01"),
        ("owt-rcpt-002", "RX-1002", "88.00", "2026-09-02"),
        ("owt-rcpt-003", "RX-1003", "3.25", "2026-09-03"),
        ("owt-rcpt-004", "RX-1004", "41.10", "2026-09-04"),
        ("owt-rcpt-005", "RX-1005", "19.99", "2026-09-05"),
        ("owt-rcpt-006", "RX-1006", "250.00", "2026-09-06"),
        ("owt-rcpt-007", "RX-1007", "7.77", "2026-09-07"),
        ("owt-rcpt-008", "RX-1008", "63.40", "2026-09-08"),
    ]
    test_specs = [
        ("owx-rcpt-001", "RX-9001", "15.20", "2026-10-01"),
        ("owx-rcpt-002", "RX-9002", "99.00", "2026-10-02"),
        ("owx-rcpt-003", "RX-9003", "4.50", "2026-10-03"),
        ("owx-rcpt-004", "RX-9004", "33.33", "2026-10-04"),
        ("owx-rcpt-005", "RX-9005", "210.00", "2026-10-05"),
        ("owx-rcpt-006", "RX-9006", "8.08", "2026-10-06"),
        ("owx-rcpt-007", "RX-9007", "56.70", "2026-10-07"),
        ("owx-rcpt-008", "RX-9008", "1.01", "2026-10-08"),
    ]
    # wipe / recreate
    for d in (TRAIN, TEST):
        if d.exists():
            import shutil
            shutil.rmtree(d)
    train_made, test_made = [], []
    for name, code, total, date in train_specs:
        gold = f"RCPT {code} AMT {total} DATE {date}"
        train_made.append(save(TRAIN, make_receipt(code, total, date), name, {"gold": gold, "split": "train"}))
    for name, code, total, date in test_specs:
        gold = f"RCPT {code} AMT {total} DATE {date}"
        test_made.append(save(TEST, make_receipt(code, total, date), name, {"gold": gold, "split": "test"}))
    # disjoint check
    train_ids = {x["id"] for x in train_made}
    test_ids = {x["id"] for x in test_made}
    train_golds = {x["gold"] for x in train_made}
    test_golds = {x["gold"] for x in test_made}
    payload = {
        "kind": "r50plus_c83_vision_ocr_weak_fixtures",
        "timestamp": ts(),
        "gate": GATE,
        "domain": "ocr_weak",
        "n_train": len(train_made),
        "n_test": len(test_made),
        "train_dir": "evo/office/fixtures/vision_images_ocr_weak_train",
        "test_dir": "evo/office/fixtures/vision_images_ocr_weak_test",
        "disjoint_ids": train_ids.isdisjoint(test_ids),
        "disjoint_golds": train_golds.isdisjoint(test_golds),
        "train": train_made,
        "test": test_made,
        "design": "small font + low contrast + blur + clutter; gold short RCPT/AMT/DATE",
        "innovation": "Weak vision domain to hunt LoRA Δ≥0 (dense already known-harm)",
        "gate2_3_untouched": True,
    }
    out = ROOT / "docs/r50/C83_vision_ocr_weak_fixtures.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "n_train": len(train_made),
        "n_test": len(test_made),
        "disjoint_ids": payload["disjoint_ids"],
        "disjoint_golds": payload["disjoint_golds"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
