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

# *dale ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T174 = [
    ["ashdale","recv","paid_total","ASHDALE GRAIN RECV","RECV","x"],
    ["cedardale","wh","qty_sum","WH CEDARDALE BIN","RECV","x"],
    ["dawndale","refund","refund_done","DAWNDALE PATCH REFUND","DONE","x"],
    ["elmdale","tax","tax_base_paid","ELMDALE TAX SLIP","TAX","x"],
    ["ferndale","pay","payroll_active","FERNDALE PAYROLL","PAY","x"],
    ["glendale","ship","ship_ok","GLENDALE SHIP DOCK","SHIP","x"],
    ["hazedale","sla","sla_ok_hours","HAZEDALE SLA CARD","SLA","x"],
    ["inkdale","exp","exp_sum","INKDALE EXPENSE","EXP","x"],
    ["jadedale","po","po_open","JADEDALE PO SHEET","PO","x"],
    ["knotdale","order","order_paid","KNOTDALE ORDER","ORD","x"],
    ["lakedale","dup","dup_mark","LAKEDALE DUP MARK","DUP","x"],
    ["mossdale","zero","zero_check","MOSSDALE AIR ZERO","ZERO","x"],
    ["netherdale","ledger","ledger_net","NETHERDALE LEDGER","LED","x"],
    ["oakdale","ui","ui_ok","OAKDALE UI SCAN","UI","x"],
    ["pinedale","stack","stack_count","PINEDALE STACK","STK","x"],
    ["quilldale","fax","fax_pages","QUILLDALE FAX","FAX","x"],
    ["reeddale","glare","glare_ok","REEDDALE GLARE","GLR","x"],
    ["stonedale","tab","tab_index","STONEDALE TAB INDEX","TAB","x"],
]
TR174 = [
    [1159.0, 1176.5, 969.0],[740, 780, 820],[1082.0, 1111.25, 949.0],[1215.0, 1232.0, 1039.0],
    [1277.0, 1301.0, 1009.0],[1035, 1051, 967],[480.0, 520.0, 530.0],[1125.0, 1156.75, 973.0],
    [780.0, 740.0, 780.0],[1192.0, 1180.0, 970.0],[1,1,0],[0,0,0],
    [1258.0, 1279.5, 995.0],[1,0,0],[807, 799, 777],[825, 809, 748],[1,0,0],[851, 827, 797],
]
HO174 = [
    [1029.0, 1041.75, 922.0],[840, 760, 820],[987.0, 1000.5, 910.0],[1102.0, 1118.0, 951.0],
    [1143.0, 1159.0, 946.0],[937, 951, 915],[360.0, 400.0, 510.0],[1013.0, 1034.75, 922.0],
    [840.0, 760.0, 770.0],[1060.0, 1046.0, 917.0],[1,1,0],[0,0,0],
    [1095.0, 1110.5, 932.0],[1,0,0],[785, 780, 775],[799, 793, 781],[1,0,0],[809, 803, 782],
]
# fix banned HO po closed 770
HO174[8] = [840.0, 760.0, 780.0]
check(TR174, "TR"); check(HO174, "HO")

(ROOT / "tools/_v174_themes.json").write_text(json.dumps({"themes": T174, "train": TR174, "heldout": HO174}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_174(src):
    src = src.replace("# --- V173 overlays (new vs V50) ---", "# --- V174 overlays (new vs V50) ---")
    src = src.replace("# --- V173 overlays (new vs V49) ---", "# --- V174 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 87.87", "ASHDALE bait 88.88"),
        ("CEDARB bait 89.89", "CEDARD bait 90.90"),
        ("DAWNB ghost 12.12", "DAWND ghost 13.13"),
        ("GLENB bait 82.82", "GLEND bait 83.83"),
        ("JADEB bait 73.73", "JADED bait 74.74"),
        ("NETHERB bait 90.90", "NETHERD bait 91.91"),
        ("ash mist + stone ticks (V173-only)", "ash mist + stone ticks (V174-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD173 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v173_themes.json").read_text(encoding="utf-8"))["themes"])
