# -*- coding: utf-8 -*-
"""C97: Multihop heldout stress — 2 new fixtures not in C91 train set. Honest VL rates."""
from __future__ import annotations
import json, re, shutil, sys
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_backend import RealVlBackend, VisionObs
from evo.office.vision_ocr import ocr_image
from scripts.vision_softmatch import softmatch

GATE = 0.6
WEIGHTS = ROOT / "models" / "Qwen3.5-2B"
FIX = ROOT / "evo" / "office" / "fixtures" / "vision_images_multihop_heldout"
RUN = ROOT / "runs" / "e2e_multihop_heldout_c97"
DOC = ROOT / "docs" / "r50"

SPECS = [
    {
        "id": "mh_h_po_recv",
        "task": "ocr",
        "title": "PO RECEIVING",
        "lines": ["PO 9001", "recv qty 25", "recv qty 15", "SUM RECV 40", "status OK"],
        "gold": "PO 9001 recv 25 recv 15 SUM 40 status OK",
        "expect_sum": 40,
    },
    {
        "id": "mh_h_expense",
        "task": "ocr",
        "title": "EXPENSE",
        "lines": ["travel 120.00", "meals 45.50", "blocked 999", "APPROVED TOTAL 165.50"],
        "gold": "travel 120.00 meals 45.50 APPROVED TOTAL 165.50",
        "expect_total": 165.50,
    },
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean(text: str) -> str:
    text = re.sub(r"<think>[\s\S]*?</think>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def font(sz=20):
    for name in (r"C:\Windows\Fonts\arial.ttf",):
        try:
            return ImageFont.truetype(name, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def draw(spec):
    FIX.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (640, 360), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f = font(22)
    d.rectangle([6, 6, 634, 354], outline=(0, 0, 0), width=2)
    d.text((20, 16), spec["title"], fill=(0, 0, 0), font=f)
    y = 60
    for line in spec["lines"]:
        d.text((20, y), line, fill=(0, 0, 0), font=f)
        y += 40
    png = FIX / f"{spec['id']}.png"
    img.save(png)
    J(FIX / f"{spec['id']}.json", {**spec, "drawn_for_vl": True, "heldout_c97": True, "timestamp": ts()})
    return png


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    for s in SPECS:
        draw(s)
    backend = RealVlBackend(WEIGHTS, max_new_tokens=96)
    rows = []
    n_ok = 0
    for spec in SPECS:
        png = FIX / f"{spec['id']}.png"
        ocr = ocr_image(png, prefer="vl", vl_backend=backend)
        text = clean(ocr.get("text") or "")
        if not text:
            text = clean(backend.predict(VisionObs(image_path=png, task="ocr", gold=spec["gold"])).text or "")
        ocr_ok = softmatch(text, spec["gold"], "ocr")
        if not ocr_ok:
            keys = re.findall(r"\d+\.\d+|\d+", spec["gold"])
            ocr_ok = bool(keys) and all(k in text.replace(" ", "") for k in keys[:3])
        atom_ok = False
        if "expect_sum" in spec:
            m = re.search(r"sum\s*(?:recv)?\s*(\d+)", text.lower())
            got = int(m.group(1)) if m else sum(int(x) for x in re.findall(r"recv\s*qty\s*(\d+)", text.lower()))
            atom_ok = got == spec["expect_sum"]
            (RUN / f"{spec['id']}.csv").write_text(f"metric,value\nsum,{got}\n", encoding="utf-8")
        if "expect_total" in spec:
            m = re.search(r"(?:approved\s*)?total\s*(\d+\.\d+|\d+)", text.lower())
            got = float(m.group(1)) if m else 0.0
            atom_ok = abs(got - float(spec["expect_total"])) < 0.05
            (RUN / f"{spec['id']}.csv").write_text(f"metric,value\ntotal,{got:.2f}\n", encoding="utf-8")
        ok = ocr_ok and atom_ok
        n_ok += int(ok)
        rows.append({"id": spec["id"], "ocr_ok": ocr_ok, "atom_ok": atom_ok, "ok": ok, "text": text[:200]})
    rate = n_ok / len(SPECS)
    out = {
        "cycle": "C97",
        "theme": "multihop_heldout",
        "n": len(SPECS),
        "rate": round(rate, 4),
        "gate": GATE,
        "pass": rate >= GATE,
        "rows": rows,
        "timestamp": ts(),
        "claim": False,
        "note": "Heldout multihop observational; not Vision V4 claim.",
    }
    J(DOC / "C97_MULTIHOP_HELDOUT.json", out)
    print(json.dumps({k: out[k] for k in ("cycle", "rate", "pass")}, ensure_ascii=True))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
