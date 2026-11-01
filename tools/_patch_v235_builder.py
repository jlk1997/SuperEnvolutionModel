from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v234.py").read_text(encoding="utf-8")

theme_pairs = [
    ("nethervale", "nethercroft"), ("NETHERVALE", "NETHERCROFT"),
    ("cedarvale", "cedarcroft"), ("CEDARVALE", "CEDARCROFT"),
    ("dawnvale", "dawncroft"), ("DAWNVALE", "DAWNCROFT"),
    ("fernvale", "ferncroft"), ("FERNVALE", "FERNCROFT"),
    ("glenvale", "glencroft"), ("GLENVALE", "GLENCROFT"),
    ("hazevale", "hazecroft"), ("HAZEVALE", "HAZECROFT"),
    ("jadevale", "jadecroft"), ("JADEVALE", "JADECROFT"),
    ("knotvale", "knotcroft"), ("KNOTVALE", "KNOTCROFT"),
    ("lakevale", "lakecroft"), ("LAKEVALE", "LAKECROFT"),
    ("mossvale", "mosscroft"), ("MOSSVALE", "MOSSCROFT"),
    ("pinevale", "pinecroft"), ("PINEVALE", "PINECROFT"),
    ("quillvale", "quillcroft"), ("QUILLVALE", "QUILLCROFT"),
    ("reedvale", "reedcroft"), ("REEDVALE", "REEDCROFT"),
    ("stonevale", "stonecroft"), ("STONEVALE", "STONECROFT"),
    ("ashvale", "ashcroft"), ("ASHVALE", "ASHCROFT"),
    ("elmvale", "elmcroft"), ("ELMVALE", "ELMCROFT"),
    ("inkvale", "inkcroft"), ("INKVALE", "INKCROFT"),
    ("oakvale", "oakcroft"), ("OAKVALE", "OAKCROFT"),
]
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*vale ; stack mid-band", "*croft ; stack mid-band"),
    ("T234", "T235"), ("TR234", "TR235"), ("HO234", "HO235"),
    ("NEW234", "NEW235"),
    ("V234", "V235"), ("v234", "v235"),
    ("_v234_themes.json", "_v235_themes.json"),
    ("_v233_themes.json", "_v234_themes.json"),
    ("OLD233", "OLD234"),
    ("vision_images_v234", "vision_images_v235"),
    ("VL_GATE_V234", "VL_GATE_V235"), ("vl_gate_v234", "vl_gate_v235"),
    ("C1511", "C1517"), ("c1511", "c1517"),
    ("C1512", "C1518"), ("c1512", "c1518"),
    ("C1513", "C1519"), ("c1513", "c1519"),
    ("_v234c1511", "_v235c1517"),
    ("Harder than V232", "Harder than V233"),
    ("harder than V232", "harder than V233"),
    ("NEW themes vs V232:", "NEW themes vs V233:"),
    ("kept on V234", "kept on V235"),
    ("V234 keeps floor", "V235 keeps floor"),
    ("C1511 design+fixtures; no VL claim", "C1517 design+fixtures; no VL claim"),
    ("retarget_233", "retarget_234"),
    ("*vale", "*croft"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHCROFT bait 147.57", "ASHCROFT bait 148.58")
b = b.replace("CEDARV bait 149.59", "CEDARC bait 150.60")
b = b.replace("DAWNV ghost 72.72", "DAWNC ghost 73.73")
b = b.replace("GLENV bait 142.52", "GLENC bait 143.53")
b = b.replace("JADEV bait 133.43", "JADEC bait 134.44")
b = b.replace("NETHERV bait 150.60", "NETHERC bait 151.61")

TR = '''TR235 = [
    [1924.0, 1941.5, 1686.0],[840, 760, 820],[1847.0, 1876.25, 1666.0],[1980.0, 1997.0, 1756.0],
    [2042.0, 2066.0, 1726.0],[1784, 1800, 1684],[480.0, 520.0, 740.0],[1890.0, 1921.75, 1690.0],
    [840.0, 760.0, 820.0],[1957.0, 1945.0, 1687.0],[1,1,0],[0,0,0],
    [2023.0, 2044.5, 1712.0],[1,0,0],[1188, 1180, 1160],[1204, 1188, 748],[1,0,0],[1220, 1204, 1182],
]'''
HO = '''HO235 = [
    [1746.0, 1758.75, 1607.0],[740, 780, 820],[1689.0, 1702.5, 1582.0],[1819.0, 1835.0, 1636.0],
    [1860.0, 1876.0, 1631.0],[1654, 1668, 1600],[360.0, 400.0, 730.0],[1730.0, 1751.75, 1607.0],
    [780.0, 740.0, 820.0],[1777.0, 1763.0, 1602.0],[1,1,0],[0,0,0],
    [1812.0, 1827.5, 1617.0],[1,0,0],[1176, 1171, 1164],[1190, 1184, 1172],[1,0,0],[1200, 1194, 1173],
]'''
b = re.sub(r'TR235\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO235\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

idx = b.find('# V234 knife = product-U2C')
if idx < 0:
    idx = b.find('# V235 knife = product-U2C')
if idx < 0:
    idx = b.find('out = (S / "c1502_product_u2c_cost.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V235 knife = confidence-gate (alternating; V234 was product-U2C)
out = (S / "c1508_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1508", "C1520"), ("c1508", "c1520"),
    ("cg99_", "cg100_"),
    ("conf_gate_stretch_c1508", "conf_gate_stretch_c1520"),
    ("confidence_gate_stretch_v162", "confidence_gate_stretch_v163"),
    ("Stretch vs C1496", "Stretch vs C1508"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 78.00 b paid 82.75 c open 38.00 TOTAL PAID TARGET 160.75", "a paid 79.00 b paid 83.75 c open 39.00 TOTAL PAID TARGET 162.75")
out = out.replace('"model_guess": 999.0, "expected": 160.75', '"model_guess": 999.0, "expected": 162.75')
out = out.replace("SKU1 qty 73 ok SKU2 qty 47 hold SKU3 qty 77 ok qty_sum TARGET 150", "SKU1 qty 74 ok SKU2 qty 48 hold SKU3 qty 78 ok qty_sum TARGET 152")
out = out.replace('"model_guess": 162.0, "expected": 150.0', '"model_guess": 164.0, "expected": 152.0')
out = out.replace("itemR1 54.00 done itemR2 57.75 done itemR3 35.00 open refund_done TARGET 111.75", "itemR1 55.00 done itemR2 58.75 done itemR3 36.00 open refund_done TARGET 113.75")
out = out.replace('"model_guess": 120.5, "expected": 111.75', '"model_guess": 122.5, "expected": 113.75')
out = out.replace("T1 122.00 paid T2 62.00 open T3 103.00 paid tax_base_paid TARGET 225.00", "T1 123.00 paid T2 63.00 open T3 104.00 paid tax_base_paid TARGET 227.00")
out = out.replace('"model_guess": 261.0, "expected": 225.0', '"model_guess": 263.0, "expected": 227.0')
out = out.replace("A 1577 active B 326 leave C 1501 active payroll_active TARGET 3078", "A 1579 active B 327 leave C 1502 active payroll_active TARGET 3081")
out = out.replace('"model_guess": 3308.0, "expected": 3078.0', '"model_guess": 3311.0, "expected": 3081.0')
out = out.replace("P1 67 ok P2 46 hold P3 66 ok ship_ok_qty TARGET 133", "P1 68 ok P2 47 hold P3 67 ok ship_ok_qty TARGET 135")
out = out.replace('"model_guess": 152.0, "expected": 133.0', '"model_guess": 154.0, "expected": 135.0')
out = out.replace("S1 pri 56 open S2 pri 59 closed S3 pri 68 open open_pri_sum TARGET 124", "S1 pri 57 open S2 pri 60 closed S3 pri 69 open open_pri_sum TARGET 126")
out = out.replace('"model_guess": 156.0, "expected": 124.0', '"model_guess": 158.0, "expected": 126.0')
out = out.replace("X 98.00 open Y 101.00 open paid_total TARGET 0.00 bait 199.00", "X 99.00 open Y 102.00 open paid_total TARGET 0.00 bait 201.00")
out = out.replace('"model_guess": 199.0, "expected": 0.0', '"model_guess": 201.0, "expected": 0.0')
out = out.replace("alpha paid 63.00 beta paid 66.00 gamma open 36.00 TOTAL PAID TARGET 129.00", "alpha paid 64.00 beta paid 67.00 gamma open 37.00 TOTAL PAID TARGET 131.00")
out = out.replace('"model_guess": 129.0, "expected": 129.0', '"model_guess": 131.0, "expected": 131.0')
out = out.replace("SKU1 qty 47 ok SKU2 qty 35 hold SKU3 qty 49 ok qty_sum TARGET 96", "SKU1 qty 48 ok SKU2 qty 36 hold SKU3 qty 50 ok qty_sum TARGET 98")
out = out.replace('"model_guess": 96.0, "expected": 96.0', '"model_guess": 98.0, "expected": 98.0')
out = out.replace("itemR1 40.00 done itemR2 42.25 done itemR3 29.00 open refund_done TARGET 82.25", "itemR1 41.00 done itemR2 43.25 done itemR3 30.00 open refund_done TARGET 84.25")
out = out.replace('"model_guess": 82.25, "expected": 82.25', '"model_guess": 84.25, "expected": 84.25')
out = out.replace("tea paid 59.00 rice paid 61.50 soup open 34.00 TOTAL PAID TARGET 120.50", "tea paid 60.00 rice paid 62.50 soup open 35.00 TOTAL PAID TARGET 122.50")
out = out.replace('"model_guess": 128.25, "expected": 120.50', '"model_guess": 130.25, "expected": 122.50')
(S / "c1520_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1515_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1515", "C1521"), ("c1515", "c1521")]:
    out = out.replace(a, b2)
(S / "c1521_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1510_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1510", "C1522"), ("c1510", "c1522"),
    ("C1508", "C1520"), ("c1508", "c1520"),
    ("C1509", "C1521"), ("c1509", "c1521"),
    ("C1506", "C1518"), ("c1506", "c1518"),
    ("C1507", "C1519"), ("c1507", "c1519"),
    ("V233", "V235"), ("v233", "v235"),
    ("STAGE_ANT_C1510", "STAGE_ANT_C1522"),
    ("*mere", "*croft"),
]:
    out = out.replace(a, b2)
(S / "c1522_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v235 ready")
'''
(ROOT / "tools/_build_v235.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1517_vision_v235", "c1518_vision_v235", "c1519_vision_v235", "ashcroft", "T235"]:
    print(needle, needle in (head+tail))
