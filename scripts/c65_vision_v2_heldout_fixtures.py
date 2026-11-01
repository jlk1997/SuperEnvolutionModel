# -*- coding: utf-8 -*-
"""C65: Vision V2 HELDOUT harder readable fixtures (never seen in C59/C63)."""
from __future__ import annotations
import hashlib, json
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
OUT = ROOT / "evo/office/fixtures/vision_images_v2_heldout"


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
        "readable_v2_heldout": True,
        "harder_than_v2_smoke": True,
        "heldout": True,
        "source": "c65_vision_v2_heldout",
        "timestamp": ts(),
        "gold": meta.get("gold") or meta.get(key) or "",
    }
    (OUT / f"{name}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"id": name, "png_bytes": png.stat().st_size, "task": meta["task"], "gold": meta["gold"]}


made = []

# 1 dense discount invoice OCR
img = Image.new("RGB", (700, 520), (255, 255, 255))
d = ImageDraw.Draw(img)
d.rectangle([15, 15, 685, 505], outline=(0, 0, 0), width=2)
d.text((40, 30), "CREDIT NOTE #CN-991", fill=(0, 0, 0), font=font(28, bold=True))
d.text((40, 80), "Customer: North Plant Co", fill=(0, 0, 0), font=font(20))
d.text((40, 115), "Reason: Damaged shipment", fill=(0, 0, 0), font=font(18))
d.text((40, 160), "Item A  qty 3  @ 15.00 = 45.00", fill=(0, 0, 0), font=font(18, mono=True))
d.text((40, 195), "Item B  qty 2  @ 9.50  = 19.00", fill=(0, 0, 0), font=font(18, mono=True))
d.text((40, 240), "Discount -5.00", fill=(160, 0, 0), font=font(20, bold=True))
d.text((40, 285), "CREDIT TOTAL 59.00", fill=(0, 80, 0), font=font(24, bold=True))
d.text((40, 340), "Issued 2026-10-18  Ref INV-3301", fill=(0, 0, 0), font=font(18))
g = "CREDIT NOTE CN-991 Discount -5.00 CREDIT TOTAL 59.00 Issued 2026-10-18"
made.append(save(img, "v2h-ocr-credit-001", {"task": "ocr", "ocr_text": g, "caption": "", "cells_csv": "", "gold": g}))

# 2 multi-kpi dashboard caption
img = Image.new("RGB", (720, 400), (245, 247, 250))
d = ImageDraw.Draw(img)
d.text((30, 20), "OPS DASHBOARD", fill=(20, 20, 40), font=font(26, bold=True))
boxes = [
    (40, 80, 220, 200, "Orders", "128"),
    (250, 80, 430, 200, "Late", "7"),
    (460, 80, 680, 200, "FillRate", "94%"),
]
for x0, y0, x1, y1, title, val in boxes:
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=(40, 40, 60), width=2)
    d.text((x0 + 20, y0 + 20), title, fill=(80, 80, 100), font=font(18))
    d.text((x0 + 20, y0 + 70), val, fill=(20, 20, 40), font=font(36, bold=True))
d.text((40, 240), "Alert: Bay 4 conveyor jam", fill=(180, 0, 0), font=font(20, bold=True))
d.text((40, 290), "Shift: Night  Owner: OPS", fill=(40, 40, 40), font=font(18))
g = "OPS DASHBOARD Orders 128 Late 7 FillRate 94% Alert Bay 4 conveyor jam"
made.append(save(img, "v2h-caption-dash-001", {"task": "caption", "caption": g, "ocr_text": "", "cells_csv": "", "gold": g}))

