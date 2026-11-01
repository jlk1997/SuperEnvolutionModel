"""Absorb a repeated workflow only after a measured use is cheaper than rereading.

Until a bare attempt records its real length, the book does not pretend that
using the weights costs nothing.
"""

from __future__ import annotations

from evo.stats import breakeven_uses


class AbsorbBook:
    def __init__(self):
        self.retrieval_tokens: dict[str, float] = {}
        self.train_tokens: dict[str, float] = {}
        self.seen: dict[str, int] = {}
        self.per_use: dict[str, float] = {}

    def note(self, family: str, retrieval_tokens: float, train_tokens: float) -> None:
        self.seen[family] = self.seen.get(family, 0) + 1
        self.retrieval_tokens[family] = float(retrieval_tokens)
        self.train_tokens[family] = float(train_tokens)

    def measure(self, family: str, per_use: float) -> None:
        """Record the length of one bare attempt. Zero is not a measurement."""
        if float(per_use) <= 0:
            return
        self.per_use[family] = float(per_use)

    def decision(self, family: str) -> dict:
        per_read = float(self.retrieval_tokens.get(family, 0))
        train = float(self.train_tokens.get(family, 0))
        per_use = self.per_use.get(family)
        measured = per_use is not None
        seen = int(self.seen.get(family, 0))
        uses = breakeven_uses(train, float(per_use), per_read) if measured else None
        absorb = bool(measured and uses is not None and seen >= uses)
        return {
            "family": family,
            "breakeven_uses": uses,
            "seen": seen,
            "absorb": absorb,
            "measured": measured,
            "per_use": per_use,
        }
