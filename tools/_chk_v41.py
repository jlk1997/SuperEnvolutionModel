from pathlib import Path
import re
p=Path('scripts/c354_vision_v41_heldout.py')
t=p.read_text(encoding='utf-8')
for line in t.splitlines():
    if any(k in line for k in ['FIX =', 'TRAIN_FIX', 'PROTO =', 'RUN =', 'JPEG_Q', 'hash(', '"version"', 'cycle', 'C354', 'C352', 'vision_images', 'PROTOCOL']):
        print(line[:140])
ids=re.findall(r'\("(v41h?_\d+)"', t)
print('ids', ids[:3], ids[-2:], 'n', len(ids))
print('make_fixture', 'def make_fixture' in t)
print('leftover_v40', 'v40' in t.lower())
# check c352
p2=Path('scripts/c352_vision_v41_design_and_batch.py')
t2=p2.read_text(encoding='utf-8')
ids2=re.findall(r'\("(v41_\d+)"', t2)
print('c352 ids', ids2[:3], ids2[-2:], 'n', len(ids2))
print('c352 leftover_v40 paths', 'vision_images_v40' in t2)
print('c352 V41 overlay', 'V41 overlays' in t2)
print('c353 check:')
t3=Path('scripts/c353_vision_v41_smoke.py').read_text(encoding='utf-8')
print('  FIX', [l for l in t3.splitlines() if 'FIX =' in l or 'RUN =' in l or 'C353' in l][:6])
