from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v295.py").read_text(encoding="utf-8")
idx0 = b0.find('# V295 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1882 = " in head0:
    head0 = head0[:head0.find("SC1882 = ")]

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
    ("T295", "T296"), ("TR295", "TR296"), ("HO295", "HO296"),
    ("NEW295", "NEW296"),
    ("V295", "V296"), ("v295", "v296"),
    ("_v295_themes.json", "_v296_themes.json"),
    ("_v294_themes.json", "_v295_themes.json"),
    ("OLD294", "OLD295"),
    ("vision_images_v295", "vision_images_v296"),
    ("VL_GATE_V295", "VL_GATE_V296"), ("vl_gate_v295", "vl_gate_v296"),
    ("C1877", "C1883"), ("c1877", "c1883"),
    ("C1878", "C1884"), ("c1878", "c1884"),
    ("C1879", "C1885"), ("c1879", "c1885"),
    ("_v295c1877", "_v296c1883"),
    ("Harder than V293", "Harder than V294"),
    ("harder than V293", "harder than V294"),
    ("NEW themes vs V293:", "NEW themes vs V294:"),
    ("kept on V295", "kept on V296"),
    ("V295 keeps floor", "V296 keeps floor"),
    ("C1877 design+fixtures; no VL claim", "C1883 design+fixtures; no VL claim"),
    ("retarget_294", "retarget_295"),
    ("*brook", "*dale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHBROOK bait 208.18", "ASHDALE bait 209.19")
h = h.replace("CEDARB bait 210.20", "CEDARD bait 211.21")
h = h.replace("DAWNB ghost 133.43", "DAWND ghost 134.44")
h = h.replace("GLENB bait 203.13", "GLEND bait 204.14")
h = h.replace("JADEB bait 194.04", "JADED bait 195.05")
h = h.replace("NETHERB bait 211.21", "NETHERD bait 212.22")

TR = '''TR296 = [
    [2256.0, 2273.5, 1996.0],[840, 760, 820],[2179.0, 2208.25, 1974.0],[2312.0, 2329.0, 2064.0],
    [2374.0, 2398.0, 2034.0],[2092, 2108, 1992],[490.0, 530.0, 760.0],[2222.0, 2253.75, 1998.0],
    [840.0, 760.0, 820.0],[2289.0, 2277.0, 1995.0],[1,1,0],[0,0,0],
    [2355.0, 2376.5, 2020.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO296 = [
    [2054.0, 2066.75, 1915.0],[640, 660, 820],[1997.0, 2011.5, 1890.0],[2127.0, 2143.0, 1946.0],
    [2168.0, 2184.0, 1939.0],[1950, 1962, 1910],[420.0, 460.0, 740.0],[2038.0, 2059.75, 1915.0],
    [740.0, 780.0, 820.0],[2085.0, 2071.0, 1912.0],[1,1,0],[0,0,0],
    [2120.0, 2135.5, 1925.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR296\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO296\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c1876_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1876", "C1888"), ("c1876", "c1888"),
    ("C1874", "C1886"), ("c1874", "c1886"),
    ("C1875", "C1887"), ("c1875", "c1887"),
    ("C1872", "C1884"), ("c1872", "c1884"),
    ("C1873", "C1885"), ("c1873", "c1885"),
    ("C1868", "C1880"), ("c1868", "c1880"),
    ("C1871", "C1883"), ("c1871", "c1883"),
    ("V294", "V296"), ("v294", "v296"),
    ("STAGE_ANT_C1876", "STAGE_ANT_C1888"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V296 knife = product-U2C (alternating; V295 was confidence-gate)
out = (S / "c1874_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1874", "C1886"), ("c1874", "c1886"),
    ("C1862", "C1886"), ("c1862", "c1886"),
    ("product_u2c_cost_c1874", "product_u2c_cost_c1886"),
    ("u2c_v191", "u2c_v192"),
    ("u2c_c1874", "u2c_c1886"),
]:
    out = out.replace(a, b2)
(S / "c1886_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1874")

out = (S / "c1881_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1881", "C1887"), ("c1881", "c1887")]:
    out = out.replace(a, b2)
(S / "c1887_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1888_scorecard_and_stage.py").write_text(SC1888, encoding="utf-8")
print("scorecard from fixed c1876 product-U2C pattern")
print("OK builder v296 ready")
'''
pre = "SC1888 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v296.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1883_vision_v296", "ashdale", "ferndale", "T296", "1188", "1910", "product_u2c", "retarget_295"]:
    print(needle, needle in (h+pre+tail))
