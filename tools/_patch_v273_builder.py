from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v272.py").read_text(encoding="utf-8")
idx0 = b0.find('# V272 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
    ("T272", "T273"), ("TR272", "TR273"), ("HO272", "HO273"),
    ("NEW272", "NEW273"),
    ("V272", "V273"), ("v272", "v273"),
    ("_v272_themes.json", "_v273_themes.json"),
    ("_v271_themes.json", "_v272_themes.json"),
    ("OLD271", "OLD272"),
    ("vision_images_v272", "vision_images_v273"),
    ("VL_GATE_V272", "VL_GATE_V273"), ("vl_gate_v272", "vl_gate_v273"),
    ("C1739", "C1745"), ("c1739", "c1745"),
    ("C1740", "C1746"), ("c1740", "c1746"),
    ("C1741", "C1747"), ("c1741", "c1747"),
    ("_v272c1739", "_v273c1745"),
    ("Harder than V270", "Harder than V271"),
    ("harder than V270", "harder than V271"),
    ("NEW themes vs V270:", "NEW themes vs V271:"),
    ("kept on V272", "kept on V273"),
    ("V272 keeps floor", "V273 keeps floor"),
    ("C1739 design+fixtures; no VL claim", "C1745 design+fixtures; no VL claim"),
    ("retarget_271", "retarget_272"),
    ("*fen", "*brook"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFEN bait 185.95", "ASHBROOK bait 186.96")
h = h.replace("CEDARF bait 187.97", "CEDARB bait 188.98")
h = h.replace("DAWNF ghost 110.20", "DAWNB ghost 111.21")
h = h.replace("GLENF bait 180.90", "GLENB bait 181.91")
h = h.replace("JADEF bait 171.81", "JADEB bait 172.82")
h = h.replace("NETHERF bait 188.98", "NETHERB bait 189.99")

# prefer 840+760 qty (V272 lesson); stack plateau 1188
TR = '''TR273 = [
    [2194.0, 2211.5, 1934.0],[840, 760, 820],[2117.0, 2146.25, 1912.0],[2250.0, 2267.0, 2002.0],
    [2312.0, 2336.0, 1972.0],[2030, 2046, 1930],[500.0, 540.0, 760.0],[2160.0, 2191.75, 1936.0],
    [840.0, 760.0, 820.0],[2227.0, 2215.0, 1933.0],[1,1,0],[0,0,0],
    [2293.0, 2314.5, 1958.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO273 = [
    [1992.0, 2004.75, 1853.0],[640, 660, 820],[1935.0, 1949.5, 1828.0],[2065.0, 2081.0, 1884.0],
    [2106.0, 2122.0, 1877.0],[1888, 1900, 1848],[380.0, 420.0, 740.0],[1976.0, 1997.75, 1853.0],
    [740.0, 780.0, 820.0],[2023.0, 2009.0, 1850.0],[1,1,0],[0,0,0],
    [2058.0, 2073.5, 1863.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR273\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO273\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1736_confidence_gate_stretch.py"
sc_src = "c1738_scorecard_and_stage.py"

tail = f'''# V273 knife = confidence-gate (alternating; V272 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1736", "C1748"), ("c1736", "c1748"),
    ("C1724", "C1748"), ("c1724", "c1748"),
    ("cg118_", "cg119_"),
    ("conf_gate_stretch_c1736", "conf_gate_stretch_c1748"),
    ("confidence_gate_stretch_v181", "confidence_gate_stretch_v182"),
    ("Stretch vs C1724", "Stretch vs C1736"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 97.00 b paid 101.75 c open 57.00 TOTAL PAID TARGET 198.75", "a paid 98.00 b paid 102.75 c open 58.00 TOTAL PAID TARGET 200.75")
out = out.replace('"model_guess": 999.0, "expected": 198.75', '"model_guess": 999.0, "expected": 200.75')
out = out.replace("SKU1 qty 92 ok SKU2 qty 66 hold SKU3 qty 96 ok qty_sum TARGET 188", "SKU1 qty 93 ok SKU2 qty 67 hold SKU3 qty 97 ok qty_sum TARGET 190")
out = out.replace('"model_guess": 200.0, "expected": 188.0', '"model_guess": 202.0, "expected": 190.0')
out = out.replace("itemR1 73.00 done itemR2 76.75 done itemR3 54.00 open refund_done TARGET 149.75", "itemR1 74.00 done itemR2 77.75 done itemR3 55.00 open refund_done TARGET 151.75")
out = out.replace('"model_guess": 158.5, "expected": 149.75', '"model_guess": 160.5, "expected": 151.75')
out = out.replace("T1 141.00 paid T2 81.00 open T3 122.00 paid tax_base_paid TARGET 263.00", "T1 142.00 paid T2 82.00 open T3 123.00 paid tax_base_paid TARGET 265.00")
out = out.replace('"model_guess": 299.0, "expected": 263.0', '"model_guess": 301.0, "expected": 265.0')
out = out.replace("A 1615 active B 345 leave C 1520 active payroll_active TARGET 3135", "A 1617 active B 346 leave C 1521 active payroll_active TARGET 3138")
out = out.replace('"model_guess": 3365.0, "expected": 3135.0', '"model_guess": 3368.0, "expected": 3138.0')
out = out.replace("P1 86 ok P2 65 hold P3 85 ok ship_ok_qty TARGET 171", "P1 87 ok P2 66 hold P3 86 ok ship_ok_qty TARGET 173")
out = out.replace('"model_guess": 190.0, "expected": 171.0', '"model_guess": 192.0, "expected": 173.0')
out = out.replace("S1 pri 75 open S2 pri 78 closed S3 pri 87 open open_pri_sum TARGET 162", "S1 pri 76 open S2 pri 79 closed S3 pri 88 open open_pri_sum TARGET 164")
out = out.replace('"model_guess": 194.0, "expected": 162.0', '"model_guess": 196.0, "expected": 164.0')
out = out.replace("X 117.00 open Y 120.00 open paid_total TARGET 0.00 bait 237.00", "X 118.00 open Y 121.00 open paid_total TARGET 0.00 bait 239.00")
out = out.replace('"model_guess": 237.0, "expected": 0.0', '"model_guess": 239.0, "expected": 0.0')
out = out.replace("alpha paid 82.00 beta paid 85.00 gamma open 55.00 TOTAL PAID TARGET 167.00", "alpha paid 83.00 beta paid 86.00 gamma open 56.00 TOTAL PAID TARGET 169.00")
out = out.replace('"model_guess": 167.0, "expected": 167.0', '"model_guess": 169.0, "expected": 169.0')
out = out.replace("SKU1 qty 66 ok SKU2 qty 54 hold SKU3 qty 68 ok qty_sum TARGET 134", "SKU1 qty 67 ok SKU2 qty 55 hold SKU3 qty 69 ok qty_sum TARGET 136")
out = out.replace('"model_guess": 134.0, "expected": 134.0', '"model_guess": 136.0, "expected": 136.0')
out = out.replace("itemR1 59.00 done itemR2 61.25 done itemR3 48.00 open refund_done TARGET 120.25", "itemR1 60.00 done itemR2 62.25 done itemR3 49.00 open refund_done TARGET 122.25")
out = out.replace('"model_guess": 120.25, "expected": 120.25', '"model_guess": 122.25, "expected": 122.25')
out = out.replace("tea paid 78.00 rice paid 80.50 soup open 53.00 TOTAL PAID TARGET 158.50", "tea paid 79.00 rice paid 81.50 soup open 54.00 TOTAL PAID TARGET 160.50")
out = out.replace('"model_guess": 166.25, "expected": 158.50', '"model_guess": 168.25, "expected": 160.50')
(S / "c1748_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1743_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1743", "C1749"), ("c1743", "c1749")]:
    out = out.replace(a, b2)
(S / "c1749_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1738", "C1750"), ("c1738", "c1750"),
    ("C1736", "C1748"), ("c1736", "c1748"),
    ("C1737", "C1749"), ("c1737", "c1749"),
    ("C1734", "C1746"), ("c1734", "c1746"),
    ("C1735", "C1747"), ("c1735", "c1747"),
    ("V271", "V273"), ("v271", "v273"),
    ("STAGE_ANT_C1738", "STAGE_ANT_C1750"),
    ("*moor", "*brook"),
]:
    out = out.replace(a, b2)
(S / "c1750_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v273 ready")
'''
(ROOT / "tools/_build_v273.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1745_vision_v273", "ashbrook", "fernbrook", "T273", "1188", "1848", "confidence_gate", "retarget_272"]:
    print(needle, needle in (h+tail))
