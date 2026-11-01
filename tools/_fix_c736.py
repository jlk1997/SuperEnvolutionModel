from pathlib import Path
import json
p = Path("scripts/c736_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")
t = t.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C734"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C728"}',
)
if 'C728_CONFIDENCE_GATE_STRETCH' not in t:
    t = t.replace(
        'c656 = load("docs/r50/C734_CONFIDENCE_GATE_STRETCH.json") or {}',
        'c656 = load("docs/r50/C728_CONFIDENCE_GATE_STRETCH.json") or {}',
    )
p.write_text(t, encoding="utf-8")
print("script ok", "C728_CONFIDENCE" in t)
