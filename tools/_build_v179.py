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

# *wick ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 500+540 HO 380+420
# fax hold 748; scrub BAN
T179 = [
    ["ashwick","recv","paid_total","ASHWICK GRAIN RECV","RECV","x"],
    ["cedarwick","wh","qty_sum","WH CEDARWICK BIN","RECV","x"],
    ["dawnwick","refund","refund_done","DAWNWICK PATCH REFUND","DONE","x"],
    ["elmwick","tax","tax_base_paid","ELMWICK TAX SLIP","TAX","x"],
    ["fernwick","pay","payroll_active","FERNWICK PAYROLL","PAY","x"],
    ["glenwick","ship","ship_ok","GLENWICK SHIP DOCK","SHIP","x"],
    ["hazewick","sla","sla_ok_hours","HAZEWICK SLA CARD","SLA","x"],
    ["inkwick","exp","exp_sum","INKWICK EXPENSE","EXP","x"],
    ["jadewick","po","po_open","JADEWICK PO SHEET","PO","x"],
    ["knotwick","order","order_paid","KNOTWICK ORDER","ORD","x"],
    ["lakewick","dup","dup_mark","LAKEWICK DUP MARK","DUP","x"],
    ["mosswick","zero","zero_check","MOSSWICK AIR ZERO","ZERO","x"],
    ["netherwick","ledger","ledger_net","NETHERWICK LEDGER","LED","x"],
    ["oakwick","ui","ui_ok","OAKWICK UI SCAN","UI","x"],
    ["pinewick","stack","stack_count","PINEWICK STACK","STK","x"],
    ["quillwick","fax","fax_pages","QUILLWICK FAX","FAX","x"],
    ["reedwick","glare","glare_ok","REEDWICK GLARE","GLR","x"],
    ["stonewick","tab","tab_index","STONEWICK TAB INDEX","TAB","x"],
]
TR179 = [
    [1204.0, 1221.5, 1014.0],[840, 760, 820],[1127.0, 1156.25, 994.0],[1260.0, 1277.0, 1084.0],
    [1322.0, 1346.0, 1054.0],[1080, 1096, 1012],[500.0, 540.0, 580.0],[1170.0, 1201.75, 1018.0],
    [840.0, 760.0, 820.0],[1237.0, 1225.0, 1015.0],[1,1,0],[0,0,0],
    [1303.0, 1324.5, 1040.0],[1,0,0],[852, 844, 822],[870, 854, 748],[1,0,0],[896, 872, 842],
]
HO179 = [
    [1074.0, 1086.75, 967.0],[740, 780, 820],[1032.0, 1045.5, 955.0],[1147.0, 1163.0, 996.0],
    [1188.0, 1204.0, 991.0],[982, 996, 960],[380.0, 420.0, 560.0],[1058.0, 1079.75, 967.0],
    [780.0, 740.0, 820.0],[1105.0, 1091.0, 962.0],[1,1,0],[0,0,0],
    [1140.0, 1155.5, 977.0],[1,0,0],[829, 824, 819],[844, 838, 826],[1,0,0],[854, 848, 827],
]
check(TR179, "TR"); check(HO179, "HO")

(ROOT / "tools/_v179_themes.json").write_text(json.dumps({"themes": T179, "train": TR179, "heldout": HO179}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_179(src):
    src = src.replace("# --- V178 overlays (new vs V50) ---", "# --- V179 overlays (new vs V50) ---")
    src = src.replace("# --- V178 overlays (new vs V49) ---", "# --- V179 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 92.92", "ASHWICK bait 93.93"),
        ("CEDARM bait 94.94", "CEDARW bait 95.95"),
        ("DAWNM ghost 17.17", "DAWNW ghost 18.18"),
        ("GLENM bait 87.87", "GLENW bait 88.88"),
        ("JADEM bait 78.78", "JADEW bait 79.79"),
        ("NETHERM bait 95.95", "NETHERW bait 96.96"),
        ("ash mist + stone ticks (V178-only)", "ash mist + stone ticks (V179-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD178 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v178_themes.json").read_text(encoding="utf-8"))["themes"])
