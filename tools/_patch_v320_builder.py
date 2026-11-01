from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v319.py").read_text(encoding="utf-8")
idx0 = b0.find('# V319 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2026 = " in head0:
    head0 = head0[:head0.find("SC2026 = ")]

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
    ("T319", "T320"), ("TR319", "TR320"), ("HO319", "HO320"),
    ("NEW319", "NEW320"),
    ("V319", "V320"), ("v319", "v320"),
    ("_v319_themes.json", "_v320_themes.json"),
    ("_v318_themes.json", "_v319_themes.json"),
    ("OLD318", "OLD319"),
    ("vision_images_v319", "vision_images_v320"),
    ("VL_GATE_V319", "VL_GATE_V320"), ("vl_gate_v319", "vl_gate_v320"),
    ("C2021", "C2027"), ("c2021", "c2027"),
    ("C2022", "C2028"), ("c2022", "c2028"),
    ("C2023", "C2029"), ("c2023", "c2029"),
    ("_v319c2021", "_v320c2027"),
    ("Harder than V317", "Harder than V318"),
    ("harder than V317", "harder than V318"),
    ("NEW themes vs V317:", "NEW themes vs V318:"),
    ("kept on V319", "kept on V320"),
    ("V319 keeps floor", "V320 keeps floor"),
    ("C2021 design+fixtures; no VL claim", "C2027 design+fixtures; no VL claim"),
    ("retarget_318", "retarget_319"),
    ("*ford", "*hurst"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFORD bait 232.42", "ASHHURST bait 233.43")
h = h.replace("CEDARF bait 234.44", "CEDARH bait 235.45")
h = h.replace("DAWNF ghost 157.67", "DAWNH ghost 158.68")
h = h.replace("GLENF bait 227.37", "GLENH bait 228.38")
h = h.replace("JADEF bait 218.28", "JADEH bait 219.29")
h = h.replace("NETHERF bait 235.45", "NETHERH bait 236.46")

TR = '''TR320 = [
    [2304.0, 2321.5, 2044.0],[840, 760, 820],[2227.0, 2256.25, 2022.0],[2360.0, 2377.0, 2112.0],
    [2422.0, 2446.0, 2082.0],[2140, 2156, 2040],[490.0, 530.0, 760.0],[2270.0, 2301.75, 2046.0],
    [840.0, 760.0, 820.0],[2337.0, 2325.0, 2043.0],[1,1,0],[0,0,0],
    [2403.0, 2424.5, 2068.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO320 = [
    [2102.0, 2114.75, 1963.0],[640, 660, 820],[2045.0, 2059.5, 1938.0],[2175.0, 2191.0, 1994.0],
    [2216.0, 2232.0, 1987.0],[1998, 2010, 1958],[420.0, 460.0, 740.0],[2086.0, 2107.75, 1963.0],
    [740.0, 780.0, 820.0],[2133.0, 2119.0, 1960.0],[1,1,0],[0,0,0],
    [2168.0, 2183.5, 1973.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR320\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO320\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2020_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2020", "C2032"), ("c2020", "c2032"),
    ("C2018", "C2030"), ("c2018", "c2030"),
    ("C2019", "C2031"), ("c2019", "c2031"),
    ("C2016", "C2028"), ("c2016", "c2028"),
    ("C2017", "C2029"), ("c2017", "c2029"),
    ("C2012", "C2024"), ("c2012", "c2024"),
    ("C2015", "C2027"), ("c2015", "c2027"),
    ("V318", "V320"), ("v318", "v320"),
    ("STAGE_ANT_C2020", "STAGE_ANT_C2032"),
    ("*dale", "*hurst"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V320 knife = product-U2C (alternating; V319 was confidence-gate)
out = (S / "c2018_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2018", "C2030"), ("c2018", "c2030"),
    ("C2006", "C2030"), ("c2006", "c2030"),
    ("product_u2c_cost_c2018", "product_u2c_cost_c2030"),
    ("u2c_v203", "u2c_v204"),
    ("u2c_c2018", "u2c_c2030"),
]:
    out = out.replace(a, b2)
(S / "c2030_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2018")

out = (S / "c2025_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2025", "C2031"), ("c2025", "c2031")]:
    out = out.replace(a, b2)
(S / "c2031_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2032_scorecard_and_stage.py").write_text(SC2032, encoding="utf-8")
print("scorecard from fixed c2020 product-U2C pattern")
print("OK builder v320 ready")
'''
pre = "SC2032 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v320.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2027_vision_v320", "ashhurst", "fernhurst", "T320", "1188", "1958", "product_u2c", "retarget_319"]:
    print(needle, needle in (h+pre+tail))
