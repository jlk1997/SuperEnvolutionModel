from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v261.py").read_text(encoding="utf-8")
idx0 = b0.find('# V261 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("netherfen", "netherbrook"), ("NETHERFEN", "NETHERBROOK"),
    ("cedarfen", "cedarbrook"), ("CEDARFEN", "CEDARBROOK"),
    ("dawnfen", "dawnbrook"), ("DAWNFEN", "DAWNBROOK"),
    ("fernfen", "fernbrook"), ("FERNFEN", "FERNBROOK"),
    ("glenfen", "glenbrook"), ("GLENFEN", "GLENBROOK"),
    ("hazefen", "hazebrook"), ("HAZEFEN", "HAZEBROOK"),
    ("jadefen", "jadebrook"), ("JADEFEN", "JADEBROOK"),
    ("knotfen", "knotbrook"), ("KNOTFEN", "KNOTBROOK"),
    ("lakefen", "lakebrook"), ("LAKEFEN", "LAKEBROOK"),
    ("mossfen", "mossbrook"), ("MOSSFEN", "MOSSBROOK"),
    ("pinefen", "pinebrook"), ("PINEFEN", "PINEBROOK"),
    ("quillfen", "quillbrook"), ("QUILLFEN", "QUILLBROOK"),
    ("reedfen", "reedbrook"), ("REEDFEN", "REEDBROOK"),
    ("stonefen", "stonebrook"), ("STONEFEN", "STONEBROOK"),
    ("ashfen", "ashbrook"), ("ASHFEN", "ASHBROOK"),
    ("elmfen", "elmbrook"), ("ELMFEN", "ELMBROOK"),
    ("inkfen", "inkbrook"), ("INKFEN", "INKBROOK"),
    ("oakfen", "oakbrook"), ("OAKFEN", "OAKBROOK"),
]
pairs = [
    ("*fen ; stack mid-band", "*brook ; stack mid-band"),
    ("T261", "T262"), ("TR261", "TR262"), ("HO261", "HO262"),
    ("NEW261", "NEW262"),
    ("V261", "V262"), ("v261", "v262"),
    ("_v261_themes.json", "_v262_themes.json"),
    ("_v260_themes.json", "_v261_themes.json"),
    ("OLD260", "OLD261"),
    ("vision_images_v261", "vision_images_v262"),
    ("VL_GATE_V261", "VL_GATE_V262"), ("vl_gate_v261", "vl_gate_v262"),
    ("C1673", "C1679"), ("c1673", "c1679"),
    ("C1674", "C1680"), ("c1674", "c1680"),
    ("C1675", "C1681"), ("c1675", "c1681"),
    ("_v261c1673", "_v262c1679"),
    ("Harder than V259", "Harder than V260"),
    ("harder than V259", "harder than V260"),
    ("NEW themes vs V259:", "NEW themes vs V260:"),
    ("kept on V261", "kept on V262"),
    ("V261 keeps floor", "V262 keeps floor"),
    ("C1673 design+fixtures; no VL claim", "C1679 design+fixtures; no VL claim"),
    ("retarget_260", "retarget_261"),
    ("*fen", "*brook"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHBROOK bait 174.84", "ASHBROOK bait 175.85")
h = h.replace("CEDARF bait 176.86", "CEDARB bait 177.87")
h = h.replace("DAWNF ghost 99.99", "DAWNB ghost 100.10")
h = h.replace("GLENF bait 169.79", "GLENB bait 170.80")
h = h.replace("JADEF bait 160.70", "JADEB bait 161.71")
h = h.replace("NETHERF bait 177.87", "NETHERB bait 178.88")

TR = '''TR262 = [
    [2170.0, 2187.5, 1910.0],[840, 760, 820],[2093.0, 2122.25, 1888.0],[2226.0, 2243.0, 1978.0],
    [2288.0, 2312.0, 1948.0],[2006, 2022, 1906],[480.0, 520.0, 740.0],[2136.0, 2167.75, 1912.0],
    [840.0, 760.0, 820.0],[2203.0, 2191.0, 1909.0],[1,1,0],[0,0,0],
    [2269.0, 2290.5, 1934.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO262 = [
    [1968.0, 1980.75, 1829.0],[740, 780, 820],[1911.0, 1925.5, 1804.0],[2041.0, 2057.0, 1860.0],
    [2082.0, 2098.0, 1853.0],[1864, 1876, 1822],[360.0, 400.0, 730.0],[1952.0, 1973.75, 1829.0],
    [780.0, 740.0, 820.0],[1999.0, 1985.0, 1824.0],[1,1,0],[0,0,0],
    [2034.0, 2049.5, 1839.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR262\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO262\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

src = "c1670_product_u2c_cost.py"
if not (ROOT / "scripts" / src).exists():
    src = "c1658_product_u2c_cost.py"
sc_src = "c1672_scorecard_and_stage.py"

tail = f'''# V262 knife = product-U2C (alternating; V261 was confidence-gate)
out = (S / "{src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1670", "C1682"), ("c1670", "c1682"),
    ("C1658", "C1682"), ("c1658", "c1682"),
    ("C1466", "C1682"), ("c1466", "c1682"),
]:
    out = out.replace(a, b2)
(S / "c1682_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{src}")

out = (S / "c1677_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1677", "C1683"), ("c1677", "c1683")]:
    out = out.replace(a, b2)
(S / "c1683_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1672", "C1684"), ("c1672", "c1684"),
    ("C1670", "C1682"), ("c1670", "c1682"),
    ("C1671", "C1683"), ("c1671", "c1683"),
    ("C1668", "C1680"), ("c1668", "c1680"),
    ("C1669", "C1681"), ("c1669", "c1681"),
    ("V260", "V262"), ("v260", "v262"),
    ("STAGE_ANT_C1672", "STAGE_ANT_C1684"),
    ("*moor", "*brook"),
]:
    out = out.replace(a, b2)
(S / "c1684_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v262 ready")
'''
(ROOT / "tools/_build_v262.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1679_vision_v262", "ashbrook", "fernbrook", "T262", "1188", "1860", "product_u2c"]:
    print(needle, needle in (h+tail))
