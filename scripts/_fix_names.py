from pathlib import Path
fixes = {
    'scripts/c371_vision_v44_design_and_batch.py': [
        ('C371_VISION_V43_DESIGN.json', 'C371_VISION_V44_DESIGN.json'),
    ],
    'scripts/c372_vision_v44_smoke.py': [
        ('C372_VISION_V43_SMOKE.json', 'C372_VISION_V44_SMOKE.json'),
        ('C372b_VISION_GATE_V43_CLAIM.json', 'C372b_VISION_GATE_V44_CLAIM.json'),
    ],
    'scripts/c373_vision_v44_heldout.py': [
        ('C373_VISION_V43_HELDOUT_SMOKE.json', 'C373_VISION_V44_HELDOUT_SMOKE.json'),
        ('C373b_VISION_GATE_V43_HELDOUT_CLAIM.json', 'C373b_VISION_GATE_V44_HELDOUT_CLAIM.json'),
        ('Disjoint heldout for V42 train (C365).', 'Disjoint heldout for V44 train (C371).'),
    ],
}
for f, pairs in fixes.items():
    p = Path(f)
    t = p.read_text(encoding='utf-8')
    for a,b in pairs:
        c = t.count(a)
        t = t.replace(a,b)
        print(f, a, '->', b, 'count', c)
    p.write_text(t, encoding='utf-8')

# Fix scorecard tip slice text to C371-C376 / V44
p = Path('scripts/c376_scorecard_and_stage.py')
t = p.read_text(encoding='utf-8')
# show STAGE template section
idx = t.find('## Tip slice')
print('--- stage template snippet ---')
print(t[idx:idx+900] if idx>=0 else 'NO TIP')
