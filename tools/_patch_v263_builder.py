from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v262.py").read_text(encoding="utf-8")
idx0 = b0.find('# V262 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("netherbrook", "netherdale"), ("NETHERBROOK", "NETHERDALE"),
    ("cedarbrook", "cedardale"), ("CEDARBROOK", "CEDARDALE"),
    ("dawnbrook", "dawndale"), ("DAWNBROOK", "DAWNDALE"),
    ("fernbrook", "ferndale"), ("FERNBROOK", "FERNDALE"),
    ("glenbrook", "glendale"), ("GLENBROOK", "GLENDALE"),
    ("hazebrook", "hazedale"), ("HAZEBROOK", "HAZEDALE"),
    ("jadebrook", "jadedale"), ("JADEBROOK", "JADEDALE"),
    ("knotbrook", "knotdale"), ("KNOTBROOK", "KNOTDALE"),
    ("lakebrook", "lakedale"), ("LAKEBROOK", "LAKEDALE"),
    ("mossbrook", "mossdale"), ("MOSSBROOK", "MOSSDALE"),
    ("pinebrook", "pinedale"), ("PINEBROOK", "PINEDALE"),
    ("quillbrook", "quilldale"), ("QUILLBROOK", "QUILLDALE"),
    ("reedbrook", "reeddale"), ("REEDBROOK", "REEDDALE"),
    ("stonebrook", "stonedale"), ("STONEBROOK", "STONEDALE"),
    ("ashbrook", "ashdale"), ("ASHBROOK", "ASHDALE"),
    ("elmbrook", "elmdale"), ("ELMBROOK", "ELMDALE"),
    ("inkbrook", "inkdale"), ("INKBROOK", "INKDALE"),
    ("oakbrook", "oakdale"), ("OAKBROOK", "OAKDALE"),
]
pairs = [
    ("*brook ; stack mid-band", "*dale ; stack mid-band"),
    ("T262", "T263"), ("TR262", "TR263"), ("HO262", "HO263"),
    ("NEW262", "NEW263"),
    ("V262", "V263"), ("v262", "v263"),
    ("_v262_themes.json", "_v263_themes.json"),
    ("_v261_themes.json", "_v262_themes.json"),
    ("OLD261", "OLD262"),
    ("vision_images_v262", "vision_images_v263"),
    ("VL_GATE_V262", "VL_GATE_V263"), ("vl_gate_v262", "vl_gate_v263"),
    ("C1679", "C1685"), ("c1679", "c1685"),
    ("C1680", "C1686"), ("c1680", "c1686"),
    ("C1681", "C1687"), ("c1681", "c1687"),
    ("_v262c1679", "_v263c1685"),
    ("Harder than V260", "Harder than V261"),
    ("harder than V260", "harder than V261"),
    ("NEW themes vs V260:", "NEW themes vs V261:"),
    ("kept on V262", "kept on V263"),
    ("V262 keeps floor", "V263 keeps floor"),
    ("C1679 design+fixtures; no VL claim", "C1685 design+fixtures; no VL claim"),
    ("retarget_261", "retarget_262"),
    ("*brook", "*dale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHDALE bait 175.85", "ASHDALE bait 176.86")
h = h.replace("CEDARB bait 177.87", "CEDARD bait 178.88")
h = h.replace("DAWNB ghost 100.10", "DAWND ghost 101.11")
h = h.replace("GLENB bait 170.80", "GLEND bait 171.81")
h = h.replace("JADEB bait 161.71", "JADED bait 162.72")
h = h.replace("NETHERB bait 178.88", "NETHERD bait 179.89")

TR = '''TR263 = [
    [2172.0, 2189.5, 1912.0],[840, 760, 820],[2095.0, 2124.25, 1890.0],[2228.0, 2245.0, 1980.0],
    [2290.0, 2314.0, 1950.0],[2008, 2024, 1908],[480.0, 520.0, 740.0],[2138.0, 2169.75, 1914.0],
    [840.0, 760.0, 820.0],[2205.0, 2193.0, 1911.0],[1,1,0],[0,0,0],
    [2271.0, 2292.5, 1936.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO263 = [
    [1970.0, 1982.75, 1831.0],[740, 780, 820],[1913.0, 1927.5, 1806.0],[2043.0, 2059.0, 1862.0],
    [2084.0, 2100.0, 1855.0],[1866, 1878, 1824],[360.0, 400.0, 730.0],[1954.0, 1975.75, 1831.0],
    [780.0, 740.0, 820.0],[2001.0, 1987.0, 1826.0],[1,1,0],[0,0,0],
    [2036.0, 2051.5, 1841.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR263\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO263\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1676_confidence_gate_stretch.py"
if not (ROOT / "scripts" / cg_src).exists():
    cg_src = "c1664_confidence_gate_stretch.py"
sc_src = "c1678_scorecard_and_stage.py"

tail = f'''# V263 knife = confidence-gate (alternating; V262 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1676", "C1688"), ("c1676", "c1688"),
    ("C1664", "C1688"), ("c1664", "c1688"),
    ("cg113_", "cg114_"),
    ("conf_gate_stretch_c1676", "conf_gate_stretch_c1688"),
    ("confidence_gate_stretch_v176", "confidence_gate_stretch_v177"),
    ("Stretch vs C1664", "Stretch vs C1676"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 92.00 b paid 96.75 c open 52.00 TOTAL PAID TARGET 188.75", "a paid 93.00 b paid 97.75 c open 53.00 TOTAL PAID TARGET 190.75")
out = out.replace('"model_guess": 999.0, "expected": 188.75', '"model_guess": 999.0, "expected": 190.75')
out = out.replace("SKU1 qty 87 ok SKU2 qty 61 hold SKU3 qty 91 ok qty_sum TARGET 178", "SKU1 qty 88 ok SKU2 qty 62 hold SKU3 qty 92 ok qty_sum TARGET 180")
out = out.replace('"model_guess": 190.0, "expected": 178.0', '"model_guess": 192.0, "expected": 180.0')
out = out.replace("itemR1 68.00 done itemR2 71.75 done itemR3 49.00 open refund_done TARGET 139.75", "itemR1 69.00 done itemR2 72.75 done itemR3 50.00 open refund_done TARGET 141.75")
out = out.replace('"model_guess": 148.5, "expected": 139.75', '"model_guess": 150.5, "expected": 141.75')
out = out.replace("T1 136.00 paid T2 76.00 open T3 117.00 paid tax_base_paid TARGET 253.00", "T1 137.00 paid T2 77.00 open T3 118.00 paid tax_base_paid TARGET 255.00")
out = out.replace('"model_guess": 289.0, "expected": 253.0', '"model_guess": 291.0, "expected": 255.0')
out = out.replace("A 1605 active B 340 leave C 1515 active payroll_active TARGET 3120", "A 1607 active B 341 leave C 1516 active payroll_active TARGET 3123")
out = out.replace('"model_guess": 3350.0, "expected": 3120.0', '"model_guess": 3353.0, "expected": 3123.0')
out = out.replace("P1 81 ok P2 60 hold P3 80 ok ship_ok_qty TARGET 161", "P1 82 ok P2 61 hold P3 81 ok ship_ok_qty TARGET 163")
out = out.replace('"model_guess": 180.0, "expected": 161.0', '"model_guess": 182.0, "expected": 163.0')
out = out.replace("S1 pri 70 open S2 pri 73 closed S3 pri 82 open open_pri_sum TARGET 152", "S1 pri 71 open S2 pri 74 closed S3 pri 83 open open_pri_sum TARGET 154")
out = out.replace('"model_guess": 184.0, "expected": 152.0', '"model_guess": 186.0, "expected": 154.0')
out = out.replace("X 112.00 open Y 115.00 open paid_total TARGET 0.00 bait 227.00", "X 113.00 open Y 116.00 open paid_total TARGET 0.00 bait 229.00")
out = out.replace('"model_guess": 227.0, "expected": 0.0', '"model_guess": 229.0, "expected": 0.0')
out = out.replace("alpha paid 77.00 beta paid 80.00 gamma open 50.00 TOTAL PAID TARGET 157.00", "alpha paid 78.00 beta paid 81.00 gamma open 51.00 TOTAL PAID TARGET 159.00")
out = out.replace('"model_guess": 157.0, "expected": 157.0', '"model_guess": 159.0, "expected": 159.0')
out = out.replace("SKU1 qty 61 ok SKU2 qty 49 hold SKU3 qty 63 ok qty_sum TARGET 124", "SKU1 qty 62 ok SKU2 qty 50 hold SKU3 qty 64 ok qty_sum TARGET 126")
out = out.replace('"model_guess": 124.0, "expected": 124.0', '"model_guess": 126.0, "expected": 126.0')
out = out.replace("itemR1 54.00 done itemR2 56.25 done itemR3 43.00 open refund_done TARGET 110.25", "itemR1 55.00 done itemR2 57.25 done itemR3 44.00 open refund_done TARGET 112.25")
out = out.replace('"model_guess": 110.25, "expected": 110.25', '"model_guess": 112.25, "expected": 112.25')
out = out.replace("tea paid 73.00 rice paid 75.50 soup open 48.00 TOTAL PAID TARGET 148.50", "tea paid 74.00 rice paid 76.50 soup open 49.00 TOTAL PAID TARGET 150.50")
out = out.replace('"model_guess": 156.25, "expected": 148.50', '"model_guess": 158.25, "expected": 150.50')
(S / "c1688_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1683_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1683", "C1689"), ("c1683", "c1689")]:
    out = out.replace(a, b2)
(S / "c1689_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1678", "C1690"), ("c1678", "c1690"),
    ("C1676", "C1688"), ("c1676", "c1688"),
    ("C1677", "C1689"), ("c1677", "c1689"),
    ("C1674", "C1686"), ("c1674", "c1686"),
    ("C1675", "C1687"), ("c1675", "c1687"),
    ("V261", "V263"), ("v261", "v263"),
    ("STAGE_ANT_C1678", "STAGE_ANT_C1690"),
    ("*fen", "*dale"),
]:
    out = out.replace(a, b2)
(S / "c1690_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v263 ready")
'''
(ROOT / "tools/_build_v263.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1685_vision_v263", "ashdale", "ferndale", "T263", "1188", "1862", "confidence_gate"]:
    print(needle, needle in (h+tail))
