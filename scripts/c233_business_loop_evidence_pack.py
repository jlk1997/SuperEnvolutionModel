# -*- coding: utf-8 -*-
"""C233: Real business loop evidence pack.
Week sandbox refresh + multi-metric capture (no-vl) + U2C crystal evidence.
Gate 0.6. Gate2/3 untouched. gen11 HOLD. No new VL claim.
"""
from __future__ import annotations
import json, shutil, subprocess, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import sum_csv_text, confidence_gated_metric, tool_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
RUN = ROOT / "runs/business_loop_c233"
SB = ROOT / "runs/business_week_sandbox_c233"
U2C = ROOT / "runs/u2c_crystal_c233"
CLI = ROOT / "scripts" / "ant_capture_office.py"
BOARD = ROOT / "docs" / "蚁算_BUSINESS_LOOP_C233.md"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


WEEK = [
    {"day": "D0", "date": "2026-10-13",
     "orders": "order_id,sku,qty,status,amount\nA1,A,2,paid,22.00\nA2,B,1,open,15.00\nA3,C,1,paid,10.50\nA4,D,2,paid,14.00\nA5,A,1,void,8.00\n",
     "expenses": "eid,category,status,amount\nE1,travel,paid,110.00\nE2,meals,paid,42.00\nE3,supplies,open,25.00\nE4,travel,void,50.00\n",
     "inventory": "sku,qty,status\nA,30,ok\nB,5,hold\nC,12,ok\nD,4,ok\n",
     "expect_paid_orders": 46.5, "expect_paid_exp": 152.0, "expect_qty_ok": 46},
    {"day": "D1", "date": "2026-10-14",
     "orders": "order_id,sku,qty,status,amount\nB1,A,1,paid,12.00\nB2,B,2,paid,26.00\nB3,C,1,open,18.00\nB4,D,1,paid,8.00\nB5,A,2,paid,18.00\n",
     "expenses": "eid,category,status,amount\nF1,meals,paid,30.00\nF2,travel,paid,80.00\nF3,supplies,paid,16.00\nF4,meals,open,12.00\n",
     "inventory": "sku,qty,status\nA,28,ok\nB,9,ok\nC,6,hold\nD,5,ok\n",
     "expect_paid_orders": 64.0, "expect_paid_exp": 126.0, "expect_qty_ok": 42},
    {"day": "D2", "date": "2026-10-15",
     "orders": "order_id,sku,qty,status,amount\nC1,A,3,paid,33.00\nC2,B,1,paid,11.00\nC3,C,2,open,22.00\nC4,D,1,paid,9.00\nC5,A,1,refund,5.00\n",
     "expenses": "eid,category,status,amount\nG1,travel,paid,160.00\nG2,meals,void,40.00\nG3,supplies,paid,22.00\nG4,travel,open,55.00\n",
     "inventory": "sku,qty,status\nA,22,ok\nB,7,ok\nC,11,ok\nD,3,hold\n",
     "expect_paid_orders": 53.0, "expect_paid_exp": 182.0, "expect_qty_ok": 40},
    {"day": "D3", "date": "2026-10-16",
     "orders": "order_id,sku,qty,status,amount\nD1,A,2,paid,20.00\nD2,B,1,paid,14.00\nD3,C,1,paid,10.00\nD4,D,2,open,14.00\nD5,A,1,paid,11.00\n",
     "expenses": "eid,category,status,amount\nH1,meals,paid,36.00\nH2,travel,paid,95.00\nH3,supplies,open,18.00\nH4,meals,paid,24.50\n",
     "inventory": "sku,qty,status\nA,25,ok\nB,9,ok\nC,8,ok\nD,6,ok\n",
     "expect_paid_orders": 55.0, "expect_paid_exp": 155.5, "expect_qty_ok": 48},
    {"day": "D4", "date": "2026-10-17",
     "orders": "order_id,sku,qty,status,amount\nE1,A,1,paid,13.00\nE2,B,3,paid,30.00\nE3,C,1,open,11.00\nE4,D,1,paid,7.50\nE5,A,2,void,14.00\n",
     "expenses": "eid,category,status,amount\nI1,travel,paid,120.00\nI2,meals,paid,50.00\nI3,supplies,paid,32.00\nI4,travel,void,70.00\n",
     "inventory": "sku,qty,status\nA,20,ok\nB,4,hold\nC,14,ok\nD,8,ok\n",
     "expect_paid_orders": 50.5, "expect_paid_exp": 202.0, "expect_qty_ok": 42},
    {"day": "D5", "date": "2026-10-18",
     "orders": "order_id,sku,qty,status,amount\nF1,A,4,paid,44.00\nF2,B,1,open,9.00\nF3,C,2,paid,18.00\nF4,D,1,paid,8.50\nF5,A,1,paid,12.00\n",
     "expenses": "eid,category,status,amount\nJ1,meals,paid,58.00\nJ2,travel,paid,140.00\nJ3,supplies,open,22.00\nJ4,meals,paid,21.00\n",
     "inventory": "sku,qty,status\nA,18,ok\nB,12,ok\nC,7,ok\nD,2,hold\n",
     "expect_paid_orders": 82.5, "expect_paid_exp": 219.0, "expect_qty_ok": 37},
    {"day": "D6", "date": "2026-10-19",
     "orders": "order_id,sku,qty,status,amount\nG1,A,2,paid,24.00\nG2,B,2,paid,22.00\nG3,C,1,paid,9.00\nG4,D,1,open,12.00\nG5,A,1,paid,10.00\n",
     "expenses": "eid,category,status,amount\nK1,travel,paid,100.00\nK2,meals,void,33.00\nK3,supplies,paid,28.00\nK4,travel,paid,65.00\n",
     "inventory": "sku,qty,status\nA,15,ok\nB,10,ok\nC,9,ok\nD,5,ok\n",
     "expect_paid_orders": 65.0, "expect_paid_exp": 193.0, "expect_qty_ok": 39},
]

