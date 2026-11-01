# -*- coding: utf-8 -*-
"""C1424: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c1424"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg92_paid_force", "metric": "paid_total",
     "text": "a paid 71.00 b paid 75.75 c open 31.00 TOTAL PAID TARGET 146.75 bait 999.00",
     "model_guess": 999.0, "expected": 146.75, "want_decision": "force_tool"},
    {"id": "cg92_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 66 ok SKU2 qty 40 hold SKU3 qty 70 ok qty_sum TARGET 136",
     "model_guess": 148.0, "expected": 136.0, "want_decision": "force_tool"},
    {"id": "cg92_refund_force", "metric": "refund_done",
     "text": "itemR1 47.00 done itemR2 50.75 done itemR3 28.00 open refund_done TARGET 97.75",
     "model_guess": 106.5, "expected": 97.75, "want_decision": "force_tool"},
    {"id": "cg92_tax_force", "metric": "tax_base_paid",
     "text": "T1 115.00 paid T2 55.00 open T3 96.00 paid tax_base_paid TARGET 211.00",
     "model_guess": 247.0, "expected": 211.0, "want_decision": "force_tool"},
    {"id": "cg92_payroll_force", "metric": "payroll_active",
     "text": "A 1565 active B 319 leave C 1494 active payroll_active TARGET 3059",
     "model_guess": 3289.0, "expected": 3059.0, "want_decision": "force_tool"},
    {"id": "cg92_ship_force", "metric": "ship_ok_qty",
     "text": "P1 60 ok P2 39 hold P3 59 ok ship_ok_qty TARGET 119",
     "model_guess": 138.0, "expected": 119.0, "want_decision": "force_tool"},
    {"id": "cg92_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 49 open S2 pri 52 closed S3 pri 61 open open_pri_sum TARGET 110",
     "model_guess": 142.0, "expected": 110.0, "want_decision": "force_tool"},
    {"id": "cg92_zero_force", "metric": "paid_total",
     "text": "X 91.00 open Y 94.00 open paid_total TARGET 0.00 bait 185.00",
     "model_guess": 185.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg92_paid_trust", "metric": "paid_total",
     "text": "alpha paid 56.00 beta paid 59.00 gamma open 29.00 TOTAL PAID TARGET 115.00",
     "model_guess": 115.0, "expected": 115.0, "want_decision": "trust_model"},
    {"id": "cg92_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 40 ok SKU2 qty 28 hold SKU3 qty 42 ok qty_sum TARGET 82",
     "model_guess": 82.0, "expected": 82.0, "want_decision": "trust_model"},
    {"id": "cg92_refund_trust", "metric": "refund_done",
     "text": "itemR1 33.00 done itemR2 35.25 done itemR3 22.00 open refund_done TARGET 68.25",
     "model_guess": 68.25, "expected": 68.25, "want_decision": "trust_model"},
    {"id": "cg92_paid_path", "metric": "paid_total",
     "text": "tea paid 52.00 rice paid 54.50 soup open 27.00 TOTAL PAID TARGET 106.50",
     "model_guess": 114.25, "expected": 106.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C1424 stretch）
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

Stretch vs C1412: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C1424",
        "theme": "confidence_gate_stretch_v155",
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
    J(DOC / "C1424_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C1424", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
