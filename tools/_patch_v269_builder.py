from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v268.py").read_text(encoding="utf-8")
idx0 = b0.find('# V268 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("nethercroft", "netherholm"), ("NETHERCROFT", "NETHERHOLM"),
    ("cedarcroft", "cedarholm"), ("CEDARCROFT", "CEDARHOLM"),
    ("dawncroft", "dawnholm"), ("DAWNCROFT", "DAWNHOLM"),
    ("ferncroft", "fernholm"), ("FERNCROFT", "FERNHOLM"),
    ("glencroft", "glenholm"), ("GLENCROFT", "GLENHOLM"),
    ("hazecroft", "hazeholm"), ("HAZECROFT", "HAZEHOLM"),
    ("jadecroft", "jadeholm"), ("JADECROFT", "JADEHOLM"),
    ("knotcroft", "knotholm"), ("KNOTCROFT", "KNOTHOLM"),
    ("lakecroft", "lakeholm"), ("LAKECROFT", "LAKEHOLM"),
    ("mosscroft", "mossholm"), ("MOSSCROFT", "MOSSHOLM"),
    ("pinecroft", "pineholm"), ("PINECROFT", "PINEHOLM"),
    ("quillcroft", "quillholm"), ("QUILLCROFT", "QUILLHOLM"),
    ("reedcroft", "reedholm"), ("REEDCROFT", "REEDHOLM"),
    ("stonecroft", "stoneholm"), ("STONECROFT", "STONEHOLM"),
    ("ashcroft", "ashholm"), ("ASHCROFT", "ASHHOLM"),
    ("elmcroft", "elmholm"), ("ELMCROFT", "ELMHOLM"),
    ("inkcroft", "inkholm"), ("INKCROFT", "INKHOLM"),
    ("oakcroft", "oakholm"), ("OAKCROFT", "OAKHOLM"),
]
pairs = [
    ("*croft ; stack mid-band", "*holm ; stack mid-band"),
    ("T268", "T269"), ("TR268", "TR269"), ("HO268", "HO269"),
    ("NEW268", "NEW269"),
    ("V268", "V269"), ("v268", "v269"),
    ("_v268_themes.json", "_v269_themes.json"),
    ("_v267_themes.json", "_v268_themes.json"),
    ("OLD267", "OLD268"),
    ("vision_images_v268", "vision_images_v269"),
    ("VL_GATE_V268", "VL_GATE_V269"), ("vl_gate_v268", "vl_gate_v269"),
    ("C1715", "C1721"), ("c1715", "c1721"),
    ("C1716", "C1722"), ("c1716", "c1722"),
    ("C1717", "C1723"), ("c1717", "c1723"),
    ("_v268c1715", "_v269c1721"),
    ("Harder than V266", "Harder than V267"),
    ("harder than V266", "harder than V267"),
    ("NEW themes vs V266:", "NEW themes vs V267:"),
    ("kept on V268", "kept on V269"),
    ("V268 keeps floor", "V269 keeps floor"),
    ("C1715 design+fixtures; no VL claim", "C1721 design+fixtures; no VL claim"),
    ("retarget_267", "retarget_268"),
    ("*croft", "*holm"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHOLM bait 181.91", "ASHHOLM bait 182.92")
h = h.replace("CEDARC bait 183.93", "CEDARH bait 184.94")
h = h.replace("DAWNC ghost 106.16", "DAWNH ghost 107.17")
h = h.replace("GLENC bait 176.86", "GLENH bait 177.87")
h = h.replace("JADEC bait 167.77", "JADEH bait 168.78")
h = h.replace("NETHERC bait 184.94", "NETHERH bait 185.95")

TR = '''TR269 = [
    [2184.0, 2201.5, 1924.0],[840, 760, 820],[2107.0, 2136.25, 1902.0],[2240.0, 2257.0, 1992.0],
    [2302.0, 2326.0, 1962.0],[2020, 2036, 1920],[480.0, 520.0, 740.0],[2150.0, 2181.75, 1926.0],
    [840.0, 760.0, 820.0],[2217.0, 2205.0, 1923.0],[1,1,0],[0,0,0],
    [2283.0, 2304.5, 1948.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO269 = [
    [1982.0, 1994.75, 1843.0],[740, 780, 820],[1925.0, 1939.5, 1818.0],[2055.0, 2071.0, 1874.0],
    [2096.0, 2112.0, 1867.0],[1878, 1890, 1838],[360.0, 400.0, 730.0],[1966.0, 1987.75, 1843.0],
    [780.0, 740.0, 820.0],[2013.0, 1999.0, 1840.0],[1,1,0],[0,0,0],
    [2048.0, 2063.5, 1853.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR269\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO269\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1712_confidence_gate_stretch.py"
if not (ROOT / "scripts" / cg_src).exists():
    cg_src = "c1700_confidence_gate_stretch.py"
sc_src = "c1714_scorecard_and_stage.py"

tail = f'''# V269 knife = confidence-gate (alternating; V268 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1712", "C1724"), ("c1712", "c1724"),
    ("C1700", "C1724"), ("c1700", "c1724"),
    ("cg116_", "cg117_"),
    ("conf_gate_stretch_c1712", "conf_gate_stretch_c1724"),
    ("confidence_gate_stretch_v179", "confidence_gate_stretch_v180"),
    ("Stretch vs C1700", "Stretch vs C1712"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 95.00 b paid 99.75 c open 55.00 TOTAL PAID TARGET 194.75", "a paid 96.00 b paid 100.75 c open 56.00 TOTAL PAID TARGET 196.75")
out = out.replace('"model_guess": 999.0, "expected": 194.75', '"model_guess": 999.0, "expected": 196.75')
out = out.replace("SKU1 qty 90 ok SKU2 qty 64 hold SKU3 qty 94 ok qty_sum TARGET 184", "SKU1 qty 91 ok SKU2 qty 65 hold SKU3 qty 95 ok qty_sum TARGET 186")
out = out.replace('"model_guess": 196.0, "expected": 184.0', '"model_guess": 198.0, "expected": 186.0')
out = out.replace("itemR1 71.00 done itemR2 74.75 done itemR3 52.00 open refund_done TARGET 145.75", "itemR1 72.00 done itemR2 75.75 done itemR3 53.00 open refund_done TARGET 147.75")
out = out.replace('"model_guess": 154.5, "expected": 145.75', '"model_guess": 156.5, "expected": 147.75')
out = out.replace("T1 139.00 paid T2 79.00 open T3 120.00 paid tax_base_paid TARGET 259.00", "T1 140.00 paid T2 80.00 open T3 121.00 paid tax_base_paid TARGET 261.00")
out = out.replace('"model_guess": 295.0, "expected": 259.0', '"model_guess": 297.0, "expected": 261.0')
out = out.replace("A 1611 active B 343 leave C 1518 active payroll_active TARGET 3129", "A 1613 active B 344 leave C 1519 active payroll_active TARGET 3132")
out = out.replace('"model_guess": 3359.0, "expected": 3129.0', '"model_guess": 3362.0, "expected": 3132.0')
out = out.replace("P1 84 ok P2 63 hold P3 83 ok ship_ok_qty TARGET 167", "P1 85 ok P2 64 hold P3 84 ok ship_ok_qty TARGET 169")
out = out.replace('"model_guess": 186.0, "expected": 167.0', '"model_guess": 188.0, "expected": 169.0')
out = out.replace("S1 pri 73 open S2 pri 76 closed S3 pri 85 open open_pri_sum TARGET 158", "S1 pri 74 open S2 pri 77 closed S3 pri 86 open open_pri_sum TARGET 160")
out = out.replace('"model_guess": 190.0, "expected": 158.0', '"model_guess": 192.0, "expected": 160.0')
out = out.replace("X 115.00 open Y 118.00 open paid_total TARGET 0.00 bait 233.00", "X 116.00 open Y 119.00 open paid_total TARGET 0.00 bait 235.00")
out = out.replace('"model_guess": 233.0, "expected": 0.0', '"model_guess": 235.0, "expected": 0.0')
out = out.replace("alpha paid 80.00 beta paid 83.00 gamma open 53.00 TOTAL PAID TARGET 163.00", "alpha paid 81.00 beta paid 84.00 gamma open 54.00 TOTAL PAID TARGET 165.00")
out = out.replace('"model_guess": 163.0, "expected": 163.0', '"model_guess": 165.0, "expected": 165.0')
out = out.replace("SKU1 qty 64 ok SKU2 qty 52 hold SKU3 qty 66 ok qty_sum TARGET 130", "SKU1 qty 65 ok SKU2 qty 53 hold SKU3 qty 67 ok qty_sum TARGET 132")
out = out.replace('"model_guess": 130.0, "expected": 130.0', '"model_guess": 132.0, "expected": 132.0')
out = out.replace("itemR1 57.00 done itemR2 59.25 done itemR3 46.00 open refund_done TARGET 116.25", "itemR1 58.00 done itemR2 60.25 done itemR3 47.00 open refund_done TARGET 118.25")
out = out.replace('"model_guess": 116.25, "expected": 116.25', '"model_guess": 118.25, "expected": 118.25')
out = out.replace("tea paid 76.00 rice paid 78.50 soup open 51.00 TOTAL PAID TARGET 154.50", "tea paid 77.00 rice paid 79.50 soup open 52.00 TOTAL PAID TARGET 156.50")
out = out.replace('"model_guess": 162.25, "expected": 154.50', '"model_guess": 164.25, "expected": 156.50')
(S / "c1724_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1719_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1719", "C1725"), ("c1719", "c1725")]:
    out = out.replace(a, b2)
(S / "c1725_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1714", "C1726"), ("c1714", "c1726"),
    ("C1712", "C1724"), ("c1712", "c1724"),
    ("C1713", "C1725"), ("c1713", "c1725"),
    ("C1710", "C1722"), ("c1710", "c1722"),
    ("C1711", "C1723"), ("c1711", "c1723"),
    ("V267", "V269"), ("v267", "v269"),
    ("STAGE_ANT_C1714", "STAGE_ANT_C1726"),
    ("*vale", "*holm"),
]:
    out = out.replace(a, b2)
(S / "c1726_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v269 ready")
'''
(ROOT / "tools/_build_v269.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1721_vision_v269", "ashholm", "fernholm", "T269", "1188", "1838", "confidence_gate"]:
    print(needle, needle in (h+tail))
