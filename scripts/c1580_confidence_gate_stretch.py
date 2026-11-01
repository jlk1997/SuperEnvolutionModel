# -*- coding: utf-8 -*-
"""C1580: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c1580"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg105_paid_force", "metric": "paid_total",
     "text": "a paid 84.00 b paid 88.75 c open 44.00 TOTAL PAID TARGET 172.75 bait 999.00",
     "model_guess": 999.0, "expected": 172.75, "want_decision": "force_tool"},
    {"id": "cg105_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 79 ok SKU2 qty 53 hold SKU3 qty 83 ok qty_sum TARGET 162",
     "model_guess": 174.0, "expected": 162.0, "want_decision": "force_tool"},
    {"id": "cg105_refund_force", "metric": "refund_done",
     "text": "itemR1 60.00 done itemR2 63.75 done itemR3 41.00 open refund_done TARGET 123.75",
     "model_guess": 132.5, "expected": 123.75, "want_decision": "force_tool"},
    {"id": "cg105_tax_force", "metric": "tax_base_paid",
     "text": "T1 128.00 paid T2 68.00 open T3 109.00 paid tax_base_paid TARGET 237.00",
     "model_guess": 273.0, "expected": 237.0, "want_decision": "force_tool"},
    {"id": "cg105_payroll_force", "metric": "payroll_active",
     "text": "A 1589 active B 332 leave C 1507 active payroll_active TARGET 3096",
     "model_guess": 3326.0, "expected": 3096.0, "want_decision": "force_tool"},
    {"id": "cg105_ship_force", "metric": "ship_ok_qty",
     "text": "P1 73 ok P2 52 hold P3 72 ok ship_ok_qty TARGET 145",
     "model_guess": 164.0, "expected": 145.0, "want_decision": "force_tool"},
    {"id": "cg105_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 62 open S2 pri 65 closed S3 pri 74 open open_pri_sum TARGET 136",
     "model_guess": 168.0, "expected": 136.0, "want_decision": "force_tool"},
    {"id": "cg105_zero_force", "metric": "paid_total",
     "text": "X 104.00 open Y 107.00 open paid_total TARGET 0.00 bait 211.00",
     "model_guess": 211.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg105_paid_trust", "metric": "paid_total",
     "text": "alpha paid 69.00 beta paid 72.00 gamma open 42.00 TOTAL PAID TARGET 141.00",
     "model_guess": 141.0, "expected": 141.0, "want_decision": "trust_model"},
    {"id": "cg105_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 53 ok SKU2 qty 41 hold SKU3 qty 55 ok qty_sum TARGET 108",
     "model_guess": 108.0, "expected": 108.0, "want_decision": "trust_model"},
    {"id": "cg105_refund_trust", "metric": "refund_done",
     "text": "itemR1 46.00 done itemR2 48.25 done itemR3 35.00 open refund_done TARGET 94.25",
     "model_guess": 94.25, "expected": 94.25, "want_decision": "trust_model"},
    {"id": "cg105_paid_path", "metric": "paid_total",
     "text": "tea paid 65.00 rice paid 67.50 soup open 40.00 TOTAL PAID TARGET 132.50",
     "model_guess": 140.25, "expected": 132.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C1580 stretch）
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

Stretch vs C1568: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C1580",
        "theme": "confidence_gate_stretch_v168",
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
    J(DOC / "C1580_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C1580", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
