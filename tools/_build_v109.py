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

T109 = [
    ["falconcove","recv","paid_total","FALCONCOVE GRAIN RECV","RECV","x"],
    ["glintcove","wh","qty_sum","WH GLINTCOVE BIN","RECV","x"],
    ["harborcove","refund","refund_done","HARBORCOVE PATCH REFUND","DONE","x"],
    ["isletcove","tax","tax_base_paid","ISLETCOVE TAX SLIP","TAX","x"],
    ["jade cove".replace(" ",""),"pay","payroll_active","JADECOVE PAYROLL","PAY","x"],
    ["kelpcove","ship","ship_ok","KELPCOVE SHIP DOCK","SHIP","x"],
    ["lanterncove","sla","sla_ok_hours","LANTERNCOVE SLA CARD","SLA","x"],
    ["marlincove","exp","exp_sum","MARLINCOVE EXPENSE","EXP","x"],
    ["nectarcove","po","po_open","NECTARCOVE PO SHEET","PO","x"],
    ["ottercove","order","order_paid","OTTERCOVE ORDER","ORD","x"],
    ["prismcove","dup","dup_mark","PRISMCOVE DUP MARK","DUP","x"],
    ["quillcove","zero","zero_check","QUILLCOVE AIR ZERO","ZERO","x"],
    ["reefcove","ledger","ledger_net","REEFCOVE LEDGER","LED","x"],
    ["stonecove","ui","ui_ok","STONECOVE UI SCAN","UI","x"],
    ["tide cove".replace(" ",""),"stack","stack_count","TIDECOVE STACK","STK","x"],
    ["umbcove","fax","fax_pages","UMBCOVE FAX","FAX","x"],
    ["verdcove","glare","glare_ok","VERDCOVE GLARE","GLR","x"],
    ["wavecove","tab","tab_index","WAVECOVE TAB INDEX","TAB","x"],
]
T109[4] = ["jadecove","pay","payroll_active","JADECOVE PAYROLL","PAY","x"]
T109[14] = ["tidecove","stack","stack_count","TIDECOVE STACK","STK","x"]
TR109 = [
    [569.0, 585.5, 378.0],[495, 535, 351],[492.0, 521.25, 358.0],[623.0, 641.0, 448.0],
    [686.0, 710.0, 418.0],[444, 460, 376],[340.0, 380.0, 220.0],[534.0, 565.75, 382.0],
    [568.0, 551.0, 391.0],[601.0, 589.0, 379.0],[1,1,0],[0,0,0],
    [667.0, 688.5, 404.0],[1,0,0],[240, 232, 210],[258, 242, 233],[1,0,0],[284, 260, 230],
]
HO109 = [
    [438.0, 450.75, 331.0],[393, 433, 313],[396.0, 409.5, 319.0],[511.0, 527.0, 360.0],
    [552.0, 568.0, 355.0],[346, 360, 324],[240.0, 280.0, 180.0],[422.0, 443.75, 331.0],
    [442.0, 430.0, 334.0],[469.0, 455.0, 326.0],[1,1,0],[0,0,0],
    [504.0, 519.5, 341.0],[1,0,0],[216, 213, 208],[232, 226, 214],[1,0,0],[242, 236, 215],
]
(ROOT / "tools/_v109_themes.json").write_text(json.dumps({"themes": T109, "train": TR109, "heldout": HO109}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_109(src):
    src = src.replace("# --- V108 overlays (new vs V50) ---", "# --- V109 overlays (new vs V50) ---")
    src = src.replace("# --- V108 overlays (new vs V49) ---", "# --- V109 overlays (new vs V49) ---")
    for a, b in [
        ("MOSSRIDGE bait 52.52", "FALCONCOVE bait 53.53"),
        ("NIGHT bait 72.72", "GLINT bait 73.73"),
        ("OAT ghost 93.93", "HARBOR ghost 94.94"),
        ("ROSE bait 47.47", "KELP bait 48.48"),
        ("UMBRA bait 38.38", "NECTAR bait 39.39"),
        ("ZIRCON bait 82.82", "REEF bait 83.83"),
        ("moss mist + elder ticks (V108-only)", "falcon mist + wave ticks (V109-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD108 = "mossridge_nightridge_oatridge_pineridge_quartridge_roseridge_spruceridge_tidalridge_umbraridge_vineridge_westridge_yewridge_zirconridge_alderridge_basaltridge_coralridge_duneridge_elderridge"
NEW109 = "_".join(t[0] for t in T109)

out = (S / "c755_vision_v108_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C755", "C761"), ("c755", "c761"), ("V108", "V109"), ("v108", "v109"),
    ("_v108c755", "_v109c761"),
    ("Harder than V107", "Harder than V108"), ("harder than V107", "harder than V108"),
    (OLD108, NEW109),
    ("V108 keeps floor", "V109 keeps floor"),
    ("C755 design+fixtures; no VL claim", "C761 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C756 VL smoke", "fixtures only; claim deferred to C762 VL smoke"),
    ("No claim until C756 VL", "No claim until C762 VL"),
    ("kept on V108", "kept on V109"),
    ("vision_images_v108", "vision_images_v109"),
    ("VL_GATE_V108", "VL_GATE_V109"), ("vl_gate_v108", "vl_gate_v109"),
]:
    out = out.replace(a, b)
out = out.replace(
    "NEW themes vs V107: mossridge, nightridge, oatridge, pineridge, quartridge, roseridge, spruceridge, tidalridge,\numbraridge, vineridge, westridge, yewridge, zirconridge, alderridge, basaltridge, coralridge, duneridge, elderridge.",
    "NEW themes vs V108: falconcove, glintcove, harborcove, isletcove, jadecove, kelpcove, lanterncove, marlincove,\nnectarcove, ottercove, prismcove, quillcove, reefcove, stonecove, tidecove, umbcove, verd cove, wavecove.".replace("verd cove", "verdcove"),
)
out = replace_specs(out, build_specs(T109, "v109", "V109", TR109))
out = retarget_109(out)
(S / "c761_vision_v109_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c756_vision_v108_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C756", "C762"), ("c756", "c762"), ("V108", "V109"), ("v108", "v109"),
    ("Uses C755 fixtures", "Uses C761 fixtures"),
    ("vision_images_v108", "vision_images_v109"),
    ("vl_gate_v108", "vl_gate_v109"), ("VL_GATE_V108", "VL_GATE_V109"),
]:
    out = out.replace(a, b)
(S / "c762_vision_v109_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c757_vision_v108_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C757", "C763"), ("c757", "c763"), ("C755", "C761"),
    ("V108", "V109"), ("v108", "v109"),
    ("_v108hc757", "_v109hc763"), ("_v108c755", "_v109c761"),
    ("vl_gate_v108", "vl_gate_v109"), ("VL_GATE_V108", "VL_GATE_V109"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T109, "v109h", "V109H", HO109))
out = retarget_109(out)
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v109h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v109"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v109" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v109h_c763"'); seen_run = True; continue
    out2.append(ln)
(S / "c763_vision_v109_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

out = (S / "c752_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b in [
    ("C752", "C764"), ("c752", "c764"),
    ("conf_gate_stretch_c752", "conf_gate_stretch_c764"),
    ("after V107", "after V109"), ("after V108", "after V109"),
    ("cg55_", "cg56_"), ("cg54_", "cg56_"),
]:
    out = out.replace(a, b)
(S / "c764_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence")

out = (S / "c759_capture_office_regression.py").read_text(encoding="utf-8")
for a, b in [
    ("C759", "C765"), ("c759", "c765"),
    ("capture_regression_c759", "capture_regression_c765"),
    ("after C755-C758", "after C761-C764"),
    ("V4-V108+heldout", "V4-V109+heldout"),
]:
    out = out.replace(a, b)
if "VISION_V109_SMOKE" not in out:
    out = out.replace(
        "SMOKE_POINTERS = [",
        'SMOKE_POINTERS = [\n    ("V109", DOC / "C762_VISION_V109_SMOKE.json"),\n    ("V109_heldout", DOC / "C763_VISION_V109_HELDOUT_SMOKE.json"),\n    ("V108", DOC / "C756_VISION_V108_SMOKE.json"),\n    ("V108_heldout", DOC / "C757_VISION_V108_HELDOUT_SMOKE.json"),',
        1,
    )
(S / "c765_capture_office_regression.py").write_text(out, encoding="utf-8")
print("regression")

out = (S / "c760_scorecard_and_stage.py").read_text(encoding="utf-8")
for a, b in [
    ("C760", "C766"), ("c760", "c766"),
    ("C756", "C762"), ("C757", "C763"), ("C758", "C764"), ("C759", "C765"),
    ("C755", "C761"),
    ("V108", "V109"), ("v108", "v109"),
    ("V107", "V108"), ("v107", "v108"),
    ("v108_jpeg_q", "v109_jpeg_q"),
]:
    out = out.replace(a, b)
out = out.replace(
    'c656 = load("docs/r50/C752_CONFIDENCE_GATE_STRETCH.json") or {}',
    'c656 = load("docs/r50/C764_CONFIDENCE_GATE_STRETCH.json") or {}',
)
out = out.replace(
    'c650 = load("docs/r50/C764_PRODUCT_U2C_COST.json") or {}',
    'c650 = load("docs/r50/C758_PRODUCT_U2C_COST.json") or {}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C764"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C758"}',
)
out = out.replace(
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C758"}',
    'u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C758"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C752"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C764"}',
)
out = out.replace(
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C764"}',
    '"confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C764"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C758"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C758"}',
)
out = out.replace(
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C764"}',
    '"product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C758"}',
)
out = out.replace(
    "product-U2C replace={replace} pass={u2c_pass}",
    "confidence-gate rate={conf_rate} pass={conf_pass}",
)
out = out.replace(
    "stage_ready = bool(v109_claim and v109h_claim and v109 >= GATE and v109h >= GATE and capture_pass and disjoint and u2c_pass)",
    "stage_ready = bool(v109_claim and v109h_claim and v109 >= GATE and v109h >= GATE and capture_pass and disjoint and conf_pass)",
)
(S / "c766_scorecard_and_stage.py").write_text(out, encoding="utf-8")
for ln in out.splitlines():
    if any(x in ln for x in ("c656 =", "c650 =", '"confidence_gate"', "stage_ready =", "C764:")):
        if "load" in ln or "source" in ln or "stage_ready" in ln or "confidence-gate" in ln:
            print("CHK", ln.strip()[:130])
print("scorecard OK"); print("done")
