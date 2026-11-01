# -*- coding: utf-8 -*-
"""C151: Grow business day sandbox — more files/days, multi-day U2C.
Gate 0.6. gen11 HOLD. Gate2/3 untouched.
"""
from __future__ import annotations
import json, shutil, sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import sum_csv_text, confidence_gated_money
from evo.office.shadow_write_guarded_pilot import WRITE_ALLOWLIST

GATE = 0.6
DOC = ROOT / "docs/r50"
BASE = ROOT / "runs/business_day_sandbox_c151"
RUN = ROOT / "runs/c151_business_day_grow"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


DAYS = [
    {
        "day": "D0",
        "date": "2026-10-17",
        "orders": "order_id,sku,qty,status,amount\nO1,A,2,paid,18.00\nO2,B,1,open,40.00\nO3,A,3,paid,27.00\nO4,C,1,paid,9.00\nO5,D,2,refund,6.00\n",
        "expenses": "eid,category,status,amount\nE1,travel,paid,120.50\nE2,meals,paid,45.00\nE3,supplies,open,30.00\nE4,travel,void,99.00\n",
        "inventory": "sku,qty,status\nA,25,ok\nB,8,hold\nC,12,ok\nD,3,ok\n",
        "expect_paid_orders": 54.0,
        "expect_paid_exp": 165.50,
        "expect_qty_ok": 40,
    },
    {
        "day": "D1",
        "date": "2026-10-18",
        "orders": "order_id,sku,qty,status,amount\nP1,A,1,paid,12.00\nP2,B,2,paid,22.00\nP3,C,1,open,15.00\nP4,D,3,paid,18.00\nP5,A,1,void,9.00\n",
        "expenses": "eid,category,status,amount\nF1,meals,paid,33.00\nF2,travel,paid,80.00\nF3,supplies,paid,12.50\nF4,meals,open,20.00\n",
        "inventory": "sku,qty,status\nA,20,ok\nB,10,ok\nC,5,hold\nD,7,ok\n",
        "expect_paid_orders": 52.0,
        "expect_paid_exp": 125.50,
        "expect_qty_ok": 37,
    },
    {
        "day": "D2",
        "date": "2026-10-19",
        "orders": "order_id,sku,qty,status,amount\nQ1,A,4,paid,40.00\nQ2,B,1,paid,11.00\nQ3,C,2,open,30.00\nQ4,D,1,paid,8.50\nQ5,A,1,paid,10.00\n",
        "expenses": "eid,category,status,amount\nG1,travel,paid,200.00\nG2,meals,void,50.00\nG3,supplies,paid,25.00\nG4,travel,open,60.00\n",
        "inventory": "sku,qty,status\nA,18,ok\nB,6,ok\nC,9,ok\nD,2,hold\n",
        "expect_paid_orders": 69.5,
        "expect_paid_exp": 225.00,
        "expect_qty_ok": 33,
    },
]


def seed_multi_day(base: Path) -> dict:
    if base.exists():
        shutil.rmtree(base)
    sb = base / "sandbox"
    n_files = 0
    for d in DAYS:
        day_dir = sb / "Documents" / "inbox" / d["day"]
        for name, text in [
            ("orders.csv", d["orders"]),
            ("expenses.csv", d["expenses"]),
            ("inventory.csv", d["inventory"]),
            ("notes.txt", f"{d['date']} Bay follow-up; stamp receipts\n"),
        ]:
            p = day_dir / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
            n_files += 1
    # shared extras
    extras = {
        "Documents/inbox/vendors.csv": "vendor,status,balance\nAcme,active,1200\nBeta,hold,400\nGamma,active,800\n",
        "Documents/inbox/tax_rates.csv": "region,rate\nCN,0.13\nUS,0.08\n",
        "Documents/reports/.keep": "",
        "Documents/exports/.keep": "",
        "Desktop/scratch.txt": "temp\n",
        "secret/payroll.csv": "should_not_write,here\n",
    }
    for rel, text in extras.items():
        p = sb / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        n_files += 1
    allow = sorted(WRITE_ALLOWLIST | {
        "Documents/reports/day_summary.csv",
        "Documents/reports/day_report.md",
        "Documents/reports/week_rollup.csv",
        "Documents/exports/paid_rollup.csv",
        "Documents/exports/multi_day.json",
        "out.txt",
        "exports/summary.txt",
    })
    # per-day report allow
    for d in DAYS:
        allow.append(f"Documents/reports/{d['day']}_summary.csv")
        allow.append(f"Documents/reports/{d['day']}_report.md")
    allow = sorted(set(allow))
    (base / "ALLOWLIST.json").write_text(
        json.dumps({"write_allowlist": allow, "version": "c151_multi_day", "n_days": len(DAYS)}, indent=2) + "\n",
        encoding="utf-8",
    )
    return {"seeded": True, "n_files": n_files, "n_days": len(DAYS), "allow_n": len(allow)}


def guarded_write(sb: Path, rel: str, text: str, allow: set) -> dict:
    if ".." in rel.replace("\\", "/") or rel.replace("\\", "/").startswith("secret"):
        return {"ok": False, "reason": "path_denied", "rel": rel}
    if rel not in allow:
        return {"ok": False, "reason": "not_allowlisted", "rel": rel}
    p = sb / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return {"ok": True, "rel": rel, "bytes": len(text.encode("utf-8"))}


