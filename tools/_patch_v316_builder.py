from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v315.py").read_text(encoding="utf-8")
idx0 = b0.find('# V315 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2002 = " in head0:
    head0 = head0[:head0.find("SC2002 = ")]

theme_pairs = [
    ("nethermoor", "netherfen"), ("NETHERMOOR", "NETHERFEN"),
    ("cedarmoor", "cedarfen"), ("CEDARMOOR", "CEDARFEN"),
    ("dawnmoor", "dawnfen"), ("DAWNMOOR", "DAWNFEN"),
    ("fernmoor", "fernfen"), ("FERNMOOR", "FERNFEN"),
    ("glenmoor", "glenfen"), ("GLENMOOR", "GLENFEN"),
    ("hazemoor", "hazefen"), ("HAZEMOOR", "HAZEFEN"),
    ("jademoor", "jadefen"), ("JADEMOOR", "JADEFEN"),
    ("knotmoor", "knotfen"), ("KNOTMOOR", "KNOTFEN"),
    ("lakemoor", "lakefen"), ("LAKEMOOR", "LAKEFEN"),
    ("mossmoor", "mossfen"), ("MOSSMOOR", "MOSSFEN"),
    ("pinemoor", "pinefen"), ("PINEMOOR", "PINEFEN"),
    ("quillmoor", "quillfen"), ("QUILLMOOR", "QUILLFEN"),
    ("reedmoor", "reedfen"), ("REEDMOOR", "REEDFEN"),
    ("stonemoor", "stonefen"), ("STONEMOOR", "STONEFEN"),
    ("ashmoor", "ashfen"), ("ASHMOOR", "ASHFEN"),
    ("elmmoor", "elmfen"), ("ELMMOOR", "ELMFEN"),
    ("inkmoor", "inkfen"), ("INKMOOR", "INKFEN"),
    ("oakmoor", "oakfen"), ("OAKMOOR", "OAKFEN"),
]
pairs = [
    ("*moor ; stack mid-band", "*fen ; stack mid-band"),
    ("T315", "T316"), ("TR315", "TR316"), ("HO315", "HO316"),
    ("NEW315", "NEW316"),
    ("V315", "V316"), ("v315", "v316"),
    ("_v315_themes.json", "_v316_themes.json"),
    ("_v314_themes.json", "_v315_themes.json"),
    ("OLD314", "OLD315"),
    ("vision_images_v315", "vision_images_v316"),
    ("VL_GATE_V315", "VL_GATE_V316"), ("vl_gate_v315", "vl_gate_v316"),
    ("C1997", "C2003"), ("c1997", "c2003"),
    ("C1998", "C2004"), ("c1998", "c2004"),
    ("C1999", "C2005"), ("c1999", "c2005"),
    ("_v315c1997", "_v316c2003"),
    ("Harder than V313", "Harder than V314"),
    ("harder than V313", "harder than V314"),
    ("NEW themes vs V313:", "NEW themes vs V314:"),
    ("kept on V315", "kept on V316"),
    ("V315 keeps floor", "V316 keeps floor"),
    ("C1997 design+fixtures; no VL claim", "C2003 design+fixtures; no VL claim"),
    ("retarget_314", "retarget_315"),
    ("*moor", "*fen"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMOOR bait 228.38", "ASHFEN bait 229.39")
h = h.replace("CEDARM bait 230.40", "CEDARF bait 231.41")
h = h.replace("DAWNM ghost 153.63", "DAWNF ghost 154.64")
h = h.replace("GLENM bait 223.33", "GLENF bait 224.34")
h = h.replace("JADEM bait 214.24", "JADEF bait 215.25")
h = h.replace("NETHERM bait 231.41", "NETHERF bait 232.42")

TR = '''TR316 = [
    [2296.0, 2313.5, 2036.0],[840, 760, 820],[2219.0, 2248.25, 2014.0],[2352.0, 2369.0, 2104.0],
    [2414.0, 2438.0, 2074.0],[2132, 2148, 2032],[490.0, 530.0, 760.0],[2262.0, 2293.75, 2038.0],
    [840.0, 760.0, 820.0],[2329.0, 2317.0, 2035.0],[1,1,0],[0,0,0],
    [2395.0, 2416.5, 2060.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO316 = [
    [2094.0, 2106.75, 1955.0],[640, 660, 820],[2037.0, 2051.5, 1930.0],[2167.0, 2183.0, 1986.0],
    [2208.0, 2224.0, 1979.0],[1990, 2002, 1950],[420.0, 460.0, 740.0],[2078.0, 2099.75, 1955.0],
    [740.0, 780.0, 820.0],[2125.0, 2111.0, 1952.0],[1,1,0],[0,0,0],
    [2160.0, 2175.5, 1965.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR316\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO316\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c1996_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1996", "C2008"), ("c1996", "c2008"),
    ("C1994", "C2006"), ("c1994", "c2006"),
    ("C1995", "C2007"), ("c1995", "c2007"),
    ("C1992", "C2004"), ("c1992", "c2004"),
    ("C1993", "C2005"), ("c1993", "c2005"),
    ("C1988", "C2000"), ("c1988", "c2000"),
    ("C1991", "C2003"), ("c1991", "c2003"),
    ("V314", "V316"), ("v314", "v316"),
    ("STAGE_ANT_C1996", "STAGE_ANT_C2008"),
    ("*wick", "*fen"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V316 knife = product-U2C (alternating; V315 was confidence-gate)
out = (S / "c1994_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1994", "C2006"), ("c1994", "c2006"),
    ("C1982", "C2006"), ("c1982", "c2006"),
    ("product_u2c_cost_c1994", "product_u2c_cost_c2006"),
    ("u2c_v201", "u2c_v202"),
    ("u2c_c1994", "u2c_c2006"),
]:
    out = out.replace(a, b2)
(S / "c2006_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1994")

out = (S / "c2001_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2001", "C2007"), ("c2001", "c2007")]:
    out = out.replace(a, b2)
(S / "c2007_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2008_scorecard_and_stage.py").write_text(SC2008, encoding="utf-8")
print("scorecard from fixed c1996 product-U2C pattern")
print("OK builder v316 ready")
'''
pre = "SC2008 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v316.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2003_vision_v316", "ashfen", "fernfen", "T316", "1188", "1950", "product_u2c", "retarget_315"]:
    print(needle, needle in (h+pre+tail))
