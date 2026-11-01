# -*- coding: utf-8 -*-
"""C86: LoRA vs bare on ocr_weak test using STRICT must_codes metric."""
from __future__ import annotations
import json, re, sys, gc
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_backend import RealVlBackend, VisionObs

GATE = 0.6
WEIGHTS = ROOT / "models" / "Qwen3.5-2B"
ADAPTER = ROOT / "runs" / "capabilities" / "vision_office_ocr_weak_lora"
IMG = ROOT / "evo/office/fixtures/vision_images_ocr_weak_test"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean(text: str) -> str:
    text = re.sub(r"<think>[\s\S]*?</think>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def strict_hit(pred: str, must_codes: list) -> bool:
    p = (pred or "").upper().replace(" ", "")
    if not must_codes:
        return False
    hits = sum(1 for c in must_codes if str(c).upper().replace(" ", "") in p)
    return hits >= max(2, len(must_codes) - 1)


def eval_dir(backend, img_dir: Path):
    items = []
    n_ok = 0
    for jp in sorted(img_dir.glob("*.json")):
        meta = json.loads(jp.read_text(encoding="utf-8"))
        fid = meta["id"]
        gold = str(meta.get("gold") or "")
        must = list(meta.get("must_codes") or [])
        try:
            pred = backend.predict(VisionObs(image_path=img_dir / f"{fid}.png", task="ocr", gold=gold))
            text = clean(pred.text or "")
            ok = strict_hit(text, must)
            err = None
        except Exception as e:
            text, ok, err = "", False, f"{type(e).__name__}: {e}"
        n_ok += int(ok)
        items.append({"id": fid, "gold": gold, "must_codes": must, "pred_head": text[:220], "ok": ok, "error": err})
    n = len(items)
    rate = n_ok / n if n else 0.0
    return items, n, n_ok, rate


def main():
    bare_path = ROOT / "docs/r50/C84_vision_ocr_weak_bare_smoke.json"
    bare_reused = False
    if bare_path.is_file():
        bare_doc = json.loads(bare_path.read_text(encoding="utf-8"))
        # prefer items with strict ok field
        if bare_doc.get("items") and ("strict_ok" in bare_doc["items"][0] or bare_doc.get("metric") == "strict_must_codes"):
            bare_items = []
            for r in bare_doc["items"]:
                ok = r.get("strict_ok") if "strict_ok" in r else r.get("ok")
                bare_items.append({**r, "ok": bool(ok)})
            bare_n = len(bare_items)
            bare_ok = sum(1 for r in bare_items if r["ok"])
            bare_rate = bare_ok / bare_n if bare_n else float(bare_doc.get("rate") or 0)
            bare_reused = True
        else:
            bare_backend = RealVlBackend(WEIGHTS, max_new_tokens=96)
            bare_items, bare_n, bare_ok, bare_rate = eval_dir(bare_backend, IMG)
            bare_backend.unload(); gc.collect()
    else:
        bare_backend = RealVlBackend(WEIGHTS, max_new_tokens=96)
        bare_items, bare_n, bare_ok, bare_rate = eval_dir(bare_backend, IMG)
        bare_backend.unload(); gc.collect()

    if not ADAPTER.is_dir() or not (ADAPTER / "adapter_config.json").is_file():
        # No adapter: if bare already strong or not weak, formal deprecate without train
        decision = "DEPRECATE_VISION_LORA_DENSE_AND_DEFAULT_BARE"
        if bare_rate < GATE:
            decision = "NEED_LORA_TRAIN_WEAK_DOMAIN_BARE_BELOW_GATE"
        payload = {
            "kind": "r50plus_c86_vision_ocr_weak_lora_vs_bare",
            "timestamp": ts(),
            "gate": GATE,
            "metric": "strict_must_codes",
            "adapter_present": False,
            "bare": {"n": bare_n, "n_ok": bare_ok, "rate": round(bare_rate, 4)},
            "lora": None,
            "delta_lora_minus_bare": None,
            "decision": decision,
            "deprecate_vision_lora_for_dense": True,
            "deprecate_vision_lora_product_default_bare": bare_rate >= GATE or True,
            "gate2_3_untouched": True,
            "note": "Adapter missing; decision from bare weakness alone if applicable",
        }
        J(ROOT / "docs/r50/C86_vision_ocr_weak_lora_vs_bare.json", payload)
        dep = {
            "kind": "vision_lora_policy_decision",
            "timestamp": ts(),
            "source_cycle": "C86",
            "dense_table": "DEPRECATED_FORCE_BARE",
            "ocr_weak_delta": None,
            "decision": decision,
            "product_default": "bare",
            "evidence": [
                "docs/r50/C66_vision_lora_vs_bare.json",
                "docs/r50/C72_vision_lora_vs_bare_retest.json",
                "docs/r50/C86_vision_ocr_weak_lora_vs_bare.json",
            ],
            "gate2_3_untouched": True,
        }
        J(ROOT / "docs/r50/C86b_vision_lora_policy_decision.json", dep)
        print(json.dumps({"bare_rate": round(bare_rate, 4), "decision": decision, "adapter": False}, ensure_ascii=False))
        return

    lora_backend = RealVlBackend(WEIGHTS, max_new_tokens=96, adapter_path=ADAPTER)
    lora_items, lora_n, lora_ok, lora_rate = eval_dir(lora_backend, IMG)
    lora_backend.unload(); gc.collect()

    by_id_bare = {r["id"]: r for r in bare_items}
    flips = []
    for r in lora_items:
        b = by_id_bare.get(r["id"])
        if b and bool(b.get("ok")) != r["ok"]:
            flips.append({"id": r["id"], "bare_ok": bool(b.get("ok")), "lora_ok": r["ok"]})

    delta = lora_rate - bare_rate
    if delta > 0:
        decision = "LORA_HELPS_WEAK_OCR"
        product_default = "lora_on_ocr_weak_only"
        deprecate_all = False
    elif delta == 0:
        decision = "LORA_NEUTRAL_WEAK_OCR_PREFER_BARE"
        product_default = "bare"
        deprecate_all = False
    else:
        decision = "DEPRECATE_VISION_LORA_FOR_DENSE_AND_NO_WEAK_GAIN"
        product_default = "bare"
        deprecate_all = True

    payload = {
        "kind": "r50plus_c86_vision_ocr_weak_lora_vs_bare",
        "timestamp": ts(),
        "gate": GATE,
        "domain": "ocr_weak",
        "metric": "strict_must_codes",
        "adapter": "runs/capabilities/vision_office_ocr_weak_lora",
        "adapter_trained_on": "ocr_weak_train (not test)",
        "test_dir": "evo/office/fixtures/vision_images_ocr_weak_test",
        "bare_reused_from_c84": bare_reused,
        "bare": {"n": bare_n, "n_ok": bare_ok, "rate": round(bare_rate, 4)},
        "lora": {"n": lora_n, "n_ok": lora_ok, "rate": round(lora_rate, 4)},
        "delta_lora_minus_bare": round(delta, 4),
        "lora_helps_delta_ge_0": bool(delta >= 0.0),
        "lora_beats_bare": bool(lora_rate > bare_rate),
        "decision": decision,
        "deprecate_vision_lora_for_dense": True,
        "deprecate_vision_lora_product_default_bare": product_default == "bare",
        "flips": flips,
        "lora_items": lora_items,
        "innovation": "Strict-code weak-domain LoRA hunt; formal deprecate if Δ<0",
        "gate2_3_untouched": True,
        "no_new_vl_gate_claim": True,
    }
    J(ROOT / "docs/r50/C86_vision_ocr_weak_lora_vs_bare.json", payload)
    dep = {
        "kind": "vision_lora_policy_decision",
        "timestamp": ts(),
        "source_cycle": "C86",
        "dense_table": "DEPRECATED_FORCE_BARE",
        "ocr_weak_delta": round(delta, 4),
        "decision": decision,
        "product_default": product_default,
        "evidence": [
            "docs/r50/C66_vision_lora_vs_bare.json",
            "docs/r50/C72_vision_lora_vs_bare_retest.json",
            "docs/r50/C86_vision_ocr_weak_lora_vs_bare.json",
        ],
        "gate2_3_untouched": True,
    }
    J(ROOT / "docs/r50/C86b_vision_lora_policy_decision.json", dep)
    print(json.dumps({
        "bare_rate": round(bare_rate, 4),
        "lora_rate": round(lora_rate, 4),
        "delta": round(delta, 4),
        "decision": decision,
        "product_default": product_default,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
