# -*- coding: utf-8 -*-
"""C1700: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c1700"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg115_paid_force", "metric": "paid_total",
     "text": "a paid 94.00 b paid 98.75 c open 54.00 TOTAL PAID TARGET 192.75 bait 999.00",
     "model_guess": 999.0, "expected": 192.75, "want_decision": "force_tool"},
    {"id": "cg115_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 89 ok SKU2 qty 63 hold SKU3 qty 93 ok qty_sum TARGET 182",
     "model_guess": 194.0, "expected": 182.0, "want_decision": "force_tool"},
    {"id": "cg115_refund_force", "metric": "refund_done",
     "text": "itemR1 70.00 done itemR2 73.75 done itemR3 51.00 open refund_done TARGET 143.75",
     "model_guess": 152.5, "expected": 143.75, "want_decision": "force_tool"},
    {"id": "cg115_tax_force", "metric": "tax_base_paid",
     "text": "T1 138.00 paid T2 78.00 open T3 119.00 paid tax_base_paid TARGET 257.00",
     "model_guess": 293.0, "expected": 257.0, "want_decision": "force_tool"},
    {"id": "cg115_payroll_force", "metric": "payroll_active",
     "text": "A 1609 active B 342 leave C 1517 active payroll_active TARGET 3126",
     "model_guess": 3356.0, "expected": 3126.0, "want_decision": "force_tool"},
    {"id": "cg115_ship_force", "metric": "ship_ok_qty",
     "text": "P1 83 ok P2 62 hold P3 82 ok ship_ok_qty TARGET 165",
     "model_guess": 184.0, "expected": 165.0, "want_decision": "force_tool"},
    {"id": "cg115_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 72 open S2 pri 75 closed S3 pri 84 open open_pri_sum TARGET 156",
     "model_guess": 188.0, "expected": 156.0, "want_decision": "force_tool"},
    {"id": "cg115_zero_force", "metric": "paid_total",
     "text": "X 114.00 open Y 117.00 open paid_total TARGET 0.00 bait 231.00",
     "model_guess": 231.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg115_paid_trust", "metric": "paid_total",
     "text": "alpha paid 79.00 beta paid 82.00 gamma open 52.00 TOTAL PAID TARGET 161.00",
     "model_guess": 161.0, "expected": 161.0, "want_decision": "trust_model"},
    {"id": "cg115_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 63 ok SKU2 qty 51 hold SKU3 qty 65 ok qty_sum TARGET 128",
     "model_guess": 128.0, "expected": 128.0, "want_decision": "trust_model"},
    {"id": "cg115_refund_trust", "metric": "refund_done",
     "text": "itemR1 56.00 done itemR2 58.25 done itemR3 45.00 open refund_done TARGET 114.25",
     "model_guess": 114.25, "expected": 114.25, "want_decision": "trust_model"},
    {"id": "cg115_paid_path", "metric": "paid_total",
     "text": "tea paid 75.00 rice paid 77.50 soup open 50.00 TOTAL PAID TARGET 152.50",
     "model_guess": 160.25, "expected": 152.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C1700 stretch）
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

Stretch vs C1700: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C1700",
        "theme": "confidence_gate_stretch_v178",
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
    J(DOC / "C1700_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C1700", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
