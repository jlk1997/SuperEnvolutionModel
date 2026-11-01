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

# *brook ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 550+590 HO 430+470
T184 = [
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
TR184 = [
    [1249.0, 1266.5, 1059.0],[740, 780, 820],[1172.0, 1201.25, 1039.0],[1305.0, 1322.0, 1129.0],
    [1367.0, 1391.0, 1099.0],[1125, 1141, 1057],[550.0, 590.0, 630.0],[1215.0, 1246.75, 1063.0],
    [780.0, 740.0, 820.0],[1282.0, 1270.0, 1060.0],[1,1,0],[0,0,0],
    [1348.0, 1369.5, 1085.0],[1,0,0],[897, 889, 867],[915, 899, 748],[1,0,0],[941, 917, 887],
]
HO184 = [
    [1119.0, 1131.75, 1012.0],[840, 760, 820],[1077.0, 1090.5, 1000.0],[1192.0, 1208.0, 1041.0],
    [1233.0, 1249.0, 1036.0],[1027, 1041, 1005],[430.0, 470.0, 610.0],[1103.0, 1124.75, 1012.0],
    [840.0, 760.0, 820.0],[1150.0, 1136.0, 1007.0],[1,1,0],[0,0,0],
    [1185.0, 1200.5, 1022.0],[1,0,0],[874, 869, 864],[889, 883, 871],[1,0,0],[899, 893, 872],
]
check(TR184, "TR"); check(HO184, "HO")

(ROOT / "tools/_v184_themes.json").write_text(json.dumps({"themes": T184, "train": TR184, "heldout": HO184}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_184(src):
    src = src.replace("# --- V183 overlays (new vs V50) ---", "# --- V184 overlays (new vs V50) ---")
    src = src.replace("# --- V183 overlays (new vs V49) ---", "# --- V184 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 97.97", "ASHBROOK bait 98.98"),
        ("CEDARF bait 99.99", "CEDARB bait 100.10"),
        ("DAWNF ghost 22.22", "DAWNB ghost 23.23"),
        ("GLENF bait 92.92", "GLENB bait 93.93"),
        ("JADEF bait 83.83", "JADEB bait 84.84"),
        ("NETHERF bait 100.10", "NETHERB bait 101.11"),
        ("ash mist + stone ticks (V183-only)", "ash mist + stone ticks (V184-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD183 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v183_themes.json").read_text(encoding="utf-8"))["themes"])
NEW184 = "_".join(t[0] for t in T184)

out = (S / "c1205_vision_v183_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1205", "C1211"), ("c1205", "c1211"), ("V183", "V184"), ("v183", "v184"),
    ("_v183c1205", "_v184c1211"),
    ("Harder than V182", "Harder than V183"), ("harder than V182", "harder than V183"),
    (OLD183, NEW184),
    ("V183 keeps floor", "V184 keeps floor"),
    ("C1205 design+fixtures; no VL claim", "C1211 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1206 VL smoke", "fixtures only; claim deferred to C1212 VL smoke"),
    ("No claim until C1206 VL", "No claim until C1212 VL"),
    ("kept on V183", "kept on V184"),
    ("vision_images_v183", "vision_images_v184"),
    ("VL_GATE_V183", "VL_GATE_V184"), ("vl_gate_v183", "vl_gate_v184"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V182:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V183: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T184, "v184", "V184", TR184))
out = retarget_184(out)
(S / "c1211_vision_v184_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1206_vision_v183_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1206", "C1212"), ("c1206", "c1212"), ("V183", "V184"), ("v183", "v184"),
    ("vision_images_v183", "vision_images_v184"),
    ("VL_GATE_V183", "VL_GATE_V184"), ("vl_gate_v183", "vl_gate_v184"),
    ("runs/vision_v183", "runs/vision_v184"),
]:
    out = out.replace(a, b)
(S / "c1212_vision_v184_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1207_vision_v183_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1207", "C1213"), ("c1207", "c1213"), ("V183", "V184"), ("v183", "v184"),
    ("vision_images_v183h", "vision_images_v184h"),
    ("vision_images_v183", "vision_images_v184"),
    ("VL_GATE_V183", "VL_GATE_V184"), ("vl_gate_v183", "vl_gate_v184"),
    ("runs/vision_v183h", "runs/vision_v184h"),
    ("_v183c1205", "_v184c1211"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T184, "v184h", "V184H", HO184))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v184h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v184"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v184" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v184h_c1213"'); seen_run = True; continue
    out2.append(ln)
(S / "c1213_vision_v184_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1202_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1202", "C1214"), ("c1202", "c1214"),
    ("product_u2c_c1202", "product_u2c_c1214"),
    ("after V182", "after V184"), ("after V183", "after V184"),
]:
    out = out.replace(a, b)
(S / "c1214_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1209_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1209", "C1215"), ("c1209", "c1215"),
    ("capture_regression_c1209", "capture_regression_c1215"),
    ("after C1205-C1208", "after C1211-C1214"),
    ("V4-V183+heldout", "V4-V184+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V183", DOC / "C1206_VISION_V183_SMOKE.json"),'
if needle in out and "VISION_V184_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V184", DOC / "C1212_VISION_V184_SMOKE.json"),\n    ("V184_heldout", DOC / "C1213_VISION_V184_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1215_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1204_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1204", "C1216"), ("c1204", "c1216"),
    ("C1200", "C1212"), ("C1201", "C1213"), ("C1203", "C1215"),
    ("C1199", "C1211"), ("C1202", "C1214"),
    ("V182", "V184"), ("v182", "v184"),
    ("V181", "V183"), ("v181", "v183"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1196_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1208_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1196"', '"source": "C1208"')
out = out.replace(
    'f"- confidence-gate (prior C1196): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1208): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1216_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T184 if t[0].endswith("b")])
print("qty", TR184[1], HO184[1], "po", TR184[8], HO184[8], "sla", TR184[6], HO184[6], "fax", TR184[15], HO184[15])
print("done")
