"""Batch-promote successful adapters into capability atoms."""

from __future__ import annotations

import json
from pathlib import Path

from evo.crystal.crystallize import crystallize_from_adapter
from evo.util import repo_path


def discover_success_adapters(runs_root: Path | None = None) -> list[dict]:
    """Find census/fit adapters that look successful (have policy weights)."""
    root = runs_root or repo_path("runs")
    found = []
    # Known cleared add adapters
    candidates = [
        ("add6_mlp", "add", root / "evoplast_adapter", ["mlp"], 1.0),
        ("add6_census_mlp_s0", "add", root / "evoplast_census_mlp_s0", ["mlp"], 1.0),
        ("add6_census_mlp_s1", "add", root / "evoplast_census_mlp_s1", ["mlp"], 1.0),
        ("add6_census_mlp_s2", "add", root / "evoplast_census_mlp_s2", ["mlp"], 0.75),
        ("add6_census_attn_mlp_s0", "add", root / "evoplast_census_attn_mlp_s0", ["attn", "mlp"], 1.0),
        ("add6_census_attn_mlp_s1", "add", root / "evoplast_census_attn_mlp_s1", ["attn", "mlp"], 1.0),
        ("add6_census_attn_mlp_s2", "add", root / "evoplast_census_attn_mlp_s2", ["attn", "mlp"], 1.0),
    ]
    for name, skill, path, sites, bare in candidates:
        policy = path / "policy" / "adapter_model.safetensors"
        if policy.is_file() or (path / "adapter_model.safetensors").is_file():
            found.append(
                {
                    "name": name,
                    "skill": skill,
                    "adapter_dir": str(path),
                    "sites": sites,
                    "bare_rate": bare,
                    "birth": 0.0,
                }
            )
    return found


def batch_crystallize(runs_root: Path | None = None, *, criterion: float = 0.6) -> dict:
    rows = discover_success_adapters(runs_root)
    promoted = []
    skipped = []
    for row in rows:
        if float(row["bare_rate"]) < criterion:
            skipped.append({**row, "why": "bare_rate below criterion"})
            continue
        # skip if already present with same name
        dest = repo_path("runs") / "capabilities" / row["name"]
        if (dest / "capability.json").is_file():
            skipped.append({**row, "why": "already crystallized"})
            continue
        atom = crystallize_from_adapter(
            row["name"],
            row["skill"],
            row["adapter_dir"],
            bare_rate=float(row["bare_rate"]),
            birth=row.get("birth"),
            sites=list(row["sites"]),
            evidence={"source": "batch_crystallize", "adapter": row["adapter_dir"]},
            criterion=criterion,
        )
        promoted.append(atom.to_dict())
    report = {"promoted": promoted, "skipped": skipped, "n_promoted": len(promoted)}
    out = repo_path("runs") / "capabilities" / "batch_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")
    return report
