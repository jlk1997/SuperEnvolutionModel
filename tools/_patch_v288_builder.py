from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v287.py").read_text(encoding="utf-8")
idx0 = b0.find('# V287 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("netherhurst", "nethermere"), ("NETHERHURST", "NETHERMERE"),
    ("cedarhurst", "cedarmere"), ("CEDARHURST", "CEDARMERE"),
    ("dawnhurst", "dawnmere"), ("DAWNHURST", "DAWNMERE"),
    ("fernhurst", "fernmere"), ("FERNHURST", "FERNMERE"),
    ("glenhurst", "glenmere"), ("GLENHURST", "GLENMERE"),
    ("hazehurst", "hazemere"), ("HAZEHURST", "HAZEMERE"),
    ("jadehurst", "jademere"), ("JADEHURST", "JADEMERE"),
    ("knothurst", "knotmere"), ("KNOTHURST", "KNOTMERE"),
    ("lakehurst", "lakemere"), ("LAKEHURST", "LAKEMERE"),
    ("mosshurst", "mossmere"), ("MOSSHURST", "MOSSMERE"),
    ("pinehurst", "pinemere"), ("PINEHURST", "PINEMERE"),
    ("quillhurst", "quillmere"), ("QUILLHURST", "QUILLMERE"),
    ("reedhurst", "reedmere"), ("REEDHURST", "REEDMERE"),
    ("stonehurst", "stonemere"), ("STONEHURST", "STONEMERE"),
    ("ashhurst", "ashmere"), ("ASHHURST", "ASHMERE"),
    ("elmhurst", "elmmere"), ("ELMHURST", "ELMMERE"),
    ("inkhurst", "inkmere"), ("INKHURST", "INKMERE"),
    ("oakhurst", "oakmere"), ("OAKHURST", "OAKMERE"),
]
pairs = [
    ("*hurst ; stack mid-band", "*mere ; stack mid-band"),
    ("T287", "T288"), ("TR287", "TR288"), ("HO287", "HO288"),
    ("NEW287", "NEW288"),
    ("V287", "V288"), ("v287", "v288"),
    ("_v287_themes.json", "_v288_themes.json"),
    ("_v286_themes.json", "_v287_themes.json"),
    ("OLD286", "OLD287"),
    ("vision_images_v287", "vision_images_v288"),
    ("VL_GATE_V287", "VL_GATE_V288"), ("vl_gate_v287", "vl_gate_v288"),
    ("C1829", "C1835"), ("c1829", "c1835"),
    ("C1830", "C1836"), ("c1830", "c1836"),
    ("C1831", "C1837"), ("c1831", "c1837"),
    ("_v287c1829", "_v288c1835"),
    ("Harder than V285", "Harder than V286"),
    ("harder than V285", "harder than V286"),
    ("NEW themes vs V285:", "NEW themes vs V286:"),
    ("kept on V287", "kept on V288"),
    ("V287 keeps floor", "V288 keeps floor"),
    ("C1829 design+fixtures; no VL claim", "C1835 design+fixtures; no VL claim"),
    ("retarget_286", "retarget_287"),
    ("*hurst", "*mere"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHURST bait 200.10", "ASHMERE bait 201.11")
h = h.replace("CEDARH bait 202.12", "CEDARM bait 203.13")
h = h.replace("DAWNH ghost 125.35", "DAWNM ghost 126.36")
h = h.replace("GLENH bait 195.05", "GLENM bait 196.06")
h = h.replace("JADEH bait 186.96", "JADEM bait 187.97")
h = h.replace("NETHERH bait 203.13", "NETHERM bait 204.14")

TR = '''TR288 = [
    [2239.0, 2256.5, 1979.0],[840, 760, 820],[2162.0, 2191.25, 1957.0],[2295.0, 2312.0, 2047.0],
    [2357.0, 2381.0, 2017.0],[2075, 2091, 1975],[490.0, 530.0, 760.0],[2205.0, 2236.75, 1981.0],
    [840.0, 760.0, 820.0],[2272.0, 2260.0, 1978.0],[1,1,0],[0,0,0],
    [2338.0, 2359.5, 2003.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO288 = [
    [2037.0, 2049.75, 1898.0],[640, 660, 820],[1980.0, 1994.5, 1873.0],[2110.0, 2126.0, 1929.0],
    [2151.0, 2167.0, 1922.0],[1933, 1945, 1893],[420.0, 460.0, 740.0],[2021.0, 2042.75, 1898.0],
    [740.0, 780.0, 820.0],[2068.0, 2054.0, 1895.0],[1,1,0],[0,0,0],
    [2103.0, 2118.5, 1908.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR288\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO288\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

tail = '''# V288 knife = product-U2C (alternating; V287 was confidence-gate)
out = (S / "c1826_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1826", "C1838"), ("c1826", "c1838"),
    ("C1814", "C1838"), ("c1814", "c1838"),
    ("C1466", "C1838"), ("c1466", "c1838"),
]:
    out = out.replace(a, b2)
(S / "c1838_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1826_product_u2c_cost.py")

out = (S / "c1833_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1833", "C1839"), ("c1833", "c1839")]:
    out = out.replace(a, b2)
(S / "c1839_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1828_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1828", "C1840"), ("c1828", "c1840"),
    ("C1826", "C1838"), ("c1826", "c1838"),
    ("C1827", "C1839"), ("c1827", "c1839"),
    ("C1824", "C1836"), ("c1824", "c1836"),
    ("C1825", "C1837"), ("c1825", "c1837"),
    ("V286", "V288"), ("v286", "v288"),
    ("STAGE_ANT_C1828", "STAGE_ANT_C1840"),
    ("*ford", "*mere"),
]:
    out = out.replace(a, b2)
(S / "c1840_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1828_scorecard_and_stage.py")
print("OK builder v288 ready")
'''
(ROOT / "tools/_build_v288.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1835_vision_v288", "ashmere", "fernmere", "T288", "1188", "1893", "product_u2c", "retarget_287"]:
    print(needle, needle in (h+tail))
