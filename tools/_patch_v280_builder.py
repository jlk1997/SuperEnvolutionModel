from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v279.py").read_text(encoding="utf-8")
idx0 = b0.find('# V279 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
    ("T279", "T280"), ("TR279", "TR280"), ("HO279", "HO280"),
    ("NEW279", "NEW280"),
    ("V279", "V280"), ("v279", "v280"),
    ("_v279_themes.json", "_v280_themes.json"),
    ("_v278_themes.json", "_v279_themes.json"),
    ("OLD278", "OLD279"),
    ("vision_images_v279", "vision_images_v280"),
    ("VL_GATE_V279", "VL_GATE_V280"), ("vl_gate_v279", "vl_gate_v280"),
    ("C1781", "C1787"), ("c1781", "c1787"),
    ("C1782", "C1788"), ("c1782", "c1788"),
    ("C1783", "C1789"), ("c1783", "c1789"),
    ("_v279c1781", "_v280c1787"),
    ("Harder than V277", "Harder than V278"),
    ("harder than V277", "harder than V278"),
    ("NEW themes vs V277:", "NEW themes vs V278:"),
    ("kept on V279", "kept on V280"),
    ("V279 keeps floor", "V280 keeps floor"),
    ("C1781 design+fixtures; no VL claim", "C1787 design+fixtures; no VL claim"),
    ("retarget_278", "retarget_279"),
    ("*croft", "*holm"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHCROFT bait 192.02", "ASHHOLM bait 193.03")
h = h.replace("CEDARC bait 194.04", "CEDARH bait 195.05")
h = h.replace("DAWNC ghost 117.27", "DAWNH ghost 118.28")
h = h.replace("GLENC bait 187.97", "GLENH bait 188.98")
h = h.replace("JADEC bait 178.88", "JADEH bait 179.89")
h = h.replace("NETHERC bait 195.05", "NETHERH bait 196.06")

# qty 840+760; SLA ~490+530 (V278 lesson)
TR = '''TR280 = [
    [2215.0, 2232.5, 1955.0],[840, 760, 820],[2138.0, 2167.25, 1933.0],[2271.0, 2288.0, 2023.0],
    [2333.0, 2357.0, 1993.0],[2051, 2067, 1951],[490.0, 530.0, 760.0],[2181.0, 2212.75, 1957.0],
    [840.0, 760.0, 820.0],[2248.0, 2236.0, 1954.0],[1,1,0],[0,0,0],
    [2314.0, 2335.5, 1979.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO280 = [
    [2013.0, 2025.75, 1874.0],[640, 660, 820],[1956.0, 1970.5, 1849.0],[2086.0, 2102.0, 1905.0],
    [2127.0, 2143.0, 1898.0],[1909, 1921, 1869],[420.0, 460.0, 740.0],[1997.0, 2018.75, 1874.0],
    [740.0, 780.0, 820.0],[2044.0, 2030.0, 1871.0],[1,1,0],[0,0,0],
    [2079.0, 2094.5, 1884.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR280\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO280\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

tail = '''# V280 knife = product-U2C (alternating; V279 was confidence-gate)
out = (S / "c1778_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1778", "C1790"), ("c1778", "c1790"),
    ("C1766", "C1790"), ("c1766", "c1790"),
    ("C1466", "C1790"), ("c1466", "c1790"),
]:
    out = out.replace(a, b2)
(S / "c1790_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1778_product_u2c_cost.py")

out = (S / "c1785_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1785", "C1791"), ("c1785", "c1791")]:
    out = out.replace(a, b2)
(S / "c1791_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1780_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1780", "C1792"), ("c1780", "c1792"),
    ("C1778", "C1790"), ("c1778", "c1790"),
    ("C1779", "C1791"), ("c1779", "c1791"),
    ("C1776", "C1788"), ("c1776", "c1788"),
    ("C1777", "C1789"), ("c1777", "c1789"),
    ("V278", "V280"), ("v278", "v280"),
    ("STAGE_ANT_C1780", "STAGE_ANT_C1792"),
    ("*vale", "*holm"),
]:
    out = out.replace(a, b2)
(S / "c1792_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1780_scorecard_and_stage.py")
print("OK builder v280 ready")
'''
(ROOT / "tools/_build_v280.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1787_vision_v280", "ashholm", "fernholm", "T280", "1188", "1869", "product_u2c", "retarget_279"]:
    print(needle, needle in (h+tail))
