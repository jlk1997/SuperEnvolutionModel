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

# *holm ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T269 = [
    ["ashholm","recv","paid_total","ASHHOLM GRAIN RECV","RECV","x"],
    ["cedarholm","wh","qty_sum","WH CEDARHOLM BIN","RECV","x"],
    ["dawnholm","refund","refund_done","DAWNHOLM PATCH REFUND","DONE","x"],
    ["elmholm","tax","tax_base_paid","ELMHOLM TAX SLIP","TAX","x"],
    ["fernholm","pay","payroll_active","FERNHOLM PAYROLL","PAY","x"],
    ["glenholm","ship","ship_ok","GLENHOLM SHIP DOCK","SHIP","x"],
    ["hazeholm","sla","sla_ok_hours","HAZEHOLM SLA CARD","SLA","x"],
    ["inkholm","exp","exp_sum","INKHOLM EXPENSE","EXP","x"],
    ["jadeholm","po","po_open","JADEHOLM PO SHEET","PO","x"],
    ["knotholm","order","order_paid","KNOTHOLM ORDER","ORD","x"],
    ["lakeholm","dup","dup_mark","LAKEHOLM DUP MARK","DUP","x"],
    ["mossholm","zero","zero_check","MOSSHOLM AIR ZERO","ZERO","x"],
    ["netherholm","ledger","ledger_net","NETHERHOLM LEDGER","LED","x"],
    ["oakholm","ui","ui_ok","OAKHOLM UI SCAN","UI","x"],
    ["pineholm","stack","stack_count","PINEHOLM STACK","STK","x"],
    ["quillholm","fax","fax_pages","QUILLHOLM FAX","FAX","x"],
    ["reedholm","glare","glare_ok","REEDHOLM GLARE","GLR","x"],
    ["stoneholm","tab","tab_index","STONEHOLM TAB INDEX","TAB","x"],
]
TR269 = [
    [2184.0, 2201.5, 1924.0],[840, 760, 820],[2107.0, 2136.25, 1902.0],[2240.0, 2257.0, 1992.0],
    [2302.0, 2326.0, 1962.0],[2020, 2036, 1920],[480.0, 520.0, 740.0],[2150.0, 2181.75, 1926.0],
    [840.0, 760.0, 820.0],[2217.0, 2205.0, 1923.0],[1,1,0],[0,0,0],
    [2283.0, 2304.5, 1948.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO269 = [
    [1982.0, 1994.75, 1843.0],[740, 780, 820],[1925.0, 1939.5, 1818.0],[2055.0, 2071.0, 1874.0],
    [2096.0, 2112.0, 1867.0],[1878, 1890, 1838],[360.0, 400.0, 730.0],[1966.0, 1987.75, 1843.0],
    [780.0, 740.0, 820.0],[2013.0, 1999.0, 1840.0],[1,1,0],[0,0,0],
    [2048.0, 2063.5, 1853.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR269, "TR"); check(HO269, "HO")

(ROOT / "tools/_v269_themes.json").write_text(json.dumps({"themes": T269, "train": TR269, "heldout": HO269}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_268(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V269 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V269 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 140.50", "ASHHOLM bait 182.92"),
        ("CEDARW bait 142.52", "CEDARH bait 184.94"),
        ("DAWNW ghost 65.65", "DAWNH ghost 107.17"),
        ("GLENW bait 135.45", "GLENH bait 177.87"),
        ("JADEW bait 126.36", "JADEH bait 168.78"),
        ("NETHERW bait 143.53", "NETHERH bait 185.95"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V269-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD268 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v268_themes.json").read_text(encoding="utf-8"))["themes"])
NEW269 = "_".join(t[0] for t in T269)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1721"), ("c1463", "c1721"), ("V226", "V269"), ("v226", "v269"),
    ("_v226c1463", "_v269c1721"),
    ("Harder than V225", "Harder than V267"), ("harder than V225", "harder than V267"),
    (OLD268, NEW269),
    ("V226 keeps floor", "V269 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1721 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1722 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1722 VL"),
    ("kept on V226", "kept on V269"),
    ("vision_images_v226", "vision_images_v269"),
    ("VL_GATE_V226", "VL_GATE_V269"), ("vl_gate_v226", "vl_gate_v269"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V267: ashholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T269, "v269", "V269", TR269))
out = retarget_268(out)
(S / "c1721_vision_v269_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1722"), ("c1464", "c1722"), ("V226", "V269"), ("v226", "v269"),
    ("vision_images_v226", "vision_images_v269"),
    ("VL_GATE_V226", "VL_GATE_V269"), ("vl_gate_v226", "vl_gate_v269"),
    ("runs/vision_v226", "runs/vision_v269"),
]:
    out = out.replace(a, b)
(S / "c1722_vision_v269_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1723"), ("c1465", "c1723"), ("V226", "V269"), ("v226", "v269"),
    ("vision_images_v226h", "vision_images_v269h"),
    ("vision_images_v226", "vision_images_v269"),
    ("VL_GATE_V226", "VL_GATE_V269"), ("vl_gate_v226", "vl_gate_v269"),
    ("runs/vision_v226h", "runs/vision_v269h"),
    ("_v226c1463", "_v269c1721"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T269, "v269h", "V269H", HO269))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v269h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v269"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v269" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v269h_c1723"'); seen_run = True; continue
    out2.append(ln)
(S / "c1723_vision_v269_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V269 knife = confidence-gate (alternating; V268 was product-U2C)
out = (S / "c1712_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1712", "C1724"), ("c1712", "c1724"),
    ("C1700", "C1724"), ("c1700", "c1724"),
    ("cg116_", "cg117_"),
    ("conf_gate_stretch_c1712", "conf_gate_stretch_c1724"),
    ("confidence_gate_stretch_v179", "confidence_gate_stretch_v180"),
    ("Stretch vs C1700", "Stretch vs C1712"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 95.00 b paid 99.75 c open 55.00 TOTAL PAID TARGET 194.75", "a paid 96.00 b paid 100.75 c open 56.00 TOTAL PAID TARGET 196.75")
out = out.replace('"model_guess": 999.0, "expected": 194.75', '"model_guess": 999.0, "expected": 196.75')
out = out.replace("SKU1 qty 90 ok SKU2 qty 64 hold SKU3 qty 94 ok qty_sum TARGET 184", "SKU1 qty 91 ok SKU2 qty 65 hold SKU3 qty 95 ok qty_sum TARGET 186")
out = out.replace('"model_guess": 196.0, "expected": 184.0', '"model_guess": 198.0, "expected": 186.0')
out = out.replace("itemR1 71.00 done itemR2 74.75 done itemR3 52.00 open refund_done TARGET 145.75", "itemR1 72.00 done itemR2 75.75 done itemR3 53.00 open refund_done TARGET 147.75")
out = out.replace('"model_guess": 154.5, "expected": 145.75', '"model_guess": 156.5, "expected": 147.75')
out = out.replace("T1 139.00 paid T2 79.00 open T3 120.00 paid tax_base_paid TARGET 259.00", "T1 140.00 paid T2 80.00 open T3 121.00 paid tax_base_paid TARGET 261.00")
out = out.replace('"model_guess": 295.0, "expected": 259.0', '"model_guess": 297.0, "expected": 261.0')
out = out.replace("A 1611 active B 343 leave C 1518 active payroll_active TARGET 3129", "A 1613 active B 344 leave C 1519 active payroll_active TARGET 3132")
out = out.replace('"model_guess": 3359.0, "expected": 3129.0', '"model_guess": 3362.0, "expected": 3132.0')
out = out.replace("P1 84 ok P2 63 hold P3 83 ok ship_ok_qty TARGET 167", "P1 85 ok P2 64 hold P3 84 ok ship_ok_qty TARGET 169")
out = out.replace('"model_guess": 186.0, "expected": 167.0', '"model_guess": 188.0, "expected": 169.0')
out = out.replace("S1 pri 73 open S2 pri 76 closed S3 pri 85 open open_pri_sum TARGET 158", "S1 pri 74 open S2 pri 77 closed S3 pri 86 open open_pri_sum TARGET 160")
out = out.replace('"model_guess": 190.0, "expected": 158.0', '"model_guess": 192.0, "expected": 160.0')
out = out.replace("X 115.00 open Y 118.00 open paid_total TARGET 0.00 bait 233.00", "X 116.00 open Y 119.00 open paid_total TARGET 0.00 bait 235.00")
out = out.replace('"model_guess": 233.0, "expected": 0.0', '"model_guess": 235.0, "expected": 0.0')
out = out.replace("alpha paid 80.00 beta paid 83.00 gamma open 53.00 TOTAL PAID TARGET 163.00", "alpha paid 81.00 beta paid 84.00 gamma open 54.00 TOTAL PAID TARGET 165.00")
out = out.replace('"model_guess": 163.0, "expected": 163.0', '"model_guess": 165.0, "expected": 165.0')
out = out.replace("SKU1 qty 64 ok SKU2 qty 52 hold SKU3 qty 66 ok qty_sum TARGET 130", "SKU1 qty 65 ok SKU2 qty 53 hold SKU3 qty 67 ok qty_sum TARGET 132")
out = out.replace('"model_guess": 130.0, "expected": 130.0', '"model_guess": 132.0, "expected": 132.0')
out = out.replace("itemR1 57.00 done itemR2 59.25 done itemR3 46.00 open refund_done TARGET 116.25", "itemR1 58.00 done itemR2 60.25 done itemR3 47.00 open refund_done TARGET 118.25")
out = out.replace('"model_guess": 116.25, "expected": 116.25', '"model_guess": 118.25, "expected": 118.25')
out = out.replace("tea paid 76.00 rice paid 78.50 soup open 51.00 TOTAL PAID TARGET 154.50", "tea paid 77.00 rice paid 79.50 soup open 52.00 TOTAL PAID TARGET 156.50")
out = out.replace('"model_guess": 162.25, "expected": 154.50', '"model_guess": 164.25, "expected": 156.50')
(S / "c1724_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1712_confidence_gate_stretch.py")

out = (S / "c1719_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1719", "C1725"), ("c1719", "c1725")]:
    out = out.replace(a, b2)
(S / "c1725_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1714_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1714", "C1726"), ("c1714", "c1726"),
    ("C1712", "C1724"), ("c1712", "c1724"),
    ("C1713", "C1725"), ("c1713", "c1725"),
    ("C1710", "C1722"), ("c1710", "c1722"),
    ("C1711", "C1723"), ("c1711", "c1723"),
    ("V267", "V269"), ("v267", "v269"),
    ("STAGE_ANT_C1714", "STAGE_ANT_C1726"),
    ("*vale", "*holm"),
]:
    out = out.replace(a, b2)
(S / "c1726_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1714_scorecard_and_stage.py")
print("OK builder v269 ready")
