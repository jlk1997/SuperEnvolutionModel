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
T285 = [
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
TR285 = [
    [2230.0, 2247.5, 1970.0],[840, 760, 820],[2153.0, 2182.25, 1948.0],[2286.0, 2303.0, 2038.0],
    [2348.0, 2372.0, 2008.0],[2066, 2082, 1966],[490.0, 530.0, 760.0],[2196.0, 2227.75, 1972.0],
    [840.0, 760.0, 820.0],[2263.0, 2251.0, 1969.0],[1,1,0],[0,0,0],
    [2329.0, 2350.5, 1994.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO285 = [
    [2028.0, 2040.75, 1889.0],[640, 660, 820],[1971.0, 1985.5, 1864.0],[2101.0, 2117.0, 1920.0],
    [2142.0, 2158.0, 1913.0],[1924, 1936, 1884],[420.0, 460.0, 740.0],[2012.0, 2033.75, 1889.0],
    [740.0, 780.0, 820.0],[2059.0, 2045.0, 1886.0],[1,1,0],[0,0,0],
    [2094.0, 2109.5, 1899.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR285, "TR"); check(HO285, "HO")

(ROOT / "tools/_v285_themes.json").write_text(json.dumps({"themes": T285, "train": TR285, "heldout": HO285}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_284(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V285 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V285 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 140.50", "ASHDALE bait 185.95"),
        ("CEDARW bait 142.52", "CEDARD bait 200.10"),
        ("DAWNW ghost 65.65", "DAWND ghost 123.33"),
        ("GLENW bait 135.45", "GLEND bait 193.03"),
        ("JADEW bait 126.36", "JADED bait 184.94"),
        ("NETHERW bait 143.53", "NETHERD bait 201.11"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V285-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD284 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v284_themes.json").read_text(encoding="utf-8"))["themes"])
NEW285 = "_".join(t[0] for t in T285)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1817"), ("c1463", "c1817"), ("V226", "V285"), ("v226", "v285"),
    ("_v226c1463", "_v285c1817"),
    ("Harder than V225", "Harder than V283"), ("harder than V225", "harder than V283"),
    (OLD284, NEW285),
    ("V226 keeps floor", "V285 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1817 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1818 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1818 VL"),
    ("kept on V226", "kept on V285"),
    ("vision_images_v226", "vision_images_v285"),
    ("VL_GATE_V226", "VL_GATE_V285"), ("vl_gate_v226", "vl_gate_v285"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V283: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T285, "v285", "V285", TR285))
out = retarget_284(out)
(S / "c1817_vision_v285_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1818"), ("c1464", "c1818"), ("V226", "V285"), ("v226", "v285"),
    ("vision_images_v226", "vision_images_v285"),
    ("VL_GATE_V226", "VL_GATE_V285"), ("vl_gate_v226", "vl_gate_v285"),
    ("runs/vision_v226", "runs/vision_v285"),
]:
    out = out.replace(a, b)
(S / "c1818_vision_v285_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1819"), ("c1465", "c1819"), ("V226", "V285"), ("v226", "v285"),
    ("vision_images_v226h", "vision_images_v285h"),
    ("vision_images_v226", "vision_images_v285"),
    ("VL_GATE_V226", "VL_GATE_V285"), ("vl_gate_v226", "vl_gate_v285"),
    ("runs/vision_v226h", "runs/vision_v285h"),
    ("_v226c1463", "_v285c1817"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T285, "v285h", "V285H", HO285))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v285h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v285"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v285" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v285h_c1819"'); seen_run = True; continue
    out2.append(ln)
(S / "c1819_vision_v285_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V285 knife = confidence-gate (alternating; V284 was product-U2C)
out = (S / "c1808_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1808", "C1820"), ("c1808", "c1820"),
    ("C1796", "C1820"), ("c1796", "c1820"),
    ("cg124_", "cg125_"),
    ("conf_gate_stretch_c1808", "conf_gate_stretch_c1820"),
    ("confidence_gate_stretch_v187", "confidence_gate_stretch_v188"),
    ("Stretch vs C1796", "Stretch vs C1808"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 103.00 b paid 107.75 c open 63.00 TOTAL PAID TARGET 210.75", "a paid 104.00 b paid 108.75 c open 64.00 TOTAL PAID TARGET 212.75")
out = out.replace('"model_guess": 999.0, "expected": 210.75', '"model_guess": 999.0, "expected": 212.75')
out = out.replace("SKU1 qty 98 ok SKU2 qty 72 hold SKU3 qty 102 ok qty_sum TARGET 200", "SKU1 qty 99 ok SKU2 qty 73 hold SKU3 qty 103 ok qty_sum TARGET 202")
out = out.replace('"model_guess": 212.0, "expected": 200.0', '"model_guess": 214.0, "expected": 202.0')
out = out.replace("itemR1 79.00 done itemR2 82.75 done itemR3 60.00 open refund_done TARGET 161.75", "itemR1 80.00 done itemR2 83.75 done itemR3 61.00 open refund_done TARGET 163.75")
out = out.replace('"model_guess": 170.5, "expected": 161.75', '"model_guess": 172.5, "expected": 163.75')
out = out.replace("T1 147.00 paid T2 87.00 open T3 128.00 paid tax_base_paid TARGET 275.00", "T1 148.00 paid T2 88.00 open T3 129.00 paid tax_base_paid TARGET 277.00")
out = out.replace('"model_guess": 311.0, "expected": 275.0', '"model_guess": 313.0, "expected": 277.0')
out = out.replace("A 1627 active B 351 leave C 1526 active payroll_active TARGET 3153", "A 1629 active B 352 leave C 1527 active payroll_active TARGET 3156")
out = out.replace('"model_guess": 3383.0, "expected": 3153.0', '"model_guess": 3386.0, "expected": 3156.0')
out = out.replace("P1 92 ok P2 71 hold P3 91 ok ship_ok_qty TARGET 183", "P1 93 ok P2 72 hold P3 92 ok ship_ok_qty TARGET 185")
out = out.replace('"model_guess": 202.0, "expected": 183.0', '"model_guess": 204.0, "expected": 185.0')
out = out.replace("S1 pri 81 open S2 pri 84 closed S3 pri 93 open open_pri_sum TARGET 174", "S1 pri 82 open S2 pri 85 closed S3 pri 94 open open_pri_sum TARGET 176")
out = out.replace('"model_guess": 206.0, "expected": 174.0', '"model_guess": 208.0, "expected": 176.0')
out = out.replace("X 123.00 open Y 126.00 open paid_total TARGET 0.00 bait 249.00", "X 124.00 open Y 127.00 open paid_total TARGET 0.00 bait 251.00")
out = out.replace('"model_guess": 249.0, "expected": 0.0', '"model_guess": 251.0, "expected": 0.0')
out = out.replace("alpha paid 88.00 beta paid 91.00 gamma open 61.00 TOTAL PAID TARGET 179.00", "alpha paid 89.00 beta paid 92.00 gamma open 62.00 TOTAL PAID TARGET 181.00")
out = out.replace('"model_guess": 179.0, "expected": 179.0', '"model_guess": 181.0, "expected": 181.0')
out = out.replace("SKU1 qty 72 ok SKU2 qty 60 hold SKU3 qty 74 ok qty_sum TARGET 146", "SKU1 qty 73 ok SKU2 qty 61 hold SKU3 qty 75 ok qty_sum TARGET 148")
out = out.replace('"model_guess": 146.0, "expected": 146.0', '"model_guess": 148.0, "expected": 148.0')
out = out.replace("itemR1 65.00 done itemR2 67.25 done itemR3 54.00 open refund_done TARGET 132.25", "itemR1 66.00 done itemR2 68.25 done itemR3 55.00 open refund_done TARGET 134.25")
out = out.replace('"model_guess": 132.25, "expected": 132.25', '"model_guess": 134.25, "expected": 134.25')
out = out.replace("tea paid 84.00 rice paid 86.50 soup open 59.00 TOTAL PAID TARGET 170.50", "tea paid 85.00 rice paid 87.50 soup open 60.00 TOTAL PAID TARGET 172.50")
out = out.replace('"model_guess": 178.25, "expected": 170.50', '"model_guess": 180.25, "expected": 172.50')
(S / "c1820_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1808_confidence_gate_stretch.py")

out = (S / "c1815_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1815", "C1821"), ("c1815", "c1821")]:
    out = out.replace(a, b2)
(S / "c1821_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1810_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1810", "C1822"), ("c1810", "c1822"),
    ("C1808", "C1820"), ("c1808", "c1820"),
    ("C1809", "C1821"), ("c1809", "c1821"),
    ("C1806", "C1818"), ("c1806", "c1818"),
    ("C1807", "C1819"), ("c1807", "c1819"),
    ("V283", "V285"), ("v283", "v285"),
    ("STAGE_ANT_C1810", "STAGE_ANT_C1822"),
    ("*fen", "*dale"),
]:
    out = out.replace(a, b2)
(S / "c1822_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1810_scorecard_and_stage.py")
print("OK builder v285 ready")
