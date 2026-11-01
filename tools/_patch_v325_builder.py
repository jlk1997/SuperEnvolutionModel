from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v324.py").read_text(encoding="utf-8")
idx0 = b0.find('# V324 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2056 = " in head0:
    head0 = head0[:head0.find("SC2056 = ")]

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
    ("T324", "T325"), ("TR324", "TR325"), ("HO324", "HO325"),
    ("NEW324", "NEW325"),
    ("V324", "V325"), ("v324", "v325"),
    ("_v324_themes.json", "_v325_themes.json"),
    ("_v323_themes.json", "_v324_themes.json"),
    ("OLD323", "OLD324"),
    ("vision_images_v324", "vision_images_v325"),
    ("VL_GATE_V324", "VL_GATE_V325"), ("vl_gate_v324", "vl_gate_v325"),
    ("C2051", "C2057"), ("c2051", "c2057"),
    ("C2052", "C2058"), ("c2052", "c2058"),
    ("C2053", "C2059"), ("c2053", "c2059"),
    ("_v324c2051", "_v325c2057"),
    ("Harder than V322", "Harder than V323"),
    ("harder than V322", "harder than V323"),
    ("NEW themes vs V322:", "NEW themes vs V323:"),
    ("kept on V324", "kept on V325"),
    ("V324 keeps floor", "V325 keeps floor"),
    ("C2051 design+fixtures; no VL claim", "C2057 design+fixtures; no VL claim"),
    ("retarget_323", "retarget_324"),
    ("*holm", "*wick"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHOLM bait 237.47", "ASHWICK bait 238.48")
h = h.replace("CEDARH bait 239.49", "CEDARW bait 240.50")
h = h.replace("DAWNH ghost 162.72", "DAWNW ghost 163.73")
h = h.replace("GLENH bait 232.42", "GLENW bait 233.43")
h = h.replace("JADEH bait 223.33", "JADEW bait 224.34")
h = h.replace("NETHERH bait 240.50", "NETHERW bait 241.51")

TR = '''TR325 = [
    [2314.0, 2331.5, 2054.0],[840, 760, 820],[2237.0, 2246.25, 2032.0],[2370.0, 2387.0, 2122.0],
    [2432.0, 2456.0, 2092.0],[2150, 2166, 2050],[490.0, 530.0, 760.0],[2280.0, 2311.75, 2056.0],
    [840.0, 760.0, 820.0],[2347.0, 2335.0, 2053.0],[1,1,0],[0,0,0],
    [2413.0, 2434.5, 2078.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO325 = [
    [2112.0, 2124.75, 1973.0],[640, 660, 820],[2055.0, 2069.5, 1948.0],[2185.0, 2201.0, 2004.0],
    [2226.0, 2242.0, 1997.0],[2008, 2020, 1968],[420.0, 460.0, 740.0],[2096.0, 2117.75, 1973.0],
    [740.0, 780.0, 820.0],[2143.0, 2129.0, 1970.0],[1,1,0],[0,0,0],
    [2178.0, 2193.5, 1983.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR325\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO325\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2050_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2050", "C2062"), ("c2050", "c2062"),
    ("C2048", "C2060"), ("c2048", "c2060"),
    ("C2049", "C2061"), ("c2049", "c2061"),
    ("C2046", "C2058"), ("c2046", "c2058"),
    ("C2047", "C2059"), ("c2047", "c2059"),
    ("C2045", "C2057"), ("c2045", "c2057"),
    ("C2042", "C2054"), ("c2042", "c2054"),
    ("V323", "V325"), ("v323", "v325"),
    ("STAGE_ANT_C2050", "STAGE_ANT_C2062"),
    ("*croft", "*wick"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V325 knife = confidence-gate (alternating; V324 was product-U2C)
out = (S / "c2048_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2048", "C2060"), ("c2048", "c2060"),
    ("C2036", "C2060"), ("c2036", "c2060"),
    ("cg144_", "cg145_"),
    ("conf_gate_stretch_c2048", "conf_gate_stretch_c2060"),
    ("confidence_gate_stretch_v207", "confidence_gate_stretch_v208"),
    ("Stretch vs C2036", "Stretch vs C2048"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 123.00 b paid 127.75 c open 83.00 TOTAL PAID TARGET 250.75", "a paid 124.00 b paid 128.75 c open 84.00 TOTAL PAID TARGET 252.75")
out = out.replace('"model_guess": 999.0, "expected": 250.75', '"model_guess": 999.0, "expected": 252.75')
out = out.replace("SKU1 qty 118 ok SKU2 qty 92 hold SKU3 qty 122 ok qty_sum TARGET 240", "SKU1 qty 119 ok SKU2 qty 93 hold SKU3 qty 123 ok qty_sum TARGET 242")
out = out.replace('"model_guess": 252.0, "expected": 240.0', '"model_guess": 254.0, "expected": 242.0')
out = out.replace("itemR1 99.00 done itemR2 102.75 done itemR3 80.00 open refund_done TARGET 201.75", "itemR1 100.00 done itemR2 103.75 done itemR3 81.00 open refund_done TARGET 203.75")
out = out.replace('"model_guess": 210.5, "expected": 201.75', '"model_guess": 212.5, "expected": 203.75')
out = out.replace("T1 167.00 paid T2 107.00 open T3 148.00 paid tax_base_paid TARGET 315.00", "T1 168.00 paid T2 108.00 open T3 149.00 paid tax_base_paid TARGET 317.00")
out = out.replace('"model_guess": 351.0, "expected": 315.0', '"model_guess": 353.0, "expected": 317.0')
out = out.replace("A 1662 active B 371 leave C 1546 active payroll_active TARGET 3208", "A 1663 active B 372 leave C 1547 active payroll_active TARGET 3210")
out = out.replace('"model_guess": 3438.0, "expected": 3208.0', '"model_guess": 3440.0, "expected": 3210.0')
out = out.replace("P1 112 ok P2 91 hold P3 111 ok ship_ok_qty TARGET 223", "P1 113 ok P2 92 hold P3 112 ok ship_ok_qty TARGET 225")
out = out.replace('"model_guess": 242.0, "expected": 223.0', '"model_guess": 244.0, "expected": 225.0')
out = out.replace("S1 pri 101 open S2 pri 104 closed S3 pri 113 open open_pri_sum TARGET 214", "S1 pri 102 open S2 pri 105 closed S3 pri 114 open open_pri_sum TARGET 216")
out = out.replace('"model_guess": 246.0, "expected": 214.0', '"model_guess": 248.0, "expected": 216.0')
out = out.replace("X 143.00 open Y 146.00 open paid_total TARGET 0.00 bait 289.00", "X 144.00 open Y 147.00 open paid_total TARGET 0.00 bait 291.00")
out = out.replace('"model_guess": 289.0, "expected": 0.0', '"model_guess": 291.0, "expected": 0.0')
out = out.replace("alpha paid 108.00 beta paid 111.00 gamma open 81.00 TOTAL PAID TARGET 219.00", "alpha paid 109.00 beta paid 112.00 gamma open 82.00 TOTAL PAID TARGET 221.00")
out = out.replace('"model_guess": 219.0, "expected": 219.0', '"model_guess": 221.0, "expected": 221.0')
out = out.replace("SKU1 qty 92 ok SKU2 qty 80 hold SKU3 qty 94 ok qty_sum TARGET 186", "SKU1 qty 93 ok SKU2 qty 81 hold SKU3 qty 95 ok qty_sum TARGET 188")
out = out.replace('"model_guess": 186.0, "expected": 186.0', '"model_guess": 188.0, "expected": 188.0')
out = out.replace("itemR1 85.00 done itemR2 87.25 done itemR3 74.00 open refund_done TARGET 172.25", "itemR1 86.00 done itemR2 88.25 done itemR3 75.00 open refund_done TARGET 174.25")
out = out.replace('"model_guess": 172.25, "expected": 172.25', '"model_guess": 174.25, "expected": 174.25')
out = out.replace("tea paid 104.00 rice paid 106.50 soup open 79.00 TOTAL PAID TARGET 210.50", "tea paid 105.00 rice paid 107.50 soup open 80.00 TOTAL PAID TARGET 212.50")
out = out.replace('"model_guess": 218.25, "expected": 210.50', '"model_guess": 220.25, "expected": 212.50')
(S / "c2060_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2048_confidence_gate_stretch.py")

out = (S / "c2055_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2055", "C2061"), ("c2055", "c2061")]:
    out = out.replace(a, b2)
(S / "c2061_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2062_scorecard_and_stage.py").write_text(SC2062, encoding="utf-8")
print("scorecard from fixed c2050 conf-gate pattern")
print("OK builder v325 ready")
'''
pre = "SC2062 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v325.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2057_vision_v325", "ashwick", "fernwick", "T325", "1188", "1968", "confidence_gate", "retarget_324", "2246.25"]:
    print(needle, needle in (h+pre+tail))
