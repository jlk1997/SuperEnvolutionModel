from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v332.py").read_text(encoding="utf-8")
idx0 = b0.find('# V332 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2104 = " in head0:
    head0 = head0[:head0.find("SC2104 = ")]

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
    ("T332", "T333"), ("TR332", "TR333"), ("HO332", "HO333"),
    ("NEW332", "NEW333"),
    ("V332", "V333"), ("v332", "v333"),
    ("_v332_themes.json", "_v333_themes.json"),
    ("_v331_themes.json", "_v332_themes.json"),
    ("OLD331", "OLD332"),
    ("vision_images_v332", "vision_images_v333"),
    ("VL_GATE_V332", "VL_GATE_V333"), ("vl_gate_v332", "vl_gate_v333"),
    ("C2099", "C2105"), ("c2099", "c2105"),
    ("C2100", "C2106"), ("c2100", "c2106"),
    ("C2101", "C2107"), ("c2101", "c2107"),
    ("_v332c2099", "_v333c2105"),
    ("Harder than V330", "Harder than V331"),
    ("harder than V330", "harder than V331"),
    ("NEW themes vs V330:", "NEW themes vs V331:"),
    ("kept on V332", "kept on V333"),
    ("V332 keeps floor", "V333 keeps floor"),
    ("C2099 design+fixtures; no VL claim", "C2105 design+fixtures; no VL claim"),
    ("retarget_331", "retarget_332"),
    ("*mere", "*vale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMERE bait 245.55", "ASHVALE bait 246.56")
h = h.replace("CEDARM bait 247.57", "CEDARV bait 248.58")
h = h.replace("DAWNM ghost 170.80", "DAWNV ghost 171.81")
h = h.replace("GLENM bait 240.50", "GLENV bait 241.51")
h = h.replace("JADEM bait 231.41", "JADEV bait 232.42")
h = h.replace("NETHERM bait 248.58", "NETHERV bait 249.59")

# refund ~2251/225x stay ~224x/225x
TR = '''TR333 = [
    [2330.0, 2347.5, 2070.0],[840, 760, 820],[2251.0, 2257.25, 2046.0],[2386.0, 2403.0, 2138.0],
    [2448.0, 2472.0, 2108.0],[2166, 2182, 2066],[490.0, 530.0, 760.0],[2296.0, 2327.75, 2072.0],
    [840.0, 760.0, 820.0],[2363.0, 2351.0, 2069.0],[1,1,0],[0,0,0],
    [2429.0, 2450.5, 2094.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO333 = [
    [2128.0, 2140.75, 1989.0],[640, 660, 820],[2071.0, 2085.5, 1964.0],[2201.0, 2217.0, 2020.0],
    [2242.0, 2258.0, 2013.0],[2024, 2036, 1986],[420.0, 460.0, 740.0],[2112.0, 2133.75, 1989.0],
    [740.0, 780.0, 820.0],[2159.0, 2145.0, 1986.0],[1,1,0],[0,0,0],
    [2194.0, 2209.5, 1999.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR333\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO333\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

# conf-gate scorecard from V331 pattern (C2098), retarget to C2110 + prior PRODUCT C2102
sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2110"), ("c2098", "c2110"),
    ("C2096", "C2108"), ("c2096", "c2108"),
    ("C2097", "C2109"), ("c2097", "c2109"),
    ("C2094", "C2106"), ("c2094", "c2106"),
    ("C2095", "C2107"), ("c2095", "c2107"),
    ("C2093", "C2105"), ("c2093", "c2105"),
    ("C2090", "C2102"), ("c2090", "c2102"),
    ("V331", "V333"), ("v331", "v333"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2110"),
    ("*hurst", "*vale"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V333 knife = confidence-gate (alternating; V332 was product-U2C)
out = (S / "c2096_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2096", "C2108"), ("c2096", "c2108"),
    ("C2084", "C2108"), ("c2084", "c2108"),
    ("cg148_", "cg149_"),
    ("conf_gate_stretch_c2096", "conf_gate_stretch_c2108"),
    ("confidence_gate_stretch_v211", "confidence_gate_stretch_v212"),
    ("Stretch vs C2084", "Stretch vs C2096"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 127.00 b paid 131.75 c open 87.00 TOTAL PAID TARGET 258.75", "a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75")
out = out.replace('"model_guess": 999.0, "expected": 258.75', '"model_guess": 999.0, "expected": 260.75')
out = out.replace("SKU1 qty 122 ok SKU2 qty 96 hold SKU3 qty 126 ok qty_sum TARGET 248", "SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250")
out = out.replace('"model_guess": 260.0, "expected": 248.0', '"model_guess": 262.0, "expected": 250.0')
out = out.replace("itemR1 103.00 done itemR2 106.75 done itemR3 84.00 open refund_done TARGET 209.75", "itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75")
out = out.replace('"model_guess": 218.5, "expected": 209.75', '"model_guess": 220.5, "expected": 211.75')
out = out.replace("T1 171.00 paid T2 111.00 open T3 152.00 paid tax_base_paid TARGET 323.00", "T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00")
out = out.replace('"model_guess": 359.0, "expected": 323.0', '"model_guess": 361.0, "expected": 325.0')
out = out.replace("A 1666 active B 375 leave C 1550 active payroll_active TARGET 3216", "A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218")
out = out.replace('"model_guess": 3446.0, "expected": 3216.0', '"model_guess": 3448.0, "expected": 3218.0')
out = out.replace("P1 116 ok P2 95 hold P3 115 ok ship_ok_qty TARGET 231", "P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233")
out = out.replace('"model_guess": 250.0, "expected": 231.0', '"model_guess": 252.0, "expected": 233.0')
out = out.replace("S1 pri 105 open S2 pri 108 closed S3 pri 117 open open_pri_sum TARGET 222", "S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224")
out = out.replace('"model_guess": 254.0, "expected": 222.0', '"model_guess": 256.0, "expected": 224.0')
out = out.replace("X 147.00 open Y 150.00 open paid_total TARGET 0.00 bait 297.00", "X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00")
out = out.replace('"model_guess": 297.0, "expected": 0.0', '"model_guess": 299.0, "expected": 0.0')
out = out.replace("alpha paid 112.00 beta paid 115.00 gamma open 85.00 TOTAL PAID TARGET 227.00", "alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00")
out = out.replace('"model_guess": 227.0, "expected": 227.0', '"model_guess": 229.0, "expected": 229.0')
out = out.replace("SKU1 qty 96 ok SKU2 qty 84 hold SKU3 qty 98 ok qty_sum TARGET 194", "SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196")
out = out.replace('"model_guess": 194.0, "expected": 194.0', '"model_guess": 196.0, "expected": 196.0')
out = out.replace("itemR1 89.00 done itemR2 91.25 done itemR3 78.00 open refund_done TARGET 180.25", "itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25")
out = out.replace('"model_guess": 180.25, "expected": 180.25', '"model_guess": 182.25, "expected": 182.25')
out = out.replace("tea paid 108.00 rice paid 110.50 soup open 83.00 TOTAL PAID TARGET 218.50", "tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50")
out = out.replace('"model_guess": 226.25, "expected": 218.50', '"model_guess": 228.25, "expected": 220.50')
(S / "c2108_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2096_confidence_gate_stretch.py")

out = (S / "c2103_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2103", "C2109"), ("c2103", "c2109")]:
    out = out.replace(a, b2)
(S / "c2109_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2110_scorecard_and_stage.py").write_text(SC2110, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v333 ready")
'''
pre = "SC2110 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v333.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2105_vision_v333", "ashvale", "fernvale", "T333", "1188", "1986", "confidence_gate", "retarget_332", "2257.25"]:
    print(needle, needle in (h+pre+tail))
