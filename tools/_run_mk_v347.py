from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v346.py").read_text(encoding="utf-8")
idx0 = b0.find('# V346 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2188 = " in head0:
    head0 = head0[:head0.find("SC2188 = ")]

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
    ("T346", "T347"), ("TR346", "TR347"), ("HO346", "HO347"),
    ("NEW346", "NEW347"),
    ("V346", "V347"), ("v346", "v347"),
    ("_v346_themes.json", "_v347_themes.json"),
    ("_v345_themes.json", "_v346_themes.json"),
    ("OLD345", "OLD346"),
    ("vision_images_v346", "vision_images_v347"),
    ("VL_GATE_V346", "VL_GATE_V347"), ("vl_gate_v346", "vl_gate_v347"),
    ("C2183", "C2189"), ("c2183", "c2189"),
    ("C2184", "C2190"), ("c2184", "c2190"),
    ("C2185", "C2191"), ("c2185", "c2191"),
    ("_v346c2183", "_v347c2189"),
    ("Harder than V344", "Harder than V345"),
    ("harder than V344", "harder than V345"),
    ("NEW themes vs V344:", "NEW themes vs V345:"),
    ("kept on V346", "kept on V347"),
    ("V346 keeps floor", "V347 keeps floor"),
    ("C2183 design+fixtures; no VL claim", "C2189 design+fixtures; no VL claim"),
    ("retarget_345", "retarget_346"),
    ("*holm", "*wick"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHOLM bait 247.57", "ASHWICK bait 248.58")
h = h.replace("CEDARH bait 261.71", "CEDARW bait 262.72")
h = h.replace("DAWNH ghost 184.94", "DAWNW ghost 185.95")
h = h.replace("GLENH bait 254.64", "GLENW bait 255.65")
h = h.replace("JADEH bait 245.55", "JADEW bait 246.56")
h = h.replace("NETHERH bait 262.72", "NETHERW bait 263.73")

TR = '''TR347 = [
    [2358.0, 2375.5, 2098.0],[840, 760, 820],[2248.0, 2249.25, 2057.0],[2414.0, 2431.0, 2166.0],
    [2476.0, 2499.0, 2136.0],[2194, 2210, 2094],[490.0, 530.0, 760.0],[2324.0, 2355.75, 2100.0],
    [840.0, 760.0, 820.0],[2391.0, 2379.0, 2097.0],[1,1,0],[0,0,0],
    [2457.0, 2478.5, 2122.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO347 = [
    [2156.0, 2168.75, 2017.0],[640, 660, 820],[2099.0, 2113.5, 1992.0],[2229.0, 2245.0, 2048.0],
    [2234.0, 2245.0, 2041.0],[2052, 2064, 2014],[420.0, 460.0, 740.0],[2140.0, 2161.75, 2017.0],
    [740.0, 780.0, 820.0],[2187.0, 2173.0, 2014.0],[1,1,0],[0,0,0],
    [2222.0, 2237.5, 2027.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR347\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO347\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2194"), ("c2098", "c2194"),
    ("C2096", "C2192"), ("c2096", "c2192"),
    ("C2097", "C2193"), ("c2097", "c2193"),
    ("C2094", "C2190"), ("c2094", "c2190"),
    ("C2095", "C2191"), ("c2095", "c2191"),
    ("C2093", "C2189"), ("c2093", "c2189"),
    ("C2090", "C2186"), ("c2090", "c2186"),
    ("V331", "V347"), ("v331", "v347"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2194"),
    ("*vale", "*wick"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V347 knife = confidence-gate (alternating; V346 was product-U2C)
out = (S / "c2180_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2180", "C2192"), ("c2180", "c2192"),
    ("C2096", "C2192"), ("c2096", "c2192"),
    ("cg150_", "cg145_"),
    ("conf_gate_stretch_c2192", "conf_gate_stretch_c2192"),
    ("confidence_gate_stretch_v213", "confidence_gate_stretch_v208"),
    ("Stretch vs C2108", "Stretch vs C2114"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 134.00 b paid 138.75 c open 94.00 TOTAL PAID TARGET 272.75", "a paid 140.00 b paid 144.75 c open 100.00 TOTAL PAID TARGET 284.75")
out = out.replace('"model_guess": 999.0, "expected": 272.75', '"model_guess": 999.0, "expected": 284.75')
out = out.replace("SKU1 qty 129 ok SKU2 qty 103 hold SKU3 qty 133 ok qty_sum TARGET 262", "SKU1 qty 135 ok SKU2 qty 109 hold SKU3 qty 139 ok qty_sum TARGET 274")
out = out.replace('"model_guess": 274.0, "expected": 262.0', '"model_guess": 286.0, "expected": 274.0')
out = out.replace("itemR1 110.00 done itemR2 113.75 done itemR3 91.00 open refund_done TARGET 223.75", "itemR1 116.00 done itemR2 119.75 done itemR3 97.00 open refund_done TARGET 235.75")
out = out.replace('"model_guess": 232.5, "expected": 223.75', '"model_guess": 244.5, "expected": 235.75')
out = out.replace("T1 178.00 paid T2 118.00 open T3 159.00 paid tax_base_paid TARGET 337.00", "T1 184.00 paid T2 124.00 open T3 165.00 paid tax_base_paid TARGET 349.00")
out = out.replace('"model_guess": 373.0, "expected": 337.0', '"model_guess": 385.0, "expected": 349.0')
out = out.replace("A 1673 active B 382 leave C 1557 active payroll_active TARGET 3230", "A 1679 active B 388 leave C 1563 active payroll_active TARGET 3242")
out = out.replace('"model_guess": 3460.0, "expected": 3230.0', '"model_guess": 3472.0, "expected": 3242.0')
out = out.replace("P1 123 ok P2 102 hold P3 122 ok ship_ok_qty TARGET 245", "P1 129 ok P2 108 hold P3 128 ok ship_ok_qty TARGET 257")
out = out.replace('"model_guess": 264.0, "expected": 245.0', '"model_guess": 276.0, "expected": 257.0')
out = out.replace("S1 pri 112 open S2 pri 115 closed S3 pri 124 open open_pri_sum TARGET 236", "S1 pri 118 open S2 pri 121 closed S3 pri 130 open open_pri_sum TARGET 248")
out = out.replace('"model_guess": 268.0, "expected": 236.0', '"model_guess": 280.0, "expected": 248.0')
out = out.replace("X 154.00 open Y 157.00 open paid_total TARGET 0.00 bait 311.00", "X 160.00 open Y 163.00 open paid_total TARGET 0.00 bait 323.00")
out = out.replace('"model_guess": 311.0, "expected": 0.0', '"model_guess": 323.0, "expected": 0.0')
out = out.replace("alpha paid 119.00 beta paid 122.00 gamma open 92.00 TOTAL PAID TARGET 241.00", "alpha paid 125.00 beta paid 128.00 gamma open 98.00 TOTAL PAID TARGET 253.00")
out = out.replace('"model_guess": 241.0, "expected": 241.0', '"model_guess": 253.0, "expected": 253.0')
out = out.replace("SKU1 qty 103 ok SKU2 qty 91 hold SKU3 qty 105 ok qty_sum TARGET 208", "SKU1 qty 109 ok SKU2 qty 97 hold SKU3 qty 111 ok qty_sum TARGET 220")
out = out.replace('"model_guess": 208.0, "expected": 208.0', '"model_guess": 220.0, "expected": 220.0')
out = out.replace("itemR1 96.00 done itemR2 98.25 done itemR3 85.00 open refund_done TARGET 194.25", "itemR1 102.00 done itemR2 104.25 done itemR3 91.00 open refund_done TARGET 206.25")
out = out.replace('"model_guess": 194.25, "expected": 194.25', '"model_guess": 206.25, "expected": 206.25')
out = out.replace("tea paid 115.00 rice paid 117.50 soup open 90.00 TOTAL PAID TARGET 232.50", "tea paid 121.00 rice paid 123.50 soup open 96.00 TOTAL PAID TARGET 244.50")
out = out.replace('"model_guess": 240.25, "expected": 232.50', '"model_guess": 252.25, "expected": 244.50')
(S / "c2192_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2180_confidence_gate_stretch.py")

out = (S / "c2187_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2187", "C2193"), ("c2187", "c2193")]:
    out = out.replace(a, b2)
(S / "c2193_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2194_scorecard_and_stage.py").write_text(SC2194, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v347 ready")
'''
pre = "SC2194 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v347.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2189_vision_v347", "ashwick", "fernwick", "T347", "1188", "2014", "confidence_gate", "retarget_346", "2249.25"]:
    print(needle, needle in (h+pre+tail))

# also save as patch file for traceability
(ROOT / "tools/_patch_v347_builder.py").write_text(Path(__file__).read_text(encoding="utf-8") if False else "", encoding="utf-8")
