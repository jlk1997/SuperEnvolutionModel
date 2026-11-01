"""The shift-schedule census, with an interval instead of a bare rate."""

from __future__ import annotations

import json
from pathlib import Path

from evo.stats import power_paired, rate_interval
from evo.util import repo_path


def _finished(root: Path) -> list[Path]:
    found = []
    for seed_dir in sorted(root.glob("evolve_census_s*")):
        runs = sorted(path for path in seed_dir.iterdir() if (path / "summary.json").is_file())
        if runs:
            found.append(runs[-1])
    return found


def _morning(summary: dict) -> dict | None:
    for day in reversed(summary.get("days") or []):
        if day.get("after_last_night"):
            return day
    days = [day for day in (summary.get("days") or []) if day.get("exam")]
    return days[-1] if days else None


def _rate_flags(cell: dict) -> list[bool]:
    items = cell.get("items") or []
    if items:
        return [bool(item.get("ok")) for item in items]
    rate = cell.get("rate")
    if rate is None:
        return []
    # Older logs stored only the rate. Six items is the census paper size.
    n = 6
    wins = int(round(float(rate) * n))
    wins = max(0, min(n, wins))
    return [True] * wins + [False] * (n - wins)


def write_baseline(path: Path | None = None) -> dict:
    root = repo_path("runs")
    rows = []
    interrupted = []
    for seed_dir in sorted(root.glob("evolve_census_s*")):
        done = [item for item in seed_dir.iterdir() if (item / "summary.json").is_file()]
        partial = [item for item in seed_dir.iterdir() if item.is_dir() and not (item / "summary.json").is_file()]
        for item in partial:
            interrupted.append(str(item))
        if not done:
            continue
        summary = json.loads((done[-1] / "summary.json").read_text(encoding="utf-8"))
        morning = _morning(summary) or {}
        exam = morning.get("exam") or {}
        evolved = _rate_flags(exam.get("evolved") or {})
        agent = _rate_flags(exam.get("agent") or {})
        census = None
        for day in reversed(summary.get("days") or []):
            if day.get("census") and not day.get("after_last_night"):
                census = day["census"]
                break
        rows.append(
            {
                "run": str(done[-1]),
                "seed": summary.get("days", [{}]) and _seed_of(done[-1]),
                "evolved": rate_interval(evolved, seed=len(rows)),
                "agent": rate_interval(agent, seed=len(rows) + 10),
                "evolved_tokens": (exam.get("evolved") or {}).get("tokens"),
                "agent_tokens": (exam.get("agent") or {}).get("tokens"),
                "census": (census or {}).get("actors"),
            }
        )
    power = power_paired(0.67, 0.33, n=6, sims=200, alpha_boots=150, seed=0)
    payload = {
        "finished": rows,
        "interrupted": interrupted,
        "power_n6": power,
        "note": (
            "Seed 0 of the original census is the finished baseline. "
            "The 13:45 rerun of seed 0 was a duplicate and is not resumed. "
            "Seeds 1 and 2 are included here only once each has a summary.json."
        ),
    }
    dest = path or (repo_path("docs") / "BASELINE_V1.md")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(_markdown(payload), encoding="utf-8")
    return payload


def _seed_of(path: Path) -> str:
    for part in path.parts:
        if part.startswith("evolve_census_s"):
            return part.replace("evolve_census_s", "")
    return "?"


def _markdown(payload: dict) -> str:
    power = payload["power_n6"]
    lines = [
        "# 倒班基线 v1",
        "",
        payload["note"],
        "",
        f"每天 6 道题、成功率 0.67 对 0.33 时，配对区间落在 0 以上的功效约为 {power['power']:.2f}（{power['sims']} 次模拟）。这张纸本身分不出胜负，所以后面的考卷要更长，并且每题都留着对错。",
        "",
        "| 种子 | 进化模型 | 区间 | agent | 区间 | 进化用字 | agent 用字 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    if not payload["finished"]:
        lines.append("| 无 |  |  |  |  |  |  |")
    for row in payload["finished"]:
        evolved = row["evolved"]
        agent = row["agent"]
        lines.append(
            f"| {row['seed']} | {evolved['rate']} | [{evolved['low']}, {evolved['high']}] | "
            f"{agent['rate']} | [{agent['low']}, {agent['high']}] | {row['evolved_tokens']} | {row['agent_tokens']} |"
        )
    if payload["interrupted"]:
        lines.append("")
        lines.append("这些目录没有 summary.json，不进入基线：")
        for item in payload["interrupted"]:
            lines.append(f"- `{item}`")
    lines.append("")
    return "\n".join(lines)
