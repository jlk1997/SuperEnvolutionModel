"""Checker health: the hidden solution passes, and doing nothing or the wrong thing fails."""

from __future__ import annotations

import tempfile
from pathlib import Path

from evo.computer.actions import format_call
from evo.computer.episode import run_episode, scripted_reply
from evo.computer.license import License
from evo.office.families import FAMILIES, make_task, vandal_reply
from evo.office.packs import DEV_PACKS


def _license() -> License:
    return License(grants={"python", "shell", "read", "write", "http"}, max_steps=8, timeout=8)


def _run(task: dict, reply) -> bool:
    with tempfile.TemporaryDirectory(prefix="evo-office-") as folder:
        result = run_episode(task, reply, Path(folder), _license())
    return bool(result["ok"])


def health_one(pack: dict, family: str, variant: int = 0, seed: int = 0, drift: str | None = None) -> dict:
    task = make_task(pack, family, seed, variant=variant, difficulty=1, drift=drift)
    reference = _run(task, scripted_reply(task["calls"]))
    empty = make_task(pack, family, seed, variant=variant, difficulty=1, drift=drift)
    noop = _run(empty, lambda _messages: format_call("finish", {"answer": "skip"}))
    bad = make_task(pack, family, seed, variant=variant, difficulty=1, drift=drift)
    vandal = _run(bad, vandal_reply(bad))
    return {
        "family": family,
        "variant": variant,
        "drift": drift,
        "reference": reference,
        "noop_fails": not noop,
        "vandal_fails": not vandal,
        "ok": reference and not noop and not vandal,
    }


def health_report(seed: int = 0) -> dict:
    rows = []
    pack = DEV_PACKS[0]
    for family in FAMILIES:
        variants = (0, 1) if family in ("table", "file", "report") else (0,)
        for variant in variants:
            rows.append(health_one(pack, family, variant, seed))
    rows.append(health_one(pack, "http", 0, seed, drift="paginate"))
    rows.append(health_one(pack, "http", 0, seed, drift="rename"))
    return {"ok": all(row["ok"] for row in rows), "rows": rows}
