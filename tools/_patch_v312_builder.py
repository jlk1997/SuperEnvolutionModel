from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v311.py").read_text(encoding="utf-8")
idx0 = b0.find('# V311 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1978 = " in head0:
    head0 = head0[:head0.find("SC1978 = ")]

theme_pairs = [
    ("nethervale", "nethercroft"), ("NETHERVALE", "NETHERCROFT"),
    ("cedarvale", "cedarcroft"), ("CEDARVALE", "CEDARCROFT"),
    ("dawnvale", "dawncroft"), ("DAWNVALE", "DAWNCROFT"),
    ("fernvale", "ferncroft"), ("FERNVALE", "FERNCROFT"),
    ("glenvale", "glencroft"), ("GLENVALE", "GLENCROFT"),
    ("hazevale", "hazecroft"), ("HAZEVALE", "HAZECROFT"),
    ("jadevale", "jadecroft"), ("JADEVALE", "JADECROFT"),
    ("knotvale", "knotcroft"), ("KNOTVALE", "KNOTCROFT"),
    ("lakevale", "lakecroft"), ("LAKEVALE", "LAKECROFT"),
    ("mossvale", "mosscroft"), ("MOSSVALE", "MOSSCROFT"),
    ("pinevale", "pinecroft"), ("PINEVALE", "PINECROFT"),
    ("quillvale", "quillcroft"), ("QUILLVALE", "QUILLCROFT"),
    ("reedvale", "reedcroft"), ("REEDVALE", "REEDCROFT"),
    ("stonevale", "stonecroft"), ("STONEVALE", "STONECROFT"),
    ("ashvale", "ashcroft"), ("ASHVALE", "ASHCROFT"),
    ("elmvale", "elmcroft"), ("ELMVALE", "ELMCROFT"),
    ("inkvale", "inkcroft"), ("INKVALE", "INKCROFT"),
    ("oakvale", "oakcroft"), ("OAKVALE", "OAKCROFT"),
]
pairs = [
    ("*vale ; stack mid-band", "*croft ; stack mid-band"),
    ("T311", "T312"), ("TR311", "TR312"), ("HO311", "HO312"),
    ("NEW311", "NEW312"),
    ("V311", "V312"), ("v311", "v312"),
    ("_v311_themes.json", "_v312_themes.json"),
    ("_v310_themes.json", "_v311_themes.json"),
    ("OLD310", "OLD311"),
    ("vision_images_v311", "vision_images_v312"),
    ("VL_GATE_V311", "VL_GATE_V312"), ("vl_gate_v311", "vl_gate_v312"),
    ("C1973", "C1979"), ("c1973", "c1979"),
    ("C1974", "C1980"), ("c1974", "c1980"),
    ("C1975", "C1981"), ("c1975", "c1981"),
    ("_v311c1973", "_v312c1979"),
    ("Harder than V309", "Harder than V310"),
    ("harder than V309", "harder than V310"),
    ("NEW themes vs V309:", "NEW themes vs V310:"),
    ("kept on V311", "kept on V312"),
    ("V311 keeps floor", "V312 keeps floor"),
    ("C1973 design+fixtures; no VL claim", "C1979 design+fixtures; no VL claim"),
    ("retarget_310", "retarget_311"),
    ("*vale", "*croft"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHVALE bait 224.34", "ASHCROFT bait 225.35")
h = h.replace("CEDARV bait 226.36", "CEDARC bait 227.37")
h = h.replace("DAWNV ghost 149.59", "DAWNC ghost 150.60")
h = h.replace("GLENV bait 219.29", "GLENC bait 220.30")
h = h.replace("JADEV bait 210.20", "JADEC bait 211.21")
h = h.replace("NETHERV bait 227.37", "NETHERC bait 228.38")

TR = '''TR312 = [
    [2288.0, 2305.5, 2028.0],[840, 760, 820],[2211.0, 2240.25, 2006.0],[2344.0, 2361.0, 2096.0],
    [2406.0, 2430.0, 2066.0],[2124, 2140, 2024],[490.0, 530.0, 760.0],[2254.0, 2285.75, 2030.0],
    [840.0, 760.0, 820.0],[2321.0, 2309.0, 2027.0],[1,1,0],[0,0,0],
    [2387.0, 2408.5, 2052.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO312 = [
    [2086.0, 2098.75, 1947.0],[640, 660, 820],[2029.0, 2043.5, 1922.0],[2159.0, 2175.0, 1978.0],
    [2200.0, 2216.0, 1971.0],[1982, 1994, 1942],[420.0, 460.0, 740.0],[2070.0, 2091.75, 1947.0],
    [740.0, 780.0, 820.0],[2117.0, 2103.0, 1944.0],[1,1,0],[0,0,0],
    [2152.0, 2167.5, 1957.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR312\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO312\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c1972_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1972", "C1984"), ("c1972", "c1984"),
    ("C1970", "C1982"), ("c1970", "c1982"),
    ("C1971", "C1983"), ("c1971", "c1983"),
    ("C1968", "C1980"), ("c1968", "c1980"),
    ("C1969", "C1981"), ("c1969", "c1981"),
    ("C1964", "C1976"), ("c1964", "c1976"),
    ("C1967", "C1979"), ("c1967", "c1979"),
    ("V310", "V312"), ("v310", "v312"),
    ("STAGE_ANT_C1972", "STAGE_ANT_C1984"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V312 knife = product-U2C (alternating; V311 was confidence-gate)
out = (S / "c1970_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1970", "C1982"), ("c1970", "c1982"),
    ("C1958", "C1982"), ("c1958", "c1982"),
    ("product_u2c_cost_c1970", "product_u2c_cost_c1982"),
    ("u2c_v199", "u2c_v200"),
    ("u2c_c1970", "u2c_c1982"),
]:
    out = out.replace(a, b2)
(S / "c1982_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1970")

out = (S / "c1977_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1977", "C1983"), ("c1977", "c1983")]:
    out = out.replace(a, b2)
(S / "c1983_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1984_scorecard_and_stage.py").write_text(SC1984, encoding="utf-8")
print("scorecard from fixed c1972 product-U2C pattern")
print("OK builder v312 ready")
'''
pre = "SC1984 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v312.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1979_vision_v312", "ashcroft", "ferncroft", "T312", "1188", "1942", "product_u2c", "retarget_311"]:
    print(needle, needle in (h+pre+tail))
