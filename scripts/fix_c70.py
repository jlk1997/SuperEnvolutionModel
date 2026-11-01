
from pathlib import Path
root = Path(r'E:\envolution')
fp = root / 'scripts' / 'c70_vision_v2h_style_train_fixtures.py'
t = fp.read_text(encoding='utf-8')
old = 'fill=(0, 0), font=font(20))'
new = 'fill=(0, 0, 0), font=font(20))'
if old in t:
    fp.write_text(t.replace(old, new), encoding='utf-8')
    print('fixed')
else:
    print('no_bad_fill', 'Customer' in t)
