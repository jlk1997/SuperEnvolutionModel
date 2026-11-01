from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v277.py").read_text(encoding="utf-8")
idx0 = b0.find('# V277 knife = confidence-gate')
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
    ("T277", "T278"), ("TR277", "TR278"), ("HO277", "HO278"),
    ("NEW277", "NEW278"),
    ("V277", "V278"), ("v277", "v278"),
    ("_v277_themes.json", "_v278_themes.json"),
    ("_v276_themes.json", "_v277_themes.json"),
    ("OLD276", "OLD277"),
    ("vision_images_v277", "vision_images_v278"),
    ("VL_GATE_V277", "VL_GATE_V278"), ("vl_gate_v277", "vl_gate_v278"),
    ("C1769", "C1775"), ("c1769", "c1775"),
    ("C1770", "C1776"), ("c1770", "c1776"),
    ("C1771", "C1777"), ("c1771", "c1777"),
    ("_v277c1769", "_v278c1775"),
    ("Harder than V275", "Harder than V276"),
    ("harder than V275", "harder than V276"),
    ("NEW themes vs V275:", "NEW themes vs V276:"),
    ("kept on V277", "kept on V278"),
    ("V277 keeps floor", "V278 keeps floor"),
    ("C1769 design+fixtures; no VL claim", "C1775 design+fixtures; no VL claim"),
    ("retarget_276", "retarget_277"),
    ("*mere", "*vale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMERE bait 190.00", "ASHVALE bait 191.01")
h = h.replace("CEDARM bait 192.02", "CEDARV bait 193.03")
h = h.replace("DAWNM ghost 115.25", "DAWNV ghost 116.26")
h = h.replace("GLENM bait 185.95", "GLENV bait 186.96")
h = h.replace("JADEM bait 176.86", "JADEV bait 177.87")
h = h.replace("NETHERM bait 193.03", "NETHERV bait 194.04")

TR = '''TR278 = [
    [2209.0, 2226.5, 1949.0],[840, 760, 820],[2132.0, 2161.25, 1927.0],[2265.0, 2282.0, 2017.0],
    [2327.0, 2351.0, 1987.0],[2045, 2061, 1945],[550.0, 590.0, 760.0],[2175.0, 2206.75, 1951.0],
    [840.0, 760.0, 820.0],[2242.0, 2230.0, 1948.0],[1,1,0],[0,0,0],
    [2308.0, 2329.5, 1973.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO278 = [
    [2007.0, 2019.75, 1868.0],[640, 660, 820],[1950.0, 1964.5, 1843.0],[2080.0, 2096.0, 1899.0],
    [2121.0, 2137.0, 1892.0],[1903, 1915, 1863],[430.0, 470.0, 740.0],[1991.0, 2012.75, 1868.0],
    [740.0, 780.0, 820.0],[2038.0, 2024.0, 1865.0],[1,1,0],[0,0,0],
    [2073.0, 2088.5, 1878.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR278\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO278\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

tail = '''# V278 knife = product-U2C (alternating; V277 was confidence-gate; theme wrap *mere→*vale)
out = (S / "c1766_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1766", "C1778"), ("c1766", "c1778"),
    ("C1754", "C1778"), ("c1754", "c1778"),
    ("C1466", "C1778"), ("c1466", "c1778"),
]:
    out = out.replace(a, b2)
(S / "c1778_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1766_product_u2c_cost.py")

out = (S / "c1773_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1773", "C1779"), ("c1773", "c1779")]:
    out = out.replace(a, b2)
(S / "c1779_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1768_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1768", "C1780"), ("c1768", "c1780"),
    ("C1766", "C1778"), ("c1766", "c1778"),
    ("C1767", "C1779"), ("c1767", "c1779"),
    ("C1764", "C1776"), ("c1764", "c1776"),
    ("C1765", "C1777"), ("c1765", "c1777"),
    ("V276", "V278"), ("v276", "v278"),
    ("STAGE_ANT_C1768", "STAGE_ANT_C1780"),
    ("*hurst", "*vale"),
]:
    out = out.replace(a, b2)
(S / "c1780_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1768_scorecard_and_stage.py")
print("OK builder v278 ready")
'''
(ROOT / "tools/_build_v278.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1775_vision_v278", "ashvale", "fernvale", "T278", "1188", "1863", "product_u2c", "retarget_277", "theme wrap"]:
    print(needle, needle in (h+tail))
