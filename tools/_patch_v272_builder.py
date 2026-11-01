from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v271.py").read_text(encoding="utf-8")
idx0 = b0.find('# V271 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("nethermoor", "netherfen"), ("NETHERMOOR", "NETHERFEN"),
    ("cedarmoor", "cedarfen"), ("CEDARMOOR", "CEDARFEN"),
    ("dawnmoor", "dawnfen"), ("DAWNMOOR", "DAWNFEN"),
    ("fernmoor", "fernfen"), ("FERNMOOR", "FERNFEN"),
    ("glenmoor", "glenfen"), ("GLENMOOR", "GLENFEN"),
    ("hazemoor", "hazefen"), ("HAZEMOOR", "HAZEFEN"),
    ("jademoor", "jadefen"), ("JADEMOOR", "JADEFEN"),
    ("knotmoor", "knotfen"), ("KNOTMOOR", "KNOTFEN"),
    ("lakemoor", "lakefen"), ("LAKEMOOR", "LAKEFEN"),
    ("mossmoor", "mossfen"), ("MOSSMOOR", "MOSSFEN"),
    ("pinemoor", "pinefen"), ("PINEMOOR", "PINEFEN"),
    ("quillmoor", "quillfen"), ("QUILLMOOR", "QUILLFEN"),
    ("reedmoor", "reedfen"), ("REEDMOOR", "REEDFEN"),
    ("stonemoor", "stonefen"), ("STONEMOOR", "STONEFEN"),
    ("ashmoor", "ashfen"), ("ASHMOOR", "ASHFEN"),
    ("elmmoor", "elmfen"), ("ELMMOOR", "ELMFEN"),
    ("inkmoor", "inkfen"), ("INKMOOR", "INKFEN"),
    ("oakmoor", "oakfen"), ("OAKMOOR", "OAKFEN"),
]
pairs = [
    ("*moor ; stack mid-band", "*fen ; stack mid-band"),
    ("T271", "T272"), ("TR271", "TR272"), ("HO271", "HO272"),
    ("NEW271", "NEW272"),
    ("V271", "V272"), ("v271", "v272"),
    ("_v271_themes.json", "_v272_themes.json"),
    ("_v270_themes.json", "_v271_themes.json"),
    ("OLD270", "OLD271"),
    ("vision_images_v271", "vision_images_v272"),
    ("VL_GATE_V271", "VL_GATE_V272"), ("vl_gate_v271", "vl_gate_v272"),
    ("C1733", "C1739"), ("c1733", "c1739"),
    ("C1734", "C1740"), ("c1734", "c1740"),
    ("C1735", "C1741"), ("c1735", "c1741"),
    ("_v271c1733", "_v272c1739"),
    ("Harder than V269", "Harder than V270"),
    ("harder than V269", "harder than V270"),
    ("NEW themes vs V269:", "NEW themes vs V270:"),
    ("kept on V271", "kept on V272"),
    ("V271 keeps floor", "V272 keeps floor"),
    ("C1733 design+fixtures; no VL claim", "C1739 design+fixtures; no VL claim"),
    ("retarget_270", "retarget_271"),
    ("*moor", "*fen"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMOOR bait 184.94", "ASHFEN bait 185.95")
h = h.replace("ASHFEN bait 184.94", "ASHFEN bait 185.95")
h = h.replace("CEDARM bait 186.96", "CEDARF bait 187.97")
h = h.replace("DAWNM ghost 109.19", "DAWNF ghost 110.20")
h = h.replace("GLENM bait 179.89", "GLENF bait 180.90")
h = h.replace("JADEM bait 170.80", "JADEF bait 171.81")
h = h.replace("NETHERM bait 187.97", "NETHERF bait 188.98")

TR = '''TR272 = [
    [2191.0, 2208.5, 1931.0],[780, 740, 820],[2114.0, 2143.25, 1909.0],[2247.0, 2264.0, 1999.0],
    [2309.0, 2333.0, 1969.0],[2027, 2043, 1927],[490.0, 530.0, 750.0],[2157.0, 2188.75, 1933.0],
    [780.0, 740.0, 820.0],[2224.0, 2212.0, 1930.0],[1,1,0],[0,0,0],
    [2290.0, 2311.5, 1955.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO272 = [
    [1989.0, 2001.75, 1850.0],[640, 660, 820],[1932.0, 1946.5, 1825.0],[2062.0, 2078.0, 1881.0],
    [2103.0, 2119.0, 1874.0],[1885, 1897, 1845],[370.0, 410.0, 740.0],[1973.0, 1994.75, 1850.0],
    [740.0, 780.0, 820.0],[2020.0, 2006.0, 1847.0],[1,1,0],[0,0,0],
    [2055.0, 2070.5, 1860.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
# fix SLA 750 which is BAN - use 760 instead for TR c slot already ok; TR[6] has 750.0 as c - BAN!
# TR[6] = [490.0, 530.0, 750.0] -> change 750 to 760
TR = TR.replace("[490.0, 530.0, 750.0]", "[490.0, 530.0, 760.0]")
# HO[6] 740 ok

h = re.sub(r'TR272\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO272\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

tail = '''# V272 knife = product-U2C (alternating; V271 was confidence-gate)
out = (S / "c1730_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1730", "C1742"), ("c1730", "c1742"),
    ("C1718", "C1742"), ("c1718", "c1742"),
    ("C1466", "C1742"), ("c1466", "c1742"),
]:
    out = out.replace(a, b2)
(S / "c1742_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1730_product_u2c_cost.py")

out = (S / "c1737_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1737", "C1743"), ("c1737", "c1743")]:
    out = out.replace(a, b2)
(S / "c1743_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1732_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1732", "C1744"), ("c1732", "c1744"),
    ("C1730", "C1742"), ("c1730", "c1742"),
    ("C1731", "C1743"), ("c1731", "c1743"),
    ("C1728", "C1740"), ("c1728", "c1740"),
    ("C1729", "C1741"), ("c1729", "c1741"),
    ("V270", "V272"), ("v270", "v272"),
    ("STAGE_ANT_C1732", "STAGE_ANT_C1744"),
    ("*wick", "*fen"),
]:
    out = out.replace(a, b2)
(S / "c1744_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1732_scorecard_and_stage.py")
print("OK builder v272 ready")
'''
(ROOT / "tools/_build_v272.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1739_vision_v272", "ashfen", "fernfen", "T272", "1188", "1845", "product_u2c", "retarget_271"]:
    print(needle, needle in (h+tail))
