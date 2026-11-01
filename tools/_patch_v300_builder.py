from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v299.py").read_text(encoding="utf-8")
idx0 = b0.find('# V299 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1906 = " in head0:
    head0 = head0[:head0.find("SC1906 = ")]

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
    ("T299", "T300"), ("TR299", "TR300"), ("HO299", "HO300"),
    ("NEW299", "NEW300"),
    ("V299", "V300"), ("v299", "v300"),
    ("_v299_themes.json", "_v300_themes.json"),
    ("_v298_themes.json", "_v299_themes.json"),
    ("OLD298", "OLD299"),
    ("vision_images_v299", "vision_images_v300"),
    ("VL_GATE_V299", "VL_GATE_V300"), ("vl_gate_v299", "vl_gate_v300"),
    ("C1901", "C1907"), ("c1901", "c1907"),
    ("C1902", "C1908"), ("c1902", "c1908"),
    ("C1903", "C1909"), ("c1903", "c1909"),
    ("_v299c1901", "_v300c1907"),
    ("Harder than V297", "Harder than V298"),
    ("harder than V297", "harder than V298"),
    ("NEW themes vs V297:", "NEW themes vs V298:"),
    ("kept on V299", "kept on V300"),
    ("V299 keeps floor", "V300 keeps floor"),
    ("C1901 design+fixtures; no VL claim", "C1907 design+fixtures; no VL claim"),
    ("retarget_298", "retarget_299"),
    ("*mere", "*vale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMERE bait 212.22", "ASHVALE bait 213.23")
h = h.replace("CEDARM bait 214.24", "CEDARV bait 215.25")
h = h.replace("DAWNM ghost 137.47", "DAWNV ghost 138.48")
h = h.replace("GLENM bait 207.17", "GLENV bait 208.18")
h = h.replace("JADEM bait 198.08", "JADEV bait 199.09")
h = h.replace("NETHERM bait 215.25", "NETHERV bait 216.26")

TR = '''TR300 = [
    [2264.0, 2281.5, 2004.0],[840, 760, 820],[2187.0, 2216.25, 1982.0],[2320.0, 2337.0, 2072.0],
    [2382.0, 2406.0, 2042.0],[2100, 2116, 2000],[490.0, 530.0, 760.0],[2230.0, 2261.75, 2006.0],
    [840.0, 760.0, 820.0],[2297.0, 2285.0, 2003.0],[1,1,0],[0,0,0],
    [2363.0, 2384.5, 2028.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO300 = [
    [2062.0, 2074.75, 1923.0],[640, 660, 820],[2005.0, 2019.5, 1898.0],[2135.0, 2151.0, 1954.0],
    [2176.0, 2192.0, 1947.0],[1958, 1970, 1918],[420.0, 460.0, 740.0],[2046.0, 2067.75, 1923.0],
    [740.0, 780.0, 820.0],[2093.0, 2079.0, 1920.0],[1,1,0],[0,0,0],
    [2128.0, 2143.5, 1933.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR300\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO300\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c1900_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1900", "C1912"), ("c1900", "c1912"),
    ("C1898", "C1910"), ("c1898", "c1910"),
    ("C1899", "C1911"), ("c1899", "c1911"),
    ("C1896", "C1908"), ("c1896", "c1908"),
    ("C1897", "C1909"), ("c1897", "c1909"),
    ("C1892", "C1904"), ("c1892", "c1904"),
    ("C1895", "C1907"), ("c1895", "c1907"),
    ("V298", "V300"), ("v298", "v300"),
    ("STAGE_ANT_C1900", "STAGE_ANT_C1912"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V300 knife = product-U2C (alternating; V299 was confidence-gate; theme wrap *mere→*vale)
out = (S / "c1898_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1898", "C1910"), ("c1898", "c1910"),
    ("C1886", "C1910"), ("c1886", "c1910"),
    ("product_u2c_cost_c1898", "product_u2c_cost_c1910"),
    ("u2c_v193", "u2c_v194"),
    ("u2c_c1898", "u2c_c1910"),
]:
    out = out.replace(a, b2)
(S / "c1910_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1898")

out = (S / "c1905_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1905", "C1911"), ("c1905", "c1911")]:
    out = out.replace(a, b2)
(S / "c1911_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1912_scorecard_and_stage.py").write_text(SC1912, encoding="utf-8")
print("scorecard from fixed c1900 product-U2C pattern")
print("OK builder v300 ready")
'''
pre = "SC1912 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v300.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1907_vision_v300", "ashvale", "fernvale", "T300", "1188", "1918", "product_u2c", "retarget_299", "theme wrap"]:
    print(needle, needle in (h+pre+tail))
