from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v331.py").read_text(encoding="utf-8")
idx0 = b0.find('# V331 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2098 = " in head0:
    head0 = head0[:head0.find("SC2098 = ")]

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
    ("T331", "T332"), ("TR331", "TR332"), ("HO331", "HO332"),
    ("NEW331", "NEW332"),
    ("V331", "V332"), ("v331", "v332"),
    ("_v331_themes.json", "_v332_themes.json"),
    ("_v330_themes.json", "_v331_themes.json"),
    ("OLD330", "OLD331"),
    ("vision_images_v331", "vision_images_v332"),
    ("VL_GATE_V331", "VL_GATE_V332"), ("vl_gate_v331", "vl_gate_v332"),
    ("C2093", "C2099"), ("c2093", "c2099"),
    ("C2094", "C2100"), ("c2094", "c2100"),
    ("C2095", "C2101"), ("c2095", "c2101"),
    ("_v331c2093", "_v332c2099"),
    ("Harder than V329", "Harder than V330"),
    ("harder than V329", "harder than V330"),
    ("NEW themes vs V329:", "NEW themes vs V330:"),
    ("kept on V331", "kept on V332"),
    ("V331 keeps floor", "V332 keeps floor"),
    ("C2093 design+fixtures; no VL claim", "C2099 design+fixtures; no VL claim"),
    ("retarget_330", "retarget_331"),
    ("*hurst", "*mere"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHURST bait 244.54", "ASHMERE bait 245.55")
h = h.replace("CEDARH bait 246.56", "CEDARM bait 247.57")
h = h.replace("DAWNH ghost 169.79", "DAWNM ghost 170.80")
h = h.replace("GLENH bait 239.49", "GLENM bait 240.50")
h = h.replace("JADEH bait 230.40", "JADEM bait 231.41")
h = h.replace("NETHERH bait 247.57", "NETHERM bait 248.58")

# refund ~2250/2259.25 stay in 224x/225x (avoid 226x OCR 2↔6 trap)
TR = '''TR332 = [
    [2328.0, 2345.5, 2068.0],[840, 760, 820],[2250.0, 2259.25, 2045.0],[2384.0, 2401.0, 2136.0],
    [2446.0, 2470.0, 2106.0],[2164, 2180, 2064],[490.0, 530.0, 760.0],[2294.0, 2325.75, 2070.0],
    [840.0, 760.0, 820.0],[2361.0, 2349.0, 2067.0],[1,1,0],[0,0,0],
    [2427.0, 2448.5, 2092.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO332 = [
    [2126.0, 2138.75, 1987.0],[640, 660, 820],[2069.0, 2083.5, 1962.0],[2199.0, 2215.0, 2018.0],
    [2240.0, 2256.0, 2011.0],[2022, 2034, 1984],[420.0, 460.0, 740.0],[2110.0, 2131.75, 1987.0],
    [740.0, 780.0, 820.0],[2157.0, 2143.0, 1984.0],[1,1,0],[0,0,0],
    [2192.0, 2207.5, 1997.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR332\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO332\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

# product-U2C scorecard from V330 pattern (C2092), retarget to C2104 + prior CONF C2096
sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2104"), ("c2092", "c2104"),
    ("C2090", "C2102"), ("c2090", "c2102"),
    ("C2091", "C2103"), ("c2091", "c2103"),
    ("C2088", "C2100"), ("c2088", "c2100"),
    ("C2089", "C2101"), ("c2089", "c2101"),
    ("C2084", "C2096"), ("c2084", "c2096"),
    ("C2087", "C2099"), ("c2087", "c2099"),
    ("V330", "V332"), ("v330", "v332"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2104"),
    ("*ford", "*mere"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V332 knife = product-U2C (alternating; V331 was confidence-gate)
out = (S / "c2090_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2090", "C2102"), ("c2090", "c2102"),
    ("C2078", "C2102"), ("c2078", "c2102"),
    ("product_u2c_cost_c2090", "product_u2c_cost_c2102"),
    ("u2c_v209", "u2c_v210"),
    ("u2c_c2090", "u2c_c2102"),
]:
    out = out.replace(a, b2)
(S / "c2102_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2090")

out = (S / "c2097_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2097", "C2103"), ("c2097", "c2103")]:
    out = out.replace(a, b2)
(S / "c2103_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2104_scorecard_and_stage.py").write_text(SC2104, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v332 ready")
'''
pre = "SC2104 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v332.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2099_vision_v332", "ashmere", "fernmere", "T332", "1188", "1984", "product_u2c", "retarget_331", "2259.25"]:
    print(needle, needle in (h+pre+tail))
