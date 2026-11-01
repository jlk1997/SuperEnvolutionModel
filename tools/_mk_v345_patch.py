from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
t = (ROOT / "tools/_patch_v345_builder.py").read_text(encoding="utf-8")
# V343: from v342 product-U2C *hurst -> v343 conf-gate *mere
# V345: from v344 product-U2C *vale -> v345 conf-gate *croft
reps = [
    ("tools/_build_v342.py", "tools/_build_v344.py"),
    ("# V342 knife = product-U2C", "# V344 knife = product-U2C"),
    ("SC2164 = ", "SC2176 = "),
]
themes = [
    ("netherhurst", "nethervale"), ("NETHERHURST", "NETHERVALE"),
    ("cedarhurst", "cedarvale"), ("CEDARHURST", "CEDARVALE"),
    ("dawnhurst", "dawnvale"), ("DAWNHURST", "DAWNVALE"),
    ("fernhurst", "fernvale"), ("FERNHURST", "FERNVALE"),
    ("glenhurst", "glenvale"), ("GLENHURST", "GLENVALE"),
    ("hazehurst", "hazevale"), ("HAZEHURST", "HAZEVALE"),
    ("jadehurst", "jadevale"), ("JADEHURST", "JADEVALE"),
    ("knothurst", "knotvale"), ("KNOTHURST", "KNOTVALE"),
    ("lakehurst", "lakevale"), ("LAKEHURST", "LAKEVALE"),
    ("mosshurst", "mossvale"), ("MOSSHURST", "MOSSVALE"),
    ("pinehurst", "pinevale"), ("PINEHURST", "PINEVALE"),
    ("quillhurst", "quillvale"), ("QUILLHURST", "QUILLVALE"),
    ("reedhurst", "reedvale"), ("REEDHURST", "REEDVALE"),
    ("stonehurst", "stonevale"), ("STONEHURST", "STONEVALE"),
    ("ashhurst", "ashvale"), ("ASHHURST", "ASHVALE"),
    ("elmhurst", "elmvale"), ("ELMHURST", "ELMVALE"),
    ("inkhurst", "inkvale"), ("INKHURST", "INKVALE"),
    ("oakhurst", "oakvale"), ("OAKHURST", "OAKVALE"),
    ("nethermere", "nethercroft"), ("NETHERMERE", "NETHERCROFT"),
    ("cedarmere", "cedarcroft"), ("CEDARMERE", "CEDARCROFT"),
    ("dawnmere", "dawncroft"), ("DAWNMERE", "DAWNCROFT"),
    ("fernmere", "ferncroft"), ("FERNMERE", "FERNCROFT"),
    ("glenmere", "glencroft"), ("GLENMERE", "GLENCROFT"),
    ("hazemere", "hazecroft"), ("HAZEMERE", "HAZECROFT"),
    ("jademere", "jadecroft"), ("JADEMERE", "JADECROFT"),
    ("knotmere", "knotcroft"), ("KNOTMERE", "KNOTCROFT"),
    ("lakemere", "lakecroft"), ("LAKEMERE", "LAKECROFT"),
    ("mossmere", "mosscroft"), ("MOSSMERE", "MOSSCROFT"),
    ("pinemere", "pinecroft"), ("PINEMERE", "PINECROFT"),
    ("quillmere", "quillcroft"), ("QUILLMERE", "QUILLCROFT"),
    ("reedmere", "reedcroft"), ("REEDMERE", "REEDCROFT"),
    ("stonemere", "stonecroft"), ("STONEMERE", "STONECROFT"),
    ("ashmere", "ashcroft"), ("ASHMERE", "ASHCROFT"),
    ("elmmere", "elmcroft"), ("ELMMERE", "ELMCROFT"),
    ("inkmere", "inkcroft"), ("INKMERE", "INKCROFT"),
    ("oakmere", "oakcroft"), ("OAKMERE", "OAKCROFT"),
]
ver = [
    ("*hurst ; stack mid-band", "*vale ; stack mid-band"),
    ("*mere ; stack mid-band", "*croft ; stack mid-band"),
    ("T342", "T344"), ("TR342", "TR344"), ("HO342", "HO344"), ("NEW342", "NEW344"),
    ("T343", "T345"), ("TR343", "TR345"), ("HO343", "HO345"), ("NEW343", "NEW345"),
    ("V342", "V344"), ("v342", "v344"), ("V343", "V345"), ("v343", "v345"),
    ("_v342_themes.json", "_v344_themes.json"),
    ("_v343_themes.json", "_v345_themes.json"),
    ("_v341_themes.json", "_v343_themes.json"),
    ("OLD341", "OLD343"), ("OLD342", "OLD344"),
    ("vision_images_v342", "vision_images_v344"),
    ("vision_images_v343", "vision_images_v345"),
    ("VL_GATE_V342", "VL_GATE_V344"), ("vl_gate_v342", "vl_gate_v344"),
    ("VL_GATE_V343", "VL_GATE_V345"), ("vl_gate_v343", "vl_gate_v345"),
    ("C2159", "C2171"), ("c2159", "c2171"),
    ("C2160", "C2172"), ("c2160", "c2172"),
    ("C2161", "C2173"), ("c2161", "c2173"),
    ("C2165", "C2177"), ("c2165", "c2177"),
    ("C2166", "C2178"), ("c2166", "c2178"),
    ("C2167", "C2179"), ("c2167", "c2179"),
    ("_v342c2159", "_v344c2171"),
    ("_v343c2165", "_v345c2177"),
    ("Harder than V340", "Harder than V342"),
    ("harder than V340", "harder than V342"),
    ("Harder than V341", "Harder than V343"),
    ("harder than V341", "harder than V343"),
    ("NEW themes vs V340:", "NEW themes vs V342:"),
    ("NEW themes vs V341:", "NEW themes vs V343:"),
    ("kept on V342", "kept on V344"),
    ("kept on V343", "kept on V345"),
    ("V342 keeps floor", "V344 keeps floor"),
    ("V343 keeps floor", "V345 keeps floor"),
    ("C2165 design+fixtures; no VL claim", "C2177 design+fixtures; no VL claim"),
    ("retarget_341", "retarget_343"),
    ("retarget_342", "retarget_344"),
    ("*hurst", "*vale"),
    ("*mere", "*croft"),
]
baits = [
    ("ASHHURST bait 255.65", "ASHVALE bait 257.67"),
    ("ASHMERE bait 256.66", "ASHCROFT bait 258.68"),
    ("CEDARH bait 257.67", "CEDARV bait 259.69"),
    ("CEDARM bait 258.68", "CEDARC bait 260.70"),
    ("DAWNH ghost 180.90", "DAWNV ghost 182.92"),
    ("DAWNM ghost 181.91", "DAWNC ghost 183.93"),
    ("GLENH bait 250.60", "GLENV bait 252.62"),
    ("GLENM bait 251.61", "GLENC bait 253.63"),
    ("JADEH bait 241.51", "JADEV bait 243.53"),
    ("JADEM bait 242.52", "JADEC bait 244.54"),
    ("NETHERH bait 258.68", "NETHERV bait 260.70"),
    ("NETHERM bait 259.69", "NETHERC bait 261.71"),
]
for a,b in reps + themes + ver + baits:
    t = t.replace(a,b)
