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

# *mere ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T200 = [
    ["ashmere","recv","paid_total","ASHMERE GRAIN RECV","RECV","x"],
    ["cedarmere","wh","qty_sum","WH CEDARMERE BIN","RECV","x"],
    ["dawnmere","refund","refund_done","DAWNMERE PATCH REFUND","DONE","x"],
    ["elmmere","tax","tax_base_paid","ELMMERE TAX SLIP","TAX","x"],
    ["fernmere","pay","payroll_active","FERNMERE PAYROLL","PAY","x"],
    ["glenmere","ship","ship_ok","GLENMERE SHIP DOCK","SHIP","x"],
    ["hazemere","sla","sla_ok_hours","HAZEMERE SLA CARD","SLA","x"],
    ["inkmere","exp","exp_sum","INKMERE EXPENSE","EXP","x"],
    ["jademere","po","po_open","JADEMERE PO SHEET","PO","x"],
    ["knotmere","order","order_paid","KNOTMERE ORDER","ORD","x"],
    ["lakemere","dup","dup_mark","LAKEMERE DUP MARK","DUP","x"],
    ["mossmere","zero","zero_check","MOSSMERE AIR ZERO","ZERO","x"],
    ["nethermere","ledger","ledger_net","NETHERMERE LEDGER","LED","x"],
    ["oakmere","ui","ui_ok","OAKMERE UI SCAN","UI","x"],
    ["pinemere","stack","stack_count","PINEMERE STACK","STK","x"],
    ["quillmere","fax","fax_pages","QUILLMERE FAX","FAX","x"],
    ["reedmere","glare","glare_ok","REEDMERE GLARE","GLR","x"],
    ["stonemere","tab","tab_index","STONEMERE TAB INDEX","TAB","x"],
]
TR200 = [
    [1393.0, 1410.5, 1203.0],[740, 780, 820],[1316.0, 1345.25, 1183.0],[1449.0, 1466.0, 1273.0],
    [1511.0, 1535.0, 1243.0],[1269, 1285, 1201],[480.0, 520.0, 710.0],[1359.0, 1390.75, 1207.0],
    [780.0, 740.0, 820.0],[1426.0, 1414.0, 1204.0],[1,1,0],[0,0,0],
    [1492.0, 1513.5, 1229.0],[1,0,0],[1041, 1033, 1011],[1059, 1043, 748],[1,0,0],[1085, 1061, 1031],
]
HO200 = [
    [1263.0, 1275.75, 1156.0],[840, 760, 820],[1221.0, 1234.5, 1144.0],[1336.0, 1352.0, 1185.0],
    [1377.0, 1393.0, 1180.0],[1171, 1185, 1149],[360.0, 400.0, 740.0],[1247.0, 1268.75, 1156.0],
    [840.0, 760.0, 820.0],[1294.0, 1280.0, 1151.0],[1,1,0],[0,0,0],
    [1329.0, 1344.5, 1166.0],[1,0,0],[1018, 1013, 1008],[1033, 1027, 1015],[1,0,0],[1043, 1037, 1016],
]
check(TR200, "TR"); check(HO200, "HO")

(ROOT / "tools/_v200_themes.json").write_text(json.dumps({"themes": T200, "train": TR200, "heldout": HO200}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_200(src):
    src = src.replace("# --- V199 overlays (new vs V50) ---", "# --- V200 overlays (new vs V50) ---")
    src = src.replace("# --- V199 overlays (new vs V49) ---", "# --- V200 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 113.23", "ASHMERE bait 114.24"),
        ("CEDARH bait 115.25", "CEDARM bait 116.26"),
        ("DAWNH ghost 38.38", "DAWNM ghost 39.39"),
        ("GLENH bait 108.18", "GLENM bait 109.19"),
        ("JADEH bait 99.99", "JADEM bait 100.10"),
        ("NETHERH bait 116.26", "NETHERM bait 117.27"),
        ("ash mist + stone ticks (V199-only)", "ash mist + stone ticks (V200-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD199 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v199_themes.json").read_text(encoding="utf-8"))["themes"])
NEW200 = "_".join(t[0] for t in T200)

out = (S / "c1301_vision_v199_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1301", "C1307"), ("c1301", "c1307"), ("V199", "V200"), ("v199", "v200"),
    ("_v199c1301", "_v200c1307"),
    ("Harder than V198", "Harder than V199"), ("harder than V198", "harder than V199"),
    (OLD199, NEW200),
    ("V199 keeps floor", "V200 keeps floor"),
    ("C1301 design+fixtures; no VL claim", "C1307 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1302 VL smoke", "fixtures only; claim deferred to C1308 VL smoke"),
    ("No claim until C1302 VL", "No claim until C1308 VL"),
    ("kept on V199", "kept on V200"),
    ("vision_images_v199", "vision_images_v200"),
    ("VL_GATE_V199", "VL_GATE_V200"), ("vl_gate_v199", "vl_gate_v200"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V198:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V199: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T200, "v200", "V200", TR200))
out = retarget_200(out)
(S / "c1307_vision_v200_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1302_vision_v199_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1302", "C1308"), ("c1302", "c1308"), ("V199", "V200"), ("v199", "v200"),
    ("vision_images_v199", "vision_images_v200"),
    ("VL_GATE_V199", "VL_GATE_V200"), ("vl_gate_v199", "vl_gate_v200"),
    ("runs/vision_v199", "runs/vision_v200"),
]:
    out = out.replace(a, b)
(S / "c1308_vision_v200_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1303_vision_v199_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1303", "C1309"), ("c1303", "c1309"), ("V199", "V200"), ("v199", "v200"),
    ("vision_images_v199h", "vision_images_v200h"),
    ("vision_images_v199", "vision_images_v200"),
    ("VL_GATE_V199", "VL_GATE_V200"), ("vl_gate_v199", "vl_gate_v200"),
    ("runs/vision_v199h", "runs/vision_v200h"),
    ("_v199c1301", "_v200c1307"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T200, "v200h", "V200H", HO200))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v200h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v200"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v200" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v200h_c1309"'); seen_run = True; continue
    out2.append(ln)
(S / "c1309_vision_v200_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1298_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1298", "C1310"), ("c1298", "c1310"),
    ("product_u2c_c1298", "product_u2c_c1310"),
    ("after V198", "after V200"), ("after V199", "after V200"),
]:
    out = out.replace(a, b)
(S / "c1310_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1305_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1305", "C1311"), ("c1305", "c1311"),
    ("capture_regression_c1305", "capture_regression_c1311"),
    ("after C1301-C1304", "after C1307-C1310"),
    ("V4-V199+heldout", "V4-V200+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V199", DOC / "C1302_VISION_V199_SMOKE.json"),'
if needle in out and "VISION_V200_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V200", DOC / "C1308_VISION_V200_SMOKE.json"),\n    ("V200_heldout", DOC / "C1309_VISION_V200_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1311_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1300_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1300", "C1312"), ("c1300", "c1312"),
    ("C1296", "C1308"), ("C1297", "C1309"), ("C1299", "C1311"),
    ("C1295", "C1307"), ("C1298", "C1310"),
    ("V198", "V200"), ("v198", "v200"),
    ("V197", "V199"), ("v197", "v199"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1292_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1304_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1292"', '"source": "C1304"')
out = out.replace(
    'f"- confidence-gate (prior C1292): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1304): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1312_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T200 if t[0].endswith("b")])
print("qty", TR200[1], HO200[1], "po", TR200[8], HO200[8], "sla", TR200[6], HO200[6], "fax", TR200[15], HO200[15])
print("done")
