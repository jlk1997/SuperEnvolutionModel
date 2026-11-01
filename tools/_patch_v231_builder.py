from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v230.py").read_text(encoding="utf-8")

theme_pairs = [
    ("netherdale", "netherford"), ("NETHERDALE", "NETHERFORD"),
    ("cedardale", "cedarford"), ("CEDARDALE", "CEDARFORD"),
    ("dawndale", "dawnford"), ("DAWNDALE", "DAWNFORD"),
    ("ferndale", "fernford"), ("FERNDALE", "FERNFORD"),
    ("glendale", "glenford"), ("GLENDALE", "GLENFORD"),
    ("hazedale", "hazeford"), ("HAZEDALE", "HAZEFORD"),
    ("jadedale", "jadeford"), ("JADEDALE", "JADEFORD"),
    ("knotdale", "knotford"), ("KNOTDALE", "KNOTFORD"),
    ("lakedale", "lakeford"), ("LAKEDALE", "LAKEFORD"),
    ("mossdale", "mossford"), ("MOSSDALE", "MOSSFORD"),
    ("pinedale", "pineford"), ("PINEDALE", "PINEFORD"),
    ("quilldale", "quillford"), ("QUILLDALE", "QUILLFORD"),
    ("reeddale", "reedford"), ("REEDDALE", "REEDFORD"),
    ("stonedale", "stoneford"), ("STONEDALE", "STONEFORD"),
    ("ashdale", "ashford"), ("ASHDALE", "ASHFORD"),
    ("elmdale", "elmford"), ("ELMDALE", "ELMFORD"),
    ("inkdale", "inkford"), ("INKDALE", "INKFORD"),
    ("oakdale", "oakford"), ("OAKDALE", "OAKFORD"),
]
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*dale ; stack mid-band", "*ford ; stack mid-band"),
    ("T230", "T231"), ("TR230", "TR231"), ("HO230", "HO231"),
    ("NEW230", "NEW231"),
    ("V230", "V231"), ("v230", "v231"),
    ("_v230_themes.json", "_v231_themes.json"),
    ("_v229_themes.json", "_v230_themes.json"),
    ("OLD229", "OLD230"),
    ("vision_images_v230", "vision_images_v231"),
    ("VL_GATE_V230", "VL_GATE_V231"), ("vl_gate_v230", "vl_gate_v231"),
    ("C1487", "C1493"), ("c1487", "c1493"),
    ("C1488", "C1494"), ("c1488", "c1494"),
    ("C1489", "C1495"), ("c1489", "c1495"),
    ("_v230c1487", "_v231c1493"),
    ("Harder than V228", "Harder than V229"),
    ("harder than V228", "harder than V229"),
    ("NEW themes vs V228:", "NEW themes vs V229:"),
    ("kept on V230", "kept on V231"),
    ("V230 keeps floor", "V231 keeps floor"),
    ("C1487 design+fixtures; no VL claim", "C1493 design+fixtures; no VL claim"),
    ("retarget_229", "retarget_230"),
    ("*dale", "*ford"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHFORD bait 143.53", "ASHFORD bait 144.54")
b = b.replace("CEDARD bait 145.55", "CEDARF bait 146.56")
b = b.replace("DAWND ghost 68.68", "DAWNF ghost 69.69")
b = b.replace("GLEND bait 138.48", "GLENF bait 139.49")
b = b.replace("JADED bait 129.39", "JADEF bait 130.40")
b = b.replace("NETHERD bait 146.56", "NETHERF bait 147.57")

TR = '''TR231 = [
    [1852.0, 1869.5, 1622.0],[840, 760, 820],[1775.0, 1804.25, 1602.0],[1908.0, 1925.0, 1692.0],
    [1970.0, 1994.0, 1662.0],[1720, 1736, 1620],[480.0, 520.0, 740.0],[1818.0, 1849.75, 1626.0],
    [840.0, 760.0, 820.0],[1885.0, 1873.0, 1623.0],[1,1,0],[0,0,0],
    [1951.0, 1972.5, 1648.0],[1,0,0],[1172, 1164, 1144],[1188, 1172, 748],[1,0,0],[1204, 1188, 1166],
]'''
HO = '''HO231 = [
    [1682.0, 1694.75, 1543.0],[740, 780, 820],[1625.0, 1638.5, 1518.0],[1755.0, 1771.0, 1572.0],
    [1796.0, 1812.0, 1567.0],[1590, 1604, 1536],[360.0, 400.0, 730.0],[1666.0, 1687.75, 1543.0],
    [780.0, 740.0, 820.0],[1713.0, 1699.0, 1538.0],[1,1,0],[0,0,0],
    [1748.0, 1763.5, 1553.0],[1,0,0],[1160, 1155, 1148],[1174, 1168, 1156],[1,0,0],[1184, 1178, 1157],
]'''
b = re.sub(r'TR231\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO231\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

idx = b.find('# V230 knife = product-U2C')
if idx < 0:
    idx = b.find('# V231 knife = product-U2C')
if idx < 0:
    idx = b.find('out = (S / "c1478_product_u2c_cost.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V231 knife = confidence-gate (alternating; V230 was product-U2C)
out = (S / "c1484_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1484", "C1496"), ("c1484", "c1496"),
    ("cg97_", "cg98_"),
    ("conf_gate_stretch_c1484", "conf_gate_stretch_c1496"),
    ("confidence_gate_stretch_v160", "confidence_gate_stretch_v161"),
    ("Stretch vs C1472", "Stretch vs C1484"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 76.00 b paid 80.75 c open 36.00 TOTAL PAID TARGET 156.75", "a paid 77.00 b paid 81.75 c open 37.00 TOTAL PAID TARGET 158.75")
out = out.replace('"model_guess": 999.0, "expected": 156.75', '"model_guess": 999.0, "expected": 158.75')
out = out.replace("SKU1 qty 71 ok SKU2 qty 45 hold SKU3 qty 75 ok qty_sum TARGET 146", "SKU1 qty 72 ok SKU2 qty 46 hold SKU3 qty 76 ok qty_sum TARGET 148")
out = out.replace('"model_guess": 158.0, "expected": 146.0', '"model_guess": 160.0, "expected": 148.0')
out = out.replace("itemR1 52.00 done itemR2 55.75 done itemR3 33.00 open refund_done TARGET 107.75", "itemR1 53.00 done itemR2 56.75 done itemR3 34.00 open refund_done TARGET 109.75")
out = out.replace('"model_guess": 116.5, "expected": 107.75', '"model_guess": 118.5, "expected": 109.75')
out = out.replace("T1 120.00 paid T2 60.00 open T3 101.00 paid tax_base_paid TARGET 221.00", "T1 121.00 paid T2 61.00 open T3 102.00 paid tax_base_paid TARGET 223.00")
out = out.replace('"model_guess": 257.0, "expected": 221.0', '"model_guess": 259.0, "expected": 223.0')
out = out.replace("A 1573 active B 324 leave C 1499 active payroll_active TARGET 3072", "A 1575 active B 325 leave C 1500 active payroll_active TARGET 3075")
out = out.replace('"model_guess": 3302.0, "expected": 3072.0', '"model_guess": 3305.0, "expected": 3075.0')
out = out.replace("P1 65 ok P2 44 hold P3 64 ok ship_ok_qty TARGET 129", "P1 66 ok P2 45 hold P3 65 ok ship_ok_qty TARGET 131")
out = out.replace('"model_guess": 148.0, "expected": 129.0', '"model_guess": 150.0, "expected": 131.0')
out = out.replace("S1 pri 54 open S2 pri 57 closed S3 pri 66 open open_pri_sum TARGET 120", "S1 pri 55 open S2 pri 58 closed S3 pri 67 open open_pri_sum TARGET 122")
out = out.replace('"model_guess": 152.0, "expected": 120.0', '"model_guess": 154.0, "expected": 122.0')
out = out.replace("X 96.00 open Y 99.00 open paid_total TARGET 0.00 bait 195.00", "X 97.00 open Y 100.00 open paid_total TARGET 0.00 bait 197.00")
out = out.replace('"model_guess": 195.0, "expected": 0.0', '"model_guess": 197.0, "expected": 0.0')
out = out.replace("alpha paid 61.00 beta paid 64.00 gamma open 34.00 TOTAL PAID TARGET 125.00", "alpha paid 62.00 beta paid 65.00 gamma open 35.00 TOTAL PAID TARGET 127.00")
out = out.replace('"model_guess": 125.0, "expected": 125.0', '"model_guess": 127.0, "expected": 127.0')
out = out.replace("SKU1 qty 45 ok SKU2 qty 33 hold SKU3 qty 47 ok qty_sum TARGET 92", "SKU1 qty 46 ok SKU2 qty 34 hold SKU3 qty 48 ok qty_sum TARGET 94")
out = out.replace('"model_guess": 92.0, "expected": 92.0', '"model_guess": 94.0, "expected": 94.0')
out = out.replace("itemR1 38.00 done itemR2 40.25 done itemR3 27.00 open refund_done TARGET 78.25", "itemR1 39.00 done itemR2 41.25 done itemR3 28.00 open refund_done TARGET 80.25")
out = out.replace('"model_guess": 78.25, "expected": 78.25', '"model_guess": 80.25, "expected": 80.25')
out = out.replace("tea paid 57.00 rice paid 59.50 soup open 32.00 TOTAL PAID TARGET 116.50", "tea paid 58.00 rice paid 60.50 soup open 33.00 TOTAL PAID TARGET 118.50")
out = out.replace('"model_guess": 124.25, "expected": 116.50', '"model_guess": 126.25, "expected": 118.50')
(S / "c1496_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1491_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1491", "C1497"), ("c1491", "c1497")]:
    out = out.replace(a, b2)
(S / "c1497_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1486_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1486", "C1498"), ("c1486", "c1498"),
    ("C1484", "C1496"), ("c1484", "c1496"),
    ("C1485", "C1497"), ("c1485", "c1497"),
    ("C1482", "C1494"), ("c1482", "c1494"),
    ("C1483", "C1495"), ("c1483", "c1495"),
    ("V229", "V231"), ("v229", "v231"),
    ("STAGE_ANT_C1486", "STAGE_ANT_C1498"),
    ("*brook", "*ford"),
]:
    out = out.replace(a, b2)
(S / "c1498_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v231 ready")
'''
(ROOT / "tools/_build_v231.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1493_vision_v231", "c1494_vision_v231", "c1495_vision_v231", "ashford", "T231"]:
    print(needle, needle in (head+tail))