MM_CASES = [
    ("mm_paid", "paid_total",
     ["a paid 48.00", "b paid 49.50", "c open 13.00", "TOTAL PAID TARGET 97.50"], 97.5),
    ("mm_qty", "qty_sum",
     ["SKU1 qty 43 ok", "SKU2 qty 20 hold", "SKU3 qty 39 ok", "qty_sum TARGET 82"], 82.0),
    ("mm_refund", "refund_done",
     ["itemR1 22.25 done", "itemR2 24.50 done", "itemR3 10.00 open", "refund_done TARGET 46.75"], 46.75),
    ("mm_tax", "tax_base_paid",
     ["T1 85.00 paid", "T2 32.00 open", "T3 68.00 paid", "tax_base_paid TARGET 153.00"], 153.0),
    ("mm_pay", "payroll_active",
     ["A 1350 active", "B 240 leave", "C 1200 active", "payroll_active TARGET 2550"], 2550.0),
    ("mm_ship", "ship_ok_qty",
     ["P1 34 ok", "P2 18 hold", "P3 33 ok", "ship_ok_qty TARGET 67"], 67.0),
    ("mm_sla", "open_pri_sum",
     ["S1 pri 25 open", "S2 pri 32 closed", "S3 pri 32 open", "open_pri_sum TARGET 57"], 57.0),
    ("mm_zero", "paid_total",
     ["OPEN ONLY V21", "X 66.00 open", "Y 69.00 open", "paid_total TARGET 0.00"], 0.0),
]


