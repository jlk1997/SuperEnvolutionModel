from pathlib import Path
import re
for ver in ["v49","v50","v51"]:
    for p in Path("scripts").glob(f"*vision_{ver}_design*.py"):
        t=p.read_text(encoding="utf-8")
        themes=re.findall(r'"('+ver+r'_\d+)",\s*"(\w+)"', t)
        print(ver, [x[1] for x in themes])
