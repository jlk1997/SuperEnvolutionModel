# -*- coding: utf-8 -*-
"""C1784: Non-vision knife — confidence-gate stretch + money_tool agree cases.
Gate 0.6. Gate2/3 untouched. gen11 HOLD. No fake VL scores.
"""
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ant_capture_office_lib import parse_metric_gated, parse_paid, CONFIDENCE_GATE, MONEY_TOOL
from evo.office.money_tool import sum_paid_from_text

GATE = 0.6
DOC = ROOT / "docs" / "r50"
RUN = ROOT / "runs" / "conf_gate_stretch_c1784"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg122_paid_force", "metric": "paid_total",
     "text": "a paid 101.00 b paid 105.75 c open 61.00 TOTAL PAID TARGET 206.75 bait 999.00",
     "model_guess": 999.0, "expected": 206.75, "want_decision": "force_tool"},
    {"id": "cg122_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 96 ok SKU2 qty 70 hold SKU3 qty 100 ok qty_sum TARGET 196",
     "model_guess": 208.0, "expected": 196.0, "want_decision": "force_tool"},
    {"id": "cg122_refund_force", "metric": "refund_done",
     "text": "itemR1 77.00 done itemR2 80.75 done itemR3 58.00 open refund_done TARGET 157.75",
     "model_guess": 166.5, "expected": 157.75, "want_decision": "force_tool"},
    {"id": "cg122_tax_force", "metric": "tax_base_paid",
     "text": "T1 145.00 paid T2 85.00 open T3 126.00 paid tax_base_paid TARGET 271.00",
     "model_guess": 307.0, "expected": 271.0, "want_decision": "force_tool"},
    {"id": "cg122_payroll_force", "metric": "payroll_active",
     "text": "A 1623 active B 349 leave C 1524 active payroll_active TARGET 3147",
     "model_guess": 3377.0, "expected": 3147.0, "want_decision": "force_tool"},
    {"id": "cg122_ship_force", "metric": "ship_ok_qty",
     "text": "P1 90 ok P2 69 hold P3 89 ok ship_ok_qty TARGET 179",
     "model_guess": 198.0, "expected": 179.0, "want_decision": "force_tool"},
    {"id": "cg122_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 79 open S2 pri 82 closed S3 pri 91 open open_pri_sum TARGET 170",
     "model_guess": 202.0, "expected": 170.0, "want_decision": "force_tool"},
    {"id": "cg122_zero_force", "metric": "paid_total",
     "text": "X 121.00 open Y 124.00 open paid_total TARGET 0.00 bait 245.00",
     "model_guess": 245.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg122_paid_trust", "metric": "paid_total",
     "text": "alpha paid 86.00 beta paid 89.00 gamma open 59.00 TOTAL PAID TARGET 175.00",
     "model_guess": 175.0, "expected": 175.0, "want_decision": "trust_model"},
    {"id": "cg122_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 70 ok SKU2 qty 58 hold SKU3 qty 72 ok qty_sum TARGET 142",
     "model_guess": 142.0, "expected": 142.0, "want_decision": "trust_model"},
    {"id": "cg122_refund_trust", "metric": "refund_done",
     "text": "itemR1 63.00 done itemR2 65.25 done itemR3 52.00 open refund_done TARGET 128.25",
     "model_guess": 128.25, "expected": 128.25, "want_decision": "trust_model"},
    {"id": "cg122_paid_path", "metric": "paid_total",
     "text": "tea paid 82.00 rice paid 84.50 soup open 57.00 TOTAL PAID TARGET 166.50",
     "model_guess": 174.25, "expected": 166.50, "want_decision": "force_tool", "also_parse_paid": True},
]



def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
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
            tool = sum_paid_from_text(c["text"])
            ok = ok and abs(float(pv) - float(c["expected"])) <= 0.01
            ok = ok and tool is not None and abs(float(tool) - float(c["expected"])) <= 0.08
            meta = dict(meta or {})
            meta["parse_paid"] = {"value": pv, "meta": pm, "tool": tool}
        n_ok += int(ok)
        rows.append({
            "id": c["id"], "metric": c["metric"], "ok": ok,
            "value": val, "expected": c["expected"],
            "decision": decision, "want_decision": c["want_decision"],
            "meta": meta,
        })
    n = len(rows)
    rate = round(n_ok / n, 4) if n else 0.0
    gate_pass = n >= 10 and rate >= GATE and CONFIDENCE_GATE and MONEY_TOOL
    md = f"""# 蚁算 Confidence-Gated Capture（C1784 stretch）
Updated: {ts()} (Asia/Shanghai)

| 项 | 值 |
| --- | --- |
| n / n_ok / rate | {n} / {n_ok} / {rate} |
| CONFIDENCE_GATE | {CONFIDENCE_GATE} |
| MONEY_TOOL | {MONEY_TOOL} |
| pass | {gate_pass} |
| metrics | {sorted({c['metric'] for c in CASES})} |
| gen11 | HOLD |
| Gate2/3 | untouched |
| Gate | {GATE} |

Stretch vs C1784: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C1784",
        "theme": "confidence_gate_stretch_v185",
        "gate": GATE,
        "timestamp": ts(),
        "n": n, "n_ok": n_ok, "rate": rate,
        "CONFIDENCE_GATE": CONFIDENCE_GATE,
        "MONEY_TOOL": MONEY_TOOL,
        "metrics_covered": sorted({c["metric"] for c in CASES}),
        "rows": rows,
        "gate_pass": gate_pass,
        "pass": gate_pass,
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "note": "Non-vision confidence-gate knife; no VL claim",
    }
    J(DOC / "C1784_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C1784", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
