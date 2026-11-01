from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v293.py").read_text(encoding="utf-8")
idx0 = b0.find('# V293 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
# strip SC1870 assignment if present in head
if "SC1870 = " in head0:
    head0 = head0[:head0.find("SC1870 = ")]

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
    ("T293", "T294"), ("TR293", "TR294"), ("HO293", "HO294"),
    ("NEW293", "NEW294"),
    ("V293", "V294"), ("v293", "v294"),
    ("_v293_themes.json", "_v294_themes.json"),
    ("_v292_themes.json", "_v293_themes.json"),
    ("OLD292", "OLD293"),
    ("vision_images_v293", "vision_images_v294"),
    ("VL_GATE_V293", "VL_GATE_V294"), ("vl_gate_v293", "vl_gate_v294"),
    ("C1865", "C1871"), ("c1865", "c1871"),
    ("C1866", "C1872"), ("c1866", "c1872"),
    ("C1867", "C1873"), ("c1867", "c1873"),
    ("_v293c1865", "_v294c1871"),
    ("Harder than V291", "Harder than V292"),
    ("harder than V291", "harder than V292"),
    ("NEW themes vs V291:", "NEW themes vs V292:"),
    ("kept on V293", "kept on V294"),
    ("V293 keeps floor", "V294 keeps floor"),
    ("C1865 design+fixtures; no VL claim", "C1871 design+fixtures; no VL claim"),
    ("retarget_292", "retarget_293"),
    ("*moor", "*fen"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMOOR bait 206.16", "ASHFEN bait 207.17")
h = h.replace("CEDARM bait 208.18", "CEDARF bait 209.19")
h = h.replace("DAWNM ghost 131.41", "DAWNF ghost 132.42")
h = h.replace("GLENM bait 201.11", "GLENF bait 202.12")
h = h.replace("JADEM bait 192.02", "JADEF bait 193.03")
h = h.replace("NETHERM bait 209.19", "NETHERF bait 210.20")

TR = '''TR294 = [
    [2252.0, 2269.5, 1992.0],[840, 760, 820],[2175.0, 2204.25, 1970.0],[2308.0, 2325.0, 2060.0],
    [2370.0, 2394.0, 2030.0],[2088, 2104, 1988],[490.0, 530.0, 760.0],[2218.0, 2249.75, 1994.0],
    [840.0, 760.0, 820.0],[2285.0, 2273.0, 1991.0],[1,1,0],[0,0,0],
    [2351.0, 2372.5, 2016.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO294 = [
    [2050.0, 2062.75, 1911.0],[640, 660, 820],[1993.0, 2007.5, 1886.0],[2123.0, 2139.0, 1942.0],
    [2164.0, 2180.0, 1935.0],[1946, 1958, 1906],[420.0, 460.0, 740.0],[2034.0, 2055.75, 1911.0],
    [740.0, 780.0, 820.0],[2081.0, 2067.0, 1908.0],[1,1,0],[0,0,0],
    [2116.0, 2131.5, 1921.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR294\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO294\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

# Fixed product-U2C scorecard from c1864
sc_body = (ROOT / "scripts/c1864_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1864", "C1876"), ("c1864", "c1876"),
    ("C1862", "C1874"), ("c1862", "c1874"),
    ("C1863", "C1875"), ("c1863", "c1875"),
    ("C1860", "C1872"), ("c1860", "c1872"),
    ("C1861", "C1873"), ("c1861", "c1873"),
    ("C1856", "C1868"), ("c1856", "c1868"),
    ("C1859", "C1871"), ("c1859", "c1871"),
    ("V292", "V294"), ("v292", "v294"),
    ("STAGE_ANT_C1864", "STAGE_ANT_C1876"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V294 knife = product-U2C (alternating; V293 was confidence-gate)
out = (S / "c1862_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1862", "C1874"), ("c1862", "c1874"),
    ("C1850", "C1874"), ("c1850", "c1874"),
    ("product_u2c_cost_c1862", "product_u2c_cost_c1874"),
    ("u2c_v190", "u2c_v191"),
    ("u2c_c1862", "u2c_c1874"),
]:
    out = out.replace(a, b2)
(S / "c1874_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1862")

out = (S / "c1869_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1869", "C1875"), ("c1869", "c1875")]:
    out = out.replace(a, b2)
(S / "c1875_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1876_scorecard_and_stage.py").write_text(SC1876, encoding="utf-8")
print("scorecard from fixed c1864 product-U2C pattern")
print("OK builder v294 ready")
'''
pre = "SC1876 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v294.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1871_vision_v294", "ashfen", "fernfen", "T294", "1188", "1906", "product_u2c", "retarget_293"]:
    print(needle, needle in (h+pre+tail))
