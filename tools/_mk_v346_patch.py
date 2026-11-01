from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
t = (ROOT / "tools/_patch_v346_builder.py").read_text(encoding="utf-8")
# V344: from v343 conf-gate *mere -> v344 product-U2C *vale
# V346: from v345 conf-gate *croft -> v346 product-U2C *holm
reps = [
    ("tools/_build_v343.py", "tools/_build_v345.py"),
    ("# V343 knife = confidence-gate", "# V345 knife = confidence-gate"),
    ("SC2170 = ", "SC2182 = "),
]
themes = [
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
    ("nethervale", "netherholm"), ("NETHERVALE", "NETHERHOLM"),
    ("cedarvale", "cedarholm"), ("CEDARVALE", "CEDARHOLM"),
    ("dawnvale", "dawnholm"), ("DAWNVALE", "DAWNHOLM"),
    ("fernvale", "fernholm"), ("FERNVALE", "FERNHOLM"),
    ("glenvale", "glenholm"), ("GLENVALE", "GLENHOLM"),
    ("hazevale", "hazeholm"), ("HAZEVALE", "HAZEHOLM"),
    ("jadevale", "jadeholm"), ("JADEVALE", "JADEHOLM"),
    ("knotvale", "knotholm"), ("KNOTVALE", "KNOTHOLM"),
    ("lakevale", "lakeholm"), ("LAKEVALE", "LAKEHOLM"),
    ("mossvale", "mossholm"), ("MOSSVALE", "MOSSHOLM"),
    ("pinevale", "pineholm"), ("PINEVALE", "PINEHOLM"),
    ("quillvale", "quillholm"), ("QUILLVALE", "QUILLHOLM"),
    ("reedvale", "reedholm"), ("REEDVALE", "REEDHOLM"),
    ("stonevale", "stoneholm"), ("STONEVALE", "STONEHOLM"),
    ("ashvale", "ashholm"), ("ASHVALE", "ASHHOLM"),
    ("elmvale", "elmholm"), ("ELMVALE", "ELMHOLM"),
    ("inkvale", "inkholm"), ("INKVALE", "INKHOLM"),
    ("oakvale", "oakholm"), ("OAKVALE", "OAKHOLM"),
]
ver = [
    ("*mere ; stack mid-band", "*croft ; stack mid-band"),
    ("*vale ; stack mid-band", "*holm ; stack mid-band"),
    ("T343", "T345"), ("TR343", "TR345"), ("HO343", "HO345"), ("NEW343", "NEW345"),
    ("T344", "T346"), ("TR344", "TR346"), ("HO344", "HO346"), ("NEW344", "NEW346"),
    ("V343", "V345"), ("v343", "v345"), ("V344", "V346"), ("v344", "v346"),
    ("_v343_themes.json", "_v345_themes.json"),
    ("_v344_themes.json", "_v346_themes.json"),
    ("_v342_themes.json", "_v344_themes.json"),
    ("OLD342", "OLD344"), ("OLD343", "OLD345"),
    ("vision_images_v343", "vision_images_v345"),
    ("vision_images_v344", "vision_images_v346"),
    ("VL_GATE_V343", "VL_GATE_V345"), ("vl_gate_v343", "vl_gate_v345"),
    ("VL_GATE_V344", "VL_GATE_V346"), ("vl_gate_v344", "vl_gate_v346"),
    ("C2165", "C2177"), ("c2165", "c2177"),
    ("C2166", "C2178"), ("c2166", "c2178"),
    ("C2167", "C2179"), ("c2167", "c2179"),
    ("C2171", "C2183"), ("c2171", "c2183"),
    ("C2172", "C2184"), ("c2172", "c2184"),
    ("C2173", "C2185"), ("c2173", "c2185"),
    ("_v343c2165", "_v345c2177"),
    ("_v344c2171", "_v346c2183"),
    ("Harder than V341", "Harder than V343"),
    ("harder than V341", "harder than V343"),
    ("Harder than V342", "Harder than V344"),
    ("harder than V342", "harder than V344"),
    ("NEW themes vs V341:", "NEW themes vs V343:"),
    ("NEW themes vs V342:", "NEW themes vs V344:"),
    ("kept on V343", "kept on V345"),
    ("kept on V344", "kept on V346"),
    ("V343 keeps floor", "V345 keeps floor"),
    ("V344 keeps floor", "V346 keeps floor"),
    ("C2171 design+fixtures; no VL claim", "C2183 design+fixtures; no VL claim"),
    ("retarget_342", "retarget_344"),
    ("retarget_343", "retarget_345"),
    ("*mere", "*croft"),
    ("*vale", "*holm"),
]
baits = [
    ("ASHVALE bait 257.67", "ASHHOLM bait 259.69"),
    ("ASHCROFT bait 258.68", "ASHHOLM bait 259.69"),
    ("CEDARV bait 259.69", "CEDARH bait 261.71"),
    ("CEDARC bait 260.70", "CEDARH bait 261.71"),
    ("DAWNV ghost 182.92", "DAWNH ghost 184.94"),
    ("DAWNC ghost 183.93", "DAWNH ghost 184.94"),
    ("GLENV bait 252.62", "GLENH bait 254.64"),
    ("GLENC bait 253.63", "GLENH bait 254.64"),
    ("JADEV bait 243.53", "JADEH bait 245.55"),
    ("JADEC bait 244.54", "JADEH bait 245.55"),
    ("NETHERV bait 260.70", "NETHERH bait 262.72"),
    ("NETHERC bait 261.71", "NETHERH bait 262.72"),
]
for a,b in reps + themes + ver + baits:
    t = t.replace(a,b)
