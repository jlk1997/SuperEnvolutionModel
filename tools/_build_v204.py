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

# *moor ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T204 = [
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
TR204 = [
    [1429.0, 1446.5, 1239.0],[740, 780, 820],[1352.0, 1381.25, 1219.0],[1485.0, 1502.0, 1309.0],
    [1547.0, 1571.0, 1279.0],[1305, 1321, 1237],[480.0, 520.0, 710.0],[1395.0, 1426.75, 1243.0],
    [780.0, 740.0, 820.0],[1462.0, 1450.0, 1240.0],[1,1,0],[0,0,0],
    [1528.0, 1549.5, 1265.0],[1,0,0],[1077, 1069, 1047],[1095, 1079, 748],[1,0,0],[1121, 1097, 1067],
]
HO204 = [
    [1299.0, 1311.75, 1192.0],[840, 760, 820],[1257.0, 1270.5, 1180.0],[1372.0, 1388.0, 1221.0],
    [1413.0, 1429.0, 1216.0],[1207, 1221, 1185],[360.0, 400.0, 740.0],[1283.0, 1304.75, 1192.0],
    [840.0, 760.0, 820.0],[1330.0, 1316.0, 1187.0],[1,1,0],[0,0,0],
    [1365.0, 1380.5, 1202.0],[1,0,0],[1054, 1049, 1044],[1069, 1063, 1051],[1,0,0],[1079, 1073, 1052],
]
check(TR204, "TR"); check(HO204, "HO")

(ROOT / "tools/_v204_themes.json").write_text(json.dumps({"themes": T204, "train": TR204, "heldout": HO204}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_204(src):
    src = src.replace("# --- V203 overlays (new vs V50) ---", "# --- V204 overlays (new vs V50) ---")
    src = src.replace("# --- V203 overlays (new vs V49) ---", "# --- V204 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 117.27", "ASHMOOR bait 118.28"),
        ("CEDARH bait 119.29", "CEDARM bait 120.30"),
        ("DAWNH ghost 42.42", "DAWNM ghost 43.43"),
        ("GLENH bait 112.22", "GLENM bait 113.23"),
        ("JADEH bait 103.13", "JADEM bait 104.14"),
        ("NETHERH bait 120.30", "NETHERM bait 121.31"),
        ("ash mist + stone ticks (V203-only)", "ash mist + stone ticks (V204-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD203 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v203_themes.json").read_text(encoding="utf-8"))["themes"])
NEW204 = "_".join(t[0] for t in T204)

out = (S / "c1325_vision_v203_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1325", "C1331"), ("c1325", "c1331"), ("V203", "V204"), ("v203", "v204"),
    ("_v203c1325", "_v204c1331"),
    ("Harder than V202", "Harder than V203"), ("harder than V202", "harder than V203"),
    (OLD203, NEW204),
    ("V203 keeps floor", "V204 keeps floor"),
    ("C1325 design+fixtures; no VL claim", "C1331 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1326 VL smoke", "fixtures only; claim deferred to C1332 VL smoke"),
    ("No claim until C1326 VL", "No claim until C1332 VL"),
    ("kept on V203", "kept on V204"),
    ("vision_images_v203", "vision_images_v204"),
    ("VL_GATE_V203", "VL_GATE_V204"), ("vl_gate_v203", "vl_gate_v204"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V202:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V203: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T204, "v204", "V204", TR204))
out = retarget_204(out)
(S / "c1331_vision_v204_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1326_vision_v203_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1326", "C1332"), ("c1326", "c1332"), ("V203", "V204"), ("v203", "v204"),
    ("vision_images_v203", "vision_images_v204"),
    ("VL_GATE_V203", "VL_GATE_V204"), ("vl_gate_v203", "vl_gate_v204"),
    ("runs/vision_v203", "runs/vision_v204"),
]:
    out = out.replace(a, b)
(S / "c1332_vision_v204_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1327_vision_v203_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1327", "C1333"), ("c1327", "c1333"), ("V203", "V204"), ("v203", "v204"),
    ("vision_images_v203h", "vision_images_v204h"),
    ("vision_images_v203", "vision_images_v204"),
    ("VL_GATE_V203", "VL_GATE_V204"), ("vl_gate_v203", "vl_gate_v204"),
    ("runs/vision_v203h", "runs/vision_v204h"),
    ("_v203c1325", "_v204c1331"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T204, "v204h", "V204H", HO204))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v204h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v204"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v204" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v204h_c1333"'); seen_run = True; continue
    out2.append(ln)
(S / "c1333_vision_v204_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1322_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1322", "C1334"), ("c1322", "c1334"),
    ("product_u2c_c1322", "product_u2c_c1334"),
    ("after V202", "after V204"), ("after V203", "after V204"),
]:
    out = out.replace(a, b)
(S / "c1334_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1329_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1329", "C1335"), ("c1329", "c1335"),
    ("capture_regression_c1329", "capture_regression_c1335"),
    ("after C1325-C1328", "after C1331-C1334"),
    ("V4-V203+heldout", "V4-V204+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V203", DOC / "C1326_VISION_V203_SMOKE.json"),'
if needle in out and "VISION_V204_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V204", DOC / "C1332_VISION_V204_SMOKE.json"),\n    ("V204_heldout", DOC / "C1333_VISION_V204_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1335_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1324_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1324", "C1336"), ("c1324", "c1336"),
    ("C1320", "C1332"), ("C1321", "C1333"), ("C1323", "C1335"),
    ("C1319", "C1331"), ("C1322", "C1334"),
    ("V202", "V204"), ("v202", "v204"),
    ("V201", "V203"), ("v201", "v203"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1316_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1328_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1316"', '"source": "C1328"')
out = out.replace(
    'f"- confidence-gate (prior C1316): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1328): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1336_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T204 if t[0].endswith("b")])
print("qty", TR204[1], HO204[1], "po", TR204[8], HO204[8], "sla", TR204[6], HO204[6], "fax", TR204[15], HO204[15])
print("done")
