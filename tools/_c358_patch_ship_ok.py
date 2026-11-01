from pathlib import Path
p = Path("evo/office/vision_metric_parse.py")
t = p.read_text(encoding="utf-8")
old = 'elif metric == "ship_ok_qty":'
new = 'elif metric in ("ship_ok_qty", "ship_ok"):  # C358: V35+ fixtures use ship_ok'
if '("ship_ok_qty", "ship_ok")' in t:
    print("already patched")
elif old not in t:
    raise SystemExit("anchor missing")
else:
    t = t.replace(old, new, 1)
    p.write_text(t, encoding="utf-8")
    print("patched ship_ok alias")
from evo.office.vision_metric_parse import parse_metric
print("with_target", parse_metric("box1 38 ok box2 22 ok box3 27 hold ship_ok TARGET 79", "ship_ok", 79.0))
print("no_target", parse_metric("box1 38 ok box2 22 ok box3 27 hold", "ship_ok", 79.0))
print("garbage", parse_metric("SCAR DESK V41 BEST 133.00 PAGE 01 EXTRA EXTRA", "ship_ok", 79.0))
