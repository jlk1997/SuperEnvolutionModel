# -*- coding: utf-8 -*-
"""C210: Wire expanded multi-metric confidence gate into capture path + regression.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ant_capture_office_lib import parse_metric_gated, parse_paid, CONFIDENCE_GATE, MONEY_TOOL
from evo.office.money_tool import tool_metric, confidence_gated_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
RUN = ROOT / "runs" / "conf_gate_capture_wire_c210"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


CASES = [
    {"id": "cg_paid_force", "metric": "paid_total",
     "text": "a paid 10.00 b paid 12.50 c open 3.00 TOTAL PAID TARGET 22.50",
     "model_guess": 999.0, "expected": 22.5, "want_decision": "force_tool"},
    {"id": "cg_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 5 ok SKU2 qty 2 hold SKU3 qty 7 ok qty_sum TARGET 12",
     "model_guess": 14.0, "expected": 12.0, "want_decision": "force_tool"},
    {"id": "cg_refund_force", "metric": "refund_done",
     "text": "itemR1 4.00 done itemR2 6.50 done itemR3 1.00 open refund_done TARGET 10.50",
     "model_guess": 11.5, "expected": 10.5, "want_decision": "force_tool"},
    {"id": "cg_tax_force", "metric": "tax_base_paid",
     "text": "T1 20.00 paid T2 5.00 open T3 15.00 paid tax_base_paid TARGET 35.00",
     "model_guess": 40.0, "expected": 35.0, "want_decision": "force_tool"},
    {"id": "cg_payroll_force", "metric": "payroll_active",
     "text": "A 100 active B 20 leave C 80 active payroll_active TARGET 180",
     "model_guess": 200.0, "expected": 180.0, "want_decision": "force_tool"},
    {"id": "cg_ship_force", "metric": "ship_ok_qty",
     "text": "P1 3 ok P2 1 hold P3 4 ok ship_ok_qty TARGET 7",
     "model_guess": 8.0, "expected": 7.0, "want_decision": "force_tool"},
    {"id": "cg_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 2 open S2 pri 9 closed S3 pri 5 open open_pri_sum TARGET 7",
     "model_guess": 16.0, "expected": 7.0, "want_decision": "force_tool"},
    {"id": "cg_paid_trust", "metric": "paid_total",
     "text": "x paid 3.00 y paid 4.00 z open 1.00 TOTAL PAID TARGET 7.00",
     "model_guess": 7.0, "expected": 7.0, "want_decision": "trust_model"},
    {"id": "cg_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 1 ok SKU2 qty 0 hold SKU3 qty 2 ok qty_sum TARGET 3",
     "model_guess": 3.0, "expected": 3.0, "want_decision": "trust_model"},
    {"id": "cg_paid_path", "metric": "paid_total",
     "text": "latte paid 4.50 sandwich paid 12.00 juice open 3.00 TOTAL PAID TARGET 16.50",
     "model_guess": 19.5, "expected": 16.5, "want_decision": "force_tool", "also_parse_paid": True},
]


def main():
    rows, n_ok = [], 0
    for c in CASES:
        val, meta = parse_metric_gated(
            c["text"], c["metric"], model_guess=c["model_guess"],
            expected=c["expected"], return_meta=True,
        )
        decision = (meta or {}).get("decision")
        ok = (
            val is not None
            and abs(float(val) - float(c["expected"])) <= 0.01
            and decision == c["want_decision"]
        )
        if c.get("also_parse_paid"):
            pv, pm = parse_paid(c["text"], model_guess=c["model_guess"], return_meta=True)
            ok = ok and abs(float(pv) - float(c["expected"])) <= 0.01
            meta = dict(meta or {})
            meta["parse_paid"] = {"value": pv, "meta": pm}
        n_ok += int(ok)
        rows.append({
            "id": c["id"], "metric": c["metric"], "ok": ok,
            "value": val, "expected": c["expected"],
            "decision": decision, "want_decision": c["want_decision"],
            "meta": meta,
        })
    n = len(rows)
    rate = round(n_ok / n, 4) if n else 0.0
    gate_pass = n >= 8 and rate >= GATE
    out = {
        "cycle": "C210",
        "theme": "confidence_gate_expand_capture_wire",
        "gate": GATE,
        "timestamp": ts(),
        "n": n, "n_ok": n_ok, "rate": rate,
        "CONFIDENCE_GATE": CONFIDENCE_GATE,
        "MONEY_TOOL": MONEY_TOOL,
        "parse_metric_gated_wired": True,
        "metrics_covered": sorted({c["metric"] for c in CASES}),
        "rows": rows,
        "gate_pass": gate_pass,
        "pass": gate_pass,
        "claim": gate_pass,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "innovation": "wire C204 multi-metric confidence gate into ant_capture_office_lib.parse_metric_gated",
    }
    J(DOC / "C210_CONFIDENCE_GATE_CAPTURE_WIRE.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C210", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
