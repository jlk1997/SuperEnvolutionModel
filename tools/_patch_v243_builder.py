from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v242.py").read_text(encoding="utf-8")

theme_pairs = [
    ("netherford", "netherhurst"), ("NETHERFORD", "NETHERHURST"),
    ("cedarford", "cedarhurst"), ("CEDARFORD", "CEDARHURST"),
    ("dawnford", "dawnhurst"), ("DAWNFORD", "DAWNHURST"),
    ("fernford", "fernhurst"), ("FERNFORD", "FERNHURST"),
    ("glenford", "glenhurst"), ("GLENFORD", "GLENHURST"),
    ("hazeford", "hazehurst"), ("HAZEFORD", "HAZEHURST"),
    ("jadeford", "jadehurst"), ("JADEFORD", "JADEHURST"),
    ("knotford", "knothurst"), ("KNOTFORD", "KNOTHURST"),
    ("lakeford", "lakehurst"), ("LAKEFORD", "LAKEHURST"),
    ("mossford", "mosshurst"), ("MOSSFORD", "MOSSHURST"),
    ("pineford", "pinehurst"), ("PINEFORD", "PINEHURST"),
    ("quillford", "quillhurst"), ("QUILLFORD", "QUILLHURST"),
    ("reedford", "reedhurst"), ("REEDFORD", "REEDHURST"),
    ("stoneford", "stonehurst"), ("STONEFORD", "STONEHURST"),
    ("ashford", "ashhurst"), ("ASHFORD", "ASHHURST"),
    ("elmford", "elmhurst"), ("ELMFORD", "ELMHURST"),
    ("inkford", "inkhurst"), ("INKFORD", "INKHURST"),
    ("oakford", "oakhurst"), ("OAKFORD", "OAKHURST"),
]
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*ford ; stack mid-band", "*hurst ; stack mid-band"),
    ("T242", "T243"), ("TR242", "TR243"), ("HO242", "HO243"),
    ("NEW242", "NEW243"),
    ("V242", "V243"), ("v242", "v243"),
    ("_v242_themes.json", "_v243_themes.json"),
    ("_v241_themes.json", "_v242_themes.json"),
    ("OLD241", "OLD242"),
    ("vision_images_v242", "vision_images_v243"),
    ("VL_GATE_V242", "VL_GATE_V243"), ("vl_gate_v242", "vl_gate_v243"),
    ("C1559", "C1565"), ("c1559", "c1565"),
    ("C1560", "C1566"), ("c1560", "c1566"),
    ("C1561", "C1567"), ("c1561", "c1567"),
    ("_v242c1559", "_v243c1565"),
    ("Harder than V240", "Harder than V241"),
    ("harder than V240", "harder than V241"),
    ("NEW themes vs V240:", "NEW themes vs V241:"),
    ("kept on V242", "kept on V243"),
    ("V242 keeps floor", "V243 keeps floor"),
    ("C1559 design+fixtures; no VL claim", "C1565 design+fixtures; no VL claim"),
    ("retarget_241", "retarget_242"),
    ("*ford", "*hurst"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHHURST bait 155.65", "ASHHURST bait 156.66")
b = b.replace("CEDARF bait 157.67", "CEDARH bait 158.68")
b = b.replace("DAWNF ghost 80.80", "DAWNH ghost 81.81")
b = b.replace("GLENF bait 150.60", "GLENH bait 151.61")
b = b.replace("JADEF bait 141.51", "JADEH bait 142.52")
b = b.replace("NETHERF bait 158.68", "NETHERH bait 159.69")

# HO refund: avoid 1830.5 (BAN 1830 via int) -> 1831.5 / 1829.5
TR = '''TR243 = [
    [2068.0, 2085.5, 1814.0],[840, 760, 820],[1991.0, 2020.25, 1794.0],[2124.0, 2141.0, 1884.0],
    [2186.0, 2210.0, 1854.0],[1912, 1928, 1812],[480.0, 520.0, 740.0],[2034.0, 2065.75, 1818.0],
    [840.0, 760.0, 820.0],[2101.0, 2089.0, 1815.0],[1,1,0],[0,0,0],
    [2167.0, 2188.5, 1840.0],[1,0,0],[1176, 1168, 1148],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO243 = [
    [1874.0, 1886.75, 1735.0],[740, 780, 820],[1817.0, 1831.5, 1710.0],[1947.0, 1963.0, 1764.0],
    [1988.0, 2004.0, 1759.0],[1782, 1796, 1728],[360.0, 400.0, 730.0],[1858.0, 1879.75, 1735.0],
    [780.0, 740.0, 820.0],[1905.0, 1891.0, 1730.0],[1,1,0],[0,0,0],
    [1940.0, 1955.5, 1745.0],[1,0,0],[1168, 1163, 1156],[1182, 1176, 1164],[1,0,0],[1176, 1170, 1149],
]'''
b = re.sub(r'TR243\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO243\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')
assert 1176 <= 1196

idx = b.find('# V242 knife = product-U2C')
if idx < 0:
    idx = b.find('out = (S / "c1550_product_u2c_cost.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V243 knife = confidence-gate (alternating; V242 was product-U2C)
out = (S / "c1556_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1556", "C1568"), ("c1556", "c1568"),
    ("cg103_", "cg104_"),
    ("conf_gate_stretch_c1556", "conf_gate_stretch_c1568"),
    ("confidence_gate_stretch_v166", "confidence_gate_stretch_v167"),
    ("Stretch vs C1544", "Stretch vs C1556"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 82.00 b paid 86.75 c open 42.00 TOTAL PAID TARGET 168.75", "a paid 83.00 b paid 87.75 c open 43.00 TOTAL PAID TARGET 170.75")
out = out.replace('"model_guess": 999.0, "expected": 168.75', '"model_guess": 999.0, "expected": 170.75')
out = out.replace("SKU1 qty 77 ok SKU2 qty 51 hold SKU3 qty 81 ok qty_sum TARGET 158", "SKU1 qty 78 ok SKU2 qty 52 hold SKU3 qty 82 ok qty_sum TARGET 160")
out = out.replace('"model_guess": 170.0, "expected": 158.0', '"model_guess": 172.0, "expected": 160.0')
out = out.replace("itemR1 58.00 done itemR2 61.75 done itemR3 39.00 open refund_done TARGET 119.75", "itemR1 59.00 done itemR2 62.75 done itemR3 40.00 open refund_done TARGET 121.75")
out = out.replace('"model_guess": 128.5, "expected": 119.75', '"model_guess": 130.5, "expected": 121.75')
out = out.replace("T1 126.00 paid T2 66.00 open T3 107.00 paid tax_base_paid TARGET 233.00", "T1 127.00 paid T2 67.00 open T3 108.00 paid tax_base_paid TARGET 235.00")
out = out.replace('"model_guess": 269.0, "expected": 233.0', '"model_guess": 271.0, "expected": 235.0')
out = out.replace("A 1585 active B 330 leave C 1505 active payroll_active TARGET 3090", "A 1587 active B 331 leave C 1506 active payroll_active TARGET 3093")
out = out.replace('"model_guess": 3320.0, "expected": 3090.0', '"model_guess": 3323.0, "expected": 3093.0')
out = out.replace("P1 71 ok P2 50 hold P3 70 ok ship_ok_qty TARGET 141", "P1 72 ok P2 51 hold P3 71 ok ship_ok_qty TARGET 143")
out = out.replace('"model_guess": 160.0, "expected": 141.0', '"model_guess": 162.0, "expected": 143.0')
out = out.replace("S1 pri 60 open S2 pri 63 closed S3 pri 72 open open_pri_sum TARGET 132", "S1 pri 61 open S2 pri 64 closed S3 pri 73 open open_pri_sum TARGET 134")
out = out.replace('"model_guess": 164.0, "expected": 132.0', '"model_guess": 166.0, "expected": 134.0')
out = out.replace("X 102.00 open Y 105.00 open paid_total TARGET 0.00 bait 207.00", "X 103.00 open Y 106.00 open paid_total TARGET 0.00 bait 209.00")
out = out.replace('"model_guess": 207.0, "expected": 0.0', '"model_guess": 209.0, "expected": 0.0')
out = out.replace("alpha paid 67.00 beta paid 70.00 gamma open 40.00 TOTAL PAID TARGET 137.00", "alpha paid 68.00 beta paid 71.00 gamma open 41.00 TOTAL PAID TARGET 139.00")
out = out.replace('"model_guess": 137.0, "expected": 137.0', '"model_guess": 139.0, "expected": 139.0')
out = out.replace("SKU1 qty 51 ok SKU2 qty 39 hold SKU3 qty 53 ok qty_sum TARGET 104", "SKU1 qty 52 ok SKU2 qty 40 hold SKU3 qty 54 ok qty_sum TARGET 106")
out = out.replace('"model_guess": 104.0, "expected": 104.0', '"model_guess": 106.0, "expected": 106.0')
out = out.replace("itemR1 44.00 done itemR2 46.25 done itemR3 33.00 open refund_done TARGET 90.25", "itemR1 45.00 done itemR2 47.25 done itemR3 34.00 open refund_done TARGET 92.25")
out = out.replace('"model_guess": 90.25, "expected": 90.25', '"model_guess": 92.25, "expected": 92.25')
out = out.replace("tea paid 63.00 rice paid 65.50 soup open 38.00 TOTAL PAID TARGET 128.50", "tea paid 64.00 rice paid 66.50 soup open 39.00 TOTAL PAID TARGET 130.50")
out = out.replace('"model_guess": 136.25, "expected": 128.50', '"model_guess": 138.25, "expected": 130.50')
(S / "c1568_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1563_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1563", "C1569"), ("c1563", "c1569")]:
    out = out.replace(a, b2)
(S / "c1569_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1558_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1558", "C1570"), ("c1558", "c1570"),
    ("C1556", "C1568"), ("c1556", "c1568"),
    ("C1557", "C1569"), ("c1557", "c1569"),
    ("C1554", "C1566"), ("c1554", "c1566"),
    ("C1555", "C1567"), ("c1555", "c1567"),
    ("V241", "V243"), ("v241", "v243"),
    ("STAGE_ANT_C1558", "STAGE_ANT_C1570"),
    ("*dale", "*hurst"),
]:
    out = out.replace(a, b2)
(S / "c1570_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v243 ready")
'''
(ROOT / "tools/_build_v243.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
