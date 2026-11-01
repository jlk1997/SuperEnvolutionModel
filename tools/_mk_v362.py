from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v361.py").read_text(encoding="utf-8")
idx0 = b0.find("# V361 knife = confidence-gate")
if idx0 < 0:
    raise SystemExit("knife not found")
head0 = b0[:idx0]
if "SC2278 = " in head0:
    head0 = head0[:head0.find("SC2278 = ")]
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
    ("T361", "T362"), ("TR361", "TR362"), ("HO361", "HO362"),
    ("NEW361", "NEW362"),
    ("V361", "V362"), ("v361", "v362"),
    ("_v361_themes.json", "_v362_themes.json"),
    ("_v360_themes.json", "_v361_themes.json"),
    ("OLD360", "OLD361"),
    ("vision_images_v361", "vision_images_v362"),
    ("VL_GATE_V361", "VL_GATE_V362"), ("vl_gate_v361", "vl_gate_v362"),
    ("C2273", "C2279"), ("c2273", "c2279"),
    ("C2274", "C2280"), ("c2274", "c2280"),
    ("C2275", "C2281"), ("c2275", "c2281"),
    ("_v361c2273", "_v362c2279"),
    ("Harder than V359", "Harder than V360"),
    ("harder than V359", "harder than V360"),
    ("NEW themes vs V359:", "NEW themes vs V360:"),
    ("kept on V361", "kept on V362"),
    ("V361 keeps floor", "V362 keeps floor"),
    ("C2273 design+fixtures; no VL claim", "C2279 design+fixtures; no VL claim"),
    ("retarget_360", "retarget_361"),
    ("*brook", "*dale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)
h = h.replace("ASHBROOK bait 262.72", "ASHDALE bait 263.73")
h = h.replace("CEDARB bait 276.86", "CEDARD bait 277.87")
h = h.replace("DAWNB ghost 199.10", "DAWND ghost 200.11")
h = h.replace("GLENB bait 269.79", "GLEND bait 270.80")
h = h.replace("JADEB bait 260.70", "JADED bait 261.71")
h = h.replace("NETHERB bait 277.87", "NETHERD bait 278.88")
TR = """TR362 = [
    [2388.0, 2405.5, 2128.0],[840, 760, 820],[2251.0, 2252.25, 2041.0],[2444.0, 2461.0, 2196.0],
    [2493.0, 2494.0, 2166.0],[2224, 2240, 2124],[490.0, 530.0, 760.0],[2354.0, 2385.75, 2130.0],
    [840.0, 760.0, 820.0],[2421.0, 2409.0, 2127.0],[1,1,0],[0,0,0],
    [2455.0, 2474.5, 2094.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO362 = [
    [2186.0, 2198.75, 2047.0],[640, 660, 820],[2129.0, 2143.5, 2022.0],[2259.0, 2275.0, 2078.0],
    [2263.0, 2274.0, 2071.0],[2082, 2094, 2044],[420.0, 460.0, 740.0],[2170.0, 2191.75, 2047.0],
    [740.0, 780.0, 820.0],[2217.0, 2203.0, 2044.0],[1,1,0],[0,0,0],
    [2247.0, 2261.5, 2051.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
h = re.sub(r"TR362\s*=\s*\[[\s\S]*?\n\]", TR, h, count=1)
h = re.sub(r"HO362\s*=\s*\[[\s\S]*?\n\]", HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2284"), ("c2092", "c2284"),
    ("C2090", "C2282"), ("c2090", "c2282"),
    ("C2091", "C2283"), ("c2091", "c2283"),
    ("C2088", "C2280"), ("c2088", "c2280"),
    ("C2089", "C2281"), ("c2089", "c2281"),
    ("C2084", "C2276"), ("c2084", "c2276"),
    ("C2087", "C2279"), ("c2087", "c2279"),
    ("V330", "V362"), ("v330", "v362"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2284"),
    ("*croft", "*dale"),
]:
    sc_body = sc_body.replace(a, b2)
tail = r'''# V362 knife = product-U2C (alternating; V361 was confidence-gate)
out = (S / "c2270_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2270", "C2282"), ("c2270", "c2282"),
    ("C2090", "C2282"), ("c2090", "c2282"),
    ("product_u2c_cost_c2282", "product_u2c_cost_c2282"),
    ("u2c_v134", "u2c_v123"),
    ("u2c_c2282", "u2c_c2282"),
]:
    out = out.replace(a, b2)
(S / "c2282_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2270")

out = (S / "c2277_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2277", "C2283"), ("c2277", "c2283")]:
    out = out.replace(a, b2)
(S / "c2283_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2284_scorecard_and_stage.py").write_text(SC2284, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v362 ready")
'''
pre = "SC2284 = " + repr(sc_body) + "\n"
text = h + pre + tail
(ROOT / "tools/_build_v362.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2279_vision_v362", "ashdale", "ferndale", "T362", "1188", "2044", "product_u2c", "retarget_361", "2252.25"]:
    print(needle, needle in text)
