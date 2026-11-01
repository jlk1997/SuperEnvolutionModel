from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
t = (ROOT / "tools/_patch_v339_builder.py").read_text(encoding="utf-8")
# V337: from v336 product-U2C *wick -> v337 conf-gate *moor
# V339: from v338 product-U2C *fen -> v339 conf-gate *brook
reps = [
    ("tools/_build_v336.py", "tools/_build_v338.py"),
    ("# V336 knife = product-U2C", "# V338 knife = product-U2C"),
    ("SC2128 = ", "SC2140 = "),
]
themes = [
    ("netherwick", "netherfen"), ("NETHERWICK", "NETHERFEN"),
    ("cedarwick", "cedarfen"), ("CEDARWICK", "CEDARFEN"),
    ("dawnwick", "dawnfen"), ("DAWNWICK", "DAWNFEN"),
    ("fernwick", "fernfen"), ("FERNWICK", "FERNFEN"),
    ("glenwick", "glenfen"), ("GLENWICK", "GLENFEN"),
    ("hazewick", "hazefen"), ("HAZEWICK", "HAZEFEN"),
    ("jadewick", "jadefen"), ("JADEWICK", "JADEFEN"),
    ("knotwick", "knotfen"), ("KNOTWICK", "KNOTFEN"),
    ("lakewick", "lakefen"), ("LAKEWICK", "LAKEFEN"),
    ("mosswick", "mossfen"), ("MOSSWICK", "MOSSFEN"),
    ("pinewick", "pinefen"), ("PINEWICK", "PINEFEN"),
    ("quillwick", "quillfen"), ("QUILLWICK", "QUILLFEN"),
    ("reedwick", "reedfen"), ("REEDWICK", "REEDFEN"),
    ("stonewick", "stonefen"), ("STONEWICK", "STONEFEN"),
    ("ashwick", "ashfen"), ("ASHWICK", "ASHFEN"),
    ("elmwick", "elmfen"), ("ELMWICK", "ELMFEN"),
    ("inkwick", "inkfen"), ("INKWICK", "INKFEN"),
    ("oakwick", "oakfen"), ("OAKWICK", "OAKFEN"),
    ("nethermoor", "netherbrook"), ("NETHERMOOR", "NETHERBROOK"),
    ("cedarmoor", "cedarbrook"), ("CEDARMOOR", "CEDARBROOK"),
    ("dawnmoor", "dawnbrook"), ("DAWNMOOR", "DAWNBROOK"),
    ("fernmoor", "fernbrook"), ("FERNMOOR", "FERNBROOK"),
    ("glenmoor", "glenbrook"), ("GLENMOOR", "GLENBROOK"),
    ("hazemoor", "hazebrook"), ("HAZEMOOR", "HAZEBROOK"),
    ("jademoor", "jadebrook"), ("JADEMOOR", "JADEBROOK"),
    ("knotmoor", "knotbrook"), ("KNOTMOOR", "KNOTBROOK"),
    ("lakemoor", "lakebrook"), ("LAKEMOOR", "LAKEBROOK"),
    ("mossmoor", "mossbrook"), ("MOSSMOOR", "MOSSBROOK"),
    ("pinemoor", "pinebrook"), ("PINEMOOR", "PINEBROOK"),
    ("quillmoor", "quillbrook"), ("QUILLMOOR", "QUILLBROOK"),
    ("reedmoor", "reedbrook"), ("REEDMOOR", "REEDBROOK"),
    ("stonemoor", "stonebrook"), ("STONEMOOR", "STONEBROOK"),
    ("ashmoor", "ashbrook"), ("ASHMOOR", "ASHBROOK"),
    ("elmmoor", "elmbrook"), ("ELMMOOR", "ELMBROOK"),
    ("inkmoor", "inkbrook"), ("INKMOOR", "INKBROOK"),
    ("oakmoor", "oakbrook"), ("OAKMOOR", "OAKBROOK"),
]
ver = [
    ("*wick ; stack mid-band", "*fen ; stack mid-band"),
    ("*moor ; stack mid-band", "*brook ; stack mid-band"),
    ("T336", "T338"), ("TR336", "TR338"), ("HO336", "HO338"), ("NEW336", "NEW338"),
    ("T337", "T339"), ("TR337", "TR339"), ("HO337", "HO339"), ("NEW337", "NEW339"),
    ("V336", "V338"), ("v336", "v338"), ("V337", "V339"), ("v337", "v339"),
    ("_v336_themes.json", "_v338_themes.json"),
    ("_v337_themes.json", "_v339_themes.json"),
    ("_v335_themes.json", "_v337_themes.json"),
    ("OLD335", "OLD337"), ("OLD336", "OLD338"),
    ("vision_images_v336", "vision_images_v338"),
    ("vision_images_v337", "vision_images_v339"),
    ("VL_GATE_V336", "VL_GATE_V338"), ("vl_gate_v336", "vl_gate_v338"),
    ("VL_GATE_V337", "VL_GATE_V339"), ("vl_gate_v337", "vl_gate_v339"),
    ("C2123", "C2135"), ("c2123", "c2135"),
    ("C2124", "C2136"), ("c2124", "c2136"),
    ("C2125", "C2137"), ("c2125", "c2137"),
    ("C2129", "C2141"), ("c2129", "c2141"),
    ("C2130", "C2142"), ("c2130", "c2142"),
    ("C2131", "C2143"), ("c2131", "c2143"),
    ("_v336c2123", "_v338c2135"),
    ("_v337c2129", "_v339c2141"),
    ("Harder than V334", "Harder than V336"),
    ("harder than V334", "harder than V336"),
    ("Harder than V335", "Harder than V337"),
    ("harder than V335", "harder than V337"),
    ("NEW themes vs V334:", "NEW themes vs V336:"),
    ("NEW themes vs V335:", "NEW themes vs V337:"),
    ("kept on V336", "kept on V338"),
    ("kept on V337", "kept on V339"),
    ("V336 keeps floor", "V338 keeps floor"),
    ("V337 keeps floor", "V339 keeps floor"),
    ("C2129 design+fixtures; no VL claim", "C2141 design+fixtures; no VL claim"),
    ("retarget_335", "retarget_337"),
    ("retarget_336", "retarget_338"),
    ("*wick", "*fen"),
    ("*moor", "*brook"),
]
baits = [
    ("ASHWICK bait 249.59", "ASHFEN bait 251.61"),
    ("ASHMOOR bait 250.60", "ASHBROOK bait 252.62"),
    ("CEDARW bait 251.61", "CEDARF bait 253.63"),
    ("CEDARM bait 252.62", "CEDARB bait 254.64"),
    ("DAWNW ghost 174.84", "DAWNF ghost 176.86"),
    ("DAWNM ghost 175.85", "DAWNB ghost 177.87"),
    ("GLENW bait 244.54", "GLENF bait 246.56"),
    ("GLENM bait 245.55", "GLENB bait 247.57"),
    ("JADEW bait 235.45", "JADEF bait 237.47"),
    ("JADEM bait 236.46", "JADEB bait 238.48"),
    ("NETHERW bait 252.62", "NETHERF bait 254.64"),
    ("NETHERM bait 253.63", "NETHERB bait 255.65"),
]
for a,b in reps + themes + ver + baits:
    t = t.replace(a,b)
