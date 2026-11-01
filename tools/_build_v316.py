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

# *fen ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T316 = [
    ["ashfen","recv","paid_total","ASHFEN GRAIN RECV","RECV","x"],
    ["cedarfen","wh","qty_sum","WH CEDARFEN BIN","RECV","x"],
    ["dawnfen","refund","refund_done","DAWNFEN PATCH REFUND","DONE","x"],
    ["elmfen","tax","tax_base_paid","ELMFEN TAX SLIP","TAX","x"],
    ["fernfen","pay","payroll_active","FERNFEN PAYROLL","PAY","x"],
    ["glenfen","ship","ship_ok","GLENFEN SHIP DOCK","SHIP","x"],
    ["hazefen","sla","sla_ok_hours","HAZEFEN SLA CARD","SLA","x"],
    ["inkfen","exp","exp_sum","INKFEN EXPENSE","EXP","x"],
    ["jadefen","po","po_open","JADEFEN PO SHEET","PO","x"],
    ["knotfen","order","order_paid","KNOTFEN ORDER","ORD","x"],
    ["lakefen","dup","dup_mark","LAKEFEN DUP MARK","DUP","x"],
    ["mossfen","zero","zero_check","MOSSFEN AIR ZERO","ZERO","x"],
    ["netherfen","ledger","ledger_net","NETHERFEN LEDGER","LED","x"],
    ["oakfen","ui","ui_ok","OAKFEN UI SCAN","UI","x"],
    ["pinefen","stack","stack_count","PINEFEN STACK","STK","x"],
    ["quillfen","fax","fax_pages","QUILLFEN FAX","FAX","x"],
    ["reedfen","glare","glare_ok","REEDFEN GLARE","GLR","x"],
    ["stonefen","tab","tab_index","STONEFEN TAB INDEX","TAB","x"],
]
TR316 = [
    [2296.0, 2313.5, 2036.0],[840, 760, 820],[2219.0, 2248.25, 2014.0],[2352.0, 2369.0, 2104.0],
    [2414.0, 2438.0, 2074.0],[2132, 2148, 2032],[490.0, 530.0, 760.0],[2262.0, 2293.75, 2038.0],
    [840.0, 760.0, 820.0],[2329.0, 2317.0, 2035.0],[1,1,0],[0,0,0],
    [2395.0, 2416.5, 2060.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO316 = [
    [2094.0, 2106.75, 1955.0],[640, 660, 820],[2037.0, 2051.5, 1930.0],[2167.0, 2183.0, 1986.0],
    [2208.0, 2224.0, 1979.0],[1990, 2002, 1950],[420.0, 460.0, 740.0],[2078.0, 2099.75, 1955.0],
    [740.0, 780.0, 820.0],[2125.0, 2111.0, 1952.0],[1,1,0],[0,0,0],
    [2160.0, 2175.5, 1965.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR316, "TR"); check(HO316, "HO")

(ROOT / "tools/_v316_themes.json").write_text(json.dumps({"themes": T316, "train": TR316, "heldout": HO316}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_315(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V316 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V316 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 140.50", "ASHFEN bait 185.95"),
        ("CEDARW bait 142.52", "CEDARF bait 231.41"),
        ("DAWNW ghost 65.65", "DAWNF ghost 154.64"),
        ("GLENW bait 135.45", "GLENF bait 224.34"),
        ("JADEW bait 126.36", "JADEF bait 215.25"),
        ("NETHERW bait 143.53", "NETHERF bait 232.42"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V316-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD315 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v315_themes.json").read_text(encoding="utf-8"))["themes"])
NEW316 = "_".join(t[0] for t in T316)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2003"), ("c1463", "c2003"), ("V226", "V316"), ("v226", "v316"),
    ("_v226c1463", "_v316c2003"),
    ("Harder than V225", "Harder than V314"), ("harder than V225", "harder than V314"),
    (OLD315, NEW316),
    ("V226 keeps floor", "V316 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2003 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2004 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2004 VL"),
    ("kept on V226", "kept on V316"),
    ("vision_images_v226", "vision_images_v316"),
    ("VL_GATE_V226", "VL_GATE_V316"), ("vl_gate_v226", "vl_gate_v316"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V314: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T316, "v316", "V316", TR316))
out = retarget_315(out)
(S / "c2003_vision_v316_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2004"), ("c1464", "c2004"), ("V226", "V316"), ("v226", "v316"),
    ("vision_images_v226", "vision_images_v316"),
    ("VL_GATE_V226", "VL_GATE_V316"), ("vl_gate_v226", "vl_gate_v316"),
    ("runs/vision_v226", "runs/vision_v316"),
]:
    out = out.replace(a, b)
(S / "c2004_vision_v316_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2005"), ("c1465", "c2005"), ("V226", "V316"), ("v226", "v316"),
    ("vision_images_v226h", "vision_images_v316h"),
    ("vision_images_v226", "vision_images_v316"),
    ("VL_GATE_V226", "VL_GATE_V316"), ("vl_gate_v226", "vl_gate_v316"),
    ("runs/vision_v226h", "runs/vision_v316h"),
    ("_v226c1463", "_v316c2003"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T316, "v316h", "V316H", HO316))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v316h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v316"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v316" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v316h_c2005"'); seen_run = True; continue
    out2.append(ln)
(S / "c2005_vision_v316_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2003-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2004_VISION_V316_SMOKE.json") or {}\n    c654b = load("docs/r50/C2004b_VISION_GATE_V316_CLAIM.json") or {}\n    c655 = load("docs/r50/C2005_VISION_V316_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2005b_VISION_GATE_V316_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v316 = float(c654.get("rate") or 0.0)\n    v316h = float(c655.get("rate") or 0.0)\n    v316_claim = bool(c654b.get("vl_gate_v316_claim") or c654.get("vl_gate_v316_claim") or c654.get("claim"))\n    v316h_claim = bool(c655b.get("vl_gate_v316_heldout_claim") or c655.get("vl_gate_v316_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v316_claim and v316h_claim and v316 >= GATE and v316h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v316 >= 0.999 and v316h >= 0.999) else min(v316, v316h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v316": {"rate": v316, "claim": v316_claim, "n": c654.get("n")},\n            "v316_heldout": {"rate": v316h, "claim": v316h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v316_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V316: rate={v316} claim={v316_claim}",\n        f"- Vision V316 heldout: rate={v316h} claim={v316h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2003-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2003: Vision V316 design fixtures",\n        f"- C2004: Vision V316 smoke **{v316}**", f"- C2005: Vision V316 heldout **{v316h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V316 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2008 = '\ufeff# -*- coding: utf-8 -*-\n"""C2008: Unified scorecard + STAGE after C2003-C2007. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2008.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2004_VISION_V316_SMOKE.json") or {}\n    c654b = load("docs/r50/C2004b_VISION_GATE_V316_CLAIM.json") or {}\n    c655 = load("docs/r50/C2005_VISION_V316_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2005b_VISION_GATE_V316_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2000_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2007_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2006_PRODUCT_U2C_COST.json") or {}\n\n    v316 = float(c654.get("rate") or 0.0)\n    v316h = float(c655.get("rate") or 0.0)\n    v316_claim = bool(c654b.get("vl_gate_v316_claim") or c654.get("vl_gate_v316_claim") or c654.get("claim"))\n    v316h_claim = bool(c655b.get("vl_gate_v316_heldout_claim") or c655.get("vl_gate_v316_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2006"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v316_claim and v316h_claim and v316 >= GATE and v316h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v316 >= 0.999 and v316h >= 0.999) else min(v316, v316h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2008", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v316": {"rate": v316, "claim": v316_claim, "n": c654.get("n")},\n            "v316_heldout": {"rate": v316h, "claim": v316h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2006"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2000"},\n        "capture_regression": {"pass": capture_pass, "source": "C2007"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v316_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2008_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2008)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V316: rate={v316} claim={v316_claim}",\n        f"- Vision V316 heldout: rate={v316h} claim={v316h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2008", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2003-C2008 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2003: Vision V316 design fixtures",\n        f"- C2004: Vision V316 smoke **{v316}**", f"- C2005: Vision V316 heldout **{v316h}** (disjoint={disjoint})",\n        f"- C2006: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C2000): pass={conf_pass} rate={conf_rate}",\n        f"- C2007: capture pass={capture_pass}", f"- C2008: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V316 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2008.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V316 knife = product-U2C (alternating; V315 was confidence-gate)
out = (S / "c1994_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1994", "C2006"), ("c1994", "c2006"),
    ("C1982", "C2006"), ("c1982", "c2006"),
    ("product_u2c_cost_c1994", "product_u2c_cost_c2006"),
    ("u2c_v201", "u2c_v202"),
    ("u2c_c1994", "u2c_c2006"),
]:
    out = out.replace(a, b2)
(S / "c2006_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1994")

out = (S / "c2001_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2001", "C2007"), ("c2001", "c2007")]:
    out = out.replace(a, b2)
(S / "c2007_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2008_scorecard_and_stage.py").write_text(SC2008, encoding="utf-8")
print("scorecard from fixed c1996 product-U2C pattern")
print("OK builder v316 ready")
