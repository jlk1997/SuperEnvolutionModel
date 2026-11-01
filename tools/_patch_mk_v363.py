from pathlib import Path
import re
p = Path("tools/_mk_v363.py")
t = p.read_text(encoding="utf-8")
# source builder
t = t.replace('tools/_build_v360.py', 'tools/_build_v362.py')
t = t.replace('# V360 knife = product-U2C', '# V362 knife = product-U2C')
t = t.replace('SC2272 = ', 'SC2284 = ')
# theme dale/ford from fen/brook intermediates: we'll replace brook->ford after fen->dale style
# Current file has fen->brook. Rewrite theme_pairs block entirely.
old_tp = re.search(r"theme_pairs = \[[\s\S]*?\]\n", t).group(0)
new_tp = '''theme_pairs = [
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
'''
t = t.replace(old_tp, new_tp)
# pairs block
old_pairs = re.search(r"pairs = \[[\s\S]*?\]\n", t).group(0)
new_pairs = '''pairs = [
    ("*dale ; stack mid-band", "*ford ; stack mid-band"),
    ("T362", "T363"), ("TR362", "TR363"), ("HO362", "HO363"),
    ("NEW362", "NEW363"),
    ("V362", "V363"), ("v362", "v363"),
    ("_v362_themes.json", "_v363_themes.json"),
    ("_v361_themes.json", "_v362_themes.json"),
    ("OLD361", "OLD362"),
    ("vision_images_v362", "vision_images_v363"),
    ("VL_GATE_V362", "VL_GATE_V363"), ("vl_gate_v362", "vl_gate_v363"),
    ("C2279", "C2285"), ("c2279", "c2285"),
    ("C2280", "C2286"), ("c2280", "c2286"),
    ("C2281", "C2287"), ("c2281", "c2287"),
    ("_v362c2279", "_v363c2285"),
    ("Harder than V360", "Harder than V361"),
    ("harder than V360", "harder than V361"),
    ("NEW themes vs V360:", "NEW themes vs V361:"),
    ("kept on V362", "kept on V363"),
    ("V362 keeps floor", "V363 keeps floor"),
    ("C2279 design+fixtures; no VL claim", "C2285 design+fixtures; no VL claim"),
    ("retarget_361", "retarget_362"),
    ("*dale", "*ford"),
]
'''
t = t.replace(old_pairs, new_pairs)
# bait replaces
for a,b in [
    ('ASHFEN bait 261.71', 'ASHDALE bait 263.73'),
    ('ASHBROOK bait 262.72', 'ASHFORD bait 264.74'),
    ('CEDARF bait 275.85', 'CEDARD bait 277.87'),
    ('CEDARB bait 276.86', 'CEDARF bait 278.88'),
    ('DAWNF ghost 198.09', 'DAWND ghost 200.11'),
    ('DAWNB ghost 199.10', 'DAWNF ghost 201.12'),
    ('GLENF bait 268.78', 'GLEND bait 270.80'),
    ('GLENB bait 269.79', 'GLENF bait 271.81'),
    ('JADEF bait 259.69', 'JADED bait 261.71'),
    ('JADEB bait 260.70', 'JADEF bait 262.72'),
    ('NETHERF bait 276.86', 'NETHERD bait 278.88'),
    ('NETHERB bait 277.87', 'NETHERF bait 279.89'),
]:
    t = t.replace(a,b)
# TR/HO
TR = '''TR = """TR363 = [
    [2390.0, 2407.5, 2130.0],[840, 760, 820],[2247.0, 2248.25, 2043.0],[2446.0, 2463.0, 2198.0],
    [2491.0, 2496.0, 2168.0],[2226, 2242, 2126],[490.0, 530.0, 760.0],[2356.0, 2387.75, 2132.0],
    [840.0, 760.0, 820.0],[2423.0, 2411.0, 2129.0],[1,1,0],[0,0,0],
    [2449.0, 2472.5, 2098.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""'''
HO = '''HO = """HO363 = [
    [2188.0, 2200.75, 2049.0],[640, 660, 820],[2131.0, 2145.5, 2024.0],[2261.0, 2277.0, 2080.0],
    [2265.0, 2276.0, 2073.0],[2084, 2096, 2046],[420.0, 460.0, 740.0],[2172.0, 2193.75, 2049.0],
    [740.0, 780.0, 820.0],[2219.0, 2205.0, 2046.0],[1,1,0],[0,0,0],
    [2249.0, 2263.5, 2053.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""'''
