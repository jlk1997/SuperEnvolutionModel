"""What survives a base-model swap: verified episodes, not the checkpoint.

Exam items are not part of the identity. A new base replays `replay_pairs`.
"""

from __future__ import annotations

import json
from pathlib import Path


class Identity:
    def __init__(self, gene: dict | None = None):
        self.gene = dict(gene or {})
        self.episodes: list[dict] = []
        self.verified: dict[str, int] = {}
        self.holds: dict[str, int] = {}
        self.in_slot: list[str] = []

    def remember(self, prompt: str, code: str, tools: list[str], split: str) -> bool:
        if split == "exam" or not (code or "").strip():
            return False
        self.episodes.append(
            {"prompt": prompt, "code": code, "tools": list(tools), "split": split}
        )
        return True

    def take(self, ledger) -> None:
        self.verified = dict(ledger.verified)
        self.holds = dict(ledger.holds)
        self.in_slot = sorted(ledger.in_slot)

    def replay_pairs(self) -> list[tuple[str, str]]:
        return [(row["prompt"], row["code"]) for row in self.episodes]

    def pack(self) -> dict:
        return {
            "gene": self.gene,
            "episodes": self.episodes,
            "verified": self.verified,
            "holds": self.holds,
            "in_slot": self.in_slot,
        }

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.pack(), indent=2), encoding="utf-8")


def load_identity(payload: dict) -> Identity:
    ident = Identity(payload.get("gene"))
    for row in payload.get("episodes") or []:
        if row.get("split") == "exam":
            continue
        ident.episodes.append(
            {
                "prompt": row.get("prompt") or "",
                "code": row.get("code") or "",
                "tools": list(row.get("tools") or []),
                "split": row.get("split") or "practice",
            }
        )
    ident.verified = dict(payload.get("verified") or {})
    ident.holds = dict(payload.get("holds") or {})
    ident.in_slot = list(payload.get("in_slot") or [])
    return ident


def carry_card(payload: dict) -> dict:
    """What a new base receives. The checkpoint stays behind. Exams are dropped."""
    raw = list((payload or {}).get("episodes") or [])
    dropped = sum(1 for row in raw if row.get("split") == "exam")
    ident = load_identity(payload or {})
    return {
        "practice": len(ident.replay_pairs()),
        "exams_dropped": dropped,
        "verified": ident.verified,
        "weights": False,
        "note": "换基座只带走验过的练习，不带走检查点。考题不在里面。",
    }
