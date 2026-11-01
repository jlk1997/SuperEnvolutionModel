from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v284.py").read_text(encoding="utf-8")
idx0 = b0.find('# V284 knife = product-U2C')
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
    ("T284", "T285"), ("TR284", "TR285"), ("HO284", "HO285"),
    ("NEW284", "NEW285"),
    ("V284", "V285"), ("v284", "v285"),
    ("_v284_themes.json", "_v285_themes.json"),
    ("_v283_themes.json", "_v284_themes.json"),
    ("OLD283", "OLD284"),
    ("vision_images_v284", "vision_images_v285"),
    ("VL_GATE_V284", "VL_GATE_V285"), ("vl_gate_v284", "vl_gate_v285"),
    ("C1811", "C1817"), ("c1811", "c1817"),
    ("C1812", "C1818"), ("c1812", "c1818"),
    ("C1813", "C1819"), ("c1813", "c1819"),
    ("_v284c1811", "_v285c1817"),
    ("Harder than V282", "Harder than V283"),
    ("harder than V282", "harder than V283"),
    ("NEW themes vs V282:", "NEW themes vs V283:"),
    ("kept on V284", "kept on V285"),
    ("V284 keeps floor", "V285 keeps floor"),
    ("C1811 design+fixtures; no VL claim", "C1817 design+fixtures; no VL claim"),
    ("retarget_283", "retarget_284"),
    ("*brook", "*dale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHBROOK bait 197.07", "ASHDALE bait 198.08")
h = h.replace("CEDARB bait 199.09", "CEDARD bait 200.10")
h = h.replace("DAWNB ghost 122.32", "DAWND ghost 123.33")
h = h.replace("GLENB bait 192.02", "GLEND bait 193.03")
h = h.replace("JADEB bait 183.93", "JADED bait 184.94")
h = h.replace("NETHERB bait 200.10", "NETHERD bait 201.11")

