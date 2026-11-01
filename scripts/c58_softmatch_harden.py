# -*- coding: utf-8 -*-
from __future__ import annotations
import json, sys
from datetime import datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.vision_softmatch import softmatch
GATE=0.6
def ts(): return datetime.now().astimezone().isoformat(timespec="seconds")
def J(p,o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
smoke=json.loads((ROOT/"docs/r50/C52_vision_v1_smoke_readable.json").read_text(encoding="utf-8"))
items=[]; n_ok=0; flipped=[]
for row in smoke["items"]:
    pred=row.get("pred_head") or ""; gold=row.get("gold") or ""; task=row.get("task") or "caption"
    ok_old=bool(row.get("ok"))
    ok_new=softmatch(pred,gold,task) if not row.get("error") else False
    n_ok+=int(ok_new)
    if ok_new and not ok_old: flipped.append(row["id"])
    items.append({**row,"ok_old":ok_old,"ok":ok_new,"softmatch_v2":True})
n=len(items); rate=n_ok/n if n else 0.0
payload={"kind":"r50plus_c58_v1_softmatch_harden","timestamp":ts(),"gate":GATE,"prior_rate":smoke.get("rate"),"rate":round(rate,4),"n":n,"n_ok":n_ok,"flipped_to_ok":flipped,"gate_pass":rate>=GATE and n>=8,"vl_gate_v1_claim_unchanged":True,"innovation":"Morphology-aware softmatch","items":items,"gate2_3_untouched":True}
J(ROOT/"docs/r50/C58_v1_softmatch_harden.json", payload)
J(ROOT/"docs/r50/C58_v1_claim_note.json", {"kind":"vision_v1_softmatch_harden_note","timestamp":ts(),"prior_claim_rate":0.8333,"rescored_rate":round(rate,4),"flipped":flipped,"claim_scope_unchanged":True,"gate2_3_untouched":True})
print(json.dumps({"rate":round(rate,4),"flipped":flipped,"n_ok":n_ok},ensure_ascii=False))
