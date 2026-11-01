from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
t = (ROOT / "tools/_patch_v341_builder.py").read_text(encoding="utf-8")
# V339: from v338 product-U2C *fen -> v339 conf-gate *brook
# V341: from v340 product-U2C *dale -> v341 conf-gate *ford
reps = [
    ("tools/_build_v338.py", "tools/_build_v340.py"),
    ("# V338 knife = product-U2C", "# V340 knife = product-U2C"),
    ("SC2140 = ", "SC2152 = "),
]
themes = [
    ("netherfen", "netherdale"), ("NETHERFEN", "NETHERDALE"),
    ("cedarfen", "cedardale"), ("CEDARFEN", "CEDARDALE"),
    ("dawnfen", "dawndale"), ("DAWNFEN", "DAWNDALE"),
    ("fernfen", "ferndale"), ("FERNFEN", "FERNDALE"),
    ("glenfen", "glendale"), ("GLENFEN", "GLENDALE"),
    ("hazefen", "hazedale"), ("HAZEFEN", "HAZEDALE"),
    ("jadefen", "jadedale"), ("JADEFEN", "JADEDALE"),
    ("knotfen", "knotdale"), ("KNOTFEN", "KNOTDALE"),
    ("lakefen", "lakedale"), ("LAKEFEN", "LAKEDALE"),
    ("mossfen", "mossdale"), ("MOSSFEN", "MOSSDALE"),
    ("pinefen", "pinedale"), ("PINEFEN", "PINEDALE"),
    ("quillfen", "quilldale"), ("QUILLFEN", "QUILLDALE"),
    ("reedfen", "reeddale"), ("REEDFEN", "REEDDALE"),
    ("stonefen", "stonedale"), ("STONEFEN", "STONEDALE"),
    ("ashfen", "ashdale"), ("ASHFEN", "ASHDALE"),
    ("elmfen", "elmdale"), ("ELMFEN", "ELMDALE"),
    ("inkfen", "inkdale"), ("INKFEN", "INKDALE"),
    ("oakfen", "oakdale"), ("OAKFEN", "OAKDALE"),
    ("netherbrook", "netherford"), ("NETHERBROOK", "NETHERFORD"),
    ("cedarbrook", "cedarford"), ("CEDARBROOK", "CEDARFORD"),
    ("dawnbrook", "dawnford"), ("DAWNBROOK", "DAWNFORD"),
    ("fernbrook", "fernford"), ("FERNBROOK", "FERNFORD"),
    ("glenbrook", "glenford"), ("GLENBROOK", "GLENFORD"),
    ("hazebrook", "hazeford"), ("HAZEBROOK", "HAZEFORD"),
    ("jadebrook", "jadeford"), ("JADEBROOK", "JADEFORD"),
    ("knotbrook", "knotford"), ("KNOTBROOK", "KNOTFORD"),
    ("lakebrook", "lakeford"), ("LAKEBROOK", "LAKEFORD"),
    ("mossbrook", "mossford"), ("MOSSBROOK", "MOSSFORD"),
    ("pinebrook", "pineford"), ("PINEBROOK", "PINEFORD"),
    ("quillbrook", "quillford"), ("QUILLBROOK", "QUILLFORD"),
    ("reedbrook", "reedford"), ("REEDBROOK", "REEDFORD"),
    ("stonebrook", "stoneford"), ("STONEBROOK", "STONEFORD"),
    ("ashbrook", "ashford"), ("ASHBROOK", "ASHFORD"),
    ("elmbrook", "elmford"), ("ELMBROOK", "ELMFORD"),
    ("inkbrook", "inkford"), ("INKBROOK", "INKFORD"),
    ("oakbrook", "oakford"), ("OAKBROOK", "OAKFORD"),
]
ver = [
    ("*fen ; stack mid-band", "*dale ; stack mid-band"),
    ("*brook ; stack mid-band", "*ford ; stack mid-band"),
    ("T338", "T340"), ("TR338", "TR340"), ("HO338", "HO340"), ("NEW338", "NEW340"),
    ("T339", "T341"), ("TR339", "TR341"), ("HO339", "HO341"), ("NEW339", "NEW341"),
    ("V338", "V340"), ("v338", "v340"), ("V339", "V341"), ("v339", "v341"),
    ("_v338_themes.json", "_v340_themes.json"),
    ("_v339_themes.json", "_v341_themes.json"),
    ("_v337_themes.json", "_v339_themes.json"),
    ("OLD337", "OLD339"), ("OLD338", "OLD340"),
    ("vision_images_v338", "vision_images_v340"),
    ("vision_images_v339", "vision_images_v341"),
    ("VL_GATE_V338", "VL_GATE_V340"), ("vl_gate_v338", "vl_gate_v340"),
    ("VL_GATE_V339", "VL_GATE_V341"), ("vl_gate_v339", "vl_gate_v341"),
    ("C2135", "C2147"), ("c2135", "c2147"),
    ("C2136", "C2148"), ("c2136", "c2148"),
    ("C2137", "C2149"), ("c2137", "c2149"),
    ("C2141", "C2153"), ("c2141", "c2153"),
    ("C2142", "C2154"), ("c2142", "c2154"),
    ("C2143", "C2155"), ("c2143", "c2155"),
    ("_v338c2135", "_v340c2147"),
    ("_v339c2141", "_v341c2153"),
    ("Harder than V336", "Harder than V338"),
    ("harder than V336", "harder than V338"),
    ("Harder than V337", "Harder than V339"),
    ("harder than V337", "harder than V339"),
    ("NEW themes vs V336:", "NEW themes vs V338:"),
    ("NEW themes vs V337:", "NEW themes vs V339:"),
    ("kept on V338", "kept on V340"),
    ("kept on V339", "kept on V341"),
    ("V338 keeps floor", "V340 keeps floor"),
    ("V339 keeps floor", "V341 keeps floor"),
    ("C2141 design+fixtures; no VL claim", "C2153 design+fixtures; no VL claim"),
    ("retarget_337", "retarget_339"),
    ("retarget_338", "retarget_340"),
    ("*fen", "*dale"),
    ("*brook", "*ford"),
]
baits = [
    ("ASHFEN bait 251.61", "ASHDALE bait 253.63"),
    ("ASHBROOK bait 252.62", "ASHFORD bait 254.64"),
    ("CEDARF bait 253.63", "CEDARD bait 255.65"),
    ("CEDARB bait 254.64", "CEDARF bait 256.66"),
    ("DAWNF ghost 176.86", "DAWND ghost 178.88"),
    ("DAWNB ghost 177.87", "DAWNF ghost 179.89"),
    ("GLENF bait 246.56", "GLEND bait 248.58"),
    ("GLENB bait 247.57", "GLENF bait 249.59"),
    ("JADEF bait 237.47", "JADED bait 239.49"),
    ("JADEB bait 238.48", "JADEF bait 240.50"),
    ("NETHERF bait 254.64", "NETHERD bait 256.66"),
    ("NETHERB bait 255.65", "NETHERF bait 257.67"),
]
for a,b in reps + themes + ver + baits:
    t = t.replace(a,b)
