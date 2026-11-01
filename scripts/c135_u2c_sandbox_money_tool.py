# -*- coding: utf-8 -*-
"""C135: U2C growth on real sandbox with money_tool. Crystallize atoms from use_log.
No fake absorb claim. Gate 0.6. gen11 HOLD.
"""
from __future__ import annotations
import csv, json, shutil, hashlib, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import sum_csv_text, prefer_tool_over_lora

GATE = 0.6
BASE = ROOT / "runs" / "u2c_sandbox_money_c135"
DOC = ROOT / "docs" / "r50"

SESSIONS = [
    {"sid": "m01_orders", "csv": "Documents/inbox/orders.csv",
     "header": ["order_id", "amount", "status"],
     "rows": [("O1", 14.5, "paid"), ("O2", 9.0, "open"), ("O3", 21.0, "paid"), ("O4", 6.5, "paid")],
     "metric": "paid_total", "expected": 42.0},
    {"sid": "m02_refunds", "csv": "Documents/inbox/refunds.csv",
     "header": ["rid", "amount", "status"],
     "rows": [("R1", 3.5, "done"), ("R2", 6.0, "open"), ("R3", 2.5, "done")],
     "metric": "refund_done", "expected": 6.0, "status_value": "done"},
    {"sid": "m03_tax", "csv": "Documents/inbox/tax.csv",
     "header": ["tid", "amount", "status"],
     "rows": [("T1", 10.0, "paid"), ("T2", 7.5, "open"), ("T3", 12.5, "paid")],
     "metric": "tax_base_paid", "expected": 22.5},
    {"sid": "m04_expense", "csv": "Documents/inbox/expense.csv",
     "header": ["eid", "amount", "status"],
     "rows": [("E1", 40.0, "paid"), ("E2", 15.0, "void"), ("E3", 18.0, "paid")],
     "metric": "paid_total", "expected": 58.0},
    {"sid": "m05_mixed_cn", "csv": "Documents/inbox/mixed.csv",
     "header": ["sku", "amount", "status"],
     "rows": [("咖啡", 4.5, "paid"), ("茶", 3.0, "paid"), ("饼", 8.0, "open")],
     "metric": "paid_total", "expected": 7.5},
    {"sid": "m06_open_zero", "csv": "Documents/inbox/opens.csv",
     "header": ["xid", "amount", "status"],
     "rows": [("X", 19.0, "open"), ("Y", 11.0, "open")],
     "metric": "paid_total", "expected": 0.0},
    {"sid": "m07_freight", "csv": "Documents/inbox/freight.csv",
     "header": ["leg", "amount", "status"],
     "rows": [("L1", 22.0, "paid"), ("L2", 18.0, "paid"), ("L3", 5.0, "open")],
     "metric": "paid_total", "expected": 40.0},
    {"sid": "m08_subs", "csv": "Documents/inbox/subs.csv",
     "header": ["plan", "amount", "status"],
     "rows": [("A", 9.99, "paid"), ("B", 14.99, "paid"), ("trial", 0.0, "open")],
     "metric": "paid_total", "expected": 24.98},
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_session(base: Path, spec: dict) -> dict:
    sb = base / "sessions" / spec["sid"] / "sandbox"
    if sb.parent.exists():
        shutil.rmtree(sb.parent)
    sb.mkdir(parents=True)
    p = sb / spec["csv"]
    p.parent.mkdir(parents=True, exist_ok=True)
    status_value = spec.get("status_value", "paid")
    # for refund_done use status done
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(spec["header"])
        for row in spec["rows"]:
            w.writerow(row)
    csv_text = p.read_text(encoding="utf-8")
    # money_tool path
    if spec["metric"] in ("paid_total", "tax_base_paid") or status_value == "paid":
        got = sum_csv_text(csv_text, amount_col=spec["header"][1], status_col=spec["header"][2], status_value=status_value)
    else:
        got = sum_csv_text(csv_text, amount_col=spec["header"][1], status_col=spec["header"][2], status_value=status_value)
    # write allowlisted crystal
    reports = sb / "Documents" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    out_csv = reports / f"{spec['metric']}.csv"
    out_csv.write_text(f"metric,value\n{spec['metric']},{got:.2f}\n", encoding="utf-8")
    (sb / "out.txt").write_text(f"{spec['metric']}={got:.2f}\nmoney_tool=true\n", encoding="utf-8")
    use_log = [
        {"phase": "use", "task": spec["metric"], "path": spec["csv"], "ok": True},
        {"phase": "tool", "money_tool": True, "got": got, "expected": spec["expected"]},
        {"phase": "grade", "ok": abs(got - spec["expected"]) < 0.08},
    ]
    atom = {
        "atom": f"u2c_money_{spec['sid']}",
        "family": "table",
        "source": "c135_sandbox_money_tool",
        "metric": spec["metric"],
        "gold": spec["expected"],
        "got": got,
        "status": "crystallized" if abs(got - spec["expected"]) < 0.08 else "failed",
        "money_tool": True,
        "policy": prefer_tool_over_lora(),
        "use_log_hash": hashlib.sha256(json.dumps(use_log, sort_keys=True).encode()).hexdigest()[:16],
    }
    atom_path = base / "atoms" / f"{spec['sid']}.json"
    J(atom_path, atom)
    J(base / "sessions" / spec["sid"] / "use_log.json", {"sid": spec["sid"], "use_log": use_log})
    ok = abs(got - spec["expected"]) < 0.08
    return {
        "sid": spec["sid"],
        "ok": ok,
        "got": got,
        "expected": spec["expected"],
        "atom": str(atom_path.relative_to(ROOT)).replace("\\", "/"),
        "money_tool": True,
    }


def main():
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)
    (BASE / "atoms").mkdir(parents=True)

    rows = []
    n_ok = 0
    for spec in SESSIONS:
        r = run_session(BASE, spec)
        rows.append(r)
        n_ok += int(r["ok"])

    n = len(rows)
    rate = n_ok / n if n else 0.0
    # growth vs prior C92 (6 sessions) — we have 8
    growth = {
        "n_sessions": n,
        "n_ok": n_ok,
        "prior_c92_sessions": 6,
        "delta_sessions": n - 6,
        "crystallized": n_ok,
        "absorb_claim": False,
        "reason": "C120 ceiling: format OK, arith unreliable — money_tool preferred; no absorb claim",
    }
    out = {
        "cycle": "C135",
        "theme": "u2c_sandbox_growth_money_tool",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "rows": rows,
        "growth": growth,
        "rate": round(rate, 4),
        "pass": rate >= GATE,
        "claim": False,
        "absorb_claim": False,
        "note": "Real sandbox sessions crystallize with money_tool. No fake LoRA absorb claim.",
    }
    J(DOC / "C135_U2C_SANDBOX_MONEY_TOOL.json", out)
    J(BASE / "judge.json", out)
    print(json.dumps({
        "cycle": "C135",
        "rate": round(rate, 4),
        "n": n,
        "n_ok": n_ok,
        "pass": out["pass"],
        "absorb_claim": False,
    }, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
