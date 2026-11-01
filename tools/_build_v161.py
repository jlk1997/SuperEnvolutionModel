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

# *fen ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
T161 = [
    ["ashfen","recv","paid_total","ASHFEN GRAIN RECV","RECV","x"],
    ["cedarfen","wh","qty_sum","WH CEDARFEN BIN","RECV","x"],
    ["dawnfen","refund","refund_done","DAWNFEN PATCH REFUND","DONE","x"],
    ["elmfen","tax","tax_base_paid","ELMFEN TAX SLIP","TAX","x"],
    ["fernfen","pay","payroll_active","FERNFEN PAYROLL","PAY","x"],
    ["glenfen","ship","ship_ok","GLENFEN SHIP DOCK","SHIP","x"],
    ["hazefen","sla","sla_ok_hours","HAZEFEN SLA CARD","SLA","x"],
    ["inkfen","exp","exp_sum","INKFEN EXPENSE","EXP","x"],
    ["jadefen","po","po_open","JADEFEN PO SHEET","PO","x"],
    ["knotfen","order","order_paid","KNOTFEN ORDER","ORD","x"],
    ["lakefen","dup","dup_mark","LAKEFEN DUP MARK","DUP","x"],
    ["mossfen","zero","zero_check","MOSSFEN AIR ZERO","ZERO","x"],
    ["netherfen","ledger","ledger_net","NETHERFEN LEDGER","LED","x"],
    ["oakfen","ui","ui_ok","OAKFEN UI SCAN","UI","x"],
    ["pinefen","stack","stack_count","PINEFEN STACK","STK","x"],
    ["quillfen","fax","fax_pages","QUILLFEN FAX","FAX","x"],
    ["reedfen","glare","glare_ok","REEDFEN GLARE","GLR","x"],
    ["stonefen","tab","tab_index","STONEFEN TAB INDEX","TAB","x"],
]
TR161 = [
    [1042.0, 1059.5, 852.0],[840, 760, 710],[965.0, 994.25, 832.0],[1098.0, 1115.0, 922.0],
    [1160.0, 1184.0, 892.0],[918, 934, 850],[460.0, 500.0, 400.0],[1008.0, 1039.75, 856.0],
    [840.0, 760.0, 710.0],[1075.0, 1063.0, 853.0],[1,1,0],[0,0,0],
    [1141.0, 1162.5, 878.0],[1,0,0],[690, 682, 660],[708, 692, 683],[1,0,0],[734, 710, 680],
]
HO161 = [
    [912.0, 924.75, 805.0],[740, 780, 760],[870.0, 883.5, 793.0],[985.0, 1001.0, 834.0],
    [1026.0, 1042.0, 829.0],[820, 834, 798],[360.0, 400.0, 380.0],[896.0, 917.75, 805.0],
    [780.0, 740.0, 690.0],[943.0, 929.0, 800.0],[1,1,0],[0,0,0],
    [978.0, 993.5, 815.0],[1,0,0],[666, 663, 658],[682, 676, 664],[1,0,0],[692, 686, 665],
]
(ROOT / "tools/_v161_themes.json").write_text(json.dumps({"themes": T161, "train": TR161, "heldout": HO161}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_161(src):
    src = src.replace("# --- V160 overlays (new vs V50) ---", "# --- V161 overlays (new vs V50) ---")
    src = src.replace("# --- V160 overlays (new vs V49) ---", "# --- V161 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 74.74", "ASHFEN bait 75.75"),
        ("CEDARM bait 86.86", "CEDARF bait 87.87"),
        ("DAWNM ghost 98.98", "DAWNF ghost 99.99"),
        ("GLENM bait 79.79", "GLENF bait 70.70"),
        ("JADEM bait 60.60", "JADEF bait 61.61"),
        ("NETHERM bait 87.87", "NETHERF bait 88.88"),
        ("ash mist + stone ticks (V160-only)", "ash mist + stone ticks (V161-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD160 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v160_themes.json").read_text(encoding="utf-8"))["themes"])
