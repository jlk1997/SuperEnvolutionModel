from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v333.py").read_text(encoding="utf-8")
idx0 = b0.find('# V333 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2110 = " in head0:
    head0 = head0[:head0.find("SC2110 = ")]

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
    ("T333", "T334"), ("TR333", "TR334"), ("HO333", "HO334"),
    ("NEW333", "NEW334"),
    ("V333", "V334"), ("v333", "v334"),
    ("_v333_themes.json", "_v334_themes.json"),
    ("_v332_themes.json", "_v333_themes.json"),
    ("OLD332", "OLD333"),
    ("vision_images_v333", "vision_images_v334"),
    ("VL_GATE_V333", "VL_GATE_V334"), ("vl_gate_v333", "vl_gate_v334"),
    ("C2105", "C2111"), ("c2105", "c2111"),
    ("C2106", "C2112"), ("c2106", "c2112"),
    ("C2107", "C2113"), ("c2107", "c2113"),
    ("_v333c2105", "_v334c2111"),
    ("Harder than V331", "Harder than V332"),
    ("harder than V331", "harder than V332"),
    ("NEW themes vs V331:", "NEW themes vs V332:"),
    ("kept on V333", "kept on V334"),
    ("V333 keeps floor", "V334 keeps floor"),
    ("C2105 design+fixtures; no VL claim", "C2111 design+fixtures; no VL claim"),
    ("retarget_332", "retarget_333"),
    ("*vale", "*croft"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHVALE bait 246.56", "ASHCROFT bait 247.57")
h = h.replace("CEDARV bait 248.58", "CEDARC bait 249.59")
h = h.replace("DAWNV ghost 171.81", "DAWNC ghost 172.82")
h = h.replace("GLENV bait 241.51", "GLENC bait 242.52")
h = h.replace("JADEV bait 232.42", "JADEC bait 233.43")
h = h.replace("NETHERV bait 249.59", "NETHERC bait 250.60")

TR = '''TR334 = [
    [2332.0, 2349.5, 2072.0],[840, 760, 820],[2252.0, 2258.25, 2047.0],[2388.0, 2405.0, 2140.0],
    [2450.0, 2474.0, 2110.0],[2168, 2184, 2068],[490.0, 530.0, 760.0],[2298.0, 2329.75, 2074.0],
    [840.0, 760.0, 820.0],[2365.0, 2353.0, 2071.0],[1,1,0],[0,0,0],
    [2431.0, 2452.5, 2096.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO334 = [
    [2130.0, 2142.75, 1991.0],[640, 660, 820],[2073.0, 2087.5, 1966.0],[2203.0, 2219.0, 2022.0],
    [2244.0, 2259.0, 2015.0],[2026, 2038, 1988],[420.0, 460.0, 740.0],[2114.0, 2135.75, 1991.0],
    [740.0, 780.0, 820.0],[2161.0, 2147.0, 1988.0],[1,1,0],[0,0,0],
    [2196.0, 2211.5, 2001.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR334\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO334\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2116"), ("c2092", "c2116"),
    ("C2090", "C2114"), ("c2090", "c2114"),
    ("C2091", "C2115"), ("c2091", "c2115"),
    ("C2088", "C2112"), ("c2088", "c2112"),
    ("C2089", "C2113"), ("c2089", "c2113"),
    ("C2084", "C2108"), ("c2084", "c2108"),
    ("C2087", "C2111"), ("c2087", "c2111"),
    ("V330", "V334"), ("v330", "v334"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2116"),
    ("*ford", "*croft"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V334 knife = product-U2C (alternating; V333 was confidence-gate)
out = (S / "c2102_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2102", "C2114"), ("c2102", "c2114"),
    ("C2090", "C2114"), ("c2090", "c2114"),
    ("product_u2c_cost_c2102", "product_u2c_cost_c2114"),
    ("u2c_v210", "u2c_v211"),
    ("u2c_c2102", "u2c_c2114"),
]:
    out = out.replace(a, b2)
(S / "c2114_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2102")

out = (S / "c2109_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2109", "C2115"), ("c2109", "c2115")]:
    out = out.replace(a, b2)
(S / "c2115_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2116_scorecard_and_stage.py").write_text(SC2116, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v334 ready")
'''
pre = "SC2116 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v334.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2111_vision_v334", "ashcroft", "ferncroft", "T334", "1188", "1988", "product_u2c", "retarget_333", "2258.25"]:
    print(needle, needle in (h+pre+tail))
