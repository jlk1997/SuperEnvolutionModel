from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v316.py").read_text(encoding="utf-8")
idx0 = b0.find('# V316 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2008 = " in head0:
    head0 = head0[:head0.find("SC2008 = ")]

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
    ("T316", "T317"), ("TR316", "TR317"), ("HO316", "HO317"),
    ("NEW316", "NEW317"),
    ("V316", "V317"), ("v316", "v317"),
    ("_v316_themes.json", "_v317_themes.json"),
    ("_v315_themes.json", "_v316_themes.json"),
    ("OLD315", "OLD316"),
    ("vision_images_v316", "vision_images_v317"),
    ("VL_GATE_V316", "VL_GATE_V317"), ("vl_gate_v316", "vl_gate_v317"),
    ("C2003", "C2009"), ("c2003", "c2009"),
    ("C2004", "C2010"), ("c2004", "c2010"),
    ("C2005", "C2011"), ("c2005", "c2011"),
    ("_v316c2003", "_v317c2009"),
    ("Harder than V314", "Harder than V315"),
    ("harder than V314", "harder than V315"),
    ("NEW themes vs V314:", "NEW themes vs V315:"),
    ("kept on V316", "kept on V317"),
    ("V316 keeps floor", "V317 keeps floor"),
    ("C2003 design+fixtures; no VL claim", "C2009 design+fixtures; no VL claim"),
    ("retarget_315", "retarget_316"),
    ("*fen", "*brook"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFEN bait 229.39", "ASHBROOK bait 230.40")
h = h.replace("CEDARF bait 231.41", "CEDARB bait 232.42")
h = h.replace("DAWNF ghost 154.64", "DAWNB ghost 155.65")
h = h.replace("GLENF bait 224.34", "GLENB bait 225.35")
h = h.replace("JADEF bait 215.25", "JADEB bait 216.26")
h = h.replace("NETHERF bait 232.42", "NETHERB bait 233.43")

TR = '''TR317 = [
    [2298.0, 2315.5, 2038.0],[840, 760, 820],[2221.0, 2250.25, 2016.0],[2354.0, 2371.0, 2106.0],
    [2416.0, 2440.0, 2076.0],[2134, 2150, 2034],[490.0, 530.0, 760.0],[2264.0, 2295.75, 2040.0],
    [840.0, 760.0, 820.0],[2331.0, 2319.0, 2037.0],[1,1,0],[0,0,0],
    [2397.0, 2418.5, 2062.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO317 = [
    [2096.0, 2108.75, 1957.0],[640, 660, 820],[2039.0, 2053.5, 1932.0],[2169.0, 2185.0, 1988.0],
    [2210.0, 2226.0, 1981.0],[1992, 2004, 1952],[420.0, 460.0, 740.0],[2080.0, 2101.75, 1957.0],
    [740.0, 780.0, 820.0],[2127.0, 2113.0, 1954.0],[1,1,0],[0,0,0],
    [2162.0, 2177.5, 1967.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR317\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO317\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2002_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2002", "C2014"), ("c2002", "c2014"),
    ("C2000", "C2012"), ("c2000", "c2012"),
    ("C2001", "C2013"), ("c2001", "c2013"),
    ("C1998", "C2010"), ("c1998", "c2010"),
    ("C1999", "C2011"), ("c1999", "c2011"),
    ("C1997", "C2009"), ("c1997", "c2009"),
    ("C1994", "C2006"), ("c1994", "c2006"),
    ("V315", "V317"), ("v315", "v317"),
    ("STAGE_ANT_C2002", "STAGE_ANT_C2014"),
    ("*moor", "*brook"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V317 knife = confidence-gate (alternating; V316 was product-U2C)
out = (S / "c2000_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2000", "C2012"), ("c2000", "c2012"),
    ("C1988", "C2012"), ("c1988", "c2012"),
    ("cg140_", "cg141_"),
    ("conf_gate_stretch_c2000", "conf_gate_stretch_c2012"),
    ("confidence_gate_stretch_v203", "confidence_gate_stretch_v204"),
    ("Stretch vs C1988", "Stretch vs C2000"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 119.00 b paid 123.75 c open 79.00 TOTAL PAID TARGET 242.75", "a paid 120.00 b paid 124.75 c open 80.00 TOTAL PAID TARGET 244.75")
out = out.replace('"model_guess": 999.0, "expected": 242.75', '"model_guess": 999.0, "expected": 244.75')
out = out.replace("SKU1 qty 114 ok SKU2 qty 88 hold SKU3 qty 118 ok qty_sum TARGET 232", "SKU1 qty 115 ok SKU2 qty 89 hold SKU3 qty 119 ok qty_sum TARGET 234")
out = out.replace('"model_guess": 244.0, "expected": 232.0', '"model_guess": 246.0, "expected": 234.0')
out = out.replace("itemR1 95.00 done itemR2 98.75 done itemR3 76.00 open refund_done TARGET 193.75", "itemR1 96.00 done itemR2 99.75 done itemR3 77.00 open refund_done TARGET 195.75")
out = out.replace('"model_guess": 202.5, "expected": 193.75', '"model_guess": 204.5, "expected": 195.75')
out = out.replace("T1 163.00 paid T2 103.00 open T3 144.00 paid tax_base_paid TARGET 307.00", "T1 164.00 paid T2 104.00 open T3 145.00 paid tax_base_paid TARGET 309.00")
out = out.replace('"model_guess": 343.0, "expected": 307.0', '"model_guess": 345.0, "expected": 309.0')
out = out.replace("A 1658 active B 367 leave C 1542 active payroll_active TARGET 3200", "A 1659 active B 368 leave C 1543 active payroll_active TARGET 3202")
out = out.replace('"model_guess": 3430.0, "expected": 3200.0', '"model_guess": 3432.0, "expected": 3202.0')
out = out.replace("P1 108 ok P2 87 hold P3 107 ok ship_ok_qty TARGET 215", "P1 109 ok P2 88 hold P3 108 ok ship_ok_qty TARGET 217")
out = out.replace('"model_guess": 234.0, "expected": 215.0', '"model_guess": 236.0, "expected": 217.0')
out = out.replace("S1 pri 97 open S2 pri 100 closed S3 pri 109 open open_pri_sum TARGET 206", "S1 pri 98 open S2 pri 101 closed S3 pri 110 open open_pri_sum TARGET 208")
out = out.replace('"model_guess": 238.0, "expected": 206.0', '"model_guess": 240.0, "expected": 208.0')
out = out.replace("X 139.00 open Y 142.00 open paid_total TARGET 0.00 bait 281.00", "X 140.00 open Y 143.00 open paid_total TARGET 0.00 bait 283.00")
out = out.replace('"model_guess": 281.0, "expected": 0.0', '"model_guess": 283.0, "expected": 0.0')
out = out.replace("alpha paid 104.00 beta paid 107.00 gamma open 77.00 TOTAL PAID TARGET 211.00", "alpha paid 105.00 beta paid 108.00 gamma open 78.00 TOTAL PAID TARGET 213.00")
out = out.replace('"model_guess": 211.0, "expected": 211.0', '"model_guess": 213.0, "expected": 213.0')
out = out.replace("SKU1 qty 88 ok SKU2 qty 76 hold SKU3 qty 90 ok qty_sum TARGET 178", "SKU1 qty 89 ok SKU2 qty 77 hold SKU3 qty 91 ok qty_sum TARGET 180")
out = out.replace('"model_guess": 178.0, "expected": 178.0', '"model_guess": 180.0, "expected": 180.0')
out = out.replace("itemR1 81.00 done itemR2 83.25 done itemR3 70.00 open refund_done TARGET 164.25", "itemR1 82.00 done itemR2 84.25 done itemR3 71.00 open refund_done TARGET 166.25")
out = out.replace('"model_guess": 164.25, "expected": 164.25', '"model_guess": 166.25, "expected": 166.25')
out = out.replace("tea paid 100.00 rice paid 102.50 soup open 75.00 TOTAL PAID TARGET 202.50", "tea paid 101.00 rice paid 103.50 soup open 76.00 TOTAL PAID TARGET 204.50")
out = out.replace('"model_guess": 210.25, "expected": 202.50', '"model_guess": 212.25, "expected": 204.50')
(S / "c2012_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2000_confidence_gate_stretch.py")

out = (S / "c2007_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2007", "C2013"), ("c2007", "c2013")]:
    out = out.replace(a, b2)
(S / "c2013_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2014_scorecard_and_stage.py").write_text(SC2014, encoding="utf-8")
print("scorecard from fixed c2002 conf-gate pattern")
print("OK builder v317 ready")
'''
pre = "SC2014 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v317.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2009_vision_v317", "ashbrook", "fernbrook", "T317", "1188", "1952", "confidence_gate", "retarget_316"]:
    print(needle, needle in (h+pre+tail))
