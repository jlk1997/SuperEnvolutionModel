from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v253.py").read_text(encoding="utf-8")
idx0 = b0.find('# V253 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("netherford", "netherhurst"), ("NETHERFORD", "NETHERHURST"),
    ("cedarford", "cedarhurst"), ("CEDARFORD", "CEDARHURST"),
    ("dawnford", "dawnhurst"), ("DAWNFORD", "DAWNHURST"),
    ("fernford", "fernhurst"), ("FERNFORD", "FERNHURST"),
    ("glenford", "glenhurst"), ("GLENFORD", "GLENHURST"),
    ("hazeford", "hazehurst"), ("HAZEFORD", "HAZEHURST"),
    ("jadeford", "jadehurst"), ("JADEFORD", "JADEHURST"),
    ("knotford", "knothurst"), ("KNOTFORD", "KNOTHURST"),
    ("lakeford", "lakehurst"), ("LAKEFORD", "LAKEHURST"),
    ("mossford", "mosshurst"), ("MOSSFORD", "MOSSHURST"),
    ("pineford", "pinehurst"), ("PINEFORD", "PINEHURST"),
    ("quillford", "quillhurst"), ("QUILLFORD", "QUILLHURST"),
    ("reedford", "reedhurst"), ("REEDFORD", "REEDHURST"),
    ("stoneford", "stonehurst"), ("STONEFORD", "STONEHURST"),
    ("ashford", "ashhurst"), ("ASHFORD", "ASHHURST"),
    ("elmford", "elmhurst"), ("ELMFORD", "ELMHURST"),
    ("inkford", "inkhurst"), ("INKFORD", "INKHURST"),
    ("oakford", "oakhurst"), ("OAKFORD", "OAKHURST"),
]
pairs = [
    ("*ford ; stack mid-band", "*hurst ; stack mid-band"),
    ("T253", "T254"), ("TR253", "TR254"), ("HO253", "HO254"),
    ("NEW253", "NEW254"),
    ("V253", "V254"), ("v253", "v254"),
    ("_v253_themes.json", "_v254_themes.json"),
    ("_v252_themes.json", "_v253_themes.json"),
    ("OLD252", "OLD253"),
    ("vision_images_v253", "vision_images_v254"),
    ("VL_GATE_V253", "VL_GATE_V254"), ("vl_gate_v253", "vl_gate_v254"),
    ("C1625", "C1631"), ("c1625", "c1631"),
    ("C1626", "C1632"), ("c1626", "c1632"),
    ("C1627", "C1633"), ("c1627", "c1633"),
    ("_v253c1625", "_v254c1631"),
    ("Harder than V251", "Harder than V252"),
    ("harder than V251", "harder than V252"),
    ("NEW themes vs V251:", "NEW themes vs V252:"),
    ("kept on V253", "kept on V254"),
    ("V253 keeps floor", "V254 keeps floor"),
    ("C1625 design+fixtures; no VL claim", "C1631 design+fixtures; no VL claim"),
    ("retarget_252", "retarget_253"),
    ("*ford", "*hurst"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHURST bait 166.76", "ASHHURST bait 167.77")
h = h.replace("CEDARF bait 168.78", "CEDARH bait 169.79")
h = h.replace("DAWNF ghost 91.91", "DAWNH ghost 92.92")
h = h.replace("GLENF bait 161.71", "GLENH bait 162.72")
h = h.replace("JADEF bait 152.62", "JADEH bait 153.63")
h = h.replace("NETHERF bait 169.79", "NETHERH bait 170.80")

TR = '''TR254 = [
    [2154.0, 2171.5, 1894.0],[840, 760, 820],[2077.0, 2106.25, 1872.0],[2210.0, 2227.0, 1962.0],
    [2272.0, 2296.0, 1932.0],[1990, 2006, 1890],[480.0, 520.0, 740.0],[2120.0, 2151.75, 1896.0],
    [840.0, 760.0, 820.0],[2187.0, 2175.0, 1893.0],[1,1,0],[0,0,0],
    [2253.0, 2274.5, 1918.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO254 = [
    [1952.0, 1964.75, 1813.0],[740, 780, 820],[1895.0, 1909.5, 1788.0],[2025.0, 2041.0, 1844.0],
    [2066.0, 2082.0, 1837.0],[1848, 1860, 1806],[360.0, 400.0, 730.0],[1936.0, 1957.75, 1813.0],
    [780.0, 740.0, 820.0],[1983.0, 1969.0, 1808.0],[1,1,0],[0,0,0],
    [2018.0, 2033.5, 1823.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR254\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO254\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

src = "c1622_product_u2c_cost.py"
if not (ROOT / "scripts" / src).exists():
    src = "c1610_product_u2c_cost.py"
sc_src = "c1624_scorecard_and_stage.py"

tail = f'''# V254 knife = product-U2C (alternating; V253 was confidence-gate)
out = (S / "{src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1622", "C1634"), ("c1622", "c1634"),
    ("C1610", "C1634"), ("c1610", "c1634"),
    ("C1466", "C1634"), ("c1466", "c1634"),
]:
    out = out.replace(a, b2)
(S / "c1634_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{src}")

out = (S / "c1629_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1629", "C1635"), ("c1629", "c1635")]:
    out = out.replace(a, b2)
(S / "c1635_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1624", "C1636"), ("c1624", "c1636"),
    ("C1622", "C1634"), ("c1622", "c1634"),
    ("C1623", "C1635"), ("c1623", "c1635"),
    ("C1620", "C1632"), ("c1620", "c1632"),
    ("C1621", "C1633"), ("c1621", "c1633"),
    ("V252", "V254"), ("v252", "v254"),
    ("STAGE_ANT_C1624", "STAGE_ANT_C1636"),
    ("*dale", "*hurst"),
]:
    out = out.replace(a, b2)
(S / "c1636_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v254 ready")
'''
(ROOT / "tools/_build_v254.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1631_vision_v254", "ashhurst", "fernhurst", "T254", "1188", "1844", "product_u2c"]:
    print(needle, needle in (h+tail))