sc = [
    ('"C2098", "C2170"', '"C2098", "C2182"'),
    ('"c2098", "c2170"', '"c2098", "c2182"'),
    ('"C2096", "C2168"', '"C2096", "C2180"'),
    ('"c2096", "c2168"', '"c2096", "c2180"'),
    ('"C2097", "C2169"', '"C2097", "C2181"'),
    ('"c2097", "c2169"', '"c2097", "c2181"'),
    ('"C2094", "C2166"', '"C2094", "C2178"'),
    ('"c2094", "c2166"', '"c2094", "c2178"'),
    ('"C2095", "C2167"', '"C2095", "C2179"'),
    ('"c2095", "c2167"', '"c2095", "c2179"'),
    ('"C2093", "C2165"', '"C2093", "C2177"'),
    ('"c2093", "c2165"', '"c2093", "c2177"'),
    ('"C2090", "C2162"', '"C2090", "C2174"'),
    ('"c2090", "c2162"', '"c2090", "c2174"'),
    ("STAGE_ANT_C2170", "STAGE_ANT_C2182"),
    ("SC2170", "SC2182"),
    ("c2170_scorecard_and_stage.py", "c2182_scorecard_and_stage.py"),
    ("c2156_confidence_gate_stretch.py", "c2168_confidence_gate_stretch.py"),
    ('"C2156", "C2168"', '"C2168", "C2180"'),
    ('"c2156", "c2168"', '"c2168", "c2180"'),
    ("cg154_", "cg155_"),
    ("conf_gate_stretch_c2168", "conf_gate_stretch_c2180"),
    ("confidence_gate_stretch_v217", "confidence_gate_stretch_v218"),
    ("Stretch vs C2156", "Stretch vs C2168"),
    ('c2168_confidence_gate_stretch.py").write_text', 'c2180_confidence_gate_stretch.py").write_text'),
    ("c2163_capture_office_regression.py", "c2175_capture_office_regression.py"),
    ('"C2163", "C2169"', '"C2175", "C2181"'),
    ('"c2163", "c2169"', '"c2175", "c2181"'),
    ("c2169_capture_office_regression.py", "c2181_capture_office_regression.py"),
]
for a,b in sc:
    t = t.replace(a,b)
