"""Evolve the trainer on real lives, then test it on rules evolution never saw.

One generation is one set of training rules, shared by every individual
(common random numbers). Fitness is `life.fitness` on selection inputs.
After the last generation three lives run on the held-out rules:

- hand: the hand-set trainer, from birth weights.
- baldwin: the best evolved trainer, from birth weights. Only the genes are inherited.
- lamarck: the best evolved trainer, from the policy weights its training life ended with.

Lamarck inherits `policy` only. A rule that lived in a slot is not carried over.
"""

from __future__ import annotations

import math
import random
import time

import torch


def run_evolve(cfg: dict) -> dict:
    from evo.evolution.es import DiagCMA, OpenAIES
    from evo.model import adapter_state, release
    from evo.plastic.curriculum import by_id, catalog, new_skills, split_skills
    from evo.plastic.life import build_body, cached_births, fitness, live
    from evo.plastic.real_genome import LIFE_GENES, decode_life, default_vector

    if not torch.cuda.is_available():
        return {"status": "no_cuda", "passed": False}
    started = time.time()
    seed = int(cfg.get("seed", 0))
    body = build_body(cfg)
    try:
        mode = str(cfg.get("skill_mode", "shown"))
        births = cached_births(body, cfg, mode)
        primer_id = cfg.get("life_primer", "add6")
        primer = by_id(primer_id, mode) if primer_id else None
        train, held = split_skills(catalog(mode))
        rule = str(cfg.get("birth_rule", "new"))
        train_new = [skill for skill in new_skills(train, births, rule) if primer is None or skill.id != primer.id]
        held_new = new_skills(held, births, rule)
        if len(train_new) < 2 or not held_new:
            return {"status": "too_few_rules", "passed": False, "train": [s.id for s in train_new], "held": [s.id for s in held_new]}
        start = default_vector()
        if str(cfg.get("es_kind", "openai")) == "cma":
            search = DiagCMA(len(LIFE_GENES), sigma=float(cfg.get("es_sigma", 0.6)), seed=seed, pop=int(cfg.get("es_pop", 6)), mean=start)
        else:
            search = OpenAIES(
                len(LIFE_GENES),
                sigma=float(cfg.get("es_sigma", 0.6)),
                lr=float(cfg.get("es_lr", 1.0)),
                seed=seed,
                pop=int(cfg.get("es_pairs", 3)),
                mean=start,
            )
        per_life = int(cfg.get("evolve_k", 3))
        history = []
        best = {"fitness": -math.inf}
        for generation in range(int(cfg.get("es_gens", 3))):
            rng = random.Random(seed * 100 + generation)
            skills = rng.sample(train_new, min(per_life, len(train_new)))
            vectors = search.ask()
            scores = []
            rows = []
            for index, vector in enumerate(vectors):
                genes = decode_life(vector)
                print(f"[evolve] gen {generation} child {index} rules={[s.id for s in skills]} genes={genes.as_dict()}", flush=True)
                report = live(body, skills, genes, cfg, primer=primer, final=False)
                report.pop("_learned", None)
                score = fitness(report, cfg)
                scores.append(score)
                rows.append(_child_row(index, score, genes, report))
                print(f"[evolve] gen {generation} child {index} fitness={score:.4f} samples={rows[-1]['samples']}", flush=True)
                if score > best["fitness"]:
                    best = {
                        "fitness": score,
                        "vector": list(vector),
                        "genes": genes.as_dict(),
                        "generation": generation,
                        "rules": [skill.id for skill in skills],
                        "state": adapter_state(body.evo.model, "policy"),
                    }
            search.tell(scores)
            history.append(
                {
                    "generation": generation,
                    "rules": [skill.id for skill in skills],
                    "children": rows,
                    "mean_fitness": round(sum(scores) / len(scores), 6),
                    "best_fitness": round(max(scores), 6),
                    "mean_genes": decode_life(search.mean).as_dict(),
                }
            )
        heldout = _heldout(body, held_new, primer, best, cfg)
        passed = heldout["baldwin"]["fitness"] > heldout["hand"]["fitness"]
        return {
            "status": "passed" if passed else "failed",
            "passed": passed,
            "train_rules": [skill.id for skill in train_new],
            "held_rules": [skill.id for skill in held_new],
            "history": history,
            "best": {key: value for key, value in best.items() if key != "state"},
            "final_mean_genes": decode_life(search.mean).as_dict(),
            "heldout": heldout,
            "seconds": round(time.time() - started, 1),
        }
    finally:
        release(body.evo)


def _child_row(index: int, score: float, genes, report: dict) -> dict:
    return {
        "child": index,
        "fitness": score,
        "genes": genes.as_dict(),
        "samples": [row["samples"] for row in report["per_skill"] if not row.get("primer")],
        "learned": report["learned"],
        "final_select": report["final_select"],
        "slots": len(report["slots"]),
        "acceleration": report["acceleration"],
        "seconds": report["seconds"],
    }


def _heldout(body, held, primer, best: dict, cfg: dict) -> dict:
    from evo.plastic.life import fitness, live
    from evo.plastic.real_genome import decode_life, default_vector

    arms = {
        "hand": (decode_life(default_vector()), None),
        "baldwin": (decode_life(best["vector"]), None),
        "lamarck": (decode_life(best["vector"]), best["state"]),
    }
    out = {}
    for arm, (genes, state) in arms.items():
        print(f"[evolve] held-out arm {arm} rules={[s.id for s in held]}", flush=True)
        report = live(body, held, genes, cfg, primer=primer, start=state)
        report.pop("_learned", None)
        counted = [row for row in report["per_skill"] if not row.get("primer")]
        out[arm] = {
            "fitness": fitness(report, cfg),
            "samples": [row["samples"] for row in counted],
            "total_samples": sum(row["samples"] if row["samples"] is not None else 2 * int(cfg.get("life_cap", 144)) for row in counted),
            "learned": sum(1 for row in counted if row["reached"]),
            "final_real": report.get("final_real"),
            "final_select": report["final_select"],
            "acceleration": report["acceleration"],
            "slots": report["slots"],
            "seconds": report["seconds"],
        }
    return out
