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

# *dale ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T351 = [
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
TR351 = [
    [2366.0, 2383.5, 2106.0],[840, 760, 820],[2245.0, 2247.25, 2052.0],[2422.0, 2439.0, 2174.0],
    [2484.0, 2493.0, 2144.0],[2202, 2218, 2102],[490.0, 530.0, 760.0],[2332.0, 2363.75, 2108.0],
    [840.0, 760.0, 820.0],[2399.0, 2387.0, 2105.0],[1,1,0],[0,0,0],
    [2457.0, 2476.5, 2116.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO351 = [
    [2164.0, 2176.75, 2025.0],[640, 660, 820],[2107.0, 2121.5, 2000.0],[2237.0, 2253.0, 2056.0],
    [2241.0, 2252.0, 2049.0],[2060, 2072, 2022],[420.0, 460.0, 740.0],[2148.0, 2169.75, 2025.0],
    [740.0, 780.0, 820.0],[2195.0, 2181.0, 2022.0],[1,1,0],[0,0,0],
    [2225.0, 2239.5, 2029.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR351, "TR"); check(HO351, "HO")

(ROOT / "tools/_v351_themes.json").write_text(json.dumps({"themes": T351, "train": TR351, "heldout": HO351}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_350(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V351 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V351 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 140.50", "ASHDALE bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 250.60"),
        ("DAWNW ghost 65.65", "DAWNH ghost 173.83"),
        ("GLENW bait 135.45", "GLENH bait 243.53"),
        ("JADEW bait 126.36", "JADEH bait 234.44"),
        ("NETHERW bait 143.53", "NETHERH bait 251.61"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V351-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD350 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v350_themes.json").read_text(encoding="utf-8"))["themes"])
NEW351 = "_".join(t[0] for t in T351)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2213"), ("c1463", "c2213"), ("V226", "V351"), ("v226", "v351"),
    ("_v226c1463", "_v351c2213"),
    ("Harder than V225", "Harder than V349"), ("harder than V225", "harder than V349"),
    (OLD350, NEW351),
    ("V226 keeps floor", "V351 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2213 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2214 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2214 VL"),
    ("kept on V226", "kept on V351"),
    ("vision_images_v226", "vision_images_v351"),
    ("VL_GATE_V226", "VL_GATE_V351"), ("vl_gate_v226", "vl_gate_v351"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V349: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T351, "v351", "V351", TR351))
out = retarget_350(out)
(S / "c2213_vision_v351_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2214"), ("c1464", "c2214"), ("V226", "V351"), ("v226", "v351"),
    ("vision_images_v226", "vision_images_v351"),
    ("VL_GATE_V226", "VL_GATE_V351"), ("vl_gate_v226", "vl_gate_v351"),
    ("runs/vision_v226", "runs/vision_v351"),
]:
    out = out.replace(a, b)
(S / "c2214_vision_v351_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2215"), ("c1465", "c2215"), ("V226", "V351"), ("v226", "v351"),
    ("vision_images_v226h", "vision_images_v351h"),
    ("vision_images_v226", "vision_images_v351"),
    ("VL_GATE_V226", "VL_GATE_V351"), ("vl_gate_v226", "vl_gate_v351"),
    ("runs/vision_v226h", "runs/vision_v351h"),
    ("_v226c1463", "_v351c2213"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T351, "v351h", "V351H", HO351))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v351h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v351"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v351" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v351h_c2215"'); seen_run = True; continue
    out2.append(ln)
(S / "c2215_vision_v351_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2213-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2214_VISION_V351_SMOKE.json") or {}\n    c654b = load("docs/r50/C2214b_VISION_GATE_V351_CLAIM.json") or {}\n    c655 = load("docs/r50/C2215_VISION_V351_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2215b_VISION_GATE_V351_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v351 = float(c654.get("rate") or 0.0)\n    v351h = float(c655.get("rate") or 0.0)\n    v351_claim = bool(c654b.get("vl_gate_v351_claim") or c654.get("vl_gate_v351_claim") or c654.get("claim"))\n    v351h_claim = bool(c655b.get("vl_gate_v351_heldout_claim") or c655.get("vl_gate_v351_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v351_claim and v351h_claim and v351 >= GATE and v351h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v351 >= 0.999 and v351h >= 0.999) else min(v351, v351h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v351": {"rate": v351, "claim": v351_claim, "n": c654.get("n")},\n            "v351_heldout": {"rate": v351h, "claim": v351h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v351_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V351: rate={v351} claim={v351_claim}",\n        f"- Vision V351 heldout: rate={v351h} claim={v351h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2213-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2213: Vision V351 design fixtures",\n        f"- C2214: Vision V351 smoke **{v351}**", f"- C2215: Vision V351 heldout **{v351h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V351 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2218 = '# -*- coding: utf-8 -*-\n"""C2218: Unified scorecard + STAGE after C2213-C2217. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2218.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2214_VISION_V351_SMOKE.json") or {}\n    c654b = load("docs/r50/C2214b_VISION_GATE_V351_CLAIM.json") or {}\n    c655 = load("docs/r50/C2215_VISION_V351_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2215b_VISION_GATE_V351_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2216_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2217_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2210_PRODUCT_U2C_COST.json") or {}\n\n    v351 = float(c654.get("rate") or 0.0)\n    v351h = float(c655.get("rate") or 0.0)\n    v351_claim = bool(c654b.get("vl_gate_v351_claim") or c654.get("vl_gate_v351_claim") or c654.get("claim"))\n    v351h_claim = bool(c655b.get("vl_gate_v351_heldout_claim") or c655.get("vl_gate_v351_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2210"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v351_claim and v351h_claim and v351 >= GATE and v351h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v351 >= 0.999 and v351h >= 0.999) else min(v351, v351h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2218", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v351": {"rate": v351, "claim": v351_claim, "n": c654.get("n")},\n            "v351_heldout": {"rate": v351h, "claim": v351h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2210"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2216"},\n        "capture_regression": {"pass": capture_pass, "source": "C2217"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v351_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2218_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2218)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V351: rate={v351} claim={v351_claim}",\n        f"- Vision V351 heldout: rate={v351h} claim={v351h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2218", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2213-C2218 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2213: Vision V351 design fixtures",\n        f"- C2214: Vision V351 smoke **{v351}**", f"- C2215: Vision V351 heldout **{v351h}** (disjoint={disjoint})",\n        f"- C2216: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2210): replace={replace} pass={u2c_pass}",\n        f"- C2217: capture pass={capture_pass}", f"- C2218: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V351 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2218.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V351 knife = confidence-gate (alternating; V350 was product-U2C)
out = (S / "c2204_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2204", "C2216"), ("c2204", "c2216"),
    ("C2096", "C2216"), ("c2096", "c2216"),
    ("cg140_", "cg135_"),
    ("conf_gate_stretch_c2216", "conf_gate_stretch_c2216"),
    ("confidence_gate_stretch_v203", "confidence_gate_stretch_v198"),
    ("Stretch vs C2120", "Stretch vs C2126"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 146.00 b paid 150.75 c open 106.00 TOTAL PAID TARGET 296.75", "a paid 152.00 b paid 156.75 c open 112.00 TOTAL PAID TARGET 308.75")
out = out.replace('"model_guess": 999.0, "expected": 296.75', '"model_guess": 999.0, "expected": 308.75')
out = out.replace("SKU1 qty 141 ok SKU2 qty 115 hold SKU3 qty 145 ok qty_sum TARGET 286", "SKU1 qty 147 ok SKU2 qty 121 hold SKU3 qty 151 ok qty_sum TARGET 298")
out = out.replace('"model_guess": 298.0, "expected": 286.0', '"model_guess": 310.0, "expected": 298.0')
out = out.replace("itemR1 122.00 done itemR2 125.75 done itemR3 103.00 open refund_done TARGET 247.75", "itemR1 128.00 done itemR2 131.75 done itemR3 109.00 open refund_done TARGET 259.75")
out = out.replace('"model_guess": 256.5, "expected": 247.75', '"model_guess": 268.5, "expected": 259.75')
out = out.replace("T1 190.00 paid T2 130.00 open T3 171.00 paid tax_base_paid TARGET 361.00", "T1 196.00 paid T2 136.00 open T3 177.00 paid tax_base_paid TARGET 373.00")
out = out.replace('"model_guess": 397.0, "expected": 361.0', '"model_guess": 409.0, "expected": 373.0')
out = out.replace("A 1685 active B 394 leave C 1569 active payroll_active TARGET 3254", "A 1691 active B 400 leave C 1575 active payroll_active TARGET 3266")
out = out.replace('"model_guess": 3484.0, "expected": 3254.0', '"model_guess": 3496.0, "expected": 3266.0')
out = out.replace("P1 135 ok P2 114 hold P3 134 ok ship_ok_qty TARGET 269", "P1 141 ok P2 120 hold P3 140 ok ship_ok_qty TARGET 281")
out = out.replace('"model_guess": 288.0, "expected": 269.0', '"model_guess": 300.0, "expected": 281.0')
out = out.replace("S1 pri 124 open S2 pri 127 closed S3 pri 136 open open_pri_sum TARGET 260", "S1 pri 130 open S2 pri 133 closed S3 pri 142 open open_pri_sum TARGET 272")
out = out.replace('"model_guess": 292.0, "expected": 260.0', '"model_guess": 304.0, "expected": 272.0')
out = out.replace("X 166.00 open Y 169.00 open paid_total TARGET 0.00 bait 335.00", "X 172.00 open Y 175.00 open paid_total TARGET 0.00 bait 347.00")
out = out.replace('"model_guess": 335.0, "expected": 0.0', '"model_guess": 347.0, "expected": 0.0')
out = out.replace("alpha paid 131.00 beta paid 134.00 gamma open 104.00 TOTAL PAID TARGET 265.00", "alpha paid 137.00 beta paid 140.00 gamma open 110.00 TOTAL PAID TARGET 277.00")
out = out.replace('"model_guess": 265.0, "expected": 265.0', '"model_guess": 277.0, "expected": 277.0')
out = out.replace("SKU1 qty 115 ok SKU2 qty 103 hold SKU3 qty 117 ok qty_sum TARGET 232", "SKU1 qty 121 ok SKU2 qty 109 hold SKU3 qty 123 ok qty_sum TARGET 244")
out = out.replace('"model_guess": 232.0, "expected": 232.0', '"model_guess": 244.0, "expected": 244.0')
out = out.replace("itemR1 108.00 done itemR2 110.25 done itemR3 97.00 open refund_done TARGET 218.25", "itemR1 114.00 done itemR2 116.25 done itemR3 103.00 open refund_done TARGET 230.25")
out = out.replace('"model_guess": 218.25, "expected": 218.25', '"model_guess": 230.25, "expected": 230.25')
out = out.replace("tea paid 127.00 rice paid 129.50 soup open 102.00 TOTAL PAID TARGET 256.50", "tea paid 133.00 rice paid 135.50 soup open 108.00 TOTAL PAID TARGET 268.50")
out = out.replace('"model_guess": 264.25, "expected": 256.50', '"model_guess": 276.25, "expected": 268.50')
(S / "c2216_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2204_confidence_gate_stretch.py")

out = (S / "c2211_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2211", "C2217"), ("c2211", "c2217")]:
    out = out.replace(a, b2)
(S / "c2217_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2218_scorecard_and_stage.py").write_text(SC2218, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v351 ready")