# 3 dense inventory table
img = Image.new("RGB", (700, 380), (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((20, 15), "STOCK SNAPSHOT", fill=(0, 0, 0), font=font(22, bold=True))
headers = ["bin", "sku", "onhand", "reserved", "avail"]
rows = [
    ["A1", "BOLT-M6", "500", "40", "460"],
    ["A2", "NUT-M6", "480", "20", "460"],
    ["B3", "WASHER", "900", "100", "800"],
    ["C1", "GLUE-X", "55", "5", "50"],
]
x0 = [20, 90, 250, 380, 520]
for i, h in enumerate(headers):
    d.text((x0[i], 55), h, fill=(0, 0, 120), font=font(16, bold=True, mono=True))
y = 95
for row in rows:
    for i, cell in enumerate(row):
        d.text((x0[i], y), cell, fill=(0, 0, 0), font=font(16, mono=True))
    y += 40
cg = "bin,sku,onhand,reserved,avail\nA1,BOLT-M6,500,40,460\nA2,NUT-M6,480,20,460\nB3,WASHER,900,100,800\nC1,GLUE-X,55,5,50"
made.append(save(img, "v2h-table-stock-001", {"task": "table_cells", "cells_csv": cg, "ocr_text": "", "caption": "", "gold": cg}))

# 4 danger modal UI
img = Image.new("RGB", (640, 420), (35, 38, 45))
d = ImageDraw.Draw(img)
d.rectangle([70, 50, 570, 370], fill=(250, 250, 252), outline=(10, 10, 10), width=3)
d.text((110, 80), "Overwrite sealed pack?", fill=(20, 20, 20), font=font(26, bold=True))
d.text((110, 140), "This burns gen11 seal permanently.", fill=(80, 40, 40), font=font(18))
d.text((110, 180), "Type CONFIRM to proceed.", fill=(60, 60, 60), font=font(18))
d.rectangle([120, 240, 280, 300], fill=(210, 210, 210), outline=(0, 0, 0), width=2)
d.text((150, 255), "Abort", fill=(0, 0, 0), font=font(22, bold=True))
d.rectangle([340, 240, 520, 300], fill=(190, 30, 30), outline=(80, 0, 0), width=2)
d.text((365, 255), "Overwrite", fill=(255, 255, 255), font=font(20, bold=True))
g = "Overwrite sealed pack? burns gen11 seal [Abort] [Overwrite]"
made.append(save(img, "v2h-ui-seal-001", {"task": "caption", "caption": g, "ocr_text": "Abort Overwrite", "cells_csv": "", "gold": g}))

# 5 packing label OCR mixed
img = Image.new("RGB", (640, 360), (255, 255, 240))
d = ImageDraw.Draw(img)
d.rectangle([20, 20, 620, 340], outline=(0, 0, 0), width=3)
d.text((40, 40), "PACK LABEL", fill=(0, 0, 0), font=font(26, bold=True))
d.text((40, 90), "TO: West Hub Dock 2", fill=(0, 0, 0), font=font(22))
d.text((40, 135), "CARTON 3 of 5", fill=(0, 0, 0), font=font(20, bold=True))
d.text((40, 185), "SKU MIX: BOLT-M6 x40, NUT-M6 x40", fill=(0, 0, 0), font=font(18, mono=True))
d.text((40, 235), "TRACKING TRK-77821", fill=(0, 0, 120), font=font(20, bold=True))
d.text((40, 285), "FRAGILE  KEEP DRY", fill=(160, 0, 0), font=font(22, bold=True))
g = "PACK LABEL TO West Hub Dock 2 CARTON 3 of 5 TRACKING TRK-77821 FRAGILE KEEP DRY"
made.append(save(img, "v2h-ocr-pack-001", {"task": "ocr", "ocr_text": g, "caption": "", "cells_csv": "", "gold": g}))

# 6 shift roster table
img = Image.new("RGB", (640, 340), (252, 252, 255))
d = ImageDraw.Draw(img)
d.text((20, 15), "ROSTER NIGHT", fill=(0, 0, 0), font=font(22, bold=True))
headers = ["role", "name", "bay", "radio"]
rows = [["Lead", "Mei", "4", "R1"], ["Picker", "Jon", "2", "R3"], ["QA", "Lia", "1", "R2"]]
x0 = [30, 160, 320, 440]
for i, h in enumerate(headers):
    d.text((x0[i], 60), h, fill=(0, 0, 100), font=font(18, bold=True, mono=True))
y = 105
for row in rows:
    for i, cell in enumerate(row):
        d.text((x0[i], y), cell, fill=(0, 0, 0), font=font(18, mono=True))
    y += 45
cg = "role,name,bay,radio\nLead,Mei,4,R1\nPicker,Jon,2,R3\nQA,Lia,1,R2"
made.append(save(img, "v2h-table-roster-001", {"task": "table_cells", "cells_csv": cg, "ocr_text": "", "caption": "", "gold": cg}))

# 7 cluttered bench caption with labels
img = Image.new("RGB", (680, 380), (230, 235, 240))
d = ImageDraw.Draw(img)
d.rectangle([40, 180, 640, 320], fill=(140, 100, 60), outline=(70, 40, 20), width=3)
d.rectangle([80, 60, 280, 180], fill=(40, 40, 50), outline=(10, 10, 10), width=2)
d.rectangle([100, 40, 260, 140], fill=(120, 180, 255), outline=(20, 20, 30), width=2)
d.ellipse([500, 200, 600, 280], fill=(220, 40, 40), outline=(80, 0, 0), width=2)
d.rectangle([320, 90, 420, 170], fill=(200, 200, 210), outline=(60, 60, 70), width=2)
d.text((30, 20), "repair bench laptop blue screen red jar toolbox", fill=(10, 10, 10), font=font(18, bold=True))
g = "repair bench laptop blue screen red jar toolbox"
made.append(save(img, "v2h-caption-bench-001", {"task": "caption", "caption": g, "ocr_text": "", "cells_csv": "", "gold": g}))

# 8 access control UI
img = Image.new("RGB", (600, 360), (28, 30, 36))
d = ImageDraw.Draw(img)
d.text((40, 30), "Access Control", fill=(240, 240, 240), font=font(26, bold=True))
d.text((40, 100), "SSH keys", fill=(220, 220, 220), font=font(22))
d.rectangle([400, 95, 500, 140], fill=(40, 180, 80), outline=(20, 100, 40), width=2)
d.text((40, 180), "Root login", fill=(220, 220, 220), font=font(22))
d.rectangle([400, 175, 500, 220], fill=(80, 80, 90), outline=(40, 40, 50), width=2)
d.text((40, 260), "ssh ON root OFF", fill=(180, 180, 180), font=font(18))
g = "Access Control SSH keys ON Root login OFF"
made.append(save(img, "v2h-ui-access-001", {"task": "caption", "caption": g, "ocr_text": "SSH keys Root login", "cells_csv": "", "gold": g}))

# 9 PO OCR with currency
img = Image.new("RGB", (640, 400), (255, 255, 255))
d = ImageDraw.Draw(img)
d.rectangle([20, 20, 620, 380], outline=(0, 0, 0), width=2)
d.text((40, 40), "PURCHASE ORDER PO-5520", fill=(0, 0, 0), font=font(24, bold=True))
d.text((40, 90), "Supplier: Ant Steel", fill=(0, 0, 0), font=font(20))
d.text((40, 130), "Buyer: East Warehouse", fill=(0, 0, 0), font=font(20))
d.text((40, 180), "Plate 10mm x 4  @ 120.00 = 480.00", fill=(0, 0, 0), font=font(18, mono=True))
d.text((40, 220), "Freight 35.00", fill=(0, 0, 0), font=font(18, mono=True))
d.text((40, 270), "GRAND TOTAL USD 515.00", fill=(120, 0, 0), font=font(22, bold=True))
d.text((40, 320), "Need by 2026-11-01", fill=(0, 0, 0), font=font(20))
g = "PURCHASE ORDER PO-5520 GRAND TOTAL USD 515.00 Need by 2026-11-01"
made.append(save(img, "v2h-ocr-po-001", {"task": "ocr", "ocr_text": g, "caption": "", "cells_csv": "", "gold": g}))

# 10 defect log table
img = Image.new("RGB", (680, 320), (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((20, 15), "DEFECT LOG", fill=(0, 0, 0), font=font(22, bold=True))
headers = ["id", "area", "sev", "status"]
rows = [["D01", "Paint", "H", "open"], ["D02", "Weld", "M", "fixed"], ["D03", "Seal", "H", "open"]]
x0 = [30, 120, 280, 400]
for i, h in enumerate(headers):
    d.text((x0[i], 55), h, fill=(100, 0, 0), font=font(18, bold=True, mono=True))
y = 100
for row in rows:
    for i, cell in enumerate(row):
        d.text((x0[i], y), cell, fill=(0, 0, 0), font=font(18, mono=True))
    y += 45
cg = "id,area,sev,status\nD01,Paint,H,open\nD02,Weld,M,fixed\nD03,Seal,H,open"
made.append(save(img, "v2h-table-defect-001", {"task": "table_cells", "cells_csv": cg, "ocr_text": "", "caption": "", "gold": cg}))

payload = {
    "kind": "r50plus_c65_vision_v2_heldout_fixtures",
    "timestamp": ts(),
    "gate": GATE,
    "n": len(made),
    "fixtures": made,
    "dir": "evo/office/fixtures/vision_images_v2_heldout",
    "disjoint_from": "evo/office/fixtures/vision_images_v2",
    "innovation": "Heldout harder V2 readable set never seen in C63 smoke",
    "vl_gate_v2_heldout_claim": False,
    "gate2_3_untouched": True,
    "v1_v2_claims_untouched": True,
}
(ROOT / "docs/r50").mkdir(parents=True, exist_ok=True)
(ROOT / "docs/r50/C65_vision_v2_heldout_fixtures.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps({"n": len(made), "ids": [m["id"] for m in made]}, ensure_ascii=False))
