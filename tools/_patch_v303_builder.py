from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v302.py").read_text(encoding="utf-8")
idx0 = b0.find('# V302 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1924 = " in head0:
    head0 = head0[:head0.find("SC1924 = ")]

theme_pairs = [
    ("netherholm", "netherwick"), ("NETHERHOLM", "NETHERWICK"),
    ("cedarholm", "cedarwick"), ("CEDARHOLM", "CEDARWICK"),
    ("dawnholm", "dawnwick"), ("DAWNHOLM", "DAWNWICK"),
    ("fernholm", "fernwick"), ("FERNHOLM", "FERNWICK"),
    ("glenholm", "glenwick"), ("GLENHOLM", "GLENWICK"),
    ("hazeholm", "hazewick"), ("HAZEHOLM", "HAZEWICK"),
    ("jadeholm", "jadewick"), ("JADEHOLM", "JADEWICK"),
    ("knotholm", "knotwick"), ("KNOTHOLM", "KNOTWICK"),
    ("lakeholm", "lakewick"), ("LAKEHOLM", "LAKEWICK"),
    ("mossholm", "mosswick"), ("MOSSHOLM", "MOSSWICK"),
    ("pineholm", "pinewick"), ("PINEHOLM", "PINEWICK"),
    ("quillholm", "quillwick"), ("QUILLHOLM", "QUILLWICK"),
    ("reedholm", "reedwick"), ("REEDHOLM", "REEDWICK"),
    ("stoneholm", "stonewick"), ("STONEHOLM", "STONEWICK"),
    ("ashholm", "ashwick"), ("ASHHOLM", "ASHWICK"),
    ("elmholm", "elmwick"), ("ELMHOLM", "ELMWICK"),
    ("inkholm", "inkwick"), ("INKHOLM", "INKWICK"),
    ("oakholm", "oakwick"), ("OAKHOLM", "OAKWICK"),
]
pairs = [
    ("*holm ; stack mid-band", "*wick ; stack mid-band"),
    ("T302", "T303"), ("TR302", "TR303"), ("HO302", "HO303"),
    ("NEW302", "NEW303"),
    ("V302", "V303"), ("v302", "v303"),
    ("_v302_themes.json", "_v303_themes.json"),
    ("_v301_themes.json", "_v302_themes.json"),
    ("OLD301", "OLD302"),
    ("vision_images_v302", "vision_images_v303"),
    ("VL_GATE_V302", "VL_GATE_V303"), ("vl_gate_v302", "vl_gate_v303"),
    ("C1919", "C1925"), ("c1919", "c1925"),
    ("C1920", "C1926"), ("c1920", "c1926"),
    ("C1921", "C1927"), ("c1921", "c1927"),
    ("_v302c1919", "_v303c1925"),
    ("Harder than V300", "Harder than V301"),
    ("harder than V300", "harder than V301"),
    ("NEW themes vs V300:", "NEW themes vs V301:"),
    ("kept on V302", "kept on V303"),
    ("V302 keeps floor", "V303 keeps floor"),
    ("C1919 design+fixtures; no VL claim", "C1925 design+fixtures; no VL claim"),
    ("retarget_301", "retarget_302"),
    ("*holm", "*wick"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHOLM bait 215.25", "ASHWICK bait 216.26")
h = h.replace("CEDARH bait 217.27", "CEDARW bait 218.28")
h = h.replace("DAWNH ghost 140.50", "DAWNW ghost 141.51")
h = h.replace("GLENH bait 210.20", "GLENW bait 211.21")
h = h.replace("JADEH bait 201.11", "JADEW bait 202.12")
h = h.replace("NETHERH bait 218.28", "NETHERW bait 219.29")

TR = '''TR303 = [
    [2270.0, 2287.5, 2010.0],[840, 760, 820],[2193.0, 2222.25, 1988.0],[2326.0, 2343.0, 2078.0],
    [2388.0, 2412.0, 2048.0],[2106, 2122, 2006],[490.0, 530.0, 760.0],[2236.0, 2267.75, 2012.0],
    [840.0, 760.0, 820.0],[2303.0, 2291.0, 2009.0],[1,1,0],[0,0,0],
    [2369.0, 2390.5, 2034.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO303 = [
    [2068.0, 2080.75, 1929.0],[640, 660, 820],[2011.0, 2025.5, 1904.0],[2141.0, 2157.0, 1960.0],
    [2182.0, 2198.0, 1953.0],[1964, 1976, 1924],[420.0, 460.0, 740.0],[2052.0, 2073.75, 1929.0],
    [740.0, 780.0, 820.0],[2099.0, 2085.0, 1926.0],[1,1,0],[0,0,0],
    [2134.0, 2149.5, 1939.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR303\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO303\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1916_confidence_gate_stretch.py"
sc_body = (ROOT / "scripts/c1918_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1918", "C1930"), ("c1918", "c1930"),
    ("C1916", "C1928"), ("c1916", "c1928"),
    ("C1917", "C1929"), ("c1917", "c1929"),
    ("C1914", "C1926"), ("c1914", "c1926"),
    ("C1915", "C1927"), ("c1915", "c1927"),
    ("V301", "V303"), ("v301", "v303"),
    ("STAGE_ANT_C1918", "STAGE_ANT_C1930"),
    ("*croft", "*wick"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V303 knife = confidence-gate (alternating; V302 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1916", "C1928"), ("c1916", "c1928"),
    ("C1904", "C1928"), ("c1904", "c1928"),
    ("cg133_", "cg134_"),
    ("conf_gate_stretch_c1916", "conf_gate_stretch_c1928"),
    ("confidence_gate_stretch_v196", "confidence_gate_stretch_v197"),
    ("Stretch vs C1904", "Stretch vs C1916"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 112.00 b paid 116.75 c open 72.00 TOTAL PAID TARGET 228.75", "a paid 113.00 b paid 117.75 c open 73.00 TOTAL PAID TARGET 230.75")
out = out.replace('"model_guess": 999.0, "expected": 228.75', '"model_guess": 999.0, "expected": 230.75')
out = out.replace("SKU1 qty 107 ok SKU2 qty 81 hold SKU3 qty 111 ok qty_sum TARGET 218", "SKU1 qty 108 ok SKU2 qty 82 hold SKU3 qty 112 ok qty_sum TARGET 220")
out = out.replace('"model_guess": 230.0, "expected": 218.0', '"model_guess": 232.0, "expected": 220.0')
out = out.replace("itemR1 88.00 done itemR2 91.75 done itemR3 69.00 open refund_done TARGET 179.75", "itemR1 89.00 done itemR2 92.75 done itemR3 70.00 open refund_done TARGET 181.75")
out = out.replace('"model_guess": 188.5, "expected": 179.75', '"model_guess": 190.5, "expected": 181.75')
out = out.replace("T1 156.00 paid T2 96.00 open T3 137.00 paid tax_base_paid TARGET 293.00", "T1 157.00 paid T2 97.00 open T3 138.00 paid tax_base_paid TARGET 295.00")
out = out.replace('"model_guess": 329.0, "expected": 293.0', '"model_guess": 331.0, "expected": 295.0')
out = out.replace("A 1645 active B 360 leave C 1535 active payroll_active TARGET 3180", "A 1647 active B 361 leave C 1536 active payroll_active TARGET 3183")
out = out.replace('"model_guess": 3410.0, "expected": 3180.0', '"model_guess": 3413.0, "expected": 3183.0')
out = out.replace("P1 101 ok P2 80 hold P3 100 ok ship_ok_qty TARGET 201", "P1 102 ok P2 81 hold P3 101 ok ship_ok_qty TARGET 203")
out = out.replace('"model_guess": 220.0, "expected": 201.0', '"model_guess": 222.0, "expected": 203.0')
out = out.replace("S1 pri 90 open S2 pri 93 closed S3 pri 102 open open_pri_sum TARGET 192", "S1 pri 91 open S2 pri 94 closed S3 pri 103 open open_pri_sum TARGET 194")
out = out.replace('"model_guess": 224.0, "expected": 192.0', '"model_guess": 226.0, "expected": 194.0')
out = out.replace("X 132.00 open Y 135.00 open paid_total TARGET 0.00 bait 267.00", "X 133.00 open Y 136.00 open paid_total TARGET 0.00 bait 269.00")
out = out.replace('"model_guess": 267.0, "expected": 0.0', '"model_guess": 269.0, "expected": 0.0')
out = out.replace("alpha paid 97.00 beta paid 100.00 gamma open 70.00 TOTAL PAID TARGET 197.00", "alpha paid 98.00 beta paid 101.00 gamma open 71.00 TOTAL PAID TARGET 199.00")
out = out.replace('"model_guess": 197.0, "expected": 197.0', '"model_guess": 199.0, "expected": 199.0')
out = out.replace("SKU1 qty 81 ok SKU2 qty 69 hold SKU3 qty 83 ok qty_sum TARGET 164", "SKU1 qty 82 ok SKU2 qty 70 hold SKU3 qty 84 ok qty_sum TARGET 166")
out = out.replace('"model_guess": 164.0, "expected": 164.0', '"model_guess": 166.0, "expected": 166.0')
out = out.replace("itemR1 74.00 done itemR2 76.25 done itemR3 63.00 open refund_done TARGET 150.25", "itemR1 75.00 done itemR2 77.25 done itemR3 64.00 open refund_done TARGET 152.25")
out = out.replace('"model_guess": 150.25, "expected": 150.25', '"model_guess": 152.25, "expected": 152.25')
out = out.replace("tea paid 93.00 rice paid 95.50 soup open 68.00 TOTAL PAID TARGET 188.50", "tea paid 94.00 rice paid 96.50 soup open 69.00 TOTAL PAID TARGET 190.50")
out = out.replace('"model_guess": 196.25, "expected": 188.50', '"model_guess": 198.25, "expected": 190.50')
(S / "c1928_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1923_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1923", "C1929"), ("c1923", "c1929")]:
    out = out.replace(a, b2)
(S / "c1929_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1930_scorecard_and_stage.py").write_text(SC1930, encoding="utf-8")
print("scorecard from fixed c1918 conf-gate pattern")
print("OK builder v303 ready")
'''
pre = "SC1930 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v303.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1925_vision_v303", "ashwick", "fernwick", "T303", "1188", "1924", "confidence_gate", "retarget_302"]:
    print(needle, needle in (h+pre+tail))
