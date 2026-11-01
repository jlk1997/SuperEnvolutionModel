from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v256.py").read_text(encoding="utf-8")
idx0 = b0.find('# V256 knife = product-U2C')
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
    ("T256", "T257"), ("TR256", "TR257"), ("HO256", "HO257"),
    ("NEW256", "NEW257"),
    ("V256", "V257"), ("v256", "v257"),
    ("_v256_themes.json", "_v257_themes.json"),
    ("_v255_themes.json", "_v256_themes.json"),
    ("OLD255", "OLD256"),
    ("vision_images_v256", "vision_images_v257"),
    ("VL_GATE_V256", "VL_GATE_V257"), ("vl_gate_v256", "vl_gate_v257"),
    ("C1643", "C1649"), ("c1643", "c1649"),
    ("C1644", "C1650"), ("c1644", "c1650"),
    ("C1645", "C1651"), ("c1645", "c1651"),
    ("_v256c1643", "_v257c1649"),
    ("Harder than V254", "Harder than V255"),
    ("harder than V254", "harder than V255"),
    ("NEW themes vs V254:", "NEW themes vs V255:"),
    ("kept on V256", "kept on V257"),
    ("V256 keeps floor", "V257 keeps floor"),
    ("C1643 design+fixtures; no VL claim", "C1649 design+fixtures; no VL claim"),
    ("retarget_255", "retarget_256"),
    ("*vale", "*croft"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHCROFT bait 169.79", "ASHCROFT bait 170.80")
h = h.replace("CEDARV bait 171.81", "CEDARC bait 172.82")
h = h.replace("DAWNV ghost 94.94", "DAWNC ghost 95.95")
h = h.replace("GLENV bait 164.74", "GLENC bait 165.75")
h = h.replace("JADEV bait 155.65", "JADEC bait 156.66")
h = h.replace("NETHERV bait 172.82", "NETHERC bait 173.83")

TR = '''TR257 = [
    [2160.0, 2177.5, 1900.0],[840, 760, 820],[2083.0, 2112.25, 1878.0],[2216.0, 2233.0, 1968.0],
    [2278.0, 2302.0, 1938.0],[1996, 2012, 1896],[480.0, 520.0, 740.0],[2126.0, 2157.75, 1902.0],
    [840.0, 760.0, 820.0],[2193.0, 2181.0, 1899.0],[1,1,0],[0,0,0],
    [2259.0, 2280.5, 1924.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO257 = [
    [1958.0, 1970.75, 1819.0],[740, 780, 820],[1901.0, 1915.5, 1794.0],[2031.0, 2047.0, 1850.0],
    [2072.0, 2088.0, 1843.0],[1854, 1866, 1812],[360.0, 400.0, 730.0],[1942.0, 1963.75, 1819.0],
    [780.0, 740.0, 820.0],[1989.0, 1975.0, 1814.0],[1,1,0],[0,0,0],
    [2024.0, 2039.5, 1829.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR257\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO257\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1640_confidence_gate_stretch.py"
if not (ROOT / "scripts" / cg_src).exists():
    cg_src = "c1628_confidence_gate_stretch.py"
sc_src = "c1642_scorecard_and_stage.py"

tail = f'''# V257 knife = confidence-gate (alternating; V256 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1640", "C1652"), ("c1640", "c1652"),
    ("C1628", "C1652"), ("c1628", "c1652"),
    ("cg110_", "cg111_"),
    ("conf_gate_stretch_c1640", "conf_gate_stretch_c1652"),
    ("confidence_gate_stretch_v173", "confidence_gate_stretch_v174"),
    ("Stretch vs C1628", "Stretch vs C1640"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 89.00 b paid 93.75 c open 49.00 TOTAL PAID TARGET 182.75", "a paid 90.00 b paid 94.75 c open 50.00 TOTAL PAID TARGET 184.75")
out = out.replace('"model_guess": 999.0, "expected": 182.75', '"model_guess": 999.0, "expected": 184.75')
out = out.replace("SKU1 qty 84 ok SKU2 qty 58 hold SKU3 qty 88 ok qty_sum TARGET 172", "SKU1 qty 85 ok SKU2 qty 59 hold SKU3 qty 89 ok qty_sum TARGET 174")
out = out.replace('"model_guess": 184.0, "expected": 172.0', '"model_guess": 186.0, "expected": 174.0')
out = out.replace("itemR1 65.00 done itemR2 68.75 done itemR3 46.00 open refund_done TARGET 133.75", "itemR1 66.00 done itemR2 69.75 done itemR3 47.00 open refund_done TARGET 135.75")
out = out.replace('"model_guess": 142.5, "expected": 133.75', '"model_guess": 144.5, "expected": 135.75')
out = out.replace("T1 133.00 paid T2 73.00 open T3 114.00 paid tax_base_paid TARGET 247.00", "T1 134.00 paid T2 74.00 open T3 115.00 paid tax_base_paid TARGET 249.00")
out = out.replace('"model_guess": 283.0, "expected": 247.0', '"model_guess": 285.0, "expected": 249.0')
out = out.replace("A 1599 active B 337 leave C 1512 active payroll_active TARGET 3111", "A 1601 active B 338 leave C 1513 active payroll_active TARGET 3114")
out = out.replace('"model_guess": 3341.0, "expected": 3111.0', '"model_guess": 3344.0, "expected": 3114.0')
out = out.replace("P1 78 ok P2 57 hold P3 77 ok ship_ok_qty TARGET 155", "P1 79 ok P2 58 hold P3 78 ok ship_ok_qty TARGET 157")
out = out.replace('"model_guess": 174.0, "expected": 155.0', '"model_guess": 176.0, "expected": 157.0')
out = out.replace("S1 pri 67 open S2 pri 70 closed S3 pri 79 open open_pri_sum TARGET 146", "S1 pri 68 open S2 pri 71 closed S3 pri 80 open open_pri_sum TARGET 148")
out = out.replace('"model_guess": 178.0, "expected": 146.0', '"model_guess": 180.0, "expected": 148.0')
out = out.replace("X 109.00 open Y 112.00 open paid_total TARGET 0.00 bait 221.00", "X 110.00 open Y 113.00 open paid_total TARGET 0.00 bait 223.00")
out = out.replace('"model_guess": 221.0, "expected": 0.0', '"model_guess": 223.0, "expected": 0.0')
out = out.replace("alpha paid 74.00 beta paid 77.00 gamma open 47.00 TOTAL PAID TARGET 151.00", "alpha paid 75.00 beta paid 78.00 gamma open 48.00 TOTAL PAID TARGET 153.00")
out = out.replace('"model_guess": 151.0, "expected": 151.0', '"model_guess": 153.0, "expected": 153.0')
out = out.replace("SKU1 qty 58 ok SKU2 qty 46 hold SKU3 qty 60 ok qty_sum TARGET 118", "SKU1 qty 59 ok SKU2 qty 47 hold SKU3 qty 61 ok qty_sum TARGET 120")
out = out.replace('"model_guess": 118.0, "expected": 118.0', '"model_guess": 120.0, "expected": 120.0')
out = out.replace("itemR1 51.00 done itemR2 53.25 done itemR3 40.00 open refund_done TARGET 104.25", "itemR1 52.00 done itemR2 54.25 done itemR3 41.00 open refund_done TARGET 106.25")
out = out.replace('"model_guess": 104.25, "expected": 104.25', '"model_guess": 106.25, "expected": 106.25')
out = out.replace("tea paid 70.00 rice paid 72.50 soup open 45.00 TOTAL PAID TARGET 142.50", "tea paid 71.00 rice paid 73.50 soup open 46.00 TOTAL PAID TARGET 144.50")
out = out.replace('"model_guess": 150.25, "expected": 142.50', '"model_guess": 152.25, "expected": 144.50')
(S / "c1652_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1647_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1647", "C1653"), ("c1647", "c1653")]:
    out = out.replace(a, b2)
(S / "c1653_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1642", "C1654"), ("c1642", "c1654"),
    ("C1640", "C1652"), ("c1640", "c1652"),
    ("C1641", "C1653"), ("c1641", "c1653"),
    ("C1638", "C1650"), ("c1638", "c1650"),
    ("C1639", "C1651"), ("c1639", "c1651"),
    ("V255", "V257"), ("v255", "v257"),
    ("STAGE_ANT_C1642", "STAGE_ANT_C1654"),
    ("*mere", "*croft"),
]:
    out = out.replace(a, b2)
(S / "c1654_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v257 ready")
'''
(ROOT / "tools/_build_v257.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1649_vision_v257", "ashcroft", "ferncroft", "T257", "1188", "1850", "confidence_gate"]:
    print(needle, needle in (h+tail))
