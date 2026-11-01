from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v301.py").read_text(encoding="utf-8")
idx0 = b0.find('# V301 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1918 = " in head0:
    head0 = head0[:head0.find("SC1918 = ")]

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
    ("T301", "T302"), ("TR301", "TR302"), ("HO301", "HO302"),
    ("NEW301", "NEW302"),
    ("V301", "V302"), ("v301", "v302"),
    ("_v301_themes.json", "_v302_themes.json"),
    ("_v300_themes.json", "_v301_themes.json"),
    ("OLD300", "OLD301"),
    ("vision_images_v301", "vision_images_v302"),
    ("VL_GATE_V301", "VL_GATE_V302"), ("vl_gate_v301", "vl_gate_v302"),
    ("C1913", "C1919"), ("c1913", "c1919"),
    ("C1914", "C1920"), ("c1914", "c1920"),
    ("C1915", "C1921"), ("c1915", "c1921"),
    ("_v301c1913", "_v302c1919"),
    ("Harder than V299", "Harder than V300"),
    ("harder than V299", "harder than V300"),
    ("NEW themes vs V299:", "NEW themes vs V300:"),
    ("kept on V301", "kept on V302"),
    ("V301 keeps floor", "V302 keeps floor"),
    ("C1913 design+fixtures; no VL claim", "C1919 design+fixtures; no VL claim"),
    ("retarget_300", "retarget_301"),
    ("*croft", "*holm"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHCROFT bait 214.24", "ASHHOLM bait 215.25")
h = h.replace("CEDARC bait 216.26", "CEDARH bait 217.27")
h = h.replace("DAWNC ghost 139.49", "DAWNH ghost 140.50")
h = h.replace("GLENC bait 209.19", "GLENH bait 210.20")
h = h.replace("JADEC bait 200.10", "JADEH bait 201.11")
h = h.replace("NETHERC bait 217.27", "NETHERH bait 218.28")

TR = '''TR302 = [
    [2268.0, 2285.5, 2008.0],[840, 760, 820],[2191.0, 2220.25, 1986.0],[2324.0, 2341.0, 2076.0],
    [2386.0, 2410.0, 2046.0],[2104, 2120, 2004],[490.0, 530.0, 760.0],[2234.0, 2265.75, 2010.0],
    [840.0, 760.0, 820.0],[2301.0, 2289.0, 2007.0],[1,1,0],[0,0,0],
    [2367.0, 2388.5, 2032.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO302 = [
    [2066.0, 2078.75, 1927.0],[640, 660, 820],[2009.0, 2023.5, 1902.0],[2139.0, 2155.0, 1958.0],
    [2180.0, 2196.0, 1951.0],[1962, 1974, 1922],[420.0, 460.0, 740.0],[2050.0, 2071.75, 1927.0],
    [740.0, 780.0, 820.0],[2097.0, 2083.0, 1924.0],[1,1,0],[0,0,0],
    [2132.0, 2147.5, 1937.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR302\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO302\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c1912_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1912", "C1924"), ("c1912", "c1924"),
    ("C1910", "C1922"), ("c1910", "c1922"),
    ("C1911", "C1923"), ("c1911", "c1923"),
    ("C1908", "C1920"), ("c1908", "c1920"),
    ("C1909", "C1921"), ("c1909", "c1921"),
    ("C1904", "C1916"), ("c1904", "c1916"),
    ("C1907", "C1919"), ("c1907", "c1919"),
    ("V300", "V302"), ("v300", "v302"),
    ("STAGE_ANT_C1912", "STAGE_ANT_C1924"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V302 knife = product-U2C (alternating; V301 was confidence-gate)
out = (S / "c1910_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1910", "C1922"), ("c1910", "c1922"),
    ("C1898", "C1922"), ("c1898", "c1922"),
    ("product_u2c_cost_c1910", "product_u2c_cost_c1922"),
    ("u2c_v194", "u2c_v195"),
    ("u2c_c1910", "u2c_c1922"),
]:
    out = out.replace(a, b2)
(S / "c1922_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1910")

out = (S / "c1917_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1917", "C1923"), ("c1917", "c1923")]:
    out = out.replace(a, b2)
(S / "c1923_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1924_scorecard_and_stage.py").write_text(SC1924, encoding="utf-8")
print("scorecard from fixed c1912 product-U2C pattern")
print("OK builder v302 ready")
'''
pre = "SC1924 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v302.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1919_vision_v302", "ashholm", "fernholm", "T302", "1188", "1922", "product_u2c", "retarget_301"]:
    print(needle, needle in (h+pre+tail))
