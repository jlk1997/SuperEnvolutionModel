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

# *dale (rotation restart); qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740
# SLA TR 480+520 HO 360+400 (lesson: avoid 550+590→1249 misparse)
T185 = [
    ["ashdale","recv","paid_total","ASHDALE GRAIN RECV","RECV","x"],
    ["cedardale","wh","qty_sum","WH CEDARDALE BIN","RECV","x"],
    ["dawndale","refund","refund_done","DAWNDALE PATCH REFUND","DONE","x"],
    ["elmdale","tax","tax_base_paid","ELMDALE TAX SLIP","TAX","x"],
    ["ferndale","pay","payroll_active","FERNDALE PAYROLL","PAY","x"],
    ["glendale","ship","ship_ok","GLENDALE SHIP DOCK","SHIP","x"],
    ["hazedale","sla","sla_ok_hours","HAZEDALE SLA CARD","SLA","x"],
    ["inkdale","exp","exp_sum","INKDALE EXPENSE","EXP","x"],
    ["jadedale","po","po_open","JADEDALE PO SHEET","PO","x"],
    ["knotdale","order","order_paid","KNOTDALE ORDER","ORD","x"],
    ["lakedale","dup","dup_mark","LAKEDALE DUP MARK","DUP","x"],
    ["mossdale","zero","zero_check","MOSSDALE AIR ZERO","ZERO","x"],
    ["netherdale","ledger","ledger_net","NETHERDALE LEDGER","LED","x"],
    ["oakdale","ui","ui_ok","OAKDALE UI SCAN","UI","x"],
    ["pinedale","stack","stack_count","PINEDALE STACK","STK","x"],
    ["quilldale","fax","fax_pages","QUILLDALE FAX","FAX","x"],
    ["reeddale","glare","glare_ok","REEDDALE GLARE","GLR","x"],
    ["stonedale","tab","tab_index","STONEDALE TAB INDEX","TAB","x"],
]
TR185 = [
    [1258.0, 1275.5, 1068.0],[840, 760, 820],[1181.0, 1210.25, 1048.0],[1314.0, 1331.0, 1138.0],
    [1376.0, 1400.0, 1108.0],[1134, 1150, 1066],[480.0, 520.0, 650.0],[1224.0, 1255.75, 1072.0],
    [840.0, 760.0, 820.0],[1291.0, 1279.0, 1069.0],[1,1,0],[0,0,0],
    [1357.0, 1378.5, 1094.0],[1,0,0],[906, 898, 876],[924, 908, 748],[1,0,0],[950, 926, 896],
]
HO185 = [
    [1128.0, 1140.75, 1021.0],[740, 780, 820],[1086.0, 1099.5, 1009.0],[1201.0, 1217.0, 1050.0],
    [1242.0, 1258.0, 1045.0],[1036, 1050, 1014],[360.0, 400.0, 590.0],[1112.0, 1133.75, 1021.0],
    [780.0, 740.0, 820.0],[1159.0, 1145.0, 1016.0],[1,1,0],[0,0,0],
    [1194.0, 1209.5, 1031.0],[1,0,0],[883, 878, 873],[898, 892, 880],[1,0,0],[908, 902, 881],
]
check(TR185, "TR"); check(HO185, "HO")

(ROOT / "tools/_v185_themes.json").write_text(json.dumps({"themes": T185, "train": TR185, "heldout": HO185}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_185(src):
    src = src.replace("# --- V184 overlays (new vs V50) ---", "# --- V185 overlays (new vs V50) ---")
    src = src.replace("# --- V184 overlays (new vs V49) ---", "# --- V185 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 98.98", "ASHDALE bait 99.99"),
        ("CEDARB bait 100.10", "CEDARD bait 101.11"),
        ("DAWNB ghost 23.23", "DAWND ghost 24.24"),
        ("GLENB bait 93.93", "GLEND bait 94.94"),
        ("JADEB bait 84.84", "JADED bait 85.85"),
        ("NETHERB bait 101.11", "NETHERD bait 102.12"),
        ("ash mist + stone ticks (V184-only)", "ash mist + stone ticks (V185-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD184 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v184_themes.json").read_text(encoding="utf-8"))["themes"])
