# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
BAN = {755, 756, 770, 750, 830, 1830, 1560}

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

def check(rows, label):
    for i, row in enumerate(rows):
        for v in row:
            if isinstance(v, (int, float)) and int(v) in BAN:
                raise SystemExit(f"banned {v} in {label}[{i}]={row}")

# *fen ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T172 = [
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
TR172 = [
    [1141.0, 1158.5, 951.0],[740, 780, 820],[1064.0, 1093.25, 931.0],[1197.0, 1214.0, 1021.0],
    [1259.0, 1283.0, 991.0],[1017, 1033, 949],[480.0, 520.0, 510.0],[1107.0, 1138.75, 955.0],
    [780.0, 740.0, 760.0],[1174.0, 1162.0, 952.0],[1,1,0],[0,0,0],
    [1240.0, 1261.5, 977.0],[1,0,0],[789, 781, 759],[807, 791, 748],[1,0,0],[833, 809, 779],
]
HO172 = [
    [1011.0, 1023.75, 904.0],[840, 760, 820],[969.0, 982.5, 892.0],[1084.0, 1100.0, 933.0],
    [1125.0, 1141.0, 928.0],[919, 933, 897],[360.0, 400.0, 490.0],[995.0, 1016.75, 904.0],
    [840.0, 760.0, 740.0],[1042.0, 1028.0, 899.0],[1,1,0],[0,0,0],
    [1077.0, 1092.5, 914.0],[1,0,0],[767, 762, 757],[781, 775, 763],[1,0,0],[791, 785, 764],
]
# TR tabA 833 close to 830 — avoid 830; 833 ok. HO stack has 757 ok.
check(TR172, "TR"); check(HO172, "HO")

(ROOT / "tools/_v172_themes.json").write_text(json.dumps({"themes": T172, "train": TR172, "heldout": HO172}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_172(src):
    src = src.replace("# --- V171 overlays (new vs V50) ---", "# --- V172 overlays (new vs V50) ---")
    src = src.replace("# --- V171 overlays (new vs V49) ---", "# --- V172 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 85.85", "ASHFEN bait 86.86"),
        ("CEDARM bait 87.87", "CEDARF bait 88.88"),
        ("DAWNM ghost 99.99", "DAWNF ghost 11.11"),
        ("GLENM bait 80.80", "GLENF bait 81.81"),
        ("JADEM bait 71.71", "JADEF bait 72.72"),
        ("NETHERM bait 88.88", "NETHERF bait 89.89"),
        ("ash mist + stone ticks (V171-only)", "ash mist + stone ticks (V172-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD171 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v171_themes.json").read_text(encoding="utf-8"))["themes"])
NEW172 = "_".join(t[0] for t in T172)

out = (S / "c1133_vision_v171_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1133", "C1139"), ("c1133", "c1139"), ("V171", "V172"), ("v171", "v172"),
    ("_v171c1133", "_v172c1139"),
    ("Harder than V170", "Harder than V171"), ("harder than V170", "harder than V171"),
    (OLD171, NEW172),
    ("V171 keeps floor", "V172 keeps floor"),
    ("C1133 design+fixtures; no VL claim", "C1139 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1134 VL smoke", "fixtures only; claim deferred to C1140 VL smoke"),
    ("No claim until C1134 VL", "No claim until C1140 VL"),
    ("kept on V171", "kept on V172"),
    ("vision_images_v171", "vision_images_v172"),
    ("VL_GATE_V171", "VL_GATE_V172"), ("vl_gate_v171", "vl_gate_v172"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V170:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V171: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T172, "v172", "V172", TR172))
out = retarget_172(out)
(S / "c1139_vision_v172_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1134_vision_v171_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1134", "C1140"), ("c1134", "c1140"), ("V171", "V172"), ("v171", "v172"),
    ("vision_images_v171", "vision_images_v172"),
    ("VL_GATE_V171", "VL_GATE_V172"), ("vl_gate_v171", "vl_gate_v172"),
    ("runs/vision_v171", "runs/vision_v172"),
]:
    out = out.replace(a, b)
(S / "c1140_vision_v172_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1135_vision_v171_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1135", "C1141"), ("c1135", "c1141"), ("V171", "V172"), ("v171", "v172"),
    ("vision_images_v171h", "vision_images_v172h"),
    ("vision_images_v171", "vision_images_v172"),
    ("VL_GATE_V171", "VL_GATE_V172"), ("vl_gate_v171", "vl_gate_v172"),
    ("runs/vision_v171h", "runs/vision_v172h"),
    ("_v171c1133", "_v172c1139"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T172, "v172h", "V172H", HO172))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v172h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v172"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v172" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v172h_c1141"'); seen_run = True; continue
    out2.append(ln)
(S / "c1141_vision_v172_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1130_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1130", "C1142"), ("c1130", "c1142"),
    ("product_u2c_c1130", "product_u2c_c1142"),
    ("after V170", "after V172"), ("after V171", "after V172"),
]:
    out = out.replace(a, b)
(S / "c1142_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1137_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1137", "C1143"), ("c1137", "c1143"),
    ("capture_regression_c1137", "capture_regression_c1143"),
    ("after C1133-C1136", "after C1139-C1142"),
    ("V4-V171+heldout", "V4-V172+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V171", DOC / "C1134_VISION_V171_SMOKE.json"),'
if needle in out and "VISION_V172_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V172", DOC / "C1140_VISION_V172_SMOKE.json"),\n    ("V172_heldout", DOC / "C1141_VISION_V172_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1143_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1138_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1138", "C1144"), ("c1138", "c1144"),
    ("C1134", "C1140"), ("C1135", "C1141"), ("C1137", "C1143"),
    ("C1133", "C1139"),
    ("V171", "V172"), ("v171", "v172"),
    ("V170", "V171"), ("v170", "v171"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1136_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1136_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1130_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1142_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1130"', '"source": "C1142"')
out = out.replace('"source": "C1136"', '"source": "C1136"')
out = out.replace(
    "stage_ready = bool(v172_claim and v172h_claim and v172 >= GATE and v172h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v172_claim and v172h_claim and v172 >= GATE and v172h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1142: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1142: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1136: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1142: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1130): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1136): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1142): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1136): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1144_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T172 if t[0].endswith("b")])
print("qty", TR172[1], HO172[1], "po", TR172[8], HO172[8], "sla", TR172[6], HO172[6], "fax", TR172[15], HO172[15])
print("done")
