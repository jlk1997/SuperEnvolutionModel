from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
# Start fresh from v228 builder again
src = (ROOT / "tools/_build_v228.py").read_text(encoding="utf-8")
(ROOT / "tools/_build_v229.py").write_text(src, encoding="utf-8")
b = src

theme_pairs = [
    ("netherfen", "netherbrook"), ("NETHERFEN", "NETHERBROOK"),
    ("cedarfen", "cedarbrook"), ("CEDARFEN", "CEDARBROOK"),
    ("dawnfen", "dawnbrook"), ("DAWNFEN", "DAWNBROOK"),
    ("fernfen", "fernbrook"), ("FERNFEN", "FERNBROOK"),
    ("glenfen", "glenbrook"), ("GLENFEN", "GLENBROOK"),
    ("hazefen", "hazebrook"), ("HAZEFEN", "HAZEBROOK"),
    ("jadefen", "jadebrook"), ("JADEFEN", "JADEBROOK"),
    ("knotfen", "knotbrook"), ("KNOTFEN", "KNOTBROOK"),
    ("lakefen", "lakebrook"), ("LAKEFEN", "LAKEBROOK"),
    ("mossfen", "mossbrook"), ("MOSSFEN", "MOSSBROOK"),
    ("pinefen", "pinebrook"), ("PINEFEN", "PINEBROOK"),
    ("quillfen", "quillbrook"), ("QUILLFEN", "QUILLBROOK"),
    ("reedfen", "reedbrook"), ("REEDFEN", "REEDBROOK"),
    ("stonefen", "stonebrook"), ("STONEFEN", "STONEBROOK"),
    ("ashfen", "ashbrook"), ("ASHFEN", "ASHBROOK"),
    ("elmfen", "elmbrook"), ("ELMFEN", "ELMBROOK"),
    ("inkfen", "inkbrook"), ("INKFEN", "INKBROOK"),
    ("oakfen", "oakbrook"), ("OAKFEN", "OAKBROOK"),
]
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*fen ; stack mid-band", "*brook ; stack mid-band"),
    ("T228", "T229"), ("TR228", "TR229"), ("HO228", "HO229"),
    ("NEW228", "NEW229"),
    ("V228", "V229"), ("v228", "v229"),
    ("_v228_themes.json", "_v229_themes.json"),
    ("_v226_themes.json", "_v228_themes.json"),
    ("OLD226", "OLD228"),
    ("vision_images_v228", "vision_images_v229"),
    ("VL_GATE_V228", "VL_GATE_V229"), ("vl_gate_v228", "vl_gate_v229"),
    ("C1475", "C1481"), ("c1475", "c1481"),
    ("C1476", "C1482"), ("c1476", "c1482"),
    ("C1477", "C1483"), ("c1477", "c1483"),
    ("_v228c1475", "_v229c1481"),
    ("Harder than V226", "Harder than V227"),
    ("harder than V226", "harder than V227"),
    ("NEW themes vs V226:", "NEW themes vs V227:"),
    ("kept on V228", "kept on V229"),
    ("V228 keeps floor", "V229 keeps floor"),
    ("C1475 design+fixtures; no VL claim", "C1481 design+fixtures; no VL claim"),
    ("retarget_227", "retarget_228"),
    ("*fen", "*brook"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHBROOK bait 141.51", "ASHBROOK bait 142.52")
b = b.replace("CEDARM bait 143.53", "CEDARB bait 144.54")
b = b.replace("DAWNM ghost 66.66", "DAWNB ghost 67.67")
b = b.replace("GLENM bait 136.46", "GLENB bait 137.47")
b = b.replace("JADEM bait 127.37", "JADEB bait 128.38")
b = b.replace("NETHERM bait 144.54", "NETHERB bait 145.55")

# fax c = 748 not 756 (BAN)
TR = '''TR229 = [
    [1816.0, 1833.5, 1590.0],[840, 760, 820],[1739.0, 1768.25, 1570.0],[1872.0, 1889.0, 1660.0],
    [1934.0, 1958.0, 1630.0],[1688, 1704, 1588],[480.0, 520.0, 740.0],[1782.0, 1813.75, 1594.0],
    [840.0, 760.0, 820.0],[1849.0, 1837.0, 1591.0],[1,1,0],[0,0,0],
    [1915.0, 1936.5, 1616.0],[1,0,0],[1164, 1156, 1136],[1180, 1164, 748],[1,0,0],[1196, 1180, 1158],
]'''
HO = '''HO229 = [
    [1650.0, 1662.75, 1511.0],[740, 780, 820],[1593.0, 1606.5, 1486.0],[1723.0, 1739.0, 1540.0],
    [1764.0, 1780.0, 1535.0],[1558, 1572, 1504],[360.0, 400.0, 730.0],[1634.0, 1655.75, 1511.0],
    [780.0, 740.0, 820.0],[1681.0, 1667.0, 1506.0],[1,1,0],[0,0,0],
    [1716.0, 1731.5, 1521.0],[1,0,0],[1152, 1147, 1140],[1166, 1160, 1148],[1,0,0],[1176, 1170, 1149],
]'''
b = re.sub(r'TR229\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO229\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

idx = b.find('# V228 knife = product-U2C')
if idx < 0:
    idx = b.find('# V229 knife = product-U2C')
if idx < 0:
    idx = b.find('out = (S / "c1466_product_u2c_cost.py")')
    if idx < 0:
        raise SystemExit('knife block not found: ' + b[-400:])
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V229 knife = confidence-gate (alternating; V228 was product-U2C)
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
'''
(ROOT / "tools/_build_v229.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1481_vision_v229", "c1482_vision_v229", "c1483_vision_v229", "ashbrook", "T229"]:
    print(needle, needle in (head+tail))
