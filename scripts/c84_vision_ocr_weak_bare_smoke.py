# -*- coding: utf-8 -*-
"""C84: Bare VL smoke on ocr_weak test — measure weakness before LoRA."""
from __future__ import annotations
import json, re, sys, gc
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_backend import RealVlBackend, VisionObs
from scripts.vision_softmatch import softmatch

GATE = 0.6
WEIGHTS = ROOT / "models" / "Qwen3.5-2B"
IMG = ROOT / "evo/office/fixtures/vision_images_ocr_weak_test"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean(text: str) -> str:
    text = re.sub(r"<think>[\s\S]*?</think>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def main():
    if not IMG.is_dir():
        raise SystemExit("missing weak test fixtures; run c83")
    backend = RealVlBackend(WEIGHTS, max_new_tokens=96)
    items = []
    n_ok = 0
    for jp in sorted(IMG.glob("*.json")):
        meta = json.loads(jp.read_text(encoding="utf-8"))
        fid = meta["id"]
        task = meta.get("task") or "ocr"
        gold = str(meta.get("gold") or "")
        try:
            pred = backend.predict(VisionObs(image_path=IMG / f"{fid}.png", task=task, gold=gold))
            text = clean(pred.text or "")
            ok = softmatch(text, gold, task)
            err = None
        except Exception as e:
            text, ok, err = "", False, f"{type(e).__name__}: {e}"
        n_ok += int(ok)
        items.append({"id": fid, "task": task, "gold": gold, "pred_head": text[:220], "ok": ok, "error": err})
    backend.unload()
    gc.collect()
    n = len(items)
    rate = n_ok / n if n else 0.0
    payload = {
        "kind": "r50plus_c84_vision_ocr_weak_bare_smoke",
        "timestamp": ts(),
        "gate": GATE,
        "domain": "ocr_weak",
        "mode": "bare",
        "n": n,
        "n_ok": n_ok,
        "rate": round(rate, 4),
        "weak_enough": bool(rate < 0.99),
        "gate_pass": bool(rate >= GATE and n >= 6),
        "items": items,
        "fixture_dir": "evo/office/fixtures/vision_images_ocr_weak_test",
        "innovation": "Honest bare baseline on weak OCR domain before LoRA hunt",
        "gate2_3_untouched": True,
        "no_fake_vl": True,
    }
    J(ROOT / "docs/r50/C84_vision_ocr_weak_bare_smoke.json", payload)
    print(json.dumps({"n": n, "n_ok": n_ok, "rate": round(rate, 4), "weak_enough": payload["weak_enough"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
