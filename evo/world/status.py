"""Read a run while it is still going. The census log is the scoreboard."""

from __future__ import annotations

import json
from pathlib import Path


def latest_metrics(root: Path) -> Path | None:
    files = [path for path in root.glob("**/metrics.jsonl") if path.is_file()]
    if not files:
        return None
    return max(files, key=lambda path: path.stat().st_mtime)


def format_events(rows: list[dict]) -> str:
    lines = []
    for row in rows:
        event = row.get("event")
        if event == "day0":
            lines.append(
                f"[day0] agent={row.get('agent_rate')} base={row.get('base_rate')} difficulty={row.get('difficulty')}"
            )
        elif event == "night":
            lines.append(
                f"[night] day={row.get('day')} keep={row.get('keep')} "
                f"gate {row.get('gate_before')}->{row.get('gate_after')} "
                f"chain={row.get('chain_gate')} reject={row.get('reject')}"
            )
        elif event == "census":
            report = row.get("report") or {}
            evolved = report.get("evolved") or {}
            agent = report.get("agent") or {}
            lines.append(
                f"[census] day={row.get('day')} n={row.get('n')} "
                f"evolved alive={evolved.get('alive')} forgotten={evolved.get('forgotten')} "
                f"mastery={evolved.get('mastery')} tokens={evolved.get('tokens_per_ok')} "
                f"agent alive={agent.get('alive')} tokens={agent.get('tokens_per_ok')}"
            )
        elif event == "day":
            exam = row.get("exam") or {}
            evolved = (exam.get("evolved") or {}).get("rate")
            agent = (exam.get("agent") or {}).get("rate")
            lines.append(
                f"[day] day={row.get('day')} evolved={evolved} agent={agent} "
                f"rolled_back={row.get('rolled_back')} reject={row.get('reject')} route={row.get('route')}"
            )
        elif event == "morning":
            exam = row.get("exam") or {}
            lines.append(
                f"[morning] evolved={(exam.get('evolved') or {}).get('rate')} "
                f"agent={(exam.get('agent') or {}).get('rate')} chain={row.get('chain')}"
            )
        elif event == "done":
            lines.append(f"[done] {row.get('run')}")
        elif event == "joint_adapters":
            lines.append(f"[joint] ok={row.get('ok')}")
    return "\n".join(lines) if lines else "[status] no scored events yet"


def read_status(path: Path) -> str:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    header = f"[status] {path.parent.name}  {path.parent.parent.name}"
    body = format_events(rows)
    return header + "\n" + body
