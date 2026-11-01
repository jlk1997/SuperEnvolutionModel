from pathlib import Path
import re
for f in ['c371_vision_v44_design_and_batch.py','c372_vision_v44_smoke.py','c373_vision_v44_heldout.py','c374_product_u2c_cost.py','c375_capture_office_regression.py','c376_scorecard_and_stage.py']:
    t=Path('scripts/'+f).read_text(encoding='utf-8')
    bad=[s for s in ['vision_images_v43','C365','C366_','C367_','C368_','C369_','C370_','vl_gate_v43','VISION_V43'] if s in t]
    print(f, 'leftover', bad)
t=Path('scripts/c371_vision_v44_design_and_batch.py').read_text(encoding='utf-8')
print('train ids', re.findall(r'"(v44_\d+)"', t))
print('overlay', '# --- V44 overlays' in t)
print('FIX', 'vision_images_v44' in t)
t=Path('scripts/c373_vision_v44_heldout.py').read_text(encoding='utf-8')
print('held ids', re.findall(r'"(v44h_\d+)"', t))
print('held FIX', 'vision_images_v44h' in t)
# scorecard key vars
t=Path('scripts/c376_scorecard_and_stage.py').read_text(encoding='utf-8')
for needle in ['v44 =', 'v44h =', 'v43 =', 'c372 =', 'STAGE_ANT_C376', 'C372_VISION']:
    print(needle, needle in t)
