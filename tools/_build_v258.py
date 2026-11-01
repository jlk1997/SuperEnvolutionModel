# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"
BAN = {755, 756, 770, 750, 830, 1830, 1560}

def lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag):
    if metric == "paid_total":
        expected, body = a + b, [f"a paid {a:.2f}", f"b paid {b:.2f}", f"c open {c:.2f}", f"TOTAL PAID TARGET {a+b:.2f}"]
    elif metric == "qty_sum":
        expected = float(a + b); body = [f"SKU1 qty {a} ok", f"SKU2 qty {c} hold", f"SKU3 qty {b} ok", f"qty_sum TARGET {a+b}"]
    elif metric == "refund_done":
        expected, body = a + b, [f"itemR1 {a:.2f} done", f"itemR2 {b:.2f} done", f"itemR3 {c:.2f} open", f"refund_done TARGET {a+b:.2f}"]
    elif metric == "tax_base_paid":
        expected, body = a + b, [f"base {a:.2f} paid", f"addon {b:.2f} paid", f"skip {c:.2f}", f"tax_base_paid TARGET {a+b:.2f}"]
    elif metric == "payroll_active":
        expected, body = a + b, [f"empA {a:.2f} active", f"empB {b:.2f} active", f"empC {c:.2f} leave", f"payroll_active TARGET {a+b:.2f}"]
    elif metric == "ship_ok":
        expected = float(a + b); body = [f"box1 {a} ok", f"box2 {b} ok", f"box3 {c} hold", f"ship_ok TARGET {a+b}"]
    elif metric == "sla_ok_hours":
        expected, body = a + b, [f"job1 {a:.2f} hours ok", f"job2 {b:.2f} hours ok", f"job3 {c:.2f} hours late", f"sla_ok_hours TARGET {a+b:.2f}"]
    elif metric == "exp_sum":
        expected, body = a + b, [f"e1 {a:.2f}", f"e2 {b:.2f}", f"e3 {c:.2f} void", f"exp_sum TARGET {a+b:.2f}"]
    elif metric == "po_open":
        expected, body = a + b, [f"line1 {a:.2f} open", f"line2 {b:.2f} open", f"line3 {c:.2f} closed", f"po_open TARGET {a+b:.2f}"]
    elif metric == "order_paid":
        expected, body = a + b, [f"skuA {a:.2f} paid", f"skuB {b:.2f} paid", f"skuC {c:.2f} due", f"order_paid TARGET {a+b:.2f}"]
    elif metric == "dup_mark":
        expected, body = 2.0, ["markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"]
    elif metric == "zero_check":
        expected, body = 0.0, ["z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"]
    elif metric == "ledger_net":
        expected, body = a + b, [f"dr {a:.2f}", f"cr {b:.2f}", f"adj {c:.2f}", f"ledger_net TARGET {a+b:.2f}"]
    elif metric == "ui_ok":
        expected, body = 1.0, ["btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"]
    elif metric == "stack_count":
        expected = float(a + b); body = [f"p1 {a}", f"p2 {b}", f"p3 {c}", f"stack_count TARGET {a+b}"]
    elif metric == "fax_pages":
        expected = float(a + b); body = [f"pgA {a}", f"pgB {b}", f"pgC {c} drop", f"fax_pages TARGET {a+b}"]
    elif metric == "glare_ok":
        expected, body = 1.0, ["zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"]
    elif metric == "tab_index":
        expected = float(a + b); body = [f"tabA {a}", f"tabB {b}", f"tabC {c}", f"tab_index TARGET {a+b}"]
    else:
        raise ValueError(metric)
    return expected, [f"{title} {tag}"] + body

def build_specs(themes, prefix, tag, abcs):
    lines = ["SPECS = ["]
    for i, (t, abc) in enumerate(zip(themes, abcs), 1):
        name, kind_suf, metric, title, stamp, _bk = t
        a, b, c = abc
        expected, body = lines_for_metric(name, kind_suf, metric, title, stamp, a, b, c, tag)
        fid = f"{prefix}_{i:02d}"; kind = f"{name}_{kind_suf}"
        body_l = ",\n     ".join(repr(x) for x in body)
        lines.append(f'    ("{fid}", "{kind}", "{metric}", {repr(float(expected))},\n     [{body_l}],\n     {repr(name)}, "{stamp}"),')
    lines.append("]")
    return "\n".join(lines) + "\n"

def replace_specs(src, new_specs):
    return re.sub(r"SPECS = \[.*?\n\]\n", new_specs + "\n", src, count=1, flags=re.S)

def check(rows, label):
    for i, row in enumerate(rows):
        for v in row:
            if isinstance(v, (int, float)) and int(v) in BAN:
                raise SystemExit(f"banned {v} in {label}[{i}]={row}")

