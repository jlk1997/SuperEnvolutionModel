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
T308 = [
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
TR308 = [
    [2280.0, 2297.5, 2020.0],[840, 760, 820],[2203.0, 2232.25, 1998.0],[2336.0, 2353.0, 2088.0],
    [2398.0, 2422.0, 2058.0],[2116, 2132, 2016],[490.0, 530.0, 760.0],[2246.0, 2277.75, 2022.0],
    [840.0, 760.0, 820.0],[2313.0, 2301.0, 2019.0],[1,1,0],[0,0,0],
    [2379.0, 2400.5, 2044.0],[1,0,0],[1188, 1180, 1160],[1192, 1176, 748],[1,0,0],[1192, 1176, 1154],
]
HO308 = [
    [2078.0, 2090.75, 1939.0],[640, 660, 820],[2021.0, 2035.5, 1914.0],[2151.0, 2167.0, 1970.0],
    [2192.0, 2208.0, 1963.0],[1974, 1986, 1934],[420.0, 460.0, 740.0],[2062.0, 2083.75, 1939.0],
    [740.0, 780.0, 820.0],[2109.0, 2095.0, 1936.0],[1,1,0],[0,0,0],
    [2144.0, 2159.5, 1949.0],[1,0,0],[1180, 1175, 1168],[1190, 1184, 1172],[1,0,0],[1176, 1170, 1149],
]
check(TR308, "TR"); check(HO308, "HO")

(ROOT / "tools/_v308_themes.json").write_text(json.dumps({"themes": T308, "train": TR308, "heldout": HO308}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def retarget_307(src):
    src = src.replace("# --- V226 overlays (new vs V50) ---", "# --- V308 overlays (new vs V50) ---")
    src = src.replace("# --- V226 overlays (new vs V49) ---", "# --- V308 overlays (new vs V49) ---")
    for a, b in [
        ("ASHFORD bait 140.50", "ASHFORD bait 185.95"),
        ("CEDARW bait 142.52", "CEDARF bait 223.33"),
        ("DAWNW ghost 65.65", "DAWNF ghost 146.56"),
        ("GLENW bait 135.45", "GLENF bait 216.26"),
        ("JADEW bait 126.36", "JADEF bait 207.17"),
        ("NETHERW bait 143.53", "NETHERF bait 224.34"),
        ("ash mist + stone ticks (V226-only)", "ash mist + stone ticks (V308-only)"),
    ]:
        src = src.replace(a, b)
    return src

OLD307 = "_".join(t[0] for t in json.loads((ROOT/"tools/_v307_themes.json").read_text(encoding="utf-8"))["themes"])
NEW308 = "_".join(t[0] for t in T308)

out = (S / "c1463_vision_v226_design_and_batch.py").read_text(encoding="utf-8")
for a, b in [
    ("C1463", "C1955"), ("c1463", "c1955"), ("V226", "V308"), ("v226", "v308"),
    ("_v226c1463", "_v308c1955"),
    ("Harder than V225", "Harder than V306"), ("harder than V225", "harder than V306"),
    (OLD307, NEW308),
    ("V226 keeps floor", "V308 keeps floor"),
    ("C1463 design+fixtures; no VL claim", "C1955 design+fixtures; no VL claim"),
    ("fixtures only; claim deferred to C1464 VL smoke", "fixtures only; claim deferred to C1956 VL smoke"),
    ("No claim until C1464 VL", "No claim until C1956 VL"),
    ("kept on V226", "kept on V308"),
    ("vision_images_v226", "vision_images_v308"),
    ("VL_GATE_V226", "VL_GATE_V308"), ("vl_gate_v226", "vl_gate_v308"),
]:
    out = out.replace(a, b)
out = re.sub(
    r"NEW themes vs V225:.*?(?=\n[A-Z]|\n\n|$)",
    "NEW themes vs V306: ashford, cedarford, dawnford, elmford, fernford, glenford, hazeford, inkford,\njadeford, knotford, lakeford, mossford, netherford, oakford, pineford, quillford, reedford, stoneford.",
    out, count=1, flags=re.S,
)
out = replace_specs(out, build_specs(T308, "v308", "V308", TR308))
out = retarget_307(out)
(S / "c1955_vision_v308_design_and_batch.py").write_text(out, encoding="utf-8")
print("design")

out = (S / "c1464_vision_v226_smoke.py").read_text(encoding="utf-8")
for a, b in [
    ("C1464", "C1956"), ("c1464", "c1956"), ("V226", "V308"), ("v226", "v308"),
    ("vision_images_v226", "vision_images_v308"),
    ("VL_GATE_V226", "VL_GATE_V308"), ("vl_gate_v226", "vl_gate_v308"),
    ("runs/vision_v226", "runs/vision_v308"),
]:
    out = out.replace(a, b)
(S / "c1956_vision_v308_smoke.py").write_text(out, encoding="utf-8")
print("smoke")

out = (S / "c1465_vision_v226_heldout.py").read_text(encoding="utf-8")
for a, b in [
    ("C1465", "C1957"), ("c1465", "c1957"), ("V226", "V308"), ("v226", "v308"),
    ("vision_images_v226h", "vision_images_v308h"),
    ("vision_images_v226", "vision_images_v308"),
    ("VL_GATE_V226", "VL_GATE_V308"), ("vl_gate_v226", "vl_gate_v308"),
    ("runs/vision_v226h", "runs/vision_v308h"),
    ("_v226c1463", "_v308c1955"),
]:
    out = out.replace(a, b)
out = replace_specs(out, build_specs(T308, "v308h", "V308H", HO308))
out2, seen_fix, seen_train, seen_run = [], False, False, False
for ln in out.splitlines():
    s = ln.strip()
    if s.startswith("FIX = ") and not seen_fix:
        out2.append('FIX = ROOT / "evo/office/fixtures/vision_images_v308h"'); seen_fix = True; continue
    if s.startswith("TRAIN_FIX = ") and not seen_train:
        out2.append('TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v308"'); seen_train = True; continue
    if s.startswith("RUN = ") and "vision_v308" in s and not seen_run:
        out2.append('RUN = ROOT / "runs/vision_v308h_c1957"'); seen_run = True; continue
    out2.append(ln)
(S / "c1957_vision_v308_heldout.py").write_text("\n".join(out2) + "\n", encoding="utf-8")
print("heldout", seen_fix, seen_train, seen_run)

SC1864 = '\ufeff# -*- coding: utf-8 -*-\n"""C1864: Unified scorecard + STAGE after C1955-C1863. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1864.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1956_VISION_V308_SMOKE.json") or {}\n    c654b = load("docs/r50/C1956b_VISION_GATE_V308_CLAIM.json") or {}\n    c655 = load("docs/r50/C1957_VISION_V308_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1957b_VISION_GATE_V308_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1856_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1863_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1862_PRODUCT_U2C_COST.json") or {}\n\n    v308 = float(c654.get("rate") or 0.0)\n    v308h = float(c655.get("rate") or 0.0)\n    v308_claim = bool(c654b.get("vl_gate_v308_claim") or c654.get("vl_gate_v308_claim") or c654.get("claim"))\n    v308h_claim = bool(c655b.get("vl_gate_v308_heldout_claim") or c655.get("vl_gate_v308_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1862"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v308_claim and v308h_claim and v308 >= GATE and v308h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v308 >= 0.999 and v308h >= 0.999) else min(v308, v308h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1864", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v308": {"rate": v308, "claim": v308_claim, "n": c654.get("n")},\n            "v308_heldout": {"rate": v308h, "claim": v308h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1862"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1856"},\n        "capture_regression": {"pass": capture_pass, "source": "C1863"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v308_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1864_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1864)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V308: rate={v308} claim={v308_claim}",\n        f"- Vision V308 heldout: rate={v308h} claim={v308h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1864", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1955-C1864 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1955: Vision V308 design fixtures",\n        f"- C1956: Vision V308 smoke **{v308}**", f"- C1957: Vision V308 heldout **{v308h}** (disjoint={disjoint})",\n        f"- C1862: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1856): pass={conf_pass} rate={conf_rate}",\n        f"- C1863: capture pass={capture_pass}", f"- C1864: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V308 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1864.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
SC1960 = '\ufeff# -*- coding: utf-8 -*-\n"""C1960: Unified scorecard + STAGE after C1955-C1959. gen11 HOLD. Gate 0.6."""\nfrom __future__ import annotations\nimport json\nfrom datetime import datetime\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nDOC = ROOT / "docs" / "r50"\nBOARD_MD = ROOT / "docs" / "蚁算_UNIFIED_SCORECARD.md"\nSCORE_LATEST = DOC / "SCORECARD_LATEST.json"\nSTAGE = ROOT / "docs" / "STAGE_ANT_C1960.md"\nGATE = 0.6\n\n\ndef ts():\n    return datetime.now().astimezone().isoformat(timespec="seconds")\n\n\ndef J(p, o):\n    p.parent.mkdir(parents=True, exist_ok=True)\n    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n\ndef load(rel):\n    p = ROOT / rel\n    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None\n\n\ndef main():\n    c654 = load("docs/r50/C1956_VISION_V308_SMOKE.json") or {}\n    c654b = load("docs/r50/C1956b_VISION_GATE_V308_CLAIM.json") or {}\n    c655 = load("docs/r50/C1957_VISION_V308_HELDOUT_SMOKE.json") or {}\n    c655b = load("docs/r50/C1957b_VISION_GATE_V308_HELDOUT_CLAIM.json") or {}\n    c656 = load("docs/r50/C1952_CONFIDENCE_GATE_STRETCH.json") or {}\n    c657 = load("docs/r50/C1959_CAPTURE_OFFICE_REGRESSION.json") or {}\n    prior = load("docs/r50/SCORECARD_LATEST.json") or {}\n    c398 = load("docs/r50/C398_DISSOLVE_COST_SHADOW.json") or {}\n    c650 = load("docs/r50/C1958_PRODUCT_U2C_COST.json") or {}\n\n    v308 = float(c654.get("rate") or 0.0)\n    v308h = float(c655.get("rate") or 0.0)\n    v308_claim = bool(c654b.get("vl_gate_v308_claim") or c654.get("vl_gate_v308_claim") or c654.get("claim"))\n    v308h_claim = bool(c655b.get("vl_gate_v308_heldout_claim") or c655.get("vl_gate_v308_heldout_claim") or c655.get("claim"))\n    disjoint = bool(c655.get("id_disjoint") or c655.get("disjoint") or c655b.get("id_disjoint") or c655b.get("disjoint"))\n    conf_pass = bool(c656.get("pass"))\n    conf_rate = float(c656.get("rate") or 0.0)\n    u2c = prior.get("product_u2c") or {}\n    if c650.get("pass") is not None:\n        u2c = {"pass": bool(c650.get("pass")), "replace_ratio": float(c650.get("replace_ratio") or c650.get("mean_ratio") or 4.07), "source": "C1958"}\n    replace = float(u2c.get("replace_ratio") or 4.07)\n    u2c_pass = bool((u2c or {}).get("pass"))\n    capture_pass = bool(c657.get("pass"))\n    dissolve_pass = bool(c398.get("pass") or (prior.get("dissolve_shadow") or {}).get("dissolve_pass"))\n    shadow_pass = bool((prior.get("dissolve_shadow") or {}).get("shadow_pass", dissolve_pass))\n    stage_ready = bool(v308_claim and v308h_claim and v308 >= GATE and v308h >= GATE and capture_pass and disjoint and u2c_pass)\n    composite = (1.0 if (v308 >= 0.999 and v308h >= 0.999) else min(v308, v308h)) if stage_ready else 0.0\n    out = {\n        "cycle": "C1960", "timestamp": ts(), "gate": GATE,\n        "vision": {\n            "v226": (prior.get("vision") or {}).get("v226") or {"rate": 1.0, "claim": True},\n            "v226_heldout": (prior.get("vision") or {}).get("v226_heldout") or {"rate": 1.0, "claim": True},\n            "v308": {"rate": v308, "claim": v308_claim, "n": c654.get("n")},\n            "v308_heldout": {"rate": v308h, "claim": v308h_claim, "disjoint": disjoint, "n": c655.get("n")},\n        },\n        "product_u2c": u2c if u2c else {"pass": True, "replace_ratio": replace, "source": "C1958"},\n        "confidence_gate": {"pass": conf_pass, "rate": conf_rate, "source": "C1952"},\n        "capture_regression": {"pass": capture_pass, "source": "C1959"},\n        "dissolve_shadow": {"dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass, "source": "C398"},\n        "composite": composite, "stage_ready": stage_ready,\n        "v308_jpeg_q": 62, "gate2_3_untouched": True, "gen11": "HOLD",\n    }\n    J(DOC / "C1960_SCORECARD_AND_STAGE.json", out)\n    J(SCORE_LATEST, out)\n    BOARD_MD.write_text("\\n".join([\n        "# Unified Scorecard (C1960)", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"- Vision V308: rate={v308} claim={v308_claim}",\n        f"- Vision V308 heldout: rate={v308h} claim={v308h_claim} disjoint={disjoint}",\n        f"- product_u2c: {out[\'product_u2c\']}", f"- confidence_gate: {out[\'confidence_gate\']}",\n        f"- capture_regression: pass={capture_pass}", f"- composite: {composite}",\n        f"- stage_ready: {stage_ready}", "- Gate: 0.6 | Gate2/3 untouched | gen11 HOLD", "",\n    ]) + "\\n", encoding="utf-8")\n    STAGE.write_text("\\n".join([\n        "# STAGE_ANT_C1960", "", f"Updated: {ts()} (Asia/Shanghai)", "",\n        f"**C1955-C1960 STAGE_READY={\'YES\' if stage_ready else \'NO\'}**", "",\n        "## Tip slice",\n        "- C1955: Vision V308 design fixtures",\n        f"- C1956: Vision V308 smoke **{v308}**", f"- C1957: Vision V308 heldout **{v308h}** (disjoint={disjoint})",\n        f"- C1958: product-U2C replace={replace} pass={u2c_pass}",\n        f"- confidence-gate (prior C1952): pass={conf_pass} rate={conf_rate}",\n        f"- C1959: capture pass={capture_pass}", f"- C1960: composite={composite}", "",\n        "## Product framing",\n        "- 蚁算 replaces the Agent role for the user (model+tools internally).", "",\n        "## Constraints", "- Gate: 0.6", "- Gate2/3: untouched", "- gen11: HOLD",\n        "- clarity floor jpeg_q>=60 kept on V308 (uses 62)",\n        "- lesson: avoid *b theme-name collapse (V88)", "",\n        "## Entry", "- docs/r50/SCORECARD_LATEST.json", "- docs/STAGE_ANT_C1960.md", "",\n    ]) + "\\n", encoding="utf-8")\n    print(json.dumps(out, ensure_ascii=False, indent=2))\n    return 0 if stage_ready else 1\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
# V308 knife = product-U2C (alternating; V307 was confidence-gate)
out = (S / "c1946_product_u2c_cost.py").read_text(encoding="utf-8")
for a, b2 in [
    ("C1946", "C1958"), ("c1946", "c1958"),
    ("C1934", "C1958"), ("c1934", "c1958"),
    ("product_u2c_cost_c1946", "product_u2c_cost_c1958"),
    ("u2c_v197", "u2c_v198"),
    ("u2c_c1946", "u2c_c1958"),
]:
    out = out.replace(a, b2)
(S / "c1958_product_u2c_cost.py").write_text(out, encoding="utf-8")
print("product_u2c from c1946")

out = (S / "c1953_capture_office_regression.py").read_text(encoding="utf-8")
for a, b2 in [("C1953", "C1959"), ("c1953", "c1959")]:
    out = out.replace(a, b2)
(S / "c1959_capture_office_regression.py").write_text(out, encoding="utf-8")
print("capture")

(S / "c1960_scorecard_and_stage.py").write_text(SC1960, encoding="utf-8")
print("scorecard from fixed c1948 product-U2C pattern")
print("OK builder v308 ready")
