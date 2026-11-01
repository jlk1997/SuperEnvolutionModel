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

# *ford ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T187 = [
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
TR187 = [
    [1276.0, 1293.5, 1086.0],[840, 760, 820],[1199.0, 1228.25, 1066.0],[1332.0, 1349.0, 1156.0],
    [1394.0, 1418.0, 1126.0],[1152, 1168, 1084],[480.0, 520.0, 670.0],[1242.0, 1273.75, 1090.0],
    [840.0, 760.0, 820.0],[1309.0, 1297.0, 1087.0],[1,1,0],[0,0,0],
    [1375.0, 1396.5, 1112.0],[1,0,0],[924, 916, 894],[942, 926, 748],[1,0,0],[968, 944, 914],
]
HO187 = [
    [1146.0, 1158.75, 1039.0],[740, 780, 820],[1104.0, 1117.5, 1027.0],[1219.0, 1235.0, 1068.0],
    [1260.0, 1276.0, 1063.0],[1054, 1068, 1032],[360.0, 400.0, 610.0],[1130.0, 1151.75, 1039.0],
    [780.0, 740.0, 820.0],[1177.0, 1163.0, 1034.0],[1,1,0],[0,0,0],
    [1212.0, 1227.5, 1049.0],[1,0,0],[901, 896, 891],[916, 910, 898],[1,0,0],[926, 920, 899],
]
check(TR187, "TR"); check(HO187, "HO")

(ROOT / "tools/_v187_themes.json").write_text(json.dumps({"themes": T187, "train": TR187, "heldout": HO187}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_187(src):
    src = src.replace("# --- V186 overlays (new vs V50) ---", "# --- V187 overlays (new vs V50) ---")
    src = src.replace("# --- V186 overlays (new vs V49) ---", "# --- V187 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 100.10", "ASHFORD bait 101.11"),
        ("CEDARV bait 102.12", "CEDARF bait 103.13"),
        ("DAWNV ghost 25.25", "DAWNF ghost 26.26"),
        ("GLENV bait 95.95", "GLENF bait 96.96"),
        ("JADEV bait 86.86", "JADEF bait 87.87"),
        ("NETHERV bait 103.13", "NETHERF bait 104.14"),
        ("ash mist + stone ticks (V186-only)", "ash mist + stone ticks (V187-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD186 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v186_themes.json").read_text(encoding="utf-8"))["themes"])
NEW187 = "_".join(t[0] for t in T187)

out = (S / "c1223_vision_v186_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1223", "C1229"), ("c1223", "c1229"), ("V186", "V187"), ("v186", "v187"),
    ("_v186c1223", "_v187c1229"),
    ("Harder than V185", "Harder than V186"), ("harder than V185", "harder than V186"),
    (OLD186, NEW187),
    ("V186 keeps floor", "V187 keeps floor"),
    ("C1223 design+fixtures; no VL claim", "C1229 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1224 VL smoke", "fixtures only; claim deferred to C1230 VL smoke"),
    ("No claim until C1224 VL", "No claim until C1230 VL"),
    ("kept on V186", "kept on V187"),
    ("vision_images_v186", "vision_images_v187"),
    ("VL_GATE_V186", "VL_GATE_V187"), ("vl_gate_v186", "vl_gate_v187"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V185:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V186: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T187, "v187", "V187", TR187))
out = retarget_187(out)
(S / "c1229_vision_v187_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1224_vision_v186_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1224", "C1230"), ("c1224", "c1230"), ("V186", "V187"), ("v186", "v187"),
    ("vision_images_v186", "vision_images_v187"),
    ("VL_GATE_V186", "VL_GATE_V187"), ("vl_gate_v186", "vl_gate_v187"),
    ("runs/vision_v186", "runs/vision_v187"),
]:
    out = out.replace(a, b)
(S / "c1230_vision_v187_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1225_vision_v186_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1225", "C1231"), ("c1225", "c1231"), ("V186", "V187"), ("v186", "v187"),
    ("vision_images_v186h", "vision_images_v187h"),
    ("vision_images_v186", "vision_images_v187"),
    ("VL_GATE_V186", "VL_GATE_V187"), ("vl_gate_v186", "vl_gate_v187"),
    ("runs/vision_v186h", "runs/vision_v187h"),
    ("_v186c1223", "_v187c1229"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T187, "v187h", "V187H", HO187))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v187h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v187"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v187" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v187h_c1231"'); seen_run = True; continue
    out2.append(ln)
(S / "c1231_vision_v187_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1220_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1220", "C1232"), ("c1220", "c1232"),
    ("conf_gate_stretch_c1220", "conf_gate_stretch_c1232"),
    ("cg75_", "cg76_"),
    ("after V185", "after V187"), ("after V186", "after V187"),
]:
    out = out.replace(a, b)
(S / "c1232_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1227_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1227", "C1233"), ("c1227", "c1233"),
    ("capture_regression_c1227", "capture_regression_c1233"),
    ("after C1223-C1226", "after C1229-C1232"),
    ("V4-V186+heldout", "V4-V187+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V186", DOC / "C1224_VISION_V186_SMOKE.json"),'
if needle in out and "VISION_V187_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V187", DOC / "C1230_VISION_V187_SMOKE.json"),\n    ("V187_heldout", DOC / "C1231_VISION_V187_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1233_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1222_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1222", "C1234"), ("c1222", "c1234"),
    ("C1218", "C1230"), ("C1219", "C1231"), ("C1221", "C1233"),
    ("C1217", "C1229"), ("C1220", "C1232"),
    ("V185", "V187"), ("v185", "v187"),
    ("V184", "V186"), ("v184", "v186"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1214_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1226_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1214"', '"source": "C1226"')
out = out.replace(
    'f"- product-U2C (prior C1214): replace={replace} pass={u2c_pass}"',
    'f"- product-U2C (prior C1226): replace={replace} pass={u2c_pass}"',
)
(S / "c1234_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T187 if t[0].endswith("b")])
print("qty", TR187[1], HO187[1], "po", TR187[8], HO187[8], "sla", TR187[6], HO187[6], "fax", TR187[15], HO187[15])
print("done")
