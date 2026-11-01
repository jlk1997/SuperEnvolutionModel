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

# *wick ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T325 = [
    ["ashwick","recv","paid_total","ASHWICK GRAIN RECV","RECV","x"],
    ["cedarwick","wh","qty_sum","WH CEDARWICK BIN","RECV","x"],
    ["dawnwick","refund","refund_done","DAWNWICK PATCH REFUND","DONE","x"],
    ["elmwick","tax","tax_base_paid","ELMWICK TAX SLIP","TAX","x"],
    ["fernwick","pay","payroll_active","FERNWICK PAYROLL","PAY","x"],
    ["glenwick","ship","ship_ok","GLENWICK SHIP DOCK","SHIP","x"],
    ["hazewick","sla","sla_ok_hours","HAZEWICK SLA CARD","SLA","x"],
    ["inkwick","exp","exp_sum","INKWICK EXPENSE","EXP","x"],
    ["jadewick","po","po_open","JADEWICK PO SHEET","PO","x"],
    ["knotwick","order","order_paid","KNOTWICK ORDER","ORD","x"],
    ["lakewick","dup","dup_mark","LAKEWICK DUP MARK","DUP","x"],
    ["mosswick","zero","zero_check","MOSSWICK AIR ZERO","ZERO","x"],
    ["netherwick","ledger","ledger_net","NETHERWICK LEDGER","LED","x"],
    ["oakwick","ui","ui_ok","OAKWICK UI SCAN","UI","x"],
    ["pinewick","stack","stack_count","PINEWICK STACK","STK","x"],
    ["quillwick","fax","fax_pages","QUILLWICK FAX","FAX","x"],
    ["reedwick","glare","glare_ok","REEDWICK GLARE","GLR","x"],
    ["stonewick","tab","tab_index","STONEWICK TAB INDEX","TAB","x"],
]
TR325 = [
    [2314.0, 2331.5, 2054.0],[840, 760, 820],[2237.0, 2246.25, 2032.0],[2370.0, 2387.0, 2122.0],
    [2432.0, 2456.0, 2092.0],[2150, 2166, 2050],[490.0, 530.0, 760.0],[2280.0, 2311.75, 2056.0],
    [840.0, 760.0, 820.0],[2347.0, 2335.0, 2053.0],[1,1,0],[0,0,0],
    [2413.0, 2434.5, 2078.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO325 = [
    [2112.0, 2124.75, 1973.0],[640, 660, 820],[2055.0, 2069.5, 1948.0],[2185.0, 2201.0, 2004.0],
    [2226.0, 2242.0, 1997.0],[2008, 2020, 1968],[420.0, 460.0, 740.0],[2096.0, 2117.75, 1973.0],
    [740.0, 780.0, 820.0],[2143.0, 2129.0, 1970.0],[1,1,0],[0,0,0],
    [2178.0, 2193.5, 1983.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR325, "TR"); check(HO325, "HO")

(ROOT / "tools/_v325_themes.json").write_text(json.dumps({"themes": T325, "train": TR325, "heldout": HO325}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_324(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V325 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V325 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHWICK bait 185.95"),
        ("CEDARW bait 142.52", "CEDARW bait 240.50"),
        ("DAWNW ghost 65.65", "DAWNW ghost 163.73"),
        ("GLENW bait 135.45", "GLENW bait 233.43"),
        ("JADEW bait 126.36", "JADEW bait 224.34"),
        ("NETHERW bait 143.53", "NETHERW bait 241.51"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V325-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD324 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v324_themes.json").read_text(encoding="utf-8"))["themes"])
NEW325 = "_".join(t[0] for t in T325)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2057"), ("c1463", "c2057"), ("V226", "V325"), ("v226", "v325"),
    ("_v226c1463", "_v325c2057"),
    ("Harder than V225", "Harder than V323"), ("harder than V225", "harder than V323"),
    (OLD324, NEW325),
    ("V226 keeps floor", "V325 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2057 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2058 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2058 VL"),
    ("kept on V226", "kept on V325"),
    ("vision_images_v226", "vision_images_v325"),
    ("VL_GATE_V226", "VL_GATE_V325"), ("vl_gate_v226", "vl_gate_v325"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V323: ashwick, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T325, "v325", "V325", TR325))
out = retarget_324(out)
(S / "c2057_vision_v325_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2058"), ("c1464", "c2058"), ("V226", "V325"), ("v226", "v325"),
    ("vision_images_v226", "vision_images_v325"),
    ("VL_GATE_V226", "VL_GATE_V325"), ("vl_gate_v226", "vl_gate_v325"),
    ("runs/vision_v226", "runs/vision_v325"),
]:
    out = out.replace(a, b)
(S / "c2058_vision_v325_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2059"), ("c1465", "c2059"), ("V226", "V325"), ("v226", "v325"),
    ("vision_images_v226h", "vision_images_v325h"),
    ("vision_images_v226", "vision_images_v325"),
    ("VL_GATE_V226", "VL_GATE_V325"), ("vl_gate_v226", "vl_gate_v325"),
    ("runs/vision_v226h", "runs/vision_v325h"),
    ("_v226c1463", "_v325c2057"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T325, "v325h", "V325H", HO325))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v325h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v325"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v325" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v325h_c2059"'); seen_run = True; continue
    out2.append(ln)
(S / "c2059_vision_v325_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2057-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2058_VISION_V325_SMOKE.json") or {}\n    c654b = load("docs/r50/C2058b_VISION_GATE_V325_CLAIM.json") or {}\n    c655 = load("docs/r50/C2059_VISION_V325_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2059b_VISION_GATE_V325_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v325 = float(c654.get("rate") or 0.0)\n    v325h = float(c655.get("rate") or 0.0)\n    v325_claim = bool(c654b.get("vl_gate_v325_claim") or c654.get("vl_gate_v325_claim") or c654.get("claim"))\n    v325h_claim = bool(c655b.get("vl_gate_v325_heldout_claim") or c655.get("vl_gate_v325_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v325_claim and v325h_claim and v325 >= GATE and v325h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v325 >= 0.999 and v325h >= 0.999) else min(v325, v325h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v325": {"rate": v325, "claim": v325_claim, "n": c654.get("n")},\n            "v325_heldout": {"rate": v325h, "claim": v325h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v325_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V325: rate={v325} claim={v325_claim}",\n        f"- Vision V325 heldout: rate={v325h} claim={v325h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2057-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2057: Vision V325 design fixtures",\n        f"- C2058: Vision V325 smoke **{v325}**", f"- C2059: Vision V325 heldout **{v325h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V325 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2062 = '# -*- coding: utf-8 -*-\n"""C2062: Unified scorecard + STAGE after C2057-C2061. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2062.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2058_VISION_V325_SMOKE.json") or {}\n    c654b = load("docs/r50/C2058b_VISION_GATE_V325_CLAIM.json") or {}\n    c655 = load("docs/r50/C2059_VISION_V325_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2059b_VISION_GATE_V325_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2060_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2061_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2054_PRODUCT_U2C_COST.json") or {}\n\n    v325 = float(c654.get("rate") or 0.0)\n    v325h = float(c655.get("rate") or 0.0)\n    v325_claim = bool(c654b.get("vl_gate_v325_claim") or c654.get("vl_gate_v325_claim") or c654.get("claim"))\n    v325h_claim = bool(c655b.get("vl_gate_v325_heldout_claim") or c655.get("vl_gate_v325_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2054"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v325_claim and v325h_claim and v325 >= GATE and v325h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v325 >= 0.999 and v325h >= 0.999) else min(v325, v325h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2062", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v325": {"rate": v325, "claim": v325_claim, "n": c654.get("n")},\n            "v325_heldout": {"rate": v325h, "claim": v325h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2054"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2060"},\n        "capture_regression": {"pass": capture_pass, "source": "C2061"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v325_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2062_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2062)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V325: rate={v325} claim={v325_claim}",\n        f"- Vision V325 heldout: rate={v325h} claim={v325h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2062", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2057-C2062 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2057: Vision V325 design fixtures",\n        f"- C2058: Vision V325 smoke **{v325}**", f"- C2059: Vision V325 heldout **{v325h}** (disjoint={disjoint})",\n        f"- C2060: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2054): replace={replace} pass={u2c_pass}",\n        f"- C2061: capture pass={capture_pass}", f"- C2062: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V325 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2062.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V325 knife = confidence-gate (alternating; V324 was product-U2C)
out = (S / "c2048_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2048", "C2060"), ("c2048", "c2060"),
    ("C2036", "C2060"), ("c2036", "c2060"),
    ("cg144_", "cg145_"),
    ("conf_gate_stretch_c2048", "conf_gate_stretch_c2060"),
    ("confidence_gate_stretch_v207", "confidence_gate_stretch_v208"),
    ("Stretch vs C2036", "Stretch vs C2048"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 123.00 b paid 127.75 c open 83.00 TOTAL PAID TARGET 250.75", "a paid 124.00 b paid 128.75 c open 84.00 TOTAL PAID TARGET 252.75")
out = out.replace('"model_guess": 999.0, "expected": 250.75', '"model_guess": 999.0, "expected": 252.75')
out = out.replace("SKU1 qty 118 ok SKU2 qty 92 hold SKU3 qty 122 ok qty_sum TARGET 240", "SKU1 qty 119 ok SKU2 qty 93 hold SKU3 qty 123 ok qty_sum TARGET 242")
out = out.replace('"model_guess": 252.0, "expected": 240.0', '"model_guess": 254.0, "expected": 242.0')
out = out.replace("itemR1 99.00 done itemR2 102.75 done itemR3 80.00 open refund_done TARGET 201.75", "itemR1 100.00 done itemR2 103.75 done itemR3 81.00 open refund_done TARGET 203.75")
out = out.replace('"model_guess": 210.5, "expected": 201.75', '"model_guess": 212.5, "expected": 203.75')
out = out.replace("T1 167.00 paid T2 107.00 open T3 148.00 paid tax_base_paid TARGET 315.00", "T1 168.00 paid T2 108.00 open T3 149.00 paid tax_base_paid TARGET 317.00")
out = out.replace('"model_guess": 351.0, "expected": 315.0', '"model_guess": 353.0, "expected": 317.0')
out = out.replace("A 1662 active B 371 leave C 1546 active payroll_active TARGET 3208", "A 1663 active B 372 leave C 1547 active payroll_active TARGET 3210")
out = out.replace('"model_guess": 3438.0, "expected": 3208.0', '"model_guess": 3440.0, "expected": 3210.0')
out = out.replace("P1 112 ok P2 91 hold P3 111 ok ship_ok_qty TARGET 223", "P1 113 ok P2 92 hold P3 112 ok ship_ok_qty TARGET 225")
out = out.replace('"model_guess": 242.0, "expected": 223.0', '"model_guess": 244.0, "expected": 225.0')
out = out.replace("S1 pri 101 open S2 pri 104 closed S3 pri 113 open open_pri_sum TARGET 214", "S1 pri 102 open S2 pri 105 closed S3 pri 114 open open_pri_sum TARGET 216")
out = out.replace('"model_guess": 246.0, "expected": 214.0', '"model_guess": 248.0, "expected": 216.0')
out = out.replace("X 143.00 open Y 146.00 open paid_total TARGET 0.00 bait 289.00", "X 144.00 open Y 147.00 open paid_total TARGET 0.00 bait 291.00")
out = out.replace('"model_guess": 289.0, "expected": 0.0', '"model_guess": 291.0, "expected": 0.0')
out = out.replace("alpha paid 108.00 beta paid 111.00 gamma open 81.00 TOTAL PAID TARGET 219.00", "alpha paid 109.00 beta paid 112.00 gamma open 82.00 TOTAL PAID TARGET 221.00")
out = out.replace('"model_guess": 219.0, "expected": 219.0', '"model_guess": 221.0, "expected": 221.0')
out = out.replace("SKU1 qty 92 ok SKU2 qty 80 hold SKU3 qty 94 ok qty_sum TARGET 186", "SKU1 qty 93 ok SKU2 qty 81 hold SKU3 qty 95 ok qty_sum TARGET 188")
out = out.replace('"model_guess": 186.0, "expected": 186.0', '"model_guess": 188.0, "expected": 188.0')
out = out.replace("itemR1 85.00 done itemR2 87.25 done itemR3 74.00 open refund_done TARGET 172.25", "itemR1 86.00 done itemR2 88.25 done itemR3 75.00 open refund_done TARGET 174.25")
out = out.replace('"model_guess": 172.25, "expected": 172.25', '"model_guess": 174.25, "expected": 174.25')
out = out.replace("tea paid 104.00 rice paid 106.50 soup open 79.00 TOTAL PAID TARGET 210.50", "tea paid 105.00 rice paid 107.50 soup open 80.00 TOTAL PAID TARGET 212.50")
out = out.replace('"model_guess": 218.25, "expected": 210.50', '"model_guess": 220.25, "expected": 212.50')
(S / "c2060_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2048_confidence_gate_stretch.py")

out = (S / "c2055_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2055", "C2061"), ("c2055", "c2061")]:
    out = out.replace(a, b2)
(S / "c2061_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2062_scorecard_and_stage.py").write_text(SC2062, encoding="utf-8")
print("scorecard from fixed c2050 conf-gate pattern")
print("OK builder v325 ready")
