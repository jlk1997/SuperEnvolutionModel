"""Shadow, assist, and auto on a folder. Shadow never changes the folder.

Frozen. The plasticity-evolution line does not extend this module.
"""

from __future__ import annotations

import json
from pathlib import Path

from evo.computer.actions import Call, format_call
from evo.computer.episode import run_episode
from evo.computer.license import License


def run_pilot(folder: Path, tasks: list[dict], reply, mode: str, confirm=None, auto_families: set[str] | None = None, on_event=None) -> dict:
    folder.mkdir(parents=True, exist_ok=True)
    before = _snapshot(folder)
    license = License(
        grants={"python", "shell", "read", "write", "http"},
        mode=mode,
        auto_families=auto_families or set(),
        confirm=confirm,
        max_steps=4,
    )
    audit = folder / "audit.jsonl"
    results = []
    for task in tasks:
        results.append(run_episode(task, reply, folder, license, audit_path=audit, on_event=on_event))
    after = _snapshot(folder)
    changed = sorted(set(before) ^ set(after) | {name for name in before if before.get(name) != after.get(name)})
    changed = [name for name in changed if name != "audit.jsonl"]
    return {
        "mode": mode,
        "ok": [row["ok"] for row in results],
        "changed": changed,
        "audit": audit.is_file(),
    }


def apply_feedback(verdict: str) -> str:
    """accept keeps the trace, reject drops it, correct asks for another attempt."""
    if verdict not in ("accept", "reject", "correct"):
        raise ValueError(verdict)
    return verdict


def demo(root: Path | None = None) -> dict:
    """A synthetic folder, not the user's real files."""
    import tempfile

    base = Path(root) if root else Path(tempfile.mkdtemp(prefix="evo-pilot-"))
    base.mkdir(parents=True, exist_ok=True)
    (base / "book.csv").write_text("amount,status\n10,paid\n", encoding="utf-8")
    task = {
        "id": "pilot-write",
        "family": "report",
        "prompt": "Write out.txt",
        "setup": None,
        "check": lambda workspace: (workspace / "out.txt").is_file(),
        "calls": [],
    }

    def write_reply(_messages):
        return format_call("write_file", {"path": "out.txt", "text": "done\n"})

    shadow = run_pilot(base / "shadow", [{**task, "setup": _seed}], write_reply, "shadow")
    assist = run_pilot(base / "assist", [{**task, "setup": _seed}], write_reply, "assist")
    auto = run_pilot(
        base / "auto",
        [{**task, "family": "report", "setup": _seed}],
        write_reply,
        "auto",
        auto_families={"table"},
    )
    return {"root": str(base), "shadow_changed": shadow["changed"], "assist_changed": assist["changed"], "auto_ok": auto["ok"], "feedback": apply_feedback("reject")}


def _seed(workspace: Path) -> None:
    (workspace / "book.csv").write_text("amount,status\n10,paid\n", encoding="utf-8")


def _snapshot(folder: Path) -> dict[str, str]:
    rows = {}
    for path in folder.rglob("*"):
        if path.is_file():
            rows[str(path.relative_to(folder))] = path.read_text(encoding="utf-8", errors="replace")
    return rows
