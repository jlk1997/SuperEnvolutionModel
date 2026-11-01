from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v259.py").read_text(encoding="utf-8")
idx0 = b0.find('# V259 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
pairs = [
    ("*wick ; stack mid-band", "*moor ; stack mid-band"),
    ("T259", "T260"), ("TR259", "TR260"), ("HO259", "HO260"),
    ("NEW259", "NEW260"),
    ("V259", "V260"), ("v259", "v260"),
    ("_v259_themes.json", "_v260_themes.json"),
    ("_v258_themes.json", "_v259_themes.json"),
    ("OLD258", "OLD259"),
    ("vision_images_v259", "vision_images_v260"),
    ("VL_GATE_V259", "VL_GATE_V260"), ("vl_gate_v259", "vl_gate_v260"),
    ("C1661", "C1667"), ("c1661", "c1667"),
    ("C1662", "C1668"), ("c1662", "c1668"),
    ("C1663", "C1669"), ("c1663", "c1669"),
    ("_v259c1661", "_v260c1667"),
    ("Harder than V257", "Harder than V258"),
    ("harder than V257", "harder than V258"),
    ("NEW themes vs V257:", "NEW themes vs V258:"),
    ("kept on V259", "kept on V260"),
    ("V259 keeps floor", "V260 keeps floor"),
    ("C1661 design+fixtures; no VL claim", "C1667 design+fixtures; no VL claim"),
    ("retarget_258", "retarget_259"),
    ("*wick", "*moor"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMOOR bait 172.82", "ASHMOOR bait 173.83")
h = h.replace("CEDARW bait 174.84", "CEDARM bait 175.85")
h = h.replace("DAWNW ghost 97.97", "DAWNM ghost 98.98")
h = h.replace("GLENW bait 167.77", "GLENM bait 168.78")
h = h.replace("JADEW bait 158.68", "JADEM bait 159.69")
h = h.replace("NETHERW bait 175.85", "NETHERM bait 176.86")

TR = '''TR260 = [
    [2166.0, 2183.5, 1906.0],[840, 760, 820],[2089.0, 2118.25, 1884.0],[2222.0, 2239.0, 1974.0],
    [2284.0, 2308.0, 1944.0],[2002, 2018, 1902],[480.0, 520.0, 740.0],[2132.0, 2163.75, 1908.0],
    [840.0, 760.0, 820.0],[2199.0, 2187.0, 1905.0],[1,1,0],[0,0,0],
    [2265.0, 2286.5, 1930.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO260 = [
    [1964.0, 1976.75, 1825.0],[740, 780, 820],[1907.0, 1921.5, 1800.0],[2037.0, 2053.0, 1856.0],
    [2078.0, 2094.0, 1849.0],[1860, 1872, 1818],[360.0, 400.0, 730.0],[1948.0, 1969.75, 1825.0],
    [780.0, 740.0, 820.0],[1995.0, 1981.0, 1820.0],[1,1,0],[0,0,0],
    [2030.0, 2045.5, 1835.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR260\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO260\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

src = "c1658_product_u2c_cost.py"
if not (ROOT / "scripts" / src).exists():
    src = "c1646_product_u2c_cost.py"
sc_src = "c1660_scorecard_and_stage.py"

tail = f'''# V260 knife = product-U2C (alternating; V259 was confidence-gate)
out = (S / "{src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1658", "C1670"), ("c1658", "c1670"),
    ("C1646", "C1670"), ("c1646", "c1670"),
    ("C1466", "C1670"), ("c1466", "c1670"),
]:
    out = out.replace(a, b2)
(S / "c1670_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{src}")

out = (S / "c1665_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1665", "C1671"), ("c1665", "c1671")]:
    out = out.replace(a, b2)
(S / "c1671_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1660", "C1672"), ("c1660", "c1672"),
    ("C1658", "C1670"), ("c1658", "c1670"),
    ("C1659", "C1671"), ("c1659", "c1671"),
    ("C1656", "C1668"), ("c1656", "c1668"),
    ("C1657", "C1669"), ("c1657", "c1669"),
    ("V258", "V260"), ("v258", "v260"),
    ("STAGE_ANT_C1660", "STAGE_ANT_C1672"),
    ("*holm", "*moor"),
]:
    out = out.replace(a, b2)
(S / "c1672_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v260 ready")
'''
(ROOT / "tools/_build_v260.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1667_vision_v260", "ashmoor", "fernmoor", "T260", "1188", "1856", "product_u2c"]:
    print(needle, needle in (h+tail))
