from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v339.py").read_text(encoding="utf-8")
idx0 = b0.find('# V339 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2146 = " in head0:
    head0 = head0[:head0.find("SC2146 = ")]

theme_pairs = [
    ("netherbrook", "netherdale"), ("NETHERBROOK", "NETHERDALE"),
    ("cedarbrook", "cedardale"), ("CEDARBROOK", "CEDARDALE"),
    ("dawnbrook", "dawndale"), ("DAWNBROOK", "DAWNDALE"),
    ("fernbrook", "ferndale"), ("FERNBROOK", "FERNDALE"),
    ("glenbrook", "glendale"), ("GLENBROOK", "GLENDALE"),
    ("hazebrook", "hazedale"), ("HAZEBROOK", "HAZEDALE"),
    ("jadebrook", "jadedale"), ("JADEBROOK", "JADEDALE"),
    ("knotbrook", "knotdale"), ("KNOTBROOK", "KNOTDALE"),
    ("lakebrook", "lakedale"), ("LAKEBROOK", "LAKEDALE"),
    ("mossbrook", "mossdale"), ("MOSSBROOK", "MOSSDALE"),
    ("pinebrook", "pinedale"), ("PINEBROOK", "PINEDALE"),
    ("quillbrook", "quilldale"), ("QUILLBROOK", "QUILLDALE"),
    ("reedbrook", "reeddale"), ("REEDBROOK", "REEDDALE"),
    ("stonebrook", "stonedale"), ("STONEBROOK", "STONEDALE"),
    ("ashbrook", "ashdale"), ("ASHBROOK", "ASHDALE"),
    ("elmbrook", "elmdale"), ("ELMBROOK", "ELMDALE"),
    ("inkbrook", "inkdale"), ("INKBROOK", "INKDALE"),
    ("oakbrook", "oakdale"), ("OAKBROOK", "OAKDALE"),
]
pairs = [
    ("*brook ; stack mid-band", "*dale ; stack mid-band"),
    ("T339", "T340"), ("TR339", "TR340"), ("HO339", "HO340"),
    ("NEW339", "NEW340"),
    ("V339", "V340"), ("v339", "v340"),
    ("_v339_themes.json", "_v340_themes.json"),
    ("_v338_themes.json", "_v339_themes.json"),
    ("OLD338", "OLD339"),
    ("vision_images_v339", "vision_images_v340"),
    ("VL_GATE_V339", "VL_GATE_V340"), ("vl_gate_v339", "vl_gate_v340"),
    ("C2141", "C2147"), ("c2141", "c2147"),
    ("C2142", "C2148"), ("c2142", "c2148"),
    ("C2143", "C2149"), ("c2143", "c2149"),
    ("_v339c2141", "_v340c2147"),
    ("Harder than V337", "Harder than V338"),
    ("harder than V337", "harder than V338"),
    ("NEW themes vs V337:", "NEW themes vs V338:"),
    ("kept on V339", "kept on V340"),
    ("V339 keeps floor", "V340 keeps floor"),
    ("C2147 design+fixtures; no VL claim", "C2147 design+fixtures; no VL claim"),
    ("retarget_338", "retarget_339"),
    ("*brook", "*dale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHDALE bait 249.59", "ASHDALE bait 247.57")
h = h.replace("CEDARD bait 255.65", "CEDARD bait 255.65")
h = h.replace("DAWND ghost 178.88", "DAWND ghost 178.88")
h = h.replace("GLEND bait 248.58", "GLEND bait 248.58")
h = h.replace("JADED bait 239.49", "JADED bait 239.49")
h = h.replace("NETHERD bait 256.66", "NETHERD bait 256.66")

TR = '''TR340 = [
    [2344.0, 2361.5, 2084.0],[840, 760, 820],[2253.0, 2259.25, 2053.0],[2400.0, 2417.0, 2152.0],
    [2462.0, 2486.0, 2122.0],[2180, 2196, 2080],[490.0, 530.0, 760.0],[2310.0, 2341.75, 2086.0],
    [840.0, 760.0, 820.0],[2377.0, 2365.0, 2083.0],[1,1,0],[0,0,0],
    [2443.0, 2464.5, 2108.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO340 = [
    [2142.0, 2154.75, 2003.0],[640, 660, 820],[2085.0, 2099.5, 1978.0],[2215.0, 2231.0, 2034.0],
    [2238.0, 2249.0, 2027.0],[2038, 2050, 2000],[420.0, 460.0, 740.0],[2126.0, 2147.75, 2003.0],
    [740.0, 780.0, 820.0],[2173.0, 2159.0, 2000.0],[1,1,0],[0,0,0],
    [2208.0, 2223.5, 2013.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR340\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO340\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2152"), ("c2092", "c2152"),
    ("C2090", "C2150"), ("c2090", "c2150"),
    ("C2091", "C2151"), ("c2091", "c2151"),
    ("C2088", "C2148"), ("c2088", "c2148"),
    ("C2089", "C2149"), ("c2089", "c2149"),
    ("C2084", "C2144"), ("c2084", "c2144"),
    ("C2087", "C2147"), ("c2087", "c2147"),
    ("V330", "V340"), ("v330", "v340"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2152"),
    ("*ford", "*dale"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V340 knife = product-U2C (alternating; V339 was confidence-gate)
out = (S / "c2138_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2138", "C2150"), ("c2138", "c2150"),
    ("C2090", "C2150"), ("c2090", "c2150"),
    ("product_u2c_cost_c2150", "product_u2c_cost_c2150"),
    ("u2c_v216", "u2c_v211"),
    ("u2c_c2150", "u2c_c2150"),
]:
    out = out.replace(a, b2)
(S / "c2150_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2138")

out = (S / "c2145_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2145", "C2151"), ("c2145", "c2151")]:
    out = out.replace(a, b2)
(S / "c2151_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2152_scorecard_and_stage.py").write_text(SC2152, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v340 ready")
'''
pre = "SC2152 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v340.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2147_vision_v340", "ashdale", "ferndale", "T340", "1188", "2000", "product_u2c", "retarget_339", "2259.25"]:
    print(needle, needle in (h+pre+tail))
