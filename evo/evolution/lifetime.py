"""One life, scored for selection. The task seed is shared across the population."""

from __future__ import annotations

from evo.bench.families import build_catalog, families_in, sample_stream, split_catalog
from evo.bench.lifetime_eval import evaluate_sequence
from evo.bench.metrics import learning_curve_area
from evo.evolution.genome import CLUSTERS, GENE_NAMES, Genome, decode, logit
from evo.plastic.learner import PlasticLearner


ARITH_REPEATS = 4
ARITH_EPISODES = 3
LOGIC_EPISODES = 2
INNATE_COST = 0.08


def catalog(seed: int = 0):
    families = build_catalog(seed=seed)
    return split_catalog(families)


def shared_tasks(n: int, seed: int):
    train, held = catalog()
    return sample_stream(train + held, n, seed)


def lifetime_fitness(genome: Genome, mode: str, seed: int = 0) -> dict:
    """Baldwin learns. Darwin is scored at birth. Lamarck learns, then writes into innate genes."""
    if mode not in {"baldwin", "darwin", "lamarck"}:
        raise ValueError(mode)
    train, held = catalog(0)
    arith = families_in(train, "arith", heldout=False)[:ARITH_REPEATS]
    logic = families_in(train, "logic", heldout=False)[:1]
    learner = PlasticLearner(genome)
    total = 0.0
    count = 0

    def block(family, cluster: str, episodes: int) -> None:
        nonlocal total, count
        for _ in range(episodes):
            total += learner.readiness(family.id, cluster)
            count += 1
            if mode != "darwin":
                learner.learn(family.id, cluster)

    for family in arith:
        block(family, "arith", ARITH_EPISODES)
    for family in logic:
        block(family, "logic", LOGIC_EPISODES)
    mean_p = total / count if count else 0.0
    cost = INNATE_COST * sum(genome.unit(f"innate.{cluster}") ** 2 for cluster in CLUSTERS)
    inherited = assimilate(genome, learner) if mode == "lamarck" else genome
    probe_family = families_in(held, "arith", heldout=True)[0]
    probe = PlasticLearner(genome)
    probe_curve, _needed = probe.practice(probe_family.id, "arith", budget=6)
    return {
        "fitness": mean_p - cost,
        "mean_p": mean_p,
        "cost": cost,
        "birth_frequent": genome.innate("arith"),
        "birth_rare": genome.innate("logic"),
        "birth_balanced": sum(genome.innate(cluster) for cluster in CLUSTERS) / len(CLUSTERS),
        "post_area": learning_curve_area(probe_curve),
        "offspring_birth_rare": inherited.innate("logic"),
        "offspring_birth_frequent": inherited.innate("arith"),
        "lamarck_vector": inherited.vector,
        "mode": mode,
        "seed": seed,
    }


def assimilate(genome: Genome, learner: PlasticLearner) -> Genome:
    """Copy practiced cluster skill into the innate genes. Baldwin does not call this."""
    vector = list(genome.vector)
    for cluster in CLUSTERS:
        learned = float(learner.cluster.get(cluster, 0.0))
        target = min(0.74, max(genome.innate(cluster), learned * 0.85))
        unit = min(0.98, max(0.02, target / 0.75))
        index = GENE_NAMES.index(f"innate.{cluster}")
        vector[index] = max(vector[index], logit(unit))
    return decode(vector)


def text_family_ids(seed: int, n: int = 4) -> list[str]:
    """Family order for one shared stream. Same seed, same order, for every individual."""
    import random

    train, _held = catalog(0)
    families = families_in(train, "text", heldout=False)
    rng = random.Random(seed)
    rng.shuffle(families)
    return [family.id for family in families[:n]]


def text_area(genome: Genome, budget: int = 3, gain: float = 1.0, seed: int = 0) -> float:
    """Smooth fitness for the strategy: a short life on the shared text stream."""
    train, _held = catalog(0)
    by_id = {family.id: family for family in families_in(train, "text", heldout=False)}
    families = [by_id[family_id] for family_id in text_family_ids(seed) if family_id in by_id]
    report = evaluate_sequence(genome, families, budget=budget, gain=gain)
    # Birth level is not a learning gain. Unused sites pay a small plasticity cost,
    # so a text life is pushed onto the delta site rather than every site at once.
    birth = report["curves"][0][0] if report["curves"] else 0.0
    unused = genome.site_strength("attn", "mid") + genome.site_strength("mlp", "mid")
    return float(report["area"] - birth - 0.05 * unused)


def heldout_ar(genome: Genome, cluster: str = "text", budget: int = 8, gain: float = 1.0) -> dict:
    _train, held = catalog(0)
    families = families_in(held, cluster, heldout=True)[:5]
    report = evaluate_sequence(genome, families, budget=budget, gain=gain)
    return {"ar": report["ar"], "ns": report["ns"], "ei": report["ei"], "area": report["area"]}
