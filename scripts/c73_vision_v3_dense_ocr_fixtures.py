# -*- coding: utf-8 -*-
"""C73a: Harder VL denser OCR / multi-row tables (honest drawn fixtures)."""
from __future__ import annotations
import hashlib, json
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
OUT = ROOT / "evo/office/fixtures/vision_images_v3_dense"


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
        "v3_dense": True,
        "harder_than_v2_heldout": True,
        "source": "c73_vision_v3_dense",
        "timestamp": ts(),
        "gold": meta.get("gold") or meta.get(key) or "",
    }
    (OUT / f"{name}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"id": name, "png_bytes": png.stat().st_size, "task": meta["task"], "gold": meta["gold"]}


made = []

# 6-col dense inventory
img = Image.new("RGB", (860, 420), (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((16, 10), "INV DENSE OCR TABLE", fill=(0, 0, 0), font=font(20, bold=True))
headers = ["bin", "sku", "onhand", "reserved", "avail", "zone"]
rows = [
    ["A1", "BOLT-M6", "500", "40", "460", "N"],
    ["A2", "NUT-M6", "480", "20", "460", "N"],
    ["B3", "WASHER", "900", "100", "800", "S"],
    ["C1", "GLUE-X", "55", "5", "50", "E"],
    ["D2", "TAPE-K", "120", "12", "108", "W"],
    ["E4", "OIL-Z", "33", "3", "30", "S"],
]
x0 = [16, 80, 240, 360, 500, 640]
for i, h in enumerate(headers):
    d.text((x0[i], 50), h, fill=(0, 0, 120), font=font(15, bold=True, mono=True))
y = 85
for row in rows:
    for i, cell in enumerate(row):
        d.text((x0[i], y), cell, fill=(0, 0, 0), font=font(15, mono=True))
    y += 36
cg = "bin,sku,onhand,reserved,avail,zone\n" + "\n".join(",".join(r) for r in rows)
made.append(save(img, "v3-table-inv6-001", {"task": "table_cells", "cells_csv": cg, "gold": cg}))

# multi-line invoice OCR denser
img = Image.new("RGB", (720, 560), (255, 255, 255))
d = ImageDraw.Draw(img)
d.rectangle([12, 12, 708, 548], outline=(0, 0, 0), width=2)
d.text((30, 24), "TAX INVOICE INV-88421", fill=(0, 0, 0), font=font(24, bold=True))
d.text((30, 70), "Bill To: Harbor Logistics LLC", fill=(0, 0, 0), font=font(18))
d.text((30, 100), "Ship To: Dock 9 Cold Store", fill=(0, 0, 0), font=font(18))
lines = [
    "Line1  SKU BOLT-M6  qty 40  @ 0.80 = 32.00",
    "Line2  SKU NUT-M6   qty 40  @ 0.50 = 20.00",
    "Line3  SKU WASHER   qty 80  @ 0.20 = 16.00",
    "Line4  SKU GLUE-X   qty 4   @ 5.00 = 20.00",
]
y = 150
for ln in lines:
    d.text((30, y), ln, fill=(0, 0, 0), font=font(16, mono=True))
    y += 32
d.text((30, 300), "Subtotal 88.00", fill=(0, 0, 0), font=font(18))
d.text((30, 335), "VAT 8.80", fill=(0, 0, 0), font=font(18))
d.text((30, 380), "GRAND TOTAL USD 96.80", fill=(140, 0, 0), font=font(22, bold=True))
d.text((30, 430), "Due 2026-11-12  PO-REF PO-5520", fill=(0, 0, 0), font=font(18))
d.text((30, 470), "Terms Net 30", fill=(40, 40, 40), font=font(16))
g = "TAX INVOICE INV-88421 Subtotal 88.00 VAT 8.80 GRAND TOTAL USD 96.80 Due 2026-11-12"
made.append(save(img, "v3-ocr-taxinv-001", {"task": "ocr", "ocr_text": g, "gold": g}))

# packing list OCR
img = Image.new("RGB", (700, 480), (255, 255, 245))
d = ImageDraw.Draw(img)
d.rectangle([15, 15, 685, 465], outline=(0, 0, 0), width=3)
d.text((35, 30), "PACKING LIST PL-2201", fill=(0, 0, 0), font=font(24, bold=True))
d.text((35, 80), "From: Ant Hub  To: West Hub Dock 2", fill=(0, 0, 0), font=font(18))
d.text((35, 120), "Cartons: 5  Weight: 42.5 kg", fill=(0, 0, 0), font=font(18))
d.text((35, 170), "C1 BOLT-M6 x100", fill=(0, 0, 0), font=font(17, mono=True))
d.text((35, 205), "C2 NUT-M6 x100", fill=(0, 0, 0), font=font(17, mono=True))
d.text((35, 240), "C3 WASHER x200", fill=(0, 0, 0), font=font(17, mono=True))
d.text((35, 275), "C4 GLUE-X x10", fill=(0, 0, 0), font=font(17, mono=True))
d.text((35, 310), "C5 MIX SPARE", fill=(0, 0, 0), font=font(17, mono=True))
d.text((35, 370), "TRACKING TRK-77821 FRAGILE", fill=(0, 0, 140), font=font(20, bold=True))
g = "PACKING LIST PL-2201 Cartons 5 Weight 42.5 kg TRACKING TRK-77821 FRAGILE"
made.append(save(img, "v3-ocr-plist-001", {"task": "ocr", "ocr_text": g, "gold": g}))

# KPI board caption denser
img = Image.new("RGB", (760, 420), (240, 242, 246))
d = ImageDraw.Draw(img)
d.text((24, 16), "PLANT KPI BOARD", fill=(10, 10, 30), font=font(24, bold=True))
kpis = [
    (30, 70, 200, 180, "Throughput", "412"),
    (220, 70, 390, 180, "Defectppm", "180"),
    (410, 70, 580, 180, "OTIF", "91%"),
    (600, 70, 740, 180, "WIP", "67"),
]
for x0b, y0, x1, y1, title, val in kpis:
    d.rectangle([x0b, y0, x1, y1], fill=(255, 255, 255), outline=(30, 30, 50), width=2)
    d.text((x0b + 12, y0 + 16), title, fill=(70, 70, 90), font=font(15))
    d.text((x0b + 12, y0 + 55), val, fill=(10, 10, 30), font=font(30, bold=True))
d.text((30, 220), "Alert: Bay 4 conveyor jam + Line B feeder jam", fill=(180, 0, 0), font=font(18, bold=True))
d.text((30, 270), "Shift Night  Owner OPS+MFG", fill=(30, 30, 30), font=font(18))
d.text((30, 320), "Updated 2026-10-18 23:10 Asia/Shanghai", fill=(60, 60, 60), font=font(16))
g = "PLANT KPI BOARD Throughput 412 Defectppm 180 OTIF 91% WIP 67 Alert Bay 4 conveyor jam"
made.append(save(img, "v3-caption-kpi-001", {"task": "caption", "caption": g, "gold": g}))

# defect dense table 5 cols
img = Image.new("RGB", (780, 380), (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((16, 12), "DEFECT DENSE", fill=(0, 0, 0), font=font(20, bold=True))
headers = ["id", "area", "sev", "status", "owner"]
rows = [
    ["D01", "Paint", "H", "open", "Mei"],
    ["D02", "Weld", "M", "fixed", "Jon"],
    ["D03", "Seal", "H", "open", "Lia"],
    ["D04", "Bolt", "L", "open", "Kai"],
    ["D05", "Wire", "M", "fixed", "Ann"],
]
x0 = [20, 100, 240, 340, 480]
for i, h in enumerate(headers):
    d.text((x0[i], 50), h, fill=(120, 0, 0), font=font(16, bold=True, mono=True))
y = 90
for row in rows:
    for i, cell in enumerate(row):
        d.text((x0[i], y), cell, fill=(0, 0, 0), font=font(16, mono=True))
    y += 40
cg = "id,area,sev,status,owner\n" + "\n".join(",".join(r) for r in rows)
made.append(save(img, "v3-table-def5-001", {"task": "table_cells", "cells_csv": cg, "gold": cg}))

# UI settings denser caption
img = Image.new("RGB", (640, 400), (26, 28, 34))
d = ImageDraw.Draw(img)
d.text((36, 24), "Secure Gateway", fill=(240, 240, 240), font=font(24, bold=True))
d.text((36, 90), "SSH keys", fill=(220, 220, 220), font=font(20))
d.rectangle([420, 85, 520, 125], fill=(40, 180, 80), outline=(20, 100, 40), width=2)
d.text((36, 150), "Root login", fill=(220, 220, 220), font=font(20))
d.rectangle([420, 145, 520, 185], fill=(80, 80, 90), outline=(40, 40, 50), width=2)
d.text((36, 210), "MFA", fill=(220, 220, 220), font=font(20))
d.rectangle([420, 205, 520, 245], fill=(40, 180, 80), outline=(20, 100, 40), width=2)
d.text((36, 290), "ssh ON root OFF mfa ON", fill=(180, 180, 180), font=font(18))
g = "Secure Gateway SSH keys ON Root login OFF MFA ON"
made.append(save(img, "v3-ui-secure-001", {"task": "caption", "caption": g, "gold": g}))

# receipt OCR
img = Image.new("RGB", (520, 560), (255, 255, 255))
d = ImageDraw.Draw(img)
d.rectangle([10, 10, 510, 550], outline=(0, 0, 0), width=2)
d.text((40, 30), "RECEIPT R-3099", fill=(0, 0, 0), font=font(22, bold=True))
d.text((40, 80), "Store: Ant Mart #12", fill=(0, 0, 0), font=font(18))
d.text((40, 120), "Coffee  x2  6.00", fill=(0, 0, 0), font=font(17, mono=True))
d.text((40, 155), "Bun     x1  2.50", fill=(0, 0, 0), font=font(17, mono=True))
d.text((40, 190), "Water   x3  4.50", fill=(0, 0, 0), font=font(17, mono=True))
d.text((40, 240), "Subtotal 13.00", fill=(0, 0, 0), font=font(18))
d.text((40, 280), "Tax 1.04", fill=(0, 0, 0), font=font(18))
d.text((40, 330), "PAID TOTAL 14.04", fill=(0, 100, 0), font=font(22, bold=True))
d.text((40, 390), "Card ****4412", fill=(0, 0, 0), font=font(18))
d.text((40, 430), "2026-10-18 21:05", fill=(40, 40, 40), font=font(16))
g = "RECEIPT R-3099 Subtotal 13.00 Tax 1.04 PAID TOTAL 14.04 Card 4412"
made.append(save(img, "v3-ocr-receipt-001", {"task": "ocr", "ocr_text": g, "gold": g}))

# schedule table
img = Image.new("RGB", (720, 340), (252, 252, 255))
d = ImageDraw.Draw(img)
d.text((16, 12), "BAY SCHEDULE", fill=(0, 0, 0), font=font(20, bold=True))
headers = ["bay", "job", "start", "end", "owner"]
rows = [
    ["1", "Pick", "08:00", "10:00", "Ann"],
    ["2", "Pack", "09:00", "12:00", "Jon"],
    ["4", "QA", "10:00", "13:00", "Lia"],
    ["7", "Ship", "13:00", "16:00", "Kai"],
]
x0 = [20, 100, 240, 360, 500]
for i, h in enumerate(headers):
    d.text((x0[i], 55), h, fill=(0, 0, 100), font=font(16, bold=True, mono=True))
y = 95
for row in rows:
    for i, cell in enumerate(row):
        d.text((x0[i], y), cell, fill=(0, 0, 0), font=font(16, mono=True))
    y += 40
cg = "bay,job,start,end,owner\n" + "\n".join(",".join(r) for r in rows)
made.append(save(img, "v3-table-sched-001", {"task": "table_cells", "cells_csv": cg, "gold": cg}))

payload = {
    "kind": "r50plus_c73_vision_v3_dense_fixtures",
    "timestamp": ts(),
    "gate": GATE,
    "n": len(made),
    "fixtures": made,
    "dir": "evo/office/fixtures/vision_images_v3_dense",
    "innovation": "Harder denser OCR/tables than V2 heldout; honest drawn",
    "vl_gate_v3_claim": False,
    "gate2_3_untouched": True,
    "v1_v2_claims_untouched": True,
}
(ROOT / "docs/r50").mkdir(parents=True, exist_ok=True)
(ROOT / "docs/r50/C73_vision_v3_dense_fixtures.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps({"n": len(made), "ids": [m["id"] for m in made]}, ensure_ascii=False))
