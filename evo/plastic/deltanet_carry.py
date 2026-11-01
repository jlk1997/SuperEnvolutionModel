"""Fast state carried across episodes. No gradient.

Numeric state is decayed and mixed, which is what the tests and the reference
organism's fast gene correspond to. A transformer cache is kept or dropped:
the model applies its own decay. The carry gene decides whether it is kept.
"""

from __future__ import annotations

from evo.evolution.genome import Genome


class StateCarry:
    def __init__(self, carry: float, decay: float):
        self.carry = float(carry)
        self.decay = float(decay)
        self._state = None

    def reset(self) -> None:
        self._state = None

    def remember(self, state) -> None:
        if self.carry <= 0.0 or state is None:
            self._state = None
            return
        decayed = _decay(state, self.decay)
        if isinstance(decayed, list) and isinstance(self._state, list) and len(self._state) == len(decayed):
            self._state = [
                (1.0 - self.carry) * old + self.carry * new for old, new in zip(self._state, decayed)
            ]
            return
        self._state = decayed

    def recall(self):
        if self.carry <= 0.0:
            return None
        return self._state


def carry_from_genome(genome: Genome) -> StateCarry:
    rate = genome.unit("mem.carry")
    if rate < 0.02:
        rate = 0.0
    decay = 0.5 + 0.5 * genome.unit("mem.carry_decay")
    return StateCarry(rate, decay)


def _decay(state, decay: float):
    if isinstance(state, (list, tuple)) and state and isinstance(state[0], (int, float)):
        return [float(value) * float(decay) for value in state]
    return state


def absorb_forward(evo, text: str, carry: StateCarry, adapter: str | None) -> dict:
    """One no-grad forward. The cache is stored only when the carry gene is on."""
    if carry.carry <= 0.0 or not str(text).strip():
        carry.reset()
        return {"absorbed": False}
    import torch

    from evo.model import activate

    tok = evo.tok
    encoded = tok(text, return_tensors="pt", add_special_tokens=False, truncation=True, max_length=256)
    encoded = {key: value.to(evo.device) for key, value in encoded.items()}
    evo.model.eval()
    with torch.no_grad(), activate(evo.model, adapter):
        first = evo.model(**encoded, use_cache=True)
    cache = getattr(first, "past_key_values", None)
    carry.remember(cache)
    return {"absorbed": cache is not None}
