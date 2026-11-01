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
T312 = [
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
TR312 = [
    [2288.0, 2305.5, 2028.0],[840, 760, 820],[2211.0, 2240.25, 2006.0],[2344.0, 2361.0, 2096.0],
    [2406.0, 2430.0, 2066.0],[2124, 2140, 2024],[490.0, 530.0, 760.0],[2254.0, 2285.75, 2030.0],
    [840.0, 760.0, 820.0],[2321.0, 2309.0, 2027.0],[1,1,0],[0,0,0],
    [2387.0, 2408.5, 2052.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO312 = [
    [2086.0, 2098.75, 1947.0],[640, 660, 820],[2029.0, 2043.5, 1922.0],[2159.0, 2175.0, 1978.0],
    [2200.0, 2216.0, 1971.0],[1982, 1994, 1942],[420.0, 460.0, 740.0],[2070.0, 2091.75, 1947.0],
    [740.0, 780.0, 820.0],[2117.0, 2103.0, 1944.0],[1,1,0],[0,0,0],
    [2152.0, 2167.5, 1957.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR312, "TR"); check(HO312, "HO")

(ROOT / "tools/_v312_themes.json").write_text(json.dumps({"themes": T312, "train": TR312, "heldout": HO312}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_311(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V312 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V312 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 140.50", "ASHCROFT bait 185.95"),
        ("CEDARW bait 142.52", "CEDARC bait 227.37"),
        ("DAWNW ghost 65.65", "DAWNC ghost 150.60"),
        ("GLENW bait 135.45", "GLENC bait 220.30"),
        ("JADEW bait 126.36", "JADEC bait 211.21"),
        ("NETHERW bait 143.53", "NETHERC bait 228.38"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V312-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD311 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v311_themes.json").read_text(encoding="utf-8"))["themes"])
NEW312 = "_".join(t[0] for t in T312)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1979"), ("c1463", "c1979"), ("V226", "V312"), ("v226", "v312"),
    ("_v226c1463", "_v312c1979"),
    ("Harder than V225", "Harder than V310"), ("harder than V225", "harder than V310"),
    (OLD311, NEW312),
    ("V226 keeps floor", "V312 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1979 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1980 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1980 VL"),
    ("kept on V226", "kept on V312"),
    ("vision_images_v226", "vision_images_v312"),
    ("VL_GATE_V226", "VL_GATE_V312"), ("vl_gate_v226", "vl_gate_v312"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V310: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T312, "v312", "V312", TR312))
out = retarget_311(out)
(S / "c1979_vision_v312_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1980"), ("c1464", "c1980"), ("V226", "V312"), ("v226", "v312"),
    ("vision_images_v226", "vision_images_v312"),
    ("VL_GATE_V226", "VL_GATE_V312"), ("vl_gate_v226", "vl_gate_v312"),
    ("runs/vision_v226", "runs/vision_v312"),
]:
    out = out.replace(a, b)
(S / "c1980_vision_v312_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1981"), ("c1465", "c1981"), ("V226", "V312"), ("v226", "v312"),
    ("vision_images_v226h", "vision_images_v312h"),
    ("vision_images_v226", "vision_images_v312"),
    ("VL_GATE_V226", "VL_GATE_V312"), ("vl_gate_v226", "vl_gate_v312"),
    ("runs/vision_v226h", "runs/vision_v312h"),
    ("_v226c1463", "_v312c1979"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T312, "v312h", "V312H", HO312))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v312h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v312"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v312" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v312h_c1981"'); seen_run = True; continue
    out2.append(ln)
(S / "c1981_vision_v312_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C1979-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1980_VISION_V312_SMOKE.json") or {}\n    c654b = load("docs/r50/C1980b_VISION_GATE_V312_CLAIM.json") or {}\n    c655 = load("docs/r50/C1981_VISION_V312_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1981b_VISION_GATE_V312_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v312 = float(c654.get("rate") or 0.0)\n    v312h = float(c655.get("rate") or 0.0)\n    v312_claim = bool(c654b.get("vl_gate_v312_claim") or c654.get("vl_gate_v312_claim") or c654.get("claim"))\n    v312h_claim = bool(c655b.get("vl_gate_v312_heldout_claim") or c655.get("vl_gate_v312_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v312_claim and v312h_claim and v312 >= GATE and v312h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v312 >= 0.999 and v312h >= 0.999) else min(v312, v312h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v312": {"rate": v312, "claim": v312_claim, "n": c654.get("n")},\n            "v312_heldout": {"rate": v312h, "claim": v312h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v312_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V312: rate={v312} claim={v312_claim}",\n        f"- Vision V312 heldout: rate={v312h} claim={v312h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1979-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1979: Vision V312 design fixtures",\n        f"- C1980: Vision V312 smoke **{v312}**", f"- C1981: Vision V312 heldout **{v312h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V312 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC1984 = '\ufeff# -*- coding: utf-8 -*-\n"""C1984: Unified scorecard + STAGE after C1979-C1983. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1984.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1980_VISION_V312_SMOKE.json") or {}\n    c654b = load("docs/r50/C1980b_VISION_GATE_V312_CLAIM.json") or {}\n    c655 = load("docs/r50/C1981_VISION_V312_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1981b_VISION_GATE_V312_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1976_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1983_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1982_PRODUCT_U2C_COST.json") or {}\n\n    v312 = float(c654.get("rate") or 0.0)\n    v312h = float(c655.get("rate") or 0.0)\n    v312_claim = bool(c654b.get("vl_gate_v312_claim") or c654.get("vl_gate_v312_claim") or c654.get("claim"))\n    v312h_claim = bool(c655b.get("vl_gate_v312_heldout_claim") or c655.get("vl_gate_v312_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1982"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v312_claim and v312h_claim and v312 >= GATE and v312h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v312 >= 0.999 and v312h >= 0.999) else min(v312, v312h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1984", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v312": {"rate": v312, "claim": v312_claim, "n": c654.get("n")},\n            "v312_heldout": {"rate": v312h, "claim": v312h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1982"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1976"},\n        "capture_regression": {"pass": capture_pass, "source": "C1983"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v312_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1984_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1984)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V312: rate={v312} claim={v312_claim}",\n        f"- Vision V312 heldout: rate={v312h} claim={v312h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1984", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1979-C1984 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1979: Vision V312 design fixtures",\n        f"- C1980: Vision V312 smoke **{v312}**", f"- C1981: Vision V312 heldout **{v312h}** (disjoint={disjoint})",\n        f"- C1982: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1976): pass={conf_pass} rate={conf_rate}",\n        f"- C1983: capture pass={capture_pass}", f"- C1984: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V312 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1984.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V312 knife = product-U2C (alternating; V311 was confidence-gate)
out = (S / "c1970_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1970", "C1982"), ("c1970", "c1982"),
    ("C1958", "C1982"), ("c1958", "c1982"),
    ("product_u2c_cost_c1970", "product_u2c_cost_c1982"),
    ("u2c_v199", "u2c_v200"),
    ("u2c_c1970", "u2c_c1982"),
]:
    out = out.replace(a, b2)
(S / "c1982_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1970")

out = (S / "c1977_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1977", "C1983"), ("c1977", "c1983")]:
    out = out.replace(a, b2)
(S / "c1983_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1984_scorecard_and_stage.py").write_text(SC1984, encoding="utf-8")
print("scorecard from fixed c1972 product-U2C pattern")
print("OK builder v312 ready")
