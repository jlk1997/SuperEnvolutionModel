from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v254.py").read_text(encoding="utf-8")
idx0 = b0.find('# V254 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
    ("T254", "T255"), ("TR254", "TR255"), ("HO254", "HO255"),
    ("NEW254", "NEW255"),
    ("V254", "V255"), ("v254", "v255"),
    ("_v254_themes.json", "_v255_themes.json"),
    ("_v253_themes.json", "_v254_themes.json"),
    ("OLD253", "OLD254"),
    ("vision_images_v254", "vision_images_v255"),
    ("VL_GATE_V254", "VL_GATE_V255"), ("vl_gate_v254", "vl_gate_v255"),
    ("C1631", "C1637"), ("c1631", "c1637"),
    ("C1632", "C1638"), ("c1632", "c1638"),
    ("C1633", "C1639"), ("c1633", "c1639"),
    ("_v254c1631", "_v255c1637"),
    ("Harder than V252", "Harder than V253"),
    ("harder than V252", "harder than V253"),
    ("NEW themes vs V252:", "NEW themes vs V253:"),
    ("kept on V254", "kept on V255"),
    ("V254 keeps floor", "V255 keeps floor"),
    ("C1631 design+fixtures; no VL claim", "C1637 design+fixtures; no VL claim"),
    ("retarget_253", "retarget_254"),
    ("*hurst", "*mere"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMERE bait 167.77", "ASHMERE bait 168.78")
h = h.replace("CEDARH bait 169.79", "CEDARM bait 170.80")
h = h.replace("DAWNH ghost 92.92", "DAWNM ghost 93.93")
h = h.replace("GLENH bait 162.72", "GLENM bait 163.73")
h = h.replace("JADEH bait 153.63", "JADEM bait 154.64")
h = h.replace("NETHERH bait 170.80", "NETHERM bait 171.81")

TR = '''TR255 = [
    [2156.0, 2173.5, 1896.0],[840, 760, 820],[2079.0, 2108.25, 1874.0],[2212.0, 2229.0, 1964.0],
    [2274.0, 2298.0, 1934.0],[1992, 2008, 1892],[480.0, 520.0, 740.0],[2122.0, 2153.75, 1898.0],
    [840.0, 760.0, 820.0],[2189.0, 2177.0, 1895.0],[1,1,0],[0,0,0],
    [2255.0, 2276.5, 1920.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO255 = [
    [1954.0, 1966.75, 1815.0],[740, 780, 820],[1897.0, 1911.5, 1790.0],[2027.0, 2043.0, 1846.0],
    [2068.0, 2084.0, 1839.0],[1850, 1862, 1808],[360.0, 400.0, 730.0],[1938.0, 1959.75, 1815.0],
    [780.0, 740.0, 820.0],[1985.0, 1971.0, 1810.0],[1,1,0],[0,0,0],
    [2020.0, 2035.5, 1825.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR255\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO255\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1628_confidence_gate_stretch.py"
if not (ROOT / "scripts" / cg_src).exists():
    cg_src = "c1616_confidence_gate_stretch.py"
sc_src = "c1630_scorecard_and_stage.py"

tail = f'''# V255 knife = confidence-gate (alternating; V254 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1628", "C1640"), ("c1628", "c1640"),
    ("C1616", "C1640"), ("c1616", "c1640"),
    ("cg109_", "cg110_"),
    ("conf_gate_stretch_c1628", "conf_gate_stretch_c1640"),
    ("confidence_gate_stretch_v172", "confidence_gate_stretch_v173"),
    ("Stretch vs C1616", "Stretch vs C1628"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 88.00 b paid 92.75 c open 48.00 TOTAL PAID TARGET 180.75", "a paid 89.00 b paid 93.75 c open 49.00 TOTAL PAID TARGET 182.75")
out = out.replace('"model_guess": 999.0, "expected": 180.75', '"model_guess": 999.0, "expected": 182.75')
out = out.replace("SKU1 qty 83 ok SKU2 qty 57 hold SKU3 qty 87 ok qty_sum TARGET 170", "SKU1 qty 84 ok SKU2 qty 58 hold SKU3 qty 88 ok qty_sum TARGET 172")
out = out.replace('"model_guess": 182.0, "expected": 170.0', '"model_guess": 184.0, "expected": 172.0')
out = out.replace("itemR1 64.00 done itemR2 67.75 done itemR3 45.00 open refund_done TARGET 131.75", "itemR1 65.00 done itemR2 68.75 done itemR3 46.00 open refund_done TARGET 133.75")
out = out.replace('"model_guess": 140.5, "expected": 131.75', '"model_guess": 142.5, "expected": 133.75')
out = out.replace("T1 132.00 paid T2 72.00 open T3 113.00 paid tax_base_paid TARGET 245.00", "T1 133.00 paid T2 73.00 open T3 114.00 paid tax_base_paid TARGET 247.00")
out = out.replace('"model_guess": 281.0, "expected": 245.0', '"model_guess": 283.0, "expected": 247.0')
out = out.replace("A 1597 active B 336 leave C 1511 active payroll_active TARGET 3108", "A 1599 active B 337 leave C 1512 active payroll_active TARGET 3111")
out = out.replace('"model_guess": 3338.0, "expected": 3108.0', '"model_guess": 3341.0, "expected": 3111.0')
out = out.replace("P1 77 ok P2 56 hold P3 76 ok ship_ok_qty TARGET 153", "P1 78 ok P2 57 hold P3 77 ok ship_ok_qty TARGET 155")
out = out.replace('"model_guess": 172.0, "expected": 153.0', '"model_guess": 174.0, "expected": 155.0')
out = out.replace("S1 pri 66 open S2 pri 69 closed S3 pri 78 open open_pri_sum TARGET 144", "S1 pri 67 open S2 pri 70 closed S3 pri 79 open open_pri_sum TARGET 146")
out = out.replace('"model_guess": 176.0, "expected": 144.0', '"model_guess": 178.0, "expected": 146.0')
out = out.replace("X 108.00 open Y 111.00 open paid_total TARGET 0.00 bait 219.00", "X 109.00 open Y 112.00 open paid_total TARGET 0.00 bait 221.00")
out = out.replace('"model_guess": 219.0, "expected": 0.0', '"model_guess": 221.0, "expected": 0.0')
out = out.replace("alpha paid 73.00 beta paid 76.00 gamma open 46.00 TOTAL PAID TARGET 149.00", "alpha paid 74.00 beta paid 77.00 gamma open 47.00 TOTAL PAID TARGET 151.00")
out = out.replace('"model_guess": 149.0, "expected": 149.0', '"model_guess": 151.0, "expected": 151.0')
out = out.replace("SKU1 qty 57 ok SKU2 qty 45 hold SKU3 qty 59 ok qty_sum TARGET 116", "SKU1 qty 58 ok SKU2 qty 46 hold SKU3 qty 60 ok qty_sum TARGET 118")
out = out.replace('"model_guess": 116.0, "expected": 116.0', '"model_guess": 118.0, "expected": 118.0')
out = out.replace("itemR1 50.00 done itemR2 52.25 done itemR3 39.00 open refund_done TARGET 102.25", "itemR1 51.00 done itemR2 53.25 done itemR3 40.00 open refund_done TARGET 104.25")
out = out.replace('"model_guess": 102.25, "expected": 102.25', '"model_guess": 104.25, "expected": 104.25')
out = out.replace("tea paid 69.00 rice paid 71.50 soup open 44.00 TOTAL PAID TARGET 140.50", "tea paid 70.00 rice paid 72.50 soup open 45.00 TOTAL PAID TARGET 142.50")
out = out.replace('"model_guess": 148.25, "expected": 140.50', '"model_guess": 150.25, "expected": 142.50')
(S / "c1640_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1635_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1635", "C1641"), ("c1635", "c1641")]:
    out = out.replace(a, b2)
(S / "c1641_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1630", "C1642"), ("c1630", "c1642"),
    ("C1628", "C1640"), ("c1628", "c1640"),
    ("C1629", "C1641"), ("c1629", "c1641"),
    ("C1626", "C1638"), ("c1626", "c1638"),
    ("C1627", "C1639"), ("c1627", "c1639"),
    ("V253", "V255"), ("v253", "v255"),
    ("STAGE_ANT_C1630", "STAGE_ANT_C1642"),
    ("*ford", "*mere"),
]:
    out = out.replace(a, b2)
(S / "c1642_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v255 ready")
'''
(ROOT / "tools/_build_v255.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1637_vision_v255", "ashmere", "fernmere", "T255", "1188", "1846", "confidence_gate"]:
    print(needle, needle in (h+tail))
