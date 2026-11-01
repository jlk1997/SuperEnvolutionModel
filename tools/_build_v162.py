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

# *brook ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T162 = [
    ["ashbrook","recv","paid_total","ASHBROOK GRAIN RECV","RECV","x"],
    ["cedarbrook","wh","qty_sum","WH CEDARBROOK BIN","RECV","x"],
    ["dawnbrook","refund","refund_done","DAWNBROOK PATCH REFUND","DONE","x"],
    ["elmbrook","tax","tax_base_paid","ELMBROOK TAX SLIP","TAX","x"],
    ["fernbrook","pay","payroll_active","FERNBROOK PAYROLL","PAY","x"],
    ["glenbrook","ship","ship_ok","GLENBROOK SHIP DOCK","SHIP","x"],
    ["hazebrook","sla","sla_ok_hours","HAZEBROOK SLA CARD","SLA","x"],
    ["inkbrook","exp","exp_sum","INKBROOK EXPENSE","EXP","x"],
    ["jadebrook","po","po_open","JADEBROOK PO SHEET","PO","x"],
    ["knotbrook","order","order_paid","KNOTBROOK ORDER","ORD","x"],
    ["lakebrook","dup","dup_mark","LAKEBROOK DUP MARK","DUP","x"],
    ["mossbrook","zero","zero_check","MOSSBROOK AIR ZERO","ZERO","x"],
    ["netherbrook","ledger","ledger_net","NETHERBROOK LEDGER","LED","x"],
    ["oakbrook","ui","ui_ok","OAKBROOK UI SCAN","UI","x"],
    ["pinebrook","stack","stack_count","PINEBROOK STACK","STK","x"],
    ["quillbrook","fax","fax_pages","QUILLBROOK FAX","FAX","x"],
    ["reedbrook","glare","glare_ok","REEDBROOK GLARE","GLR","x"],
    ["stonebrook","tab","tab_index","STONEBROOK TAB INDEX","TAB","x"],
]
TR162 = [
    [1051.0, 1068.5, 861.0],[740, 780, 720],[974.0, 1003.25, 841.0],[1107.0, 1124.0, 931.0],
    [1169.0, 1193.0, 901.0],[927, 943, 859],[480.0, 520.0, 410.0],[1017.0, 1048.75, 865.0],
    [780.0, 740.0, 690.0],[1084.0, 1072.0, 862.0],[1,1,0],[0,0,0],
    [1150.0, 1171.5, 887.0],[1,0,0],[699, 691, 669],[717, 701, 692],[1,0,0],[743, 719, 689],
]
HO162 = [
    [921.0, 933.75, 814.0],[840, 760, 770],[879.0, 892.5, 802.0],[994.0, 1010.0, 843.0],
    [1035.0, 1051.0, 838.0],[829, 843, 807],[360.0, 400.0, 390.0],[905.0, 926.75, 814.0],
    [840.0, 760.0, 700.0],[952.0, 938.0, 809.0],[1,1,0],[0,0,0],
    [987.0, 1002.5, 824.0],[1,0,0],[675, 672, 667],[691, 685, 673],[1,0,0],[701, 695, 674],
]
(ROOT / "tools/_v162_themes.json").write_text(json.dumps({"themes": T162, "train": TR162, "heldout": HO162}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_162(src):
    src = src.replace("# --- V161 overlays (new vs V50) ---", "# --- V162 overlays (new vs V50) ---")
    src = src.replace("# --- V161 overlays (new vs V49) ---", "# --- V162 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 75.75", "ASHBROOK bait 76.76"),
        ("CEDARF bait 87.87", "CEDARB bait 88.88"),
        ("DAWNF ghost 99.99", "DAWNB ghost 90.90"),
        ("GLENF bait 70.70", "GLENB bait 71.71"),
        ("JADEF bait 61.61", "JADEB bait 62.62"),
        ("NETHERF bait 88.88", "NETHERB bait 89.89"),
        ("ash mist + stone ticks (V161-only)", "ash mist + stone ticks (V162-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD161 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v161_themes.json").read_text(encoding="utf-8"))["themes"])
