from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v291.py").read_text(encoding="utf-8")
idx0 = b0.find('# V291 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("netherholm", "netherwick"), ("NETHERHOLM", "NETHERWICK"),
    ("cedarholm", "cedarwick"), ("CEDARHOLM", "CEDARWICK"),
    ("dawnholm", "dawnwick"), ("DAWNHOLM", "DAWNWICK"),
    ("fernholm", "fernwick"), ("FERNHOLM", "FERNWICK"),
    ("glenholm", "glenwick"), ("GLENHOLM", "GLENWICK"),
    ("hazeholm", "hazewick"), ("HAZEHOLM", "HAZEWICK"),
    ("jadeholm", "jadewick"), ("JADEHOLM", "JADEWICK"),
    ("knotholm", "knotwick"), ("KNOTHOLM", "KNOTWICK"),
    ("lakeholm", "lakewick"), ("LAKEHOLM", "LAKEWICK"),
    ("mossholm", "mosswick"), ("MOSSHOLM", "MOSSWICK"),
    ("pineholm", "pinewick"), ("PINEHOLM", "PINEWICK"),
    ("quillholm", "quillwick"), ("QUILLHOLM", "QUILLWICK"),
    ("reedholm", "reedwick"), ("REEDHOLM", "REEDWICK"),
    ("stoneholm", "stonewick"), ("STONEHOLM", "STONEWICK"),
    ("ashholm", "ashwick"), ("ASHHOLM", "ASHWICK"),
    ("elmholm", "elmwick"), ("ELMHOLM", "ELMWICK"),
    ("inkholm", "inkwick"), ("INKHOLM", "INKWICK"),
    ("oakholm", "oakwick"), ("OAKHOLM", "OAKWICK"),
]
pairs = [
    ("*holm ; stack mid-band", "*wick ; stack mid-band"),
    ("T291", "T292"), ("TR291", "TR292"), ("HO291", "HO292"),
    ("NEW291", "NEW292"),
    ("V291", "V292"), ("v291", "v292"),
    ("_v291_themes.json", "_v292_themes.json"),
    ("_v290_themes.json", "_v291_themes.json"),
    ("OLD290", "OLD291"),
    ("vision_images_v291", "vision_images_v292"),
    ("VL_GATE_V291", "VL_GATE_V292"), ("vl_gate_v291", "vl_gate_v292"),
    ("C1853", "C1859"), ("c1853", "c1859"),
    ("C1854", "C1860"), ("c1854", "c1860"),
    ("C1855", "C1861"), ("c1855", "c1861"),
    ("_v291c1853", "_v292c1859"),
    ("Harder than V289", "Harder than V290"),
    ("harder than V289", "harder than V290"),
    ("NEW themes vs V289:", "NEW themes vs V290:"),
    ("kept on V291", "kept on V292"),
    ("V291 keeps floor", "V292 keeps floor"),
    ("C1853 design+fixtures; no VL claim", "C1859 design+fixtures; no VL claim"),
    ("retarget_290", "retarget_291"),
    ("*holm", "*wick"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHOLM bait 204.14", "ASHWICK bait 205.15")
h = h.replace("CEDARH bait 206.16", "CEDARW bait 207.17")
h = h.replace("DAWNH ghost 129.39", "DAWNW ghost 130.40")
h = h.replace("GLENH bait 199.09", "GLENW bait 200.10")
h = h.replace("JADEH bait 190.00", "JADEW bait 191.01")
h = h.replace("NETHERH bait 207.17", "NETHERW bait 208.18")

TR = '''TR292 = [
    [2248.0, 2265.5, 1988.0],[840, 760, 820],[2171.0, 2200.25, 1966.0],[2304.0, 2321.0, 2056.0],
    [2366.0, 2390.0, 2026.0],[2084, 2100, 1984],[490.0, 530.0, 760.0],[2214.0, 2245.75, 1990.0],
    [840.0, 760.0, 820.0],[2281.0, 2269.0, 1987.0],[1,1,0],[0,0,0],
    [2347.0, 2368.5, 2012.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO292 = [
    [2046.0, 2058.75, 1907.0],[640, 660, 820],[1989.0, 2003.5, 1882.0],[2119.0, 2135.0, 1938.0],
    [2160.0, 2176.0, 1931.0],[1942, 1954, 1902],[420.0, 460.0, 740.0],[2030.0, 2051.75, 1907.0],
    [740.0, 780.0, 820.0],[2077.0, 2063.0, 1904.0],[1,1,0],[0,0,0],
    [2112.0, 2127.5, 1917.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR292\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO292\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

u2c_src = "c1850_product_u2c_cost.py"

# Emit fixed product-U2C scorecard (copy of working c1852 pattern) rather than blind-rename
sc_body = (ROOT / "scripts/c1852_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1852", "C1864"), ("c1852", "c1864"),
    ("C1850", "C1862"), ("c1850", "c1862"),
    ("C1851", "C1863"), ("c1851", "c1863"),
    ("C1848", "C1860"), ("c1848", "c1860"),
    ("C1849", "C1861"), ("c1849", "c1861"),
    ("C1844", "C1856"), ("c1844", "c1856"),
    ("C1847", "C1859"), ("c1847", "c1859"),
    ("V290", "V292"), ("v290", "v292"),
    ("STAGE_ANT_C1852", "STAGE_ANT_C1864"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V292 knife = product-U2C (alternating; V291 was confidence-gate)
out = (S / "{u2c_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1850", "C1862"), ("c1850", "c1862"),
    ("C1838", "C1862"), ("c1838", "c1862"),
    ("product_u2c_cost_c1850", "product_u2c_cost_c1862"),
    ("u2c_v189", "u2c_v190"),
    ("u2c_c1850", "u2c_c1862"),
]:
    out = out.replace(a, b2)
(S / "c1862_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{u2c_src}")

out = (S / "c1857_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1857", "C1863"), ("c1857", "c1863")]:
    out = out.replace(a, b2)
(S / "c1863_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1864_scorecard_and_stage.py").write_text({repr(sc_body)}, encoding="utf-8")
print("scorecard from fixed c1852 pattern")
print("OK builder v292 ready")
'''
# Fix the sc_body embedding - use write directly in patch instead
(ROOT / "tools/_build_v292.py").write_text(h + '# PLACEHOLDER_TAIL\n', encoding="utf-8")
# Write sc separately then assemble
(ROOT / "scripts/_sc1864_template.py").write_text(sc_body, encoding="utf-8")
print("head ok", len(h), "sc template", len(sc_body))
for needle in ["c1859_vision_v292", "ashwick", "fernwick", "T292", "1188", "1902"]:
    print(needle, needle in h)
