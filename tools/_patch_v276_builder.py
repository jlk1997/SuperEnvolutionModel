from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v275.py").read_text(encoding="utf-8")
idx0 = b0.find('# V275 knife = confidence-gate')
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
    ("T275", "T276"), ("TR275", "TR276"), ("HO275", "HO276"),
    ("NEW275", "NEW276"),
    ("V275", "V276"), ("v275", "v276"),
    ("_v275_themes.json", "_v276_themes.json"),
    ("_v274_themes.json", "_v275_themes.json"),
    ("OLD274", "OLD275"),
    ("vision_images_v275", "vision_images_v276"),
    ("VL_GATE_V275", "VL_GATE_V276"), ("vl_gate_v275", "vl_gate_v276"),
    ("C1757", "C1763"), ("c1757", "c1763"),
    ("C1758", "C1764"), ("c1758", "c1764"),
    ("C1759", "C1765"), ("c1759", "c1765"),
    ("_v275c1757", "_v276c1763"),
    ("Harder than V273", "Harder than V274"),
    ("harder than V273", "harder than V274"),
    ("NEW themes vs V273:", "NEW themes vs V274:"),
    ("kept on V275", "kept on V276"),
    ("V275 keeps floor", "V276 keeps floor"),
    ("C1757 design+fixtures; no VL claim", "C1763 design+fixtures; no VL claim"),
    ("retarget_274", "retarget_275"),
    ("*ford", "*hurst"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFORD bait 188.98", "ASHHURST bait 189.99")
h = h.replace("CEDARF bait 190.00", "CEDARH bait 191.01")
h = h.replace("DAWNF ghost 113.23", "DAWNH ghost 114.24")
h = h.replace("GLENF bait 183.93", "GLENH bait 184.94")
h = h.replace("JADEF bait 174.84", "JADEH bait 175.85")
h = h.replace("NETHERF bait 191.01", "NETHERH bait 192.02")

TR = '''TR276 = [
    [2203.0, 2220.5, 1943.0],[840, 760, 820],[2126.0, 2155.25, 1921.0],[2259.0, 2276.0, 2011.0],
    [2321.0, 2345.0, 1981.0],[2039, 2055, 1939],[530.0, 570.0, 760.0],[2169.0, 2200.75, 1945.0],
    [840.0, 760.0, 820.0],[2236.0, 2224.0, 1942.0],[1,1,0],[0,0,0],
    [2302.0, 2323.5, 1967.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO276 = [
    [2001.0, 2013.75, 1862.0],[640, 660, 820],[1944.0, 1958.5, 1837.0],[2074.0, 2090.0, 1893.0],
    [2115.0, 2131.0, 1886.0],[1897, 1909, 1857],[410.0, 450.0, 740.0],[1985.0, 2006.75, 1862.0],
    [740.0, 780.0, 820.0],[2032.0, 2018.0, 1859.0],[1,1,0],[0,0,0],
    [2067.0, 2082.5, 1872.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR276\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO276\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

tail = '''# V276 knife = product-U2C (alternating; V275 was confidence-gate)
out = (S / "c1754_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1754", "C1766"), ("c1754", "c1766"),
    ("C1742", "C1766"), ("c1742", "c1766"),
    ("C1466", "C1766"), ("c1466", "c1766"),
]:
    out = out.replace(a, b2)
(S / "c1766_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1754_product_u2c_cost.py")

out = (S / "c1761_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1761", "C1767"), ("c1761", "c1767")]:
    out = out.replace(a, b2)
(S / "c1767_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1756_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1756", "C1768"), ("c1756", "c1768"),
    ("C1754", "C1766"), ("c1754", "c1766"),
    ("C1755", "C1767"), ("c1755", "c1767"),
    ("C1752", "C1764"), ("c1752", "c1764"),
    ("C1753", "C1765"), ("c1753", "c1765"),
    ("V274", "V276"), ("v274", "v276"),
    ("STAGE_ANT_C1756", "STAGE_ANT_C1768"),
    ("*dale", "*hurst"),
]:
    out = out.replace(a, b2)
(S / "c1768_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1756_scorecard_and_stage.py")
print("OK builder v276 ready")
'''
(ROOT / "tools/_build_v276.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1763_vision_v276", "ashhurst", "fernhurst", "T276", "1188", "1857", "product_u2c", "retarget_275"]:
    print(needle, needle in (h+tail))
