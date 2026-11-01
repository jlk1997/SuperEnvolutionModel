"""The plasticity genome. Evolution searches this vector, not the base weights.

Fifty-odd genes: a learning rate for every layer-group, site, and timescale,
an allocation and an innate value per task cluster, and the memory genes that
gate fast state, replay, and consolidation.
"""

from __future__ import annotations

import math


LAYER_GROUPS = ("early", "mid", "late", "last")
SITES = ("attn", "delta", "mlp")
SCALES = ("fast", "mid", "slow")
CLUSTERS = ("arith", "text", "list", "logic")
PRIMARY_SITE = {"arith": "attn", "text": "delta", "list": "mlp", "logic": "attn"}

MEM_GENES = (
    "carry",
    "carry_decay",
    "consolidate_after",
    "replay_ratio",
    "kl_anchor",
    "write_after",
    "birth_scale",
    "fast_mix",
    "mid_mix",
    "slow_mix",
    "surprise_gate",
    "forget_penalty",
)


def gene_names() -> list[str]:
    names = [f"lr.{group}.{site}.{scale}" for group in LAYER_GROUPS for site in SITES for scale in SCALES]
    for cluster in CLUSTERS:
        names.append(f"alloc.{cluster}")
        names.append(f"innate.{cluster}")
    names.extend(f"mem.{name}" for name in MEM_GENES)
    return names


GENE_NAMES = gene_names()


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(value)))


def sigmoid(value: float) -> float:
    if value >= 12:
        return 1.0
    if value <= -12:
        return 0.0
    return 1.0 / (1.0 + math.exp(-value))


def logit(unit: float) -> float:
    clipped = min(0.999, max(0.001, float(unit)))
    return math.log(clipped / (1.0 - clipped))


class Genome:
    """One decoded individual. `vector` is what the evolutionary strategy updates."""

    def __init__(self, vector: list[float]):
        if len(vector) != len(GENE_NAMES):
            raise ValueError(f"genome length {len(vector)} != {len(GENE_NAMES)}")
        self.vector = [float(value) for value in vector]
        self.values = dict(zip(GENE_NAMES, self.vector))

    def logit_of(self, name: str) -> float:
        return self.values[name]

    def unit(self, name: str) -> float:
        return sigmoid(self.values[name])

    def site_strength(self, site: str, scale: str) -> float:
        """Last-group gene carries most of the gradient. The earlier groups still count.

        One coordinate has to be able to move the site, or a 4-way average
        dilutes the evolutionary signal until the map looks flat.
        """
        last = self.unit(f"lr.last.{site}.{scale}")
        earlier = [self.unit(f"lr.{group}.{site}.{scale}") for group in LAYER_GROUPS if group != "last"]
        return 0.75 * last + 0.25 * (sum(earlier) / len(earlier))

    def cluster_alpha(self, cluster: str, scale: str) -> float:
        """Step size for one cluster at one timescale. Expressed genes only."""
        site = PRIMARY_SITE[cluster]
        strength = self.site_strength(site, scale)
        alloc = self.unit(f"alloc.{cluster}")
        mix = self.unit(f"mem.{scale}_mix")
        scale_v = 0.02 + 0.45 * mix
        alpha = scale_v * (0.2 + 0.8 * alloc) * (0.2 + 0.8 * strength)
        if scale == "mid":
            alpha *= 1.0 - 0.5 * self.unit("mem.kl_anchor")
        if scale == "slow":
            alpha *= 0.3 + 0.7 * self.unit("mem.replay_ratio")
        return alpha

    def innate(self, cluster: str) -> float:
        """Birth competence on a cluster, in [0, 0.75]. Learning is not included."""
        return 0.75 * self.unit(f"innate.{cluster}")

    def write_after(self) -> int:
        return 1 + int(self.unit("mem.write_after") * 7)

    def plasticity_map(self) -> dict[str, float]:
        return {site: self.site_strength(site, "mid") for site in SITES}


def decode(vector: list[float]) -> Genome:
    return Genome(vector)


def make_vector(default: float = 0.0, **named: float) -> list[float]:
    vector = [float(default)] * len(GENE_NAMES)
    index = {name: pos for pos, name in enumerate(GENE_NAMES)}
    for name, value in named.items():
        if name not in index:
            raise KeyError(name)
        vector[index[name]] = float(value)
    return vector


def _fill(vector: list[float], predicate, value: float) -> list[float]:
    out = list(vector)
    for pos, name in enumerate(GENE_NAMES):
        if predicate(name):
            out[pos] = float(value)
    return out


def hand_vector() -> list[float]:
    """A moderate learner. Plasticity is real, birth competence is low, fast state is off."""
    vector = make_vector(-1.2)
    vector = _fill(vector, lambda name: name.startswith("lr.") and (name.endswith(".mid") or name.endswith(".slow")), 0.6)
    vector = _fill(vector, lambda name: name.startswith("alloc."), 0.6)
    for name, value in (
        ("mem.mid_mix", 0.8),
        ("mem.slow_mix", 0.8),
        ("mem.fast_mix", -1.0),
        ("mem.birth_scale", 0.8),
        ("mem.replay_ratio", 0.5),
        ("mem.carry", -2.0),
        ("mem.forget_penalty", -2.0),
        ("mem.kl_anchor", -1.5),
    ):
        vector[GENE_NAMES.index(name)] = value
    return _fill(vector, lambda name: name.startswith("innate."), -1.6)


def weak_vector() -> list[float]:
    """Little plasticity and little innate skill. Evolution has to earn both."""
    vector = make_vector(-0.8)
    vector = _fill(vector, lambda name: name.startswith("innate."), -1.8)
    vector[GENE_NAMES.index("mem.forget_penalty")] = -1.5
    vector[GENE_NAMES.index("mem.kl_anchor")] = -1.0
    return vector


def fit_vector() -> list[float]:
    """Where a real Qwen3.5 LoRA should write.

    A one-step probe on this base moved the loss through the MLP, less through
    DeltaNet, and barely through attention. Attention stays under the floor.
    """
    vector = make_vector(-2.0)
    vector = _fill(vector, lambda name: ".mlp." in name and (name.endswith(".mid") or name.endswith(".slow")), 2.2)
    vector = _fill(vector, lambda name: ".delta." in name and name.endswith(".mid"), 1.4)
    vector[GENE_NAMES.index("mem.mid_mix")] = 1.2
    vector[GENE_NAMES.index("mem.slow_mix")] = 0.4
    vector[GENE_NAMES.index("mem.replay_ratio")] = 1.5
    vector[GENE_NAMES.index("mem.kl_anchor")] = -2.0
    vector[GENE_NAMES.index("mem.carry")] = -2.0
    return vector


def icl_vector() -> list[float]:
    """Fast state inside one family, no slow transfer. The in-context baseline."""
    vector = make_vector(-3.5)
    vector = _fill(vector, lambda name: name.startswith("innate."), -1.6)
    vector[GENE_NAMES.index("mem.carry")] = 2.5
    vector[GENE_NAMES.index("mem.carry_decay")] = 2.0
    vector[GENE_NAMES.index("mem.fast_mix")] = 1.5
    return vector


def layer_group(index: int, n_layers: int) -> str:
    if n_layers <= 0:
        raise ValueError("n_layers must be positive")
    bucket = min(len(LAYER_GROUPS) - 1, int(index * len(LAYER_GROUPS) / n_layers))
    return LAYER_GROUPS[bucket]
