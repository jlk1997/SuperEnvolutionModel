from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v320.py").read_text(encoding="utf-8")
idx0 = b0.find('# V320 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2032 = " in head0:
    head0 = head0[:head0.find("SC2032 = ")]

theme_pairs = [
    ("netherhurst", "nethermere"), ("NETHERHURST", "NETHERMERE"),
    ("cedarhurst", "cedarmere"), ("CEDARHURST", "CEDARMERE"),
    ("dawnhurst", "dawnmere"), ("DAWNHURST", "DAWNMERE"),
    ("fernhurst", "fernmere"), ("FERNHURST", "FERNMERE"),
    ("glenhurst", "glenmere"), ("GLENHURST", "GLENMERE"),
    ("hazehurst", "hazemere"), ("HAZEHURST", "HAZEMERE"),
    ("jadehurst", "jademere"), ("JADEHURST", "JADEMERE"),
    ("knothurst", "knotmere"), ("KNOTHURST", "KNOTMERE"),
    ("lakehurst", "lakemere"), ("LAKEHURST", "LAKEMERE"),
    ("mosshurst", "mossmere"), ("MOSSHURST", "MOSSMERE"),
    ("pinehurst", "pinemere"), ("PINEHURST", "PINEMERE"),
    ("quillhurst", "quillmere"), ("QUILLHURST", "QUILLMERE"),
    ("reedhurst", "reedmere"), ("REEDHURST", "REEDMERE"),
    ("stonehurst", "stonemere"), ("STONEHURST", "STONEMERE"),
    ("ashhurst", "ashmere"), ("ASHHURST", "ASHMERE"),
    ("elmhurst", "elmmere"), ("ELMHURST", "ELMMERE"),
    ("inkhurst", "inkmere"), ("INKHURST", "INKMERE"),
    ("oakhurst", "oakmere"), ("OAKHURST", "OAKMERE"),
]
pairs = [
    ("*hurst ; stack mid-band", "*mere ; stack mid-band"),
    ("T320", "T321"), ("TR320", "TR321"), ("HO320", "HO321"),
    ("NEW320", "NEW321"),
    ("V320", "V321"), ("v320", "v321"),
    ("_v320_themes.json", "_v321_themes.json"),
    ("_v319_themes.json", "_v320_themes.json"),
    ("OLD319", "OLD320"),
    ("vision_images_v320", "vision_images_v321"),
    ("VL_GATE_V320", "VL_GATE_V321"), ("vl_gate_v320", "vl_gate_v321"),
    ("C2027", "C2033"), ("c2027", "c2033"),
    ("C2028", "C2034"), ("c2028", "c2034"),
    ("C2029", "C2035"), ("c2029", "c2035"),
    ("_v320c2027", "_v321c2033"),
    ("Harder than V318", "Harder than V319"),
    ("harder than V318", "harder than V319"),
    ("NEW themes vs V318:", "NEW themes vs V319:"),
    ("kept on V320", "kept on V321"),
    ("V320 keeps floor", "V321 keeps floor"),
    ("C2027 design+fixtures; no VL claim", "C2033 design+fixtures; no VL claim"),
    ("retarget_319", "retarget_320"),
    ("*hurst", "*mere"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHURST bait 233.43", "ASHMERE bait 234.44")
h = h.replace("CEDARH bait 235.45", "CEDARM bait 236.46")
h = h.replace("DAWNH ghost 158.68", "DAWNM ghost 159.69")
h = h.replace("GLENH bait 228.38", "GLENM bait 229.39")
h = h.replace("JADEH bait 219.29", "JADEM bait 220.30")
h = h.replace("NETHERH bait 236.46", "NETHERM bait 237.47")

TR = '''TR321 = [
    [2306.0, 2323.5, 2046.0],[840, 760, 820],[2229.0, 2258.25, 2024.0],[2362.0, 2379.0, 2114.0],
    [2424.0, 2448.0, 2084.0],[2142, 2158, 2042],[490.0, 530.0, 760.0],[2272.0, 2303.75, 2048.0],
    [840.0, 760.0, 820.0],[2339.0, 2327.0, 2045.0],[1,1,0],[0,0,0],
    [2405.0, 2426.5, 2070.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO321 = [
    [2104.0, 2116.75, 1965.0],[640, 660, 820],[2047.0, 2061.5, 1940.0],[2177.0, 2193.0, 1996.0],
    [2218.0, 2234.0, 1989.0],[2000, 2012, 1960],[420.0, 460.0, 740.0],[2088.0, 2109.75, 1965.0],
    [740.0, 780.0, 820.0],[2135.0, 2121.0, 1962.0],[1,1,0],[0,0,0],
    [2170.0, 2185.5, 1975.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR321\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO321\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2026_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2026", "C2038"), ("c2026", "c2038"),
    ("C2024", "C2036"), ("c2024", "c2036"),
    ("C2025", "C2037"), ("c2025", "c2037"),
    ("C2022", "C2034"), ("c2022", "c2034"),
    ("C2023", "C2035"), ("c2023", "c2035"),
    ("C2021", "C2033"), ("c2021", "c2033"),
    ("C2018", "C2030"), ("c2018", "c2030"),
    ("V319", "V321"), ("v319", "v321"),
    ("STAGE_ANT_C2026", "STAGE_ANT_C2038"),
    ("*ford", "*mere"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V321 knife = confidence-gate (alternating; V320 was product-U2C)
out = (S / "c2024_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2024", "C2036"), ("c2024", "c2036"),
    ("C2012", "C2036"), ("c2012", "c2036"),
    ("cg142_", "cg143_"),
    ("conf_gate_stretch_c2024", "conf_gate_stretch_c2036"),
    ("confidence_gate_stretch_v205", "confidence_gate_stretch_v206"),
    ("Stretch vs C2012", "Stretch vs C2024"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 121.00 b paid 125.75 c open 81.00 TOTAL PAID TARGET 246.75", "a paid 122.00 b paid 126.75 c open 82.00 TOTAL PAID TARGET 248.75")
out = out.replace('"model_guess": 999.0, "expected": 246.75', '"model_guess": 999.0, "expected": 248.75')
out = out.replace("SKU1 qty 116 ok SKU2 qty 90 hold SKU3 qty 120 ok qty_sum TARGET 236", "SKU1 qty 117 ok SKU2 qty 91 hold SKU3 qty 121 ok qty_sum TARGET 238")
out = out.replace('"model_guess": 248.0, "expected": 236.0', '"model_guess": 250.0, "expected": 238.0')
out = out.replace("itemR1 97.00 done itemR2 100.75 done itemR3 78.00 open refund_done TARGET 197.75", "itemR1 98.00 done itemR2 101.75 done itemR3 79.00 open refund_done TARGET 199.75")
out = out.replace('"model_guess": 206.5, "expected": 197.75', '"model_guess": 208.5, "expected": 199.75')
out = out.replace("T1 165.00 paid T2 105.00 open T3 146.00 paid tax_base_paid TARGET 311.00", "T1 166.00 paid T2 106.00 open T3 147.00 paid tax_base_paid TARGET 313.00")
out = out.replace('"model_guess": 347.0, "expected": 311.0', '"model_guess": 349.0, "expected": 313.0')
out = out.replace("A 1660 active B 369 leave C 1544 active payroll_active TARGET 3204", "A 1661 active B 370 leave C 1545 active payroll_active TARGET 3206")
out = out.replace('"model_guess": 3434.0, "expected": 3204.0', '"model_guess": 3436.0, "expected": 3206.0')
out = out.replace("P1 110 ok P2 89 hold P3 109 ok ship_ok_qty TARGET 219", "P1 111 ok P2 90 hold P3 110 ok ship_ok_qty TARGET 221")
out = out.replace('"model_guess": 238.0, "expected": 219.0', '"model_guess": 240.0, "expected": 221.0')
out = out.replace("S1 pri 99 open S2 pri 102 closed S3 pri 111 open open_pri_sum TARGET 210", "S1 pri 100 open S2 pri 103 closed S3 pri 112 open open_pri_sum TARGET 212")
out = out.replace('"model_guess": 242.0, "expected": 210.0', '"model_guess": 244.0, "expected": 212.0')
out = out.replace("X 141.00 open Y 144.00 open paid_total TARGET 0.00 bait 285.00", "X 142.00 open Y 145.00 open paid_total TARGET 0.00 bait 287.00")
out = out.replace('"model_guess": 285.0, "expected": 0.0', '"model_guess": 287.0, "expected": 0.0')
out = out.replace("alpha paid 106.00 beta paid 109.00 gamma open 79.00 TOTAL PAID TARGET 215.00", "alpha paid 107.00 beta paid 110.00 gamma open 80.00 TOTAL PAID TARGET 217.00")
out = out.replace('"model_guess": 215.0, "expected": 215.0', '"model_guess": 217.0, "expected": 217.0')
out = out.replace("SKU1 qty 90 ok SKU2 qty 78 hold SKU3 qty 92 ok qty_sum TARGET 182", "SKU1 qty 91 ok SKU2 qty 79 hold SKU3 qty 93 ok qty_sum TARGET 184")
out = out.replace('"model_guess": 182.0, "expected": 182.0', '"model_guess": 184.0, "expected": 184.0')
out = out.replace("itemR1 83.00 done itemR2 85.25 done itemR3 72.00 open refund_done TARGET 168.25", "itemR1 84.00 done itemR2 86.25 done itemR3 73.00 open refund_done TARGET 170.25")
out = out.replace('"model_guess": 168.25, "expected": 168.25', '"model_guess": 170.25, "expected": 170.25')
out = out.replace("tea paid 102.00 rice paid 104.50 soup open 77.00 TOTAL PAID TARGET 206.50", "tea paid 103.00 rice paid 105.50 soup open 78.00 TOTAL PAID TARGET 208.50")
out = out.replace('"model_guess": 214.25, "expected": 206.50', '"model_guess": 216.25, "expected": 208.50')
(S / "c2036_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2024_confidence_gate_stretch.py")

out = (S / "c2031_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2031", "C2037"), ("c2031", "c2037")]:
    out = out.replace(a, b2)
(S / "c2037_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2038_scorecard_and_stage.py").write_text(SC2038, encoding="utf-8")
print("scorecard from fixed c2026 conf-gate pattern")
print("OK builder v321 ready")
'''
pre = "SC2038 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v321.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2033_vision_v321", "ashmere", "fernmere", "T321", "1188", "1960", "confidence_gate", "retarget_320"]:
    print(needle, needle in (h+pre+tail))
