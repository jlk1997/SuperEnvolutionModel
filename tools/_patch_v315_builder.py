from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v314.py").read_text(encoding="utf-8")
idx0 = b0.find('# V314 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1996 = " in head0:
    head0 = head0[:head0.find("SC1996 = ")]

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
    ("T314", "T315"), ("TR314", "TR315"), ("HO314", "HO315"),
    ("NEW314", "NEW315"),
    ("V314", "V315"), ("v314", "v315"),
    ("_v314_themes.json", "_v315_themes.json"),
    ("_v313_themes.json", "_v314_themes.json"),
    ("OLD313", "OLD314"),
    ("vision_images_v314", "vision_images_v315"),
    ("VL_GATE_V314", "VL_GATE_V315"), ("vl_gate_v314", "vl_gate_v315"),
    ("C1991", "C1997"), ("c1991", "c1997"),
    ("C1992", "C1998"), ("c1992", "c1998"),
    ("C1993", "C1999"), ("c1993", "c1999"),
    ("_v314c1991", "_v315c1997"),
    ("Harder than V312", "Harder than V313"),
    ("harder than V312", "harder than V313"),
    ("NEW themes vs V312:", "NEW themes vs V313:"),
    ("kept on V314", "kept on V315"),
    ("V314 keeps floor", "V315 keeps floor"),
    ("C1991 design+fixtures; no VL claim", "C1997 design+fixtures; no VL claim"),
    ("retarget_313", "retarget_314"),
    ("*wick", "*moor"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHWICK bait 227.37", "ASHMOOR bait 228.38")
h = h.replace("CEDARW bait 229.39", "CEDARM bait 230.40")
h = h.replace("DAWNW ghost 152.62", "DAWNM ghost 153.63")
h = h.replace("GLENW bait 222.32", "GLENM bait 223.33")
h = h.replace("JADEW bait 213.23", "JADEM bait 214.24")
h = h.replace("NETHERW bait 230.40", "NETHERM bait 231.41")

TR = '''TR315 = [
    [2294.0, 2311.5, 2034.0],[840, 760, 820],[2217.0, 2246.25, 2012.0],[2350.0, 2367.0, 2102.0],
    [2412.0, 2436.0, 2072.0],[2130, 2146, 2030],[490.0, 530.0, 760.0],[2260.0, 2291.75, 2036.0],
    [840.0, 760.0, 820.0],[2327.0, 2315.0, 2033.0],[1,1,0],[0,0,0],
    [2393.0, 2414.5, 2058.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO315 = [
    [2092.0, 2104.75, 1953.0],[640, 660, 820],[2035.0, 2049.5, 1928.0],[2165.0, 2181.0, 1984.0],
    [2206.0, 2222.0, 1977.0],[1988, 2000, 1948],[420.0, 460.0, 740.0],[2076.0, 2097.75, 1953.0],
    [740.0, 780.0, 820.0],[2123.0, 2109.0, 1950.0],[1,1,0],[0,0,0],
    [2158.0, 2173.5, 1963.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR315\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO315\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c1990_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1990", "C2002"), ("c1990", "c2002"),
    ("C1988", "C2000"), ("c1988", "c2000"),
    ("C1989", "C2001"), ("c1989", "c2001"),
    ("C1986", "C1998"), ("c1986", "c1998"),
    ("C1987", "C1999"), ("c1987", "c1999"),
    ("C1469", "C1997"), ("c1469", "c1997"),
    ("C1466", "C1994"), ("c1466", "c1994"),
    ("V313", "V315"), ("v313", "v315"),
    ("STAGE_ANT_C1990", "STAGE_ANT_C2002"),
    ("*holm", "*moor"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V315 knife = confidence-gate (alternating; V314 was product-U2C)
out = (S / "c1988_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1988", "C2000"), ("c1988", "c2000"),
    ("C1976", "C2000"), ("c1976", "c2000"),
    ("cg139_", "cg140_"),
    ("conf_gate_stretch_c1988", "conf_gate_stretch_c2000"),
    ("confidence_gate_stretch_v202", "confidence_gate_stretch_v203"),
    ("Stretch vs C1976", "Stretch vs C1988"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 118.00 b paid 122.75 c open 78.00 TOTAL PAID TARGET 240.75", "a paid 119.00 b paid 123.75 c open 79.00 TOTAL PAID TARGET 242.75")
out = out.replace('"model_guess": 999.0, "expected": 240.75', '"model_guess": 999.0, "expected": 242.75')
out = out.replace("SKU1 qty 113 ok SKU2 qty 87 hold SKU3 qty 117 ok qty_sum TARGET 230", "SKU1 qty 114 ok SKU2 qty 88 hold SKU3 qty 118 ok qty_sum TARGET 232")
out = out.replace('"model_guess": 242.0, "expected": 230.0', '"model_guess": 244.0, "expected": 232.0')
out = out.replace("itemR1 94.00 done itemR2 97.75 done itemR3 75.00 open refund_done TARGET 191.75", "itemR1 95.00 done itemR2 98.75 done itemR3 76.00 open refund_done TARGET 193.75")
out = out.replace('"model_guess": 200.5, "expected": 191.75', '"model_guess": 202.5, "expected": 193.75')
out = out.replace("T1 162.00 paid T2 102.00 open T3 143.00 paid tax_base_paid TARGET 305.00", "T1 163.00 paid T2 103.00 open T3 144.00 paid tax_base_paid TARGET 307.00")
out = out.replace('"model_guess": 341.0, "expected": 305.0', '"model_guess": 343.0, "expected": 307.0')
out = out.replace("A 1657 active B 366 leave C 1541 active payroll_active TARGET 3198", "A 1658 active B 367 leave C 1542 active payroll_active TARGET 3200")
out = out.replace('"model_guess": 3428.0, "expected": 3198.0', '"model_guess": 3430.0, "expected": 3200.0')
out = out.replace("P1 107 ok P2 86 hold P3 106 ok ship_ok_qty TARGET 213", "P1 108 ok P2 87 hold P3 107 ok ship_ok_qty TARGET 215")
out = out.replace('"model_guess": 232.0, "expected": 213.0', '"model_guess": 234.0, "expected": 215.0')
out = out.replace("S1 pri 96 open S2 pri 99 closed S3 pri 108 open open_pri_sum TARGET 204", "S1 pri 97 open S2 pri 100 closed S3 pri 109 open open_pri_sum TARGET 206")
out = out.replace('"model_guess": 236.0, "expected": 204.0', '"model_guess": 238.0, "expected": 206.0')
out = out.replace("X 138.00 open Y 141.00 open paid_total TARGET 0.00 bait 279.00", "X 139.00 open Y 142.00 open paid_total TARGET 0.00 bait 281.00")
out = out.replace('"model_guess": 279.0, "expected": 0.0', '"model_guess": 281.0, "expected": 0.0')
out = out.replace("alpha paid 103.00 beta paid 106.00 gamma open 76.00 TOTAL PAID TARGET 209.00", "alpha paid 104.00 beta paid 107.00 gamma open 77.00 TOTAL PAID TARGET 211.00")
out = out.replace('"model_guess": 209.0, "expected": 209.0', '"model_guess": 211.0, "expected": 211.0')
out = out.replace("SKU1 qty 87 ok SKU2 qty 75 hold SKU3 qty 89 ok qty_sum TARGET 176", "SKU1 qty 88 ok SKU2 qty 76 hold SKU3 qty 90 ok qty_sum TARGET 178")
out = out.replace('"model_guess": 176.0, "expected": 176.0', '"model_guess": 178.0, "expected": 178.0')
out = out.replace("itemR1 80.00 done itemR2 82.25 done itemR3 69.00 open refund_done TARGET 162.25", "itemR1 81.00 done itemR2 83.25 done itemR3 70.00 open refund_done TARGET 164.25")
out = out.replace('"model_guess": 162.25, "expected": 162.25', '"model_guess": 164.25, "expected": 164.25')
out = out.replace("tea paid 99.00 rice paid 101.50 soup open 74.00 TOTAL PAID TARGET 200.50", "tea paid 100.00 rice paid 102.50 soup open 75.00 TOTAL PAID TARGET 202.50")
out = out.replace('"model_guess": 208.25, "expected": 200.50', '"model_guess": 210.25, "expected": 202.50')
(S / "c2000_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1988_confidence_gate_stretch.py")

out = (S / "c1995_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1995", "C2001"), ("c1995", "c2001")]:
    out = out.replace(a, b2)
(S / "c2001_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2002_scorecard_and_stage.py").write_text(SC2002, encoding="utf-8")
print("scorecard from fixed c1990 conf-gate pattern")
print("OK builder v315 ready")
'''
pre = "SC2002 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v315.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1997_vision_v315", "ashmoor", "fernmoor", "T315", "1188", "1948", "confidence_gate", "retarget_314"]:
    print(needle, needle in (h+pre+tail))
