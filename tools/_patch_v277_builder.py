from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v276.py").read_text(encoding="utf-8")
idx0 = b0.find('# V276 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
    ("T276", "T277"), ("TR276", "TR277"), ("HO276", "HO277"),
    ("NEW276", "NEW277"),
    ("V276", "V277"), ("v276", "v277"),
    ("_v276_themes.json", "_v277_themes.json"),
    ("_v275_themes.json", "_v276_themes.json"),
    ("OLD275", "OLD276"),
    ("vision_images_v276", "vision_images_v277"),
    ("VL_GATE_V276", "VL_GATE_V277"), ("vl_gate_v276", "vl_gate_v277"),
    ("C1763", "C1769"), ("c1763", "c1769"),
    ("C1764", "C1770"), ("c1764", "c1770"),
    ("C1765", "C1771"), ("c1765", "c1771"),
    ("_v276c1763", "_v277c1769"),
    ("Harder than V274", "Harder than V275"),
    ("harder than V274", "harder than V275"),
    ("NEW themes vs V274:", "NEW themes vs V275:"),
    ("kept on V276", "kept on V277"),
    ("V276 keeps floor", "V277 keeps floor"),
    ("C1763 design+fixtures; no VL claim", "C1769 design+fixtures; no VL claim"),
    ("retarget_275", "retarget_276"),
    ("*hurst", "*mere"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHURST bait 189.99", "ASHMERE bait 190.00")
h = h.replace("CEDARH bait 191.01", "CEDARM bait 192.02")
h = h.replace("DAWNH ghost 114.24", "DAWNM ghost 115.25")
h = h.replace("GLENH bait 184.94", "GLENM bait 185.95")
h = h.replace("JADEH bait 175.85", "JADEM bait 176.86")
h = h.replace("NETHERH bait 192.02", "NETHERM bait 193.03")

TR = '''TR277 = [
    [2206.0, 2223.5, 1946.0],[840, 760, 820],[2129.0, 2158.25, 1924.0],[2262.0, 2279.0, 2014.0],
    [2324.0, 2348.0, 1984.0],[2042, 2058, 1942],[540.0, 580.0, 760.0],[2172.0, 2203.75, 1948.0],
    [840.0, 760.0, 820.0],[2239.0, 2227.0, 1945.0],[1,1,0],[0,0,0],
    [2305.0, 2326.5, 1970.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO277 = [
    [2004.0, 2016.75, 1865.0],[640, 660, 820],[1947.0, 1961.5, 1840.0],[2077.0, 2093.0, 1896.0],
    [2118.0, 2134.0, 1889.0],[1900, 1912, 1860],[420.0, 460.0, 740.0],[1988.0, 2009.75, 1865.0],
    [740.0, 780.0, 820.0],[2035.0, 2021.0, 1862.0],[1,1,0],[0,0,0],
    [2070.0, 2085.5, 1875.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR277\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO277\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1760_confidence_gate_stretch.py"
sc_src = "c1762_scorecard_and_stage.py"

tail = f'''# V277 knife = confidence-gate (alternating; V276 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1760", "C1772"), ("c1760", "c1772"),
    ("C1748", "C1772"), ("c1748", "c1772"),
    ("cg120_", "cg121_"),
    ("conf_gate_stretch_c1760", "conf_gate_stretch_c1772"),
    ("confidence_gate_stretch_v183", "confidence_gate_stretch_v184"),
    ("Stretch vs C1748", "Stretch vs C1760"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 99.00 b paid 103.75 c open 59.00 TOTAL PAID TARGET 202.75", "a paid 100.00 b paid 104.75 c open 60.00 TOTAL PAID TARGET 204.75")
out = out.replace('"model_guess": 999.0, "expected": 202.75', '"model_guess": 999.0, "expected": 204.75')
out = out.replace("SKU1 qty 94 ok SKU2 qty 68 hold SKU3 qty 98 ok qty_sum TARGET 192", "SKU1 qty 95 ok SKU2 qty 69 hold SKU3 qty 99 ok qty_sum TARGET 194")
out = out.replace('"model_guess": 204.0, "expected": 192.0', '"model_guess": 206.0, "expected": 194.0')
out = out.replace("itemR1 75.00 done itemR2 78.75 done itemR3 56.00 open refund_done TARGET 153.75", "itemR1 76.00 done itemR2 79.75 done itemR3 57.00 open refund_done TARGET 155.75")
out = out.replace('"model_guess": 162.5, "expected": 153.75', '"model_guess": 164.5, "expected": 155.75')
out = out.replace("T1 143.00 paid T2 83.00 open T3 124.00 paid tax_base_paid TARGET 267.00", "T1 144.00 paid T2 84.00 open T3 125.00 paid tax_base_paid TARGET 269.00")
out = out.replace('"model_guess": 303.0, "expected": 267.0', '"model_guess": 305.0, "expected": 269.0')
out = out.replace("A 1619 active B 347 leave C 1522 active payroll_active TARGET 3141", "A 1621 active B 348 leave C 1523 active payroll_active TARGET 3144")
out = out.replace('"model_guess": 3371.0, "expected": 3141.0', '"model_guess": 3374.0, "expected": 3144.0')
out = out.replace("P1 88 ok P2 67 hold P3 87 ok ship_ok_qty TARGET 175", "P1 89 ok P2 68 hold P3 88 ok ship_ok_qty TARGET 177")
out = out.replace('"model_guess": 194.0, "expected": 175.0', '"model_guess": 196.0, "expected": 177.0')
out = out.replace("S1 pri 77 open S2 pri 80 closed S3 pri 89 open open_pri_sum TARGET 166", "S1 pri 78 open S2 pri 81 closed S3 pri 90 open open_pri_sum TARGET 168")
out = out.replace('"model_guess": 198.0, "expected": 166.0', '"model_guess": 200.0, "expected": 168.0')
out = out.replace("X 119.00 open Y 122.00 open paid_total TARGET 0.00 bait 241.00", "X 120.00 open Y 123.00 open paid_total TARGET 0.00 bait 243.00")
out = out.replace('"model_guess": 241.0, "expected": 0.0', '"model_guess": 243.0, "expected": 0.0')
out = out.replace("alpha paid 84.00 beta paid 87.00 gamma open 57.00 TOTAL PAID TARGET 171.00", "alpha paid 85.00 beta paid 88.00 gamma open 58.00 TOTAL PAID TARGET 173.00")
out = out.replace('"model_guess": 171.0, "expected": 171.0', '"model_guess": 173.0, "expected": 173.0')
out = out.replace("SKU1 qty 68 ok SKU2 qty 56 hold SKU3 qty 70 ok qty_sum TARGET 138", "SKU1 qty 69 ok SKU2 qty 57 hold SKU3 qty 71 ok qty_sum TARGET 140")
out = out.replace('"model_guess": 138.0, "expected": 138.0', '"model_guess": 140.0, "expected": 140.0')
out = out.replace("itemR1 61.00 done itemR2 63.25 done itemR3 50.00 open refund_done TARGET 124.25", "itemR1 62.00 done itemR2 64.25 done itemR3 51.00 open refund_done TARGET 126.25")
out = out.replace('"model_guess": 124.25, "expected": 124.25', '"model_guess": 126.25, "expected": 126.25')
out = out.replace("tea paid 80.00 rice paid 82.50 soup open 55.00 TOTAL PAID TARGET 162.50", "tea paid 81.00 rice paid 83.50 soup open 56.00 TOTAL PAID TARGET 164.50")
out = out.replace('"model_guess": 170.25, "expected": 162.50', '"model_guess": 172.25, "expected": 164.50')
(S / "c1772_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1767_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1767", "C1773"), ("c1767", "c1773")]:
    out = out.replace(a, b2)
(S / "c1773_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1762", "C1774"), ("c1762", "c1774"),
    ("C1760", "C1772"), ("c1760", "c1772"),
    ("C1761", "C1773"), ("c1761", "c1773"),
    ("C1758", "C1770"), ("c1758", "c1770"),
    ("C1759", "C1771"), ("c1759", "c1771"),
    ("V275", "V277"), ("v275", "v277"),
    ("STAGE_ANT_C1762", "STAGE_ANT_C1774"),
    ("*ford", "*mere"),
]:
    out = out.replace(a, b2)
(S / "c1774_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v277 ready")
'''
(ROOT / "tools/_build_v277.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1769_vision_v277", "ashmere", "fernmere", "T277", "1188", "1860", "confidence_gate", "retarget_276"]:
    print(needle, needle in (h+tail))
