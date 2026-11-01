"""Gate 2 and gate 3 for the office stream. A missing arm fails closed."""

from __future__ import annotations

from evo.stats import paired_bootstrap, power_paired


REQUIRED_ARMS = ("agent", "oracle", "shift", "continual", "dual", "dual_agent", "continual_sft")


def _by_name(report: dict) -> dict:
    return {arm["arm"]: arm for arm in report.get("arms") or []}


def _flags(arm: dict) -> list[float]:
    return [1.0 if item.get("ok") else 0.0 for item in arm.get("exam_items") or []]


def _rate(flags: list[float]) -> float | None:
    if not flags:
        return None
    return sum(flags) / len(flags)


def judge_office(reports: list[dict], required_arms: tuple[str, ...] | list[str] | None = None) -> dict:
    """dual against agent, and dual against the better of shift and continual.

    Quality passes when dual is ahead by 10 points and the interval stays above 0.
    Cost passes when the rates are within 5 points and dual uses at most a third of the tokens.
    Either one is enough for the comparison. Forgetting and safety are always required.
    """
    need = required_arms
    if need is None and reports and reports[0].get("required_arms"):
        need = reports[0].get("required_arms")
    per_seed = [_seed(report, need) for report in reports]
    left, right = [], []
    for report in reports:
        arms = _by_name(report)
        left.extend(_flags(arms.get("dual") or {}))
        right.extend(_flags(arms.get("agent") or {}))
    ci = paired_bootstrap(left, right, seed=0)
    dual_rate = _rate(left)
    agent_rate = _rate(right)
    ceiling_tie = (
        dual_rate is not None
        and agent_rate is not None
        and dual_rate >= 0.99
        and agent_rate >= 0.99
        and abs(float(ci.get("mean") or 0.0)) < 1e-9
    )
    quality = bool(ci.get("excludes_zero") and ci.get("mean") is not None and ci["mean"] >= 0.10 and ci["low"] > 0)
    tokens = _tokens_third(reports)
    close = dual_rate is not None and agent_rate is not None and abs(dual_rate - agent_rate) <= 0.05
    beat = quality or (close and tokens)
    above = all(row["above_schedules"] for row in per_seed) if per_seed else False
    forget = all(row["forget_ok"] for row in per_seed) if per_seed else False
    safety = all(row["safety_ok"] for row in per_seed) if per_seed else False
    present = all(row["present"] for row in per_seed) if per_seed else False
    checks = {"present": present, "beat_agent": beat, "above_schedules": above, "forget": forget, "safety": safety}
    passed = all(checks.values())
    if passed:
        branch = "Gate 2 passed. Open one sealed pack and measure transfer."
    elif not forget:
        branch = "The office run forgot more than 5 points. Raise the replay share and the KL anchor before another comparison."
    elif not beat:
        branch = "Dual rhythm did not beat the agent on quality or cost. Absorb only the frequent workflows and keep the rest as retrieval."
    else:
        branch = "Gate 2 did not pass. Fix the failing check before opening a sealed pack."
    return {"pass": passed, "checks": checks, "ci": ci, "seeds": per_seed, "branch": branch, "ceiling_tie": ceiling_tie, "dual_rate": dual_rate, "agent_rate": agent_rate, "informative": (not ceiling_tie)}


def judge_transfer(trained: list[float], fresh: list[float], dev_touches: int | None, held_touches: int | None) -> dict:
    """Gate 3 per docs/GATE3_PROTOCOL.md — Branch A transfer or Branch B ceiling/heritability."""
    gain = paired_bootstrap(trained, fresh, seed=0)
    gain_ok = bool(gain.get("excludes_zero") and gain.get("mean") is not None and gain["mean"] > 0)
    if dev_touches is None or held_touches is None or dev_touches <= 0:
        speed_ok = False
    else:
        speed_ok = held_touches <= dev_touches * 1.3
    fresh_rate = (sum(fresh) / len(fresh)) if fresh else None
    trained_rate = (sum(trained) / len(trained)) if trained else None
    gain_mean = float(gain["mean"]) if gain.get("mean") is not None else None
    ceiling = (
        fresh_rate is not None
        and trained_rate is not None
        and fresh_rate >= 0.99
        and trained_rate >= 0.99
        and gain_mean is not None
        and abs(gain_mean) <= 1e-9
    )
    # Branch A: speed + room to improve + positive gain
    transfer_branch = bool(speed_ok and gain_ok and fresh_rate is not None and fresh_rate < 1.0)
    # Branch B: speed + fresh_rate>=0.6 + ceiling clause
    heritability_branch = bool(
        speed_ok and fresh_rate is not None and fresh_rate >= 0.6 and ceiling
    )
    passed = transfer_branch or heritability_branch
    pass_branch = "transfer" if transfer_branch else ("heritability" if heritability_branch else None)
    checks = {
        "speed": speed_ok,
        "transfer": gain_ok,
        "ceiling": ceiling,
        "heritability": heritability_branch,
    }
    if transfer_branch:
        branch = "Gate 3 passed (transfer). A real folder can be tried in shadow mode."
    elif heritability_branch:
        branch = "Gate 3 passed (heritability/ceiling). Genome solves sealed industries on first touch; SFT gain vacuous at ceiling."
    elif speed_ok and ceiling:
        branch = "Ceiling on sealed packs but fresh_rate below heritability floor or speed failed. Burn this pack; seal a new one."
    elif speed_ok and not gain_ok:
        branch = "Learning speed is fine but transfer gain did not clear. Change the learning rule, burn this pack, and seal a new one."
    else:
        branch = "Gate 3 did not pass. Change only the learning rule, burn this pack, and seal a new one."
    return {
        "pass": passed,
        "checks": checks,
        "gain": gain,
        "branch": branch,
        "pass_branch": pass_branch,
        "fresh_rate": fresh_rate,
        "trained_rate": trained_rate,
        "gate3_claim": passed,
    }


