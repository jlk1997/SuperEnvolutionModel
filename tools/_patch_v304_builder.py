from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v303.py").read_text(encoding="utf-8")
idx0 = b0.find('# V303 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1930 = " in head0:
    head0 = head0[:head0.find("SC1930 = ")]

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
    ("T303", "T304"), ("TR303", "TR304"), ("HO303", "HO304"),
    ("NEW303", "NEW304"),
    ("V303", "V304"), ("v303", "v304"),
    ("_v303_themes.json", "_v304_themes.json"),
    ("_v302_themes.json", "_v303_themes.json"),
    ("OLD302", "OLD303"),
    ("vision_images_v303", "vision_images_v304"),
    ("VL_GATE_V303", "VL_GATE_V304"), ("vl_gate_v303", "vl_gate_v304"),
    ("C1925", "C1931"), ("c1925", "c1931"),
    ("C1926", "C1932"), ("c1926", "c1932"),
    ("C1927", "C1933"), ("c1927", "c1933"),
    ("_v303c1925", "_v304c1931"),
    ("Harder than V301", "Harder than V302"),
    ("harder than V301", "harder than V302"),
    ("NEW themes vs V301:", "NEW themes vs V302:"),
    ("kept on V303", "kept on V304"),
    ("V303 keeps floor", "V304 keeps floor"),
    ("C1925 design+fixtures; no VL claim", "C1931 design+fixtures; no VL claim"),
    ("retarget_302", "retarget_303"),
    ("*wick", "*moor"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHWICK bait 216.26", "ASHMOOR bait 217.27")
h = h.replace("CEDARW bait 218.28", "CEDARM bait 219.29")
h = h.replace("DAWNW ghost 141.51", "DAWNM ghost 142.52")
h = h.replace("GLENW bait 211.21", "GLENM bait 212.22")
h = h.replace("JADEW bait 202.12", "JADEM bait 203.13")
h = h.replace("NETHERW bait 219.29", "NETHERM bait 220.30")

TR = '''TR304 = [
    [2272.0, 2289.5, 2012.0],[840, 760, 820],[2195.0, 2224.25, 1990.0],[2328.0, 2345.0, 2080.0],
    [2390.0, 2414.0, 2050.0],[2108, 2124, 2008],[490.0, 530.0, 760.0],[2238.0, 2269.75, 2014.0],
    [840.0, 760.0, 820.0],[2305.0, 2293.0, 2011.0],[1,1,0],[0,0,0],
    [2371.0, 2392.5, 2036.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO304 = [
    [2070.0, 2082.75, 1931.0],[640, 660, 820],[2013.0, 2027.5, 1906.0],[2143.0, 2159.0, 1962.0],
    [2184.0, 2200.0, 1955.0],[1966, 1978, 1926],[420.0, 460.0, 740.0],[2054.0, 2075.75, 1931.0],
    [740.0, 780.0, 820.0],[2101.0, 2087.0, 1928.0],[1,1,0],[0,0,0],
    [2136.0, 2151.5, 1941.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR304\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO304\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c1924_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1924", "C1936"), ("c1924", "c1936"),
    ("C1922", "C1934"), ("c1922", "c1934"),
    ("C1923", "C1935"), ("c1923", "c1935"),
    ("C1920", "C1932"), ("c1920", "c1932"),
    ("C1921", "C1933"), ("c1921", "c1933"),
    ("C1916", "C1928"), ("c1916", "c1928"),
    ("C1919", "C1931"), ("c1919", "c1931"),
    ("V302", "V304"), ("v302", "v304"),
    ("STAGE_ANT_C1924", "STAGE_ANT_C1936"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V304 knife = product-U2C (alternating; V303 was confidence-gate)
out = (S / "c1922_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1922", "C1934"), ("c1922", "c1934"),
    ("C1910", "C1934"), ("c1910", "c1934"),
    ("product_u2c_cost_c1922", "product_u2c_cost_c1934"),
    ("u2c_v195", "u2c_v196"),
    ("u2c_c1922", "u2c_c1934"),
]:
    out = out.replace(a, b2)
(S / "c1934_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1922")

out = (S / "c1929_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1929", "C1935"), ("c1929", "c1935")]:
    out = out.replace(a, b2)
(S / "c1935_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1936_scorecard_and_stage.py").write_text(SC1936, encoding="utf-8")
print("scorecard from fixed c1924 product-U2C pattern")
print("OK builder v304 ready")
'''
pre = "SC1936 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v304.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1931_vision_v304", "ashmoor", "fernmoor", "T304", "1188", "1926", "product_u2c", "retarget_303"]:
    print(needle, needle in (h+pre+tail))
