from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v304.py").read_text(encoding="utf-8")
idx0 = b0.find('# V304 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1936 = " in head0:
    head0 = head0[:head0.find("SC1936 = ")]

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
    ("T304", "T305"), ("TR304", "TR305"), ("HO304", "HO305"),
    ("NEW304", "NEW305"),
    ("V304", "V305"), ("v304", "v305"),
    ("_v304_themes.json", "_v305_themes.json"),
    ("_v303_themes.json", "_v304_themes.json"),
    ("OLD303", "OLD304"),
    ("vision_images_v304", "vision_images_v305"),
    ("VL_GATE_V304", "VL_GATE_V305"), ("vl_gate_v304", "vl_gate_v305"),
    ("C1931", "C1937"), ("c1931", "c1937"),
    ("C1932", "C1938"), ("c1932", "c1938"),
    ("C1933", "C1939"), ("c1933", "c1939"),
    ("_v304c1931", "_v305c1937"),
    ("Harder than V302", "Harder than V303"),
    ("harder than V302", "harder than V303"),
    ("NEW themes vs V302:", "NEW themes vs V303:"),
    ("kept on V304", "kept on V305"),
    ("V304 keeps floor", "V305 keeps floor"),
    ("C1931 design+fixtures; no VL claim", "C1937 design+fixtures; no VL claim"),
    ("retarget_303", "retarget_304"),
    ("*moor", "*fen"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMOOR bait 217.27", "ASHFEN bait 218.28")
h = h.replace("CEDARM bait 219.29", "CEDARF bait 220.30")
h = h.replace("DAWNM ghost 142.52", "DAWNF ghost 143.53")
h = h.replace("GLENM bait 212.22", "GLENF bait 213.23")
h = h.replace("JADEM bait 203.13", "JADEF bait 204.14")
h = h.replace("NETHERM bait 220.30", "NETHERF bait 221.31")

TR = '''TR305 = [
    [2274.0, 2291.5, 2014.0],[840, 760, 820],[2197.0, 2226.25, 1992.0],[2330.0, 2347.0, 2082.0],
    [2392.0, 2416.0, 2052.0],[2110, 2126, 2010],[490.0, 530.0, 760.0],[2240.0, 2271.75, 2016.0],
    [840.0, 760.0, 820.0],[2307.0, 2295.0, 2013.0],[1,1,0],[0,0,0],
    [2373.0, 2394.5, 2038.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO305 = [
    [2072.0, 2084.75, 1933.0],[640, 660, 820],[2015.0, 2029.5, 1908.0],[2145.0, 2161.0, 1964.0],
    [2186.0, 2202.0, 1957.0],[1968, 1980, 1928],[420.0, 460.0, 740.0],[2056.0, 2077.75, 1933.0],
    [740.0, 780.0, 820.0],[2103.0, 2089.0, 1930.0],[1,1,0],[0,0,0],
    [2138.0, 2153.5, 1943.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR305\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO305\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1928_confidence_gate_stretch.py"
sc_body = (ROOT / "scripts/c1930_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1930", "C1942"), ("c1930", "c1942"),
    ("C1928", "C1940"), ("c1928", "c1940"),
    ("C1929", "C1941"), ("c1929", "c1941"),
    ("C1926", "C1938"), ("c1926", "c1938"),
    ("C1927", "C1939"), ("c1927", "c1939"),
    ("V303", "V305"), ("v303", "v305"),
    ("STAGE_ANT_C1930", "STAGE_ANT_C1942"),
    ("*wick", "*fen"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V305 knife = confidence-gate (alternating; V304 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1928", "C1940"), ("c1928", "c1940"),
    ("C1916", "C1940"), ("c1916", "c1940"),
    ("cg134_", "cg135_"),
    ("conf_gate_stretch_c1928", "conf_gate_stretch_c1940"),
    ("confidence_gate_stretch_v197", "confidence_gate_stretch_v198"),
    ("Stretch vs C1916", "Stretch vs C1928"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 113.00 b paid 117.75 c open 73.00 TOTAL PAID TARGET 230.75", "a paid 114.00 b paid 118.75 c open 74.00 TOTAL PAID TARGET 232.75")
out = out.replace('"model_guess": 999.0, "expected": 230.75', '"model_guess": 999.0, "expected": 232.75')
out = out.replace("SKU1 qty 108 ok SKU2 qty 82 hold SKU3 qty 112 ok qty_sum TARGET 220", "SKU1 qty 109 ok SKU2 qty 83 hold SKU3 qty 113 ok qty_sum TARGET 222")
out = out.replace('"model_guess": 232.0, "expected": 220.0', '"model_guess": 234.0, "expected": 222.0')
out = out.replace("itemR1 89.00 done itemR2 92.75 done itemR3 70.00 open refund_done TARGET 181.75", "itemR1 90.00 done itemR2 93.75 done itemR3 71.00 open refund_done TARGET 183.75")
out = out.replace('"model_guess": 190.5, "expected": 181.75', '"model_guess": 192.5, "expected": 183.75')
out = out.replace("T1 157.00 paid T2 97.00 open T3 138.00 paid tax_base_paid TARGET 295.00", "T1 158.00 paid T2 98.00 open T3 139.00 paid tax_base_paid TARGET 297.00")
out = out.replace('"model_guess": 331.0, "expected": 295.0', '"model_guess": 333.0, "expected": 297.0')
out = out.replace("A 1647 active B 361 leave C 1536 active payroll_active TARGET 3183", "A 1649 active B 362 leave C 1537 active payroll_active TARGET 3186")
out = out.replace('"model_guess": 3413.0, "expected": 3183.0', '"model_guess": 3416.0, "expected": 3186.0')
out = out.replace("P1 102 ok P2 81 hold P3 101 ok ship_ok_qty TARGET 203", "P1 103 ok P2 82 hold P3 102 ok ship_ok_qty TARGET 205")
out = out.replace('"model_guess": 222.0, "expected": 203.0', '"model_guess": 224.0, "expected": 205.0')
out = out.replace("S1 pri 91 open S2 pri 94 closed S3 pri 103 open open_pri_sum TARGET 194", "S1 pri 92 open S2 pri 95 closed S3 pri 104 open open_pri_sum TARGET 196")
out = out.replace('"model_guess": 226.0, "expected": 194.0', '"model_guess": 228.0, "expected": 196.0')
out = out.replace("X 133.00 open Y 136.00 open paid_total TARGET 0.00 bait 269.00", "X 134.00 open Y 137.00 open paid_total TARGET 0.00 bait 271.00")
out = out.replace('"model_guess": 269.0, "expected": 0.0', '"model_guess": 271.0, "expected": 0.0')
out = out.replace("alpha paid 98.00 beta paid 101.00 gamma open 71.00 TOTAL PAID TARGET 199.00", "alpha paid 99.00 beta paid 102.00 gamma open 72.00 TOTAL PAID TARGET 201.00")
out = out.replace('"model_guess": 199.0, "expected": 199.0', '"model_guess": 201.0, "expected": 201.0')
out = out.replace("SKU1 qty 82 ok SKU2 qty 70 hold SKU3 qty 84 ok qty_sum TARGET 166", "SKU1 qty 83 ok SKU2 qty 71 hold SKU3 qty 85 ok qty_sum TARGET 168")
out = out.replace('"model_guess": 166.0, "expected": 166.0', '"model_guess": 168.0, "expected": 168.0')
out = out.replace("itemR1 75.00 done itemR2 77.25 done itemR3 64.00 open refund_done TARGET 152.25", "itemR1 76.00 done itemR2 78.25 done itemR3 65.00 open refund_done TARGET 154.25")
out = out.replace('"model_guess": 152.25, "expected": 152.25', '"model_guess": 154.25, "expected": 154.25')
out = out.replace("tea paid 94.00 rice paid 96.50 soup open 69.00 TOTAL PAID TARGET 190.50", "tea paid 95.00 rice paid 97.50 soup open 70.00 TOTAL PAID TARGET 192.50")
out = out.replace('"model_guess": 198.25, "expected": 190.50', '"model_guess": 200.25, "expected": 192.50')
(S / "c1940_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1935_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1935", "C1941"), ("c1935", "c1941")]:
    out = out.replace(a, b2)
(S / "c1941_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1942_scorecard_and_stage.py").write_text(SC1942, encoding="utf-8")
print("scorecard from fixed c1930 conf-gate pattern")
print("OK builder v305 ready")
'''
pre = "SC1942 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v305.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1937_vision_v305", "ashfen", "fernfen", "T305", "1188", "1928", "confidence_gate", "retarget_304"]:
    print(needle, needle in (h+pre+tail))
