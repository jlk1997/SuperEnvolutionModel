# -*- coding: utf-8 -*-
"""Dual-vs-agent cost ledger stub from archival office summaries (蚁算 v0.2.5).

Uses exam_items.steps as step cost; tokens unknown in archival summaries → null.
Does not retrain. Does not touch Gate2/3 claims.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


DEFAULT_SUMMARIES = [
    "runs/office_gate2_full_slate_s0/20261017-201213/summary.json",
    "runs/office_gate2_full_slate_s1/20261017-210105/summary.json",
    "runs/office_gate2_mid_n_dual_s0/20261018-105958/summary.json",
    "runs/office_gate2_mid_n_dual_s1/20261018-114219/summary.json",
]


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
        "tokens_total": None,
        "tokens_mean": None,
        "tokens_available": False,
    }


def build(root: Path | None = None, rels: list[str] | None = None) -> dict:
    root = root or repo_root()
    rels = rels or DEFAULT_SUMMARIES
    rows = []
    missing = []
    dual_steps = []
    agent_steps = []
    dual_fail = []
    agent_fail = []
    for rel in rels:
        path = root / rel
        if not path.is_file():
            missing.append(rel)
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        arms = {a["arm"]: _arm_cost(a) for a in (data.get("arms") or [])}
        dual = arms.get("dual")
        agent = arms.get("agent")
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
            "dual_vs_agent": {
                "dual_ok_rate": dual["ok_rate"] if dual else None,
                "agent_ok_rate": agent["ok_rate"] if agent else None,
                "dual_steps_mean": dual["steps_mean"] if dual else None,
                "agent_steps_mean": agent["steps_mean"] if agent else None,
                "dual_fail_rate": dual["fail_rate"] if dual else None,
                "agent_fail_rate": agent["fail_rate"] if agent else None,
                "step_advantage_agent_minus_dual": (
                    (agent["steps_mean"] - dual["steps_mean"])
                    if dual and agent and dual["steps_mean"] is not None and agent["steps_mean"] is not None
                    else None
                ),
            },
        })

    def _mean(xs):
        return (sum(xs) / len(xs)) if xs else None

    evidence = {
        "kind": "dual_vs_agent_cost_ledger",
        "product": "蚁算模型",
        "version": "0.2.5",
        "gate": "0.6",
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "method": "archival_summary_steps",
        "gpu": False,
        "vl": False,
        "tokens_note": "Archival exam_items lack token counts; tokens_* are null stubs until model_turn_log aggregation.",
        "summaries": rels,
        "missing": missing,
        "rows": rows,
        "aggregate": {
            "n_reports": len(rows),
            "dual_steps_mean": _mean(dual_steps),
            "agent_steps_mean": _mean(agent_steps),
            "dual_fail_rate_mean": _mean(dual_fail),
            "agent_fail_rate_mean": _mean(agent_fail),
            "step_delta_agent_minus_dual": (
                (_mean(agent_steps) - _mean(dual_steps))
                if dual_steps and agent_steps
                else None
            ),
        },
        "gate2_claim_untouched": True,
        "pass": bool(rows) and not missing,
        "notes": "Stub ledger for 蚁算 v0.2.5 product demo; not a new Gate claim.",
    }
    return evidence


def to_markdown(ev: dict) -> str:
    agg = ev["aggregate"]
    lines = [
        "# Dual vs Agent 成本账本（蚁算 v0.2.5 stub）",
        "",
        f"时间：{ev['timestamp']}（Asia/Shanghai）",
        f"方法：{ev['method']} ｜ Gate **{ev['gate']}** ｜ tokens 暂不可用",
        "",
        f"判断：**{'PASS' if ev['pass'] else 'FAIL'}**（有归档摘要可聚合）",
        "",
        "## 汇总",
        f"- reports={agg['n_reports']}",
        f"- dual_steps_mean={agg['dual_steps_mean']}",
        f"- agent_steps_mean={agg['agent_steps_mean']}",
        f"- step_delta (agent−dual)={agg['step_delta_agent_minus_dual']}",
        f"- dual_fail_rate_mean={agg['dual_fail_rate_mean']}",
        f"- agent_fail_rate_mean={agg['agent_fail_rate_mean']}",
        "",
        "| summary | seed | dual_ok | agent_ok | dual_steps | agent_steps | dual_fail | agent_fail |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in ev["rows"]:
        d = r["dual_vs_agent"]
        lines.append(
            f"| `{r['path']}` | {r['seed']} | {d['dual_ok_rate']} | {d['agent_ok_rate']} | "
            f"{d['dual_steps_mean']} | {d['agent_steps_mean']} | {d['dual_fail_rate']} | {d['agent_fail_rate']} |"
        )
    lines += [
        "",
        "## 说明",
        "- Gate2/3 CLAIM 不动。",
        "- tokens 需后续从 model_turn_log 补齐。",
        "- 无 VL。",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    root = repo_root()
    ev = build(root)
    docs = root / "docs"
    stamp = datetime.now().strftime("%Y-%m-%d")
    jp = docs / f"COST_LEDGER_DUAL_VS_AGENT_{stamp}.json"
    mp = docs / f"COST_LEDGER_DUAL_VS_AGENT_{stamp}.md"
    jp.write_text(json.dumps(ev, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mp.write_text(to_markdown(ev), encoding="utf-8")
    print(json.dumps({"pass": ev["pass"], "json": str(jp), "aggregate": ev["aggregate"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
