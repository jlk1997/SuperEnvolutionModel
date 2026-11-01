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

# *ford ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
T165 = [
    ["ashford","recv","paid_total","ASHFORD GRAIN RECV","RECV","x"],
    ["cedarford","wh","qty_sum","WH CEDARFORD BIN","RECV","x"],
    ["dawnford","refund","refund_done","DAWNFORD PATCH REFUND","DONE","x"],
    ["elmford","tax","tax_base_paid","ELMFORD TAX SLIP","TAX","x"],
    ["fernford","pay","payroll_active","FERNFORD PAYROLL","PAY","x"],
    ["glenford","ship","ship_ok","GLENFORD SHIP DOCK","SHIP","x"],
    ["hazeford","sla","sla_ok_hours","HAZEFORD SLA CARD","SLA","x"],
    ["inkford","exp","exp_sum","INKFORD EXPENSE","EXP","x"],
    ["jadeford","po","po_open","JADEFORD PO SHEET","PO","x"],
    ["knotford","order","order_paid","KNOTFORD ORDER","ORD","x"],
    ["lakeford","dup","dup_mark","LAKEFORD DUP MARK","DUP","x"],
    ["mossford","zero","zero_check","MOSSFORD AIR ZERO","ZERO","x"],
    ["netherford","ledger","ledger_net","NETHERFORD LEDGER","LED","x"],
    ["oakford","ui","ui_ok","OAKFORD UI SCAN","UI","x"],
    ["pineford","stack","stack_count","PINEFORD STACK","STK","x"],
    ["quillford","fax","fax_pages","QUILLFORD FAX","FAX","x"],
    ["reedford","glare","glare_ok","REEDFORD GLARE","GLR","x"],
    ["stoneford","tab","tab_index","STONEFORD TAB INDEX","TAB","x"],
]
TR165 = [
    [1078.0, 1095.5, 888.0],[840, 760, 750],[1001.0, 1030.25, 868.0],[1134.0, 1151.0, 958.0],
    [1196.0, 1220.0, 928.0],[954, 970, 886],[460.0, 500.0, 440.0],[1044.0, 1075.75, 892.0],
    [840.0, 760.0, 690.0],[1111.0, 1099.0, 889.0],[1,1,0],[0,0,0],
    [1177.0, 1198.5, 914.0],[1,0,0],[726, 718, 696],[744, 728, 719],[1,0,0],[770, 746, 716],
]
HO165 = [
    [948.0, 960.75, 841.0],[740, 780, 800],[906.0, 919.5, 829.0],[1021.0, 1037.0, 870.0],
    [1062.0, 1078.0, 865.0],[856, 870, 834],[360.0, 400.0, 420.0],[932.0, 953.75, 841.0],
    [780.0, 740.0, 670.0],[979.0, 965.0, 836.0],[1,1,0],[0,0,0],
    [1014.0, 1029.5, 851.0],[1,0,0],[702, 699, 694],[718, 712, 700],[1,0,0],[728, 722, 701],
]
(ROOT / "tools/_v165_themes.json").write_text(json.dumps({"themes": T165, "train": TR165, "heldout": HO165}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_165(src):
    src = src.replace("# --- V164 overlays (new vs V50) ---", "# --- V165 overlays (new vs V50) ---")
    src = src.replace("# --- V164 overlays (new vs V49) ---", "# --- V165 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 78.78", "ASHFORD bait 79.79"),
        ("CEDARV bait 80.80", "CEDARF bait 81.81"),
        ("DAWNV ghost 92.92", "DAWNF ghost 93.93"),
        ("GLENV bait 73.73", "GLENF bait 74.74"),
        ("JADEV bait 64.64", "JADEF bait 65.65"),
        ("NETHERV bait 81.81", "NETHERF bait 82.82"),
        ("ash mist + stone ticks (V164-only)", "ash mist + stone ticks (V165-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD164 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v164_themes.json").read_text(encoding="utf-8"))["themes"])
