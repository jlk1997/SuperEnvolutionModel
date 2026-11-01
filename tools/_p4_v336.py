from pathlib import Path
import re
p = Path("tools/_patch_v336_builder.py")
t = p.read_text(encoding="utf-8")
reps = [
    ("ASHHOLM bait 246.56", "ASHWICK bait 249.59"),
    ("ASHCROFT bait 247.57", "ASHWICK bait 249.59"),
    ("CEDARV bait 248.58", "CEDARW bait 251.61"),
    ("CEDARC bait 249.59", "CEDARW bait 251.61"),
    ("DAWNV ghost 171.81", "DAWNW ghost 174.84"),
    ("DAWNC ghost 172.82", "DAWNW ghost 174.84"),
    ("GLENV bait 241.51", "GLENW bait 244.54"),
    ("GLENC bait 242.52", "GLENW bait 244.54"),
    ("JADEV bait 232.42", "JADEW bait 235.45"),
    ("JADEC bait 233.43", "JADEW bait 235.45"),
    ("NETHERV bait 249.59", "NETHERW bait 252.62"),
    ("NETHERC bait 250.60", "NETHERW bait 252.62"),
    ('"C2092", "C2116"', '"C2092", "C2128"'),
    ('"c2092", "c2116"', '"c2092", "c2128"'),
    ('"C2090", "C2114"', '"C2090", "C2126"'),
    ('"c2090", "c2114"', '"c2090", "c2126"'),
    ('"C2091", "C2115"', '"C2091", "C2127"'),
    ('"c2091", "c2115"', '"c2091", "c2127"'),
    ('"C2084", "C2108"', '"C2084", "C2120"'),
    ('"c2084", "c2108"', '"c2084", "c2120"'),
    ("STAGE_ANT_C2116", "STAGE_ANT_C2128"),
    ("SC2116", "SC2128"),
    ("c2116_scorecard_and_stage.py", "c2128_scorecard_and_stage.py"),
    ("c2102_product_u2c_cost.py", "c2114_product_u2c_cost.py"),
    ('"C2102", "C2114"', '"C2114", "C2126"'),
    ('"c2102", "c2114"', '"c2114", "c2126"'),
    ("product_u2c_cost_c2102", "product_u2c_cost_c2114"),
    ("product_u2c_cost_c2114", "product_u2c_cost_c2126"),
    ("u2c_v210", "u2c_v212"),
    ("u2c_c2102", "u2c_c2114"),
    ("u2c_c2114", "u2c_c2126"),
    ('c2114_product_u2c_cost.py").write_text', 'c2126_product_u2c_cost.py").write_text'),
    ("product_u2c from c2102", "product_u2c from c2114"),
    ("c2109_capture_office_regression.py", "c2121_capture_office_regression.py"),
    ('"C2109", "C2115"', '"C2121", "C2127"'),
    ('"c2109", "c2115"', '"c2121", "c2127"'),
    ("c2115_capture_office_regression.py", "c2127_capture_office_regression.py"),
]
for a, b in reps:
    t = t.replace(a, b)
TR = "TR336 = [\n    [2336.0, 2353.5, 2076.0],[840, 760, 820],[2254.0, 2255.25, 2049.0],[2392.0, 2409.0, 2144.0],\n    [2454.0, 2478.0, 2114.0],[2172, 2188, 2072],[490.0, 530.0, 760.0],[2302.0, 2333.75, 2078.0],\n    [840.0, 760.0, 820.0],[2369.0, 2357.0, 2075.0],[1,1,0],[0,0,0],\n    [2435.0, 2456.5, 2100.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],\n]"
HO = "HO336 = [\n    [2134.0, 2146.75, 1995.0],[640, 660, 820],[2077.0, 2091.5, 1970.0],[2207.0, 2223.0, 2026.0],\n    [2243.0, 2254.0, 2019.0],[2030, 2042, 1992],[420.0, 460.0, 740.0],[2118.0, 2139.75, 1995.0],\n    [740.0, 780.0, 820.0],[2165.0, 2151.0, 1992.0],[1,1,0],[0,0,0],\n    [2200.0, 2215.5, 2005.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],\n]"
t = re.sub(r"TR336\s*=\s*\[[\s\S]*?\n\]", TR, t, count=1)
t = re.sub(r"HO336\s*=\s*\[[\s\S]*?\n\]", HO, t, count=1)
# needle list at end
t = t.replace("2258.25", "2255.25")
t = t.replace("1988", "1992")
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [("TR", TR), ("HO", HO)]:
    for n in re.findall(r"[\d.]+", block):
        if int(float(n)) in BAN:
            raise SystemExit(f"banned {n} in {label}")
p.write_text(t, encoding="utf-8")
print("pass4ok", len(t))
for n in ["C2128", "C2126", "C2120", "c2126_product", "c2121_capture", "c2127_capture", "2255.25", "ASHWICK", "product_u2c from c2114"]:
    print(n, n in t)
