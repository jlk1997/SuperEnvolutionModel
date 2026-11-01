from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v232.py").read_text(encoding="utf-8")

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
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*hurst ; stack mid-band", "*mere ; stack mid-band"),
    ("T232", "T233"), ("TR232", "TR233"), ("HO232", "HO233"),
    ("NEW232", "NEW233"),
    ("V232", "V233"), ("v232", "v233"),
    ("_v232_themes.json", "_v233_themes.json"),
    ("_v231_themes.json", "_v232_themes.json"),
    ("OLD231", "OLD232"),
    ("vision_images_v232", "vision_images_v233"),
    ("VL_GATE_V232", "VL_GATE_V233"), ("vl_gate_v232", "vl_gate_v233"),
    ("C1499", "C1505"), ("c1499", "c1505"),
    ("C1500", "C1506"), ("c1500", "c1506"),
    ("C1501", "C1507"), ("c1501", "c1507"),
    ("_v232c1499", "_v233c1505"),
    ("Harder than V230", "Harder than V231"),
    ("harder than V230", "harder than V231"),
    ("NEW themes vs V230:", "NEW themes vs V231:"),
    ("kept on V232", "kept on V233"),
    ("V232 keeps floor", "V233 keeps floor"),
    ("C1499 design+fixtures; no VL claim", "C1505 design+fixtures; no VL claim"),
    ("retarget_231", "retarget_232"),
    ("*hurst", "*mere"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHMERE bait 145.55", "ASHMERE bait 146.56")
b = b.replace("CEDARH bait 147.57", "CEDARM bait 148.58")
b = b.replace("DAWNH ghost 70.70", "DAWNM ghost 71.71")
b = b.replace("GLENH bait 140.50", "GLENM bait 141.51")
b = b.replace("JADEH bait 131.41", "JADEM bait 132.42")
b = b.replace("NETHERH bait 148.58", "NETHERM bait 149.59")

TR = '''TR233 = [
    [1888.0, 1905.5, 1654.0],[840, 760, 820],[1811.0, 1840.25, 1634.0],[1944.0, 1961.0, 1724.0],
    [2006.0, 2030.0, 1694.0],[1752, 1768, 1652],[480.0, 520.0, 740.0],[1854.0, 1885.75, 1658.0],
    [840.0, 760.0, 820.0],[1921.0, 1909.0, 1655.0],[1,1,0],[0,0,0],
    [1987.0, 2008.5, 1680.0],[1,0,0],[1180, 1172, 1152],[1196, 1180, 748],[1,0,0],[1212, 1196, 1174],
]'''
HO = '''HO233 = [
    [1714.0, 1726.75, 1575.0],[740, 780, 820],[1657.0, 1670.5, 1550.0],[1787.0, 1803.0, 1604.0],
    [1828.0, 1844.0, 1599.0],[1622, 1636, 1568],[360.0, 400.0, 730.0],[1698.0, 1719.75, 1575.0],
    [780.0, 740.0, 820.0],[1745.0, 1731.0, 1570.0],[1,1,0],[0,0,0],
    [1780.0, 1795.5, 1585.0],[1,0,0],[1168, 1163, 1156],[1182, 1176, 1164],[1,0,0],[1192, 1186, 1165],
]'''
b = re.sub(r'TR233\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO233\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

idx = b.find('# V232 knife = product-U2C')
if idx < 0:
    idx = b.find('# V233 knife = product-U2C')
if idx < 0:
    idx = b.find('out = (S / "c1490_product_u2c_cost.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V233 knife = confidence-gate (alternating; V232 was product-U2C)
out = (S / "c1496_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1496", "C1508"), ("c1496", "c1508"),
    ("cg98_", "cg99_"),
    ("conf_gate_stretch_c1496", "conf_gate_stretch_c1508"),
    ("confidence_gate_stretch_v161", "confidence_gate_stretch_v162"),
    ("Stretch vs C1484", "Stretch vs C1496"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 77.00 b paid 81.75 c open 37.00 TOTAL PAID TARGET 158.75", "a paid 78.00 b paid 82.75 c open 38.00 TOTAL PAID TARGET 160.75")
out = out.replace('"model_guess": 999.0, "expected": 158.75', '"model_guess": 999.0, "expected": 160.75')
out = out.replace("SKU1 qty 72 ok SKU2 qty 46 hold SKU3 qty 76 ok qty_sum TARGET 148", "SKU1 qty 73 ok SKU2 qty 47 hold SKU3 qty 77 ok qty_sum TARGET 150")
out = out.replace('"model_guess": 160.0, "expected": 148.0', '"model_guess": 162.0, "expected": 150.0')
out = out.replace("itemR1 53.00 done itemR2 56.75 done itemR3 34.00 open refund_done TARGET 109.75", "itemR1 54.00 done itemR2 57.75 done itemR3 35.00 open refund_done TARGET 111.75")
out = out.replace('"model_guess": 118.5, "expected": 109.75', '"model_guess": 120.5, "expected": 111.75')
out = out.replace("T1 121.00 paid T2 61.00 open T3 102.00 paid tax_base_paid TARGET 223.00", "T1 122.00 paid T2 62.00 open T3 103.00 paid tax_base_paid TARGET 225.00")
out = out.replace('"model_guess": 259.0, "expected": 223.0', '"model_guess": 261.0, "expected": 225.0')
out = out.replace("A 1575 active B 325 leave C 1500 active payroll_active TARGET 3075", "A 1577 active B 326 leave C 1501 active payroll_active TARGET 3078")
out = out.replace('"model_guess": 3305.0, "expected": 3075.0', '"model_guess": 3308.0, "expected": 3078.0')
out = out.replace("P1 66 ok P2 45 hold P3 65 ok ship_ok_qty TARGET 131", "P1 67 ok P2 46 hold P3 66 ok ship_ok_qty TARGET 133")
out = out.replace('"model_guess": 150.0, "expected": 131.0', '"model_guess": 152.0, "expected": 133.0')
out = out.replace("S1 pri 55 open S2 pri 58 closed S3 pri 67 open open_pri_sum TARGET 122", "S1 pri 56 open S2 pri 59 closed S3 pri 68 open open_pri_sum TARGET 124")
out = out.replace('"model_guess": 154.0, "expected": 122.0', '"model_guess": 156.0, "expected": 124.0')
out = out.replace("X 97.00 open Y 100.00 open paid_total TARGET 0.00 bait 197.00", "X 98.00 open Y 101.00 open paid_total TARGET 0.00 bait 199.00")
out = out.replace('"model_guess": 197.0, "expected": 0.0', '"model_guess": 199.0, "expected": 0.0')
out = out.replace("alpha paid 62.00 beta paid 65.00 gamma open 35.00 TOTAL PAID TARGET 127.00", "alpha paid 63.00 beta paid 66.00 gamma open 36.00 TOTAL PAID TARGET 129.00")
out = out.replace('"model_guess": 127.0, "expected": 127.0', '"model_guess": 129.0, "expected": 129.0')
out = out.replace("SKU1 qty 46 ok SKU2 qty 34 hold SKU3 qty 48 ok qty_sum TARGET 94", "SKU1 qty 47 ok SKU2 qty 35 hold SKU3 qty 49 ok qty_sum TARGET 96")
out = out.replace('"model_guess": 94.0, "expected": 94.0', '"model_guess": 96.0, "expected": 96.0')
out = out.replace("itemR1 39.00 done itemR2 41.25 done itemR3 28.00 open refund_done TARGET 80.25", "itemR1 40.00 done itemR2 42.25 done itemR3 29.00 open refund_done TARGET 82.25")
out = out.replace('"model_guess": 80.25, "expected": 80.25', '"model_guess": 82.25, "expected": 82.25')
out = out.replace("tea paid 58.00 rice paid 60.50 soup open 33.00 TOTAL PAID TARGET 118.50", "tea paid 59.00 rice paid 61.50 soup open 34.00 TOTAL PAID TARGET 120.50")
out = out.replace('"model_guess": 126.25, "expected": 118.50', '"model_guess": 128.25, "expected": 120.50')
(S / "c1508_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1503_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1503", "C1509"), ("c1503", "c1509")]:
    out = out.replace(a, b2)
(S / "c1509_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1498_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1498", "C1510"), ("c1498", "c1510"),
    ("C1496", "C1508"), ("c1496", "c1508"),
    ("C1497", "C1509"), ("c1497", "c1509"),
    ("C1494", "C1506"), ("c1494", "c1506"),
    ("C1495", "C1507"), ("c1495", "c1507"),
    ("V231", "V233"), ("v231", "v233"),
    ("STAGE_ANT_C1498", "STAGE_ANT_C1510"),
    ("*ford", "*mere"),
]:
    out = out.replace(a, b2)
(S / "c1510_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v233 ready")
'''
(ROOT / "tools/_build_v233.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1505_vision_v233", "c1506_vision_v233", "c1507_vision_v233", "ashmere", "T233"]:
    print(needle, needle in (head+tail))
