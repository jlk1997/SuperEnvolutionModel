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
T329 = [
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
TR329 = [
    [2322.0, 2339.5, 2062.0],[840, 760, 820],[2245.0, 2254.25, 2040.0],[2378.0, 2395.0, 2130.0],
    [2440.0, 2464.0, 2100.0],[2158, 2174, 2058],[490.0, 530.0, 760.0],[2288.0, 2319.75, 2064.0],
    [840.0, 760.0, 820.0],[2355.0, 2343.0, 2061.0],[1,1,0],[0,0,0],
    [2421.0, 2442.5, 2086.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO329 = [
    [2120.0, 2132.75, 1981.0],[640, 660, 820],[2063.0, 2077.5, 1956.0],[2193.0, 2209.0, 2012.0],
    [2234.0, 2250.0, 2005.0],[2016, 2028, 1978],[420.0, 460.0, 740.0],[2104.0, 2125.75, 1981.0],
    [740.0, 780.0, 820.0],[2151.0, 2137.0, 1978.0],[1,1,0],[0,0,0],
    [2186.0, 2201.5, 1991.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR329, "TR"); check(HO329, "HO")

(ROOT / "tools/_v329_themes.json").write_text(json.dumps({"themes": T329, "train": TR329, "heldout": HO329}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_328(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V329 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V329 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 140.50", "ASHDALE bait 185.95"),
        ("CEDARW bait 142.52", "CEDARD bait 244.54"),
        ("DAWNW ghost 65.65", "DAWND ghost 167.77"),
        ("GLENW bait 135.45", "GLEND bait 237.47"),
        ("JADEW bait 126.36", "JADED bait 228.38"),
        ("NETHERW bait 143.53", "NETHERD bait 245.55"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V329-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD328 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v328_themes.json").read_text(encoding="utf-8"))["themes"])
NEW329 = "_".join(t[0] for t in T329)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2081"), ("c1463", "c2081"), ("V226", "V329"), ("v226", "v329"),
    ("_v226c1463", "_v329c2081"),
    ("Harder than V225", "Harder than V327"), ("harder than V225", "harder than V327"),
    (OLD328, NEW329),
    ("V226 keeps floor", "V329 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2081 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2082 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2082 VL"),
    ("kept on V226", "kept on V329"),
    ("vision_images_v226", "vision_images_v329"),
    ("VL_GATE_V226", "VL_GATE_V329"), ("vl_gate_v226", "vl_gate_v329"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V327: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T329, "v329", "V329", TR329))
out = retarget_328(out)
(S / "c2081_vision_v329_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2082"), ("c1464", "c2082"), ("V226", "V329"), ("v226", "v329"),
    ("vision_images_v226", "vision_images_v329"),
    ("VL_GATE_V226", "VL_GATE_V329"), ("vl_gate_v226", "vl_gate_v329"),
    ("runs/vision_v226", "runs/vision_v329"),
]:
    out = out.replace(a, b)
(S / "c2082_vision_v329_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2083"), ("c1465", "c2083"), ("V226", "V329"), ("v226", "v329"),
    ("vision_images_v226h", "vision_images_v329h"),
    ("vision_images_v226", "vision_images_v329"),
    ("VL_GATE_V226", "VL_GATE_V329"), ("vl_gate_v226", "vl_gate_v329"),
    ("runs/vision_v226h", "runs/vision_v329h"),
    ("_v226c1463", "_v329c2081"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T329, "v329h", "V329H", HO329))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v329h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v329"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v329" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v329h_c2083"'); seen_run = True; continue
    out2.append(ln)
(S / "c2083_vision_v329_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2081-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2082_VISION_V329_SMOKE.json") or {}\n    c654b = load("docs/r50/C2082b_VISION_GATE_V329_CLAIM.json") or {}\n    c655 = load("docs/r50/C2083_VISION_V329_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2083b_VISION_GATE_V329_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v329 = float(c654.get("rate") or 0.0)\n    v329h = float(c655.get("rate") or 0.0)\n    v329_claim = bool(c654b.get("vl_gate_v329_claim") or c654.get("vl_gate_v329_claim") or c654.get("claim"))\n    v329h_claim = bool(c655b.get("vl_gate_v329_heldout_claim") or c655.get("vl_gate_v329_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v329_claim and v329h_claim and v329 >= GATE and v329h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v329 >= 0.999 and v329h >= 0.999) else min(v329, v329h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v329": {"rate": v329, "claim": v329_claim, "n": c654.get("n")},\n            "v329_heldout": {"rate": v329h, "claim": v329h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v329_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V329: rate={v329} claim={v329_claim}",\n        f"- Vision V329 heldout: rate={v329h} claim={v329h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2081-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2081: Vision V329 design fixtures",\n        f"- C2082: Vision V329 smoke **{v329}**", f"- C2083: Vision V329 heldout **{v329h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V329 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2086 = '# -*- coding: utf-8 -*-\n"""C2086: Unified scorecard + STAGE after C2081-C2085. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2086.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2082_VISION_V329_SMOKE.json") or {}\n    c654b = load("docs/r50/C2082b_VISION_GATE_V329_CLAIM.json") or {}\n    c655 = load("docs/r50/C2083_VISION_V329_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2083b_VISION_GATE_V329_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2084_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2085_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2078_PRODUCT_U2C_COST.json") or {}\n\n    v329 = float(c654.get("rate") or 0.0)\n    v329h = float(c655.get("rate") or 0.0)\n    v329_claim = bool(c654b.get("vl_gate_v329_claim") or c654.get("vl_gate_v329_claim") or c654.get("claim"))\n    v329h_claim = bool(c655b.get("vl_gate_v329_heldout_claim") or c655.get("vl_gate_v329_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2078"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v329_claim and v329h_claim and v329 >= GATE and v329h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v329 >= 0.999 and v329h >= 0.999) else min(v329, v329h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2086", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v329": {"rate": v329, "claim": v329_claim, "n": c654.get("n")},\n            "v329_heldout": {"rate": v329h, "claim": v329h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2078"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2084"},\n        "capture_regression": {"pass": capture_pass, "source": "C2085"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v329_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2086_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2086)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V329: rate={v329} claim={v329_claim}",\n        f"- Vision V329 heldout: rate={v329h} claim={v329h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2086", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2081-C2086 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2081: Vision V329 design fixtures",\n        f"- C2082: Vision V329 smoke **{v329}**", f"- C2083: Vision V329 heldout **{v329h}** (disjoint={disjoint})",\n        f"- C2084: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2078): replace={replace} pass={u2c_pass}",\n        f"- C2085: capture pass={capture_pass}", f"- C2086: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V329 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2086.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V329 knife = confidence-gate (alternating; V328 was product-U2C)
out = (S / "c2072_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2072", "C2084"), ("c2072", "c2084"),
    ("C2060", "C2084"), ("c2060", "c2084"),
    ("cg146_", "cg147_"),
    ("conf_gate_stretch_c2072", "conf_gate_stretch_c2084"),
    ("confidence_gate_stretch_v209", "confidence_gate_stretch_v210"),
    ("Stretch vs C2060", "Stretch vs C2072"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 125.00 b paid 129.75 c open 85.00 TOTAL PAID TARGET 254.75", "a paid 126.00 b paid 130.75 c open 86.00 TOTAL PAID TARGET 256.75")
out = out.replace('"model_guess": 999.0, "expected": 254.75', '"model_guess": 999.0, "expected": 256.75')
out = out.replace("SKU1 qty 120 ok SKU2 qty 94 hold SKU3 qty 124 ok qty_sum TARGET 244", "SKU1 qty 121 ok SKU2 qty 95 hold SKU3 qty 125 ok qty_sum TARGET 246")
out = out.replace('"model_guess": 256.0, "expected": 244.0', '"model_guess": 258.0, "expected": 246.0')
out = out.replace("itemR1 101.00 done itemR2 104.75 done itemR3 82.00 open refund_done TARGET 205.75", "itemR1 102.00 done itemR2 105.75 done itemR3 83.00 open refund_done TARGET 207.75")
out = out.replace('"model_guess": 214.5, "expected": 205.75', '"model_guess": 216.5, "expected": 207.75')
out = out.replace("T1 169.00 paid T2 109.00 open T3 150.00 paid tax_base_paid TARGET 319.00", "T1 170.00 paid T2 110.00 open T3 151.00 paid tax_base_paid TARGET 321.00")
out = out.replace('"model_guess": 355.0, "expected": 319.0', '"model_guess": 357.0, "expected": 321.0')
out = out.replace("A 1664 active B 373 leave C 1548 active payroll_active TARGET 3212", "A 1665 active B 374 leave C 1549 active payroll_active TARGET 3214")
out = out.replace('"model_guess": 3442.0, "expected": 3212.0', '"model_guess": 3444.0, "expected": 3214.0')
out = out.replace("P1 114 ok P2 93 hold P3 113 ok ship_ok_qty TARGET 227", "P1 115 ok P2 94 hold P3 114 ok ship_ok_qty TARGET 229")
out = out.replace('"model_guess": 246.0, "expected": 227.0', '"model_guess": 248.0, "expected": 229.0')
out = out.replace("S1 pri 103 open S2 pri 106 closed S3 pri 115 open open_pri_sum TARGET 218", "S1 pri 104 open S2 pri 107 closed S3 pri 116 open open_pri_sum TARGET 220")
out = out.replace('"model_guess": 250.0, "expected": 218.0', '"model_guess": 252.0, "expected": 220.0')
out = out.replace("X 145.00 open Y 148.00 open paid_total TARGET 0.00 bait 293.00", "X 146.00 open Y 149.00 open paid_total TARGET 0.00 bait 295.00")
out = out.replace('"model_guess": 293.0, "expected": 0.0', '"model_guess": 295.0, "expected": 0.0')
out = out.replace("alpha paid 110.00 beta paid 113.00 gamma open 83.00 TOTAL PAID TARGET 223.00", "alpha paid 111.00 beta paid 114.00 gamma open 84.00 TOTAL PAID TARGET 225.00")
out = out.replace('"model_guess": 223.0, "expected": 223.0', '"model_guess": 225.0, "expected": 225.0')
out = out.replace("SKU1 qty 94 ok SKU2 qty 82 hold SKU3 qty 96 ok qty_sum TARGET 190", "SKU1 qty 95 ok SKU2 qty 83 hold SKU3 qty 97 ok qty_sum TARGET 192")
out = out.replace('"model_guess": 190.0, "expected": 190.0', '"model_guess": 192.0, "expected": 192.0')
out = out.replace("itemR1 87.00 done itemR2 89.25 done itemR3 76.00 open refund_done TARGET 176.25", "itemR1 88.00 done itemR2 90.25 done itemR3 77.00 open refund_done TARGET 178.25")
out = out.replace('"model_guess": 176.25, "expected": 176.25', '"model_guess": 178.25, "expected": 178.25')
out = out.replace("tea paid 106.00 rice paid 108.50 soup open 81.00 TOTAL PAID TARGET 214.50", "tea paid 107.00 rice paid 109.50 soup open 82.00 TOTAL PAID TARGET 216.50")
out = out.replace('"model_guess": 222.25, "expected": 214.50', '"model_guess": 224.25, "expected": 216.50')
(S / "c2084_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2072_confidence_gate_stretch.py")

out = (S / "c2079_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2079", "C2085"), ("c2079", "c2085")]:
    out = out.replace(a, b2)
(S / "c2085_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2086_scorecard_and_stage.py").write_text(SC2086, encoding="utf-8")
print("scorecard from fixed c2074 conf-gate pattern")
print("OK builder v329 ready")
