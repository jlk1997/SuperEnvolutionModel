from pathlib import Path
import re
ROOT = Path(r"E:/envolution")
p = (ROOT / "tools/_patch_v336_builder.py").read_text(encoding="utf-8")

TR = """TR336 = [
    [2336.0, 2353.5, 2076.0],[840, 760, 820],[2254.0, 2255.25, 2049.0],[2392.0, 2409.0, 2144.0],
    [2454.0, 2478.0, 2114.0],[2172, 2188, 2072],[490.0, 530.0, 760.0],[2302.0, 2333.75, 2078.0],
    [840.0, 760.0, 820.0],[2369.0, 2357.0, 2075.0],[1,1,0],[0,0,0],
    [2435.0, 2456.5, 2100.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]"""
HO = """HO336 = [
    [2134.0, 2146.75, 1995.0],[640, 660, 820],[2077.0, 2091.5, 1970.0],[2207.0, 2223.0, 2026.0],
    [2243.0, 2254.0, 2019.0],[2030, 2042, 1992],[420.0, 460.0, 740.0],[2118.0, 2139.75, 1995.0],
    [740.0, 780.0, 820.0],[2165.0, 2151.0, 1992.0],[1,1,0],[0,0,0],
    [2200.0, 2215.5, 2005.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]"""
p = re.sub(r"TR = '''TR336 = \[[\s\S]*?\]'''", "TR = '''" + TR + "'''", p, count=1)
p = re.sub(r"HO = '''HO336 = \[[\s\S]*?\]'''", "HO = '''" + HO + "'''", p, count=1)

sc_and_tail = r'''
sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2092", "C2128"), ("c2092", "c2128"),
    ("C2090", "C2126"), ("c2090", "c2126"),
    ("C2091", "C2127"), ("c2091", "c2127"),
    ("C2088", "C2124"), ("c2088", "c2124"),
    ("C2089", "C2125"), ("c2089", "c2125"),
    ("C2084", "C2120"), ("c2084", "c2120"),
    ("C2087", "C2123"), ("c2087", "c2123"),
    ("V330", "V336"), ("v330", "v336"),
    ("STAGE_ANT_C2092", "STAGE_ANT_C2128"),
    ("*ford", "*wick"),
]:
    sc_body = sc_body.replace(a, b2)

tail = f'''# V336 knife = product-U2C (alternating; V335 was confidence-gate)
out = (S / "c2114_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2114", "C2126"), ("c2114", "c2126"),
    ("C2102", "C2126"), ("c2102", "c2126"),
    ("product_u2c_cost_c2114", "product_u2c_cost_c2126"),
    ("u2c_v211", "u2c_v212"),
    ("u2c_c2114", "u2c_c2126"),
]:
    out = out.replace(a, b2)
(S / "c2126_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2114")

out = (S / "c2121_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2121", "C2127"), ("c2121", "c2127")]:
    out = out.replace(a, b2)
(S / "c2127_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2128_scorecard_and_stage.py").write_text(SC2128, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v336 ready")
'''
pre = "SC2128 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v336.py").write_text(h + pre + tail, encoding="utf-8")
print("wrote", len(h)+len(pre)+len(tail))
for needle in ["c2123_vision_v336", "ashwick", "fernwick", "T336", "1188", "1992", "product_u2c", "retarget_335", "2255.25"]:
    print(needle, needle in (h+pre+tail))
'''
idx = p.find('sc_body = (ROOT / "scripts/c2092_scorecard_and_stage.py")')
if idx < 0:
    raise SystemExit("sc_body not found")
p = p[:idx] + sc_and_tail.lstrip("\n")
(ROOT / "tools/_patch_v336_builder.py").write_text(p, encoding="utf-8")
print("patch fixed", len(p))
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f"banned {v} in {label}")
print("BAN ok", "2255.25" in TR)
