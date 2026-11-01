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

# *wick ; qty/SLA OCR-safe; stack/fax/tab mid-band
T226 = [
    ["ashwick","recv","paid_total","ASHWICK GRAIN RECV","RECV","x"],
    ["cedarwick","wh","qty_sum","WH CEDARWICK BIN","RECV","x"],
    ["dawnwick","refund","refund_done","DAWNWICK PATCH REFUND","DONE","x"],
    ["elmwick","tax","tax_base_paid","ELMWICK TAX SLIP","TAX","x"],
    ["fernwick","pay","payroll_active","FERNWICK PAYROLL","PAY","x"],
    ["glenwick","ship","ship_ok","GLENWICK SHIP DOCK","SHIP","x"],
    ["hazewick","sla","sla_ok_hours","HAZEWICK SLA CARD","SLA","x"],
    ["inkwick","exp","exp_sum","INKWICK EXPENSE","EXP","x"],
    ["jadewick","po","po_open","JADEWICK PO SHEET","PO","x"],
    ["knotwick","order","order_paid","KNOTWICK ORDER","ORD","x"],
    ["lakewick","dup","dup_mark","LAKEWICK DUP MARK","DUP","x"],
    ["mosswick","zero","zero_check","MOSSWICK AIR ZERO","ZERO","x"],
    ["netherwick","ledger","ledger_net","NETHERWICK LEDGER","LED","x"],
    ["oakwick","ui","ui_ok","OAKWICK UI SCAN","UI","x"],
    ["pinewick","stack","stack_count","PINEWICK STACK","STK","x"],
    ["quillwick","fax","fax_pages","QUILLWICK FAX","FAX","x"],
    ["reedwick","glare","glare_ok","REEDWICK GLARE","GLR","x"],
    ["stonewick","tab","tab_index","STONEWICK TAB INDEX","TAB","x"],
]
TR226 = [
    [1762.0, 1779.5, 1542.0],[840, 760, 820],[1685.0, 1714.25, 1522.0],[1818.0, 1835.0, 1612.0],
    [1880.0, 1904.0, 1582.0],[1638, 1654, 1540],[480.0, 520.0, 740.0],[1728.0, 1759.75, 1546.0],
    [840.0, 760.0, 820.0],[1795.0, 1783.0, 1543.0],[1,1,0],[0,0,0],
    [1861.0, 1882.5, 1568.0],[1,0,0],[1148, 1140, 1120],[1214, 1198, 748],[1,0,0],[1230, 1214, 1192],
]
HO226 = [
    [1602.0, 1614.75, 1465.0],[740, 780, 820],[1561.0, 1573.5, 1453.0],[1675.0, 1691.0, 1494.0],
    [1716.0, 1732.0, 1489.0],[1510, 1524, 1458],[360.0, 400.0, 730.0],[1586.0, 1607.75, 1465.0],
    [780.0, 740.0, 820.0],[1633.0, 1619.0, 1460.0],[1,1,0],[0,0,0],
    [1668.0, 1683.5, 1475.0],[1,0,0],[1135, 1130, 1125],[1190, 1184, 1172],[1,0,0],[1200, 1194, 1173],
]
check(TR226, "TR"); check(HO226, "HO")

(ROOT / "tools/_v226_themes.json").write_text(json.dumps({"themes": T226, "train": TR226, "heldout": HO226}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_226(src):
    src = src.replace("# --- V225 overlays (new vs V50) ---", "# --- V226 overlays (new vs V50) ---")
    src = src.replace("# --- V225 overlays (new vs V49) ---", "# --- V226 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 139.49", "ASHWICK bait 140.50"),
        ("CEDARH bait 141.51", "CEDARW bait 142.52"),
        ("DAWNH ghost 64.64", "DAWNW ghost 65.65"),
        ("GLENH bait 134.44", "GLENW bait 135.45"),
        ("JADEH bait 125.35", "JADEW bait 126.36"),
        ("NETHERH bait 142.52", "NETHERW bait 143.53"),
        ("ash mist + stone ticks (V225-only)", "ash mist + stone ticks (V226-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD225 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v225_themes.json").read_text(encoding="utf-8"))["themes"])
