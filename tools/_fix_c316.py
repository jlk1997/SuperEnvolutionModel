from pathlib import Path
p=Path('scripts/c316_vision_v35_heldout.py')
t=p.read_text(encoding='utf-8')
# fix leftover seeds / docstrings
fixes=[
    ('_v34hc316','_v35hc316'),
    ('Vision V33 heldout','Vision V35 heldout'),
    ('Disjoint heldout for V33 train (C303)','Disjoint heldout for V35 train (C314)'),
    ('V33 keeps floor','V35 keeps floor'),
]
for a,b in fixes:
    if a in t:
        t=t.replace(a,b)
        print('fixed', a, '->', b)
p.write_text(t, encoding='utf-8')
# verify SPECS lines parse
import re, sys
sys.path.insert(0,'.')
from evo.office.vision_metric_parse import parse_metric
# extract SPECS by exec partial - safer: run make after gen via importing after fixtures
# Quick: find line tuples with expected and last TARGET from SPECS block by reading make_fixture inputs
# Just compile-check
compile(t, str(p), 'exec')
print('compile ok')
# check SPECS have TARGET lines
for i,l in enumerate(t.splitlines(),1):
    if 'TARGET' in l and 'v35h' in t[max(0,t.find(l)-200):t.find(l)+50]:
        pass
print('SPECS count', t.count('v35h_'))
print('seed', '_v35hc316' in t, '_v34hc316' in t)
