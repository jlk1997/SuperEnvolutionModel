from pathlib import Path
p = Path('scripts/c352_vision_v41_design_and_batch.py')
t = p.read_text(encoding='utf-8')
t = t.replace('VL_GATE_V40_PROTOCOL.md', 'VL_GATE_V41_PROTOCOL.md')
p.write_text(t, encoding='utf-8')
# also fix design json protocol field if already written
dj = Path('docs/r50/C352_VISION_V41_DESIGN.json')
if dj.is_file():
    import json
    o = json.loads(dj.read_text(encoding='utf-8'))
    o['protocol'] = 'docs/蚁算_VL_GATE_V41_PROTOCOL.md'
    dj.write_text(json.dumps(o, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
# write protocol if missing
proto = Path('docs') / '蚁算_VL_GATE_V41_PROTOCOL.md'
if not proto.is_file() or 'V40' in proto.read_text(encoding='utf-8')[:200]:
    # re-run just the protocol write by importing main pieces - simpler: write manually
    from datetime import datetime
    ts = datetime.now().astimezone().isoformat(timespec='seconds')
    proto.write_text(f"""# Ant VL Gate V41 Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V40: basalt/velvet/bronze/silk/graphite/flint/pewter/gauze,
walnut/mica/slate/air/bamboo/lacquer/quartz/parchment/rivet/canvas.
Binder ring + stapler scatter overlays; clarity floor kept.

## Clarity floor (mandatory)
- jpeg quality >= **60** (V41 uses 60)
- photocopy downsample max **/2**
- Gaussian blur radius <= **0.5**
- Protect text band y=70..250
- TARGET / amount lines high-contrast bold

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke

## Honesty
- V40 train/heldout retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores in C352.
""", encoding='utf-8')
print('proto', proto.is_file(), proto.name)
print('script has V41_PROTOCOL', 'VL_GATE_V41_PROTOCOL.md' in p.read_text(encoding='utf-8'))
