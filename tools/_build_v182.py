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

# *moor ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 530+570 HO 410+450
T182 = [
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
TR182 = [
    [1231.0, 1248.5, 1041.0],[740, 780, 820],[1154.0, 1183.25, 1021.0],[1287.0, 1304.0, 1111.0],
    [1349.0, 1373.0, 1081.0],[1107, 1123, 1039],[530.0, 570.0, 610.0],[1197.0, 1228.75, 1045.0],
    [780.0, 740.0, 820.0],[1264.0, 1252.0, 1042.0],[1,1,0],[0,0,0],
    [1330.0, 1351.5, 1067.0],[1,0,0],[879, 871, 849],[897, 881, 748],[1,0,0],[923, 899, 869],
]
HO182 = [
    [1101.0, 1113.75, 994.0],[840, 760, 820],[1059.0, 1072.5, 982.0],[1174.0, 1190.0, 1023.0],
    [1215.0, 1231.0, 1018.0],[1009, 1023, 987],[410.0, 450.0, 590.0],[1085.0, 1106.75, 994.0],
    [840.0, 760.0, 820.0],[1132.0, 1118.0, 989.0],[1,1,0],[0,0,0],
    [1167.0, 1182.5, 1004.0],[1,0,0],[856, 851, 846],[871, 865, 853],[1,0,0],[881, 875, 854],
]
check(TR182, "TR"); check(HO182, "HO")

(ROOT / "tools/_v182_themes.json").write_text(json.dumps({"themes": T182, "train": TR182, "heldout": HO182}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_182(src):
    src = src.replace("# --- V181 overlays (new vs V50) ---", "# --- V182 overlays (new vs V50) ---")
    src = src.replace("# --- V181 overlays (new vs V49) ---", "# --- V182 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 95.95", "ASHMOOR bait 96.96"),
        ("CEDARH bait 97.97", "CEDARM bait 98.98"),
        ("DAWNH ghost 20.20", "DAWNM ghost 21.21"),
        ("GLENH bait 90.90", "GLENM bait 91.91"),
        ("JADEH bait 81.81", "JADEM bait 82.82"),
        ("NETHERH bait 98.98", "NETHERM bait 99.99"),
        ("ash mist + stone ticks (V181-only)", "ash mist + stone ticks (V182-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD181 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v181_themes.json").read_text(encoding="utf-8"))["themes"])
NEW182 = "_".join(t[0] for t in T182)

out = (S / "c1193_vision_v181_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1193", "C1199"), ("c1193", "c1199"), ("V181", "V182"), ("v181", "v182"),
    ("_v181c1193", "_v182c1199"),
    ("Harder than V180", "Harder than V181"), ("harder than V180", "harder than V181"),
    (OLD181, NEW182),
    ("V181 keeps floor", "V182 keeps floor"),
    ("C1193 design+fixtures; no VL claim", "C1199 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1194 VL smoke", "fixtures only; claim deferred to C1200 VL smoke"),
    ("No claim until C1194 VL", "No claim until C1200 VL"),
    ("kept on V181", "kept on V182"),
    ("vision_images_v181", "vision_images_v182"),
    ("VL_GATE_V181", "VL_GATE_V182"), ("vl_gate_v181", "vl_gate_v182"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V180:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V181: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T182, "v182", "V182", TR182))
out = retarget_182(out)
(S / "c1199_vision_v182_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1194_vision_v181_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1194", "C1200"), ("c1194", "c1200"), ("V181", "V182"), ("v181", "v182"),
    ("vision_images_v181", "vision_images_v182"),
    ("VL_GATE_V181", "VL_GATE_V182"), ("vl_gate_v181", "vl_gate_v182"),
    ("runs/vision_v181", "runs/vision_v182"),
]:
    out = out.replace(a, b)
(S / "c1200_vision_v182_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1195_vision_v181_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1195", "C1201"), ("c1195", "c1201"), ("V181", "V182"), ("v181", "v182"),
    ("vision_images_v181h", "vision_images_v182h"),
    ("vision_images_v181", "vision_images_v182"),
    ("VL_GATE_V181", "VL_GATE_V182"), ("vl_gate_v181", "vl_gate_v182"),
    ("runs/vision_v181h", "runs/vision_v182h"),
    ("_v181c1193", "_v182c1199"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T182, "v182h", "V182H", HO182))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v182h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v182"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v182" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v182h_c1201"'); seen_run = True; continue
    out2.append(ln)
(S / "c1201_vision_v182_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1190_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1190", "C1202"), ("c1190", "c1202"),
    ("product_u2c_c1190", "product_u2c_c1202"),
    ("after V180", "after V182"), ("after V181", "after V182"),
]:
    out = out.replace(a, b)
(S / "c1202_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1197_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1197", "C1203"), ("c1197", "c1203"),
    ("capture_regression_c1197", "capture_regression_c1203"),
    ("after C1193-C1196", "after C1199-C1202"),
    ("V4-V181+heldout", "V4-V182+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V181", DOC / "C1194_VISION_V181_SMOKE.json"),'
if needle in out and "VISION_V182_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V182", DOC / "C1200_VISION_V182_SMOKE.json"),\n    ("V182_heldout", DOC / "C1201_VISION_V182_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1203_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1192_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1192", "C1204"), ("c1192", "c1204"),
    ("C1188", "C1200"), ("C1189", "C1201"), ("C1191", "C1203"),
    ("C1187", "C1199"), ("C1190", "C1202"),
    ("V180", "V182"), ("v180", "v182"),
    ("V179", "V181"), ("v179", "v181"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1184_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1196_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1184"', '"source": "C1196"')
out = out.replace(
    'f"- confidence-gate (prior C1184): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1196): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1204_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T182 if t[0].endswith("b")])
print("qty", TR182[1], HO182[1], "po", TR182[8], HO182[8], "sla", TR182[6], HO182[6], "fax", TR182[15], HO182[15])
print("done")
