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

# *moor ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T337 = [
    ["ashmoor","recv","paid_total","ASHMOOR GRAIN RECV","RECV","x"],
    ["cedarmoor","wh","qty_sum","WH CEDARMOOR BIN","RECV","x"],
    ["dawnmoor","refund","refund_done","DAWNMOOR PATCH REFUND","DONE","x"],
    ["elmmoor","tax","tax_base_paid","ELMMOOR TAX SLIP","TAX","x"],
    ["fernmoor","pay","payroll_active","FERNMOOR PAYROLL","PAY","x"],
    ["glenmoor","ship","ship_ok","GLENMOOR SHIP DOCK","SHIP","x"],
    ["hazemoor","sla","sla_ok_hours","HAZEMOOR SLA CARD","SLA","x"],
    ["inkmoor","exp","exp_sum","INKMOOR EXPENSE","EXP","x"],
    ["jademoor","po","po_open","JADEMOOR PO SHEET","PO","x"],
    ["knotmoor","order","order_paid","KNOTMOOR ORDER","ORD","x"],
    ["lakemoor","dup","dup_mark","LAKEMOOR DUP MARK","DUP","x"],
    ["mossmoor","zero","zero_check","MOSSMOOR AIR ZERO","ZERO","x"],
    ["nethermoor","ledger","ledger_net","NETHERMOOR LEDGER","LED","x"],
    ["oakmoor","ui","ui_ok","OAKMOOR UI SCAN","UI","x"],
    ["pinemoor","stack","stack_count","PINEMOOR STACK","STK","x"],
    ["quillmoor","fax","fax_pages","QUILLMOOR FAX","FAX","x"],
    ["reedmoor","glare","glare_ok","REEDMOOR GLARE","GLR","x"],
    ["stonemoor","tab","tab_index","STONEMOOR TAB INDEX","TAB","x"],
]
TR337 = [
    [2338.0, 2355.5, 2078.0],[840, 760, 820],[2250.0, 2256.25, 2050.0],[2394.0, 2411.0, 2146.0],
    [2456.0, 2480.0, 2116.0],[2174, 2190, 2074],[490.0, 530.0, 760.0],[2304.0, 2335.75, 2080.0],
    [840.0, 760.0, 820.0],[2371.0, 2359.0, 2077.0],[1,1,0],[0,0,0],
    [2437.0, 2458.5, 2102.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO337 = [
    [2136.0, 2148.75, 1997.0],[640, 660, 820],[2079.0, 2093.5, 1972.0],[2209.0, 2225.0, 2028.0],
    [2241.0, 2252.0, 2021.0],[2032, 2044, 1994],[420.0, 460.0, 740.0],[2120.0, 2141.75, 1997.0],
    [740.0, 780.0, 820.0],[2167.0, 2153.0, 1994.0],[1,1,0],[0,0,0],
    [2202.0, 2217.5, 2007.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR337, "TR"); check(HO337, "HO")

(ROOT / "tools/_v337_themes.json").write_text(json.dumps({"themes": T337, "train": TR337, "heldout": HO337}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_336(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V337 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V337 overlays (new vs V49) ---")
    for a, b in [
        ("ASHMOOR bait 140.50", "ASHMOOR bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 250.60"),
        ("DAWNW ghost 65.65", "DAWNH ghost 173.83"),
        ("GLENW bait 135.45", "GLENH bait 243.53"),
        ("JADEW bait 126.36", "JADEH bait 234.44"),
        ("NETHERW bait 143.53", "NETHERH bait 251.61"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V337-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD336 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v336_themes.json").read_text(encoding="utf-8"))["themes"])
NEW337 = "_".join(t[0] for t in T337)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C2129"), ("c1463", "c2129"), ("V226", "V337"), ("v226", "v337"),
    ("_v226c1463", "_v337c2129"),
    ("Harder than V225", "Harder than V335"), ("harder than V225", "harder than V335"),
    (OLD336, NEW337),
    ("V226 keeps floor", "V337 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C2129 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C2130 VL smoke"),
    ("No claim until C1464 VL", "No claim until C2130 VL"),
    ("kept on V226", "kept on V337"),
    ("vision_images_v226", "vision_images_v337"),
    ("VL_GATE_V226", "VL_GATE_V337"), ("vl_gate_v226", "vl_gate_v337"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V335: ashmoor, cedarmoor, dawnmoor, elmmoor, fernmoor, glenmoor, hazemoor, inkmoor,\njademoor, knotmoor, lakemoor, mossmoor, nethermoor, oakmoor, pinemoor, quillmoor, reedmoor, stonemoor.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T337, "v337", "V337", TR337))
out = retarget_336(out)
(S / "c2129_vision_v337_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C2130"), ("c1464", "c2130"), ("V226", "V337"), ("v226", "v337"),
    ("vision_images_v226", "vision_images_v337"),
    ("VL_GATE_V226", "VL_GATE_V337"), ("vl_gate_v226", "vl_gate_v337"),
    ("runs/vision_v226", "runs/vision_v337"),
]:
    out = out.replace(a, b)
(S / "c2130_vision_v337_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C2131"), ("c1465", "c2131"), ("V226", "V337"), ("v226", "v337"),
    ("vision_images_v226h", "vision_images_v337h"),
    ("vision_images_v226", "vision_images_v337"),
    ("VL_GATE_V226", "VL_GATE_V337"), ("vl_gate_v226", "vl_gate_v337"),
    ("runs/vision_v226h", "runs/vision_v337h"),
    ("_v226c1463", "_v337c2129"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T337, "v337h", "V337H", HO337))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v337h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v337"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v337" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v337h_c2131"'); seen_run = True; continue
    out2.append(ln)
(S / "c2131_vision_v337_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C2129-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2130_VISION_V337_SMOKE.json") or {}\n    c654b = load("docs/r50/C2130b_VISION_GATE_V337_CLAIM.json") or {}\n    c655 = load("docs/r50/C2131_VISION_V337_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2131b_VISION_GATE_V337_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v337 = float(c654.get("rate") or 0.0)\n    v337h = float(c655.get("rate") or 0.0)\n    v337_claim = bool(c654b.get("vl_gate_v337_claim") or c654.get("vl_gate_v337_claim") or c654.get("claim"))\n    v337h_claim = bool(c655b.get("vl_gate_v337_heldout_claim") or c655.get("vl_gate_v337_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v337_claim and v337h_claim and v337 >= GATE and v337h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v337 >= 0.999 and v337h >= 0.999) else min(v337, v337h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v337": {"rate": v337, "claim": v337_claim, "n": c654.get("n")},\n            "v337_heldout": {"rate": v337h, "claim": v337h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v337_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V337: rate={v337} claim={v337_claim}",\n        f"- Vision V337 heldout: rate={v337h} claim={v337h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2129-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2129: Vision V337 design fixtures",\n        f"- C2130: Vision V337 smoke **{v337}**", f"- C2131: Vision V337 heldout **{v337h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V337 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC2134 = '# -*- coding: utf-8 -*-\n"""C2134: Unified scorecard + STAGE after C2129-C2133. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C2134.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C2130_VISION_V337_SMOKE.json") or {}\n    c654b = load("docs/r50/C2130b_VISION_GATE_V337_CLAIM.json") or {}\n    c655 = load("docs/r50/C2131_VISION_V337_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C2131b_VISION_GATE_V337_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C2132_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C2133_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C2126_PRODUCT_U2C_COST.json") or {}\n\n    v337 = float(c654.get("rate") or 0.0)\n    v337h = float(c655.get("rate") or 0.0)\n    v337_claim = bool(c654b.get("vl_gate_v337_claim") or c654.get("vl_gate_v337_claim") or c654.get("claim"))\n    v337h_claim = bool(c655b.get("vl_gate_v337_heldout_claim") or c655.get("vl_gate_v337_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C2126"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v337_claim and v337h_claim and v337 >= GATE and v337h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v337 >= 0.999 and v337h >= 0.999) else min(v337, v337h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C2134", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v337": {"rate": v337, "claim": v337_claim, "n": c654.get("n")},\n            "v337_heldout": {"rate": v337h, "claim": v337h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C2126"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C2132"},\n        "capture_regression": {"pass": capture_pass, "source": "C2133"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v337_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C2134_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C2134)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V337: rate={v337} claim={v337_claim}",\n        f"- Vision V337 heldout: rate={v337h} claim={v337h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C2134", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C2129-C2134 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C2129: Vision V337 design fixtures",\n        f"- C2130: Vision V337 smoke **{v337}**", f"- C2131: Vision V337 heldout **{v337h}** (disjoint={disjoint})",\n        f"- C2132: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C2126): replace={replace} pass={u2c_pass}",\n        f"- C2133: capture pass={capture_pass}", f"- C2134: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V337 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C2134.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V337 knife = confidence-gate (alternating; V336 was product-U2C)
out = (S / "c2120_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C2120", "C2132"), ("c2120", "c2132"),
    ("C2096", "C2132"), ("c2096", "c2132"),
    ("cg151_", "cg150_"),
    ("conf_gate_stretch_c2132", "conf_gate_stretch_c2132"),
    ("confidence_gate_stretch_v214", "confidence_gate_stretch_v213"),
    ("Stretch vs C2120", "Stretch vs C2108"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 128.00 b paid 132.75 c open 88.00 TOTAL PAID TARGET 260.75", "a paid 130.00 b paid 134.75 c open 90.00 TOTAL PAID TARGET 264.75")
out = out.replace('"model_guess": 999.0, "expected": 260.75', '"model_guess": 999.0, "expected": 264.75')
out = out.replace("SKU1 qty 123 ok SKU2 qty 97 hold SKU3 qty 127 ok qty_sum TARGET 250", "SKU1 qty 125 ok SKU2 qty 99 hold SKU3 qty 129 ok qty_sum TARGET 254")
out = out.replace('"model_guess": 262.0, "expected": 250.0', '"model_guess": 266.0, "expected": 254.0')
out = out.replace("itemR1 104.00 done itemR2 107.75 done itemR3 85.00 open refund_done TARGET 211.75", "itemR1 106.00 done itemR2 109.75 done itemR3 87.00 open refund_done TARGET 215.75")
out = out.replace('"model_guess": 220.5, "expected": 211.75', '"model_guess": 224.5, "expected": 215.75')
out = out.replace("T1 172.00 paid T2 112.00 open T3 153.00 paid tax_base_paid TARGET 325.00", "T1 174.00 paid T2 114.00 open T3 155.00 paid tax_base_paid TARGET 329.00")
out = out.replace('"model_guess": 361.0, "expected": 325.0', '"model_guess": 365.0, "expected": 329.0')
out = out.replace("A 1667 active B 376 leave C 1551 active payroll_active TARGET 3218", "A 1669 active B 378 leave C 1553 active payroll_active TARGET 3222")
out = out.replace('"model_guess": 3448.0, "expected": 3218.0', '"model_guess": 3452.0, "expected": 3222.0')
out = out.replace("P1 117 ok P2 96 hold P3 116 ok ship_ok_qty TARGET 233", "P1 119 ok P2 98 hold P3 118 ok ship_ok_qty TARGET 237")
out = out.replace('"model_guess": 252.0, "expected": 233.0', '"model_guess": 256.0, "expected": 237.0')
out = out.replace("S1 pri 106 open S2 pri 109 closed S3 pri 118 open open_pri_sum TARGET 224", "S1 pri 108 open S2 pri 111 closed S3 pri 120 open open_pri_sum TARGET 228")
out = out.replace('"model_guess": 256.0, "expected": 224.0', '"model_guess": 260.0, "expected": 228.0')
out = out.replace("X 148.00 open Y 151.00 open paid_total TARGET 0.00 bait 299.00", "X 150.00 open Y 153.00 open paid_total TARGET 0.00 bait 303.00")
out = out.replace('"model_guess": 299.0, "expected": 0.0', '"model_guess": 303.0, "expected": 0.0')
out = out.replace("alpha paid 113.00 beta paid 116.00 gamma open 86.00 TOTAL PAID TARGET 229.00", "alpha paid 115.00 beta paid 118.00 gamma open 88.00 TOTAL PAID TARGET 233.00")
out = out.replace('"model_guess": 229.0, "expected": 229.0', '"model_guess": 233.0, "expected": 233.0')
out = out.replace("SKU1 qty 97 ok SKU2 qty 85 hold SKU3 qty 99 ok qty_sum TARGET 196", "SKU1 qty 99 ok SKU2 qty 87 hold SKU3 qty 101 ok qty_sum TARGET 200")
out = out.replace('"model_guess": 196.0, "expected": 196.0', '"model_guess": 200.0, "expected": 200.0')
out = out.replace("itemR1 90.00 done itemR2 92.25 done itemR3 79.00 open refund_done TARGET 182.25", "itemR1 92.00 done itemR2 94.25 done itemR3 81.00 open refund_done TARGET 186.25")
out = out.replace('"model_guess": 182.25, "expected": 182.25', '"model_guess": 186.25, "expected": 186.25')
out = out.replace("tea paid 109.00 rice paid 111.50 soup open 84.00 TOTAL PAID TARGET 220.50", "tea paid 111.00 rice paid 113.50 soup open 86.00 TOTAL PAID TARGET 224.50")
out = out.replace('"model_guess": 228.25, "expected": 220.50', '"model_guess": 232.25, "expected": 224.50')
(S / "c2132_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c2120_confidence_gate_stretch.py")

out = (S / "c2127_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C2127", "C2133"), ("c2127", "c2133")]:
    out = out.replace(a, b2)
(S / "c2133_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c2134_scorecard_and_stage.py").write_text(SC2134, encoding="utf-8")
print("scorecard from fixed c2098 conf-gate pattern")
print("OK builder v337 ready")
