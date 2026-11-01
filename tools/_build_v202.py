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

# *croft ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T202 = [
    ["ashcroft","recv","paid_total","ASHCROFT GRAIN RECV","RECV","x"],
    ["cedarcroft","wh","qty_sum","WH CEDARCROFT BIN","RECV","x"],
    ["dawncroft","refund","refund_done","DAWNCROFT PATCH REFUND","DONE","x"],
    ["elmcroft","tax","tax_base_paid","ELMCROFT TAX SLIP","TAX","x"],
    ["ferncroft","pay","payroll_active","FERNCROFT PAYROLL","PAY","x"],
    ["glencroft","ship","ship_ok","GLENCROFT SHIP DOCK","SHIP","x"],
    ["hazecroft","sla","sla_ok_hours","HAZECROFT SLA CARD","SLA","x"],
    ["inkcroft","exp","exp_sum","INKCROFT EXPENSE","EXP","x"],
    ["jadecroft","po","po_open","JADECROFT PO SHEET","PO","x"],
    ["knotcroft","order","order_paid","KNOTCROFT ORDER","ORD","x"],
    ["lakecroft","dup","dup_mark","LAKECROFT DUP MARK","DUP","x"],
    ["mosscroft","zero","zero_check","MOSSCROFT AIR ZERO","ZERO","x"],
    ["nethercroft","ledger","ledger_net","NETHERCROFT LEDGER","LED","x"],
    ["oakcroft","ui","ui_ok","OAKCROFT UI SCAN","UI","x"],
    ["pinecroft","stack","stack_count","PINECROFT STACK","STK","x"],
    ["quillcroft","fax","fax_pages","QUILLCROFT FAX","FAX","x"],
    ["reedcroft","glare","glare_ok","REEDCROFT GLARE","GLR","x"],
    ["stonecroft","tab","tab_index","STONECROFT TAB INDEX","TAB","x"],
]
TR202 = [
    [1411.0, 1428.5, 1221.0],[740, 780, 820],[1334.0, 1363.25, 1201.0],[1467.0, 1484.0, 1291.0],
    [1529.0, 1553.0, 1261.0],[1287, 1303, 1219],[480.0, 520.0, 730.0],[1377.0, 1408.75, 1225.0],
    [780.0, 740.0, 820.0],[1444.0, 1432.0, 1222.0],[1,1,0],[0,0,0],
    [1510.0, 1531.5, 1247.0],[1,0,0],[1059, 1051, 1029],[1077, 1061, 748],[1,0,0],[1103, 1079, 1049],
]
HO202 = [
    [1281.0, 1293.75, 1174.0],[840, 760, 820],[1239.0, 1252.5, 1162.0],[1354.0, 1370.0, 1203.0],
    [1395.0, 1411.0, 1198.0],[1189, 1203, 1167],[360.0, 400.0, 720.0],[1265.0, 1286.75, 1174.0],
    [840.0, 760.0, 820.0],[1312.0, 1298.0, 1169.0],[1,1,0],[0,0,0],
    [1347.0, 1362.5, 1184.0],[1,0,0],[1036, 1031, 1026],[1051, 1045, 1033],[1,0,0],[1061, 1055, 1034],
]
check(TR202, "TR"); check(HO202, "HO")

(ROOT / "tools/_v202_themes.json").write_text(json.dumps({"themes": T202, "train": TR202, "heldout": HO202}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_202(src):
    src = src.replace("# --- V201 overlays (new vs V50) ---", "# --- V202 overlays (new vs V50) ---")
    src = src.replace("# --- V201 overlays (new vs V49) ---", "# --- V202 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 115.25", "ASHCROFT bait 116.26"),
        ("CEDARW bait 117.27", "CEDARC bait 118.28"),
        ("DAWNW ghost 40.40", "DAWNC ghost 41.41"),
        ("GLENW bait 110.20", "GLENC bait 111.21"),
        ("JADEW bait 101.11", "JADEC bait 102.12"),
        ("NETHERW bait 118.28", "NETHERC bait 119.29"),
        ("ash mist + stone ticks (V201-only)", "ash mist + stone ticks (V202-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD201 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v201_themes.json").read_text(encoding="utf-8"))["themes"])
