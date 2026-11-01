from pathlib import Path
t = Path("tools/_gen_v51_slim.py").read_text(encoding="utf-8")
print(t[:3000])
print("---")
print("len", len(t))
