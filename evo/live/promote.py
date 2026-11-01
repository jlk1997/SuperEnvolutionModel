"""Where a verified success is allowed to go.

One success stays in the fast state. Repeated successes may enter the skill
adapter. Only a skill that later exams still pass may touch the slow core.
A drift wipes that tool back to the bottom.
"""

from __future__ import annotations


DEFAULT_LADDER = {
    "slot_after": 2,
    "core_holds": 1,
}


class Ledger:
    def __init__(self):
        self.verified: dict[str, int] = {}
        self.holds: dict[str, int] = {}
        self.cross: dict[str, int] = {}
        self.in_slot: set[str] = set()

    def note_practice(self, tools: list[str], ok: bool) -> None:
        if not ok:
            return
        for name in tools:
            self.verified[name] = self.verified.get(name, 0) + 1

    def note_exam(self, tools: list[str], ok: bool) -> None:
        for name in tools:
            if name not in self.in_slot:
                continue
            if ok:
                self.holds[name] = self.holds.get(name, 0) + 1
            else:
                self.holds[name] = 0

    def note_cross(self, tools: list[str], ok: bool) -> None:
        """A skill that also helps another pack. Required only when the ladder sets cross_holds."""
        for name in tools:
            if ok:
                self.cross[name] = self.cross.get(name, 0) + 1
            else:
                self.cross[name] = 0

    def mark_slot(self, tools: list[str]) -> None:
        for name in tools:
            self.in_slot.add(name)

    def forget(self, name: str) -> None:
        self.verified.pop(name, None)
        self.holds.pop(name, None)
        self.cross.pop(name, None)
        self.in_slot.discard(name)

    def destination(self, tools: list[str], ladder: dict | None = None) -> str:
        """`fast` does not run the optimizer. `slot` and `core` do."""
        rules = dict(DEFAULT_LADDER)
        if ladder:
            rules.update(ladder)
        if not tools:
            return "fast"
        if all(name in self.in_slot and self.holds.get(name, 0) >= int(rules["core_holds"]) for name in tools):
            need = int(rules.get("cross_holds") or 0)
            if need > 0 and not all(self.cross.get(name, 0) >= need for name in tools):
                return "local"
            return "core"
        if all(self.verified.get(name, 0) >= int(rules["slot_after"]) for name in tools):
            return "slot"
        return "fast"
