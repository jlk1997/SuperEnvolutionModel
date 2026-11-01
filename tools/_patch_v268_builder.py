from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v267.py").read_text(encoding="utf-8")
idx0 = b0.find('# V267 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
    ("T267", "T268"), ("TR267", "TR268"), ("HO267", "HO268"),
    ("NEW267", "NEW268"),
    ("V267", "V268"), ("v267", "v268"),
    ("_v267_themes.json", "_v268_themes.json"),
    ("_v266_themes.json", "_v267_themes.json"),
    ("OLD266", "OLD267"),
    ("vision_images_v267", "vision_images_v268"),
    ("VL_GATE_V267", "VL_GATE_V268"), ("vl_gate_v267", "vl_gate_v268"),
    ("C1709", "C1715"), ("c1709", "c1715"),
    ("C1710", "C1716"), ("c1710", "c1716"),
    ("C1711", "C1717"), ("c1711", "c1717"),
    ("_v267c1709", "_v268c1715"),
    ("Harder than V265", "Harder than V266"),
    ("harder than V265", "harder than V266"),
    ("NEW themes vs V265:", "NEW themes vs V266:"),
    ("kept on V267", "kept on V268"),
    ("V267 keeps floor", "V268 keeps floor"),
    ("C1709 design+fixtures; no VL claim", "C1715 design+fixtures; no VL claim"),
    ("retarget_266", "retarget_267"),
    ("*vale", "*croft"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHCROFT bait 180.90", "ASHCROFT bait 181.91")
h = h.replace("CEDARV bait 182.92", "CEDARC bait 183.93")
h = h.replace("DAWNV ghost 105.15", "DAWNC ghost 106.16")
h = h.replace("GLENV bait 175.85", "GLENC bait 176.86")
h = h.replace("JADEV bait 166.76", "JADEC bait 167.77")
h = h.replace("NETHERV bait 183.93", "NETHERC bait 184.94")

TR = '''TR268 = [
    [2182.0, 2199.5, 1922.0],[840, 760, 820],[2105.0, 2134.25, 1900.0],[2238.0, 2255.0, 1990.0],
    [2300.0, 2324.0, 1960.0],[2018, 2034, 1918],[480.0, 520.0, 740.0],[2148.0, 2179.75, 1924.0],
    [840.0, 760.0, 820.0],[2215.0, 2203.0, 1921.0],[1,1,0],[0,0,0],
    [2281.0, 2302.5, 1946.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO268 = [
    [1980.0, 1992.75, 1841.0],[740, 780, 820],[1923.0, 1937.5, 1816.0],[2053.0, 2069.0, 1872.0],
    [2094.0, 2110.0, 1865.0],[1876, 1888, 1836],[360.0, 400.0, 730.0],[1964.0, 1985.75, 1841.0],
    [780.0, 740.0, 820.0],[2011.0, 1997.0, 1838.0],[1,1,0],[0,0,0],
    [2046.0, 2061.5, 1851.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR268\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO268\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

src = "c1706_product_u2c_cost.py"
if not (ROOT / "scripts" / src).exists():
    src = "c1694_product_u2c_cost.py"
sc_src = "c1708_scorecard_and_stage.py"

tail = f'''# V268 knife = product-U2C (alternating; V267 was confidence-gate)
out = (S / "{src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1706", "C1718"), ("c1706", "c1718"),
    ("C1694", "C1718"), ("c1694", "c1718"),
    ("C1466", "C1718"), ("c1466", "c1718"),
]:
    out = out.replace(a, b2)
(S / "c1718_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{src}")

out = (S / "c1713_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1713", "C1719"), ("c1713", "c1719")]:
    out = out.replace(a, b2)
(S / "c1719_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1708", "C1720"), ("c1708", "c1720"),
    ("C1706", "C1718"), ("c1706", "c1718"),
    ("C1707", "C1719"), ("c1707", "c1719"),
    ("C1704", "C1716"), ("c1704", "c1716"),
    ("C1705", "C1717"), ("c1705", "c1717"),
    ("V266", "V268"), ("v266", "v268"),
    ("STAGE_ANT_C1708", "STAGE_ANT_C1720"),
    ("*mere", "*croft"),
]:
    out = out.replace(a, b2)
(S / "c1720_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v268 ready")
'''
(ROOT / "tools/_build_v268.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1715_vision_v268", "ashcroft", "ferncroft", "T268", "1188", "1836", "product_u2c"]:
    print(needle, needle in (h+tail))
