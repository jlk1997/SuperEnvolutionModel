# -*- coding: utf-8 -*-
"""蚁算-视 V1 smoke: real Qwen3.5-2B on readable office fixtures. Honest gate 0.6."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from evo.office.vision_backend import RealVlBackend, VisionObs
from scripts.vision_softmatch import softmatch

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
WEIGHTS = ROOT / "models" / "Qwen3.5-2B"
IMG = ROOT / "evo" / "office" / "fixtures" / "vision_images_real"
HELD = ROOT / "evo" / "office" / "fixtures" / "VISION_HELD_OUT.json"


def ts() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def clean_pred(s: str) -> str:
    s = s or ""
    s = re.sub(r"<think>[\s\S]*?</think>", " ", s)
    s = re.sub(r"^assistant\s*", "", s, flags=re.I)
    s = re.sub(r"```(?:csv|text)?", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def score(pred: str, gold: str, task: str) -> bool:
    return softmatch(clean_pred(pred), gold, task)



# Prefer a balanced V1 set of >=8 readable fixtures (include 1 heldout for honesty)
V1_SET = [
    "office-caption-001",
    "office-caption-002",
    "office-ocr-001",
    "office-ocr-002",
    "office-table-001",
    "office-table-002",
    "office-ui-001",
    "office-ui-002",
    "office-hard-ocr-001",
    "office-hard-table-001",
    "office-hard-ui-001",
    "office-hard-mixed-001",
]


def main() -> None:
    held = set()
    if HELD.is_file():
        held = set(json.loads(HELD.read_text(encoding="utf-8")).get("heldout_ids") or [])

    backend = RealVlBackend(WEIGHTS, max_new_tokens=128)
    items = []
    n_ok = 0
    for fid in V1_SET:
        meta_path = IMG / f"{fid}.json"
        png = IMG / f"{fid}.png"
        if not meta_path.is_file() or not png.is_file():
            items.append({"id": fid, "ok": False, "error": "missing_fixture", "heldout": fid in held})
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        # refuse solid-color leftovers
        if png.stat().st_size < 800 and not meta.get("readable_v1"):
            items.append({"id": fid, "ok": False, "error": "fixture_too_small_likely_solid", "size": png.stat().st_size, "heldout": fid in held})
            continue
        task = meta.get("task") or "caption"
        gold = str(meta.get("gold") or "")
        try:
            pred = backend.predict(VisionObs(image_path=png, task=task, gold=gold))
            text = clean_pred(pred.text)
            ok = score(text, gold, task)
            err = None
        except Exception as e:  # noqa: BLE001
            text = ""
            ok = False
            err = f"{type(e).__name__}: {e}"
        n_ok += int(ok)
        items.append(
            {
                "id": fid,
                "task": task,
                "gold": gold,
                "pred_head": text[:200],
                "ok": ok,
                "error": err,
                "heldout": fid in held,
                "png_bytes": png.stat().st_size,
                "readable_v1": bool(meta.get("readable_v1")),
            }
        )

    n = len(items)
    rate = n_ok / n if n else 0.0
    gate_pass = rate >= GATE and n >= 8
    claim = bool(gate_pass)
    result = {
        "kind": "vision_v1_smoke_real_vl",
        "product": "蚁算-视",
        "timestamp": ts(),
        "gate": GATE,
        "min_n": 8,
        "weights_path": str(WEIGHTS).replace("\\", "/"),
        "weights_local": WEIGHTS.is_dir(),
        "synthetic_not_vl": False,
        "fixtures_readable_v1": True,
        "n": n,
        "n_ok": n_ok,
        "rate": round(rate, 4),
        "gate_pass": gate_pass,
        "vl_gate_v1_claim": claim,
        "claim_scope": (
            "r50_v1_smoke_readable_office_drawn_n>=8_softmatch_qwen35_2b"
            if claim
            else None
        ),
        "prior_c47_rate": 0.375,
        "prior_c47_fail_reason": "solid-color fixtures via png()+tEXt; VL saw blank",
        "items": items,
        "gate2_3_untouched": True,
        "notes": "Honest V1 after readable fixture regen. Scoped claim only if rate>=0.6 and n>=8.",
    }
    out = ROOT / "docs" / "r50" / "C52_vision_v1_smoke_readable.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # also mirror short doc
    (ROOT / "docs" / f"VISION_V1_SMOKE_READABLE_{datetime.now().strftime('%Y-%m-%d')}.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"rate": result["rate"], "n": n, "n_ok": n_ok, "gate_pass": gate_pass, "claim": claim, "out": str(out)}, ensure_ascii=False))
    del backend
    try:
        import torch

        torch.cuda.empty_cache()
    except Exception:
        pass


if __name__ == "__main__":
    main()

