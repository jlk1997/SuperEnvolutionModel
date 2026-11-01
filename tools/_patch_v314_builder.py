from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v313.py").read_text(encoding="utf-8")
idx0 = b0.find('# V313 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1990 = " in head0:
    head0 = head0[:head0.find("SC1990 = ")]

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
    ("T313", "T314"), ("TR313", "TR314"), ("HO313", "HO314"),
    ("NEW313", "NEW314"),
    ("V313", "V314"), ("v313", "v314"),
    ("_v313_themes.json", "_v314_themes.json"),
    ("_v312_themes.json", "_v313_themes.json"),
    ("OLD312", "OLD313"),
    ("vision_images_v313", "vision_images_v314"),
    ("VL_GATE_V313", "VL_GATE_V314"), ("vl_gate_v313", "vl_gate_v314"),
    ("C1985", "C1991"), ("c1985", "c1991"),
    ("C1986", "C1992"), ("c1986", "c1992"),
    ("C1987", "C1993"), ("c1987", "c1993"),
    ("_v313c1985", "_v314c1991"),
    ("Harder than V311", "Harder than V312"),
    ("harder than V311", "harder than V312"),
    ("NEW themes vs V311:", "NEW themes vs V312:"),
    ("kept on V313", "kept on V314"),
    ("V313 keeps floor", "V314 keeps floor"),
    ("C1985 design+fixtures; no VL claim", "C1991 design+fixtures; no VL claim"),
    ("retarget_312", "retarget_313"),
    ("*holm", "*wick"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHOLM bait 226.36", "ASHWICK bait 227.37")
h = h.replace("CEDARH bait 228.38", "CEDARW bait 229.39")
h = h.replace("DAWNH ghost 151.61", "DAWNW ghost 152.62")
h = h.replace("GLENH bait 221.31", "GLENW bait 222.32")
h = h.replace("JADEH bait 212.22", "JADEW bait 213.23")
h = h.replace("NETHERH bait 229.39", "NETHERW bait 230.40")

TR = '''TR314 = [
    [2292.0, 2309.5, 2032.0],[840, 760, 820],[2215.0, 2244.25, 2010.0],[2348.0, 2365.0, 2100.0],
    [2410.0, 2434.0, 2070.0],[2128, 2144, 2028],[490.0, 530.0, 760.0],[2258.0, 2289.75, 2034.0],
    [840.0, 760.0, 820.0],[2325.0, 2313.0, 2031.0],[1,1,0],[0,0,0],
    [2391.0, 2412.5, 2056.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO314 = [
    [2090.0, 2102.75, 1951.0],[640, 660, 820],[2033.0, 2047.5, 1926.0],[2163.0, 2179.0, 1982.0],
    [2204.0, 2220.0, 1975.0],[1986, 1998, 1946],[420.0, 460.0, 740.0],[2074.0, 2095.75, 1951.0],
    [740.0, 780.0, 820.0],[2121.0, 2107.0, 1948.0],[1,1,0],[0,0,0],
    [2156.0, 2171.5, 1961.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR314\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO314\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c1984_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1984", "C1996"), ("c1984", "c1996"),
    ("C1982", "C1994"), ("c1982", "c1994"),
    ("C1983", "C1995"), ("c1983", "c1995"),
    ("C1980", "C1992"), ("c1980", "c1992"),
    ("C1981", "C1993"), ("c1981", "c1993"),
    ("C1976", "C1988"), ("c1976", "c1988"),
    ("C1979", "C1991"), ("c1979", "c1991"),
    ("V312", "V314"), ("v312", "v314"),
    ("STAGE_ANT_C1984", "STAGE_ANT_C1996"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V314 knife = product-U2C (alternating; V313 was confidence-gate)
out = (S / "c1982_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1982", "C1994"), ("c1982", "c1994"),
    ("C1970", "C1994"), ("c1970", "c1994"),
    ("product_u2c_cost_c1982", "product_u2c_cost_c1994"),
    ("u2c_v200", "u2c_v201"),
    ("u2c_c1982", "u2c_c1994"),
]:
    out = out.replace(a, b2)
(S / "c1994_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1982")

out = (S / "c1989_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1989", "C1995"), ("c1989", "c1995")]:
    out = out.replace(a, b2)
(S / "c1995_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1996_scorecard_and_stage.py").write_text(SC1996, encoding="utf-8")
print("scorecard from fixed c1984 product-U2C pattern")
print("OK builder v314 ready")
'''
pre = "SC1996 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v314.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1991_vision_v314", "ashwick", "fernwick", "T314", "1188", "1946", "product_u2c", "retarget_313"]:
    print(needle, needle in (h+pre+tail))
