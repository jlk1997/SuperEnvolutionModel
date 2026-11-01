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

# *mere ; qty TR 740+780 HO 840+760; PO TR 780+740 HO 840+760; SLA TR 480+520 HO 360+400
T178 = [
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
TR178 = [
    [1195.0, 1212.5, 1005.0],[740, 780, 820],[1118.0, 1147.25, 985.0],[1251.0, 1268.0, 1075.0],
    [1313.0, 1337.0, 1045.0],[1071, 1087, 1003],[480.0, 520.0, 570.0],[1161.0, 1192.75, 1009.0],
    [780.0, 740.0, 810.0],[1228.0, 1216.0, 1006.0],[1,1,0],[0,0,0],
    [1294.0, 1315.5, 1031.0],[1,0,0],[843, 835, 813],[861, 845, 748],[1,0,0],[887, 863, 833],
]
HO178 = [
    [1065.0, 1077.75, 958.0],[840, 760, 820],[1023.0, 1036.5, 946.0],[1138.0, 1154.0, 987.0],
    [1179.0, 1195.0, 982.0],[973, 987, 951],[360.0, 400.0, 550.0],[1049.0, 1070.75, 958.0],
    [840.0, 760.0, 810.0],[1096.0, 1082.0, 953.0],[1,1,0],[0,0,0],
    [1131.0, 1146.5, 968.0],[1,0,0],[821, 816, 811],[835, 829, 817],[1,0,0],[845, 839, 818],
]
check(TR178, "TR"); check(HO178, "HO")

(ROOT / "tools/_v178_themes.json").write_text(json.dumps({"themes": T178, "train": TR178, "heldout": HO178}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_178(src):
    src = src.replace("# --- V177 overlays (new vs V50) ---", "# --- V178 overlays (new vs V50) ---")
    src = src.replace("# --- V177 overlays (new vs V49) ---", "# --- V178 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 91.91", "ASHMERE bait 92.92"),
        ("CEDARH bait 93.93", "CEDARM bait 94.94"),
        ("DAWNH ghost 16.16", "DAWNM ghost 17.17"),
        ("GLENH bait 86.86", "GLENM bait 87.87"),
        ("JADEH bait 77.77", "JADEM bait 78.78"),
        ("NETHERH bait 94.94", "NETHERM bait 95.95"),
        ("ash mist + stone ticks (V177-only)", "ash mist + stone ticks (V178-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD177 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v177_themes.json").read_text(encoding="utf-8"))["themes"])
NEW178 = "_".join(t[0] for t in T178)

out = (S / "c1169_vision_v177_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1169", "C1175"), ("c1169", "c1175"), ("V177", "V178"), ("v177", "v178"),
    ("_v177c1169", "_v178c1175"),
    ("Harder than V176", "Harder than V177"), ("harder than V176", "harder than V177"),
    (OLD177, NEW178),
    ("V177 keeps floor", "V178 keeps floor"),
    ("C1169 design+fixtures; no VL claim", "C1175 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1170 VL smoke", "fixtures only; claim deferred to C1176 VL smoke"),
    ("No claim until C1170 VL", "No claim until C1176 VL"),
    ("kept on V177", "kept on V178"),
    ("vision_images_v177", "vision_images_v178"),
    ("VL_GATE_V177", "VL_GATE_V178"), ("vl_gate_v177", "vl_gate_v178"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V176:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V177: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T178, "v178", "V178", TR178))
out = retarget_178(out)
(S / "c1175_vision_v178_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1170_vision_v177_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1170", "C1176"), ("c1170", "c1176"), ("V177", "V178"), ("v177", "v178"),
    ("vision_images_v177", "vision_images_v178"),
    ("VL_GATE_V177", "VL_GATE_V178"), ("vl_gate_v177", "vl_gate_v178"),
    ("runs/vision_v177", "runs/vision_v178"),
]:
    out = out.replace(a, b)
(S / "c1176_vision_v178_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1171_vision_v177_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1171", "C1177"), ("c1171", "c1177"), ("V177", "V178"), ("v177", "v178"),
    ("vision_images_v177h", "vision_images_v178h"),
    ("vision_images_v177", "vision_images_v178"),
    ("VL_GATE_V177", "VL_GATE_V178"), ("vl_gate_v177", "vl_gate_v178"),
    ("runs/vision_v177h", "runs/vision_v178h"),
    ("_v177c1169", "_v178c1175"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T178, "v178h", "V178H", HO178))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v178h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v178"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v178" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v178h_c1177"'); seen_run = True; continue
    out2.append(ln)
(S / "c1177_vision_v178_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1166_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C1166", "C1178"), ("c1166", "c1178"),
    ("product_u2c_c1166", "product_u2c_c1178"),
    ("after V176", "after V178"), ("after V177", "after V178"),
]:
    out = out.replace(a, b)
(S / "c1178_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c1173_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1173", "C1179"), ("c1173", "c1179"),
    ("capture_regression_c1173", "capture_regression_c1179"),
    ("after C1169-C1172", "after C1175-C1178"),
    ("V4-V177+heldout", "V4-V178+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V177", DOC / "C1170_VISION_V177_SMOKE.json"),'
if needle in out and "VISION_V178_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V178", DOC / "C1176_VISION_V178_SMOKE.json"),\n    ("V178_heldout", DOC / "C1177_VISION_V178_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1179_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1174_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1174", "C1180"), ("c1174", "c1180"),
    ("C1170", "C1176"), ("C1171", "C1177"), ("C1173", "C1179"),
    ("C1169", "C1175"),
    ("V177", "V178"), ("v177", "v178"),
    ("V176", "V177"), ("v176", "v177"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1172_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1172_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1166_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1178_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1166"', '"source": "C1178"')
out = out.replace('"source": "C1172"', '"source": "C1172"')
out = out.replace(
    "stage_ready = bool(v178_claim and v178h_claim and v178 >= GATE and v178h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v178_claim and v178h_claim and v178 >= GATE and v178h >= GATE and capture_pass and disjoint and u2c_pass)",
)
out = out.replace(
    'f"- C1178: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1178: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- C1172: confidence-gate pass={conf_pass} rate={conf_rate}"',
    'f"- C1178: product-U2C replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- product-U2C (prior C1166): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1172): pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- product-U2C (prior C1178): replace={replace} pass={u2c_pass}"',
    'f"- confidence-gate (prior C1172): pass={conf_pass} rate={conf_rate}"',
)
(S / "c1180_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T178 if t[0].endswith("b")])
print("qty", TR178[1], HO178[1], "po", TR178[8], HO178[8], "sla", TR178[6], HO178[6], "fax", TR178[15], HO178[15])
print("done")
