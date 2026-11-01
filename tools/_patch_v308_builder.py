from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v307.py").read_text(encoding="utf-8")
idx0 = b0.find('# V307 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1954 = " in head0:
    head0 = head0[:head0.find("SC1954 = ")]

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
    ("T307", "T308"), ("TR307", "TR308"), ("HO307", "HO308"),
    ("NEW307", "NEW308"),
    ("V307", "V308"), ("v307", "v308"),
    ("_v307_themes.json", "_v308_themes.json"),
    ("_v306_themes.json", "_v307_themes.json"),
    ("OLD306", "OLD307"),
    ("vision_images_v307", "vision_images_v308"),
    ("VL_GATE_V307", "VL_GATE_V308"), ("vl_gate_v307", "vl_gate_v308"),
    ("C1949", "C1955"), ("c1949", "c1955"),
    ("C1950", "C1956"), ("c1950", "c1956"),
    ("C1951", "C1957"), ("c1951", "c1957"),
    ("_v307c1949", "_v308c1955"),
    ("Harder than V305", "Harder than V306"),
    ("harder than V305", "harder than V306"),
    ("NEW themes vs V305:", "NEW themes vs V306:"),
    ("kept on V307", "kept on V308"),
    ("V307 keeps floor", "V308 keeps floor"),
    ("C1949 design+fixtures; no VL claim", "C1955 design+fixtures; no VL claim"),
    ("retarget_306", "retarget_307"),
    ("*dale", "*ford"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHDALE bait 220.30", "ASHFORD bait 221.31")
h = h.replace("CEDARD bait 222.32", "CEDARF bait 223.33")
h = h.replace("DAWND ghost 145.55", "DAWNF ghost 146.56")
h = h.replace("GLEND bait 215.25", "GLENF bait 216.26")
h = h.replace("JADED bait 206.16", "JADEF bait 207.17")
h = h.replace("NETHERD bait 223.33", "NETHERF bait 224.34")

TR = '''TR308 = [
    [2280.0, 2297.5, 2020.0],[840, 760, 820],[2203.0, 2232.25, 1998.0],[2336.0, 2353.0, 2088.0],
    [2398.0, 2422.0, 2058.0],[2116, 2132, 2016],[490.0, 530.0, 760.0],[2246.0, 2277.75, 2022.0],
    [840.0, 760.0, 820.0],[2313.0, 2301.0, 2019.0],[1,1,0],[0,0,0],
    [2379.0, 2400.5, 2044.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO308 = [
    [2078.0, 2090.75, 1939.0],[640, 660, 820],[2021.0, 2035.5, 1914.0],[2151.0, 2167.0, 1970.0],
    [2192.0, 2208.0, 1963.0],[1974, 1986, 1934],[420.0, 460.0, 740.0],[2062.0, 2083.75, 1939.0],
    [740.0, 780.0, 820.0],[2109.0, 2095.0, 1936.0],[1,1,0],[0,0,0],
    [2144.0, 2159.5, 1949.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR308\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO308\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c1948_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1948", "C1960"), ("c1948", "c1960"),
    ("C1946", "C1958"), ("c1946", "c1958"),
    ("C1947", "C1959"), ("c1947", "c1959"),
    ("C1944", "C1956"), ("c1944", "c1956"),
    ("C1945", "C1957"), ("c1945", "c1957"),
    ("C1940", "C1952"), ("c1940", "c1952"),
    ("C1943", "C1955"), ("c1943", "c1955"),
    ("V306", "V308"), ("v306", "v308"),
    ("STAGE_ANT_C1948", "STAGE_ANT_C1960"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V308 knife = product-U2C (alternating; V307 was confidence-gate)
out = (S / "c1946_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1946", "C1958"), ("c1946", "c1958"),
    ("C1934", "C1958"), ("c1934", "c1958"),
    ("product_u2c_cost_c1946", "product_u2c_cost_c1958"),
    ("u2c_v197", "u2c_v198"),
    ("u2c_c1946", "u2c_c1958"),
]:
    out = out.replace(a, b2)
(S / "c1958_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1946")

out = (S / "c1953_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1953", "C1959"), ("c1953", "c1959")]:
    out = out.replace(a, b2)
(S / "c1959_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1960_scorecard_and_stage.py").write_text(SC1960, encoding="utf-8")
print("scorecard from fixed c1948 product-U2C pattern")
print("OK builder v308 ready")
'''
pre = "SC1960 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v308.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1955_vision_v308", "ashford", "fernford", "T308", "1188", "1934", "product_u2c", "retarget_307"]:
    print(needle, needle in (h+pre+tail))
