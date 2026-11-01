from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v312.py").read_text(encoding="utf-8")
idx0 = b0.find('# V312 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1984 = " in head0:
    head0 = head0[:head0.find("SC1984 = ")]

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
pairs = [
    ("*croft ; stack mid-band", "*holm ; stack mid-band"),
    ("T312", "T313"), ("TR312", "TR313"), ("HO312", "HO313"),
    ("NEW312", "NEW313"),
    ("V312", "V313"), ("v312", "v313"),
    ("_v312_themes.json", "_v313_themes.json"),
    ("_v311_themes.json", "_v312_themes.json"),
    ("OLD311", "OLD312"),
    ("vision_images_v312", "vision_images_v313"),
    ("VL_GATE_V312", "VL_GATE_V313"), ("vl_gate_v312", "vl_gate_v313"),
    ("C1979", "C1985"), ("c1979", "c1985"),
    ("C1980", "C1986"), ("c1980", "c1986"),
    ("C1981", "C1987"), ("c1981", "c1987"),
    ("_v312c1979", "_v313c1985"),
    ("Harder than V310", "Harder than V311"),
    ("harder than V310", "harder than V311"),
    ("NEW themes vs V310:", "NEW themes vs V311:"),
    ("kept on V312", "kept on V313"),
    ("V312 keeps floor", "V313 keeps floor"),
    ("C1979 design+fixtures; no VL claim", "C1985 design+fixtures; no VL claim"),
    ("retarget_311", "retarget_312"),
    ("*croft", "*holm"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHCROFT bait 225.35", "ASHHOLM bait 226.36")
h = h.replace("CEDARC bait 227.37", "CEDARH bait 228.38")
h = h.replace("DAWNC ghost 150.60", "DAWNH ghost 151.61")
h = h.replace("GLENC bait 220.30", "GLENH bait 221.31")
h = h.replace("JADEC bait 211.21", "JADEH bait 212.22")
h = h.replace("NETHERC bait 228.38", "NETHERH bait 229.39")

TR = '''TR313 = [
    [2290.0, 2307.5, 2030.0],[840, 760, 820],[2213.0, 2242.25, 2008.0],[2346.0, 2363.0, 2098.0],
    [2408.0, 2432.0, 2068.0],[2126, 2142, 2026],[490.0, 530.0, 760.0],[2256.0, 2287.75, 2032.0],
    [840.0, 760.0, 820.0],[2323.0, 2311.0, 2029.0],[1,1,0],[0,0,0],
    [2389.0, 2410.5, 2054.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO313 = [
    [2088.0, 2100.75, 1949.0],[640, 660, 820],[2031.0, 2045.5, 1924.0],[2161.0, 2177.0, 1980.0],
    [2202.0, 2218.0, 1973.0],[1984, 1996, 1944],[420.0, 460.0, 740.0],[2072.0, 2093.75, 1949.0],
    [740.0, 780.0, 820.0],[2119.0, 2105.0, 1946.0],[1,1,0],[0,0,0],
    [2154.0, 2169.5, 1959.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR313\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO313\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1976_confidence_gate_stretch.py"
sc_body = (ROOT / "scripts/c1978_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1978", "C1990"), ("c1978", "c1990"),
    ("C1976", "C1988"), ("c1976", "c1988"),
    ("C1977", "C1989"), ("c1977", "c1989"),
    ("C1974", "C1986"), ("c1974", "c1986"),
    ("C1975", "C1987"), ("c1975", "c1987"),
    ("V311", "V313"), ("v311", "v313"),
    ("STAGE_ANT_C1978", "STAGE_ANT_C1990"),
    ("*vale", "*holm"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V313 knife = confidence-gate (alternating; V312 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1976", "C1988"), ("c1976", "c1988"),
    ("C1964", "C1988"), ("c1964", "c1988"),
    ("cg138_", "cg139_"),
    ("conf_gate_stretch_c1976", "conf_gate_stretch_c1988"),
    ("confidence_gate_stretch_v201", "confidence_gate_stretch_v202"),
    ("Stretch vs C1964", "Stretch vs C1976"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 117.00 b paid 121.75 c open 77.00 TOTAL PAID TARGET 238.75", "a paid 118.00 b paid 122.75 c open 78.00 TOTAL PAID TARGET 240.75")
out = out.replace('"model_guess": 999.0, "expected": 238.75', '"model_guess": 999.0, "expected": 240.75')
out = out.replace("SKU1 qty 112 ok SKU2 qty 86 hold SKU3 qty 116 ok qty_sum TARGET 228", "SKU1 qty 113 ok SKU2 qty 87 hold SKU3 qty 117 ok qty_sum TARGET 230")
out = out.replace('"model_guess": 240.0, "expected": 228.0', '"model_guess": 242.0, "expected": 230.0')
out = out.replace("itemR1 93.00 done itemR2 96.75 done itemR3 74.00 open refund_done TARGET 189.75", "itemR1 94.00 done itemR2 97.75 done itemR3 75.00 open refund_done TARGET 191.75")
out = out.replace('"model_guess": 198.5, "expected": 189.75', '"model_guess": 200.5, "expected": 191.75')
out = out.replace("T1 161.00 paid T2 101.00 open T3 142.00 paid tax_base_paid TARGET 303.00", "T1 162.00 paid T2 102.00 open T3 143.00 paid tax_base_paid TARGET 305.00")
out = out.replace('"model_guess": 339.0, "expected": 303.0', '"model_guess": 341.0, "expected": 305.0')
out = out.replace("A 1655 active B 365 leave C 1540 active payroll_active TARGET 3195", "A 1657 active B 366 leave C 1541 active payroll_active TARGET 3198")
out = out.replace('"model_guess": 3425.0, "expected": 3195.0', '"model_guess": 3428.0, "expected": 3198.0')
out = out.replace("P1 106 ok P2 85 hold P3 105 ok ship_ok_qty TARGET 211", "P1 107 ok P2 86 hold P3 106 ok ship_ok_qty TARGET 213")
out = out.replace('"model_guess": 230.0, "expected": 211.0', '"model_guess": 232.0, "expected": 213.0')
out = out.replace("S1 pri 95 open S2 pri 98 closed S3 pri 107 open open_pri_sum TARGET 202", "S1 pri 96 open S2 pri 99 closed S3 pri 108 open open_pri_sum TARGET 204")
out = out.replace('"model_guess": 234.0, "expected": 202.0', '"model_guess": 236.0, "expected": 204.0')
out = out.replace("X 137.00 open Y 140.00 open paid_total TARGET 0.00 bait 277.00", "X 138.00 open Y 141.00 open paid_total TARGET 0.00 bait 279.00")
out = out.replace('"model_guess": 277.0, "expected": 0.0', '"model_guess": 279.0, "expected": 0.0')
out = out.replace("alpha paid 102.00 beta paid 105.00 gamma open 75.00 TOTAL PAID TARGET 207.00", "alpha paid 103.00 beta paid 106.00 gamma open 76.00 TOTAL PAID TARGET 209.00")
out = out.replace('"model_guess": 207.0, "expected": 207.0', '"model_guess": 209.0, "expected": 209.0')
out = out.replace("SKU1 qty 86 ok SKU2 qty 74 hold SKU3 qty 88 ok qty_sum TARGET 174", "SKU1 qty 87 ok SKU2 qty 75 hold SKU3 qty 89 ok qty_sum TARGET 176")
out = out.replace('"model_guess": 174.0, "expected": 174.0', '"model_guess": 176.0, "expected": 176.0')
out = out.replace("itemR1 79.00 done itemR2 81.25 done itemR3 68.00 open refund_done TARGET 160.25", "itemR1 80.00 done itemR2 82.25 done itemR3 69.00 open refund_done TARGET 162.25")
out = out.replace('"model_guess": 160.25, "expected": 160.25', '"model_guess": 162.25, "expected": 162.25')
out = out.replace("tea paid 98.00 rice paid 100.50 soup open 73.00 TOTAL PAID TARGET 198.50", "tea paid 99.00 rice paid 101.50 soup open 74.00 TOTAL PAID TARGET 200.50")
out = out.replace('"model_guess": 206.25, "expected": 198.50', '"model_guess": 208.25, "expected": 200.50')
(S / "c1988_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1983_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1983", "C1989"), ("c1983", "c1989")]:
    out = out.replace(a, b2)
(S / "c1989_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1990_scorecard_and_stage.py").write_text(SC1990, encoding="utf-8")
print("scorecard from fixed c1978 conf-gate pattern")
print("OK builder v313 ready")
'''
pre = "SC1990 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v313.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1985_vision_v313", "ashholm", "fernholm", "T313", "1188", "1944", "confidence_gate", "retarget_312"]:
    print(needle, needle in (h+pre+tail))
