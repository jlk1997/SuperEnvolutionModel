from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v246.py").read_text(encoding="utf-8")

theme_pairs = [
    ("nethercroft", "netherholm"), ("NETHERCROFT", "NETHERHOLM"),
    ("cedarcroft", "cedarholm"), ("CEDARCROFT", "CEDARHOLM"),
    ("dawncroft", "dawnholm"), ("DAWNCROFT", "DAWNHOLM"),
    ("ferncroft", "fernholm"), ("FERNCROFT", "FERNHOLM"),
    ("glencroft", "glenholm"), ("GLENCROFT", "GLENHOLM"),
    ("hazecroft", "hazeholm"), ("HAZECROFT", "HAZEHOLM"),
    ("jadecroft", "jadeholm"), ("JADECROFT", "JADEHOLM"),
    ("knotcroft", "knotholm"), ("KNOTCROFT", "KNOTHOLM"),
    ("lakecroft", "lakeholm"), ("LAKECROFT", "LAKEHOLM"),
    ("mosscroft", "mossholm"), ("MOSSCROFT", "MOSSHOLM"),
    ("pinecroft", "pineholm"), ("PINECROFT", "PINEHOLM"),
    ("quillcroft", "quillholm"), ("QUILLCROFT", "QUILLHOLM"),
    ("reedcroft", "reedholm"), ("REEDCROFT", "REEDHOLM"),
    ("stonecroft", "stoneholm"), ("STONECROFT", "STONEHOLM"),
    ("ashcroft", "ashholm"), ("ASHCROFT", "ASHHOLM"),
    ("elmcroft", "elmholm"), ("ELMCROFT", "ELMHOLM"),
    ("inkcroft", "inkholm"), ("INKCROFT", "INKHOLM"),
    ("oakcroft", "oakholm"), ("OAKCROFT", "OAKHOLM"),
]
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*croft ; stack mid-band", "*holm ; stack mid-band"),
    ("T246", "T247"), ("TR246", "TR247"), ("HO246", "HO247"),
    ("NEW246", "NEW247"),
    ("V246", "V247"), ("v246", "v247"),
    ("_v246_themes.json", "_v247_themes.json"),
    ("_v245_themes.json", "_v246_themes.json"),
    ("OLD245", "OLD246"),
    ("vision_images_v246", "vision_images_v247"),
    ("VL_GATE_V246", "VL_GATE_V247"), ("vl_gate_v246", "vl_gate_v247"),
    ("C1583", "C1589"), ("c1583", "c1589"),
    ("C1584", "C1590"), ("c1584", "c1590"),
    ("C1585", "C1591"), ("c1585", "c1591"),
    ("_v246c1583", "_v247c1589"),
    ("Harder than V244", "Harder than V245"),
    ("harder than V244", "harder than V245"),
    ("NEW themes vs V244:", "NEW themes vs V245:"),
    ("kept on V246", "kept on V247"),
    ("V246 keeps floor", "V247 keeps floor"),
    ("C1583 design+fixtures; no VL claim", "C1589 design+fixtures; no VL claim"),
    ("retarget_245", "retarget_246"),
    ("*croft", "*holm"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHHOLM bait 159.69", "ASHHOLM bait 160.70")
b = b.replace("CEDARC bait 161.71", "CEDARH bait 162.72")
b = b.replace("DAWNC ghost 84.84", "DAWNH ghost 85.85")
b = b.replace("GLENC bait 154.64", "GLENH bait 155.65")
b = b.replace("JADEC bait 145.55", "JADEH bait 146.56")
b = b.replace("NETHERC bait 162.72", "NETHERH bait 163.73")

# Money bump; STACK PLATEAU at 1188 (do NOT climb toward 1200)
# HO ship avoid 1830 - use 1834/1846
TR = '''TR247 = [
    [2140.0, 2157.5, 1880.0],[840, 760, 820],[2063.0, 2092.25, 1858.0],[2196.0, 2213.0, 1948.0],
    [2258.0, 2282.0, 1918.0],[1976, 1992, 1876],[480.0, 520.0, 740.0],[2106.0, 2137.75, 1882.0],
    [840.0, 760.0, 820.0],[2173.0, 2161.0, 1879.0],[1,1,0],[0,0,0],
    [2239.0, 2260.5, 1904.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO247 = [
    [1938.0, 1950.75, 1799.0],[740, 780, 820],[1881.0, 1895.5, 1774.0],[2011.0, 2027.0, 1828.0],
    [2052.0, 2068.0, 1823.0],[1834, 1846, 1792],[360.0, 400.0, 730.0],[1922.0, 1943.75, 1799.0],
    [780.0, 740.0, 820.0],[1969.0, 1955.0, 1794.0],[1,1,0],[0,0,0],
    [2004.0, 2019.5, 1809.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
b = re.sub(r'TR247\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO247\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')
assert 1188 <= 1196

idx = b.find('# V246 knife = product-U2C')
if idx < 0:
    idx = b.find('out = (S / "c1574_product_u2c_cost.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V247 knife = confidence-gate (alternating; V246 was product-U2C)
out = (S / "c1580_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1580", "C1592"), ("c1580", "c1592"),
    ("cg105_", "cg106_"),
    ("conf_gate_stretch_c1580", "conf_gate_stretch_c1592"),
    ("confidence_gate_stretch_v168", "confidence_gate_stretch_v169"),
    ("Stretch vs C1568", "Stretch vs C1580"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 84.00 b paid 88.75 c open 44.00 TOTAL PAID TARGET 172.75", "a paid 85.00 b paid 89.75 c open 45.00 TOTAL PAID TARGET 174.75")
out = out.replace('"model_guess": 999.0, "expected": 172.75', '"model_guess": 999.0, "expected": 174.75')
out = out.replace("SKU1 qty 79 ok SKU2 qty 53 hold SKU3 qty 83 ok qty_sum TARGET 162", "SKU1 qty 80 ok SKU2 qty 54 hold SKU3 qty 84 ok qty_sum TARGET 164")
out = out.replace('"model_guess": 174.0, "expected": 162.0', '"model_guess": 176.0, "expected": 164.0')
out = out.replace("itemR1 60.00 done itemR2 63.75 done itemR3 41.00 open refund_done TARGET 123.75", "itemR1 61.00 done itemR2 64.75 done itemR3 42.00 open refund_done TARGET 125.75")
out = out.replace('"model_guess": 132.5, "expected": 123.75', '"model_guess": 134.5, "expected": 125.75')
out = out.replace("T1 128.00 paid T2 68.00 open T3 109.00 paid tax_base_paid TARGET 237.00", "T1 129.00 paid T2 69.00 open T3 110.00 paid tax_base_paid TARGET 239.00")
out = out.replace('"model_guess": 273.0, "expected": 237.0', '"model_guess": 275.0, "expected": 239.0')
out = out.replace("A 1589 active B 332 leave C 1507 active payroll_active TARGET 3096", "A 1591 active B 333 leave C 1508 active payroll_active TARGET 3099")
out = out.replace('"model_guess": 3326.0, "expected": 3096.0', '"model_guess": 3329.0, "expected": 3099.0')
out = out.replace("P1 73 ok P2 52 hold P3 72 ok ship_ok_qty TARGET 145", "P1 74 ok P2 53 hold P3 73 ok ship_ok_qty TARGET 147")
out = out.replace('"model_guess": 164.0, "expected": 145.0', '"model_guess": 166.0, "expected": 147.0')
out = out.replace("S1 pri 62 open S2 pri 65 closed S3 pri 74 open open_pri_sum TARGET 136", "S1 pri 63 open S2 pri 66 closed S3 pri 75 open open_pri_sum TARGET 138")
out = out.replace('"model_guess": 168.0, "expected": 136.0', '"model_guess": 170.0, "expected": 138.0')
out = out.replace("X 104.00 open Y 107.00 open paid_total TARGET 0.00 bait 211.00", "X 105.00 open Y 108.00 open paid_total TARGET 0.00 bait 213.00")
out = out.replace('"model_guess": 211.0, "expected": 0.0', '"model_guess": 213.0, "expected": 0.0')
out = out.replace("alpha paid 69.00 beta paid 72.00 gamma open 42.00 TOTAL PAID TARGET 141.00", "alpha paid 70.00 beta paid 73.00 gamma open 43.00 TOTAL PAID TARGET 143.00")
out = out.replace('"model_guess": 141.0, "expected": 141.0', '"model_guess": 143.0, "expected": 143.0')
out = out.replace("SKU1 qty 53 ok SKU2 qty 41 hold SKU3 qty 55 ok qty_sum TARGET 108", "SKU1 qty 54 ok SKU2 qty 42 hold SKU3 qty 56 ok qty_sum TARGET 110")
out = out.replace('"model_guess": 108.0, "expected": 108.0', '"model_guess": 110.0, "expected": 110.0')
out = out.replace("itemR1 46.00 done itemR2 48.25 done itemR3 35.00 open refund_done TARGET 94.25", "itemR1 47.00 done itemR2 49.25 done itemR3 36.00 open refund_done TARGET 96.25")
out = out.replace('"model_guess": 94.25, "expected": 94.25', '"model_guess": 96.25, "expected": 96.25')
out = out.replace("tea paid 65.00 rice paid 67.50 soup open 40.00 TOTAL PAID TARGET 132.50", "tea paid 66.00 rice paid 68.50 soup open 41.00 TOTAL PAID TARGET 134.50")
out = out.replace('"model_guess": 140.25, "expected": 132.50', '"model_guess": 142.25, "expected": 134.50')
(S / "c1592_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate")

out = (S / "c1587_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1587", "C1593"), ("c1587", "c1593")]:
    out = out.replace(a, b2)
(S / "c1593_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1582_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1582", "C1594"), ("c1582", "c1594"),
    ("C1580", "C1592"), ("c1580", "c1592"),
    ("C1581", "C1593"), ("c1581", "c1593"),
    ("C1578", "C1590"), ("c1578", "c1590"),
    ("C1579", "C1591"), ("c1579", "c1591"),
    ("V245", "V247"), ("v245", "v247"),
    ("STAGE_ANT_C1582", "STAGE_ANT_C1594"),
    ("*vale", "*holm"),
]:
    out = out.replace(a, b2)
(S / "c1594_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v247 ready")
'''
(ROOT / "tools/_build_v247.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1589_vision_v247", "c1590_vision_v247", "c1591_vision_v247", "ashholm", "T247", "1188"]:
    print(needle, needle in (head+tail))
