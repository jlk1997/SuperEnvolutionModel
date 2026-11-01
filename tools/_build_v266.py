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

# *mere ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T266 = [
    ["ashmere","recv","paid_total","ASHMERE GRAIN RECV","RECV","x"],
    ["cedarmere","wh","qty_sum","WH CEDARMERE BIN","RECV","x"],
    ["dawnmere","refund","refund_done","DAWNMERE PATCH REFUND","DONE","x"],
    ["elmmere","tax","tax_base_paid","ELMMERE TAX SLIP","TAX","x"],
    ["fernmere","pay","payroll_active","FERNMERE PAYROLL","PAY","x"],
    ["glenmere","ship","ship_ok","GLENMERE SHIP DOCK","SHIP","x"],
    ["hazemere","sla","sla_ok_hours","HAZEMERE SLA CARD","SLA","x"],
    ["inkmere","exp","exp_sum","INKMERE EXPENSE","EXP","x"],
    ["jademere","po","po_open","JADEMERE PO SHEET","PO","x"],
    ["knotmere","order","order_paid","KNOTMERE ORDER","ORD","x"],
    ["lakemere","dup","dup_mark","LAKEMERE DUP MARK","DUP","x"],
    ["mossmere","zero","zero_check","MOSSMERE AIR ZERO","ZERO","x"],
    ["nethermere","ledger","ledger_net","NETHERMERE LEDGER","LED","x"],
    ["oakmere","ui","ui_ok","OAKMERE UI SCAN","UI","x"],
    ["pinemere","stack","stack_count","PINEMERE STACK","STK","x"],
    ["quillmere","fax","fax_pages","QUILLMERE FAX","FAX","x"],
    ["reedmere","glare","glare_ok","REEDMERE GLARE","GLR","x"],
    ["stonemere","tab","tab_index","STONEMERE TAB INDEX","TAB","x"],
]
TR266 = [
    [2178.0, 2195.5, 1918.0],[840, 760, 820],[2101.0, 2130.25, 1896.0],[2234.0, 2251.0, 1986.0],
    [2296.0, 2320.0, 1956.0],[2014, 2030, 1914],[480.0, 520.0, 740.0],[2144.0, 2175.75, 1920.0],
    [840.0, 760.0, 820.0],[2211.0, 2199.0, 1917.0],[1,1,0],[0,0,0],
    [2277.0, 2298.5, 1942.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO266 = [
    [1976.0, 1988.75, 1837.0],[740, 780, 820],[1919.0, 1933.5, 1812.0],[2049.0, 2065.0, 1868.0],
    [2090.0, 2106.0, 1861.0],[1872, 1884, 1832],[360.0, 400.0, 730.0],[1960.0, 1981.75, 1837.0],
    [780.0, 740.0, 820.0],[2007.0, 1993.0, 1834.0],[1,1,0],[0,0,0],
    [2042.0, 2057.5, 1847.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR266, "TR"); check(HO266, "HO")

(ROOT / "tools/_v266_themes.json").write_text(json.dumps({"themes": T266, "train": TR266, "heldout": HO266}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_265(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V266 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V266 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 140.50", "ASHMERE bait 179.89"),
        ("CEDARW bait 142.52", "CEDARM bait 181.91"),
        ("DAWNW ghost 65.65", "DAWNM ghost 104.14"),
        ("GLENW bait 135.45", "GLENM bait 174.84"),
        ("JADEW bait 126.36", "JADEM bait 165.75"),
        ("NETHERW bait 143.53", "NETHERM bait 182.92"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V266-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD265 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v265_themes.json").read_text(encoding="utf-8"))["themes"])
NEW266 = "_".join(t[0] for t in T266)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1703"), ("c1463", "c1703"), ("V226", "V266"), ("v226", "v266"),
    ("_v226c1463", "_v266c1703"),
    ("Harder than V225", "Harder than V264"), ("harder than V225", "harder than V264"),
    (OLD265, NEW266),
    ("V226 keeps floor", "V266 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1703 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1704 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1704 VL"),
    ("kept on V226", "kept on V266"),
    ("vision_images_v226", "vision_images_v266"),
    ("VL_GATE_V226", "VL_GATE_V266"), ("vl_gate_v226", "vl_gate_v266"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V264: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T266, "v266", "V266", TR266))
out = retarget_265(out)
(S / "c1703_vision_v266_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1704"), ("c1464", "c1704"), ("V226", "V266"), ("v226", "v266"),
    ("vision_images_v226", "vision_images_v266"),
    ("VL_GATE_V226", "VL_GATE_V266"), ("vl_gate_v226", "vl_gate_v266"),
    ("runs/vision_v226", "runs/vision_v266"),
]:
    out = out.replace(a, b)
(S / "c1704_vision_v266_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1705"), ("c1465", "c1705"), ("V226", "V266"), ("v226", "v266"),
    ("vision_images_v226h", "vision_images_v266h"),
    ("vision_images_v226", "vision_images_v266"),
    ("VL_GATE_V226", "VL_GATE_V266"), ("vl_gate_v226", "vl_gate_v266"),
    ("runs/vision_v226h", "runs/vision_v266h"),
    ("_v226c1463", "_v266c1703"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T266, "v266h", "V266H", HO266))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v266h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v266"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v266" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v266h_c1705"'); seen_run = True; continue
    out2.append(ln)
(S / "c1705_vision_v266_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

# V266 knife = product-U2C (alternating; V265 was confidence-gate)
out = (S / "c1694_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1694", "C1706"), ("c1694", "c1706"),
    ("C1682", "C1706"), ("c1682", "c1706"),
    ("C1466", "C1706"), ("c1466", "c1706"),
]:
    out = out.replace(a, b2)
(S / "c1706_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from", "c1694_product_u2c_cost.py")

out = (S / "c1701_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1701", "C1707"), ("c1701", "c1707")]:
    out = out.replace(a, b2)
(S / "c1707_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

out = (S / "c1696_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1696", "C1708"), ("c1696", "c1708"),
    ("C1694", "C1706"), ("c1694", "c1706"),
    ("C1695", "C1707"), ("c1695", "c1707"),
    ("C1692", "C1704"), ("c1692", "c1704"),
    ("C1693", "C1705"), ("c1693", "c1705"),
    ("V264", "V266"), ("v264", "v266"),
    ("STAGE_ANT_C1696", "STAGE_ANT_C1708"),
    ("*ford", "*mere"),
]:
    out = out.replace(a, b2)
(S / "c1708_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("scorecard from", "c1696_scorecard_and_stage.py")
print("OK builder v266 ready")