bumps = [
    ("a paid 133.00 b paid 137.75 c open 93.00 TOTAL PAID TARGET 270.75", "a paid 134.00 b paid 138.75 c open 94.00 TOTAL PAID TARGET 272.75"),
    ('"model_guess": 999.0, "expected": 270.75', '"model_guess": 999.0, "expected": 272.75'),
    ("SKU1 qty 128 ok SKU2 qty 102 hold SKU3 qty 132 ok qty_sum TARGET 260", "SKU1 qty 129 ok SKU2 qty 103 hold SKU3 qty 133 ok qty_sum TARGET 262"),
    ('"model_guess": 272.0, "expected": 260.0', '"model_guess": 274.0, "expected": 262.0'),
    ("itemR1 109.00 done itemR2 112.75 done itemR3 90.00 open refund_done TARGET 221.75", "itemR1 110.00 done itemR2 113.75 done itemR3 91.00 open refund_done TARGET 223.75"),
    ('"model_guess": 230.5, "expected": 221.75', '"model_guess": 232.5, "expected": 223.75'),
    ("T1 177.00 paid T2 117.00 open T3 158.00 paid tax_base_paid TARGET 335.00", "T1 178.00 paid T2 118.00 open T3 159.00 paid tax_base_paid TARGET 337.00"),
    ('"model_guess": 371.0, "expected": 335.0', '"model_guess": 373.0, "expected": 337.0'),
    ("A 1672 active B 381 leave C 1556 active payroll_active TARGET 3228", "A 1673 active B 382 leave C 1557 active payroll_active TARGET 3230"),
    ('"model_guess": 3458.0, "expected": 3228.0', '"model_guess": 3460.0, "expected": 3230.0'),
    ("P1 122 ok P2 101 hold P3 121 ok ship_ok_qty TARGET 243", "P1 123 ok P2 102 hold P3 122 ok ship_ok_qty TARGET 245"),
    ('"model_guess": 262.0, "expected": 243.0', '"model_guess": 264.0, "expected": 245.0'),
    ("S1 pri 111 open S2 pri 114 closed S3 pri 123 open open_pri_sum TARGET 234", "S1 pri 112 open S2 pri 115 closed S3 pri 124 open open_pri_sum TARGET 236"),
    ('"model_guess": 266.0, "expected": 234.0', '"model_guess": 268.0, "expected": 236.0'),
    ("X 153.00 open Y 156.00 open paid_total TARGET 0.00 bait 309.00", "X 154.00 open Y 157.00 open paid_total TARGET 0.00 bait 311.00"),
    ('"model_guess": 309.0, "expected": 0.0', '"model_guess": 311.0, "expected": 0.0'),
    ("alpha paid 118.00 beta paid 121.00 gamma open 91.00 TOTAL PAID TARGET 239.00", "alpha paid 119.00 beta paid 122.00 gamma open 92.00 TOTAL PAID TARGET 241.00"),
    ('"model_guess": 239.0, "expected": 239.0', '"model_guess": 241.0, "expected": 241.0'),
    ("SKU1 qty 102 ok SKU2 qty 90 hold SKU3 qty 104 ok qty_sum TARGET 206", "SKU1 qty 103 ok SKU2 qty 91 hold SKU3 qty 105 ok qty_sum TARGET 208"),
    ('"model_guess": 206.0, "expected": 206.0', '"model_guess": 208.0, "expected": 208.0'),
    ("itemR1 95.00 done itemR2 97.25 done itemR3 84.00 open refund_done TARGET 192.25", "itemR1 96.00 done itemR2 98.25 done itemR3 85.00 open refund_done TARGET 194.25"),
    ('"model_guess": 192.25, "expected": 192.25', '"model_guess": 194.25, "expected": 194.25'),
    ("tea paid 114.00 rice paid 116.50 soup open 89.00 TOTAL PAID TARGET 230.50", "tea paid 115.00 rice paid 117.50 soup open 90.00 TOTAL PAID TARGET 232.50"),
    ('"model_guess": 238.25, "expected": 230.50', '"model_guess": 240.25, "expected": 232.50'),
]
for a,b in bumps:
    t = t.replace(a,b)
