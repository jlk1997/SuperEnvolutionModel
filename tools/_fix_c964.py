from pathlib import Path
p = Path(r"scripts/c964_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")
t = t.replace(
    'c656 = load("docs/r50/C962_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C956_CONFIDENCE_GATE_STRETCH.json") or {}',
)
t = t.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C962"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C956"}',
)
p.write_text(t, encoding="utf-8")
assert "C956_CONFIDENCE_GATE_STRETCH" in t
assert '"source": "C956"' in t
print("c964 fixed")