NEW165 = "_".join(t[0] for t in T165)

out = (S / "c1091_vision_v164_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1091", "C1097"), ("c1091", "c1097"), ("V164", "V165"), ("v164", "v165"),
    ("_v164c1091", "_v165c1097"),
    ("Harder than V163", "Harder than V164"), ("harder than V163", "harder than V164"),
    (OLD164, NEW165),
    ("V164 keeps floor", "V165 keeps floor"),
    ("C1091 design+fixtures; no VL claim", "C1097 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1092 VL smoke", "fixtures only; claim deferred to C1098 VL smoke"),
    ("No claim until C1092 VL", "No claim until C1098 VL"),
    ("kept on V164", "kept on V165"),
    ("vision_images_v164", "vision_images_v165"),
    ("VL_GATE_V164", "VL_GATE_V165"), ("vl_gate_v164", "vl_gate_v165"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V163:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V164: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T165, "v165", "V165", TR165))
out = retarget_165(out)
(S / "c1097_vision_v165_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1092_vision_v164_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1092", "C1098"), ("c1092", "c1098"), ("V164", "V165"), ("v164", "v165"),
    ("vision_images_v164", "vision_images_v165"),
    ("VL_GATE_V164", "VL_GATE_V165"), ("vl_gate_v164", "vl_gate_v165"),
    ("runs/vision_v164", "runs/vision_v165"),
]:
    out = out.replace(a, b)
(S / "c1098_vision_v165_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1093_vision_v164_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1093", "C1099"), ("c1093", "c1099"), ("V164", "V165"), ("v164", "v165"),
    ("vision_images_v164h", "vision_images_v165h"),
    ("vision_images_v164", "vision_images_v165"),
    ("VL_GATE_V164", "VL_GATE_V165"), ("vl_gate_v164", "vl_gate_v165"),
    ("runs/vision_v164h", "runs/vision_v165h"),
    ("_v164c1091", "_v165c1097"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T165, "v165h", "V165H", HO165))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v165h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v165"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v165" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v165h_c1099"'); seen_run = True; continue
    out2.append(ln)
(S / "c1099_vision_v165_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1088_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1088", "C1100"), ("c1088", "c1100"),
    ("conf_gate_stretch_c1088", "conf_gate_stretch_c1100"),
    ("after V163", "after V165"), ("after V164", "after V165"),
    ("cg83_", "cg84_"),
]:
    out = out.replace(a, b)
(S / "c1100_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1095_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1095", "C1101"), ("c1095", "c1101"),
    ("capture_regression_c1095", "capture_regression_c1101"),
    ("after C1091-C1094", "after C1097-C1100"),
    ("V4-V164+heldout", "V4-V165+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V164", DOC / "C1092_VISION_V164_SMOKE.json"),'
if needle in out and "VISION_V165_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V165", DOC / "C1098_VISION_V165_SMOKE.json"),\n    ("V165_heldout", DOC / "C1099_VISION_V165_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1101_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1096_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1096", "C1102"), ("c1096", "c1102"),
    ("C1092", "C1098"), ("C1093", "C1099"), ("C1095", "C1101"),
    ("C1091", "C1097"),
    ("V164", "V165"), ("v164", "v165"),
    ("V163", "V164"), ("v163", "v164"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1094_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1094_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1088_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1100_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1094"', '"source": "C1094"')
out = out.replace('"source": "C1088"', '"source": "C1100"')
out = out.replace(
    "stage_ready = bool(v165_claim and v165h_claim and v165 >= GATE and v165h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v165_claim and v165h_claim and v165 >= GATE and v165h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1100: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1100: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1094: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1100: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1088): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1094): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1100): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1094): replace={replace} pass={u2c_pass}"',
)
(S / "c1102_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T165 if t[0].endswith("b")])
print("qty", TR165[1], HO165[1], "po", TR165[8], HO165[8], "sla", TR165[6], HO165[6])
print("done")
