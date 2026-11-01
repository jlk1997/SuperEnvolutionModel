# -*- coding: utf-8 -*-
"""C171: Vision V10 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V10 train (C166/C167). Same hardening family.
Gate 0.6. Gate2/3 untouched. gen11 HOLD. V0-V9 untouched.
"""
from __future__ import annotations
import gc, json, re, sys, random
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v10h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v10h_c171"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V10_HELDOUT_PROTOCOL.md"

# Disjoint from V10 train amounts
SPECS = [
    ("v10h_01", "sticky_receipt", "paid_total", 21.75,
     ["STICKY RECEIPT V10H", "a paid 9.50", "b paid 12.25", "c open 3.00", "TOTAL PAID TARGET 21.75"],
     "便签收据H", "RECV"),
    ("v10h_02", "coffee_wh", "qty_sum", 29.0,
     ["WH COFFEE V10H", "SKU1 qty 14 ok", "SKU2 qty 5 hold", "SKU3 qty 15 ok", "qty_sum TARGET 29"],
     "咖啡仓单H", "RECV"),
    ("v10h_03", "zorder_refund", "refund_done", 11.25,
     ["ZORDER REFUND V10H", "itemR1 4.75 done", "itemR2 6.50 done", "itemR3 3.00 open", "refund_done TARGET 11.25"],
     "叠窗退款H", "DONE"),
    ("v10h_04", "fade_tax", "tax_base_paid", 36.0,
     ["TAX FADE V10H", "T1 20.00 paid", "T2 8.00 open", "T3 16.00 paid", "tax_base_paid TARGET 36.00"],
     "淡墨税联H", "RECV"),
    ("v10h_05", "chatbait_payroll", "payroll_active", 880.0,
     ["PAYROLL CHAT V10H", "A 450 active", "B 100 leave", "C 430 active", "payroll_active TARGET 880"],
     "聊天干扰薪资H", "OK"),
    ("v10h_06", "fold_ship", "ship_ok_qty", 22.0,
     ["SHIP FOLD V10H", "P1 13 ok", "P2 5 hold", "P3 9 ok", "ship_ok_qty TARGET 22"],
     "折痕发货H", "SHIP"),
    ("v10h_07", "cal_sla", "open_pri_sum", 16.0,
     ["SLA CAL V10H", "S1 pri 8 open", "S2 pri 10 closed", "S3 pri 8 open", "open_pri_sum TARGET 16"],
     "日历SLAH", "OPEN"),
    ("v10h_08", "sticky_exp", "paid_total", 37.5,
     ["EXPENSE STICKY V10H", "E1 21.00 paid", "E2 7.00 void", "E3 16.50 paid", "paid_total TARGET 37.50"],
     "便签报销H", "RECV"),
    ("v10h_09", "zorder_po", "paid_total", 29.25,
     ["PO-Z V10H", "itemA paid 15.00", "itemB paid 14.25", "itemC open 5.00", "TOTAL PAID TARGET 29.25"],
     "叠窗采购H", "RECV"),
    ("v10h_10", "coffee_order", "paid_total", 22.0,
     ["ORDER COFFEE V10H", "A paid 12.00", "B paid 10.00", "C open 4.00", "TOTAL PAID TARGET 22.00"],
     "咖啡订单H", "RECV"),
    ("v10h_11", "dup_sticky", "paid_total", 27.0,
     ["INVOICE #V10H-DUP", "line paid 9.00", "line paid 9.00", "line paid 9.00", "TOTAL PAID TARGET 27.00"],
     "便签重复H", "RECV"),
    ("v10h_12", "edge_zero_fade", "paid_total", 0.0,
     ["OPEN ONLY V10H", "X 11.00 open", "Y 13.00 open", "paid_total TARGET 0.00"],
     "未付淡墨H", "HOLD"),
    ("v10h_13", "chat_ledger", "paid_total", 14.5,
     ["LEDGER CHAT V10H", "rA paid 7.25", "rB paid 7.25", "rC open 1.50", "TOTAL PAID TARGET 14.50"],
     "聊天账本H", "RECV"),
    ("v10h_14", "fold_ui", "paid_total", 18.75,
     ["UI FOLD V10H", "alpha paid 8.50", "beta paid 10.25", "gamma open 2.50", "TOTAL PAID TARGET 18.75"],
     "折痕界面H", "RECV"),
    ("v10h_15", "stain_stack", "paid_total", 26.5,
     ["HEAVY STAIN V10H", "x paid 14.00 usd", "y paid 12.50 usd", "z open 4.00 usd", "TOTAL PAID TARGET 26.50"],
     "污渍重章H", "RECV"),
    ("v10h_16", "mix_cal", "paid_total", 23.0,
     ["CN-EN CAL MIX V10H", "tea paid 10.00", "rice paid 13.00", "soup open 2.00", "TOTAL PAID TARGET 23.00"],
     "中英日历H", "RECV"),
    ("v10h_17", "triple_win", "paid_total", 32.25,
     ["TRIPLE WIN V10H", "w1 paid 15.00", "w2 paid 17.25", "w3 open 6.00", "TOTAL PAID TARGET 32.25"],
     "三窗办公H", "RECV"),
    ("v10h_18", "footnote_bait", "paid_total", 12.5,
     ["FOOTNOTE V10H", "p1 paid 6.00", "p2 paid 6.50", "p3 open 2.25", "TOTAL PAID TARGET 12.50"],
     "脚注诱饵H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V10 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V10 train (C167). Different ids/amounts; same sticky/coffee/z-order/fade/chatbait family.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only on PASS

## Honesty
- Gate2/3 untouched. V0-V9 untouched. gen11 HOLD.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v10h") & 0xFFFFFFFF)
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

    d.rectangle([14, 14, 470, 560], fill=(232, 226, 216), outline=(70, 70, 70), width=2)
    d.line([(16, 200), (468, 215)], fill=(160, 150, 140), width=3)
    d.line([(16, 203), (468, 218)], fill=(190, 180, 170), width=1)
    d.ellipse([300, 380, 420, 500], outline=(140, 100, 70), width=4)
    d.ellipse([310, 390, 410, 490], fill=(190, 160, 130))
    d.rectangle([320, 55, 455, 130], fill=(255, 245, 120), outline=(200, 180, 40), width=2)
    d.text((328, 65), "TODO IGNORE", fill=(80, 60, 20), font=f_note)
    d.text((328, 85), "bait 555.00", fill=(120, 40, 40), font=f_sm)
    d.text((328, 105), "do not sum", fill=(80, 60, 20), font=f_tiny)

    d.text((80, 240), "777", fill=(205, 200, 190), font=f_wm)
    d.text((200, 360), "666", fill=(200, 195, 185), font=f_wm)
    d.text((40, 320), "GHOST PAGE copy TOTAL 42", fill=(200, 195, 188), font=f_tiny)

    d.rectangle([22, 22, 300, 50], fill=(45, 60, 80))
    d.text((28, 26), (cn_title or kind)[:22], fill=(230, 230, 230), font=f_title)
    y = 60
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        fill = (30, 30, 30) if y < 140 else (70, 70, 70) if y < 180 else (95, 95, 95)
        d.text((28, y), ln[:52], fill=fill, font=font)
        y += 18
    d.text((28, 520), "footnote bait subtotal 999.00 ignore", fill=(150, 145, 135), font=f_tiny)
    for (cx, cy, label, col) in [(380, 170, stamp, (190, 40, 40)), (250, 250, "VOID", (150, 55, 55))]:
        d.ellipse([cx - 50, cy - 22, cx + 40, cy + 28], outline=col, width=3)
        d.text((cx - 18, cy - 6), label[:6], fill=col, font=f_stamp)

    d.rectangle([500, 30, 760, 300], fill=(248, 248, 252), outline=(50, 50, 70), width=2)
    d.rectangle([500, 30, 760, 58], fill=(60, 90, 130))
    d.text((510, 36), "CHAT bait IGNORE", fill=(255, 230, 230), font=f_sm)
    d.text((510, 70), "boss: pay 888.00 now", fill=(20, 20, 20), font=f_sm)
    d.text((510, 95), "bot: total 777.00", fill=(20, 20, 20), font=f_sm)
    d.text((510, 120), "me: not this window", fill=(20, 20, 20), font=f_sm)
    d.text((510, 150), f"{fid} chat#OLD", fill=(40, 40, 40), font=f_tiny)

    d.rectangle([520, 320, 960, 560], fill=(245, 250, 245), outline=(50, 80, 50), width=2)
    d.rectangle([520, 320, 960, 348], fill=(50, 100, 60))
    d.text((530, 326), "CALENDAR crosstalk", fill=(230, 255, 230), font=f_sm)
    d.text((530, 360), "meeting fee 666.00", fill=(20, 20, 20), font=f_sm)
    d.text((530, 385), "travel 555.00 open", fill=(20, 20, 20), font=f_sm)
    d.text((530, 410), "do not parse this panel", fill=(20, 20, 20), font=f_sm)
    d.text((530, 450), "event#V10H-CAL", fill=(40, 40, 40), font=f_tiny)

    d.rectangle([780, 40, 960, 200], fill=(255, 240, 240), outline=(120, 40, 40), width=2)
    d.text((790, 50), "WIN-D VOID", fill=(120, 20, 20), font=f_sm)
    d.text((790, 80), "old 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((790, 105), "tiny 444.00", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 580, 980, 620], fill=(25, 25, 32))
    d.text((10, 590), "Start | Sticky | Chat | Cal | POS  [V10H]", fill=(200, 200, 200), font=f_tiny)

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
        "disjoint_from_train": True,
        "hardening": [
            "sticky_occlusion", "coffee_stain", "zorder_3win", "faded_ink",
            "chat_bait", "fold_crease", "calendar_crosstalk", "footnote_bait",
        ],
    }


def soft_ocr_ok(text, lines):
    t = (text or "").lower().replace(" ", "")
    keys = re.findall(r"\d+\.?\d*", " ".join(lines))
    if not t:
        return False
    hit = sum(1 for k in keys[:5] if k.replace(".00", "") in t or k in t)
    return hit >= max(2, min(3, len(keys[:5]) // 2))


def gpu_free_mib():
    try:
        import subprocess
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10,
        )
        return float((r.stdout or "0").strip().split("\n")[0])
    except Exception:
        return 0.0


def main():
    PROTO.write_text(PROTOCOL.format(ts=ts()), encoding="utf-8")
    if FIX.exists():
        for p in FIX.glob("*.png"):
            p.unlink()
    items = []
    for fid, kind, metric, expected, lines, cn, stamp in SPECS:
        items.append(make_fixture(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v10_heldout", "n": len(items), "gate": GATE,
        "theme": "v10_heldout_disjoint", "harder_than": "v9_heldout",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C171", "theme": "vision_v10_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v10_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C171_VISION_V10_HELDOUT_SMOKE.json", out)
        print(json.dumps(out, ensure_ascii=False))
        return 1

    from evo.office.vision_backend import RealVlBackend
    from evo.office.vision_ocr import ocr_image
    RUN.mkdir(parents=True, exist_ok=True)
    backend = RealVlBackend(WEIGHTS, max_new_tokens=200)
    rows, n_ok = [], 0
    try:
        for it in items:
            ocr = ocr_image(ROOT / it["path"], prefer="vl", vl_backend=backend)
            text = re.sub(r"<think>[\s\S]*?</think>", " ", ocr.get("text") or "")
            text = re.sub(r"\s+", " ", text).strip()
            ocr_ok = soft_ocr_ok(text, it["lines"])
            got, atom_ok = parse_metric(text, it["metric"], it["expected"])
            ok = bool(ocr_ok and atom_ok)
            n_ok += int(ok)
            rows.append({
                "id": it["id"], "kind": it["kind"], "metric": it["metric"],
                "ocr_ok": ocr_ok, "atom_ok": atom_ok, "ok": ok,
                "got": got, "expected": it["expected"], "ocr_preview": text[:360],
            })
            print(json.dumps({"id": it["id"], "ok": ok, "got": got, "expected": it["expected"]}, ensure_ascii=False), flush=True)
    finally:
        try:
            backend.unload()
        except Exception:
            pass
        gc.collect()
        try:
            import torch
            torch.cuda.empty_cache()
        except Exception:
            pass

    n = len(rows)
    rate = round(n_ok / n, 4) if n else 0.0
    gate_pass = n >= 16 and rate >= GATE
    claim = gate_pass
    scope = "r50plus_v10_heldout_disjoint_n>=16_c162_parse_qwen35_2b_c171" if claim else None
    out = {
        "cycle": "C171",
        "theme": "vision_v10_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v10_heldout_claim": claim,
        "claim_scope": scope,
        "train_ref": "docs/r50/C167b_VISION_GATE_V10_CLAIM.json",
        "disjoint": True,
        "gate2_3_untouched": True,
        "v0_v9_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "V10 heldout real VL; claim only if rate>=0.6",
    }
    J(DOC / "C171_VISION_V10_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C171b_VISION_GATE_V10_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v10_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v10_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "v0_v9_untouched": True,
            "gen11": "HOLD",
            "cycle": "C171",
        })
    print(json.dumps({
        "cycle": "C171", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
