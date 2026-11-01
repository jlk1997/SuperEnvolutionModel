from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v249.py").read_text(encoding="utf-8")
idx0 = b0.find('# V249 knife = confidence-gate')
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
# Note: fernfen is intentional (theme cycle *fen); avoid *b collapse
pairs = [
    ("*moor ; stack mid-band", "*fen ; stack mid-band"),
    ("T249", "T250"), ("TR249", "TR250"), ("HO249", "HO250"),
    ("NEW249", "NEW250"),
    ("V249", "V250"), ("v249", "v250"),
    ("_v249_themes.json", "_v250_themes.json"),
    ("_v248_themes.json", "_v249_themes.json"),
    ("OLD248", "OLD249"),
    ("vision_images_v249", "vision_images_v250"),
    ("VL_GATE_V249", "VL_GATE_V250"), ("vl_gate_v249", "vl_gate_v250"),
    ("C1601", "C1607"), ("c1601", "c1607"),
    ("C1602", "C1608"), ("c1602", "c1608"),
    ("C1603", "C1609"), ("c1603", "c1609"),
    ("_v249c1601", "_v250c1607"),
    ("Harder than V247", "Harder than V248"),
    ("harder than V247", "harder than V248"),
    ("NEW themes vs V247:", "NEW themes vs V248:"),
    ("kept on V249", "kept on V250"),
    ("V249 keeps floor", "V250 keeps floor"),
    ("C1601 design+fixtures; no VL claim", "C1607 design+fixtures; no VL claim"),
    ("retarget_248", "retarget_249"),
    ("*moor", "*fen"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFEN bait 162.72", "ASHFEN bait 163.73")
h = h.replace("CEDARM bait 164.74", "CEDARF bait 165.75")
h = h.replace("DAWNM ghost 87.87", "DAWNF ghost 88.88")
h = h.replace("GLENM bait 157.67", "GLENF bait 158.68")
h = h.replace("JADEM bait 148.58", "JADEF bait 149.59")
h = h.replace("NETHERM bait 165.75", "NETHERF bait 166.76")

TR = '''TR250 = [
    [2146.0, 2163.5, 1886.0],[840, 760, 820],[2069.0, 2098.25, 1864.0],[2202.0, 2219.0, 1954.0],
    [2264.0, 2288.0, 1924.0],[1982, 1998, 1882],[480.0, 520.0, 740.0],[2112.0, 2143.75, 1888.0],
    [840.0, 760.0, 820.0],[2179.0, 2167.0, 1885.0],[1,1,0],[0,0,0],
    [2245.0, 2266.5, 1910.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO250 = [
    [1944.0, 1956.75, 1805.0],[740, 780, 820],[1887.0, 1901.5, 1780.0],[2017.0, 2033.0, 1836.0],
    [2058.0, 2074.0, 1829.0],[1840, 1852, 1798],[360.0, 400.0, 730.0],[1928.0, 1949.75, 1805.0],
    [780.0, 740.0, 820.0],[1975.0, 1961.0, 1800.0],[1,1,0],[0,0,0],
    [2010.0, 2025.5, 1815.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR250\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO250\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

src = "c1598_product_u2c_cost.py"
if not (ROOT / "scripts" / src).exists():
    src = "c1586_product_u2c_cost.py"
sc_src = "c1600_scorecard_and_stage.py"

tail = f'''# V250 knife = product-U2C (alternating; V249 was confidence-gate)
out = (S / "{src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1598", "C1610"), ("c1598", "c1610"),
    ("C1586", "C1610"), ("c1586", "c1610"),
    ("C1466", "C1610"), ("c1466", "c1610"),
]:
    out = out.replace(a, b2)
(S / "c1610_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{src}")

out = (S / "c1605_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1605", "C1611"), ("c1605", "c1611")]:
    out = out.replace(a, b2)
(S / "c1611_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1600", "C1612"), ("c1600", "c1612"),
    ("C1598", "C1610"), ("c1598", "c1610"),
    ("C1599", "C1611"), ("c1599", "c1611"),
    ("C1596", "C1608"), ("c1596", "c1608"),
    ("C1597", "C1609"), ("c1597", "c1609"),
    ("V248", "V250"), ("v248", "v250"),
    ("STAGE_ANT_C1600", "STAGE_ANT_C1612"),
    ("*wick", "*fen"),
]:
    out = out.replace(a, b2)
(S / "c1612_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v250 ready")
'''
(ROOT / "tools/_build_v250.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
# warn if fernfen accidentally became something bad / *b collapse
if "fernfen" not in h and "FERNFEN" not in h:
    print("WARN fernfen missing")
else:
    print("fernfen ok")
for needle in ["c1607_vision_v250", "ashfen", "T250", "1188", "1836", "product_u2c"]:
    print(needle, needle in (h+tail))
