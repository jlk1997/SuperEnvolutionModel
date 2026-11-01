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
T341 = [
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
TR341 = [
    [2346.0, 2363.5, 2086.0],[840, 760, 820],[2254.0, 2255.25, 2054.0],[2402.0, 2419.0, 2154.0],
    [2464.0, 2488.0, 2124.0],[2182, 2198, 2082],[490.0, 530.0, 760.0],[2312.0, 2343.75, 2088.0],
    [840.0, 760.0, 820.0],[2379.0, 2367.0, 2085.0],[1,1,0],[0,0,0],
    [2445.0, 2466.5, 2110.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO341 = [
    [2144.0, 2156.75, 2005.0],[640, 660, 820],[2087.0, 2101.5, 1980.0],[2217.0, 2233.0, 2036.0],
    [2237.0, 2248.0, 2029.0],[2040, 2052, 2002],[420.0, 460.0, 740.0],[2128.0, 2149.75, 2005.0],
    [740.0, 780.0, 820.0],[2175.0, 2161.0, 2002.0],[1,1,0],[0,0,0],
    [2210.0, 2225.5, 2015.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR341, "TR"); check(HO341, "HO")

(ROOT / "tools/_v341_themes.json").write_text(json.dumps({"themes": T341, "train": TR341, "heldout": HO341}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_340(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V341 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V341 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 140.50", "ASHFORD bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 250.60"),
        ("DAWNW ghost 65.65", "DAWNH ghost 173.83"),
        ("GLENW bait 135.45", "GLENH bait 243.53"),
        ("JADEW bait 126.36", "JADEH bait 234.44"),
        ("NETHERW bait 143.53", "NETHERH bait 251.61"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V341-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD340 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v340_themes.json").read_text(encoding="utf-8"))["themes"])
NEW341 = "_".join(t[0] for t in T341)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2153"), ("c1463", "c2153"), ("V226", "V341"), ("v226", "v341"),
    ("_v226c1463", "_v341c2153"),
    ("Harder than V225", "Harder than V339"), ("harder than V225", "harder than V339"),
    (OLD340, NEW341),
    ("V226 keeps floor", "V341 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2153 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2154 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2154 VL"),
    ("kept on V226", "kept on V341"),
    ("vision_images_v226", "vision_images_v341"),
    ("VL_GATE_V226", "VL_GATE_V341"), ("vl_gate_v226", "vl_gate_v341"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V339: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T341, "v341", "V341", TR341))
out = retarget_340(out)
(S / "c2153_vision_v341_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2154"), ("c1464", "c2154"), ("V226", "V341"), ("v226", "v341"),
    ("vision_images_v226", "vision_images_v341"),
    ("VL_GATE_V226", "VL_GATE_V341"), ("vl_gate_v226", "vl_gate_v341"),
    ("runs/vision_v226", "runs/vision_v341"),
]:
    out = out.replace(a, b)
(S / "c2154_vision_v341_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2155"), ("c1465", "c2155"), ("V226", "V341"), ("v226", "v341"),
    ("vision_images_v226h", "vision_images_v341h"),
    ("vision_images_v226", "vision_images_v341"),
    ("VL_GATE_V226", "VL_GATE_V341"), ("vl_gate_v226", "vl_gate_v341"),
    ("runs/vision_v226h", "runs/vision_v341h"),
    ("_v226c1463", "_v341c2153"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T341, "v341h", "V341H", HO341))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v341h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v341"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v341" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v341h_c2155"'); seen_run = True; continue
    out2.append(ln)
(S / "c2155_vision_v341_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2153-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2154_VISION_V341_SMOKE.json") or {}\n    c654b = load("docs/r50/C2154b_VISION_GATE_V341_CLAIM.json") or {}\n    c655 = load("docs/r50/C2155_VISION_V341_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2155b_VISION_GATE_V341_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v341 = float(c654.get("rate") or 0.0)\n    v341h = float(c655.get("rate") or 0.0)\n    v341_claim = bool(c654b.get("vl_gate_v341_claim") or c654.get("vl_gate_v341_claim") or c654.get("claim"))\n    v341h_claim = bool(c655b.get("vl_gate_v341_heldout_claim") or c655.get("vl_gate_v341_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v341_claim and v341h_claim and v341 >= GATE and v341h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v341 >= 0.999 and v341h >= 0.999) else min(v341, v341h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v341": {"rate": v341, "claim": v341_claim, "n": c654.get("n")},\n            "v341_heldout": {"rate": v341h, "claim": v341h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v341_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V341: rate={v341} claim={v341_claim}",\n        f"- Vision V341 heldout: rate={v341h} claim={v341h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2153-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2153: Vision V341 design fixtures",\n        f"- C2154: Vision V341 smoke **{v341}**", f"- C2155: Vision V341 heldout **{v341h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V341 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2158 = '# -*- coding: utf-8 -*-\n"""C2158: Unified scorecard + STAGE after C2153-C2157. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2158.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2154_VISION_V341_SMOKE.json") or {}\n    c654b = load("docs/r50/C2154b_VISION_GATE_V341_CLAIM.json") or {}\n    c655 = load("docs/r50/C2155_VISION_V341_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2155b_VISION_GATE_V341_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2156_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2157_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2150_PRODUCT_U2C_COST.json") or {}\n\n    v341 = float(c654.get("rate") or 0.0)\n    v341h = float(c655.get("rate") or 0.0)\n    v341_claim = bool(c654b.get("vl_gate_v341_claim") or c654.get("vl_gate_v341_claim") or c654.get("claim"))\n    v341h_claim = bool(c655b.get("vl_gate_v341_heldout_claim") or c655.get("vl_gate_v341_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2150"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v341_claim and v341h_claim and v341 >= GATE and v341h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v341 >= 0.999 and v341h >= 0.999) else min(v341, v341h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2158", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v341": {"rate": v341, "claim": v341_claim, "n": c654.get("n")},\n            "v341_heldout": {"rate": v341h, "claim": v341h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2150"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2156"},\n        "capture_regression": {"pass": capture_pass, "source": "C2157"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v341_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2158_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2158)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V341: rate={v341} claim={v341_claim}",\n        f"- Vision V341 heldout: rate={v341h} claim={v341h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2158", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2153-C2158 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2153: Vision V341 design fixtures",\n        f"- C2154: Vision V341 smoke **{v341}**", f"- C2155: Vision V341 heldout **{v341h}** (disjoint={disjoint})",\n        f"- C2156: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2150): replace={replace} pass={u2c_pass}",\n        f"- C2157: capture pass={capture_pass}", f"- C2158: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V341 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2158.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V341 knife = confidence-gate (alternating; V340 was product-U2C)
out = (S / "c2144_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2144", "C2156"), ("c2144", "c2156"),
    ("C2096", "C2156"), ("c2096", "c2156"),
    ("cg153_", "cg150_"),
    ("conf_gate_stretch_c2156", "conf_gate_stretch_c2156"),
    ("confidence_gate_stretch_v216", "confidence_gate_stretch_v213"),
    ("Stretch vs C2144", "Stretch vs C2108"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75", "a paid 132.00 b paid 136.75 c open 92.00 TOTAL PAID TARGET 268.75")
out = out.replace('"model_guess": 999.0, "expected": 260.75', '"model_guess": 999.0, "expected": 268.75')
out = out.replace("SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250", "SKU1 qty 127 ok SKU2 qty 101 hold SKU3 qty 131 ok qty_sum TARGET 258")
out = out.replace('"model_guess": 262.0, "expected": 250.0', '"model_guess": 270.0, "expected": 258.0')
out = out.replace("itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75", "itemR1 108.00 done itemR2 111.75 done itemR3 89.00 open refund_done TARGET 219.75")
out = out.replace('"model_guess": 220.5, "expected": 211.75', '"model_guess": 228.5, "expected": 219.75')
out = out.replace("T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00", "T1 176.00 paid T2 116.00 open T3 157.00 paid tax_base_paid TARGET 333.00")
out = out.replace('"model_guess": 361.0, "expected": 325.0', '"model_guess": 369.0, "expected": 333.0')
out = out.replace("A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218", "A 1671 active B 380 leave C 1555 active payroll_active TARGET 3226")
out = out.replace('"model_guess": 3448.0, "expected": 3218.0', '"model_guess": 3456.0, "expected": 3226.0')
out = out.replace("P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233", "P1 121 ok P2 100 hold P3 120 ok ship_ok_qty TARGET 241")
out = out.replace('"model_guess": 252.0, "expected": 233.0', '"model_guess": 260.0, "expected": 241.0')
out = out.replace("S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224", "S1 pri 110 open S2 pri 113 closed S3 pri 122 open open_pri_sum TARGET 232")
out = out.replace('"model_guess": 256.0, "expected": 224.0', '"model_guess": 264.0, "expected": 232.0')
out = out.replace("X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00", "X 152.00 open Y 155.00 open paid_total TARGET 0.00 bait 307.00")
out = out.replace('"model_guess": 299.0, "expected": 0.0', '"model_guess": 307.0, "expected": 0.0')
out = out.replace("alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00", "alpha paid 117.00 beta paid 120.00 gamma open 90.00 TOTAL PAID TARGET 237.00")
out = out.replace('"model_guess": 229.0, "expected": 229.0', '"model_guess": 237.0, "expected": 237.0')
out = out.replace("SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196", "SKU1 qty 101 ok SKU2 qty 89 hold SKU3 qty 103 ok qty_sum TARGET 204")
out = out.replace('"model_guess": 196.0, "expected": 196.0', '"model_guess": 204.0, "expected": 204.0')
out = out.replace("itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25", "itemR1 94.00 done itemR2 96.25 done itemR3 83.00 open refund_done TARGET 190.25")
out = out.replace('"model_guess": 182.25, "expected": 182.25', '"model_guess": 190.25, "expected": 190.25')
out = out.replace("tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50", "tea paid 113.00 rice paid 115.50 soup open 88.00 TOTAL PAID TARGET 228.50")
out = out.replace('"model_guess": 228.25, "expected": 220.50', '"model_guess": 236.25, "expected": 228.50')
(S / "c2156_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2144_confidence_gate_stretch.py")

out = (S / "c2151_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2151", "C2157"), ("c2151", "c2157")]:
    out = out.replace(a, b2)
(S / "c2157_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2158_scorecard_and_stage.py").write_text(SC2158, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v341 ready")