NEW179 = "_".join(t[0] for t in T179)

out = (S / "c1175_vision_v178_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1175", "C1181"), ("c1175", "c1181"), ("V178", "V179"), ("v178", "v179"),
    ("_v178c1175", "_v179c1181"),
    ("Harder than V177", "Harder than V178"), ("harder than V177", "harder than V178"),
    (OLD178, NEW179),
    ("V178 keeps floor", "V179 keeps floor"),
    ("C1175 design+fixtures; no VL claim", "C1181 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1176 VL smoke", "fixtures only; claim deferred to C1182 VL smoke"),
    ("No claim until C1176 VL", "No claim until C1182 VL"),
    ("kept on V178", "kept on V179"),
    ("vision_images_v178", "vision_images_v179"),
    ("VL_GATE_V178", "VL_GATE_V179"), ("vl_gate_v178", "vl_gate_v179"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V177:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V178: ashwick, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T179, "v179", "V179", TR179))
out = retarget_179(out)
(S / "c1181_vision_v179_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1176_vision_v178_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1176", "C1182"), ("c1176", "c1182"), ("V178", "V179"), ("v178", "v179"),
    ("vision_images_v178", "vision_images_v179"),
    ("VL_GATE_V178", "VL_GATE_V179"), ("vl_gate_v178", "vl_gate_v179"),
    ("runs/vision_v178", "runs/vision_v179"),
]:
    out = out.replace(a, b)
(S / "c1182_vision_v179_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1177_vision_v178_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1177", "C1183"), ("c1177", "c1183"), ("V178", "V179"), ("v178", "v179"),
    ("vision_images_v178h", "vision_images_v179h"),
    ("vision_images_v178", "vision_images_v179"),
    ("VL_GATE_V178", "VL_GATE_V179"), ("vl_gate_v178", "vl_gate_v179"),
    ("runs/vision_v178h", "runs/vision_v179h"),
    ("_v178c1175", "_v179c1181"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T179, "v179h", "V179H", HO179))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v179h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v179"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v179" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v179h_c1183"'); seen_run = True; continue
    out2.append(ln)
(S / "c1183_vision_v179_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1172_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1172", "C1184"), ("c1172", "c1184"),
    ("conf_gate_stretch_c1172", "conf_gate_stretch_c1184"),
    ("cg71_", "cg72_"),
    ("after V177", "after V179"), ("after V178", "after V179"),
]:
    out = out.replace(a, b)
(S / "c1184_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("conf")

out = (S / "c1179_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1179", "C1185"), ("c1179", "c1185"),
    ("capture_regression_c1179", "capture_regression_c1185"),
    ("after C1175-C1178", "after C1181-C1184"),
    ("V4-V178+heldout", "V4-V179+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V178", DOC / "C1176_VISION_V178_SMOKE.json"),'
if needle in out and "VISION_V179_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V179", DOC / "C1182_VISION_V179_SMOKE.json"),\n    ("V179_heldout", DOC / "C1183_VISION_V179_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1185_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1174_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1174", "C1186"), ("c1174", "c1186"),
    ("C1170", "C1182"), ("C1171", "C1183"), ("C1173", "C1185"),
    ("C1169", "C1181"), ("C1172", "C1184"),
    ("V177", "V179"), ("v177", "v179"),
    ("V176", "V178"), ("v176", "v178"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c650 = load("docs/r50/C1166_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1178_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1166"', '"source": "C1178"')
out = out.replace(
    'f"- product-U2C (prior C1166): replace={replace} pass={u2c_pass}"',
    'f"- product-U2C (prior C1178): replace={replace} pass={u2c_pass}"',
)
(S / "c1186_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T179 if t[0].endswith("b")])
print("qty", TR179[1], HO179[1], "po", TR179[8], HO179[8], "sla", TR179[6], HO179[6], "fax", TR179[15], HO179[15])
print("done")
