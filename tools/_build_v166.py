# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

def lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag):
    if metric == "paid_total":
        expected, body = a + b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"]
    elif metric == "qty_sum":
        expected = float(a + b); body = [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"]
    elif metric == "refund_done":
        expected, body = a + b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"]
    elif metric == "tax_base_paid":
        expected, body = a + b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"]
    elif metric == "payroll_active":
        expected, body = a + b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"]
    elif metric == "ship_ok":
        expected = float(a + b); body = [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"]
    elif metric == "sla_ok_hours":
        expected, body = a + b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"]
    elif metric == "exp_sum":
        expected, body = a + b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"]
    elif metric == "po_open":
        expected, body = a + b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"]
    elif metric == "order_paid":
        expected, body = a + b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"]
    elif metric == "dup_mark":
        expected, body = 2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"]
    elif metric == "zero_check":
        expected, body = 0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"]
    elif metric == "ledger_net":
        expected, body = a + b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"]
    elif metric == "ui_ok":
        expected, body = 1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"]
    elif metric == "stack_count":
        expected = float(a + b); body = [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"]
    elif metric == "fax_pages":
        expected = float(a + b); body = [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"]
    elif metric == "glare_ok":
        expected, body = 1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"]
    elif metric == "tab_index":
        expected = float(a + b); body = [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"]
    else:
        raise ValueError(metric)
    return expected, [f"{title} {tag}"] + body

def build_specs(themes, prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, (t, abc) in enumerate(zip(themes, abcs), 1):
        name, kind_suf, metric, title, stamp, _bk = t
        a, b, c = abc
        expected, body = lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag)
        fid = f"{prefix}_{i:02d}"; kind = f"{name}_{kind_suf}"
        body_l = ",\n     ".join(repr(x) for x in body)
        lines.append(f'    ("{fid}", "{kind}", "{metric}", {repr(float(expected))},\n     [{body_l}],\n     {repr(name)}, "{stamp}"),')
    lines.append("]")
    return "\n".join(lines) + "\n"

def replace_specs(src, new_specs):
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)

# *holm ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T166 = [
    ["ashholm","recv","paid_total","ASHHOLM GRAIN RECV","RECV","x"],
    ["cedarholm","wh","qty_sum","WH CEDARHOLM BIN","RECV","x"],
    ["dawnholm","refund","refund_done","DAWNHOLM PATCH REFUND","DONE","x"],
    ["elmholm","tax","tax_base_paid","ELMHOLM TAX SLIP","TAX","x"],
    ["fernholm","pay","payroll_active","FERNHOLM PAYROLL","PAY","x"],
    ["glenholm","ship","ship_ok","GLENHOLM SHIP DOCK","SHIP","x"],
    ["hazeholm","sla","sla_ok_hours","HAZEHOLM SLA CARD","SLA","x"],
    ["inkholm","exp","exp_sum","INKHOLM EXPENSE","EXP","x"],
    ["jadeholm","po","po_open","JADEHOLM PO SHEET","PO","x"],
    ["knotholm","order","order_paid","KNOTHOLM ORDER","ORD","x"],
    ["lakeholm","dup","dup_mark","LAKEHOLM DUP MARK","DUP","x"],
    ["mossholm","zero","zero_check","MOSSHOLM AIR ZERO","ZERO","x"],
    ["netherholm","ledger","ledger_net","NETHERHOLM LEDGER","LED","x"],
    ["oakholm","ui","ui_ok","OAKHOLM UI SCAN","UI","x"],
    ["pineholm","stack","stack_count","PINEHOLM STACK","STK","x"],
    ["quillholm","fax","fax_pages","QUILLHOLM FAX","FAX","x"],
    ["reedholm","glare","glare_ok","REEDHOLM GLARE","GLR","x"],
    ["stoneholm","tab","tab_index","STONEHOLM TAB INDEX","TAB","x"],
]
TR166 = [
    [1087.0, 1104.5, 897.0],[740, 780, 760],[1010.0, 1039.25, 877.0],[1143.0, 1160.0, 967.0],
    [1205.0, 1229.0, 937.0],[963, 979, 895],[480.0, 520.0, 450.0],[1053.0, 1084.75, 901.0],
    [780.0, 740.0, 700.0],[1120.0, 1108.0, 898.0],[1,1,0],[0,0,0],
    [1186.0, 1207.5, 923.0],[1,0,0],[735, 727, 705],[753, 737, 728],[1,0,0],[779, 755, 725],
]
HO166 = [
    [957.0, 969.75, 850.0],[840, 760, 810],[915.0, 928.5, 838.0],[1030.0, 1046.0, 879.0],
    [1071.0, 1087.0, 874.0],[865, 879, 843],[360.0, 400.0, 430.0],[941.0, 962.75, 850.0],
    [840.0, 760.0, 680.0],[988.0, 974.0, 845.0],[1,1,0],[0,0,0],
    [1023.0, 1038.5, 860.0],[1,0,0],[711, 708, 703],[727, 721, 709],[1,0,0],[737, 731, 710],
]
(ROOT / "tools/_v166_themes.json").write_text(json.dumps({"themes": T166, "train": TR166, "heldout": HO166}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_166(src):
    src = src.replace("# --- V165 overlays (new vs V50) ---", "# --- V166 overlays (new vs V50) ---")
    src = src.replace("# --- V165 overlays (new vs V49) ---", "# --- V166 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 79.79", "ASHHOLM bait 80.80"),
        ("CEDARF bait 81.81", "CEDARH bait 82.82"),
        ("DAWNF ghost 93.93", "DAWNH ghost 94.94"),
        ("GLENF bait 74.74", "GLENH bait 75.75"),
        ("JADEF bait 65.65", "JADEH bait 66.66"),
        ("NETHERF bait 82.82", "NETHERH bait 83.83"),
        ("ash mist + stone ticks (V165-only)", "ash mist + stone ticks (V166-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD165 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v165_themes.json").read_text(encoding="utf-8"))["themes"])
NEW166 = "_".join(t[0] for t in T166)

out = (S / "c1097_vision_v165_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1097", "C1103"), ("c1097", "c1103"), ("V165", "V166"), ("v165", "v166"),
    ("_v165c1097", "_v166c1103"),
    ("Harder than V164", "Harder than V165"), ("harder than V164", "harder than V165"),
    (OLD165, NEW166),
    ("V165 keeps floor", "V166 keeps floor"),
    ("C1097 design+fixtures; no VL claim", "C1103 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1098 VL smoke", "fixtures only; claim deferred to C1104 VL smoke"),
    ("No claim until C1098 VL", "No claim until C1104 VL"),
    ("kept on V165", "kept on V166"),
    ("vision_images_v165", "vision_images_v166"),
    ("VL_GATE_V165", "VL_GATE_V166"), ("vl_gate_v165", "vl_gate_v166"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V164:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V165: ashholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T166, "v166", "V166", TR166))
out = retarget_166(out)
(S / "c1103_vision_v166_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1098_vision_v165_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1098", "C1104"), ("c1098", "c1104"), ("V165", "V166"), ("v165", "v166"),
    ("vision_images_v165", "vision_images_v166"),
    ("VL_GATE_V165", "VL_GATE_V166"), ("vl_gate_v165", "vl_gate_v166"),
    ("runs/vision_v165", "runs/vision_v166"),
]:
    out = out.replace(a, b)
(S / "c1104_vision_v166_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1099_vision_v165_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1099", "C1105"), ("c1099", "c1105"), ("V165", "V166"), ("v165", "v166"),
    ("vision_images_v165h", "vision_images_v166h"),
    ("vision_images_v165", "vision_images_v166"),
    ("VL_GATE_V165", "VL_GATE_V166"), ("vl_gate_v165", "vl_gate_v166"),
    ("runs/vision_v165h", "runs/vision_v166h"),
    ("_v165c1097", "_v166c1103"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T166, "v166h", "V166H", HO166))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v166h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v166"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v166" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v166h_c1105"'); seen_run = True; continue
    out2.append(ln)
