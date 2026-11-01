from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v240.py").read_text(encoding="utf-8")

theme_pairs = [
    ("netherbrook", "netherdale"), ("NETHERBROOK", "NETHERDALE"),
    ("cedarbrook", "cedardale"), ("CEDARBROOK", "CEDARDALE"),
    ("dawnbrook", "dawndale"), ("DAWNBROOK", "DAWNDALE"),
    ("fernbrook", "ferndale"), ("FERNBROOK", "FERNDALE"),
    ("glenbrook", "glendale"), ("GLENBROOK", "GLENDALE"),
    ("hazebrook", "hazedale"), ("HAZEBROOK", "HAZEDALE"),
    ("jadebrook", "jadedale"), ("JADEBROOK", "JADEDALE"),
    ("knotbrook", "knotdale"), ("KNOTBROOK", "KNOTDALE"),
    ("lakebrook", "lakedale"), ("LAKEBROOK", "LAKEDALE"),
    ("mossbrook", "mossdale"), ("MOSSBROOK", "MOSSDALE"),
    ("pinebrook", "pinedale"), ("PINEBROOK", "PINEDALE"),
    ("quillbrook", "quilldale"), ("QUILLBROOK", "QUILLDALE"),
    ("reedbrook", "reeddale"), ("REEDBROOK", "REEDDALE"),
    ("stonebrook", "stonedale"), ("STONEBROOK", "STONEDALE"),
    ("ashbrook", "ashdale"), ("ASHBROOK", "ASHDALE"),
    ("elmbrook", "elmdale"), ("ELMBROOK", "ELMDALE"),
    ("inkbrook", "inkdale"), ("INKBROOK", "INKDALE"),
    ("oakbrook", "oakdale"), ("OAKBROOK", "OAKDALE"),
]
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*brook ; stack mid-band", "*dale ; stack mid-band"),
    ("T240", "T241"), ("TR240", "TR241"), ("HO240", "HO241"),
    ("NEW240", "NEW241"),
    ("V240", "V241"), ("v240", "v241"),
    ("_v240_themes.json", "_v241_themes.json"),
    ("_v239_themes.json", "_v240_themes.json"),
    ("OLD239", "OLD240"),
    ("vision_images_v240", "vision_images_v241"),
    ("VL_GATE_V240", "VL_GATE_V241"), ("vl_gate_v240", "vl_gate_v241"),
    ("C1547", "C1553"), ("c1547", "c1553"),
    ("C1548", "C1554"), ("c1548", "c1554"),
    ("C1549", "C1555"), ("c1549", "c1555"),
    ("_v240c1547", "_v241c1553"),
    ("Harder than V238", "Harder than V239"),
    ("harder than V238", "harder than V239"),
    ("NEW themes vs V238:", "NEW themes vs V239:"),
    ("kept on V240", "kept on V241"),
    ("V240 keeps floor", "V241 keeps floor"),
    ("C1547 design+fixtures; no VL claim", "C1553 design+fixtures; no VL claim"),
    ("retarget_239", "retarget_240"),
    ("*brook", "*dale"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHDALE bait 153.63", "ASHDALE bait 154.64")
b = b.replace("CEDARB bait 155.65", "CEDARD bait 156.66")
b = b.replace("DAWNB ghost 78.78", "DAWND ghost 79.79")
b = b.replace("GLENB bait 148.58", "GLEND bait 149.59")
b = b.replace("JADEB bait 139.49", "JADED bait 140.50")
b = b.replace("NETHERB bait 156.66", "NETHERD bait 157.67")

# Money bump; stack STAY mid-band (p1<=1196) — hold at 1168 not climb toward 1200
TR = '''TR241 = [
    [2032.0, 2049.5, 1782.0],[840, 760, 820],[1955.0, 1984.25, 1762.0],[2088.0, 2105.0, 1852.0],
    [2150.0, 2174.0, 1822.0],[1880, 1896, 1780],[480.0, 520.0, 740.0],[1998.0, 2029.75, 1786.0],
    [840.0, 760.0, 820.0],[2065.0, 2053.0, 1783.0],[1,1,0],[0,0,0],
    [2131.0, 2152.5, 1808.0],[1,0,0],[1168, 1160, 1140],[1184, 1168, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO241 = [
    [1842.0, 1854.75, 1703.0],[740, 780, 820],[1785.0, 1798.5, 1678.0],[1915.0, 1931.0, 1732.0],
    [1956.0, 1972.0, 1727.0],[1750, 1764, 1696],[360.0, 400.0, 730.0],[1826.0, 1847.75, 1703.0],
    [780.0, 740.0, 820.0],[1873.0, 1859.0, 1698.0],[1,1,0],[0,0,0],
    [1908.0, 1923.5, 1713.0],[1,0,0],[1160, 1155, 1148],[1174, 1168, 1156],[1,0,0],[1176, 1170, 1149],
]'''
b = re.sub(r'TR241\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO241\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')
assert 1168 <= 1196

idx = b.find('# V240 knife = product-U2C')
if idx < 0:
    idx = b.find('# V241 knife = product-U2C')
if idx < 0:
    idx = b.find('out = (S / "c1538_product_u2c_cost.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V241 knife = confidence-gate (alternating; V240 was product-U2C)
out = (S / "c1544_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1544", "C1556"), ("c1544", "c1556"),
    ("cg102_", "cg103_"),
    ("conf_gate_stretch_c1544", "conf_gate_stretch_c1556"),
    ("confidence_gate_stretch_v165", "confidence_gate_stretch_v166"),
    ("Stretch vs C1532", "Stretch vs C1544"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 81.00 b paid 85.75 c open 41.00 TOTAL PAID TARGET 166.75", "a paid 82.00 b paid 86.75 c open 42.00 TOTAL PAID TARGET 168.75")
out = out.replace('"model_guess": 999.0, "expected": 166.75', '"model_guess": 999.0, "expected": 168.75')
out = out.replace("SKU1 qty 76 ok SKU2 qty 50 hold SKU3 qty 80 ok qty_sum TARGET 156", "SKU1 qty 77 ok SKU2 qty 51 hold SKU3 qty 81 ok qty_sum TARGET 158")
out = out.replace('"model_guess": 168.0, "expected": 156.0', '"model_guess": 170.0, "expected": 158.0')
out = out.replace("itemR1 57.00 done itemR2 60.75 done itemR3 38.00 open refund_done TARGET 117.75", "itemR1 58.00 done itemR2 61.75 done itemR3 39.00 open refund_done TARGET 119.75")
out = out.replace('"model_guess": 126.5, "expected": 117.75', '"model_guess": 128.5, "expected": 119.75')
out = out.replace("T1 125.00 paid T2 65.00 open T3 106.00 paid tax_base_paid TARGET 231.00", "T1 126.00 paid T2 66.00 open T3 107.00 paid tax_base_paid TARGET 233.00")
out = out.replace('"model_guess": 267.0, "expected": 231.0', '"model_guess": 269.0, "expected": 233.0')
out = out.replace("A 1583 active B 329 leave C 1504 active payroll_active TARGET 3087", "A 1585 active B 330 leave C 1505 active payroll_active TARGET 3090")
out = out.replace('"model_guess": 3317.0, "expected": 3087.0', '"model_guess": 3320.0, "expected": 3090.0')
out = out.replace("P1 70 ok P2 49 hold P3 69 ok ship_ok_qty TARGET 139", "P1 71 ok P2 50 hold P3 70 ok ship_ok_qty TARGET 141")
out = out.replace('"model_guess": 158.0, "expected": 139.0', '"model_guess": 160.0, "expected": 141.0')
out = out.replace("S1 pri 59 open S2 pri 62 closed S3 pri 71 open open_pri_sum TARGET 130", "S1 pri 60 open S2 pri 63 closed S3 pri 72 open open_pri_sum TARGET 132")
out = out.replace('"model_guess": 162.0, "expected": 130.0', '"model_guess": 164.0, "expected": 132.0')
out = out.replace("X 101.00 open Y 104.00 open paid_total TARGET 0.00 bait 205.00", "X 102.00 open Y 105.00 open paid_total TARGET 0.00 bait 207.00")
out = out.replace('"model_guess": 205.0, "expected": 0.0', '"model_guess": 207.0, "expected": 0.0')
out = out.replace("alpha paid 66.00 beta paid 69.00 gamma open 39.00 TOTAL PAID TARGET 135.00", "alpha paid 67.00 beta paid 70.00 gamma open 40.00 TOTAL PAID TARGET 137.00")
out = out.replace('"model_guess": 135.0, "expected": 135.0', '"model_guess": 137.0, "expected": 137.0')
out = out.replace("SKU1 qty 50 ok SKU2 qty 38 hold SKU3 qty 52 ok qty_sum TARGET 102", "SKU1 qty 51 ok SKU2 qty 39 hold SKU3 qty 53 ok qty_sum TARGET 104")
out = out.replace('"model_guess": 102.0, "expected": 102.0', '"model_guess": 104.0, "expected": 104.0')
out = out.replace("itemR1 43.00 done itemR2 45.25 done itemR3 32.00 open refund_done TARGET 88.25", "itemR1 44.00 done itemR2 46.25 done itemR3 33.00 open refund_done TARGET 90.25")
out = out.replace('"model_guess": 88.25, "expected": 88.25', '"model_guess": 90.25, "expected": 90.25')
out = out.replace("tea paid 62.00 rice paid 64.50 soup open 37.00 TOTAL PAID TARGET 126.50", "tea paid 63.00 rice paid 65.50 soup open 38.00 TOTAL PAID TARGET 128.50")
out = out.replace('"model_guess": 134.25, "expected": 126.50', '"model_guess": 136.25, "expected": 128.50')
(S / "c1556_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1551_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1551", "C1557"), ("c1551", "c1557")]:
    out = out.replace(a, b2)
(S / "c1557_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1546_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1546", "C1558"), ("c1546", "c1558"),
    ("C1544", "C1556"), ("c1544", "c1556"),
    ("C1545", "C1557"), ("c1545", "c1557"),
    ("C1542", "C1554"), ("c1542", "c1554"),
    ("C1543", "C1555"), ("c1543", "c1555"),
    ("V239", "V241"), ("v239", "v241"),
    ("STAGE_ANT_C1546", "STAGE_ANT_C1558"),
    ("*fen", "*dale"),
]:
    out = out.replace(a, b2)
(S / "c1558_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v241 ready")
'''
(ROOT / "tools/_build_v241.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1553_vision_v241", "c1554_vision_v241", "c1555_vision_v241", "ashdale", "T241", "1168"]:
    print(needle, needle in (head+tail))
