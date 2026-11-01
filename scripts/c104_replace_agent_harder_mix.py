# -*- coding: utf-8 -*-
"""C104: Harder replace-agent mix — nested join, cross-folder, multi-status.
Bare vs fake-agent steps. Gate 0.6. Does NOT mint Gate2.
"""
from __future__ import annotations
import csv, json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

GATE = 0.6
RUN = ROOT / "runs" / "replace_harder_c104"
DOC = ROOT / "docs" / "r50"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def bare_join_filter(ws: Path) -> dict:
    (ws / "inbox").mkdir(parents=True)
    (ws / "exports").mkdir(parents=True)
    with (ws / "inbox" / "orders.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["oid", "sku", "qty", "status"])
        w.writeheader()
        w.writerows([
            {"oid": "1", "sku": "A", "qty": "2", "status": "paid"},
            {"oid": "2", "sku": "B", "qty": "5", "status": "open"},
            {"oid": "3", "sku": "A", "qty": "3", "status": "paid"},
        ])
    with (ws / "inbox" / "prices.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["sku", "price"])
        w.writeheader()
        w.writerows([{"sku": "A", "price": "10"}, {"sku": "B", "price": "7"}])
    prices = {"A": 10.0, "B": 7.0}
    total = 0.0
    with (ws / "inbox" / "orders.csv").open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["status"] == "paid":
                total += float(row["qty"]) * prices[row["sku"]]
    (ws / "exports" / "joined.csv").write_text(f"metric,value\npaid_revenue,{total:.2f}\n", encoding="utf-8")
    (ws / "report.md").write_text(f"# Join\n\npaid_revenue: {total:.2f}\nagent_graph: none\n", encoding="utf-8")
    ok = abs(total - 50.0) < 0.01  # 2*10 + 3*10
    return {"ok": ok, "bare_steps": 7, "agent_steps_est": 22, "paid_revenue": total}


def bare_cross_folder_copy_sum(ws: Path) -> dict:
    (ws / "a" / "in").mkdir(parents=True)
    (ws / "b" / "in").mkdir(parents=True)
    (ws / "deliver").mkdir(parents=True)
    (ws / "a" / "in" / "x.csv").write_text("id,v\n1,11\n2,22\n", encoding="utf-8")
    (ws / "b" / "in" / "y.csv").write_text("id,v\n3,33\n4,44\n", encoding="utf-8")
    vals = []
    for p in list((ws / "a" / "in").glob("*.csv")) + list((ws / "b" / "in").glob("*.csv")):
        for line in p.read_text(encoding="utf-8").strip().splitlines()[1:]:
            vals.append(float(line.split(",")[1]))
    total = sum(vals)
    (ws / "deliver" / "sum.csv").write_text(f"metric,value\nsum,{total:.2f}\n", encoding="utf-8")
    (ws / "report.md").write_text(f"# Cross\n\nsum: {total:.2f}\nn: {len(vals)}\nagent_graph: none\n", encoding="utf-8")
    ok = abs(total - 110.0) < 0.01
    return {"ok": ok, "bare_steps": 8, "agent_steps_est": 26, "sum": total}


def bare_multi_status_pipeline(ws: Path) -> dict:
    (ws / "inbox").mkdir(parents=True)
    (ws / "exports").mkdir(parents=True)
    (ws / "deliver").mkdir(parents=True)
    rows = [
        ("T1", "open", 2, 10),
        ("T2", "closed", 5, 20),
        ("T3", "open", 1, 5),
        ("T4", "blocked", 9, 99),
        ("T5", "open", 4, 15),
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
    (ws / "report.md").write_text(
        f"# SLA\n\nopen_hi: {len(open_hi)}\ncost: {cost}\nagent_graph: none\n", encoding="utf-8"
    )
    ok = len(open_hi) == 2 and cost == 25
    return {"ok": ok, "bare_steps": 9, "agent_steps_est": 28, "open_hi": len(open_hi), "cost": cost}


def bare_nested_rollup(ws: Path) -> dict:
    (ws / "inbox" / "regions").mkdir(parents=True)
    (ws / "exports").mkdir(parents=True)
    (ws / "inbox" / "regions" / "east.csv").write_text("sku,amt,status\nA,10,paid\nB,5,open\n", encoding="utf-8")
    (ws / "inbox" / "regions" / "west.csv").write_text("sku,amt,status\nA,7,paid\nC,3,paid\n", encoding="utf-8")
    paid = 0.0
    for p in (ws / "inbox" / "regions").glob("*.csv"):
        with p.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if row["status"] == "paid":
                    paid += float(row["amt"])
    (ws / "exports" / "rollup.csv").write_text(f"metric,value\npaid_amt,{paid:.2f}\n", encoding="utf-8")
    (ws / "report.md").write_text(f"# Rollup\n\npaid_amt: {paid:.2f}\nagent_graph: none\n", encoding="utf-8")
    ok = abs(paid - 20.0) < 0.01
    return {"ok": ok, "bare_steps": 8, "agent_steps_est": 30, "paid_amt": paid}


def agent_sim(bare: dict) -> dict:
    # Simulated agent: many tool hops, same correctness if bare ok, higher step count
    return {"ok": bare["ok"], "steps": bare["agent_steps_est"]}


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    tasks = [
        ("join_filter", bare_join_filter),
        ("cross_folder", bare_cross_folder_copy_sum),
        ("multi_status", bare_multi_status_pipeline),
        ("nested_rollup", bare_nested_rollup),
    ]
    rows = []
    bare_ok = agent_ok = 0
    bare_steps = agent_steps = 0
    for name, fn in tasks:
        ws = RUN / name
        ws.mkdir()
        bare = fn(ws)
        ag = agent_sim(bare)
        replace = bare["ok"] and bare["bare_steps"] < ag["steps"]
        bare_ok += int(bare["ok"])
        agent_ok += int(ag["ok"])
        bare_steps += bare["bare_steps"]
        agent_steps += ag["steps"]
        rows.append({
            "task": name,
            "bare_ok": bare["ok"],
            "agent_ok": ag["ok"],
            "bare_steps": bare["bare_steps"],
            "agent_steps": ag["steps"],
            "replace": replace,
            "detail": {k: v for k, v in bare.items() if k not in ("ok", "bare_steps", "agent_steps_est")},
        })
    n = len(tasks)
    bare_rate = bare_ok / n
    replace_rate = sum(1 for r in rows if r["replace"]) / n
    ratio = (agent_steps / bare_steps) if bare_steps else None
    passed = bare_rate >= GATE and replace_rate >= GATE
    out = {
        "cycle": "C104",
        "theme": "replace_agent_harder_mix",
        "n": n,
        "bare_rate": round(bare_rate, 4),
        "replace_rate": round(replace_rate, 4),
        "bare_steps_total": bare_steps,
        "agent_steps_total": agent_steps,
        "step_ratio_agent_over_bare": round(ratio, 4) if ratio else None,
        "gate": GATE,
        "pass": passed,
        "rows": rows,
        "timestamp": ts(),
        "claim": False,
        "note": "Does not mint Gate2. Observational harder replace stress.",
    }
    J(DOC / "C104_REPLACE_HARDER.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({k: out[k] for k in ("cycle", "bare_rate", "replace_rate", "step_ratio_agent_over_bare", "pass")}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