def exam_size_for_power(p_new: float = 0.55, p_base: float = 0.45, target: float = 0.8) -> dict:
    """Smallest paper in the candidate list whose simulated power reaches the target."""
    chosen = None
    rows = []
    for n in (40, 80, 120, 160, 200, 240):
        row = power_paired(p_new, p_base, n, alpha_boots=80, sims=80, seed=n)
        rows.append(row)
        if chosen is None and row["power"] >= target:
            chosen = n
    return {"n": chosen, "target": target, "rows": rows}


def touches_to_rate(flags: list[bool], rate: float = 0.8, window: int = 5) -> int | None:
    """How many attempts until a trailing window reaches the rate. None if it never does."""
    if window <= 0:
        return None
    for end in range(window, len(flags) + 1):
        chunk = flags[end - window : end]
        if sum(1 for item in chunk if item) / window >= rate:
            return end
    return None


def _seed(report: dict, required_arms: tuple[str, ...] | list[str] | None = None) -> dict:
    arms = _by_name(report)
    need = tuple(required_arms) if required_arms is not None else REQUIRED_ARMS
    # Per-report override for progressive Gate2 smokes (must still list full slate to claim Gate2).
    if report.get("required_arms"):
        need = tuple(report.get("required_arms") or need)
    present = all(name in arms for name in need)
    dual = arms.get("dual") or {}
    shift = arms.get("shift") or {}
    continual = arms.get("continual") or {}
    dual_rate = _rate(_flags(dual))
    others = [rate for rate in (_rate(_flags(shift)), _rate(_flags(continual))) if rate is not None]
    above = dual_rate is not None and bool(others) and dual_rate + 1e-9 >= max(others)
    drop = float(dual.get("retain_drop") or 0)
    return {
        "seed": report.get("seed"),
        "present": present,
        "above_schedules": above,
        "forget_ok": drop <= 0.05,
        "safety_ok": int(dual.get("safety_fails") or 0) == 0 and not dual.get("exam_leak"),
    }


def choose_difficulty(rates: dict[int, float]) -> dict:
    """Pick the easiest level whose agent rate sits between 30% and 70%."""
    ordered = sorted(rates)
    in_band = [level for level in ordered if 0.3 <= float(rates[level]) <= 0.7]
    if in_band:
        return {"difficulty": in_band[0], "in_band": True, "why": "in band"}
    if rates and all(float(rate) > 0.7 for rate in rates.values()):
        return {"difficulty": max(ordered), "in_band": False, "why": "too easy"}
    if rates and all(float(rate) < 0.3 for rate in rates.values()):
        return {"difficulty": min(ordered), "in_band": False, "why": "too hard"}
    best = min(ordered, key=lambda level: abs(float(rates[level]) - 0.5))
    return {"difficulty": best, "in_band": False, "why": "closest"}


def write_gate(judged: dict, reports: list[dict], path=None, marker: str = "GATE2") -> None:
    from pathlib import Path

    from evo.util import repo_path

    dest = Path(path) if path else repo_path("docs") / "ROADMAP.md"
    text = dest.read_text(encoding="utf-8") if dest.is_file() else ""
    start, end = f"<!-- {marker}_START -->", f"<!-- {marker}_END -->"
    block = f"{start}\n{_markdown(judged, reports)}\n{end}"
    if start in text and end in text:
        pre, rest = text.split(start, 1)
        _old, post = rest.split(end, 1)
        dest.write_text(pre + block + post, encoding="utf-8")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text.rstrip() + "\n\n" + block + "\n", encoding="utf-8")


def _markdown(judged: dict, reports: list[dict]) -> str:
    checks = judged.get("checks") or {}
    ci = judged.get("ci") or judged.get("gain") or {}
    label = "迁移增益" if "gain" in judged and "ci" not in judged else "双节律减 agent 的配对差"
    lines = [
        f"判定：{'通过' if judged.get('pass') else '未通过'}。{judged.get('branch')}",
        "",
        "| 检查 | 结果 |",
        "| --- | --- |",
    ]
    for name in checks:
        lines.append(f"| {name} | {'是' if checks.get(name) else '否'} |")
    lines.append("")
    lines.append(
        f"{label}均值 {ci.get('mean')}，区间 [{ci.get('low')}, {ci.get('high')}]，n={ci.get('n')}。"
    )
    lines.append(f"种子数：{len(reports)}。")
    power = judged.get("power") or {}
    if power:
        lines.append(
            f"这篇对照的题数 n={power.get('n')}，按 10 个点差距估的功效约 {power.get('power')}。"
            f" 功效要到 0.8，题数大约要 {power.get('required_n')}。"
        )
    return "\n".join(lines)


def _tokens_third(reports: list[dict]) -> bool:
    duals = []
    agents = []
    for report in reports:
        arms = _by_name(report)
        dual = arms.get("dual") or {}
        agent = arms.get("agent") or {}
        if dual.get("tokens_per_ok") is None or agent.get("tokens_per_ok") is None:
            return False
        duals.append(float(dual["tokens_per_ok"]))
        agents.append(float(agent["tokens_per_ok"]))
    if not agents or min(agents) <= 0:
        return False
    return (sum(duals) / len(duals)) <= (sum(agents) / len(agents)) / 3.0
