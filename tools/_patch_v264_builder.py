from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v263.py").read_text(encoding="utf-8")
idx0 = b0.find('# V263 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
    ("T263", "T264"), ("TR263", "TR264"), ("HO263", "HO264"),
    ("NEW263", "NEW264"),
    ("V263", "V264"), ("v263", "v264"),
    ("_v263_themes.json", "_v264_themes.json"),
    ("_v262_themes.json", "_v263_themes.json"),
    ("OLD262", "OLD263"),
    ("vision_images_v263", "vision_images_v264"),
    ("VL_GATE_V263", "VL_GATE_V264"), ("vl_gate_v263", "vl_gate_v264"),
    ("C1685", "C1691"), ("c1685", "c1691"),
    ("C1686", "C1692"), ("c1686", "c1692"),
    ("C1687", "C1693"), ("c1687", "c1693"),
    ("_v263c1685", "_v264c1691"),
    ("Harder than V261", "Harder than V262"),
    ("harder than V261", "harder than V262"),
    ("NEW themes vs V261:", "NEW themes vs V262:"),
    ("kept on V263", "kept on V264"),
    ("V263 keeps floor", "V264 keeps floor"),
    ("C1685 design+fixtures; no VL claim", "C1691 design+fixtures; no VL claim"),
    ("retarget_262", "retarget_263"),
    ("*dale", "*ford"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFORD bait 176.86", "ASHFORD bait 177.87")
h = h.replace("CEDARD bait 178.88", "CEDARF bait 179.89")
h = h.replace("DAWND ghost 101.11", "DAWNF ghost 102.12")
h = h.replace("GLEND bait 171.81", "GLENF bait 172.82")
h = h.replace("JADED bait 162.72", "JADEF bait 163.73")
h = h.replace("NETHERD bait 179.89", "NETHERF bait 180.90")

TR = '''TR264 = [
    [2174.0, 2191.5, 1914.0],[840, 760, 820],[2097.0, 2126.25, 1892.0],[2230.0, 2247.0, 1982.0],
    [2292.0, 2316.0, 1952.0],[2010, 2026, 1910],[480.0, 520.0, 740.0],[2140.0, 2171.75, 1916.0],
    [840.0, 760.0, 820.0],[2207.0, 2195.0, 1913.0],[1,1,0],[0,0,0],
    [2273.0, 2294.5, 1938.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO264 = [
    [1972.0, 1984.75, 1833.0],[740, 780, 820],[1915.0, 1929.5, 1808.0],[2045.0, 2061.0, 1864.0],
    [2086.0, 2102.0, 1857.0],[1868, 1880, 1826],[360.0, 400.0, 730.0],[1956.0, 1977.75, 1833.0],
    [780.0, 740.0, 820.0],[2003.0, 1989.0, 1828.0],[1,1,0],[0,0,0],
    [2038.0, 2053.5, 1843.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR264\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO264\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

src = "c1682_product_u2c_cost.py"
if not (ROOT / "scripts" / src).exists():
    src = "c1670_product_u2c_cost.py"
sc_src = "c1684_scorecard_and_stage.py"

tail = f'''# V264 knife = product-U2C (alternating; V263 was confidence-gate)
out = (S / "{src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1682", "C1694"), ("c1682", "c1694"),
    ("C1670", "C1694"), ("c1670", "c1694"),
    ("C1466", "C1694"), ("c1466", "c1694"),
]:
    out = out.replace(a, b2)
(S / "c1694_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{src}")

out = (S / "c1689_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1689", "C1695"), ("c1689", "c1695")]:
    out = out.replace(a, b2)
(S / "c1695_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1684", "C1696"), ("c1684", "c1696"),
    ("C1682", "C1694"), ("c1682", "c1694"),
    ("C1683", "C1695"), ("c1683", "c1695"),
    ("C1680", "C1692"), ("c1680", "c1692"),
    ("C1681", "C1693"), ("c1681", "c1693"),
    ("V262", "V264"), ("v262", "v264"),
    ("STAGE_ANT_C1684", "STAGE_ANT_C1696"),
    ("*brook", "*ford"),
]:
    out = out.replace(a, b2)
(S / "c1696_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v264 ready")
'''
(ROOT / "tools/_build_v264.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1691_vision_v264", "ashford", "fernford", "T264", "1188", "1864", "product_u2c"]:
    print(needle, needle in (h+tail))
