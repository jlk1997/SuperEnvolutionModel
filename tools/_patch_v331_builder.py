from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v330.py").read_text(encoding="utf-8")
idx0 = b0.find('# V330 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2092 = " in head0:
    head0 = head0[:head0.find("SC2092 = ")]

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
    ("T330", "T331"), ("TR330", "TR331"), ("HO330", "HO331"),
    ("NEW330", "NEW331"),
    ("V330", "V331"), ("v330", "v331"),
    ("_v330_themes.json", "_v331_themes.json"),
    ("_v329_themes.json", "_v330_themes.json"),
    ("OLD329", "OLD330"),
    ("vision_images_v330", "vision_images_v331"),
    ("VL_GATE_V330", "VL_GATE_V331"), ("vl_gate_v330", "vl_gate_v331"),
    ("C2087", "C2093"), ("c2087", "c2093"),
    ("C2088", "C2094"), ("c2088", "c2094"),
    ("C2089", "C2095"), ("c2089", "c2095"),
    ("_v330c2087", "_v331c2093"),
    ("Harder than V328", "Harder than V329"),
    ("harder than V328", "harder than V329"),
    ("NEW themes vs V328:", "NEW themes vs V329:"),
    ("kept on V330", "kept on V331"),
    ("V330 keeps floor", "V331 keeps floor"),
    ("C2087 design+fixtures; no VL claim", "C2093 design+fixtures; no VL claim"),
    ("retarget_329", "retarget_330"),
    ("*ford", "*hurst"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFORD bait 243.53", "ASHHURST bait 244.54")
h = h.replace("CEDARF bait 245.55", "CEDARH bait 246.56")
h = h.replace("DAWNF ghost 168.78", "DAWNH ghost 169.79")
h = h.replace("GLENF bait 238.48", "GLENH bait 239.49")
h = h.replace("JADEF bait 229.39", "JADEH bait 230.40")
h = h.replace("NETHERF bait 246.56", "NETHERH bait 247.57")

TR = '''TR331 = [
    [2326.0, 2343.5, 2066.0],[840, 760, 820],[2249.0, 2258.25, 2044.0],[2382.0, 2399.0, 2134.0],
    [2444.0, 2468.0, 2104.0],[2162, 2178, 2062],[490.0, 530.0, 760.0],[2292.0, 2323.75, 2068.0],
    [840.0, 760.0, 820.0],[2359.0, 2347.0, 2065.0],[1,1,0],[0,0,0],
    [2425.0, 2446.5, 2090.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO331 = [
    [2124.0, 2136.75, 1985.0],[640, 660, 820],[2067.0, 2081.5, 1960.0],[2197.0, 2213.0, 2016.0],
    [2238.0, 2254.0, 2009.0],[2020, 2032, 1982],[420.0, 460.0, 740.0],[2108.0, 2129.75, 1985.0],
    [740.0, 780.0, 820.0],[2155.0, 2141.0, 1982.0],[1,1,0],[0,0,0],
    [2190.0, 2205.5, 1995.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR331\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO331\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2086_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2086", "C2098"), ("c2086", "c2098"),
    ("C2084", "C2096"), ("c2084", "c2096"),
    ("C2085", "C2097"), ("c2085", "c2097"),
    ("C2082", "C2094"), ("c2082", "c2094"),
    ("C2083", "C2095"), ("c2083", "c2095"),
    ("C2081", "C2093"), ("c2081", "c2093"),
    ("C2078", "C2090"), ("c2078", "c2090"),
    ("V329", "V331"), ("v329", "v331"),
    ("STAGE_ANT_C2086", "STAGE_ANT_C2098"),
    ("*dale", "*hurst"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V331 knife = confidence-gate (alternating; V330 was product-U2C)
out = (S / "c2084_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2084", "C2096"), ("c2084", "c2096"),
    ("C2072", "C2096"), ("c2072", "c2096"),
    ("cg147_", "cg148_"),
    ("conf_gate_stretch_c2084", "conf_gate_stretch_c2096"),
    ("confidence_gate_stretch_v210", "confidence_gate_stretch_v211"),
    ("Stretch vs C2072", "Stretch vs C2084"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 126.00 b paid 130.75 c open 86.00 TOTAL PAID TARGET 256.75", "a paid 127.00 b paid 131.75 c open 87.00 TOTAL PAID TARGET 258.75")
out = out.replace('"model_guess": 999.0, "expected": 256.75', '"model_guess": 999.0, "expected": 258.75')
out = out.replace("SKU1 qty 121 ok SKU2 qty 95 hold SKU3 qty 125 ok qty_sum TARGET 246", "SKU1 qty 122 ok SKU2 qty 96 hold SKU3 qty 126 ok qty_sum TARGET 248")
out = out.replace('"model_guess": 258.0, "expected": 246.0', '"model_guess": 260.0, "expected": 248.0')
out = out.replace("itemR1 102.00 done itemR2 105.75 done itemR3 83.00 open refund_done TARGET 207.75", "itemR1 103.00 done itemR2 106.75 done itemR3 84.00 open refund_done TARGET 209.75")
out = out.replace('"model_guess": 216.5, "expected": 207.75', '"model_guess": 218.5, "expected": 209.75')
out = out.replace("T1 170.00 paid T2 110.00 open T3 151.00 paid tax_base_paid TARGET 321.00", "T1 171.00 paid T2 111.00 open T3 152.00 paid tax_base_paid TARGET 323.00")
out = out.replace('"model_guess": 357.0, "expected": 321.0', '"model_guess": 359.0, "expected": 323.0')
out = out.replace("A 1665 active B 374 leave C 1549 active payroll_active TARGET 3214", "A 1666 active B 375 leave C 1550 active payroll_active TARGET 3216")
out = out.replace('"model_guess": 3444.0, "expected": 3214.0', '"model_guess": 3446.0, "expected": 3216.0')
out = out.replace("P1 115 ok P2 94 hold P3 114 ok ship_ok_qty TARGET 229", "P1 116 ok P2 95 hold P3 115 ok ship_ok_qty TARGET 231")
out = out.replace('"model_guess": 248.0, "expected": 229.0', '"model_guess": 250.0, "expected": 231.0')
out = out.replace("S1 pri 104 open S2 pri 107 closed S3 pri 116 open open_pri_sum TARGET 220", "S1 pri 105 open S2 pri 108 closed S3 pri 117 open open_pri_sum TARGET 222")
out = out.replace('"model_guess": 252.0, "expected": 220.0', '"model_guess": 254.0, "expected": 222.0')
out = out.replace("X 146.00 open Y 149.00 open paid_total TARGET 0.00 bait 295.00", "X 147.00 open Y 150.00 open paid_total TARGET 0.00 bait 297.00")
out = out.replace('"model_guess": 295.0, "expected": 0.0', '"model_guess": 297.0, "expected": 0.0')
out = out.replace("alpha paid 111.00 beta paid 114.00 gamma open 84.00 TOTAL PAID TARGET 225.00", "alpha paid 112.00 beta paid 115.00 gamma open 85.00 TOTAL PAID TARGET 227.00")
out = out.replace('"model_guess": 225.0, "expected": 225.0', '"model_guess": 227.0, "expected": 227.0')
out = out.replace("SKU1 qty 95 ok SKU2 qty 83 hold SKU3 qty 97 ok qty_sum TARGET 192", "SKU1 qty 96 ok SKU2 qty 84 hold SKU3 qty 98 ok qty_sum TARGET 194")
out = out.replace('"model_guess": 192.0, "expected": 192.0', '"model_guess": 194.0, "expected": 194.0')
out = out.replace("itemR1 88.00 done itemR2 90.25 done itemR3 77.00 open refund_done TARGET 178.25", "itemR1 89.00 done itemR2 91.25 done itemR3 78.00 open refund_done TARGET 180.25")
out = out.replace('"model_guess": 178.25, "expected": 178.25', '"model_guess": 180.25, "expected": 180.25')
out = out.replace("tea paid 107.00 rice paid 109.50 soup open 82.00 TOTAL PAID TARGET 216.50", "tea paid 108.00 rice paid 110.50 soup open 83.00 TOTAL PAID TARGET 218.50")
out = out.replace('"model_guess": 224.25, "expected": 216.50', '"model_guess": 226.25, "expected": 218.50')
(S / "c2096_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2084_confidence_gate_stretch.py")

out = (S / "c2091_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2091", "C2097"), ("c2091", "c2097")]:
    out = out.replace(a, b2)
(S / "c2097_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2098_scorecard_and_stage.py").write_text(SC2098, encoding="utf-8")
print("scorecard from fixed c2086 conf-gate pattern")
print("OK builder v331 ready")
'''
pre = "SC2098 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v331.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2093_vision_v331", "ashhurst", "fernhurst", "T331", "1188", "1982", "confidence_gate", "retarget_330", "2258.25"]:
    print(needle, needle in (h+pre+tail))
