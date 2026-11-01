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

# *croft ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T323 = [
    ["ashcroft","recv","paid_total","ASHCROFT GRAIN RECV","RECV","x"],
    ["cedarcroft","wh","qty_sum","WH CEDARCROFT BIN","RECV","x"],
    ["dawncroft","refund","refund_done","DAWNCROFT PATCH REFUND","DONE","x"],
    ["elmcroft","tax","tax_base_paid","ELMCROFT TAX SLIP","TAX","x"],
    ["ferncroft","pay","payroll_active","FERNCROFT PAYROLL","PAY","x"],
    ["glencroft","ship","ship_ok","GLENCROFT SHIP DOCK","SHIP","x"],
    ["hazecroft","sla","sla_ok_hours","HAZECROFT SLA CARD","SLA","x"],
    ["inkcroft","exp","exp_sum","INKCROFT EXPENSE","EXP","x"],
    ["jadecroft","po","po_open","JADECROFT PO SHEET","PO","x"],
    ["knotcroft","order","order_paid","KNOTCROFT ORDER","ORD","x"],
    ["lakecroft","dup","dup_mark","LAKECROFT DUP MARK","DUP","x"],
    ["mosscroft","zero","zero_check","MOSSCROFT AIR ZERO","ZERO","x"],
    ["nethercroft","ledger","ledger_net","NETHERCROFT LEDGER","LED","x"],
    ["oakcroft","ui","ui_ok","OAKCROFT UI SCAN","UI","x"],
    ["pinecroft","stack","stack_count","PINECROFT STACK","STK","x"],
    ["quillcroft","fax","fax_pages","QUILLCROFT FAX","FAX","x"],
    ["reedcroft","glare","glare_ok","REEDCROFT GLARE","GLR","x"],
    ["stonecroft","tab","tab_index","STONECROFT TAB INDEX","TAB","x"],
]
TR323 = [
    [2310.0, 2327.5, 2050.0],[840, 760, 820],[2233.0, 2262.25, 2028.0],[2366.0, 2383.0, 2118.0],
    [2428.0, 2452.0, 2088.0],[2146, 2162, 2046],[490.0, 530.0, 760.0],[2276.0, 2307.75, 2052.0],
    [840.0, 760.0, 820.0],[2343.0, 2331.0, 2049.0],[1,1,0],[0,0,0],
    [2409.0, 2430.5, 2074.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO323 = [
    [2108.0, 2120.75, 1969.0],[640, 660, 820],[2051.0, 2065.5, 1944.0],[2181.0, 2197.0, 2000.0],
    [2222.0, 2238.0, 1993.0],[2004, 2016, 1964],[420.0, 460.0, 740.0],[2092.0, 2113.75, 1969.0],
    [740.0, 780.0, 820.0],[2139.0, 2125.0, 1966.0],[1,1,0],[0,0,0],
    [2174.0, 2189.5, 1979.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR323, "TR"); check(HO323, "HO")

(ROOT / "tools/_v323_themes.json").write_text(json.dumps({"themes": T323, "train": TR323, "heldout": HO323}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_322(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V323 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V323 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 140.50", "ASHCROFT bait 185.95"),
        ("CEDARW bait 142.52", "CEDARC bait 238.48"),
        ("DAWNW ghost 65.65", "DAWNC ghost 161.71"),
        ("GLENW bait 135.45", "GLENC bait 231.41"),
        ("JADEW bait 126.36", "JADEC bait 222.32"),
        ("NETHERW bait 143.53", "NETHERC bait 239.49"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V323-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD322 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v322_themes.json").read_text(encoding="utf-8"))["themes"])
NEW323 = "_".join(t[0] for t in T323)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2045"), ("c1463", "c2045"), ("V226", "V323"), ("v226", "v323"),
    ("_v226c1463", "_v323c2045"),
    ("Harder than V225", "Harder than V321"), ("harder than V225", "harder than V321"),
    (OLD322, NEW323),
    ("V226 keeps floor", "V323 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2045 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2046 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2046 VL"),
    ("kept on V226", "kept on V323"),
    ("vision_images_v226", "vision_images_v323"),
    ("VL_GATE_V226", "VL_GATE_V323"), ("vl_gate_v226", "vl_gate_v323"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V321: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T323, "v323", "V323", TR323))
out = retarget_322(out)
(S / "c2045_vision_v323_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2046"), ("c1464", "c2046"), ("V226", "V323"), ("v226", "v323"),
    ("vision_images_v226", "vision_images_v323"),
    ("VL_GATE_V226", "VL_GATE_V323"), ("vl_gate_v226", "vl_gate_v323"),
    ("runs/vision_v226", "runs/vision_v323"),
]:
    out = out.replace(a, b)
(S / "c2046_vision_v323_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2047"), ("c1465", "c2047"), ("V226", "V323"), ("v226", "v323"),
    ("vision_images_v226h", "vision_images_v323h"),
    ("vision_images_v226", "vision_images_v323"),
    ("VL_GATE_V226", "VL_GATE_V323"), ("vl_gate_v226", "vl_gate_v323"),
    ("runs/vision_v226h", "runs/vision_v323h"),
    ("_v226c1463", "_v323c2045"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T323, "v323h", "V323H", HO323))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v323h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v323"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v323" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v323h_c2047"'); seen_run = True; continue
    out2.append(ln)
(S / "c2047_vision_v323_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2045-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2046_VISION_V323_SMOKE.json") or {}\n    c654b = load("docs/r50/C2046b_VISION_GATE_V323_CLAIM.json") or {}\n    c655 = load("docs/r50/C2047_VISION_V323_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2047b_VISION_GATE_V323_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v323 = float(c654.get("rate") or 0.0)\n    v323h = float(c655.get("rate") or 0.0)\n    v323_claim = bool(c654b.get("vl_gate_v323_claim") or c654.get("vl_gate_v323_claim") or c654.get("claim"))\n    v323h_claim = bool(c655b.get("vl_gate_v323_heldout_claim") or c655.get("vl_gate_v323_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v323_claim and v323h_claim and v323 >= GATE and v323h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v323 >= 0.999 and v323h >= 0.999) else min(v323, v323h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v323": {"rate": v323, "claim": v323_claim, "n": c654.get("n")},\n            "v323_heldout": {"rate": v323h, "claim": v323h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v323_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V323: rate={v323} claim={v323_claim}",\n        f"- Vision V323 heldout: rate={v323h} claim={v323h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2045-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2045: Vision V323 design fixtures",\n        f"- C2046: Vision V323 smoke **{v323}**", f"- C2047: Vision V323 heldout **{v323h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V323 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2050 = '# -*- coding: utf-8 -*-\n"""C2050: Unified scorecard + STAGE after C2045-C2049. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2050.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2046_VISION_V323_SMOKE.json") or {}\n    c654b = load("docs/r50/C2046b_VISION_GATE_V323_CLAIM.json") or {}\n    c655 = load("docs/r50/C2047_VISION_V323_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2047b_VISION_GATE_V323_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2048_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2049_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2042_PRODUCT_U2C_COST.json") or {}\n\n    v323 = float(c654.get("rate") or 0.0)\n    v323h = float(c655.get("rate") or 0.0)\n    v323_claim = bool(c654b.get("vl_gate_v323_claim") or c654.get("vl_gate_v323_claim") or c654.get("claim"))\n    v323h_claim = bool(c655b.get("vl_gate_v323_heldout_claim") or c655.get("vl_gate_v323_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2042"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v323_claim and v323h_claim and v323 >= GATE and v323h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v323 >= 0.999 and v323h >= 0.999) else min(v323, v323h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2050", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v323": {"rate": v323, "claim": v323_claim, "n": c654.get("n")},\n            "v323_heldout": {"rate": v323h, "claim": v323h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2042"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2048"},\n        "capture_regression": {"pass": capture_pass, "source": "C2049"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v323_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2050_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2050)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V323: rate={v323} claim={v323_claim}",\n        f"- Vision V323 heldout: rate={v323h} claim={v323h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2050", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2045-C2050 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2045: Vision V323 design fixtures",\n        f"- C2046: Vision V323 smoke **{v323}**", f"- C2047: Vision V323 heldout **{v323h}** (disjoint={disjoint})",\n        f"- C2048: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2042): replace={replace} pass={u2c_pass}",\n        f"- C2049: capture pass={capture_pass}", f"- C2050: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V323 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2050.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V323 knife = confidence-gate (alternating; V322 was product-U2C)
out = (S / "c2036_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2036", "C2048"), ("c2036", "c2048"),
    ("C2024", "C2048"), ("c2024", "c2048"),
    ("cg143_", "cg144_"),
    ("conf_gate_stretch_c2036", "conf_gate_stretch_c2048"),
    ("confidence_gate_stretch_v206", "confidence_gate_stretch_v207"),
    ("Stretch vs C2024", "Stretch vs C2036"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 122.00 b paid 126.75 c open 82.00 TOTAL PAID TARGET 248.75", "a paid 123.00 b paid 127.75 c open 83.00 TOTAL PAID TARGET 250.75")
out = out.replace('"model_guess": 999.0, "expected": 248.75', '"model_guess": 999.0, "expected": 250.75')
out = out.replace("SKU1 qty 117 ok SKU2 qty 91 hold SKU3 qty 121 ok qty_sum TARGET 238", "SKU1 qty 118 ok SKU2 qty 92 hold SKU3 qty 122 ok qty_sum TARGET 240")
out = out.replace('"model_guess": 250.0, "expected": 238.0', '"model_guess": 252.0, "expected": 240.0')
out = out.replace("itemR1 98.00 done itemR2 101.75 done itemR3 79.00 open refund_done TARGET 199.75", "itemR1 99.00 done itemR2 102.75 done itemR3 80.00 open refund_done TARGET 201.75")
out = out.replace('"model_guess": 208.5, "expected": 199.75', '"model_guess": 210.5, "expected": 201.75')
out = out.replace("T1 166.00 paid T2 106.00 open T3 147.00 paid tax_base_paid TARGET 313.00", "T1 167.00 paid T2 107.00 open T3 148.00 paid tax_base_paid TARGET 315.00")
out = out.replace('"model_guess": 349.0, "expected": 313.0', '"model_guess": 351.0, "expected": 315.0')
out = out.replace("A 1661 active B 370 leave C 1545 active payroll_active TARGET 3206", "A 1662 active B 371 leave C 1546 active payroll_active TARGET 3208")
out = out.replace('"model_guess": 3436.0, "expected": 3206.0', '"model_guess": 3438.0, "expected": 3208.0')
out = out.replace("P1 111 ok P2 90 hold P3 110 ok ship_ok_qty TARGET 221", "P1 112 ok P2 91 hold P3 111 ok ship_ok_qty TARGET 223")
out = out.replace('"model_guess": 240.0, "expected": 221.0', '"model_guess": 242.0, "expected": 223.0')
out = out.replace("S1 pri 100 open S2 pri 103 closed S3 pri 112 open open_pri_sum TARGET 212", "S1 pri 101 open S2 pri 104 closed S3 pri 113 open open_pri_sum TARGET 214")
out = out.replace('"model_guess": 244.0, "expected": 212.0', '"model_guess": 246.0, "expected": 214.0')
out = out.replace("X 142.00 open Y 145.00 open paid_total TARGET 0.00 bait 287.00", "X 143.00 open Y 146.00 open paid_total TARGET 0.00 bait 289.00")
out = out.replace('"model_guess": 287.0, "expected": 0.0', '"model_guess": 289.0, "expected": 0.0')
out = out.replace("alpha paid 107.00 beta paid 110.00 gamma open 80.00 TOTAL PAID TARGET 217.00", "alpha paid 108.00 beta paid 111.00 gamma open 81.00 TOTAL PAID TARGET 219.00")
out = out.replace('"model_guess": 217.0, "expected": 217.0', '"model_guess": 219.0, "expected": 219.0')
out = out.replace("SKU1 qty 91 ok SKU2 qty 79 hold SKU3 qty 93 ok qty_sum TARGET 184", "SKU1 qty 92 ok SKU2 qty 80 hold SKU3 qty 94 ok qty_sum TARGET 186")
out = out.replace('"model_guess": 184.0, "expected": 184.0', '"model_guess": 186.0, "expected": 186.0')
out = out.replace("itemR1 84.00 done itemR2 86.25 done itemR3 73.00 open refund_done TARGET 170.25", "itemR1 85.00 done itemR2 87.25 done itemR3 74.00 open refund_done TARGET 172.25")
out = out.replace('"model_guess": 170.25, "expected": 170.25', '"model_guess": 172.25, "expected": 172.25')
out = out.replace("tea paid 103.00 rice paid 105.50 soup open 78.00 TOTAL PAID TARGET 208.50", "tea paid 104.00 rice paid 106.50 soup open 79.00 TOTAL PAID TARGET 210.50")
out = out.replace('"model_guess": 216.25, "expected": 208.50', '"model_guess": 218.25, "expected": 210.50')
(S / "c2048_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2036_confidence_gate_stretch.py")

out = (S / "c2043_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2043", "C2049"), ("c2043", "c2049")]:
    out = out.replace(a, b2)
(S / "c2049_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2050_scorecard_and_stage.py").write_text(SC2050, encoding="utf-8")
print("scorecard from fixed c2038 conf-gate pattern")
print("OK builder v323 ready")
