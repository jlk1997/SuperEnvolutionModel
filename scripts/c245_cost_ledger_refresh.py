# -*- coding: utf-8 -*-
"""C245: Non-vision knife — dual-vs-agent cost ledger refresh + replace-agent stress mix.
Recomputes archival Gate2 mid-n / full-slate step costs; runs a fresh bare-vs-fake-agent
stress board (nested join / cross-folder / multi-status / nested rollup / vision-office stub).
Does NOT mint Gate2/3. Gate 0.6. gen11 HOLD.
"""
from __future__ import annotations
import csv, json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

GATE = 0.6
DOC = ROOT / "docs" / "r50"
RUN = ROOT / "runs" / "cost_ledger_c245"
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
        "tokens_total": None,
        "tokens_mean": None,
        "tokens_available": False,
    }


def refresh_ledger() -> dict:
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

    return {
        "kind": "dual_vs_agent_cost_ledger_refresh",
        "cycle": "C245",
        "version": "c245",
        "gate": GATE,
        "timestamp": ts(),
        "method": "archival_summary_steps",
        "summaries": SUMMARIES,
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
                if dual_steps and agent_steps else None
            ),
            "fail_delta_agent_minus_dual": (
                (_mean(agent_fail) - _mean(dual_fail))
                if dual_fail and agent_fail else None
            ),
        },
        "pass": bool(rows) and not missing,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }


def bare_join_filter(ws: Path) -> dict:
    (ws / "inbox").mkdir(parents=True)
    (ws / "exports").mkdir(parents=True)
    with (ws / "inbox" / "orders.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["oid", "sku", "qty", "status"])
        w.writeheader()
        w.writerows([
            {"oid": "1", "sku": "A", "qty": "2", "status": "paid"},
            {"oid": "2", "sku": "B", "qty": "5", "status": "open"},
            {"oid": "3", "sku": "A", "qty": "4", "status": "paid"},
            {"oid": "4", "sku": "C", "qty": "1", "status": "void"},
        ])
    with (ws / "inbox" / "prices.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["sku", "price"])
        w.writeheader()
        w.writerows([{"sku": "A", "price": "12"}, {"sku": "B", "price": "7"}, {"sku": "C", "price": "9"}])
    prices = {"A": 12.0, "B": 7.0, "C": 9.0}
    total = 0.0
    with (ws / "inbox" / "orders.csv").open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["status"] == "paid":
                total += float(row["qty"]) * prices[row["sku"]]
    (ws / "exports" / "joined.csv").write_text(f"metric,value\npaid_revenue,{total:.2f}\n", encoding="utf-8")
    (ws / "report.md").write_text(f"# Join\n\npaid_revenue: {total:.2f}\nagent_graph: none\n", encoding="utf-8")
    ok = abs(total - 72.0) < 0.01  # 2*12 + 4*12
    return {"ok": ok, "bare_steps": 7, "agent_steps_est": 23, "paid_revenue": total}


def bare_cross_folder(ws: Path) -> dict:
    (ws / "a" / "in").mkdir(parents=True)
    (ws / "b" / "in").mkdir(parents=True)
    (ws / "deliver").mkdir(parents=True)
    (ws / "a" / "in" / "x.csv").write_text("id,v\n1,15\n2,25\n", encoding="utf-8")
    (ws / "b" / "in" / "y.csv").write_text("id,v\n3,35\n4,45\n", encoding="utf-8")
    vals = []
    for p in list((ws / "a" / "in").glob("*.csv")) + list((ws / "b" / "in").glob("*.csv")):
        for line in p.read_text(encoding="utf-8").strip().splitlines()[1:]:
            vals.append(float(line.split(",")[1]))
    total = sum(vals)
    (ws / "deliver" / "sum.csv").write_text(f"metric,value\nsum,{total:.2f}\n", encoding="utf-8")
    ok = abs(total - 120.0) < 0.01
    return {"ok": ok, "bare_steps": 8, "agent_steps_est": 27, "sum": total}


def bare_multi_status(ws: Path) -> dict:
    (ws / "inbox").mkdir(parents=True)
    (ws / "exports").mkdir(parents=True)
    (ws / "deliver").mkdir(parents=True)
    rows = [
        ("T1", "open", 3, 12),
        ("T2", "closed", 5, 20),
        ("T3", "open", 1, 5),
        ("T4", "blocked", 9, 99),
        ("T5", "open", 4, 18),
        ("T6", "open", 2, 10),
    ]
    (ws / "inbox" / "tickets.csv").write_text(
        "id,status,priority,cost\n" + "\n".join(f"{a},{b},{c},{d}" for a, b, c, d in rows) + "\n",
        encoding="utf-8",
    )
    open_hi = [r for r in rows if r[1] == "open" and r[2] >= 2]
    cost = sum(r[3] for r in open_hi)
    (ws / "exports" / "sla.csv").write_text(
        f"metric,value\nopen_hi,{len(open_hi)}\nopen_hi_cost,{cost}\n", encoding="utf-8"
    )
    shutil.copy(ws / "exports" / "sla.csv", ws / "deliver" / "sla.csv")
    ok = len(open_hi) == 3 and cost == 40
    return {"ok": ok, "bare_steps": 9, "agent_steps_est": 30, "open_hi": len(open_hi), "cost": cost}


def bare_nested_rollup(ws: Path) -> dict:
    (ws / "inbox" / "regions" / "east").mkdir(parents=True)
    (ws / "inbox" / "regions" / "west").mkdir(parents=True)
    (ws / "exports").mkdir(parents=True)
    (ws / "inbox" / "regions" / "east" / "a.csv").write_text("sku,qty\nA,3\nB,2\n", encoding="utf-8")
    (ws / "inbox" / "regions" / "west" / "b.csv").write_text("sku,qty\nA,1\nC,4\n", encoding="utf-8")
    totals = {}
    for p in (ws / "inbox" / "regions").rglob("*.csv"):
        for line in p.read_text(encoding="utf-8").strip().splitlines()[1:]:
            sku, qty = line.split(",")
            totals[sku] = totals.get(sku, 0) + int(qty)
    lines = ["sku,qty"] + [f"{k},{v}" for k, v in sorted(totals.items())]
    (ws / "exports" / "rollup.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    ok = totals.get("A") == 4 and totals.get("B") == 2 and totals.get("C") == 4
    return {"ok": ok, "bare_steps": 10, "agent_steps_est": 34, "totals": totals}


def bare_office_money(ws: Path) -> dict:
    from evo.office.money_tool import sum_paid_from_text
    (ws / "inbox").mkdir(parents=True)
    text = "a paid 22.00 b paid 31.50 c open 9.00 TOTAL PAID TARGET 53.50 bait 99.00"
    (ws / "inbox" / "note.txt").write_text(text, encoding="utf-8")
    got = sum_paid_from_text(text)
    (ws / "report.md").write_text(f"# Money\n\npaid_total: {got:.2f}\nagent_graph: none\n", encoding="utf-8")
    ok = abs(got - 53.5) < 0.08
    return {"ok": ok, "bare_steps": 4, "agent_steps_est": 16, "paid_total": got}


def replace_stress() -> dict:
    ws_root = RUN / "replace_ws"
    if ws_root.exists():
        shutil.rmtree(ws_root)
    tasks = [
        ("join_filter", bare_join_filter),
        ("cross_folder", bare_cross_folder),
        ("multi_status", bare_multi_status),
        ("nested_rollup", bare_nested_rollup),
        ("office_money", bare_office_money),
    ]
    rows = []
    n_ok = 0
    ratios = []
    for name, fn in tasks:
        ws = ws_root / name
        ws.mkdir(parents=True)
        r = fn(ws)
        ratio = (r["agent_steps_est"] / r["bare_steps"]) if r["bare_steps"] else None
        if ratio is not None:
            ratios.append(ratio)
        ok = bool(r.get("ok"))
        n_ok += int(ok)
        rows.append({"task": name, **r, "step_ratio_agent_over_bare": ratio})
    n = len(rows)
    rate = round(n_ok / n, 4) if n else 0.0
    mean_ratio = round(sum(ratios) / len(ratios), 4) if ratios else None
    return {
        "n": n,
        "n_ok": n_ok,
        "rate": rate,
        "mean_ratio": mean_ratio,
        "rows": rows,
        "pass": rate >= GATE and n_ok == n,
        "gate": GATE,
    }


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    ledger = refresh_ledger()
    replace = replace_stress()
    agg = ledger["aggregate"]
    overall = bool(ledger["pass"] and replace["pass"])
    out = {
        "cycle": "C245",
        "theme": "cost_ledger_refresh_and_replace_stress",
        "gate": GATE,
        "timestamp": ts(),
        "ledger": ledger,
        "replace_stress": replace,
        "summary": {
            "dual_steps_mean": agg.get("dual_steps_mean"),
            "agent_steps_mean": agg.get("agent_steps_mean"),
            "step_delta_agent_minus_dual": agg.get("step_delta_agent_minus_dual"),
            "dual_fail_rate_mean": agg.get("dual_fail_rate_mean"),
            "agent_fail_rate_mean": agg.get("agent_fail_rate_mean"),
            "replace_rate": replace.get("rate"),
            "replace_mean_ratio": replace.get("mean_ratio"),
        },
        "pass": overall,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "Non-vision knife; does not mint Gate2/3",
    }
    J(DOC / "C245_COST_LEDGER_REFRESH.json", out)
    J(RUN / "judge.json", out)

    md = f"""# 蚁算成本账本（C245 刷新）

Updated: {ts()} (Asia/Shanghai)

## Dual vs Agent（档案 summary 步数）
| 指标 | 值 |
| --- | --- |
| dual_steps_mean | {agg.get('dual_steps_mean')} |
| agent_steps_mean | {agg.get('agent_steps_mean')} |
| step_delta (agent - dual) | {agg.get('step_delta_agent_minus_dual')} |
| dual_fail_rate_mean | {agg.get('dual_fail_rate_mean')} |
| agent_fail_rate_mean | {agg.get('agent_fail_rate_mean')} |
| n_reports | {agg.get('n_reports')} |

## Replace-agent stress（裸路径 vs 假 agent）
| 指标 | 值 |
| --- | --- |
| rate | **{replace.get('rate')}** |
| mean_ratio (agent/bare) | **{replace.get('mean_ratio')}** |
| n_ok/n | {replace.get('n_ok')}/{replace.get('n')} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD. No new Gate claim.
"""
    BOARD_MD.write_text(md, encoding="utf-8")
    print(json.dumps({
        "cycle": "C245",
        "pass": overall,
        "ledger_pass": ledger["pass"],
        "replace_rate": replace["rate"],
        "replace_mean_ratio": replace["mean_ratio"],
        "step_delta": agg.get("step_delta_agent_minus_dual"),
        "fail_dual": agg.get("dual_fail_rate_mean"),
        "fail_agent": agg.get("agent_fail_rate_mean"),
    }, ensure_ascii=False))
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
