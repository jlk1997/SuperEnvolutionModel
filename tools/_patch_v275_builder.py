from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v274.py").read_text(encoding="utf-8")
idx0 = b0.find('# V274 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
    ("T274", "T275"), ("TR274", "TR275"), ("HO274", "HO275"),
    ("NEW274", "NEW275"),
    ("V274", "V275"), ("v274", "v275"),
    ("_v274_themes.json", "_v275_themes.json"),
    ("_v273_themes.json", "_v274_themes.json"),
    ("OLD273", "OLD274"),
    ("vision_images_v274", "vision_images_v275"),
    ("VL_GATE_V274", "VL_GATE_V275"), ("vl_gate_v274", "vl_gate_v275"),
    ("C1751", "C1757"), ("c1751", "c1757"),
    ("C1752", "C1758"), ("c1752", "c1758"),
    ("C1753", "C1759"), ("c1753", "c1759"),
    ("_v274c1751", "_v275c1757"),
    ("Harder than V272", "Harder than V273"),
    ("harder than V272", "harder than V273"),
    ("NEW themes vs V272:", "NEW themes vs V273:"),
    ("kept on V274", "kept on V275"),
    ("V274 keeps floor", "V275 keeps floor"),
    ("C1751 design+fixtures; no VL claim", "C1757 design+fixtures; no VL claim"),
    ("retarget_273", "retarget_274"),
    ("*dale", "*ford"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHDALE bait 187.97", "ASHFORD bait 188.98")
h = h.replace("CEDARD bait 189.99", "CEDARF bait 190.00")
h = h.replace("DAWND ghost 112.22", "DAWNF ghost 113.23")
h = h.replace("GLEND bait 182.92", "GLENF bait 183.93")
h = h.replace("JADED bait 173.83", "JADEF bait 174.84")
h = h.replace("NETHERD bait 190.00", "NETHERF bait 191.01")

TR = '''TR275 = [
    [2200.0, 2217.5, 1940.0],[840, 760, 820],[2123.0, 2152.25, 1918.0],[2256.0, 2273.0, 2008.0],
    [2318.0, 2342.0, 1978.0],[2036, 2052, 1936],[520.0, 560.0, 760.0],[2166.0, 2197.75, 1942.0],
    [840.0, 760.0, 820.0],[2233.0, 2221.0, 1939.0],[1,1,0],[0,0,0],
    [2299.0, 2320.5, 1964.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO275 = [
    [1998.0, 2010.75, 1859.0],[640, 660, 820],[1941.0, 1955.5, 1834.0],[2071.0, 2087.0, 1890.0],
    [2112.0, 2128.0, 1883.0],[1894, 1906, 1854],[400.0, 440.0, 740.0],[1982.0, 2003.75, 1859.0],
    [740.0, 780.0, 820.0],[2029.0, 2015.0, 1856.0],[1,1,0],[0,0,0],
    [2064.0, 2079.5, 1869.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR275\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO275\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1748_confidence_gate_stretch.py"
sc_src = "c1750_scorecard_and_stage.py"

tail = f'''# V275 knife = confidence-gate (alternating; V274 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1748", "C1760"), ("c1748", "c1760"),
    ("C1736", "C1760"), ("c1736", "c1760"),
    ("cg119_", "cg120_"),
    ("conf_gate_stretch_c1748", "conf_gate_stretch_c1760"),
    ("confidence_gate_stretch_v182", "confidence_gate_stretch_v183"),
    ("Stretch vs C1736", "Stretch vs C1748"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 98.00 b paid 102.75 c open 58.00 TOTAL PAID TARGET 200.75", "a paid 99.00 b paid 103.75 c open 59.00 TOTAL PAID TARGET 202.75")
out = out.replace('"model_guess": 999.0, "expected": 200.75', '"model_guess": 999.0, "expected": 202.75')
out = out.replace("SKU1 qty 93 ok SKU2 qty 67 hold SKU3 qty 97 ok qty_sum TARGET 190", "SKU1 qty 94 ok SKU2 qty 68 hold SKU3 qty 98 ok qty_sum TARGET 192")
out = out.replace('"model_guess": 202.0, "expected": 190.0', '"model_guess": 204.0, "expected": 192.0')
out = out.replace("itemR1 74.00 done itemR2 77.75 done itemR3 55.00 open refund_done TARGET 151.75", "itemR1 75.00 done itemR2 78.75 done itemR3 56.00 open refund_done TARGET 153.75")
out = out.replace('"model_guess": 160.5, "expected": 151.75', '"model_guess": 162.5, "expected": 153.75')
out = out.replace("T1 142.00 paid T2 82.00 open T3 123.00 paid tax_base_paid TARGET 265.00", "T1 143.00 paid T2 83.00 open T3 124.00 paid tax_base_paid TARGET 267.00")
out = out.replace('"model_guess": 301.0, "expected": 265.0', '"model_guess": 303.0, "expected": 267.0')
out = out.replace("A 1617 active B 346 leave C 1521 active payroll_active TARGET 3138", "A 1619 active B 347 leave C 1522 active payroll_active TARGET 3141")
out = out.replace('"model_guess": 3368.0, "expected": 3138.0', '"model_guess": 3371.0, "expected": 3141.0')
out = out.replace("P1 87 ok P2 66 hold P3 86 ok ship_ok_qty TARGET 173", "P1 88 ok P2 67 hold P3 87 ok ship_ok_qty TARGET 175")
out = out.replace('"model_guess": 192.0, "expected": 173.0', '"model_guess": 194.0, "expected": 175.0')
out = out.replace("S1 pri 76 open S2 pri 79 closed S3 pri 88 open open_pri_sum TARGET 164", "S1 pri 77 open S2 pri 80 closed S3 pri 89 open open_pri_sum TARGET 166")
out = out.replace('"model_guess": 196.0, "expected": 164.0', '"model_guess": 198.0, "expected": 166.0')
out = out.replace("X 118.00 open Y 121.00 open paid_total TARGET 0.00 bait 239.00", "X 119.00 open Y 122.00 open paid_total TARGET 0.00 bait 241.00")
out = out.replace('"model_guess": 239.0, "expected": 0.0', '"model_guess": 241.0, "expected": 0.0')
out = out.replace("alpha paid 83.00 beta paid 86.00 gamma open 56.00 TOTAL PAID TARGET 169.00", "alpha paid 84.00 beta paid 87.00 gamma open 57.00 TOTAL PAID TARGET 171.00")
out = out.replace('"model_guess": 169.0, "expected": 169.0', '"model_guess": 171.0, "expected": 171.0')
out = out.replace("SKU1 qty 67 ok SKU2 qty 55 hold SKU3 qty 69 ok qty_sum TARGET 136", "SKU1 qty 68 ok SKU2 qty 56 hold SKU3 qty 70 ok qty_sum TARGET 138")
out = out.replace('"model_guess": 136.0, "expected": 136.0', '"model_guess": 138.0, "expected": 138.0')
out = out.replace("itemR1 60.00 done itemR2 62.25 done itemR3 49.00 open refund_done TARGET 122.25", "itemR1 61.00 done itemR2 63.25 done itemR3 50.00 open refund_done TARGET 124.25")
out = out.replace('"model_guess": 122.25, "expected": 122.25', '"model_guess": 124.25, "expected": 124.25')
out = out.replace("tea paid 79.00 rice paid 81.50 soup open 54.00 TOTAL PAID TARGET 160.50", "tea paid 80.00 rice paid 82.50 soup open 55.00 TOTAL PAID TARGET 162.50")
out = out.replace('"model_guess": 168.25, "expected": 160.50', '"model_guess": 170.25, "expected": 162.50')
(S / "c1760_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1755_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1755", "C1761"), ("c1755", "c1761")]:
    out = out.replace(a, b2)
(S / "c1761_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1750", "C1762"), ("c1750", "c1762"),
    ("C1748", "C1760"), ("c1748", "c1760"),
    ("C1749", "C1761"), ("c1749", "c1761"),
    ("C1746", "C1758"), ("c1746", "c1758"),
    ("C1747", "C1759"), ("c1747", "c1759"),
    ("V273", "V275"), ("v273", "v275"),
    ("STAGE_ANT_C1750", "STAGE_ANT_C1762"),
    ("*brook", "*ford"),
]:
    out = out.replace(a, b2)
(S / "c1762_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v275 ready")
'''
(ROOT / "tools/_build_v275.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1757_vision_v275", "ashford", "fernford", "T275", "1188", "1854", "confidence_gate", "retarget_274"]:
    print(needle, needle in (h+tail))
