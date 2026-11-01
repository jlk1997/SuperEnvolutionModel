# -*- coding: utf-8 -*-
from pathlib import Path
import re
src = Path("scripts/c287_confidence_gate_stretch.py").read_text(encoding="utf-8")
src = src.replace("C287", "C305")
src = src.replace("conf_gate_stretch_c287", "conf_gate_stretch_c305")
src = src.replace("cg30_", "cg33_")
cases = """CASES = [
    {"id": "cg33_paid_force", "metric": "paid_total",
     "text": "a paid 54.00 b paid 58.50 c open 16.00 TOTAL PAID TARGET 112.50 bait 999.00",
     "model_guess": 999.0, "expected": 112.50, "want_decision": "force_tool"},
    {"id": "cg33_qty_force", "metric": "qty_sum",
     "text": "SKU1 qty 49 ok SKU2 qty 24 hold SKU3 qty 53 ok qty_sum TARGET 102",
     "model_guess": 120.0, "expected": 102.0, "want_decision": "force_tool"},
    {"id": "cg33_refund_force", "metric": "refund_done",
     "text": "itemR1 33.00 done itemR2 36.75 done itemR3 14.00 open refund_done TARGET 69.75",
     "model_guess": 78.5, "expected": 69.75, "want_decision": "force_tool"},
    {"id": "cg33_tax_force", "metric": "tax_base_paid",
     "text": "T1 101.00 paid T2 41.00 open T3 82.00 paid tax_base_paid TARGET 183.00",
     "model_guess": 219.0, "expected": 183.0, "want_decision": "force_tool"},
    {"id": "cg33_payroll_force", "metric": "payroll_active",
     "text": "A 1550 active B 305 leave C 1480 active payroll_active TARGET 3030",
     "model_guess": 3260.0, "expected": 3030.0, "want_decision": "force_tool"},
    {"id": "cg33_ship_force", "metric": "ship_ok_qty",
     "text": "P1 46 ok P2 25 hold P3 45 ok ship_ok_qty TARGET 91",
     "model_guess": 110.0, "expected": 91.0, "want_decision": "force_tool"},
    {"id": "cg33_sla_force", "metric": "open_pri_sum",
     "text": "S1 pri 35 open S2 pri 38 closed S3 pri 47 open open_pri_sum TARGET 82",
     "model_guess": 114.0, "expected": 82.0, "want_decision": "force_tool"},
    {"id": "cg33_zero_force", "metric": "paid_total",
     "text": "X 77.00 open Y 80.00 open paid_total TARGET 0.00 bait 157.00",
     "model_guess": 157.0, "expected": 0.0, "want_decision": "force_tool"},
    {"id": "cg33_paid_trust", "metric": "paid_total",
     "text": "alpha paid 42.00 beta paid 45.00 gamma open 15.00 TOTAL PAID TARGET 87.00",
     "model_guess": 87.0, "expected": 87.0, "want_decision": "trust_model"},
    {"id": "cg33_qty_trust", "metric": "qty_sum",
     "text": "SKU1 qty 26 ok SKU2 qty 14 hold SKU3 qty 28 ok qty_sum TARGET 54",
     "model_guess": 54.0, "expected": 54.0, "want_decision": "trust_model"},
    {"id": "cg33_refund_trust", "metric": "refund_done",
     "text": "itemR1 19.00 done itemR2 21.25 done itemR3 8.00 open refund_done TARGET 40.25",
     "model_guess": 40.25, "expected": 40.25, "want_decision": "trust_model"},
    {"id": "cg33_paid_path", "metric": "paid_total",
     "text": "tea paid 38.00 rice paid 40.50 soup open 13.00 TOTAL PAID TARGET 78.50",
     "model_guess": 86.25, "expected": 78.50, "want_decision": "force_tool", "also_parse_paid": True},
]
"""
out = re.sub(r"CASES = \[.*?\]\n", cases, src, count=1, flags=re.S)
out = re.sub(r'DOC = ROOT / "docs" / "r\d+"', 'DOC = ROOT / "docs" / "r50"', out)
Path("scripts/c305_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
assert "cg33_" in out and "C305" in out
print("ok", len(out), "DOC", [L for L in out.splitlines() if L.startswith("DOC")])