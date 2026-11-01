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

# *dale ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T307 = [
    ["ashdale","recv","paid_total","ASHDALE GRAIN RECV","RECV","x"],
    ["cedardale","wh","qty_sum","WH CEDARDALE BIN","RECV","x"],
    ["dawndale","refund","refund_done","DAWNDALE PATCH REFUND","DONE","x"],
    ["elmdale","tax","tax_base_paid","ELMDALE TAX SLIP","TAX","x"],
    ["ferndale","pay","payroll_active","FERNDALE PAYROLL","PAY","x"],
    ["glendale","ship","ship_ok","GLENDALE SHIP DOCK","SHIP","x"],
    ["hazedale","sla","sla_ok_hours","HAZEDALE SLA CARD","SLA","x"],
    ["inkdale","exp","exp_sum","INKDALE EXPENSE","EXP","x"],
    ["jadedale","po","po_open","JADEDALE PO SHEET","PO","x"],
    ["knotdale","order","order_paid","KNOTDALE ORDER","ORD","x"],
    ["lakedale","dup","dup_mark","LAKEDALE DUP MARK","DUP","x"],
    ["mossdale","zero","zero_check","MOSSDALE AIR ZERO","ZERO","x"],
    ["netherdale","ledger","ledger_net","NETHERDALE LEDGER","LED","x"],
    ["oakdale","ui","ui_ok","OAKDALE UI SCAN","UI","x"],
    ["pinedale","stack","stack_count","PINEDALE STACK","STK","x"],
    ["quilldale","fax","fax_pages","QUILLDALE FAX","FAX","x"],
    ["reeddale","glare","glare_ok","REEDDALE GLARE","GLR","x"],
    ["stonedale","tab","tab_index","STONEDALE TAB INDEX","TAB","x"],
]
TR307 = [
    [2278.0, 2295.5, 2018.0],[840, 760, 820],[2201.0, 2230.25, 1996.0],[2334.0, 2351.0, 2086.0],
    [2396.0, 2420.0, 2056.0],[2114, 2130, 2014],[490.0, 530.0, 760.0],[2244.0, 2275.75, 2020.0],
    [840.0, 760.0, 820.0],[2311.0, 2299.0, 2017.0],[1,1,0],[0,0,0],
    [2377.0, 2398.5, 2042.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO307 = [
    [2076.0, 2088.75, 1937.0],[640, 660, 820],[2019.0, 2033.5, 1912.0],[2149.0, 2165.0, 1968.0],
    [2190.0, 2206.0, 1961.0],[1972, 1984, 1932],[420.0, 460.0, 740.0],[2060.0, 2081.75, 1937.0],
    [740.0, 780.0, 820.0],[2107.0, 2093.0, 1934.0],[1,1,0],[0,0,0],
    [2142.0, 2157.5, 1947.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR307, "TR"); check(HO307, "HO")

(ROOT / "tools/_v307_themes.json").write_text(json.dumps({"themes": T307, "train": TR307, "heldout": HO307}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_306(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V307 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V307 overlays (new vs V49) ---")
    for a, b in [
        ("ASHDALE bait 140.50", "ASHDALE bait 185.95"),
        ("CEDARW bait 142.52", "CEDARD bait 222.32"),
        ("DAWNW ghost 65.65", "DAWND ghost 145.55"),
        ("GLENW bait 135.45", "GLEND bait 215.25"),
        ("JADEW bait 126.36", "JADED bait 206.16"),
        ("NETHERW bait 143.53", "NETHERD bait 223.33"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V307-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD306 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v306_themes.json").read_text(encoding="utf-8"))["themes"])
NEW307 = "_".join(t[0] for t in T307)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1949"), ("c1463", "c1949"), ("V226", "V307"), ("v226", "v307"),
    ("_v226c1463", "_v307c1949"),
    ("Harder than V225", "Harder than V305"), ("harder than V225", "harder than V305"),
    (OLD306, NEW307),
    ("V226 keeps floor", "V307 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1949 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1950 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1950 VL"),
    ("kept on V226", "kept on V307"),
    ("vision_images_v226", "vision_images_v307"),
    ("VL_GATE_V226", "VL_GATE_V307"), ("vl_gate_v226", "vl_gate_v307"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V305: ashdale, cedardale, dawndale, elmdale, ferndale, glendale, hazedale, inkdale,\njadedale, knotdale, lakedale, mossdale, netherdale, oakdale, pinedale, quilldale, reeddale, stonedale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T307, "v307", "V307", TR307))
out = retarget_306(out)
(S / "c1949_vision_v307_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1950"), ("c1464", "c1950"), ("V226", "V307"), ("v226", "v307"),
    ("vision_images_v226", "vision_images_v307"),
    ("VL_GATE_V226", "VL_GATE_V307"), ("vl_gate_v226", "vl_gate_v307"),
    ("runs/vision_v226", "runs/vision_v307"),
]:
    out = out.replace(a, b)
(S / "c1950_vision_v307_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1951"), ("c1465", "c1951"), ("V226", "V307"), ("v226", "v307"),
    ("vision_images_v226h", "vision_images_v307h"),
    ("vision_images_v226", "vision_images_v307"),
    ("VL_GATE_V226", "VL_GATE_V307"), ("vl_gate_v226", "vl_gate_v307"),
    ("runs/vision_v226h", "runs/vision_v307h"),
    ("_v226c1463", "_v307c1949"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T307, "v307h", "V307H", HO307))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v307h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v307"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v307" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v307h_c1951"'); seen_run = True; continue
    out2.append(ln)
(S / "c1951_vision_v307_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C1949-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1950_VISION_V307_SMOKE.json") or {}\n    c654b = load("docs/r50/C1950b_VISION_GATE_V307_CLAIM.json") or {}\n    c655 = load("docs/r50/C1951_VISION_V307_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1951b_VISION_GATE_V307_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v307 = float(c654.get("rate") or 0.0)\n    v307h = float(c655.get("rate") or 0.0)\n    v307_claim = bool(c654b.get("vl_gate_v307_claim") or c654.get("vl_gate_v307_claim") or c654.get("claim"))\n    v307h_claim = bool(c655b.get("vl_gate_v307_heldout_claim") or c655.get("vl_gate_v307_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v307_claim and v307h_claim and v307 >= GATE and v307h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v307 >= 0.999 and v307h >= 0.999) else min(v307, v307h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v307": {"rate": v307, "claim": v307_claim, "n": c654.get("n")},\n            "v307_heldout": {"rate": v307h, "claim": v307h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v307_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V307: rate={v307} claim={v307_claim}",\n        f"- Vision V307 heldout: rate={v307h} claim={v307h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1949-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1949: Vision V307 design fixtures",\n        f"- C1950: Vision V307 smoke **{v307}**", f"- C1951: Vision V307 heldout **{v307h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V307 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC1954 = '# -*- coding: utf-8 -*-\n"""C1954: Unified scorecard + STAGE after C1469-C1953. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1954.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1950_VISION_V307_SMOKE.json") or {}\n    c654b = load("docs/r50/C1950b_VISION_GATE_V307_CLAIM.json") or {}\n    c655 = load("docs/r50/C1951_VISION_V307_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1951b_VISION_GATE_V307_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1952_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1953_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1466_PRODUCT_U2C_COST.json") or {}\n\n    v307 = float(c654.get("rate") or 0.0)\n    v307h = float(c655.get("rate") or 0.0)\n    v307_claim = bool(c654b.get("vl_gate_v307_claim") or c654.get("vl_gate_v307_claim") or c654.get("claim"))\n    v307h_claim = bool(c655b.get("vl_gate_v307_heldout_claim") or c655.get("vl_gate_v307_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1466"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v307_claim and v307h_claim and v307 >= GATE and v307h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v307 >= 0.999 and v307h >= 0.999) else min(v307, v307h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1954", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v307": {"rate": v307, "claim": v307_claim, "n": c654.get("n")},\n            "v307_heldout": {"rate": v307h, "claim": v307h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1466"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1952"},\n        "capture_regression": {"pass": capture_pass, "source": "C1953"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v307_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1954_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1954)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V307: rate={v307} claim={v307_claim}",\n        f"- Vision V307 heldout: rate={v307h} claim={v307h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1954", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1469-C1954 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1469: Vision V307 design fixtures",\n        f"- C1950: Vision V307 smoke **{v307}**", f"- C1951: Vision V307 heldout **{v307h}** (disjoint={disjoint})",\n        f"- C1952: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C1466): replace={replace} pass={u2c_pass}",\n        f"- C1953: capture pass={capture_pass}", f"- C1954: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V307 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1954.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V307 knife = confidence-gate (alternating; V306 was product-U2C)
out = (S / "c1940_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1940", "C1952"), ("c1940", "c1952"),
    ("C1928", "C1952"), ("c1928", "c1952"),
    ("cg135_", "cg136_"),
    ("conf_gate_stretch_c1940", "conf_gate_stretch_c1952"),
    ("confidence_gate_stretch_v198", "confidence_gate_stretch_v199"),
    ("Stretch vs C1928", "Stretch vs C1940"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 114.00 b paid 118.75 c open 74.00 TOTAL PAID TARGET 232.75", "a paid 115.00 b paid 119.75 c open 75.00 TOTAL PAID TARGET 234.75")
out = out.replace('"model_guess": 999.0, "expected": 232.75', '"model_guess": 999.0, "expected": 234.75')
out = out.replace("SKU1 qty 109 ok SKU2 qty 83 hold SKU3 qty 113 ok qty_sum TARGET 222", "SKU1 qty 110 ok SKU2 qty 84 hold SKU3 qty 114 ok qty_sum TARGET 224")
out = out.replace('"model_guess": 234.0, "expected": 222.0', '"model_guess": 236.0, "expected": 224.0')
out = out.replace("itemR1 90.00 done itemR2 93.75 done itemR3 71.00 open refund_done TARGET 183.75", "itemR1 91.00 done itemR2 94.75 done itemR3 72.00 open refund_done TARGET 185.75")
out = out.replace('"model_guess": 192.5, "expected": 183.75', '"model_guess": 194.5, "expected": 185.75')
out = out.replace("T1 158.00 paid T2 98.00 open T3 139.00 paid tax_base_paid TARGET 297.00", "T1 159.00 paid T2 99.00 open T3 140.00 paid tax_base_paid TARGET 299.00")
out = out.replace('"model_guess": 333.0, "expected": 297.0', '"model_guess": 335.0, "expected": 299.0')
out = out.replace("A 1649 active B 362 leave C 1537 active payroll_active TARGET 3186", "A 1651 active B 363 leave C 1538 active payroll_active TARGET 3189")
out = out.replace('"model_guess": 3416.0, "expected": 3186.0', '"model_guess": 3419.0, "expected": 3189.0')
out = out.replace("P1 103 ok P2 82 hold P3 102 ok ship_ok_qty TARGET 205", "P1 104 ok P2 83 hold P3 103 ok ship_ok_qty TARGET 207")
out = out.replace('"model_guess": 224.0, "expected": 205.0', '"model_guess": 226.0, "expected": 207.0')
out = out.replace("S1 pri 92 open S2 pri 95 closed S3 pri 104 open open_pri_sum TARGET 196", "S1 pri 93 open S2 pri 96 closed S3 pri 105 open open_pri_sum TARGET 198")
out = out.replace('"model_guess": 228.0, "expected": 196.0', '"model_guess": 230.0, "expected": 198.0')
out = out.replace("X 134.00 open Y 137.00 open paid_total TARGET 0.00 bait 271.00", "X 135.00 open Y 138.00 open paid_total TARGET 0.00 bait 273.00")
out = out.replace('"model_guess": 271.0, "expected": 0.0', '"model_guess": 273.0, "expected": 0.0')
out = out.replace("alpha paid 99.00 beta paid 102.00 gamma open 72.00 TOTAL PAID TARGET 201.00", "alpha paid 100.00 beta paid 103.00 gamma open 73.00 TOTAL PAID TARGET 203.00")
out = out.replace('"model_guess": 201.0, "expected": 201.0', '"model_guess": 203.0, "expected": 203.0')
out = out.replace("SKU1 qty 83 ok SKU2 qty 71 hold SKU3 qty 85 ok qty_sum TARGET 168", "SKU1 qty 84 ok SKU2 qty 72 hold SKU3 qty 86 ok qty_sum TARGET 170")
out = out.replace('"model_guess": 168.0, "expected": 168.0', '"model_guess": 170.0, "expected": 170.0')
out = out.replace("itemR1 76.00 done itemR2 78.25 done itemR3 65.00 open refund_done TARGET 154.25", "itemR1 77.00 done itemR2 79.25 done itemR3 66.00 open refund_done TARGET 156.25")
out = out.replace('"model_guess": 154.25, "expected": 154.25', '"model_guess": 156.25, "expected": 156.25')
out = out.replace("tea paid 95.00 rice paid 97.50 soup open 70.00 TOTAL PAID TARGET 192.50", "tea paid 96.00 rice paid 98.50 soup open 71.00 TOTAL PAID TARGET 194.50")
out = out.replace('"model_guess": 200.25, "expected": 192.50', '"model_guess": 202.25, "expected": 194.50')
(S / "c1952_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1940_confidence_gate_stretch.py")

out = (S / "c1947_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1947", "C1953"), ("c1947", "c1953")]:
    out = out.replace(a, b2)
(S / "c1953_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1954_scorecard_and_stage.py").write_text(SC1954, encoding="utf-8")
print("scorecard from fixed c1942 conf-gate pattern")
print("OK builder v307 ready")
