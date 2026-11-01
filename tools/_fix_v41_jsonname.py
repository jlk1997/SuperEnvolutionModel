from pathlib import Path
import json, shutil
# fix script output filename
p = Path('scripts/c352_vision_v41_design_and_batch.py')
t = p.read_text(encoding='utf-8')
t = t.replace('C352_VISION_V40_DESIGN.json', 'C352_VISION_V41_DESIGN.json')
t = t.replace('C346_VISION_V40_DESIGN.json', 'C352_VISION_V41_DESIGN.json')
p.write_text(t, encoding='utf-8')
# rename existing json
old = Path('docs/r50/C352_VISION_V40_DESIGN.json')
new = Path('docs/r50/C352_VISION_V41_DESIGN.json')
if old.is_file():
    o = json.loads(old.read_text(encoding='utf-8'))
    o['protocol'] = 'docs/蚁算_VL_GATE_V41_PROTOCOL.md'
    new.write_text(json.dumps(o, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    old.unlink()
    print('renamed design json')
# fix judge if any
rj = Path('runs/vision_v41_c352/judge.json')
if rj.is_file():
    o = json.loads(rj.read_text(encoding='utf-8'))
    o['protocol'] = 'docs/蚁算_VL_GATE_V41_PROTOCOL.md'
    rj.write_text(json.dumps(o, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('ok', new.is_file(), 'V40_DESIGN' not in p.read_text(encoding='utf-8'))
