from pathlib import Path
p = Path("scripts/c400_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")
old = 'disjoint = bool(c397.get("disjoint") or c397b.get("disjoint"))'
new = 'disjoint = bool(c397.get("id_disjoint") or c397.get("disjoint") or c397b.get("id_disjoint") or c397b.get("disjoint"))'
if old not in t:
    raise SystemExit("needle missing: " + repr(old[:60]))
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("ok")
