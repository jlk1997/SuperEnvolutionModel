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

# *hurst ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
T159 = [
    ["ashhurst","recv","paid_total","ASHHURST GRAIN RECV","RECV","x"],
    ["cedarhurst","wh","qty_sum","WH CEDARHURST BIN","RECV","x"],
    ["dawnhurst","refund","refund_done","DAWNHURST PATCH REFUND","DONE","x"],
    ["elmhurst","tax","tax_base_paid","ELMHURST TAX SLIP","TAX","x"],
    ["fernhurst","pay","payroll_active","FERNHURST PAYROLL","PAY","x"],
    ["glenhurst","ship","ship_ok","GLENHURST SHIP DOCK","SHIP","x"],
    ["hazehurst","sla","sla_ok_hours","HAZEHURST SLA CARD","SLA","x"],
    ["inkhurst","exp","exp_sum","INKHURST EXPENSE","EXP","x"],
    ["jadehurst","po","po_open","JADEHURST PO SHEET","PO","x"],
    ["knothurst","order","order_paid","KNOTHURST ORDER","ORD","x"],
    ["lakehurst","dup","dup_mark","LAKEHURST DUP MARK","DUP","x"],
    ["mosshurst","zero","zero_check","MOSSHURST AIR ZERO","ZERO","x"],
    ["netherhurst","ledger","ledger_net","NETHERHURST LEDGER","LED","x"],
    ["oakhurst","ui","ui_ok","OAKHURST UI SCAN","UI","x"],
    ["pinehurst","stack","stack_count","PINEHURST STACK","STK","x"],
    ["quillhurst","fax","fax_pages","QUILLHURST FAX","FAX","x"],
    ["reedhurst","glare","glare_ok","REEDHURST GLARE","GLR","x"],
    ["stonehurst","tab","tab_index","STONEHURST TAB INDEX","TAB","x"],
]
TR159 = [
    [1024.0, 1041.5, 834.0],[840, 760, 690],[947.0, 976.25, 814.0],[1080.0, 1097.0, 904.0],
    [1142.0, 1166.0, 874.0],[900, 916, 832],[460.0, 500.0, 380.0],[990.0, 1021.75, 838.0],
    [840.0, 760.0, 720.0],[1057.0, 1045.0, 835.0],[1,1,0],[0,0,0],
    [1123.0, 1144.5, 860.0],[1,0,0],[672, 664, 642],[690, 674, 665],[1,0,0],[716, 692, 662],
]
HO159 = [
    [894.0, 906.75, 787.0],[740, 780, 750],[852.0, 865.5, 775.0],[967.0, 983.0, 816.0],
    [1008.0, 1024.0, 811.0],[802, 816, 780],[360.0, 400.0, 360.0],[878.0, 899.75, 787.0],
    [780.0, 740.0, 700.0],[925.0, 911.0, 782.0],[1,1,0],[0,0,0],
    [960.0, 975.5, 797.0],[1,0,0],[648, 645, 640],[664, 658, 646],[1,0,0],[674, 668, 647],
]
(ROOT / "tools/_v159_themes.json").write_text(json.dumps({"themes": T159, "train": TR159, "heldout": HO159}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_159(src):
    src = src.replace("# --- V158 overlays (new vs V50) ---", "# --- V159 overlays (new vs V50) ---")
    src = src.replace("# --- V158 overlays (new vs V49) ---", "# --- V159 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 72.72", "ASHHURST bait 73.73"),
        ("CEDARC bait 84.84", "CEDARH bait 85.85"),
        ("DAWNC ghost 96.96", "DAWNH ghost 97.97"),
        ("GLENC bait 77.77", "GLENH bait 78.78"),
        ("JADEC bait 68.68", "JADEH bait 69.69"),
        ("NETHERC bait 85.85", "NETHERH bait 86.86"),
        ("ash mist + stone ticks (V158-only)", "ash mist + stone ticks (V159-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD158 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v158_themes.json").read_text(encoding="utf-8"))["themes"])
