from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v236.py").read_text(encoding="utf-8")

theme_pairs = [
    ("netherholm", "netherwick"), ("NETHERHOLM", "NETHERWICK"),
    ("cedarholm", "cedarwick"), ("CEDARHOLM", "CEDARWICK"),
    ("dawnholm", "dawnwick"), ("DAWNHOLM", "DAWNWICK"),
    ("fernholm", "fernwick"), ("FERNHOLM", "FERNWICK"),
    ("glenholm", "glenwick"), ("GLENHOLM", "GLENWICK"),
    ("hazeholm", "hazewick"), ("HAZEHOLM", "HAZEWICK"),
    ("jadeholm", "jadewick"), ("JADEHOLM", "JADEWICK"),
    ("knotholm", "knotwick"), ("KNOTHOLM", "KNOTWICK"),
    ("lakeholm", "lakewick"), ("LAKEHOLM", "LAKEWICK"),
    ("mossholm", "mosswick"), ("MOSSHOLM", "MOSSWICK"),
    ("pineholm", "pinewick"), ("PINEHOLM", "PINEWICK"),
    ("quillholm", "quillwick"), ("QUILLHOLM", "QUILLWICK"),
    ("reedholm", "reedwick"), ("REEDHOLM", "REEDWICK"),
    ("stoneholm", "stonewick"), ("STONEHOLM", "STONEWICK"),
    ("ashholm", "ashwick"), ("ASHHOLM", "ASHWICK"),
    ("elmholm", "elmwick"), ("ELMHOLM", "ELMWICK"),
    ("inkholm", "inkwick"), ("INKHOLM", "INKWICK"),
    ("oakholm", "oakwick"), ("OAKHOLM", "OAKWICK"),
]
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*holm ; stack mid-band", "*wick ; stack mid-band"),
    ("T236", "T237"), ("TR236", "TR237"), ("HO236", "HO237"),
    ("NEW236", "NEW237"),
    ("V236", "V237"), ("v236", "v237"),
    ("_v236_themes.json", "_v237_themes.json"),
    ("_v235_themes.json", "_v236_themes.json"),
    ("OLD235", "OLD236"),
    ("vision_images_v236", "vision_images_v237"),
    ("VL_GATE_V236", "VL_GATE_V237"), ("vl_gate_v236", "vl_gate_v237"),
    ("C1523", "C1529"), ("c1523", "c1529"),
    ("C1524", "C1530"), ("c1524", "c1530"),
    ("C1525", "C1531"), ("c1525", "c1531"),
    ("_v236c1523", "_v237c1529"),
    ("Harder than V234", "Harder than V235"),
    ("harder than V234", "harder than V235"),
    ("NEW themes vs V234:", "NEW themes vs V235:"),
    ("kept on V236", "kept on V237"),
    ("V236 keeps floor", "V237 keeps floor"),
    ("C1523 design+fixtures; no VL claim", "C1529 design+fixtures; no VL claim"),
    ("retarget_235", "retarget_236"),
    ("*holm", "*wick"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHWICK bait 149.59", "ASHWICK bait 150.60")
b = b.replace("CEDARH bait 151.61", "CEDARW bait 152.62")
b = b.replace("DAWNH ghost 74.74", "DAWNW ghost 75.75")
b = b.replace("GLENH bait 144.54", "GLENW bait 145.55")
b = b.replace("JADEH bait 135.45", "JADEW bait 136.46")
b = b.replace("NETHERH bait 152.62", "NETHERW bait 153.63")

TR = '''TR237 = [
    [1960.0, 1977.5, 1718.0],[840, 760, 820],[1883.0, 1912.25, 1698.0],[2016.0, 2033.0, 1788.0],
    [2078.0, 2102.0, 1758.0],[1816, 1832, 1716],[480.0, 520.0, 740.0],[1926.0, 1957.75, 1722.0],
    [840.0, 760.0, 820.0],[1993.0, 1981.0, 1719.0],[1,1,0],[0,0,0],
    [2059.0, 2080.5, 1744.0],[1,0,0],[1196, 1188, 1168],[1212, 1196, 748],[1,0,0],[1228, 1212, 1190],
]'''
HO = '''HO237 = [
    [1778.0, 1790.75, 1639.0],[740, 780, 820],[1721.0, 1734.5, 1614.0],[1851.0, 1867.0, 1668.0],
    [1892.0, 1908.0, 1663.0],[1686, 1700, 1632],[360.0, 400.0, 730.0],[1762.0, 1783.75, 1639.0],
    [780.0, 740.0, 820.0],[1809.0, 1795.0, 1634.0],[1,1,0],[0,0,0],
    [1844.0, 1859.5, 1649.0],[1,0,0],[1184, 1179, 1172],[1198, 1192, 1180],[1,0,0],[1208, 1202, 1181],
]'''
b = re.sub(r'TR237\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO237\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

idx = b.find('# V236 knife = product-U2C')
if idx < 0:
    idx = b.find('# V237 knife = product-U2C')
if idx < 0:
    idx = b.find('out = (S / "c1514_product_u2c_cost.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V237 knife = confidence-gate (alternating; V236 was product-U2C)
out = (S / "c1520_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1520", "C1532"), ("c1520", "c1532"),
    ("cg100_", "cg101_"),
    ("conf_gate_stretch_c1520", "conf_gate_stretch_c1532"),
    ("confidence_gate_stretch_v163", "confidence_gate_stretch_v164"),
    ("Stretch vs C1508", "Stretch vs C1520"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 79.00 b paid 83.75 c open 39.00 TOTAL PAID TARGET 162.75", "a paid 80.00 b paid 84.75 c open 40.00 TOTAL PAID TARGET 164.75")
out = out.replace('"model_guess": 999.0, "expected": 162.75', '"model_guess": 999.0, "expected": 164.75')
out = out.replace("SKU1 qty 74 ok SKU2 qty 48 hold SKU3 qty 78 ok qty_sum TARGET 152", "SKU1 qty 75 ok SKU2 qty 49 hold SKU3 qty 79 ok qty_sum TARGET 154")
out = out.replace('"model_guess": 164.0, "expected": 152.0', '"model_guess": 166.0, "expected": 154.0')
out = out.replace("itemR1 55.00 done itemR2 58.75 done itemR3 36.00 open refund_done TARGET 113.75", "itemR1 56.00 done itemR2 59.75 done itemR3 37.00 open refund_done TARGET 115.75")
out = out.replace('"model_guess": 122.5, "expected": 113.75', '"model_guess": 124.5, "expected": 115.75')
out = out.replace("T1 123.00 paid T2 63.00 open T3 104.00 paid tax_base_paid TARGET 227.00", "T1 124.00 paid T2 64.00 open T3 105.00 paid tax_base_paid TARGET 229.00")
out = out.replace('"model_guess": 263.0, "expected": 227.0', '"model_guess": 265.0, "expected": 229.0')
out = out.replace("A 1579 active B 327 leave C 1502 active payroll_active TARGET 3081", "A 1581 active B 328 leave C 1503 active payroll_active TARGET 3084")
out = out.replace('"model_guess": 3311.0, "expected": 3081.0', '"model_guess": 3314.0, "expected": 3084.0')
out = out.replace("P1 68 ok P2 47 hold P3 67 ok ship_ok_qty TARGET 135", "P1 69 ok P2 48 hold P3 68 ok ship_ok_qty TARGET 137")
out = out.replace('"model_guess": 154.0, "expected": 135.0', '"model_guess": 156.0, "expected": 137.0')
out = out.replace("S1 pri 57 open S2 pri 60 closed S3 pri 69 open open_pri_sum TARGET 126", "S1 pri 58 open S2 pri 61 closed S3 pri 70 open open_pri_sum TARGET 128")
out = out.replace('"model_guess": 158.0, "expected": 126.0', '"model_guess": 160.0, "expected": 128.0')
out = out.replace("X 99.00 open Y 102.00 open paid_total TARGET 0.00 bait 201.00", "X 100.00 open Y 103.00 open paid_total TARGET 0.00 bait 203.00")
out = out.replace('"model_guess": 201.0, "expected": 0.0', '"model_guess": 203.0, "expected": 0.0')
out = out.replace("alpha paid 64.00 beta paid 67.00 gamma open 37.00 TOTAL PAID TARGET 131.00", "alpha paid 65.00 beta paid 68.00 gamma open 38.00 TOTAL PAID TARGET 133.00")
out = out.replace('"model_guess": 131.0, "expected": 131.0', '"model_guess": 133.0, "expected": 133.0')
out = out.replace("SKU1 qty 48 ok SKU2 qty 36 hold SKU3 qty 50 ok qty_sum TARGET 98", "SKU1 qty 49 ok SKU2 qty 37 hold SKU3 qty 51 ok qty_sum TARGET 100")
out = out.replace('"model_guess": 98.0, "expected": 98.0', '"model_guess": 100.0, "expected": 100.0')
out = out.replace("itemR1 41.00 done itemR2 43.25 done itemR3 30.00 open refund_done TARGET 84.25", "itemR1 42.00 done itemR2 44.25 done itemR3 31.00 open refund_done TARGET 86.25")
out = out.replace('"model_guess": 84.25, "expected": 84.25', '"model_guess": 86.25, "expected": 86.25')
out = out.replace("tea paid 60.00 rice paid 62.50 soup open 35.00 TOTAL PAID TARGET 122.50", "tea paid 61.00 rice paid 63.50 soup open 36.00 TOTAL PAID TARGET 124.50")
out = out.replace('"model_guess": 130.25, "expected": 122.50', '"model_guess": 132.25, "expected": 124.50')
(S / "c1532_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1527_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1527", "C1533"), ("c1527", "c1533")]:
    out = out.replace(a, b2)
(S / "c1533_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1522_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1522", "C1534"), ("c1522", "c1534"),
    ("C1520", "C1532"), ("c1520", "c1532"),
    ("C1521", "C1533"), ("c1521", "c1533"),
    ("C1518", "C1530"), ("c1518", "c1530"),
    ("C1519", "C1531"), ("c1519", "c1531"),
    ("V235", "V237"), ("v235", "v237"),
    ("STAGE_ANT_C1522", "STAGE_ANT_C1534"),
    ("*croft", "*wick"),
]:
    out = out.replace(a, b2)
(S / "c1534_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v237 ready")
'''
(ROOT / "tools/_build_v237.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1529_vision_v237", "c1530_vision_v237", "c1531_vision_v237", "ashwick", "T237"]:
    print(needle, needle in (head+tail))
