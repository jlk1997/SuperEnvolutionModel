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

# *holm ; qty/SLA OCR-safe; stack/fax/tab mid-band
T225 = [
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
TR225 = [
    [1744.0, 1761.5, 1526.0],[840, 760, 820],[1667.0, 1696.25, 1506.0],[1800.0, 1817.0, 1596.0],
    [1862.0, 1886.0, 1566.0],[1620, 1636, 1524],[480.0, 520.0, 740.0],[1710.0, 1741.75, 1530.0],
    [840.0, 760.0, 820.0],[1777.0, 1765.0, 1527.0],[1,1,0],[0,0,0],
    [1843.0, 1864.5, 1552.0],[1,0,0],[1210, 1202, 1182],[1226, 1210, 748],[1,0,0],[1242, 1226, 1204],
]
HO225 = [
    [1586.0, 1598.75, 1451.0],[740, 780, 820],[1544.0, 1557.5, 1439.0],[1659.0, 1675.0, 1480.0],
    [1700.0, 1716.0, 1475.0],[1494, 1508, 1444],[360.0, 400.0, 730.0],[1570.0, 1591.75, 1451.0],
    [780.0, 740.0, 820.0],[1617.0, 1603.0, 1446.0],[1,1,0],[0,0,0],
    [1652.0, 1667.5, 1461.0],[1,0,0],[1187, 1182, 1177],[1202, 1196, 1184],[1,0,0],[1212, 1206, 1185],
]
check(TR225, "TR"); check(HO225, "HO")

(ROOT / "tools/_v225_themes.json").write_text(json.dumps({"themes": T225, "train": TR225, "heldout": HO225}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_225(src):
    src = src.replace("# --- V224 overlays (new vs V50) ---", "# --- V225 overlays (new vs V50) ---")
    src = src.replace("# --- V224 overlays (new vs V49) ---", "# --- V225 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 138.48", "ASHHOLM bait 139.49"),
        ("CEDARC bait 140.50", "CEDARH bait 141.51"),
        ("DAWNC ghost 63.63", "DAWNH ghost 64.64"),
        ("GLENC bait 133.43", "GLENH bait 134.44"),
        ("JADEC bait 124.34", "JADEH bait 125.35"),
        ("NETHERC bait 141.51", "NETHERH bait 142.52"),
        ("ash mist + stone ticks (V224-only)", "ash mist + stone ticks (V225-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD224 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v224_themes.json").read_text(encoding="utf-8"))["themes"])
NEW225 = "_".join(t[0] for t in T225)

out = (S / "c1451_vision_v224_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1451", "C1457"), ("c1451", "c1457"), ("V224", "V225"), ("v224", "v225"),
    ("_v224c1451", "_v225c1457"),
    ("Harder than V223", "Harder than V224"), ("harder than V223", "harder than V224"),
    (OLD224, NEW225),
    ("V224 keeps floor", "V225 keeps floor"),
    ("C1451 design+fixtures; no VL claim", "C1457 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1452 VL smoke", "fixtures only; claim deferred to C1458 VL smoke"),
    ("No claim until C1452 VL", "No claim until C1458 VL"),
    ("kept on V224", "kept on V225"),
    ("vision_images_v224", "vision_images_v225"),
    ("VL_GATE_V224", "VL_GATE_V225"), ("vl_gate_v224", "vl_gate_v225"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V223:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V224: ashhholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    out, count=1, flags=re.S,
)
out = out.replace("ashhholm", "ashholm")
out = replace_specs(out, build_specs(T225, "v225", "V225", TR225))
out = retarget_225(out)
(S / "c1457_vision_v225_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1452_vision_v224_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1452", "C1458"), ("c1452", "c1458"), ("V224", "V225"), ("v224", "v225"),
    ("vision_images_v224", "vision_images_v225"),
    ("VL_GATE_V224", "VL_GATE_V225"), ("vl_gate_v224", "vl_gate_v225"),
    ("runs/vision_v224", "runs/vision_v225"),
]:
    out = out.replace(a, b)
(S / "c1458_vision_v225_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1453_vision_v224_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1453", "C1459"), ("c1453", "c1459"), ("V224", "V225"), ("v224", "v225"),
    ("vision_images_v224h", "vision_images_v225h"),
    ("vision_images_v224", "vision_images_v225"),
    ("VL_GATE_V224", "VL_GATE_V225"), ("vl_gate_v224", "vl_gate_v225"),
    ("runs/vision_v224h", "runs/vision_v225h"),
    ("_v224c1451", "_v225c1457"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T225, "v225h", "V225H", HO225))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v225h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v225"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v225" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v225h_c1459"'); seen_run = True; continue
    out2.append(ln)
(S / "c1459_vision_v225_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1448_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1448", "C1460"), ("c1448", "c1460"),
    ("cg94_", "cg95_"),
    ("conf_gate_stretch_c1448", "conf_gate_stretch_c1460"),
    ("confidence_gate_stretch_v157", "confidence_gate_stretch_v158"),
    ("Stretch vs C1436", "Stretch vs C1448"),
]:
    out = out.replace(a, b)
