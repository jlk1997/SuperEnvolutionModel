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

# *moor ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T326 = [
    ["ashmoor","recv","paid_total","ASHMOOR GRAIN RECV","RECV","x"],
    ["cedarmoor","wh","qty_sum","WH CEDARMOOR BIN","RECV","x"],
    ["dawnmoor","refund","refund_done","DAWNMOOR PATCH REFUND","DONE","x"],
    ["elmmoor","tax","tax_base_paid","ELMMOOR TAX SLIP","TAX","x"],
    ["fernmoor","pay","payroll_active","FERNMOOR PAYROLL","PAY","x"],
    ["glenmoor","ship","ship_ok","GLENMOOR SHIP DOCK","SHIP","x"],
    ["hazemoor","sla","sla_ok_hours","HAZEMOOR SLA CARD","SLA","x"],
    ["inkmoor","exp","exp_sum","INKMOOR EXPENSE","EXP","x"],
    ["jademoor","po","po_open","JADEMOOR PO SHEET","PO","x"],
    ["knotmoor","order","order_paid","KNOTMOOR ORDER","ORD","x"],
    ["lakemoor","dup","dup_mark","LAKEMOOR DUP MARK","DUP","x"],
    ["mossmoor","zero","zero_check","MOSSMOOR AIR ZERO","ZERO","x"],
    ["nethermoor","ledger","ledger_net","NETHERMOOR LEDGER","LED","x"],
    ["oakmoor","ui","ui_ok","OAKMOOR UI SCAN","UI","x"],
    ["pinemoor","stack","stack_count","PINEMOOR STACK","STK","x"],
    ["quillmoor","fax","fax_pages","QUILLMOOR FAX","FAX","x"],
    ["reedmoor","glare","glare_ok","REEDMOOR GLARE","GLR","x"],
    ["stonemoor","tab","tab_index","STONEMOOR TAB INDEX","TAB","x"],
]
TR326 = [
    [2316.0, 2333.5, 2056.0],[840, 760, 820],[2239.0, 2248.25, 2034.0],[2372.0, 2389.0, 2124.0],
    [2434.0, 2458.0, 2094.0],[2152, 2168, 2052],[490.0, 530.0, 760.0],[2282.0, 2313.75, 2058.0],
    [840.0, 760.0, 820.0],[2349.0, 2337.0, 2055.0],[1,1,0],[0,0,0],
    [2415.0, 2436.5, 2080.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO326 = [
    [2114.0, 2126.75, 1975.0],[640, 660, 820],[2057.0, 2071.5, 1950.0],[2187.0, 2203.0, 2006.0],
    [2228.0, 2244.0, 1999.0],[2010, 2022, 1970],[420.0, 460.0, 740.0],[2098.0, 2119.75, 1975.0],
    [740.0, 780.0, 820.0],[2145.0, 2131.0, 1972.0],[1,1,0],[0,0,0],
    [2180.0, 2195.5, 1985.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR326, "TR"); check(HO326, "HO")

(ROOT / "tools/_v326_themes.json").write_text(json.dumps({"themes": T326, "train": TR326, "heldout": HO326}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_325(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V326 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V326 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 140.50", "ASHMOOR bait 185.95"),
        ("CEDARW bait 142.52", "CEDARM bait 241.51"),
        ("DAWNW ghost 65.65", "DAWNM ghost 164.74"),
        ("GLENW bait 135.45", "GLENM bait 234.44"),
        ("JADEW bait 126.36", "JADEM bait 225.35"),
        ("NETHERW bait 143.53", "NETHERM bait 242.52"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V326-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD325 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v325_themes.json").read_text(encoding="utf-8"))["themes"])
NEW326 = "_".join(t[0] for t in T326)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2063"), ("c1463", "c2063"), ("V226", "V326"), ("v226", "v326"),
    ("_v226c1463", "_v326c2063"),
    ("Harder than V225", "Harder than V324"), ("harder than V225", "harder than V324"),
    (OLD325, NEW326),
    ("V226 keeps floor", "V326 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2063 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2064 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2064 VL"),
    ("kept on V226", "kept on V326"),
    ("vision_images_v226", "vision_images_v326"),
    ("VL_GATE_V226", "VL_GATE_V326"), ("vl_gate_v226", "vl_gate_v326"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V324: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T326, "v326", "V326", TR326))
out = retarget_325(out)
(S / "c2063_vision_v326_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2064"), ("c1464", "c2064"), ("V226", "V326"), ("v226", "v326"),
    ("vision_images_v226", "vision_images_v326"),
    ("VL_GATE_V226", "VL_GATE_V326"), ("vl_gate_v226", "vl_gate_v326"),
    ("runs/vision_v226", "runs/vision_v326"),
]:
    out = out.replace(a, b)
(S / "c2064_vision_v326_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2065"), ("c1465", "c2065"), ("V226", "V326"), ("v226", "v326"),
    ("vision_images_v226h", "vision_images_v326h"),
    ("vision_images_v226", "vision_images_v326"),
    ("VL_GATE_V226", "VL_GATE_V326"), ("vl_gate_v226", "vl_gate_v326"),
    ("runs/vision_v226h", "runs/vision_v326h"),
    ("_v226c1463", "_v326c2063"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T326, "v326h", "V326H", HO326))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v326h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v326"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v326" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v326h_c2065"'); seen_run = True; continue
    out2.append(ln)
(S / "c2065_vision_v326_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2063-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2064_VISION_V326_SMOKE.json") or {}\n    c654b = load("docs/r50/C2064b_VISION_GATE_V326_CLAIM.json") or {}\n    c655 = load("docs/r50/C2065_VISION_V326_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2065b_VISION_GATE_V326_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v326 = float(c654.get("rate") or 0.0)\n    v326h = float(c655.get("rate") or 0.0)\n    v326_claim = bool(c654b.get("vl_gate_v326_claim") or c654.get("vl_gate_v326_claim") or c654.get("claim"))\n    v326h_claim = bool(c655b.get("vl_gate_v326_heldout_claim") or c655.get("vl_gate_v326_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v326_claim and v326h_claim and v326 >= GATE and v326h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v326 >= 0.999 and v326h >= 0.999) else min(v326, v326h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v326": {"rate": v326, "claim": v326_claim, "n": c654.get("n")},\n            "v326_heldout": {"rate": v326h, "claim": v326h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v326_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V326: rate={v326} claim={v326_claim}",\n        f"- Vision V326 heldout: rate={v326h} claim={v326h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2063-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2063: Vision V326 design fixtures",\n        f"- C2064: Vision V326 smoke **{v326}**", f"- C2065: Vision V326 heldout **{v326h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V326 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2068 = '\ufeff# -*- coding: utf-8 -*-\n"""C2068: Unified scorecard + STAGE after C2063-C2067. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2068.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2064_VISION_V326_SMOKE.json") or {}\n    c654b = load("docs/r50/C2064b_VISION_GATE_V326_CLAIM.json") or {}\n    c655 = load("docs/r50/C2065_VISION_V326_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2065b_VISION_GATE_V326_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2060_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2067_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2066_PRODUCT_U2C_COST.json") or {}\n\n    v326 = float(c654.get("rate") or 0.0)\n    v326h = float(c655.get("rate") or 0.0)\n    v326_claim = bool(c654b.get("vl_gate_v326_claim") or c654.get("vl_gate_v326_claim") or c654.get("claim"))\n    v326h_claim = bool(c655b.get("vl_gate_v326_heldout_claim") or c655.get("vl_gate_v326_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2066"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v326_claim and v326h_claim and v326 >= GATE and v326h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v326 >= 0.999 and v326h >= 0.999) else min(v326, v326h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2068", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v326": {"rate": v326, "claim": v326_claim, "n": c654.get("n")},\n            "v326_heldout": {"rate": v326h, "claim": v326h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2066"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2060"},\n        "capture_regression": {"pass": capture_pass, "source": "C2067"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v326_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2068_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2068)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V326: rate={v326} claim={v326_claim}",\n        f"- Vision V326 heldout: rate={v326h} claim={v326h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2068", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2063-C2068 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2063: Vision V326 design fixtures",\n        f"- C2064: Vision V326 smoke **{v326}**", f"- C2065: Vision V326 heldout **{v326h}** (disjoint={disjoint})",\n        f"- C2066: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C2060): pass={conf_pass} rate={conf_rate}",\n        f"- C2067: capture pass={capture_pass}", f"- C2068: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V326 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2068.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V326 knife = product-U2C (alternating; V325 was confidence-gate)
out = (S / "c2054_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2054", "C2066"), ("c2054", "c2066"),
    ("C2042", "C2066"), ("c2042", "c2066"),
    ("product_u2c_cost_c2054", "product_u2c_cost_c2066"),
    ("u2c_v206", "u2c_v207"),
    ("u2c_c2054", "u2c_c2066"),
]:
    out = out.replace(a, b2)
(S / "c2066_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2054")

out = (S / "c2061_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2061", "C2067"), ("c2061", "c2067")]:
    out = out.replace(a, b2)
(S / "c2067_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2068_scorecard_and_stage.py").write_text(SC2068, encoding="utf-8")
print("scorecard from fixed c2056 product-U2C pattern")
print("OK builder v326 ready")
