from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v356.py").read_text(encoding="utf-8")
idx0 = b0.find("# V356 knife = product-U2C")
if idx0 < 0:
    raise SystemExit("knife not found")
head0 = b0[:idx0]
if "SC2248 = " in head0:
    head0 = head0[:head0.find("SC2248 = ")]
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
    ("T356", "T357"), ("TR356", "TR357"), ("HO356", "HO357"),
    ("NEW356", "NEW357"),
    ("V356", "V357"), ("v356", "v357"),
    ("_v356_themes.json", "_v357_themes.json"),
    ("_v355_themes.json", "_v356_themes.json"),
    ("OLD355", "OLD356"),
    ("vision_images_v356", "vision_images_v357"),
    ("VL_GATE_V356", "VL_GATE_V357"), ("vl_gate_v356", "vl_gate_v357"),
    ("C2243", "C2249"), ("c2243", "c2249"),
    ("C2244", "C2250"), ("c2244", "c2250"),
    ("C2245", "C2251"), ("c2245", "c2251"),
    ("_v356c2243", "_v357c2249"),
    ("Harder than V354", "Harder than V355"),
    ("harder than V354", "harder than V355"),
    ("NEW themes vs V354:", "NEW themes vs V355:"),
    ("kept on V356", "kept on V357"),
    ("V356 keeps floor", "V357 keeps floor"),
    ("C2243 design+fixtures; no VL claim", "C2249 design+fixtures; no VL claim"),
    ("retarget_355", "retarget_356"),
    ("*croft", "*holm"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)
