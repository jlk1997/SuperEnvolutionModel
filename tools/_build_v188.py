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

# *holm ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T188 = [
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
TR188 = [
    [1285.0, 1302.5, 1095.0],[740, 780, 820],[1208.0, 1237.25, 1075.0],[1341.0, 1358.0, 1165.0],
    [1403.0, 1427.0, 1135.0],[1161, 1177, 1093],[480.0, 520.0, 680.0],[1251.0, 1282.75, 1099.0],
    [780.0, 740.0, 820.0],[1318.0, 1306.0, 1096.0],[1,1,0],[0,0,0],
    [1384.0, 1405.5, 1121.0],[1,0,0],[933, 925, 903],[951, 935, 748],[1,0,0],[977, 953, 923],
]
HO188 = [
    [1155.0, 1167.75, 1048.0],[840, 760, 820],[1113.0, 1126.5, 1036.0],[1228.0, 1244.0, 1077.0],
    [1269.0, 1285.0, 1072.0],[1063, 1077, 1041],[360.0, 400.0, 620.0],[1139.0, 1160.75, 1048.0],
    [840.0, 760.0, 820.0],[1186.0, 1172.0, 1043.0],[1,1,0],[0,0,0],
    [1221.0, 1236.5, 1058.0],[1,0,0],[910, 905, 900],[925, 919, 907],[1,0,0],[935, 929, 908],
]
check(TR188, "TR"); check(HO188, "HO")

(ROOT / "tools/_v188_themes.json").write_text(json.dumps({"themes": T188, "train": TR188, "heldout": HO188}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_188(src):
    src = src.replace("# --- V187 overlays (new vs V50) ---", "# --- V188 overlays (new vs V50) ---")
    src = src.replace("# --- V187 overlays (new vs V49) ---", "# --- V188 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 101.11", "ASHHOLM bait 102.12"),
        ("CEDARF bait 103.13", "CEDARH bait 104.14"),
        ("DAWNF ghost 26.26", "DAWNH ghost 27.27"),
        ("GLENF bait 96.96", "GLENH bait 97.97"),
        ("JADEF bait 87.87", "JADEH bait 88.88"),
        ("NETHERF bait 104.14", "NETHERH bait 105.15"),
        ("ash mist + stone ticks (V187-only)", "ash mist + stone ticks (V188-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD187 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v187_themes.json").read_text(encoding="utf-8"))["themes"])
NEW188 = "_".join(t[0] for t in T188)

out = (S / "c1229_vision_v187_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1229", "C1235"), ("c1229", "c1235"), ("V187", "V188"), ("v187", "v188"),
    ("_v187c1229", "_v188c1235"),
    ("Harder than V186", "Harder than V187"), ("harder than V186", "harder than V187"),
    (OLD187, NEW188),
    ("V187 keeps floor", "V188 keeps floor"),
    ("C1229 design+fixtures; no VL claim", "C1235 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1230 VL smoke", "fixtures only; claim deferred to C1236 VL smoke"),
    ("No claim until C1230 VL", "No claim until C1236 VL"),
    ("kept on V187", "kept on V188"),
    ("vision_images_v187", "vision_images_v188"),
    ("VL_GATE_V187", "VL_GATE_V188"), ("vl_gate_v187", "vl_gate_v188"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V186:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V187: ashholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T188, "v188", "V188", TR188))
out = retarget_188(out)
(S / "c1235_vision_v188_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1230_vision_v187_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1230", "C1236"), ("c1230", "c1236"), ("V187", "V188"), ("v187", "v188"),
    ("vision_images_v187", "vision_images_v188"),
    ("VL_GATE_V187", "VL_GATE_V188"), ("vl_gate_v187", "vl_gate_v188"),
    ("runs/vision_v187", "runs/vision_v188"),
]:
    out = out.replace(a, b)
(S / "c1236_vision_v188_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1231_vision_v187_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1231", "C1237"), ("c1231", "c1237"), ("V187", "V188"), ("v187", "v188"),
    ("vision_images_v187h", "vision_images_v188h"),
    ("vision_images_v187", "vision_images_v188"),
    ("VL_GATE_V187", "VL_GATE_V188"), ("vl_gate_v187", "vl_gate_v188"),
    ("runs/vision_v187h", "runs/vision_v188h"),
    ("_v187c1229", "_v188c1235"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T188, "v188h", "V188H", HO188))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v188h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v188"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v188" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v188h_c1237"'); seen_run = True; continue
    out2.append(ln)
(S / "c1237_vision_v188_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1226_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1226", "C1238"), ("c1226", "c1238"),
    ("product_u2c_c1226", "product_u2c_c1238"),
    ("after V186", "after V188"), ("after V187", "after V188"),
]:
    out = out.replace(a, b)
(S / "c1238_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1233_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1233", "C1239"), ("c1233", "c1239"),
    ("capture_regression_c1233", "capture_regression_c1239"),
    ("after C1229-C1232", "after C1235-C1238"),
    ("V4-V187+heldout", "V4-V188+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V187", DOC / "C1230_VISION_V187_SMOKE.json"),'
if needle in out and "VISION_V188_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V188", DOC / "C1236_VISION_V188_SMOKE.json"),\n    ("V188_heldout", DOC / "C1237_VISION_V188_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1239_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1228_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1228", "C1240"), ("c1228", "c1240"),
    ("C1224", "C1236"), ("C1225", "C1237"), ("C1227", "C1239"),
    ("C1223", "C1235"), ("C1226", "C1238"),
    ("V186", "V188"), ("v186", "v188"),
    ("V185", "V187"), ("v185", "v187"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1220_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1232_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace('"source": "C1220"', '"source": "C1232"')
out = out.replace(
    'f"- confidence-gate (prior C1220): pass={conf_pass} rate={conf_rate}"',
    'f"- confidence-gate (prior C1232): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1240_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T188 if t[0].endswith("b")])
print("qty", TR188[1], HO188[1], "po", TR188[8], HO188[8], "sla", TR188[6], HO188[6], "fax", TR188[15], HO188[15])
print("done")
