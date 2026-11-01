from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
t = (ROOT / "tools/_patch_v343_builder.py").read_text(encoding="utf-8")
# V341: from v340 product-U2C *dale -> v341 conf-gate *ford
# V343: from v342 product-U2C *hurst -> v343 conf-gate *mere
reps = [
    ("tools/_build_v340.py", "tools/_build_v342.py"),
    ("# V340 knife = product-U2C", "# V342 knife = product-U2C"),
    ("SC2152 = ", "SC2164 = "),
]
themes = [
    ("netherdale", "netherhurst"), ("NETHERDALE", "NETHERHURST"),
    ("cedardale", "cedarhurst"), ("CEDARDALE", "CEDARHURST"),
    ("dawndale", "dawnhurst"), ("DAWNDALE", "DAWNHURST"),
    ("ferndale", "fernhurst"), ("FERNDALE", "FERNHURST"),
    ("glendale", "glenhurst"), ("GLENDALE", "GLENHURST"),
    ("hazedale", "hazehurst"), ("HAZEDALE", "HAZEHURST"),
    ("jadedale", "jadehurst"), ("JADEDALE", "JADEHURST"),
    ("knotdale", "knothurst"), ("KNOTDALE", "KNOTHURST"),
    ("lakedale", "lakehurst"), ("LAKEDALE", "LAKEHURST"),
    ("mossdale", "mosshurst"), ("MOSSDALE", "MOSSHURST"),
    ("pinedale", "pinehurst"), ("PINEDALE", "PINEHURST"),
    ("quilldale", "quillhurst"), ("QUILLDALE", "QUILLHURST"),
    ("reeddale", "reedhurst"), ("REEDDALE", "REEDHURST"),
    ("stonedale", "stonehurst"), ("STONEDALE", "STONEHURST"),
    ("ashdale", "ashhurst"), ("ASHDALE", "ASHHURST"),
    ("elmdale", "elmhurst"), ("ELMDALE", "ELMHURST"),
    ("inkdale", "inkhurst"), ("INKDALE", "INKHURST"),
    ("oakdale", "oakhurst"), ("OAKDALE", "OAKHURST"),
    ("netherford", "nethermere"), ("NETHERFORD", "NETHERMERE"),
    ("cedarford", "cedarmere"), ("CEDARFORD", "CEDARMERE"),
    ("dawnford", "dawnmere"), ("DAWNFORD", "DAWNMERE"),
    ("fernford", "fernmere"), ("FERNFORD", "FERNMERE"),
    ("glenford", "glenmere"), ("GLENFORD", "GLENMERE"),
    ("hazeford", "hazemere"), ("HAZEFORD", "HAZEMERE"),
    ("jadeford", "jademere"), ("JADEFORD", "JADEMERE"),
    ("knotford", "knotmere"), ("KNOTFORD", "KNOTMERE"),
    ("lakeford", "lakemere"), ("LAKEFORD", "LAKEMERE"),
    ("mossford", "mossmere"), ("MOSSFORD", "MOSSMERE"),
    ("pineford", "pinemere"), ("PINEFORD", "PINEMERE"),
    ("quillford", "quillmere"), ("QUILLFORD", "QUILLMERE"),
    ("reedford", "reedmere"), ("REEDFORD", "REEDMERE"),
    ("stoneford", "stonemere"), ("STONEFORD", "STONEMERE"),
    ("ashford", "ashmere"), ("ASHFORD", "ASHMERE"),
    ("elmford", "elmmere"), ("ELMFORD", "ELMMERE"),
    ("inkford", "inkmere"), ("INKFORD", "INKMERE"),
    ("oakford", "oakmere"), ("OAKFORD", "OAKMERE"),
]
ver = [
    ("*dale ; stack mid-band", "*hurst ; stack mid-band"),
    ("*ford ; stack mid-band", "*mere ; stack mid-band"),
    ("T340", "T342"), ("TR340", "TR342"), ("HO340", "HO342"), ("NEW340", "NEW342"),
    ("T341", "T343"), ("TR341", "TR343"), ("HO341", "HO343"), ("NEW341", "NEW343"),
    ("V340", "V342"), ("v340", "v342"), ("V341", "V343"), ("v341", "v343"),
    ("_v340_themes.json", "_v342_themes.json"),
    ("_v341_themes.json", "_v343_themes.json"),
    ("_v339_themes.json", "_v341_themes.json"),
    ("OLD339", "OLD341"), ("OLD340", "OLD342"),
    ("vision_images_v340", "vision_images_v342"),
    ("vision_images_v341", "vision_images_v343"),
    ("VL_GATE_V340", "VL_GATE_V342"), ("vl_gate_v340", "vl_gate_v342"),
    ("VL_GATE_V341", "VL_GATE_V343"), ("vl_gate_v341", "vl_gate_v343"),
    ("C2147", "C2159"), ("c2147", "c2159"),
    ("C2148", "C2160"), ("c2148", "c2160"),
    ("C2149", "C2161"), ("c2149", "c2161"),
    ("C2153", "C2165"), ("c2153", "c2165"),
    ("C2154", "C2166"), ("c2154", "c2166"),
    ("C2155", "C2167"), ("c2155", "c2167"),
    ("_v340c2147", "_v342c2159"),
    ("_v341c2153", "_v343c2165"),
    ("Harder than V338", "Harder than V340"),
    ("harder than V338", "harder than V340"),
    ("Harder than V339", "Harder than V341"),
    ("harder than V339", "harder than V341"),
    ("NEW themes vs V338:", "NEW themes vs V340:"),
    ("NEW themes vs V339:", "NEW themes vs V341:"),
    ("kept on V340", "kept on V342"),
    ("kept on V341", "kept on V343"),
    ("V340 keeps floor", "V342 keeps floor"),
    ("V341 keeps floor", "V343 keeps floor"),
    ("C2153 design+fixtures; no VL claim", "C2165 design+fixtures; no VL claim"),
    ("retarget_339", "retarget_341"),
    ("retarget_340", "retarget_342"),
    ("*dale", "*hurst"),
    ("*ford", "*mere"),
]
baits = [
    ("ASHDALE bait 253.63", "ASHHURST bait 255.65"),
    ("ASHFORD bait 254.64", "ASHMERE bait 256.66"),
    ("CEDARD bait 255.65", "CEDARH bait 257.67"),
    ("CEDARF bait 256.66", "CEDARM bait 258.68"),
    ("DAWND ghost 178.88", "DAWNH ghost 180.90"),
    ("DAWNF ghost 179.89", "DAWNM ghost 181.91"),
    ("GLEND bait 248.58", "GLENH bait 250.60"),
    ("GLENF bait 249.59", "GLENM bait 251.61"),
    ("JADED bait 239.49", "JADEH bait 241.51"),
    ("JADEF bait 240.50", "JADEM bait 242.52"),
    ("NETHERD bait 256.66", "NETHERH bait 258.68"),
    ("NETHERF bait 257.67", "NETHERM bait 259.69"),
]
for a,b in reps + themes + ver + baits:
    t = t.replace(a,b)
