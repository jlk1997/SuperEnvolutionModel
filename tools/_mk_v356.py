from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v355.py").read_text(encoding="utf-8")
idx0 = b0.find("# V355 knife = confidence-gate")
if idx0 < 0:
    raise SystemExit("knife not found")
head0 = b0[:idx0]
if "SC2242 = " in head0:
    head0 = head0[:head0.find("SC2242 = ")]
theme_pairs = [
    ("nethervale", "nethercroft"), ("NETHERVALE", "NETHERCROFT"),
    ("cedarvale", "cedarcroft"), ("CEDARVALE", "CEDARCROFT"),
    ("dawnvale", "dawncroft"), ("DAWNVALE", "DAWNCROFT"),
    ("fernvale", "ferncroft"), ("FERNVALE", "FERNCROFT"),
    ("glenvale", "glencroft"), ("GLENVALE", "GLENCROFT"),
    ("hazevale", "hazecroft"), ("HAZEVALE", "HAZECROFT"),
    ("jadevale", "jadecroft"), ("JADEVALE", "JADECROFT"),
    ("knotvale", "knotcroft"), ("KNOTVALE", "KNOTCROFT"),
    ("lakevale", "lakecroft"), ("LAKEVALE", "LAKECROFT"),
    ("mossvale", "mosscroft"), ("MOSSVALE", "MOSSCROFT"),
    ("pinevale", "pinecroft"), ("PINEVALE", "PINECROFT"),
    ("quillvale", "quillcroft"), ("QUILLVALE", "QUILLCROFT"),
    ("reedvale", "reedcroft"), ("REEDVALE", "REEDCROFT"),
    ("stonevale", "stonecroft"), ("STONEVALE", "STONECROFT"),
    ("ashvale", "ashcroft"), ("ASHVALE", "ASHCROFT"),
    ("elmvale", "elmcroft"), ("ELMVALE", "ELMCROFT"),
    ("inkvale", "inkcroft"), ("INKVALE", "INKCROFT"),
    ("oakvale", "oakcroft"), ("OAKVALE", "OAKCROFT"),
]
pairs = [
    ("*vale ; stack mid-band", "*croft ; stack mid-band"),
    ("T355", "T356"), ("TR355", "TR356"), ("HO355", "HO356"),
    ("NEW355", "NEW356"),
    ("V355", "V356"), ("v355", "v356"),
    ("_v355_themes.json", "_v356_themes.json"),
    ("_v354_themes.json", "_v355_themes.json"),
    ("OLD354", "OLD355"),
    ("vision_images_v355", "vision_images_v356"),
    ("VL_GATE_V355", "VL_GATE_V356"), ("vl_gate_v355", "vl_gate_v356"),
    ("C2237", "C2243"), ("c2237", "c2243"),
    ("C2238", "C2244"), ("c2238", "c2244"),
    ("C2239", "C2245"), ("c2239", "c2245"),
    ("_v355c2237", "_v356c2243"),
    ("Harder than V353", "Harder than V354"),
    ("harder than V353", "harder than V354"),
    ("NEW themes vs V353:", "NEW themes vs V354:"),
    ("kept on V355", "kept on V356"),
    ("V355 keeps floor", "V356 keeps floor"),
    ("C2237 design+fixtures; no VL claim", "C2243 design+fixtures; no VL claim"),
    ("retarget_354", "retarget_355"),
    ("*vale", "*croft"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)
h = h.replace("ASHVALE bait 256.66", "ASHCROFT bait 257.67")
h = h.replace("CEDARV bait 270.80", "CEDARC bait 271.81")
h = h.replace("DAWNV ghost 193.04", "DAWNC ghost 194.05")
h = h.replace("GLENV bait 263.73", "GLENC bait 264.74")
h = h.replace("JADEV bait 254.64", "JADEC bait 255.65")
h = h.replace("NETHERV bait 271.81", "NETHERC bait 272.82")
TR = """TR356 = [
    [2376.0, 2393.5, 2116.0],[840, 760, 820],[2251.0, 2252.25, 2047.0],[2432.0, 2449.0, 2184.0],
    [2494.0, 2497.0, 2154.0],[2212, 2228, 2112],[490.0, 530.0, 760.0],[2342.0, 2373.75, 2118.0],
    [840.0, 760.0, 820.0],[2409.0, 2397.0, 2115.0],[1,1,0],[0,0,0],
    [2453.0, 2472.5, 2106.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO356 = [
    [2174.0, 2186.75, 2035.0],[640, 660, 820],[2117.0, 2131.5, 2010.0],[2247.0, 2263.0, 2066.0],
    [2251.0, 2262.0, 2059.0],[2070, 2082, 2032],[420.0, 460.0, 740.0],[2158.0, 2179.75, 2035.0],
    [740.0, 780.0, 820.0],[2205.0, 2191.0, 2032.0],[1,1,0],[0,0,0],
    [2235.0, 2249.5, 2039.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
h = re.sub(r"TR356\s*=\s*\[[\s\S]*?\n\]", TR, h, count=1)
h = re.sub(r"HO356\s*=\s*\[[\s\S]*?\n\]", HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2248"), ("c2092", "c2248"),
    ("C2090", "C2246"), ("c2090", "c2246"),
    ("C2091", "C2247"), ("c2091", "c2247"),
    ("C2088", "C2244"), ("c2088", "c2244"),
    ("C2089", "C2245"), ("c2089", "c2245"),
    ("C2084", "C2240"), ("c2084", "c2240"),
    ("C2087", "C2243"), ("c2087", "c2243"),
    ("V330", "V356"), ("v330", "v356"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2248"),
    ("*croft", "*croft"),
]:
    sc_body = sc_body.replace(a, b2)
tail = r'''# V356 knife = product-U2C (alternating; V355 was confidence-gate)
out = (S / "c2234_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2234", "C2246"), ("c2234", "c2246"),
    ("C2090", "C2246"), ("c2090", "c2246"),
    ("product_u2c_cost_c2246", "product_u2c_cost_c2246"),
    ("u2c_v167", "u2c_v156"),
    ("u2c_c2246", "u2c_c2246"),
]:
    out = out.replace(a, b2)
(S / "c2246_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2234")

out = (S / "c2241_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2241", "C2247"), ("c2241", "c2247")]:
    out = out.replace(a, b2)
(S / "c2247_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2248_scorecard_and_stage.py").write_text(SC2248, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v356 ready")
'''
pre = "SC2248 = " + repr(sc_body) + "\n"
text = h + pre + tail
(ROOT / "tools/_build_v356.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2243_vision_v356", "ashcroft", "ferncroft", "T356", "1188", "2032", "product_u2c", "retarget_355", "2252.25"]:
    print(needle, needle in text)
