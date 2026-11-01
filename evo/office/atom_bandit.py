# -*- coding: utf-8 -*-
import random
from dataclasses import dataclass, field
@dataclass
class Bandit:
    epsilon: float = 0.1
    counts: dict = field(default_factory=dict)
    values: dict = field(default_factory=dict)
    def select(self, atoms, rng=None):
        rng = rng or random.Random(0)
        for a in atoms:
            self.counts.setdefault(a,0); self.values.setdefault(a,0.0)
        if rng.random()<self.epsilon: return rng.choice(atoms)
        return max(atoms, key=lambda a: self.values[a])
    def update(self, atom, reward):
        self.counts[atom]=self.counts.get(atom,0)+1
        n=self.counts[atom]; v=self.values.get(atom,0.0)
        self.values[atom]=v+(reward-v)/n