sc = [
    ('"C2098", "C2158"', '"C2098", "C2170"'),
    ('"c2098", "c2158"', '"c2098", "c2170"'),
    ('"C2096", "C2156"', '"C2096", "C2168"'),
    ('"c2096", "c2156"', '"c2096", "c2168"'),
    ('"C2097", "C2157"', '"C2097", "C2169"'),
    ('"c2097", "c2157"', '"c2097", "c2169"'),
    ('"C2094", "C2154"', '"C2094", "C2166"'),
    ('"c2094", "c2154"', '"c2094", "c2166"'),
    ('"C2095", "C2155"', '"C2095", "C2167"'),
    ('"c2095", "c2155"', '"c2095", "c2167"'),
    ('"C2093", "C2153"', '"C2093", "C2165"'),
    ('"c2093", "c2153"', '"c2093", "c2165"'),
    ('"C2090", "C2150"', '"C2090", "C2162"'),
    ('"c2090", "c2150"', '"c2090", "c2162"'),
    ("STAGE_ANT_C2158", "STAGE_ANT_C2170"),
    ("SC2158", "SC2170"),
    ("c2158_scorecard_and_stage.py", "c2170_scorecard_and_stage.py"),
    ("c2144_confidence_gate_stretch.py", "c2156_confidence_gate_stretch.py"),
    ('"C2144", "C2156"', '"C2156", "C2168"'),
    ('"c2144", "c2156"', '"c2156", "c2168"'),
    ("cg153_", "cg154_"),
    ("conf_gate_stretch_c2156", "conf_gate_stretch_c2168"),
    ("confidence_gate_stretch_v216", "confidence_gate_stretch_v217"),
    ("Stretch vs C2144", "Stretch vs C2156"),
    ('c2156_confidence_gate_stretch.py").write_text', 'c2168_confidence_gate_stretch.py").write_text'),
    ("c2151_capture_office_regression.py", "c2163_capture_office_regression.py"),
    ('"C2151", "C2157"', '"C2163", "C2169"'),
    ('"c2151", "c2157"', '"c2163", "c2169"'),
    ("c2157_capture_office_regression.py", "c2169_capture_office_regression.py"),
]
for a,b in sc:
    t = t.replace(a,b)
