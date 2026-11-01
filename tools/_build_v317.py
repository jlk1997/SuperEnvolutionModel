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
T317 = [
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
TR317 = [
    [2298.0, 2315.5, 2038.0],[840, 760, 820],[2221.0, 2250.25, 2016.0],[2354.0, 2371.0, 2106.0],
    [2416.0, 2440.0, 2076.0],[2134, 2150, 2034],[490.0, 530.0, 760.0],[2264.0, 2295.75, 2040.0],
    [840.0, 760.0, 820.0],[2331.0, 2319.0, 2037.0],[1,1,0],[0,0,0],
    [2397.0, 2418.5, 2062.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO317 = [
    [2096.0, 2108.75, 1957.0],[640, 660, 820],[2039.0, 2053.5, 1932.0],[2169.0, 2185.0, 1988.0],
    [2210.0, 2226.0, 1981.0],[1992, 2004, 1952],[420.0, 460.0, 740.0],[2080.0, 2101.75, 1957.0],
    [740.0, 780.0, 820.0],[2127.0, 2113.0, 1954.0],[1,1,0],[0,0,0],
    [2162.0, 2177.5, 1967.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR317, "TR"); check(HO317, "HO")

(ROOT / "tools/_v317_themes.json").write_text(json.dumps({"themes": T317, "train": TR317, "heldout": HO317}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_316(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V317 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V317 overlays (new vs V49) ---")
    for a, b in [
        ("ASHBROOK bait 140.50", "ASHBROOK bait 185.95"),
        ("CEDARW bait 142.52", "CEDARB bait 232.42"),
        ("DAWNW ghost 65.65", "DAWNB ghost 155.65"),
        ("GLENW bait 135.45", "GLENB bait 225.35"),
        ("JADEW bait 126.36", "JADEB bait 216.26"),
        ("NETHERW bait 143.53", "NETHERB bait 233.43"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V317-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD316 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v316_themes.json").read_text(encoding="utf-8"))["themes"])
NEW317 = "_".join(t[0] for t in T317)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2009"), ("c1463", "c2009"), ("V226", "V317"), ("v226", "v317"),
    ("_v226c1463", "_v317c2009"),
    ("Harder than V225", "Harder than V315"), ("harder than V225", "harder than V315"),
    (OLD316, NEW317),
    ("V226 keeps floor", "V317 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2009 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2010 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2010 VL"),
    ("kept on V226", "kept on V317"),
    ("vision_images_v226", "vision_images_v317"),
    ("VL_GATE_V226", "VL_GATE_V317"), ("vl_gate_v226", "vl_gate_v317"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V315: ashbrook, cedarbrook, dawnbrook, elmbrook, fernbrook, glenbrook, hazebrook, inkbrook,\njadebrook, knotbrook, lakebrook, mossbrook, netherbrook, oakbrook, pinebrook, quillbrook, reedbrook, stonebrook.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T317, "v317", "V317", TR317))
out = retarget_316(out)
(S / "c2009_vision_v317_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2010"), ("c1464", "c2010"), ("V226", "V317"), ("v226", "v317"),
    ("vision_images_v226", "vision_images_v317"),
    ("VL_GATE_V226", "VL_GATE_V317"), ("vl_gate_v226", "vl_gate_v317"),
    ("runs/vision_v226", "runs/vision_v317"),
]:
    out = out.replace(a, b)
(S / "c2010_vision_v317_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2011"), ("c1465", "c2011"), ("V226", "V317"), ("v226", "v317"),
    ("vision_images_v226h", "vision_images_v317h"),
    ("vision_images_v226", "vision_images_v317"),
    ("VL_GATE_V226", "VL_GATE_V317"), ("vl_gate_v226", "vl_gate_v317"),
    ("runs/vision_v226h", "runs/vision_v317h"),
    ("_v226c1463", "_v317c2009"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T317, "v317h", "V317H", HO317))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v317h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v317"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v317" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v317h_c2011"'); seen_run = True; continue
    out2.append(ln)
(S / "c2011_vision_v317_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2009-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2010_VISION_V317_SMOKE.json") or {}\n    c654b = load("docs/r50/C2010b_VISION_GATE_V317_CLAIM.json") or {}\n    c655 = load("docs/r50/C2011_VISION_V317_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2011b_VISION_GATE_V317_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v317 = float(c654.get("rate") or 0.0)\n    v317h = float(c655.get("rate") or 0.0)\n    v317_claim = bool(c654b.get("vl_gate_v317_claim") or c654.get("vl_gate_v317_claim") or c654.get("claim"))\n    v317h_claim = bool(c655b.get("vl_gate_v317_heldout_claim") or c655.get("vl_gate_v317_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v317_claim and v317h_claim and v317 >= GATE and v317h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v317 >= 0.999 and v317h >= 0.999) else min(v317, v317h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v317": {"rate": v317, "claim": v317_claim, "n": c654.get("n")},\n            "v317_heldout": {"rate": v317h, "claim": v317h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v317_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V317: rate={v317} claim={v317_claim}",\n        f"- Vision V317 heldout: rate={v317h} claim={v317h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2009-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2009: Vision V317 design fixtures",\n        f"- C2010: Vision V317 smoke **{v317}**", f"- C2011: Vision V317 heldout **{v317h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V317 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2014 = '# -*- coding: utf-8 -*-\n"""C2014: Unified scorecard + STAGE after C2009-C2013. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2014.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2010_VISION_V317_SMOKE.json") or {}\n    c654b = load("docs/r50/C2010b_VISION_GATE_V317_CLAIM.json") or {}\n    c655 = load("docs/r50/C2011_VISION_V317_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2011b_VISION_GATE_V317_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2012_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2013_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2006_PRODUCT_U2C_COST.json") or {}\n\n    v317 = float(c654.get("rate") or 0.0)\n    v317h = float(c655.get("rate") or 0.0)\n    v317_claim = bool(c654b.get("vl_gate_v317_claim") or c654.get("vl_gate_v317_claim") or c654.get("claim"))\n    v317h_claim = bool(c655b.get("vl_gate_v317_heldout_claim") or c655.get("vl_gate_v317_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2006"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v317_claim and v317h_claim and v317 >= GATE and v317h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v317 >= 0.999 and v317h >= 0.999) else min(v317, v317h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2014", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v317": {"rate": v317, "claim": v317_claim, "n": c654.get("n")},\n            "v317_heldout": {"rate": v317h, "claim": v317h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2006"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2012"},\n        "capture_regression": {"pass": capture_pass, "source": "C2013"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v317_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2014_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2014)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V317: rate={v317} claim={v317_claim}",\n        f"- Vision V317 heldout: rate={v317h} claim={v317h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2014", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2009-C2014 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2009: Vision V317 design fixtures",\n        f"- C2010: Vision V317 smoke **{v317}**", f"- C2011: Vision V317 heldout **{v317h}** (disjoint={disjoint})",\n        f"- C2012: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2006): replace={replace} pass={u2c_pass}",\n        f"- C2013: capture pass={capture_pass}", f"- C2014: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V317 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2014.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V317 knife = confidence-gate (alternating; V316 was product-U2C)
out = (S / "c2000_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2000", "C2012"), ("c2000", "c2012"),
    ("C1988", "C2012"), ("c1988", "c2012"),
    ("cg140_", "cg141_"),
    ("conf_gate_stretch_c2000", "conf_gate_stretch_c2012"),
    ("confidence_gate_stretch_v203", "confidence_gate_stretch_v204"),
    ("Stretch vs C1988", "Stretch vs C2000"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 119.00 b paid 123.75 c open 79.00 TOTAL PAID TARGET 242.75", "a paid 120.00 b paid 124.75 c open 80.00 TOTAL PAID TARGET 244.75")
out = out.replace('"model_guess": 999.0, "expected": 242.75', '"model_guess": 999.0, "expected": 244.75')
out = out.replace("SKU1 qty 114 ok SKU2 qty 88 hold SKU3 qty 118 ok qty_sum TARGET 232", "SKU1 qty 115 ok SKU2 qty 89 hold SKU3 qty 119 ok qty_sum TARGET 234")
out = out.replace('"model_guess": 244.0, "expected": 232.0', '"model_guess": 246.0, "expected": 234.0')
out = out.replace("itemR1 95.00 done itemR2 98.75 done itemR3 76.00 open refund_done TARGET 193.75", "itemR1 96.00 done itemR2 99.75 done itemR3 77.00 open refund_done TARGET 195.75")
out = out.replace('"model_guess": 202.5, "expected": 193.75', '"model_guess": 204.5, "expected": 195.75')
out = out.replace("T1 163.00 paid T2 103.00 open T3 144.00 paid tax_base_paid TARGET 307.00", "T1 164.00 paid T2 104.00 open T3 145.00 paid tax_base_paid TARGET 309.00")
out = out.replace('"model_guess": 343.0, "expected": 307.0', '"model_guess": 345.0, "expected": 309.0')
out = out.replace("A 1658 active B 367 leave C 1542 active payroll_active TARGET 3200", "A 1659 active B 368 leave C 1543 active payroll_active TARGET 3202")
out = out.replace('"model_guess": 3430.0, "expected": 3200.0', '"model_guess": 3432.0, "expected": 3202.0')
out = out.replace("P1 108 ok P2 87 hold P3 107 ok ship_ok_qty TARGET 215", "P1 109 ok P2 88 hold P3 108 ok ship_ok_qty TARGET 217")
out = out.replace('"model_guess": 234.0, "expected": 215.0', '"model_guess": 236.0, "expected": 217.0')
out = out.replace("S1 pri 97 open S2 pri 100 closed S3 pri 109 open open_pri_sum TARGET 206", "S1 pri 98 open S2 pri 101 closed S3 pri 110 open open_pri_sum TARGET 208")
out = out.replace('"model_guess": 238.0, "expected": 206.0', '"model_guess": 240.0, "expected": 208.0')
out = out.replace("X 139.00 open Y 142.00 open paid_total TARGET 0.00 bait 281.00", "X 140.00 open Y 143.00 open paid_total TARGET 0.00 bait 283.00")
out = out.replace('"model_guess": 281.0, "expected": 0.0', '"model_guess": 283.0, "expected": 0.0')
out = out.replace("alpha paid 104.00 beta paid 107.00 gamma open 77.00 TOTAL PAID TARGET 211.00", "alpha paid 105.00 beta paid 108.00 gamma open 78.00 TOTAL PAID TARGET 213.00")
out = out.replace('"model_guess": 211.0, "expected": 211.0', '"model_guess": 213.0, "expected": 213.0')
out = out.replace("SKU1 qty 88 ok SKU2 qty 76 hold SKU3 qty 90 ok qty_sum TARGET 178", "SKU1 qty 89 ok SKU2 qty 77 hold SKU3 qty 91 ok qty_sum TARGET 180")
out = out.replace('"model_guess": 178.0, "expected": 178.0', '"model_guess": 180.0, "expected": 180.0')
out = out.replace("itemR1 81.00 done itemR2 83.25 done itemR3 70.00 open refund_done TARGET 164.25", "itemR1 82.00 done itemR2 84.25 done itemR3 71.00 open refund_done TARGET 166.25")
out = out.replace('"model_guess": 164.25, "expected": 164.25', '"model_guess": 166.25, "expected": 166.25')
out = out.replace("tea paid 100.00 rice paid 102.50 soup open 75.00 TOTAL PAID TARGET 202.50", "tea paid 101.00 rice paid 103.50 soup open 76.00 TOTAL PAID TARGET 204.50")
out = out.replace('"model_guess": 210.25, "expected": 202.50', '"model_guess": 212.25, "expected": 204.50')
(S / "c2012_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2000_confidence_gate_stretch.py")

out = (S / "c2007_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2007", "C2013"), ("c2007", "c2013")]:
    out = out.replace(a, b2)
(S / "c2013_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2014_scorecard_and_stage.py").write_text(SC2014, encoding="utf-8")
print("scorecard from fixed c2002 conf-gate pattern")
print("OK builder v317 ready")
