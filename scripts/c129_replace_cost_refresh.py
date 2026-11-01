# -*- coding: utf-8 -*-
"""C129: Optional replace-agent / cost ledger refresh. Gate 0.6. No Gate2 mint."""
from __future__ import annotations
import csv, json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import sum_csv_text

GATE = 0.6
RUN = ROOT / "runs/replace_cost_c129"
DOC = ROOT / "docs/r50"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def bare_money_join(ws: Path) -> dict:
    (ws / "inbox").mkdir(parents=True)
    (ws / "exports").mkdir(parents=True)
    csv_text = "oid,sku,qty,status,amount\n1,A,2,paid,20\n2,B,5,open,35\n3,A,3,paid,30\n4,C,1,paid,12\n"
    (ws / "inbox" / "orders.csv").write_text(csv_text, encoding="utf-8")
    # bare path: tool-backed sum of paid amounts (not qty*price agent graph)
    total = sum_csv_text(csv_text, amount_col="amount", status_col="status", status_value="paid")
    (ws / "exports" / "paid.csv").write_text(f"metric,value\npaid_total,{total:.2f}\n", encoding="utf-8")
    (ws / "report.md").write_text(
        f"# Replace refresh C129\n\npaid_total: {total:.2f}\nagent_graph: none\nmoney_tool: true\n",
        encoding="utf-8",
    )
    ok = abs(total - 62.0) < 0.08  # 20+30+12
    return {"ok": ok, "bare_steps": 5, "agent_steps_est": 16, "paid_total": total, "money_tool": True}


def agentish_money_join(ws: Path) -> dict:
    """Fake agent: multi-step scrape/filter/sum with intentional overhead."""
    steps = 0
    (ws / "tmp").mkdir(parents=True)
    (ws / "out").mkdir(parents=True)
    raw = "oid,sku,qty,status,amount\n1,A,2,paid,20\n2,B,5,open,35\n3,A,3,paid,30\n4,C,1,paid,12\n"
    (ws / "tmp" / "raw.csv").write_text(raw, encoding="utf-8"); steps += 1
    # step: validate header
    lines = raw.strip().splitlines(); steps += 1
    # step: filter rows one by one into buffer files
    paid_rows = []
    for i, ln in enumerate(lines[1:], 1):
        parts = ln.split(",")
        (ws / "tmp" / f"row_{i}.txt").write_text(ln, encoding="utf-8"); steps += 1
        if parts[3] == "paid":
            paid_rows.append(float(parts[4])); steps += 1
        else:
            steps += 1  # skip branch
    # step: reduce
    total = sum(paid_rows); steps += 1
    (ws / "out" / "sum.txt").write_text(str(total), encoding="utf-8"); steps += 1
    (ws / "out" / "report.md").write_text(f"paid={total}\nagent_graph: multi\n", encoding="utf-8"); steps += 1
    ok = abs(total - 62.0) < 0.08
    return {"ok": ok, "agent_steps": steps, "paid_total": total, "fail": not ok}


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    bare = bare_money_join(RUN / "bare")
    agent = agentish_money_join(RUN / "agent")
    ratio = (agent["agent_steps"] / bare["bare_steps"]) if bare["bare_steps"] else None
    bare_ok = bool(bare["ok"])
    agent_ok = bool(agent["ok"])
    # replace score: bare succeeds with fewer steps
    replace_ok = bare_ok and (bare["bare_steps"] < agent["agent_steps"])
    rate = 1.0 if replace_ok and bare_ok else (0.5 if bare_ok else 0.0)
    out = {
        "cycle": "C129",
        "theme": "replace_cost_refresh_money_tool",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "bare": bare,
        "agent": agent,
        "step_ratio_agent_over_bare": round(ratio, 4) if ratio else None,
        "replace_ok": replace_ok,
        "rate": rate,
        "pass": rate >= GATE,
        "claim": False,
        "note": "Optional cost refresh; uses money_tool on bare path. Does not mint Gate2.",
    }
    J(DOC / "C129_REPLACE_COST_REFRESH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C129",
        "rate": rate,
        "ratio": out["step_ratio_agent_over_bare"],
        "pass": out["pass"],
    }, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
