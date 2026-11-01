from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
t = (ROOT / "tools/_patch_v344_builder.py").read_text(encoding="utf-8")
# V342: from v341 conf-gate *ford -> v342 product-U2C *hurst
# V344: from v343 conf-gate *mere -> v344 product-U2C *vale (theme wrap)
reps = [
    ("tools/_build_v341.py", "tools/_build_v343.py"),
    ("# V341 knife = confidence-gate", "# V343 knife = confidence-gate"),
    ("SC2158 = ", "SC2170 = "),
]
themes = [
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
]
ver = [
    ("*ford ; stack mid-band", "*mere ; stack mid-band"),
    ("*hurst ; stack mid-band", "*vale ; stack mid-band"),
    ("T341", "T343"), ("TR341", "TR343"), ("HO341", "HO343"), ("NEW341", "NEW343"),
    ("T342", "T344"), ("TR342", "TR344"), ("HO342", "HO344"), ("NEW342", "NEW344"),
    ("V341", "V343"), ("v341", "v343"), ("V342", "V344"), ("v342", "v344"),
    ("_v341_themes.json", "_v343_themes.json"),
    ("_v342_themes.json", "_v344_themes.json"),
    ("_v340_themes.json", "_v342_themes.json"),
    ("OLD340", "OLD342"), ("OLD341", "OLD343"),
    ("vision_images_v341", "vision_images_v343"),
    ("vision_images_v342", "vision_images_v344"),
    ("VL_GATE_V341", "VL_GATE_V343"), ("vl_gate_v341", "vl_gate_v343"),
    ("VL_GATE_V342", "VL_GATE_V344"), ("vl_gate_v342", "vl_gate_v344"),
    ("C2153", "C2165"), ("c2153", "c2165"),
    ("C2154", "C2166"), ("c2154", "c2166"),
    ("C2155", "C2167"), ("c2155", "c2167"),
    ("C2159", "C2171"), ("c2159", "c2171"),
    ("C2160", "C2172"), ("c2160", "c2172"),
    ("C2161", "C2173"), ("c2161", "c2173"),
    ("_v341c2153", "_v343c2165"),
    ("_v342c2159", "_v344c2171"),
    ("Harder than V339", "Harder than V341"),
    ("harder than V339", "harder than V341"),
    ("Harder than V340", "Harder than V342"),
    ("harder than V340", "harder than V342"),
    ("NEW themes vs V339:", "NEW themes vs V341:"),
    ("NEW themes vs V340:", "NEW themes vs V342:"),
    ("kept on V341", "kept on V343"),
    ("kept on V342", "kept on V344"),
    ("V341 keeps floor", "V343 keeps floor"),
    ("V342 keeps floor", "V344 keeps floor"),
    ("C2159 design+fixtures; no VL claim", "C2171 design+fixtures; no VL claim"),
    ("retarget_340", "retarget_342"),
    ("retarget_341", "retarget_343"),
    ("*ford", "*mere"),
    ("*hurst", "*vale"),
]
baits = [
    ("ASHHURST bait 255.65", "ASHVALE bait 257.67"),
    ("ASHMERE bait 256.66", "ASHVALE bait 257.67"),
    ("CEDARH bait 257.67", "CEDARV bait 259.69"),
    ("CEDARM bait 258.68", "CEDARV bait 259.69"),
    ("DAWNH ghost 180.90", "DAWNV ghost 182.92"),
    ("DAWNM ghost 181.91", "DAWNV ghost 182.92"),
    ("GLENH bait 250.60", "GLENV bait 252.62"),
    ("GLENM bait 251.61", "GLENV bait 252.62"),
    ("JADEH bait 241.51", "JADEV bait 243.53"),
    ("JADEM bait 242.52", "JADEV bait 243.53"),
    ("NETHERH bait 258.68", "NETHERV bait 260.70"),
    ("NETHERM bait 259.69", "NETHERV bait 260.70"),
]
for a,b in reps + themes + ver + baits:
    t = t.replace(a,b)
sc = [
    ('"C2092", "C2164"', '"C2092", "C2176"'),
    ('"c2092", "c2164"', '"c2092", "c2176"'),
    ('"C2090", "C2162"', '"C2090", "C2174"'),
    ('"c2090", "c2162"', '"c2090", "c2174"'),
    ('"C2091", "C2163"', '"C2091", "C2175"'),
    ('"c2091", "c2163"', '"c2091", "c2175"'),
    ('"C2084", "C2156"', '"C2084", "C2168"'),
    ('"c2084", "c2156"', '"c2084", "c2168"'),
    ("STAGE_ANT_C2164", "STAGE_ANT_C2176"),
    ("SC2164", "SC2176"),
    ("c2164_scorecard_and_stage.py", "c2176_scorecard_and_stage.py"),
    ("c2150_product_u2c_cost.py", "c2162_product_u2c_cost.py"),
    ('"C2150", "C2162"', '"C2162", "C2174"'),
    ('"c2150", "c2162"', '"c2162", "c2174"'),
    ("product_u2c_cost_c2162", "product_u2c_cost_c2174"),
    ("u2c_v218", "u2c_v220"),
    ("u2c_c2162", "u2c_c2174"),
    ('c2162_product_u2c_cost.py").write_text', 'c2174_product_u2c_cost.py").write_text'),
    ("product_u2c from c2150", "product_u2c from c2162"),
    ("c2157_capture_office_regression.py", "c2169_capture_office_regression.py"),
    ('"C2157", "C2163"', '"C2169", "C2175"'),
    ('"c2157", "c2163"', '"c2169", "c2175"'),
    ("c2163_capture_office_regression.py", "c2175_capture_office_regression.py"),
]
for a,b in sc:
    t = t.replace(a,b)
TR = "TR344 = [\n    [2352.0, 2369.5, 2092.0],[840, 760, 820],[2252.0, 2258.25, 2057.0],[2408.0, 2425.0, 2160.0],\n    [2470.0, 2494.0, 2130.0],[2188, 2204, 2088],[490.0, 530.0, 760.0],[2318.0, 2349.75, 2094.0],\n    [840.0, 760.0, 820.0],[2385.0, 2373.0, 2091.0],[1,1,0],[0,0,0],\n    [2451.0, 2472.5, 2116.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],\n]"
HO = "HO344 = [\n    [2150.0, 2162.75, 2011.0],[640, 660, 820],[2093.0, 2107.5, 1986.0],[2223.0, 2239.0, 2042.0],\n    [2234.0, 2245.0, 2035.0],[2046, 2058, 2008],[420.0, 460.0, 740.0],[2134.0, 2155.75, 2011.0],\n    [740.0, 780.0, 820.0],[2181.0, 2167.0, 2008.0],[1,1,0],[0,0,0],\n    [2216.0, 2231.5, 2021.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],\n]"
t = re.sub(r"TR344\s*=\s*\[[\s\S]*?\n\]", TR, t, count=1)
t = re.sub(r"HO344\s*=\s*\[[\s\S]*?\n\]", HO, t, count=1)
t = t.replace("2256.25", "2258.25")
t = t.replace("2004", "2008")
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        if int(float(n)) in BAN:
            raise SystemExit(f"banned {n} in {label}")
(ROOT / "tools/_patch_v344_builder.py").write_text(t, encoding="utf-8")
print("v344 patch", len(t))
for n in ["c2171_vision_v344", "ashvale", "C2176", "C2174", "C2168", "c2174_product", "2258.25", "nethervale", "*vale"]:
    print(n, n in t)
