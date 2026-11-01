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

# *croft ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T257 = [
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
TR257 = [
    [2160.0, 2177.5, 1900.0],[840, 760, 820],[2083.0, 2112.25, 1878.0],[2216.0, 2233.0, 1968.0],
    [2278.0, 2302.0, 1938.0],[1996, 2012, 1896],[480.0, 520.0, 740.0],[2126.0, 2157.75, 1902.0],
    [840.0, 760.0, 820.0],[2193.0, 2181.0, 1899.0],[1,1,0],[0,0,0],
    [2259.0, 2280.5, 1924.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO257 = [
    [1958.0, 1970.75, 1819.0],[740, 780, 820],[1901.0, 1915.5, 1794.0],[2031.0, 2047.0, 1850.0],
    [2072.0, 2088.0, 1843.0],[1854, 1866, 1812],[360.0, 400.0, 730.0],[1942.0, 1963.75, 1819.0],
    [780.0, 740.0, 820.0],[1989.0, 1975.0, 1814.0],[1,1,0],[0,0,0],
    [2024.0, 2039.5, 1829.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR257, "TR"); check(HO257, "HO")

(ROOT / "tools/_v257_themes.json").write_text(json.dumps({"themes": T257, "train": TR257, "heldout": HO257}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_256(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V257 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V257 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 140.50", "ASHCROFT bait 170.80"),
        ("CEDARW bait 142.52", "CEDARC bait 172.82"),
        ("DAWNW ghost 65.65", "DAWNC ghost 95.95"),
        ("GLENW bait 135.45", "GLENC bait 165.75"),
        ("JADEW bait 126.36", "JADEC bait 156.66"),
        ("NETHERW bait 143.53", "NETHERC bait 173.83"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V257-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD256 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v256_themes.json").read_text(encoding="utf-8"))["themes"])
NEW257 = "_".join(t[0] for t in T257)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1649"), ("c1463", "c1649"), ("V226", "V257"), ("v226", "v257"),
    ("_v226c1463", "_v257c1649"),
    ("Harder than V225", "Harder than V255"), ("harder than V225", "harder than V255"),
    (OLD256, NEW257),
    ("V226 keeps floor", "V257 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1649 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1650 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1650 VL"),
    ("kept on V226", "kept on V257"),
    ("vision_images_v226", "vision_images_v257"),
    ("VL_GATE_V226", "VL_GATE_V257"), ("vl_gate_v226", "vl_gate_v257"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V255: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T257, "v257", "V257", TR257))
out = retarget_256(out)
(S / "c1649_vision_v257_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1650"), ("c1464", "c1650"), ("V226", "V257"), ("v226", "v257"),
    ("vision_images_v226", "vision_images_v257"),
    ("VL_GATE_V226", "VL_GATE_V257"), ("vl_gate_v226", "vl_gate_v257"),
    ("runs/vision_v226", "runs/vision_v257"),
]:
    out = out.replace(a, b)
(S / "c1650_vision_v257_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1651"), ("c1465", "c1651"), ("V226", "V257"), ("v226", "v257"),
    ("vision_images_v226h", "vision_images_v257h"),
    ("vision_images_v226", "vision_images_v257"),
    ("VL_GATE_V226", "VL_GATE_V257"), ("vl_gate_v226", "vl_gate_v257"),
    ("runs/vision_v226h", "runs/vision_v257h"),
    ("_v226c1463", "_v257c1649"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T257, "v257h", "V257H", HO257))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v257h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v257"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v257" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v257h_c1651"'); seen_run = True; continue
    out2.append(ln)
(S / "c1651_vision_v257_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V257 knife = confidence-gate (alternating; V256 was product-U2C)
out = (S / "c1640_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1640", "C1652"), ("c1640", "c1652"),
    ("C1628", "C1652"), ("c1628", "c1652"),
    ("cg110_", "cg111_"),
    ("conf_gate_stretch_c1640", "conf_gate_stretch_c1652"),
    ("confidence_gate_stretch_v173", "confidence_gate_stretch_v174"),
    ("Stretch vs C1628", "Stretch vs C1640"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 89.00 b paid 93.75 c open 49.00 TOTAL PAID TARGET 182.75", "a paid 90.00 b paid 94.75 c open 50.00 TOTAL PAID TARGET 184.75")
out = out.replace('"model_guess": 999.0, "expected": 182.75', '"model_guess": 999.0, "expected": 184.75')
out = out.replace("SKU1 qty 84 ok SKU2 qty 58 hold SKU3 qty 88 ok qty_sum TARGET 172", "SKU1 qty 85 ok SKU2 qty 59 hold SKU3 qty 89 ok qty_sum TARGET 174")
out = out.replace('"model_guess": 184.0, "expected": 172.0', '"model_guess": 186.0, "expected": 174.0')
out = out.replace("itemR1 65.00 done itemR2 68.75 done itemR3 46.00 open refund_done TARGET 133.75", "itemR1 66.00 done itemR2 69.75 done itemR3 47.00 open refund_done TARGET 135.75")
out = out.replace('"model_guess": 142.5, "expected": 133.75', '"model_guess": 144.5, "expected": 135.75')
out = out.replace("T1 133.00 paid T2 73.00 open T3 114.00 paid tax_base_paid TARGET 247.00", "T1 134.00 paid T2 74.00 open T3 115.00 paid tax_base_paid TARGET 249.00")
out = out.replace('"model_guess": 283.0, "expected": 247.0', '"model_guess": 285.0, "expected": 249.0')
out = out.replace("A 1599 active B 337 leave C 1512 active payroll_active TARGET 3111", "A 1601 active B 338 leave C 1513 active payroll_active TARGET 3114")
out = out.replace('"model_guess": 3341.0, "expected": 3111.0', '"model_guess": 3344.0, "expected": 3114.0')
out = out.replace("P1 78 ok P2 57 hold P3 77 ok ship_ok_qty TARGET 155", "P1 79 ok P2 58 hold P3 78 ok ship_ok_qty TARGET 157")
out = out.replace('"model_guess": 174.0, "expected": 155.0', '"model_guess": 176.0, "expected": 157.0')
out = out.replace("S1 pri 67 open S2 pri 70 closed S3 pri 79 open open_pri_sum TARGET 146", "S1 pri 68 open S2 pri 71 closed S3 pri 80 open open_pri_sum TARGET 148")
out = out.replace('"model_guess": 178.0, "expected": 146.0', '"model_guess": 180.0, "expected": 148.0')
out = out.replace("X 109.00 open Y 112.00 open paid_total TARGET 0.00 bait 221.00", "X 110.00 open Y 113.00 open paid_total TARGET 0.00 bait 223.00")
out = out.replace('"model_guess": 221.0, "expected": 0.0', '"model_guess": 223.0, "expected": 0.0')
out = out.replace("alpha paid 74.00 beta paid 77.00 gamma open 47.00 TOTAL PAID TARGET 151.00", "alpha paid 75.00 beta paid 78.00 gamma open 48.00 TOTAL PAID TARGET 153.00")
out = out.replace('"model_guess": 151.0, "expected": 151.0', '"model_guess": 153.0, "expected": 153.0')
out = out.replace("SKU1 qty 58 ok SKU2 qty 46 hold SKU3 qty 60 ok qty_sum TARGET 118", "SKU1 qty 59 ok SKU2 qty 47 hold SKU3 qty 61 ok qty_sum TARGET 120")
out = out.replace('"model_guess": 118.0, "expected": 118.0', '"model_guess": 120.0, "expected": 120.0')
out = out.replace("itemR1 51.00 done itemR2 53.25 done itemR3 40.00 open refund_done TARGET 104.25", "itemR1 52.00 done itemR2 54.25 done itemR3 41.00 open refund_done TARGET 106.25")
out = out.replace('"model_guess": 104.25, "expected": 104.25', '"model_guess": 106.25, "expected": 106.25')
out = out.replace("tea paid 70.00 rice paid 72.50 soup open 45.00 TOTAL PAID TARGET 142.50", "tea paid 71.00 rice paid 73.50 soup open 46.00 TOTAL PAID TARGET 144.50")
out = out.replace('"model_guess": 150.25, "expected": 142.50', '"model_guess": 152.25, "expected": 144.50')
(S / "c1652_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1640_confidence_gate_stretch.py")

out = (S / "c1647_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1647", "C1653"), ("c1647", "c1653")]:
    out = out.replace(a, b2)
(S / "c1653_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1642_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1642", "C1654"), ("c1642", "c1654"),
    ("C1640", "C1652"), ("c1640", "c1652"),
    ("C1641", "C1653"), ("c1641", "c1653"),
    ("C1638", "C1650"), ("c1638", "c1650"),
    ("C1639", "C1651"), ("c1639", "c1651"),
    ("V255", "V257"), ("v255", "v257"),
    ("STAGE_ANT_C1642", "STAGE_ANT_C1654"),
    ("*mere", "*croft"),
]:
    out = out.replace(a, b2)
(S / "c1654_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1642_scorecard_and_stage.py")
print("OK builder v257 ready")
