# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("scripts/c289_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")
needle = '    c263 = load("docs/r50/C263_DISSOLVE_COST_SHADOW.json") or {}\n    c269 = load("docs/r50/C287_CONFIDENCE_GATE_STRETCH.json") or {}\n'
insert = (
    '    c263 = load("docs/r50/C263_DISSOLVE_COST_SHADOW.json") or {}\n'
    '    c281 = load("docs/r50/C281_PRODUCT_U2C_COST.json") or {}\n'
    '    c269 = load("docs/r50/C287_CONFIDENCE_GATE_STRETCH.json") or {}\n'
)
if "C281_PRODUCT_U2C_COST" not in t:
    if needle not in t:
        raise SystemExit("needle missing")
    t = t.replace(needle, insert)
t = t.replace(
    'rl = (c269.get("replace_ledger") or {})',
    'rl = ((c281.get("replace_ledger") if "c281" in dir() or True else {}) or c269.get("replace_ledger") or {})',
)
# cleaner replace of rl line
t = t.replace(
    'rl = ((c281.get("replace_ledger") if "c281" in dir() or True else {}) or c269.get("replace_ledger") or {})',
    'rl = (c281.get("replace_ledger") or c269.get("replace_ledger") or {})',
)
t = t.replace(
    '"source": "C287" if rl.get("mean_ratio") is not None else "C263"',
    '"source": "C281" if (c281.get("replace_ledger") or {}).get("mean_ratio") is not None else ("C287" if rl.get("mean_ratio") is not None else "C263")',
)
p.write_text(t, encoding="utf-8")
compile(t, "c289", "exec")
print("ok")
