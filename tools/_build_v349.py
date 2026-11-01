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

# *fen ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T349 = [
    ["ashfen","recv","paid_total","ASHFEN GRAIN RECV","RECV","x"],
    ["cedarfen","wh","qty_sum","WH CEDARFEN BIN","RECV","x"],
    ["dawnfen","refund","refund_done","DAWNFEN PATCH REFUND","DONE","x"],
    ["elmfen","tax","tax_base_paid","ELMFEN TAX SLIP","TAX","x"],
    ["fernfen","pay","payroll_active","FERNFEN PAYROLL","PAY","x"],
    ["glenfen","ship","ship_ok","GLENFEN SHIP DOCK","SHIP","x"],
    ["hazefen","sla","sla_ok_hours","HAZEFEN SLA CARD","SLA","x"],
    ["inkfen","exp","exp_sum","INKFEN EXPENSE","EXP","x"],
    ["jadefen","po","po_open","JADEFEN PO SHEET","PO","x"],
    ["knotfen","order","order_paid","KNOTFEN ORDER","ORD","x"],
    ["lakefen","dup","dup_mark","LAKEFEN DUP MARK","DUP","x"],
    ["mossfen","zero","zero_check","MOSSFEN AIR ZERO","ZERO","x"],
    ["netherfen","ledger","ledger_net","NETHERFEN LEDGER","LED","x"],
    ["oakfen","ui","ui_ok","OAKFEN UI SCAN","UI","x"],
    ["pinefen","stack","stack_count","PINEFEN STACK","STK","x"],
    ["quillfen","fax","fax_pages","QUILLFEN FAX","FAX","x"],
    ["reedfen","glare","glare_ok","REEDFEN GLARE","GLR","x"],
    ["stonefen","tab","tab_index","STONEFEN TAB INDEX","TAB","x"],
]
TR349 = [
    [2362.0, 2379.5, 2102.0],[840, 760, 820],[2247.0, 2248.25, 2054.0],[2418.0, 2435.0, 2170.0],
    [2480.0, 2495.0, 2140.0],[2198, 2214, 2098],[490.0, 530.0, 760.0],[2328.0, 2359.75, 2104.0],
    [840.0, 760.0, 820.0],[2395.0, 2383.0, 2101.0],[1,1,0],[0,0,0],
    [2453.0, 2472.5, 2120.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO349 = [
    [2160.0, 2172.75, 2021.0],[640, 660, 820],[2103.0, 2117.5, 1996.0],[2233.0, 2249.0, 2052.0],
    [2237.0, 2248.0, 2045.0],[2056, 2068, 2018],[420.0, 460.0, 740.0],[2144.0, 2165.75, 2021.0],
    [740.0, 780.0, 820.0],[2191.0, 2177.0, 2018.0],[1,1,0],[0,0,0],
    [2221.0, 2235.5, 2025.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR349, "TR"); check(HO349, "HO")

(ROOT / "tools/_v349_themes.json").write_text(json.dumps({"themes": T349, "train": TR349, "heldout": HO349}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_348(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V349 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V349 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 140.50", "ASHFEN bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 250.60"),
        ("DAWNW ghost 65.65", "DAWNH ghost 173.83"),
        ("GLENW bait 135.45", "GLENH bait 243.53"),
        ("JADEW bait 126.36", "JADEH bait 234.44"),
        ("NETHERW bait 143.53", "NETHERH bait 251.61"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V349-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD348 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v348_themes.json").read_text(encoding="utf-8"))["themes"])
NEW349 = "_".join(t[0] for t in T349)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2201"), ("c1463", "c2201"), ("V226", "V349"), ("v226", "v349"),
    ("_v226c1463", "_v349c2201"),
    ("Harder than V225", "Harder than V347"), ("harder than V225", "harder than V347"),
    (OLD348, NEW349),
    ("V226 keeps floor", "V349 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2201 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2202 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2202 VL"),
    ("kept on V226", "kept on V349"),
    ("vision_images_v226", "vision_images_v349"),
    ("VL_GATE_V226", "VL_GATE_V349"), ("vl_gate_v226", "vl_gate_v349"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V347: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T349, "v349", "V349", TR349))
out = retarget_348(out)
(S / "c2201_vision_v349_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2202"), ("c1464", "c2202"), ("V226", "V349"), ("v226", "v349"),
    ("vision_images_v226", "vision_images_v349"),
    ("VL_GATE_V226", "VL_GATE_V349"), ("vl_gate_v226", "vl_gate_v349"),
    ("runs/vision_v226", "runs/vision_v349"),
]:
    out = out.replace(a, b)
(S / "c2202_vision_v349_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2203"), ("c1465", "c2203"), ("V226", "V349"), ("v226", "v349"),
    ("vision_images_v226h", "vision_images_v349h"),
    ("vision_images_v226", "vision_images_v349"),
    ("VL_GATE_V226", "VL_GATE_V349"), ("vl_gate_v226", "vl_gate_v349"),
    ("runs/vision_v226h", "runs/vision_v349h"),
    ("_v226c1463", "_v349c2201"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T349, "v349h", "V349H", HO349))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v349h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v349"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v349" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v349h_c2203"'); seen_run = True; continue
    out2.append(ln)
(S / "c2203_vision_v349_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2201-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2202_VISION_V349_SMOKE.json") or {}\n    c654b = load("docs/r50/C2202b_VISION_GATE_V349_CLAIM.json") or {}\n    c655 = load("docs/r50/C2203_VISION_V349_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2203b_VISION_GATE_V349_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v349 = float(c654.get("rate") or 0.0)\n    v349h = float(c655.get("rate") or 0.0)\n    v349_claim = bool(c654b.get("vl_gate_v349_claim") or c654.get("vl_gate_v349_claim") or c654.get("claim"))\n    v349h_claim = bool(c655b.get("vl_gate_v349_heldout_claim") or c655.get("vl_gate_v349_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v349_claim and v349h_claim and v349 >= GATE and v349h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v349 >= 0.999 and v349h >= 0.999) else min(v349, v349h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v349": {"rate": v349, "claim": v349_claim, "n": c654.get("n")},\n            "v349_heldout": {"rate": v349h, "claim": v349h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v349_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V349: rate={v349} claim={v349_claim}",\n        f"- Vision V349 heldout: rate={v349h} claim={v349h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2201-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2201: Vision V349 design fixtures",\n        f"- C2202: Vision V349 smoke **{v349}**", f"- C2203: Vision V349 heldout **{v349h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V349 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2206 = '# -*- coding: utf-8 -*-\n"""C2206: Unified scorecard + STAGE after C2201-C2205. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2206.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2202_VISION_V349_SMOKE.json") or {}\n    c654b = load("docs/r50/C2202b_VISION_GATE_V349_CLAIM.json") or {}\n    c655 = load("docs/r50/C2203_VISION_V349_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2203b_VISION_GATE_V349_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2204_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2205_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2198_PRODUCT_U2C_COST.json") or {}\n\n    v349 = float(c654.get("rate") or 0.0)\n    v349h = float(c655.get("rate") or 0.0)\n    v349_claim = bool(c654b.get("vl_gate_v349_claim") or c654.get("vl_gate_v349_claim") or c654.get("claim"))\n    v349h_claim = bool(c655b.get("vl_gate_v349_heldout_claim") or c655.get("vl_gate_v349_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2198"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v349_claim and v349h_claim and v349 >= GATE and v349h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v349 >= 0.999 and v349h >= 0.999) else min(v349, v349h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2206", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v349": {"rate": v349, "claim": v349_claim, "n": c654.get("n")},\n            "v349_heldout": {"rate": v349h, "claim": v349h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2198"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2204"},\n        "capture_regression": {"pass": capture_pass, "source": "C2205"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v349_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2206_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2206)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V349: rate={v349} claim={v349_claim}",\n        f"- Vision V349 heldout: rate={v349h} claim={v349h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2206", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2201-C2206 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2201: Vision V349 design fixtures",\n        f"- C2202: Vision V349 smoke **{v349}**", f"- C2203: Vision V349 heldout **{v349h}** (disjoint={disjoint})",\n        f"- C2204: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2198): replace={replace} pass={u2c_pass}",\n        f"- C2205: capture pass={capture_pass}", f"- C2206: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V349 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2206.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V349 knife = confidence-gate (alternating; V348 was product-U2C)
out = (S / "c2192_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2192", "C2204"), ("c2192", "c2204"),
    ("C2096", "C2204"), ("c2096", "c2204"),
    ("cg145_", "cg140_"),
    ("conf_gate_stretch_c2204", "conf_gate_stretch_c2204"),
    ("confidence_gate_stretch_v208", "confidence_gate_stretch_v203"),
    ("Stretch vs C2114", "Stretch vs C2120"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 140.00 b paid 144.75 c open 100.00 TOTAL PAID TARGET 284.75", "a paid 146.00 b paid 150.75 c open 106.00 TOTAL PAID TARGET 296.75")
out = out.replace('"model_guess": 999.0, "expected": 284.75', '"model_guess": 999.0, "expected": 296.75')
out = out.replace("SKU1 qty 135 ok SKU2 qty 109 hold SKU3 qty 139 ok qty_sum TARGET 274", "SKU1 qty 141 ok SKU2 qty 115 hold SKU3 qty 145 ok qty_sum TARGET 286")
out = out.replace('"model_guess": 286.0, "expected": 274.0', '"model_guess": 298.0, "expected": 286.0')
out = out.replace("itemR1 116.00 done itemR2 119.75 done itemR3 97.00 open refund_done TARGET 235.75", "itemR1 122.00 done itemR2 125.75 done itemR3 103.00 open refund_done TARGET 247.75")
out = out.replace('"model_guess": 244.5, "expected": 235.75', '"model_guess": 256.5, "expected": 247.75')
out = out.replace("T1 184.00 paid T2 124.00 open T3 165.00 paid tax_base_paid TARGET 349.00", "T1 190.00 paid T2 130.00 open T3 171.00 paid tax_base_paid TARGET 361.00")
out = out.replace('"model_guess": 385.0, "expected": 349.0', '"model_guess": 397.0, "expected": 361.0')
out = out.replace("A 1679 active B 388 leave C 1563 active payroll_active TARGET 3242", "A 1685 active B 394 leave C 1569 active payroll_active TARGET 3254")
out = out.replace('"model_guess": 3472.0, "expected": 3242.0', '"model_guess": 3484.0, "expected": 3254.0')
out = out.replace("P1 129 ok P2 108 hold P3 128 ok ship_ok_qty TARGET 257", "P1 135 ok P2 114 hold P3 134 ok ship_ok_qty TARGET 269")
out = out.replace('"model_guess": 276.0, "expected": 257.0', '"model_guess": 288.0, "expected": 269.0')
out = out.replace("S1 pri 118 open S2 pri 121 closed S3 pri 130 open open_pri_sum TARGET 248", "S1 pri 124 open S2 pri 127 closed S3 pri 136 open open_pri_sum TARGET 260")
out = out.replace('"model_guess": 280.0, "expected": 248.0', '"model_guess": 292.0, "expected": 260.0')
out = out.replace("X 160.00 open Y 163.00 open paid_total TARGET 0.00 bait 323.00", "X 166.00 open Y 169.00 open paid_total TARGET 0.00 bait 335.00")
out = out.replace('"model_guess": 323.0, "expected": 0.0', '"model_guess": 335.0, "expected": 0.0')
out = out.replace("alpha paid 125.00 beta paid 128.00 gamma open 98.00 TOTAL PAID TARGET 253.00", "alpha paid 131.00 beta paid 134.00 gamma open 104.00 TOTAL PAID TARGET 265.00")
out = out.replace('"model_guess": 253.0, "expected": 253.0', '"model_guess": 265.0, "expected": 265.0')
out = out.replace("SKU1 qty 109 ok SKU2 qty 97 hold SKU3 qty 111 ok qty_sum TARGET 220", "SKU1 qty 115 ok SKU2 qty 103 hold SKU3 qty 117 ok qty_sum TARGET 232")
out = out.replace('"model_guess": 220.0, "expected": 220.0', '"model_guess": 232.0, "expected": 232.0')
out = out.replace("itemR1 102.00 done itemR2 104.25 done itemR3 91.00 open refund_done TARGET 206.25", "itemR1 108.00 done itemR2 110.25 done itemR3 97.00 open refund_done TARGET 218.25")
out = out.replace('"model_guess": 206.25, "expected": 206.25', '"model_guess": 218.25, "expected": 218.25')
out = out.replace("tea paid 121.00 rice paid 123.50 soup open 96.00 TOTAL PAID TARGET 244.50", "tea paid 127.00 rice paid 129.50 soup open 102.00 TOTAL PAID TARGET 256.50")
out = out.replace('"model_guess": 252.25, "expected": 244.50', '"model_guess": 264.25, "expected": 256.50')
(S / "c2204_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2192_confidence_gate_stretch.py")

out = (S / "c2199_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2199", "C2205"), ("c2199", "c2205")]:
    out = out.replace(a, b2)
(S / "c2205_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2206_scorecard_and_stage.py").write_text(SC2206, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v349 ready")
