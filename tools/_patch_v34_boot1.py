# -*- coding: utf-8 -*-
"""Patch tools/_boot_v34_c308.py from V33 template into V34+dissolve bootstrapper."""
from __future__ import annotations
import re
from pathlib import Path

P = Path("tools/_boot_v34_c308.py")
t = P.read_text(encoding="utf-8")

# Header
t = t.replace(
    '"""Bootstrap C302-C307 Vision V33 suite from V32 scripts + confidence-gate NV."""',
    '"""Bootstrap C308-C313 Vision V34 suite from V33 scripts + dissolve/shadow NV."""',
)
t = t.replace('"_v33_specs.json"', '"_v34_specs.json"')

# Overlay: rename marker and replace block body later
V34_OVERLAY = r'''
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
    # brass bolt heads
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
    # chrome glare band
    d.polygon([(60, 12), (420, 12), (410, 26), (70, 26)], fill=(200, 210, 220), outline=(100, 120, 140), width=1)
    d.text((80, 13), "CHROME bait 55.55", fill=(40, 60, 80), font=f_tiny)
    # index flag tabs right
    for ti, col in enumerate([(220, 80, 80), (80, 180, 80), (80, 80, 220)]):
        yy = 90 + ti * 40
        d.polygon([(990, yy), (1020, yy + 10), (990, yy + 20)], fill=col)
'''

# Replace V33_OVERLAY assignment
t = re.sub(
    r"V33_OVERLAY = r'''.*?'''",
    "V34_OVERLAY = r'''" + V34_OVERLAY + "'''",
    t,
    count=1,
    flags=re.S,
)

# Theme constants
t = t.replace(
    'THEMES_OLD = "Kraft|Linen|Thermal|Dossier|Chrono|Rubber|Checker|Vellum|Brad|Scroll|Ditto|Flock|Matrix|Axon|Twine|Chamfer|Snap"',
    'THEMES_OLD = "Parchment|Cork|Canvas|Rivet|Holo|Zip|Filament|Honey|Marble|Copper|Acetate|Perf|Waxseal|Magnet|Crepe|Satin|Spiral"',
)
t = t.replace(
    'THEMES_NEW = "Parchment|Cork|Canvas|Rivet|Holo|Zip|Filament|Honey|Marble|Copper|Acetate|Perf|Waxseal|Magnet|Crepe|Satin|Spiral"',
    'THEMES_NEW = "Bamboo|Slate|Denim|Brass|Prism|Latch|Amber|Quarry|Tin|Mylar|Felt|Stitch|Enamel|Cord|Rice|Chrome|Index"',
)
t = t.replace(
    'THEMES_OLD_S = "kraft_linen_thermal_dossier_chrono_rubber_checker_vellum_brad_scroll_ditto_flock_matrix_axon_twine_chamfer_snap"',
    'THEMES_OLD_S = "parchment_cork_canvas_rivet_holo_zip_filament_honey_marble_copper_acetate_perf_waxseal_magnet_crepe_satin_spiral"',
)
t = t.replace(
    'THEMES_NEW_S = "parchment_cork_canvas_rivet_holo_zip_filament_honey_marble_copper_acetate_perf_waxseal_magnet_crepe_satin_spiral"',
    'THEMES_NEW_S = "bamboo_slate_denim_brass_prism_latch_amber_quarry_tin_mylar_felt_stitch_enamel_cord_rice_chrome_index"',
)
t = t.replace(
    'THEMES_SHORT = "parchment/cork/canvas/rivet/holo/zip/filament/honey/marble/copper/acetate/perf/waxseal/magnet/crepe/satin/spiral"',
    'THEMES_SHORT = "bamboo/slate/denim/brass/prism/latch/amber/quarry/tin/mylar/felt/stitch/enamel/cord/rice/chrome/index"',
)

P.write_text(t, encoding="utf-8")
print("phase1 ok", "V34_OVERLAY" in t, "V33_OVERLAY" in t)