NEW185 = "_".join(t[0] for t in T185)

out = (S / "c1211_vision_v184_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1211", "C1217"), ("c1211", "c1217"), ("V184", "V185"), ("v184", "v185"),
    ("_v184c1211", "_v185c1217"),
    ("Harder than V183", "Harder than V184"), ("harder than V183", "harder than V184"),
    (OLD184, NEW185),
    ("V184 keeps floor", "V185 keeps floor"),
    ("C1211 design+fixtures; no VL claim", "C1217 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1212 VL smoke", "fixtures only; claim deferred to C1218 VL smoke"),
    ("No claim until C1212 VL", "No claim until C1218 VL"),
    ("kept on V184", "kept on V185"),
    ("vision_images_v184", "vision_images_v185"),
    ("VL_GATE_V184", "VL_GATE_V185"), ("vl_gate_v184", "vl_gate_v185"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V183:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V184: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T185, "v185", "V185", TR185))
out = retarget_185(out)
(S / "c1217_vision_v185_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1212_vision_v184_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1212", "C1218"), ("c1212", "c1218"), ("V184", "V185"), ("v184", "v185"),
    ("vision_images_v184", "vision_images_v185"),
    ("VL_GATE_V184", "VL_GATE_V185"), ("vl_gate_v184", "vl_gate_v185"),
    ("runs/vision_v184", "runs/vision_v185"),
]:
    out = out.replace(a, b)
(S / "c1218_vision_v185_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1213_vision_v184_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1213", "C1219"), ("c1213", "c1219"), ("V184", "V185"), ("v184", "v185"),
    ("vision_images_v184h", "vision_images_v185h"),
    ("vision_images_v184", "vision_images_v185"),
    ("VL_GATE_V184", "VL_GATE_V185"), ("vl_gate_v184", "vl_gate_v185"),
    ("runs/vision_v184h", "runs/vision_v185h"),
    ("_v184c1211", "_v185c1217"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T185, "v185h", "V185H", HO185))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v185h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v185"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v185" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v185h_c1219"'); seen_run = True; continue
    out2.append(ln)
(S / "c1219_vision_v185_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1208_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1208", "C1220"), ("c1208", "c1220"),
    ("conf_gate_stretch_c1208", "conf_gate_stretch_c1220"),
    ("cg74_", "cg75_"),
    ("after V183", "after V185"), ("after V184", "after V185"),
]:
    out = out.replace(a, b)
(S / "c1220_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1215_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1215", "C1221"), ("c1215", "c1221"),
    ("capture_regression_c1215", "capture_regression_c1221"),
    ("after C1211-C1214", "after C1217-C1220"),
    ("V4-V184+heldout", "V4-V185+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V184", DOC / "C1212_VISION_V184_SMOKE.json"),'
if needle in out and "VISION_V185_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V185", DOC / "C1218_VISION_V185_SMOKE.json"),\n    ("V185_heldout", DOC / "C1219_VISION_V185_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1221_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1210_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1210", "C1222"), ("c1210", "c1222"),
    ("C1206", "C1218"), ("C1207", "C1219"), ("C1209", "C1221"),
    ("C1205", "C1217"), ("C1208", "C1220"),
    ("V183", "V185"), ("v183", "v185"),
    ("V182", "V184"), ("v182", "v184"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1202_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1214_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1202"', '"source": "C1214"')
out = out.replace(
    'f"- product-U2C (prior C1202): replace={replace} pass={u2c_pass}"',
    'f"- product-U2C (prior C1214): replace={replace} pass={u2c_pass}"',
)
(S / "c1222_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T185 if t[0].endswith("b")])
print("qty", TR185[1], HO185[1], "po", TR185[8], HO185[8], "sla", TR185[6], HO185[6], "fax", TR185[15], HO185[15])
print("done")