(S / "c1105_vision_v166_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1094_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1094", "C1106"), ("c1094", "c1106"),
    ("product_u2c_c1094", "product_u2c_c1106"),
    ("after V164", "after V166"), ("after V163", "after V166"),
]:
    out = out.replace(a, b)
(S / "c1106_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1101_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1101", "C1107"), ("c1101", "c1107"),
    ("capture_regression_c1101", "capture_regression_c1107"),
    ("after C1097-C1100", "after C1103-C1106"),
    ("V4-V165+heldout", "V4-V166+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V165", DOC / "C1098_VISION_V165_SMOKE.json"),'
if needle in out and "VISION_V166_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V166", DOC / "C1104_VISION_V166_SMOKE.json"),\n    ("V166_heldout", DOC / "C1105_VISION_V166_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1107_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1102_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1102", "C1108"), ("c1102", "c1108"),
    ("C1098", "C1104"), ("C1099", "C1105"), ("C1101", "C1107"),
    ("C1097", "C1103"),
    ("V165", "V166"), ("v165", "v166"),
    ("V164", "V165"), ("v164", "v165"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1100_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1100_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1094_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1106_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1094"', '"source": "C1106"')
out = out.replace('"source": "C1100"', '"source": "C1100"')
out = out.replace(
    "stage_ready = bool(v166_claim and v166h_claim and v166 >= GATE and v166h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v166_claim and v166h_claim and v166 >= GATE and v166h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1106: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1106: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1100: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1106: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1094): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1100): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1106): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1100): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1108_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T166 if t[0].endswith("b")])
print("qty", TR166[1], HO166[1], "po", TR166[8], HO166[8], "sla", TR166[6], HO166[6])
print("done")
