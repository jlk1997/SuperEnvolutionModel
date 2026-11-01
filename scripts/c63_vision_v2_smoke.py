# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re, sys
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from evo.office.vision_backend import RealVlBackend, VisionObs
from scripts.vision_softmatch import softmatch
GATE=0.6
WEIGHTS=ROOT/"models"/"Qwen3.5-2B"
def ts(): return datetime.now().astimezone().isoformat(timespec="seconds")
def J(p,o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
img_dir=ROOT/"evo/office/fixtures/vision_images_v2"
ids=sorted(p.stem for p in img_dir.glob("*.png"))
backend=RealVlBackend(WEIGHTS, max_new_tokens=128)
items=[]; n_ok=0
for fid in ids:
    meta=json.loads((img_dir/f"{fid}.json").read_text(encoding="utf-8"))
    task=meta.get("task") or "caption"; gold=str(meta.get("gold") or "")
    try:
        pred=backend.predict(VisionObs(image_path=img_dir/f"{fid}.png", task=task, gold=gold))
        text=pred.text or ""
        text=re.sub(r"<think>[\s\S]*?</think>", " ", text)
        text=re.sub(r"\s+", " ", text).strip()
        ok=softmatch(text, gold, task); err=None
    except Exception as e:
        text, ok, err = "", False, f"{type(e).__name__}: {e}"
    n_ok += int(ok)
    items.append({"id":fid,"task":task,"gold":gold,"pred_head":text[:220],"ok":ok,"error":err})
n=len(items); rate=n_ok/n if n else 0.0; claim=bool(rate>=GATE and n>=8)
payload={"kind":"r50plus_c63_vision_v2_smoke","timestamp":ts(),"gate":GATE,"n":n,"n_ok":n_ok,"rate":round(rate,4),"gate_pass":claim,"vl_gate_v2_claim":claim,"claim_scope":("r50plus_v2_harder_readable_office_drawn_n>=8_softmatch_qwen35_2b" if claim else None),"items":items,"weights":"models/Qwen3.5-2B","v1_claim_untouched":True,"gate2_3_untouched":True,"open_domain_benchmark":False,"innovation":"First honest Vision V2 smoke on harder fixtures"}
J(ROOT/"docs/r50/C63_vision_v2_smoke.json",payload)
if claim:
    J(ROOT/"docs/r50/C63b_vision_gate_v2_claim.json",{"kind":"vision_gate_v2_claim","timestamp":ts(),"vl_gate_v2_claim":True,"rate":round(rate,4),"n":n,"n_ok":n_ok,"gate":GATE,"claim_scope":payload["claim_scope"],"gate2_3_untouched":True,"v1_untouched":True})
del backend
try:
    import torch; torch.cuda.empty_cache()
except Exception:
    pass
print(json.dumps({"rate":round(rate,4),"n":n,"n_ok":n_ok,"claim":claim},ensure_ascii=False))
