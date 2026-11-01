from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
src = (ROOT / "tools/_build_v229.py").read_text(encoding="utf-8")
b = src

# brook -> dale (longer first)
theme_pairs = [
    ("netherbrook", "netherdale"), ("NETHERBROOK", "NETHERDALE"),
    ("cedarbrook", "cedardale"), ("CEDARBROOK", "CEDARDALE"),
    ("dawnbrook", "dawndale"), ("DAWNBROOK", "DAWNDALE"),
    ("fernbrook", "ferndale"), ("FERNBROOK", "FERNDALE"),
    ("glenbrook", "glendale"), ("GLENBROOK", "GLENDALE"),
    ("hazebrook", "hazedale"), ("HAZEBROOK", "HAZEDALE"),
    ("jadebrook", "jadedale"), ("JADEBROOK", "JADEDALE"),
    ("knotbrook", "knotdale"), ("KNOTBROOK", "KNOTDALE"),
    ("lakebrook", "lakedale"), ("LAKEBROOK", "LAKEDALE"),
    ("mossbrook", "mossdale"), ("MOSSBROOK", "MOSSDALE"),
    ("pinebrook", "pinedale"), ("PINEBROOK", "PINEDALE"),
    ("quillbrook", "quilldale"), ("QUILLBROOK", "QUILLDALE"),
    ("reedbrook", "reeddale"), ("REEDBROOK", "REEDDALE"),
    ("stonebrook", "stonedale"), ("STONEBROOK", "STONEDALE"),
    ("ashbrook", "ashdale"), ("ASHBROOK", "ASHDALE"),
    ("elmbrook", "elmdale"), ("ELMBROOK", "ELMDALE"),
    ("inkbrook", "inkdale"), ("INKBROOK", "INKDALE"),
    ("oakbrook", "oakdale"), ("OAKBROOK", "OAKDALE"),
]
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*brook ; stack mid-band", "*dale ; stack mid-band"),
    ("T229", "T230"), ("TR229", "TR230"), ("HO229", "HO230"),
    ("NEW229", "NEW230"),
    ("V229", "V230"), ("v229", "v230"),
    ("_v229_themes.json", "_v230_themes.json"),
    ("_v228_themes.json", "_v229_themes.json"),
    ("OLD228", "OLD229"),
    ("vision_images_v229", "vision_images_v230"),
    ("VL_GATE_V229", "VL_GATE_V230"), ("vl_gate_v229", "vl_gate_v230"),
    ("C1481", "C1487"), ("c1481", "c1487"),
    ("C1482", "C1488"), ("c1482", "c1488"),
    ("C1483", "C1489"), ("c1483", "c1489"),
    ("_v229c1481", "_v230c1487"),
    ("Harder than V227", "Harder than V228"),
    ("harder than V227", "harder than V228"),
    ("NEW themes vs V227:", "NEW themes vs V228:"),
    ("kept on V229", "kept on V230"),
    ("V229 keeps floor", "V230 keeps floor"),
    ("C1481 design+fixtures; no VL claim", "C1487 design+fixtures; no VL claim"),
    ("retarget_228", "retarget_229"),
    ("*brook", "*dale"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHDALE bait 142.52", "ASHDALE bait 143.53")
b = b.replace("CEDARB bait 144.54", "CEDARD bait 145.55")
b = b.replace("DAWNB ghost 67.67", "DAWND ghost 68.68")
b = b.replace("GLENB bait 137.47", "GLEND bait 138.48")
b = b.replace("JADEB bait 128.38", "JADED bait 129.39")
b = b.replace("NETHERB bait 145.55", "NETHERD bait 146.56")

TR = '''TR230 = [
    [1834.0, 1851.5, 1606.0],[840, 760, 820],[1757.0, 1786.25, 1586.0],[1890.0, 1907.0, 1676.0],
    [1952.0, 1976.0, 1646.0],[1704, 1720, 1604],[480.0, 520.0, 740.0],[1800.0, 1831.75, 1610.0],
    [840.0, 760.0, 820.0],[1867.0, 1855.0, 1607.0],[1,1,0],[0,0,0],
    [1933.0, 1954.5, 1632.0],[1,0,0],[1168, 1160, 1140],[1184, 1168, 748],[1,0,0],[1200, 1184, 1162],
]'''
HO = '''HO230 = [
    [1666.0, 1678.75, 1527.0],[740, 780, 820],[1609.0, 1622.5, 1502.0],[1739.0, 1755.0, 1556.0],
    [1780.0, 1796.0, 1551.0],[1574, 1588, 1520],[360.0, 400.0, 730.0],[1650.0, 1671.75, 1527.0],
    [780.0, 740.0, 820.0],[1697.0, 1683.0, 1522.0],[1,1,0],[0,0,0],
    [1732.0, 1747.5, 1537.0],[1,0,0],[1156, 1151, 1144],[1170, 1164, 1152],[1,0,0],[1180, 1174, 1153],
]'''
b = re.sub(r'TR230\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO230\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

# Replace conf-gate knife with product-U2C
idx = b.find('# V229 knife = confidence-gate')
if idx < 0:
    idx = b.find('# V230 knife = confidence-gate')
if idx < 0:
    idx = b.find('out = (S / "c1472_confidence_gate_stretch.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V230 knife = product-U2C (alternating; V229 was conf-gate)
out = (S / "c1478_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1478", "C1490"), ("c1478", "c1490"),
    ("product_u2c_c1478", "product_u2c_c1490"),
    ("vs C1466", "vs C1478"),
]:
    out = out.replace(a, b2)
(S / "c1490_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1485_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1485", "C1491"), ("c1485", "c1491")]:
    out = out.replace(a, b2)
(S / "c1491_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1480_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1480", "C1492"), ("c1480", "c1492"),
    ("C1478", "C1490"), ("c1478", "c1490"),
    ("C1479", "C1491"), ("c1479", "c1491"),
    ("C1476", "C1488"), ("c1476", "c1488"),
    ("C1477", "C1489"), ("c1477", "c1489"),
    ("V228", "V230"), ("v228", "v230"),
    ("STAGE_ANT_C1480", "STAGE_ANT_C1492"),
    ("*fen", "*dale"),
]:
    out = out.replace(a, b2)
(S / "c1492_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v230 ready")
'''
(ROOT / "tools/_build_v230.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1487_vision_v230", "c1488_vision_v230", "c1489_vision_v230", "ashdale", "T230"]:
    print(needle, needle in (head+tail))
