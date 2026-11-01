"""Population search over genomes.

OpenAI-ES and diagonal CMA-ES search the plasticity map (Baldwinian: children
inherit the genome, not the weights). The three-mode comparison is a
truncation GA so Lamarckian inheritance has somewhere to write.
"""

from __future__ import annotations

import random

from evo.evolution.es import DiagCMA, OpenAIES
from evo.evolution.genome import GENE_NAMES, decode, icl_vector, weak_vector
from evo.evolution.lifetime import heldout_ar, lifetime_fitness, text_area


def _mutate(vector: list[float], rng: random.Random, sigma: float) -> list[float]:
    return [value + rng.gauss(0.0, sigma) for value in vector]


def evolve_mode(mode: str, generations: int = 16, pop: int = 20, seed: int = 0, sigma: float = 0.4) -> dict:
    rng = random.Random(seed)
    origin = weak_vector()
    people = [origin] + [_mutate(origin, rng, sigma) for _ in range(pop - 1)]
    history = []
    for generation in range(generations):
        scored = []
        for vector in people:
            genome = decode(vector)
            report = lifetime_fitness(genome, mode, seed=seed + generation * 1009)
            child = report["lamarck_vector"] if mode == "lamarck" else vector
            scored.append((report["fitness"], child, report))
        scored.sort(key=lambda row: row[0], reverse=True)
        history.append(_summary(generation, scored))
        parents = scored[: max(2, pop // 2)]
        people = [parents[0][1], parents[1][1]]
        while len(people) < pop:
            people.append(_mutate(rng.choice(parents)[1], rng, sigma))
    return {"mode": mode, "history": history, "best_vector": people[0]}


def evolve_modes(generations: int = 16, pop: int = 20, seed: int = 0) -> dict:
    return {mode: evolve_mode(mode, generations=generations, pop=pop, seed=seed) for mode in ("baldwin", "lamarck", "darwin")}


def evolve_plasticity(cfg: dict | None = None) -> dict:
    """ES on the text cluster. Fitness is learning-curve area. Report is held-out AR."""
    cfg = cfg or {}
    method = str(cfg.get("es", "openai"))
    generations = int(cfg.get("generations", 12))
    pop = int(cfg.get("pop", 8))
    seed = int(cfg.get("seed", 0))
    sigma = float(cfg.get("sigma", 0.45))
    lr = float(cfg.get("es_lr", 0.35))
    dim = len(GENE_NAMES)
    origin = weak_vector()
    if method == "cma":
        strategy = DiagCMA(dim, sigma=sigma, seed=seed, pop=pop, mean=origin)
    else:
        strategy = OpenAIES(dim, sigma=sigma, lr=lr, seed=seed, pop=pop, mean=origin)
        method = "openai"
    history = []
    evals = 0
    # One task seed for the whole search. Every individual is scored on it.
    task_seed = seed
    for generation in range(generations):
        samples = strategy.ask()
        scores = [text_area(decode(vector), seed=task_seed) for vector in samples]
        evals += len(scores)
        strategy.tell(scores)
        mean_genome = decode(strategy.mean)
        history.append(
            {
                "generation": generation,
                "task_seed": task_seed,
                "best": max(scores),
                "mean_fitness": text_area(mean_genome, seed=task_seed),
                "map": mean_genome.plasticity_map(),
            }
        )
    final = decode(strategy.mean)
    random_best, random_median = _random_search(evals, seed + 17, task_seed)
    return {
        "method": method,
        "evals": evals,
        "task_seed": task_seed,
        "history": history,
        "genome": final.vector,
        "map": final.plasticity_map(),
        "area": text_area(final, seed=task_seed),
        "heldout": heldout_ar(final),
        "baselines": {
            "weak": _baseline(decode(weak_vector()), task_seed),
            "icl": _baseline(decode(icl_vector()), task_seed),
            "random_best": random_best,
            "random_median": random_median,
        },
    }


def transfer_genome(genome_vector: list[float], source_gain: float = 0.6, target_gain: float = 1.0) -> dict:
    """The genome is base-agnostic. Heritability is how much of its AR survives the move."""
    from evo.bench.metrics import heritability

    genome = decode(genome_vector)
    source = heldout_ar(genome, gain=source_gain)
    target = heldout_ar(genome, gain=target_gain)
    floor = heldout_ar(decode(weak_vector()), gain=target_gain)
    return {
        "source_gain": source_gain,
        "target_gain": target_gain,
        "ar_source": source["ar"],
        "ar_transferred": target["ar"],
        "ar_floor": floor["ar"],
        "heritability": heritability(source["ar"], target["ar"], floor=floor["ar"]),
    }


def sweep_signal(seed: int = 0) -> dict:
    """M1: two genomes, one replicate. The gap must beat the replicate error."""
    del seed
    from evo.evolution.genome import make_vector

    strong = decode(_boost(make_vector(1.4)))
    weak = decode(make_vector(-2.5))
    first = text_area(strong, budget=4)
    second = text_area(strong, budget=4)
    low = text_area(weak, budget=4)
    return {
        "strong": first,
        "replicate": second,
        "weak": low,
        "gap": first - low,
        "replicate_error": abs(first - second),
        "passed": abs(first - second) < 0.02 and (first - low) > 0.15,
    }


def _boost(vector: list[float]) -> list[float]:
    from evo.evolution.genome import GENE_NAMES

    out = list(vector)
    for index, name in enumerate(GENE_NAMES):
        if name.startswith("alloc.") or name.startswith("lr.") or name in {"mem.mid_mix", "mem.slow_mix", "mem.replay_ratio"}:
            out[index] = 1.6
        if name.startswith("innate."):
            out[index] = -1.4
    return out


def _baseline(genome, task_seed: int = 0) -> dict:
    report = heldout_ar(genome)
    return {"area": text_area(genome, seed=task_seed), "ar": report["ar"], "ns": report["ns"]}


def _random_search(evals: int, seed: int, task_seed: int) -> tuple[float, float]:
    rng = random.Random(seed)
    scores = []
    for _ in range(max(4, evals)):
        vector = [rng.gauss(-0.8, 0.45) for _ in range(len(GENE_NAMES))]
        scores.append(text_area(decode(vector), seed=task_seed))
    scores.sort()
    mid = scores[len(scores) // 2]
    return scores[-1], mid


def _summary(generation: int, scored: list) -> dict:
    reports = [row[2] for row in scored]
    def avg(key: str) -> float:
        return sum(float(report[key]) for report in reports) / len(reports)

    best = scored[0][2]
    return {
        "generation": generation,
        "fitness": avg("fitness"),
        "best_fitness": scored[0][0],
        "birth_frequent": avg("birth_frequent"),
        "birth_rare": avg("birth_rare"),
        "birth_balanced": avg("birth_balanced"),
        "post_area": avg("post_area"),
        "offspring_birth_rare": avg("offspring_birth_rare"),
        "offspring_birth_frequent": avg("offspring_birth_frequent"),
        "best_post_area": best["post_area"],
        "best_birth_balanced": best["birth_balanced"],
        "best_birth_frequent": best["birth_frequent"],
        "best_birth_rare": best["birth_rare"],
    }
