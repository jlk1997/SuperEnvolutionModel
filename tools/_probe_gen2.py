from pathlib import Path
t = Path("tools/_gen_v51_slim.py").read_text(encoding="utf-8")
Path("tools/_gen_v51_slim_dump.txt").write_text(t, encoding="utf-8")
print("written", len(t))
# print rest after first 3000
print(t[3000:8000])
