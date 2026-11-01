from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v269.py").read_text(encoding="utf-8")
idx0 = b0.find('# V269 knife = confidence-gate')
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
    ("T269", "T270"), ("TR269", "TR270"), ("HO269", "HO270"),
    ("NEW269", "NEW270"),
    ("V269", "V270"), ("v269", "v270"),
    ("_v269_themes.json", "_v270_themes.json"),
    ("_v268_themes.json", "_v269_themes.json"),
    ("OLD268", "OLD269"),
    ("vision_images_v269", "vision_images_v270"),
    ("VL_GATE_V269", "VL_GATE_V270"), ("vl_gate_v269", "vl_gate_v270"),
    ("C1721", "C1727"), ("c1721", "c1727"),
    ("C1722", "C1728"), ("c1722", "c1728"),
    ("C1723", "C1729"), ("c1723", "c1729"),
    ("_v269c1721", "_v270c1727"),
    ("Harder than V267", "Harder than V268"),
    ("harder than V267", "harder than V268"),
    ("NEW themes vs V267:", "NEW themes vs V268:"),
    ("kept on V269", "kept on V270"),
    ("V269 keeps floor", "V270 keeps floor"),
    ("C1721 design+fixtures; no VL claim", "C1727 design+fixtures; no VL claim"),
    ("retarget_268", "retarget_269"),
    ("*holm", "*wick"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHWICK bait 182.92", "ASHWICK bait 183.93")
h = h.replace("CEDARH bait 184.94", "CEDARW bait 185.95")
h = h.replace("DAWNH ghost 107.17", "DAWNW ghost 108.18")
h = h.replace("GLENH bait 177.87", "GLENW bait 178.88")
h = h.replace("JADEH bait 168.78", "JADEW bait 169.79")
h = h.replace("NETHERH bait 185.95", "NETHERW bait 186.96")

TR = '''TR270 = [
    [2186.0, 2203.5, 1926.0],[840, 760, 820],[2109.0, 2138.25, 1904.0],[2242.0, 2259.0, 1994.0],
    [2304.0, 2328.0, 1964.0],[2022, 2038, 1922],[480.0, 520.0, 740.0],[2152.0, 2183.75, 1928.0],
    [840.0, 760.0, 820.0],[2219.0, 2207.0, 1925.0],[1,1,0],[0,0,0],
    [2285.0, 2306.5, 1950.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO270 = [
    [1984.0, 1996.75, 1845.0],[740, 780, 820],[1927.0, 1941.5, 1820.0],[2057.0, 2073.0, 1876.0],
    [2098.0, 2114.0, 1869.0],[1880, 1892, 1840],[360.0, 400.0, 730.0],[1968.0, 1989.75, 1845.0],
    [780.0, 740.0, 820.0],[2015.0, 2001.0, 1842.0],[1,1,0],[0,0,0],
    [2050.0, 2065.5, 1855.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR270\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO270\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

src = "c1718_product_u2c_cost.py"
if not (ROOT / "scripts" / src).exists():
    src = "c1706_product_u2c_cost.py"
sc_src = "c1720_scorecard_and_stage.py"

tail = f'''# V270 knife = product-U2C (alternating; V269 was confidence-gate)
out = (S / "{src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1718", "C1730"), ("c1718", "c1730"),
    ("C1706", "C1730"), ("c1706", "c1730"),
    ("C1466", "C1730"), ("c1466", "c1730"),
]:
    out = out.replace(a, b2)
(S / "c1730_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{src}")

out = (S / "c1725_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1725", "C1731"), ("c1725", "c1731")]:
    out = out.replace(a, b2)
(S / "c1731_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1720", "C1732"), ("c1720", "c1732"),
    ("C1718", "C1730"), ("c1718", "c1730"),
    ("C1719", "C1731"), ("c1719", "c1731"),
    ("C1716", "C1728"), ("c1716", "c1728"),
    ("C1717", "C1729"), ("c1717", "c1729"),
    ("V268", "V270"), ("v268", "v270"),
    ("STAGE_ANT_C1720", "STAGE_ANT_C1732"),
    ("*croft", "*wick"),
]:
    out = out.replace(a, b2)
(S / "c1732_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v270 ready")
'''
(ROOT / "tools/_build_v270.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1727_vision_v270", "ashwick", "fernwick", "T270", "1188", "1840", "product_u2c"]:
    print(needle, needle in (h+tail))
