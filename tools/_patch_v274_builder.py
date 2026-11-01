from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v273.py").read_text(encoding="utf-8")
idx0 = b0.find('# V273 knife = confidence-gate')
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
    ("T273", "T274"), ("TR273", "TR274"), ("HO273", "HO274"),
    ("NEW273", "NEW274"),
    ("V273", "V274"), ("v273", "v274"),
    ("_v273_themes.json", "_v274_themes.json"),
    ("_v272_themes.json", "_v273_themes.json"),
    ("OLD272", "OLD273"),
    ("vision_images_v273", "vision_images_v274"),
    ("VL_GATE_V273", "VL_GATE_V274"), ("vl_gate_v273", "vl_gate_v274"),
    ("C1745", "C1751"), ("c1745", "c1751"),
    ("C1746", "C1752"), ("c1746", "c1752"),
    ("C1747", "C1753"), ("c1747", "c1753"),
    ("_v273c1745", "_v274c1751"),
    ("Harder than V271", "Harder than V272"),
    ("harder than V271", "harder than V272"),
    ("NEW themes vs V271:", "NEW themes vs V272:"),
    ("kept on V273", "kept on V274"),
    ("V273 keeps floor", "V274 keeps floor"),
    ("C1745 design+fixtures; no VL claim", "C1751 design+fixtures; no VL claim"),
    ("retarget_272", "retarget_273"),
    ("*brook", "*dale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHBROOK bait 186.96", "ASHDALE bait 187.97")
h = h.replace("CEDARB bait 188.98", "CEDARD bait 189.99")
h = h.replace("DAWNB ghost 111.21", "DAWND ghost 112.22")
h = h.replace("GLENB bait 181.91", "GLEND bait 182.92")
h = h.replace("JADEB bait 172.82", "JADED bait 173.83")
h = h.replace("NETHERB bait 189.99", "NETHERD bait 190.00")

TR = '''TR274 = [
    [2197.0, 2214.5, 1937.0],[840, 760, 820],[2120.0, 2149.25, 1915.0],[2253.0, 2270.0, 2005.0],
    [2315.0, 2339.0, 1975.0],[2033, 2049, 1933],[510.0, 550.0, 760.0],[2163.0, 2194.75, 1939.0],
    [840.0, 760.0, 820.0],[2230.0, 2218.0, 1936.0],[1,1,0],[0,0,0],
    [2296.0, 2317.5, 1961.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO274 = [
    [1995.0, 2007.75, 1856.0],[640, 660, 820],[1938.0, 1952.5, 1831.0],[2068.0, 2084.0, 1887.0],
    [2109.0, 2125.0, 1880.0],[1891, 1903, 1851],[390.0, 430.0, 740.0],[1979.0, 2000.75, 1856.0],
    [740.0, 780.0, 820.0],[2026.0, 2012.0, 1853.0],[1,1,0],[0,0,0],
    [2061.0, 2076.5, 1866.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR274\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO274\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

tail = '''# V274 knife = product-U2C (alternating; V273 was confidence-gate)
out = (S / "c1742_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1742", "C1754"), ("c1742", "c1754"),
    ("C1730", "C1754"), ("c1730", "c1754"),
    ("C1466", "C1754"), ("c1466", "c1754"),
]:
    out = out.replace(a, b2)
(S / "c1754_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1742_product_u2c_cost.py")

out = (S / "c1749_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1749", "C1755"), ("c1749", "c1755")]:
    out = out.replace(a, b2)
(S / "c1755_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1744_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1744", "C1756"), ("c1744", "c1756"),
    ("C1742", "C1754"), ("c1742", "c1754"),
    ("C1743", "C1755"), ("c1743", "c1755"),
    ("C1740", "C1752"), ("c1740", "c1752"),
    ("C1741", "C1753"), ("c1741", "c1753"),
    ("V272", "V274"), ("v272", "v274"),
    ("STAGE_ANT_C1744", "STAGE_ANT_C1756"),
    ("*fen", "*dale"),
]:
    out = out.replace(a, b2)
(S / "c1756_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1744_scorecard_and_stage.py")
print("OK builder v274 ready")
'''
(ROOT / "tools/_build_v274.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1751_vision_v274", "ashdale", "ferndale", "T274", "1188", "1851", "product_u2c", "retarget_273"]:
    print(needle, needle in (h+tail))
