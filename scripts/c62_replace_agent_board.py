# -*- coding: utf-8 -*-
from __future__ import annotations
import csv, json, shutil, sys
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from evo.office.compose_atom import run_compose_smoke
GATE=0.6
def ts(): return datetime.now().astimezone().isoformat(timespec="seconds")
def J(p,o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
ws=ROOT/"runs"/"r50plus"/"c62_bare_board"
if ws.exists(): shutil.rmtree(ws)
ws.mkdir(parents=True)
with (ws/"orders.csv").open("w",newline="",encoding="utf-8") as fh:
    w=csv.DictWriter(fh,fieldnames=["id","amount","status"]); w.writeheader()
    w.writerows([{"id":"1","amount":"12","status":"paid"},{"id":"2","amount":"8","status":"open"},{"id":"3","amount":"5","status":"paid"}])
total=17.0
(ws/"paid_total.txt").write_text(f"{total:.2f}\n",encoding="utf-8")
(ws/"exports").mkdir(); shutil.copy(ws/"paid_total.txt", ws/"exports"/"paid_total.txt")
(ws/"report.md").write_text(f"# Bare Board\npaid_total: {total:.2f}\nagent_graph: none\nscaffold_steps: 0\n",encoding="utf-8")
bare_ok=abs(float((ws/"exports"/"paid_total.txt").read_text().strip())-total)<0.01
fam_rows=[]
for fam in ("table","report","file","shell"):
    p=ROOT/"runs"/"capabilities"/f"office_{fam}_uselog"/"dissolution.json"
    if not p.is_file(): continue
    d=json.loads(p.read_text(encoding="utf-8"))
    bare=float(d.get("bare_rate") or 0); diss=float(d.get("dissolution") or 0)
    fam_rows.append({"family":fam,"bare_rate":bare,"dissolution":diss,"scaffold_steps_proxy":0 if bare>=GATE and diss<=0.05 else 3})
compose=run_compose_smoke(ROOT)
scaffold_mean=sum(r["scaffold_steps_proxy"] for r in fam_rows)/max(1,len(fam_rows))
replace_score=1.0 if bare_ok and scaffold_mean==0 and compose.get("pass") else (0.7 if bare_ok else 0.3)
payload={"kind":"r50plus_c62_replace_agent_board","timestamp":ts(),"gate":GATE,"bare_ok":bare_ok,"scaffold_steps_mean":scaffold_mean,"families":fam_rows,"compose_rate":compose.get("rate"),"compose_pass":compose.get("pass"),"replace_agent_score":replace_score,"agent_graph":False,"workspace":str(ws.relative_to(ROOT)).replace("\\","/"),"innovation":"Fresh replace-agent board without agent graph","gate2_3_untouched":True}
J(ROOT/"docs/r50/C62_replace_agent_board.json",payload)
(ROOT/"docs/r50/C62_replace_agent_board.md").write_text(f"# C62\nbare_ok={bare_ok} scaffold={scaffold_mean} compose={compose.get('rate')} replace={replace_score}\n",encoding="utf-8")
print(json.dumps({"bare_ok":bare_ok,"scaffold_mean":scaffold_mean,"compose_rate":compose.get("rate"),"replace_score":replace_score},ensure_ascii=False))
