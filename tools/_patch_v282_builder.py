from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v281.py").read_text(encoding="utf-8")
idx0 = b0.find('# V281 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("netherwick", "nethermoor"), ("NETHERWICK", "NETHERMOOR"),
    ("cedarwick", "cedarmoor"), ("CEDARWICK", "CEDARMOOR"),
    ("dawnwick", "dawnmoor"), ("DAWNWICK", "DAWNMOOR"),
    ("fernwick", "fernmoor"), ("FERNWICK", "FERNMOOR"),
    ("glenwick", "glenmoor"), ("GLENWICK", "GLENMOOR"),
    ("hazewick", "hazemoor"), ("HAZEWICK", "HAZEMOOR"),
    ("jadewick", "jademoor"), ("JADEWICK", "JADEMOOR"),
    ("knotwick", "knotmoor"), ("KNOTWICK", "KNOTMOOR"),
    ("lakewick", "lakemoor"), ("LAKEWICK", "LAKEMOOR"),
    ("mosswick", "mossmoor"), ("MOSSWICK", "MOSSMOOR"),
    ("pinewick", "pinemoor"), ("PINEWICK", "PINEMOOR"),
    ("quillwick", "quillmoor"), ("QUILLWICK", "QUILLMOOR"),
    ("reedwick", "reedmoor"), ("REEDWICK", "REEDMOOR"),
    ("stonewick", "stonemoor"), ("STONEWICK", "STONEMOOR"),
    ("ashwick", "ashmoor"), ("ASHWICK", "ASHMOOR"),
    ("elmwick", "elmmoor"), ("ELMWICK", "ELMMOOR"),
    ("inkwick", "inkmoor"), ("INKWICK", "INKMOOR"),
    ("oakwick", "oakmoor"), ("OAKWICK", "OAKMOOR"),
]
pairs = [
    ("*wick ; stack mid-band", "*moor ; stack mid-band"),
    ("T281", "T282"), ("TR281", "TR282"), ("HO281", "HO282"),
    ("NEW281", "NEW282"),
    ("V281", "V282"), ("v281", "v282"),
    ("_v281_themes.json", "_v282_themes.json"),
    ("_v280_themes.json", "_v281_themes.json"),
    ("OLD280", "OLD281"),
    ("vision_images_v281", "vision_images_v282"),
    ("VL_GATE_V281", "VL_GATE_V282"), ("vl_gate_v281", "vl_gate_v282"),
    ("C1793", "C1799"), ("c1793", "c1799"),
    ("C1794", "C1800"), ("c1794", "c1800"),
    ("C1795", "C1801"), ("c1795", "c1801"),
    ("_v281c1793", "_v282c1799"),
    ("Harder than V279", "Harder than V280"),
    ("harder than V279", "harder than V280"),
    ("NEW themes vs V279:", "NEW themes vs V280:"),
    ("kept on V281", "kept on V282"),
    ("V281 keeps floor", "V282 keeps floor"),
    ("C1793 design+fixtures; no VL claim", "C1799 design+fixtures; no VL claim"),
    ("retarget_280", "retarget_281"),
    ("*wick", "*moor"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHWICK bait 194.04", "ASHMOOR bait 195.05")
h = h.replace("CEDARW bait 196.06", "CEDARM bait 197.07")
h = h.replace("DAWNW ghost 119.29", "DAWNM ghost 120.30")
h = h.replace("GLENW bait 189.99", "GLENM bait 190.00")
h = h.replace("JADEW bait 180.90", "JADEM bait 181.91")
h = h.replace("NETHERW bait 197.07", "NETHERM bait 198.08")

TR = '''TR282 = [
    [2221.0, 2238.5, 1961.0],[840, 760, 820],[2144.0, 2173.25, 1939.0],[2277.0, 2294.0, 2029.0],
    [2339.0, 2363.0, 1999.0],[2057, 2073, 1957],[490.0, 530.0, 760.0],[2187.0, 2218.75, 1963.0],
    [840.0, 760.0, 820.0],[2254.0, 2242.0, 1960.0],[1,1,0],[0,0,0],
    [2320.0, 2341.5, 1985.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO282 = [
    [2019.0, 2031.75, 1880.0],[640, 660, 820],[1962.0, 1976.5, 1855.0],[2092.0, 2108.0, 1911.0],
    [2133.0, 2149.0, 1904.0],[1915, 1927, 1875],[420.0, 460.0, 740.0],[2003.0, 2024.75, 1880.0],
    [740.0, 780.0, 820.0],[2050.0, 2036.0, 1877.0],[1,1,0],[0,0,0],
    [2085.0, 2100.5, 1890.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR282\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO282\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

tail = '''# V282 knife = product-U2C (alternating; V281 was confidence-gate)
out = (S / "c1790_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1790", "C1802"), ("c1790", "c1802"),
    ("C1778", "C1802"), ("c1778", "c1802"),
    ("C1466", "C1802"), ("c1466", "c1802"),
]:
    out = out.replace(a, b2)
(S / "c1802_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1790_product_u2c_cost.py")

out = (S / "c1797_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1797", "C1803"), ("c1797", "c1803")]:
    out = out.replace(a, b2)
(S / "c1803_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1792_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1792", "C1804"), ("c1792", "c1804"),
    ("C1790", "C1802"), ("c1790", "c1802"),
    ("C1791", "C1803"), ("c1791", "c1803"),
    ("C1788", "C1800"), ("c1788", "c1800"),
    ("C1789", "C1801"), ("c1789", "c1801"),
    ("V280", "V282"), ("v280", "v282"),
    ("STAGE_ANT_C1792", "STAGE_ANT_C1804"),
    ("*holm", "*moor"),
]:
    out = out.replace(a, b2)
(S / "c1804_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1792_scorecard_and_stage.py")
print("OK builder v282 ready")
'''
(ROOT / "tools/_build_v282.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1799_vision_v282", "ashmoor", "fernmoor", "T282", "1188", "1875", "product_u2c", "retarget_281"]:
    print(needle, needle in (h+tail))
