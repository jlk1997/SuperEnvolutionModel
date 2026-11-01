# -*- coding: utf-8 -*-
"""C1868: Non-vision knife — confidence-gate stretch + money_tool agree cases.
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
RUN = ROOT / "runs" / "conf_gate_stretch_c1868"
BOARD = ROOT / "docs" / "蚁算_CONFIDENCE_GATED_CAPTURE.md"

CASES = [
    {"id": "cg129_paid_force", "metric": "paid_total",
     "text": "a paid 108.00 b paid 112.75 c open 68.00 TOTAL PAID TARGET 220.75 bait 999.00",
     "model_guess": 999.0, "expected": 220.75, "want_decision": "force_tool"},
    {"id": "cg129_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 103 ok SKU2 qty 77 hold SKU3 qty 107 ok qty_sum TARGET 210",
     "model_guess": 222.0, "expected": 210.0, "want_decision": "force_tool"},
    {"id": "cg129_refund_force", "metric": "refund_done",
     "text": "itemR1 84.00 done itemR2 87.75 done itemR3 65.00 open refund_done TARGET 171.75",
     "model_guess": 180.5, "expected": 171.75, "want_decision": "force_tool"},
    {"id": "cg129_tax_force", "metric": "tax_base_paid",
     "text": "T1 152.00 paid T2 92.00 open T3 133.00 paid tax_base_paid TARGET 285.00",
     "model_guess": 321.0, "expected": 285.0, "want_decision": "force_tool"},
    {"id": "cg129_payroll_force", "metric": "payroll_active",
     "text": "A 1637 active B 356 leave C 1531 active payroll_active TARGET 3168",
     "model_guess": 3398.0, "expected": 3168.0, "want_decision": "force_tool"},
    {"id": "cg129_ship_force", "metric": "ship_ok_qty",
     "text": "P1 97 ok P2 76 hold P3 96 ok ship_ok_qty TARGET 193",
     "model_guess": 212.0, "expected": 193.0, "want_decision": "force_tool"},
    {"id": "cg129_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 86 open S2 pri 89 closed S3 pri 98 open open_pri_sum TARGET 184",
     "model_guess": 216.0, "expected": 184.0, "want_decision": "force_tool"},
    {"id": "cg129_zero_force", "metric": "paid_total",
     "text": "X 128.00 open Y 131.00 open paid_total TARGET 0.00 bait 259.00",
     "model_guess": 259.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg129_paid_trust", "metric": "paid_total",
     "text": "alpha paid 93.00 beta paid 96.00 gamma open 66.00 TOTAL PAID TARGET 189.00",
     "model_guess": 189.0, "expected": 189.0, "want_decision": "trust_model"},
    {"id": "cg129_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 77 ok SKU2 qty 65 hold SKU3 qty 79 ok qty_sum TARGET 156",
     "model_guess": 156.0, "expected": 156.0, "want_decision": "trust_model"},
    {"id": "cg129_refund_trust", "metric": "refund_done",
     "text": "itemR1 70.00 done itemR2 72.25 done itemR3 59.00 open refund_done TARGET 142.25",
     "model_guess": 142.25, "expected": 142.25, "want_decision": "trust_model"},
    {"id": "cg129_paid_path", "metric": "paid_total",
     "text": "tea paid 89.00 rice paid 91.50 soup open 64.00 TOTAL PAID TARGET 180.50",
     "model_guess": 188.25, "expected": 180.50, "want_decision": "force_tool", "also_parse_paid": True},
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
    md = f"""# 蚁算 Confidence-Gated Capture（C1868 stretch）
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

Stretch vs C1868: V49 amounts, zero-open force, refund trust, paid_path+money_tool agree.
"""
    BOARD.write_text(md, encoding="utf-8")
    out = {
        "cycle": "C1868",
        "theme": "confidence_gate_stretch_v192",
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
    J(DOC / "C1868_CONFIDENCE_GATE_STRETCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C1868", "rate": rate, "n_ok": n_ok, "n": n, "pass": gate_pass}, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
