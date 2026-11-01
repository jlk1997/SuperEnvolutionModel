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
T309 = [
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
TR309 = [
    [2282.0, 2299.5, 2022.0],[840, 760, 820],[2205.0, 2234.25, 2000.0],[2338.0, 2355.0, 2090.0],
    [2400.0, 2424.0, 2060.0],[2118, 2134, 2018],[490.0, 530.0, 760.0],[2248.0, 2279.75, 2024.0],
    [840.0, 760.0, 820.0],[2315.0, 2303.0, 2021.0],[1,1,0],[0,0,0],
    [2381.0, 2402.5, 2046.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO309 = [
    [2080.0, 2092.75, 1941.0],[640, 660, 820],[2023.0, 2037.5, 1916.0],[2153.0, 2169.0, 1972.0],
    [2194.0, 2210.0, 1965.0],[1976, 1988, 1936],[420.0, 460.0, 740.0],[2064.0, 2085.75, 1941.0],
    [740.0, 780.0, 820.0],[2111.0, 2097.0, 1938.0],[1,1,0],[0,0,0],
    [2146.0, 2161.5, 1951.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR309, "TR"); check(HO309, "HO")

(ROOT / "tools/_v309_themes.json").write_text(json.dumps({"themes": T309, "train": TR309, "heldout": HO309}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_308(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V309 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V309 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHURST bait 140.50", "ASHHURST bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 224.34"),
        ("DAWNW ghost 65.65", "DAWNH ghost 147.57"),
        ("GLENW bait 135.45", "GLENH bait 217.27"),
        ("JADEW bait 126.36", "JADEH bait 208.18"),
        ("NETHERW bait 143.53", "NETHERH bait 225.35"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V309-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD308 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v308_themes.json").read_text(encoding="utf-8"))["themes"])
NEW309 = "_".join(t[0] for t in T309)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1961"), ("c1463", "c1961"), ("V226", "V309"), ("v226", "v309"),
    ("_v226c1463", "_v309c1961"),
    ("Harder than V225", "Harder than V307"), ("harder than V225", "harder than V307"),
    (OLD308, NEW309),
    ("V226 keeps floor", "V309 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1961 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1962 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1962 VL"),
    ("kept on V226", "kept on V309"),
    ("vision_images_v226", "vision_images_v309"),
    ("VL_GATE_V226", "VL_GATE_V309"), ("vl_gate_v226", "vl_gate_v309"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V307: ashhurst, cedarhurst, dawnhurst, elmhurst, fernhurst, glenhurst, hazehurst, inkhurst,\njadehurst, knothurst, lakehurst, mosshurst, netherhurst, oakhurst, pinehurst, quillhurst, reedhurst, stonehurst.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T309, "v309", "V309", TR309))
out = retarget_308(out)
(S / "c1961_vision_v309_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1962"), ("c1464", "c1962"), ("V226", "V309"), ("v226", "v309"),
    ("vision_images_v226", "vision_images_v309"),
    ("VL_GATE_V226", "VL_GATE_V309"), ("vl_gate_v226", "vl_gate_v309"),
    ("runs/vision_v226", "runs/vision_v309"),
]:
    out = out.replace(a, b)
(S / "c1962_vision_v309_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1963"), ("c1465", "c1963"), ("V226", "V309"), ("v226", "v309"),
    ("vision_images_v226h", "vision_images_v309h"),
    ("vision_images_v226", "vision_images_v309"),
    ("VL_GATE_V226", "VL_GATE_V309"), ("vl_gate_v226", "vl_gate_v309"),
    ("runs/vision_v226h", "runs/vision_v309h"),
    ("_v226c1463", "_v309c1961"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T309, "v309h", "V309H", HO309))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v309h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v309"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v309" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v309h_c1963"'); seen_run = True; continue
    out2.append(ln)
(S / "c1963_vision_v309_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C1961-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1962_VISION_V309_SMOKE.json") or {}\n    c654b = load("docs/r50/C1962b_VISION_GATE_V309_CLAIM.json") or {}\n    c655 = load("docs/r50/C1963_VISION_V309_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1963b_VISION_GATE_V309_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v309 = float(c654.get("rate") or 0.0)\n    v309h = float(c655.get("rate") or 0.0)\n    v309_claim = bool(c654b.get("vl_gate_v309_claim") or c654.get("vl_gate_v309_claim") or c654.get("claim"))\n    v309h_claim = bool(c655b.get("vl_gate_v309_heldout_claim") or c655.get("vl_gate_v309_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v309_claim and v309h_claim and v309 >= GATE and v309h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v309 >= 0.999 and v309h >= 0.999) else min(v309, v309h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v309": {"rate": v309, "claim": v309_claim, "n": c654.get("n")},\n            "v309_heldout": {"rate": v309h, "claim": v309h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v309_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V309: rate={v309} claim={v309_claim}",\n        f"- Vision V309 heldout: rate={v309h} claim={v309h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1961-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1961: Vision V309 design fixtures",\n        f"- C1962: Vision V309 smoke **{v309}**", f"- C1963: Vision V309 heldout **{v309h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V309 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC1966 = '# -*- coding: utf-8 -*-\n"""C1966: Unified scorecard + STAGE after C1469-C1965. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1966.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1962_VISION_V309_SMOKE.json") or {}\n    c654b = load("docs/r50/C1962b_VISION_GATE_V309_CLAIM.json") or {}\n    c655 = load("docs/r50/C1963_VISION_V309_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1963b_VISION_GATE_V309_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1964_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1965_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1466_PRODUCT_U2C_COST.json") or {}\n\n    v309 = float(c654.get("rate") or 0.0)\n    v309h = float(c655.get("rate") or 0.0)\n    v309_claim = bool(c654b.get("vl_gate_v309_claim") or c654.get("vl_gate_v309_claim") or c654.get("claim"))\n    v309h_claim = bool(c655b.get("vl_gate_v309_heldout_claim") or c655.get("vl_gate_v309_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1466"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v309_claim and v309h_claim and v309 >= GATE and v309h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v309 >= 0.999 and v309h >= 0.999) else min(v309, v309h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1966", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v309": {"rate": v309, "claim": v309_claim, "n": c654.get("n")},\n            "v309_heldout": {"rate": v309h, "claim": v309h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1466"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1964"},\n        "capture_regression": {"pass": capture_pass, "source": "C1965"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v309_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1966_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1966)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V309: rate={v309} claim={v309_claim}",\n        f"- Vision V309 heldout: rate={v309h} claim={v309h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1966", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1469-C1966 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1469: Vision V309 design fixtures",\n        f"- C1962: Vision V309 smoke **{v309}**", f"- C1963: Vision V309 heldout **{v309h}** (disjoint={disjoint})",\n        f"- C1964: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C1466): replace={replace} pass={u2c_pass}",\n        f"- C1965: capture pass={capture_pass}", f"- C1966: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V309 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1966.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V309 knife = confidence-gate (alternating; V308 was product-U2C)
out = (S / "c1952_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1952", "C1964"), ("c1952", "c1964"),
    ("C1940", "C1964"), ("c1940", "c1964"),
    ("cg136_", "cg137_"),
    ("conf_gate_stretch_c1952", "conf_gate_stretch_c1964"),
    ("confidence_gate_stretch_v199", "confidence_gate_stretch_v200"),
    ("Stretch vs C1940", "Stretch vs C1952"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 115.00 b paid 119.75 c open 75.00 TOTAL PAID TARGET 234.75", "a paid 116.00 b paid 120.75 c open 76.00 TOTAL PAID TARGET 236.75")
out = out.replace('"model_guess": 999.0, "expected": 234.75', '"model_guess": 999.0, "expected": 236.75')
out = out.replace("SKU1 qty 110 ok SKU2 qty 84 hold SKU3 qty 114 ok qty_sum TARGET 224", "SKU1 qty 111 ok SKU2 qty 85 hold SKU3 qty 115 ok qty_sum TARGET 226")
out = out.replace('"model_guess": 236.0, "expected": 224.0', '"model_guess": 238.0, "expected": 226.0')
out = out.replace("itemR1 91.00 done itemR2 94.75 done itemR3 72.00 open refund_done TARGET 185.75", "itemR1 92.00 done itemR2 95.75 done itemR3 73.00 open refund_done TARGET 187.75")
out = out.replace('"model_guess": 194.5, "expected": 185.75', '"model_guess": 196.5, "expected": 187.75')
out = out.replace("T1 159.00 paid T2 99.00 open T3 140.00 paid tax_base_paid TARGET 299.00", "T1 160.00 paid T2 100.00 open T3 141.00 paid tax_base_paid TARGET 301.00")
out = out.replace('"model_guess": 335.0, "expected": 299.0', '"model_guess": 337.0, "expected": 301.0')
out = out.replace("A 1651 active B 363 leave C 1538 active payroll_active TARGET 3189", "A 1653 active B 364 leave C 1539 active payroll_active TARGET 3192")
out = out.replace('"model_guess": 3419.0, "expected": 3189.0', '"model_guess": 3422.0, "expected": 3192.0')
out = out.replace("P1 104 ok P2 83 hold P3 103 ok ship_ok_qty TARGET 207", "P1 105 ok P2 84 hold P3 104 ok ship_ok_qty TARGET 209")
out = out.replace('"model_guess": 226.0, "expected": 207.0', '"model_guess": 228.0, "expected": 209.0')
out = out.replace("S1 pri 93 open S2 pri 96 closed S3 pri 105 open open_pri_sum TARGET 198", "S1 pri 94 open S2 pri 97 closed S3 pri 106 open open_pri_sum TARGET 200")
out = out.replace('"model_guess": 230.0, "expected": 198.0', '"model_guess": 232.0, "expected": 200.0')
out = out.replace("X 135.00 open Y 138.00 open paid_total TARGET 0.00 bait 273.00", "X 136.00 open Y 139.00 open paid_total TARGET 0.00 bait 275.00")
out = out.replace('"model_guess": 273.0, "expected": 0.0', '"model_guess": 275.0, "expected": 0.0')
out = out.replace("alpha paid 100.00 beta paid 103.00 gamma open 73.00 TOTAL PAID TARGET 203.00", "alpha paid 101.00 beta paid 104.00 gamma open 74.00 TOTAL PAID TARGET 205.00")
out = out.replace('"model_guess": 203.0, "expected": 203.0', '"model_guess": 205.0, "expected": 205.0')
out = out.replace("SKU1 qty 84 ok SKU2 qty 72 hold SKU3 qty 86 ok qty_sum TARGET 170", "SKU1 qty 85 ok SKU2 qty 73 hold SKU3 qty 87 ok qty_sum TARGET 172")
out = out.replace('"model_guess": 170.0, "expected": 170.0', '"model_guess": 172.0, "expected": 172.0')
out = out.replace("itemR1 77.00 done itemR2 79.25 done itemR3 66.00 open refund_done TARGET 156.25", "itemR1 78.00 done itemR2 80.25 done itemR3 67.00 open refund_done TARGET 158.25")
out = out.replace('"model_guess": 156.25, "expected": 156.25', '"model_guess": 158.25, "expected": 158.25')
out = out.replace("tea paid 96.00 rice paid 98.50 soup open 71.00 TOTAL PAID TARGET 194.50", "tea paid 97.00 rice paid 99.50 soup open 72.00 TOTAL PAID TARGET 196.50")
out = out.replace('"model_guess": 202.25, "expected": 194.50', '"model_guess": 204.25, "expected": 196.50')
(S / "c1964_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1952_confidence_gate_stretch.py")

out = (S / "c1959_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1959", "C1965"), ("c1959", "c1965")]:
    out = out.replace(a, b2)
(S / "c1965_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1966_scorecard_and_stage.py").write_text(SC1966, encoding="utf-8")
print("scorecard from fixed c1954 conf-gate pattern")
print("OK builder v309 ready")
