from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v353.py").read_text(encoding="utf-8")
idx0 = b0.find("# V353 knife = confidence-gate")
if idx0 < 0:
    raise SystemExit("knife not found")
head0 = b0[:idx0]
if "SC2230 = " in head0:
    head0 = head0[:head0.find("SC2230 = ")]
theme_pairs = [
    ("netherhurst", "nethermere"), ("NETHERHURST", "NETHERMERE"),
    ("cedarhurst", "cedarmere"), ("CEDARHURST", "CEDARMERE"),
    ("dawnhurst", "dawnmere"), ("DAWNHURST", "DAWNMERE"),
    ("fernhurst", "fernmere"), ("FERNHURST", "FERNMERE"),
    ("glenhurst", "glenmere"), ("GLENHURST", "GLENMERE"),
    ("hazehurst", "hazemere"), ("HAZEHURST", "HAZEMERE"),
    ("jadehurst", "jademere"), ("JADEHURST", "JADEMERE"),
    ("knothurst", "knotmere"), ("KNOTHURST", "KNOTMERE"),
    ("lakehurst", "lakemere"), ("LAKEHURST", "LAKEMERE"),
    ("mosshurst", "mossmere"), ("MOSSHURST", "MOSSMERE"),
    ("pinehurst", "pinemere"), ("PINEHURST", "PINEMERE"),
    ("quillhurst", "quillmere"), ("QUILLHURST", "QUILLMERE"),
    ("reedhurst", "reedmere"), ("REEDHURST", "REEDMERE"),
    ("stonehurst", "stonemere"), ("STONEHURST", "STONEMERE"),
    ("ashhurst", "ashmere"), ("ASHHURST", "ASHMERE"),
    ("elmhurst", "elmmere"), ("ELMHURST", "ELMMERE"),
    ("inkhurst", "inkmere"), ("INKHURST", "INKMERE"),
    ("oakhurst", "oakmere"), ("OAKHURST", "OAKMERE"),
]
pairs = [
    ("*hurst ; stack mid-band", "*mere ; stack mid-band"),
    ("T353", "T354"), ("TR353", "TR354"), ("HO353", "HO354"),
    ("NEW353", "NEW354"),
    ("V353", "V354"), ("v353", "v354"),
    ("_v353_themes.json", "_v354_themes.json"),
    ("_v352_themes.json", "_v353_themes.json"),
    ("OLD352", "OLD353"),
    ("vision_images_v353", "vision_images_v354"),
    ("VL_GATE_V353", "VL_GATE_V354"), ("vl_gate_v353", "vl_gate_v354"),
    ("C2225", "C2231"), ("c2225", "c2231"),
    ("C2226", "C2232"), ("c2226", "c2232"),
    ("C2227", "C2233"), ("c2227", "c2233"),
    ("_v353c2225", "_v354c2231"),
    ("Harder than V351", "Harder than V352"),
    ("harder than V351", "harder than V352"),
    ("NEW themes vs V351:", "NEW themes vs V352:"),
    ("kept on V353", "kept on V354"),
    ("V353 keeps floor", "V354 keeps floor"),
    ("C2225 design+fixtures; no VL claim", "C2231 design+fixtures; no VL claim"),
    ("retarget_352", "retarget_353"),
    ("*hurst", "*mere"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)
h = h.replace("ASHHURST bait 254.64", "ASHMERE bait 255.65")
h = h.replace("CEDARH bait 268.78", "CEDARM bait 269.79")
h = h.replace("DAWNH ghost 191.02", "DAWNM ghost 192.03")
h = h.replace("GLENH bait 261.71", "GLENM bait 262.72")
h = h.replace("JADEH bait 252.62", "JADEM bait 253.63")
h = h.replace("NETHERH bait 269.79", "NETHERM bait 270.80")
TR = """TR354 = [
    [2372.0, 2389.5, 2112.0],[840, 760, 820],[2258.0, 2259.25, 2049.0],[2428.0, 2445.0, 2180.0],
    [2490.0, 2494.0, 2150.0],[2208, 2224, 2108],[490.0, 530.0, 760.0],[2338.0, 2369.75, 2114.0],
    [840.0, 760.0, 820.0],[2405.0, 2393.0, 2111.0],[1,1,0],[0,0,0],
    [2463.0, 2482.5, 2110.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO354 = [
    [2170.0, 2182.75, 2031.0],[640, 660, 820],[2113.0, 2127.5, 2006.0],[2243.0, 2259.0, 2062.0],
    [2247.0, 2258.0, 2055.0],[2066, 2078, 2028],[420.0, 460.0, 740.0],[2154.0, 2175.75, 2031.0],
    [740.0, 780.0, 820.0],[2201.0, 2187.0, 2028.0],[1,1,0],[0,0,0],
    [2231.0, 2245.5, 2035.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
h = re.sub(r"TR354\s*=\s*\[[\s\S]*?\n\]", TR, h, count=1)
h = re.sub(r"HO354\s*=\s*\[[\s\S]*?\n\]", HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2236"), ("c2092", "c2236"),
    ("C2090", "C2234"), ("c2090", "c2234"),
    ("C2091", "C2235"), ("c2091", "c2235"),
    ("C2088", "C2232"), ("c2088", "c2232"),
    ("C2089", "C2233"), ("c2089", "c2233"),
    ("C2084", "C2228"), ("c2084", "c2228"),
    ("C2087", "C2231"), ("c2087", "c2231"),
    ("V330", "V354"), ("v330", "v354"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2236"),
    ("*croft", "*mere"),
]:
    sc_body = sc_body.replace(a, b2)
tail = r'''# V354 knife = product-U2C (alternating; V353 was confidence-gate)
out = (S / "c2222_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2222", "C2234"), ("c2222", "c2234"),
    ("C2090", "C2234"), ("c2090", "c2234"),
    ("product_u2c_cost_c2234", "product_u2c_cost_c2234"),
    ("u2c_v178", "u2c_v167"),
    ("u2c_c2234", "u2c_c2234"),
]:
    out = out.replace(a, b2)
(S / "c2234_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2222")

out = (S / "c2229_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2229", "C2235"), ("c2229", "c2235")]:
    out = out.replace(a, b2)
(S / "c2235_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2236_scorecard_and_stage.py").write_text(SC2236, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v354 ready")
'''
pre = "SC2236 = " + repr(sc_body) + "\n"
text = h + pre + tail
(ROOT / "tools/_build_v354.py").write_text(text, encoding="utf-8")
print("wrote", len(text))
for needle in ["c2231_vision_v354", "ashmere", "fernmere", "T354", "1188", "2028", "product_u2c", "retarget_353", "2259.25"]:
    print(needle, needle in text)
