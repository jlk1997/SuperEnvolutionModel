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

# *brook ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T206 = [
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
TR206 = [
    [1447.0, 1464.5, 1257.0],[740, 780, 820],[1370.0, 1399.25, 1237.0],[1503.0, 1520.0, 1327.0],
    [1565.0, 1589.0, 1297.0],[1323, 1339, 1255],[480.0, 520.0, 730.0],[1413.0, 1444.75, 1261.0],
    [780.0, 740.0, 820.0],[1480.0, 1468.0, 1258.0],[1,1,0],[0,0,0],
    [1546.0, 1567.5, 1283.0],[1,0,0],[1095, 1087, 1065],[1113, 1097, 748],[1,0,0],[1139, 1115, 1085],
]
HO206 = [
    [1317.0, 1329.75, 1210.0],[840, 760, 820],[1275.0, 1288.5, 1198.0],[1390.0, 1406.0, 1239.0],
    [1431.0, 1447.0, 1234.0],[1225, 1239, 1203],[360.0, 400.0, 720.0],[1301.0, 1322.75, 1210.0],
    [840.0, 760.0, 820.0],[1348.0, 1334.0, 1205.0],[1,1,0],[0,0,0],
    [1383.0, 1398.5, 1220.0],[1,0,0],[1072, 1067, 1062],[1087, 1081, 1069],[1,0,0],[1097, 1091, 1070],
]
check(TR206, "TR"); check(HO206, "HO")

(ROOT / "tools/_v206_themes.json").write_text(json.dumps({"themes": T206, "train": TR206, "heldout": HO206}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_206(src):
    src = src.replace("# --- V205 overlays (new vs V50) ---", "# --- V206 overlays (new vs V50) ---")
    src = src.replace("# --- V205 overlays (new vs V49) ---", "# --- V206 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 119.29", "ASHBROOK bait 120.30"),
        ("CEDARF bait 121.31", "CEDARB bait 122.32"),
        ("DAWNF ghost 44.44", "DAWNB ghost 45.45"),
        ("GLENF bait 114.24", "GLENB bait 115.25"),
        ("JADEF bait 105.15", "JADEB bait 106.16"),
        ("NETHERF bait 122.32", "NETHERB bait 123.33"),
        ("ash mist + stone ticks (V205-only)", "ash mist + stone ticks (V206-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD205 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v205_themes.json").read_text(encoding="utf-8"))["themes"])
NEW206 = "_".join(t[0] for t in T206)

out = (S / "c1337_vision_v205_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1337", "C1343"), ("c1337", "c1343"), ("V205", "V206"), ("v205", "v206"),
    ("_v205c1337", "_v206c1343"),
    ("Harder than V204", "Harder than V205"), ("harder than V204", "harder than V205"),
    (OLD205, NEW206),
    ("V205 keeps floor", "V206 keeps floor"),
    ("C1337 design+fixtures; no VL claim", "C1343 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1338 VL smoke", "fixtures only; claim deferred to C1344 VL smoke"),
    ("No claim until C1338 VL", "No claim until C1344 VL"),
    ("kept on V205", "kept on V206"),
    ("vision_images_v205", "vision_images_v206"),
    ("VL_GATE_V205", "VL_GATE_V206"), ("vl_gate_v205", "vl_gate_v206"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V204:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V205: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T206, "v206", "V206", TR206))
out = retarget_206(out)
(S / "c1343_vision_v206_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1338_vision_v205_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1338", "C1344"), ("c1338", "c1344"), ("V205", "V206"), ("v205", "v206"),
    ("vision_images_v205", "vision_images_v206"),
    ("VL_GATE_V205", "VL_GATE_V206"), ("vl_gate_v205", "vl_gate_v206"),
    ("runs/vision_v205", "runs/vision_v206"),
]:
    out = out.replace(a, b)
(S / "c1344_vision_v206_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1339_vision_v205_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1339", "C1345"), ("c1339", "c1345"), ("V205", "V206"), ("v205", "v206"),
    ("vision_images_v205h", "vision_images_v206h"),
    ("vision_images_v205", "vision_images_v206"),
    ("VL_GATE_V205", "VL_GATE_V206"), ("vl_gate_v205", "vl_gate_v206"),
    ("runs/vision_v205h", "runs/vision_v206h"),
    ("_v205c1337", "_v206c1343"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T206, "v206h", "V206H", HO206))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v206h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v206"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v206" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v206h_c1345"'); seen_run = True; continue
    out2.append(ln)
(S / "c1345_vision_v206_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1334_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1334", "C1346"), ("c1334", "c1346"),
    ("product_u2c_c1334", "product_u2c_c1346"),
    ("after V204", "after V206"), ("after V205", "after V206"),
]:
    out = out.replace(a, b)
(S / "c1346_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1341_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1341", "C1347"), ("c1341", "c1347"),
    ("capture_regression_c1341", "capture_regression_c1347"),
    ("after C1337-C1340", "after C1343-C1346"),
    ("V4-V205+heldout", "V4-V206+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V205", DOC / "C1338_VISION_V205_SMOKE.json"),'
if needle in out and "VISION_V206_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V206", DOC / "C1344_VISION_V206_SMOKE.json"),\n    ("V206_heldout", DOC / "C1345_VISION_V206_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1347_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1336_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1336", "C1348"), ("c1336", "c1348"),
    ("C1332", "C1344"), ("C1333", "C1345"), ("C1335", "C1347"),
    ("C1331", "C1343"), ("C1334", "C1346"),
    ("V204", "V206"), ("v204", "v206"),
    ("V203", "V205"), ("v203", "v205"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1328_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1340_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1328"', '"source": "C1340"')
out = out.replace(
    'f"- confidence-gate (prior C1328): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1340): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1348_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T206 if t[0].endswith("b")])
print("qty", TR206[1], HO206[1], "po", TR206[8], HO206[8], "sla", TR206[6], HO206[6], "fax", TR206[15], HO206[15])
print("done")
