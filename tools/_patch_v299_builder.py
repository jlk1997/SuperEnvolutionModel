from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v298.py").read_text(encoding="utf-8")
idx0 = b0.find('# V298 knife = product-U2C')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]
if "SC1900 = " in head0:
    head0 = head0[:head0.find("SC1900 = ")]

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
    ("T298", "T299"), ("TR298", "TR299"), ("HO298", "HO299"),
    ("NEW298", "NEW299"),
    ("V298", "V299"), ("v298", "v299"),
    ("_v298_themes.json", "_v299_themes.json"),
    ("_v297_themes.json", "_v298_themes.json"),
    ("OLD297", "OLD298"),
    ("vision_images_v298", "vision_images_v299"),
    ("VL_GATE_V298", "VL_GATE_V299"), ("vl_gate_v298", "vl_gate_v299"),
    ("C1895", "C1901"), ("c1895", "c1901"),
    ("C1896", "C1902"), ("c1896", "c1902"),
    ("C1897", "C1903"), ("c1897", "c1903"),
    ("_v298c1895", "_v299c1901"),
    ("Harder than V296", "Harder than V297"),
    ("harder than V296", "harder than V297"),
    ("NEW themes vs V296:", "NEW themes vs V297:"),
    ("kept on V298", "kept on V299"),
    ("V298 keeps floor", "V299 keeps floor"),
    ("C1895 design+fixtures; no VL claim", "C1901 design+fixtures; no VL claim"),
    ("retarget_297", "retarget_298"),
    ("*hurst", "*mere"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHURST bait 211.21", "ASHMERE bait 212.22")
h = h.replace("CEDARH bait 213.23", "CEDARM bait 214.24")
h = h.replace("DAWNH ghost 136.46", "DAWNM ghost 137.47")
h = h.replace("GLENH bait 206.16", "GLENM bait 207.17")
h = h.replace("JADEH bait 197.07", "JADEM bait 198.08")
h = h.replace("NETHERH bait 214.24", "NETHERM bait 215.25")

TR = '''TR299 = [
    [2262.0, 2279.5, 2002.0],[840, 760, 820],[2185.0, 2214.25, 1980.0],[2318.0, 2335.0, 2070.0],
    [2380.0, 2404.0, 2040.0],[2098, 2114, 1998],[490.0, 530.0, 760.0],[2228.0, 2259.75, 2004.0],
    [840.0, 760.0, 820.0],[2295.0, 2283.0, 2001.0],[1,1,0],[0,0,0],
    [2361.0, 2382.5, 2026.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO299 = [
    [2060.0, 2072.75, 1921.0],[640, 660, 820],[2003.0, 2017.5, 1896.0],[2133.0, 2149.0, 1952.0],
    [2174.0, 2190.0, 1945.0],[1956, 1968, 1916],[420.0, 460.0, 740.0],[2044.0, 2065.75, 1921.0],
    [740.0, 780.0, 820.0],[2091.0, 2077.0, 1918.0],[1,1,0],[0,0,0],
    [2126.0, 2141.5, 1931.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR299\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO299\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

cg_src = "c1892_confidence_gate_stretch.py"
sc_body = (ROOT / "scripts/c1894_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1894", "C1906"), ("c1894", "c1906"),
    ("C1892", "C1904"), ("c1892", "c1904"),
    ("C1893", "C1905"), ("c1893", "c1905"),
    ("C1890", "C1902"), ("c1890", "c1902"),
    ("C1891", "C1903"), ("c1891", "c1903"),
    ("V297", "V299"), ("v297", "v299"),
    ("STAGE_ANT_C1894", "STAGE_ANT_C1906"),
    ("*ford", "*mere"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V299 knife = confidence-gate (alternating; V298 was product-U2C)
out = (S / "{cg_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1892", "C1904"), ("c1892", "c1904"),
    ("C1880", "C1904"), ("c1880", "c1904"),
    ("cg131_", "cg132_"),
    ("conf_gate_stretch_c1892", "conf_gate_stretch_c1904"),
    ("confidence_gate_stretch_v194", "confidence_gate_stretch_v195"),
    ("Stretch vs C1880", "Stretch vs C1892"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 110.00 b paid 114.75 c open 70.00 TOTAL PAID TARGET 224.75", "a paid 111.00 b paid 115.75 c open 71.00 TOTAL PAID TARGET 226.75")
out = out.replace('"model_guess": 999.0, "expected": 224.75', '"model_guess": 999.0, "expected": 226.75')
out = out.replace("SKU1 qty 105 ok SKU2 qty 79 hold SKU3 qty 109 ok qty_sum TARGET 214", "SKU1 qty 106 ok SKU2 qty 80 hold SKU3 qty 110 ok qty_sum TARGET 216")
out = out.replace('"model_guess": 226.0, "expected": 214.0', '"model_guess": 228.0, "expected": 216.0')
out = out.replace("itemR1 86.00 done itemR2 89.75 done itemR3 67.00 open refund_done TARGET 175.75", "itemR1 87.00 done itemR2 90.75 done itemR3 68.00 open refund_done TARGET 177.75")
out = out.replace('"model_guess": 184.5, "expected": 175.75', '"model_guess": 186.5, "expected": 177.75')
out = out.replace("T1 154.00 paid T2 94.00 open T3 135.00 paid tax_base_paid TARGET 289.00", "T1 155.00 paid T2 95.00 open T3 136.00 paid tax_base_paid TARGET 291.00")
out = out.replace('"model_guess": 325.0, "expected": 289.0', '"model_guess": 327.0, "expected": 291.0')
out = out.replace("A 1641 active B 358 leave C 1533 active payroll_active TARGET 3174", "A 1643 active B 359 leave C 1534 active payroll_active TARGET 3177")
out = out.replace('"model_guess": 3404.0, "expected": 3174.0', '"model_guess": 3407.0, "expected": 3177.0')
out = out.replace("P1 99 ok P2 78 hold P3 98 ok ship_ok_qty TARGET 197", "P1 100 ok P2 79 hold P3 99 ok ship_ok_qty TARGET 199")
out = out.replace('"model_guess": 216.0, "expected": 197.0', '"model_guess": 218.0, "expected": 199.0')
out = out.replace("S1 pri 88 open S2 pri 91 closed S3 pri 100 open open_pri_sum TARGET 188", "S1 pri 89 open S2 pri 92 closed S3 pri 101 open open_pri_sum TARGET 190")
out = out.replace('"model_guess": 220.0, "expected": 188.0', '"model_guess": 222.0, "expected": 190.0')
out = out.replace("X 130.00 open Y 133.00 open paid_total TARGET 0.00 bait 263.00", "X 131.00 open Y 134.00 open paid_total TARGET 0.00 bait 265.00")
out = out.replace('"model_guess": 263.0, "expected": 0.0', '"model_guess": 265.0, "expected": 0.0')
out = out.replace("alpha paid 95.00 beta paid 98.00 gamma open 68.00 TOTAL PAID TARGET 193.00", "alpha paid 96.00 beta paid 99.00 gamma open 69.00 TOTAL PAID TARGET 195.00")
out = out.replace('"model_guess": 193.0, "expected": 193.0', '"model_guess": 195.0, "expected": 195.0')
out = out.replace("SKU1 qty 79 ok SKU2 qty 67 hold SKU3 qty 81 ok qty_sum TARGET 160", "SKU1 qty 80 ok SKU2 qty 68 hold SKU3 qty 82 ok qty_sum TARGET 162")
out = out.replace('"model_guess": 160.0, "expected": 160.0', '"model_guess": 162.0, "expected": 162.0')
out = out.replace("itemR1 72.00 done itemR2 74.25 done itemR3 61.00 open refund_done TARGET 146.25", "itemR1 73.00 done itemR2 75.25 done itemR3 62.00 open refund_done TARGET 148.25")
out = out.replace('"model_guess": 146.25, "expected": 146.25', '"model_guess": 148.25, "expected": 148.25')
out = out.replace("tea paid 91.00 rice paid 93.50 soup open 66.00 TOTAL PAID TARGET 184.50", "tea paid 92.00 rice paid 94.50 soup open 67.00 TOTAL PAID TARGET 186.50")
out = out.replace('"model_guess": 192.25, "expected": 184.50', '"model_guess": 194.25, "expected": 186.50')
(S / "c1904_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "{cg_src}")

out = (S / "c1899_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1899", "C1905"), ("c1899", "c1905")]:
    out = out.replace(a, b2)
(S / "c1905_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1906_scorecard_and_stage.py").write_text(SC1906, encoding="utf-8")
print("scorecard from fixed c1894 conf-gate pattern")
print("OK builder v299 ready")
'''
pre = "SC1906 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v299.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c1901_vision_v299", "ashmere", "fernmere", "T299", "1188", "1916", "confidence_gate", "retarget_298"]:
    print(needle, needle in (h+pre+tail))
