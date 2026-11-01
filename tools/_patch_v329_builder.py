from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v328.py").read_text(encoding="utf-8")
idx0 = b0.find('# V328 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2080 = " in head0:
    head0 = head0[:head0.find("SC2080 = ")]

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
    ("T328", "T329"), ("TR328", "TR329"), ("HO328", "HO329"),
    ("NEW328", "NEW329"),
    ("V328", "V329"), ("v328", "v329"),
    ("_v328_themes.json", "_v329_themes.json"),
    ("_v327_themes.json", "_v328_themes.json"),
    ("OLD327", "OLD328"),
    ("vision_images_v328", "vision_images_v329"),
    ("VL_GATE_V328", "VL_GATE_V329"), ("vl_gate_v328", "vl_gate_v329"),
    ("C2075", "C2081"), ("c2075", "c2081"),
    ("C2076", "C2082"), ("c2076", "c2082"),
    ("C2077", "C2083"), ("c2077", "c2083"),
    ("_v328c2075", "_v329c2081"),
    ("Harder than V326", "Harder than V327"),
    ("harder than V326", "harder than V327"),
    ("NEW themes vs V326:", "NEW themes vs V327:"),
    ("kept on V328", "kept on V329"),
    ("V328 keeps floor", "V329 keeps floor"),
    ("C2075 design+fixtures; no VL claim", "C2081 design+fixtures; no VL claim"),
    ("retarget_327", "retarget_328"),
    ("*brook", "*dale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHBROOK bait 241.51", "ASHDALE bait 242.52")
h = h.replace("CEDARB bait 243.53", "CEDARD bait 244.54")
h = h.replace("DAWNB ghost 166.76", "DAWND ghost 167.77")
h = h.replace("GLENB bait 236.46", "GLEND bait 237.47")
h = h.replace("JADEB bait 227.37", "JADED bait 228.38")
h = h.replace("NETHERB bait 244.54", "NETHERD bait 245.55")

TR = '''TR329 = [
    [2322.0, 2339.5, 2062.0],[840, 760, 820],[2245.0, 2254.25, 2040.0],[2378.0, 2395.0, 2130.0],
    [2440.0, 2464.0, 2100.0],[2158, 2174, 2058],[490.0, 530.0, 760.0],[2288.0, 2319.75, 2064.0],
    [840.0, 760.0, 820.0],[2355.0, 2343.0, 2061.0],[1,1,0],[0,0,0],
    [2421.0, 2442.5, 2086.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO329 = [
    [2120.0, 2132.75, 1981.0],[640, 660, 820],[2063.0, 2077.5, 1956.0],[2193.0, 2209.0, 2012.0],
    [2234.0, 2250.0, 2005.0],[2016, 2028, 1978],[420.0, 460.0, 740.0],[2104.0, 2125.75, 1981.0],
    [740.0, 780.0, 820.0],[2151.0, 2137.0, 1978.0],[1,1,0],[0,0,0],
    [2186.0, 2201.5, 1991.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR329\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO329\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2074_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2074", "C2086"), ("c2074", "c2086"),
    ("C2072", "C2084"), ("c2072", "c2084"),
    ("C2073", "C2085"), ("c2073", "c2085"),
    ("C2070", "C2082"), ("c2070", "c2082"),
    ("C2071", "C2083"), ("c2071", "c2083"),
    ("C2069", "C2081"), ("c2069", "c2081"),
    ("C2066", "C2078"), ("c2066", "c2078"),
    ("V327", "V329"), ("v327", "v329"),
    ("STAGE_ANT_C2074", "STAGE_ANT_C2086"),
    ("*fen", "*dale"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V329 knife = confidence-gate (alternating; V328 was product-U2C)
out = (S / "c2072_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2072", "C2084"), ("c2072", "c2084"),
    ("C2060", "C2084"), ("c2060", "c2084"),
    ("cg146_", "cg147_"),
    ("conf_gate_stretch_c2072", "conf_gate_stretch_c2084"),
    ("confidence_gate_stretch_v209", "confidence_gate_stretch_v210"),
    ("Stretch vs C2060", "Stretch vs C2072"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 125.00 b paid 129.75 c open 85.00 TOTAL PAID TARGET 254.75", "a paid 126.00 b paid 130.75 c open 86.00 TOTAL PAID TARGET 256.75")
out = out.replace('"model_guess": 999.0, "expected": 254.75', '"model_guess": 999.0, "expected": 256.75')
out = out.replace("SKU1 qty 120 ok SKU2 qty 94 hold SKU3 qty 124 ok qty_sum TARGET 244", "SKU1 qty 121 ok SKU2 qty 95 hold SKU3 qty 125 ok qty_sum TARGET 246")
out = out.replace('"model_guess": 256.0, "expected": 244.0', '"model_guess": 258.0, "expected": 246.0')
out = out.replace("itemR1 101.00 done itemR2 104.75 done itemR3 82.00 open refund_done TARGET 205.75", "itemR1 102.00 done itemR2 105.75 done itemR3 83.00 open refund_done TARGET 207.75")
out = out.replace('"model_guess": 214.5, "expected": 205.75', '"model_guess": 216.5, "expected": 207.75')
out = out.replace("T1 169.00 paid T2 109.00 open T3 150.00 paid tax_base_paid TARGET 319.00", "T1 170.00 paid T2 110.00 open T3 151.00 paid tax_base_paid TARGET 321.00")
out = out.replace('"model_guess": 355.0, "expected": 319.0', '"model_guess": 357.0, "expected": 321.0')
out = out.replace("A 1664 active B 373 leave C 1548 active payroll_active TARGET 3212", "A 1665 active B 374 leave C 1549 active payroll_active TARGET 3214")
out = out.replace('"model_guess": 3442.0, "expected": 3212.0', '"model_guess": 3444.0, "expected": 3214.0')
out = out.replace("P1 114 ok P2 93 hold P3 113 ok ship_ok_qty TARGET 227", "P1 115 ok P2 94 hold P3 114 ok ship_ok_qty TARGET 229")
out = out.replace('"model_guess": 246.0, "expected": 227.0', '"model_guess": 248.0, "expected": 229.0')
out = out.replace("S1 pri 103 open S2 pri 106 closed S3 pri 115 open open_pri_sum TARGET 218", "S1 pri 104 open S2 pri 107 closed S3 pri 116 open open_pri_sum TARGET 220")
out = out.replace('"model_guess": 250.0, "expected": 218.0', '"model_guess": 252.0, "expected": 220.0')
out = out.replace("X 145.00 open Y 148.00 open paid_total TARGET 0.00 bait 293.00", "X 146.00 open Y 149.00 open paid_total TARGET 0.00 bait 295.00")
out = out.replace('"model_guess": 293.0, "expected": 0.0', '"model_guess": 295.0, "expected": 0.0')
out = out.replace("alpha paid 110.00 beta paid 113.00 gamma open 83.00 TOTAL PAID TARGET 223.00", "alpha paid 111.00 beta paid 114.00 gamma open 84.00 TOTAL PAID TARGET 225.00")
out = out.replace('"model_guess": 223.0, "expected": 223.0', '"model_guess": 225.0, "expected": 225.0')
out = out.replace("SKU1 qty 94 ok SKU2 qty 82 hold SKU3 qty 96 ok qty_sum TARGET 190", "SKU1 qty 95 ok SKU2 qty 83 hold SKU3 qty 97 ok qty_sum TARGET 192")
out = out.replace('"model_guess": 190.0, "expected": 190.0', '"model_guess": 192.0, "expected": 192.0')
out = out.replace("itemR1 87.00 done itemR2 89.25 done itemR3 76.00 open refund_done TARGET 176.25", "itemR1 88.00 done itemR2 90.25 done itemR3 77.00 open refund_done TARGET 178.25")
out = out.replace('"model_guess": 176.25, "expected": 176.25', '"model_guess": 178.25, "expected": 178.25')
out = out.replace("tea paid 106.00 rice paid 108.50 soup open 81.00 TOTAL PAID TARGET 214.50", "tea paid 107.00 rice paid 109.50 soup open 82.00 TOTAL PAID TARGET 216.50")
out = out.replace('"model_guess": 222.25, "expected": 214.50', '"model_guess": 224.25, "expected": 216.50')
(S / "c2084_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2072_confidence_gate_stretch.py")

out = (S / "c2079_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2079", "C2085"), ("c2079", "c2085")]:
    out = out.replace(a, b2)
(S / "c2085_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2086_scorecard_and_stage.py").write_text(SC2086, encoding="utf-8")
print("scorecard from fixed c2074 conf-gate pattern")
print("OK builder v329 ready")
'''
pre = "SC2086 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v329.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2081_vision_v329", "ashdale", "ferndale", "T329", "1188", "1978", "confidence_gate", "retarget_328", "2254.25"]:
    print(needle, needle in (h+pre+tail))
