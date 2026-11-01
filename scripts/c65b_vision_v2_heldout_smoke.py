# -*- coding: utf-8 -*-
"""C65b: Honest Vision V2 heldout smoke on bare Qwen3.5-2B. Claim only rate>=0.6 & n>=8."""
from __future__ import annotations
import json, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_backend import RealVlBackend, VisionObs
from scripts.vision_softmatch import softmatch

GATE = 0.6
WEIGHTS = ROOT / "models" / "Qwen3.5-2B"
IMG = ROOT / "evo/office/fixtures/vision_images_v2_heldout"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean(text: str) -> str:
    text = re.sub(r"<think>[\s\S]*?</think>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def eval_dir(backend, img_dir: Path):
    ids = sorted(p.stem for p in img_dir.glob("*.png"))
    items = []
    n_ok = 0
    for fid in ids:
        meta = json.loads((img_dir / f"{fid}.json").read_text(encoding="utf-8"))
        task = meta.get("task") or "caption"
        gold = str(meta.get("gold") or "")
        try:
            pred = backend.predict(VisionObs(image_path=img_dir / f"{fid}.png", task=task, gold=gold))
            text = clean(pred.text or "")
            ok = softmatch(text, gold, task)
            err = None
        except Exception as e:
            text, ok, err = "", False, f"{type(e).__name__}: {e}"
        n_ok += int(ok)
        items.append({"id": fid, "task": task, "gold": gold, "pred_head": text[:240], "ok": ok, "error": err})
    n = len(items)
    rate = n_ok / n if n else 0.0
    return items, n, n_ok, rate


def main():
    backend = RealVlBackend(WEIGHTS, max_new_tokens=128)
    items, n, n_ok, rate = eval_dir(backend, IMG)
    claim = bool(rate >= GATE and n >= 8)
    payload = {
        "kind": "r50plus_c65_vision_v2_heldout_smoke",
        "timestamp": ts(),
        "gate": GATE,
        "n": n,
        "n_ok": n_ok,
        "rate": round(rate, 4),
        "gate_pass": claim,
        "vl_gate_v2_heldout_claim": claim,
        "claim_scope": (
            "r50plus_v2_heldout_harder_readable_office_drawn_n>=8_softmatch_qwen35_2b_bare"
            if claim
            else None
        ),
        "items": items,
        "weights": "models/Qwen3.5-2B",
        "adapter": None,
        "mode": "bare",
        "v1_v2_claims_untouched": True,
        "gate2_3_untouched": True,
        "open_domain_benchmark": False,
        "innovation": "Honest heldout V2 retest; claim only if >=0.6",
    }
    J(ROOT / "docs/r50/C65b_vision_v2_heldout_smoke.json", payload)
    if claim:
        J(
            ROOT / "docs/r50/C65c_vision_gate_v2_heldout_claim.json",
            {
                "kind": "vision_gate_v2_heldout_claim",
                "timestamp": ts(),
                "vl_gate_v2_heldout_claim": True,
                "rate": round(rate, 4),
                "n": n,
                "n_ok": n_ok,
                "gate": GATE,
                "claim_scope": payload["claim_scope"],
                "gate2_3_untouched": True,
                "v1_v2_untouched": True,
            },
        )
    backend.unload()
    print(json.dumps({"rate": round(rate, 4), "n": n, "n_ok": n_ok, "claim": claim}, ensure_ascii=False))


if __name__ == "__main__":
    main()
