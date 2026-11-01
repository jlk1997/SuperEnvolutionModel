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

# *brook ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T339 = [
    ["ashbrook","recv","paid_total","ASHBROOK GRAIN RECV","RECV","x"],
    ["cedarbrook","wh","qty_sum","WH CEDARBROOK BIN","RECV","x"],
    ["dawnbrook","refund","refund_done","DAWNBROOK PATCH REFUND","DONE","x"],
    ["elmbrook","tax","tax_base_paid","ELMBROOK TAX SLIP","TAX","x"],
    ["fernbrook","pay","payroll_active","FERNBROOK PAYROLL","PAY","x"],
    ["glenbrook","ship","ship_ok","GLENBROOK SHIP DOCK","SHIP","x"],
    ["hazebrook","sla","sla_ok_hours","HAZEBROOK SLA CARD","SLA","x"],
    ["inkbrook","exp","exp_sum","INKBROOK EXPENSE","EXP","x"],
    ["jadebrook","po","po_open","JADEBROOK PO SHEET","PO","x"],
    ["knotbrook","order","order_paid","KNOTBROOK ORDER","ORD","x"],
    ["lakebrook","dup","dup_mark","LAKEBROOK DUP MARK","DUP","x"],
    ["mossbrook","zero","zero_check","MOSSBROOK AIR ZERO","ZERO","x"],
    ["netherbrook","ledger","ledger_net","NETHERBROOK LEDGER","LED","x"],
    ["oakbrook","ui","ui_ok","OAKBROOK UI SCAN","UI","x"],
    ["pinebrook","stack","stack_count","PINEBROOK STACK","STK","x"],
    ["quillbrook","fax","fax_pages","QUILLBROOK FAX","FAX","x"],
    ["reedbrook","glare","glare_ok","REEDBROOK GLARE","GLR","x"],
    ["stonebrook","tab","tab_index","STONEBROOK TAB INDEX","TAB","x"],
]
TR339 = [
    [2342.0, 2359.5, 2082.0],[840, 760, 820],[2252.0, 2258.25, 2052.0],[2398.0, 2415.0, 2150.0],
    [2460.0, 2484.0, 2120.0],[2178, 2194, 2078],[490.0, 530.0, 760.0],[2308.0, 2339.75, 2084.0],
    [840.0, 760.0, 820.0],[2375.0, 2363.0, 2081.0],[1,1,0],[0,0,0],
    [2441.0, 2462.5, 2106.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO339 = [
    [2140.0, 2152.75, 2001.0],[640, 660, 820],[2083.0, 2097.5, 1976.0],[2213.0, 2229.0, 2032.0],
    [2239.0, 2250.0, 2025.0],[2036, 2048, 1998],[420.0, 460.0, 740.0],[2124.0, 2145.75, 2001.0],
    [740.0, 780.0, 820.0],[2171.0, 2157.0, 1998.0],[1,1,0],[0,0,0],
    [2206.0, 2221.5, 2011.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR339, "TR"); check(HO339, "HO")

(ROOT / "tools/_v339_themes.json").write_text(json.dumps({"themes": T339, "train": TR339, "heldout": HO339}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_338(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V339 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V339 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 140.50", "ASHBROOK bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 250.60"),
        ("DAWNW ghost 65.65", "DAWNH ghost 173.83"),
        ("GLENW bait 135.45", "GLENH bait 243.53"),
        ("JADEW bait 126.36", "JADEH bait 234.44"),
        ("NETHERW bait 143.53", "NETHERH bait 251.61"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V339-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD338 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v338_themes.json").read_text(encoding="utf-8"))["themes"])
NEW339 = "_".join(t[0] for t in T339)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2141"), ("c1463", "c2141"), ("V226", "V339"), ("v226", "v339"),
    ("_v226c1463", "_v339c2141"),
    ("Harder than V225", "Harder than V337"), ("harder than V225", "harder than V337"),
    (OLD338, NEW339),
    ("V226 keeps floor", "V339 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2141 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2142 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2142 VL"),
    ("kept on V226", "kept on V339"),
    ("vision_images_v226", "vision_images_v339"),
    ("VL_GATE_V226", "VL_GATE_V339"), ("vl_gate_v226", "vl_gate_v339"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V337: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T339, "v339", "V339", TR339))
out = retarget_338(out)
(S / "c2141_vision_v339_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2142"), ("c1464", "c2142"), ("V226", "V339"), ("v226", "v339"),
    ("vision_images_v226", "vision_images_v339"),
    ("VL_GATE_V226", "VL_GATE_V339"), ("vl_gate_v226", "vl_gate_v339"),
    ("runs/vision_v226", "runs/vision_v339"),
]:
    out = out.replace(a, b)
(S / "c2142_vision_v339_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2143"), ("c1465", "c2143"), ("V226", "V339"), ("v226", "v339"),
    ("vision_images_v226h", "vision_images_v339h"),
    ("vision_images_v226", "vision_images_v339"),
    ("VL_GATE_V226", "VL_GATE_V339"), ("vl_gate_v226", "vl_gate_v339"),
    ("runs/vision_v226h", "runs/vision_v339h"),
    ("_v226c1463", "_v339c2141"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T339, "v339h", "V339H", HO339))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v339h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v339"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v339" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v339h_c2143"'); seen_run = True; continue
    out2.append(ln)
(S / "c2143_vision_v339_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2141-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2142_VISION_V339_SMOKE.json") or {}\n    c654b = load("docs/r50/C2142b_VISION_GATE_V339_CLAIM.json") or {}\n    c655 = load("docs/r50/C2143_VISION_V339_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2143b_VISION_GATE_V339_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v339 = float(c654.get("rate") or 0.0)\n    v339h = float(c655.get("rate") or 0.0)\n    v339_claim = bool(c654b.get("vl_gate_v339_claim") or c654.get("vl_gate_v339_claim") or c654.get("claim"))\n    v339h_claim = bool(c655b.get("vl_gate_v339_heldout_claim") or c655.get("vl_gate_v339_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v339_claim and v339h_claim and v339 >= GATE and v339h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v339 >= 0.999 and v339h >= 0.999) else min(v339, v339h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v339": {"rate": v339, "claim": v339_claim, "n": c654.get("n")},\n            "v339_heldout": {"rate": v339h, "claim": v339h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v339_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V339: rate={v339} claim={v339_claim}",\n        f"- Vision V339 heldout: rate={v339h} claim={v339h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2141-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2141: Vision V339 design fixtures",\n        f"- C2142: Vision V339 smoke **{v339}**", f"- C2143: Vision V339 heldout **{v339h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V339 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2146 = '# -*- coding: utf-8 -*-\n"""C2146: Unified scorecard + STAGE after C2141-C2145. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2146.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2142_VISION_V339_SMOKE.json") or {}\n    c654b = load("docs/r50/C2142b_VISION_GATE_V339_CLAIM.json") or {}\n    c655 = load("docs/r50/C2143_VISION_V339_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2143b_VISION_GATE_V339_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2144_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2145_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2138_PRODUCT_U2C_COST.json") or {}\n\n    v339 = float(c654.get("rate") or 0.0)\n    v339h = float(c655.get("rate") or 0.0)\n    v339_claim = bool(c654b.get("vl_gate_v339_claim") or c654.get("vl_gate_v339_claim") or c654.get("claim"))\n    v339h_claim = bool(c655b.get("vl_gate_v339_heldout_claim") or c655.get("vl_gate_v339_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2138"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v339_claim and v339h_claim and v339 >= GATE and v339h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v339 >= 0.999 and v339h >= 0.999) else min(v339, v339h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2146", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v339": {"rate": v339, "claim": v339_claim, "n": c654.get("n")},\n            "v339_heldout": {"rate": v339h, "claim": v339h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2138"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2144"},\n        "capture_regression": {"pass": capture_pass, "source": "C2145"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v339_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2146_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2146)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V339: rate={v339} claim={v339_claim}",\n        f"- Vision V339 heldout: rate={v339h} claim={v339h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2146", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2141-C2146 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2141: Vision V339 design fixtures",\n        f"- C2142: Vision V339 smoke **{v339}**", f"- C2143: Vision V339 heldout **{v339h}** (disjoint={disjoint})",\n        f"- C2144: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2138): replace={replace} pass={u2c_pass}",\n        f"- C2145: capture pass={capture_pass}", f"- C2146: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V339 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2146.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V339 knife = confidence-gate (alternating; V338 was product-U2C)
out = (S / "c2132_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2132", "C2144"), ("c2132", "c2144"),
    ("C2096", "C2144"), ("c2096", "c2144"),
    ("cg152_", "cg150_"),
    ("conf_gate_stretch_c2144", "conf_gate_stretch_c2144"),
    ("confidence_gate_stretch_v215", "confidence_gate_stretch_v213"),
    ("Stretch vs C2132", "Stretch vs C2108"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75", "a paid 131.00 b paid 135.75 c open 91.00 TOTAL PAID TARGET 266.75")
out = out.replace('"model_guess": 999.0, "expected": 260.75', '"model_guess": 999.0, "expected": 266.75')
out = out.replace("SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250", "SKU1 qty 126 ok SKU2 qty 100 hold SKU3 qty 130 ok qty_sum TARGET 256")
out = out.replace('"model_guess": 262.0, "expected": 250.0', '"model_guess": 268.0, "expected": 256.0')
out = out.replace("itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75", "itemR1 107.00 done itemR2 110.75 done itemR3 88.00 open refund_done TARGET 217.75")
out = out.replace('"model_guess": 220.5, "expected": 211.75', '"model_guess": 226.5, "expected": 217.75')
out = out.replace("T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00", "T1 175.00 paid T2 115.00 open T3 156.00 paid tax_base_paid TARGET 331.00")
out = out.replace('"model_guess": 361.0, "expected": 325.0', '"model_guess": 367.0, "expected": 331.0')
out = out.replace("A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218", "A 1670 active B 379 leave C 1554 active payroll_active TARGET 3224")
out = out.replace('"model_guess": 3448.0, "expected": 3218.0', '"model_guess": 3454.0, "expected": 3224.0')
out = out.replace("P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233", "P1 120 ok P2 99 hold P3 119 ok ship_ok_qty TARGET 239")
out = out.replace('"model_guess": 252.0, "expected": 233.0', '"model_guess": 258.0, "expected": 239.0')
out = out.replace("S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224", "S1 pri 109 open S2 pri 112 closed S3 pri 121 open open_pri_sum TARGET 230")
out = out.replace('"model_guess": 256.0, "expected": 224.0', '"model_guess": 262.0, "expected": 230.0')
out = out.replace("X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00", "X 151.00 open Y 154.00 open paid_total TARGET 0.00 bait 305.00")
out = out.replace('"model_guess": 299.0, "expected": 0.0', '"model_guess": 305.0, "expected": 0.0')
out = out.replace("alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00", "alpha paid 116.00 beta paid 119.00 gamma open 89.00 TOTAL PAID TARGET 235.00")
out = out.replace('"model_guess": 229.0, "expected": 229.0', '"model_guess": 235.0, "expected": 235.0')
out = out.replace("SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196", "SKU1 qty 100 ok SKU2 qty 88 hold SKU3 qty 102 ok qty_sum TARGET 202")
out = out.replace('"model_guess": 196.0, "expected": 196.0', '"model_guess": 202.0, "expected": 202.0')
out = out.replace("itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25", "itemR1 93.00 done itemR2 95.25 done itemR3 82.00 open refund_done TARGET 188.25")
out = out.replace('"model_guess": 182.25, "expected": 182.25', '"model_guess": 188.25, "expected": 188.25')
out = out.replace("tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50", "tea paid 112.00 rice paid 114.50 soup open 87.00 TOTAL PAID TARGET 226.50")
out = out.replace('"model_guess": 228.25, "expected": 220.50', '"model_guess": 234.25, "expected": 226.50')
(S / "c2144_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2132_confidence_gate_stretch.py")

out = (S / "c2139_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2139", "C2145"), ("c2139", "c2145")]:
    out = out.replace(a, b2)
(S / "c2145_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2146_scorecard_and_stage.py").write_text(SC2146, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v339 ready")
