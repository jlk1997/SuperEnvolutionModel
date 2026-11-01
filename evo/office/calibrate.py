"""Find a difficulty where the frozen agent is neither helpless nor already done."""

from __future__ import annotations

import tempfile
from pathlib import Path

from evo.computer.episode import run_episode
from evo.office.families import make_task
from evo.office.judge import choose_difficulty
from evo.office.packs import DEV_PACKS
from evo.office.stream import _license, _model_reply, _notes


def calibrate(evo, cfg: dict) -> dict:
    levels = [int(level) for level in (cfg.get("calibrate_levels") or [1, 3, 5])]
    per = int(cfg.get("calibrate_items", 4))
    rates = {}
    for level in levels:
        flags = []
        for index in range(per):
            task = make_task(DEV_PACKS[0], "table", 8000 + index, variant=0, difficulty=level)
            notes = _notes("agent", task)
            if notes:
                task["prompt"] = task["prompt"] + "\n\n" + notes
            with tempfile.TemporaryDirectory(prefix="evo-cal-") as folder:
                result = run_episode(task, _model_reply(evo, cfg, "policy"), Path(folder), _license(cfg))
            flags.append(1.0 if result["ok"] else 0.0)
        rates[level] = sum(flags) / len(flags) if flags else 0.0
    choice = choose_difficulty(rates)
    choice["rates"] = {str(level): rate for level, rate in rates.items()}
    return choice
