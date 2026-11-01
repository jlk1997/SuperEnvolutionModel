from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v239.py").read_text(encoding="utf-8")

theme_pairs = [
    ("netherfen", "netherbrook"), ("NETHERFEN", "NETHERBROOK"),
    ("cedarfen", "cedarbrook"), ("CEDARFEN", "CEDARBROOK"),
    ("dawnfen", "dawnbrook"), ("DAWNFEN", "DAWNBROOK"),
    ("fernfen", "fernbrook"), ("FERNFEN", "FERNBROOK"),
    ("glenfen", "glenbrook"), ("GLENFEN", "GLENBROOK"),
    ("hazefen", "hazebrook"), ("HAZEFEN", "HAZEBROOK"),
    ("jadefen", "jadebrook"), ("JADEFEN", "JADEBROOK"),
    ("knotfen", "knotbrook"), ("KNOTFEN", "KNOTBROOK"),
    ("lakefen", "lakebrook"), ("LAKEFEN", "LAKEBROOK"),
    ("mossfen", "mossbrook"), ("MOSSFEN", "MOSSBROOK"),
    ("pinefen", "pinebrook"), ("PINEFEN", "PINEBROOK"),
    ("quillfen", "quillbrook"), ("QUILLFEN", "QUILLBROOK"),
    ("reedfen", "reedbrook"), ("REEDFEN", "REEDBROOK"),
    ("stonefen", "stonebrook"), ("STONEFEN", "STONEBROOK"),
    ("ashfen", "ashbrook"), ("ASHFEN", "ASHBROOK"),
    ("elmfen", "elmbrook"), ("ELMFEN", "ELMBROOK"),
    ("inkfen", "inkbrook"), ("INKFEN", "INKBROOK"),
    ("oakfen", "oakbrook"), ("OAKFEN", "OAKBROOK"),
]
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*fen ; stack mid-band", "*brook ; stack mid-band"),
    ("T239", "T240"), ("TR239", "TR240"), ("HO239", "HO240"),
    ("NEW239", "NEW240"),
    ("V239", "V240"), ("v239", "v240"),
    ("_v239_themes.json", "_v240_themes.json"),
    ("_v238_themes.json", "_v239_themes.json"),
    ("OLD238", "OLD239"),
    ("vision_images_v239", "vision_images_v240"),
    ("VL_GATE_V239", "VL_GATE_V240"), ("vl_gate_v239", "vl_gate_v240"),
    ("C1541", "C1547"), ("c1541", "c1547"),
    ("C1542", "C1548"), ("c1542", "c1548"),
    ("C1543", "C1549"), ("c1543", "c1549"),
    ("_v239c1541", "_v240c1547"),
    ("Harder than V237", "Harder than V238"),
    ("harder than V237", "harder than V238"),
    ("NEW themes vs V237:", "NEW themes vs V238:"),
    ("kept on V239", "kept on V240"),
    ("V239 keeps floor", "V240 keeps floor"),
    ("C1541 design+fixtures; no VL claim", "C1547 design+fixtures; no VL claim"),
    ("retarget_238", "retarget_239"),
    ("*fen", "*brook"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHBROOK bait 152.62", "ASHBROOK bait 153.63")
b = b.replace("CEDARF bait 154.64", "CEDARB bait 155.65")
b = b.replace("DAWNF ghost 77.77", "DAWNB ghost 78.78")
b = b.replace("GLENF bait 147.57", "GLENB bait 148.58")
b = b.replace("JADEF bait 138.48", "JADEB bait 139.49")
b = b.replace("NETHERF bait 155.65", "NETHERB bait 156.66")

# Money bump; stack STAY mid-band (p1<=1196)
TR = '''TR240 = [
    [2014.0, 2031.5, 1766.0],[840, 760, 820],[1937.0, 1966.25, 1746.0],[2070.0, 2087.0, 1836.0],
    [2132.0, 2156.0, 1806.0],[1864, 1880, 1764],[480.0, 520.0, 740.0],[1980.0, 2011.75, 1770.0],
    [840.0, 760.0, 820.0],[2047.0, 2035.0, 1767.0],[1,1,0],[0,0,0],
    [2113.0, 2134.5, 1792.0],[1,0,0],[1164, 1156, 1136],[1180, 1164, 748],[1,0,0],[1196, 1180, 1158],
]'''
HO = '''HO240 = [
    [1826.0, 1838.75, 1687.0],[740, 780, 820],[1769.0, 1782.5, 1662.0],[1899.0, 1915.0, 1716.0],
    [1940.0, 1956.0, 1711.0],[1734, 1748, 1680],[360.0, 400.0, 730.0],[1810.0, 1831.75, 1687.0],
    [780.0, 740.0, 820.0],[1857.0, 1843.0, 1682.0],[1,1,0],[0,0,0],
    [1892.0, 1907.5, 1697.0],[1,0,0],[1156, 1151, 1144],[1170, 1164, 1152],[1,0,0],[1180, 1174, 1153],
]'''
b = re.sub(r'TR240\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO240\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')
# stack p1 assert
assert 1164 <= 1196 and 1156 <= 1196

idx = b.find('# V239 knife = confidence-gate')
if idx < 0:
    idx = b.find('# V240 knife = confidence-gate')
if idx < 0:
    idx = b.find('out = (S / "c1532_confidence_gate_stretch.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V240 knife = product-U2C (alternating; V239 was conf-gate)
out = (S / "c1538_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1538", "C1550"), ("c1538", "c1550"),
    ("product_u2c_c1538", "product_u2c_c1550"),
    ("vs C1526", "vs C1538"),
]:
    out = out.replace(a, b2)
(S / "c1550_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1545_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1545", "C1551"), ("c1545", "c1551")]:
    out = out.replace(a, b2)
(S / "c1551_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1540_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1540", "C1552"), ("c1540", "c1552"),
    ("C1538", "C1550"), ("c1538", "c1550"),
    ("C1539", "C1551"), ("c1539", "c1551"),
    ("C1536", "C1548"), ("c1536", "c1548"),
    ("C1537", "C1549"), ("c1537", "c1549"),
    ("V238", "V240"), ("v238", "v240"),
    ("STAGE_ANT_C1540", "STAGE_ANT_C1552"),
    ("*moor", "*brook"),
]:
    out = out.replace(a, b2)
(S / "c1552_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v240 ready")
'''
(ROOT / "tools/_build_v240.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1547_vision_v240", "c1548_vision_v240", "c1549_vision_v240", "ashbrook", "T240", "1164"]:
    print(needle, needle in (head+tail))
