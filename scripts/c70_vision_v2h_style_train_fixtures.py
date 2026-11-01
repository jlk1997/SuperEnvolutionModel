# -*- coding: utf-8 -*-
"""C70: Heldout-STYLE train fixtures — same density as V2 heldout, DISJOINT ids/content.
Never overlaps vision_images_v2_heldout. Used only for LoRA re-absorb.
"""
from __future__ import annotations
import hashlib, json
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
OUT = ROOT / "evo/office/fixtures/vision_images_v2h_style_train"
HELD = ROOT / "evo/office/fixtures/vision_images_v2_heldout"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def font(size, bold=False, mono=False):
    if mono:
        p = Path(r"C:\Windows\Fonts\consola.ttf")
    elif bold:
        p = Path(r"C:\Windows\Fonts\arialbd.ttf")
    else:
        p = Path(r"C:\Windows\Fonts\arial.ttf")
    return ImageFont.truetype(str(p), size=size)


def save(img, name, meta):
    OUT.mkdir(parents=True, exist_ok=True)
    png = OUT / f"{name}.png"
    img.save(png, format="PNG")
    digest = hashlib.sha256(png.read_bytes()).hexdigest()
    task = meta["task"]
    key = {"caption": "caption", "ocr": "ocr_text", "table_cells": "cells_csv"}[task]
    meta = {
        **meta,
        "id": name,
        "sha256": digest,
        "synthetic_not_vl": False,
        "drawn_for_vl": True,
        "heldout_style_train": True,
        "disjoint_from_heldout": True,
        "source": "c70_vision_v2h_style_train",
        "timestamp": ts(),
        "gold": meta.get("gold") or meta.get(key) or "",
    }
    (OUT / f"{name}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"id": name, "png_bytes": png.stat().st_size, "task": meta["task"], "gold": meta["gold"]}


made = []

# dense stock-like table (different SKUs)
img = Image.new("RGB", (720, 400), (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((20, 15), "WAREHOUSE SNAP", fill=(0, 0, 0), font=font(22, bold=True))
headers = ["slot", "part", "qty", "hold", "free"]
rows = [
    ["S1", "SCREW-M4", "320", "30", "290"],
    ["S2", "RIVET-8", "210", "10", "200"],
    ["T4", "TAPE-K", "88", "8", "80"],
    ["U9", "OIL-Z", "44", "4", "40"],
]
x0 = [20, 100, 280, 400, 520]
for i, h in enumerate(headers):
    d.text((x0[i], 55), h, fill=(0, 0, 120), font=font(16, bold=True, mono=True))
y = 95
for row in rows:
    for i, cell in enumerate(row):
        d.text((x0[i], y), cell, fill=(0, 0, 0), font=font(16, mono=True))
    y += 40
cg = "slot,part,qty,hold,free\nS1,SCREW-M4,320,30,290\nS2,RIVET-8,210,10,200\nT4,TAPE-K,88,8,80\nU9,OIL-Z,44,4,40"
made.append(save(img, "v2t-table-wh-001", {"task": "table_cells", "cells_csv": cg, "gold": cg}))

# another dense table
img = Image.new("RGB", (700, 360), (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((20, 15), "QC BATCH", fill=(0, 0, 0), font=font(22, bold=True))
headers = ["lot", "line", "pass", "fail", "rate"]
rows = [["L11", "A", "90", "2", "97%"], ["L12", "B", "80", "5", "94%"], ["L13", "C", "70", "1", "98%"]]
x0 = [30, 140, 260, 380, 500]
for i, h in enumerate(headers):
    d.text((x0[i], 55), h, fill=(100, 0, 0), font=font(18, bold=True, mono=True))
y = 100
for row in rows:
    for i, cell in enumerate(row):
        d.text((x0[i], y), cell, fill=(0, 0, 0), font=font(18, mono=True))
    y += 45
cg = "lot,line,pass,fail,rate\nL11,A,90,2,97%\nL12,B,80,5,94%\nL13,C,70,1,98%"
made.append(save(img, "v2t-table-qc-001", {"task": "table_cells", "cells_csv": cg, "gold": cg}))

# debit note OCR
img = Image.new("RGB", (680, 480), (255, 255, 255))
d = ImageDraw.Draw(img)
d.rectangle([15, 15, 665, 465], outline=(0, 0, 0), width=2)
d.text((40, 30), "DEBIT NOTE #DN-440", fill=(0, 0, 0), font=font(28, bold=True))
d.text((40, 80), "Vendor: South Mill Ltd", fill=(0, 0, 0), font=font(20))
d.text((40, 115), "Reason: Short delivery", fill=(0, 0, 0), font=font(18))
d.text((40, 160), "Item X  qty 5  @ 12.00 = 60.00", fill=(0, 0, 0), font=font(18, mono=True))
d.text((40, 195), "Item Y  qty 1  @ 8.00  = 8.00", fill=(0, 0, 0), font=font(18, mono=True))
d.text((40, 240), "Fee 2.00", fill=(160, 0, 0), font=font(20, bold=True))
d.text((40, 285), "DEBIT TOTAL 70.00", fill=(0, 80, 0), font=font(24, bold=True))
d.text((40, 340), "Issued 2026-10-19  Ref PO-8810", fill=(0, 0, 0), font=font(18))
g = "DEBIT NOTE DN-440 Fee 2.00 DEBIT TOTAL 70.00 Issued 2026-10-19"
made.append(save(img, "v2t-ocr-debit-001", {"task": "ocr", "ocr_text": g, "gold": g}))

# ship label OCR
img = Image.new("RGB", (640, 360), (255, 255, 240))
d = ImageDraw.Draw(img)
d.rectangle([20, 20, 620, 340], outline=(0, 0, 0), width=3)
d.text((40, 40), "SHIP LABEL", fill=(0, 0, 0), font=font(26, bold=True))
d.text((40, 90), "TO: East Gate Bay 7", fill=(0, 0, 0), font=font(22))
d.text((40, 135), "PALLET 2 of 3", fill=(0, 0, 0), font=font(20, bold=True))
d.text((40, 185), "SKU MIX: SCREW-M4 x20, RIVET-8 x10", fill=(0, 0, 0), font=font(18, mono=True))
d.text((40, 235), "TRACKING TRK-99001", fill=(0, 0, 120), font=font(20, bold=True))
d.text((40, 285), "HEAVY  THIS SIDE UP", fill=(160, 0, 0), font=font(22, bold=True))
g = "SHIP LABEL TO East Gate Bay 7 PALLET 2 of 3 TRACKING TRK-99001 HEAVY THIS SIDE UP"
made.append(save(img, "v2t-ocr-ship-001", {"task": "ocr", "ocr_text": g, "gold": g}))

# sales order OCR
img = Image.new("RGB", (640, 400), (255, 255, 255))
d = ImageDraw.Draw(img)
d.rectangle([20, 20, 620, 380], outline=(0, 0, 0), width=2)
d.text((40, 40), "SALES ORDER SO-7711", fill=(0, 0, 0), font=font(24, bold=True))
d.text((40, 90), "Customer: West Retail", fill=(0, 0, 0), font=font(20))
d.text((40, 130), "Seller: Ant Parts", fill=(0, 0, 0), font=font(20))
d.text((40, 180), "Bracket set x 6  @ 25.00 = 150.00", fill=(0, 0, 0), font=font(18, mono=True))
d.text((40, 220), "Ship 12.00", fill=(0, 0, 0), font=font(18, mono=True))
d.text((40, 270), "ORDER TOTAL USD 162.00", fill=(120, 0, 0), font=font(22, bold=True))
d.text((40, 320), "Ship by 2026-11-05", fill=(0, 0, 0), font=font(20))
g = "SALES ORDER SO-7711 ORDER TOTAL USD 162.00 Ship by 2026-11-05"
made.append(save(img, "v2t-ocr-so-001", {"task": "ocr", "ocr_text": g, "gold": g}))

# ops dash caption
img = Image.new("RGB", (720, 400), (245, 247, 250))
d = ImageDraw.Draw(img)
d.text((30, 20), "LINE DASHBOARD", fill=(20, 20, 40), font=font(26, bold=True))
boxes = [(40, 80, 220, 200, "Jobs", "64"), (250, 80, 430, 200, "Scrap", "3"), (460, 80, 680, 200, "OEE", "88%")]
for x0b, y0, x1, y1, title, val in boxes:
    d.rectangle([x0b, y0, x1, y1], fill=(255, 255, 255), outline=(40, 40, 60), width=2)
    d.text((x0b + 20, y0 + 20), title, fill=(80, 80, 100), font=font(18))
    d.text((x0b + 20, y0 + 70), val, fill=(20, 20, 40), font=font(36, bold=True))
d.text((40, 240), "Alert: Line B feeder jam", fill=(180, 0, 0), font=font(20, bold=True))
d.text((40, 290), "Shift: Day  Owner: MFG", fill=(40, 40, 40), font=font(18))
g = "LINE DASHBOARD Jobs 64 Scrap 3 OEE 88% Alert Line B feeder jam"
made.append(save(img, "v2t-caption-line-001", {"task": "caption", "caption": g, "gold": g}))

# bench caption
img = Image.new("RGB", (680, 380), (230, 235, 240))
d = ImageDraw.Draw(img)
d.rectangle([40, 180, 640, 320], fill=(140, 100, 60), outline=(70, 40, 20), width=3)
d.rectangle([80, 60, 280, 180], fill=(40, 40, 50), outline=(10, 10, 10), width=2)
d.rectangle([100, 40, 260, 140], fill=(80, 200, 120), outline=(20, 20, 30), width=2)
d.ellipse([500, 200, 600, 280], fill=(40, 40, 220), outline=(0, 0, 80), width=2)
d.text((30, 20), "assembly desk green panel blue can wrench", fill=(10, 10, 10), font=font(18, bold=True))
g = "assembly desk green panel blue can wrench"
made.append(save(img, "v2t-caption-desk-001", {"task": "caption", "caption": g, "gold": g}))

# UI
img = Image.new("RGB", (600, 360), (28, 30, 36))
d = ImageDraw.Draw(img)
d.text((40, 30), "Backup Policy", fill=(240, 240, 240), font=font(26, bold=True))
d.text((40, 100), "Auto backup", fill=(220, 220, 220), font=font(22))
d.rectangle([400, 95, 500, 140], fill=(40, 180, 80), outline=(20, 100, 40), width=2)
d.text((40, 180), "Cloud sync", fill=(220, 220, 220), font=font(22))
d.rectangle([400, 175, 500, 220], fill=(80, 80, 90), outline=(40, 40, 50), width=2)
d.text((40, 260), "backup ON cloud OFF", fill=(180, 180, 180), font=font(18))
g = "Backup Policy Auto backup ON Cloud sync OFF"
made.append(save(img, "v2t-ui-backup-001", {"task": "caption", "caption": g, "gold": g}))

# modal UI
img = Image.new("RGB", (640, 420), (35, 38, 45))
d = ImageDraw.Draw(img)
d.rectangle([70, 50, 570, 370], fill=(250, 250, 252), outline=(10, 10, 10), width=3)
d.text((110, 80), "Purge temp cache?", fill=(20, 20, 20), font=font(26, bold=True))
d.text((110, 140), "This frees 12 GB disk.", fill=(80, 40, 40), font=font(18))
d.text((110, 180), "Type PURGE to proceed.", fill=(60, 60, 60), font=font(18))
d.rectangle([120, 240, 280, 300], fill=(210, 210, 210), outline=(0, 0, 0), width=2)
d.text((150, 255), "Cancel", fill=(0, 0, 0), font=font(22, bold=True))
d.rectangle([340, 240, 520, 300], fill=(190, 30, 30), outline=(80, 0, 0), width=2)
d.text((380, 255), "Purge", fill=(255, 255, 255), font=font(20, bold=True))
g = "Purge temp cache? frees 12 GB [Cancel] [Purge]"
made.append(save(img, "v2t-ui-purge-001", {"task": "caption", "caption": g, "gold": g}))

# roster-like
img = Image.new("RGB", (640, 340), (252, 252, 255))
d = ImageDraw.Draw(img)
d.text((20, 15), "ROSTER DAY", fill=(0, 0, 0), font=font(22, bold=True))
headers = ["role", "name", "bay", "radio"]
rows = [["Lead", "Kai", "1", "R4"], ["Picker", "Ann", "3", "R5"], ["QA", "Bo", "2", "R6"]]
x0 = [30, 160, 320, 440]
for i, h in enumerate(headers):
    d.text((x0[i], 60), h, fill=(0, 0, 100), font=font(18, bold=True, mono=True))
y = 105
for row in rows:
    for i, cell in enumerate(row):
        d.text((x0[i], y), cell, fill=(0, 0, 0), font=font(18, mono=True))
    y += 45
cg = "role,name,bay,radio\nLead,Kai,1,R4\nPicker,Ann,3,R5\nQA,Bo,2,R6"
made.append(save(img, "v2t-table-day-001", {"task": "table_cells", "cells_csv": cg, "gold": cg}))

# collision check vs heldout
held_ids = set()
if HELD.is_dir():
    held_ids = {p.stem for p in HELD.glob("*.png")}
train_ids = {m["id"] for m in made}
overlap = sorted(train_ids & held_ids)

payload = {
    "kind": "r50plus_c70_vision_v2h_style_train_fixtures",
    "timestamp": ts(),
    "gate": GATE,
    "n": len(made),
    "fixtures": made,
    "dir": "evo/office/fixtures/vision_images_v2h_style_train",
    "disjoint_from": "evo/office/fixtures/vision_images_v2_heldout",
    "overlap_ids": overlap,
    "innovation": "Heldout-style train set for LoRA re-absorb; never equals heldout test",
    "gate2_3_untouched": True,
    "v1_v2_claims_untouched": True,
}
(ROOT / "docs/r50").mkdir(parents=True, exist_ok=True)
(ROOT / "docs/r50/C70_vision_v2h_style_train_fixtures.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps({"n": len(made), "overlap": overlap, "ids": [m["id"] for m in made]}, ensure_ascii=False))
