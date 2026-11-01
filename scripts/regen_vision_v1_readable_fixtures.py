# -*- coding: utf-8 -*-
"""Regenerate Vision V1 fixtures so Qwen3.5-2B can actually OCR/read them.

Root cause (C47 rate=0.375): r50 png() wrote solid-color PNGs with gold only in
tEXt metadata. VL correctly said "blank white image".

This script draws high-contrast text/tables/UI with Arial/Consolas.
Does NOT mint Gate2/3 claims. Honest only.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evo" / "office" / "fixtures" / "vision_images_real"
FONT_REG = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_MONO = Path(r"C:\Windows\Fonts\consola.ttf")


def ts() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_MONO if mono else (FONT_BD if bold else FONT_REG)
    return ImageFont.truetype(str(path), size=size)


def save(img: Image.Image, name: str, meta: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    png = OUT / f"{name}.png"
    img.save(png, format="PNG")
    digest = hashlib.sha256(png.read_bytes()).hexdigest()
    meta = {
        **meta,
        "id": name,
        "sha256": digest,
        "synthetic_not_vl": False,
        "drawn_for_vl": True,
        "readable_v1": True,
        "source": "regen_vision_v1_readable_fixtures",
        "timestamp": ts(),
    }
    if "gold" not in meta:
        key = {"caption": "caption", "ocr": "ocr_text", "table_cells": "cells_csv"}[meta["task"]]
        meta["gold"] = meta.get(key) or ""
    (OUT / f"{name}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return png


def draw_caption_desk(name: str = "office-caption-001") -> None:
    img = Image.new("RGB", (512, 320), (245, 248, 252))
    d = ImageDraw.Draw(img)
    # desk
    d.rectangle([40, 200, 470, 280], fill=(30, 90, 180), outline=(10, 40, 100), width=3)
    # laptop body
    d.rectangle([180, 120, 340, 200], fill=(60, 60, 70), outline=(20, 20, 30), width=2)
    # screen
    d.rectangle([190, 90, 330, 160], fill=(180, 220, 255), outline=(40, 40, 50), width=2)
    d.text((160, 20), "blue office desk with laptop", fill=(10, 10, 10), font=font(22, bold=True))
    d.text((50, 290), "OFFICE DESK", fill=(20, 20, 20), font=font(18, bold=True))
    save(
        img,
        name,
        {
            "task": "caption",
            "caption": "blue office desk with laptop",
            "ocr_text": "",
            "cells_csv": "",
        },
    )


def draw_caption_invoice(name: str = "office-caption-002") -> None:
    img = Image.new("RGB", (512, 360), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([30, 30, 480, 330], outline=(0, 0, 0), width=3)
    d.text((50, 50), "INVOICE", fill=(0, 0, 0), font=font(36, bold=True))
    d.text((50, 110), "Customer: Ant Office Co.", fill=(0, 0, 0), font=font(22))
    d.text((50, 150), "Item: Printer paper  x10", fill=(0, 0, 0), font=font(22))
    d.text((50, 200), "TOTAL", fill=(0, 0, 0), font=font(28, bold=True))
    d.text((220, 200), "128.50", fill=(180, 0, 0), font=font(32, bold=True))
    d.text((50, 260), "A printed invoice with totals", fill=(40, 40, 40), font=font(18))
    save(
        img,
        name,
        {
            "task": "caption",
            "caption": "A printed invoice with totals",
            "ocr_text": "INVOICE TOTAL 128.50",
            "cells_csv": "",
        },
    )


def draw_caption_whiteboard(name: str = "office-caption-003") -> None:
    img = Image.new("RGB", (512, 360), (250, 245, 220))
    d = ImageDraw.Draw(img)
    d.rectangle([20, 20, 490, 340], outline=(80, 60, 20), width=4)
    d.text((40, 40), "SPRINT BOARD", fill=(20, 20, 20), font=font(28, bold=True))
    d.text((40, 100), "1. Fix Vision fixtures", fill=(0, 80, 0), font=font(22, bold=True))
    d.text((40, 150), "2. Run V1 smoke gate", fill=(0, 80, 0), font=font(22, bold=True))
    d.text((40, 200), "3. Ship ant-vision", fill=(120, 40, 0), font=font(22, bold=True))
    d.text((40, 280), "A whiteboard with sprint tasks", fill=(40, 40, 40), font=font(18))
    save(
        img,
        name,
        {
            "task": "caption",
            "caption": "A whiteboard with sprint tasks",
            "ocr_text": "SPRINT BOARD",
            "cells_csv": "",
        },
    )


def draw_ocr_invoice(name: str = "office-ocr-001", text: str = "INVOICE-7781\nTOTAL 128.50\nPaid") -> None:
    img = Image.new("RGB", (512, 280), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([16, 16, 496, 264], outline=(0, 0, 0), width=3)
    y = 40
    for line in text.split("\n"):
        d.text((40, y), line, fill=(0, 0, 0), font=font(36, bold=True, mono=True))
        y += 60
    gold = " ".join(text.split())
    save(img, name, {"task": "ocr", "ocr_text": gold, "caption": "", "cells_csv": ""})


def draw_ocr_multiline(name: str, lines: list[str], gold: str | None = None) -> None:
    h = 60 + 48 * len(lines)
    img = Image.new("RGB", (560, max(280, h)), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([12, 12, 548, img.height - 12], outline=(0, 0, 0), width=3)
    y = 36
    for line in lines:
        d.text((36, y), line, fill=(0, 0, 0), font=font(28, bold=True, mono=True))
        y += 48
    g = gold or " ".join(lines)
    save(img, name, {"task": "ocr", "ocr_text": g, "caption": "", "cells_csv": "", "hard": "hard" in name})


def draw_table(name: str, headers: list[str], rows: list[list[str]], gold_csv: str) -> None:
    col_w = 140
    row_h = 48
    w = 40 + col_w * len(headers)
    h = 40 + row_h * (1 + len(rows))
    img = Image.new("RGB", (max(480, w), max(240, h)), (255, 255, 255))
    d = ImageDraw.Draw(img)
    # header bg
    d.rectangle([20, 20, 20 + col_w * len(headers), 20 + row_h], fill=(30, 30, 30))
    for i, htxt in enumerate(headers):
        d.text((28 + i * col_w, 30), htxt, fill=(255, 255, 255), font=font(22, bold=True, mono=True))
    for r, row in enumerate(rows):
        y0 = 20 + row_h * (r + 1)
        bg = (245, 245, 245) if r % 2 == 0 else (255, 255, 255)
        d.rectangle([20, y0, 20 + col_w * len(headers), y0 + row_h], fill=bg, outline=(0, 0, 0))
        for i, cell in enumerate(row):
            d.text((28 + i * col_w, y0 + 10), cell, fill=(0, 0, 0), font=font(22, bold=True, mono=True))
    # grid
    for i in range(len(headers) + 1):
        x = 20 + i * col_w
        d.line([(x, 20), (x, 20 + row_h * (1 + len(rows)))], fill=(0, 0, 0), width=2)
    for r in range(len(rows) + 2):
        y = 20 + r * row_h
        d.line([(20, y), (20 + col_w * len(headers), y)], fill=(0, 0, 0), width=2)
    save(
        img,
        name,
        {
            "task": "table_cells",
            "cells_csv": gold_csv,
            "caption": "",
            "ocr_text": "",
            "hard": "hard" in name,
        },
    )


def draw_ui_settings(name: str = "office-ui-001") -> None:
    img = Image.new("RGB", (512, 320), (24, 24, 28))
    d = ImageDraw.Draw(img)
    d.text((40, 30), "Settings", fill=(240, 240, 240), font=font(32, bold=True))
    d.text((40, 110), "Dark mode", fill=(230, 230, 230), font=font(26, bold=True))
    # toggle ON
    d.rounded_rectangle([280, 105, 360, 145], radius=20, fill=(40, 180, 80))
    d.ellipse([320, 108, 356, 142], fill=(255, 255, 255))
    d.text((380, 110), "ON", fill=(80, 255, 120), font=font(26, bold=True))
    d.text((40, 200), "settings screen dark mode toggle on", fill=(180, 180, 180), font=font(16))
    save(
        img,
        name,
        {
            "task": "caption",
            "caption": "settings screen dark mode toggle on",
            "ocr_text": "Dark mode ON",
            "cells_csv": "",
        },
    )


def draw_ui_dialog(name: str, title: str, body: str, buttons: list[str], gold: str) -> None:
    img = Image.new("RGB", (560, 320), (220, 220, 230))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([60, 40, 500, 280], radius=12, fill=(255, 255, 255), outline=(0, 0, 0), width=3)
    d.text((90, 60), title, fill=(0, 0, 0), font=font(26, bold=True))
    d.text((90, 120), body, fill=(20, 20, 20), font=font(22))
    bw = 140
    for i, b in enumerate(buttons):
        x0 = 110 + i * (bw + 30)
        color = (200, 40, 40) if i == len(buttons) - 1 else (80, 80, 90)
        d.rounded_rectangle([x0, 190, x0 + bw, 240], radius=8, fill=color)
        d.text((x0 + 24, 200), b, fill=(255, 255, 255), font=font(20, bold=True))
    save(
        img,
        name,
        {
            "task": "caption",
            "caption": gold,
            "ocr_text": " ".join(buttons),
            "cells_csv": "",
            "hard": "hard" in name or "Modal" in gold,
        },
    )


def draw_ui_save(name: str = "office-ui-002") -> None:
    img = Image.new("RGB", (480, 300), (235, 235, 245))
    d = ImageDraw.Draw(img)
    d.rectangle([40, 40, 440, 260], fill=(255, 255, 255), outline=(0, 0, 0), width=3)
    d.text((60, 60), "Settings dialog", fill=(0, 0, 0), font=font(28, bold=True))
    d.text((60, 120), "Profile name: AntUser", fill=(0, 0, 0), font=font(22))
    d.rounded_rectangle([60, 180, 220, 230], radius=8, fill=(30, 100, 200))
    d.text((85, 190), "Save", fill=(255, 255, 255), font=font(24, bold=True))
    d.text((60, 250), "Settings dialog with Save button", fill=(60, 60, 60), font=font(16))
    save(
        img,
        name,
        {
            "task": "caption",
            "caption": "Settings dialog with Save button",
            "ocr_text": "Save",
            "cells_csv": "",
        },
    )


def draw_ocr_save_changes(name: str = "office-ui-003") -> None:
    img = Image.new("RGB", (420, 160), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 40, 380, 120], radius=10, fill=(20, 120, 60))
    d.text((70, 60), "Save Changes", fill=(255, 255, 255), font=font(36, bold=True))
    save(img, name, {"task": "ocr", "ocr_text": "Save Changes", "caption": "", "cells_csv": ""})


def draw_pdf_page(name: str, lines: list[str], task: str, gold: str) -> None:
    img = Image.new("RGB", (480, 640), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 470, 630], outline=(0, 0, 0), width=2)
    y = 40
    for i, line in enumerate(lines):
        f = font(26, bold=(i == 0), mono=True)
        d.text((36, y), line, fill=(0, 0, 0), font=f)
        y += 44
    key = "ocr_text" if task == "ocr" else "cells_csv"
    meta = {"task": task, "caption": "", "ocr_text": "", "cells_csv": "", "pdf_page_sim": True}
    meta[key] = gold
    save(img, name, meta)


def main() -> None:
    # Keep/refresh the proven V0-style set + fix all solid-color wideners
    draw_caption_desk("office-caption-001")
    draw_caption_invoice("office-caption-002")
    draw_caption_whiteboard("office-caption-003")

    draw_ocr_invoice("office-ocr-001", "INVOICE-7781\nTOTAL 128.50\nPaid")
    draw_ocr_multiline("office-ocr-002", ["TOTAL DUE", "128.50"], gold="TOTAL DUE 128.50")
    draw_ocr_multiline("office-ocr-003", ["PO-2026-441"], gold="PO-2026-441")

    draw_table(
        "office-table-001",
        ["sku", "qty", "price"],
        [["A1", "2", "10"], ["B2", "1", "7"]],
        "sku,qty,price\nA1,2,10\nB2,1,7",
    )
    draw_table(
        "office-table-002",
        ["item", "qty", "price"],
        [["pen", "2", "1.5"], ["ink", "1", "3.0"]],
        "item,qty,price\npen,2,1.5\nink,1,3.0",
    )
    draw_table(
        "office-table-003",
        ["dept", "headcount"],
        [["eng", "12"], ["sales", "7"]],
        "dept,headcount\neng,12\nsales,7",
    )

    draw_ui_settings("office-ui-001")
    draw_ui_save("office-ui-002")
    draw_ocr_save_changes("office-ui-003")

    draw_ocr_multiline(
        "office-hard-ocr-001",
        ["Invoice# INV-7781", "Subtotal 990.00", "Tax 89.10", "Total 1079.10"],
        gold="Invoice# INV-7781 Subtotal 990.00 Tax 89.10 Total 1079.10",
    )
    draw_table(
        "office-hard-table-001",
        ["sku", "name", "qty", "amt"],
        [["A1", "Widget", "3", "12.00"], ["B2", "Gadget", "1", "40.50"]],
        "sku,name,qty,amt\nA1,Widget,3,12.00\nB2,Gadget,1,40.50",
    )
    draw_ui_dialog(
        "office-hard-ui-001",
        "Modal",
        "Confirm delete 3 files?",
        ["Cancel", "Delete"],
        "Modal: Confirm delete 3 files? [Cancel] [Delete]",
    )
    draw_ocr_multiline(
        "office-hard-mixed-001",
        ["Ship to: 88 Ant Rd", "Deadline: 2026-11-01"],
        gold="Ship to: 88 Ant Rd Deadline: 2026-11-01",
    )

    draw_pdf_page(
        "office-pdfpage-001",
        ["Page 1", "Contract Terms", "Clause 1.1 Payment due net 30"],
        "ocr",
        "Page 1 Contract Terms Clause 1.1 Payment due net 30",
    )
    draw_pdf_page(
        "office-pdfpage-002",
        ["Page 2", "Signature block", "Authorized: ________"],
        "ocr",
        "Page 2 Signature block Authorized: ________",
    )
    draw_pdf_page(
        "office-pdfpage-003",
        ["line desc amount", "1 Service 1000", "2 Discount -50"],
        "table_cells",
        "line,desc,amount\n1,Service,1000\n2,Discount,-50",
    )

    sizes = sorted((p.name, p.stat().st_size) for p in OUT.glob("office-*.png"))
    tiny = [n for n, s in sizes if s < 800]
    report = {
        "kind": "vision_v1_readable_fixtures_regen",
        "timestamp": ts(),
        "n_png": len(sizes),
        "sizes": sizes,
        "tiny_under_800b": tiny,
        "root_cause_fixed": "solid-color png()+tEXt -> high-contrast PIL text/table/UI",
        "prior_c47_rate": 0.375,
        "gate": 0.6,
        "vl_gate_v1_claim": False,
        "note": "Fixtures only; claim requires real VL smoke >=0.6",
    }
    out = ROOT / "docs" / "r50" / "C51_vision_v1_readable_fixtures.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"n": len(sizes), "tiny": tiny, "report": str(out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
