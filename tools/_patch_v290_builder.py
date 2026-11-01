from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v289.py").read_text(encoding="utf-8")
idx0 = b0.find('# V289 knife = confidence-gate')
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
    ("T289", "T290"), ("TR289", "TR290"), ("HO289", "HO290"),
    ("NEW289", "NEW290"),
    ("V289", "V290"), ("v289", "v290"),
    ("_v289_themes.json", "_v290_themes.json"),
    ("_v288_themes.json", "_v289_themes.json"),
    ("OLD288", "OLD289"),
    ("vision_images_v289", "vision_images_v290"),
    ("VL_GATE_V289", "VL_GATE_V290"), ("vl_gate_v289", "vl_gate_v290"),
    ("C1841", "C1847"), ("c1841", "c1847"),
    ("C1842", "C1848"), ("c1842", "c1848"),
    ("C1843", "C1849"), ("c1843", "c1849"),
    ("_v289c1841", "_v290c1847"),
    ("Harder than V287", "Harder than V288"),
    ("harder than V287", "harder than V288"),
    ("NEW themes vs V287:", "NEW themes vs V288:"),
    ("kept on V289", "kept on V290"),
    ("V289 keeps floor", "V290 keeps floor"),
    ("C1841 design+fixtures; no VL claim", "C1847 design+fixtures; no VL claim"),
    ("retarget_288", "retarget_289"),
    ("*vale", "*croft"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHVALE bait 202.12", "ASHCROFT bait 203.13")
h = h.replace("CEDARV bait 204.14", "CEDARC bait 205.15")
h = h.replace("DAWNV ghost 127.37", "DAWNC ghost 128.38")
h = h.replace("GLENV bait 197.07", "GLENC bait 198.08")
h = h.replace("JADEV bait 188.98", "JADEC bait 189.99")
h = h.replace("NETHERV bait 205.15", "NETHERC bait 206.16")

TR = '''TR290 = [
    [2244.0, 2261.5, 1984.0],[840, 760, 820],[2167.0, 2196.25, 1962.0],[2300.0, 2317.0, 2052.0],
    [2362.0, 2386.0, 2022.0],[2080, 2096, 1980],[490.0, 530.0, 760.0],[2210.0, 2241.75, 1986.0],
    [840.0, 760.0, 820.0],[2277.0, 2265.0, 1983.0],[1,1,0],[0,0,0],
    [2343.0, 2364.5, 2008.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO290 = [
    [2042.0, 2054.75, 1903.0],[640, 660, 820],[1985.0, 1999.5, 1878.0],[2115.0, 2131.0, 1934.0],
    [2156.0, 2172.0, 1927.0],[1938, 1950, 1898],[420.0, 460.0, 740.0],[2026.0, 2047.75, 1903.0],
    [740.0, 780.0, 820.0],[2073.0, 2059.0, 1900.0],[1,1,0],[0,0,0],
    [2108.0, 2123.5, 1913.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR290\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO290\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

u2c_src = "c1838_product_u2c_cost.py"
sc_src = "c1846_scorecard_and_stage.py"

tail = f'''# V290 knife = product-U2C (alternating; V289 was confidence-gate)
out = (S / "{u2c_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1838", "C1850"), ("c1838", "c1850"),
    ("C1826", "C1850"), ("c1826", "c1850"),
    ("product_u2c_cost_c1838", "product_u2c_cost_c1850"),
    ("u2c_v188", "u2c_v189"),
]:
    out = out.replace(a, b2)
(S / "c1850_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{u2c_src}")

out = (S / "c1845_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1845", "C1851"), ("c1845", "c1851")]:
    out = out.replace(a, b2)
(S / "c1851_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1846", "C1852"), ("c1846", "c1852"),
    ("C1844", "C1850"), ("c1844", "c1850"),
    ("C1845", "C1851"), ("c1845", "c1851"),
    ("C1842", "C1848"), ("c1842", "c1848"),
    ("C1843", "C1849"), ("c1843", "c1849"),
    ("V289", "V290"), ("v289", "v290"),
    ("STAGE_ANT_C1846", "STAGE_ANT_C1852"),
    ("*vale", "*croft"),
    ("confidence-gate", "product-U2C"),
    ("confidence_gate", "product_u2c"),
]:
    out = out.replace(a, b2)
(S / "c1852_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v290 ready")
'''
(ROOT / "tools/_build_v290.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1847_vision_v290", "ashcroft", "ferncroft", "T290", "1188", "1898", "product_u2c", "retarget_289"]:
    print(needle, needle in (h+tail))
