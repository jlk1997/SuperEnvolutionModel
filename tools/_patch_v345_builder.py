from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v344.py").read_text(encoding="utf-8")
idx0 = b0.find('# V344 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2176 = " in head0:
    head0 = head0[:head0.find("SC2176 = ")]

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
    ("T344", "T345"), ("TR344", "TR345"), ("HO344", "HO345"),
    ("NEW344", "NEW345"),
    ("V344", "V345"), ("v344", "v345"),
    ("_v344_themes.json", "_v345_themes.json"),
    ("_v343_themes.json", "_v344_themes.json"),
    ("OLD343", "OLD344"),
    ("vision_images_v344", "vision_images_v345"),
    ("VL_GATE_V344", "VL_GATE_V345"), ("vl_gate_v344", "vl_gate_v345"),
    ("C2171", "C2177"), ("c2171", "c2177"),
    ("C2172", "C2178"), ("c2172", "c2178"),
    ("C2173", "C2179"), ("c2173", "c2179"),
    ("_v344c2171", "_v345c2177"),
    ("Harder than V342", "Harder than V343"),
    ("harder than V342", "harder than V343"),
    ("NEW themes vs V342:", "NEW themes vs V343:"),
    ("kept on V344", "kept on V345"),
    ("V344 keeps floor", "V345 keeps floor"),
    ("C2171 design+fixtures; no VL claim", "C2177 design+fixtures; no VL claim"),
    ("retarget_343", "retarget_344"),
    ("*vale", "*croft"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHVALE bait 247.57", "ASHCROFT bait 248.58")
h = h.replace("CEDARV bait 259.69", "CEDARC bait 260.70")
h = h.replace("DAWNV ghost 182.92", "DAWNC ghost 183.93")
h = h.replace("GLENV bait 252.62", "GLENC bait 253.63")
h = h.replace("JADEV bait 243.53", "JADEC bait 244.54")
h = h.replace("NETHERV bait 260.70", "NETHERC bait 261.71")

TR = '''TR345 = [
    [2354.0, 2371.5, 2094.0],[840, 760, 820],[2253.0, 2259.25, 2058.0],[2410.0, 2427.0, 2162.0],
    [2472.0, 2496.0, 2132.0],[2190, 2206, 2090],[490.0, 530.0, 760.0],[2320.0, 2351.75, 2096.0],
    [840.0, 760.0, 820.0],[2387.0, 2375.0, 2093.0],[1,1,0],[0,0,0],
    [2453.0, 2474.5, 2118.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO345 = [
    [2152.0, 2164.75, 2013.0],[640, 660, 820],[2095.0, 2109.5, 1988.0],[2225.0, 2241.0, 2044.0],
    [2233.0, 2244.0, 2037.0],[2048, 2060, 2010],[420.0, 460.0, 740.0],[2136.0, 2157.75, 2013.0],
    [740.0, 780.0, 820.0],[2183.0, 2169.0, 2010.0],[1,1,0],[0,0,0],
    [2218.0, 2233.5, 2023.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR345\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO345\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2182"), ("c2098", "c2182"),
    ("C2096", "C2180"), ("c2096", "c2180"),
    ("C2097", "C2181"), ("c2097", "c2181"),
    ("C2094", "C2178"), ("c2094", "c2178"),
    ("C2095", "C2179"), ("c2095", "c2179"),
    ("C2093", "C2177"), ("c2093", "c2177"),
    ("C2090", "C2174"), ("c2090", "c2174"),
    ("V331", "V345"), ("v331", "v345"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2182"),
    ("*vale", "*croft"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V345 knife = confidence-gate (alternating; V344 was product-U2C)
out = (S / "c2168_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2168", "C2180"), ("c2168", "c2180"),
    ("C2096", "C2180"), ("c2096", "c2180"),
    ("cg155_", "cg150_"),
    ("conf_gate_stretch_c2180", "conf_gate_stretch_c2180"),
    ("confidence_gate_stretch_v218", "confidence_gate_stretch_v213"),
    ("Stretch vs C2168", "Stretch vs C2108"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75", "a paid 134.00 b paid 138.75 c open 94.00 TOTAL PAID TARGET 272.75")
out = out.replace('"model_guess": 999.0, "expected": 260.75', '"model_guess": 999.0, "expected": 272.75')
out = out.replace("SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250", "SKU1 qty 129 ok SKU2 qty 103 hold SKU3 qty 133 ok qty_sum TARGET 262")
out = out.replace('"model_guess": 262.0, "expected": 250.0', '"model_guess": 274.0, "expected": 262.0')
out = out.replace("itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75", "itemR1 110.00 done itemR2 113.75 done itemR3 91.00 open refund_done TARGET 223.75")
out = out.replace('"model_guess": 220.5, "expected": 211.75', '"model_guess": 232.5, "expected": 223.75')
out = out.replace("T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00", "T1 178.00 paid T2 118.00 open T3 159.00 paid tax_base_paid TARGET 337.00")
out = out.replace('"model_guess": 361.0, "expected": 325.0', '"model_guess": 373.0, "expected": 337.0')
out = out.replace("A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218", "A 1673 active B 382 leave C 1557 active payroll_active TARGET 3230")
out = out.replace('"model_guess": 3448.0, "expected": 3218.0', '"model_guess": 3460.0, "expected": 3230.0')
out = out.replace("P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233", "P1 123 ok P2 102 hold P3 122 ok ship_ok_qty TARGET 245")
out = out.replace('"model_guess": 252.0, "expected": 233.0', '"model_guess": 264.0, "expected": 245.0')
out = out.replace("S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224", "S1 pri 112 open S2 pri 115 closed S3 pri 124 open open_pri_sum TARGET 236")
out = out.replace('"model_guess": 256.0, "expected": 224.0', '"model_guess": 268.0, "expected": 236.0')
out = out.replace("X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00", "X 154.00 open Y 157.00 open paid_total TARGET 0.00 bait 311.00")
out = out.replace('"model_guess": 299.0, "expected": 0.0', '"model_guess": 311.0, "expected": 0.0')
out = out.replace("alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00", "alpha paid 119.00 beta paid 122.00 gamma open 92.00 TOTAL PAID TARGET 241.00")
out = out.replace('"model_guess": 229.0, "expected": 229.0', '"model_guess": 241.0, "expected": 241.0')
out = out.replace("SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196", "SKU1 qty 103 ok SKU2 qty 91 hold SKU3 qty 105 ok qty_sum TARGET 208")
out = out.replace('"model_guess": 196.0, "expected": 196.0', '"model_guess": 208.0, "expected": 208.0')
out = out.replace("itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25", "itemR1 96.00 done itemR2 98.25 done itemR3 85.00 open refund_done TARGET 194.25")
out = out.replace('"model_guess": 182.25, "expected": 182.25', '"model_guess": 194.25, "expected": 194.25')
out = out.replace("tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50", "tea paid 115.00 rice paid 117.50 soup open 90.00 TOTAL PAID TARGET 232.50")
out = out.replace('"model_guess": 228.25, "expected": 220.50', '"model_guess": 240.25, "expected": 232.50')
(S / "c2180_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2168_confidence_gate_stretch.py")

out = (S / "c2175_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2175", "C2181"), ("c2175", "c2181")]:
    out = out.replace(a, b2)
(S / "c2181_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2182_scorecard_and_stage.py").write_text(SC2182, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v345 ready")
'''
pre = "SC2182 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v345.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2177_vision_v345", "ashcroft", "ferncroft", "T345", "1188", "2010", "confidence_gate", "retarget_344", "2259.25"]:
    print(needle, needle in (h+pre+tail))
