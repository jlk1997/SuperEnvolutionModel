from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v248.py").read_text(encoding="utf-8")
idx0 = b0.find('# V248 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
    ("T248", "T249"), ("TR248", "TR249"), ("HO248", "HO249"),
    ("NEW248", "NEW249"),
    ("V248", "V249"), ("v248", "v249"),
    ("_v248_themes.json", "_v249_themes.json"),
    ("_v247_themes.json", "_v248_themes.json"),
    ("OLD247", "OLD248"),
    ("vision_images_v248", "vision_images_v249"),
    ("VL_GATE_V248", "VL_GATE_V249"), ("vl_gate_v248", "vl_gate_v249"),
    ("C1595", "C1601"), ("c1595", "c1601"),
    ("C1596", "C1602"), ("c1596", "c1602"),
    ("C1597", "C1603"), ("c1597", "c1603"),
    ("_v248c1595", "_v249c1601"),
    ("Harder than V246", "Harder than V247"),
    ("harder than V246", "harder than V247"),
    ("NEW themes vs V246:", "NEW themes vs V247:"),
    ("kept on V248", "kept on V249"),
    ("V248 keeps floor", "V249 keeps floor"),
    ("C1595 design+fixtures; no VL claim", "C1601 design+fixtures; no VL claim"),
    ("retarget_247", "retarget_248"),
    ("*wick", "*moor"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMOOR bait 161.71", "ASHMOOR bait 162.72")
h = h.replace("CEDARW bait 163.73", "CEDARM bait 164.74")
h = h.replace("DAWNW ghost 86.86", "DAWNM ghost 87.87")
h = h.replace("GLENW bait 156.66", "GLENM bait 157.67")
h = h.replace("JADEW bait 147.57", "JADEM bait 148.58")
h = h.replace("NETHERW bait 164.74", "NETHERM bait 165.75")

# Money bump; STACK PLATEAU 1188; HO avoid BAN 1830
TR = '''TR249 = [
    [2144.0, 2161.5, 1884.0],[840, 760, 820],[2067.0, 2096.25, 1862.0],[2200.0, 2217.0, 1952.0],
    [2262.0, 2286.0, 1922.0],[1980, 1996, 1880],[480.0, 520.0, 740.0],[2110.0, 2141.75, 1886.0],
    [840.0, 760.0, 820.0],[2177.0, 2165.0, 1883.0],[1,1,0],[0,0,0],
    [2243.0, 2264.5, 1908.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO249 = [
    [1942.0, 1954.75, 1803.0],[740, 780, 820],[1885.0, 1899.5, 1778.0],[2015.0, 2031.0, 1834.0],
    [2056.0, 2072.0, 1827.0],[1838, 1850, 1796],[360.0, 400.0, 730.0],[1926.0, 1947.75, 1803.0],
    [780.0, 740.0, 820.0],[1973.0, 1959.0, 1798.0],[1,1,0],[0,0,0],
    [2008.0, 2023.5, 1813.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR249\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO249\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

# conf-gate source: prefer latest stretch
cg_src = "c1592_confidence_gate_stretch.py"
if not (ROOT / "scripts" / cg_src).exists():
    cg_src = "c1580_confidence_gate_stretch.py"
sc_src = "c1594_scorecard_and_stage.py"  # conf-gate era

tail = f'''# V249 knife = confidence-gate (alternating; V248 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1592", "C1604"), ("c1592", "c1604"),
    ("C1580", "C1604"), ("c1580", "c1604"),
    ("cg106_", "cg107_"),
    ("conf_gate_stretch_c1592", "conf_gate_stretch_c1604"),
    ("confidence_gate_stretch_v169", "confidence_gate_stretch_v170"),
    ("Stretch vs C1580", "Stretch vs C1592"),
]:
    out = out.replace(a, b2)
# light money bump from V247 stretch targets
out = out.replace("a paid 85.00 b paid 89.75 c open 45.00 TOTAL PAID TARGET 174.75", "a paid 86.00 b paid 90.75 c open 46.00 TOTAL PAID TARGET 176.75")
out = out.replace('"model_guess": 999.0, "expected": 174.75', '"model_guess": 999.0, "expected": 176.75')
out = out.replace("SKU1 qty 80 ok SKU2 qty 54 hold SKU3 qty 84 ok qty_sum TARGET 164", "SKU1 qty 81 ok SKU2 qty 55 hold SKU3 qty 85 ok qty_sum TARGET 166")
out = out.replace('"model_guess": 176.0, "expected": 164.0', '"model_guess": 178.0, "expected": 166.0')
out = out.replace("itemR1 61.00 done itemR2 64.75 done itemR3 42.00 open refund_done TARGET 125.75", "itemR1 62.00 done itemR2 65.75 done itemR3 43.00 open refund_done TARGET 127.75")
out = out.replace('"model_guess": 134.5, "expected": 125.75', '"model_guess": 136.5, "expected": 127.75')
out = out.replace("T1 129.00 paid T2 69.00 open T3 110.00 paid tax_base_paid TARGET 239.00", "T1 130.00 paid T2 70.00 open T3 111.00 paid tax_base_paid TARGET 241.00")
out = out.replace('"model_guess": 275.0, "expected": 239.0', '"model_guess": 277.0, "expected": 241.0')
out = out.replace("A 1591 active B 333 leave C 1508 active payroll_active TARGET 3099", "A 1593 active B 334 leave C 1509 active payroll_active TARGET 3102")
out = out.replace('"model_guess": 3329.0, "expected": 3099.0', '"model_guess": 3332.0, "expected": 3102.0')
out = out.replace("P1 74 ok P2 53 hold P3 73 ok ship_ok_qty TARGET 147", "P1 75 ok P2 54 hold P3 74 ok ship_ok_qty TARGET 149")
out = out.replace('"model_guess": 166.0, "expected": 147.0', '"model_guess": 168.0, "expected": 149.0')
out = out.replace("S1 pri 63 open S2 pri 66 closed S3 pri 75 open open_pri_sum TARGET 138", "S1 pri 64 open S2 pri 67 closed S3 pri 76 open open_pri_sum TARGET 140")
out = out.replace('"model_guess": 170.0, "expected": 138.0', '"model_guess": 172.0, "expected": 140.0')
out = out.replace("X 105.00 open Y 108.00 open paid_total TARGET 0.00 bait 213.00", "X 106.00 open Y 109.00 open paid_total TARGET 0.00 bait 215.00")
out = out.replace('"model_guess": 213.0, "expected": 0.0', '"model_guess": 215.0, "expected": 0.0')
out = out.replace("alpha paid 70.00 beta paid 73.00 gamma open 43.00 TOTAL PAID TARGET 143.00", "alpha paid 71.00 beta paid 74.00 gamma open 44.00 TOTAL PAID TARGET 145.00")
out = out.replace('"model_guess": 143.0, "expected": 143.0', '"model_guess": 145.0, "expected": 145.0')
out = out.replace("SKU1 qty 54 ok SKU2 qty 42 hold SKU3 qty 56 ok qty_sum TARGET 110", "SKU1 qty 55 ok SKU2 qty 43 hold SKU3 qty 57 ok qty_sum TARGET 112")
out = out.replace('"model_guess": 110.0, "expected": 110.0', '"model_guess": 112.0, "expected": 112.0')
out = out.replace("itemR1 47.00 done itemR2 49.25 done itemR3 36.00 open refund_done TARGET 96.25", "itemR1 48.00 done itemR2 50.25 done itemR3 37.00 open refund_done TARGET 98.25")
out = out.replace('"model_guess": 96.25, "expected": 96.25', '"model_guess": 98.25, "expected": 98.25')
out = out.replace("tea paid 66.00 rice paid 68.50 soup open 41.00 TOTAL PAID TARGET 134.50", "tea paid 67.00 rice paid 69.50 soup open 42.00 TOTAL PAID TARGET 136.50")
out = out.replace('"model_guess": 142.25, "expected": 134.50', '"model_guess": 144.25, "expected": 136.50')
(S / "c1604_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1599_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1599", "C1605"), ("c1599", "c1605")]:
    out = out.replace(a, b2)
(S / "c1605_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1594", "C1606"), ("c1594", "c1606"),
    ("C1592", "C1604"), ("c1592", "c1604"),
    ("C1593", "C1605"), ("c1593", "c1605"),
    ("C1590", "C1602"), ("c1590", "c1602"),
    ("C1591", "C1603"), ("c1591", "c1603"),
    ("V247", "V249"), ("v247", "v249"),
    ("STAGE_ANT_C1594", "STAGE_ANT_C1606"),
    ("*holm", "*moor"),
]:
    out = out.replace(a, b2)
(S / "c1606_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v249 ready")
'''
(ROOT / "tools/_build_v249.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1601_vision_v249", "ashmoor", "T249", "1188", "1834", "confidence_gate"]:
    print(needle, needle in (h+tail))
