from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v258.py").read_text(encoding="utf-8")
idx0 = b0.find('# V258 knife = product-U2C')
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
    ("T258", "T259"), ("TR258", "TR259"), ("HO258", "HO259"),
    ("NEW258", "NEW259"),
    ("V258", "V259"), ("v258", "v259"),
    ("_v258_themes.json", "_v259_themes.json"),
    ("_v257_themes.json", "_v258_themes.json"),
    ("OLD257", "OLD258"),
    ("vision_images_v258", "vision_images_v259"),
    ("VL_GATE_V258", "VL_GATE_V259"), ("vl_gate_v258", "vl_gate_v259"),
    ("C1655", "C1661"), ("c1655", "c1661"),
    ("C1656", "C1662"), ("c1656", "c1662"),
    ("C1657", "C1663"), ("c1657", "c1663"),
    ("_v258c1655", "_v259c1661"),
    ("Harder than V256", "Harder than V257"),
    ("harder than V256", "harder than V257"),
    ("NEW themes vs V256:", "NEW themes vs V257:"),
    ("kept on V258", "kept on V259"),
    ("V258 keeps floor", "V259 keeps floor"),
    ("C1655 design+fixtures; no VL claim", "C1661 design+fixtures; no VL claim"),
    ("retarget_257", "retarget_258"),
    ("*holm", "*wick"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHWICK bait 171.81", "ASHWICK bait 172.82")
h = h.replace("CEDARH bait 173.83", "CEDARW bait 174.84")
h = h.replace("DAWNH ghost 96.96", "DAWNW ghost 97.97")
h = h.replace("GLENH bait 166.76", "GLENW bait 167.77")
h = h.replace("JADEH bait 157.67", "JADEW bait 158.68")
h = h.replace("NETHERH bait 174.84", "NETHERW bait 175.85")

TR = '''TR259 = [
    [2164.0, 2181.5, 1904.0],[840, 760, 820],[2087.0, 2116.25, 1882.0],[2220.0, 2237.0, 1972.0],
    [2282.0, 2306.0, 1942.0],[2000, 2016, 1900],[480.0, 520.0, 740.0],[2130.0, 2161.75, 1906.0],
    [840.0, 760.0, 820.0],[2197.0, 2185.0, 1903.0],[1,1,0],[0,0,0],
    [2263.0, 2284.5, 1928.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO259 = [
    [1962.0, 1974.75, 1823.0],[740, 780, 820],[1905.0, 1919.5, 1798.0],[2035.0, 2051.0, 1854.0],
    [2076.0, 2092.0, 1847.0],[1858, 1870, 1816],[360.0, 400.0, 730.0],[1946.0, 1967.75, 1823.0],
    [780.0, 740.0, 820.0],[1993.0, 1979.0, 1818.0],[1,1,0],[0,0,0],
    [2028.0, 2043.5, 1833.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR259\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO259\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1652_confidence_gate_stretch.py"
if not (ROOT / "scripts" / cg_src).exists():
    cg_src = "c1640_confidence_gate_stretch.py"
sc_src = "c1654_scorecard_and_stage.py"

tail = f'''# V259 knife = confidence-gate (alternating; V258 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1652", "C1664"), ("c1652", "c1664"),
    ("C1640", "C1664"), ("c1640", "c1664"),
    ("cg111_", "cg112_"),
    ("conf_gate_stretch_c1652", "conf_gate_stretch_c1664"),
    ("confidence_gate_stretch_v174", "confidence_gate_stretch_v175"),
    ("Stretch vs C1640", "Stretch vs C1652"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 90.00 b paid 94.75 c open 50.00 TOTAL PAID TARGET 184.75", "a paid 91.00 b paid 95.75 c open 51.00 TOTAL PAID TARGET 186.75")
out = out.replace('"model_guess": 999.0, "expected": 184.75', '"model_guess": 999.0, "expected": 186.75')
out = out.replace("SKU1 qty 85 ok SKU2 qty 59 hold SKU3 qty 89 ok qty_sum TARGET 174", "SKU1 qty 86 ok SKU2 qty 60 hold SKU3 qty 90 ok qty_sum TARGET 176")
out = out.replace('"model_guess": 186.0, "expected": 174.0', '"model_guess": 188.0, "expected": 176.0')
out = out.replace("itemR1 66.00 done itemR2 69.75 done itemR3 47.00 open refund_done TARGET 135.75", "itemR1 67.00 done itemR2 70.75 done itemR3 48.00 open refund_done TARGET 137.75")
out = out.replace('"model_guess": 144.5, "expected": 135.75', '"model_guess": 146.5, "expected": 137.75')
out = out.replace("T1 134.00 paid T2 74.00 open T3 115.00 paid tax_base_paid TARGET 249.00", "T1 135.00 paid T2 75.00 open T3 116.00 paid tax_base_paid TARGET 251.00")
out = out.replace('"model_guess": 285.0, "expected": 249.0', '"model_guess": 287.0, "expected": 251.0')
out = out.replace("A 1601 active B 338 leave C 1513 active payroll_active TARGET 3114", "A 1603 active B 339 leave C 1514 active payroll_active TARGET 3117")
out = out.replace('"model_guess": 3344.0, "expected": 3114.0', '"model_guess": 3347.0, "expected": 3117.0')
out = out.replace("P1 79 ok P2 58 hold P3 78 ok ship_ok_qty TARGET 157", "P1 80 ok P2 59 hold P3 79 ok ship_ok_qty TARGET 159")
out = out.replace('"model_guess": 176.0, "expected": 157.0', '"model_guess": 178.0, "expected": 159.0')
out = out.replace("S1 pri 68 open S2 pri 71 closed S3 pri 80 open open_pri_sum TARGET 148", "S1 pri 69 open S2 pri 72 closed S3 pri 81 open open_pri_sum TARGET 150")
out = out.replace('"model_guess": 180.0, "expected": 148.0', '"model_guess": 182.0, "expected": 150.0')
out = out.replace("X 110.00 open Y 113.00 open paid_total TARGET 0.00 bait 223.00", "X 111.00 open Y 114.00 open paid_total TARGET 0.00 bait 225.00")
out = out.replace('"model_guess": 223.0, "expected": 0.0', '"model_guess": 225.0, "expected": 0.0')
out = out.replace("alpha paid 75.00 beta paid 78.00 gamma open 48.00 TOTAL PAID TARGET 153.00", "alpha paid 76.00 beta paid 79.00 gamma open 49.00 TOTAL PAID TARGET 155.00")
out = out.replace('"model_guess": 153.0, "expected": 153.0', '"model_guess": 155.0, "expected": 155.0')
out = out.replace("SKU1 qty 59 ok SKU2 qty 47 hold SKU3 qty 61 ok qty_sum TARGET 120", "SKU1 qty 60 ok SKU2 qty 48 hold SKU3 qty 62 ok qty_sum TARGET 122")
out = out.replace('"model_guess": 120.0, "expected": 120.0', '"model_guess": 122.0, "expected": 122.0')
out = out.replace("itemR1 52.00 done itemR2 54.25 done itemR3 41.00 open refund_done TARGET 106.25", "itemR1 53.00 done itemR2 55.25 done itemR3 42.00 open refund_done TARGET 108.25")
out = out.replace('"model_guess": 106.25, "expected": 106.25', '"model_guess": 108.25, "expected": 108.25')
out = out.replace("tea paid 71.00 rice paid 73.50 soup open 46.00 TOTAL PAID TARGET 144.50", "tea paid 72.00 rice paid 74.50 soup open 47.00 TOTAL PAID TARGET 146.50")
out = out.replace('"model_guess": 152.25, "expected": 144.50', '"model_guess": 154.25, "expected": 146.50')
(S / "c1664_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1659_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1659", "C1665"), ("c1659", "c1665")]:
    out = out.replace(a, b2)
(S / "c1665_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1654", "C1666"), ("c1654", "c1666"),
    ("C1652", "C1664"), ("c1652", "c1664"),
    ("C1653", "C1665"), ("c1653", "c1665"),
    ("C1650", "C1662"), ("c1650", "c1662"),
    ("C1651", "C1663"), ("c1651", "c1663"),
    ("V257", "V259"), ("v257", "v259"),
    ("STAGE_ANT_C1654", "STAGE_ANT_C1666"),
    ("*croft", "*wick"),
]:
    out = out.replace(a, b2)
(S / "c1666_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v259 ready")
'''
(ROOT / "tools/_build_v259.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1661_vision_v259", "ashwick", "fernwick", "T259", "1188", "1854", "confidence_gate"]:
    print(needle, needle in (h+tail))
