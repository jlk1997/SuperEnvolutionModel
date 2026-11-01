from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v322.py").read_text(encoding="utf-8")
idx0 = b0.find('# V322 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2044 = " in head0:
    head0 = head0[:head0.find("SC2044 = ")]

theme_pairs = [
    ("nethervale", "nethercroft"), ("NETHERVALE", "NETHERCROFT"),
    ("cedarvale", "cedarcroft"), ("CEDARVALE", "CEDARCROFT"),
    ("dawnvale", "dawncroft"), ("DAWNVALE", "DAWNCROFT"),
    ("fernvale", "ferncroft"), ("FERNVALE", "FERNCROFT"),
    ("glenvale", "glencroft"), ("GLENVALE", "GLENCROFT"),
    ("hazevale", "hazecroft"), ("HAZEVALE", "HAZECROFT"),
    ("jadevale", "jadecroft"), ("JADEVALE", "JADECROFT"),
    ("knotvale", "knotcroft"), ("KNOTVALE", "KNOTCROFT"),
    ("lakevale", "lakecroft"), ("LAKEVALE", "LAKECROFT"),
    ("mossvale", "mosscroft"), ("MOSSVALE", "MOSSCROFT"),
    ("pinevale", "pinecroft"), ("PINEVALE", "PINECROFT"),
    ("quillvale", "quillcroft"), ("QUILLVALE", "QUILLCROFT"),
    ("reedvale", "reedcroft"), ("REEDVALE", "REEDCROFT"),
    ("stonevale", "stonecroft"), ("STONEVALE", "STONECROFT"),
    ("ashvale", "ashcroft"), ("ASHVALE", "ASHCROFT"),
    ("elmvale", "elmcroft"), ("ELMVALE", "ELMCROFT"),
    ("inkvale", "inkcroft"), ("INKVALE", "INKCROFT"),
    ("oakvale", "oakcroft"), ("OAKVALE", "OAKCROFT"),
]
pairs = [
    ("*vale ; stack mid-band", "*croft ; stack mid-band"),
    ("T322", "T323"), ("TR322", "TR323"), ("HO322", "HO323"),
    ("NEW322", "NEW323"),
    ("V322", "V323"), ("v322", "v323"),
    ("_v322_themes.json", "_v323_themes.json"),
    ("_v321_themes.json", "_v322_themes.json"),
    ("OLD321", "OLD322"),
    ("vision_images_v322", "vision_images_v323"),
    ("VL_GATE_V322", "VL_GATE_V323"), ("vl_gate_v322", "vl_gate_v323"),
    ("C2039", "C2045"), ("c2039", "c2045"),
    ("C2040", "C2046"), ("c2040", "c2046"),
    ("C2041", "C2047"), ("c2041", "c2047"),
    ("_v322c2039", "_v323c2045"),
    ("Harder than V320", "Harder than V321"),
    ("harder than V320", "harder than V321"),
    ("NEW themes vs V320:", "NEW themes vs V321:"),
    ("kept on V322", "kept on V323"),
    ("V322 keeps floor", "V323 keeps floor"),
    ("C2039 design+fixtures; no VL claim", "C2045 design+fixtures; no VL claim"),
    ("retarget_321", "retarget_322"),
    ("*vale", "*croft"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHVALE bait 235.45", "ASHCROFT bait 236.46")
h = h.replace("CEDARV bait 237.47", "CEDARC bait 238.48")
h = h.replace("DAWNV ghost 160.70", "DAWNC ghost 161.71")
h = h.replace("GLENV bait 230.40", "GLENC bait 231.41")
h = h.replace("JADEV bait 221.31", "JADEC bait 222.32")
h = h.replace("NETHERV bait 238.48", "NETHERC bait 239.49")

TR = '''TR323 = [
    [2310.0, 2327.5, 2050.0],[840, 760, 820],[2233.0, 2262.25, 2028.0],[2366.0, 2383.0, 2118.0],
    [2428.0, 2452.0, 2088.0],[2146, 2162, 2046],[490.0, 530.0, 760.0],[2276.0, 2307.75, 2052.0],
    [840.0, 760.0, 820.0],[2343.0, 2331.0, 2049.0],[1,1,0],[0,0,0],
    [2409.0, 2430.5, 2074.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO323 = [
    [2108.0, 2120.75, 1969.0],[640, 660, 820],[2051.0, 2065.5, 1944.0],[2181.0, 2197.0, 2000.0],
    [2222.0, 2238.0, 1993.0],[2004, 2016, 1964],[420.0, 460.0, 740.0],[2092.0, 2113.75, 1969.0],
    [740.0, 780.0, 820.0],[2139.0, 2125.0, 1966.0],[1,1,0],[0,0,0],
    [2174.0, 2189.5, 1979.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR323\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO323\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2038_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2038", "C2050"), ("c2038", "c2050"),
    ("C2036", "C2048"), ("c2036", "c2048"),
    ("C2037", "C2049"), ("c2037", "c2049"),
    ("C2034", "C2046"), ("c2034", "c2046"),
    ("C2035", "C2047"), ("c2035", "c2047"),
    ("C2033", "C2045"), ("c2033", "c2045"),
    ("C2030", "C2042"), ("c2030", "c2042"),
    ("V321", "V323"), ("v321", "v323"),
    ("STAGE_ANT_C2038", "STAGE_ANT_C2050"),
    ("*mere", "*croft"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V323 knife = confidence-gate (alternating; V322 was product-U2C)
out = (S / "c2036_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2036", "C2048"), ("c2036", "c2048"),
    ("C2024", "C2048"), ("c2024", "c2048"),
    ("cg143_", "cg144_"),
    ("conf_gate_stretch_c2036", "conf_gate_stretch_c2048"),
    ("confidence_gate_stretch_v206", "confidence_gate_stretch_v207"),
    ("Stretch vs C2024", "Stretch vs C2036"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 122.00 b paid 126.75 c open 82.00 TOTAL PAID TARGET 248.75", "a paid 123.00 b paid 127.75 c open 83.00 TOTAL PAID TARGET 250.75")
out = out.replace('"model_guess": 999.0, "expected": 248.75', '"model_guess": 999.0, "expected": 250.75')
out = out.replace("SKU1 qty 117 ok SKU2 qty 91 hold SKU3 qty 121 ok qty_sum TARGET 238", "SKU1 qty 118 ok SKU2 qty 92 hold SKU3 qty 122 ok qty_sum TARGET 240")
out = out.replace('"model_guess": 250.0, "expected": 238.0', '"model_guess": 252.0, "expected": 240.0')
out = out.replace("itemR1 98.00 done itemR2 101.75 done itemR3 79.00 open refund_done TARGET 199.75", "itemR1 99.00 done itemR2 102.75 done itemR3 80.00 open refund_done TARGET 201.75")
out = out.replace('"model_guess": 208.5, "expected": 199.75', '"model_guess": 210.5, "expected": 201.75')
out = out.replace("T1 166.00 paid T2 106.00 open T3 147.00 paid tax_base_paid TARGET 313.00", "T1 167.00 paid T2 107.00 open T3 148.00 paid tax_base_paid TARGET 315.00")
out = out.replace('"model_guess": 349.0, "expected": 313.0', '"model_guess": 351.0, "expected": 315.0')
out = out.replace("A 1661 active B 370 leave C 1545 active payroll_active TARGET 3206", "A 1662 active B 371 leave C 1546 active payroll_active TARGET 3208")
out = out.replace('"model_guess": 3436.0, "expected": 3206.0', '"model_guess": 3438.0, "expected": 3208.0')
out = out.replace("P1 111 ok P2 90 hold P3 110 ok ship_ok_qty TARGET 221", "P1 112 ok P2 91 hold P3 111 ok ship_ok_qty TARGET 223")
out = out.replace('"model_guess": 240.0, "expected": 221.0', '"model_guess": 242.0, "expected": 223.0')
out = out.replace("S1 pri 100 open S2 pri 103 closed S3 pri 112 open open_pri_sum TARGET 212", "S1 pri 101 open S2 pri 104 closed S3 pri 113 open open_pri_sum TARGET 214")
out = out.replace('"model_guess": 244.0, "expected": 212.0', '"model_guess": 246.0, "expected": 214.0')
out = out.replace("X 142.00 open Y 145.00 open paid_total TARGET 0.00 bait 287.00", "X 143.00 open Y 146.00 open paid_total TARGET 0.00 bait 289.00")
out = out.replace('"model_guess": 287.0, "expected": 0.0', '"model_guess": 289.0, "expected": 0.0')
out = out.replace("alpha paid 107.00 beta paid 110.00 gamma open 80.00 TOTAL PAID TARGET 217.00", "alpha paid 108.00 beta paid 111.00 gamma open 81.00 TOTAL PAID TARGET 219.00")
out = out.replace('"model_guess": 217.0, "expected": 217.0', '"model_guess": 219.0, "expected": 219.0')
out = out.replace("SKU1 qty 91 ok SKU2 qty 79 hold SKU3 qty 93 ok qty_sum TARGET 184", "SKU1 qty 92 ok SKU2 qty 80 hold SKU3 qty 94 ok qty_sum TARGET 186")
out = out.replace('"model_guess": 184.0, "expected": 184.0', '"model_guess": 186.0, "expected": 186.0')
out = out.replace("itemR1 84.00 done itemR2 86.25 done itemR3 73.00 open refund_done TARGET 170.25", "itemR1 85.00 done itemR2 87.25 done itemR3 74.00 open refund_done TARGET 172.25")
out = out.replace('"model_guess": 170.25, "expected": 170.25', '"model_guess": 172.25, "expected": 172.25')
out = out.replace("tea paid 103.00 rice paid 105.50 soup open 78.00 TOTAL PAID TARGET 208.50", "tea paid 104.00 rice paid 106.50 soup open 79.00 TOTAL PAID TARGET 210.50")
out = out.replace('"model_guess": 216.25, "expected": 208.50', '"model_guess": 218.25, "expected": 210.50')
(S / "c2048_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2036_confidence_gate_stretch.py")

out = (S / "c2043_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2043", "C2049"), ("c2043", "c2049")]:
    out = out.replace(a, b2)
(S / "c2049_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2050_scorecard_and_stage.py").write_text(SC2050, encoding="utf-8")
print("scorecard from fixed c2038 conf-gate pattern")
print("OK builder v323 ready")
'''
pre = "SC2050 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v323.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2045_vision_v323", "ashcroft", "ferncroft", "T323", "1188", "1964", "confidence_gate", "retarget_322"]:
    print(needle, needle in (h+pre+tail))
