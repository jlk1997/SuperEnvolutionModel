from pathlib import Path
ROOT = Path(r"E:/envolution")
b = (ROOT / "tools/_build_v228.py").read_text(encoding="utf-8")
repls = [
    ('(S / "c1470_vision_v228_smoke.py")', '(S / "c1476_vision_v228_smoke.py")'),
    ('("C1464", "C1470"), ("c1464", "c1470")', '("C1464", "C1476"), ("c1464", "c1476")'),
    ('(S / "c1471_vision_v228_heldout.py")', '(S / "c1477_vision_v228_heldout.py")'),
    ('("C1465", "C1471"), ("c1465", "c1471")', '("C1465", "C1477"), ("c1465", "c1477")'),
    ('RUN = ROOT / "runs/vision_v228h_c1471"', 'RUN = ROOT / "runs/vision_v228h_c1477"'),
    ("fixtures only; claim deferred to C1470 VL smoke", "fixtures only; claim deferred to C1476 VL smoke"),
    ("No claim until C1470 VL", "No claim until C1476 VL"),
]
for a, c in repls:
    if a not in b:
        print("MISSING", repr(a[:70]))
    else:
        b = b.replace(a, c)
        print("ok", a[:50])
idx = b.find('out = (S / "c1460_confidence_gate_stretch.py").read_text')
if idx < 0:
    raise SystemExit("cg block not found")
head = b[:idx]
tail = r'''# V228 knife = product-U2C (alternating; V227 was conf-gate)
out = (S / "c1466_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1466", "C1478"), ("c1466", "c1478"),
    ("product_u2c_c1466", "product_u2c_c1478"),
    ("vs C1454", "vs C1466"),
]:
    out = out.replace(a, b2)
(S / "c1478_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c")

out = (S / "c1467_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1467", "C1479"), ("c1467", "c1479"),
]:
    out = out.replace(a, b2)
(S / "c1479_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1468_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1468", "C1480"), ("c1468", "c1480"),
    ("C1466", "C1478"), ("c1466", "c1478"),
    ("C1467", "C1479"), ("c1467", "c1479"),
    ("C1464", "C1476"), ("c1464", "c1476"),
    ("C1465", "C1477"), ("c1465", "c1477"),
    ("V226", "V228"), ("v226", "v228"),
    ("STAGE_ANT_C1468", "STAGE_ANT_C1480"),
    ("*wick", "*fen"),
]:
    out = out.replace(a, b2)
(S / "c1480_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard")
print("OK builder v228 ready")
'''
(ROOT / "tools/_build_v228.py").write_text(head + tail, encoding="utf-8")
print("wrote", len(head) + len(tail))