NEW161 = "_".join(t[0] for t in T161)

out = (S / "c1067_vision_v160_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1067", "C1073"), ("c1067", "c1073"), ("V160", "V161"), ("v160", "v161"),
    ("_v160c1067", "_v161c1073"),
    ("Harder than V159", "Harder than V160"), ("harder than V159", "harder than V160"),
    (OLD160, NEW161),
    ("V160 keeps floor", "V161 keeps floor"),
    ("C1067 design+fixtures; no VL claim", "C1073 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1068 VL smoke", "fixtures only; claim deferred to C1074 VL smoke"),
    ("No claim until C1068 VL", "No claim until C1074 VL"),
    ("kept on V160", "kept on V161"),
    ("vision_images_v160", "vision_images_v161"),
    ("VL_GATE_V160", "VL_GATE_V161"), ("vl_gate_v160", "vl_gate_v161"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V159:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V160: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T161, "v161", "V161", TR161))
out = retarget_161(out)
(S / "c1073_vision_v161_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1068_vision_v160_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1068", "C1074"), ("c1068", "c1074"), ("V160", "V161"), ("v160", "v161"),
    ("vision_images_v160", "vision_images_v161"),
    ("VL_GATE_V160", "VL_GATE_V161"), ("vl_gate_v160", "vl_gate_v161"),
    ("runs/vision_v160", "runs/vision_v161"),
]:
    out = out.replace(a, b)
(S / "c1074_vision_v161_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1069_vision_v160_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1069", "C1075"), ("c1069", "c1075"), ("V160", "V161"), ("v160", "v161"),
    ("vision_images_v160h", "vision_images_v161h"),
    ("vision_images_v160", "vision_images_v161"),
    ("VL_GATE_V160", "VL_GATE_V161"), ("vl_gate_v160", "vl_gate_v161"),
    ("runs/vision_v160h", "runs/vision_v161h"),
    ("_v160c1067", "_v161c1073"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T161, "v161h", "V161H", HO161))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v161h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v161"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v161" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v161h_c1075"'); seen_run = True; continue
    out2.append(ln)
(S / "c1075_vision_v161_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1064_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1064", "C1076"), ("c1064", "c1076"),
    ("conf_gate_stretch_c1064", "conf_gate_stretch_c1076"),
    ("after V159", "after V161"), ("after V160", "after V161"),
    ("cg81_", "cg82_"),
]:
    out = out.replace(a, b)
(S / "c1076_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1071_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1071", "C1077"), ("c1071", "c1077"),
    ("capture_regression_c1071", "capture_regression_c1077"),
    ("after C1067-C1070", "after C1073-C1076"),
    ("V4-V160+heldout", "V4-V161+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V160", DOC / "C1068_VISION_V160_SMOKE.json"),'
if needle in out and "VISION_V161_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V161", DOC / "C1074_VISION_V161_SMOKE.json"),\n    ("V161_heldout", DOC / "C1075_VISION_V161_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1077_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1072_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1072", "C1078"), ("c1072", "c1078"),
    ("C1068", "C1074"), ("C1069", "C1075"), ("C1071", "C1077"),
    ("C1067", "C1073"),
    ("V160", "V161"), ("v160", "v161"),
    ("V159", "V160"), ("v159", "v160"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1070_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1070_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1064_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1076_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1070"', '"source": "C1070"')
out = out.replace('"source": "C1064"', '"source": "C1076"')
out = out.replace(
    "stage_ready = bool(v161_claim and v161h_claim and v161 >= GATE and v161h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v161_claim and v161h_claim and v161 >= GATE and v161h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1076: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1076: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1070: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1076: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1064): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1070): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1076): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1070): replace={replace} pass={u2c_pass}"',
)
(S / "c1078_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T161 if t[0].endswith("b")])
print("qty", TR161[1], HO161[1], "po", TR161[8], HO161[8], "sla", TR161[6], HO161[6])
print("done")
