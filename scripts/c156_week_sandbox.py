# -*- coding: utf-8 -*-
"""C156: Week-long business sandbox automation (7 days).
Shadow-guarded writes + money_tool rollups + U2C crystal per day.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import json, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import sum_csv_text, confidence_gated_money
from evo.office.shadow_write_guarded_pilot import WRITE_ALLOWLIST

GATE = 0.6
DOC = ROOT / "docs/r50"
BASE = ROOT / "runs/business_week_sandbox_c156"
RUN = ROOT / "runs/c156_week_sandbox"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


WEEK = [
    {
        "day": "D0", "date": "2026-10-13",
        "orders": "order_id,sku,qty,status,amount\nA1,A,2,paid,20.00\nA2,B,1,open,15.00\nA3,C,1,paid,9.50\nA4,D,2,paid,12.00\nA5,A,1,void,8.00\n",
        "expenses": "eid,category,status,amount\nE1,travel,paid,100.00\nE2,meals,paid,40.00\nE3,supplies,open,25.00\nE4,travel,void,50.00\n",
        "inventory": "sku,qty,status\nA,30,ok\nB,5,hold\nC,10,ok\nD,4,ok\n",
        "expect_paid_orders": 41.5, "expect_paid_exp": 140.0, "expect_qty_ok": 44,
    },
    {
        "day": "D1", "date": "2026-10-14",
        "orders": "order_id,sku,qty,status,amount\nB1,A,1,paid,11.00\nB2,B,2,paid,24.00\nB3,C,1,open,18.00\nB4,D,1,paid,7.00\nB5,A,2,paid,16.00\n",
        "expenses": "eid,category,status,amount\nF1,meals,paid,28.00\nF2,travel,paid,75.00\nF3,supplies,paid,15.00\nF4,meals,open,12.00\n",
        "inventory": "sku,qty,status\nA,28,ok\nB,8,ok\nC,6,hold\nD,5,ok\n",
        "expect_paid_orders": 58.0, "expect_paid_exp": 118.0, "expect_qty_ok": 41,
    },
    {
        "day": "D2", "date": "2026-10-15",
        "orders": "order_id,sku,qty,status,amount\nC1,A,3,paid,30.00\nC2,B,1,paid,10.00\nC3,C,2,open,22.00\nC4,D,1,paid,8.00\nC5,A,1,refund,5.00\n",
        "expenses": "eid,category,status,amount\nG1,travel,paid,150.00\nG2,meals,void,40.00\nG3,supplies,paid,20.00\nG4,travel,open,55.00\n",
        "inventory": "sku,qty,status\nA,22,ok\nB,7,ok\nC,11,ok\nD,3,hold\n",
        "expect_paid_orders": 48.0, "expect_paid_exp": 170.0, "expect_qty_ok": 40,
    },
    {
        "day": "D3", "date": "2026-10-16",
        "orders": "order_id,sku,qty,status,amount\nD1,A,2,paid,18.00\nD2,B,1,paid,13.00\nD3,C,1,paid,9.00\nD4,D,2,open,14.00\nD5,A,1,paid,10.00\n",
        "expenses": "eid,category,status,amount\nH1,meals,paid,35.00\nH2,travel,paid,90.00\nH3,supplies,open,18.00\nH4,meals,paid,22.50\n",
        "inventory": "sku,qty,status\nA,25,ok\nB,9,ok\nC,8,ok\nD,6,ok\n",
        "expect_paid_orders": 50.0, "expect_paid_exp": 147.5, "expect_qty_ok": 48,
    },
    {
        "day": "D4", "date": "2026-10-17",
        "orders": "order_id,sku,qty,status,amount\nE1,A,1,paid,12.00\nE2,B,3,paid,27.00\nE3,C,1,open,11.00\nE4,D,1,paid,6.50\nE5,A,2,void,14.00\n",
        "expenses": "eid,category,status,amount\nI1,travel,paid,110.00\nI2,meals,paid,48.00\nI3,supplies,paid,30.00\nI4,travel,void,70.00\n",
        "inventory": "sku,qty,status\nA,20,ok\nB,4,hold\nC,14,ok\nD,8,ok\n",
        "expect_paid_orders": 45.5, "expect_paid_exp": 188.0, "expect_qty_ok": 42,
    },
    {
        "day": "D5", "date": "2026-10-18",
        "orders": "order_id,sku,qty,status,amount\nF1,A,4,paid,40.00\nF2,B,1,open,9.00\nF3,C,2,paid,16.00\nF4,D,1,paid,7.50\nF5,A,1,paid,11.00\n",
        "expenses": "eid,category,status,amount\nJ1,meals,paid,55.00\nJ2,travel,paid,130.00\nJ3,supplies,open,22.00\nJ4,meals,paid,19.00\n",
        "inventory": "sku,qty,status\nA,18,ok\nB,12,ok\nC,7,ok\nD,2,hold\n",
        "expect_paid_orders": 74.5, "expect_paid_exp": 204.0, "expect_qty_ok": 37,
    },
    {
        "day": "D6", "date": "2026-10-19",
        "orders": "order_id,sku,qty,status,amount\nG1,A,2,paid,22.00\nG2,B,2,paid,20.00\nG3,C,1,paid,8.00\nG4,D,1,open,12.00\nG5,A,1,paid,9.00\n",
        "expenses": "eid,category,status,amount\nK1,travel,paid,95.00\nK2,meals,void,33.00\nK3,supplies,paid,27.00\nK4,travel,paid,60.00\n",
        "inventory": "sku,qty,status\nA,15,ok\nB,10,ok\nC,9,ok\nD,5,ok\n",
        "expect_paid_orders": 59.0, "expect_paid_exp": 182.0, "expect_qty_ok": 39,
    },
]


def seed_day(sb: Path, day: dict) -> int:
    files = {
        f"Documents/inbox/{day['day']}_orders.csv": day["orders"],
        f"Documents/inbox/{day['day']}_expenses.csv": day["expenses"],
        f"Documents/inbox/{day['day']}_inventory.csv": day["inventory"],
        f"Documents/inbox/{day['day']}_notes.txt": f"Week sandbox {day['day']} {day['date']}\n",
    }
    for rel, text in files.items():
        p = sb / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return len(files)


def guarded_write(sb: Path, rel: str, text: str, allow: set) -> dict:
    norm = rel.replace("\\", "/")
    if ".." in norm or norm.startswith("secret"):
        return {"ok": False, "reason": "path_denied", "rel": rel}
    if rel not in allow:
        return {"ok": False, "reason": "not_allowlisted", "rel": rel}
    p = sb / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return {"ok": True, "rel": rel, "bytes": len(text.encode("utf-8"))}


def run_day(sb: Path, day: dict, allow: set) -> dict:
    o_path = sb / f"Documents/inbox/{day['day']}_orders.csv"
    e_path = sb / f"Documents/inbox/{day['day']}_expenses.csv"
    i_path = sb / f"Documents/inbox/{day['day']}_inventory.csv"
    orders = o_path.read_text(encoding="utf-8")
    expenses = e_path.read_text(encoding="utf-8")
    inv = i_path.read_text(encoding="utf-8")
    paid_o = sum_csv_text(orders)
    paid_e = sum_csv_text(expenses)
    # qty ok
    qty_ok = 0.0
    for line in inv.strip().splitlines()[1:]:
        parts = line.split(",")
        if len(parts) >= 3 and parts[2].strip() == "ok":
            qty_ok += float(parts[1])
    gate = confidence_gated_money(orders.replace(",", " "), model_guess=paid_o + 3.0)  # force disagree→tool
    ok_o = abs(paid_o - day["expect_paid_orders"]) < 0.08
    ok_e = abs(paid_e - day["expect_paid_exp"]) < 0.08
    ok_q = abs(qty_ok - day["expect_qty_ok"]) < 0.08
    day_paid = round(paid_o + paid_e, 2)
    summary_csv = f"day,date,paid_orders,paid_expenses,day_paid,qty_ok\n{day['day']},{day['date']},{paid_o},{paid_e},{day_paid},{qty_ok}\n"
    report_md = f"# {day['day']} {day['date']}\n- paid_orders={paid_o}\n- paid_expenses={paid_e}\n- day_paid={day_paid}\n- qty_ok={qty_ok}\n"
    w1 = guarded_write(sb, f"Documents/reports/{day['day']}_summary.csv", summary_csv, allow)
    w2 = guarded_write(sb, f"Documents/reports/{day['day']}_report.md", report_md, allow)
    w3 = guarded_write(sb, f"Documents/exports/{day['day']}_paid_rollup.csv", f"paid\n{day_paid}\n", allow)
    deny = guarded_write(sb, "secret/leak.csv", "nope\n", allow)
    crystal = {
        "atom": "week_day_rollup",
        "day": day["day"],
        "inputs": [str(o_path.name), str(e_path.name), str(i_path.name)],
        "outputs": [w1.get("rel"), w2.get("rel"), w3.get("rel")],
        "ok": ok_o and ok_e and ok_q and w1["ok"] and w2["ok"] and w3["ok"] and not deny["ok"],
    }
    return {
        "day": day["day"], "date": day["date"],
        "paid_orders": paid_o, "paid_expenses": paid_e, "day_paid": day_paid, "qty_ok": qty_ok,
        "ok_orders": ok_o, "ok_expenses": ok_e, "ok_qty": ok_q,
        "writes": [w1, w2, w3], "deny_secret": deny,
        "confidence_gate": {"value": gate["value"], "reason": gate["reason"], "agree": gate["agree"]},
        "crystal": crystal,
        "ok": crystal["ok"],
    }


def main():
    if BASE.exists():
        shutil.rmtree(BASE)
    sb = BASE / "sandbox"
    sb.mkdir(parents=True)
    allow = sorted(WRITE_ALLOWLIST | {
        "Documents/reports/D0_summary.csv", "Documents/reports/D0_report.md", "Documents/exports/D0_paid_rollup.csv",
        "Documents/reports/D1_summary.csv", "Documents/reports/D1_report.md", "Documents/exports/D1_paid_rollup.csv",
        "Documents/reports/D2_summary.csv", "Documents/reports/D2_report.md", "Documents/exports/D2_paid_rollup.csv",
        "Documents/reports/D3_summary.csv", "Documents/reports/D3_report.md", "Documents/exports/D3_paid_rollup.csv",
        "Documents/reports/D4_summary.csv", "Documents/reports/D4_report.md", "Documents/exports/D4_paid_rollup.csv",
        "Documents/reports/D5_summary.csv", "Documents/reports/D5_report.md", "Documents/exports/D5_paid_rollup.csv",
        "Documents/reports/D6_summary.csv", "Documents/reports/D6_report.md", "Documents/exports/D6_paid_rollup.csv",
        "Documents/reports/week_summary.csv", "Documents/reports/week_report.md",
        "Documents/exports/week_paid_rollup.csv", "out.txt", "exports/summary.txt",
    })
    (BASE / "ALLOWLIST.json").write_text(json.dumps({"write_allowlist": allow, "version": "c156_week"}, indent=2) + "\n", encoding="utf-8")
    allow_set = set(allow)
    n_files = 0
    for d in WEEK:
        n_files += seed_day(sb, d)
    day_rows = []
    for d in WEEK:
        day_rows.append(run_day(sb, d, allow_set))
    week_paid = round(sum(r["day_paid"] for r in day_rows), 2)
    n_ok = sum(1 for r in day_rows if r["ok"])
    rate = n_ok / len(day_rows) if day_rows else 0.0
    week_csv = "day,date,day_paid,ok\n" + "".join(f"{r['day']},{r['date']},{r['day_paid']},{int(r['ok'])}\n" for r in day_rows)
    week_md = f"# Week rollup\n- days={len(day_rows)}\n- week_paid={week_paid}\n- rate={rate}\n"
    wsum = guarded_write(sb, "Documents/reports/week_summary.csv", week_csv, allow_set)
    wrep = guarded_write(sb, "Documents/reports/week_report.md", week_md, allow_set)
    wroll = guarded_write(sb, "Documents/exports/week_paid_rollup.csv", f"week_paid\n{week_paid}\n", allow_set)
    expect_week = round(sum(d["expect_paid_orders"] + d["expect_paid_exp"] for d in WEEK), 2)
    out = {
        "cycle": "C156",
        "theme": "week_long_business_sandbox_7d",
        "gate": GATE,
        "timestamp": ts(),
        "n_days": len(day_rows),
        "n_files_seeded": n_files,
        "n_ok_days": n_ok,
        "rate": round(rate, 4),
        "week_paid": week_paid,
        "expect_week_paid": expect_week,
        "week_paid_ok": abs(week_paid - expect_week) < 0.08,
        "days": day_rows,
        "week_writes": [wsum, wrep, wroll],
        "gate_pass": rate >= GATE and len(day_rows) >= 7,
        "pass": rate >= GATE and len(day_rows) >= 7 and abs(week_paid - expect_week) < 0.08,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "7-day automated sandbox with allowlist writes + money_tool. Not a Gate2/3 claim.",
    }
    J(DOC / "C156_WEEK_SANDBOX.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C156", "n_days": out["n_days"], "rate": out["rate"],
        "week_paid": week_paid, "pass": out["pass"],
    }, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
