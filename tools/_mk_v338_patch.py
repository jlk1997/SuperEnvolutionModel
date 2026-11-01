from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
# Start from clean V336 product-U2C patch structure
t = (ROOT / "tools/_patch_v336_builder.py").read_text(encoding="utf-8")
# V336: from v335 conf-gate *holm -> v336 product-U2C *wick
# V338: from v337 conf-gate *moor -> v338 product-U2C *fen
reps = [
    ("tools/_build_v335.py", "tools/_build_v337.py"),
    ("# V335 knife = confidence-gate", "# V337 knife = confidence-gate"),
    ("SC2122 = ", "SC2134 = "),
]
themes = [
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
]
ver = [
    ("*holm ; stack mid-band", "*moor ; stack mid-band"),
    ("*wick ; stack mid-band", "*fen ; stack mid-band"),
    ("T335", "T337"), ("TR335", "TR337"), ("HO335", "HO337"), ("NEW335", "NEW337"),
    ("T336", "T338"), ("TR336", "TR338"), ("HO336", "HO338"), ("NEW336", "NEW338"),
    ("V335", "V337"), ("v335", "v337"), ("V336", "V338"), ("v336", "v338"),
    ("_v335_themes.json", "_v337_themes.json"),
    ("_v336_themes.json", "_v338_themes.json"),
    ("_v334_themes.json", "_v336_themes.json"),
    ("OLD334", "OLD336"), ("OLD335", "OLD337"),
    ("vision_images_v335", "vision_images_v337"),
    ("vision_images_v336", "vision_images_v338"),
    ("VL_GATE_V335", "VL_GATE_V337"), ("vl_gate_v335", "vl_gate_v337"),
    ("VL_GATE_V336", "VL_GATE_V338"), ("vl_gate_v336", "vl_gate_v338"),
    ("C2117", "C2129"), ("c2117", "c2129"),
    ("C2118", "C2130"), ("c2118", "c2130"),
    ("C2119", "C2131"), ("c2119", "c2131"),
    ("C2123", "C2135"), ("c2123", "c2135"),
    ("C2124", "C2136"), ("c2124", "c2136"),
    ("C2125", "C2137"), ("c2125", "c2137"),
    ("_v335c2117", "_v337c2129"),
    ("_v336c2123", "_v338c2135"),
    ("Harder than V333", "Harder than V335"),
    ("harder than V333", "harder than V335"),
    ("Harder than V334", "Harder than V336"),
    ("harder than V334", "harder than V336"),
    ("NEW themes vs V333:", "NEW themes vs V335:"),
    ("NEW themes vs V334:", "NEW themes vs V336:"),
    ("kept on V335", "kept on V337"),
    ("kept on V336", "kept on V338"),
    ("V335 keeps floor", "V337 keeps floor"),
    ("V336 keeps floor", "V338 keeps floor"),
    ("C2123 design+fixtures; no VL claim", "C2135 design+fixtures; no VL claim"),
    ("retarget_334", "retarget_336"),
    ("retarget_335", "retarget_337"),
    ("*holm", "*moor"),
    ("*wick", "*fen"),
]
baits = [
    ("ASHWICK bait 249.59", "ASHFEN bait 251.61"),
    ("ASHMOOR bait 248.58", "ASHFEN bait 251.61"),
    ("CEDARW bait 251.61", "CEDARF bait 253.63"),
    ("CEDARM bait 250.60", "CEDARF bait 253.63"),
    ("DAWNW ghost 174.84", "DAWNF ghost 176.86"),
    ("DAWNM ghost 173.83", "DAWNF ghost 176.86"),
    ("GLENW bait 244.54", "GLENF bait 246.56"),
    ("GLENM bait 243.53", "GLENF bait 246.56"),
    ("JADEW bait 235.45", "JADEF bait 237.47"),
    ("JADEM bait 234.44", "JADEF bait 237.47"),
    ("NETHERW bait 252.62", "NETHERF bait 254.64"),
    ("NETHERM bait 251.61", "NETHERF bait 254.64"),
]
for a,b in reps + themes + ver + baits:
    t = t.replace(a,b)
sc = [
    ('"C2092", "C2128"', '"C2092", "C2140"'),
    ('"c2092", "c2128"', '"c2092", "c2140"'),
    ('"C2090", "C2126"', '"C2090", "C2138"'),
    ('"c2090", "c2126"', '"c2090", "c2138"'),
    ('"C2091", "C2127"', '"C2091", "C2139"'),
    ('"c2091", "c2127"', '"c2091", "c2139"'),
    ('"C2084", "C2120"', '"C2084", "C2132"'),
    ('"c2084", "c2120"', '"c2084", "c2132"'),
    ("STAGE_ANT_C2128", "STAGE_ANT_C2140"),
    ("SC2128", "SC2140"),
    ("c2128_scorecard_and_stage.py", "c2140_scorecard_and_stage.py"),
    ("c2114_product_u2c_cost.py", "c2126_product_u2c_cost.py"),
    ('"C2114", "C2126"', '"C2126", "C2138"'),
    ('"c2114", "c2126"', '"c2126", "c2138"'),
    ("product_u2c_cost_c2126", "product_u2c_cost_c2138"),
    ("u2c_v212", "u2c_v214"),
    ("u2c_c2126", "u2c_c2138"),
    ('c2126_product_u2c_cost.py").write_text', 'c2138_product_u2c_cost.py").write_text'),
    ("product_u2c from c2114", "product_u2c from c2126"),
    ("c2121_capture_office_regression.py", "c2133_capture_office_regression.py"),
    ('"C2121", "C2127"', '"C2133", "C2139"'),
    ('"c2121", "c2127"', '"c2133", "c2139"'),
    ("c2127_capture_office_regression.py", "c2139_capture_office_regression.py"),
]
for a,b in sc:
    t = t.replace(a,b)
TR = "TR338 = [\n    [2340.0, 2357.5, 2080.0],[840, 760, 820],[2251.0, 2257.25, 2051.0],[2396.0, 2413.0, 2148.0],\n    [2458.0, 2482.0, 2118.0],[2176, 2192, 2076],[490.0, 530.0, 760.0],[2306.0, 2337.75, 2082.0],\n    [840.0, 760.0, 820.0],[2373.0, 2361.0, 2079.0],[1,1,0],[0,0,0],\n    [2439.0, 2460.5, 2104.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],\n]"
HO = "HO338 = [\n    [2138.0, 2150.75, 1999.0],[640, 660, 820],[2081.0, 2095.5, 1974.0],[2211.0, 2227.0, 2030.0],\n    [2240.0, 2251.0, 2023.0],[2034, 2046, 1996],[420.0, 460.0, 740.0],[2122.0, 2143.75, 1999.0],\n    [740.0, 780.0, 820.0],[2169.0, 2155.0, 1996.0],[1,1,0],[0,0,0],\n    [2204.0, 2219.5, 2009.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],\n]"
t = re.sub(r"TR338\s*=\s*\[[\s\S]*?\n\]", TR, t, count=1)
t = re.sub(r"HO338\s*=\s*\[[\s\S]*?\n\]", HO, t, count=1)
t = t.replace("2255.25", "2257.25")
t = t.replace("1992", "1996")
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        if int(float(n)) in BAN:
            raise SystemExit(f"banned {n} in {label}")
(ROOT / "tools/_patch_v338_builder.py").write_text(t, encoding="utf-8")
print("v338 patch", len(t))
for n in ["c2135_vision_v338", "ashfen", "C2140", "C2138", "C2132", "c2126_product", "c2138_product", "2257.25", "netherfen", "*fen"]:
    print(n, n in t)
