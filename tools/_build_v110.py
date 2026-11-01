# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(r"E:\envolution")
S = ROOT / "scripts"

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

T110 = [
    ["anchorpeak","recv","paid_total","ANCHORPEAK GRAIN RECV","RECV","x"],
    ["brookpeak","wh","qty_sum","WH BROOKPEAK BIN","RECV","x"],
    ["cliffpeak","refund","refund_done","CLIFFPEAK PATCH REFUND","DONE","x"],
    ["driftpeak","tax","tax_base_paid","DRIFTPEAK TAX SLIP","TAX","x"],
    ["echopeak","pay","payroll_active","ECHOPEAK PAYROLL","PAY","x"],
    ["flintpeak","ship","ship_ok","FLINTPEAK SHIP DOCK","SHIP","x"],
    ["granitepeak","sla","sla_ok_hours","GRANITEPEAK SLA CARD","SLA","x"],
    ["havenpeak","exp","exp_sum","HAVENPEAK EXPENSE","EXP","x"],
    ["ivorypeak","po","po_open","IVORYPEAK PO SHEET","PO","x"],
    ["jasperpeak","order","order_paid","JASPERPEAK ORDER","ORD","x"],
    ["knollpeak","dup","dup_mark","KNOLLPEAK DUP MARK","DUP","x"],
    ["ledgepeak","zero","zero_check","LEDGEPEAK AIR ZERO","ZERO","x"],
    ["maplepeak","ledger","ledger_net","MAPLEPEAK LEDGER","LED","x"],
    ["northpeak","ui","ui_ok","NORTHPEAK UI SCAN","UI","x"],
    ["opalpeak","stack","stack_count","OPALPEAK STACK","STK","x"],
    ["plumepeak","fax","fax_pages","PLUMEPEAK FAX","FAX","x"],
    ["quartzpeak","glare","glare_ok","QUARTZPEAK GLARE","GLR","x"],
    ["ridgepeak","tab","tab_index","RIDGEPEAK TAB INDEX","TAB","x"],
]
TR110 = [
    [580.0, 596.5, 389.0],[506, 546, 362],[503.0, 532.25, 369.0],[634.0, 652.0, 459.0],
    [697.0, 721.0, 429.0],[455, 471, 387],[340.0, 380.0, 220.0],[545.0, 576.75, 393.0],
    [579.0, 562.0, 402.0],[612.0, 600.0, 390.0],[1,1,0],[0,0,0],
    [678.0, 699.5, 415.0],[1,0,0],[247, 239, 217],[265, 249, 240],[1,0,0],[291, 267, 237],
]
HO110 = [
    [449.0, 461.75, 342.0],[404, 444, 324],[407.0, 420.5, 330.0],[522.0, 538.0, 371.0],
    [563.0, 579.0, 366.0],[357, 371, 335],[240.0, 280.0, 180.0],[433.0, 454.75, 342.0],
    [453.0, 441.0, 345.0],[480.0, 466.0, 337.0],[1,1,0],[0,0,0],
    [515.0, 530.5, 352.0],[1,0,0],[223, 220, 215],[239, 233, 221],[1,0,0],[249, 243, 222],
]
(ROOT / "tools/_v110_themes.json").write_text(json.dumps({"themes": T110, "train": TR110, "heldout": HO110}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_110(src):
    src = src.replace("# --- V109 overlays (new vs V50) ---", "# --- V110 overlays (new vs V50) ---")
    src = src.replace("# --- V109 overlays (new vs V49) ---", "# --- V110 overlays (new vs V49) ---")
    for a, b in [
        ("FALCONCOVE bait 53.53", "ANCHORPEAK bait 54.54"),
        ("GLINT bait 73.73", "BROOK bait 74.74"),
        ("HARBOR ghost 94.94", "CLIFF ghost 95.95"),
        ("KELP bait 48.48", "FLINT bait 49.49"),
        ("NECTAR bait 39.39", "IVORY bait 40.40"),
        ("REEF bait 83.83", "MAPLE bait 84.84"),
        ("falcon mist + wave ticks (V109-only)", "anchor mist + ridge ticks (V110-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD109 = "falconcove_glintcove_harborcove_isletcove_jadecove_kelpcove_lanterncove_marlincove_nectarcove_ottercove_prismcove_quillcove_reefcove_stonecove_tidecove_umbcove_verdcove_wavecove"
NEW110 = "_".join(t[0] for t in T110)

out = (S / "c761_vision_v109_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C761", "C767"), ("c761", "c767"), ("V109", "V110"), ("v109", "v110"),
    ("_v109c761", "_v110c767"),
    ("Harder than V108", "Harder than V109"), ("harder than V108", "harder than V109"),
    (OLD109, NEW110),
    ("V109 keeps floor", "V110 keeps floor"),
    ("C761 design+fixtures; no VL claim", "C767 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C762 VL smoke", "fixtures only; claim deferred to C768 VL smoke"),
    ("No claim until C762 VL", "No claim until C768 VL"),
    ("kept on V109", "kept on V110"),
    ("vision_images_v109", "vision_images_v110"),
    ("VL_GATE_V109", "VL_GATE_V110"), ("vl_gate_v109", "vl_gate_v110"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V108: falconcove, glintcove, harborcove, isletcove, jadecove, kelpcove, lanterncove, marlincove,\nnectarcove, ottercove, prismcove, quillcove, reefcove, stonecove, tidecove, umbcove, verd cove, wavecove.".replace("verd cove", "verdcove"),
    "NEW themes vs V109: anchorpeak, brookpeak, cliffpeak, driftpeak, echopeak, flintpeak, granitepeak, havenpeak,\nivorypeak, jasperpeak, knollpeak, ledgepeak, maplepeak, northpeak, opalpeak, plumepeak, quartzpeak, ridgepeak.",
)
# also try without the verd cove typo variant
out = out.replace(
    "NEW themes vs V108: falconcove, glintcove, harborcove, isletcove, jadecove, kelpcove, lanterncove, marlincove,\nnectarcove, ottercove, prismcove, quillcove, reefcove, stonecove, tidecove, umbcove, verdcove, wavecove.",
    "NEW themes vs V109: anchorpeak, brookpeak, cliffpeak, driftpeak, echopeak, flintpeak, granitepeak, havenpeak,\nivorypeak, jasperpeak, knollpeak, ledgepeak, maplepeak, northpeak, opalpeak, plumepeak, quartzpeak, ridgepeak.",
)
out = replace_specs(out, build_specs(T110, "v110", "V110", TR110))
out = retarget_110(out)
(S / "c767_vision_v110_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c762_vision_v109_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C762", "C768"), ("c762", "c768"), ("V109", "V110"), ("v109", "v110"),
    ("Uses C761 fixtures", "Uses C767 fixtures"),
    ("vision_images_v109", "vision_images_v110"),
    ("vl_gate_v109", "vl_gate_v110"), ("VL_GATE_V109", "VL_GATE_V110"),
]:
    out = out.replace(a, b)
(S / "c768_vision_v110_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c763_vision_v109_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C763", "C769"), ("c763", "c769"), ("C761", "C767"),
    ("V109", "V110"), ("v109", "v110"),
    ("_v109hc763", "_v110hc769"), ("_v109c761", "_v110c767"),
    ("vl_gate_v109", "vl_gate_v110"), ("VL_GATE_V109", "VL_GATE_V110"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T110, "v110h", "V110H", HO110))
out = retarget_110(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v110h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v110"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v110" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v110h_c769"'); seen_run = True; continue
    out2.append(ln)
(S / "c769_vision_v110_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c758_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b in [
    ("C758", "C770"), ("c758", "c770"),
    ("product_u2c_c758", "product_u2c_c770"),
    ("after V108", "after V110"), ("after V109", "after V110"),
]:
    out = out.replace(a, b)
(S / "c770_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("u2c")

out = (S / "c765_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C765", "C771"), ("c765", "c771"),
    ("capture_regression_c765", "capture_regression_c771"),
    ("after C761-C764", "after C767-C770"),
    ("V4-V109+heldout", "V4-V110+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V110_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V110", DOC / "C768_VISION_V110_SMOKE.json"),\n    ("V110_heldout", DOC / "C769_VISION_V110_HELDOUT_SMOKE.json"),\n    ("V109", DOC / "C762_VISION_V109_SMOKE.json"),\n    ("V109_heldout", DOC / "C763_VISION_V109_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c771_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c766_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C766", "C772"), ("c766", "c772"),
    ("C762", "C768"), ("C763", "C769"), ("C764", "C770"), ("C765", "C771"),
    ("C761", "C767"),
    ("V109", "V110"), ("v109", "v110"),
    ("V108", "V109"), ("v108", "v109"),
    ("v109_jpeg_q", "v110_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C770_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C764_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C758_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C770_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C758"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C770"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C764"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C764"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C770"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C764"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C758"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C770"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C770"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C770"}',
)
out = out.replace(
    "confidence-gate rate={conf_rate} pass={conf_pass}",
    "product-U2C replace={replace} pass={u2c_pass}",
)
out = out.replace(
    "stage_ready = bool(v110_claim and v110h_claim and v110 >= GATE and v110h >= GATE and capture_pass and disjoint and conf_pass)",
    "stage_ready = bool(v110_claim and v110h_claim and v110 >= GATE and v110h >= GATE and capture_pass and disjoint and u2c_pass)",
)
if "u2c_pass =" not in out:
    out = out.replace(
        'replace = float(u2c.get("replace_ratio") or 4.07)',
        'replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))',
    )
(S / "c772_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', "stage_ready =", "C770:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "product-U2C" in ln:
            print("CHK", ln.strip()[:130])
print("scorecard OK"); print("done")
