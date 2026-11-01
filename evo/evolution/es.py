"""OpenAI-ES and a diagonal CMA-ES. Both take a fitness list and move a mean vector.

Higher fitness is better. Task randomness stays outside these classes so a
generation can share one task seed (common random numbers).
"""

from __future__ import annotations

import math
import random


class OpenAIES:
    """Antithetic evolution strategy with centered ranks (Salimans et al.)."""

    def __init__(self, dim: int, sigma: float = 0.5, lr: float = 0.3, seed: int = 0, pop: int = 8, mean: list[float] | None = None):
        self.dim = int(dim)
        self.sigma = float(sigma)
        self.lr = float(lr)
        self.pop = int(pop)
        self.rng = random.Random(seed)
        self.mean = [0.0] * self.dim if mean is None else [float(value) for value in mean]
        if len(self.mean) != self.dim:
            raise ValueError("mean length does not match dim")
        self._noise: list[list[float]] = []

    def ask(self) -> list[list[float]]:
        self._noise = []
        out = []
        for _ in range(self.pop):
            epsilon = [self.rng.gauss(0.0, 1.0) for _ in range(self.dim)]
            self._noise.append(epsilon)
            out.append([value + self.sigma * noise for value, noise in zip(self.mean, epsilon)])
            out.append([value - self.sigma * noise for value, noise in zip(self.mean, epsilon)])
        return out

    def tell(self, scores: list[float]) -> None:
        if len(scores) != 2 * self.pop:
            raise ValueError(f"expected {2 * self.pop} scores, got {len(scores)}")
        order = sorted(range(len(scores)), key=lambda index: scores[index])
        shaped = [0.0] * len(scores)
        span = max(1, len(scores) - 1)
        for rank, index in enumerate(order):
            shaped[index] = rank / span * 2.0 - 1.0
        grad = [0.0] * self.dim
        for pair, epsilon in enumerate(self._noise):
            advantage = shaped[2 * pair] - shaped[2 * pair + 1]
            for dim in range(self.dim):
                grad[dim] += advantage * epsilon[dim]
        # Rank advantage is O(1). Average over the pairs, then step lr * sigma.
        scale = self.lr * self.sigma / float(self.pop)
        self.mean = [value + scale * part for value, part in zip(self.mean, grad)]


class DiagCMA:
    """Diagonal CMA-ES. Variances adapt per coordinate; the full covariance is not stored."""

    def __init__(self, dim: int, sigma: float = 0.5, seed: int = 0, pop: int | None = None, mean: list[float] | None = None):
        self.dim = int(dim)
        self.sigma = float(sigma)
        self.var = [1.0] * self.dim
        self.pop = int(pop or max(6, 4 + int(3 * math.log(self.dim))))
        self.mu = max(1, self.pop // 2)
        self.rng = random.Random(seed)
        self.mean = [0.0] * self.dim if mean is None else [float(value) for value in mean]
        raw = [math.log(self.mu + 0.5) - math.log(index + 1) for index in range(self.mu)]
        total = sum(raw) or 1.0
        self.weights = [weight / total for weight in raw]
        self._samples: list[list[float]] = []
        self._z: list[list[float]] = []

    def ask(self) -> list[list[float]]:
        self._samples = []
        self._z = []
        for _ in range(self.pop):
            noise = [self.rng.gauss(0.0, 1.0) for _ in range(self.dim)]
            sample = [
                self.mean[dim] + self.sigma * math.sqrt(self.var[dim]) * noise[dim] for dim in range(self.dim)
            ]
            self._z.append(noise)
            self._samples.append(sample)
        return self._samples

    def tell(self, scores: list[float]) -> None:
        if len(scores) != len(self._samples):
            raise ValueError("scores do not match the last ask()")
        order = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)
        picked = order[: self.mu]
        new_mean = []
        new_var = []
        rate = 0.25
        for dim in range(self.dim):
            mixed = 0.0
            second = 0.0
            for weight, index in zip(self.weights, picked):
                mixed += weight * self._samples[index][dim]
                second += weight * (self._z[index][dim] ** 2)
            new_mean.append(mixed)
            updated = (1.0 - rate) * self.var[dim] + rate * self.var[dim] * second
            new_var.append(min(8.0, max(0.05, updated)))
        self.mean = new_mean
        self.var = new_var
        self.sigma = max(0.05, self.sigma * 0.985)
