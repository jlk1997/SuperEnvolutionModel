"""Language-model plasticity census (Epoch A-3).

Preregistered multi-seed, multi-site smoke-to-full path. Does not lower the 0.6 gate.
Full runs are expensive on a laptop GPU; use `dry: true` to write the plan only, or
`smoke: true` for one seed / mlp / skill=add.
"""

from __future__ import annotations

import json
import time
from copy import deepcopy
from typing import Any

from evo.registry import PRIMARY, require_ready
from evo.util import repo_path


DEFAULT_SITES = (
    ("mlp", ["mlp"]),
    ("attn", ["attn"]),
    ("attn_mlp", ["attn", "mlp"]),
)


def plan_cells(cfg: dict) -> list[dict]:
    seeds = list(cfg.get("seeds") or [int(cfg.get("seed", 0))])
    if cfg.get("smoke"):
        seeds = seeds[:1]
    site_rows = list(cfg.get("site_sweeps") or DEFAULT_SITES)
    if cfg.get("smoke"):
        site_rows = [row for row in site_rows if row[0] == "mlp"][:1] or site_rows[:1]
    skill = str(cfg.get("skill") or ("add" if cfg.get("smoke") else "stack"))
    cells = []
    for seed in seeds:
        for name, sites in site_rows:
            cells.append(
                {
                    "seed": int(seed),
                    "site_id": name,
                    "fit_sites": list(sites),
                    "skill": skill,
                }
            )
    return cells


def run_census(cfg: dict) -> dict:
    """Run or dry-run the preregistered LM plasticity census."""
    cfg = dict(cfg)
    require_ready(cfg)
    cells = plan_cells(cfg)
    report: dict[str, Any] = {
        "stage": "census",
        "preregistered": True,
        "criterion": 0.6,
        "model_name": cfg.get("model_name"),
        "primary": PRIMARY,
        "n_cells": len(cells),
        "cells_plan": cells,
        "dry": bool(cfg.get("dry")),
        "smoke": bool(cfg.get("smoke")),
        "results": [],
        "passed": False,
    }
    if cfg.get("dry"):
        report["status"] = "dry_plan"
        report["passed"] = None
        report["recommendation"] = (
            "Dry plan only. Re-run with dry: false to execute. "
            "Judge each cell by model.passed; do not lower 0.6."
        )
        _write(cfg, report)
        return report

    from evo.plastic.fit import run_model_fit

    started = time.perf_counter()
    for cell in cells:
        child = deepcopy(cfg)
        child["seed"] = cell["seed"]
        child["fit_sites"] = cell["fit_sites"]
        child["skill"] = cell["skill"]
        child["actor"] = "model"
        child["stage"] = "m0"
        child["write"] = False
        # Avoid clobbering the main fit adapter unless this cell passes.
        child["adapter_dir"] = str(
            repo_path("runs")
            / f"evoplast_census_{cell['site_id']}_s{cell['seed']}"
        )
        print(
            f"[census] seed={cell['seed']} sites={cell['site_id']} skill={cell['skill']}",
            flush=True,
        )
        t0 = time.perf_counter()
        try:
            model = run_model_fit(child)
        except Exception as exc:  # noqa: BLE001 — census must record cell failures
            model = {
                "passed": False,
                "status": "error",
                "reason": f"{type(exc).__name__}: {exc}",
            }
        row = {
            **cell,
            "seconds": round(time.perf_counter() - t0, 1),
            "passed": bool(model.get("passed")),
            "status": model.get("status"),
            "birth": model.get("birth"),
            "add_rate": model.get("add_rate"),
            "add_kept": model.get("add_kept"),
            "gain": model.get("gain"),
            "vram_mb": model.get("vram_mb"),
            "recommendation": model.get("recommendation") or model.get("reason"),
            "adapter": model.get("adapter"),
        }
        report["results"].append(row)
        print(
            f"[census] done passed={row['passed']} status={row['status']} s={row['seconds']}",
            flush=True,
        )

    report["seconds"] = round(time.perf_counter() - started, 1)
    report["n_passed"] = sum(1 for row in report["results"] if row["passed"])
    # Smoke passes if the single mlp/add cell clears 0.6. Full census requires
    # every preregistered cell to pass (strict); partial maps are still written.
    if report["smoke"]:
        report["passed"] = report["n_passed"] == len(report["results"]) and bool(report["results"])
    else:
        report["passed"] = report["n_passed"] == len(report["results"]) and bool(report["results"])
    report["status"] = "passed" if report["passed"] else "failed"
    _write(cfg, report)
    return report


def _write(cfg: dict, report: dict) -> None:
    if not cfg.get("write", True):
        return
    name = str(cfg.get("run_name") or "evoplast_census")
    dest = repo_path("runs") / f"{name}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")
    print(f"[census] wrote {dest}", flush=True)
