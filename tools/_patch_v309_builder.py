from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v308.py").read_text(encoding="utf-8")
idx0 = b0.find('# V308 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1960 = " in head0:
    head0 = head0[:head0.find("SC1960 = ")]

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
    ("T308", "T309"), ("TR308", "TR309"), ("HO308", "HO309"),
    ("NEW308", "NEW309"),
    ("V308", "V309"), ("v308", "v309"),
    ("_v308_themes.json", "_v309_themes.json"),
    ("_v307_themes.json", "_v308_themes.json"),
    ("OLD307", "OLD308"),
    ("vision_images_v308", "vision_images_v309"),
    ("VL_GATE_V308", "VL_GATE_V309"), ("vl_gate_v308", "vl_gate_v309"),
    ("C1955", "C1961"), ("c1955", "c1961"),
    ("C1956", "C1962"), ("c1956", "c1962"),
    ("C1957", "C1963"), ("c1957", "c1963"),
    ("_v308c1955", "_v309c1961"),
    ("Harder than V306", "Harder than V307"),
    ("harder than V306", "harder than V307"),
    ("NEW themes vs V306:", "NEW themes vs V307:"),
    ("kept on V308", "kept on V309"),
    ("V308 keeps floor", "V309 keeps floor"),
    ("C1955 design+fixtures; no VL claim", "C1961 design+fixtures; no VL claim"),
    ("retarget_307", "retarget_308"),
    ("*ford", "*hurst"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFORD bait 221.31", "ASHHURST bait 222.32")
h = h.replace("CEDARF bait 223.33", "CEDARH bait 224.34")
h = h.replace("DAWNF ghost 146.56", "DAWNH ghost 147.57")
h = h.replace("GLENF bait 216.26", "GLENH bait 217.27")
h = h.replace("JADEF bait 207.17", "JADEH bait 208.18")
h = h.replace("NETHERF bait 224.34", "NETHERH bait 225.35")

TR = '''TR309 = [
    [2282.0, 2299.5, 2022.0],[840, 760, 820],[2205.0, 2234.25, 2000.0],[2338.0, 2355.0, 2090.0],
    [2400.0, 2424.0, 2060.0],[2118, 2134, 2018],[490.0, 530.0, 760.0],[2248.0, 2279.75, 2024.0],
    [840.0, 760.0, 820.0],[2315.0, 2303.0, 2021.0],[1,1,0],[0,0,0],
    [2381.0, 2402.5, 2046.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO309 = [
    [2080.0, 2092.75, 1941.0],[640, 660, 820],[2023.0, 2037.5, 1916.0],[2153.0, 2169.0, 1972.0],
    [2194.0, 2210.0, 1965.0],[1976, 1988, 1936],[420.0, 460.0, 740.0],[2064.0, 2085.75, 1941.0],
    [740.0, 780.0, 820.0],[2111.0, 2097.0, 1938.0],[1,1,0],[0,0,0],
    [2146.0, 2161.5, 1951.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR309\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO309\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1952_confidence_gate_stretch.py"
sc_body = (ROOT / "scripts/c1954_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1954", "C1966"), ("c1954", "c1966"),
    ("C1952", "C1964"), ("c1952", "c1964"),
    ("C1953", "C1965"), ("c1953", "c1965"),
    ("C1950", "C1962"), ("c1950", "c1962"),
    ("C1951", "C1963"), ("c1951", "c1963"),
    ("V307", "V309"), ("v307", "v309"),
    ("STAGE_ANT_C1954", "STAGE_ANT_C1966"),
    ("*dale", "*hurst"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V309 knife = confidence-gate (alternating; V308 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1952", "C1964"), ("c1952", "c1964"),
    ("C1940", "C1964"), ("c1940", "c1964"),
    ("cg136_", "cg137_"),
    ("conf_gate_stretch_c1952", "conf_gate_stretch_c1964"),
    ("confidence_gate_stretch_v199", "confidence_gate_stretch_v200"),
    ("Stretch vs C1940", "Stretch vs C1952"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 115.00 b paid 119.75 c open 75.00 TOTAL PAID TARGET 234.75", "a paid 116.00 b paid 120.75 c open 76.00 TOTAL PAID TARGET 236.75")
out = out.replace('"model_guess": 999.0, "expected": 234.75', '"model_guess": 999.0, "expected": 236.75')
out = out.replace("SKU1 qty 110 ok SKU2 qty 84 hold SKU3 qty 114 ok qty_sum TARGET 224", "SKU1 qty 111 ok SKU2 qty 85 hold SKU3 qty 115 ok qty_sum TARGET 226")
out = out.replace('"model_guess": 236.0, "expected": 224.0', '"model_guess": 238.0, "expected": 226.0')
out = out.replace("itemR1 91.00 done itemR2 94.75 done itemR3 72.00 open refund_done TARGET 185.75", "itemR1 92.00 done itemR2 95.75 done itemR3 73.00 open refund_done TARGET 187.75")
out = out.replace('"model_guess": 194.5, "expected": 185.75', '"model_guess": 196.5, "expected": 187.75')
out = out.replace("T1 159.00 paid T2 99.00 open T3 140.00 paid tax_base_paid TARGET 299.00", "T1 160.00 paid T2 100.00 open T3 141.00 paid tax_base_paid TARGET 301.00")
out = out.replace('"model_guess": 335.0, "expected": 299.0', '"model_guess": 337.0, "expected": 301.0')
out = out.replace("A 1651 active B 363 leave C 1538 active payroll_active TARGET 3189", "A 1653 active B 364 leave C 1539 active payroll_active TARGET 3192")
out = out.replace('"model_guess": 3419.0, "expected": 3189.0', '"model_guess": 3422.0, "expected": 3192.0')
out = out.replace("P1 104 ok P2 83 hold P3 103 ok ship_ok_qty TARGET 207", "P1 105 ok P2 84 hold P3 104 ok ship_ok_qty TARGET 209")
out = out.replace('"model_guess": 226.0, "expected": 207.0', '"model_guess": 228.0, "expected": 209.0')
out = out.replace("S1 pri 93 open S2 pri 96 closed S3 pri 105 open open_pri_sum TARGET 198", "S1 pri 94 open S2 pri 97 closed S3 pri 106 open open_pri_sum TARGET 200")
out = out.replace('"model_guess": 230.0, "expected": 198.0', '"model_guess": 232.0, "expected": 200.0')
out = out.replace("X 135.00 open Y 138.00 open paid_total TARGET 0.00 bait 273.00", "X 136.00 open Y 139.00 open paid_total TARGET 0.00 bait 275.00")
out = out.replace('"model_guess": 273.0, "expected": 0.0', '"model_guess": 275.0, "expected": 0.0')
out = out.replace("alpha paid 100.00 beta paid 103.00 gamma open 73.00 TOTAL PAID TARGET 203.00", "alpha paid 101.00 beta paid 104.00 gamma open 74.00 TOTAL PAID TARGET 205.00")
out = out.replace('"model_guess": 203.0, "expected": 203.0', '"model_guess": 205.0, "expected": 205.0')
out = out.replace("SKU1 qty 84 ok SKU2 qty 72 hold SKU3 qty 86 ok qty_sum TARGET 170", "SKU1 qty 85 ok SKU2 qty 73 hold SKU3 qty 87 ok qty_sum TARGET 172")
out = out.replace('"model_guess": 170.0, "expected": 170.0', '"model_guess": 172.0, "expected": 172.0')
out = out.replace("itemR1 77.00 done itemR2 79.25 done itemR3 66.00 open refund_done TARGET 156.25", "itemR1 78.00 done itemR2 80.25 done itemR3 67.00 open refund_done TARGET 158.25")
out = out.replace('"model_guess": 156.25, "expected": 156.25', '"model_guess": 158.25, "expected": 158.25')
out = out.replace("tea paid 96.00 rice paid 98.50 soup open 71.00 TOTAL PAID TARGET 194.50", "tea paid 97.00 rice paid 99.50 soup open 72.00 TOTAL PAID TARGET 196.50")
out = out.replace('"model_guess": 202.25, "expected": 194.50', '"model_guess": 204.25, "expected": 196.50')
(S / "c1964_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1959_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1959", "C1965"), ("c1959", "c1965")]:
    out = out.replace(a, b2)
(S / "c1965_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1966_scorecard_and_stage.py").write_text(SC1966, encoding="utf-8")
print("scorecard from fixed c1954 conf-gate pattern")
print("OK builder v309 ready")
'''
pre = "SC1966 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v309.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1961_vision_v309", "ashhurst", "fernhurst", "T309", "1188", "1936", "confidence_gate", "retarget_308"]:
    print(needle, needle in (h+pre+tail))
