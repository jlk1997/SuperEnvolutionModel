# -*- coding: utf-8 -*-
"""蚁算-视 real VL U2C: use→grade→crystallize→micro-absorb→route. Honest only."""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


def clean(s: str) -> str:
    import re
    s = re.sub(r"<think>[\s\S]*?</think>", " ", s or "")
    return re.sub(r"\s+", " ", s).strip()


def micro_absorb_vl(root: Path, pairs: list[dict], weights: Path, out_adapter: Path) -> dict:
    """Tiny LoRA absorb on Qwen3.5-2B using text+image pairs. Few steps, honest."""
    import torch
    from peft import LoraConfig, get_peft_model
    from PIL import Image
    from transformers import AutoModelForImageTextToText, AutoProcessor

    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor = AutoProcessor.from_pretrained(str(weights), trust_remote_code=True)
    model = AutoModelForImageTextToText.from_pretrained(
        str(weights), trust_remote_code=True, dtype=torch.bfloat16 if device == "cuda" else torch.float32,
        device_map="auto" if device == "cuda" else None,
    )
    # target common projection / attn modules; fall back to all-linear if needed
    targets = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    try:
        peft_cfg = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.0, bias="none", target_modules=targets)
        model = get_peft_model(model, peft_cfg)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"lora_attach:{type(e).__name__}:{e}", "steps": 0}

    model.train()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=1e-4)
    steps = 0
    losses = []
    prompts = {
        "caption": "Describe this image in one short sentence.",
        "ocr": "Read all visible text in this image. Reply with the text only.",
        "table_cells": "Extract the table as CSV. Reply with CSV only.",
    }
    for epoch in range(2):
        for row in pairs:
            img = Image.open(root / row["image"]).convert("RGB")
            task = row["task"]
            gold = row["gold"]
            user = prompts.get(task, prompts["caption"])
            messages = [
                {"role": "user", "content": [{"type": "image", "image": img}, {"type": "text", "text": user}]},
                {"role": "assistant", "content": [{"type": "text", "text": gold}]},
            ]
            try:
                chat = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
                batch = processor(text=[chat], images=[img], return_tensors="pt", padding=True)
                batch = {k: v.to(model.device) if hasattr(v, "to") else v for k, v in batch.items()}
                labels = batch["input_ids"].clone()
                out = model(**batch, labels=labels)
                loss = out.loss
                if loss is None:
                    continue
                opt.zero_grad()
                loss.backward()
                opt.step()
                steps += 1
                losses.append(float(loss.detach().cpu()))
            except Exception as e:  # noqa: BLE001
                return {"ok": False, "error": f"train_step:{type(e).__name__}:{e}", "steps": steps, "losses": losses}

    out_adapter.mkdir(parents=True, exist_ok=True)
    try:
        model.save_pretrained(str(out_adapter))
        processor.save_pretrained(str(out_adapter))
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"save:{type(e).__name__}:{e}", "steps": steps, "losses": losses}
    return {
        "ok": True,
        "steps": steps,
        "loss_last": losses[-1] if losses else None,
        "loss_mean": sum(losses) / len(losses) if losses else None,
        "adapter": str(out_adapter.relative_to(root)).replace("\\", "/"),
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    smoke_path = root / "docs" / "VISION_V0_SMOKE_REAL_VL_2026-10-18.json"
    smoke = json.loads(smoke_path.read_text(encoding="utf-8"))
    weights = Path(smoke["weights_path"])
    base = root / "runs" / "vision_u2c_real"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)

    use_log = []
    graded = []
    pairs = []
    for row in smoke["rows"]:
        img_rel = f"evo/office/fixtures/vision_images_real/{row['image']}"
        ok = bool(row.get("ok"))
        use_log.append({
            "phase": "use",
            "task_id": row["image"],
            "task": row["task"],
            "image": img_rel,
            "pred": row.get("pred"),
            "backend": "real_vl",
            "synthetic_not_vl": False,
            "weights_local": True,
        })
        graded.append({"task_id": row["image"], "ok": ok, "gold": row.get("gold")})
        use_log.append({"phase": "grade", "task_id": row["image"], "ok": ok})
        if ok:
            pairs.append({
                "image": img_rel,
                "task": row["task"],
                "gold": row["gold"],
                "pred": row.get("pred"),
            })

    rate = sum(1 for g in graded if g["ok"]) / max(len(graded), 1)
    pairs_path = base / "vision_graded_pairs.jsonl"
    pairs_path.write_text("\n".join(json.dumps(p, ensure_ascii=False) for p in pairs) + "\n", encoding="utf-8")

    # crystallize
    atoms = []
    for fam in ("caption", "ocr", "table"):
        atoms.append({
            "atom": f"vision_{fam}_uselog_real",
            "family": f"vision_{fam}",
            "status": "crystallized_real_vl",
            "source": "vision_u2c_real",
            "bare_rate": rate,
            "criterion": 0.6,
            "weights_local": True,
            "vl_gate_claim": False,
            "synthetic_not_vl": False,
            "weights_path": str(weights).replace("\\", "/"),
        })
    atom_path = base / "vision_atoms_crystallized.json"
    atom_path.write_text(json.dumps({"atoms": atoms, "rate": rate}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    use_log.append({"phase": "crystallize", "n_atoms": len(atoms), "path": str(atom_path.relative_to(root)).replace("\\", "/")})

    # micro absorb (real train)
    adapter_dir = root / "runs" / "capabilities" / "vision_office_real_vl_lora"
    absorb = micro_absorb_vl(root, pairs, weights, adapter_dir)
    use_log.append({"phase": "absorb", "method": "peft_lora_micro", **absorb})

    # route
    use_log.append({
        "phase": "route",
        "selected": [a["atom"] for a in atoms],
        "why": ["real_vl_crystal", "prefer_vision_atoms_when_image", "weights_local"],
        "backend": "real_vl",
    })

    log_path = base / "vision_u2c_use_log.jsonl"
    log_path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in use_log) + "\n", encoding="utf-8")

    # registry update
    reg_path = root / "evo" / "office" / "fixtures" / "vision_atom_registry.json"
    registry = {
        "kind": "vision_atom_registry",
        "product": "蚁算-视",
        "version": "STRONG_C3_REAL_VL",
        "gate": "0.6",
        "weights_local": True,
        "vl_gate_claim": False,
        "weights_path": str(weights).replace("\\", "/"),
        "atoms": [
            {
                "atom": a["atom"],
                "family": a["family"],
                "status": "crystallized_real_vl" + ("_absorbed" if absorb.get("ok") else "_absorb_attempted"),
                "stub_path": None,
                "bare_rate": rate,
                "adapter": absorb.get("adapter"),
                "dissolve_path": [
                    "real VL use_log -> grade",
                    "crystallize vision_*_uselog_real",
                    "micro LoRA absorb",
                    "route prefer_atoms when image",
                ],
            }
            for a in atoms
        ],
        "notes": "Real VL unlocked via Qwen3.5-2B. vl_gate_claim false until formal VISION_GATE doc.",
    }
    reg_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    phases = [e["phase"] for e in use_log]
    required = ["use", "grade", "crystallize", "absorb", "route"]
    evidence = {
        "kind": "vision_u2c_real",
        "product": "蚁算-视",
        "version": "STRONG_C3",
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "gate": "0.6",
        "weights_local": True,
        "synthetic_not_vl": False,
        "weights_path": str(weights).replace("\\", "/"),
        "n_tasks": len(graded),
        "rate": rate,
        "gate_pass_smoke": rate >= 0.6,
        "absorb": absorb,
        "atoms": atoms,
        "phases_present": phases,
        "required_phases": required,
        "registry_updated": str(reg_path.relative_to(root)).replace("\\", "/"),
        "log": str(log_path.relative_to(root)).replace("\\", "/"),
        "pairs": str(pairs_path.relative_to(root)).replace("\\", "/"),
        "vl_gate_claim": False,
        "pass": all(p in phases for p in required) and rate >= 0.6,
        "notes": "Real VL U2C on drawn office fixtures. Absorb is micro LoRA; not a full Epoch D CLAIM.",
    }
    out = root / "docs" / "VISION_U2C_REAL_2026-10-18.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pass": evidence["pass"], "rate": rate, "absorb_ok": absorb.get("ok"), "path": str(out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
