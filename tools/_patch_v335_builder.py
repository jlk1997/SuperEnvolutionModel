from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v334.py").read_text(encoding="utf-8")
idx0 = b0.find('# V334 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2116 = " in head0:
    head0 = head0[:head0.find("SC2116 = ")]

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
    ("T334", "T335"), ("TR334", "TR335"), ("HO334", "HO335"),
    ("NEW334", "NEW335"),
    ("V334", "V335"), ("v334", "v335"),
    ("_v334_themes.json", "_v335_themes.json"),
    ("_v333_themes.json", "_v334_themes.json"),
    ("OLD333", "OLD334"),
    ("vision_images_v334", "vision_images_v335"),
    ("VL_GATE_V334", "VL_GATE_V335"), ("vl_gate_v334", "vl_gate_v335"),
    ("C2111", "C2117"), ("c2111", "c2117"),
    ("C2112", "C2118"), ("c2112", "c2118"),
    ("C2113", "C2119"), ("c2113", "c2119"),
    ("_v334c2111", "_v335c2117"),
    ("Harder than V332", "Harder than V333"),
    ("harder than V332", "harder than V333"),
    ("NEW themes vs V332:", "NEW themes vs V333:"),
    ("kept on V334", "kept on V335"),
    ("V334 keeps floor", "V335 keeps floor"),
    ("C2111 design+fixtures; no VL claim", "C2117 design+fixtures; no VL claim"),
    ("retarget_333", "retarget_334"),
    ("*croft", "*holm"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHCROFT bait 247.57", "ASHHOLM bait 248.58")
h = h.replace("CEDARC bait 249.59", "CEDARH bait 250.60")
h = h.replace("DAWNC ghost 172.82", "DAWNH ghost 173.83")
h = h.replace("GLENC bait 242.52", "GLENH bait 243.53")
h = h.replace("JADEC bait 233.43", "JADEH bait 234.44")
h = h.replace("NETHERC bait 250.60", "NETHERH bait 251.61")

TR = '''TR335 = [
    [2334.0, 2351.5, 2074.0],[840, 760, 820],[2253.0, 2259.25, 2048.0],[2390.0, 2407.0, 2142.0],
    [2452.0, 2476.0, 2112.0],[2170, 2186, 2070],[490.0, 530.0, 760.0],[2300.0, 2331.75, 2076.0],
    [840.0, 760.0, 820.0],[2367.0, 2355.0, 2073.0],[1,1,0],[0,0,0],
    [2433.0, 2454.5, 2098.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO335 = [
    [2132.0, 2144.75, 1993.0],[640, 660, 820],[2075.0, 2089.5, 1968.0],[2205.0, 2221.0, 2024.0],
    [2245.0, 2256.0, 2017.0],[2028, 2040, 1990],[420.0, 460.0, 740.0],[2116.0, 2137.75, 1993.0],
    [740.0, 780.0, 820.0],[2163.0, 2149.0, 1990.0],[1,1,0],[0,0,0],
    [2198.0, 2213.5, 2003.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR335\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO335\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2122"), ("c2098", "c2122"),
    ("C2096", "C2120"), ("c2096", "c2120"),
    ("C2097", "C2121"), ("c2097", "c2121"),
    ("C2094", "C2118"), ("c2094", "c2118"),
    ("C2095", "C2119"), ("c2095", "c2119"),
    ("C2093", "C2117"), ("c2093", "c2117"),
    ("C2090", "C2114"), ("c2090", "c2114"),
    ("V331", "V335"), ("v331", "v335"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2122"),
    ("*hurst", "*holm"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V335 knife = confidence-gate (alternating; V334 was product-U2C)
out = (S / "c2108_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2108", "C2120"), ("c2108", "c2120"),
    ("C2096", "C2120"), ("c2096", "c2120"),
    ("cg149_", "cg150_"),
    ("conf_gate_stretch_c2108", "conf_gate_stretch_c2120"),
    ("confidence_gate_stretch_v212", "confidence_gate_stretch_v213"),
    ("Stretch vs C2096", "Stretch vs C2108"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75", "a paid 129.00 b paid 133.75 c open 89.00 TOTAL PAID TARGET 262.75")
out = out.replace('"model_guess": 999.0, "expected": 260.75', '"model_guess": 999.0, "expected": 262.75')
out = out.replace("SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250", "SKU1 qty 124 ok SKU2 qty 98 hold SKU3 qty 128 ok qty_sum TARGET 252")
out = out.replace('"model_guess": 262.0, "expected": 250.0', '"model_guess": 264.0, "expected": 252.0')
out = out.replace("itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75", "itemR1 105.00 done itemR2 108.75 done itemR3 86.00 open refund_done TARGET 213.75")
out = out.replace('"model_guess": 220.5, "expected": 211.75', '"model_guess": 222.5, "expected": 213.75')
out = out.replace("T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00", "T1 173.00 paid T2 113.00 open T3 154.00 paid tax_base_paid TARGET 327.00")
out = out.replace('"model_guess": 361.0, "expected": 325.0', '"model_guess": 363.0, "expected": 327.0')
out = out.replace("A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218", "A 1668 active B 377 leave C 1552 active payroll_active TARGET 3220")
out = out.replace('"model_guess": 3448.0, "expected": 3218.0', '"model_guess": 3450.0, "expected": 3220.0')
out = out.replace("P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233", "P1 118 ok P2 97 hold P3 117 ok ship_ok_qty TARGET 235")
out = out.replace('"model_guess": 252.0, "expected": 233.0', '"model_guess": 254.0, "expected": 235.0')
out = out.replace("S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224", "S1 pri 107 open S2 pri 110 closed S3 pri 119 open open_pri_sum TARGET 226")
out = out.replace('"model_guess": 256.0, "expected": 224.0', '"model_guess": 258.0, "expected": 226.0')
out = out.replace("X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00", "X 149.00 open Y 152.00 open paid_total TARGET 0.00 bait 301.00")
out = out.replace('"model_guess": 299.0, "expected": 0.0', '"model_guess": 301.0, "expected": 0.0')
out = out.replace("alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00", "alpha paid 114.00 beta paid 117.00 gamma open 87.00 TOTAL PAID TARGET 231.00")
out = out.replace('"model_guess": 229.0, "expected": 229.0', '"model_guess": 231.0, "expected": 231.0')
out = out.replace("SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196", "SKU1 qty 98 ok SKU2 qty 86 hold SKU3 qty 100 ok qty_sum TARGET 198")
out = out.replace('"model_guess": 196.0, "expected": 196.0', '"model_guess": 198.0, "expected": 198.0')
out = out.replace("itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25", "itemR1 91.00 done itemR2 93.25 done itemR3 80.00 open refund_done TARGET 184.25")
out = out.replace('"model_guess": 182.25, "expected": 182.25', '"model_guess": 184.25, "expected": 184.25')
out = out.replace("tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50", "tea paid 110.00 rice paid 112.50 soup open 85.00 TOTAL PAID TARGET 222.50")
out = out.replace('"model_guess": 228.25, "expected": 220.50', '"model_guess": 230.25, "expected": 222.50')
(S / "c2120_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2108_confidence_gate_stretch.py")

out = (S / "c2115_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2115", "C2121"), ("c2115", "c2121")]:
    out = out.replace(a, b2)
(S / "c2121_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2122_scorecard_and_stage.py").write_text(SC2122, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v335 ready")
'''
pre = "SC2122 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v335.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2117_vision_v335", "ashholm", "fernholm", "T335", "1188", "1990", "confidence_gate", "retarget_334", "2259.25"]:
    print(needle, needle in (h+pre+tail))
