from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v286.py").read_text(encoding="utf-8")
idx0 = b0.find('# V286 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("netherford", "netherhurst"), ("NETHERFORD", "NETHERHURST"),
    ("cedarford", "cedarhurst"), ("CEDARFORD", "CEDARHURST"),
    ("dawnford", "dawnhurst"), ("DAWNFORD", "DAWNHURST"),
    ("fernford", "fernhurst"), ("FERNFORD", "FERNHURST"),
    ("glenford", "glenhurst"), ("GLENFORD", "GLENHURST"),
    ("hazeford", "hazehurst"), ("HAZEFORD", "HAZEHURST"),
    ("jadeford", "jadehurst"), ("JADEFORD", "JADEHURST"),
    ("knotford", "knothurst"), ("KNOTFORD", "KNOTHURST"),
    ("lakeford", "lakehurst"), ("LAKEFORD", "LAKEHURST"),
    ("mossford", "mosshurst"), ("MOSSFORD", "MOSSHURST"),
    ("pineford", "pinehurst"), ("PINEFORD", "PINEHURST"),
    ("quillford", "quillhurst"), ("QUILLFORD", "QUILLHURST"),
    ("reedford", "reedhurst"), ("REEDFORD", "REEDHURST"),
    ("stoneford", "stonehurst"), ("STONEFORD", "STONEHURST"),
    ("ashford", "ashhurst"), ("ASHFORD", "ASHHURST"),
    ("elmford", "elmhurst"), ("ELMFORD", "ELMHURST"),
    ("inkford", "inkhurst"), ("INKFORD", "INKHURST"),
    ("oakford", "oakhurst"), ("OAKFORD", "OAKHURST"),
]
pairs = [
    ("*ford ; stack mid-band", "*hurst ; stack mid-band"),
    ("T286", "T287"), ("TR286", "TR287"), ("HO286", "HO287"),
    ("NEW286", "NEW287"),
    ("V286", "V287"), ("v286", "v287"),
    ("_v286_themes.json", "_v287_themes.json"),
    ("_v285_themes.json", "_v286_themes.json"),
    ("OLD285", "OLD286"),
    ("vision_images_v286", "vision_images_v287"),
    ("VL_GATE_V286", "VL_GATE_V287"), ("vl_gate_v286", "vl_gate_v287"),
    ("C1823", "C1829"), ("c1823", "c1829"),
    ("C1824", "C1830"), ("c1824", "c1830"),
    ("C1825", "C1831"), ("c1825", "c1831"),
    ("_v286c1823", "_v287c1829"),
    ("Harder than V284", "Harder than V285"),
    ("harder than V284", "harder than V285"),
    ("NEW themes vs V284:", "NEW themes vs V285:"),
    ("kept on V286", "kept on V287"),
    ("V286 keeps floor", "V287 keeps floor"),
    ("C1823 design+fixtures; no VL claim", "C1829 design+fixtures; no VL claim"),
    ("retarget_285", "retarget_286"),
    ("*ford", "*hurst"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFORD bait 199.09", "ASHHURST bait 200.10")
h = h.replace("CEDARF bait 201.11", "CEDARH bait 202.12")
h = h.replace("DAWNF ghost 124.34", "DAWNH ghost 125.35")
h = h.replace("GLENF bait 194.04", "GLENH bait 195.05")
h = h.replace("JADEF bait 185.95", "JADEH bait 186.96")
h = h.replace("NETHERF bait 202.12", "NETHERH bait 203.13")

TR = '''TR287 = [
    [2236.0, 2253.5, 1976.0],[840, 760, 820],[2159.0, 2188.25, 1954.0],[2292.0, 2309.0, 2044.0],
    [2354.0, 2378.0, 2014.0],[2072, 2088, 1972],[490.0, 530.0, 760.0],[2202.0, 2233.75, 1978.0],
    [840.0, 760.0, 820.0],[2269.0, 2257.0, 1975.0],[1,1,0],[0,0,0],
    [2335.0, 2356.5, 2000.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO287 = [
    [2034.0, 2046.75, 1895.0],[640, 660, 820],[1977.0, 1991.5, 1870.0],[2107.0, 2123.0, 1926.0],
    [2148.0, 2164.0, 1919.0],[1930, 1942, 1890],[420.0, 460.0, 740.0],[2018.0, 2039.75, 1895.0],
    [740.0, 780.0, 820.0],[2065.0, 2051.0, 1892.0],[1,1,0],[0,0,0],
    [2100.0, 2115.5, 1905.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR287\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO287\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1820_confidence_gate_stretch.py"
sc_src = "c1822_scorecard_and_stage.py"

tail = f'''# V287 knife = confidence-gate (alternating; V286 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1820", "C1832"), ("c1820", "c1832"),
    ("C1808", "C1832"), ("c1808", "c1832"),
    ("cg125_", "cg126_"),
    ("conf_gate_stretch_c1820", "conf_gate_stretch_c1832"),
    ("confidence_gate_stretch_v188", "confidence_gate_stretch_v189"),
    ("Stretch vs C1808", "Stretch vs C1820"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 104.00 b paid 108.75 c open 64.00 TOTAL PAID TARGET 212.75", "a paid 105.00 b paid 109.75 c open 65.00 TOTAL PAID TARGET 214.75")
out = out.replace('"model_guess": 999.0, "expected": 212.75', '"model_guess": 999.0, "expected": 214.75')
out = out.replace("SKU1 qty 99 ok SKU2 qty 73 hold SKU3 qty 103 ok qty_sum TARGET 202", "SKU1 qty 100 ok SKU2 qty 74 hold SKU3 qty 104 ok qty_sum TARGET 204")
out = out.replace('"model_guess": 214.0, "expected": 202.0', '"model_guess": 216.0, "expected": 204.0')
out = out.replace("itemR1 80.00 done itemR2 83.75 done itemR3 61.00 open refund_done TARGET 163.75", "itemR1 81.00 done itemR2 84.75 done itemR3 62.00 open refund_done TARGET 165.75")
out = out.replace('"model_guess": 172.5, "expected": 163.75', '"model_guess": 174.5, "expected": 165.75')
out = out.replace("T1 148.00 paid T2 88.00 open T3 129.00 paid tax_base_paid TARGET 277.00", "T1 149.00 paid T2 89.00 open T3 130.00 paid tax_base_paid TARGET 279.00")
out = out.replace('"model_guess": 313.0, "expected": 277.0', '"model_guess": 315.0, "expected": 279.0')
out = out.replace("A 1629 active B 352 leave C 1527 active payroll_active TARGET 3156", "A 1631 active B 353 leave C 1528 active payroll_active TARGET 3159")
out = out.replace('"model_guess": 3386.0, "expected": 3156.0', '"model_guess": 3389.0, "expected": 3159.0')
out = out.replace("P1 93 ok P2 72 hold P3 92 ok ship_ok_qty TARGET 185", "P1 94 ok P2 73 hold P3 93 ok ship_ok_qty TARGET 187")
out = out.replace('"model_guess": 204.0, "expected": 185.0', '"model_guess": 206.0, "expected": 187.0')
out = out.replace("S1 pri 82 open S2 pri 85 closed S3 pri 94 open open_pri_sum TARGET 176", "S1 pri 83 open S2 pri 86 closed S3 pri 95 open open_pri_sum TARGET 178")
out = out.replace('"model_guess": 208.0, "expected": 176.0', '"model_guess": 210.0, "expected": 178.0')
out = out.replace("X 124.00 open Y 127.00 open paid_total TARGET 0.00 bait 251.00", "X 125.00 open Y 128.00 open paid_total TARGET 0.00 bait 253.00")
out = out.replace('"model_guess": 251.0, "expected": 0.0', '"model_guess": 253.0, "expected": 0.0')
out = out.replace("alpha paid 89.00 beta paid 92.00 gamma open 62.00 TOTAL PAID TARGET 181.00", "alpha paid 90.00 beta paid 93.00 gamma open 63.00 TOTAL PAID TARGET 183.00")
out = out.replace('"model_guess": 181.0, "expected": 181.0', '"model_guess": 183.0, "expected": 183.0')
out = out.replace("SKU1 qty 73 ok SKU2 qty 61 hold SKU3 qty 75 ok qty_sum TARGET 148", "SKU1 qty 74 ok SKU2 qty 62 hold SKU3 qty 76 ok qty_sum TARGET 150")
out = out.replace('"model_guess": 148.0, "expected": 148.0', '"model_guess": 150.0, "expected": 150.0')
out = out.replace("itemR1 66.00 done itemR2 68.25 done itemR3 55.00 open refund_done TARGET 134.25", "itemR1 67.00 done itemR2 69.25 done itemR3 56.00 open refund_done TARGET 136.25")
out = out.replace('"model_guess": 134.25, "expected": 134.25', '"model_guess": 136.25, "expected": 136.25')
out = out.replace("tea paid 85.00 rice paid 87.50 soup open 60.00 TOTAL PAID TARGET 172.50", "tea paid 86.00 rice paid 88.50 soup open 61.00 TOTAL PAID TARGET 174.50")
out = out.replace('"model_guess": 180.25, "expected": 172.50', '"model_guess": 182.25, "expected": 174.50')
(S / "c1832_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1827_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1827", "C1833"), ("c1827", "c1833")]:
    out = out.replace(a, b2)
(S / "c1833_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1822", "C1834"), ("c1822", "c1834"),
    ("C1820", "C1832"), ("c1820", "c1832"),
    ("C1821", "C1833"), ("c1821", "c1833"),
    ("C1818", "C1830"), ("c1818", "c1830"),
    ("C1819", "C1831"), ("c1819", "c1831"),
    ("V285", "V287"), ("v285", "v287"),
    ("STAGE_ANT_C1822", "STAGE_ANT_C1834"),
    ("*dale", "*hurst"),
]:
    out = out.replace(a, b2)
(S / "c1834_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v287 ready")
'''
(ROOT / "tools/_build_v287.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1829_vision_v287", "ashhurst", "fernhurst", "T287", "1188", "1890", "confidence_gate", "retarget_286"]:
    print(needle, needle in (h+tail))
