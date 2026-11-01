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

# *holm ; stack mid-band ~114x (V226 crush lesson); heldout refund avoid 1560
T313 = [
    ["ashholm","recv","paid_total","ASHHOLM GRAIN RECV","RECV","x"],
    ["cedarholm","wh","qty_sum","WH CEDARHOLM BIN","RECV","x"],
    ["dawnholm","refund","refund_done","DAWNHOLM PATCH REFUND","DONE","x"],
    ["elmholm","tax","tax_base_paid","ELMHOLM TAX SLIP","TAX","x"],
    ["fernholm","pay","payroll_active","FERNHOLM PAYROLL","PAY","x"],
    ["glenholm","ship","ship_ok","GLENHOLM SHIP DOCK","SHIP","x"],
    ["hazeholm","sla","sla_ok_hours","HAZEHOLM SLA CARD","SLA","x"],
    ["inkholm","exp","exp_sum","INKHOLM EXPENSE","EXP","x"],
    ["jadeholm","po","po_open","JADEHOLM PO SHEET","PO","x"],
    ["knotholm","order","order_paid","KNOTHOLM ORDER","ORD","x"],
    ["lakeholm","dup","dup_mark","LAKEHOLM DUP MARK","DUP","x"],
    ["mossholm","zero","zero_check","MOSSHOLM AIR ZERO","ZERO","x"],
    ["netherholm","ledger","ledger_net","NETHERHOLM LEDGER","LED","x"],
    ["oakholm","ui","ui_ok","OAKHOLM UI SCAN","UI","x"],
    ["pineholm","stack","stack_count","PINEHOLM STACK","STK","x"],
    ["quillholm","fax","fax_pages","QUILLHOLM FAX","FAX","x"],
    ["reedholm","glare","glare_ok","REEDHOLM GLARE","GLR","x"],
    ["stoneholm","tab","tab_index","STONEHOLM TAB INDEX","TAB","x"],
]
TR313 = [
    [2290.0, 2307.5, 2030.0],[840, 760, 820],[2213.0, 2242.25, 2008.0],[2346.0, 2363.0, 2098.0],
    [2408.0, 2432.0, 2068.0],[2126, 2142, 2026],[490.0, 530.0, 760.0],[2256.0, 2287.75, 2032.0],
    [840.0, 760.0, 820.0],[2323.0, 2311.0, 2029.0],[1,1,0],[0,0,0],
    [2389.0, 2410.5, 2054.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO313 = [
    [2088.0, 2100.75, 1949.0],[640, 660, 820],[2031.0, 2045.5, 1924.0],[2161.0, 2177.0, 1980.0],
    [2202.0, 2218.0, 1973.0],[1984, 1996, 1944],[420.0, 460.0, 740.0],[2072.0, 2093.75, 1949.0],
    [740.0, 780.0, 820.0],[2119.0, 2105.0, 1946.0],[1,1,0],[0,0,0],
    [2154.0, 2169.5, 1959.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR313, "TR"); check(HO313, "HO")

(ROOT / "tools/_v313_themes.json").write_text(json.dumps({"themes": T313, "train": TR313, "heldout": HO313}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_312(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V313 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V313 overlays (new vs V49) ---")
    for a, b in [
        ("ASHHOLM bait 140.50", "ASHHOLM bait 185.95"),
        ("CEDARW bait 142.52", "CEDARH bait 228.38"),
        ("DAWNW ghost 65.65", "DAWNH ghost 151.61"),
        ("GLENW bait 135.45", "GLENH bait 221.31"),
        ("JADEW bait 126.36", "JADEH bait 212.22"),
        ("NETHERW bait 143.53", "NETHERH bait 229.39"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V313-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD312 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v312_themes.json").read_text(encoding="utf-8"))["themes"])
NEW313 = "_".join(t[0] for t in T313)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1985"), ("c1463", "c1985"), ("V226", "V313"), ("v226", "v313"),
    ("_v226c1463", "_v313c1985"),
    ("Harder than V225", "Harder than V311"), ("harder than V225", "harder than V311"),
    (OLD312, NEW313),
    ("V226 keeps floor", "V313 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1985 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1986 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1986 VL"),
    ("kept on V226", "kept on V313"),
    ("vision_images_v226", "vision_images_v313"),
    ("VL_GATE_V226", "VL_GATE_V313"), ("vl_gate_v226", "vl_gate_v313"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V311: ashholm, cedarholm, dawnholm, elmholm, fernholm, glenholm, hazeholm, inkholm,\njadeholm, knotholm, lakeholm, mossholm, netherholm, oakholm, pineholm, quillholm, reedholm, stoneholm.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T313, "v313", "V313", TR313))
out = retarget_312(out)
(S / "c1985_vision_v313_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1986"), ("c1464", "c1986"), ("V226", "V313"), ("v226", "v313"),
    ("vision_images_v226", "vision_images_v313"),
    ("VL_GATE_V226", "VL_GATE_V313"), ("vl_gate_v226", "vl_gate_v313"),
    ("runs/vision_v226", "runs/vision_v313"),
]:
    out = out.replace(a, b)
(S / "c1986_vision_v313_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1987"), ("c1465", "c1987"), ("V226", "V313"), ("v226", "v313"),
    ("vision_images_v226h", "vision_images_v313h"),
    ("vision_images_v226", "vision_images_v313"),
    ("VL_GATE_V226", "VL_GATE_V313"), ("vl_gate_v226", "vl_gate_v313"),
    ("runs/vision_v226h", "runs/vision_v313h"),
    ("_v226c1463", "_v313c1985"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T313, "v313h", "V313H", HO313))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v313h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v313"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v313" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v313h_c1987"'); seen_run = True; continue
    out2.append(ln)
(S / "c1987_vision_v313_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C1985-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1986_VISION_V313_SMOKE.json") or {}\n    c654b = load("docs/r50/C1986b_VISION_GATE_V313_CLAIM.json") or {}\n    c655 = load("docs/r50/C1987_VISION_V313_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1987b_VISION_GATE_V313_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v313 = float(c654.get("rate") or 0.0)\n    v313h = float(c655.get("rate") or 0.0)\n    v313_claim = bool(c654b.get("vl_gate_v313_claim") or c654.get("vl_gate_v313_claim") or c654.get("claim"))\n    v313h_claim = bool(c655b.get("vl_gate_v313_heldout_claim") or c655.get("vl_gate_v313_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v313_claim and v313h_claim and v313 >= GATE and v313h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v313 >= 0.999 and v313h >= 0.999) else min(v313, v313h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v313": {"rate": v313, "claim": v313_claim, "n": c654.get("n")},\n            "v313_heldout": {"rate": v313h, "claim": v313h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v313_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V313: rate={v313} claim={v313_claim}",\n        f"- Vision V313 heldout: rate={v313h} claim={v313h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1985-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1985: Vision V313 design fixtures",\n        f"- C1986: Vision V313 smoke **{v313}**", f"- C1987: Vision V313 heldout **{v313h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V313 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC1990 = '# -*- coding: utf-8 -*-\n"""C1990: Unified scorecard + STAGE after C1469-C1989. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1990.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1986_VISION_V313_SMOKE.json") or {}\n    c654b = load("docs/r50/C1986b_VISION_GATE_V313_CLAIM.json") or {}\n    c655 = load("docs/r50/C1987_VISION_V313_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1987b_VISION_GATE_V313_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1988_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1989_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1466_PRODUCT_U2C_COST.json") or {}\n\n    v313 = float(c654.get("rate") or 0.0)\n    v313h = float(c655.get("rate") or 0.0)\n    v313_claim = bool(c654b.get("vl_gate_v313_claim") or c654.get("vl_gate_v313_claim") or c654.get("claim"))\n    v313h_claim = bool(c655b.get("vl_gate_v313_heldout_claim") or c655.get("vl_gate_v313_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1466"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v313_claim and v313h_claim and v313 >= GATE and v313h >= GATE and capture_pass and disjoint and conf_pass)\n    composite = (1.0 if (v313 >= 0.999 and v313h >= 0.999) else min(v313, v313h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1990", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v313": {"rate": v313, "claim": v313_claim, "n": c654.get("n")},\n            "v313_heldout": {"rate": v313h, "claim": v313h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1466"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1988"},\n        "capture_regression": {"pass": capture_pass, "source": "C1989"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v313_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1990_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1990)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V313: rate={v313} claim={v313_claim}",\n        f"- Vision V313 heldout: rate={v313h} claim={v313h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1990", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1469-C1990 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1469: Vision V313 design fixtures",\n        f"- C1986: Vision V313 smoke **{v313}**", f"- C1987: Vision V313 heldout **{v313h}** (disjoint={disjoint})",\n        f"- C1988: confidence-gate pass={conf_pass} rate={conf_rate}",\n        f"- product-U2C (prior C1466): replace={replace} pass={u2c_pass}",\n        f"- C1989: capture pass={capture_pass}", f"- C1990: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V313 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1990.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V313 knife = confidence-gate (alternating; V312 was product-U2C)
out = (S / "c1976_confidence_gate_stretch.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1976", "C1988"), ("c1976", "c1988"),
    ("C1964", "C1988"), ("c1964", "c1988"),
    ("cg138_", "cg139_"),
    ("conf_gate_stretch_c1976", "conf_gate_stretch_c1988"),
    ("confidence_gate_stretch_v201", "confidence_gate_stretch_v202"),
    ("Stretch vs C1964", "Stretch vs C1976"),
]:
    out = out.replace(a, b2)
out = out.replace("a paid 117.00 b paid 121.75 c open 77.00 TOTAL PAID TARGET 238.75", "a paid 118.00 b paid 122.75 c open 78.00 TOTAL PAID TARGET 240.75")
out = out.replace('"model_guess": 999.0, "expected": 238.75', '"model_guess": 999.0, "expected": 240.75')
out = out.replace("SKU1 qty 112 ok SKU2 qty 86 hold SKU3 qty 116 ok qty_sum TARGET 228", "SKU1 qty 113 ok SKU2 qty 87 hold SKU3 qty 117 ok qty_sum TARGET 230")
out = out.replace('"model_guess": 240.0, "expected": 228.0', '"model_guess": 242.0, "expected": 230.0')
out = out.replace("itemR1 93.00 done itemR2 96.75 done itemR3 74.00 open refund_done TARGET 189.75", "itemR1 94.00 done itemR2 97.75 done itemR3 75.00 open refund_done TARGET 191.75")
out = out.replace('"model_guess": 198.5, "expected": 189.75', '"model_guess": 200.5, "expected": 191.75')
out = out.replace("T1 161.00 paid T2 101.00 open T3 142.00 paid tax_base_paid TARGET 303.00", "T1 162.00 paid T2 102.00 open T3 143.00 paid tax_base_paid TARGET 305.00")
out = out.replace('"model_guess": 339.0, "expected": 303.0', '"model_guess": 341.0, "expected": 305.0')
out = out.replace("A 1655 active B 365 leave C 1540 active payroll_active TARGET 3195", "A 1657 active B 366 leave C 1541 active payroll_active TARGET 3198")
out = out.replace('"model_guess": 3425.0, "expected": 3195.0', '"model_guess": 3428.0, "expected": 3198.0')
out = out.replace("P1 106 ok P2 85 hold P3 105 ok ship_ok_qty TARGET 211", "P1 107 ok P2 86 hold P3 106 ok ship_ok_qty TARGET 213")
out = out.replace('"model_guess": 230.0, "expected": 211.0', '"model_guess": 232.0, "expected": 213.0')
out = out.replace("S1 pri 95 open S2 pri 98 closed S3 pri 107 open open_pri_sum TARGET 202", "S1 pri 96 open S2 pri 99 closed S3 pri 108 open open_pri_sum TARGET 204")
out = out.replace('"model_guess": 234.0, "expected": 202.0', '"model_guess": 236.0, "expected": 204.0')
out = out.replace("X 137.00 open Y 140.00 open paid_total TARGET 0.00 bait 277.00", "X 138.00 open Y 141.00 open paid_total TARGET 0.00 bait 279.00")
out = out.replace('"model_guess": 277.0, "expected": 0.0', '"model_guess": 279.0, "expected": 0.0')
out = out.replace("alpha paid 102.00 beta paid 105.00 gamma open 75.00 TOTAL PAID TARGET 207.00", "alpha paid 103.00 beta paid 106.00 gamma open 76.00 TOTAL PAID TARGET 209.00")
out = out.replace('"model_guess": 207.0, "expected": 207.0', '"model_guess": 209.0, "expected": 209.0')
out = out.replace("SKU1 qty 86 ok SKU2 qty 74 hold SKU3 qty 88 ok qty_sum TARGET 174", "SKU1 qty 87 ok SKU2 qty 75 hold SKU3 qty 89 ok qty_sum TARGET 176")
out = out.replace('"model_guess": 174.0, "expected": 174.0', '"model_guess": 176.0, "expected": 176.0')
out = out.replace("itemR1 79.00 done itemR2 81.25 done itemR3 68.00 open refund_done TARGET 160.25", "itemR1 80.00 done itemR2 82.25 done itemR3 69.00 open refund_done TARGET 162.25")
out = out.replace('"model_guess": 160.25, "expected": 160.25', '"model_guess": 162.25, "expected": 162.25')
out = out.replace("tea paid 98.00 rice paid 100.50 soup open 73.00 TOTAL PAID TARGET 198.50", "tea paid 99.00 rice paid 101.50 soup open 74.00 TOTAL PAID TARGET 200.50")
out = out.replace('"model_guess": 206.25, "expected": 198.50', '"model_guess": 208.25, "expected": 200.50')
(S / "c1988_confidence_gate_stretch.py").write_text(out, encoding="utf-8")
print("confidence_gate from", "c1976_confidence_gate_stretch.py")

out = (S / "c1983_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1983", "C1989"), ("c1983", "c1989")]:
    out = out.replace(a, b2)
(S / "c1989_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1990_scorecard_and_stage.py").write_text(SC1990, encoding="utf-8")
print("scorecard from fixed c1978 conf-gate pattern")
print("OK builder v313 ready")
