from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v233.py").read_text(encoding="utf-8")

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
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*mere ; stack mid-band", "*vale ; stack mid-band"),
    ("T233", "T234"), ("TR233", "TR234"), ("HO233", "HO234"),
    ("NEW233", "NEW234"),
    ("V233", "V234"), ("v233", "v234"),
    ("_v233_themes.json", "_v234_themes.json"),
    ("_v232_themes.json", "_v233_themes.json"),
    ("OLD232", "OLD233"),
    ("vision_images_v233", "vision_images_v234"),
    ("VL_GATE_V233", "VL_GATE_V234"), ("vl_gate_v233", "vl_gate_v234"),
    ("C1505", "C1511"), ("c1505", "c1511"),
    ("C1506", "C1512"), ("c1506", "c1512"),
    ("C1507", "C1513"), ("c1507", "c1513"),
    ("_v233c1505", "_v234c1511"),
    ("Harder than V231", "Harder than V232"),
    ("harder than V231", "harder than V232"),
    ("NEW themes vs V231:", "NEW themes vs V232:"),
    ("kept on V233", "kept on V234"),
    ("V233 keeps floor", "V234 keeps floor"),
    ("C1505 design+fixtures; no VL claim", "C1511 design+fixtures; no VL claim"),
    ("retarget_232", "retarget_233"),
    ("*mere", "*vale"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHVALE bait 146.56", "ASHVALE bait 147.57")
b = b.replace("CEDARM bait 148.58", "CEDARV bait 149.59")
b = b.replace("DAWNM ghost 71.71", "DAWNV ghost 72.72")
b = b.replace("GLENM bait 141.51", "GLENV bait 142.52")
b = b.replace("JADEM bait 132.42", "JADEV bait 133.43")
b = b.replace("NETHERM bait 149.59", "NETHERV bait 150.60")

TR = '''TR234 = [
    [1906.0, 1923.5, 1670.0],[840, 760, 820],[1829.0, 1858.25, 1650.0],[1962.0, 1979.0, 1740.0],
    [2024.0, 2048.0, 1710.0],[1768, 1784, 1668],[480.0, 520.0, 740.0],[1872.0, 1903.75, 1674.0],
    [840.0, 760.0, 820.0],[1939.0, 1927.0, 1671.0],[1,1,0],[0,0,0],
    [2005.0, 2026.5, 1696.0],[1,0,0],[1184, 1176, 1156],[1200, 1184, 748],[1,0,0],[1216, 1200, 1178],
]'''
HO = '''HO234 = [
    [1730.0, 1742.75, 1591.0],[740, 780, 820],[1673.0, 1686.5, 1566.0],[1803.0, 1819.0, 1620.0],
    [1844.0, 1860.0, 1615.0],[1638, 1652, 1584],[360.0, 400.0, 730.0],[1714.0, 1735.75, 1591.0],
    [780.0, 740.0, 820.0],[1761.0, 1747.0, 1586.0],[1,1,0],[0,0,0],
    [1796.0, 1811.5, 1601.0],[1,0,0],[1172, 1167, 1160],[1186, 1180, 1168],[1,0,0],[1196, 1190, 1169],
]'''
b = re.sub(r'TR234\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO234\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

idx = b.find('# V233 knife = confidence-gate')
if idx < 0:
    idx = b.find('# V234 knife = confidence-gate')
if idx < 0:
    idx = b.find('out = (S / "c1496_confidence_gate_stretch.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V234 knife = product-U2C (alternating; V233 was conf-gate)
out = (S / "c1502_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1502", "C1514"), ("c1502", "c1514"),
    ("product_u2c_c1502", "product_u2c_c1514"),
    ("vs C1490", "vs C1502"),
]:
    out = out.replace(a, b2)
(S / "c1514_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1509_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1509", "C1515"), ("c1509", "c1515")]:
    out = out.replace(a, b2)
(S / "c1515_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1504_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1504", "C1516"), ("c1504", "c1516"),
    ("C1502", "C1514"), ("c1502", "c1514"),
    ("C1503", "C1515"), ("c1503", "c1515"),
    ("C1500", "C1512"), ("c1500", "c1512"),
    ("C1501", "C1513"), ("c1501", "c1513"),
    ("V232", "V234"), ("v232", "v234"),
    ("STAGE_ANT_C1504", "STAGE_ANT_C1516"),
    ("*hurst", "*vale"),
]:
    out = out.replace(a, b2)
(S / "c1516_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v234 ready")
'''
(ROOT / "tools/_build_v234.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
for needle in ["c1511_vision_v234", "c1512_vision_v234", "c1513_vision_v234", "ashvale", "T234"]:
    print(needle, needle in (head+tail))
