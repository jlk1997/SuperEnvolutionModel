from pathlib import Path
ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v292.py").read_text(encoding="utf-8")
b = b.replace("# PLACEHOLDER_TAIL\n", "")
sc_body = (ROOT / "scripts/_sc1864_template.py").read_text(encoding="utf-8")
tail = '''# V292 knife = product-U2C (alternating; V291 was confidence-gate)
out = (S / "c1850_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1850", "C1862"), ("c1850", "c1862"),
    ("C1838", "C1862"), ("c1838", "c1862"),
    ("product_u2c_cost_c1850", "product_u2c_cost_c1862"),
    ("u2c_v189", "u2c_v190"),
    ("u2c_c1850", "u2c_c1862"),
]:
    out = out.replace(a, b2)
(S / "c1862_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1850_product_u2c_cost.py")

out = (S / "c1857_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1857", "C1863"), ("c1857", "c1863")]:
    out = out.replace(a, b2)
(S / "c1863_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1864_scorecard_and_stage.py").write_text(SC1864, encoding="utf-8")
print("scorecard from fixed c1852 pattern")
print("OK builder v292 ready")
'''
# Inject SC1864 as a module-level string before the knife section
# Find a good insert point: after S = ROOT / "scripts" or similar
if "S = " not in b and "S=" not in b.split("knife")[0]:
    # builders usually define S early; check
    pass
# Prepend SC1864 constant just before knife marker by putting assignment at start of tail
pre = "SC1864 = " + repr(sc_body) + "\n"
(ROOT / "tools/_build_v292.py").write_text(b + pre + tail, encoding="utf-8")
print("builder bytes", (ROOT / "tools/_build_v292.py").stat().st_size)
