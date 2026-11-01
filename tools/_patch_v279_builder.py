from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v278.py").read_text(encoding="utf-8")
idx0 = b0.find('# V278 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

theme_pairs = [
    ("nethervale", "nethercroft"), ("NETHERVALE", "NETHERCROFT"),
    ("cedarvale", "cedarcroft"), ("CEDARVALE", "CEDARCROFT"),
    ("dawnvale", "dawncroft"), ("DAWNVALE", "DAWNCROFT"),
    ("fernvale", "ferncroft"), ("FERNVALE", "FERNCROFT"),
    ("glenvale", "glencroft"), ("GLENVALE", "GLENCROFT"),
    ("hazevale", "hazecroft"), ("HAZEVALE", "HAZECROFT"),
    ("jadevale", "jadecroft"), ("JADEVALE", "JADECROFT"),
    ("knotvale", "knotcroft"), ("KNOTVALE", "KNOTCROFT"),
    ("lakevale", "lakecroft"), ("LAKEVALE", "LAKECROFT"),
    ("mossvale", "mosscroft"), ("MOSSVALE", "MOSSCROFT"),
    ("pinevale", "pinecroft"), ("PINEVALE", "PINECROFT"),
    ("quillvale", "quillcroft"), ("QUILLVALE", "QUILLCROFT"),
    ("reedvale", "reedcroft"), ("REEDVALE", "REEDCROFT"),
    ("stonevale", "stonecroft"), ("STONEVALE", "STONECROFT"),
    ("ashvale", "ashcroft"), ("ASHVALE", "ASHCROFT"),
    ("elmvale", "elmcroft"), ("ELMVALE", "ELMCROFT"),
    ("inkvale", "inkcroft"), ("INKVALE", "INKCROFT"),
    ("oakvale", "oakcroft"), ("OAKVALE", "OAKCROFT"),
]
pairs = [
    ("*vale ; stack mid-band", "*croft ; stack mid-band"),
    ("T278", "T279"), ("TR278", "TR279"), ("HO278", "HO279"),
    ("NEW278", "NEW279"),
    ("V278", "V279"), ("v278", "v279"),
    ("_v278_themes.json", "_v279_themes.json"),
    ("_v277_themes.json", "_v278_themes.json"),
    ("OLD277", "OLD278"),
    ("vision_images_v278", "vision_images_v279"),
    ("VL_GATE_V278", "VL_GATE_V279"), ("vl_gate_v278", "vl_gate_v279"),
    ("C1775", "C1781"), ("c1775", "c1781"),
    ("C1776", "C1782"), ("c1776", "c1782"),
    ("C1777", "C1783"), ("c1777", "c1783"),
    ("_v278c1775", "_v279c1781"),
    ("Harder than V276", "Harder than V277"),
    ("harder than V276", "harder than V277"),
    ("NEW themes vs V276:", "NEW themes vs V277:"),
    ("kept on V278", "kept on V279"),
    ("V278 keeps floor", "V279 keeps floor"),
    ("C1775 design+fixtures; no VL claim", "C1781 design+fixtures; no VL claim"),
    ("retarget_277", "retarget_278"),
    ("*vale", "*croft"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHVALE bait 191.01", "ASHCROFT bait 192.02")
h = h.replace("CEDARV bait 193.03", "CEDARC bait 194.04")
h = h.replace("DAWNV ghost 116.26", "DAWNC ghost 117.27")
h = h.replace("GLENV bait 186.96", "GLENC bait 187.97")
h = h.replace("JADEV bait 177.87", "JADEC bait 178.88")
h = h.replace("NETHERV bait 194.04", "NETHERC bait 195.05")

# keep SLA mid-band after V278 550+590→1249 trap; use 490+530
TR = '''TR279 = [
    [2212.0, 2229.5, 1952.0],[840, 760, 820],[2135.0, 2164.25, 1930.0],[2268.0, 2285.0, 2020.0],
    [2330.0, 2354.0, 1990.0],[2048, 2064, 1948],[490.0, 530.0, 760.0],[2178.0, 2209.75, 1954.0],
    [840.0, 760.0, 820.0],[2245.0, 2233.0, 1951.0],[1,1,0],[0,0,0],
    [2311.0, 2332.5, 1976.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO279 = [
    [2010.0, 2022.75, 1871.0],[640, 660, 820],[1953.0, 1967.5, 1846.0],[2083.0, 2099.0, 1902.0],
    [2124.0, 2140.0, 1895.0],[1906, 1918, 1866],[420.0, 460.0, 740.0],[1994.0, 2015.75, 1871.0],
    [740.0, 780.0, 820.0],[2041.0, 2027.0, 1868.0],[1,1,0],[0,0,0],
    [2076.0, 2091.5, 1881.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR279\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO279\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1772_confidence_gate_stretch.py"
sc_src = "c1774_scorecard_and_stage.py"

tail = f'''# V279 knife = confidence-gate (alternating; V278 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1772", "C1784"), ("c1772", "c1784"),
    ("C1760", "C1784"), ("c1760", "c1784"),
    ("cg121_", "cg122_"),
    ("conf_gate_stretch_c1772", "conf_gate_stretch_c1784"),
    ("confidence_gate_stretch_v184", "confidence_gate_stretch_v185"),
    ("Stretch vs C1760", "Stretch vs C1772"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 100.00 b paid 104.75 c open 60.00 TOTAL PAID TARGET 204.75", "a paid 101.00 b paid 105.75 c open 61.00 TOTAL PAID TARGET 206.75")
out = out.replace('"model_guess": 999.0, "expected": 204.75', '"model_guess": 999.0, "expected": 206.75')
out = out.replace("SKU1 qty 95 ok SKU2 qty 69 hold SKU3 qty 99 ok qty_sum TARGET 194", "SKU1 qty 96 ok SKU2 qty 70 hold SKU3 qty 100 ok qty_sum TARGET 196")
out = out.replace('"model_guess": 206.0, "expected": 194.0', '"model_guess": 208.0, "expected": 196.0')
out = out.replace("itemR1 76.00 done itemR2 79.75 done itemR3 57.00 open refund_done TARGET 155.75", "itemR1 77.00 done itemR2 80.75 done itemR3 58.00 open refund_done TARGET 157.75")
out = out.replace('"model_guess": 164.5, "expected": 155.75', '"model_guess": 166.5, "expected": 157.75')
out = out.replace("T1 144.00 paid T2 84.00 open T3 125.00 paid tax_base_paid TARGET 269.00", "T1 145.00 paid T2 85.00 open T3 126.00 paid tax_base_paid TARGET 271.00")
out = out.replace('"model_guess": 305.0, "expected": 269.0', '"model_guess": 307.0, "expected": 271.0')
out = out.replace("A 1621 active B 348 leave C 1523 active payroll_active TARGET 3144", "A 1623 active B 349 leave C 1524 active payroll_active TARGET 3147")
out = out.replace('"model_guess": 3374.0, "expected": 3144.0', '"model_guess": 3377.0, "expected": 3147.0')
out = out.replace("P1 89 ok P2 68 hold P3 88 ok ship_ok_qty TARGET 177", "P1 90 ok P2 69 hold P3 89 ok ship_ok_qty TARGET 179")
out = out.replace('"model_guess": 196.0, "expected": 177.0', '"model_guess": 198.0, "expected": 179.0')
out = out.replace("S1 pri 78 open S2 pri 81 closed S3 pri 90 open open_pri_sum TARGET 168", "S1 pri 79 open S2 pri 82 closed S3 pri 91 open open_pri_sum TARGET 170")
out = out.replace('"model_guess": 200.0, "expected": 168.0', '"model_guess": 202.0, "expected": 170.0')
out = out.replace("X 120.00 open Y 123.00 open paid_total TARGET 0.00 bait 243.00", "X 121.00 open Y 124.00 open paid_total TARGET 0.00 bait 245.00")
out = out.replace('"model_guess": 243.0, "expected": 0.0', '"model_guess": 245.0, "expected": 0.0')
out = out.replace("alpha paid 85.00 beta paid 88.00 gamma open 58.00 TOTAL PAID TARGET 173.00", "alpha paid 86.00 beta paid 89.00 gamma open 59.00 TOTAL PAID TARGET 175.00")
out = out.replace('"model_guess": 173.0, "expected": 173.0', '"model_guess": 175.0, "expected": 175.0')
out = out.replace("SKU1 qty 69 ok SKU2 qty 57 hold SKU3 qty 71 ok qty_sum TARGET 140", "SKU1 qty 70 ok SKU2 qty 58 hold SKU3 qty 72 ok qty_sum TARGET 142")
out = out.replace('"model_guess": 140.0, "expected": 140.0', '"model_guess": 142.0, "expected": 142.0')
out = out.replace("itemR1 62.00 done itemR2 64.25 done itemR3 51.00 open refund_done TARGET 126.25", "itemR1 63.00 done itemR2 65.25 done itemR3 52.00 open refund_done TARGET 128.25")
out = out.replace('"model_guess": 126.25, "expected": 126.25', '"model_guess": 128.25, "expected": 128.25')
out = out.replace("tea paid 81.00 rice paid 83.50 soup open 56.00 TOTAL PAID TARGET 164.50", "tea paid 82.00 rice paid 84.50 soup open 57.00 TOTAL PAID TARGET 166.50")
out = out.replace('"model_guess": 172.25, "expected": 164.50', '"model_guess": 174.25, "expected": 166.50')
(S / "c1784_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1779_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1779", "C1785"), ("c1779", "c1785")]:
    out = out.replace(a, b2)
(S / "c1785_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1774", "C1786"), ("c1774", "c1786"),
    ("C1772", "C1784"), ("c1772", "c1784"),
    ("C1773", "C1785"), ("c1773", "c1785"),
    ("C1770", "C1782"), ("c1770", "c1782"),
    ("C1771", "C1783"), ("c1771", "c1783"),
    ("V277", "V279"), ("v277", "v279"),
    ("STAGE_ANT_C1774", "STAGE_ANT_C1786"),
    ("*mere", "*croft"),
]:
    out = out.replace(a, b2)
(S / "c1786_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v279 ready")
'''
(ROOT / "tools/_build_v279.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1781_vision_v279", "ashcroft", "ferncroft", "T279", "1188", "1866", "confidence_gate", "retarget_278"]:
    print(needle, needle in (h+tail))