NEW202 = "_".join(t[0] for t in T202)

out = (S / "c1313_vision_v201_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1313", "C1319"), ("c1313", "c1319"), ("V201", "V202"), ("v201", "v202"),
    ("_v201c1313", "_v202c1319"),
    ("Harder than V200", "Harder than V201"), ("harder than V200", "harder than V201"),
    (OLD201, NEW202),
    ("V201 keeps floor", "V202 keeps floor"),
    ("C1313 design+fixtures; no VL claim", "C1319 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1314 VL smoke", "fixtures only; claim deferred to C1320 VL smoke"),
    ("No claim until C1314 VL", "No claim until C1320 VL"),
    ("kept on V201", "kept on V202"),
    ("vision_images_v201", "vision_images_v202"),
    ("VL_GATE_V201", "VL_GATE_V202"), ("vl_gate_v201", "vl_gate_v202"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V200:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V201: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T202, "v202", "V202", TR202))
out = retarget_202(out)
(S / "c1319_vision_v202_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1314_vision_v201_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1314", "C1320"), ("c1314", "c1320"), ("V201", "V202"), ("v201", "v202"),
    ("vision_images_v201", "vision_images_v202"),
    ("VL_GATE_V201", "VL_GATE_V202"), ("vl_gate_v201", "vl_gate_v202"),
    ("runs/vision_v201", "runs/vision_v202"),
]:
    out = out.replace(a, b)
(S / "c1320_vision_v202_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1315_vision_v201_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1315", "C1321"), ("c1315", "c1321"), ("V201", "V202"), ("v201", "v202"),
    ("vision_images_v201h", "vision_images_v202h"),
    ("vision_images_v201", "vision_images_v202"),
    ("VL_GATE_V201", "VL_GATE_V202"), ("vl_gate_v201", "vl_gate_v202"),
    ("runs/vision_v201h", "runs/vision_v202h"),
    ("_v201c1313", "_v202c1319"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T202, "v202h", "V202H", HO202))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v202h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v202"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v202" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v202h_c1321"'); seen_run = True; continue
    out2.append(ln)
(S / "c1321_vision_v202_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1310_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1310", "C1322"), ("c1310", "c1322"),
    ("product_u2c_c1310", "product_u2c_c1322"),
    ("after V200", "after V202"), ("after V201", "after V202"),
]:
    out = out.replace(a, b)
(S / "c1322_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1317_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1317", "C1323"), ("c1317", "c1323"),
    ("capture_regression_c1317", "capture_regression_c1323"),
    ("after C1313-C1316", "after C1319-C1322"),
    ("V4-V201+heldout", "V4-V202+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V201", DOC / "C1314_VISION_V201_SMOKE.json"),'
if needle in out and "VISION_V202_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V202", DOC / "C1320_VISION_V202_SMOKE.json"),\n    ("V202_heldout", DOC / "C1321_VISION_V202_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1323_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1312_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1312", "C1324"), ("c1312", "c1324"),
    ("C1308", "C1320"), ("C1309", "C1321"), ("C1311", "C1323"),
    ("C1307", "C1319"), ("C1310", "C1322"),
    ("V200", "V202"), ("v200", "v202"),
    ("V199", "V201"), ("v199", "v201"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1304_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1316_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1304"', '"source": "C1316"')
out = out.replace(
    'f"- confidence-gate (prior C1304): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1316): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1324_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T202 if t[0].endswith("b")])
print("qty", TR202[1], HO202[1], "po", TR202[8], HO202[8], "sla", TR202[6], HO202[6], "fax", TR202[15], HO202[15])
print("done")
