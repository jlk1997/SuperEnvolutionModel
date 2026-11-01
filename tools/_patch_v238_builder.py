from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v237.py").read_text(encoding="utf-8")

theme_pairs = [
    ("netherwick", "nethermoor"), ("NETHERWICK", "NETHERMOOR"),
    ("cedarwick", "cedarmoor"), ("CEDARWICK", "CEDARMOOR"),
    ("dawnwick", "dawnmoor"), ("DAWNWICK", "DAWNMOOR"),
    ("fernwick", "fernmoor"), ("FERNWICK", "FERNMOOR"),
    ("glenwick", "glenmoor"), ("GLENWICK", "GLENMOOR"),
    ("hazewick", "hazemoor"), ("HAZEWICK", "HAZEMOOR"),
    ("jadewick", "jademoor"), ("JADEWICK", "JADEMOOR"),
    ("knotwick", "knotmoor"), ("KNOTWICK", "KNOTMOOR"),
    ("lakewick", "lakemoor"), ("LAKEWICK", "LAKEMOOR"),
    ("mosswick", "mossmoor"), ("MOSSWICK", "MOSSMOOR"),
    ("pinewick", "pinemoor"), ("PINEWICK", "PINEMOOR"),
    ("quillwick", "quillmoor"), ("QUILLWICK", "QUILLMOOR"),
    ("reedwick", "reedmoor"), ("REEDWICK", "REEDMOOR"),
    ("stonewick", "stonemoor"), ("STONEWICK", "STONEMOOR"),
    ("ashwick", "ashmoor"), ("ASHWICK", "ASHMOOR"),
    ("elmwick", "elmmoor"), ("ELMWICK", "ELMMOOR"),
    ("inkwick", "inkmoor"), ("INKWICK", "INKMOOR"),
    ("oakwick", "oakmoor"), ("OAKWICK", "OAKMOOR"),
]
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*wick ; stack mid-band", "*moor ; stack mid-band"),
    ("T237", "T238"), ("TR237", "TR238"), ("HO237", "HO238"),
    ("NEW237", "NEW238"),
    ("V237", "V238"), ("v237", "v238"),
    ("_v237_themes.json", "_v238_themes.json"),
    ("_v236_themes.json", "_v237_themes.json"),
    ("OLD236", "OLD237"),
    ("vision_images_v237", "vision_images_v238"),
    ("VL_GATE_V237", "VL_GATE_V238"), ("vl_gate_v237", "vl_gate_v238"),
    ("C1529", "C1535"), ("c1529", "c1535"),
    ("C1530", "C1536"), ("c1530", "c1536"),
    ("C1531", "C1537"), ("c1531", "c1537"),
    ("_v237c1529", "_v238c1535"),
    ("Harder than V235", "Harder than V236"),
    ("harder than V235", "harder than V236"),
    ("NEW themes vs V235:", "NEW themes vs V236:"),
    ("kept on V237", "kept on V238"),
    ("V237 keeps floor", "V238 keeps floor"),
    ("C1529 design+fixtures; no VL claim", "C1535 design+fixtures; no VL claim"),
    ("retarget_236", "retarget_237"),
    ("*wick", "*moor"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHMOOR bait 150.60", "ASHMOOR bait 151.61")
b = b.replace("CEDARW bait 152.62", "CEDARM bait 153.63")
b = b.replace("DAWNW ghost 75.75", "DAWNM ghost 76.76")
b = b.replace("GLENW bait 145.55", "GLENM bait 146.56")
b = b.replace("JADEW bait 136.46", "JADEM bait 137.47")
b = b.replace("NETHERW bait 153.63", "NETHERM bait 154.64")

TR = '''TR238 = [
    [1978.0, 1995.5, 1734.0],[840, 760, 820],[1901.0, 1930.25, 1714.0],[2034.0, 2051.0, 1804.0],
    [2096.0, 2120.0, 1774.0],[1832, 1848, 1732],[480.0, 520.0, 740.0],[1944.0, 1975.75, 1738.0],
    [840.0, 760.0, 820.0],[2011.0, 1999.0, 1735.0],[1,1,0],[0,0,0],
    [2077.0, 2098.5, 1760.0],[1,0,0],[1200, 1192, 1172],[1216, 1200, 748],[1,0,0],[1232, 1216, 1194],
]'''
HO = '''HO238 = [
    [1794.0, 1806.75, 1655.0],[740, 780, 820],[1737.0, 1750.5, 1630.0],[1867.0, 1883.0, 1684.0],
    [1908.0, 1924.0, 1679.0],[1702, 1716, 1648],[360.0, 400.0, 730.0],[1778.0, 1799.75, 1655.0],
    [780.0, 740.0, 820.0],[1825.0, 1811.0, 1650.0],[1,1,0],[0,0,0],
    [1860.0, 1875.5, 1665.0],[1,0,0],[1188, 1183, 1176],[1202, 1196, 1184],[1,0,0],[1212, 1206, 1185],
]'''
b = re.sub(r'TR238\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO238\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

idx = b.find('# V237 knife = confidence-gate')
if idx < 0:
    idx = b.find('# V238 knife = confidence-gate')
if idx < 0:
    idx = b.find('out = (S / "c1520_confidence_gate_stretch.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V238 knife = product-U2C (alternating; V237 was conf-gate)
out = (S / "c1526_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1526", "C1538"), ("c1526", "c1538"),
    ("product_u2c_c1526", "product_u2c_c1538"),
    ("vs C1514", "vs C1526"),
]:
    out = out.replace(a, b2)
(S / "c1538_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1533_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1533", "C1539"), ("c1533", "c1539")]:
    out = out.replace(a, b2)
(S / "c1539_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1528_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1528", "C1540"), ("c1528", "c1540"),
    ("C1526", "C1538"), ("c1526", "c1538"),
    ("C1527", "C1539"), ("c1527", "c1539"),
    ("C1524", "C1536"), ("c1524", "c1536"),
    ("C1525", "C1537"), ("c1525", "c1537"),
    ("V236", "V238"), ("v236", "v238"),
    ("STAGE_ANT_C1528", "STAGE_ANT_C1540"),
    ("*holm", "*moor"),
]:
    out = out.replace(a, b2)
(S / "c1540_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v238 ready")
'''
(ROOT / "tools/_build_v238.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1535_vision_v238", "c1536_vision_v238", "c1537_vision_v238", "ashmoor", "T238"]:
    print(needle, needle in (head+tail))
