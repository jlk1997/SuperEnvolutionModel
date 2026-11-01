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

# *holm ; qty TR 840+760 HO 740+780; PO TR 840+760 HO 780+740; SLA TR 460+500 HO 360+400
T177 = [
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
TR177 = [
    [1186.0, 1203.5, 996.0],[840, 760, 820],[1109.0, 1138.25, 976.0],[1242.0, 1259.0, 1066.0],
    [1304.0, 1328.0, 1036.0],[1062, 1078, 994],[460.0, 500.0, 560.0],[1152.0, 1183.75, 1000.0],
    [840.0, 760.0, 800.0],[1219.0, 1207.0, 997.0],[1,1,0],[0,0,0],
    [1285.0, 1306.5, 1022.0],[1,0,0],[834, 826, 804],[852, 836, 748],[1,0,0],[878, 854, 824],
]
HO177 = [
    [1056.0, 1068.75, 949.0],[740, 780, 820],[1014.0, 1027.5, 937.0],[1129.0, 1145.0, 978.0],
    [1170.0, 1186.0, 973.0],[964, 978, 942],[360.0, 400.0, 540.0],[1040.0, 1061.75, 949.0],
    [780.0, 740.0, 800.0],[1087.0, 1073.0, 944.0],[1,1,0],[0,0,0],
    [1122.0, 1137.5, 959.0],[1,0,0],[812, 807, 802],[826, 820, 808],[1,0,0],[836, 830, 809],
]
# HO tabB 830 banned
HO177[17] = [836, 828, 809]
check(TR177, "TR"); check(HO177, "HO")

(ROOT / "tools/_v177_themes.json").write_text(json.dumps({"themes": T177, "train": TR177, "heldout": HO177}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_177(src):
    src = src.replace("# --- V176 overlays (new vs V50) ---", "# --- V177 overlays (new vs V50) ---")
    src = src.replace("# --- V176 overlays (new vs V49) ---", "# --- V177 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 90.90", "ASHHOLM bait 91.91"),
        ("CEDARF bait 92.92", "CEDARH bait 93.93"),
        ("DAWNF ghost 15.15", "DAWNH ghost 16.16"),
        ("GLENF bait 85.85", "GLENH bait 86.86"),
        ("JADEF bait 76.76", "JADEH bait 77.77"),
        ("NETHERF bait 93.93", "NETHERH bait 94.94"),
        ("ash mist + stone ticks (V176-only)", "ash mist + stone ticks (V177-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD176 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v176_themes.json").read_text(encoding="utf-8"))["themes"])
NEW177 = "_".join(t[0] for t in T177)

out = (S / "c1163_vision_v176_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1163", "C1169"), ("c1163", "c1169"), ("V176", "V177"), ("v176", "v177"),
    ("_v176c1163", "_v177c1169"),
    ("Harder than V175", "Harder than V176"), ("harder than V175", "harder than V176"),
    (OLD176, NEW177),
    ("V176 keeps floor", "V177 keeps floor"),
    ("C1163 design+fixtures; no VL claim", "C1169 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1164 VL smoke", "fixtures only; claim deferred to C1170 VL smoke"),
    ("No claim until C1164 VL", "No claim until C1170 VL"),
    ("kept on V176", "kept on V177"),
    ("vision_images_v176", "vision_images_v177"),
    ("VL_GATE_V176", "VL_GATE_V177"), ("vl_gate_v176", "vl_gate_v177"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V175:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V176: ashholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T177, "v177", "V177", TR177))
out = retarget_177(out)
(S / "c1169_vision_v177_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1164_vision_v176_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1164", "C1170"), ("c1164", "c1170"), ("V176", "V177"), ("v176", "v177"),
    ("vision_images_v176", "vision_images_v177"),
    ("VL_GATE_V176", "VL_GATE_V177"), ("vl_gate_v176", "vl_gate_v177"),
    ("runs/vision_v176", "runs/vision_v177"),
]:
    out = out.replace(a, b)
(S / "c1170_vision_v177_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1165_vision_v176_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1165", "C1171"), ("c1165", "c1171"), ("V176", "V177"), ("v176", "v177"),
    ("vision_images_v176h", "vision_images_v177h"),
    ("vision_images_v176", "vision_images_v177"),
    ("VL_GATE_V176", "VL_GATE_V177"), ("vl_gate_v176", "vl_gate_v177"),
    ("runs/vision_v176h", "runs/vision_v177h"),
    ("_v176c1163", "_v177c1169"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T177, "v177h", "V177H", HO177))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v177h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v177"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v177" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v177h_c1171"'); seen_run = True; continue
    out2.append(ln)
(S / "c1171_vision_v177_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c1160_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1160", "C1172"), ("c1160", "c1172"),
    ("conf_gate_stretch_c1160", "conf_gate_stretch_c1172"),
    ("after V175", "after V177"), ("after V176", "after V177"),
    ("cg89_", "cg90_"),
]:
    out = out.replace(a, b)
(S / "c1172_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c1167_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C1167", "C1173"), ("c1167", "c1173"),
    ("capture_regression_c1167", "capture_regression_c1173"),
    ("after C1163-C1166", "after C1169-C1172"),
    ("V4-V176+heldout", "V4-V177+heldout"),
]:
    out = out.replace(a, b)
needle = '    ("V176", DOC / "C1164_VISION_V176_SMOKE.json"),'
if needle in out and "VISION_V177_SMOKE" not in out:
    out = out.replace(
        needle,
        '    ("V177", DOC / "C1170_VISION_V177_SMOKE.json"),\n    ("V177_heldout", DOC / "C1171_VISION_V177_HELDOUT_SMOKE.json"),\n' + needle,
        1,
    )
(S / "c1173_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c1168_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C1168", "C1174"), ("c1168", "c1174"),
    ("C1164", "C1170"), ("C1165", "C1171"), ("C1167", "C1173"),
    ("C1163", "C1169"),
    ("V176", "V177"), ("v176", "v177"),
    ("V175", "V176"), ("v175", "v176"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C1160_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C1172_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C1166_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C1166_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace('"source": "C1166"', '"source": "C1166"')
out = out.replace('"source": "C1160"', '"source": "C1172"')
out = out.replace(
    "stage_ready = bool(v177_claim and v177h_claim and v177 >= GATE and v177h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v177_claim and v177h_claim and v177 >= GATE and v177h >= GATE and capture_pass and disjoint and conf_pass)",
)
out = out.replace(
    'f"- C1172: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1172: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- C1166: product-U2C replace={replace} pass={u2c_pass}"',
    'f"- C1172: confidence-gate pass={conf_pass} rate={conf_rate}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1160): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1166): replace={replace} pass={u2c_pass}"',
)
out = out.replace(
    'f"- confidence-gate (prior C1172): pass={conf_pass} rate={conf_rate}"',
    'f"- product-U2C (prior C1166): replace={replace} pass={u2c_pass}"',
)
(S / "c1174_scorecard_and_stage.py").write_text(out, encoding="utf-8")
print("any_b", [t[0] for t in T177 if t[0].endswith("b")])
print("qty", TR177[1], HO177[1], "po", TR177[8], HO177[8], "sla", TR177[6], HO177[6], "fax", TR177[15], HO177[15], "tab", TR177[17], HO177[17])
print("done")
