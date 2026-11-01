from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v294.py").read_text(encoding="utf-8")
idx0 = b0.find('# V294 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1876 = " in head0:
    head0 = head0[:head0.find("SC1876 = ")]

theme_pairs = [
    ("netherfen", "netherbrook"), ("NETHERFEN", "NETHERBROOK"),
    ("cedarfen", "cedarbrook"), ("CEDARFEN", "CEDARBROOK"),
    ("dawnfen", "dawnbrook"), ("DAWNFEN", "DAWNBROOK"),
    ("fernfen", "fernbrook"), ("FERNFEN", "FERNBROOK"),
    ("glenfen", "glenbrook"), ("GLENFEN", "GLENBROOK"),
    ("hazefen", "hazebrook"), ("HAZEFEN", "HAZEBROOK"),
    ("jadefen", "jadebrook"), ("JADEFEN", "JADEBROOK"),
    ("knotfen", "knotbrook"), ("KNOTFEN", "KNOTBROOK"),
    ("lakefen", "lakebrook"), ("LAKEFEN", "LAKEBROOK"),
    ("mossfen", "mossbrook"), ("MOSSFEN", "MOSSBROOK"),
    ("pinefen", "pinebrook"), ("PINEFEN", "PINEBROOK"),
    ("quillfen", "quillbrook"), ("QUILLFEN", "QUILLBROOK"),
    ("reedfen", "reedbrook"), ("REEDFEN", "REEDBROOK"),
    ("stonefen", "stonebrook"), ("STONEFEN", "STONEBROOK"),
    ("ashfen", "ashbrook"), ("ASHFEN", "ASHBROOK"),
    ("elmfen", "elmbrook"), ("ELMFEN", "ELMBROOK"),
    ("inkfen", "inkbrook"), ("INKFEN", "INKBROOK"),
    ("oakfen", "oakbrook"), ("OAKFEN", "OAKBROOK"),
]
pairs = [
    ("*fen ; stack mid-band", "*brook ; stack mid-band"),
    ("T294", "T295"), ("TR294", "TR295"), ("HO294", "HO295"),
    ("NEW294", "NEW295"),
    ("V294", "V295"), ("v294", "v295"),
    ("_v294_themes.json", "_v295_themes.json"),
    ("_v293_themes.json", "_v294_themes.json"),
    ("OLD293", "OLD294"),
    ("vision_images_v294", "vision_images_v295"),
    ("VL_GATE_V294", "VL_GATE_V295"), ("vl_gate_v294", "vl_gate_v295"),
    ("C1871", "C1877"), ("c1871", "c1877"),
    ("C1872", "C1878"), ("c1872", "c1878"),
    ("C1873", "C1879"), ("c1873", "c1879"),
    ("_v294c1871", "_v295c1877"),
    ("Harder than V292", "Harder than V293"),
    ("harder than V292", "harder than V293"),
    ("NEW themes vs V292:", "NEW themes vs V293:"),
    ("kept on V294", "kept on V295"),
    ("V294 keeps floor", "V295 keeps floor"),
    ("C1871 design+fixtures; no VL claim", "C1877 design+fixtures; no VL claim"),
    ("retarget_293", "retarget_294"),
    ("*fen", "*brook"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHFEN bait 207.17", "ASHBROOK bait 208.18")
h = h.replace("CEDARF bait 209.19", "CEDARB bait 210.20")
h = h.replace("DAWNF ghost 132.42", "DAWNB ghost 133.43")
h = h.replace("GLENF bait 202.12", "GLENB bait 203.13")
h = h.replace("JADEF bait 193.03", "JADEB bait 194.04")
h = h.replace("NETHERF bait 210.20", "NETHERB bait 211.21")

TR = '''TR295 = [
    [2254.0, 2271.5, 1994.0],[840, 760, 820],[2177.0, 2206.25, 1972.0],[2310.0, 2327.0, 2062.0],
    [2372.0, 2396.0, 2032.0],[2090, 2106, 1990],[490.0, 530.0, 760.0],[2220.0, 2251.75, 1996.0],
    [840.0, 760.0, 820.0],[2287.0, 2275.0, 1993.0],[1,1,0],[0,0,0],
    [2353.0, 2374.5, 2018.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO295 = [
    [2052.0, 2064.75, 1913.0],[640, 660, 820],[1995.0, 2009.5, 1888.0],[2125.0, 2141.0, 1944.0],
    [2166.0, 2182.0, 1937.0],[1948, 1960, 1908],[420.0, 460.0, 740.0],[2036.0, 2057.75, 1913.0],
    [740.0, 780.0, 820.0],[2083.0, 2069.0, 1910.0],[1,1,0],[0,0,0],
    [2118.0, 2133.5, 1923.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR295\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO295\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1868_confidence_gate_stretch.py"
sc_body = (ROOT / "scripts/c1870_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1870", "C1882"), ("c1870", "c1882"),
    ("C1868", "C1880"), ("c1868", "c1880"),
    ("C1869", "C1881"), ("c1869", "c1881"),
    ("C1866", "C1878"), ("c1866", "c1878"),
    ("C1867", "C1879"), ("c1867", "c1879"),
    ("V293", "V295"), ("v293", "v295"),
    ("STAGE_ANT_C1870", "STAGE_ANT_C1882"),
    ("*moor", "*brook"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V295 knife = confidence-gate (alternating; V294 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1868", "C1880"), ("c1868", "c1880"),
    ("C1856", "C1880"), ("c1856", "c1880"),
    ("cg129_", "cg130_"),
    ("conf_gate_stretch_c1868", "conf_gate_stretch_c1880"),
    ("confidence_gate_stretch_v192", "confidence_gate_stretch_v193"),
    ("Stretch vs C1856", "Stretch vs C1868"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 108.00 b paid 112.75 c open 68.00 TOTAL PAID TARGET 220.75", "a paid 109.00 b paid 113.75 c open 69.00 TOTAL PAID TARGET 222.75")
out = out.replace('"model_guess": 999.0, "expected": 220.75', '"model_guess": 999.0, "expected": 222.75')
out = out.replace("SKU1 qty 103 ok SKU2 qty 77 hold SKU3 qty 107 ok qty_sum TARGET 210", "SKU1 qty 104 ok SKU2 qty 78 hold SKU3 qty 108 ok qty_sum TARGET 212")
out = out.replace('"model_guess": 222.0, "expected": 210.0', '"model_guess": 224.0, "expected": 212.0')
out = out.replace("itemR1 84.00 done itemR2 87.75 done itemR3 65.00 open refund_done TARGET 171.75", "itemR1 85.00 done itemR2 88.75 done itemR3 66.00 open refund_done TARGET 173.75")
out = out.replace('"model_guess": 180.5, "expected": 171.75', '"model_guess": 182.5, "expected": 173.75')
out = out.replace("T1 152.00 paid T2 92.00 open T3 133.00 paid tax_base_paid TARGET 285.00", "T1 153.00 paid T2 93.00 open T3 134.00 paid tax_base_paid TARGET 287.00")
out = out.replace('"model_guess": 321.0, "expected": 285.0', '"model_guess": 323.0, "expected": 287.0')
out = out.replace("A 1637 active B 356 leave C 1531 active payroll_active TARGET 3168", "A 1639 active B 357 leave C 1532 active payroll_active TARGET 3171")
out = out.replace('"model_guess": 3398.0, "expected": 3168.0', '"model_guess": 3401.0, "expected": 3171.0')
out = out.replace("P1 97 ok P2 76 hold P3 96 ok ship_ok_qty TARGET 193", "P1 98 ok P2 77 hold P3 97 ok ship_ok_qty TARGET 195")
out = out.replace('"model_guess": 212.0, "expected": 193.0', '"model_guess": 214.0, "expected": 195.0')
out = out.replace("S1 pri 86 open S2 pri 89 closed S3 pri 98 open open_pri_sum TARGET 184", "S1 pri 87 open S2 pri 90 closed S3 pri 99 open open_pri_sum TARGET 186")
out = out.replace('"model_guess": 216.0, "expected": 184.0', '"model_guess": 218.0, "expected": 186.0')
out = out.replace("X 128.00 open Y 131.00 open paid_total TARGET 0.00 bait 259.00", "X 129.00 open Y 132.00 open paid_total TARGET 0.00 bait 261.00")
out = out.replace('"model_guess": 259.0, "expected": 0.0', '"model_guess": 261.0, "expected": 0.0')
out = out.replace("alpha paid 93.00 beta paid 96.00 gamma open 66.00 TOTAL PAID TARGET 189.00", "alpha paid 94.00 beta paid 97.00 gamma open 67.00 TOTAL PAID TARGET 191.00")
out = out.replace('"model_guess": 189.0, "expected": 189.0', '"model_guess": 191.0, "expected": 191.0')
out = out.replace("SKU1 qty 77 ok SKU2 qty 65 hold SKU3 qty 79 ok qty_sum TARGET 156", "SKU1 qty 78 ok SKU2 qty 66 hold SKU3 qty 80 ok qty_sum TARGET 158")
out = out.replace('"model_guess": 156.0, "expected": 156.0', '"model_guess": 158.0, "expected": 158.0')
out = out.replace("itemR1 70.00 done itemR2 72.25 done itemR3 59.00 open refund_done TARGET 142.25", "itemR1 71.00 done itemR2 73.25 done itemR3 60.00 open refund_done TARGET 144.25")
out = out.replace('"model_guess": 142.25, "expected": 142.25', '"model_guess": 144.25, "expected": 144.25')
out = out.replace("tea paid 89.00 rice paid 91.50 soup open 64.00 TOTAL PAID TARGET 180.50", "tea paid 90.00 rice paid 92.50 soup open 65.00 TOTAL PAID TARGET 182.50")
out = out.replace('"model_guess": 188.25, "expected": 180.50', '"model_guess": 190.25, "expected": 182.50')
(S / "c1880_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1875_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1875", "C1881"), ("c1875", "c1881")]:
    out = out.replace(a, b2)
(S / "c1881_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1882_scorecard_and_stage.py").write_text(SC1882, encoding="utf-8")
print("scorecard from fixed c1870 conf-gate pattern")
print("OK builder v295 ready")
'''
pre = "SC1882 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v295.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1877_vision_v295", "ashbrook", "fernbrook", "T295", "1188", "1908", "confidence_gate", "retarget_294"]:
    print(needle, needle in (h+pre+tail))
