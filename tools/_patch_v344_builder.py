from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v343.py").read_text(encoding="utf-8")
idx0 = b0.find('# V343 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2170 = " in head0:
    head0 = head0[:head0.find("SC2170 = ")]

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
    ("T343", "T344"), ("TR343", "TR344"), ("HO343", "HO344"),
    ("NEW343", "NEW344"),
    ("V343", "V344"), ("v343", "v344"),
    ("_v343_themes.json", "_v344_themes.json"),
    ("_v342_themes.json", "_v343_themes.json"),
    ("OLD342", "OLD343"),
    ("vision_images_v343", "vision_images_v344"),
    ("VL_GATE_V343", "VL_GATE_V344"), ("vl_gate_v343", "vl_gate_v344"),
    ("C2165", "C2171"), ("c2165", "c2171"),
    ("C2166", "C2172"), ("c2166", "c2172"),
    ("C2167", "C2173"), ("c2167", "c2173"),
    ("_v343c2165", "_v344c2171"),
    ("Harder than V341", "Harder than V342"),
    ("harder than V341", "harder than V342"),
    ("NEW themes vs V341:", "NEW themes vs V342:"),
    ("kept on V343", "kept on V344"),
    ("V343 keeps floor", "V344 keeps floor"),
    ("C2171 design+fixtures; no VL claim", "C2171 design+fixtures; no VL claim"),
    ("retarget_342", "retarget_343"),
    ("*mere", "*vale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHVALE bait 249.59", "ASHVALE bait 247.57")
h = h.replace("CEDARV bait 259.69", "CEDARV bait 259.69")
h = h.replace("DAWNV ghost 182.92", "DAWNV ghost 182.92")
h = h.replace("GLENV bait 252.62", "GLENV bait 252.62")
h = h.replace("JADEV bait 243.53", "JADEV bait 243.53")
h = h.replace("NETHERV bait 260.70", "NETHERV bait 260.70")

TR = '''TR344 = [
    [2352.0, 2369.5, 2092.0],[840, 760, 820],[2252.0, 2258.25, 2057.0],[2408.0, 2425.0, 2160.0],
    [2470.0, 2494.0, 2130.0],[2188, 2204, 2088],[490.0, 530.0, 760.0],[2318.0, 2349.75, 2094.0],
    [840.0, 760.0, 820.0],[2385.0, 2373.0, 2091.0],[1,1,0],[0,0,0],
    [2451.0, 2472.5, 2116.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO344 = [
    [2150.0, 2162.75, 2011.0],[640, 660, 820],[2093.0, 2107.5, 1986.0],[2223.0, 2239.0, 2042.0],
    [2234.0, 2245.0, 2035.0],[2046, 2058, 2008],[420.0, 460.0, 740.0],[2134.0, 2155.75, 2011.0],
    [740.0, 780.0, 820.0],[2181.0, 2167.0, 2008.0],[1,1,0],[0,0,0],
    [2216.0, 2231.5, 2021.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR344\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO344\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2176"), ("c2092", "c2176"),
    ("C2090", "C2174"), ("c2090", "c2174"),
    ("C2091", "C2175"), ("c2091", "c2175"),
    ("C2088", "C2172"), ("c2088", "c2172"),
    ("C2089", "C2173"), ("c2089", "c2173"),
    ("C2084", "C2168"), ("c2084", "c2168"),
    ("C2087", "C2171"), ("c2087", "c2171"),
    ("V330", "V344"), ("v330", "v344"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2176"),
    ("*mere", "*vale"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V344 knife = product-U2C (alternating; V343 was confidence-gate)
out = (S / "c2162_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2162", "C2174"), ("c2162", "c2174"),
    ("C2090", "C2174"), ("c2090", "c2174"),
    ("product_u2c_cost_c2174", "product_u2c_cost_c2174"),
    ("u2c_v220", "u2c_v211"),
    ("u2c_c2174", "u2c_c2174"),
]:
    out = out.replace(a, b2)
(S / "c2174_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2162")

out = (S / "c2169_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2169", "C2175"), ("c2169", "c2175")]:
    out = out.replace(a, b2)
(S / "c2175_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2176_scorecard_and_stage.py").write_text(SC2176, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v344 ready")
'''
pre = "SC2176 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v344.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2171_vision_v344", "ashvale", "fernvale", "T344", "1188", "2008", "product_u2c", "retarget_343", "2258.25"]:
    print(needle, needle in (h+pre+tail))
