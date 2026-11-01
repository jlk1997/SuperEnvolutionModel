"""Stage runners for the plasticity line. Reference lives do not load a model."""

from __future__ import annotations

import json

from evo.bench.metrics import families_for_power
from evo.evolution.genome import GENE_NAMES, decode, hand_vector
from evo.evolution.population import evolve_modes, evolve_plasticity, sweep_signal, transfer_genome
from evo.plastic.learner import PlasticLearner


def run_m0(cfg: dict | None = None) -> dict:
    cfg = cfg or {}
    genome = decode(hand_vector())
    learner = PlasticLearner(genome)
    budget = int(cfg.get("episodes", 20))
    curve, needed = learner.practice("m0-arith", "arith", budget, criterion=float(cfg.get("criterion", 0.6)))
    start = float(curve[0])
    end = float(curve[-1])
    passed = start < float(cfg.get("start_below", 0.2)) and end >= float(cfg.get("criterion", 0.6))
    report = {
        "organism": "reference",
        "passed": passed,
        "start": start,
        "end": end,
        "n": needed,
        "episodes": budget,
    }
    if not passed:
        report["recommendation"] = (
            "Within-life learning missed the gate. Move to Qwen3.5-2B or 4B, or recalibrate "
            "difficulty so the first episode sits between 0.1 and 0.4. Do not lower the gate."
        )
    if cfg.get("actor") == "model":
        from evo.plastic.lora_life import run_model_m0

        report["model"] = run_model_m0(cfg)
        model = report["model"] or {}
        report["lm_passed"] = bool(model.get("passed"))
        if not report["lm_passed"] and model.get("recommendation"):
            report["lm_recommendation"] = model["recommendation"]
    return report


def run_m1(cfg: dict | None = None) -> dict:
    del cfg
    return sweep_signal()


def run_es(cfg: dict | None = None) -> dict:
    report = evolve_plasticity(cfg or {})
    report["passed"] = _h1_passed(report)
    return report


def run_baldwin(cfg: dict | None = None) -> dict:
    cfg = cfg or {}
    report = evolve_modes(
        generations=int(cfg.get("generations", 16)),
        pop=int(cfg.get("pop", 20)),
        seed=int(cfg.get("seed", 0)),
    )
    report["passed"] = _baldwin_passed(report)
    return report


def run_transfer(cfg: dict | None = None) -> dict:
    cfg = cfg or {}
    found = evolve_plasticity(
        {
            "generations": int(cfg.get("generations", 10)),
            "pop": int(cfg.get("pop", 8)),
            "seed": int(cfg.get("seed", 0)),
            "es": cfg.get("es", "openai"),
        }
    )
    moved = transfer_genome(
        found["genome"],
        source_gain=float(cfg.get("source_gain", 0.6)),
        target_gain=float(cfg.get("target_gain", 1.0)),
    )
    moved["passed"] = moved["heritability"] >= float(cfg.get("heritability_min", 0.5))
    moved["map"] = found["map"]
    return moved


def run_plast(cfg: dict) -> dict:
    stage = str(cfg.get("stage") or "all")
    power = families_for_power()
    if stage == "m0":
        report = {"m0": run_m0(cfg), "power": power}
    elif stage == "m1":
        report = {"m1": run_m1(cfg), "power": power}
    elif stage == "es":
        report = {"es": run_es(cfg), "power": power}
    elif stage == "baldwin":
        report = {"baldwin": run_baldwin(cfg), "power": power}
    elif stage == "transfer":
        report = {"transfer": run_transfer(cfg), "power": power}
    elif stage == "life":
        from evo.plastic.life import run_life

        report = {"life": run_life(cfg)}
    elif stage == "evolve":
        from evo.plastic.evolve_real import run_evolve

        report = {"evolve": run_evolve(cfg)}
    elif stage == "grow":
        from evo.plastic.life import run_life

        report = {"grow": run_life({**cfg, "life_units": cfg.get("life_units") or _grow_units()})}
    elif stage == "stream":
        from evo.plastic.use_stream import run_stream

        report = {"stream": run_stream(cfg)}
    elif stage == "census":
        from evo.plastic.census import run_census

        report = {"census": run_census(cfg)}
    elif stage == "all":
        report = {
            "genes": len(GENE_NAMES),
            "m0": run_m0(cfg),
            "m1": run_m1(cfg),
            "es": run_es(cfg),
            "baldwin": run_baldwin(cfg),
            "transfer": run_transfer(cfg),
            "power": power,
        }
    else:
        raise ValueError(f"unknown stage {stage}")
    report["stage"] = stage
    if cfg.get("write", True):
        _write(cfg, report)
    return report


def _grow_units() -> dict:
    return {"grow": 0.9, "sleep_every": 0.35}


def _h1_passed(report: dict) -> bool:
    evolved = float(report["area"])
    weak = float(report["baselines"]["weak"]["area"])
    icl_ar = float(report["baselines"]["icl"]["ar"])
    evolved_ar = float(report["heldout"]["ar"])
    return evolved > weak + 0.02 and evolved_ar > icl_ar and evolved_ar > 1.05


def _baldwin_passed(report: dict) -> dict:
    """Checks that held on seeds 0, 1 and 2. Darwin's rare-gene path did not."""
    baldwin = report["baldwin"]["history"]
    lamarck = report["lamarck"]["history"]
    post_gain = baldwin[-1]["post_area"] - baldwin[0]["post_area"]
    birth_gain = baldwin[-1]["birth_balanced"] - baldwin[0]["birth_balanced"]
    return {
        "post_rises_more_than_birth": post_gain > birth_gain and post_gain > 0.02,
        "frequent_over_rare": baldwin[-1]["birth_frequent"] > baldwin[-1]["birth_rare"] + 0.1,
        "lamarck_writes_frequent": lamarck[-1]["offspring_birth_frequent"] > baldwin[-1]["offspring_birth_frequent"],
    }


def _write(cfg: dict, report: dict) -> None:
    from evo.util import repo_path

    name = str(cfg.get("run_name") or "evoplast")
    dest = repo_path("runs") / f"{name}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(_lite(report), indent=2), encoding="utf-8")
    print(f"[plast] wrote {dest}", flush=True)


def _lite(report: dict):
    """Drop raw genome vectors so the run file stays a result, not a checkpoint."""
    if isinstance(report, dict):
        return {key: _lite(value) for key, value in report.items() if key not in {"genome", "best_vector", "lamarck_vector"}}
    if isinstance(report, list):
        return [_lite(value) for value in report]
    if isinstance(report, float):
        return round(report, 6)
    return report