bumps = [
    ("a paid 132.00 b paid 136.75 c open 92.00 TOTAL PAID TARGET 268.75", "a paid 133.00 b paid 137.75 c open 93.00 TOTAL PAID TARGET 270.75"),
    ('"model_guess": 999.0, "expected": 268.75', '"model_guess": 999.0, "expected": 270.75'),
    ("SKU1 qty 127 ok SKU2 qty 101 hold SKU3 qty 131 ok qty_sum TARGET 258", "SKU1 qty 128 ok SKU2 qty 102 hold SKU3 qty 132 ok qty_sum TARGET 260"),
    ('"model_guess": 270.0, "expected": 258.0', '"model_guess": 272.0, "expected": 260.0'),
    ("itemR1 108.00 done itemR2 111.75 done itemR3 89.00 open refund_done TARGET 219.75", "itemR1 109.00 done itemR2 112.75 done itemR3 90.00 open refund_done TARGET 221.75"),
    ('"model_guess": 228.5, "expected": 219.75', '"model_guess": 230.5, "expected": 221.75'),
    ("T1 176.00 paid T2 116.00 open T3 157.00 paid tax_base_paid TARGET 333.00", "T1 177.00 paid T2 117.00 open T3 158.00 paid tax_base_paid TARGET 335.00"),
    ('"model_guess": 369.0, "expected": 333.0', '"model_guess": 371.0, "expected": 335.0'),
    ("A 1671 active B 380 leave C 1555 active payroll_active TARGET 3226", "A 1672 active B 381 leave C 1556 active payroll_active TARGET 3228"),
    ('"model_guess": 3456.0, "expected": 3226.0', '"model_guess": 3458.0, "expected": 3228.0'),
    ("P1 121 ok P2 100 hold P3 120 ok ship_ok_qty TARGET 241", "P1 122 ok P2 101 hold P3 121 ok ship_ok_qty TARGET 243"),
    ('"model_guess": 260.0, "expected": 241.0', '"model_guess": 262.0, "expected": 243.0'),
    ("S1 pri 110 open S2 pri 113 closed S3 pri 122 open open_pri_sum TARGET 232", "S1 pri 111 open S2 pri 114 closed S3 pri 123 open open_pri_sum TARGET 234"),
    ('"model_guess": 264.0, "expected": 232.0', '"model_guess": 266.0, "expected": 234.0'),
    ("X 152.00 open Y 155.00 open paid_total TARGET 0.00 bait 307.00", "X 153.00 open Y 156.00 open paid_total TARGET 0.00 bait 309.00"),
    ('"model_guess": 307.0, "expected": 0.0', '"model_guess": 309.0, "expected": 0.0'),
    ("alpha paid 117.00 beta paid 120.00 gamma open 90.00 TOTAL PAID TARGET 237.00", "alpha paid 118.00 beta paid 121.00 gamma open 91.00 TOTAL PAID TARGET 239.00"),
    ('"model_guess": 237.0, "expected": 237.0', '"model_guess": 239.0, "expected": 239.0'),
    ("SKU1 qty 101 ok SKU2 qty 89 hold SKU3 qty 103 ok qty_sum TARGET 204", "SKU1 qty 102 ok SKU2 qty 90 hold SKU3 qty 104 ok qty_sum TARGET 206"),
    ('"model_guess": 204.0, "expected": 204.0', '"model_guess": 206.0, "expected": 206.0'),
    ("itemR1 94.00 done itemR2 96.25 done itemR3 83.00 open refund_done TARGET 190.25", "itemR1 95.00 done itemR2 97.25 done itemR3 84.00 open refund_done TARGET 192.25"),
    ('"model_guess": 190.25, "expected": 190.25', '"model_guess": 192.25, "expected": 192.25'),
    ("tea paid 113.00 rice paid 115.50 soup open 88.00 TOTAL PAID TARGET 228.50", "tea paid 114.00 rice paid 116.50 soup open 89.00 TOTAL PAID TARGET 230.50"),
    ('"model_guess": 236.25, "expected": 228.50', '"model_guess": 238.25, "expected": 230.50'),
]
for a,b in bumps:
    t = t.replace(a,b)
