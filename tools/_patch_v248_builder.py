from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v247.py").read_text(encoding="utf-8")

# Find knife BEFORE renumbering V247->V248
idx = b.find('# V247 knife = confidence-gate')
if idx < 0:
    raise SystemExit('knife not found pre-rename')

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
for a, c in theme_pairs:
    b = b.replace(a, c)

pairs = [
    ("*holm ; stack mid-band", "*wick ; stack mid-band"),
    ("T247", "T248"), ("TR247", "TR248"), ("HO247", "HO248"),
    ("NEW247", "NEW248"),
    ("V247", "V248"), ("v247", "v248"),
    ("_v247_themes.json", "_v248_themes.json"),
    ("_v246_themes.json", "_v247_themes.json"),
    ("OLD246", "OLD247"),
    ("vision_images_v247", "vision_images_v248"),
    ("VL_GATE_V247", "VL_GATE_V248"), ("vl_gate_v247", "vl_gate_v248"),
    ("C1589", "C1595"), ("c1589", "c1595"),
    ("C1590", "C1596"), ("c1590", "c1596"),
    ("C1591", "C1597"), ("c1591", "c1597"),
    ("_v247c1589", "_v248c1595"),
    ("Harder than V245", "Harder than V246"),
    ("harder than V245", "harder than V246"),
    ("NEW themes vs V245:", "NEW themes vs V246:"),
    ("kept on V247", "kept on V248"),
    ("V247 keeps floor", "V248 keeps floor"),
    ("C1589 design+fixtures; no VL claim", "C1595 design+fixtures; no VL claim"),
    ("retarget_246", "retarget_247"),
    ("*holm", "*wick"),
]
# Re-find knife index after theme (holm->wick) but BEFORE V247 rename: themes don't touch knife comment
# Actually themes already applied; V247 in comment still V247 until pairs. Recompute idx from original file.
b0 = (ROOT / "tools/_build_v247.py").read_text(encoding="utf-8")
idx0 = b0.find('# V247 knife = confidence-gate')
# Apply only theme to prefix length? Safer: split original, transform head only.
head0 = b0[:idx0]
tail_skip = b0[idx0:]  # discard, rewrite knife
# transform head0 same way
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHWICK bait 160.70", "ASHWICK bait 161.71")
h = h.replace("CEDARH bait 162.72", "CEDARW bait 163.73")
h = h.replace("DAWNH ghost 85.85", "DAWNW ghost 86.86")
h = h.replace("GLENH bait 155.65", "GLENW bait 156.66")
h = h.replace("JADEH bait 146.56", "JADEW bait 147.57")
h = h.replace("NETHERH bait 163.73", "NETHERW bait 164.74")

TR = '''TR248 = [
    [2142.0, 2159.5, 1882.0],[840, 760, 820],[2065.0, 2094.25, 1860.0],[2198.0, 2215.0, 1950.0],
    [2260.0, 2284.0, 1920.0],[1978, 1994, 1878],[480.0, 520.0, 740.0],[2108.0, 2139.75, 1884.0],
    [840.0, 760.0, 820.0],[2175.0, 2163.0, 1881.0],[1,1,0],[0,0,0],
    [2241.0, 2262.5, 1906.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO248 = [
    [1940.0, 1952.75, 1801.0],[740, 780, 820],[1883.0, 1897.5, 1776.0],[2013.0, 2029.0, 1832.0],
    [2054.0, 2070.0, 1825.0],[1836, 1848, 1794],[360.0, 400.0, 730.0],[1924.0, 1945.75, 1801.0],
    [780.0, 740.0, 820.0],[1971.0, 1957.0, 1796.0],[1,1,0],[0,0,0],
    [2006.0, 2021.5, 1811.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR248\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO248\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

# product-U2C source
src = None
for name in ["c1586_product_u2c_cost.py", "c1574_product_u2c_cost.py", "c1466_product_u2c_cost.py"]:
    if (ROOT / "scripts" / name).exists():
        src = name
        break
if not src:
    found = sorted((ROOT / "scripts").glob("*product_u2c*.py"))
    raise SystemExit(f'no pu2c; {[p.name for p in found[-8:]]}')

# Prefer V246 scorecard (product-U2C knife era) as scorecard template
sc_src = "c1588_scorecard_and_stage.py"
if not (ROOT / "scripts" / sc_src).exists():
    sc_src = "c1594_scorecard_and_stage.py"

tail = f'''# V248 knife = product-U2C (alternating; V247 was confidence-gate)
out = (S / "{src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1586", "C1598"), ("c1586", "c1598"),
    ("C1574", "C1598"), ("c1574", "c1598"),
    ("C1466", "C1598"), ("c1466", "c1598"),
]:
    out = out.replace(a, b2)
(S / "c1598_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{src}")

out = (S / "c1593_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1593", "C1599"), ("c1593", "c1599")]:
    out = out.replace(a, b2)
(S / "c1599_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1588", "C1600"), ("c1588", "c1600"),
    ("C1586", "C1598"), ("c1586", "c1598"),
    ("C1587", "C1599"), ("c1587", "c1599"),
    ("C1584", "C1596"), ("c1584", "c1596"),
    ("C1585", "C1597"), ("c1585", "c1597"),
    ("C1594", "C1600"), ("c1594", "c1600"),
    ("C1592", "C1598"), ("c1592", "c1598"),
    ("C1593", "C1599"), ("c1593", "c1599"),
    ("C1590", "C1596"), ("c1590", "c1596"),
    ("C1591", "C1597"), ("c1591", "c1597"),
    ("V246", "V248"), ("v246", "v248"),
    ("V247", "V248"), ("v247", "v248"),
    ("STAGE_ANT_C1588", "STAGE_ANT_C1600"),
    ("STAGE_ANT_C1594", "STAGE_ANT_C1600"),
    ("*croft", "*wick"),
    ("*holm", "*wick"),
]:
    out = out.replace(a, b2)
(S / "c1600_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v248 ready")
'''
(ROOT / "tools/_build_v248.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail), "pu2c", src, "sc", sc_src)
for needle in ["c1595_vision_v248", "ashwick", "T248", "1188", "1832", "product_u2c"]:
    print(needle, needle in (h+tail))
