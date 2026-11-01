from pathlib import Path
import re

ROOT = Path(r"E:/envolution")
b0 = (ROOT / "tools/_build_v257.py").read_text(encoding="utf-8")
idx0 = b0.find('# V257 knife = confidence-gate')
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
    ("T257", "T258"), ("TR257", "TR258"), ("HO257", "HO258"),
    ("NEW257", "NEW258"),
    ("V257", "V258"), ("v257", "v258"),
    ("_v257_themes.json", "_v258_themes.json"),
    ("_v256_themes.json", "_v257_themes.json"),
    ("OLD256", "OLD257"),
    ("vision_images_v257", "vision_images_v258"),
    ("VL_GATE_V257", "VL_GATE_V258"), ("vl_gate_v257", "vl_gate_v258"),
    ("C1649", "C1655"), ("c1649", "c1655"),
    ("C1650", "C1656"), ("c1650", "c1656"),
    ("C1651", "C1657"), ("c1651", "c1657"),
    ("_v257c1649", "_v258c1655"),
    ("Harder than V255", "Harder than V256"),
    ("harder than V255", "harder than V256"),
    ("NEW themes vs V255:", "NEW themes vs V256:"),
    ("kept on V257", "kept on V258"),
    ("V257 keeps floor", "V258 keeps floor"),
    ("C1649 design+fixtures; no VL claim", "C1655 design+fixtures; no VL claim"),
    ("retarget_256", "retarget_257"),
    ("*croft", "*holm"),
]
h = head0
for a, c in theme_pairs:
    h = h.replace(a, c)
for a, c in pairs:
    h = h.replace(a, c)

h = h.replace("ASHHOLM bait 170.80", "ASHHOLM bait 171.81")
h = h.replace("CEDARC bait 172.82", "CEDARH bait 173.83")
h = h.replace("DAWNC ghost 95.95", "DAWNH ghost 96.96")
h = h.replace("GLENC bait 165.75", "GLENH bait 166.76")
h = h.replace("JADEC bait 156.66", "JADEH bait 157.67")
h = h.replace("NETHERC bait 173.83", "NETHERH bait 174.84")

TR = '''TR258 = [
    [2162.0, 2179.5, 1902.0],[840, 760, 820],[2085.0, 2114.25, 1880.0],[2218.0, 2235.0, 1970.0],
    [2280.0, 2304.0, 1940.0],[1998, 2014, 1898],[480.0, 520.0, 740.0],[2128.0, 2159.75, 1904.0],
    [840.0, 760.0, 820.0],[2195.0, 2183.0, 1901.0],[1,1,0],[0,0,0],
    [2261.0, 2282.5, 1926.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]'''
HO = '''HO258 = [
    [1960.0, 1972.75, 1821.0],[740, 780, 820],[1903.0, 1917.5, 1796.0],[2033.0, 2049.0, 1852.0],
    [2074.0, 2090.0, 1845.0],[1856, 1868, 1814],[360.0, 400.0, 730.0],[1944.0, 1965.75, 1821.0],
    [780.0, 740.0, 820.0],[1991.0, 1977.0, 1816.0],[1,1,0],[0,0,0],
    [2026.0, 2041.5, 1831.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]'''
h = re.sub(r'TR258\s*=\s*\[[\s\S]*?\n\]', TR, h, count=1)
h = re.sub(r'HO258\s*=\s*\[[\s\S]*?\n\]', HO, h, count=1)
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')

src = "c1646_product_u2c_cost.py"
if not (ROOT / "scripts" / src).exists():
    src = "c1634_product_u2c_cost.py"
sc_src = "c1648_scorecard_and_stage.py"

tail = f'''# V258 knife = product-U2C (alternating; V257 was confidence-gate)
out = (S / "{src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1646", "C1658"), ("c1646", "c1658"),
    ("C1634", "C1658"), ("c1634", "c1658"),
    ("C1466", "C1658"), ("c1466", "c1658"),
]:
    out = out.replace(a, b2)
(S / "c1658_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "{src}")

out = (S / "c1653_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1653", "C1659"), ("c1653", "c1659")]:
    out = out.replace(a, b2)
(S / "c1659_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "{sc_src}").read_text(encoding="utf-8")
for a, b2 in [
    ("C1648", "C1660"), ("c1648", "c1660"),
    ("C1646", "C1658"), ("c1646", "c1658"),
    ("C1647", "C1659"), ("c1647", "c1659"),
    ("C1644", "C1656"), ("c1644", "c1656"),
    ("C1645", "C1657"), ("c1645", "c1657"),
    ("V256", "V258"), ("v256", "v258"),
    ("STAGE_ANT_C1648", "STAGE_ANT_C1660"),
    ("*vale", "*holm"),
]:
    out = out.replace(a, b2)
(S / "c1660_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "{sc_src}")
print("OK builder v258 ready")
'''
(ROOT / "tools/_build_v258.py").write_text(h + tail, encoding="utf-8")
print("wrote", len(h)+len(tail))
for needle in ["c1655_vision_v258", "ashholm", "fernholm", "T258", "1188", "1852", "product_u2c"]:
    print(needle, needle in (h+tail))
