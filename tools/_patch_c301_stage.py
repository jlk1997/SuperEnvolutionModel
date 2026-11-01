from pathlib import Path
p = Path("scripts/c301_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")
old_stage = """**C290-C301 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C290 | V31 design | n={c266.get('n')} graphite/emboss/carbon/binder/... |
| C291 | V31 smoke | rate={v31} claim={v31_claim} |
| C292 | V31 heldout | rate={v31h} claim={v31h_claim} |
| C293 | dissolve/shadow refresh | pass={nv_pass} |
| C294 | capture regression | pass={capture_pass} |
| C301 | scorecard | composite={composite} |"""
new_stage = """**C296-C301 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C296 | V32 design | n={c266.get('n')} kraft/linen/thermal/dossier/... |
| C297 | V32 smoke | rate={v32} claim={v32_claim} |
| C298 | V32 heldout | rate={v32h} claim={v32h_claim} |
| C299 | product/U2C/cost | pass={nv_pass} replace={replace.get('mean_ratio')} |
| C300 | capture regression | pass={capture_pass} |
| C301 | scorecard | composite={composite} |"""
if old_stage not in t:
    raise SystemExit("old_stage block not found")
t = t.replace(old_stage, new_stage, 1)
t = t.replace(
    "Stage: C290-C301; V31 CLAIM {v31}; V31 heldout CLAIM {v31h}; nv pass={nv_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}",
    "Stage: C296-C301; V32 CLAIM {v32}; V32 heldout CLAIM {v32h}; nv pass={nv_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}",
    1,
)
t = t.replace("## C272-C301 ({ts()})", "## C296-C301 ({ts()})", 1)
# also fix any leftover C290-C301 banner in scorecard json theme is fine
p.write_text(t, encoding="utf-8")
print("patched ok")
