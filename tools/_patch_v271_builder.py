from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v270.py").read_text(encoding="utf-8")
idx0 = b0.find('# V270 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("netherwick", "nethermoor"), ("NETHERWICK", "NETHERMOOR"),
    ("cedarwick", "cedarmoor"), ("CEDARWICK", "CEDARMOOR"),
    ("dawnwick", "dawnmoor"), ("DAWNWICK", "DAWNMOOR"),
    ("fernwick", "fernmoor"), ("FERNWICK", "FERNMOOR"),
    ("glenwick", "glenmoor"), ("GLENWICK", "GLENMOOR"),
    ("hazewick", "hazemoor"), ("HAZEWICK", "HAZEMOOR"),
    ("jadewick", "jademoor"), ("JADEWICK", "JADEMOOR"),
    ("knotwick", "knotmoor"), ("KNOTWICK", "KNOTMOOR"),
    ("lakewick", "lakemoor"), ("LAKEWICK", "LAKEMOOR"),
    ("mosswick", "mossmoor"), ("MOSSWICK", "MOSSMOOR"),
    ("pinewick", "pinemoor"), ("PINEWICK", "PINEMOOR"),
    ("quillwick", "quillmoor"), ("QUILLWICK", "QUILLMOOR"),
    ("reedwick", "reedmoor"), ("REEDWICK", "REEDMOOR"),
    ("stonewick", "stonemoor"), ("STONEWICK", "STONEMOOR"),
    ("ashwick", "ashmoor"), ("ASHWICK", "ASHMOOR"),
    ("elmwick", "elmmoor"), ("ELMWICK", "ELMMOOR"),
    ("inkwick", "inkmoor"), ("INKWICK", "INKMOOR"),
    ("oakwick", "oakmoor"), ("OAKWICK", "OAKMOOR"),
]
pairs = [
    ("*wick ; stack mid-band", "*moor ; stack mid-band"),
    ("T270", "T271"), ("TR270", "TR271"), ("HO270", "HO271"),
    ("NEW270", "NEW271"),
    ("V270", "V271"), ("v270", "v271"),
    ("_v270_themes.json", "_v271_themes.json"),
    ("_v269_themes.json", "_v270_themes.json"),
    ("OLD269", "OLD270"),
    ("vision_images_v270", "vision_images_v271"),
    ("VL_GATE_V270", "VL_GATE_V271"), ("vl_gate_v270", "vl_gate_v271"),
    ("C1727", "C1733"), ("c1727", "c1733"),
    ("C1728", "C1734"), ("c1728", "c1734"),
    ("C1729", "C1735"), ("c1729", "c1735"),
    ("_v270c1727", "_v271c1733"),
    ("Harder than V268", "Harder than V269"),
    ("harder than V268", "harder than V269"),
    ("NEW themes vs V268:", "NEW themes vs V269:"),
    ("kept on V270", "kept on V271"),
    ("V270 keeps floor", "V271 keeps floor"),
    ("C1727 design+fixtures; no VL claim", "C1733 design+fixtures; no VL claim"),
    ("retarget_269", "retarget_270"),
    ("*wick", "*moor"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMOOR bait 183.93", "ASHMOOR bait 184.94")
h = h.replace("CEDARW bait 185.95", "CEDARM bait 186.96")
h = h.replace("DAWNW ghost 108.18", "DAWNM ghost 109.19")
h = h.replace("GLENW bait 178.88", "GLENM bait 179.89")
h = h.replace("JADEW bait 169.79", "JADEM bait 170.80")
h = h.replace("NETHERW bait 186.96", "NETHERM bait 187.97")

TR = '''TR271 = [
    [2188.0, 2205.5, 1928.0],[840, 760, 820],[2111.0, 2140.25, 1906.0],[2244.0, 2261.0, 1996.0],
    [2306.0, 2330.0, 1966.0],[2024, 2040, 1924],[480.0, 520.0, 740.0],[2154.0, 2185.75, 1930.0],
    [840.0, 760.0, 820.0],[2221.0, 2209.0, 1927.0],[1,1,0],[0,0,0],
    [2287.0, 2308.5, 1952.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO271 = [
    [1986.0, 1998.75, 1847.0],[740, 780, 820],[1929.0, 1943.5, 1822.0],[2059.0, 2075.0, 1878.0],
    [2100.0, 2116.0, 1871.0],[1882, 1894, 1842],[360.0, 400.0, 730.0],[1970.0, 1991.75, 1847.0],
    [780.0, 740.0, 820.0],[2017.0, 2003.0, 1844.0],[1,1,0],[0,0,0],
    [2052.0, 2067.5, 1857.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR271\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO271\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1724_confidence_gate_stretch.py"
if not (ROOT / "scripts" / cg_src).exists():
    cg_src = "c1712_confidence_gate_stretch.py"
sc_src = "c1726_scorecard_and_stage.py"

tail = f'''# V271 knife = confidence-gate (alternating; V270 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1724", "C1736"), ("c1724", "c1736"),
    ("C1712", "C1736"), ("c1712", "c1736"),
    ("cg117_", "cg118_"),
    ("conf_gate_stretch_c1724", "conf_gate_stretch_c1736"),
    ("confidence_gate_stretch_v180", "confidence_gate_stretch_v181"),
    ("Stretch vs C1712", "Stretch vs C1724"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 96.00 b paid 100.75 c open 56.00 TOTAL PAID TARGET 196.75", "a paid 97.00 b paid 101.75 c open 57.00 TOTAL PAID TARGET 198.75")
out = out.replace('"model_guess": 999.0, "expected": 196.75', '"model_guess": 999.0, "expected": 198.75')
out = out.replace("SKU1 qty 91 ok SKU2 qty 65 hold SKU3 qty 95 ok qty_sum TARGET 186", "SKU1 qty 92 ok SKU2 qty 66 hold SKU3 qty 96 ok qty_sum TARGET 188")
out = out.replace('"model_guess": 198.0, "expected": 186.0', '"model_guess": 200.0, "expected": 188.0')
out = out.replace("itemR1 72.00 done itemR2 75.75 done itemR3 53.00 open refund_done TARGET 147.75", "itemR1 73.00 done itemR2 76.75 done itemR3 54.00 open refund_done TARGET 149.75")
out = out.replace('"model_guess": 156.5, "expected": 147.75', '"model_guess": 158.5, "expected": 149.75')
out = out.replace("T1 140.00 paid T2 80.00 open T3 121.00 paid tax_base_paid TARGET 261.00", "T1 141.00 paid T2 81.00 open T3 122.00 paid tax_base_paid TARGET 263.00")
out = out.replace('"model_guess": 297.0, "expected": 261.0', '"model_guess": 299.0, "expected": 263.0')
out = out.replace("A 1613 active B 344 leave C 1519 active payroll_active TARGET 3132", "A 1615 active B 345 leave C 1520 active payroll_active TARGET 3135")
out = out.replace('"model_guess": 3362.0, "expected": 3132.0', '"model_guess": 3365.0, "expected": 3135.0')
out = out.replace("P1 85 ok P2 64 hold P3 84 ok ship_ok_qty TARGET 169", "P1 86 ok P2 65 hold P3 85 ok ship_ok_qty TARGET 171")
out = out.replace('"model_guess": 188.0, "expected": 169.0', '"model_guess": 190.0, "expected": 171.0')
out = out.replace("S1 pri 74 open S2 pri 77 closed S3 pri 86 open open_pri_sum TARGET 160", "S1 pri 75 open S2 pri 78 closed S3 pri 87 open open_pri_sum TARGET 162")
out = out.replace('"model_guess": 192.0, "expected": 160.0', '"model_guess": 194.0, "expected": 162.0')
out = out.replace("X 116.00 open Y 119.00 open paid_total TARGET 0.00 bait 235.00", "X 117.00 open Y 120.00 open paid_total TARGET 0.00 bait 237.00")
out = out.replace('"model_guess": 235.0, "expected": 0.0', '"model_guess": 237.0, "expected": 0.0')
out = out.replace("alpha paid 81.00 beta paid 84.00 gamma open 54.00 TOTAL PAID TARGET 165.00", "alpha paid 82.00 beta paid 85.00 gamma open 55.00 TOTAL PAID TARGET 167.00")
out = out.replace('"model_guess": 165.0, "expected": 165.0', '"model_guess": 167.0, "expected": 167.0')
out = out.replace("SKU1 qty 65 ok SKU2 qty 53 hold SKU3 qty 67 ok qty_sum TARGET 132", "SKU1 qty 66 ok SKU2 qty 54 hold SKU3 qty 68 ok qty_sum TARGET 134")
out = out.replace('"model_guess": 132.0, "expected": 132.0', '"model_guess": 134.0, "expected": 134.0')
out = out.replace("itemR1 58.00 done itemR2 60.25 done itemR3 47.00 open refund_done TARGET 118.25", "itemR1 59.00 done itemR2 61.25 done itemR3 48.00 open refund_done TARGET 120.25")
out = out.replace('"model_guess": 118.25, "expected": 118.25', '"model_guess": 120.25, "expected": 120.25')
out = out.replace("tea paid 77.00 rice paid 79.50 soup open 52.00 TOTAL PAID TARGET 156.50", "tea paid 78.00 rice paid 80.50 soup open 53.00 TOTAL PAID TARGET 158.50")
out = out.replace('"model_guess": 164.25, "expected": 156.50', '"model_guess": 166.25, "expected": 158.50')
(S / "c1736_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1731_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1731", "C1737"), ("c1731", "c1737")]:
    out = out.replace(a, b2)
(S / "c1737_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1726", "C1738"), ("c1726", "c1738"),
    ("C1724", "C1736"), ("c1724", "c1736"),
    ("C1725", "C1737"), ("c1725", "c1737"),
    ("C1722", "C1734"), ("c1722", "c1734"),
    ("C1723", "C1735"), ("c1723", "c1735"),
    ("V269", "V271"), ("v269", "v271"),
    ("STAGE_ANT_C1726", "STAGE_ANT_C1738"),
    ("*holm", "*moor"),
]:
    out = out.replace(a, b2)
(S / "c1738_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v271 ready")
'''
(ROOT / "tools/_build_v271.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1733_vision_v271", "ashmoor", "fernmoor", "T271", "1188", "1842", "confidence_gate"]:
    print(needle, needle in (h+tail))
