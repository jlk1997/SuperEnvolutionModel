from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v318.py").read_text(encoding="utf-8")
idx0 = b0.find('# V318 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC2020 = " in head0:
    head0 = head0[:head0.find("SC2020 = ")]

theme_pairs = [
    ("netherdale", "netherford"), ("NETHERDALE", "NETHERFORD"),
    ("cedardale", "cedarford"), ("CEDARDALE", "CEDARFORD"),
    ("dawndale", "dawnford"), ("DAWNDALE", "DAWNFORD"),
    ("ferndale", "fernford"), ("FERNDALE", "FERNFORD"),
    ("glendale", "glenford"), ("GLENDALE", "GLENFORD"),
    ("hazedale", "hazeford"), ("HAZEDALE", "HAZEFORD"),
    ("jadedale", "jadeford"), ("JADEDALE", "JADEFORD"),
    ("knotdale", "knotford"), ("KNOTDALE", "KNOTFORD"),
    ("lakedale", "lakeford"), ("LAKEDALE", "LAKEFORD"),
    ("mossdale", "mossford"), ("MOSSDALE", "MOSSFORD"),
    ("pinedale", "pineford"), ("PINEDALE", "PINEFORD"),
    ("quilldale", "quillford"), ("QUILLDALE", "QUILLFORD"),
    ("reeddale", "reedford"), ("REEDDALE", "REEDFORD"),
    ("stonedale", "stoneford"), ("STONEDALE", "STONEFORD"),
    ("ashdale", "ashford"), ("ASHDALE", "ASHFORD"),
    ("elmdale", "elmford"), ("ELMDALE", "ELMFORD"),
    ("inkdale", "inkford"), ("INKDALE", "INKFORD"),
    ("oakdale", "oakford"), ("OAKDALE", "OAKFORD"),
]
pairs = [
    ("*dale ; stack mid-band", "*ford ; stack mid-band"),
    ("T318", "T319"), ("TR318", "TR319"), ("HO318", "HO319"),
    ("NEW318", "NEW319"),
    ("V318", "V319"), ("v318", "v319"),
    ("_v318_themes.json", "_v319_themes.json"),
    ("_v317_themes.json", "_v318_themes.json"),
    ("OLD317", "OLD318"),
    ("vision_images_v318", "vision_images_v319"),
    ("VL_GATE_V318", "VL_GATE_V319"), ("vl_gate_v318", "vl_gate_v319"),
    ("C2015", "C2021"), ("c2015", "c2021"),
    ("C2016", "C2022"), ("c2016", "c2022"),
    ("C2017", "C2023"), ("c2017", "c2023"),
    ("_v318c2015", "_v319c2021"),
    ("Harder than V316", "Harder than V317"),
    ("harder than V316", "harder than V317"),
    ("NEW themes vs V316:", "NEW themes vs V317:"),
    ("kept on V318", "kept on V319"),
    ("V318 keeps floor", "V319 keeps floor"),
    ("C2015 design+fixtures; no VL claim", "C2021 design+fixtures; no VL claim"),
    ("retarget_317", "retarget_318"),
    ("*dale", "*ford"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHDALE bait 231.41", "ASHFORD bait 232.42")
h = h.replace("CEDARD bait 233.43", "CEDARF bait 234.44")
h = h.replace("DAWND ghost 156.66", "DAWNF ghost 157.67")
h = h.replace("GLEND bait 226.36", "GLENF bait 227.37")
h = h.replace("JADED bait 217.27", "JADEF bait 218.28")
h = h.replace("NETHERD bait 234.44", "NETHERF bait 235.45")

TR = '''TR319 = [
    [2302.0, 2319.5, 2042.0],[840, 760, 820],[2225.0, 2254.25, 2020.0],[2358.0, 2375.0, 2110.0],
    [2420.0, 2444.0, 2080.0],[2138, 2154, 2038],[490.0, 530.0, 760.0],[2268.0, 2299.75, 2044.0],
    [840.0, 760.0, 820.0],[2335.0, 2323.0, 2041.0],[1,1,0],[0,0,0],
    [2401.0, 2422.5, 2066.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO319 = [
    [2100.0, 2112.75, 1961.0],[640, 660, 820],[2043.0, 2057.5, 1936.0],[2173.0, 2189.0, 1992.0],
    [2214.0, 2230.0, 1985.0],[1996, 2008, 1956],[420.0, 460.0, 740.0],[2084.0, 2105.75, 1961.0],
    [740.0, 780.0, 820.0],[2131.0, 2117.0, 1958.0],[1,1,0],[0,0,0],
    [2166.0, 2181.5, 1971.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR319\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO319\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

sc_body = (ROOT / "scripts/c2014_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2014", "C2026"), ("c2014", "c2026"),
    ("C2012", "C2024"), ("c2012", "c2024"),
    ("C2013", "C2025"), ("c2013", "c2025"),
    ("C2010", "C2022"), ("c2010", "c2022"),
    ("C2011", "C2023"), ("c2011", "c2023"),
    ("C2009", "C2021"), ("c2009", "c2021"),
    ("C2006", "C2018"), ("c2006", "c2018"),
    ("V317", "V319"), ("v317", "v319"),
    ("STAGE_ANT_C2014", "STAGE_ANT_C2026"),
    ("*brook", "*ford"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V319 knife = confidence-gate (alternating; V318 was product-U2C)
out = (S / "c2012_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2012", "C2024"), ("c2012", "c2024"),
    ("C2000", "C2024"), ("c2000", "c2024"),
    ("cg141_", "cg142_"),
    ("conf_gate_stretch_c2012", "conf_gate_stretch_c2024"),
    ("confidence_gate_stretch_v204", "confidence_gate_stretch_v205"),
    ("Stretch vs C2000", "Stretch vs C2012"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 120.00 b paid 124.75 c open 80.00 TOTAL PAID TARGET 244.75", "a paid 121.00 b paid 125.75 c open 81.00 TOTAL PAID TARGET 246.75")
out = out.replace('"model_guess": 999.0, "expected": 244.75', '"model_guess": 999.0, "expected": 246.75')
out = out.replace("SKU1 qty 115 ok SKU2 qty 89 hold SKU3 qty 119 ok qty_sum TARGET 234", "SKU1 qty 116 ok SKU2 qty 90 hold SKU3 qty 120 ok qty_sum TARGET 236")
out = out.replace('"model_guess": 246.0, "expected": 234.0', '"model_guess": 248.0, "expected": 236.0')
out = out.replace("itemR1 96.00 done itemR2 99.75 done itemR3 77.00 open refund_done TARGET 195.75", "itemR1 97.00 done itemR2 100.75 done itemR3 78.00 open refund_done TARGET 197.75")
out = out.replace('"model_guess": 204.5, "expected": 195.75', '"model_guess": 206.5, "expected": 197.75')
out = out.replace("T1 164.00 paid T2 104.00 open T3 145.00 paid tax_base_paid TARGET 309.00", "T1 165.00 paid T2 105.00 open T3 146.00 paid tax_base_paid TARGET 311.00")
out = out.replace('"model_guess": 345.0, "expected": 309.0', '"model_guess": 347.0, "expected": 311.0')
out = out.replace("A 1659 active B 368 leave C 1543 active payroll_active TARGET 3202", "A 1660 active B 369 leave C 1544 active payroll_active TARGET 3204")
out = out.replace('"model_guess": 3432.0, "expected": 3202.0', '"model_guess": 3434.0, "expected": 3204.0')
out = out.replace("P1 109 ok P2 88 hold P3 108 ok ship_ok_qty TARGET 217", "P1 110 ok P2 89 hold P3 109 ok ship_ok_qty TARGET 219")
out = out.replace('"model_guess": 236.0, "expected": 217.0', '"model_guess": 238.0, "expected": 219.0')
out = out.replace("S1 pri 98 open S2 pri 101 closed S3 pri 110 open open_pri_sum TARGET 208", "S1 pri 99 open S2 pri 102 closed S3 pri 111 open open_pri_sum TARGET 210")
out = out.replace('"model_guess": 240.0, "expected": 208.0', '"model_guess": 242.0, "expected": 210.0')
out = out.replace("X 140.00 open Y 143.00 open paid_total TARGET 0.00 bait 283.00", "X 141.00 open Y 144.00 open paid_total TARGET 0.00 bait 285.00")
out = out.replace('"model_guess": 283.0, "expected": 0.0', '"model_guess": 285.0, "expected": 0.0')
out = out.replace("alpha paid 105.00 beta paid 108.00 gamma open 78.00 TOTAL PAID TARGET 213.00", "alpha paid 106.00 beta paid 109.00 gamma open 79.00 TOTAL PAID TARGET 215.00")
out = out.replace('"model_guess": 213.0, "expected": 213.0', '"model_guess": 215.0, "expected": 215.0')
out = out.replace("SKU1 qty 89 ok SKU2 qty 77 hold SKU3 qty 91 ok qty_sum TARGET 180", "SKU1 qty 90 ok SKU2 qty 78 hold SKU3 qty 92 ok qty_sum TARGET 182")
out = out.replace('"model_guess": 180.0, "expected": 180.0', '"model_guess": 182.0, "expected": 182.0')
out = out.replace("itemR1 82.00 done itemR2 84.25 done itemR3 71.00 open refund_done TARGET 166.25", "itemR1 83.00 done itemR2 85.25 done itemR3 72.00 open refund_done TARGET 168.25")
out = out.replace('"model_guess": 166.25, "expected": 166.25', '"model_guess": 168.25, "expected": 168.25')
out = out.replace("tea paid 101.00 rice paid 103.50 soup open 76.00 TOTAL PAID TARGET 204.50", "tea paid 102.00 rice paid 104.50 soup open 77.00 TOTAL PAID TARGET 206.50")
out = out.replace('"model_guess": 212.25, "expected": 204.50', '"model_guess": 214.25, "expected": 206.50')
(S / "c2024_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2012_confidence_gate_stretch.py")

out = (S / "c2019_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2019", "C2025"), ("c2019", "c2025")]:
    out = out.replace(a, b2)
(S / "c2025_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2026_scorecard_and_stage.py").write_text(SC2026, encoding="utf-8")
print("scorecard from fixed c2014 conf-gate pattern")
print("OK builder v319 ready")
'''
pre = "SC2026 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v319.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2021_vision_v319", "ashford", "fernford", "T319", "1188", "1956", "confidence_gate", "retarget_318"]:
    print(needle, needle in (h+pre+tail))
