from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v352.py").read_text(encoding="utf-8")
idx0 = b0.find("# V352 knife = product-U2C")
if idx0 < 0:
    raise SystemExit("knife not found")
head0 = b0[:idx0]
if "SC2224 = " in head0:
    head0 = head0[:head0.find("SC2224 = ")]
theme_pairs = [
    ("netherford", "netherhurst"), ("NETHERFORD", "NETHERHURST"),
    ("cedarford", "cedarhurst"), ("CEDARFORD", "CEDARHURST"),
    ("dawnford", "dawnhurst"), ("DAWNFORD", "DAWNHURST"),
    ("fernford", "fernhurst"), ("FERNFORD", "FERNHURST"),
    ("glenford", "glenhurst"), ("GLENFORD", "GLENHURST"),
    ("hazeford", "hazehurst"), ("HAZEFORD", "HAZEHURST"),
    ("jadeford", "jadehurst"), ("JADEFORD", "JADEHURST"),
    ("knotford", "knothurst"), ("KNOTFORD", "KNOTHURST"),
    ("lakeford", "lakehurst"), ("LAKEFORD", "LAKEHURST"),
    ("mossford", "mosshurst"), ("MOSSFORD", "MOSSHURST"),
    ("pineford", "pinehurst"), ("PINEFORD", "PINEHURST"),
    ("quillford", "quillhurst"), ("QUILLFORD", "QUILLHURST"),
    ("reedford", "reedhurst"), ("REEDFORD", "REEDHURST"),
    ("stoneford", "stonehurst"), ("STONEFORD", "STONEHURST"),
    ("ashford", "ashhurst"), ("ASHFORD", "ASHHURST"),
    ("elmford", "elmhurst"), ("ELMFORD", "ELMHURST"),
    ("inkford", "inkhurst"), ("INKFORD", "INKHURST"),
    ("oakford", "oakhurst"), ("OAKFORD", "OAKHURST"),
]
pairs = [
    ("*ford ; stack mid-band", "*hurst ; stack mid-band"),
    ("T352", "T353"), ("TR352", "TR353"), ("HO352", "HO353"),
    ("NEW352", "NEW353"),
    ("V352", "V353"), ("v352", "v353"),
    ("_v352_themes.json", "_v353_themes.json"),
    ("_v351_themes.json", "_v352_themes.json"),
    ("OLD351", "OLD352"),
    ("vision_images_v352", "vision_images_v353"),
    ("VL_GATE_V352", "VL_GATE_V353"), ("vl_gate_v352", "vl_gate_v353"),
    ("C2219", "C2225"), ("c2219", "c2225"),
    ("C2220", "C2226"), ("c2220", "c2226"),
    ("C2221", "C2227"), ("c2221", "c2227"),
    ("_v352c2219", "_v353c2225"),
    ("Harder than V350", "Harder than V351"),
    ("harder than V350", "harder than V351"),
    ("NEW themes vs V350:", "NEW themes vs V351:"),
    ("kept on V352", "kept on V353"),
    ("V352 keeps floor", "V353 keeps floor"),
    ("C2219 design+fixtures; no VL claim", "C2225 design+fixtures; no VL claim"),
    ("retarget_351", "retarget_352"),
    ("*ford", "*hurst"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)
h = h.replace("ASHFORD bait 253.63", "ASHHURST bait 254.64")
h = h.replace("CEDARF bait 267.77", "CEDARH bait 268.78")
h = h.replace("DAWNF ghost 190.01", "DAWNH ghost 191.02")
h = h.replace("GLENF bait 260.70", "GLENH bait 261.71")
h = h.replace("JADEF bait 251.61", "JADEH bait 252.62")
h = h.replace("NETHERF bait 268.78", "NETHERH bait 269.79")
TR = """TR353 = [
    [2370.0, 2387.5, 2110.0],[840, 760, 820],[2244.0, 2245.25, 2050.0],[2426.0, 2443.0, 2178.0],
    [2488.0, 2491.0, 2148.0],[2206, 2222, 2106],[490.0, 530.0, 760.0],[2336.0, 2367.75, 2112.0],
    [840.0, 760.0, 820.0],[2403.0, 2391.0, 2109.0],[1,1,0],[0,0,0],
    [2461.0, 2480.5, 2112.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO353 = [
    [2168.0, 2180.75, 2029.0],[640, 660, 820],[2111.0, 2125.5, 2004.0],[2241.0, 2257.0, 2060.0],
    [2245.0, 2256.0, 2053.0],[2064, 2076, 2026],[420.0, 460.0, 740.0],[2152.0, 2173.75, 2029.0],
    [740.0, 780.0, 820.0],[2199.0, 2185.0, 2026.0],[1,1,0],[0,0,0],
    [2229.0, 2243.5, 2033.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
h = re.sub(r"TR353\s*=\s*\[[\s\S]*?\n\]", TR, h, count=1)
h = re.sub(r"HO353\s*=\s*\[[\s\S]*?\n\]", HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2230"), ("c2098", "c2230"),
    ("C2096", "C2228"), ("c2096", "c2228"),
    ("C2097", "C2229"), ("c2097", "c2229"),
    ("C2094", "C2226"), ("c2094", "c2226"),
    ("C2095", "C2227"), ("c2095", "c2227"),
    ("C2093", "C2225"), ("c2093", "c2225"),
    ("C2090", "C2222"), ("c2090", "c2222"),
    ("V331", "V353"), ("v331", "v353"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2230"),
    ("*vale", "*hurst"),
]:
    sc_body = sc_body.replace(a, b2)
tail = r'''# V353 knife = confidence-gate (alternating; V352 was product-U2C)
out = (S / "c2216_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2216", "C2228"), ("c2216", "c2228"),
    ("C2096", "C2228"), ("c2096", "c2228"),
    ("cg135_", "cg130_"),
    ("conf_gate_stretch_c2228", "conf_gate_stretch_c2228"),
    ("confidence_gate_stretch_v198", "confidence_gate_stretch_v193"),
    ("Stretch vs C2126", "Stretch vs C2132"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 152.00 b paid 156.75 c open 112.00 TOTAL PAID TARGET 308.75", "a paid 158.00 b paid 162.75 c open 118.00 TOTAL PAID TARGET 320.75")
out = out.replace('"model_guess": 999.0, "expected": 308.75', '"model_guess": 999.0, "expected": 320.75')
out = out.replace("SKU1 qty 147 ok SKU2 qty 121 hold SKU3 qty 151 ok qty_sum TARGET 298", "SKU1 qty 153 ok SKU2 qty 127 hold SKU3 qty 157 ok qty_sum TARGET 310")
out = out.replace('"model_guess": 310.0, "expected": 298.0', '"model_guess": 322.0, "expected": 310.0')
out = out.replace("itemR1 128.00 done itemR2 131.75 done itemR3 109.00 open refund_done TARGET 259.75", "itemR1 134.00 done itemR2 137.75 done itemR3 115.00 open refund_done TARGET 271.75")
out = out.replace('"model_guess": 268.5, "expected": 259.75', '"model_guess": 280.5, "expected": 271.75')
out = out.replace("T1 196.00 paid T2 136.00 open T3 177.00 paid tax_base_paid TARGET 373.00", "T1 202.00 paid T2 142.00 open T3 183.00 paid tax_base_paid TARGET 385.00")
out = out.replace('"model_guess": 409.0, "expected": 373.0', '"model_guess": 421.0, "expected": 385.0')
out = out.replace("A 1691 active B 400 leave C 1575 active payroll_active TARGET 3266", "A 1697 active B 406 leave C 1581 active payroll_active TARGET 3278")
out = out.replace('"model_guess": 3496.0, "expected": 3266.0', '"model_guess": 3508.0, "expected": 3278.0')
out = out.replace("P1 141 ok P2 120 hold P3 140 ok ship_ok_qty TARGET 281", "P1 147 ok P2 126 hold P3 146 ok ship_ok_qty TARGET 293")
out = out.replace('"model_guess": 300.0, "expected": 281.0', '"model_guess": 312.0, "expected": 293.0')
out = out.replace("S1 pri 130 open S2 pri 133 closed S3 pri 142 open open_pri_sum TARGET 272", "S1 pri 136 open S2 pri 139 closed S3 pri 148 open open_pri_sum TARGET 284")
out = out.replace('"model_guess": 304.0, "expected": 272.0', '"model_guess": 316.0, "expected": 284.0')
out = out.replace("X 172.00 open Y 175.00 open paid_total TARGET 0.00 bait 347.00", "X 178.00 open Y 181.00 open paid_total TARGET 0.00 bait 359.00")
out = out.replace('"model_guess": 347.0, "expected": 0.0', '"model_guess": 359.0, "expected": 0.0')
out = out.replace("alpha paid 137.00 beta paid 140.00 gamma open 110.00 TOTAL PAID TARGET 277.00", "alpha paid 143.00 beta paid 146.00 gamma open 116.00 TOTAL PAID TARGET 289.00")
out = out.replace('"model_guess": 277.0, "expected": 277.0', '"model_guess": 289.0, "expected": 289.0')
out = out.replace("SKU1 qty 121 ok SKU2 qty 109 hold SKU3 qty 123 ok qty_sum TARGET 244", "SKU1 qty 127 ok SKU2 qty 115 hold SKU3 qty 129 ok qty_sum TARGET 256")
out = out.replace('"model_guess": 244.0, "expected": 244.0', '"model_guess": 256.0, "expected": 256.0')
out = out.replace("itemR1 114.00 done itemR2 116.25 done itemR3 103.00 open refund_done TARGET 230.25", "itemR1 120.00 done itemR2 122.25 done itemR3 109.00 open refund_done TARGET 242.25")
out = out.replace('"model_guess": 230.25, "expected": 230.25', '"model_guess": 242.25, "expected": 242.25')
out = out.replace("tea paid 133.00 rice paid 135.50 soup open 108.00 TOTAL PAID TARGET 268.50", "tea paid 139.00 rice paid 141.50 soup open 114.00 TOTAL PAID TARGET 280.50")
out = out.replace('"model_guess": 276.25, "expected": 268.50', '"model_guess": 288.25, "expected": 280.50')
(S / "c2228_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2216_confidence_gate_stretch.py")

out = (S / "c2223_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2223", "C2229"), ("c2223", "c2229")]:
    out = out.replace(a, b2)
(S / "c2229_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2230_scorecard_and_stage.py").write_text(SC2230, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v353 ready")
'''
pre = "SC2230 = " + repr(sc_body) + "\n"
text = h + pre + tail
(ROOT / "tools/_build_v353.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2225_vision_v353", "ashhurst", "fernhurst", "T353", "1188", "2026", "confidence_gate", "retarget_352", "2245.25"]:
    print(needle, needle in text)
