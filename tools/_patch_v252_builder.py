from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v251.py").read_text(encoding="utf-8")
idx0 = b0.find('# V251 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
    ("T251", "T252"), ("TR251", "TR252"), ("HO251", "HO252"),
    ("NEW251", "NEW252"),
    ("V251", "V252"), ("v251", "v252"),
    ("_v251_themes.json", "_v252_themes.json"),
    ("_v250_themes.json", "_v251_themes.json"),
    ("OLD250", "OLD251"),
    ("vision_images_v251", "vision_images_v252"),
    ("VL_GATE_V251", "VL_GATE_V252"), ("vl_gate_v251", "vl_gate_v252"),
    ("C1613", "C1619"), ("c1613", "c1619"),
    ("C1614", "C1620"), ("c1614", "c1620"),
    ("C1615", "C1621"), ("c1615", "c1621"),
    ("_v251c1613", "_v252c1619"),
    ("Harder than V249", "Harder than V250"),
    ("harder than V249", "harder than V250"),
    ("NEW themes vs V249:", "NEW themes vs V250:"),
    ("kept on V251", "kept on V252"),
    ("V251 keeps floor", "V252 keeps floor"),
    ("C1613 design+fixtures; no VL claim", "C1619 design+fixtures; no VL claim"),
    ("retarget_250", "retarget_251"),
    ("*brook", "*dale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHDALE bait 164.74", "ASHDALE bait 165.75")
h = h.replace("CEDARB bait 166.76", "CEDARD bait 167.77")
h = h.replace("DAWNB ghost 89.89", "DAWND ghost 90.90")
h = h.replace("GLENB bait 159.69", "GLEND bait 160.70")
h = h.replace("JADEB bait 150.60", "JADED bait 151.61")
h = h.replace("NETHERB bait 167.77", "NETHERD bait 168.78")

TR = '''TR252 = [
    [2150.0, 2167.5, 1890.0],[840, 760, 820],[2073.0, 2102.25, 1868.0],[2206.0, 2223.0, 1958.0],
    [2268.0, 2292.0, 1928.0],[1986, 2002, 1886],[480.0, 520.0, 740.0],[2116.0, 2147.75, 1892.0],
    [840.0, 760.0, 820.0],[2183.0, 2171.0, 1889.0],[1,1,0],[0,0,0],
    [2249.0, 2270.5, 1914.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO252 = [
    [1948.0, 1960.75, 1809.0],[740, 780, 820],[1891.0, 1905.5, 1784.0],[2021.0, 2037.0, 1840.0],
    [2062.0, 2078.0, 1833.0],[1844, 1856, 1802],[360.0, 400.0, 730.0],[1932.0, 1953.75, 1809.0],
    [780.0, 740.0, 820.0],[1979.0, 1965.0, 1804.0],[1,1,0],[0,0,0],
    [2014.0, 2029.5, 1819.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR252\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO252\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

src = "c1610_product_u2c_cost.py"
if not (ROOT / "scripts" / src).exists():
    src = "c1598_product_u2c_cost.py"
sc_src = "c1612_scorecard_and_stage.py"

tail = f'''# V252 knife = product-U2C (alternating; V251 was confidence-gate)
out = (S / "{src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1610", "C1622"), ("c1610", "c1622"),
    ("C1598", "C1622"), ("c1598", "c1622"),
    ("C1466", "C1622"), ("c1466", "c1622"),
]:
    out = out.replace(a, b2)
(S / "c1622_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{src}")

out = (S / "c1617_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1617", "C1623"), ("c1617", "c1623")]:
    out = out.replace(a, b2)
(S / "c1623_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1612", "C1624"), ("c1612", "c1624"),
    ("C1610", "C1622"), ("c1610", "c1622"),
    ("C1611", "C1623"), ("c1611", "c1623"),
    ("C1608", "C1620"), ("c1608", "c1620"),
    ("C1609", "C1621"), ("c1609", "c1621"),
    ("V250", "V252"), ("v250", "v252"),
    ("STAGE_ANT_C1612", "STAGE_ANT_C1624"),
    ("*fen", "*dale"),
]:
    out = out.replace(a, b2)
(S / "c1624_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v252 ready")
'''
(ROOT / "tools/_build_v252.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1619_vision_v252", "ashdale", "ferndale", "T252", "1188", "1840", "product_u2c"]:
    print(needle, needle in (h+tail))
