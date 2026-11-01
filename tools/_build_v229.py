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

# *brook ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T229 = [
    ["ashbrook","recv","paid_total","ASHBROOK GRAIN RECV","RECV","x"],
    ["cedarbrook","wh","qty_sum","WH CEDARBROOK BIN","RECV","x"],
    ["dawnbrook","refund","refund_done","DAWNBROOK PATCH REFUND","DONE","x"],
    ["elmbrook","tax","tax_base_paid","ELMBROOK TAX SLIP","TAX","x"],
    ["fernbrook","pay","payroll_active","FERNBROOK PAYROLL","PAY","x"],
    ["glenbrook","ship","ship_ok","GLENBROOK SHIP DOCK","SHIP","x"],
    ["hazebrook","sla","sla_ok_hours","HAZEBROOK SLA CARD","SLA","x"],
    ["inkbrook","exp","exp_sum","INKBROOK EXPENSE","EXP","x"],
    ["jadebrook","po","po_open","JADEBROOK PO SHEET","PO","x"],
    ["knotbrook","order","order_paid","KNOTBROOK ORDER","ORD","x"],
    ["lakebrook","dup","dup_mark","LAKEBROOK DUP MARK","DUP","x"],
    ["mossbrook","zero","zero_check","MOSSBROOK AIR ZERO","ZERO","x"],
    ["netherbrook","ledger","ledger_net","NETHERBROOK LEDGER","LED","x"],
    ["oakbrook","ui","ui_ok","OAKBROOK UI SCAN","UI","x"],
    ["pinebrook","stack","stack_count","PINEBROOK STACK","STK","x"],
    ["quillbrook","fax","fax_pages","QUILLBROOK FAX","FAX","x"],
    ["reedbrook","glare","glare_ok","REEDBROOK GLARE","GLR","x"],
    ["stonebrook","tab","tab_index","STONEBROOK TAB INDEX","TAB","x"],
]
TR229 = [
    [1816.0, 1833.5, 1590.0],[840, 760, 820],[1739.0, 1768.25, 1570.0],[1872.0, 1889.0, 1660.0],
    [1934.0, 1958.0, 1630.0],[1688, 1704, 1588],[480.0, 520.0, 740.0],[1782.0, 1813.75, 1594.0],
    [840.0, 760.0, 820.0],[1849.0, 1837.0, 1591.0],[1,1,0],[0,0,0],
    [1915.0, 1936.5, 1616.0],[1,0,0],[1164, 1156, 1136],[1180, 1164, 748],[1,0,0],[1196, 1180, 1158],
]
HO229 = [
    [1650.0, 1662.75, 1511.0],[740, 780, 820],[1593.0, 1606.5, 1486.0],[1723.0, 1739.0, 1540.0],
    [1764.0, 1780.0, 1535.0],[1558, 1572, 1504],[360.0, 400.0, 730.0],[1634.0, 1655.75, 1511.0],
    [780.0, 740.0, 820.0],[1681.0, 1667.0, 1506.0],[1,1,0],[0,0,0],
    [1716.0, 1731.5, 1521.0],[1,0,0],[1152, 1147, 1140],[1166, 1160, 1148],[1,0,0],[1176, 1170, 1149],
]
check(TR229, "TR"); check(HO229, "HO")