sc = [
    ('"C2092", "C2176"', '"C2092", "C2188"'),
    ('"c2092", "c2176"', '"c2092", "c2188"'),
    ('"C2090", "C2174"', '"C2090", "C2186"'),
    ('"c2090", "c2174"', '"c2090", "c2186"'),
    ('"C2091", "C2175"', '"C2091", "C2187"'),
    ('"c2091", "c2175"', '"c2091", "c2187"'),
    ('"C2084", "C2168"', '"C2084", "C2180"'),
    ('"c2084", "c2168"', '"c2084", "c2180"'),
    ("STAGE_ANT_C2176", "STAGE_ANT_C2188"),
    ("SC2176", "SC2188"),
    ("c2176_scorecard_and_stage.py", "c2188_scorecard_and_stage.py"),
    ("c2162_product_u2c_cost.py", "c2174_product_u2c_cost.py"),
    ('"C2162", "C2174"', '"C2174", "C2186"'),
    ('"c2162", "c2174"', '"c2174", "c2186"'),
    ("product_u2c_cost_c2174", "product_u2c_cost_c2186"),
    ("u2c_v220", "u2c_v222"),
    ("u2c_c2174", "u2c_c2186"),
    ('c2174_product_u2c_cost.py").write_text', 'c2186_product_u2c_cost.py").write_text'),
    ("product_u2c from c2162", "product_u2c from c2174"),
    ("c2169_capture_office_regression.py", "c2181_capture_office_regression.py"),
    ('"C2169", "C2175"', '"C2181", "C2187"'),
    ('"c2169", "c2175"', '"c2181", "c2187"'),
    ("c2175_capture_office_regression.py", "c2187_capture_office_regression.py"),
]
for a,b in sc:
    t = t.replace(a,b)
TR = "TR346 = [\n    [2356.0, 2373.5, 2096.0],[840, 760, 820],[2254.0, 2255.25, 2059.0],[2412.0, 2429.0, 2164.0],\n    [2474.0, 2498.0, 2134.0],[2192, 2208, 2092],[490.0, 530.0, 760.0],[2322.0, 2353.75, 2098.0],\n    [840.0, 760.0, 820.0],[2389.0, 2377.0, 2095.0],[1,1,0],[0,0,0],\n    [2455.0, 2476.5, 2120.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],\n]"
HO = "HO346 = [\n    [2154.0, 2166.75, 2015.0],[640, 660, 820],[2097.0, 2111.5, 1990.0],[2227.0, 2243.0, 2046.0],\n    [2232.0, 2243.0, 2039.0],[2050, 2062, 2012],[420.0, 460.0, 740.0],[2138.0, 2159.75, 2015.0],\n    [740.0, 780.0, 820.0],[2185.0, 2171.0, 2012.0],[1,1,0],[0,0,0],\n    [2220.0, 2235.5, 2025.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],\n]"
t = re.sub(r"TR346\s*=\s*\[[\s\S]*?\n\]", TR, t, count=1)
t = re.sub(r"HO346\s*=\s*\[[\s\S]*?\n\]", HO, t, count=1)
t = t.replace("2258.25", "2255.25")
t = t.replace("2008", "2012")
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        if int(float(n)) in BAN:
            raise SystemExit(f"banned {n} in {label}")
(ROOT / "tools/_patch_v346_builder.py").write_text(t, encoding="utf-8")
print("v346 patch", len(t))
for n in ["c2183_vision_v346", "ashholm", "C2188", "C2186", "C2180", "c2186_product", "2255.25", "netherholm", "*holm"]:
    print(n, n in t)
