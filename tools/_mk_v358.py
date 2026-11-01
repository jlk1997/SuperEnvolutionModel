from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v357.py").read_text(encoding="utf-8")
idx0 = b0.find("# V357 knife = confidence-gate")
if idx0 < 0:
    raise SystemExit("knife not found")
head0 = b0[:idx0]
if "SC2254 = " in head0:
    head0 = head0[:head0.find("SC2254 = ")]
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
    ("T357", "T358"), ("TR357", "TR358"), ("HO357", "HO358"),
    ("NEW357", "NEW358"),
    ("V357", "V358"), ("v357", "v358"),
    ("_v357_themes.json", "_v358_themes.json"),
    ("_v356_themes.json", "_v357_themes.json"),
    ("OLD356", "OLD357"),
    ("vision_images_v357", "vision_images_v358"),
    ("VL_GATE_V357", "VL_GATE_V358"), ("vl_gate_v357", "vl_gate_v358"),
    ("C2249", "C2255"), ("c2249", "c2255"),
    ("C2250", "C2256"), ("c2250", "c2256"),
    ("C2251", "C2257"), ("c2251", "c2257"),
    ("_v357c2249", "_v358c2255"),
    ("Harder than V355", "Harder than V356"),
    ("harder than V355", "harder than V356"),
    ("NEW themes vs V355:", "NEW themes vs V356:"),
    ("kept on V357", "kept on V358"),
    ("V357 keeps floor", "V358 keeps floor"),
    ("C2249 design+fixtures; no VL claim", "C2255 design+fixtures; no VL claim"),
    ("retarget_356", "retarget_357"),
    ("*holm", "*wick"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)
h = h.replace("ASHHOLM bait 258.68", "ASHWICK bait 259.69")
h = h.replace("CEDARH bait 272.82", "CEDARW bait 273.83")
h = h.replace("DAWNH ghost 195.06", "DAWNW ghost 196.07")
h = h.replace("GLENH bait 265.75", "GLENW bait 266.76")
h = h.replace("JADEH bait 256.66", "JADEW bait 257.67")
h = h.replace("NETHERH bait 273.83", "NETHERW bait 274.84")
TR = """TR358 = [
    [2380.0, 2397.5, 2120.0],[840, 760, 820],[2253.0, 2254.25, 2045.0],[2436.0, 2453.0, 2188.0],
    [2498.0, 2497.0, 2158.0],[2216, 2232, 2116],[490.0, 530.0, 760.0],[2346.0, 2377.75, 2122.0],
    [840.0, 760.0, 820.0],[2413.0, 2401.0, 2119.0],[1,1,0],[0,0,0],
    [2457.0, 2476.5, 2102.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO358 = [
    [2178.0, 2190.75, 2039.0],[640, 660, 820],[2121.0, 2135.5, 2014.0],[2251.0, 2267.0, 2070.0],
    [2255.0, 2266.0, 2063.0],[2074, 2086, 2036],[420.0, 460.0, 740.0],[2162.0, 2183.75, 2039.0],
    [740.0, 780.0, 820.0],[2209.0, 2195.0, 2036.0],[1,1,0],[0,0,0],
    [2239.0, 2253.5, 2043.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
h = re.sub(r"TR358\s*=\s*\[[\s\S]*?\n\]", TR, h, count=1)
h = re.sub(r"HO358\s*=\s*\[[\s\S]*?\n\]", HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2260"), ("c2092", "c2260"),
    ("C2090", "C2258"), ("c2090", "c2258"),
    ("C2091", "C2259"), ("c2091", "c2259"),
    ("C2088", "C2256"), ("c2088", "c2256"),
    ("C2089", "C2257"), ("c2089", "c2257"),
    ("C2084", "C2252"), ("c2084", "c2252"),
    ("C2087", "C2255"), ("c2087", "c2255"),
    ("V330", "V358"), ("v330", "v358"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2260"),
    ("*croft", "*wick"),
]:
    sc_body = sc_body.replace(a, b2)
tail = r'''# V358 knife = product-U2C (alternating; V357 was confidence-gate)
out = (S / "c2246_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2246", "C2258"), ("c2246", "c2258"),
    ("C2090", "C2258"), ("c2090", "c2258"),
    ("product_u2c_cost_c2258", "product_u2c_cost_c2258"),
    ("u2c_v156", "u2c_v145"),
    ("u2c_c2258", "u2c_c2258"),
]:
    out = out.replace(a, b2)
(S / "c2258_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2246")

out = (S / "c2253_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2253", "C2259"), ("c2253", "c2259")]:
    out = out.replace(a, b2)
(S / "c2259_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2260_scorecard_and_stage.py").write_text(SC2260, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v358 ready")
'''
pre = "SC2260 = " + repr(sc_body) + "\n"
text = h + pre + tail
(ROOT / "tools/_build_v358.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2255_vision_v358", "ashwick", "fernwick", "T358", "1188", "2036", "product_u2c", "retarget_357", "2254.25"]:
    print(needle, needle in text)
