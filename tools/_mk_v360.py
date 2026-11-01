from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v359.py").read_text(encoding="utf-8")
idx0 = b0.find("# V359 knife = confidence-gate")
if idx0 < 0:
    raise SystemExit("knife not found")
head0 = b0[:idx0]
if "SC2266 = " in head0:
    head0 = head0[:head0.find("SC2266 = ")]
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
    ("T359", "T360"), ("TR359", "TR360"), ("HO359", "HO360"),
    ("NEW359", "NEW360"),
    ("V359", "V360"), ("v359", "v360"),
    ("_v359_themes.json", "_v360_themes.json"),
    ("_v358_themes.json", "_v359_themes.json"),
    ("OLD358", "OLD359"),
    ("vision_images_v359", "vision_images_v360"),
    ("VL_GATE_V359", "VL_GATE_V360"), ("vl_gate_v359", "vl_gate_v360"),
    ("C2261", "C2267"), ("c2261", "c2267"),
    ("C2262", "C2268"), ("c2262", "c2268"),
    ("C2263", "C2269"), ("c2263", "c2269"),
    ("_v359c2261", "_v360c2267"),
    ("Harder than V357", "Harder than V358"),
    ("harder than V357", "harder than V358"),
    ("NEW themes vs V357:", "NEW themes vs V358:"),
    ("kept on V359", "kept on V360"),
    ("V359 keeps floor", "V360 keeps floor"),
    ("C2261 design+fixtures; no VL claim", "C2267 design+fixtures; no VL claim"),
    ("retarget_358", "retarget_359"),
    ("*moor", "*fen"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)
h = h.replace("ASHMOOR bait 260.70", "ASHFEN bait 261.71")
h = h.replace("CEDARM bait 274.84", "CEDARF bait 275.85")
h = h.replace("DAWNM ghost 197.08", "DAWNF ghost 198.09")
h = h.replace("GLENM bait 267.77", "GLENF bait 268.78")
h = h.replace("JADEM bait 258.68", "JADEF bait 259.69")
h = h.replace("NETHERM bait 275.85", "NETHERF bait 276.86")
TR = """TR360 = [
    [2384.0, 2401.5, 2124.0],[840, 760, 820],[2255.0, 2257.25, 2043.0],[2440.0, 2457.0, 2192.0],
    [2497.0, 2493.0, 2162.0],[2220, 2236, 2120],[490.0, 530.0, 760.0],[2350.0, 2381.75, 2126.0],
    [840.0, 760.0, 820.0],[2417.0, 2405.0, 2123.0],[1,1,0],[0,0,0],
    [2451.0, 2470.5, 2098.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO360 = [
    [2182.0, 2194.75, 2043.0],[640, 660, 820],[2125.0, 2139.5, 2018.0],[2255.0, 2271.0, 2074.0],
    [2259.0, 2270.0, 2067.0],[2078, 2090, 2040],[420.0, 460.0, 740.0],[2166.0, 2187.75, 2043.0],
    [740.0, 780.0, 820.0],[2213.0, 2199.0, 2040.0],[1,1,0],[0,0,0],
    [2243.0, 2257.5, 2047.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
h = re.sub(r"TR360\s*=\s*\[[\s\S]*?\n\]", TR, h, count=1)
h = re.sub(r"HO360\s*=\s*\[[\s\S]*?\n\]", HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2272"), ("c2092", "c2272"),
    ("C2090", "C2270"), ("c2090", "c2270"),
    ("C2091", "C2271"), ("c2091", "c2271"),
    ("C2088", "C2268"), ("c2088", "c2268"),
    ("C2089", "C2269"), ("c2089", "c2269"),
    ("C2084", "C2264"), ("c2084", "c2264"),
    ("C2087", "C2267"), ("c2087", "c2267"),
    ("V330", "V360"), ("v330", "v360"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2272"),
    ("*croft", "*fen"),
]:
    sc_body = sc_body.replace(a, b2)
tail = r'''# V360 knife = product-U2C (alternating; V359 was confidence-gate)
out = (S / "c2258_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2258", "C2270"), ("c2258", "c2270"),
    ("C2090", "C2270"), ("c2090", "c2270"),
    ("product_u2c_cost_c2270", "product_u2c_cost_c2270"),
    ("u2c_v145", "u2c_v134"),
    ("u2c_c2270", "u2c_c2270"),
]:
    out = out.replace(a, b2)
(S / "c2270_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2258")

out = (S / "c2265_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2265", "C2271"), ("c2265", "c2271")]:
    out = out.replace(a, b2)
(S / "c2271_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2272_scorecard_and_stage.py").write_text(SC2272, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v360 ready")
'''
pre = "SC2272 = " + repr(sc_body) + "\n"
text = h + pre + tail
(ROOT / "tools/_build_v360.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2267_vision_v360", "ashfen", "fernfen", "T360", "1188", "2040", "product_u2c", "retarget_359", "2257.25"]:
    print(needle, needle in text)
