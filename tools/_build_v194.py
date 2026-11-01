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

# *fen ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T194 = [
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
TR194 = [
    [1339.0, 1356.5, 1149.0],[740, 780, 820],[1262.0, 1291.25, 1129.0],[1395.0, 1412.0, 1219.0],
    [1457.0, 1481.0, 1189.0],[1215, 1231, 1147],[480.0, 520.0, 740.0],[1305.0, 1336.75, 1153.0],
    [780.0, 740.0, 820.0],[1372.0, 1360.0, 1150.0],[1,1,0],[0,0,0],
    [1438.0, 1459.5, 1175.0],[1,0,0],[987, 979, 957],[1005, 989, 748],[1,0,0],[1031, 1007, 977],
]
HO194 = [
    [1209.0, 1221.75, 1102.0],[840, 760, 820],[1167.0, 1180.5, 1090.0],[1282.0, 1298.0, 1131.0],
    [1323.0, 1339.0, 1126.0],[1117, 1131, 1095],[360.0, 400.0, 680.0],[1193.0, 1214.75, 1102.0],
    [840.0, 760.0, 820.0],[1240.0, 1226.0, 1097.0],[1,1,0],[0,0,0],
    [1275.0, 1290.5, 1112.0],[1,0,0],[964, 959, 954],[979, 973, 961],[1,0,0],[989, 983, 962],
]
check(TR194, "TR"); check(HO194, "HO")

(ROOT / "tools/_v194_themes.json").write_text(json.dumps({"themes": T194, "train": TR194, "heldout": HO194}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_194(src):
    src = src.replace("# --- V193 overlays (new vs V50) ---", "# --- V194 overlays (new vs V50) ---")
    src = src.replace("# --- V193 overlays (new vs V49) ---", "# --- V194 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 107.17", "ASHFEN bait 108.18"),
        ("CEDARM bait 109.19", "CEDARF bait 110.20"),
        ("DAWNM ghost 32.32", "DAWNF ghost 33.33"),
        ("GLENM bait 102.12", "GLENF bait 103.13"),
        ("JADEM bait 93.93", "JADEF bait 94.94"),
        ("NETHERM bait 110.20", "NETHERF bait 111.21"),
        ("ash mist + stone ticks (V193-only)", "ash mist + stone ticks (V194-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD193 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v193_themes.json").read_text(encoding="utf-8"))["themes"])
NEW194 = "_".join(t[0] for t in T194)

out = (S / "c1265_vision_v193_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1265", "C1271"), ("c1265", "c1271"), ("V193", "V194"), ("v193", "v194"),
    ("_v193c1265", "_v194c1271"),
    ("Harder than V192", "Harder than V193"), ("harder than V192", "harder than V193"),
    (OLD193, NEW194),
    ("V193 keeps floor", "V194 keeps floor"),
    ("C1265 design+fixtures; no VL claim", "C1271 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1266 VL smoke", "fixtures only; claim deferred to C1272 VL smoke"),
    ("No claim until C1266 VL", "No claim until C1272 VL"),
    ("kept on V193", "kept on V194"),
    ("vision_images_v193", "vision_images_v194"),
    ("VL_GATE_V193", "VL_GATE_V194"), ("vl_gate_v193", "vl_gate_v194"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V192:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V193: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T194, "v194", "V194", TR194))
out = retarget_194(out)
(S / "c1271_vision_v194_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1266_vision_v193_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1266", "C1272"), ("c1266", "c1272"), ("V193", "V194"), ("v193", "v194"),
    ("vision_images_v193", "vision_images_v194"),
    ("VL_GATE_V193", "VL_GATE_V194"), ("vl_gate_v193", "vl_gate_v194"),
    ("runs/vision_v193", "runs/vision_v194"),
]:
    out = out.replace(a, b)
(S / "c1272_vision_v194_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1267_vision_v193_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1267", "C1273"), ("c1267", "c1273"), ("V193", "V194"), ("v193", "v194"),
    ("vision_images_v193h", "vision_images_v194h"),
    ("vision_images_v193", "vision_images_v194"),
    ("VL_GATE_V193", "VL_GATE_V194"), ("vl_gate_v193", "vl_gate_v194"),
    ("runs/vision_v193h", "runs/vision_v194h"),
    ("_v193c1265", "_v194c1271"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T194, "v194h", "V194H", HO194))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v194h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v194"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v194" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v194h_c1273"'); seen_run = True; continue
    out2.append(ln)
(S / "c1273_vision_v194_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1262_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1262", "C1274"), ("c1262", "c1274"),
    ("product_u2c_c1262", "product_u2c_c1274"),
    ("after V192", "after V194"), ("after V193", "after V194"),
]:
    out = out.replace(a, b)
(S / "c1274_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1269_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1269", "C1275"), ("c1269", "c1275"),
    ("capture_regression_c1269", "capture_regression_c1275"),
    ("after C1265-C1268", "after C1271-C1274"),
    ("V4-V193+heldout", "V4-V194+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V193", DOC / "C1266_VISION_V193_SMOKE.json"),'
if needle in out and "VISION_V194_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V194", DOC / "C1272_VISION_V194_SMOKE.json"),\n    ("V194_heldout", DOC / "C1273_VISION_V194_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1275_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

# scorecard from C1264 (product-U2C knife)
out = (S / "c1264_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1264", "C1276"), ("c1264", "c1276"),
    ("C1260", "C1272"), ("C1261", "C1273"), ("C1263", "C1275"),
    ("C1259", "C1271"), ("C1262", "C1274"),
    ("V192", "V194"), ("v192", "v194"),
    ("V191", "V193"), ("v191", "v193"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1256_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1268_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1256"', '"source": "C1268"')
out = out.replace(
    'f"- confidence-gate (prior C1256): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1268): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1276_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T194 if t[0].endswith("b")])
print("qty", TR194[1], HO194[1], "po", TR194[8], HO194[8], "sla", TR194[6], HO194[6], "fax", TR194[15], HO194[15])
print("done")
