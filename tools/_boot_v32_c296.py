# -*- coding: utf-8 -*-
"""Bootstrap C296-C301 Vision V32 suite from V31 scripts + product/U2C NV."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"
SPEC_PATH = ROOT / "tools" / "_v32_specs.json"

V32_OVERLAY = r'''
    # --- V32 overlays (new vs V31) ---
    # kraft fiber speckles (below text band)
    for _ in range(90):
        kx = rng.randint(70, 520)
        ky = rng.randint(320, 560)
        if in_text_band(ky):
            continue
        d.point((kx, ky), fill=(160, 130, 90))
        if rng.random() < 0.3:
            d.ellipse([kx, ky, kx + 3, ky + 2], fill=(140, 110, 70))
    # linen weave hatch
    for lx in range(70, 520, 8):
        d.line([(lx, 300), (lx + 20, 330)], fill=(190, 185, 175), width=1)
    for ly in range(300, 340, 6):
        d.line([(70, ly), (200, ly)], fill=(185, 180, 170), width=1)
    # thermal fade stripe (gray wash)
    d.rectangle([600, 80, 780, 260], fill=(230, 230, 225))
    d.text((610, 100), "THERMAL FADE bait 55.55", fill=(160, 160, 150), font=f_fax)
    # dossier tab top-right
    d.polygon([(980, 8), (1060, 8), (1060, 48), (1000, 48), (980, 28)], fill=(200, 180, 120), outline=(80, 60, 20), width=2)
    d.text((990, 18), "DOSSIER", fill=(60, 40, 10), font=f_tiny)
    # chrono stamp circle
    d.ellipse([850, 480, 950, 560], outline=(20, 20, 80), width=3)
    d.text((862, 510), "CHRONO", fill=(20, 20, 80), font=f_stamp)
    d.text((868, 530), "12:32", fill=(20, 20, 80), font=f_tiny)
    # rubber pad rectangle
    d.rectangle([100, 480, 220, 540], fill=(40, 90, 50), outline=(20, 50, 30), width=2)
    d.text((110, 500), "RUBBER", fill=(220, 255, 220), font=f_stamp)
    # checker bait tiles
    for ci in range(6):
        for cj in range(3):
            col = (60, 60, 70) if (ci + cj) % 2 == 0 else (200, 200, 210)
            d.rectangle([70 + ci * 18, 400 + cj * 18, 86 + ci * 18, 416 + cj * 18], fill=col)
    d.text((70, 458), "CHECK bait 33.33", fill=(40, 40, 50), font=f_tiny)
    # vellum translucent wash
    d.rectangle([400, 340, 540, 420], fill=(240, 245, 255))
    d.text((410, 370), "VELLUM ghost 22.22", fill=(150, 160, 180), font=f_pen)
    # brad fasteners
    for by in (90, 200, 310):
        d.ellipse([35, by, 55, by + 16], fill=(90, 90, 100), outline=(30, 30, 30), width=1)
        d.ellipse([40, by + 4, 50, by + 12], fill=(180, 180, 190))
    # scroll curl arcs
    for t in range(0, 7):
        x0 = 250 + t * 40
        d.arc([x0, 350, x0 + 36, 390], 0, 180, fill=(90, 80, 70), width=2)
    # ditto purple ghost text
    d.text((90, 380), "DITTO PURPLE bait 77.77", fill=(120, 60, 140), font=f_pen)
    # flock texture dots dense
    for _ in range(140):
        fx = rng.randint(60, 530)
        fy = rng.randint(450, 575)
        d.point((fx, fy), fill=(100, 80, 90))
    # matrix UI vertical dashes
    for my in range(70, 250, 7):
        d.line([(560, my), (575, my)], fill=(30, 30, 40), width=1)
    # axonometric grid
    for ax in range(70, 300, 24):
        d.line([(ax, 250), (ax + 40, 290)], fill=(170, 190, 210), width=1)
    for ay in range(250, 295, 12):
        d.line([(70, ay), (300, ay)], fill=(170, 190, 210), width=1)
    # twine binding loops left
    for ty in range(80, 500, 55):
        d.arc([0, ty, 40, ty + 40], 270, 90, fill=(90, 70, 40), width=2)
    # chamfer edge band
    d.polygon([(60, 14), (380, 14), (370, 28), (70, 28)], fill=(180, 140, 70), outline=(100, 70, 20), width=1)
    d.text((80, 15), "CHAMFER bait 44.44", fill=(60, 30, 0), font=f_tiny)
    # snap button tab
    d.ellipse([500, 60, 536, 96], fill=(50, 50, 60), outline=(10, 10, 10), width=2)
    d.ellipse([510, 70, 526, 86], fill=(200, 200, 210))
    d.rectangle([520, 90, 560, 130], fill=(90, 90, 100), outline=(20, 20, 20), width=1)
    d.text((524, 102), "SNAP", fill=(230, 230, 240), font=f_tiny)
'''


def specs_to_py(rows):
    lines = ["SPECS = ["]
    for r in rows:
        lines.append(
            f'    ("{r["id"]}", "{r["kind"]}", "{r["metric"]}", {r["expected"]},\n'
            f'     {json.dumps(r["lines"], ensure_ascii=False)},\n'
            f'     {json.dumps(r["cn"], ensure_ascii=False)}, "{r["stamp"]}"),'
        )
    lines.append("]")
    return "\n".join(lines) + "\n"


def replace_specs(text: str, new_specs: str) -> str:
    return re.sub(r"SPECS = \[.*?\]\n", new_specs, text, count=1, flags=re.S)


def xform_train(text: str, train_specs: str) -> str:
    reps = [
        ("C290", "C296"), ("C291", "C297"), ("C292", "C298"),
        ("v31", "v32"), ("V31", "V32"), ("V31H", "V32H"), ("v31h", "v32h"),
        ("vision_v31_c290", "vision_v32_c296"),
        ("VL_GATE_V31_PROTOCOL", "VL_GATE_V32_PROTOCOL"),
        ("vl_gate_v31_claim", "vl_gate_v32_claim"),
        ("vision_gate_v31_claim", "vision_gate_v32_claim"),
        ("r50plus_v31_", "r50plus_v32_"),
        ("SCAN DESK V31", "SCAN DESK V32"),
        ("V31 C290", "V32 C296"),
        ("V31 keeps floor", "V32 keeps floor"),
        ("Vision V31", "Vision V32"),
        ("vision_v31", "vision_v32"),
        ("_v31c290", "_v32c296"),
        ("harder than V30", "harder than V31"),
        ("NEW themes vs V30", "NEW themes vs V31"),
        ("No claim until C291 VL", "No claim until C297 VL"),
        (
            "Graphite|Emboss|Carbon|Binder|Postage|Foil|Mesh|Wax|Punch|Accordion|Stencil|Mottled|Toner|Blueprint|Clasp|Edgeband|Grommet",
            "Kraft|Linen|Thermal|Dossier|Chrono|Rubber|Checker|Vellum|Brad|Scroll|Ditto|Flock|Matrix|Axon|Twine|Chamfer|Snap",
        ),
        (
            "graphite_emboss_carbon_binder_postage_foil_mesh_wax_punch_accordion_stencil_mottled_toner_blueprint_clasp_edgeband_grommet",
            "kraft_linen_thermal_dossier_chrono_rubber_checker_vellum_brad_scroll_ditto_flock_matrix_axon_twine_chamfer_snap",
        ),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    text = replace_specs(text, train_specs)
    if "V32 overlays" not in text:
        soft = "    # soft_affine"
        if soft in text:
            text = text.replace(soft, V32_OVERLAY + "\n" + soft, 1)
        else:
            text = text.replace("    img.save(buf", V32_OVERLAY + "\n    img.save(buf", 1)
    text = re.sub(
        r"NEW themes vs V3[12]:.*?\nCLARITY FLOOR:",
        "NEW themes vs V31: kraft, linen, thermal, dossier, chrono, rubber, checker, vellum,\n"
        "brad, scroll, ditto, flock, matrix, axon, twine, chamfer, snap.\n"
        "CLARITY FLOOR:",
        text,
        count=1,
        flags=re.S,
    )
    return text


def xform_smoke(text: str) -> str:
    reps = [
        ("C291", "C297"), ("C290", "C296"),
        ("v31", "v32"), ("V31", "V32"),
        ("vision_images_v31", "vision_images_v32"),
        ("vision_v31_c291", "vision_v32_c297"),
        ("vision_v31_c285", "vision_v32_c297"),
        ("vl_gate_v31_claim", "vl_gate_v32_claim"),
        ("vision_gate_v31_claim", "vision_gate_v32_claim"),
        ("r50plus_v31_", "r50plus_v32_"),
        ("vision_v31_smoke", "vision_v32_smoke"),
        ("C291_VISION_V31", "C297_VISION_V32"),
        ("C291b_VISION_GATE_V31", "C297b_VISION_GATE_V32"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    return text


def xform_heldout(text: str, held_specs: str) -> str:
    reps = [
        ("C292", "C298"), ("C290", "C296"), ("C291", "C297"),
        ("v31h", "v32h"), ("V31H", "V32H"), ("v31", "v32"), ("V31", "V32"),
        ("vision_images_v31h", "vision_images_v32h"),
        ("vision_images_v31", "vision_images_v32"),
        ("vision_v31h_c292", "vision_v32h_c298"),
        ("VL_GATE_V31_HELDOUT_PROTOCOL", "VL_GATE_V32_HELDOUT_PROTOCOL"),
        ("vl_gate_v31_heldout_claim", "vl_gate_v32_heldout_claim"),
        ("vision_gate_v31_heldout_claim", "vision_gate_v32_heldout_claim"),
        ("r50plus_v31_heldout", "r50plus_v32_heldout"),
        ("vision_v31_heldout", "vision_v32_heldout"),
        ("C292_VISION_V31", "C298_VISION_V32"),
        ("C292b_VISION_GATE_V31", "C298b_VISION_GATE_V32"),
        ("SCAN DESK V31H", "SCAN DESK V32H"),
        ("V31H C292", "V32H C298"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    return replace_specs(text, held_specs)


def xform_nv(text: str) -> str:
    text = text.replace("C281", "C299")
    text = text.replace("product_u2c_c281", "product_u2c_c299")
    text = text.replace("C281_PRODUCT_U2C_COST.json", "C299_PRODUCT_U2C_COST.json")
    text = text.replace("vision_images_v28", "vision_images_v32")
    text = text.replace("vision_images_v31", "vision_images_v32")
    text = text.replace('"version": "v25"', '"version": "v32"')
    text = text.replace('"version": "v28"', '"version": "v32"')
    text = text.replace("missing_v25_manifest", "missing_v32_manifest")
    text = text.replace('"bare_steps": 4, "agent_steps": 15', '"bare_steps": 4, "agent_steps": 17')
    text = text.replace('"bare_steps": 3, "agent_steps": 12', '"bare_steps": 3, "agent_steps": 14', 1)
    text = text.replace('"bare_steps": 5, "agent_steps": 18', '"bare_steps": 5, "agent_steps": 20')
    text = text.replace('"bare_steps": 2, "agent_steps": 9', '"bare_steps": 2, "agent_steps": 11')
    return text


def xform_reg(text: str) -> str:
    text = text.replace("C294", "C300")
    text = text.replace("C290-C293", "C296-C299")
    text = text.replace("c290_c293", "c296_c299")
    text = text.replace("capture_regression_c294", "capture_regression_c300")
    needle = '("V31_heldout", DOC / "C292_VISION_V31_HELDOUT_SMOKE.json"),'
    insert = (
        needle
        + '\n    ("V32", DOC / "C297_VISION_V32_SMOKE.json"),'
        + '\n    ("V32_heldout", DOC / "C298_VISION_V32_HELDOUT_SMOKE.json"),'
    )
    if needle in text and '("V32"' not in text:
        text = text.replace(needle, insert)
    text = text.replace(
        '("C293_dissolve_cost_shadow", DOC / "C293_DISSOLVE_COST_SHADOW.json"),',
        '("C293_dissolve_cost_shadow", DOC / "C293_DISSOLVE_COST_SHADOW.json"),\n'
        '    ("C299_product_u2c_cost", DOC / "C299_PRODUCT_U2C_COST.json"),',
    )
    text = text.replace(
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "V31", "V31_heldout", "C233_clarity_floor", "C293_dissolve_cost_shadow"]',
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "V31", "V31_heldout", "V32", "V32_heldout", "C233_clarity_floor", "C299_product_u2c_cost"]',
    )
    text = text.replace('DOC / "C294_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C300_CAPTURE_OFFICE_REGRESSION.json"')
    return text


def xform_score(text: str) -> str:
    text = text.replace("C295", "C301")
    text = text.replace("c290_c294", "c296_c300")
    text = text.replace("STAGE_ANT_C295.md", "STAGE_ANT_C301.md")
    text = text.replace("C290-C294", "C296-C300")
    text = text.replace("C290-C295", "C296-C301")

    hist_inject = '''    c291v = load("docs/r50/C291_VISION_V31_SMOKE.json") or {}
    c291vb = load("docs/r50/C291b_VISION_GATE_V31_CLAIM.json") or {}
    c292v = load("docs/r50/C292_VISION_V31_HELDOUT_SMOKE.json") or {}
    c292vb = load("docs/r50/C292b_VISION_GATE_V31_HELDOUT_CLAIM.json") or {}
    c266 = load("docs/r50/C296_VISION_V32_DESIGN.json") or {}
    c267 = load("docs/r50/C297_VISION_V32_SMOKE.json") or {}
    c267b = load("docs/r50/C297b_VISION_GATE_V32_CLAIM.json") or {}
    c268 = load("docs/r50/C298_VISION_V32_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C298b_VISION_GATE_V32_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C300_CAPTURE_OFFICE_REGRESSION.json") or {}'''

    old_block = '''    c266 = load("docs/r50/C290_VISION_V31_DESIGN.json") or {}
    c267 = load("docs/r50/C291_VISION_V31_SMOKE.json") or {}
    c267b = load("docs/r50/C291b_VISION_GATE_V31_CLAIM.json") or {}
    c268 = load("docs/r50/C292_VISION_V31_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C292b_VISION_GATE_V31_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C294_CAPTURE_OFFICE_REGRESSION.json") or {}'''
    if old_block in text:
        text = text.replace(old_block, hist_inject)

    text = text.replace(
        'c269 = load("docs/r50/C293_DISSOLVE_COST_SHADOW.json") or {}\n'
        '    c287 = load("docs/r50/C287_CONFIDENCE_GATE_STRETCH.json") or {}',
        'c269 = load("docs/r50/C299_PRODUCT_U2C_COST.json") or {}\n'
        '    c293 = load("docs/r50/C293_DISSOLVE_COST_SHADOW.json") or {}\n'
        '    c287 = load("docs/r50/C287_CONFIDENCE_GATE_STRETCH.json") or {}',
    )
    if "C299_PRODUCT_U2C_COST" not in text:
        text = text.replace(
            'c269 = load("docs/r50/C293_DISSOLVE_COST_SHADOW.json") or {}',
            'c269 = load("docs/r50/C299_PRODUCT_U2C_COST.json") or {}\n'
            '    c293 = load("docs/r50/C293_DISSOLVE_COST_SHADOW.json") or {}',
        )

    text = text.replace(
        '''    v31 = float(c267.get("rate") or 0.0)
    v31h = float(c268.get("rate") or 0.0)''',
        '''    v31 = float(c291v.get("rate") or 0.0)
    v31h = float(c292v.get("rate") or 0.0)
    v32 = float(c267.get("rate") or 0.0)
    v32h = float(c268.get("rate") or 0.0)''',
    )
    text = text.replace(
        '''    v31_claim = bool(c267b.get("vl_gate_v31_claim") or c267.get("vl_gate_v31_claim") or c267.get("claim"))
    v31h_claim = bool(c268b.get("vl_gate_v31_heldout_claim") or c268.get("vl_gate_v31_heldout_claim") or c268.get("claim"))''',
        '''    v31_claim = bool(c291vb.get("vl_gate_v31_claim") or c291v.get("vl_gate_v31_claim") or c291v.get("claim"))
    v31h_claim = bool(c292vb.get("vl_gate_v31_heldout_claim") or c292v.get("vl_gate_v31_heldout_claim") or c292v.get("claim"))
    v32_claim = bool(c267b.get("vl_gate_v32_claim") or c267.get("vl_gate_v32_claim") or c267.get("claim"))
    v32h_claim = bool(c268b.get("vl_gate_v32_heldout_claim") or c268.get("vl_gate_v32_heldout_claim") or c268.get("claim"))''',
    )

    text = text.replace(
        '''    dissolve_pass = bool((c269.get("dissolve") or c263.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c269.get("shadow") or c263.get("shadow") or {}).get("pass", True))
    nv_pass = bool(c269.get("pass") and dissolve_pass and shadow_pass)
    conf_pass = bool(c287.get("pass"))
    conf_rate = float(c287.get("rate") or 0.0)
    dissolve_rate = float(((c269.get("dissolve") or {}).get("summary") or {}).get("n_families") or 4)''',
        '''    dissolve_pass = bool((c293.get("dissolve") or c263.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c293.get("shadow") or c263.get("shadow") or {}).get("pass", True))
    nv_pass = bool(c269.get("pass"))
    conf_pass = bool(c287.get("pass"))
    conf_rate = float(c287.get("rate") or 0.0)
    u2c_rate = float((c269.get("u2c") or {}).get("rate") or c269.get("rate") or 0.0)
    dissolve_rate = float(((c293.get("dissolve") or {}).get("summary") or {}).get("n_families") or 4)''',
    )

    text = text.replace(
        'rl = (c281.get("replace_ledger") or (c269.get("replace_stress") or {}) or c269.get("replace_ledger") or {})',
        'rl = ((c269.get("replace_ledger") or {}) or (c293.get("replace_stress") or {}) or (c281.get("replace_ledger") or {}) or {})',
    )
    text = text.replace(
        '"mean_ratio": ((c269.get("replace_stress") or {}).get("mean_ratio")\n'
        '                       or rl.get("mean_ratio")\n'
        '                       or (c263.get("replace_stress") or {}).get("mean_ratio")\n'
        '                       or (c263.get("cost_ledger") or {}).get("replace_mean_ratio") or 3.9188),',
        '"mean_ratio": (rl.get("mean_ratio")\n'
        '                       or (c269.get("replace_ledger") or {}).get("mean_ratio")\n'
        '                       or (c293.get("replace_stress") or {}).get("mean_ratio")\n'
        '                       or (c263.get("replace_stress") or {}).get("mean_ratio")\n'
        '                       or (c263.get("cost_ledger") or {}).get("replace_mean_ratio") or 3.9188),',
    )
    text = text.replace(
        '"source": "C293" if (c269.get("replace_stress") or {}).get("mean_ratio") is not None else ("C281" if (c281.get("replace_ledger") or {}).get("mean_ratio") is not None else "C263")',
        '"source": "C299" if (c269.get("replace_ledger") or {}).get("mean_ratio") is not None else ("C293" if (c293.get("replace_stress") or {}).get("mean_ratio") is not None else "C263")',
    )

    text = text.replace(
        '''        max(v31, v31h, 0.0),
        1.0 if v31_claim else 0.0,
        1.0 if v31h_claim else 0.0,''',
        '''        max(v31, v31h, 0.0),
        1.0 if v31_claim else 0.0,
        1.0 if v31h_claim else 0.0,
        max(v32, v32h, 0.0),
        1.0 if v32_claim else 0.0,
        1.0 if v32h_claim else 0.0,''',
    )
    text = text.replace(
        "v31_claim and v31h_claim and capture_pass and nv_pass",
        "v32_claim and v32h_claim and capture_pass and nv_pass",
    )

    text = text.replace(
        '''            "v31_design": {"n": c266.get("n"), "clarity_floor": c266.get("clarity_floor"), "claim": False},
            "v31_smoke": {
                "rate": v31, "n": c267.get("n"), "n_ok": c267.get("n_ok"),
                "claim": v31_claim, "fail_ids": c267.get("fail_ids"),
            },
            "v31_heldout": {
                "rate": v31h, "n": c268.get("n"), "n_ok": c268.get("n_ok"),
                "claim": v31h_claim, "fail_ids": c268.get("fail_ids"),
                "id_disjoint": c268.get("id_disjoint"),
            },''',
        '''            "v31_smoke": {"rate": v31, "claim": v31_claim},
            "v31_heldout": {"rate": v31h, "claim": v31h_claim},
            "v32_design": {"n": c266.get("n"), "clarity_floor": c266.get("clarity_floor"), "claim": False},
            "v32_smoke": {
                "rate": v32, "n": c267.get("n"), "n_ok": c267.get("n_ok"),
                "claim": v32_claim, "fail_ids": c267.get("fail_ids"),
            },
            "v32_heldout": {
                "rate": v32h, "n": c268.get("n"), "n_ok": c268.get("n_ok"),
                "claim": v32h_claim, "fail_ids": c268.get("fail_ids"),
                "id_disjoint": c268.get("id_disjoint"),
            },''',
    )
    text = text.replace(
        '''            "dissolve_cost_shadow": {"pass": nv_pass, "dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass},
            "confidence_gate_stretch": {"pass": conf_pass, "rate": conf_rate},
            "replace_ratio": replace.get("mean_ratio"),''',
        '''            "product_u2c_cost": {"pass": nv_pass, "rate": u2c_rate},
            "dissolve_cost_shadow": {"pass": bool(c293.get("pass")), "dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass},
            "confidence_gate_stretch": {"pass": conf_pass, "rate": conf_rate},
            "replace_ratio": replace.get("mean_ratio"),''',
    )

    text = text.replace(
        "| V31 smoke / heldout | **{v31} / {v31h}** claim={v31_claim}/{v31h_claim} |\n"
        "| dissolve/shadow (C293) | pass={nv_pass} dissolve={dissolve_pass} shadow={shadow_pass} |\n"
        "| confidence-gate stretch (C287) | pass={conf_pass} rate={conf_rate} |",
        "| V31 smoke / heldout | **{v31} / {v31h}** claim={v31_claim}/{v31h_claim} |\n"
        "| V32 smoke / heldout | **{v32} / {v32h}** claim={v32_claim}/{v32h_claim} |\n"
        "| product/U2C (C299) | pass={nv_pass} rate={u2c_rate} |\n"
        "| dissolve/shadow (C293) | dissolve={dissolve_pass} shadow={shadow_pass} |\n"
        "| confidence-gate stretch (C287) | pass={conf_pass} rate={conf_rate} |",
    )
    text = text.replace(
        '''| C290 | V31 design | n={c266.get('n')} graphite/emboss/carbon/binder/... |
| C291 | V31 smoke | rate={v31} claim={v31_claim} |
| C292 | V31 heldout | rate={v31h} claim={v31h_claim} |
| C293 | dissolve/shadow refresh | pass={nv_pass} |
| C294 | capture regression | pass={capture_pass} |
| C295 | scorecard | composite={composite} |''',
        '''| C296 | V32 design | n={c266.get('n')} kraft/linen/thermal/dossier/... |
| C297 | V32 smoke | rate={v32} claim={v32_claim} |
| C298 | V32 heldout | rate={v32h} claim={v32h_claim} |
| C299 | product/U2C | pass={nv_pass} rate={u2c_rate} |
| C300 | capture regression | pass={capture_pass} |
| C301 | scorecard | composite={composite} |''',
    )
    text = text.replace(
        "- V31: claim={v31_claim} rate={v31}\n- V31 heldout: claim={v31h_claim} rate={v31h}",
        "- V31: claim={v31_claim} rate={v31}\n- V31 heldout: claim={v31h_claim} rate={v31h}\n"
        "- V32: claim={v32_claim} rate={v32}\n- V32 heldout: claim={v32h_claim} rate={v32h}",
    )
    text = text.replace(
        "Stage: C290-C295; V31 CLAIM {v31}; V31 heldout CLAIM {v31h}",
        "Stage: C296-C301; V32 CLAIM {v32}; V32 heldout CLAIM {v32h}",
    )
    text = text.replace(
        "V31 design: clarity_floor jpeg_q=60 photo/=2 themes=graphite/emboss/carbon/binder/postage/foil/mesh/wax/punch/accordion/stencil/mottled/toner/blueprint/clasp/edgeband/grommet",
        "V32 design: clarity_floor jpeg_q=60 photo/=2 themes=kraft/linen/thermal/dossier/chrono/rubber/checker/vellum/brad/scroll/ditto/flock/matrix/axon/twine/chamfer/snap",
    )
    text = text.replace(
        "V31 smoke: rate={v31} n={c267.get('n')} CLAIM={v31_claim} fail={c267.get('fail_ids')}",
        "V32 smoke: rate={v32} n={c267.get('n')} CLAIM={v32_claim} fail={c267.get('fail_ids')}",
    )
    text = text.replace(
        "V31 heldout: rate={v31h} n={c268.get('n')} CLAIM={v31h_claim} disjoint={c268.get('id_disjoint')}",
        "V32 heldout: rate={v32h} n={c268.get('n')} CLAIM={v32h_claim} disjoint={c268.get('id_disjoint')}",
    )
    text = text.replace(
        "Non-vision C293: pass={nv_pass} (dissolve/shadow refresh); conf-gate C287={conf_pass}/{conf_rate}; replace_ratio={replace.get('mean_ratio')}",
        "Non-vision C299: pass={nv_pass} rate={u2c_rate} (product/U2C); dissolve C293={dissolve_pass}/{shadow_pass}; conf-gate C287={conf_pass}/{conf_rate}; replace_ratio={replace.get('mean_ratio')}",
    )
    text = text.replace("Capture regression: pass={capture_pass} (C294)", "Capture regression: pass={capture_pass} (C300)")
    text = text.replace("Scorecard composite: {composite} (C295)", "Scorecard composite: {composite} (C301)")
    text = text.replace(
        'f.write(f"- V31 smoke={v31} claim={v31_claim}; heldout={v31h} claim={v31h_claim}\\n")',
        'f.write(f"- V32 smoke={v32} claim={v32_claim}; heldout={v32h} claim={v32h_claim}\\n")',
    )
    text = text.replace(
        'f.write(f"- C293 dissolve/shadow pass={nv_pass}; conf-gate={conf_pass}/{conf_rate}; replace',
        'f.write(f"- C299 product/U2C pass={nv_pass} rate={u2c_rate}; conf-gate={conf_pass}/{conf_rate}; replace',
    )
    text = text.replace("unified_scorecard_c290_c294", "unified_scorecard_c296_c300")
    return text


def main():
    specs = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    train_specs = specs_to_py(specs["train"])
    held_specs = specs_to_py(specs["held"])
    mapping = [
        ("c290_vision_v31_design_and_batch.py", "c296_vision_v32_design_and_batch.py",
         lambda t: xform_train(t, train_specs)),
        ("c291_vision_v31_smoke.py", "c297_vision_v32_smoke.py", xform_smoke),
        ("c292_vision_v31_heldout.py", "c298_vision_v32_heldout.py",
         lambda t: xform_heldout(t, held_specs)),
        ("c281_product_u2c_cost.py", "c299_product_u2c_cost.py", xform_nv),
        ("c294_capture_office_regression.py", "c300_capture_office_regression.py", xform_reg),
        ("c295_scorecard_and_stage.py", "c301_scorecard_and_stage.py", xform_score),
    ]
    for src, dst, fn in mapping:
        t = (SCR / src).read_text(encoding="utf-8")
        out = fn(t)
        (SCR / dst).write_text(out, encoding="utf-8")
        print("wrote", dst, "bytes", len(out.encode("utf-8")))
    d = (SCR / "c296_vision_v32_design_and_batch.py").read_text(encoding="utf-8")
    assert "vision_images_v32" in d and "v32_01" in d
    assert "V32 overlays" in d
    assert "kraft_recv" in d
    assert "JPEG_Q = 60" in d
    s = (SCR / "c301_scorecard_and_stage.py").read_text(encoding="utf-8")
    assert "STAGE_ANT_C301.md" in s
    assert "C297_VISION_V32_SMOKE" in s
    assert "v32_claim" in s
    assert "C299_PRODUCT_U2C_COST" in s
    nv = (SCR / "c299_product_u2c_cost.py").read_text(encoding="utf-8")
    assert "C299" in nv and "vision_images_v32" in nv
    print("ok")


if __name__ == "__main__":
    main()
