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

# *hurst ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 520+560 HO 400+440
T181 = [
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
TR181 = [
    [1222.0, 1239.5, 1032.0],[840, 760, 820],[1145.0, 1174.25, 1012.0],[1278.0, 1295.0, 1102.0],
    [1340.0, 1364.0, 1072.0],[1098, 1114, 1030],[520.0, 560.0, 600.0],[1188.0, 1219.75, 1036.0],
    [840.0, 760.0, 820.0],[1255.0, 1243.0, 1033.0],[1,1,0],[0,0,0],
    [1321.0, 1342.5, 1058.0],[1,0,0],[870, 862, 840],[888, 872, 748],[1,0,0],[914, 890, 860],
]
HO181 = [
    [1092.0, 1104.75, 985.0],[740, 780, 820],[1050.0, 1063.5, 973.0],[1165.0, 1181.0, 1014.0],
    [1206.0, 1222.0, 1009.0],[1000, 1014, 978],[400.0, 440.0, 580.0],[1076.0, 1097.75, 985.0],
    [780.0, 740.0, 820.0],[1123.0, 1109.0, 980.0],[1,1,0],[0,0,0],
    [1158.0, 1173.5, 995.0],[1,0,0],[847, 842, 837],[862, 856, 844],[1,0,0],[872, 866, 845],
]
check(TR181, "TR"); check(HO181, "HO")

(ROOT / "tools/_v181_themes.json").write_text(json.dumps({"themes": T181, "train": TR181, "heldout": HO181}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_181(src):
    src = src.replace("# --- V180 overlays (new vs V50) ---", "# --- V181 overlays (new vs V50) ---")
    src = src.replace("# --- V180 overlays (new vs V49) ---", "# --- V181 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 94.94", "ASHHURST bait 95.95"),
        ("CEDARC bait 96.96", "CEDARH bait 97.97"),
        ("DAWNC ghost 19.19", "DAWNH ghost 20.20"),
        ("GLENC bait 89.89", "GLENH bait 90.90"),
        ("JADEC bait 80.80", "JADEH bait 81.81"),
        ("NETHERC bait 97.97", "NETHERH bait 98.98"),
        ("ash mist + stone ticks (V180-only)", "ash mist + stone ticks (V181-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD180 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v180_themes.json").read_text(encoding="utf-8"))["themes"])
NEW181 = "_".join(t[0] for t in T181)

out = (S / "c1187_vision_v180_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1187", "C1193"), ("c1187", "c1193"), ("V180", "V181"), ("v180", "v181"),
    ("_v180c1187", "_v181c1193"),
    ("Harder than V179", "Harder than V180"), ("harder than V179", "harder than V180"),
    (OLD180, NEW181),
    ("V180 keeps floor", "V181 keeps floor"),
    ("C1187 design+fixtures; no VL claim", "C1193 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1188 VL smoke", "fixtures only; claim deferred to C1194 VL smoke"),
    ("No claim until C1188 VL", "No claim until C1194 VL"),
    ("kept on V180", "kept on V181"),
    ("vision_images_v180", "vision_images_v181"),
    ("VL_GATE_V180", "VL_GATE_V181"), ("vl_gate_v180", "vl_gate_v181"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V179:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V180: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T181, "v181", "V181", TR181))
out = retarget_181(out)
(S / "c1193_vision_v181_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1188_vision_v180_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1188", "C1194"), ("c1188", "c1194"), ("V180", "V181"), ("v180", "v181"),
    ("vision_images_v180", "vision_images_v181"),
    ("VL_GATE_V180", "VL_GATE_V181"), ("vl_gate_v180", "vl_gate_v181"),
    ("runs/vision_v180", "runs/vision_v181"),
]:
    out = out.replace(a, b)
(S / "c1194_vision_v181_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1189_vision_v180_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1189", "C1195"), ("c1189", "c1195"), ("V180", "V181"), ("v180", "v181"),
    ("vision_images_v180h", "vision_images_v181h"),
    ("vision_images_v180", "vision_images_v181"),
    ("VL_GATE_V180", "VL_GATE_V181"), ("vl_gate_v180", "vl_gate_v181"),
    ("runs/vision_v180h", "runs/vision_v181h"),
    ("_v180c1187", "_v181c1193"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T181, "v181h", "V181H", HO181))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v181h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v181"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v181" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v181h_c1195"'); seen_run = True; continue
    out2.append(ln)
(S / "c1195_vision_v181_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1184_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1184", "C1196"), ("c1184", "c1196"),
    ("conf_gate_stretch_c1184", "conf_gate_stretch_c1196"),
    ("cg72_", "cg73_"),
    ("after V179", "after V181"), ("after V180", "after V181"),
]:
    out = out.replace(a, b)
(S / "c1196_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1191_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1191", "C1197"), ("c1191", "c1197"),
    ("capture_regression_c1191", "capture_regression_c1197"),
    ("after C1187-C1190", "after C1193-C1196"),
    ("V4-V180+heldout", "V4-V181+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V180", DOC / "C1188_VISION_V180_SMOKE.json"),'
if needle in out and "VISION_V181_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V181", DOC / "C1194_VISION_V181_SMOKE.json"),\n    ("V181_heldout", DOC / "C1195_VISION_V181_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1197_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1186_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1186", "C1198"), ("c1186", "c1198"),
    ("C1182", "C1194"), ("C1183", "C1195"), ("C1185", "C1197"),
    ("C1181", "C1193"), ("C1184", "C1196"),
    ("V179", "V181"), ("v179", "v181"),
    ("V178", "V180"), ("v178", "v180"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1178_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1190_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1178"', '"source": "C1190"')
out = out.replace(
    'f"- product-U2C (prior C1178): replace={replace} pass={u2c_pass}"',
    'f"- product-U2C (prior C1190): replace={replace} pass={u2c_pass}"',
)
(S / "c1198_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T181 if t[0].endswith("b")])
print("qty", TR181[1], HO181[1], "po", TR181[8], HO181[8], "sla", TR181[6], HO181[6], "fax", TR181[15], HO181[15])
print("done")
