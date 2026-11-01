# -*- coding: utf-8 -*-
"""C73b: Smoke V3 dense OCR/tables with bare Qwen3.5-2B. Gate 0.6. Honest."""
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
IMG = ROOT / "evo/office/fixtures/vision_images_v3_dense"
# optional: also eval with style LoRA for signal (not claim unless beats)
ADAPTER = ROOT / "runs" / "capabilities" / "vision_office_v2h_style_lora"


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
    if not IMG.is_dir():
        raise SystemExit("run c73 fixtures first")
    bare = RealVlBackend(WEIGHTS, max_new_tokens=160)
    items, n, n_ok, rate = eval_dir(bare, IMG)
    bare.unload()
    gc.collect()

    lora_block = None
    if ADAPTER.is_dir() and (ADAPTER / "adapter_config.json").is_file():
        lb = RealVlBackend(WEIGHTS, max_new_tokens=160, adapter_path=ADAPTER)
        li, ln, lok, lrate = eval_dir(lb, IMG)
        lb.unload()
        gc.collect()
        lora_block = {"n": ln, "n_ok": lok, "rate": round(lrate, 4), "items": li, "delta_vs_bare": round(lrate - rate, 4)}

    claim = bool(rate >= GATE and n >= 8)
    claim_path = ROOT / "docs/r50/C73c_vision_gate_v3_claim.json"
    if claim:
        J(claim_path, {
            "kind": "vision_gate_v3_dense_claim",
            "timestamp": ts(),
            "vl_gate_v3_claim": True,
            "rate": round(rate, 4),
            "n": n,
            "n_ok": n_ok,
            "gate": GATE,
            "claim_scope": "r50plus_v3_dense_readable_office_drawn_n>=8_softmatch_qwen35_2b_bare",
            "gate2_3_untouched": True,
            "v1_v2_heldout_untouched": True,
        })
    else:
        J(claim_path, {
            "kind": "vision_gate_v3_dense_claim",
            "timestamp": ts(),
            "vl_gate_v3_claim": False,
            "rate": round(rate, 4),
            "n": n,
            "n_ok": n_ok,
            "gate": GATE,
            "reason": "below_gate_or_n",
            "gate2_3_untouched": True,
        })

    payload = {
        "kind": "r50plus_c73b_vision_v3_dense_smoke",
        "timestamp": ts(),
        "gate": GATE,
        "dir": "evo/office/fixtures/vision_images_v3_dense",
        "n": n,
        "n_ok": n_ok,
        "rate": round(rate, 4),
        "gate_pass": claim,
        "items": items,
        "lora_optional": lora_block,
        "innovation": "Harder denser OCR/table VL smoke; claim only if >=0.6",
        "gate2_3_untouched": True,
        "v1_v2_claims_untouched": True,
    }
    J(ROOT / "docs/r50/C73b_vision_v3_dense_smoke.json", payload)
    print(json.dumps({
        "rate": round(rate, 4),
        "n_ok": n_ok,
        "n": n,
        "claim": claim,
        "lora_rate": None if not lora_block else lora_block["rate"],
        "lora_delta": None if not lora_block else lora_block["delta_vs_bare"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
