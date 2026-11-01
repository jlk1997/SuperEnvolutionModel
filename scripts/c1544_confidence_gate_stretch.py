# -*- coding: utf-8 -*-
"""C1544: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c1544"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg102_paid_force", "metric": "paid_total",
     "text": "a paid 81.00 b paid 85.75 c open 41.00 TOTAL PAID TARGET 166.75 bait 999.00",
     "model_guess": 999.0, "expected": 166.75, "want_decision": "force_tool"},
    {"id": "cg102_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 76 ok SKU2 qty 50 hold SKU3 qty 80 ok qty_sum TARGET 156",
     "model_guess": 168.0, "expected": 156.0, "want_decision": "force_tool"},
    {"id": "cg102_refund_force", "metric": "refund_done",
     "text": "itemR1 57.00 done itemR2 60.75 done itemR3 38.00 open refund_done TARGET 117.75",
     "model_guess": 126.5, "expected": 117.75, "want_decision": "force_tool"},
    {"id": "cg102_tax_force", "metric": "tax_base_paid",
     "text": "T1 125.00 paid T2 65.00 open T3 106.00 paid tax_base_paid TARGET 231.00",
     "model_guess": 267.0, "expected": 231.0, "want_decision": "force_tool"},
    {"id": "cg102_payroll_force", "metric": "payroll_active",
     "text": "A 1583 active B 329 leave C 1504 active payroll_active TARGET 3087",
     "model_guess": 3317.0, "expected": 3087.0, "want_decision": "force_tool"},
    {"id": "cg102_ship_force", "metric": "ship_ok_qty",
     "text": "P1 70 ok P2 49 hold P3 69 ok ship_ok_qty TARGET 139",
     "model_guess": 158.0, "expected": 139.0, "want_decision": "force_tool"},
    {"id": "cg102_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 59 open S2 pri 62 closed S3 pri 71 open open_pri_sum TARGET 130",
     "model_guess": 162.0, "expected": 130.0, "want_decision": "force_tool"},
    {"id": "cg102_zero_force", "metric": "paid_total",
     "text": "X 101.00 open Y 104.00 open paid_total TARGET 0.00 bait 205.00",
     "model_guess": 205.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg102_paid_trust", "metric": "paid_total",
     "text": "alpha paid 66.00 beta paid 69.00 gamma open 39.00 TOTAL PAID TARGET 135.00",
     "model_guess": 135.0, "expected": 135.0, "want_decision": "trust_model"},
    {"id": "cg102_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 50 ok SKU2 qty 38 hold SKU3 qty 52 ok qty_sum TARGET 102",
     "model_guess": 102.0, "expected": 102.0, "want_decision": "trust_model"},
    {"id": "cg102_refund_trust", "metric": "refund_done",
     "text": "itemR1 43.00 done itemR2 45.25 done itemR3 32.00 open refund_done TARGET 88.25",
     "model_guess": 88.25, "expected": 88.25, "want_decision": "trust_model"},
    {"id": "cg102_paid_path", "metric": "paid_total",
     "text": "tea paid 62.00 rice paid 64.50 soup open 37.00 TOTAL PAID TARGET 126.50",
     "model_guess": 134.25, "expected": 126.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C1544 stretch）
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

Stretch vs C1532: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C1544",
        "theme": "confidence_gate_stretch_v165",
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
    J(DOC / "C1544_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C1544", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
