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

# *croft ; qty/SLA OCR-safe; stack/fax/tab mid-band
T224 = [
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
TR224 = [
    [1726.0, 1743.5, 1510.0],[840, 760, 820],[1649.0, 1678.25, 1490.0],[1782.0, 1799.0, 1580.0],
    [1844.0, 1868.0, 1550.0],[1602, 1618, 1508],[480.0, 520.0, 740.0],[1692.0, 1723.75, 1514.0],
    [840.0, 760.0, 820.0],[1759.0, 1747.0, 1511.0],[1,1,0],[0,0,0],
    [1825.0, 1846.5, 1536.0],[1,0,0],[1202, 1194, 1174],[1218, 1202, 748],[1,0,0],[1234, 1218, 1196],
]
HO224 = [
    [1570.0, 1582.75, 1437.0],[740, 780, 820],[1528.0, 1541.5, 1425.0],[1643.0, 1659.0, 1466.0],
    [1684.0, 1700.0, 1461.0],[1478, 1492, 1430],[360.0, 400.0, 730.0],[1554.0, 1575.75, 1437.0],
    [780.0, 740.0, 820.0],[1601.0, 1587.0, 1432.0],[1,1,0],[0,0,0],
    [1636.0, 1651.5, 1447.0],[1,0,0],[1179, 1174, 1169],[1194, 1188, 1176],[1,0,0],[1204, 1198, 1177],
]
check(TR224, "TR"); check(HO224, "HO")

(ROOT / "tools/_v224_themes.json").write_text(json.dumps({"themes": T224, "train": TR224, "heldout": HO224}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_224(src):
    src = src.replace("# --- V223 overlays (new vs V50) ---", "# --- V224 overlays (new vs V50) ---")
    src = src.replace("# --- V223 overlays (new vs V49) ---", "# --- V224 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 137.47", "ASHCROFT bait 138.48"),
        ("CEDARV bait 139.49", "CEDARC bait 140.50"),
        ("DAWNV ghost 62.62", "DAWNC ghost 63.63"),
        ("GLENV bait 132.42", "GLENC bait 133.43"),
        ("JADEV bait 123.33", "JADEC bait 124.34"),
        ("NETHERV bait 140.50", "NETHERC bait 141.51"),
        ("ash mist + stone ticks (V223-only)", "ash mist + stone ticks (V224-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD223 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v223_themes.json").read_text(encoding="utf-8"))["themes"])
NEW224 = "_".join(t[0] for t in T224)

out = (S / "c1445_vision_v223_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1445", "C1451"), ("c1445", "c1451"), ("V223", "V224"), ("v223", "v224"),
    ("_v223c1445", "_v224c1451"),
    ("Harder than V222", "Harder than V223"), ("harder than V222", "harder than V223"),
    (OLD223, NEW224),
    ("V223 keeps floor", "V224 keeps floor"),
    ("C1445 design+fixtures; no VL claim", "C1451 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1446 VL smoke", "fixtures only; claim deferred to C1452 VL smoke"),
    ("No claim until C1446 VL", "No claim until C1452 VL"),
    ("kept on V223", "kept on V224"),
    ("vision_images_v223", "vision_images_v224"),
    ("VL_GATE_V223", "VL_GATE_V224"), ("vl_gate_v223", "vl_gate_v224"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V222:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V223: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T224, "v224", "V224", TR224))
out = retarget_224(out)
(S / "c1451_vision_v224_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1446_vision_v223_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1446", "C1452"), ("c1446", "c1452"), ("V223", "V224"), ("v223", "v224"),
    ("vision_images_v223", "vision_images_v224"),
    ("VL_GATE_V223", "VL_GATE_V224"), ("vl_gate_v223", "vl_gate_v224"),
    ("runs/vision_v223", "runs/vision_v224"),
]:
    out = out.replace(a, b)
(S / "c1452_vision_v224_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1447_vision_v223_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1447", "C1453"), ("c1447", "c1453"), ("V223", "V224"), ("v223", "v224"),
    ("vision_images_v223h", "vision_images_v224h"),
    ("vision_images_v223", "vision_images_v224"),
    ("VL_GATE_V223", "VL_GATE_V224"), ("vl_gate_v223", "vl_gate_v224"),
    ("runs/vision_v223h", "runs/vision_v224h"),
    ("_v223c1445", "_v224c1451"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T224, "v224h", "V224H", HO224))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v224h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v224"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v224" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v224h_c1453"'); seen_run = True; continue
    out2.append(ln)
(S / "c1453_vision_v224_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1442_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1442", "C1454"), ("c1442", "c1454"),
    ("product_u2c_c1442", "product_u2c_c1454"),
]:
    out = out.replace(a, b)
(S / "c1454_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1449_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1449", "C1455"), ("c1449", "c1455"),
    ("capture_regression_c1449", "capture_regression_c1455"),
    ("after C1445-C1448", "after C1451-C1454"),
    ("V4-V223+heldout", "V4-V224+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V223", DOC / "C1446_VISION_V223_SMOKE.json"),'
if needle in out and "VISION_V224_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V224", DOC / "C1452_VISION_V224_SMOKE.json"),\n    ("V224_heldout", DOC / "C1453_VISION_V224_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1455_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1444_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1444", "C1456"), ("c1444", "c1456"),
    ("C1440", "C1452"), ("C1441", "C1453"), ("C1443", "C1455"),
    ("C1439", "C1451"), ("C1442", "C1454"),
    ("V222", "V224"), ("v222", "v224"),
    ("V221", "V223"), ("v221", "v223"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1436_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1448_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1436"', '"source": "C1448"')
out = out.replace(
    'f"- confidence-gate (prior C1436): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1448): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace("C1439-C1444", "C1451-C1456")
out = out.replace("C1439-C1443", "C1451-C1455")
(S / "c1456_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T224 if t[0].endswith("b")])
print("qty", TR224[1], HO224[1], "stack", TR224[14], HO224[14], "fax", TR224[15], HO224[15])
print("done")