t = re.sub(r'TR = """TR361 = \[[\s\S]*?\]"""', TR, t, count=1)
t = re.sub(r'HO = """HO361 = \[[\s\S]*?\]"""', HO, t, count=1)
t = t.replace('r"TR361\\s*=', 'r"TR363\\s*=')
t = t.replace('r"HO361\\s*=', 'r"HO363\\s*=')
# scorecard cycle map
sc_map = [
    ('("C2098", "C2278")', '("C2098", "C2290")'),
    ('("c2098", "c2278")', '("c2098", "c2290")'),
    ('("C2096", "C2276")', '("C2096", "C2288")'),
    ('("c2096", "c2276")', '("c2096", "c2288")'),
    ('("C2097", "C2277")', '("C2097", "C2289")'),
    ('("c2097", "c2277")', '("c2097", "c2289")'),
    ('("C2094", "C2274")', '("C2094", "C2286")'),
    ('("c2094", "c2274")', '("c2094", "c2286")'),
    ('("C2095", "C2275")', '("C2095", "C2287")'),
    ('("c2095", "c2275")', '("c2095", "c2287")'),
    ('("C2093", "C2273")', '("C2093", "C2285")'),
    ('("c2093", "c2273")', '("c2093", "c2285")'),
    ('("C2090", "C2270")', '("C2090", "C2282")'),
    ('("c2090", "c2270")', '("c2090", "c2282")'),
    ('("V331", "V361")', '("V331", "V363")'),
    ('("v331", "v361")', '("v331", "v363")'),
    ('STAGE_ANT_C2278', 'STAGE_ANT_C2290'),
    ('("*vale", "*brook")', '("*vale", "*ford")'),
]
for a,b in sc_map:
    t = t.replace(a,b)
# rewrite tail from knife comment
idx = t.find("# V361 knife = confidence-gate")
if idx < 0:
    raise SystemExit('tail not found')