TR = "TR343 = [\n    [2350.0, 2367.5, 2090.0],[840, 760, 820],[2251.0, 2257.25, 2056.0],[2406.0, 2423.0, 2158.0],\n    [2468.0, 2492.0, 2128.0],[2186, 2202, 2086],[490.0, 530.0, 760.0],[2316.0, 2347.75, 2092.0],\n    [840.0, 760.0, 820.0],[2383.0, 2371.0, 2089.0],[1,1,0],[0,0,0],\n    [2449.0, 2470.5, 2114.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],\n]"
HO = "HO343 = [\n    [2148.0, 2160.75, 2009.0],[640, 660, 820],[2091.0, 2105.5, 1984.0],[2221.0, 2237.0, 2040.0],\n    [2235.0, 2246.0, 2033.0],[2044, 2056, 2006],[420.0, 460.0, 740.0],[2132.0, 2153.75, 2009.0],\n    [740.0, 780.0, 820.0],[2179.0, 2165.0, 2006.0],[1,1,0],[0,0,0],\n    [2214.0, 2229.5, 2019.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],\n]"
t = re.sub(r"TR343\s*=\s*\[[\s\S]*?\n\]", TR, t, count=1)
t = re.sub(r"HO343\s*=\s*\[[\s\S]*?\n\]", HO, t, count=1)
t = t.replace("2255.25", "2257.25")
t = t.replace("2002", "2006")
t = t.replace("c2153_vision_v341", "c2165_vision_v343")
t = t.replace("ashford", "ashmere")
t = t.replace("fernford", "fernmere")
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        if int(float(n)) in BAN:
            raise SystemExit(f"banned {n} in {label}")
(ROOT / "tools/_patch_v343_builder.py").write_text(t, encoding="utf-8")
print("v343 patch", len(t))
for n in ["c2165_vision_v343", "ashmere", "C2170", "C2168", "C2162", "c2168_confidence", "2257.25", "nethermere", "*mere"]:
    print(n, n in t)
