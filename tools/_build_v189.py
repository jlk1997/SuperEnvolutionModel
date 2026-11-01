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

# *mere ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 480+520 HO 360+400
T189 = [
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
TR189 = [
    [1294.0, 1311.5, 1104.0],[840, 760, 820],[1217.0, 1246.25, 1084.0],[1350.0, 1367.0, 1174.0],
    [1412.0, 1436.0, 1144.0],[1170, 1186, 1102],[480.0, 520.0, 690.0],[1260.0, 1291.75, 1108.0],
    [840.0, 760.0, 820.0],[1327.0, 1315.0, 1105.0],[1,1,0],[0,0,0],
    [1393.0, 1414.5, 1130.0],[1,0,0],[942, 934, 912],[960, 944, 748],[1,0,0],[986, 962, 932],
]
HO189 = [
    [1164.0, 1176.75, 1057.0],[740, 780, 820],[1122.0, 1135.5, 1045.0],[1237.0, 1253.0, 1086.0],
    [1278.0, 1294.0, 1081.0],[1072, 1086, 1050],[360.0, 400.0, 630.0],[1148.0, 1169.75, 1057.0],
    [780.0, 740.0, 820.0],[1195.0, 1181.0, 1052.0],[1,1,0],[0,0,0],
    [1230.0, 1245.5, 1067.0],[1,0,0],[919, 914, 909],[934, 928, 916],[1,0,0],[944, 938, 917],
]
check(TR189, "TR"); check(HO189, "HO")

(ROOT / "tools/_v189_themes.json").write_text(json.dumps({"themes": T189, "train": TR189, "heldout": HO189}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_189(src):
    src = src.replace("# --- V188 overlays (new vs V50) ---", "# --- V189 overlays (new vs V50) ---")
    src = src.replace("# --- V188 overlays (new vs V49) ---", "# --- V189 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 102.12", "ASHMERE bait 103.13"),
        ("CEDARH bait 104.14", "CEDARM bait 105.15"),
        ("DAWNH ghost 27.27", "DAWNM ghost 28.28"),
        ("GLENH bait 97.97", "GLENM bait 98.98"),
        ("JADEH bait 88.88", "JADEM bait 89.89"),
        ("NETHERH bait 105.15", "NETHERM bait 106.16"),
        ("ash mist + stone ticks (V188-only)", "ash mist + stone ticks (V189-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD188 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v188_themes.json").read_text(encoding="utf-8"))["themes"])
NEW189 = "_".join(t[0] for t in T189)

out = (S / "c1235_vision_v188_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1235", "C1241"), ("c1235", "c1241"), ("V188", "V189"), ("v188", "v189"),
    ("_v188c1235", "_v189c1241"),
    ("Harder than V187", "Harder than V188"), ("harder than V187", "harder than V188"),
    (OLD188, NEW189),
    ("V188 keeps floor", "V189 keeps floor"),
    ("C1235 design+fixtures; no VL claim", "C1241 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1236 VL smoke", "fixtures only; claim deferred to C1242 VL smoke"),
    ("No claim until C1236 VL", "No claim until C1242 VL"),
    ("kept on V188", "kept on V189"),
    ("vision_images_v188", "vision_images_v189"),
    ("VL_GATE_V188", "VL_GATE_V189"), ("vl_gate_v188", "vl_gate_v189"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V187:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V188: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T189, "v189", "V189", TR189))
out = retarget_189(out)
(S / "c1241_vision_v189_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1236_vision_v188_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1236", "C1242"), ("c1236", "c1242"), ("V188", "V189"), ("v188", "v189"),
    ("vision_images_v188", "vision_images_v189"),
    ("VL_GATE_V188", "VL_GATE_V189"), ("vl_gate_v188", "vl_gate_v189"),
    ("runs/vision_v188", "runs/vision_v189"),
]:
    out = out.replace(a, b)
(S / "c1242_vision_v189_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1237_vision_v188_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1237", "C1243"), ("c1237", "c1243"), ("V188", "V189"), ("v188", "v189"),
    ("vision_images_v188h", "vision_images_v189h"),
    ("vision_images_v188", "vision_images_v189"),
    ("VL_GATE_V188", "VL_GATE_V189"), ("vl_gate_v188", "vl_gate_v189"),
    ("runs/vision_v188h", "runs/vision_v189h"),
    ("_v188c1235", "_v189c1241"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T189, "v189h", "V189H", HO189))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v189h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v189"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v189" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v189h_c1243"'); seen_run = True; continue
    out2.append(ln)
(S / "c1243_vision_v189_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1232_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1232", "C1244"), ("c1232", "c1244"),
    ("conf_gate_stretch_c1232", "conf_gate_stretch_c1244"),
    ("cg76_", "cg77_"),
    ("after V187", "after V189"), ("after V188", "after V189"),
]:
    out = out.replace(a, b)
(S / "c1244_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1239_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1239", "C1245"), ("c1239", "c1245"),
    ("capture_regression_c1239", "capture_regression_c1245"),
    ("after C1235-C1238", "after C1241-C1244"),
    ("V4-V188+heldout", "V4-V189+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V188", DOC / "C1236_VISION_V188_SMOKE.json"),'
if needle in out and "VISION_V189_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V189", DOC / "C1242_VISION_V189_SMOKE.json"),\n    ("V189_heldout", DOC / "C1243_VISION_V189_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1245_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1234_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1234", "C1246"), ("c1234", "c1246"),
    ("C1230", "C1242"), ("C1231", "C1243"), ("C1233", "C1245"),
    ("C1229", "C1241"), ("C1232", "C1244"),
    ("V187", "V189"), ("v187", "v189"),
    ("V186", "V188"), ("v186", "v188"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1226_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1238_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1226"', '"source": "C1238"')
out = out.replace(
    'f"- product-U2C (prior C1226): replace={replace} pass={u2c_pass}"',
    'f"- product-U2C (prior C1238): replace={replace} pass={u2c_pass}"',
)
(S / "c1246_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T189 if t[0].endswith("b")])
print("qty", TR189[1], HO189[1], "po", TR189[8], HO189[8], "sla", TR189[6], HO189[6], "fax", TR189[15], HO189[15])
print("done")
