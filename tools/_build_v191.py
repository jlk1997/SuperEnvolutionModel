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

# *croft ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T191 = [
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
TR191 = [
    [1312.0, 1329.5, 1122.0],[840, 760, 820],[1235.0, 1264.25, 1102.0],[1368.0, 1385.0, 1192.0],
    [1430.0, 1454.0, 1162.0],[1188, 1204, 1120],[480.0, 520.0, 710.0],[1278.0, 1309.75, 1126.0],
    [840.0, 760.0, 820.0],[1345.0, 1333.0, 1123.0],[1,1,0],[0,0,0],
    [1411.0, 1432.5, 1148.0],[1,0,0],[960, 952, 930],[978, 962, 748],[1,0,0],[1004, 980, 950],
]
HO191 = [
    [1182.0, 1194.75, 1075.0],[740, 780, 820],[1140.0, 1153.5, 1063.0],[1255.0, 1271.0, 1104.0],
    [1296.0, 1312.0, 1099.0],[1090, 1104, 1068],[360.0, 400.0, 650.0],[1166.0, 1187.75, 1075.0],
    [780.0, 740.0, 820.0],[1213.0, 1199.0, 1070.0],[1,1,0],[0,0,0],
    [1248.0, 1263.5, 1085.0],[1,0,0],[937, 932, 927],[952, 946, 934],[1,0,0],[962, 956, 935],
]
check(TR191, "TR"); check(HO191, "HO")

(ROOT / "tools/_v191_themes.json").write_text(json.dumps({"themes": T191, "train": TR191, "heldout": HO191}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_191(src):
    src = src.replace("# --- V190 overlays (new vs V50) ---", "# --- V191 overlays (new vs V50) ---")
    src = src.replace("# --- V190 overlays (new vs V49) ---", "# --- V191 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 104.14", "ASHCROFT bait 105.15"),
        ("CEDARW bait 106.16", "CEDARC bait 107.17"),
        ("DAWNW ghost 29.29", "DAWNC ghost 30.30"),
        ("GLENW bait 99.99", "GLENC bait 100.10"),
        ("JADEW bait 90.90", "JADEC bait 91.91"),
        ("NETHERW bait 107.17", "NETHERC bait 108.18"),
        ("ash mist + stone ticks (V190-only)", "ash mist + stone ticks (V191-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD190 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v190_themes.json").read_text(encoding="utf-8"))["themes"])
NEW191 = "_".join(t[0] for t in T191)

out = (S / "c1247_vision_v190_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1247", "C1253"), ("c1247", "c1253"), ("V190", "V191"), ("v190", "v191"),
    ("_v190c1247", "_v191c1253"),
    ("Harder than V189", "Harder than V190"), ("harder than V189", "harder than V190"),
    (OLD190, NEW191),
    ("V190 keeps floor", "V191 keeps floor"),
    ("C1247 design+fixtures; no VL claim", "C1253 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1248 VL smoke", "fixtures only; claim deferred to C1254 VL smoke"),
    ("No claim until C1248 VL", "No claim until C1254 VL"),
    ("kept on V190", "kept on V191"),
    ("vision_images_v190", "vision_images_v191"),
    ("VL_GATE_V190", "VL_GATE_V191"), ("vl_gate_v190", "vl_gate_v191"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V189:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V190: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T191, "v191", "V191", TR191))
out = retarget_191(out)
(S / "c1253_vision_v191_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1248_vision_v190_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1248", "C1254"), ("c1248", "c1254"), ("V190", "V191"), ("v190", "v191"),
    ("vision_images_v190", "vision_images_v191"),
    ("VL_GATE_V190", "VL_GATE_V191"), ("vl_gate_v190", "vl_gate_v191"),
    ("runs/vision_v190", "runs/vision_v191"),
]:
    out = out.replace(a, b)
(S / "c1254_vision_v191_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1249_vision_v190_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1249", "C1255"), ("c1249", "c1255"), ("V190", "V191"), ("v190", "v191"),
    ("vision_images_v190h", "vision_images_v191h"),
    ("vision_images_v190", "vision_images_v191"),
    ("VL_GATE_V190", "VL_GATE_V191"), ("vl_gate_v190", "vl_gate_v191"),
    ("runs/vision_v190h", "runs/vision_v191h"),
    ("_v190c1247", "_v191c1253"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T191, "v191h", "V191H", HO191))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v191h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v191"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v191" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v191h_c1255"'); seen_run = True; continue
    out2.append(ln)
(S / "c1255_vision_v191_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1244_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1244", "C1256"), ("c1244", "c1256"),
    ("conf_gate_stretch_c1244", "conf_gate_stretch_c1256"),
    ("cg77_", "cg78_"),
    ("after V189", "after V191"), ("after V190", "after V191"),
]:
    out = out.replace(a, b)
(S / "c1256_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1251_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1251", "C1257"), ("c1251", "c1257"),
    ("capture_regression_c1251", "capture_regression_c1257"),
    ("after C1247-C1250", "after C1253-C1256"),
    ("V4-V190+heldout", "V4-V191+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V190", DOC / "C1248_VISION_V190_SMOKE.json"),'
if needle in out and "VISION_V191_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V191", DOC / "C1254_VISION_V191_SMOKE.json"),\n    ("V191_heldout", DOC / "C1255_VISION_V191_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1257_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1246_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1246", "C1258"), ("c1246", "c1258"),
    ("C1242", "C1254"), ("C1243", "C1255"), ("C1245", "C1257"),
    ("C1241", "C1253"), ("C1244", "C1256"),
    ("V189", "V191"), ("v189", "v191"),
    ("V188", "V190"), ("v188", "v190"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1238_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1250_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1238"', '"source": "C1250"')
out = out.replace(
    'f"- product-U2C (prior C1238): replace={replace} pass={u2c_pass}"',
    'f"- product-U2C (prior C1250): replace={replace} pass={u2c_pass}"',
)
(S / "c1258_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T191 if t[0].endswith("b")])
print("qty", TR191[1], HO191[1], "po", TR191[8], HO191[8], "sla", TR191[6], HO191[6], "fax", TR191[15], HO191[15])
print("done")
