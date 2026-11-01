from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v358.py").read_text(encoding="utf-8")
idx0 = b0.find("# V358 knife = product-U2C")
if idx0 < 0:
    raise SystemExit("knife not found")
head0 = b0[:idx0]
if "SC2260 = " in head0:
    head0 = head0[:head0.find("SC2260 = ")]
theme_pairs = [
    ("netherwick", "nethermoor"), ("NETHERWICK", "NETHERMOOR"),
    ("cedarwick", "cedarmoor"), ("CEDARWICK", "CEDARMOOR"),
    ("dawnwick", "dawnmoor"), ("DAWNWICK", "DAWNMOOR"),
    ("fernwick", "fernmoor"), ("FERNWICK", "FERNMOOR"),
    ("glenwick", "glenmoor"), ("GLENWICK", "GLENMOOR"),
    ("hazewick", "hazemoor"), ("HAZEWICK", "HAZEMOOR"),
    ("jadewick", "jademoor"), ("JADEWICK", "JADEMOOR"),
    ("knotwick", "knotmoor"), ("KNOTWICK", "KNOTMOOR"),
    ("lakewick", "lakemoor"), ("LAKEWICK", "LAKEMOOR"),
    ("mosswick", "mossmoor"), ("MOSSWICK", "MOSSMOOR"),
    ("pinewick", "pinemoor"), ("PINEWICK", "PINEMOOR"),
    ("quillwick", "quillmoor"), ("QUILLWICK", "QUILLMOOR"),
    ("reedwick", "reedmoor"), ("REEDWICK", "REEDMOOR"),
    ("stonewick", "stonemoor"), ("STONEWICK", "STONEMOOR"),
    ("ashwick", "ashmoor"), ("ASHWICK", "ASHMOOR"),
    ("elmwick", "elmmoor"), ("ELMWICK", "ELMMOOR"),
    ("inkwick", "inkmoor"), ("INKWICK", "INKMOOR"),
    ("oakwick", "oakmoor"), ("OAKWICK", "OAKMOOR"),
]
pairs = [
    ("*wick ; stack mid-band", "*moor ; stack mid-band"),
    ("T358", "T359"), ("TR358", "TR359"), ("HO358", "HO359"),
    ("NEW358", "NEW359"),
    ("V358", "V359"), ("v358", "v359"),
    ("_v358_themes.json", "_v359_themes.json"),
    ("_v357_themes.json", "_v358_themes.json"),
    ("OLD357", "OLD358"),
    ("vision_images_v358", "vision_images_v359"),
    ("VL_GATE_V358", "VL_GATE_V359"), ("vl_gate_v358", "vl_gate_v359"),
    ("C2255", "C2261"), ("c2255", "c2261"),
    ("C2256", "C2262"), ("c2256", "c2262"),
    ("C2257", "C2263"), ("c2257", "c2263"),
    ("_v358c2255", "_v359c2261"),
    ("Harder than V356", "Harder than V357"),
    ("harder than V356", "harder than V357"),
    ("NEW themes vs V356:", "NEW themes vs V357:"),
    ("kept on V358", "kept on V359"),
    ("V358 keeps floor", "V359 keeps floor"),
    ("C2255 design+fixtures; no VL claim", "C2261 design+fixtures; no VL claim"),
    ("retarget_357", "retarget_358"),
    ("*wick", "*moor"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)
h = h.replace("ASHWICK bait 259.69", "ASHMOOR bait 260.70")
h = h.replace("CEDARW bait 273.83", "CEDARM bait 274.84")
h = h.replace("DAWNW ghost 196.07", "DAWNM ghost 197.08")
h = h.replace("GLENW bait 266.76", "GLENM bait 267.77")
h = h.replace("JADEW bait 257.67", "JADEM bait 258.68")
h = h.replace("NETHERW bait 274.84", "NETHERM bait 275.85")
TR = """TR359 = [
    [2382.0, 2399.5, 2122.0],[840, 760, 820],[2245.0, 2247.25, 2044.0],[2438.0, 2455.0, 2190.0],
    [2499.0, 2495.0, 2160.0],[2218, 2234, 2118],[490.0, 530.0, 760.0],[2348.0, 2379.75, 2124.0],
    [840.0, 760.0, 820.0],[2415.0, 2403.0, 2121.0],[1,1,0],[0,0,0],
    [2459.0, 2478.5, 2100.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO359 = [
    [2180.0, 2192.75, 2041.0],[640, 660, 820],[2123.0, 2137.5, 2016.0],[2253.0, 2269.0, 2072.0],
    [2257.0, 2268.0, 2065.0],[2076, 2088, 2038],[420.0, 460.0, 740.0],[2164.0, 2185.75, 2041.0],
    [740.0, 780.0, 820.0],[2211.0, 2197.0, 2038.0],[1,1,0],[0,0,0],
    [2241.0, 2255.5, 2045.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
h = re.sub(r"TR359\s*=\s*\[[\s\S]*?\n\]", TR, h, count=1)
h = re.sub(r"HO359\s*=\s*\[[\s\S]*?\n\]", HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2266"), ("c2098", "c2266"),
    ("C2096", "C2264"), ("c2096", "c2264"),
    ("C2097", "C2265"), ("c2097", "c2265"),
    ("C2094", "C2262"), ("c2094", "c2262"),
    ("C2095", "C2263"), ("c2095", "c2263"),
    ("C2093", "C2261"), ("c2093", "c2261"),
    ("C2090", "C2258"), ("c2090", "c2258"),
    ("V331", "V359"), ("v331", "v359"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2266"),
    ("*vale", "*moor"),
]:
    sc_body = sc_body.replace(a, b2)
tail = r'''# V359 knife = confidence-gate (alternating; V358 was product-U2C)
out = (S / "c2252_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2252", "C2264"), ("c2252", "c2264"),
    ("C2096", "C2264"), ("c2096", "c2264"),
    ("cg120_", "cg115_"),
    ("conf_gate_stretch_c2264", "conf_gate_stretch_c2264"),
    ("confidence_gate_stretch_v183", "confidence_gate_stretch_v178"),
    ("Stretch vs C2144", "Stretch vs C2150"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 170.00 b paid 174.75 c open 130.00 TOTAL PAID TARGET 344.75", "a paid 176.00 b paid 180.75 c open 136.00 TOTAL PAID TARGET 356.75")
out = out.replace('"model_guess": 999.0, "expected": 344.75', '"model_guess": 999.0, "expected": 356.75')
out = out.replace("SKU1 qty 165 ok SKU2 qty 139 hold SKU3 qty 169 ok qty_sum TARGET 334", "SKU1 qty 171 ok SKU2 qty 145 hold SKU3 qty 175 ok qty_sum TARGET 346")
out = out.replace('"model_guess": 346.0, "expected": 334.0', '"model_guess": 358.0, "expected": 346.0')
out = out.replace("itemR1 146.00 done itemR2 149.75 done itemR3 127.00 open refund_done TARGET 295.75", "itemR1 152.00 done itemR2 155.75 done itemR3 133.00 open refund_done TARGET 307.75")
out = out.replace('"model_guess": 304.5, "expected": 295.75', '"model_guess": 316.5, "expected": 307.75')
out = out.replace("T1 214.00 paid T2 154.00 open T3 195.00 paid tax_base_paid TARGET 409.00", "T1 220.00 paid T2 160.00 open T3 201.00 paid tax_base_paid TARGET 421.00")
out = out.replace('"model_guess": 445.0, "expected": 409.0', '"model_guess": 457.0, "expected": 421.0')
out = out.replace("A 1709 active B 418 leave C 1593 active payroll_active TARGET 3302", "A 1715 active B 424 leave C 1599 active payroll_active TARGET 3314")
out = out.replace('"model_guess": 3532.0, "expected": 3302.0', '"model_guess": 3544.0, "expected": 3314.0')
out = out.replace("P1 159 ok P2 138 hold P3 158 ok ship_ok_qty TARGET 317", "P1 165 ok P2 144 hold P3 164 ok ship_ok_qty TARGET 329")
out = out.replace('"model_guess": 336.0, "expected": 317.0', '"model_guess": 348.0, "expected": 329.0')
out = out.replace("S1 pri 148 open S2 pri 151 closed S3 pri 160 open open_pri_sum TARGET 308", "S1 pri 154 open S2 pri 157 closed S3 pri 166 open open_pri_sum TARGET 320")
out = out.replace('"model_guess": 340.0, "expected": 308.0', '"model_guess": 352.0, "expected": 320.0')
out = out.replace("X 190.00 open Y 193.00 open paid_total TARGET 0.00 bait 383.00", "X 196.00 open Y 199.00 open paid_total TARGET 0.00 bait 395.00")
out = out.replace('"model_guess": 383.0, "expected": 0.0', '"model_guess": 395.0, "expected": 0.0')
out = out.replace("alpha paid 155.00 beta paid 158.00 gamma open 128.00 TOTAL PAID TARGET 313.00", "alpha paid 161.00 beta paid 164.00 gamma open 134.00 TOTAL PAID TARGET 325.00")
out = out.replace('"model_guess": 313.0, "expected": 313.0', '"model_guess": 325.0, "expected": 325.0')
out = out.replace("SKU1 qty 139 ok SKU2 qty 127 hold SKU3 qty 141 ok qty_sum TARGET 280", "SKU1 qty 145 ok SKU2 qty 133 hold SKU3 qty 147 ok qty_sum TARGET 292")
out = out.replace('"model_guess": 280.0, "expected": 280.0', '"model_guess": 292.0, "expected": 292.0')
out = out.replace("itemR1 132.00 done itemR2 134.25 done itemR3 121.00 open refund_done TARGET 266.25", "itemR1 138.00 done itemR2 140.25 done itemR3 127.00 open refund_done TARGET 278.25")
out = out.replace('"model_guess": 266.25, "expected": 266.25', '"model_guess": 278.25, "expected": 278.25')
out = out.replace("tea paid 151.00 rice paid 153.50 soup open 126.00 TOTAL PAID TARGET 304.50", "tea paid 157.00 rice paid 159.50 soup open 132.00 TOTAL PAID TARGET 316.50")
out = out.replace('"model_guess": 312.25, "expected": 304.50', '"model_guess": 324.25, "expected": 316.50')
(S / "c2264_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2252_confidence_gate_stretch.py")

out = (S / "c2259_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2259", "C2265"), ("c2259", "c2265")]:
    out = out.replace(a, b2)
(S / "c2265_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2266_scorecard_and_stage.py").write_text(SC2266, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v359 ready")
'''
pre = "SC2266 = " + repr(sc_body) + "\n"
text = h + pre + tail
(ROOT / "tools/_build_v359.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2261_vision_v359", "ashmoor", "fernmoor", "T359", "1188", "2038", "confidence_gate", "retarget_358", "2247.25"]:
    print(needle, needle in text)
