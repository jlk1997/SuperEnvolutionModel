from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v351.py").read_text(encoding="utf-8")
idx0 = b0.find("# V351 knife = confidence-gate")
if idx0 < 0:
    raise SystemExit("knife not found")
head0 = b0[:idx0]
if "SC2218 = " in head0:
    head0 = head0[:head0.find("SC2218 = ")]
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
    ("T351", "T352"), ("TR351", "TR352"), ("HO351", "HO352"),
    ("NEW351", "NEW352"),
    ("V351", "V352"), ("v351", "v352"),
    ("_v351_themes.json", "_v352_themes.json"),
    ("_v350_themes.json", "_v351_themes.json"),
    ("OLD350", "OLD351"),
    ("vision_images_v351", "vision_images_v352"),
    ("VL_GATE_V351", "VL_GATE_V352"), ("vl_gate_v351", "vl_gate_v352"),
    ("C2213", "C2219"), ("c2213", "c2219"),
    ("C2214", "C2220"), ("c2214", "c2220"),
    ("C2215", "C2221"), ("c2215", "c2221"),
    ("_v351c2213", "_v352c2219"),
    ("Harder than V349", "Harder than V350"),
    ("harder than V349", "harder than V350"),
    ("NEW themes vs V349:", "NEW themes vs V350:"),
    ("kept on V351", "kept on V352"),
    ("V351 keeps floor", "V352 keeps floor"),
    ("C2213 design+fixtures; no VL claim", "C2219 design+fixtures; no VL claim"),
    ("retarget_350", "retarget_351"),
    ("*dale", "*ford"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)
h = h.replace("ASHDALE bait 252.62", "ASHFORD bait 253.63")
h = h.replace("CEDARD bait 266.76", "CEDARF bait 267.77")
h = h.replace("DAWND ghost 189.99", "DAWNF ghost 190.01")
h = h.replace("GLEND bait 259.69", "GLENF bait 260.70")
h = h.replace("JADED bait 250.60", "JADEF bait 251.61")
h = h.replace("NETHERD bait 267.77", "NETHERF bait 268.78")
TR = """TR352 = [
    [2368.0, 2385.5, 2108.0],[840, 760, 820],[2255.0, 2257.25, 2051.0],[2424.0, 2441.0, 2176.0],
    [2486.0, 2492.0, 2146.0],[2204, 2220, 2104],[490.0, 530.0, 760.0],[2334.0, 2365.75, 2110.0],
    [840.0, 760.0, 820.0],[2401.0, 2389.0, 2107.0],[1,1,0],[0,0,0],
    [2459.0, 2478.5, 2114.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO352 = [
    [2166.0, 2178.75, 2027.0],[640, 660, 820],[2109.0, 2123.5, 2002.0],[2239.0, 2255.0, 2058.0],
    [2243.0, 2254.0, 2051.0],[2062, 2074, 2024],[420.0, 460.0, 740.0],[2150.0, 2171.75, 2027.0],
    [740.0, 780.0, 820.0],[2197.0, 2183.0, 2024.0],[1,1,0],[0,0,0],
    [2227.0, 2241.5, 2031.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
h = re.sub(r"TR352\s*=\s*\[[\s\S]*?\n\]", TR, h, count=1)
h = re.sub(r"HO352\s*=\s*\[[\s\S]*?\n\]", HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2224"), ("c2092", "c2224"),
    ("C2090", "C2222"), ("c2090", "c2222"),
    ("C2091", "C2223"), ("c2091", "c2223"),
    ("C2088", "C2220"), ("c2088", "c2220"),
    ("C2089", "C2221"), ("c2089", "c2221"),
    ("C2084", "C2216"), ("c2084", "c2216"),
    ("C2087", "C2219"), ("c2087", "c2219"),
    ("V330", "V352"), ("v330", "v352"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2224"),
    ("*croft", "*ford"),
]:
    sc_body = sc_body.replace(a, b2)
tail = r'''# V352 knife = product-U2C (alternating; V351 was confidence-gate)
out = (S / "c2210_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2210", "C2222"), ("c2210", "c2222"),
    ("C2090", "C2222"), ("c2090", "c2222"),
    ("product_u2c_cost_c2222", "product_u2c_cost_c2222"),
    ("u2c_v189", "u2c_v178"),
    ("u2c_c2222", "u2c_c2222"),
]:
    out = out.replace(a, b2)
(S / "c2222_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2210")

out = (S / "c2217_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2217", "C2223"), ("c2217", "c2223")]:
    out = out.replace(a, b2)
(S / "c2223_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2224_scorecard_and_stage.py").write_text(SC2224, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v352 ready")
'''
pre = "SC2224 = " + repr(sc_body) + "\n"
text = h + pre + tail
(ROOT / "tools/_build_v352.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2219_vision_v352", "ashford", "fernford", "T352", "1188", "2024", "product_u2c", "retarget_351", "2257.25"]:
    print(needle, needle in text)
