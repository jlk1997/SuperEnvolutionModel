from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
t = (ROOT / "tools/_patch_v342_builder.py").read_text(encoding="utf-8")
# V340: from v339 conf-gate *brook -> v340 product-U2C *dale
# V342: from v341 conf-gate *ford -> v342 product-U2C *hurst
reps = [
    ("tools/_build_v339.py", "tools/_build_v341.py"),
    ("# V339 knife = confidence-gate", "# V341 knife = confidence-gate"),
    ("SC2146 = ", "SC2158 = "),
]
themes = [
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
]
ver = [
    ("*brook ; stack mid-band", "*ford ; stack mid-band"),
    ("*dale ; stack mid-band", "*hurst ; stack mid-band"),
    ("T339", "T341"), ("TR339", "TR341"), ("HO339", "HO341"), ("NEW339", "NEW341"),
    ("T340", "T342"), ("TR340", "TR342"), ("HO340", "HO342"), ("NEW340", "NEW342"),
    ("V339", "V341"), ("v339", "v341"), ("V340", "V342"), ("v340", "v342"),
    ("_v339_themes.json", "_v341_themes.json"),
    ("_v340_themes.json", "_v342_themes.json"),
    ("_v338_themes.json", "_v340_themes.json"),
    ("OLD338", "OLD340"), ("OLD339", "OLD341"),
    ("vision_images_v339", "vision_images_v341"),
    ("vision_images_v340", "vision_images_v342"),
    ("VL_GATE_V339", "VL_GATE_V341"), ("vl_gate_v339", "vl_gate_v341"),
    ("VL_GATE_V340", "VL_GATE_V342"), ("vl_gate_v340", "vl_gate_v342"),
    ("C2141", "C2153"), ("c2141", "c2153"),
    ("C2142", "C2154"), ("c2142", "c2154"),
    ("C2143", "C2155"), ("c2143", "c2155"),
    ("C2147", "C2159"), ("c2147", "c2159"),
    ("C2148", "C2160"), ("c2148", "c2160"),
    ("C2149", "C2161"), ("c2149", "c2161"),
    ("_v339c2141", "_v341c2153"),
    ("_v340c2147", "_v342c2159"),
    ("Harder than V337", "Harder than V339"),
    ("harder than V337", "harder than V339"),
    ("Harder than V338", "Harder than V340"),
    ("harder than V338", "harder than V340"),
    ("NEW themes vs V337:", "NEW themes vs V339:"),
    ("NEW themes vs V338:", "NEW themes vs V340:"),
    ("kept on V339", "kept on V341"),
    ("kept on V340", "kept on V342"),
    ("V339 keeps floor", "V341 keeps floor"),
    ("V340 keeps floor", "V342 keeps floor"),
    ("C2147 design+fixtures; no VL claim", "C2159 design+fixtures; no VL claim"),
    ("retarget_338", "retarget_340"),
    ("retarget_339", "retarget_341"),
    ("*brook", "*ford"),
    ("*dale", "*hurst"),
]
baits = [
    ("ASHDALE bait 253.63", "ASHHURST bait 255.65"),
    ("ASHFORD bait 254.64", "ASHHURST bait 255.65"),
    ("CEDARD bait 255.65", "CEDARH bait 257.67"),
    ("CEDARF bait 256.66", "CEDARH bait 257.67"),
    ("DAWND ghost 178.88", "DAWNH ghost 180.90"),
    ("DAWNF ghost 179.89", "DAWNH ghost 180.90"),
    ("GLEND bait 248.58", "GLENH bait 250.60"),
    ("GLENF bait 249.59", "GLENH bait 250.60"),
    ("JADED bait 239.49", "JADEH bait 241.51"),
    ("JADEF bait 240.50", "JADEH bait 241.51"),
    ("NETHERD bait 256.66", "NETHERH bait 258.68"),
    ("NETHERF bait 257.67", "NETHERH bait 258.68"),
]
for a,b in reps + themes + ver + baits:
    t = t.replace(a,b)
sc = [
    ('"C2092", "C2152"', '"C2092", "C2164"'),
    ('"c2092", "c2152"', '"c2092", "c2164"'),
    ('"C2090", "C2150"', '"C2090", "C2162"'),
    ('"c2090", "c2150"', '"c2090", "c2162"'),
    ('"C2091", "C2151"', '"C2091", "C2163"'),
    ('"c2091", "c2151"', '"c2091", "c2163"'),
    ('"C2084", "C2144"', '"C2084", "C2156"'),
    ('"c2084", "c2144"', '"c2084", "c2156"'),
    ("STAGE_ANT_C2152", "STAGE_ANT_C2164"),
    ("SC2152", "SC2164"),
    ("c2152_scorecard_and_stage.py", "c2164_scorecard_and_stage.py"),
    ("c2138_product_u2c_cost.py", "c2150_product_u2c_cost.py"),
    ('"C2138", "C2150"', '"C2150", "C2162"'),
    ('"c2138", "c2150"', '"c2150", "c2162"'),
    ("product_u2c_cost_c2150", "product_u2c_cost_c2162"),
    ("u2c_v216", "u2c_v218"),
    ("u2c_c2150", "u2c_c2162"),
    ('c2150_product_u2c_cost.py").write_text', 'c2162_product_u2c_cost.py").write_text'),
    ("product_u2c from c2138", "product_u2c from c2150"),
    ("c2145_capture_office_regression.py", "c2157_capture_office_regression.py"),
    ('"C2145", "C2151"', '"C2157", "C2163"'),
    ('"c2145", "c2151"', '"c2157", "c2163"'),
    ("c2151_capture_office_regression.py", "c2163_capture_office_regression.py"),
]
for a,b in sc:
    t = t.replace(a,b)
TR = "TR342 = [\n    [2348.0, 2365.5, 2088.0],[840, 760, 820],[2250.0, 2256.25, 2055.0],[2404.0, 2421.0, 2156.0],\n    [2466.0, 2490.0, 2126.0],[2184, 2200, 2084],[490.0, 530.0, 760.0],[2314.0, 2345.75, 2090.0],\n    [840.0, 760.0, 820.0],[2381.0, 2369.0, 2087.0],[1,1,0],[0,0,0],\n    [2447.0, 2468.5, 2112.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],\n]"
HO = "HO342 = [\n    [2146.0, 2158.75, 2007.0],[640, 660, 820],[2089.0, 2103.5, 1982.0],[2219.0, 2235.0, 2038.0],\n    [2236.0, 2247.0, 2031.0],[2042, 2054, 2004],[420.0, 460.0, 740.0],[2130.0, 2151.75, 2007.0],\n    [740.0, 780.0, 820.0],[2177.0, 2163.0, 2004.0],[1,1,0],[0,0,0],\n    [2212.0, 2227.5, 2017.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],\n]"
t = re.sub(r"TR342\s*=\s*\[[\s\S]*?\n\]", TR, t, count=1)
t = re.sub(r"HO342\s*=\s*\[[\s\S]*?\n\]", HO, t, count=1)
t = t.replace("2259.25", "2256.25")
t = t.replace("2000", "2004")
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        if int(float(n)) in BAN:
            raise SystemExit(f"banned {n} in {label}")
(ROOT / "tools/_patch_v342_builder.py").write_text(t, encoding="utf-8")
print("v342 patch", len(t))
for n in ["c2159_vision_v342", "ashhurst", "C2164", "C2162", "C2156", "c2162_product", "2256.25", "netherhurst", "*hurst"]:
    print(n, n in t)
