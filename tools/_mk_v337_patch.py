from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
p = ROOT / "tools/_patch_v337_builder.py"
t = p.read_text(encoding="utf-8")
# V335: from v334 product-U2C *croft -> v335 conf-gate *holm
# V337: from v336 product-U2C *wick -> v337 conf-gate *moor
reps = [
    ("tools/_build_v334.py", "tools/_build_v336.py"),
    ("# V334 knife = product-U2C", "# V336 knife = product-U2C"),
    ("SC2116 = ", "SC2128 = "),
]
# croft (from) -> wick ; holm (to) -> moor
themes = [
    ("nethercroft", "netherwick"), ("NETHERCROFT", "NETHERWICK"),
    ("cedarcroft", "cedarwick"), ("CEDARCROFT", "CEDARWICK"),
    ("dawncroft", "dawnwick"), ("DAWNCROFT", "DAWNWICK"),
    ("ferncroft", "fernwick"), ("FERNCROFT", "FERNWICK"),
    ("glencroft", "glenwick"), ("GLENCROFT", "GLENWICK"),
    ("hazecroft", "hazewick"), ("HAZECROFT", "HAZEWICK"),
    ("jadecroft", "jadewick"), ("JADECROFT", "JADEWICK"),
    ("knotcroft", "knotwick"), ("KNOTCROFT", "KNOTWICK"),
    ("lakecroft", "lakewick"), ("LAKECROFT", "LAKEWICK"),
    ("mosscroft", "mosswick"), ("MOSSCROFT", "MOSSWICK"),
    ("pinecroft", "pinewick"), ("PINECROFT", "PINEWICK"),
    ("quillcroft", "quillwick"), ("QUILLCROFT", "QUILLWICK"),
    ("reedcroft", "reedwick"), ("REEDCROFT", "REEDWICK"),
    ("stonecroft", "stonewick"), ("STONECROFT", "STONEWICK"),
    ("ashcroft", "ashwick"), ("ASHCROFT", "ASHWICK"),
    ("elmcroft", "elmwick"), ("ELMCROFT", "ELMWICK"),
    ("inkcroft", "inkwick"), ("INKCROFT", "INKWICK"),
    ("oakcroft", "oakwick"), ("OAKCROFT", "OAKWICK"),
    ("netherholm", "nethermoor"), ("NETHERHOLM", "NETHERMOOR"),
    ("cedarholm", "cedarmoor"), ("CEDARHOLM", "CEDARMOOR"),
    ("dawnholm", "dawnmoor"), ("DAWNHOLM", "DAWNMOOR"),
    ("fernholm", "fernmoor"), ("FERNHOLM", "FERNMOOR"),
    ("glenholm", "glenmoor"), ("GLENHOLM", "GLENMOOR"),
    ("hazeholm", "hazemoor"), ("HAZEHOLM", "HAZEMOOR"),
    ("jadeholm", "jademoor"), ("JADEHOLM", "JADEMOOR"),
    ("knotholm", "knotmoor"), ("KNOTHOLM", "KNOTMOOR"),
    ("lakeholm", "lakemoor"), ("LAKEHOLM", "LAKEMOOR"),
    ("mossholm", "mossmoor"), ("MOSSHOLM", "MOSSMOOR"),
    ("pineholm", "pinemoor"), ("PINEHOLM", "PINEMOOR"),
    ("quillholm", "quillmoor"), ("QUILLHOLM", "QUILLMOOR"),
    ("reedholm", "reedmoor"), ("REEDHOLM", "REEDMOOR"),
    ("stoneholm", "stonemoor"), ("STONEHOLM", "STONEMOOR"),
    ("ashholm", "ashmoor"), ("ASHHOLM", "ASHMOOR"),
    ("elmholm", "elmmoor"), ("ELMHOLM", "ELMMOOR"),
    ("inkholm", "inkmoor"), ("INKHOLM", "INKMOOR"),
    ("oakholm", "oakmoor"), ("OAKHOLM", "OAKMOOR"),
]
ver = [
    ("*croft ; stack mid-band", "*wick ; stack mid-band"),
    ("*holm ; stack mid-band", "*moor ; stack mid-band"),
    ("T334", "T336"), ("TR334", "TR336"), ("HO334", "HO336"), ("NEW334", "NEW336"),
    ("T335", "T337"), ("TR335", "TR337"), ("HO335", "HO337"), ("NEW335", "NEW337"),
    ("V334", "V336"), ("v334", "v336"), ("V335", "V337"), ("v335", "v337"),
    ("_v334_themes.json", "_v336_themes.json"),
    ("_v335_themes.json", "_v337_themes.json"),
    ("_v333_themes.json", "_v335_themes.json"),
    ("OLD333", "OLD335"), ("OLD334", "OLD336"),
    ("vision_images_v334", "vision_images_v336"),
    ("vision_images_v335", "vision_images_v337"),
    ("VL_GATE_V334", "VL_GATE_V336"), ("vl_gate_v334", "vl_gate_v336"),
    ("VL_GATE_V335", "VL_GATE_V337"), ("vl_gate_v335", "vl_gate_v337"),
    ("C2111", "C2123"), ("c2111", "c2123"),
    ("C2112", "C2124"), ("c2112", "c2124"),
    ("C2113", "C2125"), ("c2113", "c2125"),
    ("C2117", "C2129"), ("c2117", "c2129"),
    ("C2118", "C2130"), ("c2118", "c2130"),
    ("C2119", "C2131"), ("c2119", "c2131"),
    ("_v334c2111", "_v336c2123"),
    ("_v335c2117", "_v337c2129"),
    ("Harder than V332", "Harder than V334"),
    ("harder than V332", "harder than V334"),
    ("Harder than V333", "Harder than V335"),
    ("harder than V333", "harder than V335"),
    ("NEW themes vs V332:", "NEW themes vs V334:"),
    ("NEW themes vs V333:", "NEW themes vs V335:"),
    ("kept on V334", "kept on V336"),
    ("kept on V335", "kept on V337"),
    ("V334 keeps floor", "V336 keeps floor"),
    ("V335 keeps floor", "V337 keeps floor"),
    ("C2117 design+fixtures; no VL claim", "C2129 design+fixtures; no VL claim"),
    ("retarget_333", "retarget_335"),
    ("retarget_334", "retarget_336"),
    ("*croft", "*wick"),
    ("*holm", "*moor"),
]
baits = [
    ("ASHCROFT bait 247.57", "ASHWICK bait 249.59"),
    ("ASHHOLM bait 248.58", "ASHMOOR bait 250.60"),
    ("CEDARC bait 249.59", "CEDARW bait 251.61"),
    ("CEDARH bait 250.60", "CEDARM bait 252.62"),
    ("DAWNC ghost 172.82", "DAWNW ghost 174.84"),
    ("DAWNH ghost 173.83", "DAWNM ghost 175.85"),
    ("GLENC bait 242.52", "GLENW bait 244.54"),
    ("GLENH bait 243.53", "GLENM bait 245.55"),
    ("JADEC bait 233.43", "JADEW bait 235.45"),
    ("JADEH bait 234.44", "JADEM bait 236.46"),
    ("NETHERC bait 250.60", "NETHERW bait 252.62"),
    ("NETHERH bait 251.61", "NETHERM bait 253.63"),
]
for a,b in reps + themes + ver + baits:
    t = t.replace(a,b)
