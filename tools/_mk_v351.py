from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v350.py").read_text(encoding="utf-8")
idx0 = b0.find("# V350 knife = product-U2C")
if idx0 < 0:
    raise SystemExit("knife not found")
head0 = b0[:idx0]
if "SC2212 = " in head0:
    head0 = head0[:head0.find("SC2212 = ")]
theme_pairs = [
    ("netherbrook", "netherdale"), ("NETHERBROOK", "NETHERDALE"),
    ("cedarbrook", "cedardale"), ("CEDARBROOK", "CEDARDALE"),
    ("dawnbrook", "dawndale"), ("DAWNBROOK", "DAWNDALE"),
    ("fernbrook", "ferndale"), ("FERNBROOK", "FERNDALE"),
    ("glenbrook", "glendale"), ("GLENBROOK", "GLENDALE"),
    ("hazebrook", "hazedale"), ("HAZEBROOK", "HAZEDALE"),
    ("jadebrook", "jadedale"), ("JADEBROOK", "JADEDALE"),
    ("knotbrook", "knotdale"), ("KNOTBROOK", "KNOTDALE"),
    ("lakebrook", "lakedale"), ("LAKEBROOK", "LAKEDALE"),
    ("mossbrook", "mossdale"), ("MOSSBROOK", "MOSSDALE"),
    ("pinebrook", "pinedale"), ("PINEBROOK", "PINEDALE"),
    ("quillbrook", "quilldale"), ("QUILLBROOK", "QUILLDALE"),
    ("reedbrook", "reeddale"), ("REEDBROOK", "REEDDALE"),
    ("stonebrook", "stonedale"), ("STONEBROOK", "STONEDALE"),
    ("ashbrook", "ashdale"), ("ASHBROOK", "ASHDALE"),
    ("elmbrook", "elmdale"), ("ELMBROOK", "ELMDALE"),
    ("inkbrook", "inkdale"), ("INKBROOK", "INKDALE"),
    ("oakbrook", "oakdale"), ("OAKBROOK", "OAKDALE"),
]
pairs = [
    ("*brook ; stack mid-band", "*dale ; stack mid-band"),
    ("T350", "T351"), ("TR350", "TR351"), ("HO350", "HO351"),
    ("NEW350", "NEW351"),
    ("V350", "V351"), ("v350", "v351"),
    ("_v350_themes.json", "_v351_themes.json"),
    ("_v349_themes.json", "_v350_themes.json"),
    ("OLD349", "OLD350"),
    ("vision_images_v350", "vision_images_v351"),
    ("VL_GATE_V350", "VL_GATE_V351"), ("vl_gate_v350", "vl_gate_v351"),
    ("C2207", "C2213"), ("c2207", "c2213"),
    ("C2208", "C2214"), ("c2208", "c2214"),
    ("C2209", "C2215"), ("c2209", "c2215"),
    ("_v350c2207", "_v351c2213"),
    ("Harder than V348", "Harder than V349"),
    ("harder than V348", "harder than V349"),
    ("NEW themes vs V348:", "NEW themes vs V349:"),
    ("kept on V350", "kept on V351"),
    ("V350 keeps floor", "V351 keeps floor"),
    ("C2207 design+fixtures; no VL claim", "C2213 design+fixtures; no VL claim"),
    ("retarget_349", "retarget_350"),
    ("*brook", "*dale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)
h = h.replace("ASHBROOK bait 251.61", "ASHDALE bait 252.62")
h = h.replace("CEDARB bait 265.75", "CEDARD bait 266.76")
h = h.replace("DAWNB ghost 188.98", "DAWND ghost 189.99")
h = h.replace("GLENB bait 258.68", "GLEND bait 259.69")
h = h.replace("JADEB bait 249.59", "JADED bait 250.60")
h = h.replace("NETHERB bait 266.76", "NETHERD bait 267.77")
TR = """TR351 = [
    [2366.0, 2383.5, 2106.0],[840, 760, 820],[2245.0, 2247.25, 2052.0],[2422.0, 2439.0, 2174.0],
    [2484.0, 2493.0, 2144.0],[2202, 2218, 2102],[490.0, 530.0, 760.0],[2332.0, 2363.75, 2108.0],
    [840.0, 760.0, 820.0],[2399.0, 2387.0, 2105.0],[1,1,0],[0,0,0],
    [2457.0, 2476.5, 2116.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO351 = [
    [2164.0, 2176.75, 2025.0],[640, 660, 820],[2107.0, 2121.5, 2000.0],[2237.0, 2253.0, 2056.0],
    [2241.0, 2252.0, 2049.0],[2060, 2072, 2022],[420.0, 460.0, 740.0],[2148.0, 2169.75, 2025.0],
    [740.0, 780.0, 820.0],[2195.0, 2181.0, 2022.0],[1,1,0],[0,0,0],
    [2225.0, 2239.5, 2029.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
h = re.sub(r"TR351\s*=\s*\[[\s\S]*?\n\]", TR, h, count=1)
h = re.sub(r"HO351\s*=\s*\[[\s\S]*?\n\]", HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2218"), ("c2098", "c2218"),
    ("C2096", "C2216"), ("c2096", "c2216"),
    ("C2097", "C2217"), ("c2097", "c2217"),
    ("C2094", "C2214"), ("c2094", "c2214"),
    ("C2095", "C2215"), ("c2095", "c2215"),
    ("C2093", "C2213"), ("c2093", "c2213"),
    ("C2090", "C2210"), ("c2090", "c2210"),
    ("V331", "V351"), ("v331", "v351"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2218"),
    ("*vale", "*dale"),
]:
    sc_body = sc_body.replace(a, b2)
tail = r'''# V351 knife = confidence-gate (alternating; V350 was product-U2C)
out = (S / "c2204_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2204", "C2216"), ("c2204", "c2216"),
    ("C2096", "C2216"), ("c2096", "c2216"),
    ("cg140_", "cg135_"),
    ("conf_gate_stretch_c2216", "conf_gate_stretch_c2216"),
    ("confidence_gate_stretch_v203", "confidence_gate_stretch_v198"),
    ("Stretch vs C2120", "Stretch vs C2126"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 146.00 b paid 150.75 c open 106.00 TOTAL PAID TARGET 296.75", "a paid 152.00 b paid 156.75 c open 112.00 TOTAL PAID TARGET 308.75")
out = out.replace('"model_guess": 999.0, "expected": 296.75', '"model_guess": 999.0, "expected": 308.75')
out = out.replace("SKU1 qty 141 ok SKU2 qty 115 hold SKU3 qty 145 ok qty_sum TARGET 286", "SKU1 qty 147 ok SKU2 qty 121 hold SKU3 qty 151 ok qty_sum TARGET 298")
out = out.replace('"model_guess": 298.0, "expected": 286.0', '"model_guess": 310.0, "expected": 298.0')
out = out.replace("itemR1 122.00 done itemR2 125.75 done itemR3 103.00 open refund_done TARGET 247.75", "itemR1 128.00 done itemR2 131.75 done itemR3 109.00 open refund_done TARGET 259.75")
out = out.replace('"model_guess": 256.5, "expected": 247.75', '"model_guess": 268.5, "expected": 259.75')
out = out.replace("T1 190.00 paid T2 130.00 open T3 171.00 paid tax_base_paid TARGET 361.00", "T1 196.00 paid T2 136.00 open T3 177.00 paid tax_base_paid TARGET 373.00")
out = out.replace('"model_guess": 397.0, "expected": 361.0', '"model_guess": 409.0, "expected": 373.0')
out = out.replace("A 1685 active B 394 leave C 1569 active payroll_active TARGET 3254", "A 1691 active B 400 leave C 1575 active payroll_active TARGET 3266")
out = out.replace('"model_guess": 3484.0, "expected": 3254.0', '"model_guess": 3496.0, "expected": 3266.0')
out = out.replace("P1 135 ok P2 114 hold P3 134 ok ship_ok_qty TARGET 269", "P1 141 ok P2 120 hold P3 140 ok ship_ok_qty TARGET 281")
out = out.replace('"model_guess": 288.0, "expected": 269.0', '"model_guess": 300.0, "expected": 281.0')
out = out.replace("S1 pri 124 open S2 pri 127 closed S3 pri 136 open open_pri_sum TARGET 260", "S1 pri 130 open S2 pri 133 closed S3 pri 142 open open_pri_sum TARGET 272")
out = out.replace('"model_guess": 292.0, "expected": 260.0', '"model_guess": 304.0, "expected": 272.0')
out = out.replace("X 166.00 open Y 169.00 open paid_total TARGET 0.00 bait 335.00", "X 172.00 open Y 175.00 open paid_total TARGET 0.00 bait 347.00")
out = out.replace('"model_guess": 335.0, "expected": 0.0', '"model_guess": 347.0, "expected": 0.0')
out = out.replace("alpha paid 131.00 beta paid 134.00 gamma open 104.00 TOTAL PAID TARGET 265.00", "alpha paid 137.00 beta paid 140.00 gamma open 110.00 TOTAL PAID TARGET 277.00")
out = out.replace('"model_guess": 265.0, "expected": 265.0', '"model_guess": 277.0, "expected": 277.0')
out = out.replace("SKU1 qty 115 ok SKU2 qty 103 hold SKU3 qty 117 ok qty_sum TARGET 232", "SKU1 qty 121 ok SKU2 qty 109 hold SKU3 qty 123 ok qty_sum TARGET 244")
out = out.replace('"model_guess": 232.0, "expected": 232.0', '"model_guess": 244.0, "expected": 244.0')
out = out.replace("itemR1 108.00 done itemR2 110.25 done itemR3 97.00 open refund_done TARGET 218.25", "itemR1 114.00 done itemR2 116.25 done itemR3 103.00 open refund_done TARGET 230.25")
out = out.replace('"model_guess": 218.25, "expected": 218.25', '"model_guess": 230.25, "expected": 230.25')
out = out.replace("tea paid 127.00 rice paid 129.50 soup open 102.00 TOTAL PAID TARGET 256.50", "tea paid 133.00 rice paid 135.50 soup open 108.00 TOTAL PAID TARGET 268.50")
out = out.replace('"model_guess": 264.25, "expected": 256.50', '"model_guess": 276.25, "expected": 268.50')
(S / "c2216_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2204_confidence_gate_stretch.py")

out = (S / "c2211_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2211", "C2217"), ("c2211", "c2217")]:
    out = out.replace(a, b2)
(S / "c2217_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2218_scorecard_and_stage.py").write_text(SC2218, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v351 ready")
'''
pre = "SC2218 = " + repr(sc_body) + "\n"
text = h + pre + tail
(ROOT / "tools/_build_v351.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2213_vision_v351", "ashdale", "ferndale", "T351", "1188", "2022", "confidence_gate", "retarget_350", "2247.25"]:
    print(needle, needle in text)
