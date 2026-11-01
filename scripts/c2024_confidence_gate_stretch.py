# -*- coding: utf-8 -*-
"""C2024: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c2024"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg142_paid_force", "metric": "paid_total",
     "text": "a paid 121.00 b paid 125.75 c open 81.00 TOTAL PAID TARGET 246.75 bait 999.00",
     "model_guess": 999.0, "expected": 246.75, "want_decision": "force_tool"},
    {"id": "cg142_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 116 ok SKU2 qty 90 hold SKU3 qty 120 ok qty_sum TARGET 236",
     "model_guess": 248.0, "expected": 236.0, "want_decision": "force_tool"},
    {"id": "cg142_refund_force", "metric": "refund_done",
     "text": "itemR1 97.00 done itemR2 100.75 done itemR3 78.00 open refund_done TARGET 197.75",
     "model_guess": 206.5, "expected": 197.75, "want_decision": "force_tool"},
    {"id": "cg142_tax_force", "metric": "tax_base_paid",
     "text": "T1 165.00 paid T2 105.00 open T3 146.00 paid tax_base_paid TARGET 311.00",
     "model_guess": 347.0, "expected": 311.0, "want_decision": "force_tool"},
    {"id": "cg142_payroll_force", "metric": "payroll_active",
     "text": "A 1660 active B 369 leave C 1544 active payroll_active TARGET 3204",
     "model_guess": 3434.0, "expected": 3204.0, "want_decision": "force_tool"},
    {"id": "cg142_ship_force", "metric": "ship_ok_qty",
     "text": "P1 110 ok P2 89 hold P3 109 ok ship_ok_qty TARGET 219",
     "model_guess": 238.0, "expected": 219.0, "want_decision": "force_tool"},
    {"id": "cg142_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 99 open S2 pri 102 closed S3 pri 111 open open_pri_sum TARGET 210",
     "model_guess": 242.0, "expected": 210.0, "want_decision": "force_tool"},
    {"id": "cg142_zero_force", "metric": "paid_total",
     "text": "X 141.00 open Y 144.00 open paid_total TARGET 0.00 bait 285.00",
     "model_guess": 285.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg142_paid_trust", "metric": "paid_total",
     "text": "alpha paid 106.00 beta paid 109.00 gamma open 79.00 TOTAL PAID TARGET 215.00",
     "model_guess": 215.0, "expected": 215.0, "want_decision": "trust_model"},
    {"id": "cg142_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 90 ok SKU2 qty 78 hold SKU3 qty 92 ok qty_sum TARGET 182",
     "model_guess": 182.0, "expected": 182.0, "want_decision": "trust_model"},
    {"id": "cg142_refund_trust", "metric": "refund_done",
     "text": "itemR1 83.00 done itemR2 85.25 done itemR3 72.00 open refund_done TARGET 168.25",
     "model_guess": 168.25, "expected": 168.25, "want_decision": "trust_model"},
    {"id": "cg142_paid_path", "metric": "paid_total",
     "text": "tea paid 102.00 rice paid 104.50 soup open 77.00 TOTAL PAID TARGET 206.50",
     "model_guess": 214.25, "expected": 206.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C2024 stretch）
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

Stretch vs C2024: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C2024",
        "theme": "confidence_gate_stretch_v205",
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
    J(DOC / "C2024_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C2024", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
