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

# *mere ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T343 = [
    ["ashmere","recv","paid_total","ASHMERE GRAIN RECV","RECV","x"],
    ["cedarmere","wh","qty_sum","WH CEDARMERE BIN","RECV","x"],
    ["dawnmere","refund","refund_done","DAWNMERE PATCH REFUND","DONE","x"],
    ["elmmere","tax","tax_base_paid","ELMMERE TAX SLIP","TAX","x"],
    ["fernmere","pay","payroll_active","FERNMERE PAYROLL","PAY","x"],
    ["glenmere","ship","ship_ok","GLENMERE SHIP DOCK","SHIP","x"],
    ["hazemere","sla","sla_ok_hours","HAZEMERE SLA CARD","SLA","x"],
    ["inkmere","exp","exp_sum","INKMERE EXPENSE","EXP","x"],
    ["jademere","po","po_open","JADEMERE PO SHEET","PO","x"],
    ["knotmere","order","order_paid","KNOTMERE ORDER","ORD","x"],
    ["lakemere","dup","dup_mark","LAKEMERE DUP MARK","DUP","x"],
    ["mossmere","zero","zero_check","MOSSMERE AIR ZERO","ZERO","x"],
    ["nethermere","ledger","ledger_net","NETHERMERE LEDGER","LED","x"],
    ["oakmere","ui","ui_ok","OAKMERE UI SCAN","UI","x"],
    ["pinemere","stack","stack_count","PINEMERE STACK","STK","x"],
    ["quillmere","fax","fax_pages","QUILLMERE FAX","FAX","x"],
    ["reedmere","glare","glare_ok","REEDMERE GLARE","GLR","x"],
    ["stonemere","tab","tab_index","STONEMERE TAB INDEX","TAB","x"],
]
TR343 = [
    [2350.0, 2367.5, 2090.0],[840, 760, 820],[2251.0, 2257.25, 2056.0],[2406.0, 2423.0, 2158.0],
    [2468.0, 2492.0, 2128.0],[2186, 2202, 2086],[490.0, 530.0, 760.0],[2316.0, 2347.75, 2092.0],
    [840.0, 760.0, 820.0],[2383.0, 2371.0, 2089.0],[1,1,0],[0,0,0],
    [2449.0, 2470.5, 2114.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO343 = [
    [2148.0, 2160.75, 2009.0],[640, 660, 820],[2091.0, 2105.5, 1984.0],[2221.0, 2237.0, 2040.0],
    [2235.0, 2246.0, 2033.0],[2044, 2056, 2006],[420.0, 460.0, 740.0],[2132.0, 2153.75, 2009.0],
    [740.0, 780.0, 820.0],[2179.0, 2165.0, 2006.0],[1,1,0],[0,0,0],
    [2214.0, 2229.5, 2019.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR343, "TR"); check(HO343, "HO")

(ROOT / "tools/_v343_themes.json").write_text(json.dumps({"themes": T343, "train": TR343, "heldout": HO343}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_342(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V343 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V343 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 140.50", "ASHMERE bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 250.60"),
        ("DAWNW ghost 65.65", "DAWNH ghost 173.83"),
        ("GLENW bait 135.45", "GLENH bait 243.53"),
        ("JADEW bait 126.36", "JADEH bait 234.44"),
        ("NETHERW bait 143.53", "NETHERH bait 251.61"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V343-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD342 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v342_themes.json").read_text(encoding="utf-8"))["themes"])
NEW343 = "_".join(t[0] for t in T343)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2165"), ("c1463", "c2165"), ("V226", "V343"), ("v226", "v343"),
    ("_v226c1463", "_v343c2165"),
    ("Harder than V225", "Harder than V341"), ("harder than V225", "harder than V341"),
    (OLD342, NEW343),
    ("V226 keeps floor", "V343 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2165 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2166 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2166 VL"),
    ("kept on V226", "kept on V343"),
    ("vision_images_v226", "vision_images_v343"),
    ("VL_GATE_V226", "VL_GATE_V343"), ("vl_gate_v226", "vl_gate_v343"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V341: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T343, "v343", "V343", TR343))
out = retarget_342(out)
(S / "c2165_vision_v343_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2166"), ("c1464", "c2166"), ("V226", "V343"), ("v226", "v343"),
    ("vision_images_v226", "vision_images_v343"),
    ("VL_GATE_V226", "VL_GATE_V343"), ("vl_gate_v226", "vl_gate_v343"),
    ("runs/vision_v226", "runs/vision_v343"),
]:
    out = out.replace(a, b)
(S / "c2166_vision_v343_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2167"), ("c1465", "c2167"), ("V226", "V343"), ("v226", "v343"),
    ("vision_images_v226h", "vision_images_v343h"),
    ("vision_images_v226", "vision_images_v343"),
    ("VL_GATE_V226", "VL_GATE_V343"), ("vl_gate_v226", "vl_gate_v343"),
    ("runs/vision_v226h", "runs/vision_v343h"),
    ("_v226c1463", "_v343c2165"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T343, "v343h", "V343H", HO343))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v343h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v343"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v343" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v343h_c2167"'); seen_run = True; continue
    out2.append(ln)
(S / "c2167_vision_v343_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2165-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2166_VISION_V343_SMOKE.json") or {}\n    c654b = load("docs/r50/C2166b_VISION_GATE_V343_CLAIM.json") or {}\n    c655 = load("docs/r50/C2167_VISION_V343_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2167b_VISION_GATE_V343_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v343 = float(c654.get("rate") or 0.0)\n    v343h = float(c655.get("rate") or 0.0)\n    v343_claim = bool(c654b.get("vl_gate_v343_claim") or c654.get("vl_gate_v343_claim") or c654.get("claim"))\n    v343h_claim = bool(c655b.get("vl_gate_v343_heldout_claim") or c655.get("vl_gate_v343_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v343_claim and v343h_claim and v343 >= GATE and v343h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v343 >= 0.999 and v343h >= 0.999) else min(v343, v343h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v343": {"rate": v343, "claim": v343_claim, "n": c654.get("n")},\n            "v343_heldout": {"rate": v343h, "claim": v343h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v343_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V343: rate={v343} claim={v343_claim}",\n        f"- Vision V343 heldout: rate={v343h} claim={v343h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2165-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2165: Vision V343 design fixtures",\n        f"- C2166: Vision V343 smoke **{v343}**", f"- C2167: Vision V343 heldout **{v343h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V343 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2170 = '# -*- coding: utf-8 -*-\n"""C2170: Unified scorecard + STAGE after C2165-C2169. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2170.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2166_VISION_V343_SMOKE.json") or {}\n    c654b = load("docs/r50/C2166b_VISION_GATE_V343_CLAIM.json") or {}\n    c655 = load("docs/r50/C2167_VISION_V343_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2167b_VISION_GATE_V343_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2168_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2169_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2162_PRODUCT_U2C_COST.json") or {}\n\n    v343 = float(c654.get("rate") or 0.0)\n    v343h = float(c655.get("rate") or 0.0)\n    v343_claim = bool(c654b.get("vl_gate_v343_claim") or c654.get("vl_gate_v343_claim") or c654.get("claim"))\n    v343h_claim = bool(c655b.get("vl_gate_v343_heldout_claim") or c655.get("vl_gate_v343_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2162"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v343_claim and v343h_claim and v343 >= GATE and v343h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v343 >= 0.999 and v343h >= 0.999) else min(v343, v343h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2170", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v343": {"rate": v343, "claim": v343_claim, "n": c654.get("n")},\n            "v343_heldout": {"rate": v343h, "claim": v343h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2162"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2168"},\n        "capture_regression": {"pass": capture_pass, "source": "C2169"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v343_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2170_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2170)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V343: rate={v343} claim={v343_claim}",\n        f"- Vision V343 heldout: rate={v343h} claim={v343h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2170", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2165-C2170 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2165: Vision V343 design fixtures",\n        f"- C2166: Vision V343 smoke **{v343}**", f"- C2167: Vision V343 heldout **{v343h}** (disjoint={disjoint})",\n        f"- C2168: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2162): replace={replace} pass={u2c_pass}",\n        f"- C2169: capture pass={capture_pass}", f"- C2170: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V343 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2170.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V343 knife = confidence-gate (alternating; V342 was product-U2C)
out = (S / "c2156_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2156", "C2168"), ("c2156", "c2168"),
    ("C2096", "C2168"), ("c2096", "c2168"),
    ("cg154_", "cg150_"),
    ("conf_gate_stretch_c2168", "conf_gate_stretch_c2168"),
    ("confidence_gate_stretch_v217", "confidence_gate_stretch_v213"),
    ("Stretch vs C2156", "Stretch vs C2108"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75", "a paid 133.00 b paid 137.75 c open 93.00 TOTAL PAID TARGET 270.75")
out = out.replace('"model_guess": 999.0, "expected": 260.75', '"model_guess": 999.0, "expected": 270.75')
out = out.replace("SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250", "SKU1 qty 128 ok SKU2 qty 102 hold SKU3 qty 132 ok qty_sum TARGET 260")
out = out.replace('"model_guess": 262.0, "expected": 250.0', '"model_guess": 272.0, "expected": 260.0')
out = out.replace("itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75", "itemR1 109.00 done itemR2 112.75 done itemR3 90.00 open refund_done TARGET 221.75")
out = out.replace('"model_guess": 220.5, "expected": 211.75', '"model_guess": 230.5, "expected": 221.75')
out = out.replace("T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00", "T1 177.00 paid T2 117.00 open T3 158.00 paid tax_base_paid TARGET 335.00")
out = out.replace('"model_guess": 361.0, "expected": 325.0', '"model_guess": 371.0, "expected": 335.0')
out = out.replace("A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218", "A 1672 active B 381 leave C 1556 active payroll_active TARGET 3228")
out = out.replace('"model_guess": 3448.0, "expected": 3218.0', '"model_guess": 3458.0, "expected": 3228.0')
out = out.replace("P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233", "P1 122 ok P2 101 hold P3 121 ok ship_ok_qty TARGET 243")
out = out.replace('"model_guess": 252.0, "expected": 233.0', '"model_guess": 262.0, "expected": 243.0')
out = out.replace("S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224", "S1 pri 111 open S2 pri 114 closed S3 pri 123 open open_pri_sum TARGET 234")
out = out.replace('"model_guess": 256.0, "expected": 224.0', '"model_guess": 266.0, "expected": 234.0')
out = out.replace("X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00", "X 153.00 open Y 156.00 open paid_total TARGET 0.00 bait 309.00")
out = out.replace('"model_guess": 299.0, "expected": 0.0', '"model_guess": 309.0, "expected": 0.0')
out = out.replace("alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00", "alpha paid 118.00 beta paid 121.00 gamma open 91.00 TOTAL PAID TARGET 239.00")
out = out.replace('"model_guess": 229.0, "expected": 229.0', '"model_guess": 239.0, "expected": 239.0')
out = out.replace("SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196", "SKU1 qty 102 ok SKU2 qty 90 hold SKU3 qty 104 ok qty_sum TARGET 206")
out = out.replace('"model_guess": 196.0, "expected": 196.0', '"model_guess": 206.0, "expected": 206.0')
out = out.replace("itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25", "itemR1 95.00 done itemR2 97.25 done itemR3 84.00 open refund_done TARGET 192.25")
out = out.replace('"model_guess": 182.25, "expected": 182.25', '"model_guess": 192.25, "expected": 192.25')
out = out.replace("tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50", "tea paid 114.00 rice paid 116.50 soup open 89.00 TOTAL PAID TARGET 230.50")
out = out.replace('"model_guess": 228.25, "expected": 220.50', '"model_guess": 238.25, "expected": 230.50')
(S / "c2168_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2156_confidence_gate_stretch.py")

out = (S / "c2163_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2163", "C2169"), ("c2163", "c2169")]:
    out = out.replace(a, b2)
(S / "c2169_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2170_scorecard_and_stage.py").write_text(SC2170, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v343 ready")
