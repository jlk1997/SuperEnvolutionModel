# -*- coding: utf-8 -*-
"""C1712: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c1712"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg116_paid_force", "metric": "paid_total",
     "text": "a paid 95.00 b paid 99.75 c open 55.00 TOTAL PAID TARGET 194.75 bait 999.00",
     "model_guess": 999.0, "expected": 194.75, "want_decision": "force_tool"},
    {"id": "cg116_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 90 ok SKU2 qty 64 hold SKU3 qty 94 ok qty_sum TARGET 184",
     "model_guess": 196.0, "expected": 184.0, "want_decision": "force_tool"},
    {"id": "cg116_refund_force", "metric": "refund_done",
     "text": "itemR1 71.00 done itemR2 74.75 done itemR3 52.00 open refund_done TARGET 145.75",
     "model_guess": 154.5, "expected": 145.75, "want_decision": "force_tool"},
    {"id": "cg116_tax_force", "metric": "tax_base_paid",
     "text": "T1 139.00 paid T2 79.00 open T3 120.00 paid tax_base_paid TARGET 259.00",
     "model_guess": 295.0, "expected": 259.0, "want_decision": "force_tool"},
    {"id": "cg116_payroll_force", "metric": "payroll_active",
     "text": "A 1611 active B 343 leave C 1518 active payroll_active TARGET 3129",
     "model_guess": 3359.0, "expected": 3129.0, "want_decision": "force_tool"},
    {"id": "cg116_ship_force", "metric": "ship_ok_qty",
     "text": "P1 84 ok P2 63 hold P3 83 ok ship_ok_qty TARGET 167",
     "model_guess": 186.0, "expected": 167.0, "want_decision": "force_tool"},
    {"id": "cg116_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 73 open S2 pri 76 closed S3 pri 85 open open_pri_sum TARGET 158",
     "model_guess": 190.0, "expected": 158.0, "want_decision": "force_tool"},
    {"id": "cg116_zero_force", "metric": "paid_total",
     "text": "X 115.00 open Y 118.00 open paid_total TARGET 0.00 bait 233.00",
     "model_guess": 233.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg116_paid_trust", "metric": "paid_total",
     "text": "alpha paid 80.00 beta paid 83.00 gamma open 53.00 TOTAL PAID TARGET 163.00",
     "model_guess": 163.0, "expected": 163.0, "want_decision": "trust_model"},
    {"id": "cg116_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 64 ok SKU2 qty 52 hold SKU3 qty 66 ok qty_sum TARGET 130",
     "model_guess": 130.0, "expected": 130.0, "want_decision": "trust_model"},
    {"id": "cg116_refund_trust", "metric": "refund_done",
     "text": "itemR1 57.00 done itemR2 59.25 done itemR3 46.00 open refund_done TARGET 116.25",
     "model_guess": 116.25, "expected": 116.25, "want_decision": "trust_model"},
    {"id": "cg116_paid_path", "metric": "paid_total",
     "text": "tea paid 76.00 rice paid 78.50 soup open 51.00 TOTAL PAID TARGET 154.50",
     "model_guess": 162.25, "expected": 154.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C1712 stretch）
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

Stretch vs C1712: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C1712",
        "theme": "confidence_gate_stretch_v179",
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
    J(DOC / "C1712_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C1712", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
