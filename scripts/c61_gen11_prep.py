# -*- coding: utf-8 -*-
from __future__ import annotations
import json, shutil, sys, importlib
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
def ts(): return datetime.now().astimezone().isoformat(timespec="seconds")
def J(p,o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
src_h = ROOT/"scripts"/"heldout_gen11.py"
if src_h.is_file():
    shutil.copy(src_h, ROOT/"evo/office/heldout_gen11.py")
src_y = ROOT/"scripts"/"office_gate3_gen11.yaml"
if src_y.is_file():
    shutil.copy(src_y, ROOT/"configs/office_gate3_gen11.yaml")
snip_path = ROOT/"scripts"/"seal_gen11_snippet.py"
seal_path=ROOT/"evo/office/seal.py"
seal=seal_path.read_text(encoding="utf-8")
if "load_gen11_heldout" not in seal and snip_path.is_file():
    seal_path.write_text(seal + snip_path.read_text(encoding="utf-8"), encoding="utf-8")
run_path=ROOT/"evo/office/heldout_run.py"
run=run_path.read_text(encoding="utf-8")
if "load_gen11_heldout" not in run:
    if "load_gen10_heldout,\n)" in run:
        run=run.replace("load_gen10_heldout,\n)","load_gen10_heldout,\n    load_gen11_heldout,\n)")
    elif "load_gen10_heldout," in run:
        run=run.replace("load_gen10_heldout,","load_gen10_heldout,\n    load_gen11_heldout,",1)
    needle='if generation in ("gen10", "10", "observatory"):\n        default_seal = "runs/heldout_seal_gen10.json"'
    if "gen11" not in run and needle in run:
        run=run.replace(needle,'if generation in ("gen11", "11", "archives"):\n        default_seal = "runs/heldout_seal_gen11.json"\n    elif generation in ("gen10", "10", "observatory"):\n        default_seal = "runs/heldout_seal_gen10.json"')
    needle2='if generation in ("gen10", "10", "observatory"):\n        packs = load_gen10_heldout(open_flag, reason, record)'
    if "packs = load_gen11_heldout" not in run and needle2 in run:
        run=run.replace(needle2,'if generation in ("gen11", "11", "archives"):\n        packs = load_gen11_heldout(open_flag, reason, record)\n    elif generation in ("gen10", "10", "observatory"):\n        packs = load_gen10_heldout(open_flag, reason, record)')
    run_path.write_text(run, encoding="utf-8")
sealed_ok=False; err=None
try:
    import evo.office.seal as sealmod
    importlib.reload(sealmod)
    sealmod.load_gen11_heldout(False, "test")
except PermissionError as e:
    sealed_ok=True; err=str(e)
except Exception as e:
    err=f"{type(e).__name__}: {e}"
checklist={"rule_preregistered":True,"packs_code_present":(ROOT/"evo/office/heldout_gen11.py").is_file(),"seal_loader_present":"load_gen11_heldout" in seal_path.read_text(encoding="utf-8"),"config_present":(ROOT/"configs/office_gate3_gen11.yaml").is_file(),"open_heldout_false":True,"seal_file_absent":not (ROOT/"runs/heldout_seal_gen11.json").is_file(),"permission_error_when_closed":sealed_ok,"branch_target":"heritability","valuable_now":False,"valuable_reason":"Branch B needs fresh>=0.99; do not burn yet"}
ready=all(checklist[k] for k in ("rule_preregistered","packs_code_present","seal_loader_present","config_present","open_heldout_false","seal_file_absent","permission_error_when_closed"))
payload={"kind":"r50plus_c61_gen11_prep","timestamp":ts(),"seal_opened":False,"ready_to_open":False,"prep_complete":ready,"checklist":checklist,"closed_error_sample":err,"innovation":"Full gen11 wiring without burning seal","gate2_3_untouched":True,"note":"DO NOT open seal this cycle"}
J(ROOT/"docs/r50/C61_gen11_prep.json",payload)
J(ROOT/"docs/r50/C18_gen11_readiness.json",{"kind":"r50_c18","rule_preregistered":True,"seal_opened":False,"ready_to_open":False,"prep_complete":ready,"timestamp":ts(),"innovation":"Wiring complete; burn discipline held"})
print(json.dumps({"prep_complete":ready,"sealed_ok":sealed_ok,"err":err},ensure_ascii=False))
