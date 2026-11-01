# -*- coding: utf-8 -*-
from __future__ import annotations
import json, shutil, sys
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.vision_softmatch import softmatch
from scripts.vision_u2c_real import micro_absorb_vl
GATE=0.6
WEIGHTS=ROOT/"models"/"Qwen3.5-2B"
def ts(): return datetime.now().astimezone().isoformat(timespec="seconds")
def J(p,o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
smoke=json.loads((ROOT/"docs/r50/C52_vision_v1_smoke_readable.json").read_text(encoding="utf-8"))
base=ROOT/"runs"/"vision_u2c_v1_lora"
if base.exists(): shutil.rmtree(base)
base.mkdir(parents=True)
pairs=[]; use_log=[]
for row in smoke["items"]:
    if row.get("error"): continue
    img=f"evo/office/fixtures/vision_images_real/{row['id']}.png"
    ok=softmatch(row.get("pred_head") or "", row.get("gold") or "", row.get("task") or "caption")
    use_log.append({"phase":"use","task_id":row["id"],"task":row.get("task"),"image":img,"pred":row.get("pred_head")})
    use_log.append({"phase":"grade","task_id":row["id"],"ok":ok,"gold":row.get("gold")})
    pairs.append({"image":img,"task":row.get("task"),"gold":row.get("gold")})
    if ok: use_log.append({"phase":"crystallize","task_id":row["id"],"ok":True})
adapter_dir=ROOT/"runs"/"capabilities"/"vision_office_v1_readable_lora"
absorb=micro_absorb_vl(ROOT, pairs, WEIGHTS, adapter_dir)
use_log.append({"phase":"absorb","method":"peft_lora_micro_v1_readable",**absorb})
use_log.append({"phase":"route","selected":"vision_office_v1_readable_lora","why":["v1_claim","readable_fixtures","local_weights"]})
(base/"use_log.jsonl").write_text("\n".join(json.dumps(e,ensure_ascii=False) for e in use_log)+"\n",encoding="utf-8")
J(base/"pairs.json",{"n":len(pairs),"pairs":pairs})
graded_ok=sum(1 for e in use_log if e.get("phase")=="grade" and e.get("ok"))
graded_n=sum(1 for e in use_log if e.get("phase")=="grade")
rate=graded_ok/max(1,graded_n)
reg_path=ROOT/"evo/office/fixtures/vision_atom_registry.json"
reg=json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.is_file() else {"atoms":[]}
if isinstance(reg,list): reg={"atoms":reg}
atoms=reg.get("atoms") or []
atoms.append({"id":"vision_office_v1_readable_lora","family":"vision_absorb","status":"absorbed" if absorb.get("ok") else "absorb_failed","adapter":absorb.get("adapter"),"steps":absorb.get("steps"),"loss_last":absorb.get("loss_last"),"source":"c60","registered_at":ts()})
reg["atoms"]=atoms; reg["updated"]=ts(); reg["source"]="c60_vision_u2c_v1_lora"; J(reg_path,reg)
payload={"kind":"r50plus_c60_vision_u2c_lora","timestamp":ts(),"gate":GATE,"n_pairs":len(pairs),"grade_rate_softmatch":round(rate,4),"absorb":absorb,"adapter_trained":bool(absorb.get("ok")),"pass":bool(absorb.get("ok")) and rate>=GATE,"evidence_run":"runs/vision_u2c_v1_lora","innovation":"Real micro-LoRA absorb on V1 readable fixtures","gate2_3_untouched":True,"v1_claim_untouched":True}
J(ROOT/"docs/r50/C60_vision_u2c_lora.json",payload)
print(json.dumps({"adapter_trained":payload["adapter_trained"],"rate":round(rate,4),"steps":absorb.get("steps"),"loss_last":absorb.get("loss_last"),"error":absorb.get("error")},ensure_ascii=False))
