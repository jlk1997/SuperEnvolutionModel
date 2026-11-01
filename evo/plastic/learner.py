"""A reference organism whose learning speed is a function of its genome.

This is the mechanistic model the population experiments run on. It is not a
language model. A life is deterministic given the genome, so selection is not
swamped by sampling noise.
"""

from __future__ import annotations

from evo.evolution.genome import CLUSTERS, Genome, clamp


class PlasticLearner:
    def __init__(self, genome: Genome, gain: float = 1.0):
        self.genome = genome
        self.gain = float(gain)
        self.cluster = {name: 0.0 for name in CLUSTERS}
        self.family_comp: dict[str, float] = {}
        self.fast: dict[str, float] = {}
        self.steps = 0

    def readiness(self, family: str, cluster: str, fast: bool = True) -> float:
        value = self.genome.innate(cluster) + self.cluster[cluster] + self.family_comp.get(family, 0.0)
        if fast:
            value += self.fast.get(family, 0.0)
        return clamp(value)

    def learn(self, family: str, cluster: str) -> None:
        mid = min(0.7, self.genome.cluster_alpha(cluster, "mid") * self.gain)
        current = self.family_comp.get(family, 0.0)
        if self.genome.unit("mem.surprise_gate") > 0.85 and self.readiness(family, cluster) > 0.8:
            mid *= 0.3
        self.family_comp[family] = clamp(current + mid * (0.95 - current))
        slow = min(0.55, self.genome.cluster_alpha(cluster, "slow") * self.gain)
        self.cluster[cluster] = clamp(self.cluster[cluster] + slow * (1.0 - self.cluster[cluster]))
        fast_step = 0.35 * self.genome.unit("mem.carry") * (0.3 + 0.7 * self.genome.unit("mem.fast_mix"))
        decay = 0.35 + 0.65 * self.genome.unit("mem.carry_decay")
        self.fast[family] = clamp(self.fast.get(family, 0.0) * decay + fast_step)
        self.steps += 1
        every = 1 + int(self.genome.unit("mem.consolidate_after") * 5)
        if self.steps % every == 0:
            self.cluster[cluster] = clamp(self.cluster[cluster] + 0.04 * slow)
        self._interfere(family, cluster, mid)

    def _interfere(self, family: str, cluster: str, mid: float) -> None:
        rate = min(0.55, 0.3 * self.genome.unit("mem.forget_penalty") * mid)
        if rate <= 0:
            return
        for other, value in list(self.family_comp.items()):
            if other != family:
                self.family_comp[other] = value * (1.0 - rate)
        for other in CLUSTERS:
            if other != cluster:
                self.cluster[other] *= 1.0 - rate

    def practice(self, family: str, cluster: str, budget: int, criterion: float = 0.6) -> tuple[list[float], int]:
        """Curve starts at birth. `n` is the episode count at which competence appears."""
        start = self.readiness(family, cluster)
        curve = [start]
        hit = 0 if start >= criterion else None
        for episode in range(int(budget)):
            self.learn(family, cluster)
            value = self.readiness(family, cluster)
            curve.append(value)
            if hit is None and value >= criterion:
                hit = episode + 1
        if hit is None:
            hit = int(budget)
        return curve, hit
