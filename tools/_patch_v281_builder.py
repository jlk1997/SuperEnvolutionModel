from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v280.py").read_text(encoding="utf-8")
idx0 = b0.find('# V280 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("netherholm", "netherwick"), ("NETHERHOLM", "NETHERWICK"),
    ("cedarholm", "cedarwick"), ("CEDARHOLM", "CEDARWICK"),
    ("dawnholm", "dawnwick"), ("DAWNHOLM", "DAWNWICK"),
    ("fernholm", "fernwick"), ("FERNHOLM", "FERNWICK"),
    ("glenholm", "glenwick"), ("GLENHOLM", "GLENWICK"),
    ("hazeholm", "hazewick"), ("HAZEHOLM", "HAZEWICK"),
    ("jadeholm", "jadewick"), ("JADEHOLM", "JADEWICK"),
    ("knotholm", "knotwick"), ("KNOTHOLM", "KNOTWICK"),
    ("lakeholm", "lakewick"), ("LAKEHOLM", "LAKEWICK"),
    ("mossholm", "mosswick"), ("MOSSHOLM", "MOSSWICK"),
    ("pineholm", "pinewick"), ("PINEHOLM", "PINEWICK"),
    ("quillholm", "quillwick"), ("QUILLHOLM", "QUILLWICK"),
    ("reedholm", "reedwick"), ("REEDHOLM", "REEDWICK"),
    ("stoneholm", "stonewick"), ("STONEHOLM", "STONEWICK"),
    ("ashholm", "ashwick"), ("ASHHOLM", "ASHWICK"),
    ("elmholm", "elmwick"), ("ELMHOLM", "ELMWICK"),
    ("inkholm", "inkwick"), ("INKHOLM", "INKWICK"),
    ("oakholm", "oakwick"), ("OAKHOLM", "OAKWICK"),
]
pairs = [
    ("*holm ; stack mid-band", "*wick ; stack mid-band"),
    ("T280", "T281"), ("TR280", "TR281"), ("HO280", "HO281"),
    ("NEW280", "NEW281"),
    ("V280", "V281"), ("v280", "v281"),
    ("_v280_themes.json", "_v281_themes.json"),
    ("_v279_themes.json", "_v280_themes.json"),
    ("OLD279", "OLD280"),
    ("vision_images_v280", "vision_images_v281"),
    ("VL_GATE_V280", "VL_GATE_V281"), ("vl_gate_v280", "vl_gate_v281"),
    ("C1787", "C1793"), ("c1787", "c1793"),
    ("C1788", "C1794"), ("c1788", "c1794"),
    ("C1789", "C1795"), ("c1789", "c1795"),
    ("_v280c1787", "_v281c1793"),
    ("Harder than V278", "Harder than V279"),
    ("harder than V278", "harder than V279"),
    ("NEW themes vs V278:", "NEW themes vs V279:"),
    ("kept on V280", "kept on V281"),
    ("V280 keeps floor", "V281 keeps floor"),
    ("C1787 design+fixtures; no VL claim", "C1793 design+fixtures; no VL claim"),
    ("retarget_279", "retarget_280"),
    ("*holm", "*wick"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHOLM bait 193.03", "ASHWICK bait 194.04")
h = h.replace("CEDARH bait 195.05", "CEDARW bait 196.06")
h = h.replace("DAWNH ghost 118.28", "DAWNW ghost 119.29")
h = h.replace("GLENH bait 188.98", "GLENW bait 189.99")
h = h.replace("JADEH bait 179.89", "JADEW bait 180.90")
h = h.replace("NETHERH bait 196.06", "NETHERW bait 197.07")

TR = '''TR281 = [
    [2218.0, 2235.5, 1958.0],[840, 760, 820],[2141.0, 2170.25, 1936.0],[2274.0, 2291.0, 2026.0],
    [2336.0, 2360.0, 1996.0],[2054, 2070, 1954],[490.0, 530.0, 760.0],[2184.0, 2215.75, 1960.0],
    [840.0, 760.0, 820.0],[2251.0, 2239.0, 1957.0],[1,1,0],[0,0,0],
    [2317.0, 2338.5, 1982.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO281 = [
    [2016.0, 2028.75, 1877.0],[640, 660, 820],[1959.0, 1973.5, 1852.0],[2089.0, 2105.0, 1908.0],
    [2130.0, 2146.0, 1901.0],[1912, 1924, 1872],[420.0, 460.0, 740.0],[2000.0, 2021.75, 1877.0],
    [740.0, 780.0, 820.0],[2047.0, 2033.0, 1874.0],[1,1,0],[0,0,0],
    [2082.0, 2097.5, 1887.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR281\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO281\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1784_confidence_gate_stretch.py"
sc_src = "c1786_scorecard_and_stage.py"

tail = f'''# V281 knife = confidence-gate (alternating; V280 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1784", "C1796"), ("c1784", "c1796"),
    ("C1772", "C1796"), ("c1772", "c1796"),
    ("cg122_", "cg123_"),
    ("conf_gate_stretch_c1784", "conf_gate_stretch_c1796"),
    ("confidence_gate_stretch_v185", "confidence_gate_stretch_v186"),
    ("Stretch vs C1772", "Stretch vs C1784"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 101.00 b paid 105.75 c open 61.00 TOTAL PAID TARGET 206.75", "a paid 102.00 b paid 106.75 c open 62.00 TOTAL PAID TARGET 208.75")
out = out.replace('"model_guess": 999.0, "expected": 206.75', '"model_guess": 999.0, "expected": 208.75')
out = out.replace("SKU1 qty 96 ok SKU2 qty 70 hold SKU3 qty 100 ok qty_sum TARGET 196", "SKU1 qty 97 ok SKU2 qty 71 hold SKU3 qty 101 ok qty_sum TARGET 198")
out = out.replace('"model_guess": 208.0, "expected": 196.0', '"model_guess": 210.0, "expected": 198.0')
out = out.replace("itemR1 77.00 done itemR2 80.75 done itemR3 58.00 open refund_done TARGET 157.75", "itemR1 78.00 done itemR2 81.75 done itemR3 59.00 open refund_done TARGET 159.75")
out = out.replace('"model_guess": 166.5, "expected": 157.75', '"model_guess": 168.5, "expected": 159.75')
out = out.replace("T1 145.00 paid T2 85.00 open T3 126.00 paid tax_base_paid TARGET 271.00", "T1 146.00 paid T2 86.00 open T3 127.00 paid tax_base_paid TARGET 273.00")
out = out.replace('"model_guess": 307.0, "expected": 271.0', '"model_guess": 309.0, "expected": 273.0')
out = out.replace("A 1623 active B 349 leave C 1524 active payroll_active TARGET 3147", "A 1625 active B 350 leave C 1525 active payroll_active TARGET 3150")
out = out.replace('"model_guess": 3377.0, "expected": 3147.0', '"model_guess": 3380.0, "expected": 3150.0')
out = out.replace("P1 90 ok P2 69 hold P3 89 ok ship_ok_qty TARGET 179", "P1 91 ok P2 70 hold P3 90 ok ship_ok_qty TARGET 181")
out = out.replace('"model_guess": 198.0, "expected": 179.0', '"model_guess": 200.0, "expected": 181.0')
out = out.replace("S1 pri 79 open S2 pri 82 closed S3 pri 91 open open_pri_sum TARGET 170", "S1 pri 80 open S2 pri 83 closed S3 pri 92 open open_pri_sum TARGET 172")
out = out.replace('"model_guess": 202.0, "expected": 170.0', '"model_guess": 204.0, "expected": 172.0')
out = out.replace("X 121.00 open Y 124.00 open paid_total TARGET 0.00 bait 245.00", "X 122.00 open Y 125.00 open paid_total TARGET 0.00 bait 247.00")
out = out.replace('"model_guess": 245.0, "expected": 0.0', '"model_guess": 247.0, "expected": 0.0')
out = out.replace("alpha paid 86.00 beta paid 89.00 gamma open 59.00 TOTAL PAID TARGET 175.00", "alpha paid 87.00 beta paid 90.00 gamma open 60.00 TOTAL PAID TARGET 177.00")
out = out.replace('"model_guess": 175.0, "expected": 175.0', '"model_guess": 177.0, "expected": 177.0')
out = out.replace("SKU1 qty 70 ok SKU2 qty 58 hold SKU3 qty 72 ok qty_sum TARGET 142", "SKU1 qty 71 ok SKU2 qty 59 hold SKU3 qty 73 ok qty_sum TARGET 144")
out = out.replace('"model_guess": 142.0, "expected": 142.0', '"model_guess": 144.0, "expected": 144.0')
out = out.replace("itemR1 63.00 done itemR2 65.25 done itemR3 52.00 open refund_done TARGET 128.25", "itemR1 64.00 done itemR2 66.25 done itemR3 53.00 open refund_done TARGET 130.25")
out = out.replace('"model_guess": 128.25, "expected": 128.25', '"model_guess": 130.25, "expected": 130.25')
out = out.replace("tea paid 82.00 rice paid 84.50 soup open 57.00 TOTAL PAID TARGET 166.50", "tea paid 83.00 rice paid 85.50 soup open 58.00 TOTAL PAID TARGET 168.50")
out = out.replace('"model_guess": 174.25, "expected": 166.50', '"model_guess": 176.25, "expected": 168.50')
(S / "c1796_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1791_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1791", "C1797"), ("c1791", "c1797")]:
    out = out.replace(a, b2)
(S / "c1797_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1786", "C1798"), ("c1786", "c1798"),
    ("C1784", "C1796"), ("c1784", "c1796"),
    ("C1785", "C1797"), ("c1785", "c1797"),
    ("C1782", "C1794"), ("c1782", "c1794"),
    ("C1783", "C1795"), ("c1783", "c1795"),
    ("V279", "V281"), ("v279", "v281"),
    ("STAGE_ANT_C1786", "STAGE_ANT_C1798"),
    ("*croft", "*wick"),
]:
    out = out.replace(a, b2)
(S / "c1798_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v281 ready")
'''
(ROOT / "tools/_build_v281.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1793_vision_v281", "ashwick", "fernwick", "T281", "1188", "1872", "confidence_gate", "retarget_280"]:
    print(needle, needle in (h+tail))
