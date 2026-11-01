from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v264.py").read_text(encoding="utf-8")
idx0 = b0.find('# V264 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
    ("T264", "T265"), ("TR264", "TR265"), ("HO264", "HO265"),
    ("NEW264", "NEW265"),
    ("V264", "V265"), ("v264", "v265"),
    ("_v264_themes.json", "_v265_themes.json"),
    ("_v263_themes.json", "_v264_themes.json"),
    ("OLD263", "OLD264"),
    ("vision_images_v264", "vision_images_v265"),
    ("VL_GATE_V264", "VL_GATE_V265"), ("vl_gate_v264", "vl_gate_v265"),
    ("C1691", "C1697"), ("c1691", "c1697"),
    ("C1692", "C1698"), ("c1692", "c1698"),
    ("C1693", "C1699"), ("c1693", "c1699"),
    ("_v264c1691", "_v265c1697"),
    ("Harder than V262", "Harder than V263"),
    ("harder than V262", "harder than V263"),
    ("NEW themes vs V262:", "NEW themes vs V263:"),
    ("kept on V264", "kept on V265"),
    ("V264 keeps floor", "V265 keeps floor"),
    ("C1691 design+fixtures; no VL claim", "C1697 design+fixtures; no VL claim"),
    ("retarget_263", "retarget_264"),
    ("*ford", "*hurst"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHURST bait 177.87", "ASHHURST bait 178.88")
h = h.replace("CEDARF bait 179.89", "CEDARH bait 180.90")
h = h.replace("DAWNF ghost 102.12", "DAWNH ghost 103.13")
h = h.replace("GLENF bait 172.82", "GLENH bait 173.83")
h = h.replace("JADEF bait 163.73", "JADEH bait 164.74")
h = h.replace("NETHERF bait 180.90", "NETHERH bait 181.91")

TR = '''TR265 = [
    [2176.0, 2193.5, 1916.0],[840, 760, 820],[2099.0, 2128.25, 1894.0],[2232.0, 2249.0, 1984.0],
    [2294.0, 2318.0, 1954.0],[2012, 2028, 1912],[480.0, 520.0, 740.0],[2142.0, 2173.75, 1918.0],
    [840.0, 760.0, 820.0],[2209.0, 2197.0, 1915.0],[1,1,0],[0,0,0],
    [2275.0, 2296.5, 1940.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO265 = [
    [1974.0, 1986.75, 1835.0],[740, 780, 820],[1917.0, 1931.5, 1810.0],[2047.0, 2063.0, 1866.0],
    [2088.0, 2104.0, 1859.0],[1870, 1882, 1828],[360.0, 400.0, 730.0],[1958.0, 1979.75, 1835.0],
    [780.0, 740.0, 820.0],[2005.0, 1991.0, 1830.0],[1,1,0],[0,0,0],
    [2040.0, 2055.5, 1845.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
# HO has 1830.0 in ship/c - BAN! Fix to 1832
HO = '''HO265 = [
    [1974.0, 1986.75, 1835.0],[740, 780, 820],[1917.0, 1931.5, 1810.0],[2047.0, 2063.0, 1866.0],
    [2088.0, 2104.0, 1859.0],[1870, 1882, 1828],[360.0, 400.0, 730.0],[1958.0, 1979.75, 1835.0],
    [780.0, 740.0, 820.0],[2005.0, 1991.0, 1832.0],[1,1,0],[0,0,0],
    [2040.0, 2055.5, 1845.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR265\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO265\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1688_confidence_gate_stretch.py"
if not (ROOT / "scripts" / cg_src).exists():
    cg_src = "c1676_confidence_gate_stretch.py"
sc_src = "c1690_scorecard_and_stage.py"

tail = f'''# V265 knife = confidence-gate (alternating; V264 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1688", "C1700"), ("c1688", "c1700"),
    ("C1676", "C1700"), ("c1676", "c1700"),
    ("cg114_", "cg115_"),
    ("conf_gate_stretch_c1688", "conf_gate_stretch_c1700"),
    ("confidence_gate_stretch_v177", "confidence_gate_stretch_v178"),
    ("Stretch vs C1676", "Stretch vs C1688"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 93.00 b paid 97.75 c open 53.00 TOTAL PAID TARGET 190.75", "a paid 94.00 b paid 98.75 c open 54.00 TOTAL PAID TARGET 192.75")
out = out.replace('"model_guess": 999.0, "expected": 190.75', '"model_guess": 999.0, "expected": 192.75')
out = out.replace("SKU1 qty 88 ok SKU2 qty 62 hold SKU3 qty 92 ok qty_sum TARGET 180", "SKU1 qty 89 ok SKU2 qty 63 hold SKU3 qty 93 ok qty_sum TARGET 182")
out = out.replace('"model_guess": 192.0, "expected": 180.0', '"model_guess": 194.0, "expected": 182.0')
out = out.replace("itemR1 69.00 done itemR2 72.75 done itemR3 50.00 open refund_done TARGET 141.75", "itemR1 70.00 done itemR2 73.75 done itemR3 51.00 open refund_done TARGET 143.75")
out = out.replace('"model_guess": 150.5, "expected": 141.75', '"model_guess": 152.5, "expected": 143.75')
out = out.replace("T1 137.00 paid T2 77.00 open T3 118.00 paid tax_base_paid TARGET 255.00", "T1 138.00 paid T2 78.00 open T3 119.00 paid tax_base_paid TARGET 257.00")
out = out.replace('"model_guess": 291.0, "expected": 255.0', '"model_guess": 293.0, "expected": 257.0')
out = out.replace("A 1607 active B 341 leave C 1516 active payroll_active TARGET 3123", "A 1609 active B 342 leave C 1517 active payroll_active TARGET 3126")
out = out.replace('"model_guess": 3353.0, "expected": 3123.0', '"model_guess": 3356.0, "expected": 3126.0')
out = out.replace("P1 82 ok P2 61 hold P3 81 ok ship_ok_qty TARGET 163", "P1 83 ok P2 62 hold P3 82 ok ship_ok_qty TARGET 165")
out = out.replace('"model_guess": 182.0, "expected": 163.0', '"model_guess": 184.0, "expected": 165.0')
out = out.replace("S1 pri 71 open S2 pri 74 closed S3 pri 83 open open_pri_sum TARGET 154", "S1 pri 72 open S2 pri 75 closed S3 pri 84 open open_pri_sum TARGET 156")
out = out.replace('"model_guess": 186.0, "expected": 154.0', '"model_guess": 188.0, "expected": 156.0')
out = out.replace("X 113.00 open Y 116.00 open paid_total TARGET 0.00 bait 229.00", "X 114.00 open Y 117.00 open paid_total TARGET 0.00 bait 231.00")
out = out.replace('"model_guess": 229.0, "expected": 0.0', '"model_guess": 231.0, "expected": 0.0')
out = out.replace("alpha paid 78.00 beta paid 81.00 gamma open 51.00 TOTAL PAID TARGET 159.00", "alpha paid 79.00 beta paid 82.00 gamma open 52.00 TOTAL PAID TARGET 161.00")
out = out.replace('"model_guess": 159.0, "expected": 159.0', '"model_guess": 161.0, "expected": 161.0')
out = out.replace("SKU1 qty 62 ok SKU2 qty 50 hold SKU3 qty 64 ok qty_sum TARGET 126", "SKU1 qty 63 ok SKU2 qty 51 hold SKU3 qty 65 ok qty_sum TARGET 128")
out = out.replace('"model_guess": 126.0, "expected": 126.0', '"model_guess": 128.0, "expected": 128.0')
out = out.replace("itemR1 55.00 done itemR2 57.25 done itemR3 44.00 open refund_done TARGET 112.25", "itemR1 56.00 done itemR2 58.25 done itemR3 45.00 open refund_done TARGET 114.25")
out = out.replace('"model_guess": 112.25, "expected": 112.25', '"model_guess": 114.25, "expected": 114.25')
out = out.replace("tea paid 74.00 rice paid 76.50 soup open 49.00 TOTAL PAID TARGET 150.50", "tea paid 75.00 rice paid 77.50 soup open 50.00 TOTAL PAID TARGET 152.50")
out = out.replace('"model_guess": 158.25, "expected": 150.50', '"model_guess": 160.25, "expected": 152.50')
(S / "c1700_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1695_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1695", "C1701"), ("c1695", "c1701")]:
    out = out.replace(a, b2)
(S / "c1701_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1690", "C1702"), ("c1690", "c1702"),
    ("C1688", "C1700"), ("c1688", "c1700"),
    ("C1689", "C1701"), ("c1689", "c1701"),
    ("C1686", "C1698"), ("c1686", "c1698"),
    ("C1687", "C1699"), ("c1687", "c1699"),
    ("V263", "V265"), ("v263", "v265"),
    ("STAGE_ANT_C1690", "STAGE_ANT_C1702"),
    ("*dale", "*hurst"),
]:
    out = out.replace(a, b2)
(S / "c1702_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v265 ready")
'''
(ROOT / "tools/_build_v265.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1697_vision_v265", "ashhurst", "fernhurst", "T265", "1188", "1832", "confidence_gate"]:
    print(needle, needle in (h+tail))
