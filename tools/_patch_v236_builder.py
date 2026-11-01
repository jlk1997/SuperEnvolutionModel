from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v235.py").read_text(encoding="utf-8")

theme_pairs = [
    ("nethercroft", "netherholm"), ("NETHERCROFT", "NETHERHOLM"),
    ("cedarcroft", "cedarholm"), ("CEDARCROFT", "CEDARHOLM"),
    ("dawncroft", "dawnholm"), ("DAWNCROFT", "DAWNHOLM"),
    ("ferncroft", "fernholm"), ("FERNCROFT", "FERNHOLM"),
    ("glencroft", "glenholm"), ("GLENCROFT", "GLENHOLM"),
    ("hazecroft", "hazeholm"), ("HAZECROFT", "HAZEHOLM"),
    ("jadecroft", "jadeholm"), ("JADECROFT", "JADEHOLM"),
    ("knotcroft", "knotholm"), ("KNOTCROFT", "KNOTHOLM"),
    ("lakecroft", "lakeholm"), ("LAKECROFT", "LAKEHOLM"),
    ("mosscroft", "mossholm"), ("MOSSCROFT", "MOSSHOLM"),
    ("pinecroft", "pineholm"), ("PINECROFT", "PINEHOLM"),
    ("quillcroft", "quillholm"), ("QUILLCROFT", "QUILLHOLM"),
    ("reedcroft", "reedholm"), ("REEDCROFT", "REEDHOLM"),
    ("stonecroft", "stoneholm"), ("STONECROFT", "STONEHOLM"),
    ("ashcroft", "ashholm"), ("ASHCROFT", "ASHHOLM"),
    ("elmcroft", "elmholm"), ("ELMCROFT", "ELMHOLM"),
    ("inkcroft", "inkholm"), ("INKCROFT", "INKHOLM"),
    ("oakcroft", "oakholm"), ("OAKCROFT", "OAKHOLM"),
]
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*croft ; stack mid-band", "*holm ; stack mid-band"),
    ("T235", "T236"), ("TR235", "TR236"), ("HO235", "HO236"),
    ("NEW235", "NEW236"),
    ("V235", "V236"), ("v235", "v236"),
    ("_v235_themes.json", "_v236_themes.json"),
    ("_v234_themes.json", "_v235_themes.json"),
    ("OLD234", "OLD235"),
    ("vision_images_v235", "vision_images_v236"),
    ("VL_GATE_V235", "VL_GATE_V236"), ("vl_gate_v235", "vl_gate_v236"),
    ("C1517", "C1523"), ("c1517", "c1523"),
    ("C1518", "C1524"), ("c1518", "c1524"),
    ("C1519", "C1525"), ("c1519", "c1525"),
    ("_v235c1517", "_v236c1523"),
    ("Harder than V233", "Harder than V234"),
    ("harder than V233", "harder than V234"),
    ("NEW themes vs V233:", "NEW themes vs V234:"),
    ("kept on V235", "kept on V236"),
    ("V235 keeps floor", "V236 keeps floor"),
    ("C1517 design+fixtures; no VL claim", "C1523 design+fixtures; no VL claim"),
    ("retarget_234", "retarget_235"),
    ("*croft", "*holm"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHHOLM bait 148.58", "ASHHOLM bait 149.59")
b = b.replace("CEDARC bait 150.60", "CEDARH bait 151.61")
b = b.replace("DAWNC ghost 73.73", "DAWNH ghost 74.74")
b = b.replace("GLENC bait 143.53", "GLENH bait 144.54")
b = b.replace("JADEC bait 134.44", "JADEH bait 135.45")
b = b.replace("NETHERC bait 151.61", "NETHERH bait 152.62")

TR = '''TR236 = [
    [1942.0, 1959.5, 1702.0],[840, 760, 820],[1865.0, 1894.25, 1682.0],[1998.0, 2015.0, 1772.0],
    [2060.0, 2084.0, 1742.0],[1800, 1816, 1700],[480.0, 520.0, 740.0],[1908.0, 1939.75, 1706.0],
    [840.0, 760.0, 820.0],[1975.0, 1963.0, 1703.0],[1,1,0],[0,0,0],
    [2041.0, 2062.5, 1728.0],[1,0,0],[1192, 1184, 1164],[1208, 1192, 748],[1,0,0],[1224, 1208, 1186],
]'''
HO = '''HO236 = [
    [1762.0, 1774.75, 1623.0],[740, 780, 820],[1705.0, 1718.5, 1598.0],[1835.0, 1851.0, 1652.0],
    [1876.0, 1892.0, 1647.0],[1670, 1684, 1616],[360.0, 400.0, 730.0],[1746.0, 1767.75, 1623.0],
    [780.0, 740.0, 820.0],[1793.0, 1779.0, 1618.0],[1,1,0],[0,0,0],
    [1828.0, 1843.5, 1633.0],[1,0,0],[1180, 1175, 1168],[1194, 1188, 1176],[1,0,0],[1204, 1198, 1177],
]'''
b = re.sub(r'TR236\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO236\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

idx = b.find('# V235 knife = confidence-gate')
if idx < 0:
    idx = b.find('# V236 knife = confidence-gate')
if idx < 0:
    idx = b.find('out = (S / "c1508_confidence_gate_stretch.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V236 knife = product-U2C (alternating; V235 was conf-gate)
out = (S / "c1514_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1514", "C1526"), ("c1514", "c1526"),
    ("product_u2c_c1514", "product_u2c_c1526"),
    ("vs C1502", "vs C1514"),
]:
    out = out.replace(a, b2)
(S / "c1526_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1521_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1521", "C1527"), ("c1521", "c1527")]:
    out = out.replace(a, b2)
(S / "c1527_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1516_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1516", "C1528"), ("c1516", "c1528"),
    ("C1514", "C1526"), ("c1514", "c1526"),
    ("C1515", "C1527"), ("c1515", "c1527"),
    ("C1512", "C1524"), ("c1512", "c1524"),
    ("C1513", "C1525"), ("c1513", "c1525"),
    ("V234", "V236"), ("v234", "v236"),
    ("STAGE_ANT_C1516", "STAGE_ANT_C1528"),
    ("*vale", "*holm"),
]:
    out = out.replace(a, b2)
(S / "c1528_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v236 ready")
'''
(ROOT / "tools/_build_v236.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1523_vision_v236", "c1524_vision_v236", "c1525_vision_v236", "ashholm", "T236"]:
    print(needle, needle in (head+tail))
