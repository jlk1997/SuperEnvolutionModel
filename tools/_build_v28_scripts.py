# -*- coding: utf-8 -*-
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
SCR = ROOT / "scripts"
specs = json.loads((ROOT / "tools/_v28_specs.json").read_text(encoding="utf-8"))

def fmt_specs(rows):
    lines = ["SPECS = ["]
    for fid, kind, metric, expected, lns, cn, stamp in rows:
        lines.append(f'    ("{fid}", "{kind}", "{metric}", {expected},')
        lines.append(f"     {json.dumps(lns, ensure_ascii=False)},")
        lines.append(f"     {json.dumps(cn, ensure_ascii=False)}, {json.dumps(stamp, ensure_ascii=False)}),")
    lines.append("]")
    return "\n".join(lines) + "\n"

V28_OVERLAY = r'''
    # --- V28 overlays (new vs V27) ---
    # rust clip corner (top-right of card)
    d.rectangle([500, 22, 545, 60], fill=(120, 70, 40), outline=(60, 30, 10), width=2)
    d.ellipse([508, 18, 538, 38], fill=(140, 80, 45))
    for (rx, ry) in [(505, 50), (520, 55), (535, 48)]:
        d.ellipse([rx - 4, ry - 3, rx + 4, ry + 3], fill=(90, 50, 25))
    # wet smudge band below text band
    d.ellipse([100, 250, 220, 290], fill=(175, 185, 195))
    d.ellipse([300, 255, 400, 288], fill=(180, 190, 200))
    # hole punch triplet left margin
    for hy in (90, 160, 230):
        d.ellipse([22, hy, 42, hy + 20], fill=(210, 206, 196), outline=(40, 40, 40), width=2)
        d.ellipse([26, hy + 4, 38, hy + 16], fill=(180, 176, 166))
    # rubber band slant across lower card
    d.line([(70, 520), (520, 560)], fill=(40, 40, 50), width=5)
    d.line([(72, 524), (522, 564)], fill=(90, 90, 100), width=2)
    # desk glare wash (upper-right outside text)
    d.rectangle([400, 30, 560, 120], fill=(255, 255, 240))
    d.text((410, 60), "GLARE wash", fill=(200, 200, 180), font=f_tiny)
    # label overlap strip
    d.rectangle([780, 130, 1060, 190], fill=(255, 255, 200), outline=(0, 0, 0), width=2)
    d.text((790, 140), "OVERLAP LABEL bait 321.00", fill=(0, 0, 0), font=f_fax)
    d.text((790, 165), "DO NOT SCAN", fill=(120, 40, 40), font=f_fax)
    # fountain ink blot
    for (cx, cy, r) in [(180, 480, 36), (420, 510, 28)]:
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=(30, 30, 80))
        d.ellipse([cx - r // 2, cy - r // 3, cx + r // 2, cy + r // 3], fill=(20, 20, 60))
    # paperclip chain top-left
    for i, cx in enumerate([70, 95, 120]):
        d.ellipse([cx, 8, cx + 22, 36], outline=(80, 80, 100), width=2)
        d.ellipse([cx + 4, 12, cx + 18, 32], outline=(80, 80, 100), width=1)
    # fax noise horizontal lines (right panel)
    for yy in range(200, 450, 5):
        d.line([(760, yy), (1060, yy)], fill=(160, 160, 180), width=1)
    d.text((770, 460), "FAX NOISE bait 77.77", fill=(40, 40, 120), font=f_tiny)
    # sticky tab right of card
    d.polygon([(560, 200), (590, 200), (590, 250), (560, 240)], fill=(255, 180, 60), outline=(180, 100, 20), width=1)
    d.text((562, 215), "TAB", fill=(80, 40, 0), font=f_tiny)
    # crease X fold (below text band)
    d.line([(80, 320), (500, 480)], fill=(100, 100, 110), width=2)
    d.line([(500, 320), (80, 480)], fill=(100, 100, 110), width=2)
    # stamp over-ink smear near stamps zone
    d.ellipse([350, 500, 450, 560], fill=(160, 40, 40))
    d.text((365, 520), "OVER", fill=(255, 220, 220), font=f_stamp)
    # tape residue rectangle
    d.rectangle([90, 300, 280, 330], fill=(245, 240, 230), outline=(200, 190, 160), width=1)
    d.text((100, 308), "TAPE RES bait 12.12", fill=(140, 100, 60), font=f_tiny)
    # pencil shade margin
    for i in range(16):
        d.line([(4, 100 + i * 28), (28, 118 + i * 28)], fill=(70, 70, 80), width=2)
    # coffee ring center (below text)
    for (cx, cy, r) in [(280, 400, 55), (280, 400, 48)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(150, 100, 60), width=3)
    d.text((250, 395), "RING bait 33.33", fill=(120, 80, 40), font=f_tiny)
'''

HARDENING = '''        "hardening": [
            "rust_clip", "wet_smudge", "hole_punch", "rubber_band_slant",
            "desk_glare", "label_overlap", "fountain_blot", "paperclip_chain",
            "fax_noise", "sticky_tab", "crease_x", "stamp_overink",
            "tape_residue", "pencil_shade", "coffee_ring_center",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c272_clarity_floor",
        ],'''

THEME = "rust_wet_hole_band_glare_label_blot_clip_fax_tab_crease_overink_tape_shade_ring"
BANNER = "Rust|Wet|Hole|Band|Glare|Label|Blot|Clip|Fax|Tab|Crease|Overink|Tape|Shade|Ring"
PURPOSE = (
    "Harder than V27: rust clip, wet smudge, hole punch, rubber band slant,\n"
    "desk glare, label overlap, fountain blot, paperclip chain,\n"
    "fax noise, sticky tab, crease X, stamp over-ink,\n"
    "tape residue, pencil shade, coffee ring center.\n"
)

