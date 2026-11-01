# -*- coding: utf-8 -*-
"""Bootstrap C302-C307 Vision V33 suite from V32 scripts + confidence-gate NV."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"
SPEC_PATH = ROOT / "tools" / "_v33_specs.json"

V33_OVERLAY = r'''
    # --- V33 overlays (new vs V32) ---
    # parchment fiber wash
    for _ in range(100):
        px = rng.randint(70, 520)
        py = rng.randint(320, 560)
        if in_text_band(py):
            continue
        d.point((px, py), fill=(210, 190, 150))
        if rng.random() < 0.25:
            d.ellipse([px, py, px + 4, py + 2], fill=(190, 170, 130))
    # cork pore dots
    for _ in range(80):
        cx = rng.randint(70, 250)
        cy = rng.randint(300, 380)
        d.ellipse([cx, cy, cx + 3, cy + 3], fill=(160, 120, 70))
    # canvas weave crosshatch
    for lx in range(70, 300, 10):
        d.line([(lx, 300), (lx + 18, 330)], fill=(180, 175, 160), width=1)
    for ly in range(300, 340, 8):
        d.line([(70, ly), (220, ly)], fill=(175, 170, 155), width=1)
    # rivet heads left margin
    for ry in (95, 180, 265, 350):
        d.ellipse([28, ry, 52, ry + 20], fill=(120, 120, 130), outline=(40, 40, 50), width=2)
        d.ellipse([34, ry + 6, 46, ry + 14], fill=(200, 200, 210))
    # holo rainbow strip
    for hi, col in enumerate([(255, 80, 80), (80, 255, 80), (80, 80, 255), (255, 255, 80)]):
        d.rectangle([600 + hi * 40, 40, 638 + hi * 40, 70], fill=col)
    d.text((610, 74), "HOLO bait 55.55", fill=(90, 40, 120), font=f_tiny)
    # zip teeth row
    for zi in range(12):
        d.polygon([(400 + zi * 12, 360), (406 + zi * 12, 348), (412 + zi * 12, 360)], fill=(50, 50, 60))
    d.text((400, 366), "ZIP bait 33.33", fill=(40, 40, 50), font=f_tiny)
    # filament glow arcs
    for t in range(0, 6):
        x0 = 250 + t * 45
        d.arc([x0, 400, x0 + 40, 450], 200, 340, fill=(255, 180, 60), width=2)
    # honeycomb hex bait
    d.polygon([(70, 430), (90, 420), (110, 430), (110, 450), (90, 460), (70, 450)], outline=(180, 120, 40), width=2)
    d.text((70, 468), "HONEY bait 22.22", fill=(120, 80, 20), font=f_tiny)
    # marble veins
    for _ in range(8):
        x0 = rng.randint(300, 500)
        y0 = rng.randint(340, 500)
        d.line([(x0, y0), (x0 + rng.randint(40, 90), y0 + rng.randint(-20, 20))], fill=(160, 160, 170), width=1)
    # copper foil rectangle
    d.rectangle([850, 100, 980, 160], fill=(180, 110, 40), outline=(100, 60, 20), width=2)
    d.text((860, 120), "COPPER", fill=(255, 230, 180), font=f_stamp)
    # acetate translucent wash
    d.rectangle([420, 340, 560, 420], fill=(230, 245, 255))
    d.text((430, 370), "ACETATE ghost 77.77", fill=(100, 130, 160), font=f_pen)
    # perforation dash line
    for px in range(70, 520, 10):
        d.line([(px, 290), (px + 5, 290)], fill=(90, 90, 100), width=1)
    # wax seal circle
    d.ellipse([880, 480, 980, 560], fill=(140, 30, 40), outline=(80, 10, 20), width=3)
    d.text((900, 510), "WAX", fill=(255, 220, 220), font=f_stamp)
    # magnet bar
    d.rectangle([100, 500, 220, 545], fill=(30, 30, 80), outline=(10, 10, 40), width=2)
    d.text((115, 512), "MAGNET", fill=(200, 200, 255), font=f_stamp)
    # crepe wavy lines
    for wy in range(470, 560, 8):
        pts = [(x, wy + (3 if (x // 10) % 2 == 0 else -3)) for x in range(250, 400, 8)]
        for i in range(len(pts) - 1):
            d.line([pts[i], pts[i + 1]], fill=(170, 140, 120), width=1)
    # satin glare band
    d.polygon([(60, 14), (400, 14), (390, 28), (70, 28)], fill=(220, 200, 230), outline=(120, 80, 140), width=1)
    d.text((80, 15), "SATIN bait 44.44", fill=(80, 40, 100), font=f_tiny)
    # spiral bind coils left
    for sy in range(80, 480, 50):
        d.arc([0, sy, 36, sy + 36], 270, 90, fill=(60, 60, 70), width=2)
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


THEMES_OLD = "Kraft|Linen|Thermal|Dossier|Chrono|Rubber|Checker|Vellum|Brad|Scroll|Ditto|Flock|Matrix|Axon|Twine|Chamfer|Snap"
THEMES_NEW = "Parchment|Cork|Canvas|Rivet|Holo|Zip|Filament|Honey|Marble|Copper|Acetate|Perf|Waxseal|Magnet|Crepe|Satin|Spiral"
THEMES_OLD_S = "kraft_linen_thermal_dossier_chrono_rubber_checker_vellum_brad_scroll_ditto_flock_matrix_axon_twine_chamfer_snap"
THEMES_NEW_S = "parchment_cork_canvas_rivet_holo_zip_filament_honey_marble_copper_acetate_perf_waxseal_magnet_crepe_satin_spiral"
THEMES_SHORT = "parchment/cork/canvas/rivet/holo/zip/filament/honey/marble/copper/acetate/perf/waxseal/magnet/crepe/satin/spiral"


def xform_train(text: str, train_specs: str) -> str:
    reps = [
        ("C296", "C302"), ("C297", "C303"), ("C298", "C304"),
        ("v32", "v33"), ("V32", "V33"), ("V32H", "V33H"), ("v32h", "v33h"),
        ("vision_v32_c296", "vision_v33_c302"),
        ("VL_GATE_V32_PROTOCOL", "VL_GATE_V33_PROTOCOL"),
        ("vl_gate_v32_claim", "vl_gate_v33_claim"),
        ("vision_gate_v32_claim", "vision_gate_v33_claim"),
        ("r50plus_v32_", "r50plus_v33_"),
        ("SCAN DESK V32", "SCAN DESK V33"),
        ("V32 C296", "V33 C302"),
        ("V32 keeps floor", "V33 keeps floor"),
        ("Vision V32", "Vision V33"),
        ("vision_v32", "vision_v33"),
        ("_v32c296", "_v33c302"),
        ("harder than V31", "harder than V32"),
        ("NEW themes vs V31", "NEW themes vs V32"),
        ("No claim until C297 VL", "No claim until C303 VL"),
        (THEMES_OLD, THEMES_NEW),
        (THEMES_OLD_S, THEMES_NEW_S),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    text = replace_specs(text, train_specs)
    # strip old V32 overlay block if present, then inject V33
    text = re.sub(
        r"\n    # --- V32 overlays \(new vs V31\) ---.*?(?=\n    # soft_affine|\n    img\.save\(buf)",
        "\n",
        text,
        count=1,
        flags=re.S,
    )
    if "V33 overlays" not in text:
        soft = "    # soft_affine"
        if soft in text:
            text = text.replace(soft, V33_OVERLAY + "\n" + soft, 1)
        else:
            text = text.replace("    img.save(buf", V33_OVERLAY + "\n    img.save(buf", 1)
    text = re.sub(
        r"NEW themes vs V3[23]:.*?\nCLARITY FLOOR:",
        "NEW themes vs V32: parchment, cork, canvas, rivet, holo, zip, filament, honey,\n"
        "marble, copper, acetate, perf, waxseal, magnet, crepe, satin, spiral.\n"
        "CLARITY FLOOR:",
        text,
        count=1,
        flags=re.S,
    )
    return text


def xform_smoke(text: str) -> str:
    reps = [
        ("C297", "C303"), ("C296", "C302"),
        ("v32", "v33"), ("V32", "V33"),
        ("vision_images_v32", "vision_images_v33"),
        ("vision_v32_c297", "vision_v33_c303"),
        ("vl_gate_v32_claim", "vl_gate_v33_claim"),
        ("vision_gate_v32_claim", "vision_gate_v33_claim"),
        ("r50plus_v32_", "r50plus_v33_"),
        ("vision_v32_smoke", "vision_v33_smoke"),
        ("C297_VISION_V32", "C303_VISION_V33"),
        ("C297b_VISION_GATE_V32", "C303b_VISION_GATE_V33"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    return text


def xform_heldout(text: str, held_specs: str) -> str:
    reps = [
        ("C298", "C304"), ("C296", "C302"), ("C297", "C303"),
        ("v32h", "v33h"), ("V32H", "V33H"), ("v32", "v33"), ("V32", "V33"),
        ("vision_images_v32h", "vision_images_v33h"),
        ("vision_images_v32", "vision_images_v33"),
        ("vision_v32h_c298", "vision_v33h_c304"),
        ("VL_GATE_V32_HELDOUT_PROTOCOL", "VL_GATE_V33_HELDOUT_PROTOCOL"),
        ("vl_gate_v32_heldout_claim", "vl_gate_v33_heldout_claim"),
        ("vision_gate_v32_heldout_claim", "vision_gate_v33_heldout_claim"),
        ("r50plus_v32_heldout", "r50plus_v33_heldout"),
        ("vision_v32_heldout", "vision_v33_heldout"),
        ("C298_VISION_V32", "C304_VISION_V33"),
        ("C298b_VISION_GATE_V32", "C304b_VISION_GATE_V33"),
        ("SCAN DESK V32H", "SCAN DESK V33H"),
        ("V32H C298", "V33H C304"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    return replace_specs(text, held_specs)


def xform_nv(text: str) -> str:
    """Confidence-gate stretch from C287 -> C305 with fresh case ids."""
    text = text.replace("C287", "C305")
    text = text.replace("conf_gate_stretch_c287", "conf_gate_stretch_c305")
    text = text.replace("C287_CONFIDENCE_GATE_STRETCH.json", "C305_CONFIDENCE_GATE_STRETCH.json")
    text = text.replace("cg30_", "cg33_")
    # bump numbers slightly so cases are fresh
    bumps = [
        ("52.00", "54.00"), ("56.25", "58.50"), ("108.25", "112.50"),
        ("47", "49"), ("22", "24"), ("51", "53"), ("98", "102"),
        ("31.00", "33.00"), ("34.50", "36.75"), ("65.50", "69.75"),
        ("99.00", "101.00"), ("80.00", "82.00"), ("179.00", "183.00"),
        ("1520", "1550"), ("295", "305"), ("1450", "1480"), ("2970", "3030"),
        ("44", "46"), ("23", "25"), ("43", "45"), ("87", "91"),
        ("33", "35"), ("36", "38"), ("45", "47"), ("78", "82"),
        ("75.00", "77.00"), ("78.00", "80.00"), ("153.00", "157.00"),
        ("40.00", "42.00"), ("43.00", "45.00"), ("83.00", "87.00"),
        ("24", "26"), ("12", "14"), ("26", "28"), ("50", "54"),
        ("17.00", "19.00"), ("19.50", "21.25"), ("36.50", "40.25"),
        ("36.00", "38.00"), ("38.25", "40.50"), ("74.25", "78.50"),
        ("999.0", "1001.0"), ("120.0", "124.0"), ("78.5", "82.5"),
        ("219.0", "223.0"), ("3260.0", "3335.0"), ("110.0", "114.0"),
        ("114.0", "118.0"), ("86.25", "90.50"),
    ]
    for a, b in bumps:
        text = text.replace(a, b)
    return text


def xform_reg(text: str) -> str:
    text = text.replace("C300", "C306")
    text = text.replace("C296-C299", "C302-C305")
    text = text.replace("c296_c299", "c302_c305")
    text = text.replace("capture_regression_c300", "capture_regression_c306")
    needle = '("V32_heldout", DOC / "C298_VISION_V32_HELDOUT_SMOKE.json"),'
    insert = (
        needle
        + '\n    ("V33", DOC / "C303_VISION_V33_SMOKE.json"),'
        + '\n    ("V33_heldout", DOC / "C304_VISION_V33_HELDOUT_SMOKE.json"),'
    )
    if needle in text and '("V33"' not in text:
        text = text.replace(needle, insert)
    text = text.replace(
        '("C299_product_u2c_cost", DOC / "C299_PRODUCT_U2C_COST.json"),',
        '("C299_product_u2c_cost", DOC / "C299_PRODUCT_U2C_COST.json"),\n'
        '    ("C305_confidence_gate_stretch", DOC / "C305_CONFIDENCE_GATE_STRETCH.json"),',
    )
    text = text.replace(
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "V31", "V31_heldout", "V32", "V32_heldout", "C233_clarity_floor", "C299_product_u2c_cost"]',
        'required = ["V25", "V25_heldout", "V26", "V26_heldout", "V27", "V27_heldout", "V28", "V28_heldout", "V29", "V29_heldout", "V30", "V30_heldout", "V31", "V31_heldout", "V32", "V32_heldout", "V33", "V33_heldout", "C233_clarity_floor", "C305_confidence_gate_stretch"]',
    )
    text = text.replace('DOC / "C300_CAPTURE_OFFICE_REGRESSION.json"', 'DOC / "C306_CAPTURE_OFFICE_REGRESSION.json"')
    return text


def xform_score(text: str) -> str:
    text = text.replace("C301", "C307")
    text = text.replace("c296_c300", "c302_c306")
    text = text.replace("STAGE_ANT_C301.md", "STAGE_ANT_C307.md")
    text = text.replace("C296-C300", "C302-C306")
    text = text.replace("C296-C301", "C302-C307")
    text = text.replace("unified_scorecard_c296_c300", "unified_scorecard_c302_c306")

    hist_inject = '''    c297v = load("docs/r50/C297_VISION_V32_SMOKE.json") or {}
    c297vb = load("docs/r50/C297b_VISION_GATE_V32_CLAIM.json") or {}
    c298v = load("docs/r50/C298_VISION_V32_HELDOUT_SMOKE.json") or {}
    c298vb = load("docs/r50/C298b_VISION_GATE_V32_HELDOUT_CLAIM.json") or {}
    c291v = load("docs/r50/C291_VISION_V31_SMOKE.json") or {}
    c291vb = load("docs/r50/C291b_VISION_GATE_V31_CLAIM.json") or {}
    c292v = load("docs/r50/C292_VISION_V31_HELDOUT_SMOKE.json") or {}
    c292vb = load("docs/r50/C292b_VISION_GATE_V31_HELDOUT_CLAIM.json") or {}
    c266 = load("docs/r50/C302_VISION_V33_DESIGN.json") or {}
    c267 = load("docs/r50/C303_VISION_V33_SMOKE.json") or {}
    c267b = load("docs/r50/C303b_VISION_GATE_V33_CLAIM.json") or {}
    c268 = load("docs/r50/C304_VISION_V33_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C304b_VISION_GATE_V33_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C306_CAPTURE_OFFICE_REGRESSION.json") or {}'''

    old_block = '''    c291v = load("docs/r50/C291_VISION_V31_SMOKE.json") or {}
    c291vb = load("docs/r50/C291b_VISION_GATE_V31_CLAIM.json") or {}
    c292v = load("docs/r50/C292_VISION_V31_HELDOUT_SMOKE.json") or {}
    c292vb = load("docs/r50/C292b_VISION_GATE_V31_HELDOUT_CLAIM.json") or {}
    c266 = load("docs/r50/C296_VISION_V32_DESIGN.json") or {}
    c267 = load("docs/r50/C297_VISION_V32_SMOKE.json") or {}
    c267b = load("docs/r50/C297b_VISION_GATE_V32_CLAIM.json") or {}
    c268 = load("docs/r50/C298_VISION_V32_HELDOUT_SMOKE.json") or {}
    c268b = load("docs/r50/C298b_VISION_GATE_V32_HELDOUT_CLAIM.json") or {}
    c270 = load("docs/r50/C300_CAPTURE_OFFICE_REGRESSION.json") or {}'''
    if old_block in text:
        text = text.replace(old_block, hist_inject)

    text = text.replace(
        'c269 = load("docs/r50/C299_PRODUCT_U2C_COST.json") or {}\n'
        '    c293 = load("docs/r50/C293_DISSOLVE_COST_SHADOW.json") or {}\n'
        '    c287 = load("docs/r50/C287_CONFIDENCE_GATE_STRETCH.json") or {}',
        'c269 = load("docs/r50/C305_CONFIDENCE_GATE_STRETCH.json") or {}\n'
        '    c299 = load("docs/r50/C299_PRODUCT_U2C_COST.json") or {}\n'
        '    c293 = load("docs/r50/C293_DISSOLVE_COST_SHADOW.json") or {}\n'
        '    c287 = load("docs/r50/C287_CONFIDENCE_GATE_STRETCH.json") or {}',
    )

    text = text.replace(
        '''    v31 = float(c291v.get("rate") or 0.0)
    v31h = float(c292v.get("rate") or 0.0)
    v32 = float(c267.get("rate") or 0.0)
    v32h = float(c268.get("rate") or 0.0)''',
        '''    v31 = float(c291v.get("rate") or 0.0)
    v31h = float(c292v.get("rate") or 0.0)
    v32 = float(c297v.get("rate") or 0.0)
    v32h = float(c298v.get("rate") or 0.0)
    v33 = float(c267.get("rate") or 0.0)
    v33h = float(c268.get("rate") or 0.0)''',
    )
    text = text.replace(
        '''    v31_claim = bool(c291vb.get("vl_gate_v31_claim") or c291v.get("vl_gate_v31_claim") or c291v.get("claim"))
    v31h_claim = bool(c292vb.get("vl_gate_v31_heldout_claim") or c292v.get("vl_gate_v31_heldout_claim") or c292v.get("claim"))
    v32_claim = bool(c267b.get("vl_gate_v32_claim") or c267.get("vl_gate_v32_claim") or c267.get("claim"))
    v32h_claim = bool(c268b.get("vl_gate_v32_heldout_claim") or c268.get("vl_gate_v32_heldout_claim") or c268.get("claim"))''',
        '''    v31_claim = bool(c291vb.get("vl_gate_v31_claim") or c291v.get("vl_gate_v31_claim") or c291v.get("claim"))
    v31h_claim = bool(c292vb.get("vl_gate_v31_heldout_claim") or c292v.get("vl_gate_v31_heldout_claim") or c292v.get("claim"))
    v32_claim = bool(c297vb.get("vl_gate_v32_claim") or c297v.get("vl_gate_v32_claim") or c297v.get("claim"))
    v32h_claim = bool(c298vb.get("vl_gate_v32_heldout_claim") or c298v.get("vl_gate_v32_heldout_claim") or c298v.get("claim"))
    v33_claim = bool(c267b.get("vl_gate_v33_claim") or c267.get("vl_gate_v33_claim") or c267.get("claim"))
    v33h_claim = bool(c268b.get("vl_gate_v33_heldout_claim") or c268.get("vl_gate_v33_heldout_claim") or c268.get("claim"))''',
    )

    # NV: primary is C305 confidence gate
    text = text.replace(
        '''    dissolve_pass = bool((c293.get("dissolve") or c263.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c293.get("shadow") or c263.get("shadow") or {}).get("pass", True))
    nv_pass = bool(c269.get("pass"))
    conf_pass = bool(c287.get("pass"))
    conf_rate = float(c287.get("rate") or 0.0)
    u2c_rate = float((c269.get("u2c") or {}).get("rate") or c269.get("rate") or 0.0)
    dissolve_rate = float(((c293.get("dissolve") or {}).get("summary") or {}).get("n_families") or 4)''',
        '''    dissolve_pass = bool((c293.get("dissolve") or c263.get("dissolve") or {}).get("pass", True))
    shadow_pass = bool((c293.get("shadow") or c263.get("shadow") or {}).get("pass", True))
    nv_pass = bool(c269.get("pass"))
    conf_pass = bool(c269.get("pass") or c287.get("pass"))
    conf_rate = float(c269.get("rate") or c287.get("rate") or 0.0)
    u2c_rate = float((c299.get("u2c") or {}).get("rate") or c299.get("rate") or 0.0)
    dissolve_rate = float(((c293.get("dissolve") or {}).get("summary") or {}).get("n_families") or 4)''',
    )

    text = text.replace(
        'rl = ((c269.get("replace_ledger") or {}) or (c293.get("replace_stress") or {}) or (c281.get("replace_ledger") or {}) or {})',
        'rl = ((c299.get("replace_ledger") or {}) or (c293.get("replace_stress") or {}) or (c269.get("replace_ledger") or {}) or {})',
    )
    text = text.replace(
        '"source": "C299" if (c269.get("replace_ledger") or {}).get("mean_ratio") is not None else ("C293" if (c293.get("replace_stress") or {}).get("mean_ratio") is not None else "C263")',
        '"source": "C299" if (c299.get("replace_ledger") or {}).get("mean_ratio") is not None else ("C293" if (c293.get("replace_stress") or {}).get("mean_ratio") is not None else "C263")',
    )

    text = text.replace(
        '''        max(v32, v32h, 0.0),
        1.0 if v32_claim else 0.0,
        1.0 if v32h_claim else 0.0,''',
        '''        max(v32, v32h, 0.0),
        1.0 if v32_claim else 0.0,
        1.0 if v32h_claim else 0.0,
        max(v33, v33h, 0.0),
        1.0 if v33_claim else 0.0,
        1.0 if v33h_claim else 0.0,''',
    )
    text = text.replace(
        "v32_claim and v32h_claim and capture_pass and nv_pass",
        "v33_claim and v33h_claim and capture_pass and nv_pass",
    )

    text = text.replace(
        '''            "v32_design": {"n": c266.get("n"), "clarity_floor": c266.get("clarity_floor"), "claim": False},
            "v32_smoke": {
                "rate": v32, "n": c267.get("n"), "n_ok": c267.get("n_ok"),
                "claim": v32_claim, "fail_ids": c267.get("fail_ids"),
            },
            "v32_heldout": {
                "rate": v32h, "n": c268.get("n"), "n_ok": c268.get("n_ok"),
                "claim": v32h_claim, "fail_ids": c268.get("fail_ids"),
                "id_disjoint": c268.get("id_disjoint"),
            },''',
        '''            "v32_smoke": {"rate": v32, "claim": v32_claim},
            "v32_heldout": {"rate": v32h, "claim": v32h_claim},
            "v33_design": {"n": c266.get("n"), "clarity_floor": c266.get("clarity_floor"), "claim": False},
            "v33_smoke": {
                "rate": v33, "n": c267.get("n"), "n_ok": c267.get("n_ok"),
                "claim": v33_claim, "fail_ids": c267.get("fail_ids"),
            },
            "v33_heldout": {
                "rate": v33h, "n": c268.get("n"), "n_ok": c268.get("n_ok"),
                "claim": v33h_claim, "fail_ids": c268.get("fail_ids"),
                "id_disjoint": c268.get("id_disjoint"),
            },''',
    )

    text = text.replace(
        '''            "product_u2c_cost": {"pass": nv_pass, "rate": u2c_rate},
            "dissolve_cost_shadow": {"pass": bool(c293.get("pass")), "dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass},
            "confidence_gate_stretch": {"pass": conf_pass, "rate": conf_rate},
            "replace_ratio": replace.get("mean_ratio"),''',
        '''            "confidence_gate_stretch": {"pass": conf_pass, "rate": conf_rate, "source": "C305"},
            "product_u2c_cost": {"pass": bool(c299.get("pass")), "rate": u2c_rate},
            "dissolve_cost_shadow": {"pass": bool(c293.get("pass")), "dissolve_pass": dissolve_pass, "shadow_pass": shadow_pass},
            "replace_ratio": replace.get("mean_ratio"),''',
    )

    text = text.replace(
        "| V32 smoke / heldout | **{v32} / {v32h}** claim={v32_claim}/{v32h_claim} |\n"
        "| product/U2C (C299) | pass={nv_pass} rate={u2c_rate} |\n"
        "| dissolve/shadow (C293) | dissolve={dissolve_pass} shadow={shadow_pass} |\n"
        "| confidence-gate stretch (C287) | pass={conf_pass} rate={conf_rate} |",
        "| V32 smoke / heldout | **{v32} / {v32h}** claim={v32_claim}/{v32h_claim} |\n"
        "| V33 smoke / heldout | **{v33} / {v33h}** claim={v33_claim}/{v33h_claim} |\n"
        "| confidence-gate (C305) | pass={nv_pass} rate={conf_rate} |\n"
        "| product/U2C (C299) | pass={bool(c299.get('pass'))} rate={u2c_rate} |\n"
        "| dissolve/shadow (C293) | dissolve={dissolve_pass} shadow={shadow_pass} |",
    )
    text = text.replace(
        '''| C296 | V32 design | n={c266.get('n')} kraft/linen/thermal/dossier/... |
| C297 | V32 smoke | rate={v32} claim={v32_claim} |
| C298 | V32 heldout | rate={v32h} claim={v32h_claim} |
| C299 | product/U2C | pass={nv_pass} rate={u2c_rate} |
| C300 | capture regression | pass={capture_pass} |
| C301 | scorecard | composite={composite} |''',
        '''| C302 | V33 design | n={c266.get('n')} parchment/cork/canvas/rivet/... |
| C303 | V33 smoke | rate={v33} claim={v33_claim} |
| C304 | V33 heldout | rate={v33h} claim={v33h_claim} |
| C305 | confidence-gate | pass={nv_pass} rate={conf_rate} |
| C306 | capture regression | pass={capture_pass} |
| C307 | scorecard | composite={composite} |''',
    )
    text = text.replace(
        "- V32: claim={v32_claim} rate={v32}\n- V32 heldout: claim={v32h_claim} rate={v32h}",
        "- V32: claim={v32_claim} rate={v32}\n- V32 heldout: claim={v32h_claim} rate={v32h}\n"
        "- V33: claim={v33_claim} rate={v33}\n- V33 heldout: claim={v33h_claim} rate={v33h}",
    )
    text = text.replace(
        "Stage: C296-C301; V32 CLAIM {v32}; V32 heldout CLAIM {v32h}",
        "Stage: C302-C307; V33 CLAIM {v33}; V33 heldout CLAIM {v33h}",
    )
    text = text.replace(
        "V32 design: clarity_floor jpeg_q=60 photo/=2 themes=kraft/linen/thermal/dossier/chrono/rubber/checker/vellum/brad/scroll/ditto/flock/matrix/axon/twine/chamfer/snap",
        f"V33 design: clarity_floor jpeg_q=60 photo/=2 themes={THEMES_SHORT}",
    )
    text = text.replace(
        "V32 smoke: rate={v32} n={c267.get('n')} CLAIM={v32_claim} fail={c267.get('fail_ids')}",
        "V33 smoke: rate={v33} n={c267.get('n')} CLAIM={v33_claim} fail={c267.get('fail_ids')}",
    )
    text = text.replace(
        "V32 heldout: rate={v32h} n={c268.get('n')} CLAIM={v32h_claim} disjoint={c268.get('id_disjoint')}",
        "V33 heldout: rate={v33h} n={c268.get('n')} CLAIM={v33h_claim} disjoint={c268.get('id_disjoint')}",
    )
    text = text.replace(
        "Non-vision C299: pass={nv_pass} rate={u2c_rate} (product/U2C); dissolve C293={dissolve_pass}/{shadow_pass}; conf-gate C287={conf_pass}/{conf_rate}; replace_ratio={replace.get('mean_ratio')}",
        "Non-vision C305: pass={nv_pass} rate={conf_rate} (confidence-gate); product C299={bool(c299.get('pass'))}/{u2c_rate}; dissolve C293={dissolve_pass}/{shadow_pass}; replace_ratio={replace.get('mean_ratio')}",
    )
    text = text.replace("Capture regression: pass={capture_pass} (C300)", "Capture regression: pass={capture_pass} (C306)")
    text = text.replace("Scorecard composite: {composite} (C301)", "Scorecard composite: {composite} (C307)")
    text = text.replace(
        'f.write(f"- V32 smoke={v32} claim={v32_claim}; heldout={v32h} claim={v32h_claim}\\n")',
        'f.write(f"- V33 smoke={v33} claim={v33_claim}; heldout={v33h} claim={v33h_claim}\\n")',
    )
    text = text.replace(
        'f.write(f"- C299 product/U2C pass={nv_pass} rate={u2c_rate}; conf-gate={conf_pass}/{conf_rate}; replace',
        'f.write(f"- C305 conf-gate pass={nv_pass} rate={conf_rate}; product C299={u2c_rate}; replace',
    )
    return text


def main():
    specs = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    train_specs = specs_to_py(specs["train"])
    held_specs = specs_to_py(specs["held"])
    mapping = [
        ("c296_vision_v32_design_and_batch.py", "c302_vision_v33_design_and_batch.py",
         lambda t: xform_train(t, train_specs)),
        ("c297_vision_v32_smoke.py", "c303_vision_v33_smoke.py", xform_smoke),
        ("c298_vision_v32_heldout.py", "c304_vision_v33_heldout.py",
         lambda t: xform_heldout(t, held_specs)),
        ("c287_confidence_gate_stretch.py", "c305_confidence_gate_stretch.py", xform_nv),
        ("c300_capture_office_regression.py", "c306_capture_office_regression.py", xform_reg),
        ("c301_scorecard_and_stage.py", "c307_scorecard_and_stage.py", xform_score),
    ]
    for src, dst, fn in mapping:
        t = (SCR / src).read_text(encoding="utf-8")
        out = fn(t)
        (SCR / dst).write_text(out, encoding="utf-8")
        print("wrote", dst, "bytes", len(out.encode("utf-8")))
    d = (SCR / "c302_vision_v33_design_and_batch.py").read_text(encoding="utf-8")
    assert "vision_images_v33" in d and "v33_01" in d
    assert "V33 overlays" in d
    assert "parchment_recv" in d
    assert "JPEG_Q = 60" in d
    assert "kraft_recv" not in d
    s = (SCR / "c307_scorecard_and_stage.py").read_text(encoding="utf-8")
    assert "STAGE_ANT_C307.md" in s
    assert "C303_VISION_V33_SMOKE" in s
    assert "v33_claim" in s
    assert "C305_CONFIDENCE_GATE_STRETCH" in s
    nv = (SCR / "c305_confidence_gate_stretch.py").read_text(encoding="utf-8")
    assert "C305" in nv and "cg33_" in nv
    print("ok")


if __name__ == "__main__":
    main()
