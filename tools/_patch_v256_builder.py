from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v255.py").read_text(encoding="utf-8")
idx0 = b0.find('# V255 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
pairs = [
    ("*mere ; stack mid-band", "*vale ; stack mid-band"),
    ("T255", "T256"), ("TR255", "TR256"), ("HO255", "HO256"),
    ("NEW255", "NEW256"),
    ("V255", "V256"), ("v255", "v256"),
    ("_v255_themes.json", "_v256_themes.json"),
    ("_v254_themes.json", "_v255_themes.json"),
    ("OLD254", "OLD255"),
    ("vision_images_v255", "vision_images_v256"),
    ("VL_GATE_V255", "VL_GATE_V256"), ("vl_gate_v255", "vl_gate_v256"),
    ("C1637", "C1643"), ("c1637", "c1643"),
    ("C1638", "C1644"), ("c1638", "c1644"),
    ("C1639", "C1645"), ("c1639", "c1645"),
    ("_v255c1637", "_v256c1643"),
    ("Harder than V253", "Harder than V254"),
    ("harder than V253", "harder than V254"),
    ("NEW themes vs V253:", "NEW themes vs V254:"),
    ("kept on V255", "kept on V256"),
    ("V255 keeps floor", "V256 keeps floor"),
    ("C1637 design+fixtures; no VL claim", "C1643 design+fixtures; no VL claim"),
    ("retarget_254", "retarget_255"),
    ("*mere", "*vale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHVALE bait 168.78", "ASHVALE bait 169.79")
h = h.replace("CEDARM bait 170.80", "CEDARV bait 171.81")
h = h.replace("DAWNM ghost 93.93", "DAWNV ghost 94.94")
h = h.replace("GLENM bait 163.73", "GLENV bait 164.74")
h = h.replace("JADEM bait 154.64", "JADEV bait 155.65")
h = h.replace("NETHERM bait 171.81", "NETHERV bait 172.82")

TR = '''TR256 = [
    [2158.0, 2175.5, 1898.0],[840, 760, 820],[2081.0, 2110.25, 1876.0],[2214.0, 2231.0, 1966.0],
    [2276.0, 2300.0, 1936.0],[1994, 2010, 1894],[480.0, 520.0, 740.0],[2124.0, 2155.75, 1900.0],
    [840.0, 760.0, 820.0],[2191.0, 2179.0, 1897.0],[1,1,0],[0,0,0],
    [2257.0, 2278.5, 1922.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO256 = [
    [1956.0, 1968.75, 1817.0],[740, 780, 820],[1899.0, 1913.5, 1792.0],[2029.0, 2045.0, 1848.0],
    [2070.0, 2086.0, 1841.0],[1852, 1864, 1810],[360.0, 400.0, 730.0],[1940.0, 1961.75, 1817.0],
    [780.0, 740.0, 820.0],[1987.0, 1973.0, 1812.0],[1,1,0],[0,0,0],
    [2022.0, 2037.5, 1827.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR256\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO256\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

src = "c1634_product_u2c_cost.py"
if not (ROOT / "scripts" / src).exists():
    src = "c1622_product_u2c_cost.py"
sc_src = "c1636_scorecard_and_stage.py"

tail = f'''# V256 knife = product-U2C (alternating; V255 was confidence-gate); theme wrap *vale
out = (S / "{src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1634", "C1646"), ("c1634", "c1646"),
    ("C1622", "C1646"), ("c1622", "c1646"),
    ("C1466", "C1646"), ("c1466", "c1646"),
]:
    out = out.replace(a, b2)
(S / "c1646_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{src}")

out = (S / "c1641_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1641", "C1647"), ("c1641", "c1647")]:
    out = out.replace(a, b2)
(S / "c1647_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1636", "C1648"), ("c1636", "c1648"),
    ("C1634", "C1646"), ("c1634", "c1646"),
    ("C1635", "C1647"), ("c1635", "c1647"),
    ("C1632", "C1644"), ("c1632", "c1644"),
    ("C1633", "C1645"), ("c1633", "c1645"),
    ("V254", "V256"), ("v254", "v256"),
    ("STAGE_ANT_C1636", "STAGE_ANT_C1648"),
    ("*hurst", "*vale"),
]:
    out = out.replace(a, b2)
(S / "c1648_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v256 ready")
'''
(ROOT / "tools/_build_v256.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1643_vision_v256", "ashvale", "fernvale", "T256", "1188", "1848", "product_u2c", "*vale"]:
    print(needle, needle in (h+tail))
