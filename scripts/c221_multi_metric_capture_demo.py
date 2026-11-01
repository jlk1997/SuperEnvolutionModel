# -*- coding: utf-8 -*-
"""C221: Innovation — multi-metric capture demo.
One capture session evaluates paid_total / qty_sum / refund_done / tax_base_paid /
payroll_active / ship_ok_qty / open_pri_sum under confidence gate (tool wins on disagree).
Gate 0.6. Gate2/3 untouched. gen11 HOLD. No new VL claim.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import tool_metric, confidence_gated_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
RUN = ROOT / "runs/multi_metric_capture_c221"
BOARD = ROOT / "docs" / "蚁算_MULTI_METRIC_CAPTURE.md"

CASES = [
    {
        "id": "mm_paid",
        "metric": "paid_total",
        "text": "a paid 46.00 b paid 47.50 c open 12.00 TOTAL PAID TARGET 93.50",
        "expected": 93.5,
        "wrong_model": 120.0,
    },
    {
        "id": "mm_qty",
        "metric": "qty_sum",
        "text": "SKU1 qty 41 ok SKU2 qty 19 hold SKU3 qty 37 ok qty_sum TARGET 78",
        "expected": 78.0,
        "wrong_model": 60.0,
    },
    {
        "id": "mm_refund",
        "metric": "refund_done",
        "text": "itemR1 21.25 done itemR2 23.50 done itemR3 9.00 open refund_done TARGET 44.75",
        "expected": 44.75,
        "wrong_model": 50.0,
    },
    {
        "id": "mm_tax",
        "metric": "tax_base_paid",
        "text": "T1 82.00 paid T2 30.00 open T3 65.00 paid tax_base_paid TARGET 147.00",
        "expected": 147.0,
        "wrong_model": 100.0,
    },
    {
        "id": "mm_pay",
        "metric": "payroll_active",
        "text": "A 1310 active B 220 leave C 1170 active payroll_active TARGET 2480",
        "expected": 2480.0,
        "wrong_model": 2000.0,
    },
    {
        "id": "mm_ship",
        "metric": "ship_ok_qty",
        "text": "P1 32 ok P2 17 hold P3 31 ok ship_ok_qty TARGET 63",
        "expected": 63.0,
        "wrong_model": 80.0,
    },
    {
        "id": "mm_sla",
        "metric": "open_pri_sum",
        "text": "S1 pri 24 open S2 pri 31 closed S3 pri 31 open open_pri_sum TARGET 55",
        "expected": 55.0,
        "wrong_model": 86.0,
    },
    {
        "id": "mm_zero",
        "metric": "paid_total",
        "text": "X 61.00 open Y 64.00 open paid_total TARGET 0.00",
        "expected": 0.0,
        "wrong_model": 125.0,
    },
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    rows, n_ok = [], 0
    for c in CASES:
        tool = tool_metric(c["text"], c["metric"])
        gated = confidence_gated_metric(
            c["text"], c["metric"], model_guess=c["wrong_model"], expected=c["expected"], tol=0.08,
        )
        agree = confidence_gated_metric(
            c["text"], c["metric"], model_guess=c["expected"], expected=c["expected"], tol=0.08,
        )
        ok = (
            tool is not None
            and abs(float(tool) - c["expected"]) <= 0.08
            and gated.get("decision") == "force_tool"
            and abs(float(gated["value"]) - c["expected"]) <= 0.08
            and agree.get("decision") in ("trust_model", "agree_prefer_tool", "fallback_tool")
        )
        n_ok += int(ok)
        rows.append({
            "id": c["id"], "metric": c["metric"], "expected": c["expected"],
            "tool": tool, "force": gated, "agree": agree, "ok": ok,
        })

    n = len(rows)
    rate = round(n_ok / n, 4) if n else 0.0
    gate_pass = n >= 6 and rate >= GATE
    out = {
        "cycle": "C221",
        "theme": "multi_metric_capture_demo",
        "gate": GATE,
        "timestamp": ts(),
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "rows": rows,
        "innovation": "multi_metric_confidence_gated_capture",
        "metrics_covered": sorted({c["metric"] for c in CASES}),
        "pass": gate_pass,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "Product demo: multi-metric capture + confidence gate force_tool on disagree",
    }
    J(DOC / "C221_MULTI_METRIC_CAPTURE_DEMO.json", out)
    J(RUN / "judge.json", out)
    BOARD.write_text(
        f"""# 蚁算 MULTI-METRIC CAPTURE

Updated: {ts()} (Asia/Shanghai)

Innovation C221: one capture path covers multiple office metrics under confidence gate.

| Metric | Rate note |
| --- | --- |
| overall | {rate} ({n_ok}/{n}) |
| metrics | {', '.join(sorted({c['metric'] for c in CASES}))} |

Rule: when model disagrees with tool on expected metric → **force_tool**.
Gate 0.6. Gate2/3 untouched. gen11 HOLD. No VL claim.
""",
        encoding="utf-8",
    )
    print(json.dumps({
        "cycle": "C221", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass,
        "metrics": out["metrics_covered"],
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