# *holm ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T258 = [
    ["ashholm","recv","paid_total","ASHHOLM GRAIN RECV","RECV","x"],
    ["cedarholm","wh","qty_sum","WH CEDARHOLM BIN","RECV","x"],
    ["dawnholm","refund","refund_done","DAWNHOLM PATCH REFUND","DONE","x"],
    ["elmholm","tax","tax_base_paid","ELMHOLM TAX SLIP","TAX","x"],
    ["fernholm","pay","payroll_active","FERNHOLM PAYROLL","PAY","x"],
    ["glenholm","ship","ship_ok","GLENHOLM SHIP DOCK","SHIP","x"],
    ["hazeholm","sla","sla_ok_hours","HAZEHOLM SLA CARD","SLA","x"],
    ["inkholm","exp","exp_sum","INKHOLM EXPENSE","EXP","x"],
    ["jadeholm","po","po_open","JADEHOLM PO SHEET","PO","x"],
    ["knotholm","order","order_paid","KNOTHOLM ORDER","ORD","x"],
    ["lakeholm","dup","dup_mark","LAKEHOLM DUP MARK","DUP","x"],
    ["mossholm","zero","zero_check","MOSSHOLM AIR ZERO","ZERO","x"],
    ["netherholm","ledger","ledger_net","NETHERHOLM LEDGER","LED","x"],
    ["oakholm","ui","ui_ok","OAKHOLM UI SCAN","UI","x"],
    ["pineholm","stack","stack_count","PINEHOLM STACK","STK","x"],
    ["quillholm","fax","fax_pages","QUILLHOLM FAX","FAX","x"],
    ["reedholm","glare","glare_ok","REEDHOLM GLARE","GLR","x"],
    ["stoneholm","tab","tab_index","STONEHOLM TAB INDEX","TAB","x"],
]
TR258 = [
    [2162.0, 2179.5, 1902.0],[840, 760, 820],[2085.0, 2114.25, 1880.0],[2218.0, 2235.0, 1970.0],
    [2280.0, 2304.0, 1940.0],[1998, 2014, 1898],[480.0, 520.0, 740.0],[2128.0, 2159.75, 1904.0],
    [840.0, 760.0, 820.0],[2195.0, 2183.0, 1901.0],[1,1,0],[0,0,0],
    [2261.0, 2282.5, 1926.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO258 = [
    [1960.0, 1972.75, 1821.0],[740, 780, 820],[1903.0, 1917.5, 1796.0],[2033.0, 2049.0, 1852.0],
    [2074.0, 2090.0, 1845.0],[1856, 1868, 1814],[360.0, 400.0, 730.0],[1944.0, 1965.75, 1821.0],
    [780.0, 740.0, 820.0],[1991.0, 1977.0, 1816.0],[1,1,0],[0,0,0],
    [2026.0, 2041.5, 1831.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR258, "TR"); check(HO258, "HO")

(ROOT / "tools/_v258_themes.json").write_text(json.dumps({"themes": T258, "train": TR258, "heldout": HO258}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_257(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V258 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V258 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 140.50", "ASHHOLM bait 171.81"),
        ("CEDARW bait 142.52", "CEDARH bait 173.83"),
        ("DAWNW ghost 65.65", "DAWNH ghost 96.96"),
        ("GLENW bait 135.45", "GLENH bait 166.76"),
        ("JADEW bait 126.36", "JADEH bait 157.67"),
        ("NETHERW bait 143.53", "NETHERH bait 174.84"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V258-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD257 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v257_themes.json").read_text(encoding="utf-8"))["themes"])
NEW258 = "_".join(t[0] for t in T258)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1655"), ("c1463", "c1655"), ("V226", "V258"), ("v226", "v258"),
    ("_v226c1463", "_v258c1655"),
    ("Harder than V225", "Harder than V256"), ("harder than V225", "harder than V256"),
    (OLD257, NEW258),
    ("V226 keeps floor", "V258 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1655 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1656 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1656 VL"),
    ("kept on V226", "kept on V258"),
    ("vision_images_v226", "vision_images_v258"),
    ("VL_GATE_V226", "VL_GATE_V258"), ("vl_gate_v226", "vl_gate_v258"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V256: ashholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T258, "v258", "V258", TR258))
out = retarget_257(out)
(S / "c1655_vision_v258_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1656"), ("c1464", "c1656"), ("V226", "V258"), ("v226", "v258"),
    ("vision_images_v226", "vision_images_v258"),
    ("VL_GATE_V226", "VL_GATE_V258"), ("vl_gate_v226", "vl_gate_v258"),
    ("runs/vision_v226", "runs/vision_v258"),
]:
    out = out.replace(a, b)
(S / "c1656_vision_v258_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1657"), ("c1465", "c1657"), ("V226", "V258"), ("v226", "v258"),
    ("vision_images_v226h", "vision_images_v258h"),
    ("vision_images_v226", "vision_images_v258"),
    ("VL_GATE_V226", "VL_GATE_V258"), ("vl_gate_v226", "vl_gate_v258"),
    ("runs/vision_v226h", "runs/vision_v258h"),
    ("_v226c1463", "_v258c1655"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T258, "v258h", "V258H", HO258))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v258h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v258"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v258" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v258h_c1657"'); seen_run = True; continue
    out2.append(ln)
(S / "c1657_vision_v258_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V258 knife = product-U2C (alternating; V257 was confidence-gate)
out = (S / "c1646_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1646", "C1658"), ("c1646", "c1658"),
    ("C1634", "C1658"), ("c1634", "c1658"),
    ("C1466", "C1658"), ("c1466", "c1658"),
]:
    out = out.replace(a, b2)
(S / "c1658_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1646_product_u2c_cost.py")

out = (S / "c1653_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1653", "C1659"), ("c1653", "c1659")]:
    out = out.replace(a, b2)
(S / "c1659_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1648_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1648", "C1660"), ("c1648", "c1660"),
    ("C1646", "C1658"), ("c1646", "c1658"),
    ("C1647", "C1659"), ("c1647", "c1659"),
    ("C1644", "C1656"), ("c1644", "c1656"),
    ("C1645", "C1657"), ("c1645", "c1657"),
    ("V256", "V258"), ("v256", "v258"),
    ("STAGE_ANT_C1648", "STAGE_ANT_C1660"),
    ("*vale", "*holm"),
]:
    out = out.replace(a, b2)
(S / "c1660_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1648_scorecard_and_stage.py")
print("OK builder v258 ready")