sc = [
    ('"C2098", "C2134"', '"C2098", "C2146"'),
    ('"c2098", "c2134"', '"c2098", "c2146"'),
    ('"C2096", "C2132"', '"C2096", "C2144"'),
    ('"c2096", "c2132"', '"c2096", "c2144"'),
    ('"C2097", "C2133"', '"C2097", "C2145"'),
    ('"c2097", "c2133"', '"c2097", "c2145"'),
    ('"C2094", "C2130"', '"C2094", "C2142"'),
    ('"c2094", "c2130"', '"c2094", "c2142"'),
    ('"C2095", "C2131"', '"C2095", "C2143"'),
    ('"c2095", "c2131"', '"c2095", "c2143"'),
    ('"C2093", "C2129"', '"C2093", "C2141"'),
    ('"c2093", "c2129"', '"c2093", "c2141"'),
    ('"C2090", "C2126"', '"C2090", "C2138"'),
    ('"c2090", "c2126"', '"c2090", "c2138"'),
    ("STAGE_ANT_C2134", "STAGE_ANT_C2146"),
    ("SC2134", "SC2146"),
    ("c2134_scorecard_and_stage.py", "c2146_scorecard_and_stage.py"),
    ("c2120_confidence_gate_stretch.py", "c2132_confidence_gate_stretch.py"),
    ('"C2120", "C2132"', '"C2132", "C2144"'),
    ('"c2120", "c2132"', '"c2132", "c2144"'),
    ("cg151_", "cg152_"),
    ("conf_gate_stretch_c2132", "conf_gate_stretch_c2144"),
    ("confidence_gate_stretch_v214", "confidence_gate_stretch_v215"),
    ("Stretch vs C2120", "Stretch vs C2132"),
    ('c2132_confidence_gate_stretch.py").write_text', 'c2144_confidence_gate_stretch.py").write_text'),
    ("c2127_capture_office_regression.py", "c2139_capture_office_regression.py"),
    ('"C2127", "C2133"', '"C2139", "C2145"'),
    ('"c2127", "c2133"', '"c2139", "c2145"'),
    ("c2133_capture_office_regression.py", "c2145_capture_office_regression.py"),
]
for a,b in sc:
    t = t.replace(a,b)
