from pathlib import Path
import re, json

ROOT = Path(r"E:/envolution")
# Patch builder TR/HO stack to mid-band (anti crush; V219/V226 lesson)
b = (ROOT / "tools/_build_v238.py").read_text(encoding="utf-8")
# TR stack was [1200, 1192, 1172] -> [1156, 1148, 1128]
# HO stack was [1188, 1183, 1176] -> [1148, 1143, 1136]
# also lower fax/tab slightly to stay coherent mid-band
TR = '''TR238 = [
    [1978.0, 1995.5, 1734.0],[840, 760, 820],[1901.0, 1930.25, 1714.0],[2034.0, 2051.0, 1804.0],
    [2096.0, 2120.0, 1774.0],[1832, 1848, 1732],[480.0, 520.0, 740.0],[1944.0, 1975.75, 1738.0],
    [840.0, 760.0, 820.0],[2011.0, 1999.0, 1735.0],[1,1,0],[0,0,0],
    [2077.0, 2098.5, 1760.0],[1,0,0],[1156, 1148, 1128],[1172, 1156, 748],[1,0,0],[1188, 1172, 1150],
]'''
HO = '''HO238 = [
    [1794.0, 1806.75, 1655.0],[740, 780, 820],[1737.0, 1750.5, 1630.0],[1867.0, 1883.0, 1684.0],
    [1908.0, 1924.0, 1679.0],[1702, 1716, 1648],[360.0, 400.0, 730.0],[1778.0, 1799.75, 1655.0],
    [780.0, 740.0, 820.0],[1825.0, 1811.0, 1650.0],[1,1,0],[0,0,0],
    [1860.0, 1875.5, 1665.0],[1,0,0],[1148, 1143, 1136],[1162, 1156, 1144],[1,0,0],[1172, 1166, 1145],
]'''
BAN = {755, 756, 770, 750, 830, 1830, 1560}
for label, block in [('TR', TR), ('HO', HO)]:
    for n in re.findall(r'[\d.]+', block):
        v = float(n)
        if int(v) in BAN:
            raise SystemExit(f'banned {v} in {label}')
b = re.sub(r'TR238\s*=\s*\[[\s\S]*?\n\]', TR, b, count=1)
b = re.sub(r'HO238\s*=\s*\[[\s\S]*?\n\]', HO, b, count=1)
(ROOT / "tools/_build_v238.py").write_text(b, encoding="utf-8")
print("ABC patched")
