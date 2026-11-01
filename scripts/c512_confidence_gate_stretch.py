# -*- coding: utf-8 -*-
"""C512: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c512"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg49_paid_force", "metric": "paid_total",
     "text": "a paid 57.00 b paid 61.75 c open 17.00 TOTAL PAID TARGET 118.75 bait 999.00",
     "model_guess": 999.0, "expected": 118.75, "want_decision": "force_tool"},
    {"id": "cg49_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 52 ok SKU2 qty 26 hold SKU3 qty 56 ok qty_sum TARGET 108",
     "model_guess": 120.0, "expected": 108.0, "want_decision": "force_tool"},
    {"id": "cg49_refund_force", "metric": "refund_done",
     "text": "itemR1 33.00 done itemR2 36.75 done itemR3 14.00 open refund_done TARGET 69.75",
     "model_guess": 78.5, "expected": 69.75, "want_decision": "force_tool"},
    {"id": "cg49_tax_force", "metric": "tax_base_paid",
     "text": "T1 101.00 paid T2 41.00 open T3 82.00 paid tax_base_paid TARGET 183.00",
     "model_guess": 219.0, "expected": 183.0, "want_decision": "force_tool"},
    {"id": "cg49_payroll_force", "metric": "payroll_active",
     "text": "A 1550 active B 305 leave C 1480 active payroll_active TARGET 3030",
     "model_guess": 3260.0, "expected": 3030.0, "want_decision": "force_tool"},
    {"id": "cg49_ship_force", "metric": "ship_ok_qty",
     "text": "P1 46 ok P2 25 hold P3 45 ok ship_ok_qty TARGET 91",
     "model_guess": 110.0, "expected": 91.0, "want_decision": "force_tool"},
    {"id": "cg49_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 35 open S2 pri 38 closed S3 pri 47 open open_pri_sum TARGET 82",
     "model_guess": 114.0, "expected": 82.0, "want_decision": "force_tool"},
    {"id": "cg49_zero_force", "metric": "paid_total",
     "text": "X 77.00 open Y 80.00 open paid_total TARGET 0.00 bait 157.00",
     "model_guess": 157.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg49_paid_trust", "metric": "paid_total",
     "text": "alpha paid 42.00 beta paid 45.00 gamma open 15.00 TOTAL PAID TARGET 87.00",
     "model_guess": 87.0, "expected": 87.0, "want_decision": "trust_model"},
    {"id": "cg49_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 26 ok SKU2 qty 14 hold SKU3 qty 28 ok qty_sum TARGET 54",
     "model_guess": 54.0, "expected": 54.0, "want_decision": "trust_model"},
    {"id": "cg49_refund_trust", "metric": "refund_done",
     "text": "itemR1 19.00 done itemR2 21.25 done itemR3 8.00 open refund_done TARGET 40.25",
     "model_guess": 40.25, "expected": 40.25, "want_decision": "trust_model"},
    {"id": "cg49_paid_path", "metric": "paid_total",
     "text": "tea paid 38.00 rice paid 40.50 soup open 13.00 TOTAL PAID TARGET 78.50",
     "model_guess": 86.25, "expected": 78.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C512 stretch）
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

Stretch vs C210: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C512",
        "theme": "confidence_gate_stretch_v49",
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
    J(DOC / "C512_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C512", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
