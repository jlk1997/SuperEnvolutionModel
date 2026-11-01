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
T327 = [
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
TR327 = [
    [2318.0, 2335.5, 2058.0],[840, 760, 820],[2241.0, 2250.25, 2036.0],[2374.0, 2391.0, 2126.0],
    [2436.0, 2460.0, 2096.0],[2154, 2170, 2054],[490.0, 530.0, 760.0],[2284.0, 2315.75, 2060.0],
    [840.0, 760.0, 820.0],[2351.0, 2339.0, 2057.0],[1,1,0],[0,0,0],
    [2417.0, 2438.5, 2082.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO327 = [
    [2116.0, 2128.75, 1977.0],[640, 660, 820],[2059.0, 2073.5, 1952.0],[2189.0, 2205.0, 2008.0],
    [2230.0, 2246.0, 2001.0],[2012, 2024, 1974],[420.0, 460.0, 740.0],[2100.0, 2121.75, 1977.0],
    [740.0, 780.0, 820.0],[2147.0, 2133.0, 1974.0],[1,1,0],[0,0,0],
    [2182.0, 2197.5, 1987.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR327, "TR"); check(HO327, "HO")

(ROOT / "tools/_v327_themes.json").write_text(json.dumps({"themes": T327, "train": TR327, "heldout": HO327}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_326(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V327 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V327 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 140.50", "ASHFEN bait 185.95"),
        ("CEDARW bait 142.52", "CEDARF bait 242.52"),
        ("DAWNW ghost 65.65", "DAWNF ghost 165.75"),
        ("GLENW bait 135.45", "GLENF bait 235.45"),
        ("JADEW bait 126.36", "JADEF bait 226.36"),
        ("NETHERW bait 143.53", "NETHERF bait 243.53"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V327-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD326 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v326_themes.json").read_text(encoding="utf-8"))["themes"])
NEW327 = "_".join(t[0] for t in T327)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2069"), ("c1463", "c2069"), ("V226", "V327"), ("v226", "v327"),
    ("_v226c1463", "_v327c2069"),
    ("Harder than V225", "Harder than V325"), ("harder than V225", "harder than V325"),
    (OLD326, NEW327),
    ("V226 keeps floor", "V327 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2069 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2070 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2070 VL"),
    ("kept on V226", "kept on V327"),
    ("vision_images_v226", "vision_images_v327"),
    ("VL_GATE_V226", "VL_GATE_V327"), ("vl_gate_v226", "vl_gate_v327"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V325: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T327, "v327", "V327", TR327))
out = retarget_326(out)
(S / "c2069_vision_v327_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2070"), ("c1464", "c2070"), ("V226", "V327"), ("v226", "v327"),
    ("vision_images_v226", "vision_images_v327"),
    ("VL_GATE_V226", "VL_GATE_V327"), ("vl_gate_v226", "vl_gate_v327"),
    ("runs/vision_v226", "runs/vision_v327"),
]:
    out = out.replace(a, b)
(S / "c2070_vision_v327_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2071"), ("c1465", "c2071"), ("V226", "V327"), ("v226", "v327"),
    ("vision_images_v226h", "vision_images_v327h"),
    ("vision_images_v226", "vision_images_v327"),
    ("VL_GATE_V226", "VL_GATE_V327"), ("vl_gate_v226", "vl_gate_v327"),
    ("runs/vision_v226h", "runs/vision_v327h"),
    ("_v226c1463", "_v327c2069"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T327, "v327h", "V327H", HO327))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v327h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v327"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v327" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v327h_c2071"'); seen_run = True; continue
    out2.append(ln)
(S / "c2071_vision_v327_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2069-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2070_VISION_V327_SMOKE.json") or {}\n    c654b = load("docs/r50/C2070b_VISION_GATE_V327_CLAIM.json") or {}\n    c655 = load("docs/r50/C2071_VISION_V327_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2071b_VISION_GATE_V327_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v327 = float(c654.get("rate") or 0.0)\n    v327h = float(c655.get("rate") or 0.0)\n    v327_claim = bool(c654b.get("vl_gate_v327_claim") or c654.get("vl_gate_v327_claim") or c654.get("claim"))\n    v327h_claim = bool(c655b.get("vl_gate_v327_heldout_claim") or c655.get("vl_gate_v327_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v327_claim and v327h_claim and v327 >= GATE and v327h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v327 >= 0.999 and v327h >= 0.999) else min(v327, v327h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v327": {"rate": v327, "claim": v327_claim, "n": c654.get("n")},\n            "v327_heldout": {"rate": v327h, "claim": v327h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v327_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V327: rate={v327} claim={v327_claim}",\n        f"- Vision V327 heldout: rate={v327h} claim={v327h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2069-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2069: Vision V327 design fixtures",\n        f"- C2070: Vision V327 smoke **{v327}**", f"- C2071: Vision V327 heldout **{v327h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V327 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2074 = '# -*- coding: utf-8 -*-\n"""C2074: Unified scorecard + STAGE after C2069-C2073. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2074.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2070_VISION_V327_SMOKE.json") or {}\n    c654b = load("docs/r50/C2070b_VISION_GATE_V327_CLAIM.json") or {}\n    c655 = load("docs/r50/C2071_VISION_V327_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2071b_VISION_GATE_V327_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2072_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2073_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2066_PRODUCT_U2C_COST.json") or {}\n\n    v327 = float(c654.get("rate") or 0.0)\n    v327h = float(c655.get("rate") or 0.0)\n    v327_claim = bool(c654b.get("vl_gate_v327_claim") or c654.get("vl_gate_v327_claim") or c654.get("claim"))\n    v327h_claim = bool(c655b.get("vl_gate_v327_heldout_claim") or c655.get("vl_gate_v327_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2066"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v327_claim and v327h_claim and v327 >= GATE and v327h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v327 >= 0.999 and v327h >= 0.999) else min(v327, v327h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2074", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v327": {"rate": v327, "claim": v327_claim, "n": c654.get("n")},\n            "v327_heldout": {"rate": v327h, "claim": v327h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2066"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2072"},\n        "capture_regression": {"pass": capture_pass, "source": "C2073"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v327_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2074_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2074)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V327: rate={v327} claim={v327_claim}",\n        f"- Vision V327 heldout: rate={v327h} claim={v327h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2074", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2069-C2074 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2069: Vision V327 design fixtures",\n        f"- C2070: Vision V327 smoke **{v327}**", f"- C2071: Vision V327 heldout **{v327h}** (disjoint={disjoint})",\n        f"- C2072: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2066): replace={replace} pass={u2c_pass}",\n        f"- C2073: capture pass={capture_pass}", f"- C2074: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V327 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2074.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V327 knife = confidence-gate (alternating; V326 was product-U2C)
out = (S / "c2060_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2060", "C2072"), ("c2060", "c2072"),
    ("C2048", "C2072"), ("c2048", "c2072"),
    ("cg145_", "cg146_"),
    ("conf_gate_stretch_c2060", "conf_gate_stretch_c2072"),
    ("confidence_gate_stretch_v208", "confidence_gate_stretch_v209"),
    ("Stretch vs C2048", "Stretch vs C2060"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 124.00 b paid 128.75 c open 84.00 TOTAL PAID TARGET 252.75", "a paid 125.00 b paid 129.75 c open 85.00 TOTAL PAID TARGET 254.75")
out = out.replace('"model_guess": 999.0, "expected": 252.75', '"model_guess": 999.0, "expected": 254.75')
out = out.replace("SKU1 qty 119 ok SKU2 qty 93 hold SKU3 qty 123 ok qty_sum TARGET 242", "SKU1 qty 120 ok SKU2 qty 94 hold SKU3 qty 124 ok qty_sum TARGET 244")
out = out.replace('"model_guess": 254.0, "expected": 242.0', '"model_guess": 256.0, "expected": 244.0')
out = out.replace("itemR1 100.00 done itemR2 103.75 done itemR3 81.00 open refund_done TARGET 203.75", "itemR1 101.00 done itemR2 104.75 done itemR3 82.00 open refund_done TARGET 205.75")
out = out.replace('"model_guess": 212.5, "expected": 203.75', '"model_guess": 214.5, "expected": 205.75')
out = out.replace("T1 168.00 paid T2 108.00 open T3 149.00 paid tax_base_paid TARGET 317.00", "T1 169.00 paid T2 109.00 open T3 150.00 paid tax_base_paid TARGET 319.00")
out = out.replace('"model_guess": 353.0, "expected": 317.0', '"model_guess": 355.0, "expected": 319.0')
out = out.replace("A 1663 active B 372 leave C 1547 active payroll_active TARGET 3210", "A 1664 active B 373 leave C 1548 active payroll_active TARGET 3212")
out = out.replace('"model_guess": 3440.0, "expected": 3210.0', '"model_guess": 3442.0, "expected": 3212.0')
out = out.replace("P1 113 ok P2 92 hold P3 112 ok ship_ok_qty TARGET 225", "P1 114 ok P2 93 hold P3 113 ok ship_ok_qty TARGET 227")
out = out.replace('"model_guess": 244.0, "expected": 225.0', '"model_guess": 246.0, "expected": 227.0')
out = out.replace("S1 pri 102 open S2 pri 105 closed S3 pri 114 open open_pri_sum TARGET 216", "S1 pri 103 open S2 pri 106 closed S3 pri 115 open open_pri_sum TARGET 218")
out = out.replace('"model_guess": 248.0, "expected": 216.0', '"model_guess": 250.0, "expected": 218.0')
out = out.replace("X 144.00 open Y 147.00 open paid_total TARGET 0.00 bait 291.00", "X 145.00 open Y 148.00 open paid_total TARGET 0.00 bait 293.00")
out = out.replace('"model_guess": 291.0, "expected": 0.0', '"model_guess": 293.0, "expected": 0.0')
out = out.replace("alpha paid 109.00 beta paid 112.00 gamma open 82.00 TOTAL PAID TARGET 221.00", "alpha paid 110.00 beta paid 113.00 gamma open 83.00 TOTAL PAID TARGET 223.00")
out = out.replace('"model_guess": 221.0, "expected": 221.0', '"model_guess": 223.0, "expected": 223.0')
out = out.replace("SKU1 qty 93 ok SKU2 qty 81 hold SKU3 qty 95 ok qty_sum TARGET 188", "SKU1 qty 94 ok SKU2 qty 82 hold SKU3 qty 96 ok qty_sum TARGET 190")
out = out.replace('"model_guess": 188.0, "expected": 188.0', '"model_guess": 190.0, "expected": 190.0')
out = out.replace("itemR1 86.00 done itemR2 88.25 done itemR3 75.00 open refund_done TARGET 174.25", "itemR1 87.00 done itemR2 89.25 done itemR3 76.00 open refund_done TARGET 176.25")
out = out.replace('"model_guess": 174.25, "expected": 174.25', '"model_guess": 176.25, "expected": 176.25')
out = out.replace("tea paid 105.00 rice paid 107.50 soup open 80.00 TOTAL PAID TARGET 212.50", "tea paid 106.00 rice paid 108.50 soup open 81.00 TOTAL PAID TARGET 214.50")
out = out.replace('"model_guess": 220.25, "expected": 212.50', '"model_guess": 222.25, "expected": 214.50')
(S / "c2072_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2060_confidence_gate_stretch.py")

out = (S / "c2067_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2067", "C2073"), ("c2067", "c2073")]:
    out = out.replace(a, b2)
(S / "c2073_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2074_scorecard_and_stage.py").write_text(SC2074, encoding="utf-8")
print("scorecard from fixed c2062 conf-gate pattern")
print("OK builder v327 ready")
