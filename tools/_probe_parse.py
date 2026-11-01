import json, sys
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
from evo.office.vision_metric_parse import parse_metric
m=json.loads(Path('evo/office/fixtures/vision_images_v35/manifest.json').read_text(encoding='utf-8'))
bad=[]
for it in m['items']:
    lines='\n'.join(it['lines'])
    got, ok = parse_metric(lines, it['metric'], it['expected'])
    status='OK' if ok else 'FAIL'
    print(status, it['id'], it['metric'], 'exp', it['expected'], 'got', got, '|', it['lines'][-1])
    if not ok: bad.append(it['id'])
print('bad', bad)
# also check C316 SPECS lines by reading source tuples - dry from heldout SPECS embedded
import ast, re
src=Path('scripts/c316_vision_v35_heldout.py').read_text(encoding='utf-8')
# find SPECS = [ ... ]
