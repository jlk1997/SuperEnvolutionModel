from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v325.py").read_text(encoding="utf-8")
idx0 = b0.find('# V325 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2062 = " in head0:
    head0 = head0[:head0.find("SC2062 = ")]

theme_pairs = [
    ("netherwick", "nethermoor"), ("NETHERWICK", "NETHERMOOR"),
    ("cedarwick", "cedarmoor"), ("CEDARWICK", "CEDARMOOR"),
    ("dawnwick", "dawnmoor"), ("DAWNWICK", "DAWNMOOR"),
    ("fernwick", "fernmoor"), ("FERNWICK", "FERNMOOR"),
    ("glenwick", "glenmoor"), ("GLENWICK", "GLENMOOR"),
    ("hazewick", "hazemoor"), ("HAZEWICK", "HAZEMOOR"),
    ("jadewick", "jademoor"), ("JADEWICK", "JADEMOOR"),
    ("knotwick", "knotmoor"), ("KNOTWICK", "KNOTMOOR"),
    ("lakewick", "lakemoor"), ("LAKEWICK", "LAKEMOOR"),
    ("mosswick", "mossmoor"), ("MOSSWICK", "MOSSMOOR"),
    ("pinewick", "pinemoor"), ("PINEWICK", "PINEMOOR"),
    ("quillwick", "quillmoor"), ("QUILLWICK", "QUILLMOOR"),
    ("reedwick", "reedmoor"), ("REEDWICK", "REEDMOOR"),
    ("stonewick", "stonemoor"), ("STONEWICK", "STONEMOOR"),
    ("ashwick", "ashmoor"), ("ASHWICK", "ASHMOOR"),
    ("elmwick", "elmmoor"), ("ELMWICK", "ELMMOOR"),
    ("inkwick", "inkmoor"), ("INKWICK", "INKMOOR"),
    ("oakwick", "oakmoor"), ("OAKWICK", "OAKMOOR"),
]
pairs = [
    ("*wick ; stack mid-band", "*moor ; stack mid-band"),
    ("T325", "T326"), ("TR325", "TR326"), ("HO325", "HO326"),
    ("NEW325", "NEW326"),
    ("V325", "V326"), ("v325", "v326"),
    ("_v325_themes.json", "_v326_themes.json"),
    ("_v324_themes.json", "_v325_themes.json"),
    ("OLD324", "OLD325"),
    ("vision_images_v325", "vision_images_v326"),
    ("VL_GATE_V325", "VL_GATE_V326"), ("vl_gate_v325", "vl_gate_v326"),
    ("C2057", "C2063"), ("c2057", "c2063"),
    ("C2058", "C2064"), ("c2058", "c2064"),
    ("C2059", "C2065"), ("c2059", "c2065"),
    ("_v325c2057", "_v326c2063"),
    ("Harder than V323", "Harder than V324"),
    ("harder than V323", "harder than V324"),
    ("NEW themes vs V323:", "NEW themes vs V324:"),
    ("kept on V325", "kept on V326"),
    ("V325 keeps floor", "V326 keeps floor"),
    ("C2057 design+fixtures; no VL claim", "C2063 design+fixtures; no VL claim"),
    ("retarget_324", "retarget_325"),
    ("*wick", "*moor"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHWICK bait 238.48", "ASHMOOR bait 239.49")
h = h.replace("CEDARW bait 240.50", "CEDARM bait 241.51")
h = h.replace("DAWNW ghost 163.73", "DAWNM ghost 164.74")
h = h.replace("GLENW bait 233.43", "GLENM bait 234.44")
h = h.replace("JADEW bait 224.34", "JADEM bait 225.35")
h = h.replace("NETHERW bait 241.51", "NETHERM bait 242.52")

TR = '''TR326 = [
    [2316.0, 2333.5, 2056.0],[840, 760, 820],[2239.0, 2248.25, 2034.0],[2372.0, 2389.0, 2124.0],
    [2434.0, 2458.0, 2094.0],[2152, 2168, 2052],[490.0, 530.0, 760.0],[2282.0, 2313.75, 2058.0],
    [840.0, 760.0, 820.0],[2349.0, 2337.0, 2055.0],[1,1,0],[0,0,0],
    [2415.0, 2436.5, 2080.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO326 = [
    [2114.0, 2126.75, 1975.0],[640, 660, 820],[2057.0, 2071.5, 1950.0],[2187.0, 2203.0, 2006.0],
    [2228.0, 2244.0, 1999.0],[2010, 2022, 1970],[420.0, 460.0, 740.0],[2098.0, 2119.75, 1975.0],
    [740.0, 780.0, 820.0],[2145.0, 2131.0, 1972.0],[1,1,0],[0,0,0],
    [2180.0, 2195.5, 1985.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR326\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO326\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2056_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2056", "C2068"), ("c2056", "c2068"),
    ("C2054", "C2066"), ("c2054", "c2066"),
    ("C2055", "C2067"), ("c2055", "c2067"),
    ("C2052", "C2064"), ("c2052", "c2064"),
    ("C2053", "C2065"), ("c2053", "c2065"),
    ("C2048", "C2060"), ("c2048", "c2060"),
    ("C2051", "C2063"), ("c2051", "c2063"),
    ("V324", "V326"), ("v324", "v326"),
    ("STAGE_ANT_C2056", "STAGE_ANT_C2068"),
    ("*holm", "*moor"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V326 knife = product-U2C (alternating; V325 was confidence-gate)
out = (S / "c2054_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2054", "C2066"), ("c2054", "c2066"),
    ("C2042", "C2066"), ("c2042", "c2066"),
    ("product_u2c_cost_c2054", "product_u2c_cost_c2066"),
    ("u2c_v206", "u2c_v207"),
    ("u2c_c2054", "u2c_c2066"),
]:
    out = out.replace(a, b2)
(S / "c2066_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2054")

out = (S / "c2061_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2061", "C2067"), ("c2061", "c2067")]:
    out = out.replace(a, b2)
(S / "c2067_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2068_scorecard_and_stage.py").write_text(SC2068, encoding="utf-8")
print("scorecard from fixed c2056 product-U2C pattern")
print("OK builder v326 ready")
'''
pre = "SC2068 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v326.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2063_vision_v326", "ashmoor", "fernmoor", "T326", "1188", "1970", "product_u2c", "retarget_325", "2248.25"]:
    print(needle, needle in (h+pre+tail))
