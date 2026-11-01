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

# *hurst ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T192 = [
    ["ashhurst","recv","paid_total","ASHHURST GRAIN RECV","RECV","x"],
    ["cedarhurst","wh","qty_sum","WH CEDARHURST BIN","RECV","x"],
    ["dawnhurst","refund","refund_done","DAWNHURST PATCH REFUND","DONE","x"],
    ["elmhurst","tax","tax_base_paid","ELMHURST TAX SLIP","TAX","x"],
    ["fernhurst","pay","payroll_active","FERNHURST PAYROLL","PAY","x"],
    ["glenhurst","ship","ship_ok","GLENHURST SHIP DOCK","SHIP","x"],
    ["hazehurst","sla","sla_ok_hours","HAZEHURST SLA CARD","SLA","x"],
    ["inkhurst","exp","exp_sum","INKHURST EXPENSE","EXP","x"],
    ["jadehurst","po","po_open","JADEHURST PO SHEET","PO","x"],
    ["knothurst","order","order_paid","KNOTHURST ORDER","ORD","x"],
    ["lakehurst","dup","dup_mark","LAKEHURST DUP MARK","DUP","x"],
    ["mosshurst","zero","zero_check","MOSSHURST AIR ZERO","ZERO","x"],
    ["netherhurst","ledger","ledger_net","NETHERHURST LEDGER","LED","x"],
    ["oakhurst","ui","ui_ok","OAKHURST UI SCAN","UI","x"],
    ["pinehurst","stack","stack_count","PINEHURST STACK","STK","x"],
    ["quillhurst","fax","fax_pages","QUILLHURST FAX","FAX","x"],
    ["reedhurst","glare","glare_ok","REEDHURST GLARE","GLR","x"],
    ["stonehurst","tab","tab_index","STONEHURST TAB INDEX","TAB","x"],
]
TR192 = [
    [1321.0, 1338.5, 1131.0],[740, 780, 820],[1244.0, 1273.25, 1111.0],[1377.0, 1394.0, 1201.0],
    [1439.0, 1463.0, 1171.0],[1197, 1213, 1129],[480.0, 520.0, 720.0],[1287.0, 1318.75, 1135.0],
    [780.0, 740.0, 820.0],[1354.0, 1342.0, 1132.0],[1,1,0],[0,0,0],
    [1420.0, 1441.5, 1157.0],[1,0,0],[969, 961, 939],[987, 971, 748],[1,0,0],[1013, 989, 959],
]
HO192 = [
    [1191.0, 1203.75, 1084.0],[840, 760, 820],[1149.0, 1162.5, 1072.0],[1264.0, 1280.0, 1113.0],
    [1305.0, 1321.0, 1108.0],[1099, 1113, 1077],[360.0, 400.0, 660.0],[1175.0, 1196.75, 1084.0],
    [840.0, 760.0, 820.0],[1222.0, 1208.0, 1079.0],[1,1,0],[0,0,0],
    [1257.0, 1272.5, 1094.0],[1,0,0],[946, 941, 936],[961, 955, 943],[1,0,0],[971, 965, 944],
]
check(TR192, "TR"); check(HO192, "HO")

(ROOT / "tools/_v192_themes.json").write_text(json.dumps({"themes": T192, "train": TR192, "heldout": HO192}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_192(src):
    src = src.replace("# --- V191 overlays (new vs V50) ---", "# --- V192 overlays (new vs V50) ---")
    src = src.replace("# --- V191 overlays (new vs V49) ---", "# --- V192 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 105.15", "ASHHURST bait 106.16"),
        ("CEDARC bait 107.17", "CEDARH bait 108.18"),
        ("DAWNC ghost 30.30", "DAWNH ghost 31.31"),
        ("GLENC bait 100.10", "GLENH bait 101.11"),
        ("JADEC bait 91.91", "JADEH bait 92.92"),
        ("NETHERC bait 108.18", "NETHERH bait 109.19"),
        ("ash mist + stone ticks (V191-only)", "ash mist + stone ticks (V192-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD191 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v191_themes.json").read_text(encoding="utf-8"))["themes"])
NEW192 = "_".join(t[0] for t in T192)

out = (S / "c1253_vision_v191_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1253", "C1259"), ("c1253", "c1259"), ("V191", "V192"), ("v191", "v192"),
    ("_v191c1253", "_v192c1259"),
    ("Harder than V190", "Harder than V191"), ("harder than V190", "harder than V191"),
    (OLD191, NEW192),
    ("V191 keeps floor", "V192 keeps floor"),
    ("C1253 design+fixtures; no VL claim", "C1259 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1254 VL smoke", "fixtures only; claim deferred to C1260 VL smoke"),
    ("No claim until C1254 VL", "No claim until C1260 VL"),
    ("kept on V191", "kept on V192"),
    ("vision_images_v191", "vision_images_v192"),
    ("VL_GATE_V191", "VL_GATE_V192"), ("vl_gate_v191", "vl_gate_v192"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V190:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V191: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T192, "v192", "V192", TR192))
out = retarget_192(out)
(S / "c1259_vision_v192_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1254_vision_v191_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1254", "C1260"), ("c1254", "c1260"), ("V191", "V192"), ("v191", "v192"),
    ("vision_images_v191", "vision_images_v192"),
    ("VL_GATE_V191", "VL_GATE_V192"), ("vl_gate_v191", "vl_gate_v192"),
    ("runs/vision_v191", "runs/vision_v192"),
]:
    out = out.replace(a, b)
(S / "c1260_vision_v192_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1255_vision_v191_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1255", "C1261"), ("c1255", "c1261"), ("V191", "V192"), ("v191", "v192"),
    ("vision_images_v191h", "vision_images_v192h"),
    ("vision_images_v191", "vision_images_v192"),
    ("VL_GATE_V191", "VL_GATE_V192"), ("vl_gate_v191", "vl_gate_v192"),
    ("runs/vision_v191h", "runs/vision_v192h"),
    ("_v191c1253", "_v192c1259"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T192, "v192h", "V192H", HO192))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v192h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v192"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v192" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v192h_c1261"'); seen_run = True; continue
    out2.append(ln)
(S / "c1261_vision_v192_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1250_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1250", "C1262"), ("c1250", "c1262"),
    ("product_u2c_c1250", "product_u2c_c1262"),
    ("after V190", "after V192"), ("after V191", "after V192"),
]:
    out = out.replace(a, b)
(S / "c1262_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1257_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1257", "C1263"), ("c1257", "c1263"),
    ("capture_regression_c1257", "capture_regression_c1263"),
    ("after C1253-C1256", "after C1259-C1262"),
    ("V4-V191+heldout", "V4-V192+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V191", DOC / "C1254_VISION_V191_SMOKE.json"),'
if needle in out and "VISION_V192_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V192", DOC / "C1260_VISION_V192_SMOKE.json"),\n    ("V192_heldout", DOC / "C1261_VISION_V192_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1263_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1252_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1252", "C1264"), ("c1252", "c1264"),
    ("C1248", "C1260"), ("C1249", "C1261"), ("C1251", "C1263"),
    ("C1247", "C1259"), ("C1250", "C1262"),
    ("V190", "V192"), ("v190", "v192"),
    ("V189", "V191"), ("v189", "v191"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1244_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1256_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1244"', '"source": "C1256"')
out = out.replace(
    'f"- confidence-gate (prior C1244): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1256): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1264_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T192 if t[0].endswith("b")])
print("qty", TR192[1], HO192[1], "po", TR192[8], HO192[8], "sla", TR192[6], HO192[6], "fax", TR192[15], HO192[15])
print("done")
