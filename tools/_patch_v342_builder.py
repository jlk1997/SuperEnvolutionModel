from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v341.py").read_text(encoding="utf-8")
idx0 = b0.find('# V341 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2158 = " in head0:
    head0 = head0[:head0.find("SC2158 = ")]

theme_pairs = [
    ("netherford", "netherhurst"), ("NETHERFORD", "NETHERHURST"),
    ("cedarford", "cedarhurst"), ("CEDARFORD", "CEDARHURST"),
    ("dawnford", "dawnhurst"), ("DAWNFORD", "DAWNHURST"),
    ("fernford", "fernhurst"), ("FERNFORD", "FERNHURST"),
    ("glenford", "glenhurst"), ("GLENFORD", "GLENHURST"),
    ("hazeford", "hazehurst"), ("HAZEFORD", "HAZEHURST"),
    ("jadeford", "jadehurst"), ("JADEFORD", "JADEHURST"),
    ("knotford", "knothurst"), ("KNOTFORD", "KNOTHURST"),
    ("lakeford", "lakehurst"), ("LAKEFORD", "LAKEHURST"),
    ("mossford", "mosshurst"), ("MOSSFORD", "MOSSHURST"),
    ("pineford", "pinehurst"), ("PINEFORD", "PINEHURST"),
    ("quillford", "quillhurst"), ("QUILLFORD", "QUILLHURST"),
    ("reedford", "reedhurst"), ("REEDFORD", "REEDHURST"),
    ("stoneford", "stonehurst"), ("STONEFORD", "STONEHURST"),
    ("ashford", "ashhurst"), ("ASHFORD", "ASHHURST"),
    ("elmford", "elmhurst"), ("ELMFORD", "ELMHURST"),
    ("inkford", "inkhurst"), ("INKFORD", "INKHURST"),
    ("oakford", "oakhurst"), ("OAKFORD", "OAKHURST"),
]
pairs = [
    ("*ford ; stack mid-band", "*hurst ; stack mid-band"),
    ("T341", "T342"), ("TR341", "TR342"), ("HO341", "HO342"),
    ("NEW341", "NEW342"),
    ("V341", "V342"), ("v341", "v342"),
    ("_v341_themes.json", "_v342_themes.json"),
    ("_v340_themes.json", "_v341_themes.json"),
    ("OLD340", "OLD341"),
    ("vision_images_v341", "vision_images_v342"),
    ("VL_GATE_V341", "VL_GATE_V342"), ("vl_gate_v341", "vl_gate_v342"),
    ("C2153", "C2159"), ("c2153", "c2159"),
    ("C2154", "C2160"), ("c2154", "c2160"),
    ("C2155", "C2161"), ("c2155", "c2161"),
    ("_v341c2153", "_v342c2159"),
    ("Harder than V339", "Harder than V340"),
    ("harder than V339", "harder than V340"),
    ("NEW themes vs V339:", "NEW themes vs V340:"),
    ("kept on V341", "kept on V342"),
    ("V341 keeps floor", "V342 keeps floor"),
    ("C2159 design+fixtures; no VL claim", "C2159 design+fixtures; no VL claim"),
    ("retarget_340", "retarget_341"),
    ("*ford", "*hurst"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHURST bait 249.59", "ASHHURST bait 247.57")
h = h.replace("CEDARH bait 257.67", "CEDARH bait 257.67")
h = h.replace("DAWNH ghost 180.90", "DAWNH ghost 180.90")
h = h.replace("GLENH bait 250.60", "GLENH bait 250.60")
h = h.replace("JADEH bait 241.51", "JADEH bait 241.51")
h = h.replace("NETHERH bait 258.68", "NETHERH bait 258.68")

TR = '''TR342 = [
    [2348.0, 2365.5, 2088.0],[840, 760, 820],[2250.0, 2256.25, 2055.0],[2404.0, 2421.0, 2156.0],
    [2466.0, 2490.0, 2126.0],[2184, 2200, 2084],[490.0, 530.0, 760.0],[2314.0, 2345.75, 2090.0],
    [840.0, 760.0, 820.0],[2381.0, 2369.0, 2087.0],[1,1,0],[0,0,0],
    [2447.0, 2468.5, 2112.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO342 = [
    [2146.0, 2158.75, 2007.0],[640, 660, 820],[2089.0, 2103.5, 1982.0],[2219.0, 2235.0, 2038.0],
    [2236.0, 2247.0, 2031.0],[2042, 2054, 2004],[420.0, 460.0, 740.0],[2130.0, 2151.75, 2007.0],
    [740.0, 780.0, 820.0],[2177.0, 2163.0, 2004.0],[1,1,0],[0,0,0],
    [2212.0, 2227.5, 2017.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR342\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO342\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2164"), ("c2092", "c2164"),
    ("C2090", "C2162"), ("c2090", "c2162"),
    ("C2091", "C2163"), ("c2091", "c2163"),
    ("C2088", "C2160"), ("c2088", "c2160"),
    ("C2089", "C2161"), ("c2089", "c2161"),
    ("C2084", "C2156"), ("c2084", "c2156"),
    ("C2087", "C2159"), ("c2087", "c2159"),
    ("V330", "V342"), ("v330", "v342"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2164"),
    ("*ford", "*hurst"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V342 knife = product-U2C (alternating; V341 was confidence-gate)
out = (S / "c2150_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2150", "C2162"), ("c2150", "c2162"),
    ("C2090", "C2162"), ("c2090", "c2162"),
    ("product_u2c_cost_c2162", "product_u2c_cost_c2162"),
    ("u2c_v218", "u2c_v211"),
    ("u2c_c2162", "u2c_c2162"),
]:
    out = out.replace(a, b2)
(S / "c2162_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2150")

out = (S / "c2157_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2157", "C2163"), ("c2157", "c2163")]:
    out = out.replace(a, b2)
(S / "c2163_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2164_scorecard_and_stage.py").write_text(SC2164, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v342 ready")
'''
pre = "SC2164 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v342.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2159_vision_v342", "ashhurst", "fernhurst", "T342", "1188", "2004", "product_u2c", "retarget_341", "2256.25"]:
    print(needle, needle in (h+pre+tail))
