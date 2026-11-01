from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v360.py").read_text(encoding="utf-8")
idx0 = b0.find("# V360 knife = product-U2C")
if idx0 < 0:
    raise SystemExit("knife not found")
head0 = b0[:idx0]
if "SC2272 = " in head0:
    head0 = head0[:head0.find("SC2272 = ")]
theme_pairs = [
    ("netherfen", "netherbrook"), ("NETHERFEN", "NETHERBROOK"),
    ("cedarfen", "cedarbrook"), ("CEDARFEN", "CEDARBROOK"),
    ("dawnfen", "dawnbrook"), ("DAWNFEN", "DAWNBROOK"),
    ("fernfen", "fernbrook"), ("FERNFEN", "FERNBROOK"),
    ("glenfen", "glenbrook"), ("GLENFEN", "GLENBROOK"),
    ("hazefen", "hazebrook"), ("HAZEFEN", "HAZEBROOK"),
    ("jadefen", "jadebrook"), ("JADEFEN", "JADEBROOK"),
    ("knotfen", "knotbrook"), ("KNOTFEN", "KNOTBROOK"),
    ("lakefen", "lakebrook"), ("LAKEFEN", "LAKEBROOK"),
    ("mossfen", "mossbrook"), ("MOSSFEN", "MOSSBROOK"),
    ("pinefen", "pinebrook"), ("PINEFEN", "PINEBROOK"),
    ("quillfen", "quillbrook"), ("QUILLFEN", "QUILLBROOK"),
    ("reedfen", "reedbrook"), ("REEDFEN", "REEDBROOK"),
    ("stonefen", "stonebrook"), ("STONEFEN", "STONEBROOK"),
    ("ashfen", "ashbrook"), ("ASHFEN", "ASHBROOK"),
    ("elmfen", "elmbrook"), ("ELMFEN", "ELMBROOK"),
    ("inkfen", "inkbrook"), ("INKFEN", "INKBROOK"),
    ("oakfen", "oakbrook"), ("OAKFEN", "OAKBROOK"),
]
pairs = [
    ("*fen ; stack mid-band", "*brook ; stack mid-band"),
    ("T360", "T361"), ("TR360", "TR361"), ("HO360", "HO361"),
    ("NEW360", "NEW361"),
    ("V360", "V361"), ("v360", "v361"),
    ("_v360_themes.json", "_v361_themes.json"),
    ("_v359_themes.json", "_v360_themes.json"),
    ("OLD359", "OLD360"),
    ("vision_images_v360", "vision_images_v361"),
    ("VL_GATE_V360", "VL_GATE_V361"), ("vl_gate_v360", "vl_gate_v361"),
    ("C2267", "C2273"), ("c2267", "c2273"),
    ("C2268", "C2274"), ("c2268", "c2274"),
    ("C2269", "C2275"), ("c2269", "c2275"),
    ("_v360c2267", "_v361c2273"),
    ("Harder than V358", "Harder than V359"),
    ("harder than V358", "harder than V359"),
    ("NEW themes vs V358:", "NEW themes vs V359:"),
    ("kept on V360", "kept on V361"),
    ("V360 keeps floor", "V361 keeps floor"),
    ("C2267 design+fixtures; no VL claim", "C2273 design+fixtures; no VL claim"),
    ("retarget_359", "retarget_360"),
    ("*fen", "*brook"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)
h = h.replace("ASHFEN bait 261.71", "ASHBROOK bait 262.72")
h = h.replace("CEDARF bait 275.85", "CEDARB bait 276.86")
h = h.replace("DAWNF ghost 198.09", "DAWNB ghost 199.10")
h = h.replace("GLENF bait 268.78", "GLENB bait 269.79")
h = h.replace("JADEF bait 259.69", "JADEB bait 260.70")
h = h.replace("NETHERF bait 276.86", "NETHERB bait 277.87")
TR = """TR361 = [
    [2386.0, 2403.5, 2126.0],[840, 760, 820],[2243.0, 2245.25, 2042.0],[2442.0, 2459.0, 2194.0],
    [2495.0, 2491.0, 2164.0],[2222, 2238, 2122],[490.0, 530.0, 760.0],[2352.0, 2383.75, 2128.0],
    [840.0, 760.0, 820.0],[2419.0, 2407.0, 2125.0],[1,1,0],[0,0,0],
    [2453.0, 2472.5, 2096.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO361 = [
    [2184.0, 2196.75, 2045.0],[640, 660, 820],[2127.0, 2141.5, 2020.0],[2257.0, 2273.0, 2076.0],
    [2261.0, 2272.0, 2069.0],[2080, 2092, 2042],[420.0, 460.0, 740.0],[2168.0, 2189.75, 2045.0],
    [740.0, 780.0, 820.0],[2215.0, 2201.0, 2042.0],[1,1,0],[0,0,0],
    [2245.0, 2259.5, 2049.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
h = re.sub(r"TR361\s*=\s*\[[\s\S]*?\n\]", TR, h, count=1)
h = re.sub(r"HO361\s*=\s*\[[\s\S]*?\n\]", HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2278"), ("c2098", "c2278"),
    ("C2096", "C2276"), ("c2096", "c2276"),
    ("C2097", "C2277"), ("c2097", "c2277"),
    ("C2094", "C2274"), ("c2094", "c2274"),
    ("C2095", "C2275"), ("c2095", "c2275"),
    ("C2093", "C2273"), ("c2093", "c2273"),
    ("C2090", "C2270"), ("c2090", "c2270"),
    ("V331", "V361"), ("v331", "v361"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2278"),
    ("*vale", "*brook"),
]:
    sc_body = sc_body.replace(a, b2)
tail = r'''# V361 knife = confidence-gate (alternating; V360 was product-U2C)
out = (S / "c2264_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2264", "C2276"), ("c2264", "c2276"),
    ("C2096", "C2276"), ("c2096", "c2276"),
    ("cg115_", "cg110_"),
    ("conf_gate_stretch_c2276", "conf_gate_stretch_c2276"),
    ("confidence_gate_stretch_v178", "confidence_gate_stretch_v173"),
    ("Stretch vs C2150", "Stretch vs C2156"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 176.00 b paid 180.75 c open 136.00 TOTAL PAID TARGET 356.75", "a paid 182.00 b paid 186.75 c open 142.00 TOTAL PAID TARGET 368.75")
out = out.replace('"model_guess": 999.0, "expected": 356.75', '"model_guess": 999.0, "expected": 368.75')
out = out.replace("SKU1 qty 171 ok SKU2 qty 145 hold SKU3 qty 175 ok qty_sum TARGET 346", "SKU1 qty 177 ok SKU2 qty 151 hold SKU3 qty 181 ok qty_sum TARGET 358")
out = out.replace('"model_guess": 358.0, "expected": 346.0', '"model_guess": 370.0, "expected": 358.0')
out = out.replace("itemR1 152.00 done itemR2 155.75 done itemR3 133.00 open refund_done TARGET 307.75", "itemR1 158.00 done itemR2 161.75 done itemR3 139.00 open refund_done TARGET 319.75")
out = out.replace('"model_guess": 316.5, "expected": 307.75', '"model_guess": 328.5, "expected": 319.75')
out = out.replace("T1 220.00 paid T2 160.00 open T3 201.00 paid tax_base_paid TARGET 421.00", "T1 226.00 paid T2 166.00 open T3 207.00 paid tax_base_paid TARGET 433.00")
out = out.replace('"model_guess": 457.0, "expected": 421.0', '"model_guess": 469.0, "expected": 433.0')
out = out.replace("A 1715 active B 424 leave C 1599 active payroll_active TARGET 3314", "A 1721 active B 430 leave C 1605 active payroll_active TARGET 3326")
out = out.replace('"model_guess": 3544.0, "expected": 3314.0', '"model_guess": 3556.0, "expected": 3326.0')
out = out.replace("P1 165 ok P2 144 hold P3 164 ok ship_ok_qty TARGET 329", "P1 171 ok P2 150 hold P3 170 ok ship_ok_qty TARGET 341")
out = out.replace('"model_guess": 348.0, "expected": 329.0', '"model_guess": 360.0, "expected": 341.0')
out = out.replace("S1 pri 154 open S2 pri 157 closed S3 pri 166 open open_pri_sum TARGET 320", "S1 pri 160 open S2 pri 163 closed S3 pri 172 open open_pri_sum TARGET 332")
out = out.replace('"model_guess": 352.0, "expected": 320.0', '"model_guess": 364.0, "expected": 332.0')
out = out.replace("X 196.00 open Y 199.00 open paid_total TARGET 0.00 bait 395.00", "X 202.00 open Y 205.00 open paid_total TARGET 0.00 bait 407.00")
out = out.replace('"model_guess": 395.0, "expected": 0.0', '"model_guess": 407.0, "expected": 0.0')
out = out.replace("alpha paid 161.00 beta paid 164.00 gamma open 134.00 TOTAL PAID TARGET 325.00", "alpha paid 167.00 beta paid 170.00 gamma open 140.00 TOTAL PAID TARGET 337.00")
out = out.replace('"model_guess": 325.0, "expected": 325.0', '"model_guess": 337.0, "expected": 337.0')
out = out.replace("SKU1 qty 145 ok SKU2 qty 133 hold SKU3 qty 147 ok qty_sum TARGET 292", "SKU1 qty 151 ok SKU2 qty 139 hold SKU3 qty 153 ok qty_sum TARGET 304")
out = out.replace('"model_guess": 292.0, "expected": 292.0', '"model_guess": 304.0, "expected": 304.0')
out = out.replace("itemR1 138.00 done itemR2 140.25 done itemR3 127.00 open refund_done TARGET 278.25", "itemR1 144.00 done itemR2 146.25 done itemR3 133.00 open refund_done TARGET 290.25")
out = out.replace('"model_guess": 278.25, "expected": 278.25', '"model_guess": 290.25, "expected": 290.25')
out = out.replace("tea paid 157.00 rice paid 159.50 soup open 132.00 TOTAL PAID TARGET 316.50", "tea paid 163.00 rice paid 165.50 soup open 138.00 TOTAL PAID TARGET 328.50")
out = out.replace('"model_guess": 324.25, "expected": 316.50', '"model_guess": 336.25, "expected": 328.50')
(S / "c2276_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2264_confidence_gate_stretch.py")

out = (S / "c2271_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2271", "C2277"), ("c2271", "c2277")]:
    out = out.replace(a, b2)
(S / "c2277_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2278_scorecard_and_stage.py").write_text(SC2278, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v361 ready")
'''
pre = "SC2278 = " + repr(sc_body) + "\n"
text = h + pre + tail
(ROOT / "tools/_build_v361.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2273_vision_v361", "ashbrook", "fernbrook", "T361", "1188", "2042", "confidence_gate", "retarget_360", "2245.25"]:
    print(needle, needle in text)
