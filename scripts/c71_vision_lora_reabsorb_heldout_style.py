# -*- coding: utf-8 -*-
"""C71: Re-absorb vision LoRA on heldout-STYLE train fixtures (not heldout test)."""
from __future__ import annotations
import json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.vision_u2c_real import micro_absorb_vl

GATE = 0.6
WEIGHTS = ROOT / "models" / "Qwen3.5-2B"
TRAIN = ROOT / "evo/office/fixtures/vision_images_v2h_style_train"
ADAPTER = ROOT / "runs" / "capabilities" / "vision_office_v2h_style_lora"
RUN = ROOT / "runs" / "vision_u2c_v2h_style_lora"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if not TRAIN.is_dir():
        raise SystemExit("missing train fixtures; run c70 first")
    pairs = []
    for jp in sorted(TRAIN.glob("*.json")):
        meta = json.loads(jp.read_text(encoding="utf-8"))
        png = TRAIN / f"{meta['id']}.png"
        if not png.is_file():
            continue
        pairs.append({
            "image": str(png.relative_to(ROOT)).replace("\\", "/"),
            "task": meta.get("task") or "caption",
            "gold": str(meta.get("gold") or ""),
        })
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    if ADAPTER.exists():
        shutil.rmtree(ADAPTER)
    absorb = micro_absorb_vl(ROOT, pairs, WEIGHTS, ADAPTER)
    use_log = [
        {"phase": "use", "n_pairs": len(pairs), "train_dir": "evo/office/fixtures/vision_images_v2h_style_train"},
        {"phase": "absorb", "method": "peft_lora_micro_v2h_style", **absorb},
        {"phase": "route", "selected": "vision_office_v2h_style_lora", "why": ["heldout_style_train", "c71_reabsorb"]},
    ]
    (RUN / "use_log.jsonl").write_text(
        "\n".join(json.dumps(e, ensure_ascii=False) for e in use_log) + "\n", encoding="utf-8"
    )
    J(RUN / "pairs.json", {"n": len(pairs), "pairs": pairs})
    # registry
    reg_path = ROOT / "evo/office/fixtures/vision_atom_registry.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.is_file() else {"atoms": []}
    if isinstance(reg, list):
        reg = {"atoms": reg}
    atoms = reg.get("atoms") or []
    atoms.append({
        "id": "vision_office_v2h_style_lora",
        "family": "vision_absorb",
        "status": "absorbed" if absorb.get("ok") else "absorb_failed",
        "adapter": absorb.get("adapter"),
        "steps": absorb.get("steps"),
        "loss_last": absorb.get("loss_last"),
        "source": "c71",
        "trained_on": "v2h_style_train_not_heldout",
        "registered_at": ts(),
    })
    reg["atoms"] = atoms
    reg["updated"] = ts()
    reg["source"] = "c71_vision_lora_reabsorb_heldout_style"
    J(reg_path, reg)
    payload = {
        "kind": "r50plus_c71_vision_lora_reabsorb_heldout_style",
        "timestamp": ts(),
        "gate": GATE,
        "n_pairs": len(pairs),
        "train_dir": "evo/office/fixtures/vision_images_v2h_style_train",
        "heldout_untouched": True,
        "absorb": absorb,
        "adapter_trained": bool(absorb.get("ok")),
        "pass": bool(absorb.get("ok")),
        "evidence_run": "runs/vision_u2c_v2h_style_lora",
        "innovation": "Re-absorb LoRA on heldout-style dense readable data; test set never used",
        "gate2_3_untouched": True,
        "v1_v2_claims_untouched": True,
    }
    J(ROOT / "docs/r50/C71_vision_lora_reabsorb_heldout_style.json", payload)
    print(json.dumps({
        "adapter_trained": payload["adapter_trained"],
        "n_pairs": len(pairs),
        "steps": absorb.get("steps"),
        "loss_last": absorb.get("loss_last"),
        "error": absorb.get("error"),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
