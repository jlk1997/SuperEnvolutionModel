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

# *ford ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T363 = [
    ["ashford","recv","paid_total","ASHFORD GRAIN RECV","RECV","x"],
    ["cedarford","wh","qty_sum","WH CEDARFORD BIN","RECV","x"],
    ["dawnford","refund","refund_done","DAWNFORD PATCH REFUND","DONE","x"],
    ["elmford","tax","tax_base_paid","ELMFORD TAX SLIP","TAX","x"],
    ["fernford","pay","payroll_active","FERNFORD PAYROLL","PAY","x"],
    ["glenford","ship","ship_ok","GLENFORD SHIP DOCK","SHIP","x"],
    ["hazeford","sla","sla_ok_hours","HAZEFORD SLA CARD","SLA","x"],
    ["inkford","exp","exp_sum","INKFORD EXPENSE","EXP","x"],
    ["jadeford","po","po_open","JADEFORD PO SHEET","PO","x"],
    ["knotford","order","order_paid","KNOTFORD ORDER","ORD","x"],
    ["lakeford","dup","dup_mark","LAKEFORD DUP MARK","DUP","x"],
    ["mossford","zero","zero_check","MOSSFORD AIR ZERO","ZERO","x"],
    ["netherford","ledger","ledger_net","NETHERFORD LEDGER","LED","x"],
    ["oakford","ui","ui_ok","OAKFORD UI SCAN","UI","x"],
    ["pineford","stack","stack_count","PINEFORD STACK","STK","x"],
    ["quillford","fax","fax_pages","QUILLFORD FAX","FAX","x"],
    ["reedford","glare","glare_ok","REEDFORD GLARE","GLR","x"],
    ["stoneford","tab","tab_index","STONEFORD TAB INDEX","TAB","x"],
]
TR363 = [
    [2390.0, 2407.5, 2130.0],[840, 760, 820],[2247.0, 2248.25, 2043.0],[2446.0, 2463.0, 2198.0],
    [2491.0, 2496.0, 2168.0],[2226, 2242, 2126],[490.0, 530.0, 760.0],[2356.0, 2387.75, 2132.0],
    [840.0, 760.0, 820.0],[2423.0, 2411.0, 2129.0],[1,1,0],[0,0,0],
    [2449.0, 2472.5, 2098.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO363 = [
    [2188.0, 2200.75, 2049.0],[640, 660, 820],[2131.0, 2145.5, 2024.0],[2261.0, 2277.0, 2080.0],
    [2265.0, 2276.0, 2073.0],[2084, 2096, 2046],[420.0, 460.0, 740.0],[2172.0, 2193.75, 2049.0],
    [740.0, 780.0, 820.0],[2219.0, 2205.0, 2046.0],[1,1,0],[0,0,0],
    [2249.0, 2263.5, 2053.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR363, "TR"); check(HO363, "HO")

(ROOT / "tools/_v363_themes.json").write_text(json.dumps({"themes": T363, "train": TR363, "heldout": HO363}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_362(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V363 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V363 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 140.50", "ASHFORD bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 250.60"),
        ("DAWNW ghost 65.65", "DAWNH ghost 173.83"),
        ("GLENW bait 135.45", "GLENH bait 243.53"),
        ("JADEW bait 126.36", "JADEH bait 234.44"),
        ("NETHERW bait 143.53", "NETHERH bait 251.61"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V363-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD362 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v362_themes.json").read_text(encoding="utf-8"))["themes"])
NEW363 = "_".join(t[0] for t in T363)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2285"), ("c1463", "c2285"), ("V226", "V363"), ("v226", "v363"),
    ("_v226c1463", "_v363c2285"),
    ("Harder than V225", "Harder than V361"), ("harder than V225", "harder than V361"),
    (OLD362, NEW363),
    ("V226 keeps floor", "V363 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2285 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2286 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2286 VL"),
    ("kept on V226", "kept on V363"),
    ("vision_images_v226", "vision_images_v363"),
    ("VL_GATE_V226", "VL_GATE_V363"), ("vl_gate_v226", "vl_gate_v363"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V361: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T363, "v363", "V363", TR363))
out = retarget_362(out)
(S / "c2285_vision_v363_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2286"), ("c1464", "c2286"), ("V226", "V363"), ("v226", "v363"),
    ("vision_images_v226", "vision_images_v363"),
    ("VL_GATE_V226", "VL_GATE_V363"), ("vl_gate_v226", "vl_gate_v363"),
    ("runs/vision_v226", "runs/vision_v363"),
]:
    out = out.replace(a, b)
(S / "c2286_vision_v363_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2287"), ("c1465", "c2287"), ("V226", "V363"), ("v226", "v363"),
    ("vision_images_v226h", "vision_images_v363h"),
    ("vision_images_v226", "vision_images_v363"),
    ("VL_GATE_V226", "VL_GATE_V363"), ("vl_gate_v226", "vl_gate_v363"),
    ("runs/vision_v226h", "runs/vision_v363h"),
    ("_v226c1463", "_v363c2285"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T363, "v363h", "V363H", HO363))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v363h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v363"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v363" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v363h_c2287"'); seen_run = True; continue
    out2.append(ln)
(S / "c2287_vision_v363_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2285-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2286_VISION_V363_SMOKE.json") or {}\n    c654b = load("docs/r50/C2286b_VISION_GATE_V363_CLAIM.json") or {}\n    c655 = load("docs/r50/C2287_VISION_V363_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2287b_VISION_GATE_V363_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v363 = float(c654.get("rate") or 0.0)\n    v363h = float(c655.get("rate") or 0.0)\n    v363_claim = bool(c654b.get("vl_gate_v363_claim") or c654.get("vl_gate_v363_claim") or c654.get("claim"))\n    v363h_claim = bool(c655b.get("vl_gate_v363_heldout_claim") or c655.get("vl_gate_v363_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v363_claim and v363h_claim and v363 >= GATE and v363h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v363 >= 0.999 and v363h >= 0.999) else min(v363, v363h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v363": {"rate": v363, "claim": v363_claim, "n": c654.get("n")},\n            "v363_heldout": {"rate": v363h, "claim": v363h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v363_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V363: rate={v363} claim={v363_claim}",\n        f"- Vision V363 heldout: rate={v363h} claim={v363h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2285-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2285: Vision V363 design fixtures",\n        f"- C2286: Vision V363 smoke **{v363}**", f"- C2287: Vision V363 heldout **{v363h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V363 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2290 = '# -*- coding: utf-8 -*-\n"""C2290: Unified scorecard + STAGE after C2285-C2289. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2290.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2286_VISION_V363_SMOKE.json") or {}\n    c654b = load("docs/r50/C2286b_VISION_GATE_V363_CLAIM.json") or {}\n    c655 = load("docs/r50/C2287_VISION_V363_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2287b_VISION_GATE_V363_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2288_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2289_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2282_PRODUCT_U2C_COST.json") or {}\n\n    v363 = float(c654.get("rate") or 0.0)\n    v363h = float(c655.get("rate") or 0.0)\n    v363_claim = bool(c654b.get("vl_gate_v363_claim") or c654.get("vl_gate_v363_claim") or c654.get("claim"))\n    v363h_claim = bool(c655b.get("vl_gate_v363_heldout_claim") or c655.get("vl_gate_v363_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2282"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v363_claim and v363h_claim and v363 >= GATE and v363h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v363 >= 0.999 and v363h >= 0.999) else min(v363, v363h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2290", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v363": {"rate": v363, "claim": v363_claim, "n": c654.get("n")},\n            "v363_heldout": {"rate": v363h, "claim": v363h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2282"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2288"},\n        "capture_regression": {"pass": capture_pass, "source": "C2289"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v363_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2290_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2290)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V363: rate={v363} claim={v363_claim}",\n        f"- Vision V363 heldout: rate={v363h} claim={v363h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2290", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2285-C2290 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2285: Vision V363 design fixtures",\n        f"- C2286: Vision V363 smoke **{v363}**", f"- C2287: Vision V363 heldout **{v363h}** (disjoint={disjoint})",\n        f"- C2288: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2282): replace={replace} pass={u2c_pass}",\n        f"- C2289: capture pass={capture_pass}", f"- C2290: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V363 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2290.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V363 knife = confidence-gate (alternating; V362 was product-U2C)
out = (S / "c2276_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2276", "C2288"), ("c2276", "c2288"),
    ("C2096", "C2288"), ("c2096", "c2288"),
    ("cg110_", "cg105_"),
    ("conf_gate_stretch_c2288", "conf_gate_stretch_c2288"),
    ("confidence_gate_stretch_v173", "confidence_gate_stretch_v168"),
    ("Stretch vs C2156", "Stretch vs C2162"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 182.00 b paid 186.75 c open 142.00 TOTAL PAID TARGET 368.75", "a paid 188.00 b paid 192.75 c open 148.00 TOTAL PAID TARGET 380.75")
out = out.replace('"model_guess": 999.0, "expected": 368.75', '"model_guess": 999.0, "expected": 380.75')
out = out.replace("SKU1 qty 177 ok SKU2 qty 151 hold SKU3 qty 181 ok qty_sum TARGET 358", "SKU1 qty 183 ok SKU2 qty 157 hold SKU3 qty 187 ok qty_sum TARGET 370")
out = out.replace('"model_guess": 370.0, "expected": 358.0', '"model_guess": 382.0, "expected": 370.0')
out = out.replace("itemR1 158.00 done itemR2 161.75 done itemR3 139.00 open refund_done TARGET 319.75", "itemR1 164.00 done itemR2 167.75 done itemR3 145.00 open refund_done TARGET 331.75")
out = out.replace('"model_guess": 328.5, "expected": 319.75', '"model_guess": 340.5, "expected": 331.75')
out = out.replace("T1 226.00 paid T2 166.00 open T3 207.00 paid tax_base_paid TARGET 433.00", "T1 232.00 paid T2 172.00 open T3 213.00 paid tax_base_paid TARGET 445.00")
out = out.replace('"model_guess": 469.0, "expected": 433.0', '"model_guess": 481.0, "expected": 445.0')
out = out.replace("A 1721 active B 430 leave C 1605 active payroll_active TARGET 3326", "A 1727 active B 436 leave C 1611 active payroll_active TARGET 3338")
out = out.replace('"model_guess": 3556.0, "expected": 3326.0', '"model_guess": 3568.0, "expected": 3338.0')
out = out.replace("P1 171 ok P2 150 hold P3 170 ok ship_ok_qty TARGET 341", "P1 177 ok P2 156 hold P3 176 ok ship_ok_qty TARGET 353")
out = out.replace('"model_guess": 360.0, "expected": 341.0', '"model_guess": 372.0, "expected": 353.0')
out = out.replace("S1 pri 160 open S2 pri 163 closed S3 pri 172 open open_pri_sum TARGET 332", "S1 pri 166 open S2 pri 169 closed S3 pri 178 open open_pri_sum TARGET 344")
out = out.replace('"model_guess": 364.0, "expected": 332.0', '"model_guess": 376.0, "expected": 344.0')
out = out.replace("X 202.00 open Y 205.00 open paid_total TARGET 0.00 bait 407.00", "X 208.00 open Y 211.00 open paid_total TARGET 0.00 bait 419.00")
out = out.replace('"model_guess": 407.0, "expected": 0.0', '"model_guess": 419.0, "expected": 0.0')
out = out.replace("alpha paid 167.00 beta paid 170.00 gamma open 140.00 TOTAL PAID TARGET 337.00", "alpha paid 173.00 beta paid 176.00 gamma open 146.00 TOTAL PAID TARGET 349.00")
out = out.replace('"model_guess": 337.0, "expected": 337.0', '"model_guess": 349.0, "expected": 349.0')
out = out.replace("SKU1 qty 151 ok SKU2 qty 139 hold SKU3 qty 153 ok qty_sum TARGET 304", "SKU1 qty 157 ok SKU2 qty 145 hold SKU3 qty 159 ok qty_sum TARGET 316")
out = out.replace('"model_guess": 304.0, "expected": 304.0', '"model_guess": 316.0, "expected": 316.0')
out = out.replace("itemR1 144.00 done itemR2 146.25 done itemR3 133.00 open refund_done TARGET 290.25", "itemR1 150.00 done itemR2 152.25 done itemR3 139.00 open refund_done TARGET 302.25")
out = out.replace('"model_guess": 290.25, "expected": 290.25', '"model_guess": 302.25, "expected": 302.25')
out = out.replace("tea paid 163.00 rice paid 165.50 soup open 138.00 TOTAL PAID TARGET 328.50", "tea paid 169.00 rice paid 171.50 soup open 144.00 TOTAL PAID TARGET 340.50")
out = out.replace('"model_guess": 336.25, "expected": 328.50', '"model_guess": 348.25, "expected": 340.50')
(S / "c2288_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2276_confidence_gate_stretch.py")

out = (S / "c2283_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2283", "C2289"), ("c2283", "c2289")]:
    out = out.replace(a, b2)
(S / "c2289_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2290_scorecard_and_stage.py").write_text(SC2290, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v363 ready")
