from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v265.py").read_text(encoding="utf-8")
idx0 = b0.find('# V265 knife = confidence-gate')
if idx0 < 0:
    raise SystemExit('knife not found')
head0 = b0[:idx0]

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
    ("T265", "T266"), ("TR265", "TR266"), ("HO265", "HO266"),
    ("NEW265", "NEW266"),
    ("V265", "V266"), ("v265", "v266"),
    ("_v265_themes.json", "_v266_themes.json"),
    ("_v264_themes.json", "_v265_themes.json"),
    ("OLD264", "OLD265"),
    ("vision_images_v265", "vision_images_v266"),
    ("VL_GATE_V265", "VL_GATE_V266"), ("vl_gate_v265", "vl_gate_v266"),
    ("C1697", "C1703"), ("c1697", "c1703"),
    ("C1698", "C1704"), ("c1698", "c1704"),
    ("C1699", "C1705"), ("c1699", "c1705"),
    ("_v265c1697", "_v266c1703"),
    ("Harder than V263", "Harder than V264"),
    ("harder than V263", "harder than V264"),
    ("NEW themes vs V263:", "NEW themes vs V264:"),
    ("kept on V265", "kept on V266"),
    ("V265 keeps floor", "V266 keeps floor"),
    ("C1697 design+fixtures; no VL claim", "C1703 design+fixtures; no VL claim"),
    ("retarget_264", "retarget_265"),
    ("*hurst", "*mere"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHMERE bait 178.88", "ASHMERE bait 179.89")
h = h.replace("CEDARH bait 180.90", "CEDARM bait 181.91")
h = h.replace("DAWNH ghost 103.13", "DAWNM ghost 104.14")
h = h.replace("GLENH bait 173.83", "GLENM bait 174.84")
h = h.replace("JADEH bait 164.74", "JADEM bait 165.75")
h = h.replace("NETHERH bait 181.91", "NETHERM bait 182.92")

TR = '''TR266 = [
    [2178.0, 2195.5, 1918.0],[840, 760, 820],[2101.0, 2130.25, 1896.0],[2234.0, 2251.0, 1986.0],
    [2296.0, 2320.0, 1956.0],[2014, 2030, 1914],[480.0, 520.0, 740.0],[2144.0, 2175.75, 1920.0],
    [840.0, 760.0, 820.0],[2211.0, 2199.0, 1917.0],[1,1,0],[0,0,0],
    [2277.0, 2298.5, 1942.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
# HO order c was 1832 - bump to 1834; avoid 1830
HO = '''HO266 = [
    [1976.0, 1988.75, 1837.0],[740, 780, 820],[1919.0, 1933.5, 1812.0],[2049.0, 2065.0, 1868.0],
    [2090.0, 2106.0, 1861.0],[1872, 1884, 1830],[360.0, 400.0, 730.0],[1960.0, 1981.75, 1837.0],
    [780.0, 740.0, 820.0],[2007.0, 1993.0, 1834.0],[1,1,0],[0,0,0],
    [2042.0, 2057.5, 1847.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
# Wait - HO ship c=1830 BAN! Fix ship to 1834/1846/1832 style
HO = '''HO266 = [
    [1976.0, 1988.75, 1837.0],[740, 780, 820],[1919.0, 1933.5, 1812.0],[2049.0, 2065.0, 1868.0],
    [2090.0, 2106.0, 1861.0],[1872, 1884, 1832],[360.0, 400.0, 730.0],[1960.0, 1981.75, 1837.0],
    [780.0, 740.0, 820.0],[2007.0, 1993.0, 1834.0],[1,1,0],[0,0,0],
    [2042.0, 2057.5, 1847.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR266\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO266\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

src = "c1694_product_u2c_cost.py"
if not (ROOT / "scripts" / src).exists():
    src = "c1682_product_u2c_cost.py"
sc_src = "c1696_scorecard_and_stage.py"

tail = f'''# V266 knife = product-U2C (alternating; V265 was confidence-gate)
out = (S / "{src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1694", "C1706"), ("c1694", "c1706"),
    ("C1682", "C1706"), ("c1682", "c1706"),
    ("C1466", "C1706"), ("c1466", "c1706"),
]:
    out = out.replace(a, b2)
(S / "c1706_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{src}")

out = (S / "c1701_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1701", "C1707"), ("c1701", "c1707")]:
    out = out.replace(a, b2)
(S / "c1707_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1696", "C1708"), ("c1696", "c1708"),
    ("C1694", "C1706"), ("c1694", "c1706"),
    ("C1695", "C1707"), ("c1695", "c1707"),
    ("C1692", "C1704"), ("c1692", "c1704"),
    ("C1693", "C1705"), ("c1693", "c1705"),
    ("V264", "V266"), ("v264", "v266"),
    ("STAGE_ANT_C1696", "STAGE_ANT_C1708"),
    ("*ford", "*mere"),
]:
    out = out.replace(a, b2)
(S / "c1708_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v266 ready")
'''
(ROOT / "tools/_build_v266.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1703_vision_v266", "ashmere", "fernmere", "T266", "1188", "1834", "product_u2c"]:
    print(needle, needle in (h+tail))
