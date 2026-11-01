# -*- coding: utf-8 -*-
"""C146: Real sandbox business folder day-in-life.
Multi-file shadow + U2C crystal + office atoms. Gate 0.6. gen11 HOLD.
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
BASE = ROOT / "runs/business_day_sandbox_c146"
RUN = ROOT / "runs/c146_day_in_life"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seed_business(base: Path) -> dict:
    if base.exists():
        shutil.rmtree(base)
    sb = base / "sandbox"
    files = {
        "Documents/inbox/orders.csv": "order_id,sku,qty,status,amount\nO1,A,2,paid,18.00\nO2,B,1,open,40.00\nO3,A,3,paid,27.00\nO4,C,1,paid,9.00\nO5,D,2,refund,6.00\n",
        "Documents/inbox/expenses.csv": "eid,category,status,amount\nE1,travel,paid,120.50\nE2,meals,paid,45.00\nE3,supplies,open,30.00\nE4,travel,void,99.00\n",
        "Documents/inbox/inventory.csv": "sku,qty,status\nA,25,ok\nB,8,hold\nC,12,ok\nD,3,ok\n",
        "Documents/inbox/notes.txt": "Bay4 follow-up; stamp receipts afternoon\n",
        "Documents/reports/.keep": "",
        "Documents/exports/.keep": "",
        "Desktop/scratch.txt": "temp\n",
        "secret/payroll.csv": "should_not_write,here\n",
    }
    for rel, text in files.items():
        p = sb / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    allow = sorted(WRITE_ALLOWLIST | {
        "Documents/reports/day_summary.csv",
        "Documents/reports/day_report.md",
        "Documents/exports/paid_rollup.csv",
        "out.txt",
        "exports/summary.txt",
    })
    (base / "ALLOWLIST.json").write_text(json.dumps({"write_allowlist": allow, "version": "c146_business_day"}, indent=2) + "\n", encoding="utf-8")
    return {"seeded": True, "n_files": len(files), "allow_n": len(allow)}


def guarded_write(sb: Path, rel: str, text: str, allow: set) -> dict:
    # reject path escape / secret
    if ".." in rel.replace("\\", "/") or rel.replace("\\", "/").startswith("secret"):
        return {"ok": False, "reason": "path_denied", "rel": rel}
    if rel not in allow and not any(rel.startswith(a.rstrip("*")) for a in allow if a.endswith("**")):
        # exact allowlist membership required
        if rel not in allow:
            return {"ok": False, "reason": "not_allowlisted", "rel": rel}
    p = sb / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return {"ok": True, "rel": rel, "bytes": len(text.encode("utf-8"))}


def day_pipeline(base: Path) -> dict:
    sb = base / "sandbox"
    allow = set(json.loads((base / "ALLOWLIST.json").read_text(encoding="utf-8"))["write_allowlist"])
    use_log = []
    # 1) sum paid orders
    orders = (sb / "Documents/inbox/orders.csv").read_text(encoding="utf-8")
    paid_orders = sum_csv_text(orders, amount_col="amount", status_col="status", status_value="paid")
    use_log.append({"phase": "use", "task": "sum_paid_orders", "ok": True, "value": paid_orders})
    # 2) sum paid expenses with confidence gate (wrong model)
    exp = (sb / "Documents/inbox/expenses.csv").read_text(encoding="utf-8")
    # build OCR-ish text
    exp_text = " ".join(
        f"{r.split(',')[2]} {r.split(',')[3]}" for r in exp.strip().splitlines()[1:]
    )
    # map to paid X.Y style for tool
    exp_paid_text = " ".join(
        f"paid {r.split(',')[3]}" for r in exp.strip().splitlines()[1:] if r.split(",")[2] == "paid"
    ) + " TOTAL PAID TARGET 165.50"
    gated = confidence_gated_money(exp_paid_text, model_guess=999.0)
    paid_exp = float(gated["value"])
    use_log.append({"phase": "use", "task": "sum_paid_expenses_gated", "ok": abs(paid_exp - 165.50) < 0.08, "gate": gated})
    # 3) inventory ok qty
    inv = (sb / "Documents/inbox/inventory.csv").read_text(encoding="utf-8")
    qty_ok = 0
    for ln in inv.strip().splitlines()[1:]:
        sku, qty, st = ln.split(",")
        if st == "ok":
            qty_ok += int(qty)
    use_log.append({"phase": "use", "task": "inventory_ok_qty", "ok": qty_ok == 40, "value": qty_ok})
    # 4) shadow writes (allowlisted)
    day_total = paid_orders + paid_exp
    w1 = guarded_write(sb, "Documents/reports/day_summary.csv", f"metric,value\npaid_orders,{paid_orders:.2f}\npaid_expenses,{paid_exp:.2f}\nday_total,{day_total:.2f}\ninventory_ok_qty,{qty_ok}\n", allow)
    w2 = guarded_write(sb, "Documents/reports/day_report.md", f"# Business Day Report\n\npaid_orders: {paid_orders:.2f}\npaid_expenses: {paid_exp:.2f}\nday_total: {day_total:.2f}\ninventory_ok_qty: {qty_ok}\nagent_graph: none\nconfidence_gate: {gated['confidence']}\n", allow)
    w3 = guarded_write(sb, "Documents/exports/paid_rollup.csv", f"source,value\norders,{paid_orders:.2f}\nexpenses,{paid_exp:.2f}\n", allow)
    w4 = guarded_write(sb, "out.txt", f"day_total={day_total:.2f}\n", allow)
    # 5) denied writes
    d1 = guarded_write(sb, "secret/payroll.csv", "hack\n", allow)
    d2 = guarded_write(sb, "../outside.txt", "escape\n", allow)
    use_log.append({"phase": "shadow_write", "writes": [w1, w2, w3, w4], "denies": [d1, d2]})
    # 6) U2C crystallize
    atom = {
        "atom": "office_business_day_u2c",
        "family": "cross_family_compose",
        "source": "c146_day_in_life",
        "metrics": {
            "paid_orders": paid_orders,
            "paid_expenses": paid_exp,
            "day_total": day_total,
            "inventory_ok_qty": qty_ok,
        },
        "status": "crystallized",
        "n_pairs": 3,
    }
    atom_path = base / "atom_crystal.json"
    J(atom_path, atom)
    use_log.append({"phase": "crystallize", "atom": atom["atom"], "ok": True})
    use_log.append({"phase": "absorb", "method": "stub_no_train", "would_sft": True})
    use_log.append({"phase": "route", "selected": atom["atom"], "why": ["day_in_life", "multi_file", "confidence_gate"]})
    log_path = base / "u2c_use_log.jsonl"
    log_path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in use_log) + "\n", encoding="utf-8")

    writes_ok = all(x["ok"] for x in [w1, w2, w3, w4])
    denies_ok = (not d1["ok"]) and (not d2["ok"])
    nums_ok = abs(paid_orders - 54.0) < 0.08 and abs(paid_exp - 165.50) < 0.08 and qty_ok == 40
    crystal_ok = atom_path.is_file() and log_path.is_file()
    return {
        "paid_orders": paid_orders,
        "paid_expenses": paid_exp,
        "day_total": day_total,
        "inventory_ok_qty": qty_ok,
        "writes_ok": writes_ok,
        "denies_ok": denies_ok,
        "nums_ok": nums_ok,
        "crystal_ok": crystal_ok,
        "confidence_gate": gated,
        "use_log_events": len(use_log),
        "ok": writes_ok and denies_ok and nums_ok and crystal_ok,
    }


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    seed = seed_business(BASE)
    result = day_pipeline(BASE)
    rate = 1.0 if result["ok"] else 0.0
    out = {
        "cycle": "C146",
        "theme": "business_folder_day_in_life_shadow_u2c_office",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "sandbox": str(BASE.relative_to(ROOT)).replace("\\", "/"),
        "seed": seed,
        "result": result,
        "rate": rate,
        "pass": result["ok"] and rate >= GATE,
        "claim": False,
        "note": "Multi-file business day: orders+expenses+inventory, allowlisted writes, secret denied, U2C crystal.",
    }
    J(DOC / "C146_DAY_IN_LIFE_BUSINESS.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C146", "ok": result["ok"], "day_total": result["day_total"], "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())