# scorecard / knife: V335 used C2098 conf-gate -> C2122; we need C2134 and prior PRODUCT C2126
sc = [
    ('"C2098", "C2122"', '"C2098", "C2134"'),
    ('"c2098", "c2122"', '"c2098", "c2134"'),
    ('"C2096", "C2120"', '"C2096", "C2132"'),
    ('"c2096", "c2120"', '"c2096", "c2132"'),
    ('"C2097", "C2121"', '"C2097", "C2133"'),
    ('"c2097", "c2121"', '"c2097", "c2133"'),
    ('"C2094", "C2118"', '"C2094", "C2130"'),
    ('"c2094", "c2118"', '"c2094", "c2130"'),
    ('"C2095", "C2119"', '"C2095", "C2131"'),
    ('"c2095", "c2119"', '"c2095", "c2131"'),
    ('"C2093", "C2117"', '"C2093", "C2129"'),
    ('"c2093", "c2117"', '"c2093", "c2129"'),
    ('"C2090", "C2114"', '"C2090", "C2126"'),
    ('"c2090", "c2114"', '"c2090", "c2126"'),
    ("STAGE_ANT_C2122", "STAGE_ANT_C2134"),
    ("SC2122", "SC2134"),
    ("c2122_scorecard_and_stage.py", "c2134_scorecard_and_stage.py"),
    ("c2108_confidence_gate_stretch.py", "c2120_confidence_gate_stretch.py"),
    ('"C2108", "C2120"', '"C2120", "C2132"'),
    ('"c2108", "c2120"', '"c2120", "c2132"'),
    ('"C2096", "C2120"', '"C2108", "C2132"'),
    ('"c2096", "c2120"', '"c2108", "c2132"'),
    ("cg149_", "cg151_"),
    ("conf_gate_stretch_c2108", "conf_gate_stretch_c2120"),
    ("conf_gate_stretch_c2120", "conf_gate_stretch_c2132"),
    ("confidence_gate_stretch_v212", "confidence_gate_stretch_v214"),
    ("Stretch vs C2096", "Stretch vs C2120"),
    ('c2120_confidence_gate_stretch.py").write_text', 'c2132_confidence_gate_stretch.py").write_text'),
    ("c2115_capture_office_regression.py", "c2127_capture_office_regression.py"),
    ('"C2115", "C2121"', '"C2127", "C2133"'),
    ('"c2115", "c2121"', '"c2127", "c2133"'),
    ("c2121_capture_office_regression.py", "c2133_capture_office_regression.py"),
]
for a,b in sc:
    t = t.replace(a,b)

