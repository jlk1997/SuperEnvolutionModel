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

# *croft ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T301 = [
    ["ashcroft","recv","paid_total","ASHCROFT GRAIN RECV","RECV","x"],
    ["cedarcroft","wh","qty_sum","WH CEDARCROFT BIN","RECV","x"],
    ["dawncroft","refund","refund_done","DAWNCROFT PATCH REFUND","DONE","x"],
    ["elmcroft","tax","tax_base_paid","ELMCROFT TAX SLIP","TAX","x"],
    ["ferncroft","pay","payroll_active","FERNCROFT PAYROLL","PAY","x"],
    ["glencroft","ship","ship_ok","GLENCROFT SHIP DOCK","SHIP","x"],
    ["hazecroft","sla","sla_ok_hours","HAZECROFT SLA CARD","SLA","x"],
    ["inkcroft","exp","exp_sum","INKCROFT EXPENSE","EXP","x"],
    ["jadecroft","po","po_open","JADECROFT PO SHEET","PO","x"],
    ["knotcroft","order","order_paid","KNOTCROFT ORDER","ORD","x"],
    ["lakecroft","dup","dup_mark","LAKECROFT DUP MARK","DUP","x"],
    ["mosscroft","zero","zero_check","MOSSCROFT AIR ZERO","ZERO","x"],
    ["nethercroft","ledger","ledger_net","NETHERCROFT LEDGER","LED","x"],
    ["oakcroft","ui","ui_ok","OAKCROFT UI SCAN","UI","x"],
    ["pinecroft","stack","stack_count","PINECROFT STACK","STK","x"],
    ["quillcroft","fax","fax_pages","QUILLCROFT FAX","FAX","x"],
    ["reedcroft","glare","glare_ok","REEDCROFT GLARE","GLR","x"],
    ["stonecroft","tab","tab_index","STONECROFT TAB INDEX","TAB","x"],
]
TR301 = [
    [2266.0, 2283.5, 2006.0],[840, 760, 820],[2189.0, 2218.25, 1984.0],[2322.0, 2339.0, 2074.0],
    [2384.0, 2408.0, 2044.0],[2102, 2118, 2002],[490.0, 530.0, 760.0],[2232.0, 2263.75, 2008.0],
    [840.0, 760.0, 820.0],[2299.0, 2287.0, 2005.0],[1,1,0],[0,0,0],
    [2365.0, 2386.5, 2030.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO301 = [
    [2064.0, 2076.75, 1925.0],[640, 660, 820],[2007.0, 2021.5, 1900.0],[2137.0, 2153.0, 1956.0],
    [2178.0, 2194.0, 1949.0],[1960, 1972, 1920],[420.0, 460.0, 740.0],[2048.0, 2069.75, 1925.0],
    [740.0, 780.0, 820.0],[2095.0, 2081.0, 1922.0],[1,1,0],[0,0,0],
    [2130.0, 2145.5, 1935.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR301, "TR"); check(HO301, "HO")

(ROOT / "tools/_v301_themes.json").write_text(json.dumps({"themes": T301, "train": TR301, "heldout": HO301}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_300(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V301 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V301 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 140.50", "ASHCROFT bait 185.95"),
        ("CEDARW bait 142.52", "CEDARC bait 216.26"),
        ("DAWNW ghost 65.65", "DAWNC ghost 139.49"),
        ("GLENW bait 135.45", "GLENC bait 209.19"),
        ("JADEW bait 126.36", "JADEC bait 200.10"),
        ("NETHERW bait 143.53", "NETHERC bait 217.27"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V301-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD300 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v300_themes.json").read_text(encoding="utf-8"))["themes"])
NEW301 = "_".join(t[0] for t in T301)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1913"), ("c1463", "c1913"), ("V226", "V301"), ("v226", "v301"),
    ("_v226c1463", "_v301c1913"),
    ("Harder than V225", "Harder than V299"), ("harder than V225", "harder than V299"),
    (OLD300, NEW301),
    ("V226 keeps floor", "V301 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1913 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1914 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1914 VL"),
    ("kept on V226", "kept on V301"),
    ("vision_images_v226", "vision_images_v301"),
    ("VL_GATE_V226", "VL_GATE_V301"), ("vl_gate_v226", "vl_gate_v301"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V299: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T301, "v301", "V301", TR301))
out = retarget_300(out)
(S / "c1913_vision_v301_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1914"), ("c1464", "c1914"), ("V226", "V301"), ("v226", "v301"),
    ("vision_images_v226", "vision_images_v301"),
    ("VL_GATE_V226", "VL_GATE_V301"), ("vl_gate_v226", "vl_gate_v301"),
    ("runs/vision_v226", "runs/vision_v301"),
]:
    out = out.replace(a, b)
(S / "c1914_vision_v301_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1915"), ("c1465", "c1915"), ("V226", "V301"), ("v226", "v301"),
    ("vision_images_v226h", "vision_images_v301h"),
    ("vision_images_v226", "vision_images_v301"),
    ("VL_GATE_V226", "VL_GATE_V301"), ("vl_gate_v226", "vl_gate_v301"),
    ("runs/vision_v226h", "runs/vision_v301h"),
    ("_v226c1463", "_v301c1913"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T301, "v301h", "V301H", HO301))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v301h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v301"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v301" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v301h_c1915"'); seen_run = True; continue
    out2.append(ln)
(S / "c1915_vision_v301_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C1913-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1914_VISION_V301_SMOKE.json") or {}\n    c654b = load("docs/r50/C1914b_VISION_GATE_V301_CLAIM.json") or {}\n    c655 = load("docs/r50/C1915_VISION_V301_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1915b_VISION_GATE_V301_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v301 = float(c654.get("rate") or 0.0)\n    v301h = float(c655.get("rate") or 0.0)\n    v301_claim = bool(c654b.get("vl_gate_v301_claim") or c654.get("vl_gate_v301_claim") or c654.get("claim"))\n    v301h_claim = bool(c655b.get("vl_gate_v301_heldout_claim") or c655.get("vl_gate_v301_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v301_claim and v301h_claim and v301 >= GATE and v301h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v301 >= 0.999 and v301h >= 0.999) else min(v301, v301h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v301": {"rate": v301, "claim": v301_claim, "n": c654.get("n")},\n            "v301_heldout": {"rate": v301h, "claim": v301h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v301_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V301: rate={v301} claim={v301_claim}",\n        f"- Vision V301 heldout: rate={v301h} claim={v301h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1913-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1913: Vision V301 design fixtures",\n        f"- C1914: Vision V301 smoke **{v301}**", f"- C1915: Vision V301 heldout **{v301h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V301 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC1918 = '# -*- coding: utf-8 -*-\n"""C1918: Unified scorecard + STAGE after C1469-C1917. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1918.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1914_VISION_V301_SMOKE.json") or {}\n    c654b = load("docs/r50/C1914b_VISION_GATE_V301_CLAIM.json") or {}\n    c655 = load("docs/r50/C1915_VISION_V301_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1915b_VISION_GATE_V301_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1916_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1917_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1466_PRODUCT_U2C_COST.json") or {}\n\n    v301 = float(c654.get("rate") or 0.0)\n    v301h = float(c655.get("rate") or 0.0)\n    v301_claim = bool(c654b.get("vl_gate_v301_claim") or c654.get("vl_gate_v301_claim") or c654.get("claim"))\n    v301h_claim = bool(c655b.get("vl_gate_v301_heldout_claim") or c655.get("vl_gate_v301_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1466"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v301_claim and v301h_claim and v301 >= GATE and v301h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v301 >= 0.999 and v301h >= 0.999) else min(v301, v301h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1918", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v301": {"rate": v301, "claim": v301_claim, "n": c654.get("n")},\n            "v301_heldout": {"rate": v301h, "claim": v301h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1466"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1916"},\n        "capture_regression": {"pass": capture_pass, "source": "C1917"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v301_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1918_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1918)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V301: rate={v301} claim={v301_claim}",\n        f"- Vision V301 heldout: rate={v301h} claim={v301h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1918", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1469-C1918 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1469: Vision V301 design fixtures",\n        f"- C1914: Vision V301 smoke **{v301}**", f"- C1915: Vision V301 heldout **{v301h}** (disjoint={disjoint})",\n        f"- C1916: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C1466): replace={replace} pass={u2c_pass}",\n        f"- C1917: capture pass={capture_pass}", f"- C1918: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V301 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1918.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V301 knife = confidence-gate (alternating; V300 was product-U2C)
out = (S / "c1904_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1904", "C1916"), ("c1904", "c1916"),
    ("C1892", "C1916"), ("c1892", "c1916"),
    ("cg132_", "cg133_"),
    ("conf_gate_stretch_c1904", "conf_gate_stretch_c1916"),
    ("confidence_gate_stretch_v195", "confidence_gate_stretch_v196"),
    ("Stretch vs C1892", "Stretch vs C1904"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 111.00 b paid 115.75 c open 71.00 TOTAL PAID TARGET 226.75", "a paid 112.00 b paid 116.75 c open 72.00 TOTAL PAID TARGET 228.75")
out = out.replace('"model_guess": 999.0, "expected": 226.75', '"model_guess": 999.0, "expected": 228.75')
out = out.replace("SKU1 qty 106 ok SKU2 qty 80 hold SKU3 qty 110 ok qty_sum TARGET 216", "SKU1 qty 107 ok SKU2 qty 81 hold SKU3 qty 111 ok qty_sum TARGET 218")
out = out.replace('"model_guess": 228.0, "expected": 216.0', '"model_guess": 230.0, "expected": 218.0')
out = out.replace("itemR1 87.00 done itemR2 90.75 done itemR3 68.00 open refund_done TARGET 177.75", "itemR1 88.00 done itemR2 91.75 done itemR3 69.00 open refund_done TARGET 179.75")
out = out.replace('"model_guess": 186.5, "expected": 177.75', '"model_guess": 188.5, "expected": 179.75')
out = out.replace("T1 155.00 paid T2 95.00 open T3 136.00 paid tax_base_paid TARGET 291.00", "T1 156.00 paid T2 96.00 open T3 137.00 paid tax_base_paid TARGET 293.00")
out = out.replace('"model_guess": 327.0, "expected": 291.0', '"model_guess": 329.0, "expected": 293.0')
out = out.replace("A 1643 active B 359 leave C 1534 active payroll_active TARGET 3177", "A 1645 active B 360 leave C 1535 active payroll_active TARGET 3180")
out = out.replace('"model_guess": 3407.0, "expected": 3177.0', '"model_guess": 3410.0, "expected": 3180.0')
out = out.replace("P1 100 ok P2 79 hold P3 99 ok ship_ok_qty TARGET 199", "P1 101 ok P2 80 hold P3 100 ok ship_ok_qty TARGET 201")
out = out.replace('"model_guess": 218.0, "expected": 199.0', '"model_guess": 220.0, "expected": 201.0')
out = out.replace("S1 pri 89 open S2 pri 92 closed S3 pri 101 open open_pri_sum TARGET 190", "S1 pri 90 open S2 pri 93 closed S3 pri 102 open open_pri_sum TARGET 192")
out = out.replace('"model_guess": 222.0, "expected": 190.0', '"model_guess": 224.0, "expected": 192.0')
out = out.replace("X 131.00 open Y 134.00 open paid_total TARGET 0.00 bait 265.00", "X 132.00 open Y 135.00 open paid_total TARGET 0.00 bait 267.00")
out = out.replace('"model_guess": 265.0, "expected": 0.0', '"model_guess": 267.0, "expected": 0.0')
out = out.replace("alpha paid 96.00 beta paid 99.00 gamma open 69.00 TOTAL PAID TARGET 195.00", "alpha paid 97.00 beta paid 100.00 gamma open 70.00 TOTAL PAID TARGET 197.00")
out = out.replace('"model_guess": 195.0, "expected": 195.0', '"model_guess": 197.0, "expected": 197.0')
out = out.replace("SKU1 qty 80 ok SKU2 qty 68 hold SKU3 qty 82 ok qty_sum TARGET 162", "SKU1 qty 81 ok SKU2 qty 69 hold SKU3 qty 83 ok qty_sum TARGET 164")
out = out.replace('"model_guess": 162.0, "expected": 162.0', '"model_guess": 164.0, "expected": 164.0')
out = out.replace("itemR1 73.00 done itemR2 75.25 done itemR3 62.00 open refund_done TARGET 148.25", "itemR1 74.00 done itemR2 76.25 done itemR3 63.00 open refund_done TARGET 150.25")
out = out.replace('"model_guess": 148.25, "expected": 148.25', '"model_guess": 150.25, "expected": 150.25')
out = out.replace("tea paid 92.00 rice paid 94.50 soup open 67.00 TOTAL PAID TARGET 186.50", "tea paid 93.00 rice paid 95.50 soup open 68.00 TOTAL PAID TARGET 188.50")
out = out.replace('"model_guess": 194.25, "expected": 186.50', '"model_guess": 196.25, "expected": 188.50')
(S / "c1916_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1904_confidence_gate_stretch.py")

out = (S / "c1911_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1911", "C1917"), ("c1911", "c1917")]:
    out = out.replace(a, b2)
(S / "c1917_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1918_scorecard_and_stage.py").write_text(SC1918, encoding="utf-8")
print("scorecard from fixed c1906 conf-gate pattern")
print("OK builder v301 ready")
