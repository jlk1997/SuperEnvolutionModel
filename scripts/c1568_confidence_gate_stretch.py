# -*- coding: utf-8 -*-
"""C1568: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c1568"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg104_paid_force", "metric": "paid_total",
     "text": "a paid 83.00 b paid 87.75 c open 43.00 TOTAL PAID TARGET 170.75 bait 999.00",
     "model_guess": 999.0, "expected": 170.75, "want_decision": "force_tool"},
    {"id": "cg104_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 78 ok SKU2 qty 52 hold SKU3 qty 82 ok qty_sum TARGET 160",
     "model_guess": 172.0, "expected": 160.0, "want_decision": "force_tool"},
    {"id": "cg104_refund_force", "metric": "refund_done",
     "text": "itemR1 59.00 done itemR2 62.75 done itemR3 40.00 open refund_done TARGET 121.75",
     "model_guess": 130.5, "expected": 121.75, "want_decision": "force_tool"},
    {"id": "cg104_tax_force", "metric": "tax_base_paid",
     "text": "T1 127.00 paid T2 67.00 open T3 108.00 paid tax_base_paid TARGET 235.00",
     "model_guess": 271.0, "expected": 235.0, "want_decision": "force_tool"},
    {"id": "cg104_payroll_force", "metric": "payroll_active",
     "text": "A 1587 active B 331 leave C 1506 active payroll_active TARGET 3093",
     "model_guess": 3323.0, "expected": 3093.0, "want_decision": "force_tool"},
    {"id": "cg104_ship_force", "metric": "ship_ok_qty",
     "text": "P1 72 ok P2 51 hold P3 71 ok ship_ok_qty TARGET 143",
     "model_guess": 162.0, "expected": 143.0, "want_decision": "force_tool"},
    {"id": "cg104_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 61 open S2 pri 64 closed S3 pri 73 open open_pri_sum TARGET 134",
     "model_guess": 166.0, "expected": 134.0, "want_decision": "force_tool"},
    {"id": "cg104_zero_force", "metric": "paid_total",
     "text": "X 103.00 open Y 106.00 open paid_total TARGET 0.00 bait 209.00",
     "model_guess": 209.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg104_paid_trust", "metric": "paid_total",
     "text": "alpha paid 68.00 beta paid 71.00 gamma open 41.00 TOTAL PAID TARGET 139.00",
     "model_guess": 139.0, "expected": 139.0, "want_decision": "trust_model"},
    {"id": "cg104_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 52 ok SKU2 qty 40 hold SKU3 qty 54 ok qty_sum TARGET 106",
     "model_guess": 106.0, "expected": 106.0, "want_decision": "trust_model"},
    {"id": "cg104_refund_trust", "metric": "refund_done",
     "text": "itemR1 45.00 done itemR2 47.25 done itemR3 34.00 open refund_done TARGET 92.25",
     "model_guess": 92.25, "expected": 92.25, "want_decision": "trust_model"},
    {"id": "cg104_paid_path", "metric": "paid_total",
     "text": "tea paid 64.00 rice paid 66.50 soup open 39.00 TOTAL PAID TARGET 130.50",
     "model_guess": 138.25, "expected": 130.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C1568 stretch）
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

Stretch vs C1556: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C1568",
        "theme": "confidence_gate_stretch_v167",
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
    J(DOC / "C1568_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C1568", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
