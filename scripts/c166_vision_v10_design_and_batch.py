# -*- coding: utf-8 -*-
"""C166: Vision V10 design + fixtures (harder than V9).
Hardening: sticky occlusion, coffee stain, 3-window z-order, faded ink,
chat bait sidebar, fold crease, tiny footnote bait, calendar crosstalk.
Gate 0.6. Gate2/3 untouched. gen11 HOLD. No claim until real VL smoke.
"""
from __future__ import annotations
import json, random, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v10"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V10_PROTOCOL.md"
RUN = ROOT / "runs/vision_v10_c166"

SPECS = [
    ("v10_01", "sticky_receipt", "paid_total", 23.5,
     ["STICKY RECEIPT V10", "a paid 10.25", "b paid 13.25", "c open 4.00", "TOTAL PAID TARGET 23.50"],
     "便签收据", "RECV"),
    ("v10_02", "coffee_wh", "qty_sum", 27.0,
     ["WH COFFEE V10", "SKU1 qty 15 ok", "SKU2 qty 6 hold", "SKU3 qty 12 ok", "qty_sum TARGET 27"],
     "咖啡仓单", "RECV"),
    ("v10_03", "zorder_refund", "refund_done", 14.5,
     ["ZORDER REFUND V10", "itemR1 6.00 done", "itemR2 8.50 done", "itemR3 4.00 open", "refund_done TARGET 14.50"],
     "叠窗退款", "DONE"),
    ("v10_04", "fade_tax", "tax_base_paid", 33.0,
     ["TAX FADE V10", "T1 18.00 paid", "T2 9.00 open", "T3 15.00 paid", "tax_base_paid TARGET 33.00"],
     "淡墨税联", "RECV"),
    ("v10_05", "chatbait_payroll", "payroll_active", 1010.0,
     ["PAYROLL CHAT V10", "A 520 active", "B 110 leave", "C 490 active", "payroll_active TARGET 1010"],
     "聊天干扰薪资", "OK"),
    ("v10_06", "fold_ship", "ship_ok_qty", 19.0,
     ["SHIP FOLD V10", "P1 11 ok", "P2 6 hold", "P3 8 ok", "ship_ok_qty TARGET 19"],
     "折痕发货", "SHIP"),
    ("v10_07", "cal_sla", "open_pri_sum", 14.0,
     ["SLA CAL V10", "S1 pri 7 open", "S2 pri 11 closed", "S3 pri 7 open", "open_pri_sum TARGET 14"],
     "日历SLA", "OPEN"),
    ("v10_08", "sticky_exp", "paid_total", 42.25,
     ["EXPENSE STICKY V10", "E1 24.00 paid", "E2 9.00 void", "E3 18.25 paid", "paid_total TARGET 42.25"],
     "便签报销", "RECV"),
    ("v10_09", "zorder_po", "paid_total", 35.5,
     ["PO-Z V10", "itemA paid 19.00", "itemB paid 16.50", "itemC open 6.00", "TOTAL PAID TARGET 35.50"],
     "叠窗采购", "RECV"),
    ("v10_10", "coffee_order", "paid_total", 25.75,
     ["ORDER COFFEE V10", "A paid 14.25", "B paid 11.50", "C open 3.50", "TOTAL PAID TARGET 25.75"],
     "咖啡订单", "RECV"),
    ("v10_11", "dup_sticky", "paid_total", 18.0,
     ["INVOICE #V10-DUP", "line paid 6.00", "line paid 6.00", "line paid 6.00", "TOTAL PAID TARGET 18.00"],
     "便签重复", "RECV"),
    ("v10_12", "edge_zero_fade", "paid_total", 0.0,
     ["OPEN ONLY V10", "X 12.00 open", "Y 15.00 open", "paid_total TARGET 0.00"],
     "未付淡墨", "HOLD"),
    ("v10_13", "chat_ledger", "paid_total", 19.5,
     ["LEDGER CHAT V10", "rA paid 9.75", "rB paid 9.75", "rC open 2.00", "TOTAL PAID TARGET 19.50"],
     "聊天账本", "RECV"),
    ("v10_14", "fold_ui", "paid_total", 15.25,
     ["UI FOLD V10", "alpha paid 7.00", "beta paid 8.25", "gamma open 3.00", "TOTAL PAID TARGET 15.25"],
     "折痕界面", "RECV"),
    ("v10_15", "stain_stack", "paid_total", 31.0,
     ["HEAVY STAIN V10", "x paid 17.00 usd", "y paid 14.00 usd", "z open 5.00 usd", "TOTAL PAID TARGET 31.00"],
     "污渍重章", "RECV"),
    ("v10_16", "mix_cal", "paid_total", 20.0,
     ["CN-EN CAL MIX V10", "tea paid 9.00", "rice paid 11.00", "soup open 3.00", "TOTAL PAID TARGET 20.00"],
     "中英日历", "RECV"),
    ("v10_17", "triple_win", "paid_total", 28.5,
     ["TRIPLE WIN V10", "w1 paid 12.50", "w2 paid 16.00", "w3 open 7.00", "TOTAL PAID TARGET 28.50"],
     "三窗办公", "RECV"),
    ("v10_18", "footnote_bait", "paid_total", 16.75,
     ["FOOTNOTE V10", "p1 paid 8.25", "p2 paid 8.50", "p3 open 1.75", "TOTAL PAID TARGET 16.75"],
     "脚注诱饵", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V10 Protocol — Sticky / Coffee / Z-order / Fade / Chatbait

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V9: **sticky note occlusion**, **coffee stain**, **3-window z-order**,
**faded ink**, **chat bait sidebar**, **fold crease**, **calendar crosstalk**,
**tiny footnote bait**. Still scoped office OCR+atom.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only after smoke (C167)

## Honesty
- V9 train/heldout 1.0 retained
- Gate2/3 untouched. gen11 HOLD. No fake VL scores here.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v10") & 0xFFFFFFFF)
    try:
        from PIL import ImageGrab
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        bg = shot.crop((0, 0, min(1200, w), min(780, h))).convert("RGB").resize((980, 620))
        paper = Image.new("RGB", (980, 620), (210, 204, 194))
        img = Image.blend(bg, paper, 0.68)
        capture = True
    except Exception:
        img = Image.new("RGB", (980, 620), (210, 204, 194))
        capture = False
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 14)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 11)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 11)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 10)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 15)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 40)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 9)
        f_note = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_wm = f_tiny = f_note = ImageFont.load_default()

    # Main office paper (left)
    d.rectangle([14, 14, 470, 560], fill=(232, 226, 216), outline=(70, 70, 70), width=2)
    # fold crease
    d.line([(16, 200), (468, 215)], fill=(160, 150, 140), width=3)
    d.line([(16, 203), (468, 218)], fill=(190, 180, 170), width=1)
    # coffee stain ellipse
    d.ellipse([300, 380, 420, 500], outline=(140, 100, 70), width=4)
    d.ellipse([310, 390, 410, 490], fill=(190, 160, 130))
    # sticky note occlusion (partial cover of upper-right of paper)
    d.rectangle([320, 55, 455, 130], fill=(255, 245, 120), outline=(200, 180, 40), width=2)
    d.text((328, 65), "TODO IGNORE", fill=(80, 60, 20), font=f_note)
    d.text((328, 85), "bait 555.00", fill=(120, 40, 40), font=f_sm)
    d.text((328, 105), "do not sum", fill=(80, 60, 20), font=f_tiny)

    # watermarks / noise
    d.text((80, 240), "777", fill=(205, 200, 190), font=f_wm)
    d.text((200, 360), "666", fill=(200, 195, 185), font=f_wm)
    d.text((40, 320), "GHOST PAGE copy TOTAL 42", fill=(200, 195, 188), font=f_tiny)

    d.rectangle([22, 22, 300, 50], fill=(45, 60, 80))
    d.text((28, 26), (cn_title or kind)[:22], fill=(230, 230, 230), font=f_title)
    y = 60
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        # faded ink on later lines
        fill = (30, 30, 30) if y < 140 else (70, 70, 70) if y < 180 else (95, 95, 95)
        d.text((28, y), ln[:52], fill=fill, font=font)
        y += 18
    # tiny footnote bait
    d.text((28, 520), "footnote bait subtotal 999.00 ignore", fill=(150, 145, 135), font=f_tiny)
    # stamps
    for (cx, cy, label, col) in [(380, 170, stamp, (190, 40, 40)), (250, 250, "VOID", (150, 55, 55))]:
        d.ellipse([cx - 50, cy - 22, cx + 40, cy + 28], outline=col, width=3)
        d.text((cx - 18, cy - 6), label[:6], fill=col, font=f_stamp)

    # Window B — chat bait
    d.rectangle([500, 30, 760, 300], fill=(248, 248, 252), outline=(50, 50, 70), width=2)
    d.rectangle([500, 30, 760, 58], fill=(60, 90, 130))
    d.text((510, 36), "CHAT bait IGNORE", fill=(255, 230, 230), font=f_sm)
    d.text((510, 70), "boss: pay 888.00 now", fill=(20, 20, 20), font=f_sm)
    d.text((510, 95), "bot: total 777.00", fill=(20, 20, 20), font=f_sm)
    d.text((510, 120), "me: not this window", fill=(20, 20, 20), font=f_sm)
    d.text((510, 150), f"{fid} chat#OLD", fill=(40, 40, 40), font=f_tiny)

    # Window C — calendar crosstalk
    d.rectangle([520, 320, 960, 560], fill=(245, 250, 245), outline=(50, 80, 50), width=2)
    d.rectangle([520, 320, 960, 348], fill=(50, 100, 60))
    d.text((530, 326), "CALENDAR crosstalk", fill=(230, 255, 230), font=f_sm)
    d.text((530, 360), "meeting fee 666.00", fill=(20, 20, 20), font=f_sm)
    d.text((530, 385), "travel 555.00 open", fill=(20, 20, 20), font=f_sm)
    d.text((530, 410), "do not parse this panel", fill=(20, 20, 20), font=f_sm)
    d.text((530, 450), "event#V10-CAL", fill=(40, 40, 40), font=f_tiny)

    # Window D — tiny third peek (z-order)
    d.rectangle([780, 40, 960, 200], fill=(255, 240, 240), outline=(120, 40, 40), width=2)
    d.text((790, 50), "WIN-D VOID", fill=(120, 20, 20), font=f_sm)
    d.text((790, 80), "old 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((790, 105), "tiny 444.00", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 580, 980, 620], fill=(25, 25, 32))
    d.text((10, 590), "Start | Sticky | Chat | Cal | POS  [V10]", fill=(200, 200, 200), font=f_tiny)

    px = img.load()
    for _ in range(2200):
        x, y = rng.randint(0, 979), rng.randint(0, 619)
        v = rng.randint(0, 45)
        r, g, b = px[x, y]
        px[x, y] = (max(0, r - v), max(0, g - v), max(0, b - v))
    img = ImageEnhance.Contrast(img).enhance(0.86)
    img = img.filter(ImageFilter.SMOOTH)
    outp = FIX / f"{fid}_{kind}.png"
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "capture_blend": capture,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "hardening": [
            "sticky_occlusion", "coffee_stain", "zorder_3win", "faded_ink",
            "chat_bait", "fold_crease", "calendar_crosstalk", "footnote_bait",
        ],
    }


def main():
    PROTO.write_text(PROTOCOL.format(ts=ts()), encoding="utf-8")
    if FIX.exists():
        for p in FIX.glob("*.png"):
            p.unlink()
    items = []
    for fid, kind, metric, expected, lines, cn, stamp in SPECS:
        items.append(make_fixture(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v10", "n": len(items), "gate": GATE,
        "theme": "sticky_coffee_zorder_fade_chatbait",
        "harder_than": "v9",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    out = {
        "cycle": "C166",
        "theme": "vision_v10_design_batch",
        "gate": GATE,
        "timestamp": ts(),
        "n": len(items),
        "fixture_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "harder_than": "v9",
        "hardening": man["theme"],
        "smoke_deferred_to": "C167",
        "v9_train_rate": 1.0,
        "v9_heldout_rate": 1.0,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "pass": len(items) >= 16,
        "claim": False,
        "note": "V10 fixtures ready; claim only after real VL smoke >=0.6",
    }
    J(DOC / "C166_V10_DESIGN_BATCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({"cycle": "C166", "n": len(items), "pass": out["pass"]}, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
