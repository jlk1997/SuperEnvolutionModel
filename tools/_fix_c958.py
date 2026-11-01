# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"E:\envolution\scripts\c958_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")
# Fix leftover v140 vars that should be v141 (rate vars)
# After our partial rename, v141 = float(...) exists but some refs still say v140 for the smoke rate
fixes = [
    ("and v140 >= GATE and v141h >= GATE", "and v141 >= GATE and v141h >= GATE"),
    ("(v140 >= 0.999 and v141h >= 0.999) else min(v140, v141h)", "(v141 >= 0.999 and v141h >= 0.999) else min(v141, v141h)"),
    ('"v141": {"rate": v140, "claim": v141_claim', '"v141": {"rate": v141, "claim": v141_claim'),
    ("rate={v140} claim={v141_claim}", "rate={v141} claim={v141_claim}"),
    ("smoke **{v140}**", "smoke **{v141}**"),
    ("**C947-C958 STAGE_READY", "**C953-C958 STAGE_READY"),
    ("- C947: Vision V141 design fixtures", "- C953: Vision V141 design fixtures"),
    ("f\"- C956: confidence-gate replace={replace} pass={u2c_pass}\"",
     "f\"- C956: confidence-gate pass={conf_pass} rate={conf_rate}\",\n"
     "        f\"- product-U2C (prior C950): replace={replace} pass={u2c_pass}\""),
]
for a, b in fixes:
    if a not in t:
        print("MISSING:", repr(a)[:80])
    else:
        t = t.replace(a, b)
        print("OK:", repr(a)[:60])
p.write_text(t, encoding="utf-8")
print("---verify---")
for line in t.splitlines():
    if "v140" in line.lower() or "C947" in line or "stage_ready" in line or "C956:" in line:
        print(line)