NEW226 = "_".join(t[0] for t in T226)

out = (S / "c1457_vision_v225_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1457", "C1463"), ("c1457", "c1463"), ("V225", "V226"), ("v225", "v226"),
    ("_v225c1457", "_v226c1463"),
    ("Harder than V224", "Harder than V225"), ("harder than V224", "harder than V225"),
    (OLD225, NEW226),
    ("V225 keeps floor", "V226 keeps floor"),
    ("C1457 design+fixtures; no VL claim", "C1463 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1458 VL smoke", "fixtures only; claim deferred to C1464 VL smoke"),
    ("No claim until C1458 VL", "No claim until C1464 VL"),
    ("kept on V225", "kept on V226"),
    ("vision_images_v225", "vision_images_v226"),
    ("VL_GATE_V225", "VL_GATE_V226"), ("vl_gate_v225", "vl_gate_v226"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V224:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V225: ashwich, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
    out, count=1, flags=re.S,
)
out = out.replace("ashwich", "ashwick")
out = replace_specs(out, build_specs(T226, "v226", "V226", TR226))
out = retarget_226(out)
(S / "c1463_vision_v226_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1458_vision_v225_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1458", "C1464"), ("c1458", "c1464"), ("V225", "V226"), ("v225", "v226"),
    ("vision_images_v225", "vision_images_v226"),
    ("VL_GATE_V225", "VL_GATE_V226"), ("vl_gate_v225", "vl_gate_v226"),
    ("runs/vision_v225", "runs/vision_v226"),
]:
    out = out.replace(a, b)
(S / "c1464_vision_v226_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1459_vision_v225_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1459", "C1465"), ("c1459", "c1465"), ("V225", "V226"), ("v225", "v226"),
    ("vision_images_v225h", "vision_images_v226h"),
    ("vision_images_v225", "vision_images_v226"),
    ("VL_GATE_V225", "VL_GATE_V226"), ("vl_gate_v225", "vl_gate_v226"),
    ("runs/vision_v225h", "runs/vision_v226h"),
    ("_v225c1457", "_v226c1463"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T226, "v226h", "V226H", HO226))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v226h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v226"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v226" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v226h_c1465"'); seen_run = True; continue
    out2.append(ln)
(S / "c1465_vision_v226_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1454_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1454", "C1466"), ("c1454", "c1466"),
    ("product_u2c_c1454", "product_u2c_c1466"),
]:
    out = out.replace(a, b)
(S / "c1466_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1461_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1461", "C1467"), ("c1461", "c1467"),
    ("capture_regression_c1461", "capture_regression_c1467"),
    ("after C1457-C1460", "after C1463-C1466"),
    ("V4-V225+heldout", "V4-V226+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V225", DOC / "C1458_VISION_V225_SMOKE.json"),'
if needle in out and "VISION_V226_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V226", DOC / "C1464_VISION_V226_SMOKE.json"),\n    ("V226_heldout", DOC / "C1465_VISION_V226_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1467_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1456_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1456", "C1468"), ("c1456", "c1468"),
    ("C1452", "C1464"), ("C1453", "C1465"), ("C1455", "C1467"),
    ("C1451", "C1463"), ("C1454", "C1466"),
    ("V224", "V226"), ("v224", "v226"),
    ("V223", "V225"), ("v223", "v225"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1448_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1460_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1448"', '"source": "C1460"')
out = out.replace(
    'f"- confidence-gate (prior C1448): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1460): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace("C1451-C1456", "C1463-C1468")
out = out.replace("C1451-C1455", "C1463-C1467")
(S / "c1468_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T226 if t[0].endswith("b")])
print("qty", TR226[1], HO226[1], "stack", TR226[14], HO226[14], "fax", TR226[15], HO226[15])
print("done")
