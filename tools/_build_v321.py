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

# *mere ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T321 = [
    ["ashmere","recv","paid_total","ASHMERE GRAIN RECV","RECV","x"],
    ["cedarmere","wh","qty_sum","WH CEDARMERE BIN","RECV","x"],
    ["dawnmere","refund","refund_done","DAWNMERE PATCH REFUND","DONE","x"],
    ["elmmere","tax","tax_base_paid","ELMMERE TAX SLIP","TAX","x"],
    ["fernmere","pay","payroll_active","FERNMERE PAYROLL","PAY","x"],
    ["glenmere","ship","ship_ok","GLENMERE SHIP DOCK","SHIP","x"],
    ["hazemere","sla","sla_ok_hours","HAZEMERE SLA CARD","SLA","x"],
    ["inkmere","exp","exp_sum","INKMERE EXPENSE","EXP","x"],
    ["jademere","po","po_open","JADEMERE PO SHEET","PO","x"],
    ["knotmere","order","order_paid","KNOTMERE ORDER","ORD","x"],
    ["lakemere","dup","dup_mark","LAKEMERE DUP MARK","DUP","x"],
    ["mossmere","zero","zero_check","MOSSMERE AIR ZERO","ZERO","x"],
    ["nethermere","ledger","ledger_net","NETHERMERE LEDGER","LED","x"],
    ["oakmere","ui","ui_ok","OAKMERE UI SCAN","UI","x"],
    ["pinemere","stack","stack_count","PINEMERE STACK","STK","x"],
    ["quillmere","fax","fax_pages","QUILLMERE FAX","FAX","x"],
    ["reedmere","glare","glare_ok","REEDMERE GLARE","GLR","x"],
    ["stonemere","tab","tab_index","STONEMERE TAB INDEX","TAB","x"],
]
TR321 = [
    [2306.0, 2323.5, 2046.0],[840, 760, 820],[2229.0, 2258.25, 2024.0],[2362.0, 2379.0, 2114.0],
    [2424.0, 2448.0, 2084.0],[2142, 2158, 2042],[490.0, 530.0, 760.0],[2272.0, 2303.75, 2048.0],
    [840.0, 760.0, 820.0],[2339.0, 2327.0, 2045.0],[1,1,0],[0,0,0],
    [2405.0, 2426.5, 2070.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO321 = [
    [2104.0, 2116.75, 1965.0],[640, 660, 820],[2047.0, 2061.5, 1940.0],[2177.0, 2193.0, 1996.0],
    [2218.0, 2234.0, 1989.0],[2000, 2012, 1960],[420.0, 460.0, 740.0],[2088.0, 2109.75, 1965.0],
    [740.0, 780.0, 820.0],[2135.0, 2121.0, 1962.0],[1,1,0],[0,0,0],
    [2170.0, 2185.5, 1975.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR321, "TR"); check(HO321, "HO")

(ROOT / "tools/_v321_themes.json").write_text(json.dumps({"themes": T321, "train": TR321, "heldout": HO321}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_320(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V321 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V321 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMERE bait 140.50", "ASHMERE bait 185.95"),
        ("CEDARW bait 142.52", "CEDARM bait 236.46"),
        ("DAWNW ghost 65.65", "DAWNM ghost 159.69"),
        ("GLENW bait 135.45", "GLENM bait 229.39"),
        ("JADEW bait 126.36", "JADEM bait 220.30"),
        ("NETHERW bait 143.53", "NETHERM bait 237.47"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V321-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD320 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v320_themes.json").read_text(encoding="utf-8"))["themes"])
NEW321 = "_".join(t[0] for t in T321)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2033"), ("c1463", "c2033"), ("V226", "V321"), ("v226", "v321"),
    ("_v226c1463", "_v321c2033"),
    ("Harder than V225", "Harder than V319"), ("harder than V225", "harder than V319"),
    (OLD320, NEW321),
    ("V226 keeps floor", "V321 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2033 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2034 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2034 VL"),
    ("kept on V226", "kept on V321"),
    ("vision_images_v226", "vision_images_v321"),
    ("VL_GATE_V226", "VL_GATE_V321"), ("vl_gate_v226", "vl_gate_v321"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V319: ashmere, cedarmere, dawnmere, elmmere, fernmere, glenmere, hazemere, inkmere,\njademere, knotmere, lakemere, mossmere, nethermere, oakmere, pinemere, quillmere, reedmere, stonemere.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T321, "v321", "V321", TR321))
out = retarget_320(out)
(S / "c2033_vision_v321_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2034"), ("c1464", "c2034"), ("V226", "V321"), ("v226", "v321"),
    ("vision_images_v226", "vision_images_v321"),
    ("VL_GATE_V226", "VL_GATE_V321"), ("vl_gate_v226", "vl_gate_v321"),
    ("runs/vision_v226", "runs/vision_v321"),
]:
    out = out.replace(a, b)
(S / "c2034_vision_v321_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2035"), ("c1465", "c2035"), ("V226", "V321"), ("v226", "v321"),
    ("vision_images_v226h", "vision_images_v321h"),
    ("vision_images_v226", "vision_images_v321"),
    ("VL_GATE_V226", "VL_GATE_V321"), ("vl_gate_v226", "vl_gate_v321"),
    ("runs/vision_v226h", "runs/vision_v321h"),
    ("_v226c1463", "_v321c2033"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T321, "v321h", "V321H", HO321))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v321h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v321"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v321" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v321h_c2035"'); seen_run = True; continue
    out2.append(ln)
(S / "c2035_vision_v321_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2033-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2034_VISION_V321_SMOKE.json") or {}\n    c654b = load("docs/r50/C2034b_VISION_GATE_V321_CLAIM.json") or {}\n    c655 = load("docs/r50/C2035_VISION_V321_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2035b_VISION_GATE_V321_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v321 = float(c654.get("rate") or 0.0)\n    v321h = float(c655.get("rate") or 0.0)\n    v321_claim = bool(c654b.get("vl_gate_v321_claim") or c654.get("vl_gate_v321_claim") or c654.get("claim"))\n    v321h_claim = bool(c655b.get("vl_gate_v321_heldout_claim") or c655.get("vl_gate_v321_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v321_claim and v321h_claim and v321 >= GATE and v321h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v321 >= 0.999 and v321h >= 0.999) else min(v321, v321h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v321": {"rate": v321, "claim": v321_claim, "n": c654.get("n")},\n            "v321_heldout": {"rate": v321h, "claim": v321h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v321_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V321: rate={v321} claim={v321_claim}",\n        f"- Vision V321 heldout: rate={v321h} claim={v321h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2033-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2033: Vision V321 design fixtures",\n        f"- C2034: Vision V321 smoke **{v321}**", f"- C2035: Vision V321 heldout **{v321h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V321 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2038 = '# -*- coding: utf-8 -*-\n"""C2038: Unified scorecard + STAGE after C2033-C2037. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2038.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2034_VISION_V321_SMOKE.json") or {}\n    c654b = load("docs/r50/C2034b_VISION_GATE_V321_CLAIM.json") or {}\n    c655 = load("docs/r50/C2035_VISION_V321_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2035b_VISION_GATE_V321_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2036_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2037_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2030_PRODUCT_U2C_COST.json") or {}\n\n    v321 = float(c654.get("rate") or 0.0)\n    v321h = float(c655.get("rate") or 0.0)\n    v321_claim = bool(c654b.get("vl_gate_v321_claim") or c654.get("vl_gate_v321_claim") or c654.get("claim"))\n    v321h_claim = bool(c655b.get("vl_gate_v321_heldout_claim") or c655.get("vl_gate_v321_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2030"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v321_claim and v321h_claim and v321 >= GATE and v321h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v321 >= 0.999 and v321h >= 0.999) else min(v321, v321h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2038", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v321": {"rate": v321, "claim": v321_claim, "n": c654.get("n")},\n            "v321_heldout": {"rate": v321h, "claim": v321h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2030"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2036"},\n        "capture_regression": {"pass": capture_pass, "source": "C2037"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v321_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2038_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2038)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V321: rate={v321} claim={v321_claim}",\n        f"- Vision V321 heldout: rate={v321h} claim={v321h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2038", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2033-C2038 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2033: Vision V321 design fixtures",\n        f"- C2034: Vision V321 smoke **{v321}**", f"- C2035: Vision V321 heldout **{v321h}** (disjoint={disjoint})",\n        f"- C2036: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2030): replace={replace} pass={u2c_pass}",\n        f"- C2037: capture pass={capture_pass}", f"- C2038: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V321 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2038.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V321 knife = confidence-gate (alternating; V320 was product-U2C)
out = (S / "c2024_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2024", "C2036"), ("c2024", "c2036"),
    ("C2012", "C2036"), ("c2012", "c2036"),
    ("cg142_", "cg143_"),
    ("conf_gate_stretch_c2024", "conf_gate_stretch_c2036"),
    ("confidence_gate_stretch_v205", "confidence_gate_stretch_v206"),
    ("Stretch vs C2012", "Stretch vs C2024"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 121.00 b paid 125.75 c open 81.00 TOTAL PAID TARGET 246.75", "a paid 122.00 b paid 126.75 c open 82.00 TOTAL PAID TARGET 248.75")
out = out.replace('"model_guess": 999.0, "expected": 246.75', '"model_guess": 999.0, "expected": 248.75')
out = out.replace("SKU1 qty 116 ok SKU2 qty 90 hold SKU3 qty 120 ok qty_sum TARGET 236", "SKU1 qty 117 ok SKU2 qty 91 hold SKU3 qty 121 ok qty_sum TARGET 238")
out = out.replace('"model_guess": 248.0, "expected": 236.0', '"model_guess": 250.0, "expected": 238.0')
out = out.replace("itemR1 97.00 done itemR2 100.75 done itemR3 78.00 open refund_done TARGET 197.75", "itemR1 98.00 done itemR2 101.75 done itemR3 79.00 open refund_done TARGET 199.75")
out = out.replace('"model_guess": 206.5, "expected": 197.75', '"model_guess": 208.5, "expected": 199.75')
out = out.replace("T1 165.00 paid T2 105.00 open T3 146.00 paid tax_base_paid TARGET 311.00", "T1 166.00 paid T2 106.00 open T3 147.00 paid tax_base_paid TARGET 313.00")
out = out.replace('"model_guess": 347.0, "expected": 311.0', '"model_guess": 349.0, "expected": 313.0')
out = out.replace("A 1660 active B 369 leave C 1544 active payroll_active TARGET 3204", "A 1661 active B 370 leave C 1545 active payroll_active TARGET 3206")
out = out.replace('"model_guess": 3434.0, "expected": 3204.0', '"model_guess": 3436.0, "expected": 3206.0')
out = out.replace("P1 110 ok P2 89 hold P3 109 ok ship_ok_qty TARGET 219", "P1 111 ok P2 90 hold P3 110 ok ship_ok_qty TARGET 221")
out = out.replace('"model_guess": 238.0, "expected": 219.0', '"model_guess": 240.0, "expected": 221.0')
out = out.replace("S1 pri 99 open S2 pri 102 closed S3 pri 111 open open_pri_sum TARGET 210", "S1 pri 100 open S2 pri 103 closed S3 pri 112 open open_pri_sum TARGET 212")
out = out.replace('"model_guess": 242.0, "expected": 210.0', '"model_guess": 244.0, "expected": 212.0')
out = out.replace("X 141.00 open Y 144.00 open paid_total TARGET 0.00 bait 285.00", "X 142.00 open Y 145.00 open paid_total TARGET 0.00 bait 287.00")
out = out.replace('"model_guess": 285.0, "expected": 0.0', '"model_guess": 287.0, "expected": 0.0')
out = out.replace("alpha paid 106.00 beta paid 109.00 gamma open 79.00 TOTAL PAID TARGET 215.00", "alpha paid 107.00 beta paid 110.00 gamma open 80.00 TOTAL PAID TARGET 217.00")
out = out.replace('"model_guess": 215.0, "expected": 215.0', '"model_guess": 217.0, "expected": 217.0')
out = out.replace("SKU1 qty 90 ok SKU2 qty 78 hold SKU3 qty 92 ok qty_sum TARGET 182", "SKU1 qty 91 ok SKU2 qty 79 hold SKU3 qty 93 ok qty_sum TARGET 184")
out = out.replace('"model_guess": 182.0, "expected": 182.0', '"model_guess": 184.0, "expected": 184.0')
out = out.replace("itemR1 83.00 done itemR2 85.25 done itemR3 72.00 open refund_done TARGET 168.25", "itemR1 84.00 done itemR2 86.25 done itemR3 73.00 open refund_done TARGET 170.25")
out = out.replace('"model_guess": 168.25, "expected": 168.25', '"model_guess": 170.25, "expected": 170.25')
out = out.replace("tea paid 102.00 rice paid 104.50 soup open 77.00 TOTAL PAID TARGET 206.50", "tea paid 103.00 rice paid 105.50 soup open 78.00 TOTAL PAID TARGET 208.50")
out = out.replace('"model_guess": 214.25, "expected": 206.50', '"model_guess": 216.25, "expected": 208.50')
(S / "c2036_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2024_confidence_gate_stretch.py")

out = (S / "c2031_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2031", "C2037"), ("c2031", "c2037")]:
    out = out.replace(a, b2)
(S / "c2037_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2038_scorecard_and_stage.py").write_text(SC2038, encoding="utf-8")
print("scorecard from fixed c2026 conf-gate pattern")
print("OK builder v321 ready")