TR = '''TR285 = [
    [2230.0, 2247.5, 1970.0],[840, 760, 820],[2153.0, 2182.25, 1948.0],[2286.0, 2303.0, 2038.0],
    [2348.0, 2372.0, 2008.0],[2066, 2082, 1966],[490.0, 530.0, 760.0],[2196.0, 2227.75, 1972.0],
    [840.0, 760.0, 820.0],[2263.0, 2251.0, 1969.0],[1,1,0],[0,0,0],
    [2329.0, 2350.5, 1994.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO285 = [
    [2028.0, 2040.75, 1889.0],[640, 660, 820],[1971.0, 1985.5, 1864.0],[2101.0, 2117.0, 1920.0],
    [2142.0, 2158.0, 1913.0],[1924, 1936, 1884],[420.0, 460.0, 740.0],[2012.0, 2033.75, 1889.0],
    [740.0, 780.0, 820.0],[2059.0, 2045.0, 1886.0],[1,1,0],[0,0,0],
    [2094.0, 2109.5, 1899.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR285\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO285\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1808_confidence_gate_stretch.py"
sc_src = "c1810_scorecard_and_stage.py"

tail = f'''# V285 knife = confidence-gate (alternating; V284 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1808", "C1820"), ("c1808", "c1820"),
    ("C1796", "C1820"), ("c1796", "c1820"),
    ("cg124_", "cg125_"),
    ("conf_gate_stretch_c1808", "conf_gate_stretch_c1820"),
    ("confidence_gate_stretch_v187", "confidence_gate_stretch_v188"),
    ("Stretch vs C1796", "Stretch vs C1808"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 103.00 b paid 107.75 c open 63.00 TOTAL PAID TARGET 210.75", "a paid 104.00 b paid 108.75 c open 64.00 TOTAL PAID TARGET 212.75")
out = out.replace('"model_guess": 999.0, "expected": 210.75', '"model_guess": 999.0, "expected": 212.75')
out = out.replace("SKU1 qty 98 ok SKU2 qty 72 hold SKU3 qty 102 ok qty_sum TARGET 200", "SKU1 qty 99 ok SKU2 qty 73 hold SKU3 qty 103 ok qty_sum TARGET 202")
out = out.replace('"model_guess": 212.0, "expected": 200.0', '"model_guess": 214.0, "expected": 202.0')
out = out.replace("itemR1 79.00 done itemR2 82.75 done itemR3 60.00 open refund_done TARGET 161.75", "itemR1 80.00 done itemR2 83.75 done itemR3 61.00 open refund_done TARGET 163.75")
out = out.replace('"model_guess": 170.5, "expected": 161.75', '"model_guess": 172.5, "expected": 163.75')
out = out.replace("T1 147.00 paid T2 87.00 open T3 128.00 paid tax_base_paid TARGET 275.00", "T1 148.00 paid T2 88.00 open T3 129.00 paid tax_base_paid TARGET 277.00")
out = out.replace('"model_guess": 311.0, "expected": 275.0', '"model_guess": 313.0, "expected": 277.0')
out = out.replace("A 1627 active B 351 leave C 1526 active payroll_active TARGET 3153", "A 1629 active B 352 leave C 1527 active payroll_active TARGET 3156")
out = out.replace('"model_guess": 3383.0, "expected": 3153.0', '"model_guess": 3386.0, "expected": 3156.0')
out = out.replace("P1 92 ok P2 71 hold P3 91 ok ship_ok_qty TARGET 183", "P1 93 ok P2 72 hold P3 92 ok ship_ok_qty TARGET 185")
out = out.replace('"model_guess": 202.0, "expected": 183.0', '"model_guess": 204.0, "expected": 185.0')
out = out.replace("S1 pri 81 open S2 pri 84 closed S3 pri 93 open open_pri_sum TARGET 174", "S1 pri 82 open S2 pri 85 closed S3 pri 94 open open_pri_sum TARGET 176")
out = out.replace('"model_guess": 206.0, "expected": 174.0', '"model_guess": 208.0, "expected": 176.0')
out = out.replace("X 123.00 open Y 126.00 open paid_total TARGET 0.00 bait 249.00", "X 124.00 open Y 127.00 open paid_total TARGET 0.00 bait 251.00")
out = out.replace('"model_guess": 249.0, "expected": 0.0', '"model_guess": 251.0, "expected": 0.0')
out = out.replace("alpha paid 88.00 beta paid 91.00 gamma open 61.00 TOTAL PAID TARGET 179.00", "alpha paid 89.00 beta paid 92.00 gamma open 62.00 TOTAL PAID TARGET 181.00")
out = out.replace('"model_guess": 179.0, "expected": 179.0', '"model_guess": 181.0, "expected": 181.0')
out = out.replace("SKU1 qty 72 ok SKU2 qty 60 hold SKU3 qty 74 ok qty_sum TARGET 146", "SKU1 qty 73 ok SKU2 qty 61 hold SKU3 qty 75 ok qty_sum TARGET 148")
out = out.replace('"model_guess": 146.0, "expected": 146.0', '"model_guess": 148.0, "expected": 148.0')
out = out.replace("itemR1 65.00 done itemR2 67.25 done itemR3 54.00 open refund_done TARGET 132.25", "itemR1 66.00 done itemR2 68.25 done itemR3 55.00 open refund_done TARGET 134.25")
out = out.replace('"model_guess": 132.25, "expected": 132.25', '"model_guess": 134.25, "expected": 134.25')
out = out.replace("tea paid 84.00 rice paid 86.50 soup open 59.00 TOTAL PAID TARGET 170.50", "tea paid 85.00 rice paid 87.50 soup open 60.00 TOTAL PAID TARGET 172.50")
out = out.replace('"model_guess": 178.25, "expected": 170.50', '"model_guess": 180.25, "expected": 172.50')
(S / "c1820_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1815_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1815", "C1821"), ("c1815", "c1821")]:
    out = out.replace(a, b2)
(S / "c1821_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1810", "C1822"), ("c1810", "c1822"),
    ("C1808", "C1820"), ("c1808", "c1820"),
    ("C1809", "C1821"), ("c1809", "c1821"),
    ("C1806", "C1818"), ("c1806", "c1818"),
    ("C1807", "C1819"), ("c1807", "c1819"),
    ("V283", "V285"), ("v283", "v285"),
    ("STAGE_ANT_C1810", "STAGE_ANT_C1822"),
    ("*fen", "*dale"),
]:
    out = out.replace(a, b2)
(S / "c1822_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v285 ready")
'''
(ROOT / "tools/_build_v285.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1817_vision_v285", "ashdale", "ferndale", "T285", "1188", "1884", "confidence_gate", "retarget_284"]:
    print(needle, needle in (h+tail))
