from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v292.py").read_text(encoding="utf-8")
idx0 = b0.find('# V292 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("netherwick", "nethermoor"), ("NETHERWICK", "NETHERMOOR"),
    ("cedarwick", "cedarmoor"), ("CEDARWICK", "CEDARMOOR"),
    ("dawnwick", "dawnmoor"), ("DAWNWICK", "DAWNMOOR"),
    ("fernwick", "fernmoor"), ("FERNWICK", "FERNMOOR"),
    ("glenwick", "glenmoor"), ("GLENWICK", "GLENMOOR"),
    ("hazewick", "hazemoor"), ("HAZEWICK", "HAZEMOOR"),
    ("jadewick", "jademoor"), ("JADEWICK", "JADEMOOR"),
    ("knotwick", "knotmoor"), ("KNOTWICK", "KNOTMOOR"),
    ("lakewick", "lakemoor"), ("LAKEWICK", "LAKEMOOR"),
    ("mosswick", "mossmoor"), ("MOSSWICK", "MOSSMOOR"),
    ("pinewick", "pinemoor"), ("PINEWICK", "PINEMOOR"),
    ("quillwick", "quillmoor"), ("QUILLWICK", "QUILLMOOR"),
    ("reedwick", "reedmoor"), ("REEDWICK", "REEDMOOR"),
    ("stonewick", "stonemoor"), ("STONEWICK", "STONEMOOR"),
    ("ashwick", "ashmoor"), ("ASHWICK", "ASHMOOR"),
    ("elmwick", "elmmoor"), ("ELMWICK", "ELMMOOR"),
    ("inkwick", "inkmoor"), ("INKWICK", "INKMOOR"),
    ("oakwick", "oakmoor"), ("OAKWICK", "OAKMOOR"),
]
pairs = [
    ("*wick ; stack mid-band", "*moor ; stack mid-band"),
    ("T292", "T293"), ("TR292", "TR293"), ("HO292", "HO293"),
    ("NEW292", "NEW293"),
    ("V292", "V293"), ("v292", "v293"),
    ("_v292_themes.json", "_v293_themes.json"),
    ("_v291_themes.json", "_v292_themes.json"),
    ("OLD291", "OLD292"),
    ("vision_images_v292", "vision_images_v293"),
    ("VL_GATE_V292", "VL_GATE_V293"), ("vl_gate_v292", "vl_gate_v293"),
    ("C1859", "C1865"), ("c1859", "c1865"),
    ("C1860", "C1866"), ("c1860", "c1866"),
    ("C1861", "C1867"), ("c1861", "c1867"),
    ("_v292c1859", "_v293c1865"),
    ("Harder than V290", "Harder than V291"),
    ("harder than V290", "harder than V291"),
    ("NEW themes vs V290:", "NEW themes vs V291:"),
    ("kept on V292", "kept on V293"),
    ("V292 keeps floor", "V293 keeps floor"),
    ("C1859 design+fixtures; no VL claim", "C1865 design+fixtures; no VL claim"),
    ("retarget_291", "retarget_292"),
    ("*wick", "*moor"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHWICK bait 205.15", "ASHMOOR bait 206.16")
h = h.replace("CEDARW bait 207.17", "CEDARM bait 208.18")
h = h.replace("DAWNW ghost 130.40", "DAWNM ghost 131.41")
h = h.replace("GLENW bait 200.10", "GLENM bait 201.11")
h = h.replace("JADEW bait 191.01", "JADEM bait 192.02")
h = h.replace("NETHERW bait 208.18", "NETHERM bait 209.19")

TR = '''TR293 = [
    [2250.0, 2267.5, 1990.0],[840, 760, 820],[2173.0, 2202.25, 1968.0],[2306.0, 2323.0, 2058.0],
    [2368.0, 2392.0, 2028.0],[2086, 2102, 1986],[490.0, 530.0, 760.0],[2216.0, 2247.75, 1992.0],
    [840.0, 760.0, 820.0],[2283.0, 2271.0, 1989.0],[1,1,0],[0,0,0],
    [2349.0, 2370.5, 2014.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO293 = [
    [2048.0, 2060.75, 1909.0],[640, 660, 820],[1991.0, 2005.5, 1884.0],[2121.0, 2137.0, 1940.0],
    [2162.0, 2178.0, 1933.0],[1944, 1956, 1904],[420.0, 460.0, 740.0],[2032.0, 2053.75, 1909.0],
    [740.0, 780.0, 820.0],[2079.0, 2065.0, 1906.0],[1,1,0],[0,0,0],
    [2114.0, 2129.5, 1919.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR293\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO293\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1856_confidence_gate_stretch.py"
# Use known-good conf-gate scorecard c1858 as base
sc_body = (ROOT / "scripts/c1858_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1858", "C1870"), ("c1858", "c1870"),
    ("C1856", "C1868"), ("c1856", "c1868"),
    ("C1857", "C1869"), ("c1857", "c1869"),
    ("C1854", "C1866"), ("c1854", "c1866"),
    ("C1855", "C1867"), ("c1855", "c1867"),
    ("V291", "V293"), ("v291", "v293"),
    ("STAGE_ANT_C1858", "STAGE_ANT_C1870"),
    ("*holm", "*moor"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V293 knife = confidence-gate (alternating; V292 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1856", "C1868"), ("c1856", "c1868"),
    ("C1844", "C1868"), ("c1844", "c1868"),
    ("cg128_", "cg129_"),
    ("conf_gate_stretch_c1856", "conf_gate_stretch_c1868"),
    ("confidence_gate_stretch_v191", "confidence_gate_stretch_v192"),
    ("Stretch vs C1844", "Stretch vs C1856"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 107.00 b paid 111.75 c open 67.00 TOTAL PAID TARGET 218.75", "a paid 108.00 b paid 112.75 c open 68.00 TOTAL PAID TARGET 220.75")
out = out.replace('"model_guess": 999.0, "expected": 218.75', '"model_guess": 999.0, "expected": 220.75')
out = out.replace("SKU1 qty 102 ok SKU2 qty 76 hold SKU3 qty 106 ok qty_sum TARGET 208", "SKU1 qty 103 ok SKU2 qty 77 hold SKU3 qty 107 ok qty_sum TARGET 210")
out = out.replace('"model_guess": 220.0, "expected": 208.0', '"model_guess": 222.0, "expected": 210.0')
out = out.replace("itemR1 83.00 done itemR2 86.75 done itemR3 64.00 open refund_done TARGET 169.75", "itemR1 84.00 done itemR2 87.75 done itemR3 65.00 open refund_done TARGET 171.75")
out = out.replace('"model_guess": 178.5, "expected": 169.75', '"model_guess": 180.5, "expected": 171.75')
out = out.replace("T1 151.00 paid T2 91.00 open T3 132.00 paid tax_base_paid TARGET 283.00", "T1 152.00 paid T2 92.00 open T3 133.00 paid tax_base_paid TARGET 285.00")
out = out.replace('"model_guess": 319.0, "expected": 283.0', '"model_guess": 321.0, "expected": 285.0')
out = out.replace("A 1635 active B 355 leave C 1530 active payroll_active TARGET 3165", "A 1637 active B 356 leave C 1531 active payroll_active TARGET 3168")
out = out.replace('"model_guess": 3395.0, "expected": 3165.0', '"model_guess": 3398.0, "expected": 3168.0')
out = out.replace("P1 96 ok P2 75 hold P3 95 ok ship_ok_qty TARGET 191", "P1 97 ok P2 76 hold P3 96 ok ship_ok_qty TARGET 193")
out = out.replace('"model_guess": 210.0, "expected": 191.0', '"model_guess": 212.0, "expected": 193.0')
out = out.replace("S1 pri 85 open S2 pri 88 closed S3 pri 97 open open_pri_sum TARGET 182", "S1 pri 86 open S2 pri 89 closed S3 pri 98 open open_pri_sum TARGET 184")
out = out.replace('"model_guess": 214.0, "expected": 182.0', '"model_guess": 216.0, "expected": 184.0')
out = out.replace("X 127.00 open Y 130.00 open paid_total TARGET 0.00 bait 257.00", "X 128.00 open Y 131.00 open paid_total TARGET 0.00 bait 259.00")
out = out.replace('"model_guess": 257.0, "expected": 0.0', '"model_guess": 259.0, "expected": 0.0')
out = out.replace("alpha paid 92.00 beta paid 95.00 gamma open 65.00 TOTAL PAID TARGET 187.00", "alpha paid 93.00 beta paid 96.00 gamma open 66.00 TOTAL PAID TARGET 189.00")
out = out.replace('"model_guess": 187.0, "expected": 187.0', '"model_guess": 189.0, "expected": 189.0')
out = out.replace("SKU1 qty 76 ok SKU2 qty 64 hold SKU3 qty 78 ok qty_sum TARGET 154", "SKU1 qty 77 ok SKU2 qty 65 hold SKU3 qty 79 ok qty_sum TARGET 156")
out = out.replace('"model_guess": 154.0, "expected": 154.0', '"model_guess": 156.0, "expected": 156.0')
out = out.replace("itemR1 69.00 done itemR2 71.25 done itemR3 58.00 open refund_done TARGET 140.25", "itemR1 70.00 done itemR2 72.25 done itemR3 59.00 open refund_done TARGET 142.25")
out = out.replace('"model_guess": 140.25, "expected": 140.25', '"model_guess": 142.25, "expected": 142.25')
out = out.replace("tea paid 88.00 rice paid 90.50 soup open 63.00 TOTAL PAID TARGET 178.50", "tea paid 89.00 rice paid 91.50 soup open 64.00 TOTAL PAID TARGET 180.50")
out = out.replace('"model_guess": 186.25, "expected": 178.50', '"model_guess": 188.25, "expected": 180.50')
(S / "c1868_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1863_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1863", "C1869"), ("c1863", "c1869")]:
    out = out.replace(a, b2)
(S / "c1869_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1870_scorecard_and_stage.py").write_text(SC1870, encoding="utf-8")
print("scorecard from fixed c1858 conf-gate pattern")
print("OK builder v293 ready")
'''
pre = "SC1870 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v293.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1865_vision_v293", "ashmoor", "fernmoor", "T293", "1188", "1904", "confidence_gate", "retarget_292"]:
    print(needle, needle in (h+pre+tail))
