from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v290.py").read_text(encoding="utf-8")
idx0 = b0.find('# V290 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
    ("T290", "T291"), ("TR290", "TR291"), ("HO290", "HO291"),
    ("NEW290", "NEW291"),
    ("V290", "V291"), ("v290", "v291"),
    ("_v290_themes.json", "_v291_themes.json"),
    ("_v289_themes.json", "_v290_themes.json"),
    ("OLD289", "OLD290"),
    ("vision_images_v290", "vision_images_v291"),
    ("VL_GATE_V290", "VL_GATE_V291"), ("vl_gate_v290", "vl_gate_v291"),
    ("C1847", "C1853"), ("c1847", "c1853"),
    ("C1848", "C1854"), ("c1848", "c1854"),
    ("C1849", "C1855"), ("c1849", "c1855"),
    ("_v290c1847", "_v291c1853"),
    ("Harder than V288", "Harder than V289"),
    ("harder than V288", "harder than V289"),
    ("NEW themes vs V288:", "NEW themes vs V289:"),
    ("kept on V290", "kept on V291"),
    ("V290 keeps floor", "V291 keeps floor"),
    ("C1847 design+fixtures; no VL claim", "C1853 design+fixtures; no VL claim"),
    ("retarget_289", "retarget_290"),
    ("*croft", "*holm"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHCROFT bait 203.13", "ASHHOLM bait 204.14")
h = h.replace("CEDARC bait 205.15", "CEDARH bait 206.16")
h = h.replace("DAWNC ghost 128.38", "DAWNH ghost 129.39")
h = h.replace("GLENC bait 198.08", "GLENH bait 199.09")
h = h.replace("JADEC bait 189.99", "JADEH bait 190.00")
h = h.replace("NETHERC bait 206.16", "NETHERH bait 207.17")

TR = '''TR291 = [
    [2246.0, 2263.5, 1986.0],[840, 760, 820],[2169.0, 2198.25, 1964.0],[2302.0, 2319.0, 2054.0],
    [2364.0, 2388.0, 2024.0],[2082, 2098, 1982],[490.0, 530.0, 760.0],[2212.0, 2243.75, 1988.0],
    [840.0, 760.0, 820.0],[2279.0, 2267.0, 1985.0],[1,1,0],[0,0,0],
    [2345.0, 2366.5, 2010.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO291 = [
    [2044.0, 2056.75, 1905.0],[640, 660, 820],[1987.0, 2001.5, 1880.0],[2117.0, 2133.0, 1936.0],
    [2158.0, 2174.0, 1929.0],[1940, 1952, 1900],[420.0, 460.0, 740.0],[2028.0, 2049.75, 1905.0],
    [740.0, 780.0, 820.0],[2075.0, 2061.0, 1902.0],[1,1,0],[0,0,0],
    [2110.0, 2125.5, 1915.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR291\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO291\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1844_confidence_gate_stretch.py"
sc_src = "c1846_scorecard_and_stage.py"  # known-good conf-gate scorecard

tail = f'''# V291 knife = confidence-gate (alternating; V290 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1844", "C1856"), ("c1844", "c1856"),
    ("C1832", "C1856"), ("c1832", "c1856"),
    ("cg127_", "cg128_"),
    ("conf_gate_stretch_c1844", "conf_gate_stretch_c1856"),
    ("confidence_gate_stretch_v190", "confidence_gate_stretch_v191"),
    ("Stretch vs C1832", "Stretch vs C1844"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 106.00 b paid 110.75 c open 66.00 TOTAL PAID TARGET 216.75", "a paid 107.00 b paid 111.75 c open 67.00 TOTAL PAID TARGET 218.75")
out = out.replace('"model_guess": 999.0, "expected": 216.75', '"model_guess": 999.0, "expected": 218.75')
out = out.replace("SKU1 qty 101 ok SKU2 qty 75 hold SKU3 qty 105 ok qty_sum TARGET 206", "SKU1 qty 102 ok SKU2 qty 76 hold SKU3 qty 106 ok qty_sum TARGET 208")
out = out.replace('"model_guess": 218.0, "expected": 206.0', '"model_guess": 220.0, "expected": 208.0')
out = out.replace("itemR1 82.00 done itemR2 85.75 done itemR3 63.00 open refund_done TARGET 167.75", "itemR1 83.00 done itemR2 86.75 done itemR3 64.00 open refund_done TARGET 169.75")
out = out.replace('"model_guess": 176.5, "expected": 167.75', '"model_guess": 178.5, "expected": 169.75')
out = out.replace("T1 150.00 paid T2 90.00 open T3 131.00 paid tax_base_paid TARGET 281.00", "T1 151.00 paid T2 91.00 open T3 132.00 paid tax_base_paid TARGET 283.00")
out = out.replace('"model_guess": 317.0, "expected": 281.0', '"model_guess": 319.0, "expected": 283.0')
out = out.replace("A 1633 active B 354 leave C 1529 active payroll_active TARGET 3162", "A 1635 active B 355 leave C 1530 active payroll_active TARGET 3165")
out = out.replace('"model_guess": 3392.0, "expected": 3162.0', '"model_guess": 3395.0, "expected": 3165.0')
out = out.replace("P1 95 ok P2 74 hold P3 94 ok ship_ok_qty TARGET 189", "P1 96 ok P2 75 hold P3 95 ok ship_ok_qty TARGET 191")
out = out.replace('"model_guess": 208.0, "expected": 189.0', '"model_guess": 210.0, "expected": 191.0')
out = out.replace("S1 pri 84 open S2 pri 87 closed S3 pri 96 open open_pri_sum TARGET 180", "S1 pri 85 open S2 pri 88 closed S3 pri 97 open open_pri_sum TARGET 182")
out = out.replace('"model_guess": 212.0, "expected": 180.0', '"model_guess": 214.0, "expected": 182.0')
out = out.replace("X 126.00 open Y 129.00 open paid_total TARGET 0.00 bait 255.00", "X 127.00 open Y 130.00 open paid_total TARGET 0.00 bait 257.00")
out = out.replace('"model_guess": 255.0, "expected": 0.0', '"model_guess": 257.0, "expected": 0.0')
out = out.replace("alpha paid 91.00 beta paid 94.00 gamma open 64.00 TOTAL PAID TARGET 185.00", "alpha paid 92.00 beta paid 95.00 gamma open 65.00 TOTAL PAID TARGET 187.00")
out = out.replace('"model_guess": 185.0, "expected": 185.0', '"model_guess": 187.0, "expected": 187.0')
out = out.replace("SKU1 qty 75 ok SKU2 qty 63 hold SKU3 qty 77 ok qty_sum TARGET 152", "SKU1 qty 76 ok SKU2 qty 64 hold SKU3 qty 78 ok qty_sum TARGET 154")
out = out.replace('"model_guess": 152.0, "expected": 152.0', '"model_guess": 154.0, "expected": 154.0')
out = out.replace("itemR1 68.00 done itemR2 70.25 done itemR3 57.00 open refund_done TARGET 138.25", "itemR1 69.00 done itemR2 71.25 done itemR3 58.00 open refund_done TARGET 140.25")
out = out.replace('"model_guess": 138.25, "expected": 138.25', '"model_guess": 140.25, "expected": 140.25')
out = out.replace("tea paid 87.00 rice paid 89.50 soup open 62.00 TOTAL PAID TARGET 176.50", "tea paid 88.00 rice paid 90.50 soup open 63.00 TOTAL PAID TARGET 178.50")
out = out.replace('"model_guess": 184.25, "expected": 176.50', '"model_guess": 186.25, "expected": 178.50')
(S / "c1856_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1851_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1851", "C1857"), ("c1851", "c1857")]:
    out = out.replace(a, b2)
(S / "c1857_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1846", "C1858"), ("c1846", "c1858"),
    ("C1844", "C1856"), ("c1844", "c1856"),
    ("C1845", "C1857"), ("c1845", "c1857"),
    ("C1842", "C1854"), ("c1842", "c1854"),
    ("C1843", "C1855"), ("c1843", "c1855"),
    ("V289", "V291"), ("v289", "v291"),
    ("STAGE_ANT_C1846", "STAGE_ANT_C1858"),
    ("*vale", "*holm"),
]:
    out = out.replace(a, b2)
(S / "c1858_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v291 ready")
'''
(ROOT / "tools/_build_v291.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1853_vision_v291", "ashholm", "fernholm", "T291", "1188", "1900", "confidence_gate", "retarget_290"]:
    print(needle, needle in (h+tail))
