from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v323.py").read_text(encoding="utf-8")
idx0 = b0.find('# V323 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2050 = " in head0:
    head0 = head0[:head0.find("SC2050 = ")]

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
    ("T323", "T324"), ("TR323", "TR324"), ("HO323", "HO324"),
    ("NEW323", "NEW324"),
    ("V323", "V324"), ("v323", "v324"),
    ("_v323_themes.json", "_v324_themes.json"),
    ("_v322_themes.json", "_v323_themes.json"),
    ("OLD322", "OLD323"),
    ("vision_images_v323", "vision_images_v324"),
    ("VL_GATE_V323", "VL_GATE_V324"), ("vl_gate_v323", "vl_gate_v324"),
    ("C2045", "C2051"), ("c2045", "c2051"),
    ("C2046", "C2052"), ("c2046", "c2052"),
    ("C2047", "C2053"), ("c2047", "c2053"),
    ("_v323c2045", "_v324c2051"),
    ("Harder than V321", "Harder than V322"),
    ("harder than V321", "harder than V322"),
    ("NEW themes vs V321:", "NEW themes vs V322:"),
    ("kept on V323", "kept on V324"),
    ("V323 keeps floor", "V324 keeps floor"),
    ("C2045 design+fixtures; no VL claim", "C2051 design+fixtures; no VL claim"),
    ("retarget_322", "retarget_323"),
    ("*croft", "*holm"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHCROFT bait 236.46", "ASHHOLM bait 237.47")
h = h.replace("CEDARC bait 238.48", "CEDARH bait 239.49")
h = h.replace("DAWNC ghost 161.71", "DAWNH ghost 162.72")
h = h.replace("GLENC bait 231.41", "GLENH bait 232.42")
h = h.replace("JADEC bait 222.32", "JADEH bait 223.33")
h = h.replace("NETHERC bait 239.49", "NETHERH bait 240.50")

TR = '''TR324 = [
    [2312.0, 2329.5, 2052.0],[840, 760, 820],[2235.0, 2244.25, 2030.0],[2368.0, 2385.0, 2120.0],
    [2430.0, 2454.0, 2090.0],[2148, 2164, 2048],[490.0, 530.0, 760.0],[2278.0, 2309.75, 2054.0],
    [840.0, 760.0, 820.0],[2345.0, 2333.0, 2051.0],[1,1,0],[0,0,0],
    [2411.0, 2432.5, 2076.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO324 = [
    [2110.0, 2122.75, 1971.0],[640, 660, 820],[2053.0, 2067.5, 1946.0],[2183.0, 2199.0, 2002.0],
    [2224.0, 2240.0, 1995.0],[2006, 2018, 1966],[420.0, 460.0, 740.0],[2094.0, 2115.75, 1971.0],
    [740.0, 780.0, 820.0],[2141.0, 2127.0, 1968.0],[1,1,0],[0,0,0],
    [2176.0, 2191.5, 1981.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR324\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO324\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2044_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2044", "C2056"), ("c2044", "c2056"),
    ("C2042", "C2054"), ("c2042", "c2054"),
    ("C2043", "C2055"), ("c2043", "c2055"),
    ("C2040", "C2052"), ("c2040", "c2052"),
    ("C2041", "C2053"), ("c2041", "c2053"),
    ("C2036", "C2048"), ("c2036", "c2048"),
    ("C2039", "C2051"), ("c2039", "c2051"),
    ("V322", "V324"), ("v322", "v324"),
    ("STAGE_ANT_C2044", "STAGE_ANT_C2056"),
    ("*vale", "*holm"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V324 knife = product-U2C (alternating; V323 was confidence-gate)
out = (S / "c2042_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2042", "C2054"), ("c2042", "c2054"),
    ("C2030", "C2054"), ("c2030", "c2054"),
    ("product_u2c_cost_c2042", "product_u2c_cost_c2054"),
    ("u2c_v205", "u2c_v206"),
    ("u2c_c2042", "u2c_c2054"),
]:
    out = out.replace(a, b2)
(S / "c2054_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2042")

out = (S / "c2049_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2049", "C2055"), ("c2049", "c2055")]:
    out = out.replace(a, b2)
(S / "c2055_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2056_scorecard_and_stage.py").write_text(SC2056, encoding="utf-8")
print("scorecard from fixed c2044 product-U2C pattern")
print("OK builder v324 ready")
'''
pre = "SC2056 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v324.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2051_vision_v324", "ashholm", "fernholm", "T324", "1188", "1966", "product_u2c", "retarget_323"]:
    print(needle, needle in (h+pre+tail))
