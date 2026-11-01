from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v283.py").read_text(encoding="utf-8")
idx0 = b0.find('# V283 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
pairs = [
    ("*fen ; stack mid-band", "*brook ; stack mid-band"),
    ("T283", "T284"), ("TR283", "TR284"), ("HO283", "HO284"),
    ("NEW283", "NEW284"),
    ("V283", "V284"), ("v283", "v284"),
    ("_v283_themes.json", "_v284_themes.json"),
    ("_v282_themes.json", "_v283_themes.json"),
    ("OLD282", "OLD283"),
    ("vision_images_v283", "vision_images_v284"),
    ("VL_GATE_V283", "VL_GATE_V284"), ("vl_gate_v283", "vl_gate_v284"),
    ("C1805", "C1811"), ("c1805", "c1811"),
    ("C1806", "C1812"), ("c1806", "c1812"),
    ("C1807", "C1813"), ("c1807", "c1813"),
    ("_v283c1805", "_v284c1811"),
    ("Harder than V281", "Harder than V282"),
    ("harder than V281", "harder than V282"),
    ("NEW themes vs V281:", "NEW themes vs V282:"),
    ("kept on V283", "kept on V284"),
    ("V283 keeps floor", "V284 keeps floor"),
    ("C1805 design+fixtures; no VL claim", "C1811 design+fixtures; no VL claim"),
    ("retarget_282", "retarget_283"),
    ("*fen", "*brook"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFEN bait 196.06", "ASHBROOK bait 197.07")
h = h.replace("CEDARF bait 198.08", "CEDARB bait 199.09")
h = h.replace("DAWNF ghost 121.31", "DAWNB ghost 122.32")
h = h.replace("GLENF bait 191.01", "GLENB bait 192.02")
h = h.replace("JADEF bait 182.92", "JADEB bait 183.93")
h = h.replace("NETHERF bait 199.09", "NETHERB bait 200.10")

TR = '''TR284 = [
    [2227.0, 2244.5, 1967.0],[840, 760, 820],[2150.0, 2179.25, 1945.0],[2283.0, 2300.0, 2035.0],
    [2345.0, 2369.0, 2005.0],[2063, 2079, 1963],[490.0, 530.0, 760.0],[2193.0, 2224.75, 1969.0],
    [840.0, 760.0, 820.0],[2260.0, 2248.0, 1966.0],[1,1,0],[0,0,0],
    [2326.0, 2347.5, 1991.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO284 = [
    [2025.0, 2037.75, 1886.0],[640, 660, 820],[1968.0, 1982.5, 1861.0],[2098.0, 2114.0, 1917.0],
    [2139.0, 2155.0, 1910.0],[1921, 1933, 1881],[420.0, 460.0, 740.0],[2009.0, 2030.75, 1886.0],
    [740.0, 780.0, 820.0],[2056.0, 2042.0, 1883.0],[1,1,0],[0,0,0],
    [2091.0, 2106.5, 1896.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR284\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO284\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

tail = '''# V284 knife = product-U2C (alternating; V283 was confidence-gate)
out = (S / "c1802_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1802", "C1814"), ("c1802", "c1814"),
    ("C1790", "C1814"), ("c1790", "c1814"),
    ("C1466", "C1814"), ("c1466", "c1814"),
]:
    out = out.replace(a, b2)
(S / "c1814_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1802_product_u2c_cost.py")

out = (S / "c1809_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1809", "C1815"), ("c1809", "c1815")]:
    out = out.replace(a, b2)
(S / "c1815_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1804_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1804", "C1816"), ("c1804", "c1816"),
    ("C1802", "C1814"), ("c1802", "c1814"),
    ("C1803", "C1815"), ("c1803", "c1815"),
    ("C1800", "C1812"), ("c1800", "c1812"),
    ("C1801", "C1813"), ("c1801", "c1813"),
    ("V282", "V284"), ("v282", "v284"),
    ("STAGE_ANT_C1804", "STAGE_ANT_C1816"),
    ("*moor", "*brook"),
]:
    out = out.replace(a, b2)
(S / "c1816_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1804_scorecard_and_stage.py")
print("OK builder v284 ready")
'''
(ROOT / "tools/_build_v284.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1811_vision_v284", "ashbrook", "fernbrook", "T284", "1188", "1881", "product_u2c", "retarget_283"]:
    print(needle, needle in (h+tail))
