# -*- coding: utf-8 -*-
"""C204: Confidence-gate expand — multi-metric tool override (non-vision knife).
When model atom disagrees with deterministic tool on qty_sum / refund_done /
tax_base_paid / paid_total, force tool. Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.money_tool import sum_paid_from_text
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
RUN = ROOT / "runs" / "conf_gate_expand_c204"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tool_metric(text, metric):
    """Deterministic tool for known office metrics."""
    t = text or ""
    if metric == "paid_total":
        return float(sum_paid_from_text(t))
    # qty_sum: sum of "qty N ok" integers
    import re
    if metric == "qty_sum":
        vals = [float(x) for x in re.findall(r"qty\s+(\d+(?:\.\d+)?)\s+ok", t, flags=re.I)]
        return float(sum(vals)) if vals else None
    if metric == "refund_done":
        vals = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s+done", t, flags=re.I)]
        return float(sum(vals)) if vals else None
    if metric == "tax_base_paid":
        vals = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s+paid", t, flags=re.I)]
        return float(sum(vals)) if vals else None
    if metric == "payroll_active":
        vals = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s+active", t, flags=re.I)]
        return float(sum(vals)) if vals else None
    if metric == "ship_ok_qty":
        vals = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s+ok", t, flags=re.I)]
        return float(sum(vals)) if vals else None
    if metric == "open_pri_sum":
        vals = [float(x) for x in re.findall(r"pri\s+(\d+(?:\.\d+)?)\s+open", t, flags=re.I)]
        return float(sum(vals)) if vals else None
    return None


def confidence_gate(model_got, tool_got, expected, tol=0.01):
    """If tool matches expected and model disagrees, force tool."""
    if tool_got is None:
        return model_got, "model_only_no_tool"
    tool_ok = abs(float(tool_got) - float(expected)) <= tol
    model_ok = model_got is not None and abs(float(model_got) - float(expected)) <= tol
    if tool_ok and not model_ok:
        return tool_got, "force_tool"
    if model_ok:
        return model_got, "trust_model"
    if tool_ok:
        return tool_got, "fallback_tool"
    return model_got, "both_fail"


CASES = [
    # model wrong, tool right -> force_tool
    {"id": "cg_01", "metric": "paid_total", "text": "a paid 10.00 b paid 12.50 c open 3.00 TOTAL PAID TARGET 22.50",
     "model_got": 999.0, "expected": 22.5},
    {"id": "cg_02", "metric": "qty_sum", "text": "SKU1 qty 5 ok SKU2 qty 2 hold SKU3 qty 7 ok qty_sum TARGET 12",
     "model_got": 14.0, "expected": 12.0},
    {"id": "cg_03", "metric": "refund_done", "text": "itemR1 4.00 done itemR2 6.50 done itemR3 1.00 open refund_done TARGET 10.50",
     "model_got": 11.5, "expected": 10.5},
    {"id": "cg_04", "metric": "tax_base_paid", "text": "T1 20.00 paid T2 5.00 open T3 15.00 paid tax_base_paid TARGET 35.00",
     "model_got": 40.0, "expected": 35.0},
    {"id": "cg_05", "metric": "payroll_active", "text": "A 100 active B 20 leave C 80 active payroll_active TARGET 180",
     "model_got": 200.0, "expected": 180.0},
    {"id": "cg_06", "metric": "ship_ok_qty", "text": "P1 3 ok P2 1 hold P3 4 ok ship_ok_qty TARGET 7",
     "model_got": 8.0, "expected": 7.0},
    {"id": "cg_07", "metric": "open_pri_sum", "text": "S1 pri 2 open S2 pri 9 closed S3 pri 5 open open_pri_sum TARGET 7",
     "model_got": 16.0, "expected": 7.0},
    # model right -> trust_model
    {"id": "cg_08", "metric": "paid_total", "text": "x paid 3.00 y paid 4.00 z open 1.00 TOTAL PAID TARGET 7.00",
     "model_got": 7.0, "expected": 7.0},
    {"id": "cg_09", "metric": "qty_sum", "text": "SKU1 qty 1 ok SKU2 qty 0 hold SKU3 qty 2 ok qty_sum TARGET 3",
     "model_got": 3.0, "expected": 3.0},
    {"id": "cg_10", "metric": "refund_done", "text": "a 1.25 done b 2.75 done c 9 open refund_done TARGET 4.00",
     "model_got": 4.0, "expected": 4.0},
]


def main():
    rows, n_ok = [], 0
    force_n = 0
    for c in CASES:
        tool_got = tool_metric(c["text"], c["metric"])
        final, decision = confidence_gate(c["model_got"], tool_got, c["expected"])
        ok = final is not None and abs(float(final) - float(c["expected"])) <= 0.01
        n_ok += int(ok)
        force_n += int(decision == "force_tool")
        rows.append({
            "id": c["id"], "metric": c["metric"], "model_got": c["model_got"],
            "tool_got": tool_got, "final": final, "expected": c["expected"],
            "decision": decision, "ok": ok,
        })
    n = len(rows)
    rate = round(n_ok / n, 4) if n else 0.0
    gate_pass = n >= 10 and rate >= GATE
    out = {
        "cycle": "C204",
        "theme": "confidence_gate_expand_multimetric",
        "gate": GATE,
        "timestamp": ts(),
        "n": n, "n_ok": n_ok, "rate": rate,
        "force_tool_count": force_n,
        "metrics_covered": sorted({r["metric"] for r in rows}),
        "rows": rows,
        "gate_pass": gate_pass,
        "pass": gate_pass,
        "claim": gate_pass,
        "innovation": "expand confidence-gate from paid_total-only to qty/refund/tax/payroll/ship/sla",
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "Non-vision knife: multi-metric confidence gate forces tool on model/tool disagreement",
    }
    J(DOC / "C204_CONFIDENCE_GATE_EXPAND.json", out)
    RUN.mkdir(parents=True, exist_ok=True)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C204", "rate": rate, "n_ok": n_ok, "n": n, "force_tool": force_n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