NEW162 = "_".join(t[0] for t in T162)

out = (S / "c1073_vision_v161_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1073", "C1079"), ("c1073", "c1079"), ("V161", "V162"), ("v161", "v162"),
    ("_v161c1073", "_v162c1079"),
    ("Harder than V160", "Harder than V161"), ("harder than V160", "harder than V161"),
    (OLD161, NEW162),
    ("V161 keeps floor", "V162 keeps floor"),
    ("C1073 design+fixtures; no VL claim", "C1079 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1074 VL smoke", "fixtures only; claim deferred to C1080 VL smoke"),
    ("No claim until C1074 VL", "No claim until C1080 VL"),
    ("kept on V161", "kept on V162"),
    ("vision_images_v161", "vision_images_v162"),
    ("VL_GATE_V161", "VL_GATE_V162"), ("vl_gate_v161", "vl_gate_v162"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V160:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V161: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T162, "v162", "V162", TR162))
out = retarget_162(out)
(S / "c1079_vision_v162_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1074_vision_v161_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1074", "C1080"), ("c1074", "c1080"), ("V161", "V162"), ("v161", "v162"),
    ("vision_images_v161", "vision_images_v162"),
    ("VL_GATE_V161", "VL_GATE_V162"), ("vl_gate_v161", "vl_gate_v162"),
    ("runs/vision_v161", "runs/vision_v162"),
]:
    out = out.replace(a, b)
(S / "c1080_vision_v162_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1075_vision_v161_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1075", "C1081"), ("c1075", "c1081"), ("V161", "V162"), ("v161", "v162"),
    ("vision_images_v161h", "vision_images_v162h"),
    ("vision_images_v161", "vision_images_v162"),
    ("VL_GATE_V161", "VL_GATE_V162"), ("vl_gate_v161", "vl_gate_v162"),
    ("runs/vision_v161h", "runs/vision_v162h"),
    ("_v161c1073", "_v162c1079"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T162, "v162h", "V162H", HO162))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v162h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v162"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v162" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v162h_c1081"'); seen_run = True; continue
    out2.append(ln)
(S / "c1081_vision_v162_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1070_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1070", "C1082"), ("c1070", "c1082"),
    ("product_u2c_c1070", "product_u2c_c1082"),
    ("after V160", "after V162"), ("after V161", "after V162"),
]:
    out = out.replace(a, b)
(S / "c1082_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1077_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1077", "C1083"), ("c1077", "c1083"),
    ("capture_regression_c1077", "capture_regression_c1083"),
    ("after C1073-C1076", "after C1079-C1082"),
    ("V4-V161+heldout", "V4-V162+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V161", DOC / "C1074_VISION_V161_SMOKE.json"),'
if needle in out and "VISION_V162_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V162", DOC / "C1080_VISION_V162_SMOKE.json"),\n    ("V162_heldout", DOC / "C1081_VISION_V162_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1083_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1078_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1078", "C1084"), ("c1078", "c1084"),
    ("C1074", "C1080"), ("C1075", "C1081"), ("C1077", "C1083"),
    ("C1073", "C1079"),
    ("V161", "V162"), ("v161", "v162"),
    ("V160", "V161"), ("v160", "v161"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1070_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1082_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'c656 = load("docs/r50/C1076_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1076_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1070"', '"source": "C1082"')
out = out.replace('"source": "C1076"', '"source": "C1076"')
out = out.replace(
    "stage_ready = bool(v162_claim and v162h_claim and v162 >= GATE and v162h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v162_claim and v162h_claim and v162 >= GATE and v162h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1082: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1082: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1076: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1082: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1070): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1076): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1082): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1076): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1084_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T162 if t[0].endswith("b")])
print("qty", TR162[1], HO162[1], "po", TR162[8], HO162[8], "sla", TR162[6], HO162[6])
print("done")