# bump conf-gate samples from V337 values
bumps = [
    ("a paid 130.00 b paid 134.75 c open 90.00 TOTAL PAID TARGET 264.75", "a paid 131.00 b paid 135.75 c open 91.00 TOTAL PAID TARGET 266.75"),
    ('"model_guess": 999.0, "expected": 264.75', '"model_guess": 999.0, "expected": 266.75'),
    ("SKU1 qty 125 ok SKU2 qty 99 hold SKU3 qty 129 ok qty_sum TARGET 254", "SKU1 qty 126 ok SKU2 qty 100 hold SKU3 qty 130 ok qty_sum TARGET 256"),
    ('"model_guess": 266.0, "expected": 254.0', '"model_guess": 268.0, "expected": 256.0'),
    ("itemR1 106.00 done itemR2 109.75 done itemR3 87.00 open refund_done TARGET 215.75", "itemR1 107.00 done itemR2 110.75 done itemR3 88.00 open refund_done TARGET 217.75"),
    ('"model_guess": 224.5, "expected": 215.75', '"model_guess": 226.5, "expected": 217.75'),
    ("T1 174.00 paid T2 114.00 open T3 155.00 paid tax_base_paid TARGET 329.00", "T1 175.00 paid T2 115.00 open T3 156.00 paid tax_base_paid TARGET 331.00"),
    ('"model_guess": 365.0, "expected": 329.0', '"model_guess": 367.0, "expected": 331.0'),
    ("A 1669 active B 378 leave C 1553 active payroll_active TARGET 3222", "A 1670 active B 379 leave C 1554 active payroll_active TARGET 3224"),
    ('"model_guess": 3452.0, "expected": 3222.0', '"model_guess": 3454.0, "expected": 3224.0'),
    ("P1 119 ok P2 98 hold P3 118 ok ship_ok_qty TARGET 237", "P1 120 ok P2 99 hold P3 119 ok ship_ok_qty TARGET 239"),
    ('"model_guess": 256.0, "expected": 237.0', '"model_guess": 258.0, "expected": 239.0'),
    ("S1 pri 108 open S2 pri 111 closed S3 pri 120 open open_pri_sum TARGET 228", "S1 pri 109 open S2 pri 112 closed S3 pri 121 open open_pri_sum TARGET 230"),
    ('"model_guess": 260.0, "expected": 228.0', '"model_guess": 262.0, "expected": 230.0'),
    ("X 150.00 open Y 153.00 open paid_total TARGET 0.00 bait 303.00", "X 151.00 open Y 154.00 open paid_total TARGET 0.00 bait 305.00"),
    ('"model_guess": 303.0, "expected": 0.0', '"model_guess": 305.0, "expected": 0.0'),
    ("alpha paid 115.00 beta paid 118.00 gamma open 88.00 TOTAL PAID TARGET 233.00", "alpha paid 116.00 beta paid 119.00 gamma open 89.00 TOTAL PAID TARGET 235.00"),
    ('"model_guess": 233.0, "expected": 233.0', '"model_guess": 235.0, "expected": 235.0'),
    ("SKU1 qty 99 ok SKU2 qty 87 hold SKU3 qty 101 ok qty_sum TARGET 200", "SKU1 qty 100 ok SKU2 qty 88 hold SKU3 qty 102 ok qty_sum TARGET 202"),
    ('"model_guess": 200.0, "expected": 200.0', '"model_guess": 202.0, "expected": 202.0'),
    ("itemR1 92.00 done itemR2 94.25 done itemR3 81.00 open refund_done TARGET 186.25", "itemR1 93.00 done itemR2 95.25 done itemR3 82.00 open refund_done TARGET 188.25"),
    ('"model_guess": 186.25, "expected": 186.25', '"model_guess": 188.25, "expected": 188.25'),
    ("tea paid 111.00 rice paid 113.50 soup open 86.00 TOTAL PAID TARGET 224.50", "tea paid 112.00 rice paid 114.50 soup open 87.00 TOTAL PAID TARGET 226.50"),
    ('"model_guess": 232.25, "expected": 224.50', '"model_guess": 234.25, "expected": 226.50'),
]
for a,b in bumps:
    t = t.replace(a,b)