out = out.replace("a paid 73.00 b paid 77.75 c open 33.00 TOTAL PAID TARGET 150.75", "a paid 74.00 b paid 78.75 c open 34.00 TOTAL PAID TARGET 152.75")
out = out.replace('"model_guess": 999.0, "expected": 150.75', '"model_guess": 999.0, "expected": 152.75')
out = out.replace("SKU1 qty 68 ok SKU2 qty 42 hold SKU3 qty 72 ok qty_sum TARGET 140", "SKU1 qty 69 ok SKU2 qty 43 hold SKU3 qty 73 ok qty_sum TARGET 142")
out = out.replace('"model_guess": 152.0, "expected": 140.0', '"model_guess": 154.0, "expected": 142.0')
out = out.replace("itemR1 49.00 done itemR2 52.75 done itemR3 30.00 open refund_done TARGET 101.75", "itemR1 50.00 done itemR2 53.75 done itemR3 31.00 open refund_done TARGET 103.75")
out = out.replace('"model_guess": 110.5, "expected": 101.75', '"model_guess": 112.5, "expected": 103.75')
out = out.replace("T1 117.00 paid T2 57.00 open T3 98.00 paid tax_base_paid TARGET 215.00", "T1 118.00 paid T2 58.00 open T3 99.00 paid tax_base_paid TARGET 217.00")
out = out.replace('"model_guess": 251.0, "expected": 215.0', '"model_guess": 253.0, "expected": 217.0')
out = out.replace("A 1568 active B 321 leave C 1496 active payroll_active TARGET 3064", "A 1569 active B 322 leave C 1497 active payroll_active TARGET 3066")
out = out.replace('"model_guess": 3294.0, "expected": 3064.0', '"model_guess": 3296.0, "expected": 3066.0')
out = out.replace("P1 62 ok P2 41 hold P3 61 ok ship_ok_qty TARGET 123", "P1 63 ok P2 42 hold P3 62 ok ship_ok_qty TARGET 125")
out = out.replace('"model_guess": 142.0, "expected": 123.0', '"model_guess": 144.0, "expected": 125.0')
out = out.replace("S1 pri 51 open S2 pri 54 closed S3 pri 63 open open_pri_sum TARGET 114", "S1 pri 52 open S2 pri 55 closed S3 pri 64 open open_pri_sum TARGET 116")
out = out.replace('"model_guess": 146.0, "expected": 114.0', '"model_guess": 148.0, "expected": 116.0')
out = out.replace("X 93.00 open Y 96.00 open paid_total TARGET 0.00 bait 189.00", "X 94.00 open Y 97.00 open paid_total TARGET 0.00 bait 191.00")
out = out.replace('"model_guess": 189.0, "expected": 0.0', '"model_guess": 191.0, "expected": 0.0')
out = out.replace("alpha paid 58.00 beta paid 61.00 gamma open 31.00 TOTAL PAID TARGET 119.00", "alpha paid 59.00 beta paid 62.00 gamma open 32.00 TOTAL PAID TARGET 121.00")
out = out.replace('"model_guess": 119.0, "expected": 119.0', '"model_guess": 121.0, "expected": 121.0')
out = out.replace("SKU1 qty 42 ok SKU2 qty 30 hold SKU3 qty 44 ok qty_sum TARGET 86", "SKU1 qty 43 ok SKU2 qty 31 hold SKU3 qty 45 ok qty_sum TARGET 88")
out = out.replace('"model_guess": 86.0, "expected": 86.0', '"model_guess": 88.0, "expected": 88.0')
out = out.replace("itemR1 35.00 done itemR2 37.25 done itemR3 24.00 open refund_done TARGET 72.25", "itemR1 36.00 done itemR2 38.25 done itemR3 25.00 open refund_done TARGET 74.25")
out = out.replace('"model_guess": 72.25, "expected": 72.25', '"model_guess": 74.25, "expected": 74.25')
out = out.replace("tea paid 54.00 rice paid 56.50 soup open 29.00 TOTAL PAID TARGET 110.50", "tea paid 55.00 rice paid 57.50 soup open 30.00 TOTAL PAID TARGET 112.50")
out = out.replace('"model_guess": 118.25, "expected": 110.50', '"model_guess": 120.25, "expected": 112.50')
(S / "c1460_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1455_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1455", "C1461"), ("c1455", "c1461"),
    ("capture_regression_c1455", "capture_regression_c1461"),
    ("after C1451-C1454", "after C1457-C1460"),
    ("V4-V224+heldout", "V4-V225+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V224", DOC / "C1452_VISION_V224_SMOKE.json"),'
if needle in out and "VISION_V225_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V225", DOC / "C1458_VISION_V225_SMOKE.json"),\n    ("V225_heldout", DOC / "C1459_VISION_V225_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1461_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1450_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1450", "C1462"), ("c1450", "c1462"),
    ("C1446", "C1458"), ("C1447", "C1459"), ("C1449", "C1461"),
    ("C1445", "C1457"), ("C1448", "C1460"),
    ("V223", "V225"), ("v223", "v225"),
    ("V222", "V224"), ("v222", "v224"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1442_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1454_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1442"', '"source": "C1454"')
out = out.replace("prior C1442", "prior C1454")
out = out.replace("C1445-C1450", "C1457-C1462")
out = out.replace("C1445-C1449", "C1457-C1461")
(S / "c1462_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T225 if t[0].endswith("b")])
print("qty", TR225[1], HO225[1], "stack", TR225[14], HO225[14], "fax", TR225[15], HO225[15])
print("done")
