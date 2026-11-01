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
T271 = [
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
TR271 = [
    [2188.0, 2205.5, 1928.0],[840, 760, 820],[2111.0, 2140.25, 1906.0],[2244.0, 2261.0, 1996.0],
    [2306.0, 2330.0, 1966.0],[2024, 2040, 1924],[480.0, 520.0, 740.0],[2154.0, 2185.75, 1930.0],
    [840.0, 760.0, 820.0],[2221.0, 2209.0, 1927.0],[1,1,0],[0,0,0],
    [2287.0, 2308.5, 1952.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO271 = [
    [1986.0, 1998.75, 1847.0],[740, 780, 820],[1929.0, 1943.5, 1822.0],[2059.0, 2075.0, 1878.0],
    [2100.0, 2116.0, 1871.0],[1882, 1894, 1842],[360.0, 400.0, 730.0],[1970.0, 1991.75, 1847.0],
    [780.0, 740.0, 820.0],[2017.0, 2003.0, 1844.0],[1,1,0],[0,0,0],
    [2052.0, 2067.5, 1857.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR271, "TR"); check(HO271, "HO")

(ROOT / "tools/_v271_themes.json").write_text(json.dumps({"themes": T271, "train": TR271, "heldout": HO271}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_270(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V271 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V271 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 140.50", "ASHMOOR bait 184.94"),
        ("CEDARW bait 142.52", "CEDARM bait 186.96"),
        ("DAWNW ghost 65.65", "DAWNM ghost 109.19"),
        ("GLENW bait 135.45", "GLENM bait 179.89"),
        ("JADEW bait 126.36", "JADEM bait 170.80"),
        ("NETHERW bait 143.53", "NETHERM bait 187.97"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V271-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD270 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v270_themes.json").read_text(encoding="utf-8"))["themes"])
NEW271 = "_".join(t[0] for t in T271)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1733"), ("c1463", "c1733"), ("V226", "V271"), ("v226", "v271"),
    ("_v226c1463", "_v271c1733"),
    ("Harder than V225", "Harder than V269"), ("harder than V225", "harder than V269"),
    (OLD270, NEW271),
    ("V226 keeps floor", "V271 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1733 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1734 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1734 VL"),
    ("kept on V226", "kept on V271"),
    ("vision_images_v226", "vision_images_v271"),
    ("VL_GATE_V226", "VL_GATE_V271"), ("vl_gate_v226", "vl_gate_v271"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V269: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T271, "v271", "V271", TR271))
out = retarget_270(out)
(S / "c1733_vision_v271_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1734"), ("c1464", "c1734"), ("V226", "V271"), ("v226", "v271"),
    ("vision_images_v226", "vision_images_v271"),
    ("VL_GATE_V226", "VL_GATE_V271"), ("vl_gate_v226", "vl_gate_v271"),
    ("runs/vision_v226", "runs/vision_v271"),
]:
    out = out.replace(a, b)
(S / "c1734_vision_v271_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1735"), ("c1465", "c1735"), ("V226", "V271"), ("v226", "v271"),
    ("vision_images_v226h", "vision_images_v271h"),
    ("vision_images_v226", "vision_images_v271"),
    ("VL_GATE_V226", "VL_GATE_V271"), ("vl_gate_v226", "vl_gate_v271"),
    ("runs/vision_v226h", "runs/vision_v271h"),
    ("_v226c1463", "_v271c1733"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T271, "v271h", "V271H", HO271))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v271h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v271"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v271" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v271h_c1735"'); seen_run = True; continue
    out2.append(ln)
(S / "c1735_vision_v271_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V271 knife = confidence-gate (alternating; V270 was product-U2C)
out = (S / "c1724_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1724", "C1736"), ("c1724", "c1736"),
    ("C1712", "C1736"), ("c1712", "c1736"),
    ("cg117_", "cg118_"),
    ("conf_gate_stretch_c1724", "conf_gate_stretch_c1736"),
    ("confidence_gate_stretch_v180", "confidence_gate_stretch_v181"),
    ("Stretch vs C1712", "Stretch vs C1724"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 96.00 b paid 100.75 c open 56.00 TOTAL PAID TARGET 196.75", "a paid 97.00 b paid 101.75 c open 57.00 TOTAL PAID TARGET 198.75")
out = out.replace('"model_guess": 999.0, "expected": 196.75', '"model_guess": 999.0, "expected": 198.75')
out = out.replace("SKU1 qty 91 ok SKU2 qty 65 hold SKU3 qty 95 ok qty_sum TARGET 186", "SKU1 qty 92 ok SKU2 qty 66 hold SKU3 qty 96 ok qty_sum TARGET 188")
out = out.replace('"model_guess": 198.0, "expected": 186.0', '"model_guess": 200.0, "expected": 188.0')
out = out.replace("itemR1 72.00 done itemR2 75.75 done itemR3 53.00 open refund_done TARGET 147.75", "itemR1 73.00 done itemR2 76.75 done itemR3 54.00 open refund_done TARGET 149.75")
out = out.replace('"model_guess": 156.5, "expected": 147.75', '"model_guess": 158.5, "expected": 149.75')
out = out.replace("T1 140.00 paid T2 80.00 open T3 121.00 paid tax_base_paid TARGET 261.00", "T1 141.00 paid T2 81.00 open T3 122.00 paid tax_base_paid TARGET 263.00")
out = out.replace('"model_guess": 297.0, "expected": 261.0', '"model_guess": 299.0, "expected": 263.0')
out = out.replace("A 1613 active B 344 leave C 1519 active payroll_active TARGET 3132", "A 1615 active B 345 leave C 1520 active payroll_active TARGET 3135")
out = out.replace('"model_guess": 3362.0, "expected": 3132.0', '"model_guess": 3365.0, "expected": 3135.0')
out = out.replace("P1 85 ok P2 64 hold P3 84 ok ship_ok_qty TARGET 169", "P1 86 ok P2 65 hold P3 85 ok ship_ok_qty TARGET 171")
out = out.replace('"model_guess": 188.0, "expected": 169.0', '"model_guess": 190.0, "expected": 171.0')
out = out.replace("S1 pri 74 open S2 pri 77 closed S3 pri 86 open open_pri_sum TARGET 160", "S1 pri 75 open S2 pri 78 closed S3 pri 87 open open_pri_sum TARGET 162")
out = out.replace('"model_guess": 192.0, "expected": 160.0', '"model_guess": 194.0, "expected": 162.0')
out = out.replace("X 116.00 open Y 119.00 open paid_total TARGET 0.00 bait 235.00", "X 117.00 open Y 120.00 open paid_total TARGET 0.00 bait 237.00")
out = out.replace('"model_guess": 235.0, "expected": 0.0', '"model_guess": 237.0, "expected": 0.0')
out = out.replace("alpha paid 81.00 beta paid 84.00 gamma open 54.00 TOTAL PAID TARGET 165.00", "alpha paid 82.00 beta paid 85.00 gamma open 55.00 TOTAL PAID TARGET 167.00")
out = out.replace('"model_guess": 165.0, "expected": 165.0', '"model_guess": 167.0, "expected": 167.0')
out = out.replace("SKU1 qty 65 ok SKU2 qty 53 hold SKU3 qty 67 ok qty_sum TARGET 132", "SKU1 qty 66 ok SKU2 qty 54 hold SKU3 qty 68 ok qty_sum TARGET 134")
out = out.replace('"model_guess": 132.0, "expected": 132.0', '"model_guess": 134.0, "expected": 134.0')
out = out.replace("itemR1 58.00 done itemR2 60.25 done itemR3 47.00 open refund_done TARGET 118.25", "itemR1 59.00 done itemR2 61.25 done itemR3 48.00 open refund_done TARGET 120.25")
out = out.replace('"model_guess": 118.25, "expected": 118.25', '"model_guess": 120.25, "expected": 120.25')
out = out.replace("tea paid 77.00 rice paid 79.50 soup open 52.00 TOTAL PAID TARGET 156.50", "tea paid 78.00 rice paid 80.50 soup open 53.00 TOTAL PAID TARGET 158.50")
out = out.replace('"model_guess": 164.25, "expected": 156.50', '"model_guess": 166.25, "expected": 158.50')
(S / "c1736_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1724_confidence_gate_stretch.py")

out = (S / "c1731_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1731", "C1737"), ("c1731", "c1737")]:
    out = out.replace(a, b2)
(S / "c1737_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1726_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1726", "C1738"), ("c1726", "c1738"),
    ("C1724", "C1736"), ("c1724", "c1736"),
    ("C1725", "C1737"), ("c1725", "c1737"),
    ("C1722", "C1734"), ("c1722", "c1734"),
    ("C1723", "C1735"), ("c1723", "c1735"),
    ("V269", "V271"), ("v269", "v271"),
    ("STAGE_ANT_C1726", "STAGE_ANT_C1738"),
    ("*holm", "*moor"),
]:
    out = out.replace(a, b2)
(S / "c1738_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1726_scorecard_and_stage.py")
print("OK builder v271 ready")
