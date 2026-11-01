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

# *wick ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T281 = [
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
TR281 = [
    [2218.0, 2235.5, 1958.0],[840, 760, 820],[2141.0, 2170.25, 1936.0],[2274.0, 2291.0, 2026.0],
    [2336.0, 2360.0, 1996.0],[2054, 2070, 1954],[490.0, 530.0, 760.0],[2184.0, 2215.75, 1960.0],
    [840.0, 760.0, 820.0],[2251.0, 2239.0, 1957.0],[1,1,0],[0,0,0],
    [2317.0, 2338.5, 1982.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO281 = [
    [2016.0, 2028.75, 1877.0],[640, 660, 820],[1959.0, 1973.5, 1852.0],[2089.0, 2105.0, 1908.0],
    [2130.0, 2146.0, 1901.0],[1912, 1924, 1872],[420.0, 460.0, 740.0],[2000.0, 2021.75, 1877.0],
    [740.0, 780.0, 820.0],[2047.0, 2033.0, 1874.0],[1,1,0],[0,0,0],
    [2082.0, 2097.5, 1887.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR281, "TR"); check(HO281, "HO")

(ROOT / "tools/_v281_themes.json").write_text(json.dumps({"themes": T281, "train": TR281, "heldout": HO281}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_280(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V281 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V281 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHWICK bait 185.95"),
        ("CEDARW bait 142.52", "CEDARW bait 196.06"),
        ("DAWNW ghost 65.65", "DAWNW ghost 119.29"),
        ("GLENW bait 135.45", "GLENW bait 189.99"),
        ("JADEW bait 126.36", "JADEW bait 180.90"),
        ("NETHERW bait 143.53", "NETHERW bait 197.07"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V281-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD280 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v280_themes.json").read_text(encoding="utf-8"))["themes"])
NEW281 = "_".join(t[0] for t in T281)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1793"), ("c1463", "c1793"), ("V226", "V281"), ("v226", "v281"),
    ("_v226c1463", "_v281c1793"),
    ("Harder than V225", "Harder than V279"), ("harder than V225", "harder than V279"),
    (OLD280, NEW281),
    ("V226 keeps floor", "V281 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1793 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1794 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1794 VL"),
    ("kept on V226", "kept on V281"),
    ("vision_images_v226", "vision_images_v281"),
    ("VL_GATE_V226", "VL_GATE_V281"), ("vl_gate_v226", "vl_gate_v281"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V279: ashwick, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T281, "v281", "V281", TR281))
out = retarget_280(out)
(S / "c1793_vision_v281_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1794"), ("c1464", "c1794"), ("V226", "V281"), ("v226", "v281"),
    ("vision_images_v226", "vision_images_v281"),
    ("VL_GATE_V226", "VL_GATE_V281"), ("vl_gate_v226", "vl_gate_v281"),
    ("runs/vision_v226", "runs/vision_v281"),
]:
    out = out.replace(a, b)
(S / "c1794_vision_v281_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1795"), ("c1465", "c1795"), ("V226", "V281"), ("v226", "v281"),
    ("vision_images_v226h", "vision_images_v281h"),
    ("vision_images_v226", "vision_images_v281"),
    ("VL_GATE_V226", "VL_GATE_V281"), ("vl_gate_v226", "vl_gate_v281"),
    ("runs/vision_v226h", "runs/vision_v281h"),
    ("_v226c1463", "_v281c1793"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T281, "v281h", "V281H", HO281))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v281h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v281"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v281" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v281h_c1795"'); seen_run = True; continue
    out2.append(ln)
(S / "c1795_vision_v281_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V281 knife = confidence-gate (alternating; V280 was product-U2C)
out = (S / "c1784_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1784", "C1796"), ("c1784", "c1796"),
    ("C1772", "C1796"), ("c1772", "c1796"),
    ("cg122_", "cg123_"),
    ("conf_gate_stretch_c1784", "conf_gate_stretch_c1796"),
    ("confidence_gate_stretch_v185", "confidence_gate_stretch_v186"),
    ("Stretch vs C1772", "Stretch vs C1784"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 101.00 b paid 105.75 c open 61.00 TOTAL PAID TARGET 206.75", "a paid 102.00 b paid 106.75 c open 62.00 TOTAL PAID TARGET 208.75")
out = out.replace('"model_guess": 999.0, "expected": 206.75', '"model_guess": 999.0, "expected": 208.75')
out = out.replace("SKU1 qty 96 ok SKU2 qty 70 hold SKU3 qty 100 ok qty_sum TARGET 196", "SKU1 qty 97 ok SKU2 qty 71 hold SKU3 qty 101 ok qty_sum TARGET 198")
out = out.replace('"model_guess": 208.0, "expected": 196.0', '"model_guess": 210.0, "expected": 198.0')
out = out.replace("itemR1 77.00 done itemR2 80.75 done itemR3 58.00 open refund_done TARGET 157.75", "itemR1 78.00 done itemR2 81.75 done itemR3 59.00 open refund_done TARGET 159.75")
out = out.replace('"model_guess": 166.5, "expected": 157.75', '"model_guess": 168.5, "expected": 159.75')
out = out.replace("T1 145.00 paid T2 85.00 open T3 126.00 paid tax_base_paid TARGET 271.00", "T1 146.00 paid T2 86.00 open T3 127.00 paid tax_base_paid TARGET 273.00")
out = out.replace('"model_guess": 307.0, "expected": 271.0', '"model_guess": 309.0, "expected": 273.0')
out = out.replace("A 1623 active B 349 leave C 1524 active payroll_active TARGET 3147", "A 1625 active B 350 leave C 1525 active payroll_active TARGET 3150")
out = out.replace('"model_guess": 3377.0, "expected": 3147.0', '"model_guess": 3380.0, "expected": 3150.0')
out = out.replace("P1 90 ok P2 69 hold P3 89 ok ship_ok_qty TARGET 179", "P1 91 ok P2 70 hold P3 90 ok ship_ok_qty TARGET 181")
out = out.replace('"model_guess": 198.0, "expected": 179.0', '"model_guess": 200.0, "expected": 181.0')
out = out.replace("S1 pri 79 open S2 pri 82 closed S3 pri 91 open open_pri_sum TARGET 170", "S1 pri 80 open S2 pri 83 closed S3 pri 92 open open_pri_sum TARGET 172")
out = out.replace('"model_guess": 202.0, "expected": 170.0', '"model_guess": 204.0, "expected": 172.0')
out = out.replace("X 121.00 open Y 124.00 open paid_total TARGET 0.00 bait 245.00", "X 122.00 open Y 125.00 open paid_total TARGET 0.00 bait 247.00")
out = out.replace('"model_guess": 245.0, "expected": 0.0', '"model_guess": 247.0, "expected": 0.0')
out = out.replace("alpha paid 86.00 beta paid 89.00 gamma open 59.00 TOTAL PAID TARGET 175.00", "alpha paid 87.00 beta paid 90.00 gamma open 60.00 TOTAL PAID TARGET 177.00")
out = out.replace('"model_guess": 175.0, "expected": 175.0', '"model_guess": 177.0, "expected": 177.0')
out = out.replace("SKU1 qty 70 ok SKU2 qty 58 hold SKU3 qty 72 ok qty_sum TARGET 142", "SKU1 qty 71 ok SKU2 qty 59 hold SKU3 qty 73 ok qty_sum TARGET 144")
out = out.replace('"model_guess": 142.0, "expected": 142.0', '"model_guess": 144.0, "expected": 144.0')
out = out.replace("itemR1 63.00 done itemR2 65.25 done itemR3 52.00 open refund_done TARGET 128.25", "itemR1 64.00 done itemR2 66.25 done itemR3 53.00 open refund_done TARGET 130.25")
out = out.replace('"model_guess": 128.25, "expected": 128.25', '"model_guess": 130.25, "expected": 130.25')
out = out.replace("tea paid 82.00 rice paid 84.50 soup open 57.00 TOTAL PAID TARGET 166.50", "tea paid 83.00 rice paid 85.50 soup open 58.00 TOTAL PAID TARGET 168.50")
out = out.replace('"model_guess": 174.25, "expected": 166.50', '"model_guess": 176.25, "expected": 168.50')
(S / "c1796_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1784_confidence_gate_stretch.py")

out = (S / "c1791_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1791", "C1797"), ("c1791", "c1797")]:
    out = out.replace(a, b2)
(S / "c1797_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1786_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1786", "C1798"), ("c1786", "c1798"),
    ("C1784", "C1796"), ("c1784", "c1796"),
    ("C1785", "C1797"), ("c1785", "c1797"),
    ("C1782", "C1794"), ("c1782", "c1794"),
    ("C1783", "C1795"), ("c1783", "c1795"),
    ("V279", "V281"), ("v279", "v281"),
    ("STAGE_ANT_C1786", "STAGE_ANT_C1798"),
    ("*croft", "*wick"),
]:
    out = out.replace(a, b2)
(S / "c1798_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1786_scorecard_and_stage.py")
print("OK builder v281 ready")
