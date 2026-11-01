from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v309.py").read_text(encoding="utf-8")
idx0 = b0.find('# V309 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1966 = " in head0:
    head0 = head0[:head0.find("SC1966 = ")]

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
    ("T309", "T310"), ("TR309", "TR310"), ("HO309", "HO310"),
    ("NEW309", "NEW310"),
    ("V309", "V310"), ("v309", "v310"),
    ("_v309_themes.json", "_v310_themes.json"),
    ("_v308_themes.json", "_v309_themes.json"),
    ("OLD308", "OLD309"),
    ("vision_images_v309", "vision_images_v310"),
    ("VL_GATE_V309", "VL_GATE_V310"), ("vl_gate_v309", "vl_gate_v310"),
    ("C1961", "C1967"), ("c1961", "c1967"),
    ("C1962", "C1968"), ("c1962", "c1968"),
    ("C1963", "C1969"), ("c1963", "c1969"),
    ("_v309c1961", "_v310c1967"),
    ("Harder than V307", "Harder than V308"),
    ("harder than V307", "harder than V308"),
    ("NEW themes vs V307:", "NEW themes vs V308:"),
    ("kept on V309", "kept on V310"),
    ("V309 keeps floor", "V310 keeps floor"),
    ("C1961 design+fixtures; no VL claim", "C1967 design+fixtures; no VL claim"),
    ("retarget_308", "retarget_309"),
    ("*hurst", "*mere"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHURST bait 222.32", "ASHMERE bait 223.33")
h = h.replace("CEDARH bait 224.34", "CEDARM bait 225.35")
h = h.replace("DAWNH ghost 147.57", "DAWNM ghost 148.58")
h = h.replace("GLENH bait 217.27", "GLENM bait 218.28")
h = h.replace("JADEH bait 208.18", "JADEM bait 209.19")
h = h.replace("NETHERH bait 225.35", "NETHERM bait 226.36")

TR = '''TR310 = [
    [2284.0, 2301.5, 2024.0],[840, 760, 820],[2207.0, 2236.25, 2002.0],[2340.0, 2357.0, 2092.0],
    [2402.0, 2426.0, 2062.0],[2120, 2136, 2020],[490.0, 530.0, 760.0],[2250.0, 2281.75, 2026.0],
    [840.0, 760.0, 820.0],[2317.0, 2305.0, 2023.0],[1,1,0],[0,0,0],
    [2383.0, 2404.5, 2048.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO310 = [
    [2082.0, 2094.75, 1943.0],[640, 660, 820],[2025.0, 2039.5, 1918.0],[2155.0, 2171.0, 1974.0],
    [2196.0, 2212.0, 1967.0],[1978, 1990, 1938],[420.0, 460.0, 740.0],[2066.0, 2087.75, 1943.0],
    [740.0, 780.0, 820.0],[2113.0, 2099.0, 1940.0],[1,1,0],[0,0,0],
    [2148.0, 2163.5, 1953.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR310\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO310\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c1960_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1960", "C1972"), ("c1960", "c1972"),
    ("C1958", "C1970"), ("c1958", "c1970"),
    ("C1959", "C1971"), ("c1959", "c1971"),
    ("C1956", "C1968"), ("c1956", "c1968"),
    ("C1957", "C1969"), ("c1957", "c1969"),
    ("C1952", "C1964"), ("c1952", "c1964"),
    ("C1955", "C1967"), ("c1955", "c1967"),
    ("V308", "V310"), ("v308", "v310"),
    ("STAGE_ANT_C1960", "STAGE_ANT_C1972"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V310 knife = product-U2C (alternating; V309 was confidence-gate)
out = (S / "c1958_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1958", "C1970"), ("c1958", "c1970"),
    ("C1946", "C1970"), ("c1946", "c1970"),
    ("product_u2c_cost_c1958", "product_u2c_cost_c1970"),
    ("u2c_v198", "u2c_v199"),
    ("u2c_c1958", "u2c_c1970"),
]:
    out = out.replace(a, b2)
(S / "c1970_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1958")

out = (S / "c1965_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1965", "C1971"), ("c1965", "c1971")]:
    out = out.replace(a, b2)
(S / "c1971_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1972_scorecard_and_stage.py").write_text(SC1972, encoding="utf-8")
print("scorecard from fixed c1960 product-U2C pattern")
print("OK builder v310 ready")
'''
pre = "SC1972 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v310.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1967_vision_v310", "ashmere", "fernmere", "T310", "1188", "1938", "product_u2c", "retarget_309"]:
    print(needle, needle in (h+pre+tail))
