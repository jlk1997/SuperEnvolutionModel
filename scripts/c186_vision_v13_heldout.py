# -*- coding: utf-8 -*-
"""C186: Vision V13 heldout — disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V13 train (C182/C183). Same crumple/highlight/sticky/fold/
coffee/bleed/cyan/fluoro/punch/fax/wm/carbon family. Mild-readable TARGET.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import gc, io, json, re, sys, random
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v13h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v13h_c186"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V13_HELDOUT_PROTOCOL.md"

# Disjoint from V13 train amounts (C182/C183)
SPECS = [
    ("v13h_01", "crumple_receipt", "paid_total", 28.5,
     ["CRUMPLE RECEIPT V13H", "a paid 13.00", "b paid 15.50", "c open 5.00", "TOTAL PAID TARGET 28.50"],
     "皱纸收据H", "RECV"),
    ("v13h_02", "highlight_wh", "qty_sum", 33.0,
     ["WH HIGHLIGHT V13H", "SKU1 qty 18 ok", "SKU2 qty 6 hold", "SKU3 qty 15 ok", "qty_sum TARGET 33"],
     "荧光笔仓单H", "RECV"),
    ("v13h_03", "sticky_refund", "refund_done", 16.25,
     ["STICKY REFUND V13H", "itemR1 7.00 done", "itemR2 9.25 done", "itemR3 2.50 open", "refund_done TARGET 16.25"],
     "便利贴退款H", "DONE"),
    ("v13h_04", "fold_tax", "tax_base_paid", 55.0,
     ["TAX FOLD V13H", "T1 30.00 paid", "T2 11.00 open", "T3 25.00 paid", "tax_base_paid TARGET 55.00"],
     "折痕税联H", "RECV"),
    ("v13h_05", "coffee_payroll", "payroll_active", 890.0,
     ["PAYROLL COFFEE V13H", "A 470 active", "B 70 leave", "C 420 active", "payroll_active TARGET 890"],
     "咖啡渍薪资H", "OK"),
    ("v13h_06", "bleed_ship", "ship_ok_qty", 23.0,
     ["SHIP BLEED V13H", "P1 11 ok", "P2 6 hold", "P3 12 ok", "ship_ok_qty TARGET 23"],
     "洇墨发货H", "SHIP"),
    ("v13h_07", "cyan_sla", "open_pri_sum", 19.0,
     ["SLA CYAN V13H", "S1 pri 9 open", "S2 pri 14 closed", "S3 pri 10 open", "open_pri_sum TARGET 19"],
     "套色SLAH", "OPEN"),
    ("v13h_08", "fluoro_exp", "paid_total", 41.5,
     ["EXPENSE FLUORO V13H", "E1 22.00 paid", "E2 7.00 void", "E3 19.50 paid", "paid_total TARGET 41.50"],
     "荧光报销H", "RECV"),
    ("v13h_09", "punch_po", "paid_total", 35.75,
     ["PO-PUNCH V13H", "itemA paid 18.00", "itemB paid 17.75", "itemC open 6.00", "TOTAL PAID TARGET 35.75"],
     "打孔采购H", "RECV"),
    ("v13h_10", "fax_order", "paid_total", 29.0,
     ["ORDER FAX V13H", "A paid 14.25", "B paid 14.75", "C open 4.00", "TOTAL PAID TARGET 29.00"],
     "传真订单H", "RECV"),
    ("v13h_11", "wm_dup", "paid_total", 27.0,
     ["INVOICE #V13H-DUP", "line paid 9.00", "line paid 9.00", "line paid 9.00", "TOTAL PAID TARGET 27.00"],
     "水印重复H", "RECV"),
    ("v13h_12", "carbon_zero", "paid_total", 0.0,
     ["OPEN ONLY V13H", "X 16.00 open", "Y 19.00 open", "paid_total TARGET 0.00"],
     "复写未付H", "HOLD"),
    ("v13h_13", "crumple_ledger", "paid_total", 18.25,
     ["LEDGER CRUMPLE V13H", "rA paid 9.00", "rB paid 9.25", "rC open 3.25", "TOTAL PAID TARGET 18.25"],
     "皱纸账本H", "RECV"),
    ("v13h_14", "sticky_ui", "paid_total", 24.5,
     ["UI STICKY V13H", "alpha paid 11.50", "beta paid 13.00", "gamma open 3.50", "TOTAL PAID TARGET 24.50"],
     "便利贴界面H", "RECV"),
    ("v13h_15", "coffee_stack", "paid_total", 37.0,
     ["HEAVY COFFEE V13H", "x paid 18.50 usd", "y paid 18.50 usd", "z open 7.00 usd", "TOTAL PAID TARGET 37.00"],
     "咖啡叠窗H", "RECV"),
    ("v13h_16", "fax_mix", "paid_total", 22.5,
     ["CN-EN FAX MIX V13H", "tea paid 10.25", "rice paid 12.25", "soup open 2.50", "TOTAL PAID TARGET 22.50"],
     "中英传真H", "RECV"),
    ("v13h_17", "fold_win", "paid_total", 40.0,
     ["FOLD WIN V13H", "w1 paid 19.50", "w2 paid 20.50", "w3 open 9.00", "TOTAL PAID TARGET 40.00"],
     "折痕双窗H", "RECV"),
    ("v13h_18", "bleed_foot", "paid_total", 16.75,
     ["BLEED FOOT V13H", "p1 paid 8.00", "p2 paid 8.75", "p3 open 2.25", "TOTAL PAID TARGET 16.75"],
     "洇墨脚注H", "RECV"),
]


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# 蚁算-视 VL Gate V13 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V13 train (C182/C183). Different ids/amounts;
same crumple/highlight/sticky/fold/coffee/bleed/cyan/fax family; mild-readable TARGET.

## Gate
- rate >= **0.6**, n >= 16, real VL
- Claim only on PASS

## Honesty
- Gate2/3 untouched. V0-V12 untouched. gen11 HOLD.
"""


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v13h") & 0xFFFFFFFF)
    img = Image.new("RGB", (1040, 680), (210, 205, 195))
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 15)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 13)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 36)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = f_wm = ImageFont.load_default()

    d.rectangle([36, 18, 540, 580], fill=(242, 236, 226), outline=(35, 35, 35), width=2)
    for _ in range(14):
        x0 = rng.randint(40, 500)
        y0 = rng.randint(40, 540)
        d.arc([x0, y0, x0 + rng.randint(40, 120), y0 + rng.randint(20, 60)], 0, 180, fill=(200, 195, 185), width=1)
    d.rectangle([50, 95, 500, 118], fill=(255, 255, 120))
    d.rectangle([50, 160, 420, 182], fill=(180, 255, 180))
    d.rectangle([360, 200, 520, 280], fill=(255, 250, 120), outline=(180, 160, 40), width=2)
    d.text((370, 210), "STICKY", fill=(80, 60, 20), font=f_sm)
    d.text((370, 235), "bait 888.00", fill=(80, 60, 20), font=f_tiny)
    d.text((370, 255), "IGNORE", fill=(80, 60, 20), font=f_tiny)
    d.line([(40, 40), (520, 560)], fill=(180, 175, 165), width=2)
    d.line([(42, 38), (522, 558)], fill=(230, 225, 215), width=1)

    coffee = Image.new("RGBA", img.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(coffee)
    cd.ellipse([80, 400, 220, 540], outline=(120, 70, 30, 90), width=10)
    cd.ellipse([100, 420, 200, 520], fill=(140, 80, 40, 40))
    img = Image.alpha_composite(img.convert("RGBA"), coffee).convert("RGB")
    d = ImageDraw.Draw(img)

    for hy in (60, 200, 340, 480):
        d.ellipse([18, hy, 34, hy + 16], fill=(210, 205, 195), outline=(40, 40, 40), width=1)
    for fy in range(30, 570, 7):
        if rng.random() > 0.35:
            d.line([(40, fy), (540, fy)], fill=(195, 190, 185), width=1)

    d.text((80, 320), "CONFIDENTIAL", fill=(220, 210, 200), font=f_wm)
    d.text((100, 450), "COPY bait 777", fill=(225, 218, 208), font=f_sm)

    d.rectangle([46, 26, 330, 56], fill=(25, 45, 65))
    d.text((52, 30), (cn_title or kind)[:20], fill=(240, 240, 240), font=f_title)
    y = 70
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((55, y), ln[:54], fill=(8, 8, 8), font=font)
        y += 22

    for (cx, cy, label, col) in [(390, 140, stamp, (180, 30, 30)), (280, 250, "作废", (140, 50, 50)), (430, 300, "VOID", (150, 40, 40))]:
        d.ellipse([cx - 46, cy - 22, cx + 40, cy + 26], outline=col, width=3)
        d.text((cx - 14, cy - 6), label[:4], fill=col, font=f_stamp)
        d.ellipse([cx - 50, cy - 26, cx + 44, cy + 30], outline=col, width=1)

    d.rectangle([740, 200, 1020, 420], fill=(250, 248, 255), outline=(50, 50, 80), width=2)
    d.text((750, 210), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((750, 245), "old total 999.00", fill=(20, 20, 20), font=f_sm)
    d.text((750, 280), "do not parse", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 650, 1040, 680], fill=(18, 18, 28))
    d.text((10, 658), "V13H HELDOUT C186  [readable TARGET]", fill=(200, 200, 200), font=f_tiny)

    px = img.load()
    ww, hh = img.size
    for yy in range(120, 200):
        for xx in range(50, min(500, ww - 3)):
            r, g, b = px[xx, yy]
            px[xx, yy] = (r, g, min(255, b + 18))

    glare = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.ellipse([140, 30, 360, 160], fill=(255, 255, 220, 55))
    img = Image.alpha_composite(img.convert("RGBA"), glare).convert("RGB")

    w, h = img.size
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.025, -10, 0.01, 1, -3),
        resample=Image.BICUBIC, fillcolor=(210, 205, 195),
    )
    img = ImageEnhance.Contrast(img).enhance(0.92)
    img = ImageEnhance.Brightness(img).enhance(0.94)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=55)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    img = img.filter(ImageFilter.SMOOTH)

    outp = FIX / f"{fid}_{kind}.png"
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "disjoint_from_train": True,
        "hardening": [
            "crumple_wrinkles", "highlighter_wash", "sticky_occlusion", "fold_crease",
            "coffee_stain", "ink_bleed_stamp", "cyan_misreg", "fluorescent_glare",
            "punch_holes", "fax_lines", "confidential_wm", "carbon_fade", "jpeg_q55",
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
        "version": "v13_heldout", "n": len(items), "gate": GATE,
        "theme": "v13_heldout_disjoint", "harder_than": "v12_heldout",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C186", "theme": "vision_v13_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "vl_gate_v13_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C186_VISION_V13_HELDOUT_SMOKE.json", out)
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
    scope = "r50plus_v13_heldout_disjoint_n>=16_c162_parse_qwen35_2b_c186" if claim else None
    out = {
        "cycle": "C186",
        "theme": "vision_v13_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "vl_gate_v13_heldout_claim": claim,
        "claim_scope": scope,
        "train_ref": "docs/r50/C183b_VISION_GATE_V13_CLAIM.json",
        "disjoint": True,
        "gate2_3_untouched": True,
        "v0_v12_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
        "note": "V13 heldout real VL; claim only if rate>=0.6",
    }
    J(DOC / "C186_VISION_V13_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C186b_VISION_GATE_V13_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v13_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v13_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "gate2_3_untouched": True,
            "v0_v12_untouched": True,
            "gen11": "HOLD",
            "cycle": "C186",
        })
    print(json.dumps({
        "cycle": "C186", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
