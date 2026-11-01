from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v296.py").read_text(encoding="utf-8")
idx0 = b0.find('# V296 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1888 = " in head0:
    head0 = head0[:head0.find("SC1888 = ")]

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
    ("T296", "T297"), ("TR296", "TR297"), ("HO296", "HO297"),
    ("NEW296", "NEW297"),
    ("V296", "V297"), ("v296", "v297"),
    ("_v296_themes.json", "_v297_themes.json"),
    ("_v295_themes.json", "_v296_themes.json"),
    ("OLD295", "OLD296"),
    ("vision_images_v296", "vision_images_v297"),
    ("VL_GATE_V296", "VL_GATE_V297"), ("vl_gate_v296", "vl_gate_v297"),
    ("C1883", "C1889"), ("c1883", "c1889"),
    ("C1884", "C1890"), ("c1884", "c1890"),
    ("C1885", "C1891"), ("c1885", "c1891"),
    ("_v296c1883", "_v297c1889"),
    ("Harder than V294", "Harder than V295"),
    ("harder than V294", "harder than V295"),
    ("NEW themes vs V294:", "NEW themes vs V295:"),
    ("kept on V296", "kept on V297"),
    ("V296 keeps floor", "V297 keeps floor"),
    ("C1883 design+fixtures; no VL claim", "C1889 design+fixtures; no VL claim"),
    ("retarget_295", "retarget_296"),
    ("*dale", "*ford"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHDALE bait 209.19", "ASHFORD bait 210.20")
h = h.replace("CEDARD bait 211.21", "CEDARF bait 212.22")
h = h.replace("DAWND ghost 134.44", "DAWNF ghost 135.45")
h = h.replace("GLEND bait 204.14", "GLENF bait 205.15")
h = h.replace("JADED bait 195.05", "JADEF bait 196.06")
h = h.replace("NETHERD bait 212.22", "NETHERF bait 213.23")

TR = '''TR297 = [
    [2258.0, 2275.5, 1998.0],[840, 760, 820],[2181.0, 2210.25, 1976.0],[2314.0, 2331.0, 2066.0],
    [2376.0, 2400.0, 2036.0],[2094, 2110, 1994],[490.0, 530.0, 760.0],[2224.0, 2255.75, 2000.0],
    [840.0, 760.0, 820.0],[2291.0, 2279.0, 1997.0],[1,1,0],[0,0,0],
    [2357.0, 2378.5, 2022.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO297 = [
    [2056.0, 2068.75, 1917.0],[640, 660, 820],[1999.0, 2013.5, 1892.0],[2129.0, 2145.0, 1948.0],
    [2170.0, 2186.0, 1941.0],[1952, 1964, 1912],[420.0, 460.0, 740.0],[2040.0, 2061.75, 1917.0],
    [740.0, 780.0, 820.0],[2087.0, 2073.0, 1914.0],[1,1,0],[0,0,0],
    [2122.0, 2137.5, 1927.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR297\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO297\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1880_confidence_gate_stretch.py"
sc_body = (ROOT / "scripts/c1882_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1882", "C1894"), ("c1882", "c1894"),
    ("C1880", "C1892"), ("c1880", "c1892"),
    ("C1881", "C1893"), ("c1881", "c1893"),
    ("C1878", "C1890"), ("c1878", "c1890"),
    ("C1879", "C1891"), ("c1879", "c1891"),
    ("V295", "V297"), ("v295", "v297"),
    ("STAGE_ANT_C1882", "STAGE_ANT_C1894"),
    ("*brook", "*ford"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V297 knife = confidence-gate (alternating; V296 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1880", "C1892"), ("c1880", "c1892"),
    ("C1868", "C1892"), ("c1868", "c1892"),
    ("cg130_", "cg131_"),
    ("conf_gate_stretch_c1880", "conf_gate_stretch_c1892"),
    ("confidence_gate_stretch_v193", "confidence_gate_stretch_v194"),
    ("Stretch vs C1868", "Stretch vs C1880"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 109.00 b paid 113.75 c open 69.00 TOTAL PAID TARGET 222.75", "a paid 110.00 b paid 114.75 c open 70.00 TOTAL PAID TARGET 224.75")
out = out.replace('"model_guess": 999.0, "expected": 222.75', '"model_guess": 999.0, "expected": 224.75')
out = out.replace("SKU1 qty 104 ok SKU2 qty 78 hold SKU3 qty 108 ok qty_sum TARGET 212", "SKU1 qty 105 ok SKU2 qty 79 hold SKU3 qty 109 ok qty_sum TARGET 214")
out = out.replace('"model_guess": 224.0, "expected": 212.0', '"model_guess": 226.0, "expected": 214.0')
out = out.replace("itemR1 85.00 done itemR2 88.75 done itemR3 66.00 open refund_done TARGET 173.75", "itemR1 86.00 done itemR2 89.75 done itemR3 67.00 open refund_done TARGET 175.75")
out = out.replace('"model_guess": 182.5, "expected": 173.75', '"model_guess": 184.5, "expected": 175.75')
out = out.replace("T1 153.00 paid T2 93.00 open T3 134.00 paid tax_base_paid TARGET 287.00", "T1 154.00 paid T2 94.00 open T3 135.00 paid tax_base_paid TARGET 289.00")
out = out.replace('"model_guess": 323.0, "expected": 287.0', '"model_guess": 325.0, "expected": 289.0')
out = out.replace("A 1639 active B 357 leave C 1532 active payroll_active TARGET 3171", "A 1641 active B 358 leave C 1533 active payroll_active TARGET 3174")
out = out.replace('"model_guess": 3401.0, "expected": 3171.0', '"model_guess": 3404.0, "expected": 3174.0')
out = out.replace("P1 98 ok P2 77 hold P3 97 ok ship_ok_qty TARGET 195", "P1 99 ok P2 78 hold P3 98 ok ship_ok_qty TARGET 197")
out = out.replace('"model_guess": 214.0, "expected": 195.0', '"model_guess": 216.0, "expected": 197.0')
out = out.replace("S1 pri 87 open S2 pri 90 closed S3 pri 99 open open_pri_sum TARGET 186", "S1 pri 88 open S2 pri 91 closed S3 pri 100 open open_pri_sum TARGET 188")
out = out.replace('"model_guess": 218.0, "expected": 186.0', '"model_guess": 220.0, "expected": 188.0')
out = out.replace("X 129.00 open Y 132.00 open paid_total TARGET 0.00 bait 261.00", "X 130.00 open Y 133.00 open paid_total TARGET 0.00 bait 263.00")
out = out.replace('"model_guess": 261.0, "expected": 0.0', '"model_guess": 263.0, "expected": 0.0')
out = out.replace("alpha paid 94.00 beta paid 97.00 gamma open 67.00 TOTAL PAID TARGET 191.00", "alpha paid 95.00 beta paid 98.00 gamma open 68.00 TOTAL PAID TARGET 193.00")
out = out.replace('"model_guess": 191.0, "expected": 191.0', '"model_guess": 193.0, "expected": 193.0')
out = out.replace("SKU1 qty 78 ok SKU2 qty 66 hold SKU3 qty 80 ok qty_sum TARGET 158", "SKU1 qty 79 ok SKU2 qty 67 hold SKU3 qty 81 ok qty_sum TARGET 160")
out = out.replace('"model_guess": 158.0, "expected": 158.0', '"model_guess": 160.0, "expected": 160.0')
out = out.replace("itemR1 71.00 done itemR2 73.25 done itemR3 60.00 open refund_done TARGET 144.25", "itemR1 72.00 done itemR2 74.25 done itemR3 61.00 open refund_done TARGET 146.25")
out = out.replace('"model_guess": 144.25, "expected": 144.25', '"model_guess": 146.25, "expected": 146.25')
out = out.replace("tea paid 90.00 rice paid 92.50 soup open 65.00 TOTAL PAID TARGET 182.50", "tea paid 91.00 rice paid 93.50 soup open 66.00 TOTAL PAID TARGET 184.50")
out = out.replace('"model_guess": 190.25, "expected": 182.50', '"model_guess": 192.25, "expected": 184.50')
(S / "c1892_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1887_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1887", "C1893"), ("c1887", "c1893")]:
    out = out.replace(a, b2)
(S / "c1893_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1894_scorecard_and_stage.py").write_text(SC1894, encoding="utf-8")
print("scorecard from fixed c1882 conf-gate pattern")
print("OK builder v297 ready")
'''
pre = "SC1894 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v297.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1889_vision_v297", "ashford", "fernford", "T297", "1188", "1912", "confidence_gate", "retarget_296"]:
    print(needle, needle in (h+pre+tail))
