# -*- coding: utf-8 -*-
"""C85: Micro-LoRA absorb on ocr_weak TRAIN only (test untouched)."""
from __future__ import annotations
import json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.vision_u2c_real import micro_absorb_vl

GATE = 0.6
WEIGHTS = ROOT / "models" / "Qwen3.5-2B"
TRAIN = ROOT / "evo/office/fixtures/vision_images_ocr_weak_train"
ADAPTER = ROOT / "runs" / "capabilities" / "vision_office_ocr_weak_lora"
RUN = ROOT / "runs" / "vision_u2c_ocr_weak_lora"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if not TRAIN.is_dir():
        raise SystemExit("missing train; run c83")
    pairs = []
    for jp in sorted(TRAIN.glob("*.json")):
        meta = json.loads(jp.read_text(encoding="utf-8"))
        png = TRAIN / f"{meta['id']}.png"
        if not png.is_file():
            continue
        pairs.append({
            "image": str(png.relative_to(ROOT)).replace("\\", "/"),
            "task": meta.get("task") or "ocr",
            "gold": str(meta.get("gold") or ""),
            "domain": "ocr_weak",
        })
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    if ADAPTER.exists():
        shutil.rmtree(ADAPTER)
    absorb = micro_absorb_vl(ROOT, pairs, WEIGHTS, ADAPTER)
    use_log = [
        {"phase": "use", "n_pairs": len(pairs), "train_dir": "evo/office/fixtures/vision_images_ocr_weak_train"},
        {"phase": "absorb", "method": "peft_lora_micro_ocr_weak", **absorb},
        {"phase": "route", "selected": "vision_office_ocr_weak_lora", "why": ["domain=ocr_weak", "c85"]},
    ]
    (RUN / "use_log.jsonl").write_text(
        "\n".join(json.dumps(e, ensure_ascii=False) for e in use_log) + "\n", encoding="utf-8"
    )
    J(RUN / "pairs.json", {"n": len(pairs), "pairs": pairs})
    reg_path = ROOT / "evo/office/fixtures/vision_atom_registry.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.is_file() else {"atoms": []}
    if isinstance(reg, list):
        reg = {"atoms": reg}
    atoms = reg.get("atoms") or []
    atoms.append({
        "id": "vision_office_ocr_weak_lora",
        "family": "vision_absorb",
        "domain": "ocr_weak",
        "status": "absorbed" if absorb.get("ok") else "absorb_failed",
        "adapter": absorb.get("adapter"),
        "steps": absorb.get("steps"),
        "loss_last": absorb.get("loss_last"),
        "source": "c85",
        "trained_on": "ocr_weak_train_not_test",
        "registered_at": ts(),
    })
    reg["atoms"] = atoms
    reg["updated"] = ts()
    reg["source"] = "c85_vision_ocr_weak_lora_absorb"
    J(reg_path, reg)
    payload = {
        "kind": "r50plus_c85_vision_ocr_weak_lora_absorb",
        "timestamp": ts(),
        "gate": GATE,
        "domain": "ocr_weak",
        "n_pairs": len(pairs),
        "train_dir": "evo/office/fixtures/vision_images_ocr_weak_train",
        "test_untouched": True,
        "absorb": absorb,
        "adapter_trained": bool(absorb.get("ok")),
        "pass": bool(absorb.get("ok")),
        "evidence_run": "runs/vision_u2c_ocr_weak_lora",
        "innovation": "LoRA absorb only on weak OCR train; hunt Δ≥0 on disjoint test",
        "gate2_3_untouched": True,
    }
    J(ROOT / "docs/r50/C85_vision_ocr_weak_lora_absorb.json", payload)
    print(json.dumps({
        "adapter_trained": payload["adapter_trained"],
        "n_pairs": len(pairs),
        "steps": absorb.get("steps"),
        "loss_last": absorb.get("loss_last"),
        "error": absorb.get("error"),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
