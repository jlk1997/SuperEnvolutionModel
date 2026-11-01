from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v336.py").read_text(encoding="utf-8")
idx0 = b0.find('# V336 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2128 = " in head0:
    head0 = head0[:head0.find("SC2128 = ")]

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
    ("T336", "T337"), ("TR336", "TR337"), ("HO336", "HO337"),
    ("NEW336", "NEW337"),
    ("V336", "V337"), ("v336", "v337"),
    ("_v336_themes.json", "_v337_themes.json"),
    ("_v335_themes.json", "_v336_themes.json"),
    ("OLD335", "OLD336"),
    ("vision_images_v336", "vision_images_v337"),
    ("VL_GATE_V336", "VL_GATE_V337"), ("vl_gate_v336", "vl_gate_v337"),
    ("C2123", "C2129"), ("c2123", "c2129"),
    ("C2124", "C2130"), ("c2124", "c2130"),
    ("C2125", "C2131"), ("c2125", "c2131"),
    ("_v336c2123", "_v337c2129"),
    ("Harder than V334", "Harder than V335"),
    ("harder than V334", "harder than V335"),
    ("NEW themes vs V334:", "NEW themes vs V335:"),
    ("kept on V336", "kept on V337"),
    ("V336 keeps floor", "V337 keeps floor"),
    ("C2123 design+fixtures; no VL claim", "C2129 design+fixtures; no VL claim"),
    ("retarget_335", "retarget_336"),
    ("*wick", "*moor"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHWICK bait 247.57", "ASHMOOR bait 248.58")
h = h.replace("CEDARW bait 251.61", "CEDARM bait 252.62")
h = h.replace("DAWNW ghost 174.84", "DAWNM ghost 175.85")
h = h.replace("GLENW bait 244.54", "GLENM bait 245.55")
h = h.replace("JADEW bait 235.45", "JADEM bait 236.46")
h = h.replace("NETHERW bait 252.62", "NETHERM bait 253.63")

TR = '''TR337 = [
    [2338.0, 2355.5, 2078.0],[840, 760, 820],[2250.0, 2256.25, 2050.0],[2394.0, 2411.0, 2146.0],
    [2456.0, 2480.0, 2116.0],[2174, 2190, 2074],[490.0, 530.0, 760.0],[2304.0, 2335.75, 2080.0],
    [840.0, 760.0, 820.0],[2371.0, 2359.0, 2077.0],[1,1,0],[0,0,0],
    [2437.0, 2458.5, 2102.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO337 = [
    [2136.0, 2148.75, 1997.0],[640, 660, 820],[2079.0, 2093.5, 1972.0],[2209.0, 2225.0, 2028.0],
    [2241.0, 2252.0, 2021.0],[2032, 2044, 1994],[420.0, 460.0, 740.0],[2120.0, 2141.75, 1997.0],
    [740.0, 780.0, 820.0],[2167.0, 2153.0, 1994.0],[1,1,0],[0,0,0],
    [2202.0, 2217.5, 2007.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR337\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO337\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2134"), ("c2098", "c2134"),
    ("C2096", "C2132"), ("c2096", "c2132"),
    ("C2097", "C2133"), ("c2097", "c2133"),
    ("C2094", "C2130"), ("c2094", "c2130"),
    ("C2095", "C2131"), ("c2095", "c2131"),
    ("C2093", "C2129"), ("c2093", "c2129"),
    ("C2090", "C2126"), ("c2090", "c2126"),
    ("V331", "V337"), ("v331", "v337"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2134"),
    ("*hurst", "*moor"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V337 knife = confidence-gate (alternating; V336 was product-U2C)
out = (S / "c2120_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2120", "C2132"), ("c2120", "c2132"),
    ("C2096", "C2132"), ("c2096", "c2132"),
    ("cg151_", "cg150_"),
    ("conf_gate_stretch_c2132", "conf_gate_stretch_c2132"),
    ("confidence_gate_stretch_v214", "confidence_gate_stretch_v213"),
    ("Stretch vs C2120", "Stretch vs C2108"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75", "a paid 130.00 b paid 134.75 c open 90.00 TOTAL PAID TARGET 264.75")
out = out.replace('"model_guess": 999.0, "expected": 260.75', '"model_guess": 999.0, "expected": 264.75')
out = out.replace("SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250", "SKU1 qty 125 ok SKU2 qty 99 hold SKU3 qty 129 ok qty_sum TARGET 254")
out = out.replace('"model_guess": 262.0, "expected": 250.0', '"model_guess": 266.0, "expected": 254.0')
out = out.replace("itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75", "itemR1 106.00 done itemR2 109.75 done itemR3 87.00 open refund_done TARGET 215.75")
out = out.replace('"model_guess": 220.5, "expected": 211.75', '"model_guess": 224.5, "expected": 215.75')
out = out.replace("T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00", "T1 174.00 paid T2 114.00 open T3 155.00 paid tax_base_paid TARGET 329.00")
out = out.replace('"model_guess": 361.0, "expected": 325.0', '"model_guess": 365.0, "expected": 329.0')
out = out.replace("A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218", "A 1669 active B 378 leave C 1553 active payroll_active TARGET 3222")
out = out.replace('"model_guess": 3448.0, "expected": 3218.0', '"model_guess": 3452.0, "expected": 3222.0')
out = out.replace("P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233", "P1 119 ok P2 98 hold P3 118 ok ship_ok_qty TARGET 237")
out = out.replace('"model_guess": 252.0, "expected": 233.0', '"model_guess": 256.0, "expected": 237.0')
out = out.replace("S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224", "S1 pri 108 open S2 pri 111 closed S3 pri 120 open open_pri_sum TARGET 228")
out = out.replace('"model_guess": 256.0, "expected": 224.0', '"model_guess": 260.0, "expected": 228.0')
out = out.replace("X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00", "X 150.00 open Y 153.00 open paid_total TARGET 0.00 bait 303.00")
out = out.replace('"model_guess": 299.0, "expected": 0.0', '"model_guess": 303.0, "expected": 0.0')
out = out.replace("alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00", "alpha paid 115.00 beta paid 118.00 gamma open 88.00 TOTAL PAID TARGET 233.00")
out = out.replace('"model_guess": 229.0, "expected": 229.0', '"model_guess": 233.0, "expected": 233.0')
out = out.replace("SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196", "SKU1 qty 99 ok SKU2 qty 87 hold SKU3 qty 101 ok qty_sum TARGET 200")
out = out.replace('"model_guess": 196.0, "expected": 196.0', '"model_guess": 200.0, "expected": 200.0')
out = out.replace("itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25", "itemR1 92.00 done itemR2 94.25 done itemR3 81.00 open refund_done TARGET 186.25")
out = out.replace('"model_guess": 182.25, "expected": 182.25', '"model_guess": 186.25, "expected": 186.25')
out = out.replace("tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50", "tea paid 111.00 rice paid 113.50 soup open 86.00 TOTAL PAID TARGET 224.50")
out = out.replace('"model_guess": 228.25, "expected": 220.50', '"model_guess": 232.25, "expected": 224.50')
(S / "c2132_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2120_confidence_gate_stretch.py")

out = (S / "c2127_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2127", "C2133"), ("c2127", "c2133")]:
    out = out.replace(a, b2)
(S / "c2133_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2134_scorecard_and_stage.py").write_text(SC2134, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v337 ready")
'''
pre = "SC2134 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v337.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2129_vision_v337", "ashmoor", "fernmoor", "T337", "1188", "1994", "confidence_gate", "retarget_336", "2256.25"]:
    print(needle, needle in (h+pre+tail))
