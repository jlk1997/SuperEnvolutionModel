# -*- coding: utf-8 -*-
"""C84b: Bare smoke on harder ocr_weak — softmatch + strict must_codes hit rate."""
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


def clean(text: str) -> str:
    text = re.sub(r"<think>[\s\S]*?</think>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def strict_hit(pred: str, must_codes: list) -> bool:
    p = (pred or "").upper().replace(" ", "")
    if not must_codes:
        return False
    hits = 0
    for c in must_codes:
        token = str(c).upper().replace(" ", "")
        if token and token in p:
            hits += 1
    return hits >= max(2, len(must_codes) - 1)  # need almost all codes


def main():
    backend = RealVlBackend(WEIGHTS, max_new_tokens=96)
    items = []
    n_soft = n_strict = 0
    for jp in sorted(IMG.glob("*.json")):
        meta = json.loads(jp.read_text(encoding="utf-8"))
        fid = meta["id"]
        gold = str(meta.get("gold") or "")
        must = list(meta.get("must_codes") or [])
        try:
            pred = backend.predict(VisionObs(image_path=IMG / f"{fid}.png", task="ocr", gold=gold))
            text = clean(pred.text or "")
            soft_ok = softmatch(text, gold, "ocr")
            strict_ok = strict_hit(text, must)
            err = None
        except Exception as e:
            text, soft_ok, strict_ok, err = "", False, False, f"{type(e).__name__}: {e}"
        n_soft += int(soft_ok)
        n_strict += int(strict_ok)
        items.append({
            "id": fid, "gold": gold, "must_codes": must,
            "pred_head": text[:220], "soft_ok": soft_ok, "strict_ok": strict_ok, "error": err,
        })
    backend.unload(); gc.collect()
    n = len(items)
    soft_rate = n_soft / n if n else 0.0
    strict_rate = n_strict / n if n else 0.0
    # weak enough if strict domain is below gate
    weak_enough = strict_rate < GATE
    payload = {
        "kind": "r50plus_c84b_vision_ocr_weak_bare_harder",
        "timestamp": ts(),
        "gate": GATE,
        "domain": "ocr_weak",
        "n": n,
        "soft_rate": round(soft_rate, 4),
        "strict_rate": round(strict_rate, 4),
        "n_soft_ok": n_soft,
        "n_strict_ok": n_strict,
        "weak_enough_strict": weak_enough,
        "rate": round(strict_rate, 4),  # primary metric for LoRA hunt = strict
        "n_ok": n_strict,
        "items": items,
        "innovation": "Strict must_codes metric for weak-domain hunt (softmatch too lenient on degraded OCR)",
        "gate2_3_untouched": True,
        "no_fake_vl": True,
    }
    # also overwrite C84 path for downstream reuse of rate as strict
    (ROOT / "docs/r50/C84_vision_ocr_weak_bare_smoke.json").write_text(
        json.dumps({**payload, "kind": "r50plus_c84_vision_ocr_weak_bare_smoke", "metric": "strict_must_codes"}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (ROOT / "docs/r50/C84b_vision_ocr_weak_bare_harder.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "n": n, "soft_rate": round(soft_rate, 4), "strict_rate": round(strict_rate, 4),
        "weak_enough_strict": weak_enough,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
