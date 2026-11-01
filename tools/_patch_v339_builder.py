from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v338.py").read_text(encoding="utf-8")
idx0 = b0.find('# V338 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2140 = " in head0:
    head0 = head0[:head0.find("SC2140 = ")]

theme_pairs = [
    ("netherfen", "netherbrook"), ("NETHERFEN", "NETHERBROOK"),
    ("cedarfen", "cedarbrook"), ("CEDARFEN", "CEDARBROOK"),
    ("dawnfen", "dawnbrook"), ("DAWNFEN", "DAWNBROOK"),
    ("fernfen", "fernbrook"), ("FERNFEN", "FERNBROOK"),
    ("glenfen", "glenbrook"), ("GLENFEN", "GLENBROOK"),
    ("hazefen", "hazebrook"), ("HAZEFEN", "HAZEBROOK"),
    ("jadefen", "jadebrook"), ("JADEFEN", "JADEBROOK"),
    ("knotfen", "knotbrook"), ("KNOTFEN", "KNOTBROOK"),
    ("lakefen", "lakebrook"), ("LAKEFEN", "LAKEBROOK"),
    ("mossfen", "mossbrook"), ("MOSSFEN", "MOSSBROOK"),
    ("pinefen", "pinebrook"), ("PINEFEN", "PINEBROOK"),
    ("quillfen", "quillbrook"), ("QUILLFEN", "QUILLBROOK"),
    ("reedfen", "reedbrook"), ("REEDFEN", "REEDBROOK"),
    ("stonefen", "stonebrook"), ("STONEFEN", "STONEBROOK"),
    ("ashfen", "ashbrook"), ("ASHFEN", "ASHBROOK"),
    ("elmfen", "elmbrook"), ("ELMFEN", "ELMBROOK"),
    ("inkfen", "inkbrook"), ("INKFEN", "INKBROOK"),
    ("oakfen", "oakbrook"), ("OAKFEN", "OAKBROOK"),
]
pairs = [
    ("*fen ; stack mid-band", "*brook ; stack mid-band"),
    ("T338", "T339"), ("TR338", "TR339"), ("HO338", "HO339"),
    ("NEW338", "NEW339"),
    ("V338", "V339"), ("v338", "v339"),
    ("_v338_themes.json", "_v339_themes.json"),
    ("_v337_themes.json", "_v338_themes.json"),
    ("OLD337", "OLD338"),
    ("vision_images_v338", "vision_images_v339"),
    ("VL_GATE_V338", "VL_GATE_V339"), ("vl_gate_v338", "vl_gate_v339"),
    ("C2135", "C2141"), ("c2135", "c2141"),
    ("C2136", "C2142"), ("c2136", "c2142"),
    ("C2137", "C2143"), ("c2137", "c2143"),
    ("_v338c2135", "_v339c2141"),
    ("Harder than V336", "Harder than V337"),
    ("harder than V336", "harder than V337"),
    ("NEW themes vs V336:", "NEW themes vs V337:"),
    ("kept on V338", "kept on V339"),
    ("V338 keeps floor", "V339 keeps floor"),
    ("C2135 design+fixtures; no VL claim", "C2141 design+fixtures; no VL claim"),
    ("retarget_337", "retarget_338"),
    ("*fen", "*brook"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFEN bait 247.57", "ASHBROOK bait 248.58")
h = h.replace("CEDARF bait 253.63", "CEDARB bait 254.64")
h = h.replace("DAWNF ghost 176.86", "DAWNB ghost 177.87")
h = h.replace("GLENF bait 246.56", "GLENB bait 247.57")
h = h.replace("JADEF bait 237.47", "JADEB bait 238.48")
h = h.replace("NETHERF bait 254.64", "NETHERB bait 255.65")

TR = '''TR339 = [
    [2342.0, 2359.5, 2082.0],[840, 760, 820],[2252.0, 2258.25, 2052.0],[2398.0, 2415.0, 2150.0],
    [2460.0, 2484.0, 2120.0],[2178, 2194, 2078],[490.0, 530.0, 760.0],[2308.0, 2339.75, 2084.0],
    [840.0, 760.0, 820.0],[2375.0, 2363.0, 2081.0],[1,1,0],[0,0,0],
    [2441.0, 2462.5, 2106.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO339 = [
    [2140.0, 2152.75, 2001.0],[640, 660, 820],[2083.0, 2097.5, 1976.0],[2213.0, 2229.0, 2032.0],
    [2239.0, 2250.0, 2025.0],[2036, 2048, 1998],[420.0, 460.0, 740.0],[2124.0, 2145.75, 2001.0],
    [740.0, 780.0, 820.0],[2171.0, 2157.0, 1998.0],[1,1,0],[0,0,0],
    [2206.0, 2221.5, 2011.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR339\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO339\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2146"), ("c2098", "c2146"),
    ("C2096", "C2144"), ("c2096", "c2144"),
    ("C2097", "C2145"), ("c2097", "c2145"),
    ("C2094", "C2142"), ("c2094", "c2142"),
    ("C2095", "C2143"), ("c2095", "c2143"),
    ("C2093", "C2141"), ("c2093", "c2141"),
    ("C2090", "C2138"), ("c2090", "c2138"),
    ("V331", "V339"), ("v331", "v339"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2146"),
    ("*hurst", "*brook"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V339 knife = confidence-gate (alternating; V338 was product-U2C)
out = (S / "c2132_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2132", "C2144"), ("c2132", "c2144"),
    ("C2096", "C2144"), ("c2096", "c2144"),
    ("cg152_", "cg150_"),
    ("conf_gate_stretch_c2144", "conf_gate_stretch_c2144"),
    ("confidence_gate_stretch_v215", "confidence_gate_stretch_v213"),
    ("Stretch vs C2132", "Stretch vs C2108"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75", "a paid 131.00 b paid 135.75 c open 91.00 TOTAL PAID TARGET 266.75")
out = out.replace('"model_guess": 999.0, "expected": 260.75', '"model_guess": 999.0, "expected": 266.75')
out = out.replace("SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250", "SKU1 qty 126 ok SKU2 qty 100 hold SKU3 qty 130 ok qty_sum TARGET 256")
out = out.replace('"model_guess": 262.0, "expected": 250.0', '"model_guess": 268.0, "expected": 256.0')
out = out.replace("itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75", "itemR1 107.00 done itemR2 110.75 done itemR3 88.00 open refund_done TARGET 217.75")
out = out.replace('"model_guess": 220.5, "expected": 211.75', '"model_guess": 226.5, "expected": 217.75')
out = out.replace("T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00", "T1 175.00 paid T2 115.00 open T3 156.00 paid tax_base_paid TARGET 331.00")
out = out.replace('"model_guess": 361.0, "expected": 325.0', '"model_guess": 367.0, "expected": 331.0')
out = out.replace("A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218", "A 1670 active B 379 leave C 1554 active payroll_active TARGET 3224")
out = out.replace('"model_guess": 3448.0, "expected": 3218.0', '"model_guess": 3454.0, "expected": 3224.0')
out = out.replace("P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233", "P1 120 ok P2 99 hold P3 119 ok ship_ok_qty TARGET 239")
out = out.replace('"model_guess": 252.0, "expected": 233.0', '"model_guess": 258.0, "expected": 239.0')
out = out.replace("S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224", "S1 pri 109 open S2 pri 112 closed S3 pri 121 open open_pri_sum TARGET 230")
out = out.replace('"model_guess": 256.0, "expected": 224.0', '"model_guess": 262.0, "expected": 230.0')
out = out.replace("X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00", "X 151.00 open Y 154.00 open paid_total TARGET 0.00 bait 305.00")
out = out.replace('"model_guess": 299.0, "expected": 0.0', '"model_guess": 305.0, "expected": 0.0')
out = out.replace("alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00", "alpha paid 116.00 beta paid 119.00 gamma open 89.00 TOTAL PAID TARGET 235.00")
out = out.replace('"model_guess": 229.0, "expected": 229.0', '"model_guess": 235.0, "expected": 235.0')
out = out.replace("SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196", "SKU1 qty 100 ok SKU2 qty 88 hold SKU3 qty 102 ok qty_sum TARGET 202")
out = out.replace('"model_guess": 196.0, "expected": 196.0', '"model_guess": 202.0, "expected": 202.0')
out = out.replace("itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25", "itemR1 93.00 done itemR2 95.25 done itemR3 82.00 open refund_done TARGET 188.25")
out = out.replace('"model_guess": 182.25, "expected": 182.25', '"model_guess": 188.25, "expected": 188.25')
out = out.replace("tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50", "tea paid 112.00 rice paid 114.50 soup open 87.00 TOTAL PAID TARGET 226.50")
out = out.replace('"model_guess": 228.25, "expected": 220.50', '"model_guess": 234.25, "expected": 226.50')
(S / "c2144_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2132_confidence_gate_stretch.py")

out = (S / "c2139_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2139", "C2145"), ("c2139", "c2145")]:
    out = out.replace(a, b2)
(S / "c2145_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2146_scorecard_and_stage.py").write_text(SC2146, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v339 ready")
'''
pre = "SC2146 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v339.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2141_vision_v339", "ashbrook", "fernbrook", "T339", "1188", "1998", "confidence_gate", "retarget_338", "2258.25"]:
    print(needle, needle in (h+pre+tail))
