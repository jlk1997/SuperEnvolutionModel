# -*- coding: utf-8 -*-
"""C2048: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c2048"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg144_paid_force", "metric": "paid_total",
     "text": "a paid 123.00 b paid 127.75 c open 83.00 TOTAL PAID TARGET 250.75 bait 999.00",
     "model_guess": 999.0, "expected": 250.75, "want_decision": "force_tool"},
    {"id": "cg144_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 118 ok SKU2 qty 92 hold SKU3 qty 122 ok qty_sum TARGET 240",
     "model_guess": 252.0, "expected": 240.0, "want_decision": "force_tool"},
    {"id": "cg144_refund_force", "metric": "refund_done",
     "text": "itemR1 99.00 done itemR2 102.75 done itemR3 80.00 open refund_done TARGET 201.75",
     "model_guess": 210.5, "expected": 201.75, "want_decision": "force_tool"},
    {"id": "cg144_tax_force", "metric": "tax_base_paid",
     "text": "T1 167.00 paid T2 107.00 open T3 148.00 paid tax_base_paid TARGET 315.00",
     "model_guess": 351.0, "expected": 315.0, "want_decision": "force_tool"},
    {"id": "cg144_payroll_force", "metric": "payroll_active",
     "text": "A 1662 active B 371 leave C 1546 active payroll_active TARGET 3208",
     "model_guess": 3438.0, "expected": 3208.0, "want_decision": "force_tool"},
    {"id": "cg144_ship_force", "metric": "ship_ok_qty",
     "text": "P1 112 ok P2 91 hold P3 111 ok ship_ok_qty TARGET 223",
     "model_guess": 242.0, "expected": 223.0, "want_decision": "force_tool"},
    {"id": "cg144_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 101 open S2 pri 104 closed S3 pri 113 open open_pri_sum TARGET 214",
     "model_guess": 246.0, "expected": 214.0, "want_decision": "force_tool"},
    {"id": "cg144_zero_force", "metric": "paid_total",
     "text": "X 143.00 open Y 146.00 open paid_total TARGET 0.00 bait 289.00",
     "model_guess": 289.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg144_paid_trust", "metric": "paid_total",
     "text": "alpha paid 108.00 beta paid 111.00 gamma open 81.00 TOTAL PAID TARGET 219.00",
     "model_guess": 219.0, "expected": 219.0, "want_decision": "trust_model"},
    {"id": "cg144_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 92 ok SKU2 qty 80 hold SKU3 qty 94 ok qty_sum TARGET 186",
     "model_guess": 186.0, "expected": 186.0, "want_decision": "trust_model"},
    {"id": "cg144_refund_trust", "metric": "refund_done",
     "text": "itemR1 85.00 done itemR2 87.25 done itemR3 74.00 open refund_done TARGET 172.25",
     "model_guess": 172.25, "expected": 172.25, "want_decision": "trust_model"},
    {"id": "cg144_paid_path", "metric": "paid_total",
     "text": "tea paid 104.00 rice paid 106.50 soup open 79.00 TOTAL PAID TARGET 210.50",
     "model_guess": 218.25, "expected": 210.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C2048 stretch）
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

Stretch vs C2048: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C2048",
        "theme": "confidence_gate_stretch_v207",
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
    J(DOC / "C2048_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C2048", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