TR = "TR339 = [\n    [2342.0, 2359.5, 2082.0],[840, 760, 820],[2252.0, 2258.25, 2052.0],[2398.0, 2415.0, 2150.0],\n    [2460.0, 2484.0, 2120.0],[2178, 2194, 2078],[490.0, 530.0, 760.0],[2308.0, 2339.75, 2084.0],\n    [840.0, 760.0, 820.0],[2375.0, 2363.0, 2081.0],[1,1,0],[0,0,0],\n    [2441.0, 2462.5, 2106.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],\n]"
HO = "HO339 = [\n    [2140.0, 2152.75, 2001.0],[640, 660, 820],[2083.0, 2097.5, 1976.0],[2213.0, 2229.0, 2032.0],\n    [2239.0, 2250.0, 2025.0],[2036, 2048, 1998],[420.0, 460.0, 740.0],[2124.0, 2145.75, 2001.0],\n    [740.0, 780.0, 820.0],[2171.0, 2157.0, 1998.0],[1,1,0],[0,0,0],\n    [2206.0, 2221.5, 2011.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],\n]"
t = re.sub(r"TR339\s*=\s*\[[\s\S]*?\n\]", TR, t, count=1)
t = re.sub(r"HO339\s*=\s*\[[\s\S]*?\n\]", HO, t, count=1)
t = t.replace("2256.25", "2258.25")
t = t.replace("1994", "1998")
t = t.replace("c2129_vision_v337", "c2141_vision_v339")
t = t.replace("ashmoor", "ashbrook")
t = t.replace("fernmoor", "fernbrook")
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        if int(float(n)) in BAN:
            raise SystemExit(f"banned {n} in {label}")
(ROOT / "tools/_patch_v339_builder.py").write_text(t, encoding="utf-8")
print("v339 patch", len(t))
for n in ["c2141_vision_v339", "ashbrook", "C2146", "C2144", "C2138", "c2144_confidence", "2258.25", "netherbrook", "*brook"]:
    print(n, n in t)
