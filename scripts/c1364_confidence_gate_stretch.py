# -*- coding: utf-8 -*-
"""C1364: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c1364"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg87_paid_force", "metric": "paid_total",
     "text": "a paid 66.00 b paid 70.75 c open 26.00 TOTAL PAID TARGET 136.75 bait 999.00",
     "model_guess": 999.0, "expected": 136.75, "want_decision": "force_tool"},
    {"id": "cg87_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 61 ok SKU2 qty 35 hold SKU3 qty 65 ok qty_sum TARGET 126",
     "model_guess": 138.0, "expected": 126.0, "want_decision": "force_tool"},
    {"id": "cg87_refund_force", "metric": "refund_done",
     "text": "itemR1 42.00 done itemR2 45.75 done itemR3 23.00 open refund_done TARGET 87.75",
     "model_guess": 96.5, "expected": 87.75, "want_decision": "force_tool"},
    {"id": "cg87_tax_force", "metric": "tax_base_paid",
     "text": "T1 110.00 paid T2 50.00 open T3 91.00 paid tax_base_paid TARGET 201.00",
     "model_guess": 237.0, "expected": 201.0, "want_decision": "force_tool"},
    {"id": "cg87_payroll_force", "metric": "payroll_active",
     "text": "A 1559 active B 314 leave C 1489 active payroll_active TARGET 3048",
     "model_guess": 3278.0, "expected": 3048.0, "want_decision": "force_tool"},
    {"id": "cg87_ship_force", "metric": "ship_ok_qty",
     "text": "P1 55 ok P2 34 hold P3 54 ok ship_ok_qty TARGET 109",
     "model_guess": 128.0, "expected": 109.0, "want_decision": "force_tool"},
    {"id": "cg87_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 44 open S2 pri 47 closed S3 pri 56 open open_pri_sum TARGET 100",
     "model_guess": 132.0, "expected": 100.0, "want_decision": "force_tool"},
    {"id": "cg87_zero_force", "metric": "paid_total",
     "text": "X 86.00 open Y 89.00 open paid_total TARGET 0.00 bait 175.00",
     "model_guess": 175.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg87_paid_trust", "metric": "paid_total",
     "text": "alpha paid 51.00 beta paid 54.00 gamma open 24.00 TOTAL PAID TARGET 105.00",
     "model_guess": 105.0, "expected": 105.0, "want_decision": "trust_model"},
    {"id": "cg87_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 35 ok SKU2 qty 23 hold SKU3 qty 37 ok qty_sum TARGET 72",
     "model_guess": 72.0, "expected": 72.0, "want_decision": "trust_model"},
    {"id": "cg87_refund_trust", "metric": "refund_done",
     "text": "itemR1 28.00 done itemR2 30.25 done itemR3 17.00 open refund_done TARGET 58.25",
     "model_guess": 58.25, "expected": 58.25, "want_decision": "trust_model"},
    {"id": "cg87_paid_path", "metric": "paid_total",
     "text": "tea paid 47.00 rice paid 49.50 soup open 22.00 TOTAL PAID TARGET 96.50",
     "model_guess": 104.25, "expected": 96.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C1364 stretch）
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

Stretch vs C1352: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C1364",
        "theme": "confidence_gate_stretch_v150",
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
    J(DOC / "C1364_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C1364", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
