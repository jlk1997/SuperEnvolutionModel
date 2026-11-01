from pathlib import Path
p = Path("scripts/c730_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")
t = t.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C722"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C728"}',
)
# also ensure c656 loads C728
if 'C728_CONFIDENCE_GATE_STRETCH' not in t:
    t = t.replace(
        'c656 = load("docs/r50/C716_CONFIDENCE_GATE_STRETCH.json") or {}',
        'c656 = load("docs/r50/C728_CONFIDENCE_GATE_STRETCH.json") or {}',
    )
p.write_text(t, encoding="utf-8")
print([ln.strip() for ln in t.splitlines() if "confidence_gate" in ln or "C728_CONF" in ln or "C722_PRODUCT" in ln])
