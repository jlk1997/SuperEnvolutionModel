# -*- coding: utf-8 -*-
"""C1964: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c1964"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg137_paid_force", "metric": "paid_total",
     "text": "a paid 116.00 b paid 120.75 c open 76.00 TOTAL PAID TARGET 236.75 bait 999.00",
     "model_guess": 999.0, "expected": 236.75, "want_decision": "force_tool"},
    {"id": "cg137_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 111 ok SKU2 qty 85 hold SKU3 qty 115 ok qty_sum TARGET 226",
     "model_guess": 238.0, "expected": 226.0, "want_decision": "force_tool"},
    {"id": "cg137_refund_force", "metric": "refund_done",
     "text": "itemR1 92.00 done itemR2 95.75 done itemR3 73.00 open refund_done TARGET 187.75",
     "model_guess": 196.5, "expected": 187.75, "want_decision": "force_tool"},
    {"id": "cg137_tax_force", "metric": "tax_base_paid",
     "text": "T1 160.00 paid T2 100.00 open T3 141.00 paid tax_base_paid TARGET 301.00",
     "model_guess": 337.0, "expected": 301.0, "want_decision": "force_tool"},
    {"id": "cg137_payroll_force", "metric": "payroll_active",
     "text": "A 1653 active B 364 leave C 1539 active payroll_active TARGET 3192",
     "model_guess": 3422.0, "expected": 3192.0, "want_decision": "force_tool"},
    {"id": "cg137_ship_force", "metric": "ship_ok_qty",
     "text": "P1 105 ok P2 84 hold P3 104 ok ship_ok_qty TARGET 209",
     "model_guess": 228.0, "expected": 209.0, "want_decision": "force_tool"},
    {"id": "cg137_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 94 open S2 pri 97 closed S3 pri 106 open open_pri_sum TARGET 200",
     "model_guess": 232.0, "expected": 200.0, "want_decision": "force_tool"},
    {"id": "cg137_zero_force", "metric": "paid_total",
     "text": "X 136.00 open Y 139.00 open paid_total TARGET 0.00 bait 275.00",
     "model_guess": 275.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg137_paid_trust", "metric": "paid_total",
     "text": "alpha paid 101.00 beta paid 104.00 gamma open 74.00 TOTAL PAID TARGET 205.00",
     "model_guess": 205.0, "expected": 205.0, "want_decision": "trust_model"},
    {"id": "cg137_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 85 ok SKU2 qty 73 hold SKU3 qty 87 ok qty_sum TARGET 172",
     "model_guess": 172.0, "expected": 172.0, "want_decision": "trust_model"},
    {"id": "cg137_refund_trust", "metric": "refund_done",
     "text": "itemR1 78.00 done itemR2 80.25 done itemR3 67.00 open refund_done TARGET 158.25",
     "model_guess": 158.25, "expected": 158.25, "want_decision": "trust_model"},
    {"id": "cg137_paid_path", "metric": "paid_total",
     "text": "tea paid 97.00 rice paid 99.50 soup open 72.00 TOTAL PAID TARGET 196.50",
     "model_guess": 204.25, "expected": 196.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C1964 stretch）
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

Stretch vs C1964: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C1964",
        "theme": "confidence_gate_stretch_v200",
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
    J(DOC / "C1964_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C1964", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