TR = "TR337 = [\n    [2338.0, 2355.5, 2078.0],[840, 760, 820],[2250.0, 2256.25, 2050.0],[2394.0, 2411.0, 2146.0],\n    [2456.0, 2480.0, 2116.0],[2174, 2190, 2074],[490.0, 530.0, 760.0],[2304.0, 2335.75, 2080.0],\n    [840.0, 760.0, 820.0],[2371.0, 2359.0, 2077.0],[1,1,0],[0,0,0],\n    [2437.0, 2458.5, 2102.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],\n]"
HO = "HO337 = [\n    [2136.0, 2148.75, 1997.0],[640, 660, 820],[2079.0, 2093.5, 1972.0],[2209.0, 2225.0, 2028.0],\n    [2241.0, 2252.0, 2021.0],[2032, 2044, 1994],[420.0, 460.0, 740.0],[2120.0, 2141.75, 1997.0],\n    [740.0, 780.0, 820.0],[2167.0, 2153.0, 1994.0],[1,1,0],[0,0,0],\n    [2202.0, 2217.5, 2007.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],\n]"
t = re.sub(r"TR337\s*=\s*\[[\s\S]*?\n\]", TR, t, count=1)
t = re.sub(r"HO337\s*=\s*\[[\s\S]*?\n\]", HO, t, count=1)
t = t.replace("2259.25", "2256.25")
t = t.replace("1990", "1994")
# bump conf-gate sample numbers by +2 from V335 values already in file - leave as-is if replace chains from V335; V335 already bumped from V331. We'll bump key strings from last V335 stretch values.
bumps = [
    ("a paid 129.00 b paid 133.75 c open 89.00 TOTAL PAID TARGET 262.75", "a paid 130.00 b paid 134.75 c open 90.00 TOTAL PAID TARGET 264.75"),
    ('"model_guess": 999.0, "expected": 262.75', '"model_guess": 999.0, "expected": 264.75'),
    ("SKU1 qty 124 ok SKU2 qty 98 hold SKU3 qty 128 ok qty_sum TARGET 252", "SKU1 qty 125 ok SKU2 qty 99 hold SKU3 qty 129 ok qty_sum TARGET 254"),
    ('"model_guess": 264.0, "expected": 252.0', '"model_guess": 266.0, "expected": 254.0'),
    ("itemR1 105.00 done itemR2 108.75 done itemR3 86.00 open refund_done TARGET 213.75", "itemR1 106.00 done itemR2 109.75 done itemR3 87.00 open refund_done TARGET 215.75"),
    ('"model_guess": 222.5, "expected": 213.75', '"model_guess": 224.5, "expected": 215.75'),
    ("T1 173.00 paid T2 113.00 open T3 154.00 paid tax_base_paid TARGET 327.00", "T1 174.00 paid T2 114.00 open T3 155.00 paid tax_base_paid TARGET 329.00"),
    ('"model_guess": 363.0, "expected": 327.0', '"model_guess": 365.0, "expected": 329.0'),
    ("A 1668 active B 377 leave C 1552 active payroll_active TARGET 3220", "A 1669 active B 378 leave C 1553 active payroll_active TARGET 3222"),
    ('"model_guess": 3450.0, "expected": 3220.0', '"model_guess": 3452.0, "expected": 3222.0'),
    ("P1 118 ok P2 97 hold P3 117 ok ship_ok_qty TARGET 235", "P1 119 ok P2 98 hold P3 118 ok ship_ok_qty TARGET 237"),
    ('"model_guess": 254.0, "expected": 235.0', '"model_guess": 256.0, "expected": 237.0'),
    ("S1 pri 107 open S2 pri 110 closed S3 pri 119 open open_pri_sum TARGET 226", "S1 pri 108 open S2 pri 111 closed S3 pri 120 open open_pri_sum TARGET 228"),
    ('"model_guess": 258.0, "expected": 226.0', '"model_guess": 260.0, "expected": 228.0'),
    ("X 149.00 open Y 152.00 open paid_total TARGET 0.00 bait 301.00", "X 150.00 open Y 153.00 open paid_total TARGET 0.00 bait 303.00"),
    ('"model_guess": 301.0, "expected": 0.0', '"model_guess": 303.0, "expected": 0.0'),
    ("alpha paid 114.00 beta paid 117.00 gamma open 87.00 TOTAL PAID TARGET 231.00", "alpha paid 115.00 beta paid 118.00 gamma open 88.00 TOTAL PAID TARGET 233.00"),
    ('"model_guess": 231.0, "expected": 231.0', '"model_guess": 233.0, "expected": 233.0'),
    ("SKU1 qty 98 ok SKU2 qty 86 hold SKU3 qty 100 ok qty_sum TARGET 198", "SKU1 qty 99 ok SKU2 qty 87 hold SKU3 qty 101 ok qty_sum TARGET 200"),
    ('"model_guess": 198.0, "expected": 198.0', '"model_guess": 200.0, "expected": 200.0'),
    ("itemR1 91.00 done itemR2 93.25 done itemR3 80.00 open refund_done TARGET 184.25", "itemR1 92.00 done itemR2 94.25 done itemR3 81.00 open refund_done TARGET 186.25"),
    ('"model_guess": 184.25, "expected": 184.25', '"model_guess": 186.25, "expected": 186.25'),
    ("tea paid 110.00 rice paid 112.50 soup open 85.00 TOTAL PAID TARGET 222.50", "tea paid 111.00 rice paid 113.50 soup open 86.00 TOTAL PAID TARGET 224.50"),
    ('"model_guess": 230.25, "expected": 222.50', '"model_guess": 232.25, "expected": 224.50'),
]
for a,b in bumps:
    t = t.replace(a,b)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        if int(float(n)) in BAN:
            raise SystemExit(f"banned {n} in {label}")
# fix needle list
t = t.replace("c2117_vision_v335", "c2129_vision_v337")
t = t.replace("ashholm", "ashmoor")
t = t.replace("fernholm", "fernmoor")
t = t.replace("T335", "T337")
t = t.replace("confidence_gate", "confidence_gate")
t = t.replace("retarget_334", "retarget_336")
p.write_text(t, encoding="utf-8")
print("v337 patch", len(t))
for n in ["c2129_vision_v337", "ashmoor", "C2134", "C2132", "C2126", "c2120_confidence", "c2132_confidence", "2256.25", "nethermoor", "*moor"]:
    print(n, n in t)
