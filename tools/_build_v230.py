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

# *dale ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T230 = [
    ["ashdale","recv","paid_total","ASHDALE GRAIN RECV","RECV","x"],
    ["cedardale","wh","qty_sum","WH CEDARDALE BIN","RECV","x"],
    ["dawndale","refund","refund_done","DAWNDALE PATCH REFUND","DONE","x"],
    ["elmdale","tax","tax_base_paid","ELMDALE TAX SLIP","TAX","x"],
    ["ferndale","pay","payroll_active","FERNDALE PAYROLL","PAY","x"],
    ["glendale","ship","ship_ok","GLENDALE SHIP DOCK","SHIP","x"],
    ["hazedale","sla","sla_ok_hours","HAZEDALE SLA CARD","SLA","x"],
    ["inkdale","exp","exp_sum","INKDALE EXPENSE","EXP","x"],
    ["jadedale","po","po_open","JADEDALE PO SHEET","PO","x"],
    ["knotdale","order","order_paid","KNOTDALE ORDER","ORD","x"],
    ["lakedale","dup","dup_mark","LAKEDALE DUP MARK","DUP","x"],
    ["mossdale","zero","zero_check","MOSSDALE AIR ZERO","ZERO","x"],
    ["netherdale","ledger","ledger_net","NETHERDALE LEDGER","LED","x"],
    ["oakdale","ui","ui_ok","OAKDALE UI SCAN","UI","x"],
    ["pinedale","stack","stack_count","PINEDALE STACK","STK","x"],
    ["quilldale","fax","fax_pages","QUILLDALE FAX","FAX","x"],
    ["reeddale","glare","glare_ok","REEDDALE GLARE","GLR","x"],
    ["stonedale","tab","tab_index","STONEDALE TAB INDEX","TAB","x"],
]
TR230 = [
    [1834.0, 1851.5, 1606.0],[840, 760, 820],[1757.0, 1786.25, 1586.0],[1890.0, 1907.0, 1676.0],
    [1952.0, 1976.0, 1646.0],[1704, 1720, 1604],[480.0, 520.0, 740.0],[1800.0, 1831.75, 1610.0],
    [840.0, 760.0, 820.0],[1867.0, 1855.0, 1607.0],[1,1,0],[0,0,0],
    [1933.0, 1954.5, 1632.0],[1,0,0],[1168, 1160, 1140],[1184, 1168, 748],[1,0,0],[1200, 1184, 1162],
]
HO230 = [
    [1666.0, 1678.75, 1527.0],[740, 780, 820],[1609.0, 1622.5, 1502.0],[1739.0, 1755.0, 1556.0],
    [1780.0, 1796.0, 1551.0],[1574, 1588, 1520],[360.0, 400.0, 730.0],[1650.0, 1671.75, 1527.0],
    [780.0, 740.0, 820.0],[1697.0, 1683.0, 1522.0],[1,1,0],[0,0,0],
    [1732.0, 1747.5, 1537.0],[1,0,0],[1156, 1151, 1144],[1170, 1164, 1152],[1,0,0],[1180, 1174, 1153],
]
check(TR230, "TR"); check(HO230, "HO")

(ROOT / "tools/_v230_themes.json").write_text(json.dumps({"themes": T230, "train": TR230, "heldout": HO230}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_229(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V230 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V230 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHDALE bait 143.53"),
        ("CEDARW bait 142.52", "CEDARD bait 145.55"),
        ("DAWNW ghost 65.65", "DAWND ghost 68.68"),
        ("GLENW bait 135.45", "GLEND bait 138.48"),
        ("JADEW bait 126.36", "JADED bait 129.39"),
        ("NETHERW bait 143.53", "NETHERD bait 146.56"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V230-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD229 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v229_themes.json").read_text(encoding="utf-8"))["themes"])
NEW230 = "_".join(t[0] for t in T230)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1487"), ("c1463", "c1487"), ("V226", "V230"), ("v226", "v230"),
    ("_v226c1463", "_v230c1487"),
    ("Harder than V225", "Harder than V228"), ("harder than V225", "harder than V228"),
    (OLD229, NEW230),
    ("V226 keeps floor", "V230 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1487 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1488 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1488 VL"),
    ("kept on V226", "kept on V230"),
    ("vision_images_v226", "vision_images_v230"),
    ("VL_GATE_V226", "VL_GATE_V230"), ("vl_gate_v226", "vl_gate_v230"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V228: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T230, "v230", "V230", TR230))
out = retarget_229(out)
(S / "c1487_vision_v230_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1488"), ("c1464", "c1488"), ("V226", "V230"), ("v226", "v230"),
    ("vision_images_v226", "vision_images_v230"),
    ("VL_GATE_V226", "VL_GATE_V230"), ("vl_gate_v226", "vl_gate_v230"),
    ("runs/vision_v226", "runs/vision_v230"),
]:
    out = out.replace(a, b)
(S / "c1488_vision_v230_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1489"), ("c1465", "c1489"), ("V226", "V230"), ("v226", "v230"),
    ("vision_images_v226h", "vision_images_v230h"),
    ("vision_images_v226", "vision_images_v230"),
    ("VL_GATE_V226", "VL_GATE_V230"), ("vl_gate_v226", "vl_gate_v230"),
    ("runs/vision_v226h", "runs/vision_v230h"),
    ("_v226c1463", "_v230c1487"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T230, "v230h", "V230H", HO230))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v230h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v230"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v230" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v230h_c1489"'); seen_run = True; continue
    out2.append(ln)
(S / "c1489_vision_v230_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V230 knife = product-U2C (alternating; V229 was conf-gate)
out = (S / "c1478_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1478", "C1490"), ("c1478", "c1490"),
    ("product_u2c_c1478", "product_u2c_c1490"),
    ("vs C1466", "vs C1478"),
]:
    out = out.replace(a, b2)
(S / "c1490_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1485_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1485", "C1491"), ("c1485", "c1491")]:
    out = out.replace(a, b2)
(S / "c1491_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1480_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1480", "C1492"), ("c1480", "c1492"),
    ("C1478", "C1490"), ("c1478", "c1490"),
    ("C1479", "C1491"), ("c1479", "c1491"),
    ("C1476", "C1488"), ("c1476", "c1488"),
    ("C1477", "C1489"), ("c1477", "c1489"),
    ("V228", "V230"), ("v228", "v230"),
    ("STAGE_ANT_C1480", "STAGE_ANT_C1492"),
    ("*fen", "*dale"),
]:
    out = out.replace(a, b2)
(S / "c1492_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v230 ready")
