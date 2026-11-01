from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v327.py").read_text(encoding="utf-8")
idx0 = b0.find('# V327 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2074 = " in head0:
    head0 = head0[:head0.find("SC2074 = ")]

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
    ("T327", "T328"), ("TR327", "TR328"), ("HO327", "HO328"),
    ("NEW327", "NEW328"),
    ("V327", "V328"), ("v327", "v328"),
    ("_v327_themes.json", "_v328_themes.json"),
    ("_v326_themes.json", "_v327_themes.json"),
    ("OLD326", "OLD327"),
    ("vision_images_v327", "vision_images_v328"),
    ("VL_GATE_V327", "VL_GATE_V328"), ("vl_gate_v327", "vl_gate_v328"),
    ("C2069", "C2075"), ("c2069", "c2075"),
    ("C2070", "C2076"), ("c2070", "c2076"),
    ("C2071", "C2077"), ("c2071", "c2077"),
    ("_v327c2069", "_v328c2075"),
    ("Harder than V325", "Harder than V326"),
    ("harder than V325", "harder than V326"),
    ("NEW themes vs V325:", "NEW themes vs V326:"),
    ("kept on V327", "kept on V328"),
    ("V327 keeps floor", "V328 keeps floor"),
    ("C2069 design+fixtures; no VL claim", "C2075 design+fixtures; no VL claim"),
    ("retarget_326", "retarget_327"),
    ("*fen", "*brook"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFEN bait 240.50", "ASHBROOK bait 241.51")
h = h.replace("CEDARF bait 242.52", "CEDARB bait 243.53")
h = h.replace("DAWNF ghost 165.75", "DAWNB ghost 166.76")
h = h.replace("GLENF bait 235.45", "GLENB bait 236.46")
h = h.replace("JADEF bait 226.36", "JADEB bait 227.37")
h = h.replace("NETHERF bait 243.53", "NETHERB bait 244.54")

TR = '''TR328 = [
    [2320.0, 2337.5, 2060.0],[840, 760, 820],[2243.0, 2252.25, 2038.0],[2376.0, 2393.0, 2128.0],
    [2438.0, 2462.0, 2098.0],[2156, 2172, 2056],[490.0, 530.0, 760.0],[2286.0, 2317.75, 2062.0],
    [840.0, 760.0, 820.0],[2353.0, 2341.0, 2059.0],[1,1,0],[0,0,0],
    [2419.0, 2440.5, 2084.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO328 = [
    [2118.0, 2130.75, 1979.0],[640, 660, 820],[2061.0, 2075.5, 1954.0],[2191.0, 2207.0, 2010.0],
    [2232.0, 2248.0, 2003.0],[2014, 2026, 1976],[420.0, 460.0, 740.0],[2102.0, 2123.75, 1979.0],
    [740.0, 780.0, 820.0],[2149.0, 2135.0, 1976.0],[1,1,0],[0,0,0],
    [2184.0, 2199.5, 1989.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR328\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO328\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2068_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2068", "C2080"), ("c2068", "c2080"),
    ("C2066", "C2078"), ("c2066", "c2078"),
    ("C2067", "C2079"), ("c2067", "c2079"),
    ("C2064", "C2076"), ("c2064", "c2076"),
    ("C2065", "C2077"), ("c2065", "c2077"),
    ("C2060", "C2072"), ("c2060", "c2072"),
    ("C2063", "C2075"), ("c2063", "c2075"),
    ("V326", "V328"), ("v326", "v328"),
    ("STAGE_ANT_C2068", "STAGE_ANT_C2080"),
    ("*moor", "*brook"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V328 knife = product-U2C (alternating; V327 was confidence-gate)
out = (S / "c2066_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2066", "C2078"), ("c2066", "c2078"),
    ("C2054", "C2078"), ("c2054", "c2078"),
    ("product_u2c_cost_c2066", "product_u2c_cost_c2078"),
    ("u2c_v207", "u2c_v208"),
    ("u2c_c2066", "u2c_c2078"),
]:
    out = out.replace(a, b2)
(S / "c2078_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2066")

out = (S / "c2073_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2073", "C2079"), ("c2073", "c2079")]:
    out = out.replace(a, b2)
(S / "c2079_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2080_scorecard_and_stage.py").write_text(SC2080, encoding="utf-8")
print("scorecard from fixed c2068 product-U2C pattern")
print("OK builder v328 ready")
'''
pre = "SC2080 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v328.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2075_vision_v328", "ashbrook", "fernbrook", "T328", "1188", "1976", "product_u2c", "retarget_327", "2252.25"]:
    print(needle, needle in (h+pre+tail))
