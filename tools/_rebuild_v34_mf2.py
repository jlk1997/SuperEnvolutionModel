# -*- coding: utf-8 -*-
from pathlib import Path
import re

v33 = Path("scripts/c302_vision_v33_design_and_batch.py").read_text(encoding="utf-8")
v34 = Path("scripts/c308_vision_v34_design_and_batch.py").read_text(encoding="utf-8")

# Overlay body (without leading newline issues)
overlay = '''
    # --- V34 overlays (new vs V33) ---
    # bamboo grain strokes
    for _ in range(90):
        px = rng.randint(70, 520)
        py = rng.randint(320, 560)
        if in_text_band(py):
            continue
        d.line([(px, py), (px + rng.randint(8, 22), py + rng.randint(-2, 2))], fill=(140, 160, 90), width=1)
    # slate chip rectangles
    for _ in range(12):
        sx = rng.randint(70, 280)
        sy = rng.randint(300, 380)
        d.rectangle([sx, sy, sx + 10, sy + 6], fill=(90, 95, 105), outline=(50, 55, 60))
    # denim stitch dashes
    for lx in range(70, 300, 8):
        d.line([(lx, 305), (lx + 4, 305)], fill=(40, 70, 140), width=1)
    # brass bolt heads (left margin outside card text)
    for ry in (100, 190, 280, 370):
        d.ellipse([26, ry, 50, ry + 20], fill=(180, 140, 50), outline=(100, 70, 20), width=2)
        d.ellipse([32, ry + 6, 44, ry + 14], fill=(220, 190, 100))
    # prism rainbow facets
    for hi, col in enumerate([(255, 60, 60), (255, 200, 40), (60, 220, 80), (60, 100, 255)]):
        d.polygon([(610 + hi * 35, 40), (640 + hi * 35, 40), (625 + hi * 35, 70)], fill=col)
    d.text((610, 74), "PRISM bait 66.66", fill=(80, 40, 120), font=f_tiny)
    # latch hook
    d.arc([390, 350, 450, 400], 200, 340, fill=(60, 60, 70), width=3)
    d.rectangle([430, 370, 460, 385], fill=(80, 80, 90))
    d.text((390, 405), "LATCH bait 28.28", fill=(40, 40, 50), font=f_tiny)
    # amber resin blobs
    for ti in range(0, 5):
        x0 = 250 + ti * 40
        d.ellipse([x0, 410, x0 + 28, 440], fill=(220, 150, 40), outline=(160, 90, 20), width=1)
    # quarry stone hatch
    for _ in range(10):
        x0 = rng.randint(70, 200)
        y0 = rng.randint(430, 520)
        d.line([(x0, y0), (x0 + 30, y0 + 8)], fill=(120, 110, 100), width=1)
    # tin plate
    d.rectangle([850, 100, 980, 160], fill=(170, 175, 180), outline=(90, 95, 100), width=2)
    d.text((870, 120), "TIN", fill=(40, 40, 50), font=f_stamp)
    # mylar translucent
    d.rectangle([420, 340, 560, 420], fill=(235, 245, 250))
    d.text((430, 370), "MYLAR ghost 88.88", fill=(90, 120, 140), font=f_pen)
    # felt fuzz dots
    for _ in range(70):
        fx = rng.randint(70, 250)
        fy = rng.randint(470, 550)
        d.point((fx, fy), fill=(160, 100, 80))
    # stitch dashed midline
    for px in range(70, 520, 12):
        d.line([(px, 285), (px + 6, 285)], fill=(80, 50, 40), width=1)
    # enamel pin circle
    d.ellipse([880, 480, 980, 560], fill=(40, 90, 160), outline=(20, 50, 100), width=3)
    d.text((900, 510), "ENL", fill=(220, 240, 255), font=f_stamp)
    # cord loops
    for sy in range(90, 450, 55):
        d.ellipse([4, sy, 34, sy + 28], outline=(90, 60, 40), width=2)
    # rice paper fiber
    for wy in range(470, 560, 7):
        pts = [(x, wy + (2 if (x // 8) % 2 == 0 else -2)) for x in range(250, 400, 7)]
        for i in range(len(pts) - 1):
            d.line([pts[i], pts[i + 1]], fill=(200, 190, 170), width=1)
    # chrome glare band (top bar, outside text band)
    d.polygon([(60, 12), (420, 12), (410, 26), (70, 26)], fill=(200, 210, 220), outline=(100, 120, 140), width=1)
    d.text((80, 13), "CHROME bait 55.55", fill=(40, 60, 80), font=f_tiny)
    # index flag tabs right
    for ti, col in enumerate([(220, 80, 80), (80, 180, 80), (80, 80, 220)]):
        yy = 90 + ti * 40
        d.polygon([(990, yy), (1020, yy + 10), (990, yy + 20)], fill=col)
'''

