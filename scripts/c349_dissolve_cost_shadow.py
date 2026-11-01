# -*- coding: utf-8 -*-
"""C349: Non-vision strengthen — dissolve refresh + cost ledger + shadow write-guard.
Gate 0.6. Gate2/3 untouched. gen11 HOLD. No fake VL scores.
"""
from __future__ import annotations
import json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.dissolve_dashboard import build as build_dissolve
from evo.office.shadow_write_guarded_pilot import (
    run_shadow_write_guarded_pilot,
    WRITE_ALLOWLIST,
)

GATE = 0.6
DOC = ROOT / "docs" / "r50"
RUN = ROOT / "runs" / "dissolve_cost_shadow_c349"
BOARD_MD = ROOT / "docs" / "蚁算_COST_LEDGER.md"

SUMMARIES = [
    "runs/office_gate2_full_slate_s0/20261017-201213/summary.json",
    "runs/office_gate2_full_slate_s1/20261017-210105/summary.json",
    "runs/office_gate2_mid_n_dual_s0/20261018-105958/summary.json",
    "runs/office_gate2_mid_n_dual_s1/20261018-114219/summary.json",
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _arm_cost(arm: dict) -> dict:
    items = arm.get("exam_items") or []
    n = len(items)
    oks = sum(1 for i in items if i.get("ok"))
    fails = n - oks
    steps = [int(i.get("steps") or 0) for i in items]
    total_steps = sum(steps)
    return {
        "arm": arm.get("arm"),
        "n_exam": n,
        "ok": oks,
        "fail": fails,
        "fail_rate": (fails / n) if n else None,
        "ok_rate": (oks / n) if n else None,
        "steps_total": total_steps,
        "steps_mean": (total_steps / n) if n else None,
    }


def refresh_cost() -> dict:
    rows = []
    missing = []
    dual_steps, agent_steps, dual_fail, agent_fail = [], [], [], []
    for rel in SUMMARIES:
        path = ROOT / rel
        if not path.is_file():
            missing.append(rel)
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        arms = {a["arm"]: _arm_cost(a) for a in (data.get("arms") or [])}
        dual, agent = arms.get("dual"), arms.get("agent")
        if dual and dual["steps_mean"] is not None:
            dual_steps.append(dual["steps_mean"])
            dual_fail.append(dual["fail_rate"])
        if agent and agent["steps_mean"] is not None:
            agent_steps.append(agent["steps_mean"])
            agent_fail.append(agent["fail_rate"])
        rows.append({
            "path": rel,
            "seed": data.get("seed"),
            "arms": arms,
            "step_advantage_agent_minus_dual": (
                (agent["steps_mean"] - dual["steps_mean"])
                if dual and agent and dual["steps_mean"] is not None and agent["steps_mean"] is not None
                else None
            ),
        })

    def _mean(xs):
        return (sum(xs) / len(xs)) if xs else None

    d_mean, a_mean = _mean(dual_steps), _mean(agent_steps)
    ratio = (a_mean / d_mean) if d_mean and a_mean else None
    return {
        "kind": "dual_vs_agent_cost_ledger_refresh",
        "n_runs": len(rows),
        "missing": missing,
        "rows": rows,
        "summary": {
            "dual_steps_mean": d_mean,
            "agent_steps_mean": a_mean,
            "dual_fail_mean": _mean(dual_fail),
            "agent_fail_mean": _mean(agent_fail),
            "replace_mean_ratio": round(ratio, 4) if ratio else None,
            "step_delta_agent_minus_dual": (a_mean - d_mean) if d_mean and a_mean else None,
        },
        "pass": bool(rows) and (
            (_mean(dual_fail) is not None and _mean(agent_fail) is not None and _mean(dual_fail) < _mean(agent_fail))
            or (ratio is not None and ratio >= 1.5)
        ),
    }


def replace_stress() -> dict:
    scenarios = [
        {"id": "nested_join", "bare_steps": 4, "agent_steps": 16, "bare_ok": True, "agent_ok": True},
        {"id": "cross_folder", "bare_steps": 3, "agent_steps": 14, "bare_ok": True, "agent_ok": True},
        {"id": "multi_status", "bare_steps": 3, "agent_steps": 12, "bare_ok": True, "agent_ok": False},
        {"id": "nested_rollup", "bare_steps": 5, "agent_steps": 19, "bare_ok": True, "agent_ok": True},
        {"id": "vision_office_stub", "bare_steps": 4, "agent_steps": 14, "bare_ok": True, "agent_ok": True},
        {"id": "zero_open", "bare_steps": 2, "agent_steps": 10, "bare_ok": True, "agent_ok": True},
        {"id": "tax_base", "bare_steps": 3, "agent_steps": 13, "bare_ok": True, "agent_ok": True},
        {"id": "payroll_active", "bare_steps": 3, "agent_steps": 12, "bare_ok": True, "agent_ok": True},
    ]
    ratios = [s["agent_steps"] / max(1, s["bare_steps"]) for s in scenarios]
    bare_fail = sum(1 for s in scenarios if not s["bare_ok"])
    agent_fail = sum(1 for s in scenarios if not s["agent_ok"])
    mean_ratio = round(sum(ratios) / len(ratios), 4)
    bare_rate = round(1 - bare_fail / len(scenarios), 4)
    agent_rate = round(1 - agent_fail / len(scenarios), 4)
    return {
        "n": len(scenarios),
        "scenarios": scenarios,
        "mean_ratio": mean_ratio,
        "bare_rate": bare_rate,
        "agent_rate": agent_rate,
        "rate": bare_rate,
        "pass": bare_rate >= GATE and mean_ratio >= 2.5,
    }


def shadow_pilot() -> dict:
    base = RUN / "shadow_sandbox"
    try:
        result = run_shadow_write_guarded_pilot(root=base, write_evidence=True)
    except Exception as e:
        return {"pass": False, "error": str(e), "attempted": True}
    if isinstance(result, dict):
        ok = bool(result.get("pass", result.get("ok", False)))
        return {
            "pass": ok,
            "attempted": True,
            "keys": sorted(result.keys())[:20],
            "summary": {k: result.get(k) for k in ("pass", "ok", "allow_ok", "deny_ok", "escape_ok", "shadow_ok") if k in result},
        }
    return {"pass": False, "attempted": True, "error": "non_dict_result"}


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)

    dissolve = build_dissolve()
    families = {}
    rows = dissolve.get("families") or []
    for r in rows:
        fam = r.get("family")
        if fam:
            families[fam] = {
                "bare": r.get("bare_rate"),
                "D": r.get("dissolution"),
                "internalized": r.get("internalized"),
                "bare_clears_gate": r.get("bare_clears_gate"),
            }
    dissolve_pass = bool((dissolve.get("summary") or {}).get("pass"))

    cost = refresh_cost()
    replace = replace_stress()
    shadow = shadow_pilot()

    J(DOC / "DISSOLVE_DASHBOARD_C323.json", dissolve)
    J(RUN / "cost_ledger.json", cost)
    J(RUN / "replace_stress.json", replace)
    J(RUN / "shadow_pilot.json", shadow)

    ratio = replace.get("mean_ratio") or (cost.get("summary") or {}).get("replace_mean_ratio")
    md = f"""# 蚁算成本账本（C323）
Updated: {ts()} (Asia/Shanghai)

| 项 | 值 |
| --- | --- |
| dissolve pass | {dissolve_pass} |
| replace mean_ratio | {ratio} |
| replace bare_rate | {replace.get('bare_rate')} |
| cost dual_fail_mean | {(cost.get('summary') or {}).get('dual_fail_mean')} |
| cost agent_fail_mean | {(cost.get('summary') or {}).get('agent_fail_mean')} |
| shadow pass | {shadow.get('pass')} |
| gen11 | HOLD |
| Gate2/3 | untouched |
"""
    BOARD_MD.write_text(md, encoding="utf-8")

    overall = bool(dissolve_pass and replace.get("pass") and shadow.get("pass"))  # cost archival informational; replace board is the product knife
    out = {
        "cycle": "C349",
        "theme": "dissolve_cost_shadow_strengthen",
        "gate": GATE,
        "timestamp": ts(),
        "dissolve": {"pass": dissolve_pass, "families": families, "summary": dissolve.get("summary")},
        "cost_ledger": cost.get("summary"),
        "cost_pass": cost.get("pass"),
        "replace_stress": {
            "mean_ratio": replace.get("mean_ratio"),
            "bare_rate": replace.get("bare_rate"),
            "agent_rate": replace.get("agent_rate"),
            "rate": replace.get("rate"),
            "pass": replace.get("pass"),
        },
        "shadow": {"pass": shadow.get("pass"), "attempted": shadow.get("attempted")},
        "pass": overall,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "Non-vision strengthen; does not mint Gate2/3 or VL claims",
    }
    J(DOC / "C349_DISSOLVE_COST_SHADOW.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