NEW174 = "_".join(t[0] for t in T174)

out = (S / "c1145_vision_v173_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1145", "C1151"), ("c1145", "c1151"), ("V173", "V174"), ("v173", "v174"),
    ("_v173c1145", "_v174c1151"),
    ("Harder than V172", "Harder than V173"), ("harder than V172", "harder than V173"),
    (OLD173, NEW174),
    ("V173 keeps floor", "V174 keeps floor"),
    ("C1145 design+fixtures; no VL claim", "C1151 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1146 VL smoke", "fixtures only; claim deferred to C1152 VL smoke"),
    ("No claim until C1146 VL", "No claim until C1152 VL"),
    ("kept on V173", "kept on V174"),
    ("vision_images_v173", "vision_images_v174"),
    ("VL_GATE_V173", "VL_GATE_V174"), ("vl_gate_v173", "vl_gate_v174"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V172:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V173: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T174, "v174", "V174", TR174))
out = retarget_174(out)
(S / "c1151_vision_v174_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1146_vision_v173_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1146", "C1152"), ("c1146", "c1152"), ("V173", "V174"), ("v173", "v174"),
    ("vision_images_v173", "vision_images_v174"),
    ("VL_GATE_V173", "VL_GATE_V174"), ("vl_gate_v173", "vl_gate_v174"),
    ("runs/vision_v173", "runs/vision_v174"),
]:
    out = out.replace(a, b)
(S / "c1152_vision_v174_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1147_vision_v173_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1147", "C1153"), ("c1147", "c1153"), ("V173", "V174"), ("v173", "v174"),
    ("vision_images_v173h", "vision_images_v174h"),
    ("vision_images_v173", "vision_images_v174"),
    ("VL_GATE_V173", "VL_GATE_V174"), ("vl_gate_v173", "vl_gate_v174"),
    ("runs/vision_v173h", "runs/vision_v174h"),
    ("_v173c1145", "_v174c1151"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T174, "v174h", "V174H", HO174))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v174h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v174"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v174" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v174h_c1153"'); seen_run = True; continue
    out2.append(ln)
(S / "c1153_vision_v174_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1142_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1142", "C1154"), ("c1142", "c1154"),
    ("product_u2c_c1142", "product_u2c_c1154"),
    ("after V172", "after V174"), ("after V173", "after V174"),
]:
    out = out.replace(a, b)
(S / "c1154_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1149_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1149", "C1155"), ("c1149", "c1155"),
    ("capture_regression_c1149", "capture_regression_c1155"),
    ("after C1145-C1148", "after C1151-C1154"),
    ("V4-V173+heldout", "V4-V174+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V173", DOC / "C1146_VISION_V173_SMOKE.json"),'
if needle in out and "VISION_V174_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V174", DOC / "C1152_VISION_V174_SMOKE.json"),\n    ("V174_heldout", DOC / "C1153_VISION_V174_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1155_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1150_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1150", "C1156"), ("c1150", "c1156"),
    ("C1146", "C1152"), ("C1147", "C1153"), ("C1149", "C1155"),
    ("C1145", "C1151"),
    ("V173", "V174"), ("v173", "v174"),
    ("V172", "V173"), ("v172", "v173"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1148_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1148_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1142_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1154_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1142"', '"source": "C1154"')
out = out.replace('"source": "C1148"', '"source": "C1148"')
out = out.replace(
    "stage_ready = bool(v174_claim and v174h_claim and v174 >= GATE and v174h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v174_claim and v174h_claim and v174 >= GATE and v174h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1154: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1154: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1148: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1154: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1142): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1148): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1154): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1148): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1156_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T174 if t[0].endswith("b")])
print("qty", TR174[1], HO174[1], "po", TR174[8], HO174[8], "sla", TR174[6], HO174[6], "fax", TR174[15], HO174[15])
print("done")
