from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v321.py").read_text(encoding="utf-8")
idx0 = b0.find('# V321 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2038 = " in head0:
    head0 = head0[:head0.find("SC2038 = ")]

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
    ("T321", "T322"), ("TR321", "TR322"), ("HO321", "HO322"),
    ("NEW321", "NEW322"),
    ("V321", "V322"), ("v321", "v322"),
    ("_v321_themes.json", "_v322_themes.json"),
    ("_v320_themes.json", "_v321_themes.json"),
    ("OLD320", "OLD321"),
    ("vision_images_v321", "vision_images_v322"),
    ("VL_GATE_V321", "VL_GATE_V322"), ("vl_gate_v321", "vl_gate_v322"),
    ("C2033", "C2039"), ("c2033", "c2039"),
    ("C2034", "C2040"), ("c2034", "c2040"),
    ("C2035", "C2041"), ("c2035", "c2041"),
    ("_v321c2033", "_v322c2039"),
    ("Harder than V319", "Harder than V320"),
    ("harder than V319", "harder than V320"),
    ("NEW themes vs V319:", "NEW themes vs V320:"),
    ("kept on V321", "kept on V322"),
    ("V321 keeps floor", "V322 keeps floor"),
    ("C2033 design+fixtures; no VL claim", "C2039 design+fixtures; no VL claim"),
    ("retarget_320", "retarget_321"),
    ("*mere", "*vale"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMERE bait 234.44", "ASHVALE bait 235.45")
h = h.replace("CEDARM bait 236.46", "CEDARV bait 237.47")
h = h.replace("DAWNM ghost 159.69", "DAWNV ghost 160.70")
h = h.replace("GLENM bait 229.39", "GLENV bait 230.40")
h = h.replace("JADEM bait 220.30", "JADEV bait 221.31")
h = h.replace("NETHERM bait 237.47", "NETHERV bait 238.48")

TR = '''TR322 = [
    [2308.0, 2325.5, 2048.0],[840, 760, 820],[2231.0, 2260.25, 2026.0],[2364.0, 2381.0, 2116.0],
    [2426.0, 2450.0, 2086.0],[2144, 2160, 2044],[490.0, 530.0, 760.0],[2274.0, 2305.75, 2050.0],
    [840.0, 760.0, 820.0],[2341.0, 2329.0, 2047.0],[1,1,0],[0,0,0],
    [2407.0, 2428.5, 2072.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO322 = [
    [2106.0, 2118.75, 1967.0],[640, 660, 820],[2049.0, 2063.5, 1942.0],[2179.0, 2195.0, 1998.0],
    [2220.0, 2236.0, 1991.0],[2002, 2014, 1962],[420.0, 460.0, 740.0],[2090.0, 2111.75, 1967.0],
    [740.0, 780.0, 820.0],[2137.0, 2123.0, 1964.0],[1,1,0],[0,0,0],
    [2172.0, 2187.5, 1977.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR322\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO322\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2032_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2032", "C2044"), ("c2032", "c2044"),
    ("C2030", "C2042"), ("c2030", "c2042"),
    ("C2031", "C2043"), ("c2031", "c2043"),
    ("C2028", "C2040"), ("c2028", "c2040"),
    ("C2029", "C2041"), ("c2029", "c2041"),
    ("C2024", "C2036"), ("c2024", "c2036"),
    ("C2027", "C2039"), ("c2027", "c2039"),
    ("V320", "V322"), ("v320", "v322"),
    ("STAGE_ANT_C2032", "STAGE_ANT_C2044"),
    ("*hurst", "*vale"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V322 knife = product-U2C (alternating; V321 was confidence-gate)
out = (S / "c2030_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2030", "C2042"), ("c2030", "c2042"),
    ("C2018", "C2042"), ("c2018", "c2042"),
    ("product_u2c_cost_c2030", "product_u2c_cost_c2042"),
    ("u2c_v204", "u2c_v205"),
    ("u2c_c2030", "u2c_c2042"),
]:
    out = out.replace(a, b2)
(S / "c2042_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2030")

out = (S / "c2037_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2037", "C2043"), ("c2037", "c2043")]:
    out = out.replace(a, b2)
(S / "c2043_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2044_scorecard_and_stage.py").write_text(SC2044, encoding="utf-8")
print("scorecard from fixed c2032 product-U2C pattern")
print("OK builder v322 ready")
'''
pre = "SC2044 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v322.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2039_vision_v322", "ashvale", "fernvale", "T322", "1188", "1962", "product_u2c", "retarget_321"]:
    print(needle, needle in (h+pre+tail))
