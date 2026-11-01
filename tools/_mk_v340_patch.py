from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
t = (ROOT / "tools/_patch_v340_builder.py").read_text(encoding="utf-8")
# V338: from v337 conf-gate *moor -> v338 product-U2C *fen
# V340: from v339 conf-gate *brook -> v340 product-U2C *dale
reps = [
    ("tools/_build_v337.py", "tools/_build_v339.py"),
    ("# V337 knife = confidence-gate", "# V339 knife = confidence-gate"),
    ("SC2134 = ", "SC2146 = "),
]
themes = [
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
]
ver = [
    ("*moor ; stack mid-band", "*brook ; stack mid-band"),
    ("*fen ; stack mid-band", "*dale ; stack mid-band"),
    ("T337", "T339"), ("TR337", "TR339"), ("HO337", "HO339"), ("NEW337", "NEW339"),
    ("T338", "T340"), ("TR338", "TR340"), ("HO338", "HO340"), ("NEW338", "NEW340"),
    ("V337", "V339"), ("v337", "v339"), ("V338", "V340"), ("v338", "v340"),
    ("_v337_themes.json", "_v339_themes.json"),
    ("_v338_themes.json", "_v340_themes.json"),
    ("_v336_themes.json", "_v338_themes.json"),
    ("OLD336", "OLD338"), ("OLD337", "OLD339"),
    ("vision_images_v337", "vision_images_v339"),
    ("vision_images_v338", "vision_images_v340"),
    ("VL_GATE_V337", "VL_GATE_V339"), ("vl_gate_v337", "vl_gate_v339"),
    ("VL_GATE_V338", "VL_GATE_V340"), ("vl_gate_v338", "vl_gate_v340"),
    ("C2129", "C2141"), ("c2129", "c2141"),
    ("C2130", "C2142"), ("c2130", "c2142"),
    ("C2131", "C2143"), ("c2131", "c2143"),
    ("C2135", "C2147"), ("c2135", "c2147"),
    ("C2136", "C2148"), ("c2136", "c2148"),
    ("C2137", "C2149"), ("c2137", "c2149"),
    ("_v337c2129", "_v339c2141"),
    ("_v338c2135", "_v340c2147"),
    ("Harder than V335", "Harder than V337"),
    ("harder than V335", "harder than V337"),
    ("Harder than V336", "Harder than V338"),
    ("harder than V336", "harder than V338"),
    ("NEW themes vs V335:", "NEW themes vs V337:"),
    ("NEW themes vs V336:", "NEW themes vs V338:"),
    ("kept on V337", "kept on V339"),
    ("kept on V338", "kept on V340"),
    ("V337 keeps floor", "V339 keeps floor"),
    ("V338 keeps floor", "V340 keeps floor"),
    ("C2135 design+fixtures; no VL claim", "C2147 design+fixtures; no VL claim"),
    ("retarget_336", "retarget_338"),
    ("retarget_337", "retarget_339"),
    ("*moor", "*brook"),
    ("*fen", "*dale"),
]
baits = [
    ("ASHFEN bait 251.61", "ASHDALE bait 253.63"),
    ("ASHBROOK bait 252.62", "ASHDALE bait 253.63"),
    ("CEDARF bait 253.63", "CEDARD bait 255.65"),
    ("CEDARB bait 254.64", "CEDARD bait 255.65"),
    ("DAWNF ghost 176.86", "DAWND ghost 178.88"),
    ("DAWNB ghost 177.87", "DAWND ghost 178.88"),
    ("GLENF bait 246.56", "GLEND bait 248.58"),
    ("GLENB bait 247.57", "GLEND bait 248.58"),
    ("JADEF bait 237.47", "JADED bait 239.49"),
    ("JADEB bait 238.48", "JADED bait 239.49"),
    ("NETHERF bait 254.64", "NETHERD bait 256.66"),
    ("NETHERB bait 255.65", "NETHERD bait 256.66"),
]
for a,b in reps + themes + ver + baits:
    t = t.replace(a,b)
sc = [
    ('"C2092", "C2140"', '"C2092", "C2152"'),
    ('"c2092", "c2140"', '"c2092", "c2152"'),
    ('"C2090", "C2138"', '"C2090", "C2150"'),
    ('"c2090", "c2138"', '"c2090", "c2150"'),
    ('"C2091", "C2139"', '"C2091", "C2151"'),
    ('"c2091", "c2139"', '"c2091", "c2151"'),
    ('"C2084", "C2132"', '"C2084", "C2144"'),
    ('"c2084", "c2132"', '"c2084", "c2144"'),
    ("STAGE_ANT_C2140", "STAGE_ANT_C2152"),
    ("SC2140", "SC2152"),
    ("c2140_scorecard_and_stage.py", "c2152_scorecard_and_stage.py"),
    ("c2126_product_u2c_cost.py", "c2138_product_u2c_cost.py"),
    ('"C2126", "C2138"', '"C2138", "C2150"'),
    ('"c2126", "c2138"', '"c2138", "c2150"'),
    ("product_u2c_cost_c2138", "product_u2c_cost_c2150"),
    ("u2c_v214", "u2c_v216"),
    ("u2c_c2138", "u2c_c2150"),
    ('c2138_product_u2c_cost.py").write_text', 'c2150_product_u2c_cost.py").write_text'),
    ("product_u2c from c2126", "product_u2c from c2138"),
    ("c2133_capture_office_regression.py", "c2145_capture_office_regression.py"),
    ('"C2133", "C2139"', '"C2145", "C2151"'),
    ('"c2133", "c2139"', '"c2145", "c2151"'),
    ("c2139_capture_office_regression.py", "c2151_capture_office_regression.py"),
]
for a,b in sc:
    t = t.replace(a,b)
TR = "TR340 = [\n    [2344.0, 2361.5, 2084.0],[840, 760, 820],[2253.0, 2259.25, 2053.0],[2400.0, 2417.0, 2152.0],\n    [2462.0, 2486.0, 2122.0],[2180, 2196, 2080],[490.0, 530.0, 760.0],[2310.0, 2341.75, 2086.0],\n    [840.0, 760.0, 820.0],[2377.0, 2365.0, 2083.0],[1,1,0],[0,0,0],\n    [2443.0, 2464.5, 2108.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],\n]"
HO = "HO340 = [\n    [2142.0, 2154.75, 2003.0],[640, 660, 820],[2085.0, 2099.5, 1978.0],[2215.0, 2231.0, 2034.0],\n    [2238.0, 2249.0, 2027.0],[2038, 2050, 2000],[420.0, 460.0, 740.0],[2126.0, 2147.75, 2003.0],\n    [740.0, 780.0, 820.0],[2173.0, 2159.0, 2000.0],[1,1,0],[0,0,0],\n    [2208.0, 2223.5, 2013.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],\n]"
t = re.sub(r"TR340\s*=\s*\[[\s\S]*?\n\]", TR, t, count=1)
t = re.sub(r"HO340\s*=\s*\[[\s\S]*?\n\]", HO, t, count=1)
t = t.replace("2257.25", "2259.25")
t = t.replace("1996", "2000")
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        if int(float(n)) in BAN:
            raise SystemExit(f"banned {n} in {label}")
(ROOT / "tools/_patch_v340_builder.py").write_text(t, encoding="utf-8")
print("v340 patch", len(t))
for n in ["c2147_vision_v340", "ashdale", "C2152", "C2150", "C2144", "c2150_product", "2259.25", "netherdale", "*dale"]:
    print(n, n in t)
