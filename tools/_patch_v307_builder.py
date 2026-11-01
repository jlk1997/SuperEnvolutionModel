from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v306.py").read_text(encoding="utf-8")
idx0 = b0.find('# V306 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1948 = " in head0:
    head0 = head0[:head0.find("SC1948 = ")]

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
    ("T306", "T307"), ("TR306", "TR307"), ("HO306", "HO307"),
    ("NEW306", "NEW307"),
    ("V306", "V307"), ("v306", "v307"),
    ("_v306_themes.json", "_v307_themes.json"),
    ("_v305_themes.json", "_v306_themes.json"),
    ("OLD305", "OLD306"),
    ("vision_images_v306", "vision_images_v307"),
    ("VL_GATE_V306", "VL_GATE_V307"), ("vl_gate_v306", "vl_gate_v307"),
    ("C1943", "C1949"), ("c1943", "c1949"),
    ("C1944", "C1950"), ("c1944", "c1950"),
    ("C1945", "C1951"), ("c1945", "c1951"),
    ("_v306c1943", "_v307c1949"),
    ("Harder than V304", "Harder than V305"),
    ("harder than V304", "harder than V305"),
    ("NEW themes vs V304:", "NEW themes vs V305:"),
    ("kept on V306", "kept on V307"),
    ("V306 keeps floor", "V307 keeps floor"),
    ("C1943 design+fixtures; no VL claim", "C1949 design+fixtures; no VL claim"),
    ("retarget_305", "retarget_306"),
    ("*brook", "*dale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHBROOK bait 219.29", "ASHDALE bait 220.30")
h = h.replace("CEDARB bait 221.31", "CEDARD bait 222.32")
h = h.replace("DAWNB ghost 144.54", "DAWND ghost 145.55")
h = h.replace("GLENB bait 214.24", "GLEND bait 215.25")
h = h.replace("JADEB bait 205.15", "JADED bait 206.16")
h = h.replace("NETHERB bait 222.32", "NETHERD bait 223.33")

TR = '''TR307 = [
    [2278.0, 2295.5, 2018.0],[840, 760, 820],[2201.0, 2230.25, 1996.0],[2334.0, 2351.0, 2086.0],
    [2396.0, 2420.0, 2056.0],[2114, 2130, 2014],[490.0, 530.0, 760.0],[2244.0, 2275.75, 2020.0],
    [840.0, 760.0, 820.0],[2311.0, 2299.0, 2017.0],[1,1,0],[0,0,0],
    [2377.0, 2398.5, 2042.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO307 = [
    [2076.0, 2088.75, 1937.0],[640, 660, 820],[2019.0, 2033.5, 1912.0],[2149.0, 2165.0, 1968.0],
    [2190.0, 2206.0, 1961.0],[1972, 1984, 1932],[420.0, 460.0, 740.0],[2060.0, 2081.75, 1937.0],
    [740.0, 780.0, 820.0],[2107.0, 2093.0, 1934.0],[1,1,0],[0,0,0],
    [2142.0, 2157.5, 1947.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR307\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO307\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1940_confidence_gate_stretch.py"
sc_body = (ROOT / "scripts/c1942_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1942", "C1954"), ("c1942", "c1954"),
    ("C1940", "C1952"), ("c1940", "c1952"),
    ("C1941", "C1953"), ("c1941", "c1953"),
    ("C1938", "C1950"), ("c1938", "c1950"),
    ("C1939", "C1951"), ("c1939", "c1951"),
    ("V305", "V307"), ("v305", "v307"),
    ("STAGE_ANT_C1942", "STAGE_ANT_C1954"),
    ("*fen", "*dale"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V307 knife = confidence-gate (alternating; V306 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1940", "C1952"), ("c1940", "c1952"),
    ("C1928", "C1952"), ("c1928", "c1952"),
    ("cg135_", "cg136_"),
    ("conf_gate_stretch_c1940", "conf_gate_stretch_c1952"),
    ("confidence_gate_stretch_v198", "confidence_gate_stretch_v199"),
    ("Stretch vs C1928", "Stretch vs C1940"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 114.00 b paid 118.75 c open 74.00 TOTAL PAID TARGET 232.75", "a paid 115.00 b paid 119.75 c open 75.00 TOTAL PAID TARGET 234.75")
out = out.replace('"model_guess": 999.0, "expected": 232.75', '"model_guess": 999.0, "expected": 234.75')
out = out.replace("SKU1 qty 109 ok SKU2 qty 83 hold SKU3 qty 113 ok qty_sum TARGET 222", "SKU1 qty 110 ok SKU2 qty 84 hold SKU3 qty 114 ok qty_sum TARGET 224")
out = out.replace('"model_guess": 234.0, "expected": 222.0', '"model_guess": 236.0, "expected": 224.0')
out = out.replace("itemR1 90.00 done itemR2 93.75 done itemR3 71.00 open refund_done TARGET 183.75", "itemR1 91.00 done itemR2 94.75 done itemR3 72.00 open refund_done TARGET 185.75")
out = out.replace('"model_guess": 192.5, "expected": 183.75', '"model_guess": 194.5, "expected": 185.75')
out = out.replace("T1 158.00 paid T2 98.00 open T3 139.00 paid tax_base_paid TARGET 297.00", "T1 159.00 paid T2 99.00 open T3 140.00 paid tax_base_paid TARGET 299.00")
out = out.replace('"model_guess": 333.0, "expected": 297.0', '"model_guess": 335.0, "expected": 299.0')
out = out.replace("A 1649 active B 362 leave C 1537 active payroll_active TARGET 3186", "A 1651 active B 363 leave C 1538 active payroll_active TARGET 3189")
out = out.replace('"model_guess": 3416.0, "expected": 3186.0', '"model_guess": 3419.0, "expected": 3189.0')
out = out.replace("P1 103 ok P2 82 hold P3 102 ok ship_ok_qty TARGET 205", "P1 104 ok P2 83 hold P3 103 ok ship_ok_qty TARGET 207")
out = out.replace('"model_guess": 224.0, "expected": 205.0', '"model_guess": 226.0, "expected": 207.0')
out = out.replace("S1 pri 92 open S2 pri 95 closed S3 pri 104 open open_pri_sum TARGET 196", "S1 pri 93 open S2 pri 96 closed S3 pri 105 open open_pri_sum TARGET 198")
out = out.replace('"model_guess": 228.0, "expected": 196.0', '"model_guess": 230.0, "expected": 198.0')
out = out.replace("X 134.00 open Y 137.00 open paid_total TARGET 0.00 bait 271.00", "X 135.00 open Y 138.00 open paid_total TARGET 0.00 bait 273.00")
out = out.replace('"model_guess": 271.0, "expected": 0.0', '"model_guess": 273.0, "expected": 0.0')
out = out.replace("alpha paid 99.00 beta paid 102.00 gamma open 72.00 TOTAL PAID TARGET 201.00", "alpha paid 100.00 beta paid 103.00 gamma open 73.00 TOTAL PAID TARGET 203.00")
out = out.replace('"model_guess": 201.0, "expected": 201.0', '"model_guess": 203.0, "expected": 203.0')
out = out.replace("SKU1 qty 83 ok SKU2 qty 71 hold SKU3 qty 85 ok qty_sum TARGET 168", "SKU1 qty 84 ok SKU2 qty 72 hold SKU3 qty 86 ok qty_sum TARGET 170")
out = out.replace('"model_guess": 168.0, "expected": 168.0', '"model_guess": 170.0, "expected": 170.0')
out = out.replace("itemR1 76.00 done itemR2 78.25 done itemR3 65.00 open refund_done TARGET 154.25", "itemR1 77.00 done itemR2 79.25 done itemR3 66.00 open refund_done TARGET 156.25")
out = out.replace('"model_guess": 154.25, "expected": 154.25', '"model_guess": 156.25, "expected": 156.25')
out = out.replace("tea paid 95.00 rice paid 97.50 soup open 70.00 TOTAL PAID TARGET 192.50", "tea paid 96.00 rice paid 98.50 soup open 71.00 TOTAL PAID TARGET 194.50")
out = out.replace('"model_guess": 200.25, "expected": 192.50', '"model_guess": 202.25, "expected": 194.50')
(S / "c1952_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1947_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1947", "C1953"), ("c1947", "c1953")]:
    out = out.replace(a, b2)
(S / "c1953_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1954_scorecard_and_stage.py").write_text(SC1954, encoding="utf-8")
print("scorecard from fixed c1942 conf-gate pattern")
print("OK builder v307 ready")
'''
pre = "SC1954 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v307.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1949_vision_v307", "ashdale", "ferndale", "T307", "1188", "1932", "confidence_gate", "retarget_306"]:
    print(needle, needle in (h+pre+tail))
