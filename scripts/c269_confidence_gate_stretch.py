# -*- coding: utf-8 -*-
"""C269: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c269"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg27_paid_force", "metric": "paid_total",
     "text": "a paid 49.00 b paid 53.25 c open 14.00 TOTAL PAID TARGET 102.25 bait 999.00",
     "model_guess": 999.0, "expected": 102.25, "want_decision": "force_tool"},
    {"id": "cg27_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 45 ok SKU2 qty 21 hold SKU3 qty 49 ok qty_sum TARGET 94",
     "model_guess": 115.0, "expected": 94.0, "want_decision": "force_tool"},
    {"id": "cg27_refund_force", "metric": "refund_done",
     "text": "itemR1 29.00 done itemR2 32.50 done itemR3 12.00 open refund_done TARGET 61.50",
     "model_guess": 73.5, "expected": 61.5, "want_decision": "force_tool"},
    {"id": "cg27_tax_force", "metric": "tax_base_paid",
     "text": "T1 96.00 paid T2 38.00 open T3 77.00 paid tax_base_paid TARGET 173.00",
     "model_guess": 211.0, "expected": 173.0, "want_decision": "force_tool"},
    {"id": "cg27_payroll_force", "metric": "payroll_active",
     "text": "A 1490 active B 280 leave C 1420 active payroll_active TARGET 2910",
     "model_guess": 3190.0, "expected": 2910.0, "want_decision": "force_tool"},
    {"id": "cg27_ship_force", "metric": "ship_ok_qty",
     "text": "P1 42 ok P2 22 hold P3 41 ok ship_ok_qty TARGET 83",
     "model_guess": 105.0, "expected": 83.0, "want_decision": "force_tool"},
    {"id": "cg27_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 31 open S2 pri 34 closed S3 pri 43 open open_pri_sum TARGET 74",
     "model_guess": 108.0, "expected": 74.0, "want_decision": "force_tool"},
    {"id": "cg27_zero_force", "metric": "paid_total",
     "text": "X 71.00 open Y 74.00 open paid_total TARGET 0.00 bait 145.00",
     "model_guess": 145.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg27_paid_trust", "metric": "paid_total",
     "text": "alpha paid 38.00 beta paid 41.00 gamma open 13.00 TOTAL PAID TARGET 79.00",
     "model_guess": 79.0, "expected": 79.0, "want_decision": "trust_model"},
    {"id": "cg27_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 22 ok SKU2 qty 11 hold SKU3 qty 25 ok qty_sum TARGET 47",
     "model_guess": 47.0, "expected": 47.0, "want_decision": "trust_model"},
    {"id": "cg27_refund_trust", "metric": "refund_done",
     "text": "itemR1 16.00 done itemR2 18.50 done itemR3 6.00 open refund_done TARGET 34.50",
     "model_guess": 34.5, "expected": 34.5, "want_decision": "trust_model"},
    {"id": "cg27_paid_path", "metric": "paid_total",
     "text": "tea paid 34.00 rice paid 36.25 soup open 11.00 TOTAL PAID TARGET 70.25",
     "model_guess": 81.25, "expected": 70.25, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C269 stretch）
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

Stretch vs C210: V27 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C269",
        "theme": "confidence_gate_stretch_v27",
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
    J(DOC / "C269_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C269", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
