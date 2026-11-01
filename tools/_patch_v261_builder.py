from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v260.py").read_text(encoding="utf-8")
idx0 = b0.find('# V260 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("nethermoor", "netherfen"), ("NETHERMOOR", "NETHERFEN"),
    ("cedarmoor", "cedarfen"), ("CEDARMOOR", "CEDARFEN"),
    ("dawnmoor", "dawnfen"), ("DAWNMOOR", "DAWNFEN"),
    ("fernmoor", "fernfen"), ("FERNMOOR", "FERNFEN"),
    ("glenmoor", "glenfen"), ("GLENMOOR", "GLENFEN"),
    ("hazemoor", "hazefen"), ("HAZEMOOR", "HAZEFEN"),
    ("jademoor", "jadefen"), ("JADEMOOR", "JADEFEN"),
    ("knotmoor", "knotfen"), ("KNOTMOOR", "KNOTFEN"),
    ("lakemoor", "lakefen"), ("LAKEMOOR", "LAKEFEN"),
    ("mossmoor", "mossfen"), ("MOSSMOOR", "MOSSFEN"),
    ("pinemoor", "pinefen"), ("PINEMOOR", "PINEFEN"),
    ("quillmoor", "quillfen"), ("QUILLMOOR", "QUILLFEN"),
    ("reedmoor", "reedfen"), ("REEDMOOR", "REEDFEN"),
    ("stonemoor", "stonefen"), ("STONEMOOR", "STONEFEN"),
    ("ashmoor", "ashfen"), ("ASHMOOR", "ASHFEN"),
    ("elmmoor", "elmfen"), ("ELMMOOR", "ELMFEN"),
    ("inkmoor", "inkfen"), ("INKMOOR", "INKFEN"),
    ("oakmoor", "oakfen"), ("OAKMOOR", "OAKFEN"),
]
pairs = [
    ("*moor ; stack mid-band", "*fen ; stack mid-band"),
    ("T260", "T261"), ("TR260", "TR261"), ("HO260", "HO261"),
    ("NEW260", "NEW261"),
    ("V260", "V261"), ("v260", "v261"),
    ("_v260_themes.json", "_v261_themes.json"),
    ("_v259_themes.json", "_v260_themes.json"),
    ("OLD259", "OLD260"),
    ("vision_images_v260", "vision_images_v261"),
    ("VL_GATE_V260", "VL_GATE_V261"), ("vl_gate_v260", "vl_gate_v261"),
    ("C1667", "C1673"), ("c1667", "c1673"),
    ("C1668", "C1674"), ("c1668", "c1674"),
    ("C1669", "C1675"), ("c1669", "c1675"),
    ("_v260c1667", "_v261c1673"),
    ("Harder than V258", "Harder than V259"),
    ("harder than V258", "harder than V259"),
    ("NEW themes vs V258:", "NEW themes vs V259:"),
    ("kept on V260", "kept on V261"),
    ("V260 keeps floor", "V261 keeps floor"),
    ("C1667 design+fixtures; no VL claim", "C1673 design+fixtures; no VL claim"),
    ("retarget_259", "retarget_260"),
    ("*moor", "*fen"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFEN bait 173.83", "ASHFEN bait 174.84")
h = h.replace("CEDARM bait 175.85", "CEDARF bait 176.86")
h = h.replace("DAWNM ghost 98.98", "DAWNF ghost 99.99")
h = h.replace("GLENM bait 168.78", "GLENF bait 169.79")
h = h.replace("JADEM bait 159.69", "JADEF bait 160.70")
h = h.replace("NETHERM bait 176.86", "NETHERF bait 177.87")

TR = '''TR261 = [
    [2168.0, 2185.5, 1908.0],[840, 760, 820],[2091.0, 2120.25, 1886.0],[2224.0, 2241.0, 1976.0],
    [2286.0, 2310.0, 1946.0],[2004, 2020, 1904],[480.0, 520.0, 740.0],[2134.0, 2165.75, 1910.0],
    [840.0, 760.0, 820.0],[2201.0, 2189.0, 1907.0],[1,1,0],[0,0,0],
    [2267.0, 2288.5, 1932.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO261 = [
    [1966.0, 1978.75, 1827.0],[740, 780, 820],[1909.0, 1923.5, 1802.0],[2039.0, 2055.0, 1858.0],
    [2080.0, 2096.0, 1851.0],[1862, 1874, 1820],[360.0, 400.0, 730.0],[1950.0, 1971.75, 1827.0],
    [780.0, 740.0, 820.0],[1997.0, 1983.0, 1822.0],[1,1,0],[0,0,0],
    [2032.0, 2047.5, 1837.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR261\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO261\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1664_confidence_gate_stretch.py"
if not (ROOT / "scripts" / cg_src).exists():
    cg_src = "c1652_confidence_gate_stretch.py"
sc_src = "c1666_scorecard_and_stage.py"

tail = f'''# V261 knife = confidence-gate (alternating; V260 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1664", "C1676"), ("c1664", "c1676"),
    ("C1652", "C1676"), ("c1652", "c1676"),
    ("cg112_", "cg113_"),
    ("conf_gate_stretch_c1664", "conf_gate_stretch_c1676"),
    ("confidence_gate_stretch_v175", "confidence_gate_stretch_v176"),
    ("Stretch vs C1652", "Stretch vs C1664"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 91.00 b paid 95.75 c open 51.00 TOTAL PAID TARGET 186.75", "a paid 92.00 b paid 96.75 c open 52.00 TOTAL PAID TARGET 188.75")
out = out.replace('"model_guess": 999.0, "expected": 186.75', '"model_guess": 999.0, "expected": 188.75')
out = out.replace("SKU1 qty 86 ok SKU2 qty 60 hold SKU3 qty 90 ok qty_sum TARGET 176", "SKU1 qty 87 ok SKU2 qty 61 hold SKU3 qty 91 ok qty_sum TARGET 178")
out = out.replace('"model_guess": 188.0, "expected": 176.0', '"model_guess": 190.0, "expected": 178.0')
out = out.replace("itemR1 67.00 done itemR2 70.75 done itemR3 48.00 open refund_done TARGET 137.75", "itemR1 68.00 done itemR2 71.75 done itemR3 49.00 open refund_done TARGET 139.75")
out = out.replace('"model_guess": 146.5, "expected": 137.75', '"model_guess": 148.5, "expected": 139.75')
out = out.replace("T1 135.00 paid T2 75.00 open T3 116.00 paid tax_base_paid TARGET 251.00", "T1 136.00 paid T2 76.00 open T3 117.00 paid tax_base_paid TARGET 253.00")
out = out.replace('"model_guess": 287.0, "expected": 251.0', '"model_guess": 289.0, "expected": 253.0')
out = out.replace("A 1603 active B 339 leave C 1514 active payroll_active TARGET 3117", "A 1605 active B 340 leave C 1515 active payroll_active TARGET 3120")
out = out.replace('"model_guess": 3347.0, "expected": 3117.0', '"model_guess": 3350.0, "expected": 3120.0')
out = out.replace("P1 80 ok P2 59 hold P3 79 ok ship_ok_qty TARGET 159", "P1 81 ok P2 60 hold P3 80 ok ship_ok_qty TARGET 161")
out = out.replace('"model_guess": 178.0, "expected": 159.0', '"model_guess": 180.0, "expected": 161.0')
out = out.replace("S1 pri 69 open S2 pri 72 closed S3 pri 81 open open_pri_sum TARGET 150", "S1 pri 70 open S2 pri 73 closed S3 pri 82 open open_pri_sum TARGET 152")
out = out.replace('"model_guess": 182.0, "expected": 150.0', '"model_guess": 184.0, "expected": 152.0')
out = out.replace("X 111.00 open Y 114.00 open paid_total TARGET 0.00 bait 225.00", "X 112.00 open Y 115.00 open paid_total TARGET 0.00 bait 227.00")
out = out.replace('"model_guess": 225.0, "expected": 0.0', '"model_guess": 227.0, "expected": 0.0')
out = out.replace("alpha paid 76.00 beta paid 79.00 gamma open 49.00 TOTAL PAID TARGET 155.00", "alpha paid 77.00 beta paid 80.00 gamma open 50.00 TOTAL PAID TARGET 157.00")
out = out.replace('"model_guess": 155.0, "expected": 155.0', '"model_guess": 157.0, "expected": 157.0')
out = out.replace("SKU1 qty 60 ok SKU2 qty 48 hold SKU3 qty 62 ok qty_sum TARGET 122", "SKU1 qty 61 ok SKU2 qty 49 hold SKU3 qty 63 ok qty_sum TARGET 124")
out = out.replace('"model_guess": 122.0, "expected": 122.0', '"model_guess": 124.0, "expected": 124.0')
out = out.replace("itemR1 53.00 done itemR2 55.25 done itemR3 42.00 open refund_done TARGET 108.25", "itemR1 54.00 done itemR2 56.25 done itemR3 43.00 open refund_done TARGET 110.25")
out = out.replace('"model_guess": 108.25, "expected": 108.25', '"model_guess": 110.25, "expected": 110.25')
out = out.replace("tea paid 72.00 rice paid 74.50 soup open 47.00 TOTAL PAID TARGET 146.50", "tea paid 73.00 rice paid 75.50 soup open 48.00 TOTAL PAID TARGET 148.50")
out = out.replace('"model_guess": 154.25, "expected": 146.50', '"model_guess": 156.25, "expected": 148.50')
(S / "c1676_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1671_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1671", "C1677"), ("c1671", "c1677")]:
    out = out.replace(a, b2)
(S / "c1677_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1666", "C1678"), ("c1666", "c1678"),
    ("C1664", "C1676"), ("c1664", "c1676"),
    ("C1665", "C1677"), ("c1665", "c1677"),
    ("C1662", "C1674"), ("c1662", "c1674"),
    ("C1663", "C1675"), ("c1663", "c1675"),
    ("V259", "V261"), ("v259", "v261"),
    ("STAGE_ANT_C1666", "STAGE_ANT_C1678"),
    ("*wick", "*fen"),
]:
    out = out.replace(a, b2)
(S / "c1678_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v261 ready")
'''
(ROOT / "tools/_build_v261.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
if "fernfen" not in h and "FERNFEN" not in h:
    print("WARN fernfen missing")
else:
    print("fernfen ok")
for needle in ["c1673_vision_v261", "ashfen", "T261", "1188", "1858", "confidence_gate"]:
    print(needle, needle in (h+tail))
