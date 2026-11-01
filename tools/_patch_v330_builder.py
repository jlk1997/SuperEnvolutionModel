from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v329.py").read_text(encoding="utf-8")
idx0 = b0.find('# V329 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2086 = " in head0:
    head0 = head0[:head0.find("SC2086 = ")]

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
    ("T329", "T330"), ("TR329", "TR330"), ("HO329", "HO330"),
    ("NEW329", "NEW330"),
    ("V329", "V330"), ("v329", "v330"),
    ("_v329_themes.json", "_v330_themes.json"),
    ("_v328_themes.json", "_v329_themes.json"),
    ("OLD328", "OLD329"),
    ("vision_images_v329", "vision_images_v330"),
    ("VL_GATE_V329", "VL_GATE_V330"), ("vl_gate_v329", "vl_gate_v330"),
    ("C2081", "C2087"), ("c2081", "c2087"),
    ("C2082", "C2088"), ("c2082", "c2088"),
    ("C2083", "C2089"), ("c2083", "c2089"),
    ("_v329c2081", "_v330c2087"),
    ("Harder than V327", "Harder than V328"),
    ("harder than V327", "harder than V328"),
    ("NEW themes vs V327:", "NEW themes vs V328:"),
    ("kept on V329", "kept on V330"),
    ("V329 keeps floor", "V330 keeps floor"),
    ("C2081 design+fixtures; no VL claim", "C2087 design+fixtures; no VL claim"),
    ("retarget_328", "retarget_329"),
    ("*dale", "*ford"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHDALE bait 242.52", "ASHFORD bait 243.53")
h = h.replace("CEDARD bait 244.54", "CEDARF bait 245.55")
h = h.replace("DAWND ghost 167.77", "DAWNF ghost 168.78")
h = h.replace("GLEND bait 237.47", "GLENF bait 238.48")
h = h.replace("JADED bait 228.38", "JADEF bait 229.39")
h = h.replace("NETHERD bait 245.55", "NETHERF bait 246.56")

TR = '''TR330 = [
    [2324.0, 2341.5, 2064.0],[840, 760, 820],[2247.0, 2256.25, 2042.0],[2380.0, 2397.0, 2132.0],
    [2442.0, 2466.0, 2102.0],[2160, 2176, 2060],[490.0, 530.0, 760.0],[2290.0, 2321.75, 2066.0],
    [840.0, 760.0, 820.0],[2357.0, 2345.0, 2063.0],[1,1,0],[0,0,0],
    [2423.0, 2444.5, 2088.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO330 = [
    [2122.0, 2134.75, 1983.0],[640, 660, 820],[2065.0, 2079.5, 1958.0],[2195.0, 2211.0, 2014.0],
    [2236.0, 2252.0, 2007.0],[2018, 2030, 1980],[420.0, 460.0, 740.0],[2106.0, 2127.75, 1983.0],
    [740.0, 780.0, 820.0],[2153.0, 2139.0, 1980.0],[1,1,0],[0,0,0],
    [2188.0, 2203.5, 1993.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR330\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO330\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2080_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2080", "C2092"), ("c2080", "c2092"),
    ("C2078", "C2090"), ("c2078", "c2090"),
    ("C2079", "C2091"), ("c2079", "c2091"),
    ("C2076", "C2088"), ("c2076", "c2088"),
    ("C2077", "C2089"), ("c2077", "c2089"),
    ("C2072", "C2084"), ("c2072", "c2084"),
    ("C2075", "C2087"), ("c2075", "c2087"),
    ("V328", "V330"), ("v328", "v330"),
    ("STAGE_ANT_C2080", "STAGE_ANT_C2092"),
    ("*brook", "*ford"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V330 knife = product-U2C (alternating; V329 was confidence-gate)
out = (S / "c2078_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2078", "C2090"), ("c2078", "c2090"),
    ("C2066", "C2090"), ("c2066", "c2090"),
    ("product_u2c_cost_c2078", "product_u2c_cost_c2090"),
    ("u2c_v208", "u2c_v209"),
    ("u2c_c2078", "u2c_c2090"),
]:
    out = out.replace(a, b2)
(S / "c2090_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2078")

out = (S / "c2085_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2085", "C2091"), ("c2085", "c2091")]:
    out = out.replace(a, b2)
(S / "c2091_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2092_scorecard_and_stage.py").write_text(SC2092, encoding="utf-8")
print("scorecard from fixed c2080 product-U2C pattern")
print("OK builder v330 ready")
'''
pre = "SC2092 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v330.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2087_vision_v330", "ashford", "fernford", "T330", "1188", "1980", "product_u2c", "retarget_329", "2256.25"]:
    print(needle, needle in (h+pre+tail))
