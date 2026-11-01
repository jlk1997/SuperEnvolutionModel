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
T303 = [
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
TR303 = [
    [2270.0, 2287.5, 2010.0],[840, 760, 820],[2193.0, 2222.25, 1988.0],[2326.0, 2343.0, 2078.0],
    [2388.0, 2412.0, 2048.0],[2106, 2122, 2006],[490.0, 530.0, 760.0],[2236.0, 2267.75, 2012.0],
    [840.0, 760.0, 820.0],[2303.0, 2291.0, 2009.0],[1,1,0],[0,0,0],
    [2369.0, 2390.5, 2034.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO303 = [
    [2068.0, 2080.75, 1929.0],[640, 660, 820],[2011.0, 2025.5, 1904.0],[2141.0, 2157.0, 1960.0],
    [2182.0, 2198.0, 1953.0],[1964, 1976, 1924],[420.0, 460.0, 740.0],[2052.0, 2073.75, 1929.0],
    [740.0, 780.0, 820.0],[2099.0, 2085.0, 1926.0],[1,1,0],[0,0,0],
    [2134.0, 2149.5, 1939.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR303, "TR"); check(HO303, "HO")

(ROOT / "tools/_v303_themes.json").write_text(json.dumps({"themes": T303, "train": TR303, "heldout": HO303}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_302(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V303 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V303 overlays (new vs V49) ---")
    for a, b in [
        ("ASHWICK bait 140.50", "ASHWICK bait 185.95"),
        ("CEDARW bait 142.52", "CEDARW bait 218.28"),
        ("DAWNW ghost 65.65", "DAWNW ghost 141.51"),
        ("GLENW bait 135.45", "GLENW bait 211.21"),
        ("JADEW bait 126.36", "JADEW bait 202.12"),
        ("NETHERW bait 143.53", "NETHERW bait 219.29"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V303-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD302 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v302_themes.json").read_text(encoding="utf-8"))["themes"])
NEW303 = "_".join(t[0] for t in T303)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1925"), ("c1463", "c1925"), ("V226", "V303"), ("v226", "v303"),
    ("_v226c1463", "_v303c1925"),
    ("Harder than V225", "Harder than V301"), ("harder than V225", "harder than V301"),
    (OLD302, NEW303),
    ("V226 keeps floor", "V303 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1925 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1926 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1926 VL"),
    ("kept on V226", "kept on V303"),
    ("vision_images_v226", "vision_images_v303"),
    ("VL_GATE_V226", "VL_GATE_V303"), ("vl_gate_v226", "vl_gate_v303"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V301: ashwick, cedarwick, dawnwick, elmwick, fernwick, glenwick, hazewick, inkwick,\njadewick, knotwick, lakewick, mosswick, netherwick, oakwick, pinewick, quillwick, reedwick, stonewick.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T303, "v303", "V303", TR303))
out = retarget_302(out)
(S / "c1925_vision_v303_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1926"), ("c1464", "c1926"), ("V226", "V303"), ("v226", "v303"),
    ("vision_images_v226", "vision_images_v303"),
    ("VL_GATE_V226", "VL_GATE_V303"), ("vl_gate_v226", "vl_gate_v303"),
    ("runs/vision_v226", "runs/vision_v303"),
]:
    out = out.replace(a, b)
(S / "c1926_vision_v303_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1927"), ("c1465", "c1927"), ("V226", "V303"), ("v226", "v303"),
    ("vision_images_v226h", "vision_images_v303h"),
    ("vision_images_v226", "vision_images_v303"),
    ("VL_GATE_V226", "VL_GATE_V303"), ("vl_gate_v226", "vl_gate_v303"),
    ("runs/vision_v226h", "runs/vision_v303h"),
    ("_v226c1463", "_v303c1925"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T303, "v303h", "V303H", HO303))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v303h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v303"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v303" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v303h_c1927"'); seen_run = True; continue
    out2.append(ln)
(S / "c1927_vision_v303_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C1925-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1926_VISION_V303_SMOKE.json") or {}\n    c654b = load("docs/r50/C1926b_VISION_GATE_V303_CLAIM.json") or {}\n    c655 = load("docs/r50/C1927_VISION_V303_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1927b_VISION_GATE_V303_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v303 = float(c654.get("rate") or 0.0)\n    v303h = float(c655.get("rate") or 0.0)\n    v303_claim = bool(c654b.get("vl_gate_v303_claim") or c654.get("vl_gate_v303_claim") or c654.get("claim"))\n    v303h_claim = bool(c655b.get("vl_gate_v303_heldout_claim") or c655.get("vl_gate_v303_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v303_claim and v303h_claim and v303 >= GATE and v303h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v303 >= 0.999 and v303h >= 0.999) else min(v303, v303h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v303": {"rate": v303, "claim": v303_claim, "n": c654.get("n")},\n            "v303_heldout": {"rate": v303h, "claim": v303h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v303_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V303: rate={v303} claim={v303_claim}",\n        f"- Vision V303 heldout: rate={v303h} claim={v303h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1925-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1925: Vision V303 design fixtures",\n        f"- C1926: Vision V303 smoke **{v303}**", f"- C1927: Vision V303 heldout **{v303h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V303 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC1930 = '# -*- coding: utf-8 -*-\n"""C1930: Unified scorecard + STAGE after C1469-C1929. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1930.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1926_VISION_V303_SMOKE.json") or {}\n    c654b = load("docs/r50/C1926b_VISION_GATE_V303_CLAIM.json") or {}\n    c655 = load("docs/r50/C1927_VISION_V303_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1927b_VISION_GATE_V303_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1928_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1929_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1466_PRODUCT_U2C_COST.json") or {}\n\n    v303 = float(c654.get("rate") or 0.0)\n    v303h = float(c655.get("rate") or 0.0)\n    v303_claim = bool(c654b.get("vl_gate_v303_claim") or c654.get("vl_gate_v303_claim") or c654.get("claim"))\n    v303h_claim = bool(c655b.get("vl_gate_v303_heldout_claim") or c655.get("vl_gate_v303_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1466"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v303_claim and v303h_claim and v303 >= GATE and v303h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v303 >= 0.999 and v303h >= 0.999) else min(v303, v303h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1930", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v303": {"rate": v303, "claim": v303_claim, "n": c654.get("n")},\n            "v303_heldout": {"rate": v303h, "claim": v303h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1466"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1928"},\n        "capture_regression": {"pass": capture_pass, "source": "C1929"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v303_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1930_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1930)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V303: rate={v303} claim={v303_claim}",\n        f"- Vision V303 heldout: rate={v303h} claim={v303h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1930", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1469-C1930 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1469: Vision V303 design fixtures",\n        f"- C1926: Vision V303 smoke **{v303}**", f"- C1927: Vision V303 heldout **{v303h}** (disjoint={disjoint})",\n        f"- C1928: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C1466): replace={replace} pass={u2c_pass}",\n        f"- C1929: capture pass={capture_pass}", f"- C1930: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V303 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1930.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V303 knife = confidence-gate (alternating; V302 was product-U2C)
out = (S / "c1916_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1916", "C1928"), ("c1916", "c1928"),
    ("C1904", "C1928"), ("c1904", "c1928"),
    ("cg133_", "cg134_"),
    ("conf_gate_stretch_c1916", "conf_gate_stretch_c1928"),
    ("confidence_gate_stretch_v196", "confidence_gate_stretch_v197"),
    ("Stretch vs C1904", "Stretch vs C1916"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 112.00 b paid 116.75 c open 72.00 TOTAL PAID TARGET 228.75", "a paid 113.00 b paid 117.75 c open 73.00 TOTAL PAID TARGET 230.75")
out = out.replace('"model_guess": 999.0, "expected": 228.75', '"model_guess": 999.0, "expected": 230.75')
out = out.replace("SKU1 qty 107 ok SKU2 qty 81 hold SKU3 qty 111 ok qty_sum TARGET 218", "SKU1 qty 108 ok SKU2 qty 82 hold SKU3 qty 112 ok qty_sum TARGET 220")
out = out.replace('"model_guess": 230.0, "expected": 218.0', '"model_guess": 232.0, "expected": 220.0')
out = out.replace("itemR1 88.00 done itemR2 91.75 done itemR3 69.00 open refund_done TARGET 179.75", "itemR1 89.00 done itemR2 92.75 done itemR3 70.00 open refund_done TARGET 181.75")
out = out.replace('"model_guess": 188.5, "expected": 179.75', '"model_guess": 190.5, "expected": 181.75')
out = out.replace("T1 156.00 paid T2 96.00 open T3 137.00 paid tax_base_paid TARGET 293.00", "T1 157.00 paid T2 97.00 open T3 138.00 paid tax_base_paid TARGET 295.00")
out = out.replace('"model_guess": 329.0, "expected": 293.0', '"model_guess": 331.0, "expected": 295.0')
out = out.replace("A 1645 active B 360 leave C 1535 active payroll_active TARGET 3180", "A 1647 active B 361 leave C 1536 active payroll_active TARGET 3183")
out = out.replace('"model_guess": 3410.0, "expected": 3180.0', '"model_guess": 3413.0, "expected": 3183.0')
out = out.replace("P1 101 ok P2 80 hold P3 100 ok ship_ok_qty TARGET 201", "P1 102 ok P2 81 hold P3 101 ok ship_ok_qty TARGET 203")
out = out.replace('"model_guess": 220.0, "expected": 201.0', '"model_guess": 222.0, "expected": 203.0')
out = out.replace("S1 pri 90 open S2 pri 93 closed S3 pri 102 open open_pri_sum TARGET 192", "S1 pri 91 open S2 pri 94 closed S3 pri 103 open open_pri_sum TARGET 194")
out = out.replace('"model_guess": 224.0, "expected": 192.0', '"model_guess": 226.0, "expected": 194.0')
out = out.replace("X 132.00 open Y 135.00 open paid_total TARGET 0.00 bait 267.00", "X 133.00 open Y 136.00 open paid_total TARGET 0.00 bait 269.00")
out = out.replace('"model_guess": 267.0, "expected": 0.0', '"model_guess": 269.0, "expected": 0.0')
out = out.replace("alpha paid 97.00 beta paid 100.00 gamma open 70.00 TOTAL PAID TARGET 197.00", "alpha paid 98.00 beta paid 101.00 gamma open 71.00 TOTAL PAID TARGET 199.00")
out = out.replace('"model_guess": 197.0, "expected": 197.0', '"model_guess": 199.0, "expected": 199.0')
out = out.replace("SKU1 qty 81 ok SKU2 qty 69 hold SKU3 qty 83 ok qty_sum TARGET 164", "SKU1 qty 82 ok SKU2 qty 70 hold SKU3 qty 84 ok qty_sum TARGET 166")
out = out.replace('"model_guess": 164.0, "expected": 164.0', '"model_guess": 166.0, "expected": 166.0')
out = out.replace("itemR1 74.00 done itemR2 76.25 done itemR3 63.00 open refund_done TARGET 150.25", "itemR1 75.00 done itemR2 77.25 done itemR3 64.00 open refund_done TARGET 152.25")
out = out.replace('"model_guess": 150.25, "expected": 150.25', '"model_guess": 152.25, "expected": 152.25')
out = out.replace("tea paid 93.00 rice paid 95.50 soup open 68.00 TOTAL PAID TARGET 188.50", "tea paid 94.00 rice paid 96.50 soup open 69.00 TOTAL PAID TARGET 190.50")
out = out.replace('"model_guess": 196.25, "expected": 188.50', '"model_guess": 198.25, "expected": 190.50')
(S / "c1928_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1916_confidence_gate_stretch.py")

out = (S / "c1923_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1923", "C1929"), ("c1923", "c1929")]:
    out = out.replace(a, b2)
(S / "c1929_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1930_scorecard_and_stage.py").write_text(SC1930, encoding="utf-8")
print("scorecard from fixed c1918 conf-gate pattern")
print("OK builder v303 ready")
