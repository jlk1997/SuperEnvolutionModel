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
T282 = [
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
TR282 = [
    [2221.0, 2238.5, 1961.0],[840, 760, 820],[2144.0, 2173.25, 1939.0],[2277.0, 2294.0, 2029.0],
    [2339.0, 2363.0, 1999.0],[2057, 2073, 1957],[490.0, 530.0, 760.0],[2187.0, 2218.75, 1963.0],
    [840.0, 760.0, 820.0],[2254.0, 2242.0, 1960.0],[1,1,0],[0,0,0],
    [2320.0, 2341.5, 1985.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO282 = [
    [2019.0, 2031.75, 1880.0],[640, 660, 820],[1962.0, 1976.5, 1855.0],[2092.0, 2108.0, 1911.0],
    [2133.0, 2149.0, 1904.0],[1915, 1927, 1875],[420.0, 460.0, 740.0],[2003.0, 2024.75, 1880.0],
    [740.0, 780.0, 820.0],[2050.0, 2036.0, 1877.0],[1,1,0],[0,0,0],
    [2085.0, 2100.5, 1890.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR282, "TR"); check(HO282, "HO")

(ROOT / "tools/_v282_themes.json").write_text(json.dumps({"themes": T282, "train": TR282, "heldout": HO282}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_281(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V282 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V282 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 140.50", "ASHMOOR bait 185.95"),
        ("CEDARW bait 142.52", "CEDARM bait 197.07"),
        ("DAWNW ghost 65.65", "DAWNM ghost 120.30"),
        ("GLENW bait 135.45", "GLENM bait 190.00"),
        ("JADEW bait 126.36", "JADEM bait 181.91"),
        ("NETHERW bait 143.53", "NETHERM bait 198.08"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V282-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD281 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v281_themes.json").read_text(encoding="utf-8"))["themes"])
NEW282 = "_".join(t[0] for t in T282)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1799"), ("c1463", "c1799"), ("V226", "V282"), ("v226", "v282"),
    ("_v226c1463", "_v282c1799"),
    ("Harder than V225", "Harder than V280"), ("harder than V225", "harder than V280"),
    (OLD281, NEW282),
    ("V226 keeps floor", "V282 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1799 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1800 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1800 VL"),
    ("kept on V226", "kept on V282"),
    ("vision_images_v226", "vision_images_v282"),
    ("VL_GATE_V226", "VL_GATE_V282"), ("vl_gate_v226", "vl_gate_v282"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V280: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T282, "v282", "V282", TR282))
out = retarget_281(out)
(S / "c1799_vision_v282_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1800"), ("c1464", "c1800"), ("V226", "V282"), ("v226", "v282"),
    ("vision_images_v226", "vision_images_v282"),
    ("VL_GATE_V226", "VL_GATE_V282"), ("vl_gate_v226", "vl_gate_v282"),
    ("runs/vision_v226", "runs/vision_v282"),
]:
    out = out.replace(a, b)
(S / "c1800_vision_v282_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1801"), ("c1465", "c1801"), ("V226", "V282"), ("v226", "v282"),
    ("vision_images_v226h", "vision_images_v282h"),
    ("vision_images_v226", "vision_images_v282"),
    ("VL_GATE_V226", "VL_GATE_V282"), ("vl_gate_v226", "vl_gate_v282"),
    ("runs/vision_v226h", "runs/vision_v282h"),
    ("_v226c1463", "_v282c1799"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T282, "v282h", "V282H", HO282))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v282h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v282"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v282" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v282h_c1801"'); seen_run = True; continue
    out2.append(ln)
(S / "c1801_vision_v282_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V282 knife = product-U2C (alternating; V281 was confidence-gate)
out = (S / "c1790_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1790", "C1802"), ("c1790", "c1802"),
    ("C1778", "C1802"), ("c1778", "c1802"),
    ("C1466", "C1802"), ("c1466", "c1802"),
]:
    out = out.replace(a, b2)
(S / "c1802_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1790_product_u2c_cost.py")

out = (S / "c1797_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1797", "C1803"), ("c1797", "c1803")]:
    out = out.replace(a, b2)
(S / "c1803_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1792_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1792", "C1804"), ("c1792", "c1804"),
    ("C1790", "C1802"), ("c1790", "c1802"),
    ("C1791", "C1803"), ("c1791", "c1803"),
    ("C1788", "C1800"), ("c1788", "c1800"),
    ("C1789", "C1801"), ("c1789", "c1801"),
    ("V280", "V282"), ("v280", "v282"),
    ("STAGE_ANT_C1792", "STAGE_ANT_C1804"),
    ("*holm", "*moor"),
]:
    out = out.replace(a, b2)
(S / "c1804_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1792_scorecard_and_stage.py")
print("OK builder v282 ready")
