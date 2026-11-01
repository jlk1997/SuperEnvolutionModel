# -*- coding: utf-8 -*-
"""C338: add honest sla_ok_hours atom parse for Nh ok / N hours ok OCR."""
from pathlib import Path

p = Path("evo/office/vision_metric_parse.py")
t = p.read_text(encoding="utf-8")
old = """    elif metric == \"open_pri_sum\":
        got = sum_pri_open(t)

    if got is not None and abs(got - exp) < tol:"""
new = """    elif metric == \"open_pri_sum\":
        got = sum_pri_open(t)
    elif metric == \"sla_ok_hours\":
        # C338: sum hours marked ok — OCR often yields \"43.00h ok\" / \"43.00 hours ok\".
        # Do not count late/rate/hold; TARGET line alone is brittle under watermark ($1.50).
        got = 0.0
        for m in re.finditer(r\"(\\d+\\.?\\d*)\\s*h(?:ours)?\\s+ok\\b\", t):
            v = float(m.group(1))
            if not _is_noise(v):
                got += v
        got = round(got, 2)

    if got is not None and abs(got - exp) < tol:"""
if "elif metric == \"sla_ok_hours\":" in t and "C338" in t:
    print("already patched")
else:
    if old not in t:
        raise SystemExit("anchor missing")
    p.write_text(t.replace(old, new, 1), encoding="utf-8")
    print("patched")