sc = [
    ('"C2098", "C2146"', '"C2098", "C2158"'),
    ('"c2098", "c2146"', '"c2098", "c2158"'),
    ('"C2096", "C2144"', '"C2096", "C2156"'),
    ('"c2096", "c2144"', '"c2096", "c2156"'),
    ('"C2097", "C2145"', '"C2097", "C2157"'),
    ('"c2097", "c2145"', '"c2097", "c2157"'),
    ('"C2094", "C2142"', '"C2094", "C2154"'),
    ('"c2094", "c2142"', '"c2094", "c2154"'),
    ('"C2095", "C2143"', '"C2095", "C2155"'),
    ('"c2095", "c2143"', '"c2095", "c2155"'),
    ('"C2093", "C2141"', '"C2093", "C2153"'),
    ('"c2093", "c2141"', '"c2093", "c2153"'),
    ('"C2090", "C2138"', '"C2090", "C2150"'),
    ('"c2090", "c2138"', '"c2090", "c2150"'),
    ("STAGE_ANT_C2146", "STAGE_ANT_C2158"),
    ("SC2146", "SC2158"),
    ("c2146_scorecard_and_stage.py", "c2158_scorecard_and_stage.py"),
    ("c2132_confidence_gate_stretch.py", "c2144_confidence_gate_stretch.py"),
    ('"C2132", "C2144"', '"C2144", "C2156"'),
    ('"c2132", "c2144"', '"c2144", "c2156"'),
    ("cg152_", "cg153_"),
    ("conf_gate_stretch_c2144", "conf_gate_stretch_c2156"),
    ("confidence_gate_stretch_v215", "confidence_gate_stretch_v216"),
    ("Stretch vs C2132", "Stretch vs C2144"),
    ('c2144_confidence_gate_stretch.py").write_text', 'c2156_confidence_gate_stretch.py").write_text'),
    ("c2139_capture_office_regression.py", "c2151_capture_office_regression.py"),
    ('"C2139", "C2145"', '"C2151", "C2157"'),
    ('"c2139", "c2145"', '"c2151", "c2157"'),
    ("c2145_capture_office_regression.py", "c2157_capture_office_regression.py"),
]
for a,b in sc:
    t = t.replace(a,b)
