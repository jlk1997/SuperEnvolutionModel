from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v310.py").read_text(encoding="utf-8")
idx0 = b0.find('# V310 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1972 = " in head0:
    head0 = head0[:head0.find("SC1972 = ")]

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
    ("T310", "T311"), ("TR310", "TR311"), ("HO310", "HO311"),
    ("NEW310", "NEW311"),
    ("V310", "V311"), ("v310", "v311"),
    ("_v310_themes.json", "_v311_themes.json"),
    ("_v309_themes.json", "_v310_themes.json"),
    ("OLD309", "OLD310"),
    ("vision_images_v310", "vision_images_v311"),
    ("VL_GATE_V310", "VL_GATE_V311"), ("vl_gate_v310", "vl_gate_v311"),
    ("C1967", "C1973"), ("c1967", "c1973"),
    ("C1968", "C1974"), ("c1968", "c1974"),
    ("C1969", "C1975"), ("c1969", "c1975"),
    ("_v310c1967", "_v311c1973"),
    ("Harder than V308", "Harder than V309"),
    ("harder than V308", "harder than V309"),
    ("NEW themes vs V308:", "NEW themes vs V309:"),
    ("kept on V310", "kept on V311"),
    ("V310 keeps floor", "V311 keeps floor"),
    ("C1967 design+fixtures; no VL claim", "C1973 design+fixtures; no VL claim"),
    ("retarget_309", "retarget_310"),
    ("*mere", "*vale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMERE bait 223.33", "ASHVALE bait 224.34")
h = h.replace("CEDARM bait 225.35", "CEDARV bait 226.36")
h = h.replace("DAWNM ghost 148.58", "DAWNV ghost 149.59")
h = h.replace("GLENM bait 218.28", "GLENV bait 219.29")
h = h.replace("JADEM bait 209.19", "JADEV bait 210.20")
h = h.replace("NETHERM bait 226.36", "NETHERV bait 227.37")

TR = '''TR311 = [
    [2286.0, 2303.5, 2026.0],[840, 760, 820],[2209.0, 2238.25, 2004.0],[2342.0, 2359.0, 2094.0],
    [2404.0, 2428.0, 2064.0],[2122, 2138, 2022],[490.0, 530.0, 760.0],[2252.0, 2283.75, 2028.0],
    [840.0, 760.0, 820.0],[2319.0, 2307.0, 2025.0],[1,1,0],[0,0,0],
    [2385.0, 2406.5, 2050.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO311 = [
    [2084.0, 2096.75, 1945.0],[640, 660, 820],[2027.0, 2041.5, 1920.0],[2157.0, 2173.0, 1976.0],
    [2198.0, 2214.0, 1969.0],[1980, 1992, 1940],[420.0, 460.0, 740.0],[2068.0, 2089.75, 1945.0],
    [740.0, 780.0, 820.0],[2115.0, 2101.0, 1942.0],[1,1,0],[0,0,0],
    [2150.0, 2165.5, 1955.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR311\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO311\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1964_confidence_gate_stretch.py"
sc_body = (ROOT / "scripts/c1966_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1966", "C1978"), ("c1966", "c1978"),
    ("C1964", "C1976"), ("c1964", "c1976"),
    ("C1965", "C1977"), ("c1965", "c1977"),
    ("C1962", "C1974"), ("c1962", "c1974"),
    ("C1963", "C1975"), ("c1963", "c1975"),
    ("V309", "V311"), ("v309", "v311"),
    ("STAGE_ANT_C1966", "STAGE_ANT_C1978"),
    ("*hurst", "*vale"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V311 knife = confidence-gate (alternating; V310 was product-U2C; theme wrap *mere→*vale)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1964", "C1976"), ("c1964", "c1976"),
    ("C1952", "C1976"), ("c1952", "c1976"),
    ("cg137_", "cg138_"),
    ("conf_gate_stretch_c1964", "conf_gate_stretch_c1976"),
    ("confidence_gate_stretch_v200", "confidence_gate_stretch_v201"),
    ("Stretch vs C1952", "Stretch vs C1964"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 116.00 b paid 120.75 c open 76.00 TOTAL PAID TARGET 236.75", "a paid 117.00 b paid 121.75 c open 77.00 TOTAL PAID TARGET 238.75")
out = out.replace('"model_guess": 999.0, "expected": 236.75', '"model_guess": 999.0, "expected": 238.75')
out = out.replace("SKU1 qty 111 ok SKU2 qty 85 hold SKU3 qty 115 ok qty_sum TARGET 226", "SKU1 qty 112 ok SKU2 qty 86 hold SKU3 qty 116 ok qty_sum TARGET 228")
out = out.replace('"model_guess": 238.0, "expected": 226.0', '"model_guess": 240.0, "expected": 228.0')
out = out.replace("itemR1 92.00 done itemR2 95.75 done itemR3 73.00 open refund_done TARGET 187.75", "itemR1 93.00 done itemR2 96.75 done itemR3 74.00 open refund_done TARGET 189.75")
out = out.replace('"model_guess": 196.5, "expected": 187.75', '"model_guess": 198.5, "expected": 189.75')
out = out.replace("T1 160.00 paid T2 100.00 open T3 141.00 paid tax_base_paid TARGET 301.00", "T1 161.00 paid T2 101.00 open T3 142.00 paid tax_base_paid TARGET 303.00")
out = out.replace('"model_guess": 337.0, "expected": 301.0', '"model_guess": 339.0, "expected": 303.0')
out = out.replace("A 1653 active B 364 leave C 1539 active payroll_active TARGET 3192", "A 1655 active B 365 leave C 1540 active payroll_active TARGET 3195")
out = out.replace('"model_guess": 3422.0, "expected": 3192.0', '"model_guess": 3425.0, "expected": 3195.0')
out = out.replace("P1 105 ok P2 84 hold P3 104 ok ship_ok_qty TARGET 209", "P1 106 ok P2 85 hold P3 105 ok ship_ok_qty TARGET 211")
out = out.replace('"model_guess": 228.0, "expected": 209.0', '"model_guess": 230.0, "expected": 211.0')
out = out.replace("S1 pri 94 open S2 pri 97 closed S3 pri 106 open open_pri_sum TARGET 200", "S1 pri 95 open S2 pri 98 closed S3 pri 107 open open_pri_sum TARGET 202")
out = out.replace('"model_guess": 232.0, "expected": 200.0', '"model_guess": 234.0, "expected": 202.0')
out = out.replace("X 136.00 open Y 139.00 open paid_total TARGET 0.00 bait 275.00", "X 137.00 open Y 140.00 open paid_total TARGET 0.00 bait 277.00")
out = out.replace('"model_guess": 275.0, "expected": 0.0', '"model_guess": 277.0, "expected": 0.0')
out = out.replace("alpha paid 101.00 beta paid 104.00 gamma open 74.00 TOTAL PAID TARGET 205.00", "alpha paid 102.00 beta paid 105.00 gamma open 75.00 TOTAL PAID TARGET 207.00")
out = out.replace('"model_guess": 205.0, "expected": 205.0', '"model_guess": 207.0, "expected": 207.0')
out = out.replace("SKU1 qty 85 ok SKU2 qty 73 hold SKU3 qty 87 ok qty_sum TARGET 172", "SKU1 qty 86 ok SKU2 qty 74 hold SKU3 qty 88 ok qty_sum TARGET 174")
out = out.replace('"model_guess": 172.0, "expected": 172.0', '"model_guess": 174.0, "expected": 174.0')
out = out.replace("itemR1 78.00 done itemR2 80.25 done itemR3 67.00 open refund_done TARGET 158.25", "itemR1 79.00 done itemR2 81.25 done itemR3 68.00 open refund_done TARGET 160.25")
out = out.replace('"model_guess": 158.25, "expected": 158.25', '"model_guess": 160.25, "expected": 160.25')
out = out.replace("tea paid 97.00 rice paid 99.50 soup open 72.00 TOTAL PAID TARGET 196.50", "tea paid 98.00 rice paid 100.50 soup open 73.00 TOTAL PAID TARGET 198.50")
out = out.replace('"model_guess": 204.25, "expected": 196.50', '"model_guess": 206.25, "expected": 198.50')
(S / "c1976_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1971_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1971", "C1977"), ("c1971", "c1977")]:
    out = out.replace(a, b2)
(S / "c1977_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1978_scorecard_and_stage.py").write_text(SC1978, encoding="utf-8")
print("scorecard from fixed c1966 conf-gate pattern")
print("OK builder v311 ready")
'''
pre = "SC1978 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v311.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1973_vision_v311", "ashvale", "fernvale", "T311", "1188", "1940", "confidence_gate", "retarget_310", "theme wrap"]:
    print(needle, needle in (h+pre+tail))
