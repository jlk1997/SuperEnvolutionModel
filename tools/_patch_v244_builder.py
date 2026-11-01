from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v243.py").read_text(encoding="utf-8")

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
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*hurst ; stack mid-band", "*mere ; stack mid-band"),
    ("T243", "T244"), ("TR243", "TR244"), ("HO243", "HO244"),
    ("NEW243", "NEW244"),
    ("V243", "V244"), ("v243", "v244"),
    ("_v243_themes.json", "_v244_themes.json"),
    ("_v242_themes.json", "_v243_themes.json"),
    ("OLD242", "OLD243"),
    ("vision_images_v243", "vision_images_v244"),
    ("VL_GATE_V243", "VL_GATE_V244"), ("vl_gate_v243", "vl_gate_v244"),
    ("C1565", "C1571"), ("c1565", "c1571"),
    ("C1566", "C1572"), ("c1566", "c1572"),
    ("C1567", "C1573"), ("c1567", "c1573"),
    ("_v243c1565", "_v244c1571"),
    ("Harder than V241", "Harder than V242"),
    ("harder than V241", "harder than V242"),
    ("NEW themes vs V241:", "NEW themes vs V242:"),
    ("kept on V243", "kept on V244"),
    ("V243 keeps floor", "V244 keeps floor"),
    ("C1565 design+fixtures; no VL claim", "C1571 design+fixtures; no VL claim"),
    ("retarget_242", "retarget_243"),
    ("*hurst", "*mere"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHMERE bait 156.66", "ASHMERE bait 157.67")
b = b.replace("CEDARH bait 158.68", "CEDARM bait 159.69")
b = b.replace("DAWNH ghost 81.81", "DAWNM ghost 82.82")
b = b.replace("GLENH bait 151.61", "GLENM bait 152.62")
b = b.replace("JADEH bait 142.52", "JADEM bait 143.53")
b = b.replace("NETHERH bait 159.69", "NETHERM bait 160.70")

# Money bump; stack hold ~1180 (<=1196); HO refund avoid 1830/1560
TR = '''TR244 = [
    [2086.0, 2103.5, 1830.0],[840, 760, 820],[2009.0, 2038.25, 1810.0],[2142.0, 2159.0, 1900.0],
    [2204.0, 2228.0, 1870.0],[1928, 1944, 1828],[480.0, 520.0, 740.0],[2052.0, 2083.75, 1834.0],
    [840.0, 760.0, 820.0],[2119.0, 2107.0, 1831.0],[1,1,0],[0,0,0],
    [2185.0, 2206.5, 1856.0],[1,0,0],[1180, 1172, 1152],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
# Wait - TR paid has c=1830.0 which is BAN! Fix c to 1832.0
TR = '''TR244 = [
    [2086.0, 2103.5, 1832.0],[840, 760, 820],[2009.0, 2038.25, 1810.0],[2142.0, 2159.0, 1900.0],
    [2204.0, 2228.0, 1870.0],[1928, 1944, 1828],[480.0, 520.0, 740.0],[2052.0, 2083.75, 1834.0],
    [840.0, 760.0, 820.0],[2119.0, 2107.0, 1831.0],[1,1,0],[0,0,0],
    [2185.0, 2206.5, 1856.0],[1,0,0],[1180, 1172, 1152],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO244 = [
    [1890.0, 1902.75, 1751.0],[740, 780, 820],[1833.0, 1847.5, 1726.0],[1963.0, 1979.0, 1780.0],
    [2004.0, 2020.0, 1775.0],[1798, 1812, 1744],[360.0, 400.0, 730.0],[1874.0, 1895.75, 1751.0],
    [780.0, 740.0, 820.0],[1921.0, 1907.0, 1746.0],[1,1,0],[0,0,0],
    [1956.0, 1971.5, 1761.0],[1,0,0],[1172, 1167, 1160],[1186, 1180, 1168],[1,0,0],[1176, 1170, 1149],
]'''
b = re.sub(r'TR244\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO244\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')
assert 1180 <= 1196

idx = b.find('# V243 knife = confidence-gate')
if idx < 0:
    idx = b.find('out = (S / "c1556_confidence_gate_stretch.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V244 knife = product-U2C (alternating; V243 was conf-gate)
out = (S / "c1562_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1562", "C1574"), ("c1562", "c1574"),
    ("product_u2c_c1562", "product_u2c_c1574"),
    ("vs C1550", "vs C1562"),
]:
    out = out.replace(a, b2)
(S / "c1574_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1569_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1569", "C1575"), ("c1569", "c1575")]:
    out = out.replace(a, b2)
(S / "c1575_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1564_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1564", "C1576"), ("c1564", "c1576"),
    ("C1562", "C1574"), ("c1562", "c1574"),
    ("C1563", "C1575"), ("c1563", "c1575"),
    ("C1560", "C1572"), ("c1560", "c1572"),
    ("C1561", "C1573"), ("c1561", "c1573"),
    ("V242", "V244"), ("v242", "v244"),
    ("STAGE_ANT_C1564", "STAGE_ANT_C1576"),
    ("*ford", "*mere"),
]:
    out = out.replace(a, b2)
(S / "c1576_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v244 ready")
'''
(ROOT / "tools/_build_v244.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1571_vision_v244", "c1572_vision_v244", "c1573_vision_v244", "ashmere", "T244", "1180"]:
    print(needle, needle in (head+tail))
