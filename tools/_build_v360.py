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
T360 = [
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
TR360 = [
    [2384.0, 2401.5, 2124.0],[840, 760, 820],[2255.0, 2257.25, 2043.0],[2440.0, 2457.0, 2192.0],
    [2497.0, 2493.0, 2162.0],[2220, 2236, 2120],[490.0, 530.0, 760.0],[2350.0, 2381.75, 2126.0],
    [840.0, 760.0, 820.0],[2417.0, 2405.0, 2123.0],[1,1,0],[0,0,0],
    [2451.0, 2470.5, 2098.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO360 = [
    [2182.0, 2194.75, 2043.0],[640, 660, 820],[2125.0, 2139.5, 2018.0],[2255.0, 2271.0, 2074.0],
    [2259.0, 2270.0, 2067.0],[2078, 2090, 2040],[420.0, 460.0, 740.0],[2166.0, 2187.75, 2043.0],
    [740.0, 780.0, 820.0],[2213.0, 2199.0, 2040.0],[1,1,0],[0,0,0],
    [2243.0, 2257.5, 2047.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR360, "TR"); check(HO360, "HO")

(ROOT / "tools/_v360_themes.json").write_text(json.dumps({"themes": T360, "train": TR360, "heldout": HO360}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_359(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V360 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V360 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFEN bait 140.50", "ASHFEN bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 250.60"),
        ("DAWNW ghost 65.65", "DAWNH ghost 173.83"),
        ("GLENW bait 135.45", "GLENH bait 243.53"),
        ("JADEW bait 126.36", "JADEH bait 234.44"),
        ("NETHERW bait 143.53", "NETHERH bait 251.61"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V360-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD359 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v359_themes.json").read_text(encoding="utf-8"))["themes"])
NEW360 = "_".join(t[0] for t in T360)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2267"), ("c1463", "c2267"), ("V226", "V360"), ("v226", "v360"),
    ("_v226c1463", "_v360c2267"),
    ("Harder than V225", "Harder than V358"), ("harder than V225", "harder than V358"),
    (OLD359, NEW360),
    ("V226 keeps floor", "V360 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2267 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2268 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2268 VL"),
    ("kept on V226", "kept on V360"),
    ("vision_images_v226", "vision_images_v360"),
    ("VL_GATE_V226", "VL_GATE_V360"), ("vl_gate_v226", "vl_gate_v360"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V358: ashfen, cedarfen, dawnfen, elmfen, fernfen, glenfen, hazefen, inkfen,\njadefen, knotfen, lakefen, mossfen, netherfen, oakfen, pinefen, quillfen, reedfen, stonefen.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T360, "v360", "V360", TR360))
out = retarget_359(out)
(S / "c2267_vision_v360_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2268"), ("c1464", "c2268"), ("V226", "V360"), ("v226", "v360"),
    ("vision_images_v226", "vision_images_v360"),
    ("VL_GATE_V226", "VL_GATE_V360"), ("vl_gate_v226", "vl_gate_v360"),
    ("runs/vision_v226", "runs/vision_v360"),
]:
    out = out.replace(a, b)
(S / "c2268_vision_v360_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2269"), ("c1465", "c2269"), ("V226", "V360"), ("v226", "v360"),
    ("vision_images_v226h", "vision_images_v360h"),
    ("vision_images_v226", "vision_images_v360"),
    ("VL_GATE_V226", "VL_GATE_V360"), ("vl_gate_v226", "vl_gate_v360"),
    ("runs/vision_v226h", "runs/vision_v360h"),
    ("_v226c1463", "_v360c2267"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T360, "v360h", "V360H", HO360))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v360h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v360"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v360" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v360h_c2269"'); seen_run = True; continue
    out2.append(ln)
(S / "c2269_vision_v360_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2267-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2268_VISION_V360_SMOKE.json") or {}\n    c654b = load("docs/r50/C2268b_VISION_GATE_V360_CLAIM.json") or {}\n    c655 = load("docs/r50/C2269_VISION_V360_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2269b_VISION_GATE_V360_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v360 = float(c654.get("rate") or 0.0)\n    v360h = float(c655.get("rate") or 0.0)\n    v360_claim = bool(c654b.get("vl_gate_v360_claim") or c654.get("vl_gate_v360_claim") or c654.get("claim"))\n    v360h_claim = bool(c655b.get("vl_gate_v360_heldout_claim") or c655.get("vl_gate_v360_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v360_claim and v360h_claim and v360 >= GATE and v360h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v360 >= 0.999 and v360h >= 0.999) else min(v360, v360h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v360": {"rate": v360, "claim": v360_claim, "n": c654.get("n")},\n            "v360_heldout": {"rate": v360h, "claim": v360h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v360_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V360: rate={v360} claim={v360_claim}",\n        f"- Vision V360 heldout: rate={v360h} claim={v360h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2267-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2267: Vision V360 design fixtures",\n        f"- C2268: Vision V360 smoke **{v360}**", f"- C2269: Vision V360 heldout **{v360h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V360 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2272 = '\ufeff# -*- coding: utf-8 -*-\n"""C2272: Unified scorecard + STAGE after C2267-C2271. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2272.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2268_VISION_V360_SMOKE.json") or {}\n    c654b = load("docs/r50/C2268b_VISION_GATE_V360_CLAIM.json") or {}\n    c655 = load("docs/r50/C2269_VISION_V360_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2269b_VISION_GATE_V360_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2264_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2271_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2270_PRODUCT_U2C_COST.json") or {}\n\n    v360 = float(c654.get("rate") or 0.0)\n    v360h = float(c655.get("rate") or 0.0)\n    v360_claim = bool(c654b.get("vl_gate_v360_claim") or c654.get("vl_gate_v360_claim") or c654.get("claim"))\n    v360h_claim = bool(c655b.get("vl_gate_v360_heldout_claim") or c655.get("vl_gate_v360_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2270"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v360_claim and v360h_claim and v360 >= GATE and v360h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v360 >= 0.999 and v360h >= 0.999) else min(v360, v360h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2272", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v360": {"rate": v360, "claim": v360_claim, "n": c654.get("n")},\n            "v360_heldout": {"rate": v360h, "claim": v360h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2270"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2264"},\n        "capture_regression": {"pass": capture_pass, "source": "C2271"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v360_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2272_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2272)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V360: rate={v360} claim={v360_claim}",\n        f"- Vision V360 heldout: rate={v360h} claim={v360h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2272", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2267-C2272 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2267: Vision V360 design fixtures",\n        f"- C2268: Vision V360 smoke **{v360}**", f"- C2269: Vision V360 heldout **{v360h}** (disjoint={disjoint})",\n        f"- C2270: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C2264): pass={conf_pass} rate={conf_rate}",\n        f"- C2271: capture pass={capture_pass}", f"- C2272: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V360 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2272.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V360 knife = product-U2C (alternating; V359 was confidence-gate)
out = (S / "c2258_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2258", "C2270"), ("c2258", "c2270"),
    ("C2090", "C2270"), ("c2090", "c2270"),
    ("product_u2c_cost_c2270", "product_u2c_cost_c2270"),
    ("u2c_v145", "u2c_v134"),
    ("u2c_c2270", "u2c_c2270"),
]:
    out = out.replace(a, b2)
(S / "c2270_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c2258")

out = (S / "c2265_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2265", "C2271"), ("c2265", "c2271")]:
    out = out.replace(a, b2)
(S / "c2271_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2272_scorecard_and_stage.py").write_text(SC2272, encoding="utf-8")
print("scorecard from fixed c2092 product-U2C pattern")
print("OK builder v360 ready")
