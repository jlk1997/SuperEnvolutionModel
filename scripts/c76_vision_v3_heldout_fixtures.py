# -*- coding: utf-8 -*-
"""C76: V3 heldout harder set — denser/smaller/noisier than V3 dense train. Disjoint IDs."""
from __future__ import annotations
import hashlib, json, random
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
GATE = 0.6
OUT = ROOT / "evo/office/fixtures/vision_images_v3_heldout"
TRAIN = ROOT / "evo/office/fixtures/vision_images_v3_dense"


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


def noise(img, seed=7, dens=0.012):
    rnd = random.Random(seed)
    px = img.load()
    w, h = img.size
    n = int(w * h * dens)
    for _ in range(n):
        x, y = rnd.randrange(w), rnd.randrange(h)
        c = px[x, y]
        d = rnd.randint(-28, 28)
        px[x, y] = tuple(max(0, min(255, ch + d)) for ch in c)
    return img


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
        "v3_heldout": True,
        "harder_than_v3_dense": True,
        "disjoint_from_v3_dense": True,
        "source": "c76_vision_v3_heldout",
        "timestamp": ts(),
        "gold": meta.get("gold") or meta.get(key) or "",
    }
    (OUT / f"{name}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"id": name, "png_bytes": png.stat().st_size, "task": meta["task"], "gold": meta["gold"]}


def main():
    # ensure disjoint from train IDs
    train_ids = {p.stem for p in TRAIN.glob("*.png")} if TRAIN.is_dir() else set()
    made = []

    # 7-col dense stock (smaller font) — heldout
    img = Image.new("RGB", (980, 460), (250, 250, 252))
    d = ImageDraw.Draw(img)
    d.text((14, 8), "STOCK MATRIX HELD 7C", fill=(0, 0, 0), font=font(18, bold=True))
    headers = ["bin", "sku", "onhand", "rsv", "avail", "zone", "lot"]
    rows = [
        ["F1", "CAP-M8", "220", "18", "202", "N", "L41"],
        ["F2", "SPRING-Q", "90", "9", "81", "E", "L42"],
        ["G3", "BUSH-22", "340", "40", "300", "S", "L43"],
        ["H1", "SEAL-R", "75", "5", "70", "W", "L44"],
        ["H4", "PIN-T5", "610", "60", "550", "N", "L45"],
        ["J2", "CLIP-Z", "48", "8", "40", "E", "L46"],
        ["K9", "HOSE-9", "16", "2", "14", "S", "L47"],
    ]
    x0 = [14, 70, 200, 340, 420, 520, 620]
    for i, h in enumerate(headers):
        d.text((x0[i], 42), h, fill=(0, 0, 110), font=font(13, bold=True, mono=True))
    y = 72
    for row in rows:
        for i, cell in enumerate(row):
            d.text((x0[i], y), cell, fill=(0, 0, 0), font=font(13, mono=True))
        y += 32
    img = noise(img, seed=11)
    cg = "bin,sku,onhand,rsv,avail,zone,lot\n" + "\n".join(",".join(r) for r in rows)
    made.append(save(img, "v3h-table-stock7-001", {"task": "table_cells", "cells_csv": cg, "gold": cg, "domain": "dense_table"}))

    # multi-block PO OCR denser
    img = Image.new("RGB", (760, 620), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 750, 610], outline=(0, 0, 0), width=2)
    d.text((28, 22), "PURCHASE ORDER PO-7703", fill=(0, 0, 0), font=font(22, bold=True))
    d.text((28, 62), "Vendor: North Alloy Works", fill=(0, 0, 0), font=font(16))
    d.text((28, 90), "Ship: East Cold Bay 3", fill=(0, 0, 0), font=font(16))
    lines = [
        "L1 CAP-M8   qty 80  @ 1.10 = 88.00",
        "L2 SPRING-Q qty 40  @ 2.40 = 96.00",
        "L3 BUSH-22  qty 20  @ 4.50 = 90.00",
        "L4 SEAL-R   qty 25  @ 3.20 = 80.00",
        "L5 PIN-T5   qty 100 @ 0.55 = 55.00",
    ]
    y = 140
    for ln in lines:
        d.text((28, y), ln, fill=(0, 0, 0), font=font(15, mono=True))
        y += 30
    d.text((28, 320), "Subtotal 409.00", fill=(0, 0, 0), font=font(17))
    d.text((28, 355), "Freight 27.50", fill=(0, 0, 0), font=font(17))
    d.text((28, 400), "GRAND TOTAL USD 436.50", fill=(140, 0, 0), font=font(20, bold=True))
    d.text((28, 450), "Need by 2026-11-20  Terms Net 45", fill=(0, 0, 0), font=font(16))
    d.text((28, 490), "Buyer Ref BR-441  Approver Lia", fill=(40, 40, 40), font=font(15))
    d.text((28, 540), "DO NOT PARTIAL SHIP", fill=(120, 0, 0), font=font(16, bold=True))
    img = noise(img, seed=22, dens=0.008)
    g = "PURCHASE ORDER PO-7703 Subtotal 409.00 Freight 27.50 GRAND TOTAL USD 436.50 Need by 2026-11-20"
    made.append(save(img, "v3h-ocr-po7703-001", {"task": "ocr", "ocr_text": g, "gold": g, "domain": "ocr"}))

    # packing slip OCR
    img = Image.new("RGB", (700, 500), (255, 252, 240))
    d = ImageDraw.Draw(img)
    d.rectangle([12, 12, 688, 488], outline=(0, 0, 0), width=3)
    d.text((30, 28), "SHIPPING SLIP SS-501", fill=(0, 0, 0), font=font(22, bold=True))
    d.text((30, 75), "From Ant East  To Harbor Gate 7", fill=(0, 0, 0), font=font(17))
    d.text((30, 115), "Pallets 3  Gross 118.2 kg", fill=(0, 0, 0), font=font(17))
    for i, ln in enumerate(["P1 CAP-M8 x200", "P2 SPRING-Q x80", "P3 MIX BUSH+SEAL"]):
        d.text((30, 165 + i * 34), ln, fill=(0, 0, 0), font=font(16, mono=True))
    d.text((30, 290), "TRACKING TRK-99014 HANDLE WITH CARE", fill=(0, 0, 130), font=font(18, bold=True))
    d.text((30, 340), "Seal code GEN11-HOLD", fill=(80, 0, 0), font=font(16))
    d.text((30, 390), "Depart 2026-10-19 06:40 Asia/Shanghai", fill=(40, 40, 40), font=font(15))
    img = noise(img, seed=33)
    g = "SHIPPING SLIP SS-501 Pallets 3 Gross 118.2 kg TRACKING TRK-99014 HANDLE WITH CARE"
    made.append(save(img, "v3h-ocr-ship-001", {"task": "ocr", "ocr_text": g, "gold": g, "domain": "ocr"}))

    # KPI caption harder
    img = Image.new("RGB", (800, 440), (232, 236, 242))
    d = ImageDraw.Draw(img)
    d.text((20, 14), "LINE HEALTH BOARD", fill=(10, 10, 30), font=font(22, bold=True))
    kpis = [
        (24, 60, 190, 170, "OEE", "84%"),
        (210, 60, 380, 170, "Scrap", "2.1%"),
        (400, 60, 570, 170, "Cycle", "46s"),
        (590, 60, 770, 170, "Queue", "23"),
    ]
    for x0b, y0, x1, y1, title, val in kpis:
        d.rectangle([x0b, y0, x1, y1], fill=(255, 255, 255), outline=(20, 30, 50), width=2)
        d.text((x0b + 10, y0 + 14), title, fill=(70, 70, 90), font=font(14))
        d.text((x0b + 10, y0 + 50), val, fill=(10, 10, 30), font=font(28, bold=True))
    d.text((24, 200), "Alert: Feeder jam Line C + Vision cam offline Bay 9", fill=(170, 0, 0), font=font(17, bold=True))
    d.text((24, 250), "Shift Day  Owner MFG+QA", fill=(20, 20, 20), font=font(16))
    d.text((24, 295), "Updated 2026-10-19 00:05 Asia/Shanghai", fill=(50, 50, 50), font=font(15))
    d.text((24, 340), "Action: reroute to Bay 2 until cam back", fill=(0, 60, 0), font=font(15))
    img = noise(img, seed=44, dens=0.01)
    g = "LINE HEALTH BOARD OEE 84% Scrap 2.1% Cycle 46s Queue 23 Alert Feeder jam Line C"
    made.append(save(img, "v3h-caption-line-001", {"task": "caption", "caption": g, "gold": g, "domain": "caption"}))

    # defect 6-col table
    img = Image.new("RGB", (900, 400), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((14, 10), "DEFECT MATRIX HELD", fill=(0, 0, 0), font=font(18, bold=True))
    headers = ["id", "area", "sev", "status", "owner", "eta"]
    rows = [
        ["X11", "Coat", "H", "open", "Rui", "10:00"],
        ["X12", "Weld", "M", "wip", "Jon", "11:30"],
        ["X13", "Seal", "H", "open", "Lia", "12:00"],
        ["X14", "Wire", "L", "fixed", "Ann", "done"],
        ["X15", "Bolt", "M", "open", "Kai", "14:00"],
        ["X16", "Lens", "H", "wip", "Mei", "15:20"],
    ]
    x0 = [16, 90, 200, 280, 400, 520]
    for i, h in enumerate(headers):
        d.text((x0[i], 48), h, fill=(120, 0, 0), font=font(14, bold=True, mono=True))
    y = 82
    for row in rows:
        for i, cell in enumerate(row):
            d.text((x0[i], y), cell, fill=(0, 0, 0), font=font(14, mono=True))
        y += 36
    img = noise(img, seed=55)
    cg = "id,area,sev,status,owner,eta\n" + "\n".join(",".join(r) for r in rows)
    made.append(save(img, "v3h-table-def6-001", {"task": "table_cells", "cells_csv": cg, "gold": cg, "domain": "dense_table"}))

    # UI caption denser
    img = Image.new("RGB", (660, 420), (22, 24, 30))
    d = ImageDraw.Draw(img)
    d.text((32, 22), "Edge Firewall Panel", fill=(235, 235, 235), font=font(22, bold=True))
    rows_ui = [
        ("TLS 1.3", True),
        ("VPN only", True),
        ("Guest WiFi", False),
        ("Auto-update", True),
    ]
    y = 80
    for label, on in rows_ui:
        d.text((36, y), label, fill=(220, 220, 220), font=font(18))
        color = (40, 180, 80) if on else (80, 80, 90)
        d.rectangle([480, y - 4, 580, y + 30], fill=color, outline=(40, 40, 50), width=2)
        y += 55
    d.text((36, 320), "tls ON vpn ON guest OFF update ON", fill=(170, 170, 170), font=font(16))
    img = noise(img, seed=66, dens=0.006)
    g = "Edge Firewall Panel TLS 1.3 ON VPN only ON Guest WiFi OFF Auto-update ON"
    made.append(save(img, "v3h-ui-fw-001", {"task": "caption", "caption": g, "gold": g, "domain": "caption"}))

    # receipt OCR harder
    img = Image.new("RGB", (540, 600), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, 532, 592], outline=(0, 0, 0), width=2)
    d.text((36, 24), "RECEIPT R-7712", fill=(0, 0, 0), font=font(20, bold=True))
    d.text((36, 70), "Store: Harbor Mart #4", fill=(0, 0, 0), font=font(16))
    items = [
        "Tea     x2  5.00",
        "Bread   x1  3.20",
        "Milk    x2  6.40",
        "Soap    x1  2.80",
        "Bag     x3  4.50",
    ]
    y = 115
    for ln in items:
        d.text((36, y), ln, fill=(0, 0, 0), font=font(15, mono=True))
        y += 30
    d.text((36, 290), "Subtotal 21.90", fill=(0, 0, 0), font=font(16))
    d.text((36, 325), "Tax 1.75", fill=(0, 0, 0), font=font(16))
    d.text((36, 370), "PAID TOTAL 23.65", fill=(0, 90, 0), font=font(20, bold=True))
    d.text((36, 420), "Card ****8821", fill=(0, 0, 0), font=font(16))
    d.text((36, 460), "2026-10-19 00:12 Asia/Shanghai", fill=(40, 40, 40), font=font(14))
    d.text((36, 510), "Cashier: 09  Lane: 3", fill=(40, 40, 40), font=font(14))
    img = noise(img, seed=77)
    g = "RECEIPT R-7712 Subtotal 21.90 Tax 1.75 PAID TOTAL 23.65 Card 8821"
    made.append(save(img, "v3h-ocr-rcpt-001", {"task": "ocr", "ocr_text": g, "gold": g, "domain": "ocr"}))

    # schedule 6-col
    img = Image.new("RGB", (860, 360), (250, 252, 255))
    d = ImageDraw.Draw(img)
    d.text((14, 10), "DOCK WINDOW HELD", fill=(0, 0, 0), font=font(18, bold=True))
    headers = ["dock", "job", "start", "end", "truck", "owner"]
    rows = [
        ["A", "Unload", "06:00", "08:00", "T-12", "Ann"],
        ["B", "Load", "07:30", "10:00", "T-19", "Jon"],
        ["C", "QA", "09:00", "11:30", "T-04", "Lia"],
        ["D", "Ship", "11:00", "14:00", "T-22", "Kai"],
        ["E", "Hold", "14:00", "16:00", "T-08", "Mei"],
    ]
    x0 = [16, 90, 200, 320, 440, 580]
    for i, h in enumerate(headers):
        d.text((x0[i], 48), h, fill=(0, 0, 100), font=font(14, bold=True, mono=True))
    y = 84
    for row in rows:
        for i, cell in enumerate(row):
            d.text((x0[i], y), cell, fill=(0, 0, 0), font=font(14, mono=True))
        y += 36
    img = noise(img, seed=88)
    cg = "dock,job,start,end,truck,owner\n" + "\n".join(",".join(r) for r in rows)
    made.append(save(img, "v3h-table-dock-001", {"task": "table_cells", "cells_csv": cg, "gold": cg, "domain": "dense_table"}))

    # credit memo OCR
    img = Image.new("RGB", (700, 480), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 690, 470], outline=(0, 0, 0), width=2)
    d.text((28, 24), "CREDIT MEMO CM-4408", fill=(0, 0, 0), font=font(22, bold=True))
    d.text((28, 70), "Customer: West Plant Co", fill=(0, 0, 0), font=font(16))
    d.text((28, 105), "Reason: Short ship qty", fill=(0, 0, 0), font=font(16))
    d.text((28, 150), "Item CAP-M8 qty 10 @ 1.10 = 11.00", fill=(0, 0, 0), font=font(15, mono=True))
    d.text((28, 185), "Item SEAL-R  qty 4  @ 3.20 = 12.80", fill=(0, 0, 0), font=font(15, mono=True))
    d.text((28, 230), "Credit subtotal 23.80", fill=(0, 0, 0), font=font(16))
    d.text((28, 270), "CREDIT TOTAL 23.80", fill=(0, 100, 0), font=font(20, bold=True))
    d.text((28, 320), "Issued 2026-10-19  Ref INV-88421", fill=(0, 0, 0), font=font(15))
    d.text((28, 360), "Approver: Rui", fill=(40, 40, 40), font=font(15))
    img = noise(img, seed=99)
    g = "CREDIT MEMO CM-4408 Credit subtotal 23.80 CREDIT TOTAL 23.80 Issued 2026-10-19"
    made.append(save(img, "v3h-ocr-credit-001", {"task": "ocr", "ocr_text": g, "gold": g, "domain": "ocr"}))

    # conflict check
    overlap = [m["id"] for m in made if m["id"] in train_ids]
    if overlap:
        raise SystemExit(f"ID overlap with v3_dense: {overlap}")

    payload = {
        "kind": "r50plus_c76_vision_v3_heldout_fixtures",
        "timestamp": ts(),
        "gate": GATE,
        "n": len(made),
        "fixtures": made,
        "dir": "evo/office/fixtures/vision_images_v3_heldout",
        "disjoint_from": "evo/office/fixtures/vision_images_v3_dense",
        "train_ids_seen": sorted(train_ids),
        "overlap": overlap,
        "innovation": "Harder heldout than V3 dense: more cols, smaller fonts, mild noise, new IDs",
        "vl_gate_v3_heldout_claim": False,
        "gate2_3_untouched": True,
        "v1_v2_v3_claims_untouched": True,
    }
    (ROOT / "docs/r50").mkdir(parents=True, exist_ok=True)
    (ROOT / "docs/r50/C76_vision_v3_heldout_fixtures.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"n": len(made), "ids": [m["id"] for m in made], "overlap": overlap}, ensure_ascii=False))


if __name__ == "__main__":
    main()
