from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v354.py").read_text(encoding="utf-8")
idx0 = b0.find("# V354 knife = product-U2C")
if idx0 < 0:
    raise SystemExit("knife not found")
head0 = b0[:idx0]
if "SC2236 = " in head0:
    head0 = head0[:head0.find("SC2236 = ")]
theme_pairs = [
    ("nethermere", "nethervale"), ("NETHERMERE", "NETHERVALE"),
    ("cedarmere", "cedarvale"), ("CEDARMERE", "CEDARVALE"),
    ("dawnmere", "dawnvale"), ("DAWNMERE", "DAWNVALE"),
    ("fernmere", "fernvale"), ("FERNMERE", "FERNVALE"),
    ("glenmere", "glenvale"), ("GLENMERE", "GLENVALE"),
    ("hazemere", "hazevale"), ("HAZEMERE", "HAZEVALE"),
    ("jademere", "jadevale"), ("JADEMERE", "JADEVALE"),
    ("knotmere", "knotvale"), ("KNOTMERE", "KNOTVALE"),
    ("lakemere", "lakevale"), ("LAKEMERE", "LAKEVALE"),
    ("mossmere", "mossvale"), ("MOSSMERE", "MOSSVALE"),
    ("pinemere", "pinevale"), ("PINEMERE", "PINEVALE"),
    ("quillmere", "quillvale"), ("QUILLMERE", "QUILLVALE"),
    ("reedmere", "reedvale"), ("REEDMERE", "REEDVALE"),
    ("stonemere", "stonevale"), ("STONEMERE", "STONEVALE"),
    ("ashmere", "ashvale"), ("ASHMERE", "ASHVALE"),
    ("elmmere", "elmvale"), ("ELMMERE", "ELMVALE"),
    ("inkmere", "inkvale"), ("INKMERE", "INKVALE"),
    ("oakmere", "oakvale"), ("OAKMERE", "OAKVALE"),
]
pairs = [
    ("*mere ; stack mid-band", "*vale ; stack mid-band"),
    ("T354", "T355"), ("TR354", "TR355"), ("HO354", "HO355"),
    ("NEW354", "NEW355"),
    ("V354", "V355"), ("v354", "v355"),
    ("_v354_themes.json", "_v355_themes.json"),
    ("_v353_themes.json", "_v354_themes.json"),
    ("OLD353", "OLD354"),
    ("vision_images_v354", "vision_images_v355"),
    ("VL_GATE_V354", "VL_GATE_V355"), ("vl_gate_v354", "vl_gate_v355"),
    ("C2231", "C2237"), ("c2231", "c2237"),
    ("C2232", "C2238"), ("c2232", "c2238"),
    ("C2233", "C2239"), ("c2233", "c2239"),
    ("_v354c2231", "_v355c2237"),
    ("Harder than V352", "Harder than V353"),
    ("harder than V352", "harder than V353"),
    ("NEW themes vs V352:", "NEW themes vs V353:"),
    ("kept on V354", "kept on V355"),
    ("V354 keeps floor", "V355 keeps floor"),
    ("C2231 design+fixtures; no VL claim", "C2237 design+fixtures; no VL claim"),
    ("retarget_353", "retarget_354"),
    ("*mere", "*vale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)
h = h.replace("ASHMERE bait 255.65", "ASHVALE bait 256.66")
h = h.replace("CEDARM bait 269.79", "CEDARV bait 270.80")
h = h.replace("DAWNM ghost 192.03", "DAWNV ghost 193.04")
h = h.replace("GLENM bait 262.72", "GLENV bait 263.73")
h = h.replace("JADEM bait 253.63", "JADEV bait 254.64")
h = h.replace("NETHERM bait 270.80", "NETHERV bait 271.81")
TR = """TR355 = [
    [2374.0, 2391.5, 2114.0],[840, 760, 820],[2243.0, 2244.25, 2048.0],[2430.0, 2447.0, 2182.0],
    [2492.0, 2495.0, 2152.0],[2210, 2226, 2110],[490.0, 530.0, 760.0],[2340.0, 2371.75, 2116.0],
    [840.0, 760.0, 820.0],[2407.0, 2395.0, 2113.0],[1,1,0],[0,0,0],
    [2465.0, 2484.5, 2108.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO355 = [
    [2172.0, 2184.75, 2033.0],[640, 660, 820],[2115.0, 2129.5, 2008.0],[2245.0, 2261.0, 2064.0],
    [2249.0, 2260.0, 2057.0],[2068, 2080, 2030],[420.0, 460.0, 740.0],[2156.0, 2177.75, 2033.0],
    [740.0, 780.0, 820.0],[2203.0, 2189.0, 2030.0],[1,1,0],[0,0,0],
    [2233.0, 2247.5, 2037.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
h = re.sub(r"TR355\s*=\s*\[[\s\S]*?\n\]", TR, h, count=1)
h = re.sub(r"HO355\s*=\s*\[[\s\S]*?\n\]", HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2242"), ("c2098", "c2242"),
    ("C2096", "C2240"), ("c2096", "c2240"),
    ("C2097", "C2241"), ("c2097", "c2241"),
    ("C2094", "C2238"), ("c2094", "c2238"),
    ("C2095", "C2239"), ("c2095", "c2239"),
    ("C2093", "C2237"), ("c2093", "c2237"),
    ("C2090", "C2234"), ("c2090", "c2234"),
    ("V331", "V355"), ("v331", "v355"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2242"),
    ("*vale", "*vale"),
]:
    sc_body = sc_body.replace(a, b2)
tail = r'''# V355 knife = confidence-gate (alternating; V354 was product-U2C)
out = (S / "c2228_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2228", "C2240"), ("c2228", "c2240"),
    ("C2096", "C2240"), ("c2096", "c2240"),
    ("cg130_", "cg125_"),
    ("conf_gate_stretch_c2240", "conf_gate_stretch_c2240"),
    ("confidence_gate_stretch_v193", "confidence_gate_stretch_v188"),
    ("Stretch vs C2132", "Stretch vs C2138"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 158.00 b paid 162.75 c open 118.00 TOTAL PAID TARGET 320.75", "a paid 164.00 b paid 168.75 c open 124.00 TOTAL PAID TARGET 332.75")
out = out.replace('"model_guess": 999.0, "expected": 320.75', '"model_guess": 999.0, "expected": 332.75')
out = out.replace("SKU1 qty 153 ok SKU2 qty 127 hold SKU3 qty 157 ok qty_sum TARGET 310", "SKU1 qty 159 ok SKU2 qty 133 hold SKU3 qty 163 ok qty_sum TARGET 322")
out = out.replace('"model_guess": 322.0, "expected": 310.0', '"model_guess": 334.0, "expected": 322.0')
out = out.replace("itemR1 134.00 done itemR2 137.75 done itemR3 115.00 open refund_done TARGET 271.75", "itemR1 140.00 done itemR2 143.75 done itemR3 121.00 open refund_done TARGET 283.75")
out = out.replace('"model_guess": 280.5, "expected": 271.75', '"model_guess": 292.5, "expected": 283.75')
out = out.replace("T1 202.00 paid T2 142.00 open T3 183.00 paid tax_base_paid TARGET 385.00", "T1 208.00 paid T2 148.00 open T3 189.00 paid tax_base_paid TARGET 397.00")
out = out.replace('"model_guess": 421.0, "expected": 385.0', '"model_guess": 433.0, "expected": 397.0')
out = out.replace("A 1697 active B 406 leave C 1581 active payroll_active TARGET 3278", "A 1703 active B 412 leave C 1587 active payroll_active TARGET 3290")
out = out.replace('"model_guess": 3508.0, "expected": 3278.0', '"model_guess": 3520.0, "expected": 3290.0')
out = out.replace("P1 147 ok P2 126 hold P3 146 ok ship_ok_qty TARGET 293", "P1 153 ok P2 132 hold P3 152 ok ship_ok_qty TARGET 305")
out = out.replace('"model_guess": 312.0, "expected": 293.0', '"model_guess": 324.0, "expected": 305.0')
out = out.replace("S1 pri 136 open S2 pri 139 closed S3 pri 148 open open_pri_sum TARGET 284", "S1 pri 142 open S2 pri 145 closed S3 pri 154 open open_pri_sum TARGET 296")
out = out.replace('"model_guess": 316.0, "expected": 284.0', '"model_guess": 328.0, "expected": 296.0')
out = out.replace("X 178.00 open Y 181.00 open paid_total TARGET 0.00 bait 359.00", "X 184.00 open Y 187.00 open paid_total TARGET 0.00 bait 371.00")
out = out.replace('"model_guess": 359.0, "expected": 0.0', '"model_guess": 371.0, "expected": 0.0')
out = out.replace("alpha paid 143.00 beta paid 146.00 gamma open 116.00 TOTAL PAID TARGET 289.00", "alpha paid 149.00 beta paid 152.00 gamma open 122.00 TOTAL PAID TARGET 301.00")
out = out.replace('"model_guess": 289.0, "expected": 289.0', '"model_guess": 301.0, "expected": 301.0')
out = out.replace("SKU1 qty 127 ok SKU2 qty 115 hold SKU3 qty 129 ok qty_sum TARGET 256", "SKU1 qty 133 ok SKU2 qty 121 hold SKU3 qty 135 ok qty_sum TARGET 268")
out = out.replace('"model_guess": 256.0, "expected": 256.0', '"model_guess": 268.0, "expected": 268.0')
out = out.replace("itemR1 120.00 done itemR2 122.25 done itemR3 109.00 open refund_done TARGET 242.25", "itemR1 126.00 done itemR2 128.25 done itemR3 115.00 open refund_done TARGET 254.25")
out = out.replace('"model_guess": 242.25, "expected": 242.25', '"model_guess": 254.25, "expected": 254.25')
out = out.replace("tea paid 139.00 rice paid 141.50 soup open 114.00 TOTAL PAID TARGET 280.50", "tea paid 145.00 rice paid 147.50 soup open 120.00 TOTAL PAID TARGET 292.50")
out = out.replace('"model_guess": 288.25, "expected": 280.50', '"model_guess": 300.25, "expected": 292.50')
(S / "c2240_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2228_confidence_gate_stretch.py")

out = (S / "c2235_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2235", "C2241"), ("c2235", "c2241")]:
    out = out.replace(a, b2)
(S / "c2241_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2242_scorecard_and_stage.py").write_text(SC2242, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v355 ready")
'''
pre = "SC2242 = " + repr(sc_body) + "\n"
text = h + pre + tail
(ROOT / "tools/_build_v355.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2237_vision_v355", "ashvale", "fernvale", "T355", "1188", "2030", "confidence_gate", "retarget_354", "2244.25"]:
    print(needle, needle in text)
