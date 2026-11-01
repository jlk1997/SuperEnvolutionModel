"""Day writes, night sleep, and the morning report. Decisions do not require a model."""

from __future__ import annotations


def day_ready(counts: dict[str, int], family: str, needed: int) -> bool:
    return int(counts.get(family, 0)) >= int(needed) and int(needed) > 0


def sleep_pressure(state: dict) -> str | None:
    """Why the night should start, or None while the day continues."""
    if int(state.get("day_steps", 0)) >= int(state.get("day_budget", 10**9)):
        return "budget"
    if state.get("drift"):
        return "drift"
    if state.get("idle"):
        return "idle"
    if state.get("shift_end"):
        return "shift_end"
    return None


def interleave(fresh: list, old: list) -> list:
    """New, then old, so the night does not end on only the latest job."""
    rows = []
    length = max(len(fresh), len(old))
    for index in range(length):
        if index < len(fresh):
            rows.append(fresh[index])
        if index < len(old):
            rows.append(old[index])
    return rows


def morning_report(commits: list[dict], rollbacks: list[dict]) -> str:
    lines = ["Morning report"]
    if not commits and not rollbacks:
        lines.append("No weight changes.")
    for row in commits:
        lines.append(f"kept {row.get('name')} -> {row.get('dest')} ({row.get('why', '')})")
    for row in rollbacks:
        lines.append(f"rolled back {row.get('name')}: {row.get('why', '')}")
    lines.append("Reply rollback:<name> to undo one kept change.")
    return "\n".join(lines)


def morning_card(commits: list[dict], rollbacks: list[dict]) -> dict:
    """Structured morning. `text` is the same view the command line prints."""
    return {
        "text": morning_report(commits, rollbacks),
        "commits": [dict(row) for row in commits],
        "rollbacks": [dict(row) for row in rollbacks],
    }


def apply_rollback(commits: list[dict], name: str) -> list[dict]:
    return [row for row in commits if row.get("name") != name]
