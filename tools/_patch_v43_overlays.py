from pathlib import Path
pairs = [
    ("Obsidian|Denim|Coral|Indigo|Jade|Amber|Nickel|Moss|Pine|Opal|Granite|Void|Cedar|Enamel|Resin|Sage|Terra|Hazel",
     "Marble|Linen|Crimson|Cobalt|Emerald|Topaz|Chrome|Fern|Spruce|Pearl|Shale|Vacuum|Cypress|Glaze|Epoxy|Mint|Clay|Cork"),
    ("OBSIDIAN bait 42.42", "MARBLE bait 43.43"),
    ("CORAL bait 62.62", "CRIMSON bait 63.63"),
    ("DENIM ghost 92.92", "LINEN ghost 93.93"),
    ("JADE bait 37.37", "EMERALD bait 38.38"),
    ("PINE bait 28.28", "SPRUCE bait 29.29"),
    ("HAZEL bait 72.72", "CORK bait 73.73"),
    ('d.text((880, 138), "AMBER"', 'd.text((880, 138), "TOPAZ"'),
    ("V42 C365", "V43 C365"),
    ("V42H C367", "V43H C367"),
]
for rel in ["scripts/c365_vision_v43_design_and_batch.py", "scripts/c367_vision_v43_heldout.py"]:
    p = Path(rel)
    t = p.read_text(encoding="utf-8")
    for a, b in pairs:
        t = t.replace(a, b)
    p.write_text(t, encoding="utf-8")
    print("patched", rel, "marble" in t, "JPEG_Q = 62" in t)
