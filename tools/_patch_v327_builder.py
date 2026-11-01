from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v326.py").read_text(encoding="utf-8")
idx0 = b0.find('# V326 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2068 = " in head0:
    head0 = head0[:head0.find("SC2068 = ")]

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
    ("T326", "T327"), ("TR326", "TR327"), ("HO326", "HO327"),
    ("NEW326", "NEW327"),
    ("V326", "V327"), ("v326", "v327"),
    ("_v326_themes.json", "_v327_themes.json"),
    ("_v325_themes.json", "_v326_themes.json"),
    ("OLD325", "OLD326"),
    ("vision_images_v326", "vision_images_v327"),
    ("VL_GATE_V326", "VL_GATE_V327"), ("vl_gate_v326", "vl_gate_v327"),
    ("C2063", "C2069"), ("c2063", "c2069"),
    ("C2064", "C2070"), ("c2064", "c2070"),
    ("C2065", "C2071"), ("c2065", "c2071"),
    ("_v326c2063", "_v327c2069"),
    ("Harder than V324", "Harder than V325"),
    ("harder than V324", "harder than V325"),
    ("NEW themes vs V324:", "NEW themes vs V325:"),
    ("kept on V326", "kept on V327"),
    ("V326 keeps floor", "V327 keeps floor"),
    ("C2063 design+fixtures; no VL claim", "C2069 design+fixtures; no VL claim"),
    ("retarget_325", "retarget_326"),
    ("*moor", "*fen"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMOOR bait 239.49", "ASHFEN bait 240.50")
h = h.replace("CEDARM bait 241.51", "CEDARF bait 242.52")
h = h.replace("DAWNM ghost 164.74", "DAWNF ghost 165.75")
h = h.replace("GLENM bait 234.44", "GLENF bait 235.45")
h = h.replace("JADEM bait 225.35", "JADEF bait 226.36")
h = h.replace("NETHERM bait 242.52", "NETHERF bait 243.53")

TR = '''TR327 = [
    [2318.0, 2335.5, 2058.0],[840, 760, 820],[2241.0, 2250.25, 2036.0],[2374.0, 2391.0, 2126.0],
    [2436.0, 2460.0, 2096.0],[2154, 2170, 2054],[490.0, 530.0, 760.0],[2284.0, 2315.75, 2060.0],
    [840.0, 760.0, 820.0],[2351.0, 2339.0, 2057.0],[1,1,0],[0,0,0],
    [2417.0, 2438.5, 2082.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO327 = [
    [2116.0, 2128.75, 1977.0],[640, 660, 820],[2059.0, 2073.5, 1952.0],[2189.0, 2205.0, 2008.0],
    [2230.0, 2246.0, 2001.0],[2012, 2024, 1974],[420.0, 460.0, 740.0],[2100.0, 2121.75, 1977.0],
    [740.0, 780.0, 820.0],[2147.0, 2133.0, 1974.0],[1,1,0],[0,0,0],
    [2182.0, 2197.5, 1987.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR327\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO327\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2062_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2062", "C2074"), ("c2062", "c2074"),
    ("C2060", "C2072"), ("c2060", "c2072"),
    ("C2061", "C2073"), ("c2061", "c2073"),
    ("C2058", "C2070"), ("c2058", "c2070"),
    ("C2059", "C2071"), ("c2059", "c2071"),
    ("C2057", "C2069"), ("c2057", "c2069"),
    ("C2054", "C2066"), ("c2054", "c2066"),
    ("V325", "V327"), ("v325", "v327"),
    ("STAGE_ANT_C2062", "STAGE_ANT_C2074"),
    ("*wick", "*fen"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V327 knife = confidence-gate (alternating; V326 was product-U2C)
out = (S / "c2060_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2060", "C2072"), ("c2060", "c2072"),
    ("C2048", "C2072"), ("c2048", "c2072"),
    ("cg145_", "cg146_"),
    ("conf_gate_stretch_c2060", "conf_gate_stretch_c2072"),
    ("confidence_gate_stretch_v208", "confidence_gate_stretch_v209"),
    ("Stretch vs C2048", "Stretch vs C2060"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 124.00 b paid 128.75 c open 84.00 TOTAL PAID TARGET 252.75", "a paid 125.00 b paid 129.75 c open 85.00 TOTAL PAID TARGET 254.75")
out = out.replace('"model_guess": 999.0, "expected": 252.75', '"model_guess": 999.0, "expected": 254.75')
out = out.replace("SKU1 qty 119 ok SKU2 qty 93 hold SKU3 qty 123 ok qty_sum TARGET 242", "SKU1 qty 120 ok SKU2 qty 94 hold SKU3 qty 124 ok qty_sum TARGET 244")
out = out.replace('"model_guess": 254.0, "expected": 242.0', '"model_guess": 256.0, "expected": 244.0')
out = out.replace("itemR1 100.00 done itemR2 103.75 done itemR3 81.00 open refund_done TARGET 203.75", "itemR1 101.00 done itemR2 104.75 done itemR3 82.00 open refund_done TARGET 205.75")
out = out.replace('"model_guess": 212.5, "expected": 203.75', '"model_guess": 214.5, "expected": 205.75')
out = out.replace("T1 168.00 paid T2 108.00 open T3 149.00 paid tax_base_paid TARGET 317.00", "T1 169.00 paid T2 109.00 open T3 150.00 paid tax_base_paid TARGET 319.00")
out = out.replace('"model_guess": 353.0, "expected": 317.0', '"model_guess": 355.0, "expected": 319.0')
out = out.replace("A 1663 active B 372 leave C 1547 active payroll_active TARGET 3210", "A 1664 active B 373 leave C 1548 active payroll_active TARGET 3212")
out = out.replace('"model_guess": 3440.0, "expected": 3210.0', '"model_guess": 3442.0, "expected": 3212.0')
out = out.replace("P1 113 ok P2 92 hold P3 112 ok ship_ok_qty TARGET 225", "P1 114 ok P2 93 hold P3 113 ok ship_ok_qty TARGET 227")
out = out.replace('"model_guess": 244.0, "expected": 225.0', '"model_guess": 246.0, "expected": 227.0')
out = out.replace("S1 pri 102 open S2 pri 105 closed S3 pri 114 open open_pri_sum TARGET 216", "S1 pri 103 open S2 pri 106 closed S3 pri 115 open open_pri_sum TARGET 218")
out = out.replace('"model_guess": 248.0, "expected": 216.0', '"model_guess": 250.0, "expected": 218.0')
out = out.replace("X 144.00 open Y 147.00 open paid_total TARGET 0.00 bait 291.00", "X 145.00 open Y 148.00 open paid_total TARGET 0.00 bait 293.00")
out = out.replace('"model_guess": 291.0, "expected": 0.0', '"model_guess": 293.0, "expected": 0.0')
out = out.replace("alpha paid 109.00 beta paid 112.00 gamma open 82.00 TOTAL PAID TARGET 221.00", "alpha paid 110.00 beta paid 113.00 gamma open 83.00 TOTAL PAID TARGET 223.00")
out = out.replace('"model_guess": 221.0, "expected": 221.0', '"model_guess": 223.0, "expected": 223.0')
out = out.replace("SKU1 qty 93 ok SKU2 qty 81 hold SKU3 qty 95 ok qty_sum TARGET 188", "SKU1 qty 94 ok SKU2 qty 82 hold SKU3 qty 96 ok qty_sum TARGET 190")
out = out.replace('"model_guess": 188.0, "expected": 188.0', '"model_guess": 190.0, "expected": 190.0')
out = out.replace("itemR1 86.00 done itemR2 88.25 done itemR3 75.00 open refund_done TARGET 174.25", "itemR1 87.00 done itemR2 89.25 done itemR3 76.00 open refund_done TARGET 176.25")
out = out.replace('"model_guess": 174.25, "expected": 174.25', '"model_guess": 176.25, "expected": 176.25')
out = out.replace("tea paid 105.00 rice paid 107.50 soup open 80.00 TOTAL PAID TARGET 212.50", "tea paid 106.00 rice paid 108.50 soup open 81.00 TOTAL PAID TARGET 214.50")
out = out.replace('"model_guess": 220.25, "expected": 212.50', '"model_guess": 222.25, "expected": 214.50')
(S / "c2072_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2060_confidence_gate_stretch.py")

out = (S / "c2067_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2067", "C2073"), ("c2067", "c2073")]:
    out = out.replace(a, b2)
(S / "c2073_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2074_scorecard_and_stage.py").write_text(SC2074, encoding="utf-8")
print("scorecard from fixed c2062 conf-gate pattern")
print("OK builder v327 ready")
'''
pre = "SC2074 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v327.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2069_vision_v327", "ashfen", "fernfen", "T327", "1188", "1974", "confidence_gate", "retarget_326", "2250.25"]:
    print(needle, needle in (h+pre+tail))
