"""Nightly population. Each candidate carries a recipe. The exam does not pick the winner."""

from __future__ import annotations

import math
import random


def base_gene(cfg: dict) -> dict:
    return {
        "outer_lr": float(cfg.get("outer_lr", 5e-4)),
        "night_epochs": int(cfg.get("night_epochs", 2)),
        "chain_repeat": int(cfg.get("chain_repeat", 2)),
        "kl_coef": float(cfg.get("kl_coef", 0.5)),
        "refine": bool(cfg.get("refine", True)),
        "contrast_rounds": int(cfg.get("contrast_rounds", 6)),
        "replay_ratio": float(cfg.get("replay_ratio", 1.0)),
    }


def mutate(gene: dict, rng: random.Random) -> dict:
    child = dict(gene)
    child["outer_lr"] = min(2e-3, max(1e-5, float(gene["outer_lr"]) * math.exp(rng.uniform(-0.4, 0.4))))
    child["night_epochs"] = min(4, max(1, int(gene["night_epochs"]) + rng.choice([-1, 0, 1])))
    child["chain_repeat"] = min(4, max(1, int(gene["chain_repeat"]) + rng.choice([-1, 0, 1])))
    child["kl_coef"] = min(1.0, max(0.0, float(gene["kl_coef"]) + rng.uniform(-0.15, 0.15)))
    if rng.random() < 0.2:
        child["refine"] = not bool(gene["refine"])
    child["contrast_rounds"] = min(8, max(1, int(gene["contrast_rounds"]) + rng.choice([-2, -1, 0, 1, 2])))
    child["replay_ratio"] = min(1.0, max(0.25, float(gene["replay_ratio"]) + rng.uniform(-0.2, 0.2)))
    return child


def initial_genes(cfg: dict, count: int, rng: random.Random) -> list[dict]:
    origin = base_gene(cfg)
    genes = [origin]
    while len(genes) < count:
        genes.append(mutate(origin, rng))
    return genes


def inherit_genes(winner: dict, count: int, rng: random.Random) -> list[dict]:
    genes = [dict(winner)]
    while len(genes) < count:
        genes.append(mutate(winner, rng))
    return genes


def apply_gene(cfg: dict, gene: dict) -> dict:
    night = dict(cfg)
    night.update(gene)
    return night


def fitness(gate_after: float, chain_ok: bool | None, retest: float) -> float:
    chain = 0.5 if chain_ok is None else (1.0 if chain_ok else 0.0)
    return (float(gate_after) + chain + float(retest)) / 3.0
