from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v231.py").read_text(encoding="utf-8")

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
    ("T231", "T232"), ("TR231", "TR232"), ("HO231", "HO232"),
    ("NEW231", "NEW232"),
    ("V231", "V232"), ("v231", "v232"),
    ("_v231_themes.json", "_v232_themes.json"),
    ("_v230_themes.json", "_v231_themes.json"),
    ("OLD230", "OLD231"),
    ("vision_images_v231", "vision_images_v232"),
    ("VL_GATE_V231", "VL_GATE_V232"), ("vl_gate_v231", "vl_gate_v232"),
    ("C1493", "C1499"), ("c1493", "c1499"),
    ("C1494", "C1500"), ("c1494", "c1500"),
    ("C1495", "C1501"), ("c1495", "c1501"),
    ("_v231c1493", "_v232c1499"),
    ("Harder than V229", "Harder than V230"),
    ("harder than V229", "harder than V230"),
    ("NEW themes vs V229:", "NEW themes vs V230:"),
    ("kept on V231", "kept on V232"),
    ("V231 keeps floor", "V232 keeps floor"),
    ("C1493 design+fixtures; no VL claim", "C1499 design+fixtures; no VL claim"),
    ("retarget_230", "retarget_231"),
    ("*ford", "*hurst"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHHURST bait 144.54", "ASHHURST bait 145.55")
b = b.replace("CEDARF bait 146.56", "CEDARH bait 147.57")
b = b.replace("DAWNF ghost 69.69", "DAWNH ghost 70.70")
b = b.replace("GLENF bait 139.49", "GLENH bait 140.50")
b = b.replace("JADEF bait 130.40", "JADEH bait 131.41")
b = b.replace("NETHERF bait 147.57", "NETHERH bait 148.58")

TR = '''TR232 = [
    [1870.0, 1887.5, 1638.0],[840, 760, 820],[1793.0, 1822.25, 1618.0],[1926.0, 1943.0, 1708.0],
    [1988.0, 2012.0, 1678.0],[1736, 1752, 1636],[480.0, 520.0, 740.0],[1836.0, 1867.75, 1642.0],
    [840.0, 760.0, 820.0],[1903.0, 1891.0, 1639.0],[1,1,0],[0,0,0],
    [1969.0, 1990.5, 1664.0],[1,0,0],[1176, 1168, 1148],[1192, 1176, 748],[1,0,0],[1208, 1192, 1170],
]'''
HO = '''HO232 = [
    [1698.0, 1710.75, 1559.0],[740, 780, 820],[1641.0, 1654.5, 1534.0],[1771.0, 1787.0, 1588.0],
    [1812.0, 1828.0, 1583.0],[1606, 1620, 1552],[360.0, 400.0, 730.0],[1682.0, 1703.75, 1559.0],
    [780.0, 740.0, 820.0],[1729.0, 1715.0, 1554.0],[1,1,0],[0,0,0],
    [1764.0, 1779.5, 1569.0],[1,0,0],[1164, 1159, 1152],[1178, 1172, 1160],[1,0,0],[1188, 1182, 1161],
]'''
b = re.sub(r'TR232\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO232\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

idx = b.find('# V231 knife = confidence-gate')
if idx < 0:
    idx = b.find('# V232 knife = confidence-gate')
if idx < 0:
    idx = b.find('out = (S / "c1484_confidence_gate_stretch.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V232 knife = product-U2C (alternating; V231 was conf-gate)
out = (S / "c1490_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1490", "C1502"), ("c1490", "c1502"),
    ("product_u2c_c1490", "product_u2c_c1502"),
    ("vs C1478", "vs C1490"),
]:
    out = out.replace(a, b2)
(S / "c1502_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1497_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1497", "C1503"), ("c1497", "c1503")]:
    out = out.replace(a, b2)
(S / "c1503_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1492_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1492", "C1504"), ("c1492", "c1504"),
    ("C1490", "C1502"), ("c1490", "c1502"),
    ("C1491", "C1503"), ("c1491", "c1503"),
    ("C1488", "C1500"), ("c1488", "c1500"),
    ("C1489", "C1501"), ("c1489", "c1501"),
    ("V230", "V232"), ("v230", "v232"),
    ("STAGE_ANT_C1492", "STAGE_ANT_C1504"),
    ("*dale", "*hurst"),
]:
    out = out.replace(a, b2)
(S / "c1504_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v232 ready")
'''
(ROOT / "tools/_build_v232.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1499_vision_v232", "c1500_vision_v232", "c1501_vision_v232", "ashhurst", "T232"]:
    print(needle, needle in (head+tail))
