from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v288.py").read_text(encoding="utf-8")
idx0 = b0.find('# V288 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("nethermere", "nethervale"), ("NETHERMERE", "NETHERVALE"),
    ("cedarmere", "cedarvale"), ("CEDARMERE", "CEDARVALE"),
    ("dawnmere", "dawnvale"), ("DAWNMERE", "DAWNVALE"),
    ("fernmere", "fernvale"), ("FERNMERE", "FERNVALE"),
    ("glenmere", "glenvale"), ("GLENMERE", "GLENVALE"),
    ("hazemere", "hazevale"), ("HAZEMERE", "HAZEVALE"),
    ("jademere", "jadevale"), ("JADEMERE", "JADEVALE"),
    ("knotmere", "knotvale"), ("KNOTMERE", "KNOTVALE"),
    ("lakemere", "lakevale"), ("LAKEMERE", "LAKEVALE"),
    ("mossmere", "mossvale"), ("MOSSMERE", "MOSSVALE"),
    ("pinemere", "pinevale"), ("PINEMERE", "PINEVALE"),
    ("quillmere", "quillvale"), ("QUILLMERE", "QUILLVALE"),
    ("reedmere", "reedvale"), ("REEDMERE", "REEDVALE"),
    ("stonemere", "stonevale"), ("STONEMERE", "STONEVALE"),
    ("ashmere", "ashvale"), ("ASHMERE", "ASHVALE"),
    ("elmmere", "elmvale"), ("ELMMERE", "ELMVALE"),
    ("inkmere", "inkvale"), ("INKMERE", "INKVALE"),
    ("oakmere", "oakvale"), ("OAKMERE", "OAKVALE"),
]
pairs = [
    ("*mere ; stack mid-band", "*vale ; stack mid-band"),
    ("T288", "T289"), ("TR288", "TR289"), ("HO288", "HO289"),
    ("NEW288", "NEW289"),
    ("V288", "V289"), ("v288", "v289"),
    ("_v288_themes.json", "_v289_themes.json"),
    ("_v287_themes.json", "_v288_themes.json"),
    ("OLD287", "OLD288"),
    ("vision_images_v288", "vision_images_v289"),
    ("VL_GATE_V288", "VL_GATE_V289"), ("vl_gate_v288", "vl_gate_v289"),
    ("C1835", "C1841"), ("c1835", "c1841"),
    ("C1836", "C1842"), ("c1836", "c1842"),
    ("C1837", "C1843"), ("c1837", "c1843"),
    ("_v288c1835", "_v289c1841"),
    ("Harder than V286", "Harder than V287"),
    ("harder than V286", "harder than V287"),
    ("NEW themes vs V286:", "NEW themes vs V287:"),
    ("kept on V288", "kept on V289"),
    ("V288 keeps floor", "V289 keeps floor"),
    ("C1835 design+fixtures; no VL claim", "C1841 design+fixtures; no VL claim"),
    ("retarget_287", "retarget_288"),
    ("*mere", "*vale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMERE bait 201.11", "ASHVALE bait 202.12")
h = h.replace("CEDARM bait 203.13", "CEDARV bait 204.14")
h = h.replace("DAWNM ghost 126.36", "DAWNV ghost 127.37")
h = h.replace("GLENM bait 196.06", "GLENV bait 197.07")
h = h.replace("JADEM bait 187.97", "JADEV bait 188.98")
h = h.replace("NETHERM bait 204.14", "NETHERV bait 205.15")

TR = '''TR289 = [
    [2242.0, 2259.5, 1982.0],[840, 760, 820],[2165.0, 2194.25, 1960.0],[2298.0, 2315.0, 2050.0],
    [2360.0, 2384.0, 2020.0],[2078, 2094, 1978],[490.0, 530.0, 760.0],[2208.0, 2239.75, 1984.0],
    [840.0, 760.0, 820.0],[2275.0, 2263.0, 1981.0],[1,1,0],[0,0,0],
    [2341.0, 2362.5, 2006.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO289 = [
    [2040.0, 2052.75, 1901.0],[640, 660, 820],[1983.0, 1997.5, 1876.0],[2113.0, 2129.0, 1932.0],
    [2154.0, 2170.0, 1925.0],[1936, 1948, 1896],[420.0, 460.0, 740.0],[2024.0, 2045.75, 1901.0],
    [740.0, 780.0, 820.0],[2071.0, 2057.0, 1898.0],[1,1,0],[0,0,0],
    [2106.0, 2121.5, 1911.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR289\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO289\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1832_confidence_gate_stretch.py"
sc_src = "c1834_scorecard_and_stage.py"

tail = f'''# V289 knife = confidence-gate (alternating; V288 was product-U2C; theme wrap *mere→*vale)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1832", "C1844"), ("c1832", "c1844"),
    ("C1820", "C1844"), ("c1820", "c1844"),
    ("cg126_", "cg127_"),
    ("conf_gate_stretch_c1832", "conf_gate_stretch_c1844"),
    ("confidence_gate_stretch_v189", "confidence_gate_stretch_v190"),
    ("Stretch vs C1820", "Stretch vs C1832"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 105.00 b paid 109.75 c open 65.00 TOTAL PAID TARGET 214.75", "a paid 106.00 b paid 110.75 c open 66.00 TOTAL PAID TARGET 216.75")
out = out.replace('"model_guess": 999.0, "expected": 214.75', '"model_guess": 999.0, "expected": 216.75')
out = out.replace("SKU1 qty 100 ok SKU2 qty 74 hold SKU3 qty 104 ok qty_sum TARGET 204", "SKU1 qty 101 ok SKU2 qty 75 hold SKU3 qty 105 ok qty_sum TARGET 206")
out = out.replace('"model_guess": 216.0, "expected": 204.0', '"model_guess": 218.0, "expected": 206.0')
out = out.replace("itemR1 81.00 done itemR2 84.75 done itemR3 62.00 open refund_done TARGET 165.75", "itemR1 82.00 done itemR2 85.75 done itemR3 63.00 open refund_done TARGET 167.75")
out = out.replace('"model_guess": 174.5, "expected": 165.75', '"model_guess": 176.5, "expected": 167.75')
out = out.replace("T1 149.00 paid T2 89.00 open T3 130.00 paid tax_base_paid TARGET 279.00", "T1 150.00 paid T2 90.00 open T3 131.00 paid tax_base_paid TARGET 281.00")
out = out.replace('"model_guess": 315.0, "expected": 279.0', '"model_guess": 317.0, "expected": 281.0')
out = out.replace("A 1631 active B 353 leave C 1528 active payroll_active TARGET 3159", "A 1633 active B 354 leave C 1529 active payroll_active TARGET 3162")
out = out.replace('"model_guess": 3389.0, "expected": 3159.0', '"model_guess": 3392.0, "expected": 3162.0')
out = out.replace("P1 94 ok P2 73 hold P3 93 ok ship_ok_qty TARGET 187", "P1 95 ok P2 74 hold P3 94 ok ship_ok_qty TARGET 189")
out = out.replace('"model_guess": 206.0, "expected": 187.0', '"model_guess": 208.0, "expected": 189.0')
out = out.replace("S1 pri 83 open S2 pri 86 closed S3 pri 95 open open_pri_sum TARGET 178", "S1 pri 84 open S2 pri 87 closed S3 pri 96 open open_pri_sum TARGET 180")
out = out.replace('"model_guess": 210.0, "expected": 178.0', '"model_guess": 212.0, "expected": 180.0')
out = out.replace("X 125.00 open Y 128.00 open paid_total TARGET 0.00 bait 253.00", "X 126.00 open Y 129.00 open paid_total TARGET 0.00 bait 255.00")
out = out.replace('"model_guess": 253.0, "expected": 0.0', '"model_guess": 255.0, "expected": 0.0')
out = out.replace("alpha paid 90.00 beta paid 93.00 gamma open 63.00 TOTAL PAID TARGET 183.00", "alpha paid 91.00 beta paid 94.00 gamma open 64.00 TOTAL PAID TARGET 185.00")
out = out.replace('"model_guess": 183.0, "expected": 183.0', '"model_guess": 185.0, "expected": 185.0')
out = out.replace("SKU1 qty 74 ok SKU2 qty 62 hold SKU3 qty 76 ok qty_sum TARGET 150", "SKU1 qty 75 ok SKU2 qty 63 hold SKU3 qty 77 ok qty_sum TARGET 152")
out = out.replace('"model_guess": 150.0, "expected": 150.0', '"model_guess": 152.0, "expected": 152.0')
out = out.replace("itemR1 67.00 done itemR2 69.25 done itemR3 56.00 open refund_done TARGET 136.25", "itemR1 68.00 done itemR2 70.25 done itemR3 57.00 open refund_done TARGET 138.25")
out = out.replace('"model_guess": 136.25, "expected": 136.25', '"model_guess": 138.25, "expected": 138.25')
out = out.replace("tea paid 86.00 rice paid 88.50 soup open 61.00 TOTAL PAID TARGET 174.50", "tea paid 87.00 rice paid 89.50 soup open 62.00 TOTAL PAID TARGET 176.50")
out = out.replace('"model_guess": 182.25, "expected": 174.50', '"model_guess": 184.25, "expected": 176.50')
(S / "c1844_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1839_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1839", "C1845"), ("c1839", "c1845")]:
    out = out.replace(a, b2)
(S / "c1845_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1834", "C1846"), ("c1834", "c1846"),
    ("C1832", "C1844"), ("c1832", "c1844"),
    ("C1833", "C1845"), ("c1833", "c1845"),
    ("C1830", "C1842"), ("c1830", "c1842"),
    ("C1831", "C1843"), ("c1831", "c1843"),
    ("V287", "V289"), ("v287", "v289"),
    ("STAGE_ANT_C1834", "STAGE_ANT_C1846"),
    ("*hurst", "*vale"),
]:
    out = out.replace(a, b2)
(S / "c1846_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v289 ready")
'''
(ROOT / "tools/_build_v289.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1841_vision_v289", "ashvale", "fernvale", "T289", "1188", "1896", "confidence_gate", "retarget_288", "theme wrap"]:
    print(needle, needle in (h+tail))
