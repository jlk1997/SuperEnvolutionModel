from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v282.py").read_text(encoding="utf-8")
idx0 = b0.find('# V282 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("nethermoor", "netherfen"), ("NETHERMOOR", "NETHERFEN"),
    ("cedarmoor", "cedarfen"), ("CEDARMOOR", "CEDARFEN"),
    ("dawnmoor", "dawnfen"), ("DAWNMOOR", "DAWNFEN"),
    ("fernmoor", "fernfen"), ("FERNMOOR", "FERNFEN"),
    ("glenmoor", "glenfen"), ("GLENMOOR", "GLENFEN"),
    ("hazemoor", "hazefen"), ("HAZEMOOR", "HAZEFEN"),
    ("jademoor", "jadefen"), ("JADEMOOR", "JADEFEN"),
    ("knotmoor", "knotfen"), ("KNOTMOOR", "KNOTFEN"),
    ("lakemoor", "lakefen"), ("LAKEMOOR", "LAKEFEN"),
    ("mossmoor", "mossfen"), ("MOSSMOOR", "MOSSFEN"),
    ("pinemoor", "pinefen"), ("PINEMOOR", "PINEFEN"),
    ("quillmoor", "quillfen"), ("QUILLMOOR", "QUILLFEN"),
    ("reedmoor", "reedfen"), ("REEDMOOR", "REEDFEN"),
    ("stonemoor", "stonefen"), ("STONEMOOR", "STONEFEN"),
    ("ashmoor", "ashfen"), ("ASHMOOR", "ASHFEN"),
    ("elmmoor", "elmfen"), ("ELMMOOR", "ELMFEN"),
    ("inkmoor", "inkfen"), ("INKMOOR", "INKFEN"),
    ("oakmoor", "oakfen"), ("OAKMOOR", "OAKFEN"),
]
pairs = [
    ("*moor ; stack mid-band", "*fen ; stack mid-band"),
    ("T282", "T283"), ("TR282", "TR283"), ("HO282", "HO283"),
    ("NEW282", "NEW283"),
    ("V282", "V283"), ("v282", "v283"),
    ("_v282_themes.json", "_v283_themes.json"),
    ("_v281_themes.json", "_v282_themes.json"),
    ("OLD281", "OLD282"),
    ("vision_images_v282", "vision_images_v283"),
    ("VL_GATE_V282", "VL_GATE_V283"), ("vl_gate_v282", "vl_gate_v283"),
    ("C1799", "C1805"), ("c1799", "c1805"),
    ("C1800", "C1806"), ("c1800", "c1806"),
    ("C1801", "C1807"), ("c1801", "c1807"),
    ("_v282c1799", "_v283c1805"),
    ("Harder than V280", "Harder than V281"),
    ("harder than V280", "harder than V281"),
    ("NEW themes vs V280:", "NEW themes vs V281:"),
    ("kept on V282", "kept on V283"),
    ("V282 keeps floor", "V283 keeps floor"),
    ("C1799 design+fixtures; no VL claim", "C1805 design+fixtures; no VL claim"),
    ("retarget_281", "retarget_282"),
    ("*moor", "*fen"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMOOR bait 195.05", "ASHFEN bait 196.06")
h = h.replace("CEDARM bait 197.07", "CEDARF bait 198.08")
h = h.replace("DAWNM ghost 120.30", "DAWNF ghost 121.31")
h = h.replace("GLENM bait 190.00", "GLENF bait 191.01")
h = h.replace("JADEM bait 181.91", "JADEF bait 182.92")
h = h.replace("NETHERM bait 198.08", "NETHERF bait 199.09")

TR = '''TR283 = [
    [2224.0, 2241.5, 1964.0],[840, 760, 820],[2147.0, 2176.25, 1942.0],[2280.0, 2297.0, 2032.0],
    [2342.0, 2366.0, 2002.0],[2060, 2076, 1960],[490.0, 530.0, 760.0],[2190.0, 2221.75, 1966.0],
    [840.0, 760.0, 820.0],[2257.0, 2245.0, 1963.0],[1,1,0],[0,0,0],
    [2323.0, 2344.5, 1988.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO283 = [
    [2022.0, 2034.75, 1883.0],[640, 660, 820],[1965.0, 1979.5, 1858.0],[2095.0, 2111.0, 1914.0],
    [2136.0, 2152.0, 1907.0],[1918, 1930, 1878],[420.0, 460.0, 740.0],[2006.0, 2027.75, 1883.0],
    [740.0, 780.0, 820.0],[2053.0, 2039.0, 1880.0],[1,1,0],[0,0,0],
    [2088.0, 2103.5, 1893.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR283\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO283\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1796_confidence_gate_stretch.py"
sc_src = "c1798_scorecard_and_stage.py"

tail = f'''# V283 knife = confidence-gate (alternating; V282 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1796", "C1808"), ("c1796", "c1808"),
    ("C1784", "C1808"), ("c1784", "c1808"),
    ("cg123_", "cg124_"),
    ("conf_gate_stretch_c1796", "conf_gate_stretch_c1808"),
    ("confidence_gate_stretch_v186", "confidence_gate_stretch_v187"),
    ("Stretch vs C1784", "Stretch vs C1796"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 102.00 b paid 106.75 c open 62.00 TOTAL PAID TARGET 208.75", "a paid 103.00 b paid 107.75 c open 63.00 TOTAL PAID TARGET 210.75")
out = out.replace('"model_guess": 999.0, "expected": 208.75', '"model_guess": 999.0, "expected": 210.75')
out = out.replace("SKU1 qty 97 ok SKU2 qty 71 hold SKU3 qty 101 ok qty_sum TARGET 198", "SKU1 qty 98 ok SKU2 qty 72 hold SKU3 qty 102 ok qty_sum TARGET 200")
out = out.replace('"model_guess": 210.0, "expected": 198.0', '"model_guess": 212.0, "expected": 200.0')
out = out.replace("itemR1 78.00 done itemR2 81.75 done itemR3 59.00 open refund_done TARGET 159.75", "itemR1 79.00 done itemR2 82.75 done itemR3 60.00 open refund_done TARGET 161.75")
out = out.replace('"model_guess": 168.5, "expected": 159.75', '"model_guess": 170.5, "expected": 161.75')
out = out.replace("T1 146.00 paid T2 86.00 open T3 127.00 paid tax_base_paid TARGET 273.00", "T1 147.00 paid T2 87.00 open T3 128.00 paid tax_base_paid TARGET 275.00")
out = out.replace('"model_guess": 309.0, "expected": 273.0', '"model_guess": 311.0, "expected": 275.0')
out = out.replace("A 1625 active B 350 leave C 1525 active payroll_active TARGET 3150", "A 1627 active B 351 leave C 1526 active payroll_active TARGET 3153")
out = out.replace('"model_guess": 3380.0, "expected": 3150.0', '"model_guess": 3383.0, "expected": 3153.0')
out = out.replace("P1 91 ok P2 70 hold P3 90 ok ship_ok_qty TARGET 181", "P1 92 ok P2 71 hold P3 91 ok ship_ok_qty TARGET 183")
out = out.replace('"model_guess": 200.0, "expected": 181.0', '"model_guess": 202.0, "expected": 183.0')
out = out.replace("S1 pri 80 open S2 pri 83 closed S3 pri 92 open open_pri_sum TARGET 172", "S1 pri 81 open S2 pri 84 closed S3 pri 93 open open_pri_sum TARGET 174")
out = out.replace('"model_guess": 204.0, "expected": 172.0', '"model_guess": 206.0, "expected": 174.0')
out = out.replace("X 122.00 open Y 125.00 open paid_total TARGET 0.00 bait 247.00", "X 123.00 open Y 126.00 open paid_total TARGET 0.00 bait 249.00")
out = out.replace('"model_guess": 247.0, "expected": 0.0', '"model_guess": 249.0, "expected": 0.0')
out = out.replace("alpha paid 87.00 beta paid 90.00 gamma open 60.00 TOTAL PAID TARGET 177.00", "alpha paid 88.00 beta paid 91.00 gamma open 61.00 TOTAL PAID TARGET 179.00")
out = out.replace('"model_guess": 177.0, "expected": 177.0', '"model_guess": 179.0, "expected": 179.0')
out = out.replace("SKU1 qty 71 ok SKU2 qty 59 hold SKU3 qty 73 ok qty_sum TARGET 144", "SKU1 qty 72 ok SKU2 qty 60 hold SKU3 qty 74 ok qty_sum TARGET 146")
out = out.replace('"model_guess": 144.0, "expected": 144.0', '"model_guess": 146.0, "expected": 146.0')
out = out.replace("itemR1 64.00 done itemR2 66.25 done itemR3 53.00 open refund_done TARGET 130.25", "itemR1 65.00 done itemR2 67.25 done itemR3 54.00 open refund_done TARGET 132.25")
out = out.replace('"model_guess": 130.25, "expected": 130.25', '"model_guess": 132.25, "expected": 132.25')
out = out.replace("tea paid 83.00 rice paid 85.50 soup open 58.00 TOTAL PAID TARGET 168.50", "tea paid 84.00 rice paid 86.50 soup open 59.00 TOTAL PAID TARGET 170.50")
out = out.replace('"model_guess": 176.25, "expected": 168.50', '"model_guess": 178.25, "expected": 170.50')
(S / "c1808_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1803_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1803", "C1809"), ("c1803", "c1809")]:
    out = out.replace(a, b2)
(S / "c1809_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1798", "C1810"), ("c1798", "c1810"),
    ("C1796", "C1808"), ("c1796", "c1808"),
    ("C1797", "C1809"), ("c1797", "c1809"),
    ("C1794", "C1806"), ("c1794", "c1806"),
    ("C1795", "C1807"), ("c1795", "c1807"),
    ("V281", "V283"), ("v281", "v283"),
    ("STAGE_ANT_C1798", "STAGE_ANT_C1810"),
    ("*wick", "*fen"),
]:
    out = out.replace(a, b2)
(S / "c1810_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v283 ready")
'''
(ROOT / "tools/_build_v283.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1805_vision_v283", "ashfen", "fernfen", "T283", "1188", "1878", "confidence_gate", "retarget_282"]:
    print(needle, needle in (h+tail))