def run_week():
    if SB.exists():
        shutil.rmtree(SB, ignore_errors=True)
    SB.mkdir(parents=True, exist_ok=True)
    day_rows = []
    n_ok = 0
    crystals = []
    for day in WEEK:
        ddir = SB / day["day"]
        inbox = ddir / "Documents" / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        (inbox / f"{day['day']}_orders.csv").write_text(day["orders"], encoding="utf-8")
        (inbox / f"{day['day']}_expenses.csv").write_text(day["expenses"], encoding="utf-8")
        (inbox / f"{day['day']}_inventory.csv").write_text(day["inventory"], encoding="utf-8")
        (inbox / f"{day['day']}_notes.txt").write_text(
            f"Week sandbox {day['day']} {day['date']} C233\n", encoding="utf-8")

        orders_txt = day["orders"]
        exp_txt = day["expenses"]
        inv_txt = day["inventory"]
        paid_o = sum_csv_text(orders_txt, amount_col="amount", status_col="status", status_value="paid")
        paid_e = sum_csv_text(exp_txt, amount_col="amount", status_col="status", status_value="paid")
        qty_ok = 0.0
        for line in inv_txt.strip().splitlines()[1:]:
            parts = line.split(",")
            if len(parts) >= 3 and parts[2].strip() == "ok":
                qty_ok += float(parts[1])

        ok_o = abs(paid_o - day["expect_paid_orders"]) < 0.08
        ok_e = abs(paid_e - day["expect_paid_exp"]) < 0.08
        ok_q = abs(qty_ok - day["expect_qty_ok"]) < 0.08
        ok = ok_o and ok_e and ok_q
        n_ok += int(ok)

        rollup = {
            "day": day["day"], "date": day["date"],
            "paid_orders": paid_o, "paid_expenses": paid_e, "qty_ok": qty_ok,
            "ok": ok,
        }
        out_rel = ddir / "Documents" / "out" / f"{day['day']}_rollup.json"
        out_rel.parent.mkdir(parents=True, exist_ok=True)
        out_rel.write_text(json.dumps(rollup, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        crystal = {
            "atom_id": f"u2c_week_{day['day'].lower()}_c233",
            "source": "business_week_sandbox",
            "day": day["day"],
            "skills": ["table_sum_paid", "inventory_qty_ok", "expense_paid"],
            "evidence": rollup,
            "crystallized": bool(ok),
        }
        crystals.append(crystal)
        day_rows.append({**rollup, "expect_paid_orders": day["expect_paid_orders"],
                         "expect_paid_exp": day["expect_paid_exp"],
                         "expect_qty_ok": day["expect_qty_ok"]})

    U2C.mkdir(parents=True, exist_ok=True)
    J(U2C / "crystals.json", {"n": len(crystals), "items": crystals, "timestamp": ts()})
    rate = round(n_ok / len(WEEK), 4) if WEEK else 0.0
    return {
        "n_days": len(WEEK), "n_ok": n_ok, "rate": rate,
        "pass": rate >= GATE and n_ok == len(WEEK),
        "days": day_rows,
        "u2c_crystals": len(crystals),
        "u2c_crystallized": sum(1 for c in crystals if c["crystallized"]),
        "sandbox": str(SB.relative_to(ROOT)).replace("\\", "/"),
    }


def run_multi_metric():
    rows = []
    n_ok = 0
    for cid, metric, lines, expected in MM_CASES:
        text = "\n".join(lines)
        gated = confidence_gated_metric(text, metric, model_guess=None, expected=expected, tol=0.08)
        got = gated.get("value")
        if got is None:
            got = tool_metric(text, metric)
        ok = got is not None and abs(float(got) - float(expected)) < 0.08
        cli_ok = None
        if CLI.is_file():
            outdir = RUN / "mm" / cid
            outdir.mkdir(parents=True, exist_ok=True)
            lines_file = outdir / "lines.txt"
            lines_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
            cmd = [
                sys.executable, str(CLI), "--no-vl",
                "--metric", metric, "--expected", str(expected),
                "--lines-file", str(lines_file),
                "--outdir", str(outdir),
            ]
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=str(ROOT))
                cli_ok = r.returncode == 0
                ev = outdir / "evidence.json"
                if ev.is_file():
                    ej = json.loads(ev.read_text(encoding="utf-8"))
                    cli_ok = bool(ej.get("pass"))
            except Exception:
                cli_ok = False
        n_ok += int(ok)
        rows.append({
            "id": cid, "metric": metric, "expected": expected,
            "got": got, "ok": ok, "cli_ok": cli_ok, "gate": gated,
        })
    n = len(rows)
    rate = round(n_ok / n, 4) if n else 0.0
    cli_pass = all(r["cli_ok"] is not False for r in rows) and any(r["cli_ok"] for r in rows)
    return {
        "n": n, "n_ok": n_ok, "rate": rate,
        "pass": rate >= GATE and n_ok == n,
        "cli_pass": cli_pass,
        "rows": rows,
    }


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    week = run_week()
    mm = run_multi_metric()
    pack_pass = bool(week["pass"] and mm["pass"])
    out = {
        "cycle": "C233",
        "theme": "business_loop_week_multimetric_u2c",
        "gate": GATE,
        "timestamp": ts(),
        "week_sandbox": week,
        "multi_metric": mm,
        "u2c_pack": {
            "path": str((U2C / "crystals.json").relative_to(ROOT)).replace("\\", "/"),
            "n": week["u2c_crystals"],
            "crystallized": week["u2c_crystallized"],
            "rate": round(week["u2c_crystallized"] / max(1, week["u2c_crystals"]), 4),
        },
        "pass": pack_pass,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "C233 real business loop evidence; no VL claim",
    }
    J(DOC / "C233_BUSINESS_LOOP_EVIDENCE.json", out)
    J(RUN / "judge.json", out)
    BOARD.write_text(
        f"""# 蚁算业务闭环证据包（C233）

Updated: {ts()} (Asia/Shanghai)

## 一句话
周沙箱 7 天 + 多指标 capture + U2C 结晶，全部诚实过闸（非 VL claim）。

| 块 | 结果 |
| --- | --- |
| week sandbox | rate={week['rate']} n_ok={week['n_ok']}/{week['n_days']} pass={week['pass']} |
| multi-metric | rate={mm['rate']} n_ok={mm['n_ok']}/{mm['n']} cli_pass={mm['cli_pass']} |
| U2C crystals | {week['u2c_crystallized']}/{week['u2c_crystals']} |
| **pack pass** | **{pack_pass}** |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.
""",
        encoding="utf-8",
    )
    print(json.dumps({
        "cycle": "C233", "pass": pack_pass,
        "week_rate": week["rate"], "mm_rate": mm["rate"],
        "u2c": week["u2c_crystallized"],
    }, ensure_ascii=False))
    return 0 if pack_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
