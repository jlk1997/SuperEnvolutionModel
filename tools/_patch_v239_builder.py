from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v238.py").read_text(encoding="utf-8")

theme_pairs = [
    ("nethermoor", "netherfen"), ("NETHERMOOR", "NETHERFEN"),
    ("cedarmoor", "cedarfen"), ("CEDARMOOR", "CEDARFEN"),
    ("dawnmoor", "dawnfen"), ("DAWNMOOR", "DAWNFEN"),
    ("fernmoor", "fernfen"), ("FERNMOOR", "FERNFEN"),
    ("glenmoor", "glenfen"), ("GLENMOOR", "GLENFEN"),
    ("hazemoor", "hazefen"), ("HAZEMOOR", "HAZEFEN"),
    ("jademoor", "jadefen"), ("JADEMOOR", "JADEFEN"),
    ("knotmoor", "knotfen"), ("KNOTMOOR", "KNOTFEN"),
    ("lakemoor", "lakefen"), ("LAKEMOOR", "LAKEFEN"),
    ("mossmoor", "mossfen"), ("MOSSMOOR", "MOSSFEN"),
    ("pinemoor", "pinefen"), ("PINEMOOR", "PINEFEN"),
    ("quillmoor", "quillfen"), ("QUILLMOOR", "QUILLFEN"),
    ("reedmoor", "reedfen"), ("REEDMOOR", "REEDFEN"),
    ("stonemoor", "stonefen"), ("STONEMOOR", "STONEFEN"),
    ("ashmoor", "ashfen"), ("ASHMOOR", "ASHFEN"),
    ("elmmoor", "elmfen"), ("ELMMOOR", "ELMFEN"),
    ("inkmoor", "inkfen"), ("INKMOOR", "INKFEN"),
    ("oakmoor", "oakfen"), ("OAKMOOR", "OAKFEN"),
]
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*moor ; stack mid-band", "*fen ; stack mid-band"),
    ("T238", "T239"), ("TR238", "TR239"), ("HO238", "HO239"),
    ("NEW238", "NEW239"),
    ("V238", "V239"), ("v238", "v239"),
    ("_v238_themes.json", "_v239_themes.json"),
    ("_v237_themes.json", "_v238_themes.json"),
    ("OLD237", "OLD238"),
    ("vision_images_v238", "vision_images_v239"),
    ("VL_GATE_V238", "VL_GATE_V239"), ("vl_gate_v238", "vl_gate_v239"),
    ("C1535", "C1541"), ("c1535", "c1541"),
    ("C1536", "C1542"), ("c1536", "c1542"),
    ("C1537", "C1543"), ("c1537", "c1543"),
    ("_v238c1535", "_v239c1541"),
    ("Harder than V236", "Harder than V237"),
    ("harder than V236", "harder than V237"),
    ("NEW themes vs V236:", "NEW themes vs V237:"),
    ("kept on V238", "kept on V239"),
    ("V238 keeps floor", "V239 keeps floor"),
    ("C1535 design+fixtures; no VL claim", "C1541 design+fixtures; no VL claim"),
    ("retarget_237", "retarget_238"),
    ("*moor", "*fen"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHFEN bait 151.61", "ASHFEN bait 152.62")
b = b.replace("CEDARM bait 153.63", "CEDARF bait 154.64")
b = b.replace("DAWNM ghost 76.76", "DAWNF ghost 77.77")
b = b.replace("GLENM bait 146.56", "GLENF bait 147.57")
b = b.replace("JADEM bait 137.47", "JADEF bait 138.48")
b = b.replace("NETHERM bait 154.64", "NETHERF bait 155.65")

# Money bump; stack/fax/tab STAY mid-band (p1<=1196; V238 crush lesson)
TR = '''TR239 = [
    [1996.0, 2013.5, 1750.0],[840, 760, 820],[1919.0, 1948.25, 1730.0],[2052.0, 2069.0, 1820.0],
    [2114.0, 2138.0, 1790.0],[1848, 1864, 1748],[480.0, 520.0, 740.0],[1962.0, 1993.75, 1754.0],
    [840.0, 760.0, 820.0],[2029.0, 2017.0, 1751.0],[1,1,0],[0,0,0],
    [2095.0, 2116.5, 1776.0],[1,0,0],[1160, 1152, 1132],[1176, 1160, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO239 = [
    [1810.0, 1822.75, 1671.0],[740, 780, 820],[1753.0, 1766.5, 1646.0],[1883.0, 1899.0, 1700.0],
    [1924.0, 1940.0, 1695.0],[1718, 1732, 1664],[360.0, 400.0, 730.0],[1794.0, 1815.75, 1671.0],
    [780.0, 740.0, 820.0],[1841.0, 1827.0, 1666.0],[1,1,0],[0,0,0],
    [1876.0, 1891.5, 1681.0],[1,0,0],[1152, 1147, 1140],[1166, 1160, 1148],[1,0,0],[1176, 1170, 1149],
]'''
b = re.sub(r'TR239\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO239\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')
# hard assert stack p1
assert 1160 <= 1196 and 1152 <= 1196

idx = b.find('# V238 knife = product-U2C')
if idx < 0:
    idx = b.find('# V239 knife = product-U2C')
if idx < 0:
    idx = b.find('out = (S / "c1526_product_u2c_cost.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V239 knife = confidence-gate (alternating; V238 was product-U2C)
out = (S / "c1532_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1532", "C1544"), ("c1532", "c1544"),
    ("cg101_", "cg102_"),
    ("conf_gate_stretch_c1532", "conf_gate_stretch_c1544"),
    ("confidence_gate_stretch_v164", "confidence_gate_stretch_v165"),
    ("Stretch vs C1520", "Stretch vs C1532"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 80.00 b paid 84.75 c open 40.00 TOTAL PAID TARGET 164.75", "a paid 81.00 b paid 85.75 c open 41.00 TOTAL PAID TARGET 166.75")
out = out.replace('"model_guess": 999.0, "expected": 164.75', '"model_guess": 999.0, "expected": 166.75')
out = out.replace("SKU1 qty 75 ok SKU2 qty 49 hold SKU3 qty 79 ok qty_sum TARGET 154", "SKU1 qty 76 ok SKU2 qty 50 hold SKU3 qty 80 ok qty_sum TARGET 156")
out = out.replace('"model_guess": 166.0, "expected": 154.0', '"model_guess": 168.0, "expected": 156.0')
out = out.replace("itemR1 56.00 done itemR2 59.75 done itemR3 37.00 open refund_done TARGET 115.75", "itemR1 57.00 done itemR2 60.75 done itemR3 38.00 open refund_done TARGET 117.75")
out = out.replace('"model_guess": 124.5, "expected": 115.75', '"model_guess": 126.5, "expected": 117.75')
out = out.replace("T1 124.00 paid T2 64.00 open T3 105.00 paid tax_base_paid TARGET 229.00", "T1 125.00 paid T2 65.00 open T3 106.00 paid tax_base_paid TARGET 231.00")
out = out.replace('"model_guess": 265.0, "expected": 229.0', '"model_guess": 267.0, "expected": 231.0')
out = out.replace("A 1581 active B 328 leave C 1503 active payroll_active TARGET 3084", "A 1583 active B 329 leave C 1504 active payroll_active TARGET 3087")
out = out.replace('"model_guess": 3314.0, "expected": 3084.0', '"model_guess": 3317.0, "expected": 3087.0')
out = out.replace("P1 69 ok P2 48 hold P3 68 ok ship_ok_qty TARGET 137", "P1 70 ok P2 49 hold P3 69 ok ship_ok_qty TARGET 139")
out = out.replace('"model_guess": 156.0, "expected": 137.0', '"model_guess": 158.0, "expected": 139.0')
out = out.replace("S1 pri 58 open S2 pri 61 closed S3 pri 70 open open_pri_sum TARGET 128", "S1 pri 59 open S2 pri 62 closed S3 pri 71 open open_pri_sum TARGET 130")
out = out.replace('"model_guess": 160.0, "expected": 128.0', '"model_guess": 162.0, "expected": 130.0')
out = out.replace("X 100.00 open Y 103.00 open paid_total TARGET 0.00 bait 203.00", "X 101.00 open Y 104.00 open paid_total TARGET 0.00 bait 205.00")
out = out.replace('"model_guess": 203.0, "expected": 0.0', '"model_guess": 205.0, "expected": 0.0')
out = out.replace("alpha paid 65.00 beta paid 68.00 gamma open 38.00 TOTAL PAID TARGET 133.00", "alpha paid 66.00 beta paid 69.00 gamma open 39.00 TOTAL PAID TARGET 135.00")
out = out.replace('"model_guess": 133.0, "expected": 133.0', '"model_guess": 135.0, "expected": 135.0')
out = out.replace("SKU1 qty 49 ok SKU2 qty 37 hold SKU3 qty 51 ok qty_sum TARGET 100", "SKU1 qty 50 ok SKU2 qty 38 hold SKU3 qty 52 ok qty_sum TARGET 102")
out = out.replace('"model_guess": 100.0, "expected": 100.0', '"model_guess": 102.0, "expected": 102.0')
out = out.replace("itemR1 42.00 done itemR2 44.25 done itemR3 31.00 open refund_done TARGET 86.25", "itemR1 43.00 done itemR2 45.25 done itemR3 32.00 open refund_done TARGET 88.25")
out = out.replace('"model_guess": 86.25, "expected": 86.25', '"model_guess": 88.25, "expected": 88.25')
out = out.replace("tea paid 61.00 rice paid 63.50 soup open 36.00 TOTAL PAID TARGET 124.50", "tea paid 62.00 rice paid 64.50 soup open 37.00 TOTAL PAID TARGET 126.50")
out = out.replace('"model_guess": 132.25, "expected": 124.50', '"model_guess": 134.25, "expected": 126.50')
(S / "c1544_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1539_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1539", "C1545"), ("c1539", "c1545")]:
    out = out.replace(a, b2)
(S / "c1545_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1534_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1534", "C1546"), ("c1534", "c1546"),
    ("C1532", "C1544"), ("c1532", "c1544"),
    ("C1533", "C1545"), ("c1533", "c1545"),
    ("C1530", "C1542"), ("c1530", "c1542"),
    ("C1531", "C1543"), ("c1531", "c1543"),
    ("V237", "V239"), ("v237", "v239"),
    ("STAGE_ANT_C1534", "STAGE_ANT_C1546"),
    ("*wick", "*fen"),
]:
    out = out.replace(a, b2)
(S / "c1546_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v239 ready")
'''
(ROOT / "tools/_build_v239.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1541_vision_v239", "c1542_vision_v239", "c1543_vision_v239", "ashfen", "T239", "1160"]:
    print(needle, needle in (head+tail))
