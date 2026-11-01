"""The knobs a real-model life actually reads, as one evolvable vector.

Each coordinate is a logit. `decode_life` squashes it to [0, 1] and maps it to a
range. The 56-gene reference genome describes a simulator; this one describes
the trainer that writes the LoRA.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass


LIFE_GENES = (
    "mlp_lr",
    "attn_lr",
    "lesson",
    "replay",
    "keep",
    "batch",
    "decay",
    "grow",
    "sleep_every",
    "sleep_passes",
)

BATCHES = (4, 8, 16)
SLEEP_EVERY = (0, 2, 3, 4)
# never: everything in policy. need: a slot when a rule will not fit. always: every new rule starts in its own slot.
GROW = ("never", "need", "always")


@dataclass(frozen=True)
class LifeGenes:
    mlp_lr: float
    attn_lr: float
    lesson: int
    replay: float
    keep: float
    batch: int
    decay: float
    grow: str
    sleep_every: int
    sleep_passes: int

    def lr_at(self, site: str, index: int) -> float:
        """Rate for the `index`-th skill of a life. `decay` above 1 writes later skills harder."""
        base = self.mlp_lr if site == "mlp" else self.attn_lr
        return base * (self.decay ** int(index))

    def as_dict(self) -> dict:
        return asdict(self)


def _sigmoid(value: float) -> float:
    if value >= 0:
        return 1.0 / (1.0 + math.exp(-value))
    exp = math.exp(value)
    return exp / (1.0 + exp)


def _logit(unit: float) -> float:
    unit = min(1.0 - 1e-6, max(1e-6, float(unit)))
    return math.log(unit / (1.0 - unit))


def _pick(options: tuple, unit: float):
    return options[min(len(options) - 1, int(unit * len(options)))]


def decode_life(vector: list[float]) -> LifeGenes:
    if len(vector) != len(LIFE_GENES):
        raise ValueError(f"expected {len(LIFE_GENES)} genes, got {len(vector)}")
    u = {name: _sigmoid(float(value)) for name, value in zip(LIFE_GENES, vector)}
    attn = 0.0 if u["attn_lr"] < 0.4 else 10 ** (-5.0 + 1.5 * (u["attn_lr"] - 0.4) / 0.6)
    return LifeGenes(
        mlp_lr=10 ** (-4.7 + 1.6 * u["mlp_lr"]),
        attn_lr=attn,
        lesson=int(round(4 + 36 * u["lesson"])),
        replay=1.5 * u["replay"],
        keep=0.6 + 0.35 * u["keep"],
        batch=int(_pick(BATCHES, u["batch"])),
        decay=0.5 + u["decay"],
        grow=str(_pick(GROW, u["grow"])),
        sleep_every=int(_pick(SLEEP_EVERY, u["sleep_every"])),
        sleep_passes=int(round(1 + 5 * u["sleep_passes"])),
    )


def encode_units(**units: float) -> list[float]:
    """Logit vector from unit values. Unnamed genes sit at 0.5."""
    unknown = set(units) - set(LIFE_GENES)
    if unknown:
        raise KeyError(sorted(unknown))
    return [_logit(units.get(name, 0.5)) for name in LIFE_GENES]


def with_units(vector: list[float], **units: float) -> list[float]:
    """`vector` with the named genes moved to the given unit positions."""
    unknown = set(units) - set(LIFE_GENES)
    if unknown:
        raise KeyError(sorted(unknown))
    out = list(vector)
    for name, unit in units.items():
        out[LIFE_GENES.index(name)] = _logit(unit)
    return out


def default_vector() -> list[float]:
    """The hand-set trainer: MLP only, about 2e-4, twelve examples, half replay, keep at 0.8."""
    return encode_units(
        mlp_lr=(math.log10(2e-4) + 4.7) / 1.6,
        attn_lr=0.1,
        lesson=(12 - 4) / 36,
        replay=0.5 / 1.5,
        keep=(0.8 - 0.6) / 0.35,
        batch=0.5,
        decay=0.5,
        grow=0.2,
        sleep_every=0.1,
        sleep_passes=0.4,
    )


def grown_vector(mode: str = "need") -> list[float]:
    """The hand-set trainer with growth on and a sleep every second skill."""
    vector = default_vector()
    vector[LIFE_GENES.index("grow")] = _logit((GROW.index(mode) + 0.5) / len(GROW))
    vector[LIFE_GENES.index("sleep_every")] = _logit(0.35)
    return vector