def run_day(sb: Path, d: dict, allow: set) -> dict:
    day = d["day"]
    inbox = sb / "Documents" / "inbox" / day
    orders = (inbox / "orders.csv").read_text(encoding="utf-8")
    expenses = (inbox / "expenses.csv").read_text(encoding="utf-8")
    inv = (inbox / "inventory.csv").read_text(encoding="utf-8")
    paid_orders = sum_csv_text(orders, amount_col="amount", status_col="status", status_value="paid")
    exp_paid_text = " ".join(
        f"paid {r.split(',')[3]}" for r in expenses.strip().splitlines()[1:] if r.split(",")[2] == "paid"
    )
    gated = confidence_gated_money(exp_paid_text, model_guess=999.0)
    paid_exp = float(gated["value"])
    qty_ok = 0
    for ln in inv.strip().splitlines()[1:]:
        _sku, qty, st = ln.split(",")
        if st == "ok":
            qty_ok += int(qty)
    day_total = paid_orders + paid_exp
    w1 = guarded_write(
        sb, f"Documents/reports/{day}_summary.csv",
        f"metric,value\npaid_orders,{paid_orders:.2f}\npaid_expenses,{paid_exp:.2f}\nday_total,{day_total:.2f}\ninventory_ok_qty,{qty_ok}\n",
        allow,
    )
    w2 = guarded_write(
        sb, f"Documents/reports/{day}_report.md",
        f"# {day} ({d['date']})\n\npaid_orders: {paid_orders:.2f}\npaid_expenses: {paid_exp:.2f}\nday_total: {day_total:.2f}\ninventory_ok_qty: {qty_ok}\n",
        allow,
    )
    nums_ok = (
        abs(paid_orders - d["expect_paid_orders"]) < 0.08
        and abs(paid_exp - d["expect_paid_exp"]) < 0.08
        and qty_ok == d["expect_qty_ok"]
    )
    return {
        "day": day,
        "date": d["date"],
        "paid_orders": paid_orders,
        "paid_expenses": paid_exp,
        "day_total": day_total,
        "inventory_ok_qty": qty_ok,
        "writes_ok": w1["ok"] and w2["ok"],
        "nums_ok": nums_ok,
        "gate": gated,
        "ok": w1["ok"] and w2["ok"] and nums_ok,
    }


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    seed = seed_multi_day(BASE)
    sb = BASE / "sandbox"
    allow = set(json.loads((BASE / "ALLOWLIST.json").read_text(encoding="utf-8"))["write_allowlist"])
    day_results = [run_day(sb, d, allow) for d in DAYS]
    # week rollup
    week_paid = sum(r["day_total"] for r in day_results)
    roll = guarded_write(
        sb, "Documents/reports/week_rollup.csv",
        "day,paid_orders,paid_expenses,day_total,qty_ok\n"
        + "".join(
            f"{r['day']},{r['paid_orders']:.2f},{r['paid_expenses']:.2f},{r['day_total']:.2f},{r['inventory_ok_qty']}\n"
            for r in day_results
        )
        + f"WEEK,,,{week_paid:.2f},\n",
        allow,
    )
    export = guarded_write(
        sb, "Documents/exports/multi_day.json",
        json.dumps({"days": day_results, "week_paid": week_paid}, ensure_ascii=False, indent=2) + "\n",
        allow,
    )
    deny1 = guarded_write(sb, "secret/payroll.csv", "hack\n", allow)
    deny2 = guarded_write(sb, "../outside.txt", "escape\n", allow)
    # U2C crystal from multi-day
    atom = {
        "atom": "office_business_multiday_u2c",
        "family": "cross_family_compose",
        "source": "c151_business_day_grow",
        "n_days": len(DAYS),
        "week_paid": week_paid,
        "days": [{"day": r["day"], "day_total": r["day_total"]} for r in day_results],
        "status": "crystallized",
    }
    J(BASE / "atom_crystal.json", atom)
    use_log = [{"phase": "day", **r} for r in day_results]
    use_log.append({"phase": "rollup", "week_paid": week_paid, "ok": roll["ok"] and export["ok"]})
    use_log.append({"phase": "deny", "secret": not deny1["ok"], "escape": not deny2["ok"]})
    use_log.append({"phase": "crystallize", "atom": atom["atom"], "ok": True})
    (BASE / "u2c_use_log.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in use_log) + "\n", encoding="utf-8"
    )
    days_ok = all(r["ok"] for r in day_results)
    denies_ok = (not deny1["ok"]) and (not deny2["ok"])
    ok = days_ok and denies_ok and roll["ok"] and export["ok"] and (BASE / "atom_crystal.json").is_file()
    rate = 1.0 if ok else (sum(1 for r in day_results if r["ok"]) / max(1, len(day_results)))
    out = {
        "cycle": "C151",
        "theme": "business_day_sandbox_grow_multiday",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "sandbox": str(BASE.relative_to(ROOT)).replace("\\", "/"),
        "seed": seed,
        "days": day_results,
        "week_paid": week_paid,
        "n_days": len(DAYS),
        "n_files": seed["n_files"],
        "denies_ok": denies_ok,
        "rate": rate,
        "pass": ok and rate >= GATE,
        "claim": False,
        "note": "Grew sandbox to 3 business days + vendors/tax extras; allowlisted writes; secret denied; U2C crystal.",
    }
    J(DOC / "C151_BUSINESS_DAY_GROW.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C151", "ok": ok, "n_days": len(DAYS), "n_files": seed["n_files"],
        "week_paid": week_paid, "pass": out["pass"],
    }, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
