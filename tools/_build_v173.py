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

# *brook ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
T173 = [
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
TR173 = [
    [1150.0, 1167.5, 960.0],[840, 760, 820],[1073.0, 1102.25, 940.0],[1206.0, 1223.0, 1030.0],
    [1268.0, 1292.0, 1000.0],[1026, 1042, 958],[460.0, 500.0, 520.0],[1116.0, 1147.75, 964.0],
    [840.0, 760.0, 770.0],[1183.0, 1171.0, 961.0],[1,1,0],[0,0,0],
    [1249.0, 1270.5, 986.0],[1,0,0],[798, 790, 768],[816, 800, 748],[1,0,0],[842, 818, 788],
]
# fix banned: PO closed 770
TR173[8] = [840.0, 760.0, 780.0]
HO173 = [
    [1020.0, 1032.75, 913.0],[740, 780, 820],[978.0, 991.5, 901.0],[1093.0, 1109.0, 942.0],
    [1134.0, 1150.0, 937.0],[928, 942, 906],[360.0, 400.0, 500.0],[1004.0, 1025.75, 913.0],
    [780.0, 740.0, 750.0],[1051.0, 1037.0, 908.0],[1,1,0],[0,0,0],
    [1086.0, 1101.5, 923.0],[1,0,0],[776, 771, 766],[790, 784, 772],[1,0,0],[800, 794, 773],
]
# fix banned: HO po closed 750
HO173[8] = [780.0, 740.0, 760.0]
check(TR173, "TR"); check(HO173, "HO")

(ROOT / "tools/_v173_themes.json").write_text(json.dumps({"themes": T173, "train": TR173, "heldout": HO173}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_173(src):
    src = src.replace("# --- V172 overlays (new vs V50) ---", "# --- V173 overlays (new vs V50) ---")
    src = src.replace("# --- V172 overlays (new vs V49) ---", "# --- V173 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 86.86", "ASHBROOK bait 87.87"),
        ("CEDARF bait 88.88", "CEDARB bait 89.89"),
        ("DAWNF ghost 11.11", "DAWNB ghost 12.12"),
        ("GLENF bait 81.81", "GLENB bait 82.82"),
        ("JADEF bait 72.72", "JADEB bait 73.73"),
        ("NETHERF bait 89.89", "NETHERB bait 90.90"),
        ("ash mist + stone ticks (V172-only)", "ash mist + stone ticks (V173-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD172 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v172_themes.json").read_text(encoding="utf-8"))["themes"])
NEW173 = "_".join(t[0] for t in T173)

out = (S / "c1139_vision_v172_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1139", "C1145"), ("c1139", "c1145"), ("V172", "V173"), ("v172", "v173"),
    ("_v172c1139", "_v173c1145"),
    ("Harder than V171", "Harder than V172"), ("harder than V171", "harder than V172"),
    (OLD172, NEW173),
    ("V172 keeps floor", "V173 keeps floor"),
    ("C1139 design+fixtures; no VL claim", "C1145 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1140 VL smoke", "fixtures only; claim deferred to C1146 VL smoke"),
    ("No claim until C1140 VL", "No claim until C1146 VL"),
    ("kept on V172", "kept on V173"),
    ("vision_images_v172", "vision_images_v173"),
    ("VL_GATE_V172", "VL_GATE_V173"), ("vl_gate_v172", "vl_gate_v173"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V171:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V172: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T173, "v173", "V173", TR173))
out = retarget_173(out)
(S / "c1145_vision_v173_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1140_vision_v172_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1140", "C1146"), ("c1140", "c1146"), ("V172", "V173"), ("v172", "v173"),
    ("vision_images_v172", "vision_images_v173"),
    ("VL_GATE_V172", "VL_GATE_V173"), ("vl_gate_v172", "vl_gate_v173"),
    ("runs/vision_v172", "runs/vision_v173"),
]:
    out = out.replace(a, b)
(S / "c1146_vision_v173_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1141_vision_v172_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1141", "C1147"), ("c1141", "c1147"), ("V172", "V173"), ("v172", "v173"),
    ("vision_images_v172h", "vision_images_v173h"),
    ("vision_images_v172", "vision_images_v173"),
    ("VL_GATE_V172", "VL_GATE_V173"), ("vl_gate_v172", "vl_gate_v173"),
    ("runs/vision_v172h", "runs/vision_v173h"),
    ("_v172c1139", "_v173c1145"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T173, "v173h", "V173H", HO173))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v173h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v173"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v173" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v173h_c1147"'); seen_run = True; continue
    out2.append(ln)
(S / "c1147_vision_v173_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1136_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1136", "C1148"), ("c1136", "c1148"),
    ("conf_gate_stretch_c1136", "conf_gate_stretch_c1148"),
    ("after V171", "after V173"), ("after V172", "after V173"),
    ("cg87_", "cg88_"),
]:
    out = out.replace(a, b)
(S / "c1148_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1143_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1143", "C1149"), ("c1143", "c1149"),
    ("capture_regression_c1143", "capture_regression_c1149"),
    ("after C1139-C1142", "after C1145-C1148"),
    ("V4-V172+heldout", "V4-V173+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V172", DOC / "C1140_VISION_V172_SMOKE.json"),'
if needle in out and "VISION_V173_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V173", DOC / "C1146_VISION_V173_SMOKE.json"),\n    ("V173_heldout", DOC / "C1147_VISION_V173_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1149_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1144_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1144", "C1150"), ("c1144", "c1150"),
    ("C1140", "C1146"), ("C1141", "C1147"), ("C1143", "C1149"),
    ("C1139", "C1145"),
    ("V172", "V173"), ("v172", "v173"),
    ("V171", "V172"), ("v171", "v172"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1136_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1148_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1142_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1142_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1142"', '"source": "C1142"')
out = out.replace('"source": "C1136"', '"source": "C1148"')
out = out.replace(
    "stage_ready = bool(v173_claim and v173h_claim and v173 >= GATE and v173h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v173_claim and v173h_claim and v173 >= GATE and v173h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1148: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1148: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1142: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1148: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1136): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1142): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1148): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1142): replace={replace} pass={u2c_pass}"',
)
(S / "c1150_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T173 if t[0].endswith("b")])
print("qty", TR173[1], HO173[1], "po", TR173[8], HO173[8], "sla", TR173[6], HO173[6], "fax", TR173[15], HO173[15])
print("done")
