"""Experience the model just had. Exam items are refused."""

from __future__ import annotations

import random


class Episode:
    def __init__(
        self,
        prompt: str,
        code: str,
        ok: bool,
        tools: list[str],
        tick: int,
        split: str,
        surprise: float | None = None,
        expect=None,
        kind: str = "call",
    ):
        self.prompt = prompt
        self.code = code or ""
        self.ok = bool(ok)
        self.tools = list(tools or [])
        self.tick = int(tick)
        self.split = split
        self.expect = expect
        self.kind = kind or "call"
        if surprise is None:
            surprise = 1.0 if not self.ok else 0.1
        self.surprise = float(surprise)

    def as_dict(self) -> dict:
        return {
            "prompt": self.prompt,
            "code": self.code,
            "ok": self.ok,
            "tools": list(self.tools),
            "tick": self.tick,
            "split": self.split,
            "surprise": self.surprise,
        }


class EpisodicBuffer:
    """Recent practice. Failures and fresh items are drawn more often."""

    def __init__(self, limit: int = 64):
        self.limit = limit
        self.rows: list[Episode] = []

    def __len__(self) -> int:
        return len(self.rows)

    def add(self, episode: Episode) -> bool:
        if episode.split == "exam":
            return False
        self.rows.append(episode)
        if len(self.rows) > self.limit:
            self.rows = self.rows[-self.limit :]
        return True

    def successes(self) -> list[Episode]:
        return [row for row in self.rows if row.ok and row.code.strip()]

    def sample(self, n: int, rng: random.Random) -> list[Episode]:
        if n <= 0 or not self.rows:
            return []
        weights = []
        last = max(1, len(self.rows))
        for index, row in enumerate(self.rows):
            recency = (index + 1) / last
            fail = 1.0 if not row.ok else 0.25
            weights.append(recency * (1.0 + row.surprise) * fail)
        picked = []
        pool = list(range(len(self.rows)))
        bag = list(weights)
        for _ in range(min(n, len(pool))):
            total = sum(bag)
            if total <= 0:
                choice = rng.randrange(len(pool))
            else:
                draw = rng.random() * total
                choice = 0
                acc = 0.0
                for index, weight in enumerate(bag):
                    acc += weight
                    if acc >= draw:
                        choice = index
                        break
            picked.append(self.rows[pool.pop(choice)])
            bag.pop(choice)
        return picked

    def exam_leak(self, exam_ids: set[str]) -> list[str]:
        """Training rows whose prompt id is an exam id. The buffer stores no ids; callers pass prompts."""
        leaked = []
        exam_text = {item.strip() for item in exam_ids if item}
        for row in self.rows:
            if row.prompt.strip() in exam_text or row.split == "exam":
                leaked.append(row.prompt)
        return leaked
