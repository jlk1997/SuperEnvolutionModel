# -*- coding: utf-8 -*-
"""C1268: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c1268"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg79_paid_force", "metric": "paid_total",
     "text": "a paid 58.00 b paid 62.75 c open 18.00 TOTAL PAID TARGET 120.75 bait 999.00",
     "model_guess": 999.0, "expected": 120.75, "want_decision": "force_tool"},
    {"id": "cg79_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 53 ok SKU2 qty 27 hold SKU3 qty 57 ok qty_sum TARGET 110",
     "model_guess": 122.0, "expected": 110.0, "want_decision": "force_tool"},
    {"id": "cg79_refund_force", "metric": "refund_done",
     "text": "itemR1 34.00 done itemR2 37.75 done itemR3 15.00 open refund_done TARGET 71.75",
     "model_guess": 80.5, "expected": 71.75, "want_decision": "force_tool"},
    {"id": "cg79_tax_force", "metric": "tax_base_paid",
     "text": "T1 102.00 paid T2 42.00 open T3 83.00 paid tax_base_paid TARGET 185.00",
     "model_guess": 221.0, "expected": 185.0, "want_decision": "force_tool"},
    {"id": "cg79_payroll_force", "metric": "payroll_active",
     "text": "A 1551 active B 306 leave C 1481 active payroll_active TARGET 3032",
     "model_guess": 3262.0, "expected": 3032.0, "want_decision": "force_tool"},
    {"id": "cg79_ship_force", "metric": "ship_ok_qty",
     "text": "P1 47 ok P2 26 hold P3 46 ok ship_ok_qty TARGET 93",
     "model_guess": 112.0, "expected": 93.0, "want_decision": "force_tool"},
    {"id": "cg79_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 36 open S2 pri 39 closed S3 pri 48 open open_pri_sum TARGET 84",
     "model_guess": 116.0, "expected": 84.0, "want_decision": "force_tool"},
    {"id": "cg79_zero_force", "metric": "paid_total",
     "text": "X 78.00 open Y 81.00 open paid_total TARGET 0.00 bait 159.00",
     "model_guess": 159.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg79_paid_trust", "metric": "paid_total",
     "text": "alpha paid 43.00 beta paid 46.00 gamma open 16.00 TOTAL PAID TARGET 89.00",
     "model_guess": 89.0, "expected": 89.0, "want_decision": "trust_model"},
    {"id": "cg79_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 27 ok SKU2 qty 15 hold SKU3 qty 29 ok qty_sum TARGET 56",
     "model_guess": 56.0, "expected": 56.0, "want_decision": "trust_model"},
    {"id": "cg79_refund_trust", "metric": "refund_done",
     "text": "itemR1 20.00 done itemR2 22.25 done itemR3 9.00 open refund_done TARGET 42.25",
     "model_guess": 42.25, "expected": 42.25, "want_decision": "trust_model"},
    {"id": "cg79_paid_path", "metric": "paid_total",
     "text": "tea paid 39.00 rice paid 41.50 soup open 14.00 TOTAL PAID TARGET 80.50",
     "model_guess": 88.25, "expected": 80.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C1268 stretch）
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

Stretch vs C1256: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C1268",
        "theme": "confidence_gate_stretch_v142",
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
    J(DOC / "C1268_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C1268", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
