from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v245.py").read_text(encoding="utf-8")

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
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*vale ; stack mid-band", "*croft ; stack mid-band"),
    ("T245", "T246"), ("TR245", "TR246"), ("HO245", "HO246"),
    ("NEW245", "NEW246"),
    ("V245", "V246"), ("v245", "v246"),
    ("_v245_themes.json", "_v246_themes.json"),
    ("_v244_themes.json", "_v245_themes.json"),
    ("OLD244", "OLD245"),
    ("vision_images_v245", "vision_images_v246"),
    ("VL_GATE_V245", "VL_GATE_V246"), ("vl_gate_v245", "vl_gate_v246"),
    ("C1577", "C1583"), ("c1577", "c1583"),
    ("C1578", "C1584"), ("c1578", "c1584"),
    ("C1579", "C1585"), ("c1579", "c1585"),
    ("_v245c1577", "_v246c1583"),
    ("Harder than V243", "Harder than V244"),
    ("harder than V243", "harder than V244"),
    ("NEW themes vs V243:", "NEW themes vs V244:"),
    ("kept on V245", "kept on V246"),
    ("V245 keeps floor", "V246 keeps floor"),
    ("C1577 design+fixtures; no VL claim", "C1583 design+fixtures; no VL claim"),
    ("retarget_244", "retarget_245"),
    ("*vale", "*croft"),
]
for a, c in pairs:
    b = b.replace(a, c)

b = b.replace("ASHCROFT bait 158.68", "ASHCROFT bait 159.69")
b = b.replace("CEDARV bait 160.70", "CEDARC bait 161.71")
b = b.replace("DAWNV ghost 83.83", "DAWNC ghost 84.84")
b = b.replace("GLENV bait 153.63", "GLENC bait 154.64")
b = b.replace("JADEV bait 144.54", "JADEC bait 145.55")
b = b.replace("NETHERV bait 161.71", "NETHERC bait 162.72")

TR = '''TR246 = [
    [2122.0, 2139.5, 1864.0],[840, 760, 820],[2045.0, 2074.25, 1842.0],[2178.0, 2195.0, 1932.0],
    [2240.0, 2264.0, 1902.0],[1960, 1976, 1860],[480.0, 520.0, 740.0],[2088.0, 2119.75, 1866.0],
    [840.0, 760.0, 820.0],[2155.0, 2143.0, 1863.0],[1,1,0],[0,0,0],
    [2221.0, 2242.5, 1888.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
# HO ship a was 1830 -> 1832
HO = '''HO246 = [
    [1922.0, 1934.75, 1783.0],[740, 780, 820],[1865.0, 1879.5, 1758.0],[1995.0, 2011.0, 1812.0],
    [2036.0, 2052.0, 1807.0],[1832, 1844, 1776],[360.0, 400.0, 730.0],[1906.0, 1927.75, 1783.0],
    [780.0, 740.0, 820.0],[1953.0, 1939.0, 1778.0],[1,1,0],[0,0,0],
    [1988.0, 2003.5, 1793.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
b = re.sub(r'TR246\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO246\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')
assert 1188 <= 1196

idx = b.find('# V245 knife = confidence-gate')
if idx < 0:
    idx = b.find('out = (S / "c1568_confidence_gate_stretch.py")')
    if idx < 0:
        raise SystemExit('knife not found')
    idx = b.rfind('\n', 0, b.rfind('\n', 0, idx)) + 1

head = b[:idx]
tail = r'''# V246 knife = product-U2C (alternating; V245 was conf-gate)
out = (S / "c1574_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1574", "C1586"), ("c1574", "c1586"),
    ("product_u2c_c1574", "product_u2c_c1586"),
    ("vs C1562", "vs C1574"),
]:
    out = out.replace(a, b2)
(S / "c1586_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1581_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1581", "C1587"), ("c1581", "c1587")]:
    out = out.replace(a, b2)
(S / "c1587_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1576_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1576", "C1588"), ("c1576", "c1588"),
    ("C1574", "C1586"), ("c1574", "c1586"),
    ("C1575", "C1587"), ("c1575", "c1587"),
    ("C1572", "C1584"), ("c1572", "c1584"),
    ("C1573", "C1585"), ("c1573", "c1585"),
    ("V244", "V246"), ("v244", "v246"),
    ("STAGE_ANT_C1576", "STAGE_ANT_C1588"),
    ("*mere", "*croft"),
]:
    out = out.replace(a, b2)
(S / "c1588_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v246 ready")
'''
(ROOT / "tools/_build_v246.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head)+len(tail))
