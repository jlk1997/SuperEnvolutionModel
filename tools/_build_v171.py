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

# *moor ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
BAN = {755, 756, 770, 750, 830, 1830, 1560}
T171 = [
    ["ashmoor","recv","paid_total","ASHMOOR GRAIN RECV","RECV","x"],
    ["cedarmoor","wh","qty_sum","WH CEDARMOOR BIN","RECV","x"],
    ["dawnmoor","refund","refund_done","DAWNMOOR PATCH REFUND","DONE","x"],
    ["elmmoor","tax","tax_base_paid","ELMMOOR TAX SLIP","TAX","x"],
    ["fernmoor","pay","payroll_active","FERNMOOR PAYROLL","PAY","x"],
    ["glenmoor","ship","ship_ok","GLENMOOR SHIP DOCK","SHIP","x"],
    ["hazemoor","sla","sla_ok_hours","HAZEMOOR SLA CARD","SLA","x"],
    ["inkmoor","exp","exp_sum","INKMOOR EXPENSE","EXP","x"],
    ["jademoor","po","po_open","JADEMOOR PO SHEET","PO","x"],
    ["knotmoor","order","order_paid","KNOTMOOR ORDER","ORD","x"],
    ["lakemoor","dup","dup_mark","LAKEMOOR DUP MARK","DUP","x"],
    ["mossmoor","zero","zero_check","MOSSMOOR AIR ZERO","ZERO","x"],
    ["nethermoor","ledger","ledger_net","NETHERMOOR LEDGER","LED","x"],
    ["oakmoor","ui","ui_ok","OAKMOOR UI SCAN","UI","x"],
    ["pinemoor","stack","stack_count","PINEMOOR STACK","STK","x"],
    ["quillmoor","fax","fax_pages","QUILLMOOR FAX","FAX","x"],
    ["reedmoor","glare","glare_ok","REEDMOOR GLARE","GLR","x"],
    ["stonemoor","tab","tab_index","STONEMOOR TAB INDEX","TAB","x"],
]
TR171 = [
    [1132.0, 1149.5, 942.0],[840, 760, 810],[1055.0, 1084.25, 922.0],[1188.0, 1205.0, 1012.0],
    [1250.0, 1274.0, 982.0],[1008, 1024, 940],[460.0, 500.0, 500.0],[1098.0, 1129.75, 946.0],
    [840.0, 760.0, 750.0],[1165.0, 1153.0, 943.0],[1,1,0],[0,0,0],
    [1231.0, 1252.5, 968.0],[1,0,0],[780, 772, 750],[798, 782, 748],[1,0,0],[824, 800, 770],
]
# Fix banned: TR po closed 750 banned, stack p3 750, tabC 770 banned
TR171[8] = [840.0, 760.0, 730.0]
TR171[14] = [780, 772, 741]
TR171[17] = [824, 800, 761]
HO171 = [
    [1002.0, 1014.75, 895.0],[740, 780, 820],[960.0, 973.5, 883.0],[1075.0, 1091.0, 924.0],
    [1116.0, 1132.0, 919.0],[910, 924, 888],[360.0, 400.0, 480.0],[986.0, 1007.75, 895.0],
    [780.0, 740.0, 730.0],[1033.0, 1019.0, 890.0],[1,1,0],[0,0,0],
    [1068.0, 1083.5, 905.0],[1,0,0],[756, 753, 748],[772, 766, 754],[1,0,0],[782, 776, 755],
]
# Fix HO banned: stack p1 756, fax drop 754 ok, tabC 755 banned
HO171[14] = [758, 753, 748]
HO171[17] = [782, 776, 746]
for label, rows in [("TR", TR171), ("HO", HO171)]:
    for i, row in enumerate(rows):
        for v in row:
            if isinstance(v, (int, float)) and int(v) in BAN:
                raise SystemExit(f"banned {v} in {label}[{i}]={row}")

(ROOT / "tools/_v171_themes.json").write_text(json.dumps({"themes": T171, "train": TR171, "heldout": HO171}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_171(src):
    src = src.replace("# --- V170 overlays (new vs V50) ---", "# --- V171 overlays (new vs V50) ---")
    src = src.replace("# --- V170 overlays (new vs V49) ---", "# --- V171 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 84.84", "ASHMOOR bait 85.85"),
        ("CEDARH bait 86.86", "CEDARM bait 87.87"),
        ("DAWNH ghost 98.98", "DAWNM ghost 99.99"),
        ("GLENH bait 79.79", "GLENM bait 80.80"),
        ("JADEH bait 70.70", "JADEM bait 71.71"),
        ("NETHERH bait 87.87", "NETHERM bait 88.88"),
        ("ash mist + stone ticks (V170-only)", "ash mist + stone ticks (V171-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD170 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v170_themes.json").read_text(encoding="utf-8"))["themes"])
