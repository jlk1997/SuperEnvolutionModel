"""Multi-seed evolution runs and the comparison across stations."""

from __future__ import annotations

import json

from evo.phase4 import run_phase4
from evo.util import repo_path
from evo.world.census import later_faster, rollback_rates
from evo.world.pixels import vision_status


def run_evolve(cfg: dict) -> dict:
    stages = cfg.get("stages")
    if stages:
        reports = []
        for stage in stages:
            from evo.util import load_config

            reports.append(run_evolve(load_config(stage)))
        summary = {"stages": reports, "vision": vision_status()}
        path = repo_path("runs") / "evolve_report.json"
        path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
        print(f"[evolve] wrote {path}", flush=True)
        return summary
    seeds = list(cfg.get("seeds") or [cfg.get("seed", 0)])
    runs = []
    for seed in seeds:
        one = dict(cfg)
        one["seed"] = int(seed)
        one["run_name"] = f"{cfg.get('run_name', 'evolve')}_s{seed}"
        one.pop("seeds", None)
        one.pop("stages", None)
        runs.append(run_phase4(one))
    summary = {"run_name": cfg.get("run_name"), "seeds": seeds, "curves": [_curve(item) for item in runs]}
    summary["mean_final_alive"] = _mean_alive(summary["curves"])
    summary["mean_rollback"] = _mean_rollback(summary["curves"])
    summary["later_faster"] = _later(runs)
    summary["vision"] = vision_status() if cfg.get("pixels") else None
    out = repo_path("runs") / f"{cfg.get('run_name', 'evolve')}_curves.json"
    out.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    _write_svg(out.with_suffix(".svg"), summary["curves"])
    print(
        f"[evolve] {cfg.get('run_name')} seeds={seeds} mean_final_alive={summary.get('mean_final_alive')} "
        f"mean_rollback={summary.get('mean_rollback')} later_faster={summary.get('later_faster')}",
        flush=True,
    )
    return summary


def _curve(summary: dict) -> list[dict]:
    rows = []
    for day in summary.get("days") or []:
        census = day.get("census") or {}
        evolved = (census.get("actors") or {}).get("evolved") or {}
        agent = (census.get("actors") or {}).get("agent") or {}
        if day.get("after_last_night"):
            continue
        if not census and "exam" not in day:
            continue
        rows.append(
            {
                "day": day.get("day"),
                "alive": evolved.get("alive"),
                "forgotten": evolved.get("forgotten"),
                "mastery": evolved.get("mastery"),
                "lags": evolved.get("lags") or [],
                "tokens_per_ok": evolved.get("tokens_per_ok"),
                "agent_alive": agent.get("alive"),
                "agent_tokens_per_ok": agent.get("tokens_per_ok"),
                "route": day.get("route"),
                "inventions": day.get("inventions"),
                "reject": day.get("reject"),
                "rolled_back": bool(day.get("rolled_back")),
                "exam_evolved": (day.get("exam") or {}).get("evolved", {}).get("rate"),
            }
        )
    rates = rollback_rates([bool(row.get("rolled_back")) for row in rows])
    for row, rate in zip(rows, rates):
        row["rollback_rate"] = rate
    return rows


def _mean_alive(curves: list[list[dict]]) -> float | None:
    finals = []
    for curve in curves:
        alive = [row["alive"] for row in curve if row.get("alive") is not None]
        if alive:
            finals.append(alive[-1])
    if not finals:
        return None
    return sum(finals) / len(finals)


def _mean_rollback(curves: list[list[dict]]) -> float | None:
    finals = [curve[-1]["rollback_rate"] for curve in curves if curve and curve[-1].get("rollback_rate") is not None]
    if not finals:
        return None
    return sum(finals) / len(finals)


def _later(runs: list[dict]) -> dict | None:
    pooled = []
    for summary in runs:
        days = [day for day in (summary.get("days") or []) if (day.get("census") or {}).get("actors")]
        if not days:
            continue
        lags = ((days[-1]["census"].get("actors") or {}).get("evolved") or {}).get("lags") or []
        pooled.extend(lags)
    return later_faster(pooled)


def _write_svg(path, curves: list[list[dict]]) -> None:
    """Alive count per morning. No extra plotting library."""
    width, height, pad = 640, 240, 28
    series = []
    peak = 1
    for curve in curves:
        points = [(row.get("day") or 0, row.get("alive")) for row in curve if row.get("alive") is not None]
        if not points:
            continue
        series.append(points)
        peak = max(peak, max(value for _day, value in points))
    if not series:
        return
    last_day = max(day for points in series for day, _value in points)
    span = max(1, last_day)

    def xy(day: int, value: float) -> tuple[float, float]:
        x = pad + (width - 2 * pad) * (day / span)
        y = height - pad - (height - 2 * pad) * (value / peak)
        return x, y

    colors = ("#1b6ca8", "#c45c26", "#2f7d4a")
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{pad}" y="18" font-size="14" font-family="sans-serif">surviving skills</text>',
    ]
    for index, points in enumerate(series):
        drawn = " ".join(f"{xy(day, value)[0]:.1f},{xy(day, value)[1]:.1f}" for day, value in points)
        color = colors[index % len(colors)]
        lines.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{drawn}"/>')
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")
