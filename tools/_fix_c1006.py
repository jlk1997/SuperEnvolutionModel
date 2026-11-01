from pathlib import Path
p = Path("scripts/c1006_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")
t = t.replace('c650 = load("docs/r50/C1004_PRODUCT_U2C_COST.json") or {}', 'c650 = load("docs/r50/C998_PRODUCT_U2C_COST.json") or {}')
t = t.replace('"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1004"}', '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C998"}')
# fix u2c construction source if present
import re
t = re.sub(r'(u2c = \{[^}]*"source": )"C1004"', r'\1"C998"', t)
t = t.replace('"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C998"}', '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1004"}')
assert "C1004_CONFIDENCE_GATE_STRETCH" in t and "C998_PRODUCT_U2C_COST" in t
p.write_text(t, encoding="utf-8")
print("ok")
for ln in t.splitlines():
    if ("c650" in ln or "c656" in ln or "source" in ln) and ("load" in ln or "product" in ln or "confidence" in ln or "C998" in ln or "C1004" in ln):
        print(ln.strip()[:160])
