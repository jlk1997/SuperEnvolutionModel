# -*- coding: utf-8 -*-
from pathlib import Path
p = Path("scripts/c295_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")
old_batch = """| C284 | V30 design | n={c266.get('n')} velvet/spiral/mimeo/ribbon/neon/... |
| C285 | V30 smoke | rate={v30} claim={v30_claim} |
| C286 | V30 heldout | rate={v30h} claim={v30h_claim} |
| C287 | confidence-gate stretch | pass={conf_pass} rate={conf_rate} |
| C288 | capture regression | pass={capture_pass} |
| C295 | scorecard | composite={composite} |"""
new_batch = """| C290 | V31 design | n={c266.get('n')} graphite/emboss/carbon/binder/... |
| C291 | V31 smoke | rate={v31} claim={v31_claim} |
| C292 | V31 heldout | rate={v31h} claim={v31h_claim} |
| C293 | dissolve/shadow refresh | pass={nv_pass} |
| C294 | capture regression | pass={capture_pass} |
| C295 | scorecard | composite={composite} |"""
assert old_batch in t, "batch block missing"
t = t.replace(old_batch, new_batch)
t = t.replace("**C284-C295 STAGE_READY=", "**C290-C295 STAGE_READY=")
t = t.replace(
    "Stage: C284-C295; V30 CLAIM {v30}; V30 heldout CLAIM {v30h};",
    "Stage: C290-C295; V31 CLAIM {v31}; V31 heldout CLAIM {v31h};",
)
needle = """    replace = {
        \"mean_ratio\": (rl.get(\"mean_ratio\")
                       or (c263.get(\"replace_stress\") or {}).get(\"mean_ratio\")
                       or (c263.get(\"cost_ledger\") or {}).get(\"replace_mean_ratio\") or 3.9188),"""
new_rep = """    replace = {
        \"mean_ratio\": ((c269.get(\"replace_stress\") or {}).get(\"mean_ratio\")
                       or rl.get(\"mean_ratio\")
                       or (c263.get(\"replace_stress\") or {}).get(\"mean_ratio\")
                       or (c263.get(\"cost_ledger\") or {}).get(\"replace_mean_ratio\") or 3.9188),"""
if needle in t:
    t = t.replace(needle, new_rep)
t = t.replace(
    '"source": "C281" if (c281.get("replace_ledger") or {}).get("mean_ratio") is not None else ("C293" if rl.get("mean_ratio") is not None else "C263")',
    '"source": "C293" if (c269.get("replace_stress") or {}).get("mean_ratio") is not None else ("C281" if (c281.get("replace_ledger") or {}).get("mean_ratio") is not None else "C263")',
)
p.write_text(t, encoding="utf-8")
print("patched")
