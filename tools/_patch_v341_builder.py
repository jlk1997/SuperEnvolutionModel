from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v340.py").read_text(encoding="utf-8")
idx0 = b0.find('# V340 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2152 = " in head0:
    head0 = head0[:head0.find("SC2152 = ")]

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
    ("T340", "T341"), ("TR340", "TR341"), ("HO340", "HO341"),
    ("NEW340", "NEW341"),
    ("V340", "V341"), ("v340", "v341"),
    ("_v340_themes.json", "_v341_themes.json"),
    ("_v339_themes.json", "_v340_themes.json"),
    ("OLD339", "OLD340"),
    ("vision_images_v340", "vision_images_v341"),
    ("VL_GATE_V340", "VL_GATE_V341"), ("vl_gate_v340", "vl_gate_v341"),
    ("C2147", "C2153"), ("c2147", "c2153"),
    ("C2148", "C2154"), ("c2148", "c2154"),
    ("C2149", "C2155"), ("c2149", "c2155"),
    ("_v340c2147", "_v341c2153"),
    ("Harder than V338", "Harder than V339"),
    ("harder than V338", "harder than V339"),
    ("NEW themes vs V338:", "NEW themes vs V339:"),
    ("kept on V340", "kept on V341"),
    ("V340 keeps floor", "V341 keeps floor"),
    ("C2147 design+fixtures; no VL claim", "C2153 design+fixtures; no VL claim"),
    ("retarget_339", "retarget_340"),
    ("*dale", "*ford"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHDALE bait 247.57", "ASHFORD bait 248.58")
h = h.replace("CEDARD bait 255.65", "CEDARF bait 256.66")
h = h.replace("DAWND ghost 178.88", "DAWNF ghost 179.89")
h = h.replace("GLEND bait 248.58", "GLENF bait 249.59")
h = h.replace("JADED bait 239.49", "JADEF bait 240.50")
h = h.replace("NETHERD bait 256.66", "NETHERF bait 257.67")

TR = '''TR341 = [
    [2346.0, 2363.5, 2086.0],[840, 760, 820],[2254.0, 2255.25, 2054.0],[2402.0, 2419.0, 2154.0],
    [2464.0, 2488.0, 2124.0],[2182, 2198, 2082],[490.0, 530.0, 760.0],[2312.0, 2343.75, 2088.0],
    [840.0, 760.0, 820.0],[2379.0, 2367.0, 2085.0],[1,1,0],[0,0,0],
    [2445.0, 2466.5, 2110.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO341 = [
    [2144.0, 2156.75, 2005.0],[640, 660, 820],[2087.0, 2101.5, 1980.0],[2217.0, 2233.0, 2036.0],
    [2237.0, 2248.0, 2029.0],[2040, 2052, 2002],[420.0, 460.0, 740.0],[2128.0, 2149.75, 2005.0],
    [740.0, 780.0, 820.0],[2175.0, 2161.0, 2002.0],[1,1,0],[0,0,0],
    [2210.0, 2225.5, 2015.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR341\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO341\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2158"), ("c2098", "c2158"),
    ("C2096", "C2156"), ("c2096", "c2156"),
    ("C2097", "C2157"), ("c2097", "c2157"),
    ("C2094", "C2154"), ("c2094", "c2154"),
    ("C2095", "C2155"), ("c2095", "c2155"),
    ("C2093", "C2153"), ("c2093", "c2153"),
    ("C2090", "C2150"), ("c2090", "c2150"),
    ("V331", "V341"), ("v331", "v341"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2158"),
    ("*hurst", "*ford"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V341 knife = confidence-gate (alternating; V340 was product-U2C)
out = (S / "c2144_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2144", "C2156"), ("c2144", "c2156"),
    ("C2096", "C2156"), ("c2096", "c2156"),
    ("cg153_", "cg150_"),
    ("conf_gate_stretch_c2156", "conf_gate_stretch_c2156"),
    ("confidence_gate_stretch_v216", "confidence_gate_stretch_v213"),
    ("Stretch vs C2144", "Stretch vs C2108"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75", "a paid 132.00 b paid 136.75 c open 92.00 TOTAL PAID TARGET 268.75")
out = out.replace('"model_guess": 999.0, "expected": 260.75', '"model_guess": 999.0, "expected": 268.75')
out = out.replace("SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250", "SKU1 qty 127 ok SKU2 qty 101 hold SKU3 qty 131 ok qty_sum TARGET 258")
out = out.replace('"model_guess": 262.0, "expected": 250.0', '"model_guess": 270.0, "expected": 258.0')
out = out.replace("itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75", "itemR1 108.00 done itemR2 111.75 done itemR3 89.00 open refund_done TARGET 219.75")
out = out.replace('"model_guess": 220.5, "expected": 211.75', '"model_guess": 228.5, "expected": 219.75')
out = out.replace("T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00", "T1 176.00 paid T2 116.00 open T3 157.00 paid tax_base_paid TARGET 333.00")
out = out.replace('"model_guess": 361.0, "expected": 325.0', '"model_guess": 369.0, "expected": 333.0')
out = out.replace("A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218", "A 1671 active B 380 leave C 1555 active payroll_active TARGET 3226")
out = out.replace('"model_guess": 3448.0, "expected": 3218.0', '"model_guess": 3456.0, "expected": 3226.0')
out = out.replace("P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233", "P1 121 ok P2 100 hold P3 120 ok ship_ok_qty TARGET 241")
out = out.replace('"model_guess": 252.0, "expected": 233.0', '"model_guess": 260.0, "expected": 241.0')
out = out.replace("S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224", "S1 pri 110 open S2 pri 113 closed S3 pri 122 open open_pri_sum TARGET 232")
out = out.replace('"model_guess": 256.0, "expected": 224.0', '"model_guess": 264.0, "expected": 232.0')
out = out.replace("X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00", "X 152.00 open Y 155.00 open paid_total TARGET 0.00 bait 307.00")
out = out.replace('"model_guess": 299.0, "expected": 0.0', '"model_guess": 307.0, "expected": 0.0')
out = out.replace("alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00", "alpha paid 117.00 beta paid 120.00 gamma open 90.00 TOTAL PAID TARGET 237.00")
out = out.replace('"model_guess": 229.0, "expected": 229.0', '"model_guess": 237.0, "expected": 237.0')
out = out.replace("SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196", "SKU1 qty 101 ok SKU2 qty 89 hold SKU3 qty 103 ok qty_sum TARGET 204")
out = out.replace('"model_guess": 196.0, "expected": 196.0', '"model_guess": 204.0, "expected": 204.0')
out = out.replace("itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25", "itemR1 94.00 done itemR2 96.25 done itemR3 83.00 open refund_done TARGET 190.25")
out = out.replace('"model_guess": 182.25, "expected": 182.25', '"model_guess": 190.25, "expected": 190.25')
out = out.replace("tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50", "tea paid 113.00 rice paid 115.50 soup open 88.00 TOTAL PAID TARGET 228.50")
out = out.replace('"model_guess": 228.25, "expected": 220.50', '"model_guess": 236.25, "expected": 228.50')
(S / "c2156_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2144_confidence_gate_stretch.py")

out = (S / "c2151_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2151", "C2157"), ("c2151", "c2157")]:
    out = out.replace(a, b2)
(S / "c2157_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2158_scorecard_and_stage.py").write_text(SC2158, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v341 ready")
'''
pre = "SC2158 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v341.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2153_vision_v341", "ashford", "fernford", "T341", "1188", "2002", "confidence_gate", "retarget_340", "2255.25"]:
    print(needle, needle in (h+pre+tail))
