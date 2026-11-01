"""Read a run that is still going and print the score so far."""

from __future__ import annotations

import json
from pathlib import Path


def format_events(rows: list[dict]) -> str:
    lines = []
    for row in rows:
        event = row.get("event")
        if event == "day0":
            lines.append(
                f"[day0] agent={row.get('agent_rate')} base={row.get('base_rate')} "
                f"difficulty={row.get('difficulty')}"
            )
        elif event == "night":
            lines.append(
                f"[night] day={row.get('day')} keep={row.get('keep')} "
                f"gate={row.get('gate_before')}->{row.get('gate_after')} "
                f"chain={row.get('chain_gate')} reject={row.get('reject')}"
            )
        elif event == "census":
            report = row.get("report") or {}
            evolved = report.get("evolved") or {}
            agent = report.get("agent") or {}
            lines.append(
                f"[census] day={row.get('day')} n={row.get('n')} "
                f"evolved_alive={evolved.get('alive')} forgotten={evolved.get('forgotten')} "
                f"mastery={evolved.get('mastery')} tokens={evolved.get('tokens_per_ok')} "
                f"agent_alive={agent.get('alive')}"
            )
        elif event == "day":
            exam = row.get("exam") or {}
            evolved = (exam.get("evolved") or {}).get("rate")
            agent = (exam.get("agent") or {}).get("rate")
            base = (exam.get("base") or {}).get("rate")
            lines.append(
                f"[day] day={row.get('day')} base={base} agent={agent} evolved={evolved} "
                f"rolled_back={row.get('rolled_back')} reject={row.get('reject')} "
                f"inventions={row.get('inventions')}"
            )
        elif event == "morning":
            exam = row.get("exam") or {}
            evolved = (exam.get("evolved") or {}).get("rate")
            agent = (exam.get("agent") or {}).get("rate")
            lines.append(f"[morning] evolved={evolved} agent={agent} chain={row.get('chain')}")
        elif event == "done":
            lines.append(f"[done] {row.get('run')}")
        elif event == "joint_adapters":
            lines.append(f"[joint] ok={row.get('ok')}")
    return "\n".join(lines) if lines else "[status] no scored events yet"


def latest_metrics(root: Path) -> Path | None:
    files = [path for path in root.glob("**/metrics.jsonl") if path.is_file()]
    if not files:
        return None
    return max(files, key=lambda path: path.stat().st_mtime)


def load_events(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def status_text(root: Path, run: str | None = None) -> str:
    if run:
        path = Path(run)
        if path.is_dir():
            path = path / "metrics.jsonl"
    else:
        path = latest_metrics(root)
    if path is None or not path.is_file():
        return "[status] no run yet"
    text = format_events(load_events(path))
    return f"[status] {path.parent}\n{text}"
