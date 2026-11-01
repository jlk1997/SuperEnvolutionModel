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

# *vale ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T333 = [
    ["ashvale","recv","paid_total","ASHVALE GRAIN RECV","RECV","x"],
    ["cedarvale","wh","qty_sum","WH CEDARVALE BIN","RECV","x"],
    ["dawnvale","refund","refund_done","DAWNVALE PATCH REFUND","DONE","x"],
    ["elmvale","tax","tax_base_paid","ELMVALE TAX SLIP","TAX","x"],
    ["fernvale","pay","payroll_active","FERNVALE PAYROLL","PAY","x"],
    ["glenvale","ship","ship_ok","GLENVALE SHIP DOCK","SHIP","x"],
    ["hazevale","sla","sla_ok_hours","HAZEVALE SLA CARD","SLA","x"],
    ["inkvale","exp","exp_sum","INKVALE EXPENSE","EXP","x"],
    ["jadevale","po","po_open","JADEVALE PO SHEET","PO","x"],
    ["knotvale","order","order_paid","KNOTVALE ORDER","ORD","x"],
    ["lakevale","dup","dup_mark","LAKEVALE DUP MARK","DUP","x"],
    ["mossvale","zero","zero_check","MOSSVALE AIR ZERO","ZERO","x"],
    ["nethervale","ledger","ledger_net","NETHERVALE LEDGER","LED","x"],
    ["oakvale","ui","ui_ok","OAKVALE UI SCAN","UI","x"],
    ["pinevale","stack","stack_count","PINEVALE STACK","STK","x"],
    ["quillvale","fax","fax_pages","QUILLVALE FAX","FAX","x"],
    ["reedvale","glare","glare_ok","REEDVALE GLARE","GLR","x"],
    ["stonevale","tab","tab_index","STONEVALE TAB INDEX","TAB","x"],
]
TR333 = [
    [2330.0, 2347.5, 2070.0],[840, 760, 820],[2251.0, 2257.25, 2046.0],[2386.0, 2403.0, 2138.0],
    [2448.0, 2472.0, 2108.0],[2166, 2182, 2066],[490.0, 530.0, 760.0],[2296.0, 2327.75, 2072.0],
    [840.0, 760.0, 820.0],[2363.0, 2351.0, 2069.0],[1,1,0],[0,0,0],
    [2429.0, 2450.5, 2094.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO333 = [
    [2128.0, 2140.75, 1989.0],[640, 660, 820],[2071.0, 2085.5, 1964.0],[2201.0, 2217.0, 2020.0],
    [2242.0, 2258.0, 2013.0],[2024, 2036, 1986],[420.0, 460.0, 740.0],[2112.0, 2133.75, 1989.0],
    [740.0, 780.0, 820.0],[2159.0, 2145.0, 1986.0],[1,1,0],[0,0,0],
    [2194.0, 2209.5, 1999.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR333, "TR"); check(HO333, "HO")

(ROOT / "tools/_v333_themes.json").write_text(json.dumps({"themes": T333, "train": TR333, "heldout": HO333}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_332(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V333 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V333 overlays (new vs V49) ---")
    for a, b in [
        ("ASHVALE bait 140.50", "ASHVALE bait 185.95"),
        ("CEDARW bait 142.52", "CEDARV bait 248.58"),
        ("DAWNW ghost 65.65", "DAWNV ghost 171.81"),
        ("GLENW bait 135.45", "GLENV bait 241.51"),
        ("JADEW bait 126.36", "JADEV bait 232.42"),
        ("NETHERW bait 143.53", "NETHERV bait 249.59"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V333-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD332 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v332_themes.json").read_text(encoding="utf-8"))["themes"])
NEW333 = "_".join(t[0] for t in T333)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2105"), ("c1463", "c2105"), ("V226", "V333"), ("v226", "v333"),
    ("_v226c1463", "_v333c2105"),
    ("Harder than V225", "Harder than V331"), ("harder than V225", "harder than V331"),
    (OLD332, NEW333),
    ("V226 keeps floor", "V333 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2105 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2106 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2106 VL"),
    ("kept on V226", "kept on V333"),
    ("vision_images_v226", "vision_images_v333"),
    ("VL_GATE_V226", "VL_GATE_V333"), ("vl_gate_v226", "vl_gate_v333"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V331: ashvale, cedarvale, dawnvale, elmvale, fernvale, glenvale, hazevale, inkvale,\njadevale, knotvale, lakevale, mossvale, nethervale, oakvale, pinevale, quillvale, reedvale, stonevale.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T333, "v333", "V333", TR333))
out = retarget_332(out)
(S / "c2105_vision_v333_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2106"), ("c1464", "c2106"), ("V226", "V333"), ("v226", "v333"),
    ("vision_images_v226", "vision_images_v333"),
    ("VL_GATE_V226", "VL_GATE_V333"), ("vl_gate_v226", "vl_gate_v333"),
    ("runs/vision_v226", "runs/vision_v333"),
]:
    out = out.replace(a, b)
(S / "c2106_vision_v333_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2107"), ("c1465", "c2107"), ("V226", "V333"), ("v226", "v333"),
    ("vision_images_v226h", "vision_images_v333h"),
    ("vision_images_v226", "vision_images_v333"),
    ("VL_GATE_V226", "VL_GATE_V333"), ("vl_gate_v226", "vl_gate_v333"),
    ("runs/vision_v226h", "runs/vision_v333h"),
    ("_v226c1463", "_v333c2105"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T333, "v333h", "V333H", HO333))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v333h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v333"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v333" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v333h_c2107"'); seen_run = True; continue
    out2.append(ln)
(S / "c2107_vision_v333_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2105-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2106_VISION_V333_SMOKE.json") or {}\n    c654b = load("docs/r50/C2106b_VISION_GATE_V333_CLAIM.json") or {}\n    c655 = load("docs/r50/C2107_VISION_V333_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2107b_VISION_GATE_V333_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v333 = float(c654.get("rate") or 0.0)\n    v333h = float(c655.get("rate") or 0.0)\n    v333_claim = bool(c654b.get("vl_gate_v333_claim") or c654.get("vl_gate_v333_claim") or c654.get("claim"))\n    v333h_claim = bool(c655b.get("vl_gate_v333_heldout_claim") or c655.get("vl_gate_v333_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v333_claim and v333h_claim and v333 >= GATE and v333h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v333 >= 0.999 and v333h >= 0.999) else min(v333, v333h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v333": {"rate": v333, "claim": v333_claim, "n": c654.get("n")},\n            "v333_heldout": {"rate": v333h, "claim": v333h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v333_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V333: rate={v333} claim={v333_claim}",\n        f"- Vision V333 heldout: rate={v333h} claim={v333h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2105-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2105: Vision V333 design fixtures",\n        f"- C2106: Vision V333 smoke **{v333}**", f"- C2107: Vision V333 heldout **{v333h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V333 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2110 = '# -*- coding: utf-8 -*-\n"""C2110: Unified scorecard + STAGE after C2105-C2109. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2110.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2106_VISION_V333_SMOKE.json") or {}\n    c654b = load("docs/r50/C2106b_VISION_GATE_V333_CLAIM.json") or {}\n    c655 = load("docs/r50/C2107_VISION_V333_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2107b_VISION_GATE_V333_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2108_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2109_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2102_PRODUCT_U2C_COST.json") or {}\n\n    v333 = float(c654.get("rate") or 0.0)\n    v333h = float(c655.get("rate") or 0.0)\n    v333_claim = bool(c654b.get("vl_gate_v333_claim") or c654.get("vl_gate_v333_claim") or c654.get("claim"))\n    v333h_claim = bool(c655b.get("vl_gate_v333_heldout_claim") or c655.get("vl_gate_v333_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2102"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v333_claim and v333h_claim and v333 >= GATE and v333h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v333 >= 0.999 and v333h >= 0.999) else min(v333, v333h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2110", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v333": {"rate": v333, "claim": v333_claim, "n": c654.get("n")},\n            "v333_heldout": {"rate": v333h, "claim": v333h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2102"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2108"},\n        "capture_regression": {"pass": capture_pass, "source": "C2109"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v333_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2110_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2110)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V333: rate={v333} claim={v333_claim}",\n        f"- Vision V333 heldout: rate={v333h} claim={v333h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2110", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2105-C2110 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2105: Vision V333 design fixtures",\n        f"- C2106: Vision V333 smoke **{v333}**", f"- C2107: Vision V333 heldout **{v333h}** (disjoint={disjoint})",\n        f"- C2108: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2102): replace={replace} pass={u2c_pass}",\n        f"- C2109: capture pass={capture_pass}", f"- C2110: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V333 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2110.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V333 knife = confidence-gate (alternating; V332 was product-U2C)
out = (S / "c2096_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2096", "C2108"), ("c2096", "c2108"),
    ("C2084", "C2108"), ("c2084", "c2108"),
    ("cg148_", "cg149_"),
    ("conf_gate_stretch_c2096", "conf_gate_stretch_c2108"),
    ("confidence_gate_stretch_v211", "confidence_gate_stretch_v212"),
    ("Stretch vs C2084", "Stretch vs C2096"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 127.00 b paid 131.75 c open 87.00 TOTAL PAID TARGET 258.75", "a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75")
out = out.replace('"model_guess": 999.0, "expected": 258.75', '"model_guess": 999.0, "expected": 260.75')
out = out.replace("SKU1 qty 122 ok SKU2 qty 96 hold SKU3 qty 126 ok qty_sum TARGET 248", "SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250")
out = out.replace('"model_guess": 260.0, "expected": 248.0', '"model_guess": 262.0, "expected": 250.0')
out = out.replace("itemR1 103.00 done itemR2 106.75 done itemR3 84.00 open refund_done TARGET 209.75", "itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75")
out = out.replace('"model_guess": 218.5, "expected": 209.75', '"model_guess": 220.5, "expected": 211.75')
out = out.replace("T1 171.00 paid T2 111.00 open T3 152.00 paid tax_base_paid TARGET 323.00", "T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00")
out = out.replace('"model_guess": 359.0, "expected": 323.0', '"model_guess": 361.0, "expected": 325.0')
out = out.replace("A 1666 active B 375 leave C 1550 active payroll_active TARGET 3216", "A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218")
out = out.replace('"model_guess": 3446.0, "expected": 3216.0', '"model_guess": 3448.0, "expected": 3218.0')
out = out.replace("P1 116 ok P2 95 hold P3 115 ok ship_ok_qty TARGET 231", "P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233")
out = out.replace('"model_guess": 250.0, "expected": 231.0', '"model_guess": 252.0, "expected": 233.0')
out = out.replace("S1 pri 105 open S2 pri 108 closed S3 pri 117 open open_pri_sum TARGET 222", "S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224")
out = out.replace('"model_guess": 254.0, "expected": 222.0', '"model_guess": 256.0, "expected": 224.0')
out = out.replace("X 147.00 open Y 150.00 open paid_total TARGET 0.00 bait 297.00", "X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00")
out = out.replace('"model_guess": 297.0, "expected": 0.0', '"model_guess": 299.0, "expected": 0.0')
out = out.replace("alpha paid 112.00 beta paid 115.00 gamma open 85.00 TOTAL PAID TARGET 227.00", "alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00")
out = out.replace('"model_guess": 227.0, "expected": 227.0', '"model_guess": 229.0, "expected": 229.0')
out = out.replace("SKU1 qty 96 ok SKU2 qty 84 hold SKU3 qty 98 ok qty_sum TARGET 194", "SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196")
out = out.replace('"model_guess": 194.0, "expected": 194.0', '"model_guess": 196.0, "expected": 196.0')
out = out.replace("itemR1 89.00 done itemR2 91.25 done itemR3 78.00 open refund_done TARGET 180.25", "itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25")
out = out.replace('"model_guess": 180.25, "expected": 180.25', '"model_guess": 182.25, "expected": 182.25')
out = out.replace("tea paid 108.00 rice paid 110.50 soup open 83.00 TOTAL PAID TARGET 218.50", "tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50")
out = out.replace('"model_guess": 226.25, "expected": 218.50', '"model_guess": 228.25, "expected": 220.50')
(S / "c2108_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2096_confidence_gate_stretch.py")

out = (S / "c2103_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2103", "C2109"), ("c2103", "c2109")]:
    out = out.replace(a, b2)
(S / "c2109_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2110_scorecard_and_stage.py").write_text(SC2110, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v333 ready")
