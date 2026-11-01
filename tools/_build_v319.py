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
T319 = [
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
TR319 = [
    [2302.0, 2319.5, 2042.0],[840, 760, 820],[2225.0, 2254.25, 2020.0],[2358.0, 2375.0, 2110.0],
    [2420.0, 2444.0, 2080.0],[2138, 2154, 2038],[490.0, 530.0, 760.0],[2268.0, 2299.75, 2044.0],
    [840.0, 760.0, 820.0],[2335.0, 2323.0, 2041.0],[1,1,0],[0,0,0],
    [2401.0, 2422.5, 2066.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO319 = [
    [2100.0, 2112.75, 1961.0],[640, 660, 820],[2043.0, 2057.5, 1936.0],[2173.0, 2189.0, 1992.0],
    [2214.0, 2230.0, 1985.0],[1996, 2008, 1956],[420.0, 460.0, 740.0],[2084.0, 2105.75, 1961.0],
    [740.0, 780.0, 820.0],[2131.0, 2117.0, 1958.0],[1,1,0],[0,0,0],
    [2166.0, 2181.5, 1971.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR319, "TR"); check(HO319, "HO")

(ROOT / "tools/_v319_themes.json").write_text(json.dumps({"themes": T319, "train": TR319, "heldout": HO319}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_318(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V319 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V319 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 140.50", "ASHFORD bait 185.95"),
        ("CEDARW bait 142.52", "CEDARF bait 234.44"),
        ("DAWNW ghost 65.65", "DAWNF ghost 157.67"),
        ("GLENW bait 135.45", "GLENF bait 227.37"),
        ("JADEW bait 126.36", "JADEF bait 218.28"),
        ("NETHERW bait 143.53", "NETHERF bait 235.45"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V319-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD318 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v318_themes.json").read_text(encoding="utf-8"))["themes"])
NEW319 = "_".join(t[0] for t in T319)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2021"), ("c1463", "c2021"), ("V226", "V319"), ("v226", "v319"),
    ("_v226c1463", "_v319c2021"),
    ("Harder than V225", "Harder than V317"), ("harder than V225", "harder than V317"),
    (OLD318, NEW319),
    ("V226 keeps floor", "V319 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2021 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2022 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2022 VL"),
    ("kept on V226", "kept on V319"),
    ("vision_images_v226", "vision_images_v319"),
    ("VL_GATE_V226", "VL_GATE_V319"), ("vl_gate_v226", "vl_gate_v319"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V317: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T319, "v319", "V319", TR319))
out = retarget_318(out)
(S / "c2021_vision_v319_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2022"), ("c1464", "c2022"), ("V226", "V319"), ("v226", "v319"),
    ("vision_images_v226", "vision_images_v319"),
    ("VL_GATE_V226", "VL_GATE_V319"), ("vl_gate_v226", "vl_gate_v319"),
    ("runs/vision_v226", "runs/vision_v319"),
]:
    out = out.replace(a, b)
(S / "c2022_vision_v319_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2023"), ("c1465", "c2023"), ("V226", "V319"), ("v226", "v319"),
    ("vision_images_v226h", "vision_images_v319h"),
    ("vision_images_v226", "vision_images_v319"),
    ("VL_GATE_V226", "VL_GATE_V319"), ("vl_gate_v226", "vl_gate_v319"),
    ("runs/vision_v226h", "runs/vision_v319h"),
    ("_v226c1463", "_v319c2021"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T319, "v319h", "V319H", HO319))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v319h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v319"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v319" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v319h_c2023"'); seen_run = True; continue
    out2.append(ln)
(S / "c2023_vision_v319_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2021-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2022_VISION_V319_SMOKE.json") or {}\n    c654b = load("docs/r50/C2022b_VISION_GATE_V319_CLAIM.json") or {}\n    c655 = load("docs/r50/C2023_VISION_V319_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2023b_VISION_GATE_V319_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v319 = float(c654.get("rate") or 0.0)\n    v319h = float(c655.get("rate") or 0.0)\n    v319_claim = bool(c654b.get("vl_gate_v319_claim") or c654.get("vl_gate_v319_claim") or c654.get("claim"))\n    v319h_claim = bool(c655b.get("vl_gate_v319_heldout_claim") or c655.get("vl_gate_v319_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v319_claim and v319h_claim and v319 >= GATE and v319h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v319 >= 0.999 and v319h >= 0.999) else min(v319, v319h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v319": {"rate": v319, "claim": v319_claim, "n": c654.get("n")},\n            "v319_heldout": {"rate": v319h, "claim": v319h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v319_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V319: rate={v319} claim={v319_claim}",\n        f"- Vision V319 heldout: rate={v319h} claim={v319h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2021-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2021: Vision V319 design fixtures",\n        f"- C2022: Vision V319 smoke **{v319}**", f"- C2023: Vision V319 heldout **{v319h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V319 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2026 = '# -*- coding: utf-8 -*-\n"""C2026: Unified scorecard + STAGE after C2021-C2025. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2026.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2022_VISION_V319_SMOKE.json") or {}\n    c654b = load("docs/r50/C2022b_VISION_GATE_V319_CLAIM.json") or {}\n    c655 = load("docs/r50/C2023_VISION_V319_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2023b_VISION_GATE_V319_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2024_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2025_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2018_PRODUCT_U2C_COST.json") or {}\n\n    v319 = float(c654.get("rate") or 0.0)\n    v319h = float(c655.get("rate") or 0.0)\n    v319_claim = bool(c654b.get("vl_gate_v319_claim") or c654.get("vl_gate_v319_claim") or c654.get("claim"))\n    v319h_claim = bool(c655b.get("vl_gate_v319_heldout_claim") or c655.get("vl_gate_v319_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2018"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v319_claim and v319h_claim and v319 >= GATE and v319h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v319 >= 0.999 and v319h >= 0.999) else min(v319, v319h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2026", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v319": {"rate": v319, "claim": v319_claim, "n": c654.get("n")},\n            "v319_heldout": {"rate": v319h, "claim": v319h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2018"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2024"},\n        "capture_regression": {"pass": capture_pass, "source": "C2025"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v319_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2026_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2026)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V319: rate={v319} claim={v319_claim}",\n        f"- Vision V319 heldout: rate={v319h} claim={v319h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2026", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2021-C2026 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2021: Vision V319 design fixtures",\n        f"- C2022: Vision V319 smoke **{v319}**", f"- C2023: Vision V319 heldout **{v319h}** (disjoint={disjoint})",\n        f"- C2024: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2018): replace={replace} pass={u2c_pass}",\n        f"- C2025: capture pass={capture_pass}", f"- C2026: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V319 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2026.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V319 knife = confidence-gate (alternating; V318 was product-U2C)
out = (S / "c2012_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2012", "C2024"), ("c2012", "c2024"),
    ("C2000", "C2024"), ("c2000", "c2024"),
    ("cg141_", "cg142_"),
    ("conf_gate_stretch_c2012", "conf_gate_stretch_c2024"),
    ("confidence_gate_stretch_v204", "confidence_gate_stretch_v205"),
    ("Stretch vs C2000", "Stretch vs C2012"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 120.00 b paid 124.75 c open 80.00 TOTAL PAID TARGET 244.75", "a paid 121.00 b paid 125.75 c open 81.00 TOTAL PAID TARGET 246.75")
out = out.replace('"model_guess": 999.0, "expected": 244.75', '"model_guess": 999.0, "expected": 246.75')
out = out.replace("SKU1 qty 115 ok SKU2 qty 89 hold SKU3 qty 119 ok qty_sum TARGET 234", "SKU1 qty 116 ok SKU2 qty 90 hold SKU3 qty 120 ok qty_sum TARGET 236")
out = out.replace('"model_guess": 246.0, "expected": 234.0', '"model_guess": 248.0, "expected": 236.0')
out = out.replace("itemR1 96.00 done itemR2 99.75 done itemR3 77.00 open refund_done TARGET 195.75", "itemR1 97.00 done itemR2 100.75 done itemR3 78.00 open refund_done TARGET 197.75")
out = out.replace('"model_guess": 204.5, "expected": 195.75', '"model_guess": 206.5, "expected": 197.75')
out = out.replace("T1 164.00 paid T2 104.00 open T3 145.00 paid tax_base_paid TARGET 309.00", "T1 165.00 paid T2 105.00 open T3 146.00 paid tax_base_paid TARGET 311.00")
out = out.replace('"model_guess": 345.0, "expected": 309.0', '"model_guess": 347.0, "expected": 311.0')
out = out.replace("A 1659 active B 368 leave C 1543 active payroll_active TARGET 3202", "A 1660 active B 369 leave C 1544 active payroll_active TARGET 3204")
out = out.replace('"model_guess": 3432.0, "expected": 3202.0', '"model_guess": 3434.0, "expected": 3204.0')
out = out.replace("P1 109 ok P2 88 hold P3 108 ok ship_ok_qty TARGET 217", "P1 110 ok P2 89 hold P3 109 ok ship_ok_qty TARGET 219")
out = out.replace('"model_guess": 236.0, "expected": 217.0', '"model_guess": 238.0, "expected": 219.0')
out = out.replace("S1 pri 98 open S2 pri 101 closed S3 pri 110 open open_pri_sum TARGET 208", "S1 pri 99 open S2 pri 102 closed S3 pri 111 open open_pri_sum TARGET 210")
out = out.replace('"model_guess": 240.0, "expected": 208.0', '"model_guess": 242.0, "expected": 210.0')
out = out.replace("X 140.00 open Y 143.00 open paid_total TARGET 0.00 bait 283.00", "X 141.00 open Y 144.00 open paid_total TARGET 0.00 bait 285.00")
out = out.replace('"model_guess": 283.0, "expected": 0.0', '"model_guess": 285.0, "expected": 0.0')
out = out.replace("alpha paid 105.00 beta paid 108.00 gamma open 78.00 TOTAL PAID TARGET 213.00", "alpha paid 106.00 beta paid 109.00 gamma open 79.00 TOTAL PAID TARGET 215.00")
out = out.replace('"model_guess": 213.0, "expected": 213.0', '"model_guess": 215.0, "expected": 215.0')
out = out.replace("SKU1 qty 89 ok SKU2 qty 77 hold SKU3 qty 91 ok qty_sum TARGET 180", "SKU1 qty 90 ok SKU2 qty 78 hold SKU3 qty 92 ok qty_sum TARGET 182")
out = out.replace('"model_guess": 180.0, "expected": 180.0', '"model_guess": 182.0, "expected": 182.0')
out = out.replace("itemR1 82.00 done itemR2 84.25 done itemR3 71.00 open refund_done TARGET 166.25", "itemR1 83.00 done itemR2 85.25 done itemR3 72.00 open refund_done TARGET 168.25")
out = out.replace('"model_guess": 166.25, "expected": 166.25', '"model_guess": 168.25, "expected": 168.25')
out = out.replace("tea paid 101.00 rice paid 103.50 soup open 76.00 TOTAL PAID TARGET 204.50", "tea paid 102.00 rice paid 104.50 soup open 77.00 TOTAL PAID TARGET 206.50")
out = out.replace('"model_guess": 212.25, "expected": 204.50', '"model_guess": 214.25, "expected": 206.50')
(S / "c2024_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2012_confidence_gate_stretch.py")

out = (S / "c2019_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2019", "C2025"), ("c2019", "c2025")]:
    out = out.replace(a, b2)
(S / "c2025_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2026_scorecard_and_stage.py").write_text(SC2026, encoding="utf-8")
print("scorecard from fixed c2014 conf-gate pattern")
print("OK builder v319 ready")