NEW171 = "_".join(t[0] for t in T171)

out = (S / "c1127_vision_v170_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1127", "C1133"), ("c1127", "c1133"), ("V170", "V171"), ("v170", "v171"),
    ("_v170c1127", "_v171c1133"),
    ("Harder than V169", "Harder than V170"), ("harder than V169", "harder than V170"),
    (OLD170, NEW171),
    ("V170 keeps floor", "V171 keeps floor"),
    ("C1127 design+fixtures; no VL claim", "C1133 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1128 VL smoke", "fixtures only; claim deferred to C1134 VL smoke"),
    ("No claim until C1128 VL", "No claim until C1134 VL"),
    ("kept on V170", "kept on V171"),
    ("vision_images_v170", "vision_images_v171"),
    ("VL_GATE_V170", "VL_GATE_V171"), ("vl_gate_v170", "vl_gate_v171"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V169:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V170: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T171, "v171", "V171", TR171))
out = retarget_171(out)
(S / "c1133_vision_v171_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1128_vision_v170_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1128", "C1134"), ("c1128", "c1134"), ("V170", "V171"), ("v170", "v171"),
    ("vision_images_v170", "vision_images_v171"),
    ("VL_GATE_V170", "VL_GATE_V171"), ("vl_gate_v170", "vl_gate_v171"),
    ("runs/vision_v170", "runs/vision_v171"),
]:
    out = out.replace(a, b)
(S / "c1134_vision_v171_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1129_vision_v170_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1129", "C1135"), ("c1129", "c1135"), ("V170", "V171"), ("v170", "v171"),
    ("vision_images_v170h", "vision_images_v171h"),
    ("vision_images_v170", "vision_images_v171"),
    ("VL_GATE_V170", "VL_GATE_V171"), ("vl_gate_v170", "vl_gate_v171"),
    ("runs/vision_v170h", "runs/vision_v171h"),
    ("_v170c1127", "_v171c1133"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T171, "v171h", "V171H", HO171))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v171h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v171"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v171" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v171h_c1135"'); seen_run = True; continue
    out2.append(ln)
(S / "c1135_vision_v171_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1124_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1124", "C1136"), ("c1124", "c1136"),
    ("conf_gate_stretch_c1124", "conf_gate_stretch_c1136"),
    ("after V169", "after V171"), ("after V170", "after V171"),
    ("cg86_", "cg87_"),
]:
    out = out.replace(a, b)
(S / "c1136_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1131_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1131", "C1137"), ("c1131", "c1137"),
    ("capture_regression_c1131", "capture_regression_c1137"),
    ("after C1127-C1130", "after C1133-C1136"),
    ("V4-V170+heldout", "V4-V171+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V170", DOC / "C1128_VISION_V170_SMOKE.json"),'
if needle in out and "VISION_V171_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V171", DOC / "C1134_VISION_V171_SMOKE.json"),\n    ("V171_heldout", DOC / "C1135_VISION_V171_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1137_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1132_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1132", "C1138"), ("c1132", "c1138"),
    ("C1128", "C1134"), ("C1129", "C1135"), ("C1131", "C1137"),
    ("C1127", "C1133"),
    ("V170", "V171"), ("v170", "v171"),
    ("V169", "V170"), ("v169", "v170"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1124_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1136_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1130_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1130_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1130"', '"source": "C1130"')
out = out.replace('"source": "C1124"', '"source": "C1136"')
out = out.replace(
    "stage_ready = bool(v171_claim and v171h_claim and v171 >= GATE and v171h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v171_claim and v171h_claim and v171 >= GATE and v171h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1136: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1136: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1130: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1136: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1124): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1130): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1136): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1130): replace={replace} pass={u2c_pass}"',
)
(S / "c1138_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T171 if t[0].endswith("b")])
print("qty", TR171[1], HO171[1], "po", TR171[8], HO171[8], "sla", TR171[6], HO171[6], "fax", TR171[15], HO171[15])
print("done")