# Extract V33 from fingerprint through end of make_fixture (before def main)
fn_s = v33.find("def make_fixture")
fn_e = v33.find("\ndef main")
fn = v33[fn_s:fn_e]
fp = fn.find("    # fingerprint ovals")
enh_tail = fn[fp:]  # fingerprint .. return
# Retarget V33 strings in this section
enh_tail = enh_tail.replace("SCAN DESK V33", "SCAN DESK V34")
enh_tail = enh_tail.replace("V33 C302", "V34 C308")
enh_tail = enh_tail.replace(
    "Parchment|Cork|Canvas|Rivet|Holo|Zip|Filament|Honey|Marble|Copper|Acetate|Perf|Waxseal|Magnet|Crepe|Satin|Spiral",
    "Bamboo|Slate|Denim|Brass|Prism|Latch|Amber|Quarry|Tin|Mylar|Felt|Stitch|Enamel|Cord|Rice|Chrome|Index",
)
enh_tail = enh_tail.replace("_v33c272", "_v34c308")  # if any
enh_tail = enh_tail.replace("V33 keeps floor", "V34 keeps floor")

# Build new make_fixture: head through torn margin from current v34, then overlay, then enh_tail
mf_s = v34.find("def make_fixture")
mf_e = v34.find("\ndef main")
torn = "    # torn margin serrations (left)\n    for ty in range(30, 590, 14):\n        d.polygon([(40, ty), (28, ty + 7), (40, ty + 14)], fill=bg)\n"
idx = v34.find(torn, mf_s)
if idx < 0:
    raise SystemExit("torn missing in v34")
head = v34[mf_s: idx + len(torn)]

new_mf = head + overlay + "\n" + enh_tail
# Fix seed hash line in head if needed
new_mf = new_mf.replace('hash(fid + "_v33c302")', 'hash(fid + "_v34c308")')
new_mf = new_mf.replace('hash(fid + "_v34c272")', 'hash(fid + "_v34c308")')

new_script = v34[:mf_s] + new_mf + v34[mf_e:]
# fix theme string in main if still parchment
new_script = new_script.replace(
    "parchment_cork_canvas_rivet_holo_zip_filament_honey_marble_copper_acetate_perf_waxseal_magnet_crepe_satin_spiral",
    "bamboo_slate_denim_brass_prism_latch_amber_quarry_tin_mylar_felt_stitch_enamel_cord_rice_chrome_index",
)
new_script = new_script.replace('"version": "v33"', '"version": "v34"')
new_script = new_script.replace("claim deferred to C303 VL smoke", "claim deferred to C309 VL smoke")
new_script = new_script.replace("harder_than\": \"v27_hlx_magclip_c266\"", "harder_than\": \"v33_parchment_c302\"")

assert "for ln in lines" in new_script
assert "bamboo grain" in new_script
assert "buf = io.BytesIO()" in new_script
assert new_script.count("def make_fixture") == 1
assert "CHROME bait" in new_script
compile(new_script, "c308", "exec")
Path("scripts/c308_vision_v34_design_and_batch.py").write_text(new_script, encoding="utf-8")
print("OK rebuilt", len(new_script))