# keep head through SC body assignment start; find SC2278 = 
# Actually after replacements we still have SC2278 / tail for v361. Replace SC2278->SC2290 and rewrite tail.
t_head = t[:idx]
t_head = t_head.replace('SC2278', 'SC2290')
tail = r'''# V363 knife = confidence-gate (alternating; V362 was product-U2C)
out = (S / "c2276_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2276", "C2288"), ("c2276", "c2288"),
    ("C2096", "C2288"), ("c2096", "c2288"),
    ("cg110_", "cg105_"),
    ("conf_gate_stretch_c2288", "conf_gate_stretch_c2288"),
    ("confidence_gate_stretch_v173", "confidence_gate_stretch_v168"),
    ("Stretch vs C2156", "Stretch vs C2162"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 182.00 b paid 186.75 c open 142.00 TOTAL PAID TARGET 368.75", "a paid 188.00 b paid 192.75 c open 148.00 TOTAL PAID TARGET 380.75")
out = out.replace('"model_guess": 999.0, "expected": 368.75', '"model_guess": 999.0, "expected": 380.75')
out = out.replace("SKU1 qty 177 ok SKU2 qty 151 hold SKU3 qty 181 ok qty_sum TARGET 358", "SKU1 qty 183 ok SKU2 qty 157 hold SKU3 qty 187 ok qty_sum TARGET 370")
out = out.replace('"model_guess": 370.0, "expected": 358.0', '"model_guess": 382.0, "expected": 370.0')
out = out.replace("itemR1 158.00 done itemR2 161.75 done itemR3 139.00 open refund_done TARGET 319.75", "itemR1 164.00 done itemR2 167.75 done itemR3 145.00 open refund_done TARGET 331.75")
out = out.replace('"model_guess": 328.5, "expected": 319.75', '"model_guess": 340.5, "expected": 331.75')
out = out.replace("T1 226.00 paid T2 166.00 open T3 207.00 paid tax_base_paid TARGET 433.00", "T1 232.00 paid T2 172.00 open T3 213.00 paid tax_base_paid TARGET 445.00")
out = out.replace('"model_guess": 469.0, "expected": 433.0', '"model_guess": 481.0, "expected": 445.0')
out = out.replace("A 1721 active B 430 leave C 1605 active payroll_active TARGET 3326", "A 1727 active B 436 leave C 1611 active payroll_active TARGET 3338")
out = out.replace('"model_guess": 3556.0, "expected": 3326.0', '"model_guess": 3568.0, "expected": 3338.0')
out = out.replace("P1 171 ok P2 150 hold P3 170 ok ship_ok_qty TARGET 341", "P1 177 ok P2 156 hold P3 176 ok ship_ok_qty TARGET 353")
out = out.replace('"model_guess": 360.0, "expected": 341.0', '"model_guess": 372.0, "expected": 353.0')
out = out.replace("S1 pri 160 open S2 pri 163 closed S3 pri 172 open open_pri_sum TARGET 332", "S1 pri 166 open S2 pri 169 closed S3 pri 178 open open_pri_sum TARGET 344")
out = out.replace('"model_guess": 364.0, "expected": 332.0', '"model_guess": 376.0, "expected": 344.0')
out = out.replace("X 202.00 open Y 205.00 open paid_total TARGET 0.00 bait 407.00", "X 208.00 open Y 211.00 open paid_total TARGET 0.00 bait 419.00")
out = out.replace('"model_guess": 407.0, "expected": 0.0', '"model_guess": 419.0, "expected": 0.0')
out = out.replace("alpha paid 167.00 beta paid 170.00 gamma open 140.00 TOTAL PAID TARGET 337.00", "alpha paid 173.00 beta paid 176.00 gamma open 146.00 TOTAL PAID TARGET 349.00")
out = out.replace('"model_guess": 337.0, "expected": 337.0', '"model_guess": 349.0, "expected": 349.0')
out = out.replace("SKU1 qty 151 ok SKU2 qty 139 hold SKU3 qty 153 ok qty_sum TARGET 304", "SKU1 qty 157 ok SKU2 qty 145 hold SKU3 qty 159 ok qty_sum TARGET 316")
out = out.replace('"model_guess": 304.0, "expected": 304.0', '"model_guess": 316.0, "expected": 316.0')
out = out.replace("itemR1 144.00 done itemR2 146.25 done itemR3 133.00 open refund_done TARGET 290.25", "itemR1 150.00 done itemR2 152.25 done itemR3 139.00 open refund_done TARGET 302.25")
out = out.replace('"model_guess": 290.25, "expected": 290.25', '"model_guess": 302.25, "expected": 302.25')
out = out.replace("tea paid 163.00 rice paid 165.50 soup open 138.00 TOTAL PAID TARGET 328.50", "tea paid 169.00 rice paid 171.50 soup open 144.00 TOTAL PAID TARGET 340.50")
out = out.replace('"model_guess": 336.25, "expected": 328.50', '"model_guess": 348.25, "expected": 340.50')
(S / "c2288_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2276_confidence_gate_stretch.py")

out = (S / "c2283_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2283", "C2289"), ("c2283", "c2289")]:
    out = out.replace(a, b2)
(S / "c2289_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2290_scorecard_and_stage.py").write_text(SC2290, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v363 ready")
'''
# find pre = SC... line and keep from start of file through pre+
# The structure is: ... sc_body replaces ... then tail = r'''...''' then pre = "SC... then text = h + pre + tail
# After idx we have the old tail = r'''...'''; pre=...; text=...; write; needles
# Replace everything from idx onward with new tail assignment + pre + write + needles
rest = '''tail = r\'\'\'%s\'\'\'
pre = "SC2290 = " + repr(sc_body) + "\\n"
text = h + pre + tail
(ROOT / "tools/_build_v363.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2285_vision_v363", "ashford", "fernford", "T363", "1188", "2043", "confidence_gate", "retarget_362", "2248.25"]:
    print(needle, needle in text)
''' % tail
# Wait - nested quotes nightmare. Do differently.
p.write_text(t_head, encoding='utf-8')
print('head written', len(t_head))
open('tools/_mk_v363_tail_payload.py','w',encoding='utf-8').write('TAIL='+repr(tail)+'\n')
print('tail payload ok', len(tail))