NEW159 = "_".join(t[0] for t in T159)

out = (S / "c1055_vision_v158_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1055", "C1061"), ("c1055", "c1061"), ("V158", "V159"), ("v158", "v159"),
    ("_v158c1055", "_v159c1061"),
    ("Harder than V157", "Harder than V158"), ("harder than V157", "harder than V158"),
    (OLD158, NEW159),
    ("V158 keeps floor", "V159 keeps floor"),
    ("C1055 design+fixtures; no VL claim", "C1061 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1056 VL smoke", "fixtures only; claim deferred to C1062 VL smoke"),
    ("No claim until C1056 VL", "No claim until C1062 VL"),
    ("kept on V158", "kept on V159"),
    ("vision_images_v158", "vision_images_v159"),
    ("VL_GATE_V158", "VL_GATE_V159"), ("vl_gate_v158", "vl_gate_v159"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V157:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V158: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehust, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.".replace("jadehust","jadehurst"),
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T159, "v159", "V159", TR159))
out = retarget_159(out)
(S / "c1061_vision_v159_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1056_vision_v158_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1056", "C1062"), ("c1056", "c1062"), ("V158", "V159"), ("v158", "v159"),
    ("vision_images_v158", "vision_images_v159"),
    ("VL_GATE_V158", "VL_GATE_V159"), ("vl_gate_v158", "vl_gate_v159"),
    ("runs/vision_v158", "runs/vision_v159"),
]:
    out = out.replace(a, b)
(S / "c1062_vision_v159_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1057_vision_v158_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1057", "C1063"), ("c1057", "c1063"), ("V158", "V159"), ("v158", "v159"),
    ("vision_images_v158h", "vision_images_v159h"),
    ("vision_images_v158", "vision_images_v159"),
    ("VL_GATE_V158", "VL_GATE_V159"), ("vl_gate_v158", "vl_gate_v159"),
    ("runs/vision_v158h", "runs/vision_v159h"),
    ("_v158c1055", "_v159c1061"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T159, "v159h", "V159H", HO159))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v159h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v159"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v159" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v159h_c1063"'); seen_run = True; continue
    out2.append(ln)
(S / "c1063_vision_v159_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1052_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1052", "C1064"), ("c1052", "c1064"),
    ("conf_gate_stretch_c1052", "conf_gate_stretch_c1064"),
    ("after V157", "after V159"), ("after V158", "after V159"),
    ("cg80_", "cg81_"),
]:
    out = out.replace(a, b)
(S / "c1064_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1059_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1059", "C1065"), ("c1059", "c1065"),
    ("capture_regression_c1059", "capture_regression_c1065"),
    ("after C1055-C1058", "after C1061-C1064"),
    ("V4-V158+heldout", "V4-V159+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V158", DOC / "C1056_VISION_V158_SMOKE.json"),'
if needle in out and "VISION_V159_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V159", DOC / "C1062_VISION_V159_SMOKE.json"),\n    ("V159_heldout", DOC / "C1063_VISION_V159_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1065_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1060_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1060", "C1066"), ("c1060", "c1066"),
    ("C1056", "C1062"), ("C1057", "C1063"), ("C1059", "C1065"),
    ("C1055", "C1061"),
    ("V158", "V159"), ("v158", "v159"),
    ("V157", "V158"), ("v157", "v158"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1058_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1058_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1052_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1064_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1058"', '"source": "C1058"')
out = out.replace('"source": "C1052"', '"source": "C1064"')
out = out.replace(
    "stage_ready = bool(v159_claim and v159h_claim and v159 >= GATE and v159h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v159_claim and v159h_claim and v159 >= GATE and v159h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1064: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1064: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1058: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1064: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1052): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1058): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1064): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1058): replace={replace} pass={u2c_pass}"',
)
(S / "c1066_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T159 if t[0].endswith("b")])
print("qty", TR159[1], HO159[1], "po", TR159[8], HO159[8], "sla", TR159[6], HO159[6])
print("done")
