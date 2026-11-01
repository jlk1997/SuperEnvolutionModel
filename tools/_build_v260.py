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

# *moor ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T260 = [
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
TR260 = [
    [2166.0, 2183.5, 1906.0],[840, 760, 820],[2089.0, 2118.25, 1884.0],[2222.0, 2239.0, 1974.0],
    [2284.0, 2308.0, 1944.0],[2002, 2018, 1902],[480.0, 520.0, 740.0],[2132.0, 2163.75, 1908.0],
    [840.0, 760.0, 820.0],[2199.0, 2187.0, 1905.0],[1,1,0],[0,0,0],
    [2265.0, 2286.5, 1930.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO260 = [
    [1964.0, 1976.75, 1825.0],[740, 780, 820],[1907.0, 1921.5, 1800.0],[2037.0, 2053.0, 1856.0],
    [2078.0, 2094.0, 1849.0],[1860, 1872, 1818],[360.0, 400.0, 730.0],[1948.0, 1969.75, 1825.0],
    [780.0, 740.0, 820.0],[1995.0, 1981.0, 1820.0],[1,1,0],[0,0,0],
    [2030.0, 2045.5, 1835.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR260, "TR"); check(HO260, "HO")

(ROOT / "tools/_v260_themes.json").write_text(json.dumps({"themes": T260, "train": TR260, "heldout": HO260}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_259(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V260 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V260 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 140.50", "ASHMOOR bait 173.83"),
        ("CEDARW bait 142.52", "CEDARM bait 175.85"),
        ("DAWNW ghost 65.65", "DAWNM ghost 98.98"),
        ("GLENW bait 135.45", "GLENM bait 168.78"),
        ("JADEW bait 126.36", "JADEM bait 159.69"),
        ("NETHERW bait 143.53", "NETHERM bait 176.86"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V260-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD259 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v259_themes.json").read_text(encoding="utf-8"))["themes"])
NEW260 = "_".join(t[0] for t in T260)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1667"), ("c1463", "c1667"), ("V226", "V260"), ("v226", "v260"),
    ("_v226c1463", "_v260c1667"),
    ("Harder than V225", "Harder than V258"), ("harder than V225", "harder than V258"),
    (OLD259, NEW260),
    ("V226 keeps floor", "V260 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1667 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1668 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1668 VL"),
    ("kept on V226", "kept on V260"),
    ("vision_images_v226", "vision_images_v260"),
    ("VL_GATE_V226", "VL_GATE_V260"), ("vl_gate_v226", "vl_gate_v260"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V258: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T260, "v260", "V260", TR260))
out = retarget_259(out)
(S / "c1667_vision_v260_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1668"), ("c1464", "c1668"), ("V226", "V260"), ("v226", "v260"),
    ("vision_images_v226", "vision_images_v260"),
    ("VL_GATE_V226", "VL_GATE_V260"), ("vl_gate_v226", "vl_gate_v260"),
    ("runs/vision_v226", "runs/vision_v260"),
]:
    out = out.replace(a, b)
(S / "c1668_vision_v260_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1669"), ("c1465", "c1669"), ("V226", "V260"), ("v226", "v260"),
    ("vision_images_v226h", "vision_images_v260h"),
    ("vision_images_v226", "vision_images_v260"),
    ("VL_GATE_V226", "VL_GATE_V260"), ("vl_gate_v226", "vl_gate_v260"),
    ("runs/vision_v226h", "runs/vision_v260h"),
    ("_v226c1463", "_v260c1667"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T260, "v260h", "V260H", HO260))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v260h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v260"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v260" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v260h_c1669"'); seen_run = True; continue
    out2.append(ln)
(S / "c1669_vision_v260_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V260 knife = product-U2C (alternating; V259 was confidence-gate)
out = (S / "c1658_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1658", "C1670"), ("c1658", "c1670"),
    ("C1646", "C1670"), ("c1646", "c1670"),
    ("C1466", "C1670"), ("c1466", "c1670"),
]:
    out = out.replace(a, b2)
(S / "c1670_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1658_product_u2c_cost.py")

out = (S / "c1665_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1665", "C1671"), ("c1665", "c1671")]:
    out = out.replace(a, b2)
(S / "c1671_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1660_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1660", "C1672"), ("c1660", "c1672"),
    ("C1658", "C1670"), ("c1658", "c1670"),
    ("C1659", "C1671"), ("c1659", "c1671"),
    ("C1656", "C1668"), ("c1656", "c1668"),
    ("C1657", "C1669"), ("c1657", "c1669"),
    ("V258", "V260"), ("v258", "v260"),
    ("STAGE_ANT_C1660", "STAGE_ANT_C1672"),
    ("*holm", "*moor"),
]:
    out = out.replace(a, b2)
(S / "c1672_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1660_scorecard_and_stage.py")
print("OK builder v260 ready")
