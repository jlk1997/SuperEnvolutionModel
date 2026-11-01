from pathlib import Path

# heldout claim/scope/footer fixes
p = Path("scripts/c348_vision_v40_heldout.py")
t = p.read_text(encoding="utf-8")
t = t.replace("V39H C341 clarity floor", "V40H C348 clarity floor")
t = t.replace("r50plus_v39_heldout_hlx_magclip_n>=16_qwen35_2b_clarity_floor",
              "r50plus_v40_heldout_teak_onyx_n>=16_qwen35_2b_clarity_floor")
t = t.replace("vision_gate_v39_heldout_claim", "vision_gate_v40_heldout_claim")
t = t.replace("vl_gate_v39_heldout_claim", "vl_gate_v40_heldout_claim")
# ensure theme names ok
p.write_text(t, encoding="utf-8")
print("heldout fixed")

# regression: add V40 pointers + required
p = Path("scripts/c350_capture_office_regression.py")
t = p.read_text(encoding="utf-8")
if '("V40"' not in t:
    needle = '    ("V39_heldout", DOC / "C341_VISION_V39_HELDOUT_SMOKE.json"),'
    insert = needle + '\n    ("V40", DOC / "C347_VISION_V40_SMOKE.json"),\n    ("V40_heldout", DOC / "C348_VISION_V40_HELDOUT_SMOKE.json"),'
    if needle in t:
        t = t.replace(needle, insert, 1)
        print("inserted V40 pointers")
    else:
        print("WARN: V39_heldout needle missing")
# extend required list if present
import re
m = re.search(r'required\s*=\s*\[(.*?)\]', t, re.S)
if m and '"V40"' not in m.group(0) and "'V40'" not in m.group(0):
    old = m.group(0)
    # append before closing
    new = old[:-1] + ', "V39", "V39_heldout", "V40", "V40_heldout"]'
    # avoid dup if V39 already there
    if '"V39"' in old:
        new = old[:-1] + ', "V40", "V40_heldout"]'
    t = t.replace(old, new, 1)
    print("extended required")
else:
    print("required ok or missing", bool(m))
p.write_text(t, encoding="utf-8")

# design: verify V40 overlay once only
p = Path("scripts/c346_vision_v40_design_and_batch.py")
t = p.read_text(encoding="utf-8")
print("V40 overlay count", t.count("# --- V40 overlays (new vs V39) ---"))
print("teak_recv count", t.count("teak_recv"))
