from pathlib import Path
import re
p = Path("scripts/c724_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")
t = re.sub(
    r'f"- C722: product-U2C.*",',
    'f"- C722: product-U2C replace={replace} pass={u2c_pass}",',
    t,
)
needle = 'replace = float(u2c.get("replace_ratio") or 4.07)'
if "u2c_pass =" not in t:
    t = t.replace(
        needle,
        needle + '\n    u2c_pass = bool((u2c or {}).get("pass"))',
    )
p.write_text(t, encoding="utf-8")
print("patched")
for ln in t.splitlines():
    if "C722" in ln or "u2c_pass" in ln:
        print(ln)
