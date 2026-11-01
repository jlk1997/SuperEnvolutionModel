# -*- coding: utf-8 -*-
from pathlib import Path
import re

P = Path("tools/_boot_v34_c308.py")
t = P.read_text(encoding="utf-8")

old_smoke = '''def xform_smoke(text: str) -> str:
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
    return text'''

new_smoke = '''def xform_smoke(text: str) -> str:
    reps = [
        ("C303", "C309"), ("C302", "C308"),
        ("v33", "v34"), ("V33", "V34"),
        ("vision_images_v33", "vision_images_v34"),
        ("vision_v33_c303", "vision_v34_c309"),
        ("vl_gate_v33_claim", "vl_gate_v34_claim"),
        ("vision_gate_v33_claim", "vision_gate_v34_claim"),
        ("r50plus_v33_", "r50plus_v34_"),
        ("vision_v33_smoke", "vision_v34_smoke"),
        ("C303_VISION_V33", "C309_VISION_V34"),
        ("C303b_VISION_GATE_V33", "C309b_VISION_GATE_V34"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    return text'''

if old_smoke not in t:
    raise SystemExit("smoke not found")
t = t.replace(old_smoke, new_smoke)

old_held = '''def xform_heldout(text: str, held_specs: str) -> str:
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
    return replace_specs(text, held_specs)'''

new_held = '''def xform_heldout(text: str, held_specs: str) -> str:
    reps = [
        ("C304", "C310"), ("C302", "C308"), ("C303", "C309"),
        ("v33h", "v34h"), ("V33H", "V34H"), ("v33", "v34"), ("V33", "V34"),
        ("vision_images_v33h", "vision_images_v34h"),
        ("vision_images_v33", "vision_images_v34"),
        ("vision_v33h_c304", "vision_v34h_c310"),
        ("VL_GATE_V33_HELDOUT_PROTOCOL", "VL_GATE_V34_HELDOUT_PROTOCOL"),
        ("vl_gate_v33_heldout_claim", "vl_gate_v34_heldout_claim"),
        ("vision_gate_v33_heldout_claim", "vision_gate_v34_heldout_claim"),
        ("r50plus_v33_heldout", "r50plus_v34_heldout"),
        ("vision_v33_heldout", "vision_v34_heldout"),
        ("C304_VISION_V33", "C310_VISION_V34"),
        ("C304b_VISION_GATE_V33", "C310b_VISION_GATE_V34"),
        ("SCAN DESK V33H", "SCAN DESK V34H"),
        ("V33H C304", "V34H C310"),
    ]
    for a, b in reps:
        text = text.replace(a, b)
    return replace_specs(text, held_specs)'''

if old_held not in t:
    raise SystemExit("held not found")
t = t.replace(old_held, new_held)

# Replace entire xform_nv with dissolve version
old_nv_start = t.find('def xform_nv(text: str) -> str:')
old_reg_start = t.find('def xform_reg(text: str) -> str:')
if old_nv_start < 0 or old_reg_start < 0:
    raise SystemExit("nv/reg markers missing")

new_nv = '''def xform_nv(text: str) -> str:
    """Dissolve/shadow refresh C293 -> C311."""
    text = text.replace("C293", "C311")
    text = text.replace("dissolve_cost_shadow_c293", "dissolve_cost_shadow_c311")
    text = text.replace("DISSOLVE_DASHBOARD_C293", "DISSOLVE_DASHBOARD_C311")
    text = text.replace("C293_DISSOLVE_COST_SHADOW.json", "C311_DISSOLVE_COST_SHADOW.json")
    text = text.replace('"bare_steps": 4, "agent_steps": 16', '"bare_steps": 4, "agent_steps": 17')
    text = text.replace('"bare_steps": 3, "agent_steps": 13', '"bare_steps": 3, "agent_steps": 14', 1)
    text = text.replace('"bare_steps": 5, "agent_steps": 19', '"bare_steps": 5, "agent_steps": 20')
    text = text.replace('"bare_steps": 2, "agent_steps": 10', '"bare_steps": 2, "agent_steps": 11')
    text = text.replace('"bare_steps": 3, "agent_steps": 14', '"bare_steps": 3, "agent_steps": 15', 1)
    text = text.replace('"bare_steps": 3, "agent_steps": 12', '"bare_steps": 3, "agent_steps": 13')
    return text


'''
t = t[:old_nv_start] + new_nv + t[old_reg_start:]

P.write_text(t, encoding="utf-8")
print("phase2b smoke/held/nv ok")
