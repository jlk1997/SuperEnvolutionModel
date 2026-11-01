# -*- coding: utf-8 -*-
"""C2084: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c2084"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg147_paid_force", "metric": "paid_total",
     "text": "a paid 126.00 b paid 130.75 c open 86.00 TOTAL PAID TARGET 256.75 bait 999.00",
     "model_guess": 999.0, "expected": 256.75, "want_decision": "force_tool"},
    {"id": "cg147_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 121 ok SKU2 qty 95 hold SKU3 qty 125 ok qty_sum TARGET 246",
     "model_guess": 258.0, "expected": 246.0, "want_decision": "force_tool"},
    {"id": "cg147_refund_force", "metric": "refund_done",
     "text": "itemR1 102.00 done itemR2 105.75 done itemR3 83.00 open refund_done TARGET 207.75",
     "model_guess": 216.5, "expected": 207.75, "want_decision": "force_tool"},
    {"id": "cg147_tax_force", "metric": "tax_base_paid",
     "text": "T1 170.00 paid T2 110.00 open T3 151.00 paid tax_base_paid TARGET 321.00",
     "model_guess": 357.0, "expected": 321.0, "want_decision": "force_tool"},
    {"id": "cg147_payroll_force", "metric": "payroll_active",
     "text": "A 1665 active B 374 leave C 1549 active payroll_active TARGET 3214",
     "model_guess": 3444.0, "expected": 3214.0, "want_decision": "force_tool"},
    {"id": "cg147_ship_force", "metric": "ship_ok_qty",
     "text": "P1 115 ok P2 94 hold P3 114 ok ship_ok_qty TARGET 229",
     "model_guess": 248.0, "expected": 229.0, "want_decision": "force_tool"},
    {"id": "cg147_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 104 open S2 pri 107 closed S3 pri 116 open open_pri_sum TARGET 220",
     "model_guess": 252.0, "expected": 220.0, "want_decision": "force_tool"},
    {"id": "cg147_zero_force", "metric": "paid_total",
     "text": "X 146.00 open Y 149.00 open paid_total TARGET 0.00 bait 295.00",
     "model_guess": 295.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg147_paid_trust", "metric": "paid_total",
     "text": "alpha paid 111.00 beta paid 114.00 gamma open 84.00 TOTAL PAID TARGET 225.00",
     "model_guess": 225.0, "expected": 225.0, "want_decision": "trust_model"},
    {"id": "cg147_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 95 ok SKU2 qty 83 hold SKU3 qty 97 ok qty_sum TARGET 192",
     "model_guess": 192.0, "expected": 192.0, "want_decision": "trust_model"},
    {"id": "cg147_refund_trust", "metric": "refund_done",
     "text": "itemR1 88.00 done itemR2 90.25 done itemR3 77.00 open refund_done TARGET 178.25",
     "model_guess": 178.25, "expected": 178.25, "want_decision": "trust_model"},
    {"id": "cg147_paid_path", "metric": "paid_total",
     "text": "tea paid 107.00 rice paid 109.50 soup open 82.00 TOTAL PAID TARGET 216.50",
     "model_guess": 224.25, "expected": 216.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C2084 stretch）
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

Stretch vs C2084: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C2084",
        "theme": "confidence_gate_stretch_v210",
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
    J(DOC / "C2084_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C2084", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
