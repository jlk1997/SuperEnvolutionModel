from pathlib import Path
from evo.office.compose_atom import run_compose_smoke
import json
from datetime import datetime
ROOT=Path(__file__).resolve().parents[1]
ev=run_compose_smoke(ROOT)
p=ROOT/"docs"/f"COMPOSE_FAMILY_SMOKE_{datetime.now().strftime("%Y-%m-%d")}.json"
p.write_text(json.dumps(ev,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"pass":ev["pass"],"rate":ev["rate"],"path":str(p)},ensure_ascii=False))
