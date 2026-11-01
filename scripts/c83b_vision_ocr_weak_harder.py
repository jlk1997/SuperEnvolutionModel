# -*- coding: utf-8 -*-
"""C83b: Harder ocr_weak fixtures — extreme blur/tiny font + STRICT gold codes.
If bare still ~1.0 under softmatch, C84b also reports strict_code_hit rate.
"""
from __future__ import annotations
import hashlib, json, shutil
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
TRAIN = ROOT / "evo/office/fixtures/vision_images_ocr_weak_train"
TEST = ROOT / "evo/office/fixtures/vision_images_ocr_weak_test"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def font(size):
    for p in [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\arial.ttf"]:
        if Path(p).is_file():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


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
        "weak_domain": True,
        "harder": True,
        "source": "c83b_vision_ocr_weak_harder",
        "timestamp": ts(),
        "gold": meta.get("gold") or "",
        "must_codes": meta.get("must_codes") or [],
    }
    (out / f"{name}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"id": name, "png_bytes": png.stat().st_size, "gold": meta["gold"], "must_codes": meta["must_codes"]}


def make_hard(code: str, total: str, date: str) -> Image.Image:
    img = Image.new("RGB", (480, 300), (205, 205, 205))
    d = ImageDraw.Draw(img)
    # heavy clutter
    for i in range(0, 480, 17):
        d.line([(i, 0), (i + 40, 300)], fill=(195, 195, 195), width=1)
    d.text((8, 6), "DRAFT DRAFT DRAFT NOISE " * 3, fill=(185, 185, 185), font=font(9))
    # tiny low-contrast payload
    d.text((14, 50), f"RCPT {code}", fill=(150, 150, 150), font=font(10))
    d.text((14, 72), f"AMT {total}", fill=(148, 148, 148), font=font(10))
    d.text((14, 94), f"DATE {date}", fill=(148, 148, 148), font=font(10))
    d.text((14, 130), "AAA BBB CCC DDD EEE FFF GGG", fill=(180, 180, 180), font=font(9))
    img = img.filter(ImageFilter.GaussianBlur(radius=1.35))
    img = ImageEnhance.Contrast(img).enhance(0.55)
    img = ImageEnhance.Brightness(img).enhance(1.08)
    return img


def main():
    for d in (TRAIN, TEST):
        if d.exists():
            shutil.rmtree(d)
    train_specs = [
        ("owt-rcpt-001", "ZQ-71A9", "12.50", "2026-09-01"),
        ("owt-rcpt-002", "ZQ-71B2", "88.00", "2026-09-02"),
        ("owt-rcpt-003", "ZQ-71C3", "3.25", "2026-09-03"),
        ("owt-rcpt-004", "ZQ-71D4", "41.10", "2026-09-04"),
        ("owt-rcpt-005", "ZQ-71E5", "19.99", "2026-09-05"),
        ("owt-rcpt-006", "ZQ-71F6", "250.00", "2026-09-06"),
        ("owt-rcpt-007", "ZQ-71G7", "7.77", "2026-09-07"),
        ("owt-rcpt-008", "ZQ-71H8", "63.40", "2026-09-08"),
    ]
    test_specs = [
        ("owx-rcpt-001", "ZQ-90K1", "15.20", "2026-10-01"),
        ("owx-rcpt-002", "ZQ-90L2", "99.00", "2026-10-02"),
        ("owx-rcpt-003", "ZQ-90M3", "4.50", "2026-10-03"),
        ("owx-rcpt-004", "ZQ-90N4", "33.33", "2026-10-04"),
        ("owx-rcpt-005", "ZQ-90P5", "210.00", "2026-10-05"),
        ("owx-rcpt-006", "ZQ-90Q6", "8.08", "2026-10-06"),
        ("owx-rcpt-007", "ZQ-90R7", "56.70", "2026-10-07"),
        ("owx-rcpt-008", "ZQ-90S8", "1.01", "2026-10-08"),
    ]
    train_made, test_made = [], []
    for name, code, total, date in train_specs:
        gold = f"RCPT {code} AMT {total} DATE {date}"
        train_made.append(save(TRAIN, make_hard(code, total, date), name, {
            "gold": gold, "split": "train", "must_codes": [code, total, date],
        }))
    for name, code, total, date in test_specs:
        gold = f"RCPT {code} AMT {total} DATE {date}"
        test_made.append(save(TEST, make_hard(code, total, date), name, {
            "gold": gold, "split": "test", "must_codes": [code, total, date],
        }))
    payload = {
        "kind": "r50plus_c83b_vision_ocr_weak_harder",
        "timestamp": ts(),
        "gate": GATE,
        "domain": "ocr_weak",
        "n_train": len(train_made),
        "n_test": len(test_made),
        "disjoint_ids": True,
        "disjoint_golds": True,
        "design": "font10 + blur1.35 + contrast0.55 + clutter; must_codes for strict hit",
        "train_dir": "evo/office/fixtures/vision_images_ocr_weak_train",
        "test_dir": "evo/office/fixtures/vision_images_ocr_weak_test",
        "gate2_3_untouched": True,
    }
    out = ROOT / "docs/r50/C83b_vision_ocr_weak_harder.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"n_train": len(train_made), "n_test": len(test_made), "harder": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
