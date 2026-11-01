from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v317.py").read_text(encoding="utf-8")
idx0 = b0.find('# V317 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2014 = " in head0:
    head0 = head0[:head0.find("SC2014 = ")]

theme_pairs = [
    ("netherbrook", "netherdale"), ("NETHERBROOK", "NETHERDALE"),
    ("cedarbrook", "cedardale"), ("CEDARBROOK", "CEDARDALE"),
    ("dawnbrook", "dawndale"), ("DAWNBROOK", "DAWNDALE"),
    ("fernbrook", "ferndale"), ("FERNBROOK", "FERNDALE"),
    ("glenbrook", "glendale"), ("GLENBROOK", "GLENDALE"),
    ("hazebrook", "hazedale"), ("HAZEBROOK", "HAZEDALE"),
    ("jadebrook", "jadedale"), ("JADEBROOK", "JADEDALE"),
    ("knotbrook", "knotdale"), ("KNOTBROOK", "KNOTDALE"),
    ("lakebrook", "lakedale"), ("LAKEBROOK", "LAKEDALE"),
    ("mossbrook", "mossdale"), ("MOSSBROOK", "MOSSDALE"),
    ("pinebrook", "pinedale"), ("PINEBROOK", "PINEDALE"),
    ("quillbrook", "quilldale"), ("QUILLBROOK", "QUILLDALE"),
    ("reedbrook", "reeddale"), ("REEDBROOK", "REEDDALE"),
    ("stonebrook", "stonedale"), ("STONEBROOK", "STONEDALE"),
    ("ashbrook", "ashdale"), ("ASHBROOK", "ASHDALE"),
    ("elmbrook", "elmdale"), ("ELMBROOK", "ELMDALE"),
    ("inkbrook", "inkdale"), ("INKBROOK", "INKDALE"),
    ("oakbrook", "oakdale"), ("OAKBROOK", "OAKDALE"),
]
pairs = [
    ("*brook ; stack mid-band", "*dale ; stack mid-band"),
    ("T317", "T318"), ("TR317", "TR318"), ("HO317", "HO318"),
    ("NEW317", "NEW318"),
    ("V317", "V318"), ("v317", "v318"),
    ("_v317_themes.json", "_v318_themes.json"),
    ("_v316_themes.json", "_v317_themes.json"),
    ("OLD316", "OLD317"),
    ("vision_images_v317", "vision_images_v318"),
    ("VL_GATE_V317", "VL_GATE_V318"), ("vl_gate_v317", "vl_gate_v318"),
    ("C2009", "C2015"), ("c2009", "c2015"),
    ("C2010", "C2016"), ("c2010", "c2016"),
    ("C2011", "C2017"), ("c2011", "c2017"),
    ("_v317c2009", "_v318c2015"),
    ("Harder than V315", "Harder than V316"),
    ("harder than V315", "harder than V316"),
    ("NEW themes vs V315:", "NEW themes vs V316:"),
    ("kept on V317", "kept on V318"),
    ("V317 keeps floor", "V318 keeps floor"),
    ("C2009 design+fixtures; no VL claim", "C2015 design+fixtures; no VL claim"),
    ("retarget_316", "retarget_317"),
    ("*brook", "*dale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHBROOK bait 230.40", "ASHDALE bait 231.41")
h = h.replace("CEDARB bait 232.42", "CEDARD bait 233.43")
h = h.replace("DAWNB ghost 155.65", "DAWND ghost 156.66")
h = h.replace("GLENB bait 225.35", "GLEND bait 226.36")
h = h.replace("JADEB bait 216.26", "JADED bait 217.27")
h = h.replace("NETHERB bait 233.43", "NETHERD bait 234.44")

TR = '''TR318 = [
    [2300.0, 2317.5, 2040.0],[840, 760, 820],[2223.0, 2252.25, 2018.0],[2356.0, 2373.0, 2108.0],
    [2418.0, 2442.0, 2078.0],[2136, 2152, 2036],[490.0, 530.0, 760.0],[2266.0, 2297.75, 2042.0],
    [840.0, 760.0, 820.0],[2333.0, 2321.0, 2039.0],[1,1,0],[0,0,0],
    [2399.0, 2420.5, 2064.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO318 = [
    [2098.0, 2110.75, 1959.0],[640, 660, 820],[2041.0, 2055.5, 1934.0],[2171.0, 2187.0, 1990.0],
    [2212.0, 2228.0, 1983.0],[1994, 2006, 1954],[420.0, 460.0, 740.0],[2082.0, 2103.75, 1959.0],
    [740.0, 780.0, 820.0],[2129.0, 2115.0, 1956.0],[1,1,0],[0,0,0],
    [2164.0, 2179.5, 1969.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR318\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO318\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2008_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2008", "C2020"), ("c2008", "c2020"),
    ("C2006", "C2018"), ("c2006", "c2018"),
    ("C2007", "C2019"), ("c2007", "c2019"),
    ("C2004", "C2016"), ("c2004", "c2016"),
    ("C2005", "C2017"), ("c2005", "c2017"),
    ("C2000", "C2012"), ("c2000", "c2012"),
    ("C2003", "C2015"), ("c2003", "c2015"),
    ("V316", "V318"), ("v316", "v318"),
    ("STAGE_ANT_C2008", "STAGE_ANT_C2020"),
    ("*fen", "*dale"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V318 knife = product-U2C (alternating; V317 was confidence-gate)
out = (S / "c2006_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2006", "C2018"), ("c2006", "c2018"),
    ("C1994", "C2018"), ("c1994", "c2018"),
    ("product_u2c_cost_c2006", "product_u2c_cost_c2018"),
    ("u2c_v202", "u2c_v203"),
    ("u2c_c2006", "u2c_c2018"),
]:
    out = out.replace(a, b2)
(S / "c2018_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2006")

out = (S / "c2013_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2013", "C2019"), ("c2013", "c2019")]:
    out = out.replace(a, b2)
(S / "c2019_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2020_scorecard_and_stage.py").write_text(SC2020, encoding="utf-8")
print("scorecard from fixed c2008 product-U2C pattern")
print("OK builder v318 ready")
'''
pre = "SC2020 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v318.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2015_vision_v318", "ashdale", "ferndale", "T318", "1188", "1954", "product_u2c", "retarget_317"]:
    print(needle, needle in (h+pre+tail))
