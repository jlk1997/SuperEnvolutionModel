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

# *fen ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T272 = [
    ["ashfen","recv","paid_total","ASHFEN GRAIN RECV","RECV","x"],
    ["cedarfen","wh","qty_sum","WH CEDARFEN BIN","RECV","x"],
    ["dawnfen","refund","refund_done","DAWNFEN PATCH REFUND","DONE","x"],
    ["elmfen","tax","tax_base_paid","ELMFEN TAX SLIP","TAX","x"],
    ["fernfen","pay","payroll_active","FERNFEN PAYROLL","PAY","x"],
    ["glenfen","ship","ship_ok","GLENFEN SHIP DOCK","SHIP","x"],
    ["hazefen","sla","sla_ok_hours","HAZEFEN SLA CARD","SLA","x"],
    ["inkfen","exp","exp_sum","INKFEN EXPENSE","EXP","x"],
    ["jadefen","po","po_open","JADEFEN PO SHEET","PO","x"],
    ["knotfen","order","order_paid","KNOTFEN ORDER","ORD","x"],
    ["lakefen","dup","dup_mark","LAKEFEN DUP MARK","DUP","x"],
    ["mossfen","zero","zero_check","MOSSFEN AIR ZERO","ZERO","x"],
    ["netherfen","ledger","ledger_net","NETHERFEN LEDGER","LED","x"],
    ["oakfen","ui","ui_ok","OAKFEN UI SCAN","UI","x"],
    ["pinefen","stack","stack_count","PINEFEN STACK","STK","x"],
    ["quillfen","fax","fax_pages","QUILLFEN FAX","FAX","x"],
    ["reedfen","glare","glare_ok","REEDFEN GLARE","GLR","x"],
    ["stonefen","tab","tab_index","STONEFEN TAB INDEX","TAB","x"],
]
TR272 = [
    [2191.0, 2208.5, 1931.0],[840, 760, 820],[2114.0, 2143.25, 1909.0],[2247.0, 2264.0, 1999.0],
    [2309.0, 2333.0, 1969.0],[2027, 2043, 1927],[490.0, 530.0, 760.0],[2157.0, 2188.75, 1933.0],
    [780.0, 740.0, 820.0],[2224.0, 2212.0, 1930.0],[1,1,0],[0,0,0],
    [2290.0, 2311.5, 1955.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO272 = [
    [1989.0, 2001.75, 1850.0],[640, 660, 820],[1932.0, 1946.5, 1825.0],[2062.0, 2078.0, 1881.0],
    [2103.0, 2119.0, 1874.0],[1885, 1897, 1845],[370.0, 410.0, 740.0],[1973.0, 1994.75, 1850.0],
    [740.0, 780.0, 820.0],[2020.0, 2006.0, 1847.0],[1,1,0],[0,0,0],
    [2055.0, 2070.5, 1860.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR272, "TR"); check(HO272, "HO")

(ROOT / "tools/_v272_themes.json").write_text(json.dumps({"themes": T272, "train": TR272, "heldout": HO272}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_271(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V272 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V272 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 140.50", "ASHFEN bait 185.95"),
        ("CEDARW bait 142.52", "CEDARF bait 187.97"),
        ("DAWNW ghost 65.65", "DAWNF ghost 110.20"),
        ("GLENW bait 135.45", "GLENF bait 180.90"),
        ("JADEW bait 126.36", "JADEF bait 171.81"),
        ("NETHERW bait 143.53", "NETHERF bait 188.98"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V272-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD271 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v271_themes.json").read_text(encoding="utf-8"))["themes"])
NEW272 = "_".join(t[0] for t in T272)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1739"), ("c1463", "c1739"), ("V226", "V272"), ("v226", "v272"),
    ("_v226c1463", "_v272c1739"),
    ("Harder than V225", "Harder than V270"), ("harder than V225", "harder than V270"),
    (OLD271, NEW272),
    ("V226 keeps floor", "V272 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1739 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1740 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1740 VL"),
    ("kept on V226", "kept on V272"),
    ("vision_images_v226", "vision_images_v272"),
    ("VL_GATE_V226", "VL_GATE_V272"), ("vl_gate_v226", "vl_gate_v272"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V270: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T272, "v272", "V272", TR272))
out = retarget_271(out)
(S / "c1739_vision_v272_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1740"), ("c1464", "c1740"), ("V226", "V272"), ("v226", "v272"),
    ("vision_images_v226", "vision_images_v272"),
    ("VL_GATE_V226", "VL_GATE_V272"), ("vl_gate_v226", "vl_gate_v272"),
    ("runs/vision_v226", "runs/vision_v272"),
]:
    out = out.replace(a, b)
(S / "c1740_vision_v272_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1741"), ("c1465", "c1741"), ("V226", "V272"), ("v226", "v272"),
    ("vision_images_v226h", "vision_images_v272h"),
    ("vision_images_v226", "vision_images_v272"),
    ("VL_GATE_V226", "VL_GATE_V272"), ("vl_gate_v226", "vl_gate_v272"),
    ("runs/vision_v226h", "runs/vision_v272h"),
    ("_v226c1463", "_v272c1739"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T272, "v272h", "V272H", HO272))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v272h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v272"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v272" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v272h_c1741"'); seen_run = True; continue
    out2.append(ln)
(S / "c1741_vision_v272_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V272 knife = product-U2C (alternating; V271 was confidence-gate)
out = (S / "c1730_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1730", "C1742"), ("c1730", "c1742"),
    ("C1718", "C1742"), ("c1718", "c1742"),
    ("C1466", "C1742"), ("c1466", "c1742"),
]:
    out = out.replace(a, b2)
(S / "c1742_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1730_product_u2c_cost.py")

out = (S / "c1737_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1737", "C1743"), ("c1737", "c1743")]:
    out = out.replace(a, b2)
(S / "c1743_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1732_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1732", "C1744"), ("c1732", "c1744"),
    ("C1730", "C1742"), ("c1730", "c1742"),
    ("C1731", "C1743"), ("c1731", "c1743"),
    ("C1728", "C1740"), ("c1728", "c1740"),
    ("C1729", "C1741"), ("c1729", "c1741"),
    ("V270", "V272"), ("v270", "v272"),
    ("STAGE_ANT_C1732", "STAGE_ANT_C1744"),
    ("*wick", "*fen"),
]:
    out = out.replace(a, b2)
(S / "c1744_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1732_scorecard_and_stage.py")
print("OK builder v272 ready")
