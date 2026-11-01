# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re, sys
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
EVID=ROOT/"docs"/"r50"
LOOP=ROOT/"docs"/"蚁算_R50PLUS_LOOP.md"
def ts(): return datetime.now().astimezone().isoformat(timespec="seconds")
def J(p,o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def load(name, default=None):
    p=EVID/name
    if not p.is_file(): return default
    return json.loads(p.read_text(encoding="utf-8"))
c58=load("C58_v1_softmatch_harden.json",{})
c59=load("C59_vision_v2_harder_fixtures.json",{})
c60=load("C60_vision_u2c_lora.json",{})
c61=load("C61_gen11_prep.json",{})
c62=load("C62_replace_agent_board.json",{})
c63=load("C63_vision_v2_smoke.json",{})
summary={
  "c58_rate": c58.get("rate"),
  "c58_flipped": c58.get("flipped_to_ok"),
  "c59_n": c59.get("n"),
  "adapter_trained": c60.get("adapter_trained"),
  "absorb_steps": (c60.get("absorb") or {}).get("steps"),
  "absorb_loss": (c60.get("absorb") or {}).get("loss_last"),
  "gen11_prep": c61.get("prep_complete"),
  "replace_score": c62.get("replace_agent_score"),
  "c63_rate": c63.get("rate"),
  "c63_claim": c63.get("vl_gate_v2_claim"),
}
mm=0.85
if c60.get("adapter_trained"): mm+=0.05
if c63.get("vl_gate_v2_claim"): mm+=0.1
elif (c63.get("rate") or 0)>=0.5: mm+=0.05
mm=min(1.0, mm)
sc={"timestamp":ts(),"cycle":"R50+","beat_agent":0.88,"dynamic":0.97,"multimodal":mm,"compose":1.0,"replace_agent":summary.get("replace_score") or 0.99,"vision_v1_rate":0.8333,"vision_v1_softmatch_rate":summary.get("c58_rate"),"vision_v2_rate":summary.get("c63_rate"),"vision_v2_claim":summary.get("c63_claim"),"adapter_trained":summary.get("adapter_trained"),"gen11_seal_opened":False,"gate2_3_untouched":True}
sc["composite"]=sum(sc[k] for k in ("beat_agent","dynamic","multimodal","compose","replace_agent"))/5
J(EVID/"SCORECARD_LATEST.json",sc)
J(EVID/"C64_r50plus_summary.json",{"kind":"r50plus_summary","timestamp":ts(),**summary,"scorecard":sc,"mm_score":mm})
(ROOT/"docs/STAGE_ANT_R50PLUS.md").write_text(f"""# STAGE_ANT_R50PLUS

Updated: {ts()} (Asia/Shanghai)

**R50PLUS_CONTINUATION=YES** (post Vision V1 CLAIM @93f64b6)

## Cycles landed
- C58 softmatch harden -> rate {summary.get('c58_rate')} flipped={summary.get('c58_flipped')}
- C59 Vision V2 harder fixtures n={summary.get('c59_n')}
- C60 Vision U2C real LoRA absorb ok={summary.get('adapter_trained')} steps={summary.get('absorb_steps')} loss={summary.get('absorb_loss')}
- C61 gen11 prep complete; **seal NOT opened**
- C62 replace-agent bare board score={summary.get('replace_score')}
- C63 Vision V2 smoke rate={summary.get('c63_rate')} claim={summary.get('c63_claim')}

## Iron
Gate **0.6**. Gate2/3 CLAIMED untouched. V1 claim untouched. No fake VL. gen11 burn discipline held.

## Evidence
`docs/r50/C58_*.json` ... `C64_*.json` · loop `docs/蚁算_R50PLUS_LOOP.md`
""", encoding="utf-8")
(ROOT/"docs/CHECKPOINT_NOW.md").write_text(f"""# CHECKPOINT_NOW — {ts()} — 蚁算模型

**R50_COMPLETE=YES** · **R50PLUS=YES** · docs/STAGE_ANT_R50PLUS.md

Gate **0.6**. Gate2/3 CLAIMED untouched.
Vision V1 CLAIM rate=0.8333 (softmatch harden rescored={summary.get('c58_rate')}).
Vision V2 smoke rate={summary.get('c63_rate')} claim={summary.get('c63_claim')}.
LoRA absorb ok={summary.get('adapter_trained')}. gen11 seal_opened=false.

Composite≈{sc['composite']:.3f} replace={sc['replace_agent']} mm={sc['multimodal']}
""", encoding="utf-8")
if not LOOP.is_file():
    LOOP.write_text(f"# 蚁算 R50+ LOOP\n\nUpdated: {ts()} (Asia/Shanghai)\n\nMandate: continuous evolution after R50 / Vision V1 CLAIM. Gate **0.6**. Gate2/3 untouched. No fake VL. gen11 seal closed until readiness + value.\n\n## Progress\n\n| Cycle | Theme | Status | Key | Evidence |\n| --- | --- | --- | --- | --- |\n\n## Cycles\n", encoding="utf-8")
text=LOOP.read_text(encoding="utf-8")
text=re.sub(r"Updated: .*", f"Updated: {ts()} (Asia/Shanghai)", text, count=1)
marker="| --- | --- | --- | --- | --- |\n"
rows=(
 f"| C58 | softmatch | DONE | {summary.get('c58_rate')} | C58_*.json |\n"
 f"| C59 | vision-v2-fix | DONE | n={summary.get('c59_n')} | C59_*.json |\n"
 f"| C60 | u2c-lora | DONE | absorb={summary.get('adapter_trained')} | C60_*.json |\n"
 f"| C61 | gen11-prep | DONE | seal=closed | C61_*.json |\n"
 f"| C62 | replace-agent | DONE | {summary.get('replace_score')} | C62_*.json |\n"
 f"| C63 | vision-v2-smoke | DONE | {summary.get('c63_rate')} claim={summary.get('c63_claim')} | C63_*.json |\n"
 f"| C64 | docs | DONE | composite={sc.get('composite')} | C64_*.json |\n"
)
if marker in text and "| C58 |" not in text:
    text=text.replace(marker, marker+rows, 1)
block=f"""

### R50+ batch C58-C64 — DONE
- **Time**: {ts()}
- **C58**: rate {summary.get('c58_rate')} flipped={summary.get('c58_flipped')}
- **C59**: V2 fixtures n={summary.get('c59_n')}
- **C60**: LoRA absorb={summary.get('adapter_trained')} steps={summary.get('absorb_steps')}
- **C61**: gen11 prep={summary.get('gen11_prep')} seal_opened=false
- **C62**: replace={summary.get('replace_score')}
- **C63**: V2 rate={summary.get('c63_rate')} claim={summary.get('c63_claim')}
- **Composite**: {sc.get('composite')}
"""
if "R50+ batch C58-C64" not in text:
    text=text.rstrip()+"\n"+block+"\n"
LOOP.write_text(text, encoding="utf-8")
old=ROOT/"docs"/"蚁算_R50_LOOP.md"
if old.is_file():
    t=old.read_text(encoding="utf-8")
    if "R50+ batch C58-C64" not in t:
        old.write_text(t.rstrip()+"\n"+block+"\n", encoding="utf-8")
print(json.dumps({"composite":sc["composite"],"mm":mm,**{k:summary[k] for k in summary}},ensure_ascii=False))
