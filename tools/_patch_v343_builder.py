from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v342.py").read_text(encoding="utf-8")
idx0 = b0.find('# V342 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2164 = " in head0:
    head0 = head0[:head0.find("SC2164 = ")]

theme_pairs = [
    ("netherhurst", "nethermere"), ("NETHERHURST", "NETHERMERE"),
    ("cedarhurst", "cedarmere"), ("CEDARHURST", "CEDARMERE"),
    ("dawnhurst", "dawnmere"), ("DAWNHURST", "DAWNMERE"),
    ("fernhurst", "fernmere"), ("FERNHURST", "FERNMERE"),
    ("glenhurst", "glenmere"), ("GLENHURST", "GLENMERE"),
    ("hazehurst", "hazemere"), ("HAZEHURST", "HAZEMERE"),
    ("jadehurst", "jademere"), ("JADEHURST", "JADEMERE"),
    ("knothurst", "knotmere"), ("KNOTHURST", "KNOTMERE"),
    ("lakehurst", "lakemere"), ("LAKEHURST", "LAKEMERE"),
    ("mosshurst", "mossmere"), ("MOSSHURST", "MOSSMERE"),
    ("pinehurst", "pinemere"), ("PINEHURST", "PINEMERE"),
    ("quillhurst", "quillmere"), ("QUILLHURST", "QUILLMERE"),
    ("reedhurst", "reedmere"), ("REEDHURST", "REEDMERE"),
    ("stonehurst", "stonemere"), ("STONEHURST", "STONEMERE"),
    ("ashhurst", "ashmere"), ("ASHHURST", "ASHMERE"),
    ("elmhurst", "elmmere"), ("ELMHURST", "ELMMERE"),
    ("inkhurst", "inkmere"), ("INKHURST", "INKMERE"),
    ("oakhurst", "oakmere"), ("OAKHURST", "OAKMERE"),
]
pairs = [
    ("*hurst ; stack mid-band", "*mere ; stack mid-band"),
    ("T342", "T343"), ("TR342", "TR343"), ("HO342", "HO343"),
    ("NEW342", "NEW343"),
    ("V342", "V343"), ("v342", "v343"),
    ("_v342_themes.json", "_v343_themes.json"),
    ("_v341_themes.json", "_v342_themes.json"),
    ("OLD341", "OLD342"),
    ("vision_images_v342", "vision_images_v343"),
    ("VL_GATE_V342", "VL_GATE_V343"), ("vl_gate_v342", "vl_gate_v343"),
    ("C2159", "C2165"), ("c2159", "c2165"),
    ("C2160", "C2166"), ("c2160", "c2166"),
    ("C2161", "C2167"), ("c2161", "c2167"),
    ("_v342c2159", "_v343c2165"),
    ("Harder than V340", "Harder than V341"),
    ("harder than V340", "harder than V341"),
    ("NEW themes vs V340:", "NEW themes vs V341:"),
    ("kept on V342", "kept on V343"),
    ("V342 keeps floor", "V343 keeps floor"),
    ("C2159 design+fixtures; no VL claim", "C2165 design+fixtures; no VL claim"),
    ("retarget_341", "retarget_342"),
    ("*hurst", "*mere"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHURST bait 247.57", "ASHMERE bait 248.58")
h = h.replace("CEDARH bait 257.67", "CEDARM bait 258.68")
h = h.replace("DAWNH ghost 180.90", "DAWNM ghost 181.91")
h = h.replace("GLENH bait 250.60", "GLENM bait 251.61")
h = h.replace("JADEH bait 241.51", "JADEM bait 242.52")
h = h.replace("NETHERH bait 258.68", "NETHERM bait 259.69")

TR = '''TR343 = [
    [2350.0, 2367.5, 2090.0],[840, 760, 820],[2251.0, 2257.25, 2056.0],[2406.0, 2423.0, 2158.0],
    [2468.0, 2492.0, 2128.0],[2186, 2202, 2086],[490.0, 530.0, 760.0],[2316.0, 2347.75, 2092.0],
    [840.0, 760.0, 820.0],[2383.0, 2371.0, 2089.0],[1,1,0],[0,0,0],
    [2449.0, 2470.5, 2114.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO343 = [
    [2148.0, 2160.75, 2009.0],[640, 660, 820],[2091.0, 2105.5, 1984.0],[2221.0, 2237.0, 2040.0],
    [2235.0, 2246.0, 2033.0],[2044, 2056, 2006],[420.0, 460.0, 740.0],[2132.0, 2153.75, 2009.0],
    [740.0, 780.0, 820.0],[2179.0, 2165.0, 2006.0],[1,1,0],[0,0,0],
    [2214.0, 2229.5, 2019.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR343\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO343\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2170"), ("c2098", "c2170"),
    ("C2096", "C2168"), ("c2096", "c2168"),
    ("C2097", "C2169"), ("c2097", "c2169"),
    ("C2094", "C2166"), ("c2094", "c2166"),
    ("C2095", "C2167"), ("c2095", "c2167"),
    ("C2093", "C2165"), ("c2093", "c2165"),
    ("C2090", "C2162"), ("c2090", "c2162"),
    ("V331", "V343"), ("v331", "v343"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2170"),
    ("*hurst", "*mere"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V343 knife = confidence-gate (alternating; V342 was product-U2C)
out = (S / "c2156_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2156", "C2168"), ("c2156", "c2168"),
    ("C2096", "C2168"), ("c2096", "c2168"),
    ("cg154_", "cg150_"),
    ("conf_gate_stretch_c2168", "conf_gate_stretch_c2168"),
    ("confidence_gate_stretch_v217", "confidence_gate_stretch_v213"),
    ("Stretch vs C2156", "Stretch vs C2108"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75", "a paid 133.00 b paid 137.75 c open 93.00 TOTAL PAID TARGET 270.75")
out = out.replace('"model_guess": 999.0, "expected": 260.75', '"model_guess": 999.0, "expected": 270.75')
out = out.replace("SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250", "SKU1 qty 128 ok SKU2 qty 102 hold SKU3 qty 132 ok qty_sum TARGET 260")
out = out.replace('"model_guess": 262.0, "expected": 250.0', '"model_guess": 272.0, "expected": 260.0')
out = out.replace("itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75", "itemR1 109.00 done itemR2 112.75 done itemR3 90.00 open refund_done TARGET 221.75")
out = out.replace('"model_guess": 220.5, "expected": 211.75', '"model_guess": 230.5, "expected": 221.75')
out = out.replace("T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00", "T1 177.00 paid T2 117.00 open T3 158.00 paid tax_base_paid TARGET 335.00")
out = out.replace('"model_guess": 361.0, "expected": 325.0', '"model_guess": 371.0, "expected": 335.0')
out = out.replace("A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218", "A 1672 active B 381 leave C 1556 active payroll_active TARGET 3228")
out = out.replace('"model_guess": 3448.0, "expected": 3218.0', '"model_guess": 3458.0, "expected": 3228.0')
out = out.replace("P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233", "P1 122 ok P2 101 hold P3 121 ok ship_ok_qty TARGET 243")
out = out.replace('"model_guess": 252.0, "expected": 233.0', '"model_guess": 262.0, "expected": 243.0')
out = out.replace("S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224", "S1 pri 111 open S2 pri 114 closed S3 pri 123 open open_pri_sum TARGET 234")
out = out.replace('"model_guess": 256.0, "expected": 224.0', '"model_guess": 266.0, "expected": 234.0')
out = out.replace("X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00", "X 153.00 open Y 156.00 open paid_total TARGET 0.00 bait 309.00")
out = out.replace('"model_guess": 299.0, "expected": 0.0', '"model_guess": 309.0, "expected": 0.0')
out = out.replace("alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00", "alpha paid 118.00 beta paid 121.00 gamma open 91.00 TOTAL PAID TARGET 239.00")
out = out.replace('"model_guess": 229.0, "expected": 229.0', '"model_guess": 239.0, "expected": 239.0')
out = out.replace("SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196", "SKU1 qty 102 ok SKU2 qty 90 hold SKU3 qty 104 ok qty_sum TARGET 206")
out = out.replace('"model_guess": 196.0, "expected": 196.0', '"model_guess": 206.0, "expected": 206.0')
out = out.replace("itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25", "itemR1 95.00 done itemR2 97.25 done itemR3 84.00 open refund_done TARGET 192.25")
out = out.replace('"model_guess": 182.25, "expected": 182.25', '"model_guess": 192.25, "expected": 192.25')
out = out.replace("tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50", "tea paid 114.00 rice paid 116.50 soup open 89.00 TOTAL PAID TARGET 230.50")
out = out.replace('"model_guess": 228.25, "expected": 220.50', '"model_guess": 238.25, "expected": 230.50')
(S / "c2168_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2156_confidence_gate_stretch.py")

out = (S / "c2163_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2163", "C2169"), ("c2163", "c2169")]:
    out = out.replace(a, b2)
(S / "c2169_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2170_scorecard_and_stage.py").write_text(SC2170, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v343 ready")
'''
pre = "SC2170 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v343.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2165_vision_v343", "ashmere", "fernmere", "T343", "1188", "2006", "confidence_gate", "retarget_342", "2257.25"]:
    print(needle, needle in (h+pre+tail))
