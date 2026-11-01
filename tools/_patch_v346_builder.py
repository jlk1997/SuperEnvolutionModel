from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v345.py").read_text(encoding="utf-8")
idx0 = b0.find('# V345 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2182 = " in head0:
    head0 = head0[:head0.find("SC2182 = ")]

theme_pairs = [
    ("nethercroft", "netherholm"), ("NETHERCROFT", "NETHERHOLM"),
    ("cedarcroft", "cedarholm"), ("CEDARCROFT", "CEDARHOLM"),
    ("dawncroft", "dawnholm"), ("DAWNCROFT", "DAWNHOLM"),
    ("ferncroft", "fernholm"), ("FERNCROFT", "FERNHOLM"),
    ("glencroft", "glenholm"), ("GLENCROFT", "GLENHOLM"),
    ("hazecroft", "hazeholm"), ("HAZECROFT", "HAZEHOLM"),
    ("jadecroft", "jadeholm"), ("JADECROFT", "JADEHOLM"),
    ("knotcroft", "knotholm"), ("KNOTCROFT", "KNOTHOLM"),
    ("lakecroft", "lakeholm"), ("LAKECROFT", "LAKEHOLM"),
    ("mosscroft", "mossholm"), ("MOSSCROFT", "MOSSHOLM"),
    ("pinecroft", "pineholm"), ("PINECROFT", "PINEHOLM"),
    ("quillcroft", "quillholm"), ("QUILLCROFT", "QUILLHOLM"),
    ("reedcroft", "reedholm"), ("REEDCROFT", "REEDHOLM"),
    ("stonecroft", "stoneholm"), ("STONECROFT", "STONEHOLM"),
    ("ashcroft", "ashholm"), ("ASHCROFT", "ASHHOLM"),
    ("elmcroft", "elmholm"), ("ELMCROFT", "ELMHOLM"),
    ("inkcroft", "inkholm"), ("INKCROFT", "INKHOLM"),
    ("oakcroft", "oakholm"), ("OAKCROFT", "OAKHOLM"),
]
pairs = [
    ("*croft ; stack mid-band", "*holm ; stack mid-band"),
    ("T345", "T346"), ("TR345", "TR346"), ("HO345", "HO346"),
    ("NEW345", "NEW346"),
    ("V345", "V346"), ("v345", "v346"),
    ("_v345_themes.json", "_v346_themes.json"),
    ("_v344_themes.json", "_v345_themes.json"),
    ("OLD344", "OLD345"),
    ("vision_images_v345", "vision_images_v346"),
    ("VL_GATE_V345", "VL_GATE_V346"), ("vl_gate_v345", "vl_gate_v346"),
    ("C2177", "C2183"), ("c2177", "c2183"),
    ("C2178", "C2184"), ("c2178", "c2184"),
    ("C2179", "C2185"), ("c2179", "c2185"),
    ("_v345c2177", "_v346c2183"),
    ("Harder than V343", "Harder than V344"),
    ("harder than V343", "harder than V344"),
    ("NEW themes vs V343:", "NEW themes vs V344:"),
    ("kept on V345", "kept on V346"),
    ("V345 keeps floor", "V346 keeps floor"),
    ("C2183 design+fixtures; no VL claim", "C2183 design+fixtures; no VL claim"),
    ("retarget_344", "retarget_345"),
    ("*croft", "*holm"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHOLM bait 249.59", "ASHHOLM bait 247.57")
h = h.replace("CEDARH bait 261.71", "CEDARH bait 261.71")
h = h.replace("DAWNH ghost 184.94", "DAWNH ghost 184.94")
h = h.replace("GLENH bait 254.64", "GLENH bait 254.64")
h = h.replace("JADEH bait 245.55", "JADEH bait 245.55")
h = h.replace("NETHERH bait 262.72", "NETHERH bait 262.72")

TR = '''TR346 = [
    [2356.0, 2373.5, 2096.0],[840, 760, 820],[2254.0, 2255.25, 2059.0],[2412.0, 2429.0, 2164.0],
    [2474.0, 2498.0, 2134.0],[2192, 2208, 2092],[490.0, 530.0, 760.0],[2322.0, 2353.75, 2098.0],
    [840.0, 760.0, 820.0],[2389.0, 2377.0, 2095.0],[1,1,0],[0,0,0],
    [2455.0, 2476.5, 2120.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO346 = [
    [2154.0, 2166.75, 2015.0],[640, 660, 820],[2097.0, 2111.5, 1990.0],[2227.0, 2243.0, 2046.0],
    [2232.0, 2243.0, 2039.0],[2050, 2062, 2012],[420.0, 460.0, 740.0],[2138.0, 2159.75, 2015.0],
    [740.0, 780.0, 820.0],[2185.0, 2171.0, 2012.0],[1,1,0],[0,0,0],
    [2220.0, 2235.5, 2025.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR346\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO346\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2188"), ("c2092", "c2188"),
    ("C2090", "C2186"), ("c2090", "c2186"),
    ("C2091", "C2187"), ("c2091", "c2187"),
    ("C2088", "C2184"), ("c2088", "c2184"),
    ("C2089", "C2185"), ("c2089", "c2185"),
    ("C2084", "C2180"), ("c2084", "c2180"),
    ("C2087", "C2183"), ("c2087", "c2183"),
    ("V330", "V346"), ("v330", "v346"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2188"),
    ("*croft", "*holm"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V346 knife = product-U2C (alternating; V345 was confidence-gate)
out = (S / "c2174_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2174", "C2186"), ("c2174", "c2186"),
    ("C2090", "C2186"), ("c2090", "c2186"),
    ("product_u2c_cost_c2186", "product_u2c_cost_c2186"),
    ("u2c_v222", "u2c_v211"),
    ("u2c_c2186", "u2c_c2186"),
]:
    out = out.replace(a, b2)
(S / "c2186_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2174")

out = (S / "c2181_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2181", "C2187"), ("c2181", "c2187")]:
    out = out.replace(a, b2)
(S / "c2187_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2188_scorecard_and_stage.py").write_text(SC2188, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v346 ready")
'''
pre = "SC2188 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v346.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2183_vision_v346", "ashholm", "fernholm", "T346", "1188", "2012", "product_u2c", "retarget_345", "2255.25"]:
    print(needle, needle in (h+pre+tail))
