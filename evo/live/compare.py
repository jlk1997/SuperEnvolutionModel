"""Gate 1: continuous learning against the shift schedule, on the same stream."""

from __future__ import annotations

from pathlib import Path

from evo.live.service import absorption
from evo.stats import breakeven_uses, paired_bootstrap


def _by_name(report: dict) -> dict:
    return {arm["arm"]: arm for arm in report.get("arms") or []}


def _flags(arm: dict) -> list[float]:
    return [1.0 if item.get("ok") else 0.0 for item in arm.get("exam_items") or []]


def breakeven_for(evolved: dict, agent: dict) -> float | None:
    if not evolved or not agent:
        return None
    per_e = evolved.get("tokens_per_ok")
    per_a = agent.get("tokens_per_ok")
    if per_e is None or per_a is None:
        return None
    return breakeven_uses(float(evolved.get("train_tokens") or 0), float(per_e), float(per_a))


def judge_seed(report: dict) -> dict:
    arms = _by_name(report)
    continual = arms.get("continual")
    shift = arms.get("shift")
    agent = arms.get("agent")
    if not continual or not shift or not agent:
        checks = {name: False for name in ("lag", "forget", "tokens", "safety", "drift")}
        continual = continual or {}
        shift = shift or {}
        agent = agent or {}
    else:
        checks = {
            "lag": _lag_ok(continual.get("mastery"), shift.get("mastery")),
            "forget": int(continual.get("forgotten") or 0) <= int(shift.get("forgotten") or 0),
            "tokens": _tokens_ok(continual.get("tokens_per_ok"), agent.get("tokens_per_ok")),
            "safety": int(continual.get("safety_fails") or 0) == 0 and not continual.get("exam_leak"),
            "drift": _drift_ok(continual.get("drift_recovery"), shift.get("drift_recovery")),
        }
    left = _flags(continual)
    right = _flags(shift)
    ci = paired_bootstrap(left, right, seed=int(report.get("seed") or 0))
    checks["ci"] = bool(ci.get("excludes_zero") and ci.get("mean") is not None and ci["mean"] > 0)
    return {
        "seed": report.get("seed"),
        "checks": checks,
        "ci": ci,
        "breakeven_uses": breakeven_for(continual, agent),
        "opt_steps": {
            "continual": continual.get("opt_steps"),
            "shift": shift.get("opt_steps"),
            "continual_sft": (arms.get("continual_sft") or {}).get("opt_steps"),
        },
    }


def judge_stream(reports: list[dict]) -> dict:
    """Pooled across seeds. A missing arm fails the gate instead of counting as a win."""
    per_seed = [judge_seed(report) for report in reports]
    left = []
    right = []
    for report in reports:
        arms = _by_name(report)
        left.extend(_flags(arms.get("continual") or {}))
        right.extend(_flags(arms.get("shift") or {}))
    ci = paired_bootstrap(left, right, seed=0)
    lag = all(item["checks"]["lag"] for item in per_seed) if per_seed else False
    forget = all(item["checks"]["forget"] for item in per_seed) if per_seed else False
    tokens = all(item["checks"]["tokens"] for item in per_seed) if per_seed else False
    safety = all(item["checks"]["safety"] for item in per_seed) if per_seed else False
    drift = all(item["checks"]["drift"] for item in per_seed) if per_seed else False
    ci_ok = bool(ci.get("excludes_zero") and ci.get("mean") is not None and ci["mean"] > 0)
    checks = {"lag": lag, "forget": forget, "tokens": tokens, "safety": safety, "drift": drift, "ci": ci_ok}
    passed = all(checks.values())
    if passed:
        branch = "Gate 1 passed. The real-body and scaffold-absorption runs are the next measurement."
    elif not forget:
        branch = "Continuous learning forgot more than the shift schedule. Bring the sparse memory forward before another schedule comparison."
    elif not lag and not ci_ok:
        branch = "Continuous learning did not beat the shift schedule. Switch to micro-batches and spend the next runs on scaffold absorption."
    else:
        branch = "Gate 1 did not pass. Re-run the failing checks before opening the next stage."
    uses = [item.get("breakeven_uses") for item in per_seed if item.get("breakeven_uses") is not None]
    evolved_flags = []
    scaffold_flags = []
    for report in reports:
        arms = _by_name(report)
        evolved_flags.extend(bool(item) for item in _flags(arms.get("continual") or {}))
        scaffold_flags.extend(bool(item) for item in _flags(arms.get("oracle") or {}))
    return {
        "pass": passed,
        "checks": checks,
        "ci": ci,
        "seeds": per_seed,
        "breakeven_uses": (sum(uses) / len(uses)) if uses else None,
        "absorption": absorption(evolved_flags, scaffold_flags),
        "branch": branch,
    }


def _lag_ok(continual, shift) -> bool:
    if continual is None or shift is None:
        return False
    if float(shift) <= 0:
        return float(continual) <= float(shift)
    return float(continual) <= float(shift) * 0.7


def _tokens_ok(continual, agent) -> bool:
    if continual is None or agent is None or float(agent) <= 0:
        return False
    return float(continual) <= float(agent) / 5.0


def _drift_ok(continual, shift) -> bool:
    if continual is None:
        return False
    if shift is None:
        return True
    return float(continual) < float(shift)


def judge_office_gate(reports: list[dict]) -> dict:
    from evo.office.judge import judge_office

    return judge_office(reports)


def judge_transfer_gate(trained: list[float], fresh: list[float], dev_touches: int | None, held_touches: int | None) -> dict:
    from evo.office.judge import judge_transfer

    return judge_transfer(trained, fresh, dev_touches, held_touches)


def write_gate(path: Path, gate: dict) -> None:
    """Replace the marker block in the roadmap with this run's judgment."""
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    start, end = "<!-- GATE1_START -->", "<!-- GATE1_END -->"
    body = _gate_markdown(gate)
    block = f"{start}\n{body}\n{end}"
    if start in text and end in text:
        pre, rest = text.split(start, 1)
        _old, post = rest.split(end, 1)
        path.write_text(pre + block + post, encoding="utf-8")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n\n" + block + "\n", encoding="utf-8")


def _gate_markdown(gate: dict) -> str:
    checks = gate.get("checks") or {}
    ci = gate.get("ci") or {}
    lines = [
        f"判定：{'通过' if gate.get('pass') else '未通过'}。{gate.get('branch')}",
        "",
        "| 检查 | 结果 |",
        "| --- | --- |",
    ]
    for name in ("lag", "forget", "tokens", "safety", "drift", "ci"):
        lines.append(f"| {name} | {'是' if checks.get(name) else '否'} |")
    lines.append("")
    lines.append(
        f"连续减倒班的配对差均值 {ci.get('mean')}，区间 [{ci.get('low')}, {ci.get('high')}]，n={ci.get('n')}。"
    )
    lines.append(f"学习摊销回本点（按提示 token 计）：{gate.get('breakeven_uses')} 次。")
    return "\n".join(lines)
