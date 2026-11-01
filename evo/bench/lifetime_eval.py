"""Run one genome through a sequence of families and score the life."""

from __future__ import annotations

from evo.bench.families import Family
from evo.bench.metrics import acceleration_ratio, evolution_index, forgetting, learning_curve_area
from evo.evolution.genome import Genome
from evo.plastic.learner import PlasticLearner


def evaluate_sequence(
    genome: Genome,
    families: list[Family],
    budget: int = 8,
    criterion: float = 0.6,
    gain: float = 1.0,
) -> dict:
    learner = PlasticLearner(genome, gain=gain)
    curves = []
    counts = []
    for family in families:
        curve, needed = learner.practice(family.id, family.cluster, budget, criterion)
        curves.append(curve)
        counts.append(needed)
    areas = [learning_curve_area(curve) for curve in curves]
    later = counts[-1] if counts else 0
    first = counts[0] if counts else 0
    return {
        "ns": counts,
        "curves": curves,
        "areas": areas,
        "area": sum(areas) / len(areas) if areas else 0.0,
        "ar": acceleration_ratio(first, later) if counts else 1.0,
        "ei": evolution_index([float(value) for value in counts]),
        "start": curves[0][0] if curves else 0.0,
        "end": curves[-1][-1] if curves else 0.0,
    }


def measure_forgetting(genome: Genome, anchor: Family, distractors: list[Family], budget: int = 6) -> dict:
    """Durable competence on `anchor` before and after a run of other families."""
    learner = PlasticLearner(genome)
    learner.practice(anchor.id, anchor.cluster, budget)
    before = learner.readiness(anchor.id, anchor.cluster, fast=False)
    for family in distractors:
        learner.practice(family.id, family.cluster, max(2, budget // 2))
    after = learner.readiness(anchor.id, anchor.cluster, fast=False)
    return {"before": before, "after": after, "forgetting": forgetting(before, after)}