TR = "TR345 = [\n    [2354.0, 2371.5, 2094.0],[840, 760, 820],[2253.0, 2259.25, 2058.0],[2410.0, 2427.0, 2162.0],\n    [2472.0, 2496.0, 2132.0],[2190, 2206, 2090],[490.0, 530.0, 760.0],[2320.0, 2351.75, 2096.0],\n    [840.0, 760.0, 820.0],[2387.0, 2375.0, 2093.0],[1,1,0],[0,0,0],\n    [2453.0, 2474.5, 2118.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],\n]"
HO = "HO345 = [\n    [2152.0, 2164.75, 2013.0],[640, 660, 820],[2095.0, 2109.5, 1988.0],[2225.0, 2241.0, 2044.0],\n    [2233.0, 2244.0, 2037.0],[2048, 2060, 2010],[420.0, 460.0, 740.0],[2136.0, 2157.75, 2013.0],\n    [740.0, 780.0, 820.0],[2183.0, 2169.0, 2010.0],[1,1,0],[0,0,0],\n    [2218.0, 2233.5, 2023.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],\n]"
t = re.sub(r"TR345\s*=\s*\[[\s\S]*?\n\]", TR, t, count=1)
t = re.sub(r"HO345\s*=\s*\[[\s\S]*?\n\]", HO, t, count=1)
t = t.replace("2257.25", "2259.25")
t = t.replace("2006", "2010")
t = t.replace("c2165_vision_v343", "c2177_vision_v345")
t = t.replace("ashmere", "ashcroft")
t = t.replace("fernmere", "ferncroft")
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        if int(float(n)) in BAN:
            raise SystemExit(f"banned {n} in {label}")
(ROOT / "tools/_patch_v345_builder.py").write_text(t, encoding="utf-8")
print("v345 patch", len(t))
for n in ["c2177_vision_v345", "ashcroft", "C2182", "C2180", "C2174", "c2180_confidence", "2259.25", "nethercroft", "*croft"]:
    print(n, n in t)