bumps = [
    ("a paid 131.00 b paid 135.75 c open 91.00 TOTAL PAID TARGET 266.75", "a paid 132.00 b paid 136.75 c open 92.00 TOTAL PAID TARGET 268.75"),
    ('"model_guess": 999.0, "expected": 266.75', '"model_guess": 999.0, "expected": 268.75'),
    ("SKU1 qty 126 ok SKU2 qty 100 hold SKU3 qty 130 ok qty_sum TARGET 256", "SKU1 qty 127 ok SKU2 qty 101 hold SKU3 qty 131 ok qty_sum TARGET 258"),
    ('"model_guess": 268.0, "expected": 256.0', '"model_guess": 270.0, "expected": 258.0'),
    ("itemR1 107.00 done itemR2 110.75 done itemR3 88.00 open refund_done TARGET 217.75", "itemR1 108.00 done itemR2 111.75 done itemR3 89.00 open refund_done TARGET 219.75"),
    ('"model_guess": 226.5, "expected": 217.75', '"model_guess": 228.5, "expected": 219.75'),
    ("T1 175.00 paid T2 115.00 open T3 156.00 paid tax_base_paid TARGET 331.00", "T1 176.00 paid T2 116.00 open T3 157.00 paid tax_base_paid TARGET 333.00"),
    ('"model_guess": 367.0, "expected": 331.0', '"model_guess": 369.0, "expected": 333.0'),
    ("A 1670 active B 379 leave C 1554 active payroll_active TARGET 3224", "A 1671 active B 380 leave C 1555 active payroll_active TARGET 3226"),
    ('"model_guess": 3454.0, "expected": 3224.0', '"model_guess": 3456.0, "expected": 3226.0'),
    ("P1 120 ok P2 99 hold P3 119 ok ship_ok_qty TARGET 239", "P1 121 ok P2 100 hold P3 120 ok ship_ok_qty TARGET 241"),
    ('"model_guess": 258.0, "expected": 239.0', '"model_guess": 260.0, "expected": 241.0'),
    ("S1 pri 109 open S2 pri 112 closed S3 pri 121 open open_pri_sum TARGET 230", "S1 pri 110 open S2 pri 113 closed S3 pri 122 open open_pri_sum TARGET 232"),
    ('"model_guess": 262.0, "expected": 230.0', '"model_guess": 264.0, "expected": 232.0'),
    ("X 151.00 open Y 154.00 open paid_total TARGET 0.00 bait 305.00", "X 152.00 open Y 155.00 open paid_total TARGET 0.00 bait 307.00"),
    ('"model_guess": 305.0, "expected": 0.0', '"model_guess": 307.0, "expected": 0.0'),
    ("alpha paid 116.00 beta paid 119.00 gamma open 89.00 TOTAL PAID TARGET 235.00", "alpha paid 117.00 beta paid 120.00 gamma open 90.00 TOTAL PAID TARGET 237.00"),
    ('"model_guess": 235.0, "expected": 235.0', '"model_guess": 237.0, "expected": 237.0'),
    ("SKU1 qty 100 ok SKU2 qty 88 hold SKU3 qty 102 ok qty_sum TARGET 202", "SKU1 qty 101 ok SKU2 qty 89 hold SKU3 qty 103 ok qty_sum TARGET 204"),
    ('"model_guess": 202.0, "expected": 202.0', '"model_guess": 204.0, "expected": 204.0'),
    ("itemR1 93.00 done itemR2 95.25 done itemR3 82.00 open refund_done TARGET 188.25", "itemR1 94.00 done itemR2 96.25 done itemR3 83.00 open refund_done TARGET 190.25"),
    ('"model_guess": 188.25, "expected": 188.25', '"model_guess": 190.25, "expected": 190.25'),
    ("tea paid 112.00 rice paid 114.50 soup open 87.00 TOTAL PAID TARGET 226.50", "tea paid 113.00 rice paid 115.50 soup open 88.00 TOTAL PAID TARGET 228.50"),
    ('"model_guess": 234.25, "expected": 226.50', '"model_guess": 236.25, "expected": 228.50'),
]
for a,b in bumps:
    t = t.replace(a,b)
