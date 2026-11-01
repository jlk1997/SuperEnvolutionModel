from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v300.py").read_text(encoding="utf-8")
idx0 = b0.find('# V300 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1912 = " in head0:
    head0 = head0[:head0.find("SC1912 = ")]

theme_pairs = [
    ("nethervale", "nethercroft"), ("NETHERVALE", "NETHERCROFT"),
    ("cedarvale", "cedarcroft"), ("CEDARVALE", "CEDARCROFT"),
    ("dawnvale", "dawncroft"), ("DAWNVALE", "DAWNCROFT"),
    ("fernvale", "ferncroft"), ("FERNVALE", "FERNCROFT"),
    ("glenvale", "glencroft"), ("GLENVALE", "GLENCROFT"),
    ("hazevale", "hazecroft"), ("HAZEVALE", "HAZECROFT"),
    ("jadevale", "jadecroft"), ("JADEVALE", "JADECROFT"),
    ("knotvale", "knotcroft"), ("KNOTVALE", "KNOTCROFT"),
    ("lakevale", "lakecroft"), ("LAKEVALE", "LAKECROFT"),
    ("mossvale", "mosscroft"), ("MOSSVALE", "MOSSCROFT"),
    ("pinevale", "pinecroft"), ("PINEVALE", "PINECROFT"),
    ("quillvale", "quillcroft"), ("QUILLVALE", "QUILLCROFT"),
    ("reedvale", "reedcroft"), ("REEDVALE", "REEDCROFT"),
    ("stonevale", "stonecroft"), ("STONEVALE", "STONECROFT"),
    ("ashvale", "ashcroft"), ("ASHVALE", "ASHCROFT"),
    ("elmvale", "elmcroft"), ("ELMVALE", "ELMCROFT"),
    ("inkvale", "inkcroft"), ("INKVALE", "INKCROFT"),
    ("oakvale", "oakcroft"), ("OAKVALE", "OAKCROFT"),
]
pairs = [
    ("*vale ; stack mid-band", "*croft ; stack mid-band"),
    ("T300", "T301"), ("TR300", "TR301"), ("HO300", "HO301"),
    ("NEW300", "NEW301"),
    ("V300", "V301"), ("v300", "v301"),
    ("_v300_themes.json", "_v301_themes.json"),
    ("_v299_themes.json", "_v300_themes.json"),
    ("OLD299", "OLD300"),
    ("vision_images_v300", "vision_images_v301"),
    ("VL_GATE_V300", "VL_GATE_V301"), ("vl_gate_v300", "vl_gate_v301"),
    ("C1907", "C1913"), ("c1907", "c1913"),
    ("C1908", "C1914"), ("c1908", "c1914"),
    ("C1909", "C1915"), ("c1909", "c1915"),
    ("_v300c1907", "_v301c1913"),
    ("Harder than V298", "Harder than V299"),
    ("harder than V298", "harder than V299"),
    ("NEW themes vs V298:", "NEW themes vs V299:"),
    ("kept on V300", "kept on V301"),
    ("V300 keeps floor", "V301 keeps floor"),
    ("C1907 design+fixtures; no VL claim", "C1913 design+fixtures; no VL claim"),
    ("retarget_299", "retarget_300"),
    ("*vale", "*croft"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHVALE bait 213.23", "ASHCROFT bait 214.24")
h = h.replace("CEDARV bait 215.25", "CEDARC bait 216.26")
h = h.replace("DAWNV ghost 138.48", "DAWNC ghost 139.49")
h = h.replace("GLENV bait 208.18", "GLENC bait 209.19")
h = h.replace("JADEV bait 199.09", "JADEC bait 200.10")
h = h.replace("NETHERV bait 216.26", "NETHERC bait 217.27")

TR = '''TR301 = [
    [2266.0, 2283.5, 2006.0],[840, 760, 820],[2189.0, 2218.25, 1984.0],[2322.0, 2339.0, 2074.0],
    [2384.0, 2408.0, 2044.0],[2102, 2118, 2002],[490.0, 530.0, 760.0],[2232.0, 2263.75, 2008.0],
    [840.0, 760.0, 820.0],[2299.0, 2287.0, 2005.0],[1,1,0],[0,0,0],
    [2365.0, 2386.5, 2030.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO301 = [
    [2064.0, 2076.75, 1925.0],[640, 660, 820],[2007.0, 2021.5, 1900.0],[2137.0, 2153.0, 1956.0],
    [2178.0, 2194.0, 1949.0],[1960, 1972, 1920],[420.0, 460.0, 740.0],[2048.0, 2069.75, 1925.0],
    [740.0, 780.0, 820.0],[2095.0, 2081.0, 1922.0],[1,1,0],[0,0,0],
    [2130.0, 2145.5, 1935.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR301\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO301\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1904_confidence_gate_stretch.py"
sc_body = (ROOT / "scripts/c1906_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1906", "C1918"), ("c1906", "c1918"),
    ("C1904", "C1916"), ("c1904", "c1916"),
    ("C1905", "C1917"), ("c1905", "c1917"),
    ("C1902", "C1914"), ("c1902", "c1914"),
    ("C1903", "C1915"), ("c1903", "c1915"),
    ("V299", "V301"), ("v299", "v301"),
    ("STAGE_ANT_C1906", "STAGE_ANT_C1918"),
    ("*mere", "*croft"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V301 knife = confidence-gate (alternating; V300 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1904", "C1916"), ("c1904", "c1916"),
    ("C1892", "C1916"), ("c1892", "c1916"),
    ("cg132_", "cg133_"),
    ("conf_gate_stretch_c1904", "conf_gate_stretch_c1916"),
    ("confidence_gate_stretch_v195", "confidence_gate_stretch_v196"),
    ("Stretch vs C1892", "Stretch vs C1904"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 111.00 b paid 115.75 c open 71.00 TOTAL PAID TARGET 226.75", "a paid 112.00 b paid 116.75 c open 72.00 TOTAL PAID TARGET 228.75")
out = out.replace('"model_guess": 999.0, "expected": 226.75', '"model_guess": 999.0, "expected": 228.75')
out = out.replace("SKU1 qty 106 ok SKU2 qty 80 hold SKU3 qty 110 ok qty_sum TARGET 216", "SKU1 qty 107 ok SKU2 qty 81 hold SKU3 qty 111 ok qty_sum TARGET 218")
out = out.replace('"model_guess": 228.0, "expected": 216.0', '"model_guess": 230.0, "expected": 218.0')
out = out.replace("itemR1 87.00 done itemR2 90.75 done itemR3 68.00 open refund_done TARGET 177.75", "itemR1 88.00 done itemR2 91.75 done itemR3 69.00 open refund_done TARGET 179.75")
out = out.replace('"model_guess": 186.5, "expected": 177.75', '"model_guess": 188.5, "expected": 179.75')
out = out.replace("T1 155.00 paid T2 95.00 open T3 136.00 paid tax_base_paid TARGET 291.00", "T1 156.00 paid T2 96.00 open T3 137.00 paid tax_base_paid TARGET 293.00")
out = out.replace('"model_guess": 327.0, "expected": 291.0', '"model_guess": 329.0, "expected": 293.0')
out = out.replace("A 1643 active B 359 leave C 1534 active payroll_active TARGET 3177", "A 1645 active B 360 leave C 1535 active payroll_active TARGET 3180")
out = out.replace('"model_guess": 3407.0, "expected": 3177.0', '"model_guess": 3410.0, "expected": 3180.0')
out = out.replace("P1 100 ok P2 79 hold P3 99 ok ship_ok_qty TARGET 199", "P1 101 ok P2 80 hold P3 100 ok ship_ok_qty TARGET 201")
out = out.replace('"model_guess": 218.0, "expected": 199.0', '"model_guess": 220.0, "expected": 201.0')
out = out.replace("S1 pri 89 open S2 pri 92 closed S3 pri 101 open open_pri_sum TARGET 190", "S1 pri 90 open S2 pri 93 closed S3 pri 102 open open_pri_sum TARGET 192")
out = out.replace('"model_guess": 222.0, "expected": 190.0', '"model_guess": 224.0, "expected": 192.0')
out = out.replace("X 131.00 open Y 134.00 open paid_total TARGET 0.00 bait 265.00", "X 132.00 open Y 135.00 open paid_total TARGET 0.00 bait 267.00")
out = out.replace('"model_guess": 265.0, "expected": 0.0', '"model_guess": 267.0, "expected": 0.0')
out = out.replace("alpha paid 96.00 beta paid 99.00 gamma open 69.00 TOTAL PAID TARGET 195.00", "alpha paid 97.00 beta paid 100.00 gamma open 70.00 TOTAL PAID TARGET 197.00")
out = out.replace('"model_guess": 195.0, "expected": 195.0', '"model_guess": 197.0, "expected": 197.0')
out = out.replace("SKU1 qty 80 ok SKU2 qty 68 hold SKU3 qty 82 ok qty_sum TARGET 162", "SKU1 qty 81 ok SKU2 qty 69 hold SKU3 qty 83 ok qty_sum TARGET 164")
out = out.replace('"model_guess": 162.0, "expected": 162.0', '"model_guess": 164.0, "expected": 164.0')
out = out.replace("itemR1 73.00 done itemR2 75.25 done itemR3 62.00 open refund_done TARGET 148.25", "itemR1 74.00 done itemR2 76.25 done itemR3 63.00 open refund_done TARGET 150.25")
out = out.replace('"model_guess": 148.25, "expected": 148.25', '"model_guess": 150.25, "expected": 150.25')
out = out.replace("tea paid 92.00 rice paid 94.50 soup open 67.00 TOTAL PAID TARGET 186.50", "tea paid 93.00 rice paid 95.50 soup open 68.00 TOTAL PAID TARGET 188.50")
out = out.replace('"model_guess": 194.25, "expected": 186.50', '"model_guess": 196.25, "expected": 188.50')
(S / "c1916_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1911_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1911", "C1917"), ("c1911", "c1917")]:
    out = out.replace(a, b2)
(S / "c1917_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1918_scorecard_and_stage.py").write_text(SC1918, encoding="utf-8")
print("scorecard from fixed c1906 conf-gate pattern")
print("OK builder v301 ready")
'''
pre = "SC1918 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v301.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1913_vision_v301", "ashcroft", "ferncroft", "T301", "1188", "1920", "confidence_gate", "retarget_300"]:
    print(needle, needle in (h+pre+tail))
