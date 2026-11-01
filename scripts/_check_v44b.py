from pathlib import Path
for f, needles in [
    ('scripts/c371_vision_v44_design_and_batch.py', ['VISION_V43','v43']),
    ('scripts/c372_vision_v44_smoke.py', ['VISION_V43']),
    ('scripts/c373_vision_v44_heldout.py', ['C365','VISION_V43','v43']),
    ('scripts/c376_scorecard_and_stage.py', ['C365','C366_','C367_','VISION_V43','v43_claim','v44 ']),
]:
    lines=Path(f).read_text(encoding='utf-8').splitlines()
    print('====', f)
    for i,l in enumerate(lines,1):
        if any(n in l for n in needles):
            if 'harder' in l or 'V43' in l or 'C365' in l or 'C366_' in l or 'C367_' in l or 'VISION_V43' in l or 'vision_images_v43' in l or 'v43_claim' in l:
                print(f'{i}: {l[:140]}')