(ROOT / "tools/_v229_themes.json").write_text(json.dumps({"themes": T229, "train": TR229, "heldout": HO229}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_228(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V229 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V229 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHBROOK bait 142.52"),
        ("CEDARW bait 142.52", "CEDARB bait 144.54"),
        ("DAWNW ghost 65.65", "DAWNB ghost 67.67"),
        ("GLENW bait 135.45", "GLENB bait 137.47"),
        ("JADEW bait 126.36", "JADEB bait 128.38"),
        ("NETHERW bait 143.53", "NETHERB bait 145.55"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V229-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD228 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v228_themes.json").read_text(encoding="utf-8"))["themes"])
NEW229 = "_".join(t[0] for t in T229)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1481"), ("c1463", "c1481"), ("V226", "V229"), ("v226", "v229"),
    ("_v226c1463", "_v229c1481"),
    ("Harder than V225", "Harder than V227"), ("harder than V225", "harder than V227"),
    (OLD228, NEW229),
    ("V226 keeps floor", "V229 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1481 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1482 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1482 VL"),
    ("kept on V226", "kept on V229"),
    ("vision_images_v226", "vision_images_v229"),
    ("VL_GATE_V226", "VL_GATE_V229"), ("vl_gate_v226", "vl_gate_v229"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V227: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T229, "v229", "V229", TR229))
out = retarget_228(out)
(S / "c1481_vision_v229_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1482"), ("c1464", "c1482"), ("V226", "V229"), ("v226", "v229"),
    ("vision_images_v226", "vision_images_v229"),
    ("VL_GATE_V226", "VL_GATE_V229"), ("vl_gate_v226", "vl_gate_v229"),
    ("runs/vision_v226", "runs/vision_v229"),
]:
    out = out.replace(a, b)
(S / "c1482_vision_v229_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1483"), ("c1465", "c1483"), ("V226", "V229"), ("v226", "v229"),
    ("vision_images_v226h", "vision_images_v229h"),
    ("vision_images_v226", "vision_images_v229"),
    ("VL_GATE_V226", "VL_GATE_V229"), ("vl_gate_v226", "vl_gate_v229"),
    ("runs/vision_v226h", "runs/vision_v229h"),
    ("_v226c1463", "_v229c1481"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T229, "v229h", "V229H", HO229))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v229h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v229"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v229" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v229h_c1483"'); seen_run = True; continue
    out2.append(ln)
(S / "c1483_vision_v229_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V229 knife = confidence-gate (alternating; V228 was product-U2C)
out = (S / "c1472_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1472", "C1484"), ("c1472", "c1484"),
    ("cg96_", "cg97_"),
    ("conf_gate_stretch_c1472", "conf_gate_stretch_c1484"),
    ("confidence_gate_stretch_v159", "confidence_gate_stretch_v160"),
    ("Stretch vs C1460", "Stretch vs C1472"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 75.00 b paid 79.75 c open 35.00 TOTAL PAID TARGET 154.75", "a paid 76.00 b paid 80.75 c open 36.00 TOTAL PAID TARGET 156.75")
out = out.replace('"model_guess": 999.0, "expected": 154.75', '"model_guess": 999.0, "expected": 156.75')
out = out.replace("SKU1 qty 70 ok SKU2 qty 44 hold SKU3 qty 74 ok qty_sum TARGET 144", "SKU1 qty 71 ok SKU2 qty 45 hold SKU3 qty 75 ok qty_sum TARGET 146")
out = out.replace('"model_guess": 156.0, "expected": 144.0', '"model_guess": 158.0, "expected": 146.0')
out = out.replace("itemR1 51.00 done itemR2 54.75 done itemR3 32.00 open refund_done TARGET 105.75", "itemR1 52.00 done itemR2 55.75 done itemR3 33.00 open refund_done TARGET 107.75")
out = out.replace('"model_guess": 114.5, "expected": 105.75', '"model_guess": 116.5, "expected": 107.75')
out = out.replace("T1 119.00 paid T2 59.00 open T3 100.00 paid tax_base_paid TARGET 219.00", "T1 120.00 paid T2 60.00 open T3 101.00 paid tax_base_paid TARGET 221.00")
out = out.replace('"model_guess": 255.0, "expected": 219.0', '"model_guess": 257.0, "expected": 221.0')
out = out.replace("A 1571 active B 323 leave C 1498 active payroll_active TARGET 3069", "A 1573 active B 324 leave C 1499 active payroll_active TARGET 3072")
out = out.replace('"model_guess": 3299.0, "expected": 3069.0', '"model_guess": 3302.0, "expected": 3072.0')
out = out.replace("P1 64 ok P2 43 hold P3 63 ok ship_ok_qty TARGET 127", "P1 65 ok P2 44 hold P3 64 ok ship_ok_qty TARGET 129")
out = out.replace('"model_guess": 146.0, "expected": 127.0', '"model_guess": 148.0, "expected": 129.0')
out = out.replace("S1 pri 53 open S2 pri 56 closed S3 pri 65 open open_pri_sum TARGET 118", "S1 pri 54 open S2 pri 57 closed S3 pri 66 open open_pri_sum TARGET 120")
out = out.replace('"model_guess": 150.0, "expected": 118.0', '"model_guess": 152.0, "expected": 120.0')
out = out.replace("X 95.00 open Y 98.00 open paid_total TARGET 0.00 bait 193.00", "X 96.00 open Y 99.00 open paid_total TARGET 0.00 bait 195.00")
out = out.replace('"model_guess": 193.0, "expected": 0.0', '"model_guess": 195.0, "expected": 0.0')
out = out.replace("alpha paid 60.00 beta paid 63.00 gamma open 33.00 TOTAL PAID TARGET 123.00", "alpha paid 61.00 beta paid 64.00 gamma open 34.00 TOTAL PAID TARGET 125.00")
out = out.replace('"model_guess": 123.0, "expected": 123.0', '"model_guess": 125.0, "expected": 125.0')
out = out.replace("SKU1 qty 44 ok SKU2 qty 32 hold SKU3 qty 46 ok qty_sum TARGET 90", "SKU1 qty 45 ok SKU2 qty 33 hold SKU3 qty 47 ok qty_sum TARGET 92")
out = out.replace('"model_guess": 90.0, "expected": 90.0', '"model_guess": 92.0, "expected": 92.0')
out = out.replace("itemR1 37.00 done itemR2 39.25 done itemR3 26.00 open refund_done TARGET 76.25", "itemR1 38.00 done itemR2 40.25 done itemR3 27.00 open refund_done TARGET 78.25")
out = out.replace('"model_guess": 76.25, "expected": 76.25', '"model_guess": 78.25, "expected": 78.25')
out = out.replace("tea paid 56.00 rice paid 58.50 soup open 31.00 TOTAL PAID TARGET 114.50", "tea paid 57.00 rice paid 59.50 soup open 32.00 TOTAL PAID TARGET 116.50")
out = out.replace('"model_guess": 122.25, "expected": 114.50', '"model_guess": 124.25, "expected": 116.50')
(S / "c1484_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1479_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1479", "C1485"), ("c1479", "c1485")]:
    out = out.replace(a, b2)
(S / "c1485_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1474_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1474", "C1486"), ("c1474", "c1486"),
    ("C1472", "C1484"), ("c1472", "c1484"),
    ("C1473", "C1485"), ("c1473", "c1485"),
    ("C1470", "C1482"), ("c1470", "c1482"),
    ("C1471", "C1483"), ("c1471", "c1483"),
    ("V227", "V229"), ("v227", "v229"),
    ("STAGE_ANT_C1474", "STAGE_ANT_C1486"),
    ("*moor", "*brook"),
]:
    out = out.replace(a, b2)
(S / "c1486_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v229 ready")
