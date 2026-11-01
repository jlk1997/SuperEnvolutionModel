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

# *ford ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T154 = [
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
TR154 = [
    [979.0, 996.5, 789.0],[740, 780, 640],[902.0, 931.25, 769.0],[1035.0, 1052.0, 859.0],
    [1097.0, 1121.0, 829.0],[855, 871, 787],[480.0, 520.0, 330.0],[945.0, 976.75, 793.0],
    [780.0, 740.0, 730.0],[1012.0, 1000.0, 790.0],[1,1,0],[0,0,0],
    [1078.0, 1099.5, 815.0],[1,0,0],[627, 619, 597],[645, 629, 620],[1,0,0],[671, 647, 617],
]
HO154 = [
    [849.0, 861.75, 742.0],[840, 760, 700],[807.0, 820.5, 730.0],[922.0, 938.0, 771.0],
    [963.0, 979.0, 766.0],[757, 771, 735],[360.0, 400.0, 310.0],[833.0, 854.75, 742.0],
    [840.0, 760.0, 740.0],[880.0, 866.0, 737.0],[1,1,0],[0,0,0],
    [915.0, 930.5, 752.0],[1,0,0],[603, 600, 595],[619, 613, 601],[1,0,0],[629, 623, 602],
]
(ROOT / "tools/_v154_themes.json").write_text(json.dumps({"themes": T154, "train": TR154, "heldout": HO154}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_154(src):
    src = src.replace("# --- V153 overlays (new vs V50) ---", "# --- V154 overlays (new vs V50) ---")
    src = src.replace("# --- V153 overlays (new vs V49) ---", "# --- V154 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 77.77", "ASHFORD bait 78.78"),
        ("CEDARV bait 89.89", "CEDARF bait 80.80"),
        ("DAWNV ghost 91.91", "DAWNF ghost 92.92"),
        ("GLENV bait 72.72", "GLENF bait 73.73"),
        ("JADEV bait 63.63", "JADEF bait 64.64"),
        ("NETHERV bait 80.80", "NETHERF bait 81.81"),
        ("ash mist + stone ticks (V153-only)", "ash mist + stone ticks (V154-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD153 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v153_themes.json").read_text(encoding="utf-8"))["themes"])
NEW154 = "_".join(t[0] for t in T154)

out = (S / "c1025_vision_v153_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1025", "C1031"), ("c1025", "c1031"), ("V153", "V154"), ("v153", "v154"),
    ("_v153c1025", "_v154c1031"),
    ("Harder than V152", "Harder than V153"), ("harder than V152", "harder than V153"),
    (OLD153, NEW154),
    ("V153 keeps floor", "V154 keeps floor"),
    ("C1025 design+fixtures; no VL claim", "C1031 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1026 VL smoke", "fixtures only; claim deferred to C1032 VL smoke"),
    ("No claim until C1026 VL", "No claim until C1032 VL"),
    ("kept on V153", "kept on V154"),
    ("vision_images_v153", "vision_images_v154"),
    ("VL_GATE_V153", "VL_GATE_V154"), ("vl_gate_v153", "vl_gate_v154"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V152: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    "NEW themes vs V153: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
)
out = replace_specs(out, build_specs(T154, "v154", "V154", TR154))
out = retarget_154(out)
(S / "c1031_vision_v154_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1026_vision_v153_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1026", "C1032"), ("c1026", "c1032"), ("V153", "V154"), ("v153", "v154"),
    ("vision_images_v153", "vision_images_v154"),
    ("VL_GATE_V153", "VL_GATE_V154"), ("vl_gate_v153", "vl_gate_v154"),
    ("runs/vision_v153", "runs/vision_v154"),
]:
    out = out.replace(a, b)
(S / "c1032_vision_v154_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1027_vision_v153_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1027", "C1033"), ("c1027", "c1033"), ("V153", "V154"), ("v153", "v154"),
    ("vision_images_v153h", "vision_images_v154h"),
    ("vision_images_v153", "vision_images_v154"),
    ("VL_GATE_V153", "VL_GATE_V154"), ("vl_gate_v153", "vl_gate_v154"),
    ("runs/vision_v153h", "runs/vision_v154h"),
    ("_v153c1025", "_v154c1031"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T154, "v154h", "V154H", HO154))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v154h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v154"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v154" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v154h_c1033"'); seen_run = True; continue
    out2.append(ln)
(S / "c1033_vision_v154_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1022_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1022", "C1034"), ("c1022", "c1034"),
    ("product_u2c_c1022", "product_u2c_c1034"),
    ("after V152", "after V154"), ("after V153", "after V154"),
]:
    out = out.replace(a, b)
(S / "c1034_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1029_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1029", "C1035"), ("c1029", "c1035"),
    ("capture_regression_c1029", "capture_regression_c1035"),
    ("after C1025-C1028", "after C1031-C1034"),
    ("V4-V153+heldout", "V4-V154+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V153", DOC / "C1026_VISION_V153_SMOKE.json"),'
if needle in out and "VISION_V154_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V154", DOC / "C1032_VISION_V154_SMOKE.json"),\n    ("V154_heldout", DOC / "C1033_VISION_V154_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1035_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1030_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1030", "C1036"), ("c1030", "c1036"),
    ("C1026", "C1032"), ("C1027", "C1033"), ("C1029", "C1035"),
    ("C1025", "C1031"),
    ("V153", "V154"), ("v153", "v154"),
    ("V152", "V153"), ("v152", "v153"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1022_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1034_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1028_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1028_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1022"', '"source": "C1034"')
out = out.replace('"source": "C1028"', '"source": "C1028"')
out = out.replace(
    "stage_ready = bool(v154_claim and v154h_claim and v154 >= GATE and v154h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v154_claim and v154h_claim and v154 >= GATE and v154h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1034: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1034: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1028: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1034: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1022): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1028): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1034): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1028): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1036_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c650 =", "c656 =", "stage_ready =", "C1034:", "source")):
        if "load" in ln or "stage_ready" in ln or "C1034" in ln or "source" in ln:
            print("CHK", ln.strip()[:180])
print("any_b", [t[0] for t in T154 if t[0].endswith("b")])
print("qty", TR154[1], HO154[1], "po", TR154[8], HO154[8], "sla", TR154[6], HO154[6])
print("done")