def swap_specs(text, new_specs):
    m = re.search(r"SPECS = \[.*?\]\n\n", text, re.S)
    if not m:
        m = re.search(r"SPECS = \[.*?\]\n", text, re.S)
    if not m:
        raise SystemExit("SPECS not found")
    return text[: m.start()] + new_specs + "\n" + text[m.end() :]

def inject_overlay(text):
    markers = [
        "    # --- V27 overlays (new vs V26) ---",
        "    # --- V28 overlays (new vs V27) ---",
        "    # --- V26 overlays (new vs V25) ---",
    ]
    end_markers = [
        "    # fingerprint ovals",
        "    # rain streaks",
        "    # stamps",
        "    for i in range(4):",
        "    # staple shadow top-left",
    ]
    start = -1
    for marker in markers:
        start = text.find(marker)
        if start >= 0:
            break
    if start < 0:
        for em in end_markers:
            p = text.find(em)
            if p >= 0:
                return text[:p] + V28_OVERLAY + "\n" + text[p:]
        raise SystemExit("no overlay injection point")
    end = -1
    for em in end_markers:
        p = text.find(em, start + 10)
        if p != -1 and (end == -1 or p < end):
            end = p
    if end == -1:
        raise SystemExit("cannot find end of prior overlay")
    return text[:start] + V28_OVERLAY + "\n" + text[end:]

def replace_hardening(text):
    m = re.search(r'"hardening":\s*\[.*?\],', text, re.S)
    if not m:
        raise SystemExit("hardening not found")
    return text[: m.start()] + HARDENING.strip() + text[m.end() :]

# C272
src = (SCR / "c266_vision_v27_design_and_batch.py").read_text(encoding="utf-8")
out = src
out = out.replace("C266", "C272").replace("c266", "c272")
out = out.replace("V27", "V28").replace("v27", "v28")
out = out.replace("harder than V28", "harder than V27")
out = out.replace("NEW themes vs V28", "NEW themes vs V27")
out = out.replace("vs V28", "vs V27")
out = out.replace('harder_than": "v28_', 'harder_than": "v27_')
out = out.replace("v26_hl_crumple_c260", "v27_hlx_magclip_c266")
out = out.replace("v27_hl_crumple_c260", "v27_hlx_magclip_c266")
out = out.replace('hash(fid + "_v27c266")', 'hash(fid + "_v28c272")')
out = out.replace("C267 VL", "C273 VL")
out = swap_specs(out, fmt_specs(specs["train"]))
out = inject_overlay(out)
out = replace_hardening(out)
out = out.replace(
    "HLX|MagClip|Thermal|Coffee|DblFold|Pencil|Stapler|WM|Phone|Skew|BluePen|CorrTape|ShipLabel|BinderClip|Peel",
    BANNER,
)
out = out.replace(
    "hlx_magclip_thermal_coffee_dblfold_pencil_stapler_wm_phone_skew_bluepen_corrtape_shiplabel_binderclip_peel",
    THEME,
)
out = re.sub(
    r"Harder than V2[67]:.*?(?=\nClarity floor|\n\n## Clarity)",
    PURPOSE,
    out,
    count=1,
    flags=re.S,
)
out = re.sub(r"JPEG_Q\s*=\s*\d+", "JPEG_Q = 60", out)
(SCR / "c272_vision_v28_design_and_batch.py").write_text(out, encoding="utf-8")
print("wrote c272", len(out))

# C273
src = (SCR / "c267_vision_v27_smoke.py").read_text(encoding="utf-8")
out = src.replace("C267", "C273").replace("c267", "c273")
out = out.replace("V27", "V28").replace("v27", "v28")
out = out.replace("C266", "C272").replace("c266", "c272")
out = out.replace("vision_images_v27", "vision_images_v28")
(SCR / "c273_vision_v28_smoke.py").write_text(out, encoding="utf-8")
print("wrote c273", len(out))

# C274
src = (SCR / "c268_vision_v27_heldout.py").read_text(encoding="utf-8")
out = src.replace("C268", "C274").replace("c268", "c274")
out = out.replace("V27", "V28").replace("v27", "v28")
out = out.replace("C266", "C272").replace("c266", "c272")
out = out.replace("C267", "C273").replace("c267", "c273")
out = out.replace("vision_images_v27h", "vision_images_v28h")
out = out.replace("vision_images_v27", "vision_images_v28")
out = swap_specs(out, fmt_specs(specs["held"]))
out = out.replace('hash(fid + "_v27hc268")', 'hash(fid + "_v28hc274")')
out = out.replace('hash(fid + "_v27h', 'hash(fid + "_v28h')
if "# --- V27 overlays" in out or "# --- V28 overlays" in out or "# --- V26 overlays" in out:
    out = inject_overlay(out)
    try:
        out = replace_hardening(out)
    except SystemExit:
        pass
out = out.replace(
    "HLX|MagClip|Thermal|Coffee|DblFold|Pencil|Stapler|WM|Phone|Skew|BluePen|CorrTape|ShipLabel|BinderClip|Peel",
    BANNER,
)
out = out.replace(
    "hlx_magclip_thermal_coffee_dblfold_pencil_stapler_wm_phone_skew_bluepen_corrtape_shiplabel_binderclip_peel",
    THEME,
)
out = re.sub(r"JPEG_Q\s*=\s*\d+", "JPEG_Q = 60", out)
(SCR / "c274_vision_v28_heldout.py").write_text(out, encoding="utf-8")
print("wrote c274", len(out))
print("OK")