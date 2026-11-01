from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v266.py").read_text(encoding="utf-8")
idx0 = b0.find('# V266 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("nethermere", "nethervale"), ("NETHERMERE", "NETHERVALE"),
    ("cedarmere", "cedarvale"), ("CEDARMERE", "CEDARVALE"),
    ("dawnmere", "dawnvale"), ("DAWNMERE", "DAWNVALE"),
    ("fernmere", "fernvale"), ("FERNMERE", "FERNVALE"),
    ("glenmere", "glenvale"), ("GLENMERE", "GLENVALE"),
    ("hazemere", "hazevale"), ("HAZEMERE", "HAZEVALE"),
    ("jademere", "jadevale"), ("JADEMERE", "JADEVALE"),
    ("knotmere", "knotvale"), ("KNOTMERE", "KNOTVALE"),
    ("lakemere", "lakevale"), ("LAKEMERE", "LAKEVALE"),
    ("mossmere", "mossvale"), ("MOSSMERE", "MOSSVALE"),
    ("pinemere", "pinevale"), ("PINEMERE", "PINEVALE"),
    ("quillmere", "quillvale"), ("QUILLMERE", "QUILLVALE"),
    ("reedmere", "reedvale"), ("REEDMERE", "REEDVALE"),
    ("stonemere", "stonevale"), ("STONEMERE", "STONEVALE"),
    ("ashmere", "ashvale"), ("ASHMERE", "ASHVALE"),
    ("elmmere", "elmvale"), ("ELMMERE", "ELMVALE"),
    ("inkmere", "inkvale"), ("INKMERE", "INKVALE"),
    ("oakmere", "oakvale"), ("OAKMERE", "OAKVALE"),
]
pairs = [
    ("*mere ; stack mid-band", "*vale ; stack mid-band"),
    ("T266", "T267"), ("TR266", "TR267"), ("HO266", "HO267"),
    ("NEW266", "NEW267"),
    ("V266", "V267"), ("v266", "v267"),
    ("_v266_themes.json", "_v267_themes.json"),
    ("_v265_themes.json", "_v266_themes.json"),
    ("OLD265", "OLD266"),
    ("vision_images_v266", "vision_images_v267"),
    ("VL_GATE_V266", "VL_GATE_V267"), ("vl_gate_v266", "vl_gate_v267"),
    ("C1703", "C1709"), ("c1703", "c1709"),
    ("C1704", "C1710"), ("c1704", "c1710"),
    ("C1705", "C1711"), ("c1705", "c1711"),
    ("_v266c1703", "_v267c1709"),
    ("Harder than V264", "Harder than V265"),
    ("harder than V264", "harder than V265"),
    ("NEW themes vs V264:", "NEW themes vs V265:"),
    ("kept on V266", "kept on V267"),
    ("V266 keeps floor", "V267 keeps floor"),
    ("C1703 design+fixtures; no VL claim", "C1709 design+fixtures; no VL claim"),
    ("retarget_265", "retarget_266"),
    ("*mere", "*vale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHVALE bait 179.89", "ASHVALE bait 180.90")
h = h.replace("CEDARM bait 181.91", "CEDARV bait 182.92")
h = h.replace("DAWNM ghost 104.14", "DAWNV ghost 105.15")
h = h.replace("GLENM bait 174.84", "GLENV bait 175.85")
h = h.replace("JADEM bait 165.75", "JADEV bait 166.76")
h = h.replace("NETHERM bait 182.92", "NETHERV bait 183.93")

TR = '''TR267 = [
    [2180.0, 2197.5, 1920.0],[840, 760, 820],[2103.0, 2132.25, 1898.0],[2236.0, 2253.0, 1988.0],
    [2298.0, 2322.0, 1958.0],[2016, 2032, 1916],[480.0, 520.0, 740.0],[2146.0, 2177.75, 1922.0],
    [840.0, 760.0, 820.0],[2213.0, 2201.0, 1919.0],[1,1,0],[0,0,0],
    [2279.0, 2300.5, 1944.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
# HO: ship 1874/1886/1834; order c 1836 — avoid BAN 1830
HO = '''HO267 = [
    [1978.0, 1990.75, 1839.0],[740, 780, 820],[1921.0, 1935.5, 1814.0],[2051.0, 2067.0, 1870.0],
    [2092.0, 2108.0, 1863.0],[1874, 1886, 1834],[360.0, 400.0, 730.0],[1962.0, 1983.75, 1839.0],
    [780.0, 740.0, 820.0],[2009.0, 1995.0, 1836.0],[1,1,0],[0,0,0],
    [2044.0, 2059.5, 1849.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR267\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO267\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1700_confidence_gate_stretch.py"
if not (ROOT / "scripts" / cg_src).exists():
    cg_src = "c1688_confidence_gate_stretch.py"
sc_src = "c1702_scorecard_and_stage.py"

tail = f'''# V267 knife = confidence-gate (alternating; V266 was product-U2C); theme wrap *vale
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1700", "C1712"), ("c1700", "c1712"),
    ("C1688", "C1712"), ("c1688", "c1712"),
    ("cg115_", "cg116_"),
    ("conf_gate_stretch_c1700", "conf_gate_stretch_c1712"),
    ("confidence_gate_stretch_v178", "confidence_gate_stretch_v179"),
    ("Stretch vs C1688", "Stretch vs C1700"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 94.00 b paid 98.75 c open 54.00 TOTAL PAID TARGET 192.75", "a paid 95.00 b paid 99.75 c open 55.00 TOTAL PAID TARGET 194.75")
out = out.replace('"model_guess": 999.0, "expected": 192.75', '"model_guess": 999.0, "expected": 194.75')
out = out.replace("SKU1 qty 89 ok SKU2 qty 63 hold SKU3 qty 93 ok qty_sum TARGET 182", "SKU1 qty 90 ok SKU2 qty 64 hold SKU3 qty 94 ok qty_sum TARGET 184")
out = out.replace('"model_guess": 194.0, "expected": 182.0', '"model_guess": 196.0, "expected": 184.0')
out = out.replace("itemR1 70.00 done itemR2 73.75 done itemR3 51.00 open refund_done TARGET 143.75", "itemR1 71.00 done itemR2 74.75 done itemR3 52.00 open refund_done TARGET 145.75")
out = out.replace('"model_guess": 152.5, "expected": 143.75', '"model_guess": 154.5, "expected": 145.75')
out = out.replace("T1 138.00 paid T2 78.00 open T3 119.00 paid tax_base_paid TARGET 257.00", "T1 139.00 paid T2 79.00 open T3 120.00 paid tax_base_paid TARGET 259.00")
out = out.replace('"model_guess": 293.0, "expected": 257.0', '"model_guess": 295.0, "expected": 259.0')
out = out.replace("A 1609 active B 342 leave C 1517 active payroll_active TARGET 3126", "A 1611 active B 343 leave C 1518 active payroll_active TARGET 3129")
out = out.replace('"model_guess": 3356.0, "expected": 3126.0', '"model_guess": 3359.0, "expected": 3129.0')
out = out.replace("P1 83 ok P2 62 hold P3 82 ok ship_ok_qty TARGET 165", "P1 84 ok P2 63 hold P3 83 ok ship_ok_qty TARGET 167")
out = out.replace('"model_guess": 184.0, "expected": 165.0', '"model_guess": 186.0, "expected": 167.0')
out = out.replace("S1 pri 72 open S2 pri 75 closed S3 pri 84 open open_pri_sum TARGET 156", "S1 pri 73 open S2 pri 76 closed S3 pri 85 open open_pri_sum TARGET 158")
out = out.replace('"model_guess": 188.0, "expected": 156.0', '"model_guess": 190.0, "expected": 158.0')
out = out.replace("X 114.00 open Y 117.00 open paid_total TARGET 0.00 bait 231.00", "X 115.00 open Y 118.00 open paid_total TARGET 0.00 bait 233.00")
out = out.replace('"model_guess": 231.0, "expected": 0.0', '"model_guess": 233.0, "expected": 0.0')
out = out.replace("alpha paid 79.00 beta paid 82.00 gamma open 52.00 TOTAL PAID TARGET 161.00", "alpha paid 80.00 beta paid 83.00 gamma open 53.00 TOTAL PAID TARGET 163.00")
out = out.replace('"model_guess": 161.0, "expected": 161.0', '"model_guess": 163.0, "expected": 163.0')
out = out.replace("SKU1 qty 63 ok SKU2 qty 51 hold SKU3 qty 65 ok qty_sum TARGET 128", "SKU1 qty 64 ok SKU2 qty 52 hold SKU3 qty 66 ok qty_sum TARGET 130")
out = out.replace('"model_guess": 128.0, "expected": 128.0', '"model_guess": 130.0, "expected": 130.0')
out = out.replace("itemR1 56.00 done itemR2 58.25 done itemR3 45.00 open refund_done TARGET 114.25", "itemR1 57.00 done itemR2 59.25 done itemR3 46.00 open refund_done TARGET 116.25")
out = out.replace('"model_guess": 114.25, "expected": 114.25', '"model_guess": 116.25, "expected": 116.25')
out = out.replace("tea paid 75.00 rice paid 77.50 soup open 50.00 TOTAL PAID TARGET 152.50", "tea paid 76.00 rice paid 78.50 soup open 51.00 TOTAL PAID TARGET 154.50")
out = out.replace('"model_guess": 160.25, "expected": 152.50', '"model_guess": 162.25, "expected": 154.50')
(S / "c1712_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1707_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1707", "C1713"), ("c1707", "c1713")]:
    out = out.replace(a, b2)
(S / "c1713_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1702", "C1714"), ("c1702", "c1714"),
    ("C1700", "C1712"), ("c1700", "c1712"),
    ("C1701", "C1713"), ("c1701", "c1713"),
    ("C1698", "C1710"), ("c1698", "c1710"),
    ("C1699", "C1711"), ("c1699", "c1711"),
    ("V265", "V267"), ("v265", "v267"),
    ("STAGE_ANT_C1702", "STAGE_ANT_C1714"),
    ("*hurst", "*vale"),
]:
    out = out.replace(a, b2)
(S / "c1714_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v267 ready")
'''
(ROOT / "tools/_build_v267.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1709_vision_v267", "ashvale", "fernvale", "T267", "1188", "1834", "confidence_gate", "*vale"]:
    print(needle, needle in (h+tail))
