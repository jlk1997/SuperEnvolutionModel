# -*- coding: utf-8 -*-
"""Synthetic vision U2C absorb loop — multimodal learning pipeline without VL weights.

Demonstrates: use(image) -> grade -> crystallize vision atom -> absorb stub -> route.
All scores labeled synthetic_not_vl. RealVlBackend remains blocked.
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


def run_vision_u2c(root: Path) -> dict:
    base = root / "runs" / "vision_u2c_synthetic"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)

    img_dir = root / "evo" / "office" / "fixtures" / "vision_images"
    metas = sorted(img_dir.glob("*.json"))
    use_log = []
    graded = []
    for meta_path in metas:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        # USE: synthetic backend "prediction" == gold (wiring); real VL would differ
        pred = meta.get("gold") or ""
        gold = meta.get("gold") or ""
        ok = pred.strip() == gold.strip()
        use_log.append({
            "phase": "use",
            "task_id": meta["id"],
            "task": meta["task"],
            "image": str(meta_path.with_suffix(".png").relative_to(root)).replace("\\", "/"),
            "pred": pred,
            "synthetic_not_vl": True,
        })
        graded.append({"task_id": meta["id"], "ok": ok, "gold": gold})
        use_log.append({"phase": "grade", "task_id": meta["id"], "ok": ok})

    rate = sum(1 for g in graded if g["ok"]) / max(len(graded), 1)

    # CRYSTALLIZE vision atoms from successful grades
    atoms = []
    families = sorted({(json.loads(p.read_text(encoding="utf-8"))["task"].split("_")[0]) for p in metas})
    for fam in ("caption", "ocr", "table"):
        atom = {
            "atom": f"vision_{fam}_uselog_synth",
            "family": f"vision_{fam}",
            "status": "synthetic_crystallized",
            "source": "vision_u2c_synthetic",
            "n_pairs": sum(1 for g in graded if g["ok"]),
            "weights_local": False,
            "vl_gate_claim": False,
            "synthetic_not_vl": True,
        }
        atoms.append(atom)
    atom_path = base / "vision_atoms_crystallized.json"
    atom_path.write_text(json.dumps({"atoms": atoms}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    use_log.append({"phase": "crystallize", "n_atoms": len(atoms), "path": str(atom_path.relative_to(root)).replace("\\", "/")})

    # ABSORB stub — update registry status only (no GPU)
    reg_path = root / "evo" / "office" / "fixtures" / "vision_atom_registry.json"
    registry = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.is_file() else {"atoms": []}
    for a in registry.get("atoms") or []:
        a["status"] = "synthetic_crystallized_pending_vl"
        a["last_u2c"] = "runs/vision_u2c_synthetic"
    registry["version"] = "STRONG_C2"
    registry["synthetic_u2c"] = True
    registry["weights_local"] = False
    registry["vl_gate_claim"] = False
    reg_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    use_log.append({"phase": "absorb", "method": "registry_status_update_no_train", "gpu": False})

    # ROUTE
    use_log.append({
        "phase": "route",
        "selected": [a["atom"] for a in atoms],
        "why": ["synthetic_crystal_ready", "prefer_vision_atoms_when_image", "vl_weights_absent"],
    })

    log_path = base / "vision_u2c_use_log.jsonl"
    log_path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in use_log) + "\n", encoding="utf-8")

    phases = [e["phase"] for e in use_log]
    required = ["use", "grade", "crystallize", "absorb", "route"]
    ok = all(p in phases for p in required) and rate >= 0.6

    return {
        "kind": "vision_u2c_synthetic",
        "product": "\u8681\u7b97-\u89c6",
        "version": "STRONG_C2",
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "gate": "0.6",
        "label": "synthetic_not_vl",
        "weights_local": False,
        "vl_gate_claim": False,
        "n_tasks": len(graded),
        "rate": rate,
        "atoms": atoms,
        "phases_present": phases,
        "required_phases": required,
        "registry_updated": str(reg_path.relative_to(root)).replace("\\", "/"),
        "log": str(log_path.relative_to(root)).replace("\\", "/"),
        "pass": ok,
        "notes": "Multimodal learning PIPELINE demonstrated on synthetic fixtures. Not a VL capability claim.",
    }
