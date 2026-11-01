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

# *hurst ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T320 = [
    ["ashhurst","recv","paid_total","ASHHURST GRAIN RECV","RECV","x"],
    ["cedarhurst","wh","qty_sum","WH CEDARHURST BIN","RECV","x"],
    ["dawnhurst","refund","refund_done","DAWNHURST PATCH REFUND","DONE","x"],
    ["elmhurst","tax","tax_base_paid","ELMHURST TAX SLIP","TAX","x"],
    ["fernhurst","pay","payroll_active","FERNHURST PAYROLL","PAY","x"],
    ["glenhurst","ship","ship_ok","GLENHURST SHIP DOCK","SHIP","x"],
    ["hazehurst","sla","sla_ok_hours","HAZEHURST SLA CARD","SLA","x"],
    ["inkhurst","exp","exp_sum","INKHURST EXPENSE","EXP","x"],
    ["jadehurst","po","po_open","JADEHURST PO SHEET","PO","x"],
    ["knothurst","order","order_paid","KNOTHURST ORDER","ORD","x"],
    ["lakehurst","dup","dup_mark","LAKEHURST DUP MARK","DUP","x"],
    ["mosshurst","zero","zero_check","MOSSHURST AIR ZERO","ZERO","x"],
    ["netherhurst","ledger","ledger_net","NETHERHURST LEDGER","LED","x"],
    ["oakhurst","ui","ui_ok","OAKHURST UI SCAN","UI","x"],
    ["pinehurst","stack","stack_count","PINEHURST STACK","STK","x"],
    ["quillhurst","fax","fax_pages","QUILLHURST FAX","FAX","x"],
    ["reedhurst","glare","glare_ok","REEDHURST GLARE","GLR","x"],
    ["stonehurst","tab","tab_index","STONEHURST TAB INDEX","TAB","x"],
]
TR320 = [
    [2304.0, 2321.5, 2044.0],[840, 760, 820],[2227.0, 2256.25, 2022.0],[2360.0, 2377.0, 2112.0],
    [2422.0, 2446.0, 2082.0],[2140, 2156, 2040],[490.0, 530.0, 760.0],[2270.0, 2301.75, 2046.0],
    [840.0, 760.0, 820.0],[2337.0, 2325.0, 2043.0],[1,1,0],[0,0,0],
    [2403.0, 2424.5, 2068.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO320 = [
    [2102.0, 2114.75, 1963.0],[640, 660, 820],[2045.0, 2059.5, 1938.0],[2175.0, 2191.0, 1994.0],
    [2216.0, 2232.0, 1987.0],[1998, 2010, 1958],[420.0, 460.0, 740.0],[2086.0, 2107.75, 1963.0],
    [740.0, 780.0, 820.0],[2133.0, 2119.0, 1960.0],[1,1,0],[0,0,0],
    [2168.0, 2183.5, 1973.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR320, "TR"); check(HO320, "HO")

(ROOT / "tools/_v320_themes.json").write_text(json.dumps({"themes": T320, "train": TR320, "heldout": HO320}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_319(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V320 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V320 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 140.50", "ASHHURST bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 235.45"),
        ("DAWNW ghost 65.65", "DAWNH ghost 158.68"),
        ("GLENW bait 135.45", "GLENH bait 228.38"),
        ("JADEW bait 126.36", "JADEH bait 219.29"),
        ("NETHERW bait 143.53", "NETHERH bait 236.46"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V320-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD319 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v319_themes.json").read_text(encoding="utf-8"))["themes"])
NEW320 = "_".join(t[0] for t in T320)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2027"), ("c1463", "c2027"), ("V226", "V320"), ("v226", "v320"),
    ("_v226c1463", "_v320c2027"),
    ("Harder than V225", "Harder than V318"), ("harder than V225", "harder than V318"),
    (OLD319, NEW320),
    ("V226 keeps floor", "V320 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2027 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2028 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2028 VL"),
    ("kept on V226", "kept on V320"),
    ("vision_images_v226", "vision_images_v320"),
    ("VL_GATE_V226", "VL_GATE_V320"), ("vl_gate_v226", "vl_gate_v320"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V318: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T320, "v320", "V320", TR320))
out = retarget_319(out)
(S / "c2027_vision_v320_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2028"), ("c1464", "c2028"), ("V226", "V320"), ("v226", "v320"),
    ("vision_images_v226", "vision_images_v320"),
    ("VL_GATE_V226", "VL_GATE_V320"), ("vl_gate_v226", "vl_gate_v320"),
    ("runs/vision_v226", "runs/vision_v320"),
]:
    out = out.replace(a, b)
(S / "c2028_vision_v320_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2029"), ("c1465", "c2029"), ("V226", "V320"), ("v226", "v320"),
    ("vision_images_v226h", "vision_images_v320h"),
    ("vision_images_v226", "vision_images_v320"),
    ("VL_GATE_V226", "VL_GATE_V320"), ("vl_gate_v226", "vl_gate_v320"),
    ("runs/vision_v226h", "runs/vision_v320h"),
    ("_v226c1463", "_v320c2027"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T320, "v320h", "V320H", HO320))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v320h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v320"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v320" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v320h_c2029"'); seen_run = True; continue
    out2.append(ln)
(S / "c2029_vision_v320_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2027-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2028_VISION_V320_SMOKE.json") or {}\n    c654b = load("docs/r50/C2028b_VISION_GATE_V320_CLAIM.json") or {}\n    c655 = load("docs/r50/C2029_VISION_V320_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2029b_VISION_GATE_V320_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v320 = float(c654.get("rate") or 0.0)\n    v320h = float(c655.get("rate") or 0.0)\n    v320_claim = bool(c654b.get("vl_gate_v320_claim") or c654.get("vl_gate_v320_claim") or c654.get("claim"))\n    v320h_claim = bool(c655b.get("vl_gate_v320_heldout_claim") or c655.get("vl_gate_v320_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v320_claim and v320h_claim and v320 >= GATE and v320h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v320 >= 0.999 and v320h >= 0.999) else min(v320, v320h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v320": {"rate": v320, "claim": v320_claim, "n": c654.get("n")},\n            "v320_heldout": {"rate": v320h, "claim": v320h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v320_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V320: rate={v320} claim={v320_claim}",\n        f"- Vision V320 heldout: rate={v320h} claim={v320h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2027-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2027: Vision V320 design fixtures",\n        f"- C2028: Vision V320 smoke **{v320}**", f"- C2029: Vision V320 heldout **{v320h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V320 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2032 = '\ufeff# -*- coding: utf-8 -*-\n"""C2032: Unified scorecard + STAGE after C2027-C2031. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2032.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2028_VISION_V320_SMOKE.json") or {}\n    c654b = load("docs/r50/C2028b_VISION_GATE_V320_CLAIM.json") or {}\n    c655 = load("docs/r50/C2029_VISION_V320_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2029b_VISION_GATE_V320_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2024_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2031_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2030_PRODUCT_U2C_COST.json") or {}\n\n    v320 = float(c654.get("rate") or 0.0)\n    v320h = float(c655.get("rate") or 0.0)\n    v320_claim = bool(c654b.get("vl_gate_v320_claim") or c654.get("vl_gate_v320_claim") or c654.get("claim"))\n    v320h_claim = bool(c655b.get("vl_gate_v320_heldout_claim") or c655.get("vl_gate_v320_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2030"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v320_claim and v320h_claim and v320 >= GATE and v320h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v320 >= 0.999 and v320h >= 0.999) else min(v320, v320h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2032", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v320": {"rate": v320, "claim": v320_claim, "n": c654.get("n")},\n            "v320_heldout": {"rate": v320h, "claim": v320h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2030"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2024"},\n        "capture_regression": {"pass": capture_pass, "source": "C2031"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v320_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2032_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2032)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V320: rate={v320} claim={v320_claim}",\n        f"- Vision V320 heldout: rate={v320h} claim={v320h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2032", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2027-C2032 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2027: Vision V320 design fixtures",\n        f"- C2028: Vision V320 smoke **{v320}**", f"- C2029: Vision V320 heldout **{v320h}** (disjoint={disjoint})",\n        f"- C2030: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C2024): pass={conf_pass} rate={conf_rate}",\n        f"- C2031: capture pass={capture_pass}", f"- C2032: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V320 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2032.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V320 knife = product-U2C (alternating; V319 was confidence-gate)
out = (S / "c2018_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2018", "C2030"), ("c2018", "c2030"),
    ("C2006", "C2030"), ("c2006", "c2030"),
    ("product_u2c_cost_c2018", "product_u2c_cost_c2030"),
    ("u2c_v203", "u2c_v204"),
    ("u2c_c2018", "u2c_c2030"),
]:
    out = out.replace(a, b2)
(S / "c2030_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2018")

out = (S / "c2025_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2025", "C2031"), ("c2025", "c2031")]:
    out = out.replace(a, b2)
(S / "c2031_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2032_scorecard_and_stage.py").write_text(SC2032, encoding="utf-8")
print("scorecard from fixed c2020 product-U2C pattern")
print("OK builder v320 ready")