TR = "TR341 = [\n    [2346.0, 2363.5, 2086.0],[840, 760, 820],[2254.0, 2255.25, 2054.0],[2402.0, 2419.0, 2154.0],\n    [2464.0, 2488.0, 2124.0],[2182, 2198, 2082],[490.0, 530.0, 760.0],[2312.0, 2343.75, 2088.0],\n    [840.0, 760.0, 820.0],[2379.0, 2367.0, 2085.0],[1,1,0],[0,0,0],\n    [2445.0, 2466.5, 2110.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],\n]"
HO = "HO341 = [\n    [2144.0, 2156.75, 2005.0],[640, 660, 820],[2087.0, 2101.5, 1980.0],[2217.0, 2233.0, 2036.0],\n    [2237.0, 2248.0, 2029.0],[2040, 2052, 2002],[420.0, 460.0, 740.0],[2128.0, 2149.75, 2005.0],\n    [740.0, 780.0, 820.0],[2175.0, 2161.0, 2002.0],[1,1,0],[0,0,0],\n    [2210.0, 2225.5, 2015.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],\n]"
t = re.sub(r"TR341\s*=\s*\[[\s\S]*?\n\]", TR, t, count=1)
t = re.sub(r"HO341\s*=\s*\[[\s\S]*?\n\]", HO, t, count=1)
t = t.replace("2258.25", "2255.25")
t = t.replace("1998", "2002")
t = t.replace("c2141_vision_v339", "c2153_vision_v341")
t = t.replace("ashbrook", "ashford")
t = t.replace("fernbrook", "fernford")
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        if int(float(n)) in BAN:
            raise SystemExit(f"banned {n} in {label}")
(ROOT / "tools/_patch_v341_builder.py").write_text(t, encoding="utf-8")
print("v341 patch", len(t))
for n in ["c2153_vision_v341", "ashford", "C2158", "C2156", "C2150", "c2156_confidence", "2255.25", "netherford", "*ford"]:
    print(n, n in t)
