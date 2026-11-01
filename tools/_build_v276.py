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

# *hurst ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T276 = [
    ["ashhurst","recv","paid_total","ASHHURST GRAIN RECV","RECV","x"],
    ["cedarhurst","wh","qty_sum","WH CEDARHURST BIN","RECV","x"],
    ["dawnhurst","refund","refund_done","DAWNHURST PATCH REFUND","DONE","x"],
    ["elmhurst","tax","tax_base_paid","ELMHURST TAX SLIP","TAX","x"],
    ["fernhurst","pay","payroll_active","FERNHURST PAYROLL","PAY","x"],
    ["glenhurst","ship","ship_ok","GLENHURST SHIP DOCK","SHIP","x"],
    ["hazehurst","sla","sla_ok_hours","HAZEHURST SLA CARD","SLA","x"],
    ["inkhurst","exp","exp_sum","INKHURST EXPENSE","EXP","x"],
    ["jadehurst","po","po_open","JADEHURST PO SHEET","PO","x"],
    ["knothurst","order","order_paid","KNOTHURST ORDER","ORD","x"],
    ["lakehurst","dup","dup_mark","LAKEHURST DUP MARK","DUP","x"],
    ["mosshurst","zero","zero_check","MOSSHURST AIR ZERO","ZERO","x"],
    ["netherhurst","ledger","ledger_net","NETHERHURST LEDGER","LED","x"],
    ["oakhurst","ui","ui_ok","OAKHURST UI SCAN","UI","x"],
    ["pinehurst","stack","stack_count","PINEHURST STACK","STK","x"],
    ["quillhurst","fax","fax_pages","QUILLHURST FAX","FAX","x"],
    ["reedhurst","glare","glare_ok","REEDHURST GLARE","GLR","x"],
    ["stonehurst","tab","tab_index","STONEHURST TAB INDEX","TAB","x"],
]
TR276 = [
    [2203.0, 2220.5, 1943.0],[840, 760, 820],[2126.0, 2155.25, 1921.0],[2259.0, 2276.0, 2011.0],
    [2321.0, 2345.0, 1981.0],[2039, 2055, 1939],[530.0, 570.0, 760.0],[2169.0, 2200.75, 1945.0],
    [840.0, 760.0, 820.0],[2236.0, 2224.0, 1942.0],[1,1,0],[0,0,0],
    [2302.0, 2323.5, 1967.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO276 = [
    [2001.0, 2013.75, 1862.0],[640, 660, 820],[1944.0, 1958.5, 1837.0],[2074.0, 2090.0, 1893.0],
    [2115.0, 2131.0, 1886.0],[1897, 1909, 1857],[410.0, 450.0, 740.0],[1985.0, 2006.75, 1862.0],
    [740.0, 780.0, 820.0],[2032.0, 2018.0, 1859.0],[1,1,0],[0,0,0],
    [2067.0, 2082.5, 1872.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR276, "TR"); check(HO276, "HO")

(ROOT / "tools/_v276_themes.json").write_text(json.dumps({"themes": T276, "train": TR276, "heldout": HO276}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_275(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V276 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V276 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 140.50", "ASHHURST bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 191.01"),
        ("DAWNW ghost 65.65", "DAWNH ghost 114.24"),
        ("GLENW bait 135.45", "GLENH bait 184.94"),
        ("JADEW bait 126.36", "JADEH bait 175.85"),
        ("NETHERW bait 143.53", "NETHERH bait 192.02"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V276-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD275 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v275_themes.json").read_text(encoding="utf-8"))["themes"])
NEW276 = "_".join(t[0] for t in T276)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1763"), ("c1463", "c1763"), ("V226", "V276"), ("v226", "v276"),
    ("_v226c1463", "_v276c1763"),
    ("Harder than V225", "Harder than V274"), ("harder than V225", "harder than V274"),
    (OLD275, NEW276),
    ("V226 keeps floor", "V276 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1763 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1764 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1764 VL"),
    ("kept on V226", "kept on V276"),
    ("vision_images_v226", "vision_images_v276"),
    ("VL_GATE_V226", "VL_GATE_V276"), ("vl_gate_v226", "vl_gate_v276"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V274: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T276, "v276", "V276", TR276))
out = retarget_275(out)
(S / "c1763_vision_v276_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1764"), ("c1464", "c1764"), ("V226", "V276"), ("v226", "v276"),
    ("vision_images_v226", "vision_images_v276"),
    ("VL_GATE_V226", "VL_GATE_V276"), ("vl_gate_v226", "vl_gate_v276"),
    ("runs/vision_v226", "runs/vision_v276"),
]:
    out = out.replace(a, b)
(S / "c1764_vision_v276_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1765"), ("c1465", "c1765"), ("V226", "V276"), ("v226", "v276"),
    ("vision_images_v226h", "vision_images_v276h"),
    ("vision_images_v226", "vision_images_v276"),
    ("VL_GATE_V226", "VL_GATE_V276"), ("vl_gate_v226", "vl_gate_v276"),
    ("runs/vision_v226h", "runs/vision_v276h"),
    ("_v226c1463", "_v276c1763"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T276, "v276h", "V276H", HO276))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v276h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v276"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v276" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v276h_c1765"'); seen_run = True; continue
    out2.append(ln)
(S / "c1765_vision_v276_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V276 knife = product-U2C (alternating; V275 was confidence-gate)
out = (S / "c1754_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1754", "C1766"), ("c1754", "c1766"),
    ("C1742", "C1766"), ("c1742", "c1766"),
    ("C1466", "C1766"), ("c1466", "c1766"),
]:
    out = out.replace(a, b2)
(S / "c1766_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1754_product_u2c_cost.py")

out = (S / "c1761_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1761", "C1767"), ("c1761", "c1767")]:
    out = out.replace(a, b2)
(S / "c1767_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1756_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1756", "C1768"), ("c1756", "c1768"),
    ("C1754", "C1766"), ("c1754", "c1766"),
    ("C1755", "C1767"), ("c1755", "c1767"),
    ("C1752", "C1764"), ("c1752", "c1764"),
    ("C1753", "C1765"), ("c1753", "c1765"),
    ("V274", "V276"), ("v274", "v276"),
    ("STAGE_ANT_C1756", "STAGE_ANT_C1768"),
    ("*dale", "*hurst"),
]:
    out = out.replace(a, b2)
(S / "c1768_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1756_scorecard_and_stage.py")
print("OK builder v276 ready")
