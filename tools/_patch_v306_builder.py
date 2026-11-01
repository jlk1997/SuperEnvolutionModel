from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v305.py").read_text(encoding="utf-8")
idx0 = b0.find('# V305 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1942 = " in head0:
    head0 = head0[:head0.find("SC1942 = ")]

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
    ("T305", "T306"), ("TR305", "TR306"), ("HO305", "HO306"),
    ("NEW305", "NEW306"),
    ("V305", "V306"), ("v305", "v306"),
    ("_v305_themes.json", "_v306_themes.json"),
    ("_v304_themes.json", "_v305_themes.json"),
    ("OLD304", "OLD305"),
    ("vision_images_v305", "vision_images_v306"),
    ("VL_GATE_V305", "VL_GATE_V306"), ("vl_gate_v305", "vl_gate_v306"),
    ("C1937", "C1943"), ("c1937", "c1943"),
    ("C1938", "C1944"), ("c1938", "c1944"),
    ("C1939", "C1945"), ("c1939", "c1945"),
    ("_v305c1937", "_v306c1943"),
    ("Harder than V303", "Harder than V304"),
    ("harder than V303", "harder than V304"),
    ("NEW themes vs V303:", "NEW themes vs V304:"),
    ("kept on V305", "kept on V306"),
    ("V305 keeps floor", "V306 keeps floor"),
    ("C1937 design+fixtures; no VL claim", "C1943 design+fixtures; no VL claim"),
    ("retarget_304", "retarget_305"),
    ("*fen", "*brook"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFEN bait 218.28", "ASHBROOK bait 219.29")
h = h.replace("CEDARF bait 220.30", "CEDARB bait 221.31")
h = h.replace("DAWNF ghost 143.53", "DAWNB ghost 144.54")
h = h.replace("GLENF bait 213.23", "GLENB bait 214.24")
h = h.replace("JADEF bait 204.14", "JADEB bait 205.15")
h = h.replace("NETHERF bait 221.31", "NETHERB bait 222.32")

TR = '''TR306 = [
    [2276.0, 2293.5, 2016.0],[840, 760, 820],[2199.0, 2228.25, 1994.0],[2332.0, 2349.0, 2084.0],
    [2394.0, 2418.0, 2054.0],[2112, 2128, 2012],[490.0, 530.0, 760.0],[2242.0, 2273.75, 2018.0],
    [840.0, 760.0, 820.0],[2309.0, 2297.0, 2015.0],[1,1,0],[0,0,0],
    [2375.0, 2396.5, 2040.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO306 = [
    [2074.0, 2086.75, 1935.0],[640, 660, 820],[2017.0, 2031.5, 1910.0],[2147.0, 2163.0, 1966.0],
    [2188.0, 2204.0, 1959.0],[1970, 1982, 1930],[420.0, 460.0, 740.0],[2058.0, 2079.75, 1935.0],
    [740.0, 780.0, 820.0],[2105.0, 2091.0, 1932.0],[1,1,0],[0,0,0],
    [2140.0, 2155.5, 1945.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR306\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO306\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c1936_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1936", "C1948"), ("c1936", "c1948"),
    ("C1934", "C1946"), ("c1934", "c1946"),
    ("C1935", "C1947"), ("c1935", "c1947"),
    ("C1932", "C1944"), ("c1932", "c1944"),
    ("C1933", "C1945"), ("c1933", "c1945"),
    ("C1928", "C1940"), ("c1928", "c1940"),
    ("C1931", "C1943"), ("c1931", "c1943"),
    ("V304", "V306"), ("v304", "v306"),
    ("STAGE_ANT_C1936", "STAGE_ANT_C1948"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V306 knife = product-U2C (alternating; V305 was confidence-gate)
out = (S / "c1934_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1934", "C1946"), ("c1934", "c1946"),
    ("C1922", "C1946"), ("c1922", "c1946"),
    ("product_u2c_cost_c1934", "product_u2c_cost_c1946"),
    ("u2c_v196", "u2c_v197"),
    ("u2c_c1934", "u2c_c1946"),
]:
    out = out.replace(a, b2)
(S / "c1946_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1934")

out = (S / "c1941_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1941", "C1947"), ("c1941", "c1947")]:
    out = out.replace(a, b2)
(S / "c1947_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1948_scorecard_and_stage.py").write_text(SC1948, encoding="utf-8")
print("scorecard from fixed c1936 product-U2C pattern")
print("OK builder v306 ready")
'''
pre = "SC1948 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v306.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1943_vision_v306", "ashbrook", "fernbrook", "T306", "1188", "1930", "product_u2c", "retarget_305"]:
    print(needle, needle in (h+pre+tail))
