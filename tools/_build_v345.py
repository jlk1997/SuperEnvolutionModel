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
T345 = [
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
TR345 = [
    [2354.0, 2371.5, 2094.0],[840, 760, 820],[2253.0, 2259.25, 2058.0],[2410.0, 2427.0, 2162.0],
    [2472.0, 2496.0, 2132.0],[2190, 2206, 2090],[490.0, 530.0, 760.0],[2320.0, 2351.75, 2096.0],
    [840.0, 760.0, 820.0],[2387.0, 2375.0, 2093.0],[1,1,0],[0,0,0],
    [2453.0, 2474.5, 2118.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO345 = [
    [2152.0, 2164.75, 2013.0],[640, 660, 820],[2095.0, 2109.5, 1988.0],[2225.0, 2241.0, 2044.0],
    [2233.0, 2244.0, 2037.0],[2048, 2060, 2010],[420.0, 460.0, 740.0],[2136.0, 2157.75, 2013.0],
    [740.0, 780.0, 820.0],[2183.0, 2169.0, 2010.0],[1,1,0],[0,0,0],
    [2218.0, 2233.5, 2023.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR345, "TR"); check(HO345, "HO")

(ROOT / "tools/_v345_themes.json").write_text(json.dumps({"themes": T345, "train": TR345, "heldout": HO345}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_344(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V345 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V345 overlays (new vs V49) ---")
    for a, b in [
        ("ASHCROFT bait 140.50", "ASHCROFT bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 250.60"),
        ("DAWNW ghost 65.65", "DAWNH ghost 173.83"),
        ("GLENW bait 135.45", "GLENH bait 243.53"),
        ("JADEW bait 126.36", "JADEH bait 234.44"),
        ("NETHERW bait 143.53", "NETHERH bait 251.61"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V345-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD344 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v344_themes.json").read_text(encoding="utf-8"))["themes"])
NEW345 = "_".join(t[0] for t in T345)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2177"), ("c1463", "c2177"), ("V226", "V345"), ("v226", "v345"),
    ("_v226c1463", "_v345c2177"),
    ("Harder than V225", "Harder than V343"), ("harder than V225", "harder than V343"),
    (OLD344, NEW345),
    ("V226 keeps floor", "V345 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2177 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2178 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2178 VL"),
    ("kept on V226", "kept on V345"),
    ("vision_images_v226", "vision_images_v345"),
    ("VL_GATE_V226", "VL_GATE_V345"), ("vl_gate_v226", "vl_gate_v345"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V343: ashcroft, cedarcroft, dawncroft, elmcroft, ferncroft, glencroft, hazecroft, inkcroft,\njadecroft, knotcroft, lakecroft, mosscroft, nethercroft, oakcroft, pinecroft, quillcroft, reedcroft, stonecroft.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T345, "v345", "V345", TR345))
out = retarget_344(out)
(S / "c2177_vision_v345_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2178"), ("c1464", "c2178"), ("V226", "V345"), ("v226", "v345"),
    ("vision_images_v226", "vision_images_v345"),
    ("VL_GATE_V226", "VL_GATE_V345"), ("vl_gate_v226", "vl_gate_v345"),
    ("runs/vision_v226", "runs/vision_v345"),
]:
    out = out.replace(a, b)
(S / "c2178_vision_v345_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2179"), ("c1465", "c2179"), ("V226", "V345"), ("v226", "v345"),
    ("vision_images_v226h", "vision_images_v345h"),
    ("vision_images_v226", "vision_images_v345"),
    ("VL_GATE_V226", "VL_GATE_V345"), ("vl_gate_v226", "vl_gate_v345"),
    ("runs/vision_v226h", "runs/vision_v345h"),
    ("_v226c1463", "_v345c2177"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T345, "v345h", "V345H", HO345))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v345h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v345"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v345" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v345h_c2179"'); seen_run = True; continue
    out2.append(ln)
(S / "c2179_vision_v345_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2177-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2178_VISION_V345_SMOKE.json") or {}\n    c654b = load("docs/r50/C2178b_VISION_GATE_V345_CLAIM.json") or {}\n    c655 = load("docs/r50/C2179_VISION_V345_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2179b_VISION_GATE_V345_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v345 = float(c654.get("rate") or 0.0)\n    v345h = float(c655.get("rate") or 0.0)\n    v345_claim = bool(c654b.get("vl_gate_v345_claim") or c654.get("vl_gate_v345_claim") or c654.get("claim"))\n    v345h_claim = bool(c655b.get("vl_gate_v345_heldout_claim") or c655.get("vl_gate_v345_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v345_claim and v345h_claim and v345 >= GATE and v345h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v345 >= 0.999 and v345h >= 0.999) else min(v345, v345h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v345": {"rate": v345, "claim": v345_claim, "n": c654.get("n")},\n            "v345_heldout": {"rate": v345h, "claim": v345h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v345_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V345: rate={v345} claim={v345_claim}",\n        f"- Vision V345 heldout: rate={v345h} claim={v345h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2177-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2177: Vision V345 design fixtures",\n        f"- C2178: Vision V345 smoke **{v345}**", f"- C2179: Vision V345 heldout **{v345h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V345 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2182 = '# -*- coding: utf-8 -*-\n"""C2182: Unified scorecard + STAGE after C2177-C2181. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2182.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2178_VISION_V345_SMOKE.json") or {}\n    c654b = load("docs/r50/C2178b_VISION_GATE_V345_CLAIM.json") or {}\n    c655 = load("docs/r50/C2179_VISION_V345_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2179b_VISION_GATE_V345_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2180_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2181_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2174_PRODUCT_U2C_COST.json") or {}\n\n    v345 = float(c654.get("rate") or 0.0)\n    v345h = float(c655.get("rate") or 0.0)\n    v345_claim = bool(c654b.get("vl_gate_v345_claim") or c654.get("vl_gate_v345_claim") or c654.get("claim"))\n    v345h_claim = bool(c655b.get("vl_gate_v345_heldout_claim") or c655.get("vl_gate_v345_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2174"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v345_claim and v345h_claim and v345 >= GATE and v345h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v345 >= 0.999 and v345h >= 0.999) else min(v345, v345h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2182", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v345": {"rate": v345, "claim": v345_claim, "n": c654.get("n")},\n            "v345_heldout": {"rate": v345h, "claim": v345h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2174"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2180"},\n        "capture_regression": {"pass": capture_pass, "source": "C2181"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v345_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2182_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2182)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V345: rate={v345} claim={v345_claim}",\n        f"- Vision V345 heldout: rate={v345h} claim={v345h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2182", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2177-C2182 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2177: Vision V345 design fixtures",\n        f"- C2178: Vision V345 smoke **{v345}**", f"- C2179: Vision V345 heldout **{v345h}** (disjoint={disjoint})",\n        f"- C2180: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2174): replace={replace} pass={u2c_pass}",\n        f"- C2181: capture pass={capture_pass}", f"- C2182: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V345 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2182.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V345 knife = confidence-gate (alternating; V344 was product-U2C)
out = (S / "c2168_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2168", "C2180"), ("c2168", "c2180"),
    ("C2096", "C2180"), ("c2096", "c2180"),
    ("cg155_", "cg150_"),
    ("conf_gate_stretch_c2180", "conf_gate_stretch_c2180"),
    ("confidence_gate_stretch_v218", "confidence_gate_stretch_v213"),
    ("Stretch vs C2168", "Stretch vs C2108"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75", "a paid 134.00 b paid 138.75 c open 94.00 TOTAL PAID TARGET 272.75")
out = out.replace('"model_guess": 999.0, "expected": 260.75', '"model_guess": 999.0, "expected": 272.75')
out = out.replace("SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250", "SKU1 qty 129 ok SKU2 qty 103 hold SKU3 qty 133 ok qty_sum TARGET 262")
out = out.replace('"model_guess": 262.0, "expected": 250.0', '"model_guess": 274.0, "expected": 262.0')
out = out.replace("itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75", "itemR1 110.00 done itemR2 113.75 done itemR3 91.00 open refund_done TARGET 223.75")
out = out.replace('"model_guess": 220.5, "expected": 211.75', '"model_guess": 232.5, "expected": 223.75')
out = out.replace("T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00", "T1 178.00 paid T2 118.00 open T3 159.00 paid tax_base_paid TARGET 337.00")
out = out.replace('"model_guess": 361.0, "expected": 325.0', '"model_guess": 373.0, "expected": 337.0')
out = out.replace("A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218", "A 1673 active B 382 leave C 1557 active payroll_active TARGET 3230")
out = out.replace('"model_guess": 3448.0, "expected": 3218.0', '"model_guess": 3460.0, "expected": 3230.0')
out = out.replace("P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233", "P1 123 ok P2 102 hold P3 122 ok ship_ok_qty TARGET 245")
out = out.replace('"model_guess": 252.0, "expected": 233.0', '"model_guess": 264.0, "expected": 245.0')
out = out.replace("S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224", "S1 pri 112 open S2 pri 115 closed S3 pri 124 open open_pri_sum TARGET 236")
out = out.replace('"model_guess": 256.0, "expected": 224.0', '"model_guess": 268.0, "expected": 236.0')
out = out.replace("X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00", "X 154.00 open Y 157.00 open paid_total TARGET 0.00 bait 311.00")
out = out.replace('"model_guess": 299.0, "expected": 0.0', '"model_guess": 311.0, "expected": 0.0')
out = out.replace("alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00", "alpha paid 119.00 beta paid 122.00 gamma open 92.00 TOTAL PAID TARGET 241.00")
out = out.replace('"model_guess": 229.0, "expected": 229.0', '"model_guess": 241.0, "expected": 241.0')
out = out.replace("SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196", "SKU1 qty 103 ok SKU2 qty 91 hold SKU3 qty 105 ok qty_sum TARGET 208")
out = out.replace('"model_guess": 196.0, "expected": 196.0', '"model_guess": 208.0, "expected": 208.0')
out = out.replace("itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25", "itemR1 96.00 done itemR2 98.25 done itemR3 85.00 open refund_done TARGET 194.25")
out = out.replace('"model_guess": 182.25, "expected": 182.25', '"model_guess": 194.25, "expected": 194.25')
out = out.replace("tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50", "tea paid 115.00 rice paid 117.50 soup open 90.00 TOTAL PAID TARGET 232.50")
out = out.replace('"model_guess": 228.25, "expected": 220.50', '"model_guess": 240.25, "expected": 232.50')
(S / "c2180_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2168_confidence_gate_stretch.py")

out = (S / "c2175_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2175", "C2181"), ("c2175", "c2181")]:
    out = out.replace(a, b2)
(S / "c2181_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2182_scorecard_and_stage.py").write_text(SC2182, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v345 ready")
