from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v297.py").read_text(encoding="utf-8")
idx0 = b0.find('# V297 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1894 = " in head0:
    head0 = head0[:head0.find("SC1894 = ")]

theme_pairs = [
    ("netherford", "netherhurst"), ("NETHERFORD", "NETHERHURST"),
    ("cedarford", "cedarhurst"), ("CEDARFORD", "CEDARHURST"),
    ("dawnford", "dawnhurst"), ("DAWNFORD", "DAWNHURST"),
    ("fernford", "fernhurst"), ("FERNFORD", "FERNHURST"),
    ("glenford", "glenhurst"), ("GLENFORD", "GLENHURST"),
    ("hazeford", "hazehurst"), ("HAZEFORD", "HAZEHURST"),
    ("jadeford", "jadehurst"), ("JADEFORD", "JADEHURST"),
    ("knotford", "knothurst"), ("KNOTFORD", "KNOTHURST"),
    ("lakeford", "lakehurst"), ("LAKEFORD", "LAKEHURST"),
    ("mossford", "mosshurst"), ("MOSSFORD", "MOSSHURST"),
    ("pineford", "pinehurst"), ("PINEFORD", "PINEHURST"),
    ("quillford", "quillhurst"), ("QUILLFORD", "QUILLHURST"),
    ("reedford", "reedhurst"), ("REEDFORD", "REEDHURST"),
    ("stoneford", "stonehurst"), ("STONEFORD", "STONEHURST"),
    ("ashford", "ashhurst"), ("ASHFORD", "ASHHURST"),
    ("elmford", "elmhurst"), ("ELMFORD", "ELMHURST"),
    ("inkford", "inkhurst"), ("INKFORD", "INKHURST"),
    ("oakford", "oakhurst"), ("OAKFORD", "OAKHURST"),
]
pairs = [
    ("*ford ; stack mid-band", "*hurst ; stack mid-band"),
    ("T297", "T298"), ("TR297", "TR298"), ("HO297", "HO298"),
    ("NEW297", "NEW298"),
    ("V297", "V298"), ("v297", "v298"),
    ("_v297_themes.json", "_v298_themes.json"),
    ("_v296_themes.json", "_v297_themes.json"),
    ("OLD296", "OLD297"),
    ("vision_images_v297", "vision_images_v298"),
    ("VL_GATE_V297", "VL_GATE_V298"), ("vl_gate_v297", "vl_gate_v298"),
    ("C1889", "C1895"), ("c1889", "c1895"),
    ("C1890", "C1896"), ("c1890", "c1896"),
    ("C1891", "C1897"), ("c1891", "c1897"),
    ("_v297c1889", "_v298c1895"),
    ("Harder than V295", "Harder than V296"),
    ("harder than V295", "harder than V296"),
    ("NEW themes vs V295:", "NEW themes vs V296:"),
    ("kept on V297", "kept on V298"),
    ("V297 keeps floor", "V298 keeps floor"),
    ("C1889 design+fixtures; no VL claim", "C1895 design+fixtures; no VL claim"),
    ("retarget_296", "retarget_297"),
    ("*ford", "*hurst"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFORD bait 210.20", "ASHHURST bait 211.21")
h = h.replace("CEDARF bait 212.22", "CEDARH bait 213.23")
h = h.replace("DAWNF ghost 135.45", "DAWNH ghost 136.46")
h = h.replace("GLENF bait 205.15", "GLENH bait 206.16")
h = h.replace("JADEF bait 196.06", "JADEH bait 197.07")
h = h.replace("NETHERF bait 213.23", "NETHERH bait 214.24")

TR = '''TR298 = [
    [2260.0, 2277.5, 2000.0],[840, 760, 820],[2183.0, 2212.25, 1978.0],[2316.0, 2333.0, 2068.0],
    [2378.0, 2402.0, 2038.0],[2096, 2112, 1996],[490.0, 530.0, 760.0],[2226.0, 2257.75, 2002.0],
    [840.0, 760.0, 820.0],[2293.0, 2281.0, 1999.0],[1,1,0],[0,0,0],
    [2359.0, 2380.5, 2024.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO298 = [
    [2058.0, 2070.75, 1919.0],[640, 660, 820],[2001.0, 2015.5, 1894.0],[2131.0, 2147.0, 1950.0],
    [2172.0, 2188.0, 1943.0],[1954, 1966, 1914],[420.0, 460.0, 740.0],[2042.0, 2063.75, 1919.0],
    [740.0, 780.0, 820.0],[2089.0, 2075.0, 1916.0],[1,1,0],[0,0,0],
    [2124.0, 2139.5, 1929.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR298\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO298\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c1888_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1888", "C1900"), ("c1888", "c1900"),
    ("C1886", "C1898"), ("c1886", "c1898"),
    ("C1887", "C1899"), ("c1887", "c1899"),
    ("C1884", "C1896"), ("c1884", "c1896"),
    ("C1885", "C1897"), ("c1885", "c1897"),
    ("C1880", "C1892"), ("c1880", "c1892"),
    ("C1883", "C1895"), ("c1883", "c1895"),
    ("V296", "V298"), ("v296", "v298"),
    ("STAGE_ANT_C1888", "STAGE_ANT_C1900"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V298 knife = product-U2C (alternating; V297 was confidence-gate)
out = (S / "c1886_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1886", "C1898"), ("c1886", "c1898"),
    ("C1874", "C1898"), ("c1874", "c1898"),
    ("product_u2c_cost_c1886", "product_u2c_cost_c1898"),
    ("u2c_v192", "u2c_v193"),
    ("u2c_c1886", "u2c_c1898"),
]:
    out = out.replace(a, b2)
(S / "c1898_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1886")

out = (S / "c1893_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1893", "C1899"), ("c1893", "c1899")]:
    out = out.replace(a, b2)
(S / "c1899_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1900_scorecard_and_stage.py").write_text(SC1900, encoding="utf-8")
print("scorecard from fixed c1888 product-U2C pattern")
print("OK builder v298 ready")
'''
pre = "SC1900 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v298.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1895_vision_v298", "ashhurst", "fernhurst", "T298", "1188", "1914", "product_u2c", "retarget_297"]:
    print(needle, needle in (h+pre+tail))
