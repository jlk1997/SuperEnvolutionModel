# -*- coding: utf-8 -*-
from pathlib import Path
import re

P = Path("tools/_boot_v34_c308.py")
t = P.read_text(encoding="utf-8")

# Fix remaining V33_OVERLAY refs
t = t.replace("V33_OVERLAY", "V34_OVERLAY")
t = t.replace("V33 overlays", "V34 overlays")

# xform_train cycle/version mapping: currently C296->C302 etc; rewrite to C302->C308
# Replace the reps list content carefully by rewriting the whole xform_train function's reps

old_train_reps = '''    reps = [
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
    ]'''

new_train_reps = '''    reps = [
        ("C302", "C308"), ("C303", "C309"), ("C304", "C310"),
        ("v33", "v34"), ("V33", "V34"), ("V33H", "V34H"), ("v33h", "v34h"),
        ("vision_v33_c302", "vision_v34_c308"),
        ("VL_GATE_V33_PROTOCOL", "VL_GATE_V34_PROTOCOL"),
        ("vl_gate_v33_claim", "vl_gate_v34_claim"),
        ("vision_gate_v33_claim", "vision_gate_v34_claim"),
        ("r50plus_v33_", "r50plus_v34_"),
        ("SCAN DESK V33", "SCAN DESK V34"),
        ("V33 C302", "V34 C308"),
        ("V33 keeps floor", "V34 keeps floor"),
        ("Vision V33", "Vision V34"),
        ("vision_v33", "vision_v34"),
        ("_v33c302", "_v34c308"),
        ("harder than V32", "harder than V33"),
        ("NEW themes vs V32", "NEW themes vs V33"),
        ("No claim until C303 VL", "No claim until C309 VL"),
        (THEMES_OLD, THEMES_NEW),
        (THEMES_OLD_S, THEMES_NEW_S),
    ]'''

if old_train_reps not in t:
    raise SystemExit("train reps not found")
t = t.replace(old_train_reps, new_train_reps)

# strip overlay regex and inject
t = t.replace(
    r'r"\n    # --- V32 overlays \(new vs V31\) ---.*?(?=\n    # soft_affine|\n    img\.save\(buf)"',
    r'r"\n    # --- V33 overlays \(new vs V32\) ---.*?(?=\n    # soft_affine|\n    img\.save\(buf)"',
)
# after V33->V34 global replace above, the strip pattern may already say V34; fix strip to look for V33 in SOURCE scripts
# Actually xform_train runs on V33 source which has V33 overlays; after version replace V33->V34 the overlay rename happens.
# Strip should remove V33 overlays from source before inject. Source has "# --- V33 overlays (new vs V32) ---"
# After our global V33_OVERLAY->V34_OVERLAY and "V33 overlays"->"V34 overlays" in BOOT file only,
# the regex in boot that strips from TARGET text still needs to match V33 in the source script being transformed.
t = t.replace(
    r'r"\n    # --- V34 overlays \(new vs V33\) ---.*?(?=\n    # soft_affine|\n    img\.save\(buf)"',
    r'r"\n    # --- V33 overlays \(new vs V32\) ---.*?(?=\n    # soft_affine|\n    img\.save\(buf)"',
)
# Also if still V32 pattern:
t = t.replace(
    'r"\\n    # --- V32 overlays \\(new vs V31\\) ---.*?(?=\\n    # soft_affine|\\n    img\\.save\\(buf)"',
    'r"\\n    # --- V33 overlays \\(new vs V32\\) ---.*?(?=\\n    # soft_affine|\\n    img\\.save\\(buf)"',
)

t = t.replace('if "V34 overlays" not in text:', 'if "V34 overlays" not in text:')  # noop keep
t = t.replace("V34_OVERLAY +", "V34_OVERLAY +")

# docstring themes re.sub
t = re.sub(
    r're\.sub\(\s*r"NEW themes vs V3\[23\]:.*?CLARITY FLOOR:",\s*"NEW themes vs V32:.*?"CLARITY FLOOR:",',
    '''re.sub(
        r"NEW themes vs V3[34]:.*?\\nCLARITY FLOOR:",
        "NEW themes vs V33: bamboo, slate, denim, brass, prism, latch, amber, quarry,\\n"
        "tin, mylar, felt, stitch, enamel, cord, rice, chrome, index.\\n"
        "CLARITY FLOOR:",''',
    t,
    count=1,
    flags=re.S,
)

# Simpler: find the re.sub block for themes
old_theme_doc = '''    text = re.sub(
        r"NEW themes vs V3[23]:.*?\\nCLARITY FLOOR:",
        "NEW themes vs V32: parchment, cork, canvas, rivet, holo, zip, filament, honey,\\n"
        "marble, copper, acetate, perf, waxseal, magnet, crepe, satin, spiral.\\n"
        "CLARITY FLOOR:",
        text,
        count=1,
        flags=re.S,
    )'''
new_theme_doc = '''    text = re.sub(
        r"NEW themes vs V3[34]:.*?\\nCLARITY FLOOR:",
        "NEW themes vs V33: bamboo, slate, denim, brass, prism, latch, amber, quarry,\\n"
        "tin, mylar, felt, stitch, enamel, cord, rice, chrome, index.\\n"
        "CLARITY FLOOR:",
        text,
        count=1,
        flags=re.S,
    )'''
# After earlier V33 overlays rename, parchment block may still be there
if old_theme_doc in t:
    t = t.replace(old_theme_doc, new_theme_doc)
else:
    # try already-partially-modified
    m = re.search(r'    text = re\.sub\(\n        r"NEW themes vs V3.*?flags=re\.S,\n    \)', t, re.S)
    if m:
        t = t[:m.start()] + new_theme_doc + t[m.end():]
        print("theme doc replaced via regex")
    else:
        print("WARN theme doc not found")

P.write_text(t, encoding="utf-8")
print("phase2a ok")
