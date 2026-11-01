# -*- coding: utf-8 -*-
"""C66: Retest V2 heldout with LoRA adapter loaded vs bare. Honest delta."""
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
ADAPTER = ROOT / "runs" / "capabilities" / "vision_office_v1_readable_lora"
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
        items.append({"id": fid, "task": task, "gold": gold, "pred_head": text[:200], "ok": ok, "error": err})
    n = len(items)
    rate = n_ok / n if n else 0.0
    return items, n, n_ok, rate


def main():
    # Prefer reusing bare numbers from C65b if present and same dir
    bare_path = ROOT / "docs/r50/C65b_vision_v2_heldout_smoke.json"
    if bare_path.is_file():
        bare_doc = json.loads(bare_path.read_text(encoding="utf-8"))
        bare_items, bare_n, bare_ok, bare_rate = bare_doc["items"], bare_doc["n"], bare_doc["n_ok"], float(bare_doc["rate"])
        bare_reused = True
    else:
        bare_backend = RealVlBackend(WEIGHTS, max_new_tokens=128)
        bare_items, bare_n, bare_ok, bare_rate = eval_dir(bare_backend, IMG)
        bare_backend.unload()
        bare_reused = False
        gc.collect()

    if not ADAPTER.is_dir() or not (ADAPTER / "adapter_config.json").is_file():
        payload = {
            "kind": "r50plus_c66_vision_lora_vs_bare",
            "timestamp": ts(),
            "gate": GATE,
            "adapter_present": False,
            "error": "missing adapter",
            "bare_rate": round(bare_rate, 4),
            "lora_rate": None,
            "delta": None,
            "gate2_3_untouched": True,
        }
        J(ROOT / "docs/r50/C66_vision_lora_vs_bare.json", payload)
        print(json.dumps(payload, ensure_ascii=False))
        return

    lora_backend = RealVlBackend(WEIGHTS, max_new_tokens=128, adapter_path=ADAPTER)
    lora_items, lora_n, lora_ok, lora_rate = eval_dir(lora_backend, IMG)
    lora_backend.unload()

    # pairwise
    by_id_bare = {r["id"]: r for r in bare_items}
    flips = []
    for r in lora_items:
        b = by_id_bare.get(r["id"])
        if b and b["ok"] != r["ok"]:
            flips.append({"id": r["id"], "bare_ok": b["ok"], "lora_ok": r["ok"]})

    delta = lora_rate - bare_rate
    payload = {
        "kind": "r50plus_c66_vision_lora_vs_bare",
        "timestamp": ts(),
        "gate": GATE,
        "adapter": "runs/capabilities/vision_office_v1_readable_lora",
        "adapter_trained_on": "v1_readable (not heldout)",
        "heldout_dir": "evo/office/fixtures/vision_images_v2_heldout",
        "bare_reused_from_c65b": bare_reused,
        "bare": {"n": bare_n, "n_ok": bare_ok, "rate": round(bare_rate, 4)},
        "lora": {"n": lora_n, "n_ok": lora_ok, "rate": round(lora_rate, 4)},
        "delta_lora_minus_bare": round(delta, 4),
        "lora_beats_bare": bool(lora_rate > bare_rate),
        "lora_gate_pass": bool(lora_rate >= GATE and lora_n >= 8),
        "flips": flips,
        "lora_items": lora_items,
        "innovation": "Heldout LoRA vs bare retest; adapter never trained on heldout",
        "gate2_3_untouched": True,
        "v1_v2_claims_untouched": True,
        "note": "Does not mint new Gate2/3. Heldout claim remains from C65b bare if any.",
    }
    J(ROOT / "docs/r50/C66_vision_lora_vs_bare.json", payload)
    print(
        json.dumps(
            {
                "bare_rate": round(bare_rate, 4),
                "lora_rate": round(lora_rate, 4),
                "delta": round(delta, 4),
                "flips": len(flips),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
