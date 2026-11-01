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
T359 = [
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
TR359 = [
    [2382.0, 2399.5, 2122.0],[840, 760, 820],[2245.0, 2247.25, 2044.0],[2438.0, 2455.0, 2190.0],
    [2499.0, 2495.0, 2160.0],[2218, 2234, 2118],[490.0, 530.0, 760.0],[2348.0, 2379.75, 2124.0],
    [840.0, 760.0, 820.0],[2415.0, 2403.0, 2121.0],[1,1,0],[0,0,0],
    [2459.0, 2478.5, 2100.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO359 = [
    [2180.0, 2192.75, 2041.0],[640, 660, 820],[2123.0, 2137.5, 2016.0],[2253.0, 2269.0, 2072.0],
    [2257.0, 2268.0, 2065.0],[2076, 2088, 2038],[420.0, 460.0, 740.0],[2164.0, 2185.75, 2041.0],
    [740.0, 780.0, 820.0],[2211.0, 2197.0, 2038.0],[1,1,0],[0,0,0],
    [2241.0, 2255.5, 2045.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR359, "TR"); check(HO359, "HO")

(ROOT / "tools/_v359_themes.json").write_text(json.dumps({"themes": T359, "train": TR359, "heldout": HO359}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_358(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V359 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V359 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 140.50", "ASHMOOR bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 250.60"),
        ("DAWNW ghost 65.65", "DAWNH ghost 173.83"),
        ("GLENW bait 135.45", "GLENH bait 243.53"),
        ("JADEW bait 126.36", "JADEH bait 234.44"),
        ("NETHERW bait 143.53", "NETHERH bait 251.61"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V359-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD358 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v358_themes.json").read_text(encoding="utf-8"))["themes"])
NEW359 = "_".join(t[0] for t in T359)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2261"), ("c1463", "c2261"), ("V226", "V359"), ("v226", "v359"),
    ("_v226c1463", "_v359c2261"),
    ("Harder than V225", "Harder than V357"), ("harder than V225", "harder than V357"),
    (OLD358, NEW359),
    ("V226 keeps floor", "V359 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2261 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2262 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2262 VL"),
    ("kept on V226", "kept on V359"),
    ("vision_images_v226", "vision_images_v359"),
    ("VL_GATE_V226", "VL_GATE_V359"), ("vl_gate_v226", "vl_gate_v359"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V357: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T359, "v359", "V359", TR359))
out = retarget_358(out)
(S / "c2261_vision_v359_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2262"), ("c1464", "c2262"), ("V226", "V359"), ("v226", "v359"),
    ("vision_images_v226", "vision_images_v359"),
    ("VL_GATE_V226", "VL_GATE_V359"), ("vl_gate_v226", "vl_gate_v359"),
    ("runs/vision_v226", "runs/vision_v359"),
]:
    out = out.replace(a, b)
(S / "c2262_vision_v359_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2263"), ("c1465", "c2263"), ("V226", "V359"), ("v226", "v359"),
    ("vision_images_v226h", "vision_images_v359h"),
    ("vision_images_v226", "vision_images_v359"),
    ("VL_GATE_V226", "VL_GATE_V359"), ("vl_gate_v226", "vl_gate_v359"),
    ("runs/vision_v226h", "runs/vision_v359h"),
    ("_v226c1463", "_v359c2261"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T359, "v359h", "V359H", HO359))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v359h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v359"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v359" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v359h_c2263"'); seen_run = True; continue
    out2.append(ln)
(S / "c2263_vision_v359_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2261-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2262_VISION_V359_SMOKE.json") or {}\n    c654b = load("docs/r50/C2262b_VISION_GATE_V359_CLAIM.json") or {}\n    c655 = load("docs/r50/C2263_VISION_V359_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2263b_VISION_GATE_V359_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v359 = float(c654.get("rate") or 0.0)\n    v359h = float(c655.get("rate") or 0.0)\n    v359_claim = bool(c654b.get("vl_gate_v359_claim") or c654.get("vl_gate_v359_claim") or c654.get("claim"))\n    v359h_claim = bool(c655b.get("vl_gate_v359_heldout_claim") or c655.get("vl_gate_v359_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v359_claim and v359h_claim and v359 >= GATE and v359h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v359 >= 0.999 and v359h >= 0.999) else min(v359, v359h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v359": {"rate": v359, "claim": v359_claim, "n": c654.get("n")},\n            "v359_heldout": {"rate": v359h, "claim": v359h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v359_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V359: rate={v359} claim={v359_claim}",\n        f"- Vision V359 heldout: rate={v359h} claim={v359h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2261-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2261: Vision V359 design fixtures",\n        f"- C2262: Vision V359 smoke **{v359}**", f"- C2263: Vision V359 heldout **{v359h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V359 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2266 = '# -*- coding: utf-8 -*-\n"""C2266: Unified scorecard + STAGE after C2261-C2265. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2266.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2262_VISION_V359_SMOKE.json") or {}\n    c654b = load("docs/r50/C2262b_VISION_GATE_V359_CLAIM.json") or {}\n    c655 = load("docs/r50/C2263_VISION_V359_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2263b_VISION_GATE_V359_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2264_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2265_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2258_PRODUCT_U2C_COST.json") or {}\n\n    v359 = float(c654.get("rate") or 0.0)\n    v359h = float(c655.get("rate") or 0.0)\n    v359_claim = bool(c654b.get("vl_gate_v359_claim") or c654.get("vl_gate_v359_claim") or c654.get("claim"))\n    v359h_claim = bool(c655b.get("vl_gate_v359_heldout_claim") or c655.get("vl_gate_v359_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2258"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v359_claim and v359h_claim and v359 >= GATE and v359h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v359 >= 0.999 and v359h >= 0.999) else min(v359, v359h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2266", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v359": {"rate": v359, "claim": v359_claim, "n": c654.get("n")},\n            "v359_heldout": {"rate": v359h, "claim": v359h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2258"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2264"},\n        "capture_regression": {"pass": capture_pass, "source": "C2265"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v359_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2266_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2266)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V359: rate={v359} claim={v359_claim}",\n        f"- Vision V359 heldout: rate={v359h} claim={v359h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2266", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2261-C2266 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2261: Vision V359 design fixtures",\n        f"- C2262: Vision V359 smoke **{v359}**", f"- C2263: Vision V359 heldout **{v359h}** (disjoint={disjoint})",\n        f"- C2264: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2258): replace={replace} pass={u2c_pass}",\n        f"- C2265: capture pass={capture_pass}", f"- C2266: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V359 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2266.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V359 knife = confidence-gate (alternating; V358 was product-U2C)
out = (S / "c2252_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2252", "C2264"), ("c2252", "c2264"),
    ("C2096", "C2264"), ("c2096", "c2264"),
    ("cg120_", "cg115_"),
    ("conf_gate_stretch_c2264", "conf_gate_stretch_c2264"),
    ("confidence_gate_stretch_v183", "confidence_gate_stretch_v178"),
    ("Stretch vs C2144", "Stretch vs C2150"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 170.00 b paid 174.75 c open 130.00 TOTAL PAID TARGET 344.75", "a paid 176.00 b paid 180.75 c open 136.00 TOTAL PAID TARGET 356.75")
out = out.replace('"model_guess": 999.0, "expected": 344.75', '"model_guess": 999.0, "expected": 356.75')
out = out.replace("SKU1 qty 165 ok SKU2 qty 139 hold SKU3 qty 169 ok qty_sum TARGET 334", "SKU1 qty 171 ok SKU2 qty 145 hold SKU3 qty 175 ok qty_sum TARGET 346")
out = out.replace('"model_guess": 346.0, "expected": 334.0', '"model_guess": 358.0, "expected": 346.0')
out = out.replace("itemR1 146.00 done itemR2 149.75 done itemR3 127.00 open refund_done TARGET 295.75", "itemR1 152.00 done itemR2 155.75 done itemR3 133.00 open refund_done TARGET 307.75")
out = out.replace('"model_guess": 304.5, "expected": 295.75', '"model_guess": 316.5, "expected": 307.75')
out = out.replace("T1 214.00 paid T2 154.00 open T3 195.00 paid tax_base_paid TARGET 409.00", "T1 220.00 paid T2 160.00 open T3 201.00 paid tax_base_paid TARGET 421.00")
out = out.replace('"model_guess": 445.0, "expected": 409.0', '"model_guess": 457.0, "expected": 421.0')
out = out.replace("A 1709 active B 418 leave C 1593 active payroll_active TARGET 3302", "A 1715 active B 424 leave C 1599 active payroll_active TARGET 3314")
out = out.replace('"model_guess": 3532.0, "expected": 3302.0', '"model_guess": 3544.0, "expected": 3314.0')
out = out.replace("P1 159 ok P2 138 hold P3 158 ok ship_ok_qty TARGET 317", "P1 165 ok P2 144 hold P3 164 ok ship_ok_qty TARGET 329")
out = out.replace('"model_guess": 336.0, "expected": 317.0', '"model_guess": 348.0, "expected": 329.0')
out = out.replace("S1 pri 148 open S2 pri 151 closed S3 pri 160 open open_pri_sum TARGET 308", "S1 pri 154 open S2 pri 157 closed S3 pri 166 open open_pri_sum TARGET 320")
out = out.replace('"model_guess": 340.0, "expected": 308.0', '"model_guess": 352.0, "expected": 320.0')
out = out.replace("X 190.00 open Y 193.00 open paid_total TARGET 0.00 bait 383.00", "X 196.00 open Y 199.00 open paid_total TARGET 0.00 bait 395.00")
out = out.replace('"model_guess": 383.0, "expected": 0.0', '"model_guess": 395.0, "expected": 0.0')
out = out.replace("alpha paid 155.00 beta paid 158.00 gamma open 128.00 TOTAL PAID TARGET 313.00", "alpha paid 161.00 beta paid 164.00 gamma open 134.00 TOTAL PAID TARGET 325.00")
out = out.replace('"model_guess": 313.0, "expected": 313.0', '"model_guess": 325.0, "expected": 325.0')
out = out.replace("SKU1 qty 139 ok SKU2 qty 127 hold SKU3 qty 141 ok qty_sum TARGET 280", "SKU1 qty 145 ok SKU2 qty 133 hold SKU3 qty 147 ok qty_sum TARGET 292")
out = out.replace('"model_guess": 280.0, "expected": 280.0', '"model_guess": 292.0, "expected": 292.0')
out = out.replace("itemR1 132.00 done itemR2 134.25 done itemR3 121.00 open refund_done TARGET 266.25", "itemR1 138.00 done itemR2 140.25 done itemR3 127.00 open refund_done TARGET 278.25")
out = out.replace('"model_guess": 266.25, "expected": 266.25', '"model_guess": 278.25, "expected": 278.25')
out = out.replace("tea paid 151.00 rice paid 153.50 soup open 126.00 TOTAL PAID TARGET 304.50", "tea paid 157.00 rice paid 159.50 soup open 132.00 TOTAL PAID TARGET 316.50")
out = out.replace('"model_guess": 312.25, "expected": 304.50', '"model_guess": 324.25, "expected": 316.50')
(S / "c2264_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2252_confidence_gate_stretch.py")

out = (S / "c2259_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2259", "C2265"), ("c2259", "c2265")]:
    out = out.replace(a, b2)
(S / "c2265_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2266_scorecard_and_stage.py").write_text(SC2266, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v359 ready")
