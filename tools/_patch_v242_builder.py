from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v241.py").read_text(encoding="utf-8")

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
    ("T241", "T242"), ("TR241", "TR242"), ("HO241", "HO242"),
    ("NEW241", "NEW242"),
    ("V241", "V242"), ("v241", "v242"),
    ("_v241_themes.json", "_v242_themes.json"),
    ("_v240_themes.json", "_v241_themes.json"),
    ("OLD240", "OLD241"),
    ("vision_images_v241", "vision_images_v242"),
    ("VL_GATE_V241", "VL_GATE_V242"), ("vl_gate_v241", "vl_gate_v242"),
    ("C1553", "C1559"), ("c1553", "c1559"),
    ("C1554", "C1560"), ("c1554", "c1560"),
    ("C1555", "C1561"), ("c1555", "c1561"),
    ("_v241c1553", "_v242c1559"),
    ("Harder than V239", "Harder than V240"),
    ("harder than V239", "harder than V240"),
    ("NEW themes vs V239:", "NEW themes vs V240:"),
    ("kept on V241", "kept on V242"),
    ("V241 keeps floor", "V242 keeps floor"),
    ("C1553 design+fixtures; no VL claim", "C1559 design+fixtures; no VL claim"),
    ("retarget_240", "retarget_241"),
    ("*dale", "*ford"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHFORD bait 154.64", "ASHFORD bait 155.65")
b = b.replace("CEDARD bait 156.66", "CEDARF bait 157.67")
b = b.replace("DAWND ghost 79.79", "DAWNF ghost 80.80")
b = b.replace("GLEND bait 149.59", "GLENF bait 150.60")
b = b.replace("JADED bait 140.50", "JADEF bait 141.51")
b = b.replace("NETHERD bait 157.67", "NETHERF bait 158.68")

# Money bump; stack STAY mid-band — hold ~1172 not climb to 1200
TR = '''TR242 = [
    [2050.0, 2067.5, 1798.0],[840, 760, 820],[1973.0, 2002.25, 1778.0],[2106.0, 2123.0, 1868.0],
    [2168.0, 2192.0, 1838.0],[1896, 1912, 1796],[480.0, 520.0, 740.0],[2016.0, 2047.75, 1802.0],
    [840.0, 760.0, 820.0],[2083.0, 2071.0, 1799.0],[1,1,0],[0,0,0],
    [2149.0, 2170.5, 1824.0],[1,0,0],[1172, 1164, 1144],[1188, 1172, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO242 = [
    [1858.0, 1870.75, 1719.0],[740, 780, 820],[1801.0, 1814.5, 1694.0],[1931.0, 1947.0, 1748.0],
    [1972.0, 1988.0, 1743.0],[1766, 1780, 1712],[360.0, 400.0, 730.0],[1842.0, 1863.75, 1719.0],
    [780.0, 740.0, 820.0],[1889.0, 1875.0, 1714.0],[1,1,0],[0,0,0],
    [1924.0, 1939.5, 1729.0],[1,0,0],[1164, 1159, 1152],[1178, 1172, 1160],[1,0,0],[1176, 1170, 1149],
]'''
b = re.sub(r'TR242\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO242\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')
assert 1172 <= 1196

idx = b.find('# V241 knife = confidence-gate')
if idx < 0:
    idx = b.find('# V242 knife = confidence-gate')
if idx < 0:
    idx = b.find('out = (S / "c1544_confidence_gate_stretch.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V242 knife = product-U2C (alternating; V241 was conf-gate)
out = (S / "c1550_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1550", "C1562"), ("c1550", "c1562"),
    ("product_u2c_c1550", "product_u2c_c1562"),
    ("vs C1538", "vs C1550"),
]:
    out = out.replace(a, b2)
(S / "c1562_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1557_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1557", "C1563"), ("c1557", "c1563")]:
    out = out.replace(a, b2)
(S / "c1563_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1552_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1552", "C1564"), ("c1552", "c1564"),
    ("C1550", "C1562"), ("c1550", "c1562"),
    ("C1551", "C1563"), ("c1551", "c1563"),
    ("C1548", "C1560"), ("c1548", "c1560"),
    ("C1549", "C1561"), ("c1549", "c1561"),
    ("V240", "V242"), ("v240", "v242"),
    ("STAGE_ANT_C1552", "STAGE_ANT_C1564"),
    ("*brook", "*ford"),
]:
    out = out.replace(a, b2)
(S / "c1564_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v242 ready")
'''
(ROOT / "tools/_build_v242.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1559_vision_v242", "c1560_vision_v242", "c1561_vision_v242", "ashford", "T242", "1172"]:
    print(needle, needle in (head+tail))
