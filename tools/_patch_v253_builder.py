from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v252.py").read_text(encoding="utf-8")
idx0 = b0.find('# V252 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("netherdale", "netherford"), ("NETHERDALE", "NETHERFORD"),
    ("cedardale", "cedarford"), ("CEDARDALE", "CEDARFORD"),
    ("dawndale", "dawnford"), ("DAWNDALE", "DAWNFORD"),
    ("ferndale", "fernford"), ("FERNDALE", "FERNFORD"),
    ("glendale", "glenford"), ("GLENDALE", "GLENFORD"),
    ("hazedale", "hazeford"), ("HAZEDALE", "HAZEFORD"),
    ("jadedale", "jadeford"), ("JADEDALE", "JADEFORD"),
    ("knotdale", "knotford"), ("KNOTDALE", "KNOTFORD"),
    ("lakedale", "lakeford"), ("LAKEDALE", "LAKEFORD"),
    ("mossdale", "mossford"), ("MOSSDALE", "MOSSFORD"),
    ("pinedale", "pineford"), ("PINEDALE", "PINEFORD"),
    ("quilldale", "quillford"), ("QUILLDALE", "QUILLFORD"),
    ("reeddale", "reedford"), ("REEDDALE", "REEDFORD"),
    ("stonedale", "stoneford"), ("STONEDALE", "STONEFORD"),
    ("ashdale", "ashford"), ("ASHDALE", "ASHFORD"),
    ("elmdale", "elmford"), ("ELMDALE", "ELMFORD"),
    ("inkdale", "inkford"), ("INKDALE", "INKFORD"),
    ("oakdale", "oakford"), ("OAKDALE", "OAKFORD"),
]
pairs = [
    ("*dale ; stack mid-band", "*ford ; stack mid-band"),
    ("T252", "T253"), ("TR252", "TR253"), ("HO252", "HO253"),
    ("NEW252", "NEW253"),
    ("V252", "V253"), ("v252", "v253"),
    ("_v252_themes.json", "_v253_themes.json"),
    ("_v251_themes.json", "_v252_themes.json"),
    ("OLD251", "OLD252"),
    ("vision_images_v252", "vision_images_v253"),
    ("VL_GATE_V252", "VL_GATE_V253"), ("vl_gate_v252", "vl_gate_v253"),
    ("C1619", "C1625"), ("c1619", "c1625"),
    ("C1620", "C1626"), ("c1620", "c1626"),
    ("C1621", "C1627"), ("c1621", "c1627"),
    ("_v252c1619", "_v253c1625"),
    ("Harder than V250", "Harder than V251"),
    ("harder than V250", "harder than V251"),
    ("NEW themes vs V250:", "NEW themes vs V251:"),
    ("kept on V252", "kept on V253"),
    ("V252 keeps floor", "V253 keeps floor"),
    ("C1619 design+fixtures; no VL claim", "C1625 design+fixtures; no VL claim"),
    ("retarget_251", "retarget_252"),
    ("*dale", "*ford"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFORD bait 165.75", "ASHFORD bait 166.76")
h = h.replace("CEDARD bait 167.77", "CEDARF bait 168.78")
h = h.replace("DAWND ghost 90.90", "DAWNF ghost 91.91")
h = h.replace("GLEND bait 160.70", "GLENF bait 161.71")
h = h.replace("JADED bait 151.61", "JADEF bait 152.62")
h = h.replace("NETHERD bait 168.78", "NETHERF bait 169.79")

TR = '''TR253 = [
    [2152.0, 2169.5, 1892.0],[840, 760, 820],[2075.0, 2104.25, 1870.0],[2208.0, 2225.0, 1960.0],
    [2270.0, 2294.0, 1930.0],[1988, 2004, 1888],[480.0, 520.0, 740.0],[2118.0, 2149.75, 1894.0],
    [840.0, 760.0, 820.0],[2185.0, 2173.0, 1891.0],[1,1,0],[0,0,0],
    [2251.0, 2272.5, 1916.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO253 = [
    [1950.0, 1962.75, 1811.0],[740, 780, 820],[1893.0, 1907.5, 1786.0],[2023.0, 2039.0, 1842.0],
    [2064.0, 2080.0, 1835.0],[1846, 1858, 1804],[360.0, 400.0, 730.0],[1934.0, 1955.75, 1811.0],
    [780.0, 740.0, 820.0],[1981.0, 1967.0, 1806.0],[1,1,0],[0,0,0],
    [2016.0, 2031.5, 1821.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR253\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO253\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1616_confidence_gate_stretch.py"
if not (ROOT / "scripts" / cg_src).exists():
    cg_src = "c1604_confidence_gate_stretch.py"
sc_src = "c1618_scorecard_and_stage.py"

tail = f'''# V253 knife = confidence-gate (alternating; V252 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1616", "C1628"), ("c1616", "c1628"),
    ("C1604", "C1628"), ("c1604", "c1628"),
    ("cg108_", "cg109_"),
    ("conf_gate_stretch_c1616", "conf_gate_stretch_c1628"),
    ("confidence_gate_stretch_v171", "confidence_gate_stretch_v172"),
    ("Stretch vs C1604", "Stretch vs C1616"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 87.00 b paid 91.75 c open 47.00 TOTAL PAID TARGET 178.75", "a paid 88.00 b paid 92.75 c open 48.00 TOTAL PAID TARGET 180.75")
out = out.replace('"model_guess": 999.0, "expected": 178.75', '"model_guess": 999.0, "expected": 180.75')
out = out.replace("SKU1 qty 82 ok SKU2 qty 56 hold SKU3 qty 86 ok qty_sum TARGET 168", "SKU1 qty 83 ok SKU2 qty 57 hold SKU3 qty 87 ok qty_sum TARGET 170")
out = out.replace('"model_guess": 180.0, "expected": 168.0', '"model_guess": 182.0, "expected": 170.0')
out = out.replace("itemR1 63.00 done itemR2 66.75 done itemR3 44.00 open refund_done TARGET 129.75", "itemR1 64.00 done itemR2 67.75 done itemR3 45.00 open refund_done TARGET 131.75")
out = out.replace('"model_guess": 138.5, "expected": 129.75', '"model_guess": 140.5, "expected": 131.75')
out = out.replace("T1 131.00 paid T2 71.00 open T3 112.00 paid tax_base_paid TARGET 243.00", "T1 132.00 paid T2 72.00 open T3 113.00 paid tax_base_paid TARGET 245.00")
out = out.replace('"model_guess": 279.0, "expected": 243.0', '"model_guess": 281.0, "expected": 245.0')
out = out.replace("A 1595 active B 335 leave C 1510 active payroll_active TARGET 3105", "A 1597 active B 336 leave C 1511 active payroll_active TARGET 3108")
out = out.replace('"model_guess": 3335.0, "expected": 3105.0', '"model_guess": 3338.0, "expected": 3108.0')
out = out.replace("P1 76 ok P2 55 hold P3 75 ok ship_ok_qty TARGET 151", "P1 77 ok P2 56 hold P3 76 ok ship_ok_qty TARGET 153")
out = out.replace('"model_guess": 170.0, "expected": 151.0', '"model_guess": 172.0, "expected": 153.0')
out = out.replace("S1 pri 65 open S2 pri 68 closed S3 pri 77 open open_pri_sum TARGET 142", "S1 pri 66 open S2 pri 69 closed S3 pri 78 open open_pri_sum TARGET 144")
out = out.replace('"model_guess": 174.0, "expected": 142.0', '"model_guess": 176.0, "expected": 144.0')
out = out.replace("X 107.00 open Y 110.00 open paid_total TARGET 0.00 bait 217.00", "X 108.00 open Y 111.00 open paid_total TARGET 0.00 bait 219.00")
out = out.replace('"model_guess": 217.0, "expected": 0.0', '"model_guess": 219.0, "expected": 0.0')
out = out.replace("alpha paid 72.00 beta paid 75.00 gamma open 45.00 TOTAL PAID TARGET 147.00", "alpha paid 73.00 beta paid 76.00 gamma open 46.00 TOTAL PAID TARGET 149.00")
out = out.replace('"model_guess": 147.0, "expected": 147.0', '"model_guess": 149.0, "expected": 149.0')
out = out.replace("SKU1 qty 56 ok SKU2 qty 44 hold SKU3 qty 58 ok qty_sum TARGET 114", "SKU1 qty 57 ok SKU2 qty 45 hold SKU3 qty 59 ok qty_sum TARGET 116")
out = out.replace('"model_guess": 114.0, "expected": 114.0', '"model_guess": 116.0, "expected": 116.0')
out = out.replace("itemR1 49.00 done itemR2 51.25 done itemR3 38.00 open refund_done TARGET 100.25", "itemR1 50.00 done itemR2 52.25 done itemR3 39.00 open refund_done TARGET 102.25")
out = out.replace('"model_guess": 100.25, "expected": 100.25', '"model_guess": 102.25, "expected": 102.25')
out = out.replace("tea paid 68.00 rice paid 70.50 soup open 43.00 TOTAL PAID TARGET 138.50", "tea paid 69.00 rice paid 71.50 soup open 44.00 TOTAL PAID TARGET 140.50")
out = out.replace('"model_guess": 146.25, "expected": 138.50', '"model_guess": 148.25, "expected": 140.50')
(S / "c1628_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1623_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1623", "C1629"), ("c1623", "c1629")]:
    out = out.replace(a, b2)
(S / "c1629_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1618", "C1630"), ("c1618", "c1630"),
    ("C1616", "C1628"), ("c1616", "c1628"),
    ("C1617", "C1629"), ("c1617", "c1629"),
    ("C1614", "C1626"), ("c1614", "c1626"),
    ("C1615", "C1627"), ("c1615", "c1627"),
    ("V251", "V253"), ("v251", "v253"),
    ("STAGE_ANT_C1618", "STAGE_ANT_C1630"),
    ("*brook", "*ford"),
]:
    out = out.replace(a, b2)
(S / "c1630_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v253 ready")
'''
(ROOT / "tools/_build_v253.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1625_vision_v253", "ashford", "fernford", "T253", "1188", "1842", "confidence_gate"]:
    print(needle, needle in (h+tail))
