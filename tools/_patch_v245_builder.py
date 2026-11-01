from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v244.py").read_text(encoding="utf-8")

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
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*mere ; stack mid-band", "*vale ; stack mid-band"),
    ("T244", "T245"), ("TR244", "TR245"), ("HO244", "HO245"),
    ("NEW244", "NEW245"),
    ("V244", "V245"), ("v244", "v245"),
    ("_v244_themes.json", "_v245_themes.json"),
    ("_v243_themes.json", "_v244_themes.json"),
    ("OLD243", "OLD244"),
    ("vision_images_v244", "vision_images_v245"),
    ("VL_GATE_V244", "VL_GATE_V245"), ("vl_gate_v244", "vl_gate_v245"),
    ("C1571", "C1577"), ("c1571", "c1577"),
    ("C1572", "C1578"), ("c1572", "c1578"),
    ("C1573", "C1579"), ("c1573", "c1579"),
    ("_v244c1571", "_v245c1577"),
    ("Harder than V242", "Harder than V243"),
    ("harder than V242", "harder than V243"),
    ("NEW themes vs V242:", "NEW themes vs V243:"),
    ("kept on V244", "kept on V245"),
    ("V244 keeps floor", "V245 keeps floor"),
    ("C1571 design+fixtures; no VL claim", "C1577 design+fixtures; no VL claim"),
    ("retarget_243", "retarget_244"),
    ("*mere", "*vale"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHVALE bait 157.67", "ASHVALE bait 158.68")
b = b.replace("CEDARM bait 159.69", "CEDARV bait 160.70")
b = b.replace("DAWNM ghost 82.82", "DAWNV ghost 83.83")
b = b.replace("GLENM bait 152.62", "GLENV bait 153.63")
b = b.replace("JADEM bait 143.53", "JADEV bait 144.54")
b = b.replace("NETHERM bait 160.70", "NETHERV bait 161.71")

# Money bump; stack hold ~1184 (<=1196); avoid BAN 1560/1830
TR = '''TR245 = [
    [2104.0, 2121.5, 1848.0],[840, 760, 820],[2027.0, 2056.25, 1826.0],[2160.0, 2177.0, 1916.0],
    [2222.0, 2246.0, 1886.0],[1944, 1960, 1844],[480.0, 520.0, 740.0],[2070.0, 2101.75, 1850.0],
    [840.0, 760.0, 820.0],[2137.0, 2125.0, 1847.0],[1,1,0],[0,0,0],
    [2203.0, 2224.5, 1872.0],[1,0,0],[1184, 1176, 1156],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO245 = [
    [1906.0, 1918.75, 1767.0],[740, 780, 820],[1849.0, 1863.5, 1742.0],[1979.0, 1995.0, 1796.0],
    [2020.0, 2036.0, 1791.0],[1814, 1828, 1760],[360.0, 400.0, 730.0],[1890.0, 1911.75, 1767.0],
    [780.0, 740.0, 820.0],[1937.0, 1923.0, 1762.0],[1,1,0],[0,0,0],
    [1972.0, 1987.5, 1777.0],[1,0,0],[1176, 1171, 1164],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
b = re.sub(r'TR245\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO245\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')
assert 1184 <= 1196

idx = b.find('# V244 knife = product-U2C')
if idx < 0:
    idx = b.find('out = (S / "c1562_product_u2c_cost.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V245 knife = confidence-gate (alternating; V244 was product-U2C)
out = (S / "c1568_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1568", "C1580"), ("c1568", "c1580"),
    ("cg104_", "cg105_"),
    ("conf_gate_stretch_c1568", "conf_gate_stretch_c1580"),
    ("confidence_gate_stretch_v167", "confidence_gate_stretch_v168"),
    ("Stretch vs C1556", "Stretch vs C1568"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 83.00 b paid 87.75 c open 43.00 TOTAL PAID TARGET 170.75", "a paid 84.00 b paid 88.75 c open 44.00 TOTAL PAID TARGET 172.75")
out = out.replace('"model_guess": 999.0, "expected": 170.75', '"model_guess": 999.0, "expected": 172.75')
out = out.replace("SKU1 qty 78 ok SKU2 qty 52 hold SKU3 qty 82 ok qty_sum TARGET 160", "SKU1 qty 79 ok SKU2 qty 53 hold SKU3 qty 83 ok qty_sum TARGET 162")
out = out.replace('"model_guess": 172.0, "expected": 160.0', '"model_guess": 174.0, "expected": 162.0')
out = out.replace("itemR1 59.00 done itemR2 62.75 done itemR3 40.00 open refund_done TARGET 121.75", "itemR1 60.00 done itemR2 63.75 done itemR3 41.00 open refund_done TARGET 123.75")
out = out.replace('"model_guess": 130.5, "expected": 121.75', '"model_guess": 132.5, "expected": 123.75')
out = out.replace("T1 127.00 paid T2 67.00 open T3 108.00 paid tax_base_paid TARGET 235.00", "T1 128.00 paid T2 68.00 open T3 109.00 paid tax_base_paid TARGET 237.00")
out = out.replace('"model_guess": 271.0, "expected": 235.0', '"model_guess": 273.0, "expected": 237.0')
out = out.replace("A 1587 active B 331 leave C 1506 active payroll_active TARGET 3093", "A 1589 active B 332 leave C 1507 active payroll_active TARGET 3096")
out = out.replace('"model_guess": 3323.0, "expected": 3093.0', '"model_guess": 3326.0, "expected": 3096.0')
out = out.replace("P1 72 ok P2 51 hold P3 71 ok ship_ok_qty TARGET 143", "P1 73 ok P2 52 hold P3 72 ok ship_ok_qty TARGET 145")
out = out.replace('"model_guess": 162.0, "expected": 143.0', '"model_guess": 164.0, "expected": 145.0')
out = out.replace("S1 pri 61 open S2 pri 64 closed S3 pri 73 open open_pri_sum TARGET 134", "S1 pri 62 open S2 pri 65 closed S3 pri 74 open open_pri_sum TARGET 136")
out = out.replace('"model_guess": 166.0, "expected": 134.0', '"model_guess": 168.0, "expected": 136.0')
out = out.replace("X 103.00 open Y 106.00 open paid_total TARGET 0.00 bait 209.00", "X 104.00 open Y 107.00 open paid_total TARGET 0.00 bait 211.00")
out = out.replace('"model_guess": 209.0, "expected": 0.0', '"model_guess": 211.0, "expected": 0.0')
out = out.replace("alpha paid 68.00 beta paid 71.00 gamma open 41.00 TOTAL PAID TARGET 139.00", "alpha paid 69.00 beta paid 72.00 gamma open 42.00 TOTAL PAID TARGET 141.00")
out = out.replace('"model_guess": 139.0, "expected": 139.0', '"model_guess": 141.0, "expected": 141.0')
out = out.replace("SKU1 qty 52 ok SKU2 qty 40 hold SKU3 qty 54 ok qty_sum TARGET 106", "SKU1 qty 53 ok SKU2 qty 41 hold SKU3 qty 55 ok qty_sum TARGET 108")
out = out.replace('"model_guess": 106.0, "expected": 106.0', '"model_guess": 108.0, "expected": 108.0')
out = out.replace("itemR1 45.00 done itemR2 47.25 done itemR3 34.00 open refund_done TARGET 92.25", "itemR1 46.00 done itemR2 48.25 done itemR3 35.00 open refund_done TARGET 94.25")
out = out.replace('"model_guess": 92.25, "expected": 92.25', '"model_guess": 94.25, "expected": 94.25')
out = out.replace("tea paid 64.00 rice paid 66.50 soup open 39.00 TOTAL PAID TARGET 130.50", "tea paid 65.00 rice paid 67.50 soup open 40.00 TOTAL PAID TARGET 132.50")
out = out.replace('"model_guess": 138.25, "expected": 130.50', '"model_guess": 140.25, "expected": 132.50')
(S / "c1580_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1575_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1575", "C1581"), ("c1575", "c1581")]:
    out = out.replace(a, b2)
(S / "c1581_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1570_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1570", "C1582"), ("c1570", "c1582"),
    ("C1568", "C1580"), ("c1568", "c1580"),
    ("C1569", "C1581"), ("c1569", "c1581"),
    ("C1566", "C1578"), ("c1566", "c1578"),
    ("C1567", "C1579"), ("c1567", "c1579"),
    ("V243", "V245"), ("v243", "v245"),
    ("STAGE_ANT_C1570", "STAGE_ANT_C1582"),
    ("*hurst", "*vale"),
]:
    out = out.replace(a, b2)
(S / "c1582_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v245 ready")
'''
(ROOT / "tools/_build_v245.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1577_vision_v245", "c1578_vision_v245", "c1579_vision_v245", "ashvale", "T245", "1184"]:
    print(needle, needle in (head+tail))
