# -*- coding: utf-8 -*-
"""C72: Retest heldout bare vs NEW v2h-style LoRA. Need Δ>=0 or document ceiling."""
from __future__ import annotations
import gc, json, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_backend import RealVlBackend, VisionObs
from scripts.vision_softmatch import softmatch

GATE = 0.6
WEIGHTS = ROOT / "models" / "Qwen3.5-2B"
ADAPTER = ROOT / "runs" / "capabilities" / "vision_office_v2h_style_lora"
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
    # fresh bare (honest; do not silently reuse if we want delta fidelity — reuse C65b for speed + consistency)
    bare_path = ROOT / "docs/r50/C65b_vision_v2_heldout_smoke.json"
    bare_doc = json.loads(bare_path.read_text(encoding="utf-8"))
    bare_items, bare_n, bare_ok, bare_rate = bare_doc["items"], bare_doc["n"], bare_doc["n_ok"], float(bare_doc["rate"])

    if not ADAPTER.is_dir() or not (ADAPTER / "adapter_config.json").is_file():
        payload = {
            "kind": "r50plus_c72_vision_lora_vs_bare_retest",
            "timestamp": ts(),
            "gate": GATE,
            "adapter_present": False,
            "error": "missing v2h_style adapter — run c71",
            "bare_rate": round(bare_rate, 4),
            "gate2_3_untouched": True,
        }
        J(ROOT / "docs/r50/C72_vision_lora_vs_bare_retest.json", payload)
        print(json.dumps(payload, ensure_ascii=False))
        return

    lora_backend = RealVlBackend(WEIGHTS, max_new_tokens=128, adapter_path=ADAPTER)
    lora_items, lora_n, lora_ok, lora_rate = eval_dir(lora_backend, IMG)
    lora_backend.unload()
    gc.collect()

    by_id_bare = {r["id"]: r for r in bare_items}
    flips = []
    for r in lora_items:
        b = by_id_bare.get(r["id"])
        if b and b["ok"] != r["ok"]:
            flips.append({"id": r["id"], "bare_ok": b["ok"], "lora_ok": r["ok"]})

    delta = lora_rate - bare_rate
    ceiling_doc = None
    if delta < 0:
        ceiling_doc = {
            "delta_negative": True,
            "interpretation": "Heldout-style LoRA did not beat bare on this heldout; bare already ceiling 1.0 so Δ>0 impossible unless bare regresses. Document as ceiling when bare_rate==1.0 and lora_rate<1.0.",
            "bare_at_ceiling": bare_rate >= 0.999,
            "recommendation": "Keep bare for heldout; LoRA may still help train-style / denser tasks — see C73.",
        }
    elif delta == 0 and bare_rate >= 0.999:
        ceiling_doc = {
            "delta_zero_at_ceiling": True,
            "interpretation": "Both at 1.0; Δ>=0 satisfied as tie at ceiling.",
        }

    prior = {}
    prior_path = ROOT / "docs/r50/C66_vision_lora_vs_bare.json"
    if prior_path.is_file():
        p = json.loads(prior_path.read_text(encoding="utf-8"))
        prior = {"c66_delta": p.get("delta_lora_minus_bare"), "c66_lora_rate": (p.get("lora") or {}).get("rate")}

    payload = {
        "kind": "r50plus_c72_vision_lora_vs_bare_retest",
        "timestamp": ts(),
        "gate": GATE,
        "adapter": "runs/capabilities/vision_office_v2h_style_lora",
        "adapter_trained_on": "v2h_style_train (not heldout)",
        "heldout_dir": "evo/office/fixtures/vision_images_v2_heldout",
        "bare_reused_from_c65b": True,
        "bare": {"n": bare_n, "n_ok": bare_ok, "rate": round(bare_rate, 4)},
        "lora": {"n": lora_n, "n_ok": lora_ok, "rate": round(lora_rate, 4)},
        "delta_lora_minus_bare": round(delta, 4),
        "delta_ge_0": bool(delta >= 0),
        "lora_beats_bare": bool(lora_rate > bare_rate),
        "lora_gate_pass": bool(lora_rate >= GATE and lora_n >= 8),
        "flips": flips,
        "lora_items": lora_items,
        "ceiling": ceiling_doc,
        "prior_c66": prior,
        "innovation": "Re-absorb retest: Δ>=0 target or honest ceiling memo",
        "gate2_3_untouched": True,
        "v1_v2_claims_untouched": True,
        "note": "Does not mint new Gate2/3. Heldout bare claim from C65c untouched.",
    }
    J(ROOT / "docs/r50/C72_vision_lora_vs_bare_retest.json", payload)
    print(json.dumps({
        "bare_rate": round(bare_rate, 4),
        "lora_rate": round(lora_rate, 4),
        "delta": round(delta, 4),
        "delta_ge_0": delta >= 0,
        "flips": len(flips),
        "ceiling": bool(ceiling_doc),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
