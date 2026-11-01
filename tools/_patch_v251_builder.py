from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v250.py").read_text(encoding="utf-8")
idx0 = b0.find('# V250 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("netherfen", "netherbrook"), ("NETHERFEN", "NETHERBROOK"),
    ("cedarfen", "cedarbrook"), ("CEDARFEN", "CEDARBROOK"),
    ("dawnfen", "dawnbrook"), ("DAWNFEN", "DAWNBROOK"),
    ("fernfen", "fernbrook"), ("FERNFEN", "FERNBROOK"),
    ("glenfen", "glenbrook"), ("GLENFEN", "GLENBROOK"),
    ("hazefen", "hazebrook"), ("HAZEFEN", "HAZEBROOK"),
    ("jadefen", "jadebrook"), ("JADEFEN", "JADEBROOK"),
    ("knotfen", "knotbrook"), ("KNOTFEN", "KNOTBROOK"),
    ("lakefen", "lakebrook"), ("LAKEFEN", "LAKEBROOK"),
    ("mossfen", "mossbrook"), ("MOSSFEN", "MOSSBROOK"),
    ("pinefen", "pinebrook"), ("PINEFEN", "PINEBROOK"),
    ("quillfen", "quillbrook"), ("QUILLFEN", "QUILLBROOK"),
    ("reedfen", "reedbrook"), ("REEDFEN", "REEDBROOK"),
    ("stonefen", "stonebrook"), ("STONEFEN", "STONEBROOK"),
    ("ashfen", "ashbrook"), ("ASHFEN", "ASHBROOK"),
    ("elmfen", "elmbrook"), ("ELMFEN", "ELMBROOK"),
    ("inkfen", "inkbrook"), ("INKFEN", "INKBROOK"),
    ("oakfen", "oakbrook"), ("OAKFEN", "OAKBROOK"),
]
pairs = [
    ("*fen ; stack mid-band", "*brook ; stack mid-band"),
    ("T250", "T251"), ("TR250", "TR251"), ("HO250", "HO251"),
    ("NEW250", "NEW251"),
    ("V250", "V251"), ("v250", "v251"),
    ("_v250_themes.json", "_v251_themes.json"),
    ("_v249_themes.json", "_v250_themes.json"),
    ("OLD249", "OLD250"),
    ("vision_images_v250", "vision_images_v251"),
    ("VL_GATE_V250", "VL_GATE_V251"), ("vl_gate_v250", "vl_gate_v251"),
    ("C1607", "C1613"), ("c1607", "c1613"),
    ("C1608", "C1614"), ("c1608", "c1614"),
    ("C1609", "C1615"), ("c1609", "c1615"),
    ("_v250c1607", "_v251c1613"),
    ("Harder than V248", "Harder than V249"),
    ("harder than V248", "harder than V249"),
    ("NEW themes vs V248:", "NEW themes vs V249:"),
    ("kept on V250", "kept on V251"),
    ("V250 keeps floor", "V251 keeps floor"),
    ("C1607 design+fixtures; no VL claim", "C1613 design+fixtures; no VL claim"),
    ("retarget_249", "retarget_250"),
    ("*fen", "*brook"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHBROOK bait 163.73", "ASHBROOK bait 164.74")
h = h.replace("CEDARF bait 165.75", "CEDARB bait 166.76")
h = h.replace("DAWNF ghost 88.88", "DAWNB ghost 89.89")
h = h.replace("GLENF bait 158.68", "GLENB bait 159.69")
h = h.replace("JADEF bait 149.59", "JADEB bait 150.60")
h = h.replace("NETHERF bait 166.76", "NETHERB bait 167.77")

TR = '''TR251 = [
    [2148.0, 2165.5, 1888.0],[840, 760, 820],[2071.0, 2100.25, 1866.0],[2204.0, 2221.0, 1956.0],
    [2266.0, 2290.0, 1926.0],[1984, 2000, 1884],[480.0, 520.0, 740.0],[2114.0, 2145.75, 1890.0],
    [840.0, 760.0, 820.0],[2181.0, 2169.0, 1887.0],[1,1,0],[0,0,0],
    [2247.0, 2268.5, 1912.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO251 = [
    [1946.0, 1958.75, 1807.0],[740, 780, 820],[1889.0, 1903.5, 1782.0],[2019.0, 2035.0, 1838.0],
    [2060.0, 2076.0, 1831.0],[1842, 1854, 1800],[360.0, 400.0, 730.0],[1930.0, 1951.75, 1807.0],
    [780.0, 740.0, 820.0],[1977.0, 1963.0, 1802.0],[1,1,0],[0,0,0],
    [2012.0, 2027.5, 1817.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR251\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO251\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1604_confidence_gate_stretch.py"
if not (ROOT / "scripts" / cg_src).exists():
    cg_src = "c1592_confidence_gate_stretch.py"
sc_src = "c1606_scorecard_and_stage.py"

tail = f'''# V251 knife = confidence-gate (alternating; V250 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1604", "C1616"), ("c1604", "c1616"),
    ("C1592", "C1616"), ("c1592", "c1616"),
    ("cg107_", "cg108_"),
    ("conf_gate_stretch_c1604", "conf_gate_stretch_c1616"),
    ("confidence_gate_stretch_v170", "confidence_gate_stretch_v171"),
    ("Stretch vs C1592", "Stretch vs C1604"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 86.00 b paid 90.75 c open 46.00 TOTAL PAID TARGET 176.75", "a paid 87.00 b paid 91.75 c open 47.00 TOTAL PAID TARGET 178.75")
out = out.replace('"model_guess": 999.0, "expected": 176.75', '"model_guess": 999.0, "expected": 178.75')
out = out.replace("SKU1 qty 81 ok SKU2 qty 55 hold SKU3 qty 85 ok qty_sum TARGET 166", "SKU1 qty 82 ok SKU2 qty 56 hold SKU3 qty 86 ok qty_sum TARGET 168")
out = out.replace('"model_guess": 178.0, "expected": 166.0', '"model_guess": 180.0, "expected": 168.0')
out = out.replace("itemR1 62.00 done itemR2 65.75 done itemR3 43.00 open refund_done TARGET 127.75", "itemR1 63.00 done itemR2 66.75 done itemR3 44.00 open refund_done TARGET 129.75")
out = out.replace('"model_guess": 136.5, "expected": 127.75', '"model_guess": 138.5, "expected": 129.75')
out = out.replace("T1 130.00 paid T2 70.00 open T3 111.00 paid tax_base_paid TARGET 241.00", "T1 131.00 paid T2 71.00 open T3 112.00 paid tax_base_paid TARGET 243.00")
out = out.replace('"model_guess": 277.0, "expected": 241.0', '"model_guess": 279.0, "expected": 243.0')
out = out.replace("A 1593 active B 334 leave C 1509 active payroll_active TARGET 3102", "A 1595 active B 335 leave C 1510 active payroll_active TARGET 3105")
out = out.replace('"model_guess": 3332.0, "expected": 3102.0', '"model_guess": 3335.0, "expected": 3105.0')
out = out.replace("P1 75 ok P2 54 hold P3 74 ok ship_ok_qty TARGET 149", "P1 76 ok P2 55 hold P3 75 ok ship_ok_qty TARGET 151")
out = out.replace('"model_guess": 168.0, "expected": 149.0', '"model_guess": 170.0, "expected": 151.0')
out = out.replace("S1 pri 64 open S2 pri 67 closed S3 pri 76 open open_pri_sum TARGET 140", "S1 pri 65 open S2 pri 68 closed S3 pri 77 open open_pri_sum TARGET 142")
out = out.replace('"model_guess": 172.0, "expected": 140.0', '"model_guess": 174.0, "expected": 142.0')
out = out.replace("X 106.00 open Y 109.00 open paid_total TARGET 0.00 bait 215.00", "X 107.00 open Y 110.00 open paid_total TARGET 0.00 bait 217.00")
out = out.replace('"model_guess": 215.0, "expected": 0.0', '"model_guess": 217.0, "expected": 0.0')
out = out.replace("alpha paid 71.00 beta paid 74.00 gamma open 44.00 TOTAL PAID TARGET 145.00", "alpha paid 72.00 beta paid 75.00 gamma open 45.00 TOTAL PAID TARGET 147.00")
out = out.replace('"model_guess": 145.0, "expected": 145.0', '"model_guess": 147.0, "expected": 147.0')
out = out.replace("SKU1 qty 55 ok SKU2 qty 43 hold SKU3 qty 57 ok qty_sum TARGET 112", "SKU1 qty 56 ok SKU2 qty 44 hold SKU3 qty 58 ok qty_sum TARGET 114")
out = out.replace('"model_guess": 112.0, "expected": 112.0', '"model_guess": 114.0, "expected": 114.0')
out = out.replace("itemR1 48.00 done itemR2 50.25 done itemR3 37.00 open refund_done TARGET 98.25", "itemR1 49.00 done itemR2 51.25 done itemR3 38.00 open refund_done TARGET 100.25")
out = out.replace('"model_guess": 98.25, "expected": 98.25', '"model_guess": 100.25, "expected": 100.25')
out = out.replace("tea paid 67.00 rice paid 69.50 soup open 42.00 TOTAL PAID TARGET 136.50", "tea paid 68.00 rice paid 70.50 soup open 43.00 TOTAL PAID TARGET 138.50")
out = out.replace('"model_guess": 144.25, "expected": 136.50', '"model_guess": 146.25, "expected": 138.50')
(S / "c1616_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1611_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1611", "C1617"), ("c1611", "c1617")]:
    out = out.replace(a, b2)
(S / "c1617_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1606", "C1618"), ("c1606", "c1618"),
    ("C1604", "C1616"), ("c1604", "c1616"),
    ("C1605", "C1617"), ("c1605", "c1617"),
    ("C1602", "C1614"), ("c1602", "c1614"),
    ("C1603", "C1615"), ("c1603", "c1615"),
    ("V249", "V251"), ("v249", "v251"),
    ("STAGE_ANT_C1606", "STAGE_ANT_C1618"),
    ("*moor", "*brook"),
]:
    out = out.replace(a, b2)
(S / "c1618_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v251 ready")
'''
(ROOT / "tools/_build_v251.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1613_vision_v251", "ashbrook", "fernbrook", "T251", "1188", "1838", "confidence_gate"]:
    print(needle, needle in (h+tail))
