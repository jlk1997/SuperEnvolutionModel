from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v285.py").read_text(encoding="utf-8")
idx0 = b0.find('# V285 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
pairs = [
    ("*dale ; stack mid-band", "*ford ; stack mid-band"),
    ("T285", "T286"), ("TR285", "TR286"), ("HO285", "HO286"),
    ("NEW285", "NEW286"),
    ("V285", "V286"), ("v285", "v286"),
    ("_v285_themes.json", "_v286_themes.json"),
    ("_v284_themes.json", "_v285_themes.json"),
    ("OLD284", "OLD285"),
    ("vision_images_v285", "vision_images_v286"),
    ("VL_GATE_V285", "VL_GATE_V286"), ("vl_gate_v285", "vl_gate_v286"),
    ("C1817", "C1823"), ("c1817", "c1823"),
    ("C1818", "C1824"), ("c1818", "c1824"),
    ("C1819", "C1825"), ("c1819", "c1825"),
    ("_v285c1817", "_v286c1823"),
    ("Harder than V283", "Harder than V284"),
    ("harder than V283", "harder than V284"),
    ("NEW themes vs V283:", "NEW themes vs V284:"),
    ("kept on V285", "kept on V286"),
    ("V285 keeps floor", "V286 keeps floor"),
    ("C1817 design+fixtures; no VL claim", "C1823 design+fixtures; no VL claim"),
    ("retarget_284", "retarget_285"),
    ("*dale", "*ford"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHDALE bait 198.08", "ASHFORD bait 199.09")
h = h.replace("CEDARD bait 200.10", "CEDARF bait 201.11")
h = h.replace("DAWND ghost 123.33", "DAWNF ghost 124.34")
h = h.replace("GLEND bait 193.03", "GLENF bait 194.04")
h = h.replace("JADED bait 184.94", "JADEF bait 185.95")
h = h.replace("NETHERD bait 201.11", "NETHERF bait 202.12")

TR = '''TR286 = [
    [2233.0, 2250.5, 1973.0],[840, 760, 820],[2156.0, 2185.25, 1951.0],[2289.0, 2306.0, 2041.0],
    [2351.0, 2375.0, 2011.0],[2069, 2085, 1969],[490.0, 530.0, 760.0],[2199.0, 2230.75, 1975.0],
    [840.0, 760.0, 820.0],[2266.0, 2254.0, 1972.0],[1,1,0],[0,0,0],
    [2332.0, 2353.5, 1997.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO286 = [
    [2031.0, 2043.75, 1892.0],[640, 660, 820],[1974.0, 1988.5, 1867.0],[2104.0, 2120.0, 1923.0],
    [2145.0, 2161.0, 1916.0],[1927, 1939, 1887],[420.0, 460.0, 740.0],[2015.0, 2036.75, 1892.0],
    [740.0, 780.0, 820.0],[2062.0, 2048.0, 1889.0],[1,1,0],[0,0,0],
    [2097.0, 2112.5, 1902.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR286\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO286\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

tail = '''# V286 knife = product-U2C (alternating; V285 was confidence-gate)
out = (S / "c1814_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1814", "C1826"), ("c1814", "c1826"),
    ("C1802", "C1826"), ("c1802", "c1826"),
    ("C1466", "C1826"), ("c1466", "c1826"),
]:
    out = out.replace(a, b2)
(S / "c1826_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1814_product_u2c_cost.py")

out = (S / "c1821_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1821", "C1827"), ("c1821", "c1827")]:
    out = out.replace(a, b2)
(S / "c1827_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1816_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1816", "C1828"), ("c1816", "c1828"),
    ("C1814", "C1826"), ("c1814", "c1826"),
    ("C1815", "C1827"), ("c1815", "c1827"),
    ("C1812", "C1824"), ("c1812", "c1824"),
    ("C1813", "C1825"), ("c1813", "c1825"),
    ("V284", "V286"), ("v284", "v286"),
    ("STAGE_ANT_C1816", "STAGE_ANT_C1828"),
    ("*brook", "*ford"),
]:
    out = out.replace(a, b2)
(S / "c1828_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1816_scorecard_and_stage.py")
print("OK builder v286 ready")
'''
(ROOT / "tools/_build_v286.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1823_vision_v286", "ashford", "fernford", "T286", "1188", "1887", "product_u2c", "retarget_285"]:
    print(needle, needle in (h+tail))
