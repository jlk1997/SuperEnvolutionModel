from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v337.py").read_text(encoding="utf-8")
idx0 = b0.find('# V337 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2134 = " in head0:
    head0 = head0[:head0.find("SC2134 = ")]

theme_pairs = [
    ("nethermoor", "netherfen"), ("NETHERMOOR", "NETHERFEN"),
    ("cedarmoor", "cedarfen"), ("CEDARMOOR", "CEDARFEN"),
    ("dawnmoor", "dawnfen"), ("DAWNMOOR", "DAWNFEN"),
    ("fernmoor", "fernfen"), ("FERNMOOR", "FERNFEN"),
    ("glenmoor", "glenfen"), ("GLENMOOR", "GLENFEN"),
    ("hazemoor", "hazefen"), ("HAZEMOOR", "HAZEFEN"),
    ("jademoor", "jadefen"), ("JADEMOOR", "JADEFEN"),
    ("knotmoor", "knotfen"), ("KNOTMOOR", "KNOTFEN"),
    ("lakemoor", "lakefen"), ("LAKEMOOR", "LAKEFEN"),
    ("mossmoor", "mossfen"), ("MOSSMOOR", "MOSSFEN"),
    ("pinemoor", "pinefen"), ("PINEMOOR", "PINEFEN"),
    ("quillmoor", "quillfen"), ("QUILLMOOR", "QUILLFEN"),
    ("reedmoor", "reedfen"), ("REEDMOOR", "REEDFEN"),
    ("stonemoor", "stonefen"), ("STONEMOOR", "STONEFEN"),
    ("ashmoor", "ashfen"), ("ASHMOOR", "ASHFEN"),
    ("elmmoor", "elmfen"), ("ELMMOOR", "ELMFEN"),
    ("inkmoor", "inkfen"), ("INKMOOR", "INKFEN"),
    ("oakmoor", "oakfen"), ("OAKMOOR", "OAKFEN"),
]
pairs = [
    ("*moor ; stack mid-band", "*fen ; stack mid-band"),
    ("T337", "T338"), ("TR337", "TR338"), ("HO337", "HO338"),
    ("NEW337", "NEW338"),
    ("V337", "V338"), ("v337", "v338"),
    ("_v337_themes.json", "_v338_themes.json"),
    ("_v336_themes.json", "_v337_themes.json"),
    ("OLD336", "OLD337"),
    ("vision_images_v337", "vision_images_v338"),
    ("VL_GATE_V337", "VL_GATE_V338"), ("vl_gate_v337", "vl_gate_v338"),
    ("C2129", "C2135"), ("c2129", "c2135"),
    ("C2130", "C2136"), ("c2130", "c2136"),
    ("C2131", "C2137"), ("c2131", "c2137"),
    ("_v337c2129", "_v338c2135"),
    ("Harder than V335", "Harder than V336"),
    ("harder than V335", "harder than V336"),
    ("NEW themes vs V335:", "NEW themes vs V336:"),
    ("kept on V337", "kept on V338"),
    ("V337 keeps floor", "V338 keeps floor"),
    ("C2135 design+fixtures; no VL claim", "C2135 design+fixtures; no VL claim"),
    ("retarget_336", "retarget_337"),
    ("*moor", "*fen"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFEN bait 249.59", "ASHFEN bait 247.57")
h = h.replace("CEDARF bait 253.63", "CEDARF bait 253.63")
h = h.replace("DAWNF ghost 176.86", "DAWNF ghost 176.86")
h = h.replace("GLENF bait 246.56", "GLENF bait 246.56")
h = h.replace("JADEF bait 237.47", "JADEF bait 237.47")
h = h.replace("NETHERF bait 254.64", "NETHERF bait 254.64")

TR = '''TR338 = [
    [2340.0, 2357.5, 2080.0],[840, 760, 820],[2251.0, 2257.25, 2051.0],[2396.0, 2413.0, 2148.0],
    [2458.0, 2482.0, 2118.0],[2176, 2192, 2076],[490.0, 530.0, 760.0],[2306.0, 2337.75, 2082.0],
    [840.0, 760.0, 820.0],[2373.0, 2361.0, 2079.0],[1,1,0],[0,0,0],
    [2439.0, 2460.5, 2104.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO338 = [
    [2138.0, 2150.75, 1999.0],[640, 660, 820],[2081.0, 2095.5, 1974.0],[2211.0, 2227.0, 2030.0],
    [2240.0, 2251.0, 2023.0],[2034, 2046, 1996],[420.0, 460.0, 740.0],[2122.0, 2143.75, 1999.0],
    [740.0, 780.0, 820.0],[2169.0, 2155.0, 1996.0],[1,1,0],[0,0,0],
    [2204.0, 2219.5, 2009.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR338\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO338\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2140"), ("c2092", "c2140"),
    ("C2090", "C2138"), ("c2090", "c2138"),
    ("C2091", "C2139"), ("c2091", "c2139"),
    ("C2088", "C2136"), ("c2088", "c2136"),
    ("C2089", "C2137"), ("c2089", "c2137"),
    ("C2084", "C2132"), ("c2084", "c2132"),
    ("C2087", "C2135"), ("c2087", "c2135"),
    ("V330", "V338"), ("v330", "v338"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2140"),
    ("*ford", "*fen"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V338 knife = product-U2C (alternating; V337 was confidence-gate)
out = (S / "c2126_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2126", "C2138"), ("c2126", "c2138"),
    ("C2090", "C2138"), ("c2090", "c2138"),
    ("product_u2c_cost_c2138", "product_u2c_cost_c2138"),
    ("u2c_v214", "u2c_v211"),
    ("u2c_c2138", "u2c_c2138"),
]:
    out = out.replace(a, b2)
(S / "c2138_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2126")

out = (S / "c2133_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2133", "C2139"), ("c2133", "c2139")]:
    out = out.replace(a, b2)
(S / "c2139_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2140_scorecard_and_stage.py").write_text(SC2140, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v338 ready")
'''
pre = "SC2140 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v338.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2135_vision_v338", "ashfen", "fernfen", "T338", "1188", "1996", "product_u2c", "retarget_337", "2257.25"]:
    print(needle, needle in (h+pre+tail))
