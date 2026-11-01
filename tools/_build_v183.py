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

# *fen ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 540+580 HO 420+460
T183 = [
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
TR183 = [
    [1240.0, 1257.5, 1050.0],[840, 760, 820],[1163.0, 1192.25, 1030.0],[1296.0, 1313.0, 1120.0],
    [1358.0, 1382.0, 1090.0],[1116, 1132, 1048],[540.0, 580.0, 620.0],[1206.0, 1237.75, 1054.0],
    [840.0, 760.0, 820.0],[1273.0, 1261.0, 1051.0],[1,1,0],[0,0,0],
    [1339.0, 1360.5, 1076.0],[1,0,0],[888, 880, 858],[906, 890, 748],[1,0,0],[932, 908, 878],
]
HO183 = [
    [1110.0, 1122.75, 1003.0],[740, 780, 820],[1068.0, 1081.5, 991.0],[1183.0, 1199.0, 1032.0],
    [1224.0, 1240.0, 1027.0],[1018, 1032, 996],[420.0, 460.0, 600.0],[1094.0, 1115.75, 1003.0],
    [780.0, 740.0, 820.0],[1141.0, 1127.0, 998.0],[1,1,0],[0,0,0],
    [1176.0, 1191.5, 1013.0],[1,0,0],[865, 860, 855],[880, 874, 862],[1,0,0],[890, 884, 863],
]
check(TR183, "TR"); check(HO183, "HO")

(ROOT / "tools/_v183_themes.json").write_text(json.dumps({"themes": T183, "train": TR183, "heldout": HO183}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_183(src):
    src = src.replace("# --- V182 overlays (new vs V50) ---", "# --- V183 overlays (new vs V50) ---")
    src = src.replace("# --- V182 overlays (new vs V49) ---", "# --- V183 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 96.96", "ASHFEN bait 97.97"),
        ("CEDARM bait 98.98", "CEDARF bait 99.99"),
        ("DAWNM ghost 21.21", "DAWNF ghost 22.22"),
        ("GLENM bait 91.91", "GLENF bait 92.92"),
        ("JADEM bait 82.82", "JADEF bait 83.83"),
        ("NETHERM bait 99.99", "NETHERF bait 100.10"),
        ("ash mist + stone ticks (V182-only)", "ash mist + stone ticks (V183-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD182 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v182_themes.json").read_text(encoding="utf-8"))["themes"])
NEW183 = "_".join(t[0] for t in T183)

out = (S / "c1199_vision_v182_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1199", "C1205"), ("c1199", "c1205"), ("V182", "V183"), ("v182", "v183"),
    ("_v182c1199", "_v183c1205"),
    ("Harder than V181", "Harder than V182"), ("harder than V181", "harder than V182"),
    (OLD182, NEW183),
    ("V182 keeps floor", "V183 keeps floor"),
    ("C1199 design+fixtures; no VL claim", "C1205 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1200 VL smoke", "fixtures only; claim deferred to C1206 VL smoke"),
    ("No claim until C1200 VL", "No claim until C1206 VL"),
    ("kept on V182", "kept on V183"),
    ("vision_images_v182", "vision_images_v183"),
    ("VL_GATE_V182", "VL_GATE_V183"), ("vl_gate_v182", "vl_gate_v183"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V181:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V182: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T183, "v183", "V183", TR183))
out = retarget_183(out)
(S / "c1205_vision_v183_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1200_vision_v182_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1200", "C1206"), ("c1200", "c1206"), ("V182", "V183"), ("v182", "v183"),
    ("vision_images_v182", "vision_images_v183"),
    ("VL_GATE_V182", "VL_GATE_V183"), ("vl_gate_v182", "vl_gate_v183"),
    ("runs/vision_v182", "runs/vision_v183"),
]:
    out = out.replace(a, b)
(S / "c1206_vision_v183_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1201_vision_v182_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1201", "C1207"), ("c1201", "c1207"), ("V182", "V183"), ("v182", "v183"),
    ("vision_images_v182h", "vision_images_v183h"),
    ("vision_images_v182", "vision_images_v183"),
    ("VL_GATE_V182", "VL_GATE_V183"), ("vl_gate_v182", "vl_gate_v183"),
    ("runs/vision_v182h", "runs/vision_v183h"),
    ("_v182c1199", "_v183c1205"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T183, "v183h", "V183H", HO183))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v183h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v183"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v183" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v183h_c1207"'); seen_run = True; continue
    out2.append(ln)
(S / "c1207_vision_v183_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1196_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1196", "C1208"), ("c1196", "c1208"),
    ("conf_gate_stretch_c1196", "conf_gate_stretch_c1208"),
    ("cg73_", "cg74_"),
    ("after V181", "after V183"), ("after V182", "after V183"),
]:
    out = out.replace(a, b)
(S / "c1208_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1203_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1203", "C1209"), ("c1203", "c1209"),
    ("capture_regression_c1203", "capture_regression_c1209"),
    ("after C1199-C1202", "after C1205-C1208"),
    ("V4-V182+heldout", "V4-V183+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V182", DOC / "C1200_VISION_V182_SMOKE.json"),'
if needle in out and "VISION_V183_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V183", DOC / "C1206_VISION_V183_SMOKE.json"),\n    ("V183_heldout", DOC / "C1207_VISION_V183_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1209_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1198_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1198", "C1210"), ("c1198", "c1210"),
    ("C1194", "C1206"), ("C1195", "C1207"), ("C1197", "C1209"),
    ("C1193", "C1205"), ("C1196", "C1208"),
    ("V181", "V183"), ("v181", "v183"),
    ("V180", "V182"), ("v180", "v182"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1190_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1202_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1190"', '"source": "C1202"')
out = out.replace(
    'f"- product-U2C (prior C1190): replace={replace} pass={u2c_pass}"',
    'f"- product-U2C (prior C1202): replace={replace} pass={u2c_pass}"',
)
(S / "c1210_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T183 if t[0].endswith("b")])
print("qty", TR183[1], HO183[1], "po", TR183[8], HO183[8], "sla", TR183[6], HO183[6], "fax", TR183[15], HO183[15])
print("done")