h = h.replace("ASHCROFT bait 257.67", "ASHHOLM bait 258.68")
h = h.replace("CEDARC bait 271.81", "CEDARH bait 272.82")
h = h.replace("DAWNC ghost 194.05", "DAWNH ghost 195.06")
h = h.replace("GLENC bait 264.74", "GLENH bait 265.75")
h = h.replace("JADEC bait 255.65", "JADEH bait 256.66")
h = h.replace("NETHERC bait 272.82", "NETHERH bait 273.83")
TR = """TR357 = [
    [2378.0, 2395.5, 2118.0],[840, 760, 820],[2247.0, 2248.25, 2046.0],[2434.0, 2451.0, 2186.0],
    [2496.0, 2499.0, 2156.0],[2214, 2230, 2114],[490.0, 530.0, 760.0],[2344.0, 2375.75, 2120.0],
    [840.0, 760.0, 820.0],[2411.0, 2399.0, 2117.0],[1,1,0],[0,0,0],
    [2455.0, 2474.5, 2104.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO357 = [
    [2176.0, 2188.75, 2037.0],[640, 660, 820],[2119.0, 2133.5, 2012.0],[2249.0, 2265.0, 2068.0],
    [2253.0, 2264.0, 2061.0],[2072, 2084, 2034],[420.0, 460.0, 740.0],[2160.0, 2181.75, 2037.0],
    [740.0, 780.0, 820.0],[2207.0, 2193.0, 2034.0],[1,1,0],[0,0,0],
    [2237.0, 2251.5, 2041.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
h = re.sub(r"TR357\s*=\s*\[[\s\S]*?\n\]", TR, h, count=1)
h = re.sub(r"HO357\s*=\s*\[[\s\S]*?\n\]", HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
sc_body = (ROOT / "scripts/c2098_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2098", "C2254"), ("c2098", "c2254"),
    ("C2096", "C2252"), ("c2096", "c2252"),
    ("C2097", "C2253"), ("c2097", "c2253"),
    ("C2094", "C2250"), ("c2094", "c2250"),
    ("C2095", "C2251"), ("c2095", "c2251"),
    ("C2093", "C2249"), ("c2093", "c2249"),
    ("C2090", "C2246"), ("c2090", "c2246"),
    ("V331", "V357"), ("v331", "v357"),
    ("STAGE_ANT_C2098", "STAGE_ANT_C2254"),
    ("*vale", "*holm"),
]:
    sc_body = sc_body.replace(a, b2)
tail = r'''# V357 knife = confidence-gate (alternating; V356 was product-U2C)
out = (S / "c2240_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2240", "C2252"), ("c2240", "c2252"),
    ("C2096", "C2252"), ("c2096", "c2252"),
    ("cg125_", "cg120_"),
    ("conf_gate_stretch_c2252", "conf_gate_stretch_c2252"),
    ("confidence_gate_stretch_v188", "confidence_gate_stretch_v183"),
    ("Stretch vs C2138", "Stretch vs C2144"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 164.00 b paid 168.75 c open 124.00 TOTAL PAID TARGET 332.75", "a paid 170.00 b paid 174.75 c open 130.00 TOTAL PAID TARGET 344.75")
out = out.replace('"model_guess": 999.0, "expected": 332.75', '"model_guess": 999.0, "expected": 344.75')
out = out.replace("SKU1 qty 159 ok SKU2 qty 133 hold SKU3 qty 163 ok qty_sum TARGET 322", "SKU1 qty 165 ok SKU2 qty 139 hold SKU3 qty 169 ok qty_sum TARGET 334")
out = out.replace('"model_guess": 334.0, "expected": 322.0', '"model_guess": 346.0, "expected": 334.0')
out = out.replace("itemR1 140.00 done itemR2 143.75 done itemR3 121.00 open refund_done TARGET 283.75", "itemR1 146.00 done itemR2 149.75 done itemR3 127.00 open refund_done TARGET 295.75")
out = out.replace('"model_guess": 292.5, "expected": 283.75', '"model_guess": 304.5, "expected": 295.75')
out = out.replace("T1 208.00 paid T2 148.00 open T3 189.00 paid tax_base_paid TARGET 397.00", "T1 214.00 paid T2 154.00 open T3 195.00 paid tax_base_paid TARGET 409.00")
out = out.replace('"model_guess": 433.0, "expected": 397.0', '"model_guess": 445.0, "expected": 409.0')
out = out.replace("A 1703 active B 412 leave C 1587 active payroll_active TARGET 3290", "A 1709 active B 418 leave C 1593 active payroll_active TARGET 3302")
out = out.replace('"model_guess": 3520.0, "expected": 3290.0', '"model_guess": 3532.0, "expected": 3302.0')
out = out.replace("P1 153 ok P2 132 hold P3 152 ok ship_ok_qty TARGET 305", "P1 159 ok P2 138 hold P3 158 ok ship_ok_qty TARGET 317")
out = out.replace('"model_guess": 324.0, "expected": 305.0', '"model_guess": 336.0, "expected": 317.0')
out = out.replace("S1 pri 142 open S2 pri 145 closed S3 pri 154 open open_pri_sum TARGET 296", "S1 pri 148 open S2 pri 151 closed S3 pri 160 open open_pri_sum TARGET 308")
out = out.replace('"model_guess": 328.0, "expected": 296.0', '"model_guess": 340.0, "expected": 308.0')
out = out.replace("X 184.00 open Y 187.00 open paid_total TARGET 0.00 bait 371.00", "X 190.00 open Y 193.00 open paid_total TARGET 0.00 bait 383.00")
out = out.replace('"model_guess": 371.0, "expected": 0.0', '"model_guess": 383.0, "expected": 0.0')
out = out.replace("alpha paid 149.00 beta paid 152.00 gamma open 122.00 TOTAL PAID TARGET 301.00", "alpha paid 155.00 beta paid 158.00 gamma open 128.00 TOTAL PAID TARGET 313.00")
out = out.replace('"model_guess": 301.0, "expected": 301.0', '"model_guess": 313.0, "expected": 313.0')
out = out.replace("SKU1 qty 133 ok SKU2 qty 121 hold SKU3 qty 135 ok qty_sum TARGET 268", "SKU1 qty 139 ok SKU2 qty 127 hold SKU3 qty 141 ok qty_sum TARGET 280")
out = out.replace('"model_guess": 268.0, "expected": 268.0', '"model_guess": 280.0, "expected": 280.0')
out = out.replace("itemR1 126.00 done itemR2 128.25 done itemR3 115.00 open refund_done TARGET 254.25", "itemR1 132.00 done itemR2 134.25 done itemR3 121.00 open refund_done TARGET 266.25")
out = out.replace('"model_guess": 254.25, "expected": 254.25', '"model_guess": 266.25, "expected": 266.25')
out = out.replace("tea paid 145.00 rice paid 147.50 soup open 120.00 TOTAL PAID TARGET 292.50", "tea paid 151.00 rice paid 153.50 soup open 126.00 TOTAL PAID TARGET 304.50")
out = out.replace('"model_guess": 300.25, "expected": 292.50', '"model_guess": 312.25, "expected": 304.50')
(S / "c2252_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2240_confidence_gate_stretch.py")

out = (S / "c2247_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2247", "C2253"), ("c2247", "c2253")]:
    out = out.replace(a, b2)
(S / "c2253_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2254_scorecard_and_stage.py").write_text(SC2254, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v357 ready")
'''
pre = "SC2254 = " + repr(sc_body) + "\n"
text = h + pre + tail
(ROOT / "tools/_build_v357.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2249_vision_v357", "ashholm", "fernholm", "T357", "1188", "2034", "confidence_gate", "retarget_356", "2248.25"]:
    print(needle, needle in text)
