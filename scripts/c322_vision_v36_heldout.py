# -*- coding: utf-8 -*-
"""C322: Vision V35 heldout 鈥?disjoint fixtures + real VL claim if rate>=0.6.
Different ids/amounts from V33 train (C302/C303). Same fp/rain/staple/qr/
curl/flare/clutter/ink/torn/zig family; clarity floor.
Gate 0.6. Gate2/3 untouched. gen11 HOLD.
"""
from __future__ import annotations
import gc, io, json, random, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v36h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v35h_c322"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V36_HELDOUT_PROTOCOL.md"
TRAIN_FIX = ROOT / "evo/office/fixtures/vision_images_v36"

JPEG_Q = 60
PHOTOCOPY_DIV = 2
BLUR_R = 0.45
TEXT_BAND = (70, 250)

# Disjoint from V33 train amounts (C254)
SPECS = [
    ("v36h_01", "teak_recv", "paid_total", 76.5,
     ["TEAK GRAIN RECV V36", "a paid 36.00", "b paid 40.50", "c open 14.00", "TOTAL PAID TARGET 76.50"],
     "柚木收款单H", "RECV"),
    ("v36h_02", "marble_wh", "qty_sum", 54.0,
     ["WH MARBLE TILE V36", "SKU1 qty 24 ok", "SKU2 qty 12 hold", "SKU3 qty 30 ok", "qty_sum TARGET 54"],
     "大理石仓位单H", "RECV"),
    ("v36h_03", "canvas_refund", "refund_done", 42.25,
     ["CANVAS PATCH REFUND V36", "itemR1 20.00 done", "itemR2 22.25 done", "itemR3 9.00 open", "refund_done TARGET 42.25"],
     "帆布补丁退款单H", "DONE"),
    ("v36h_04", "cobalt_tax", "tax_base_paid", 108.0,
     ["COBALT TAX SLIP V36", "base 52.00 paid", "addon 56.00 paid", "skip 24.00", "tax_base_paid TARGET 108.00"],
     "钴蓝税基单H", "TAX"),
    ("v36h_05", "mica_pay", "payroll_active", 142.0,
     ["MICA PAYROLL V36", "empA 70.00 active", "empB 72.00 active", "empC 20.00 leave", "payroll_active TARGET 142.00"],
     "云母工资单H", "PAY"),
    ("v36h_06", "clasp_ship", "ship_ok", 35.0,
     ["CLASP SHIP DOCK V36", "box1 18 ok", "box2 9 ok", "box3 14 hold", "ship_ok TARGET 35"],
     "搭扣出货单H", "SHIP"),
    ("v36h_07", "garnet_sla", "sla_ok_hours", 46.5,
     ["GARNET SLA CARD V36", "job1 25.00h ok", "job2 21.50h ok", "job3 11.00h late", "sla_ok_hours TARGET 46.50"],
     "石榴石SLA卡H", "SLA"),
    ("v36h_08", "flint_exp", "exp_sum", 58.75,
     ["FLINT EXPENSE V36", "e1 27.00", "e2 31.75", "e3 13.00 void", "exp_sum TARGET 58.75"],
     "燧石费用单H", "EXP"),
    ("v36h_09", "steel_po", "po_open", 67.0,
     ["STEEL PO SHEET V36", "line1 36.00 open", "line2 31.00 open", "line3 15.00 closed", "po_open TARGET 67.00"],
     "钢材采购单H", "PO"),
    ("v36h_10", "kraft_order", "order_paid", 82.25,
     ["KRAFT ORDER V36", "skuA 44.00 paid", "skuB 38.25 paid", "skuC 12.00 due", "order_paid TARGET 82.25"],
     "牛皮纸订单H", "ORD"),
    ("v36h_11", "flannel_dup", "dup_mark", 2.0,
     ["FLANNEL DUP MARK V36", "markA 1", "markB 1", "markC 0", "dup_mark TARGET 2"],
     "法兰绒重复标记H", "DUP"),
    ("v36h_12", "empty_zero", "zero_check", 0.0,
     ["EMPTY VOID ZERO V36", "z1 0.00", "z2 0.00", "z3 0.00", "zero_check TARGET 0.00"],
     "空值清零单H", "ZERO"),
    ("v36h_13", "jute_ledger", "ledger_net", 126.5,
     ["JUTE LEDGER V36", "dr 60.00", "cr 66.50", "adj 20.00", "ledger_net TARGET 126.50"],
     "黄麻账本H", "LED"),
    ("v36h_14", "glaze_ui", "ui_ok", 1.0,
     ["GLAZE UI SCAN V36", "btnOK 1", "btnSkip 0", "btnBad 0", "ui_ok TARGET 1"],
     "釉面界面扫描H", "UI"),
    ("v36h_15", "sisal_stack", "stack_count", 6.0,
     ["SISAL STACK V36", "p1 3", "p2 2", "p3 1", "stack_count TARGET 6"],
     "剑麻堆叠单H", "STK"),
    ("v36h_16", "aubergine_fax", "fax_pages", 9.0,
     ["AUBERGINE FAX V36", "pgA 5", "pgB 4", "pgC 2 drop", "fax_pages TARGET 9"],
     "茄紫传真单H", "FAX"),
    ("v36h_17", "titanium_glare", "glare_ok", 1.0,
     ["TITANIUM GLARE V36", "zone1 1 ok", "zone2 0", "zone3 0", "glare_ok TARGET 1"],
     "钛光眩光单H", "GLR"),
    ("v36h_18", "dossier_tab", "tab_index", 12.0,
     ["DOSSIER TAB INDEX V36", "tabA 7", "tabB 5", "tabC 1", "tab_index TARGET 12"],
     "档案页签索引H", "TAB"),
]






def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL = """# Ant VL Gate V33 Heldout Protocol

Updated: {ts} (Asia/Shanghai)

## Purpose
Disjoint heldout for V35 train (C314). Different ids/amounts.
Same hl/crumple/rubber/clip/grease/carbon/stamp/pocket family.
Clarity floor jpeg_q>={jpeg_q}.

## Gate
rate >= 0.6, n >= 16, real VL. Gate2/3 untouched. gen11 HOLD.
"""


def in_text_band(yy):
    y0, y1 = TEXT_BAND
    return y0 <= yy <= y1


def make_fixture(fid, kind, lines, metric, expected, cn_title, stamp):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    FIX.mkdir(parents=True, exist_ok=True)
    rng = random.Random(hash(fid + "_v35hc322") & 0xFFFFFFFF)
    bg = (212, 208, 198)
    img = Image.new("RGB", (1100, 740), bg)
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 16)
        f_body = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 14)
        f_tgt = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 15)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\msyh.ttc", 11)
        f_stamp = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 14)
        f_tiny = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 10)
        f_wm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arialbd.ttf", 28)
        f_fax = ImageFont.truetype(r"C:\\Windows\\Fonts\\consola.ttf", 11)
        f_pen = ImageFont.truetype(r"C:\\Windows\\Fonts\\comic.ttf", 13)
    except Exception:
        f_title = f_body = f_tgt = f_sm = f_stamp = f_tiny = f_wm = f_fax = f_pen = ImageFont.load_default()

    d.rectangle([40, 20, 560, 600], fill=(252, 249, 240), outline=(30, 30, 30), width=2)

    for hy in (80, 160, 240, 320, 400, 480):
        d.ellipse([8, hy - 10, 36, hy + 10], outline=(60, 60, 70), width=3)
        d.ellipse([14, hy - 4, 30, hy + 4], fill=(180, 180, 190))

    for (cx, cy, r) in [(480, 420, 55), (120, 520, 40), (900, 300, 70)]:
        for rr in range(r - 8, r, 2):
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(160, 110, 70), width=2)
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(170, 120, 80))

    d.rectangle([80, 18, 280, 42], fill=(240, 230, 160))
    d.text((90, 22), "TAPE bait 33.33", fill=(100, 80, 20), font=f_tiny)

    d.line([(470, 90), (540, 200)], fill=(20, 60, 180), width=2)
    d.text((475, 160), "OK?", fill=(20, 60, 180), font=f_pen)
    d.text((475, 185), "bait 66.66", fill=(20, 60, 180), font=f_tiny)

    d.rectangle([380, 300, 540, 380], fill=(255, 250, 120), outline=(180, 160, 40), width=2)
    d.text((390, 310), "STICKY", fill=(70, 50, 10), font=f_sm)
    d.text((390, 335), "bait 88.88", fill=(70, 50, 10), font=f_tiny)
    d.text((390, 355), "IGNORE", fill=(70, 50, 10), font=f_tiny)

    for y in range(290, 560, 7):
        shade = 200 if (y // 7) % 2 == 0 else 230
        d.line([(50, y), (540, y)], fill=(shade, shade, shade), width=1)

    for (cx, cy, label, col) in [
        (420, 450, stamp, (170, 20, 20)),
        (180, 500, "VOID", (140, 30, 30)),
        (300, 550, "COPY", (50, 50, 150)),
    ]:
        d.ellipse([cx - 48, cy - 24, cx + 42, cy + 26], outline=col, width=3)
        d.text((cx - 16, cy - 6), label[:4], fill=col, font=f_stamp)

    for i in range(5):
        d.text((70 + i * 45, 310 + i * 38), "DRAFT", fill=(236, 232, 224), font=f_wm)

    d.rectangle([0, 0, 1100, 14], fill=(235, 235, 235))
    d.text((8, 1), "SCAN DESK V36H bait 222.00 PAGE 01", fill=(70, 70, 70), font=f_fax)

    d.rectangle([50, 28, 360, 58], fill=(28, 48, 68))
    d.text((56, 32), (cn_title or kind)[:18], fill=(240, 240, 240), font=f_title)

    y = 78
    for ln in lines:
        font = f_tgt if ("TARGET" in ln.upper() or "TOTAL" in ln.upper()) else f_body
        d.text((62, y + 2), ln[:54], fill=(228, 224, 214), font=font)
        d.text((60, y), ln[:54], fill=(6, 6, 6), font=font)
        y += 26

    d.rectangle([760, 220, 1060, 420], fill=(248, 246, 252), outline=(40, 40, 70), width=2)
    d.text((770, 230), "VOID WIN IGNORE", fill=(120, 40, 40), font=f_sm)
    d.text((770, 265), "old total 888.00", fill=(20, 20, 20), font=f_sm)
    d.text((770, 300), "do not parse", fill=(20, 20, 20), font=f_sm)
    d.text((770, 335), "bait 555.00", fill=(20, 20, 20), font=f_sm)

    d.rectangle([0, 710, 1100, 740], fill=(16, 16, 26))
    d.text(
        (10, 718),
        f"V36H C322 clarity floor jpeg_q{JPEG_Q} photo/{PHOTOCOPY_DIV} heldout",
        fill=(200, 200, 200),
        font=f_tiny,
    )

    px = img.load()
    ww, hh = img.size

    for t in range(0, 700, 2):
        xx = 60 + t
        yy = 280 + int(t * 0.35)
        for w in range(-2, 3):
            x2, y2 = xx + w, yy + w
            if 0 <= x2 < ww and 0 <= y2 < hh and not (in_text_band(y2) and 50 <= x2 <= 450):
                r, g, b = px[x2, y2]
                px[x2, y2] = (min(255, r + 18), min(255, g + 16), min(255, b + 12))

    for _ in range(120):
        xx = rng.randint(45, 160)
        yy = rng.randint(420, 580)
        r, g, b = px[xx, yy]
        px[xx, yy] = (max(0, r - 40), max(0, g - 50), max(0, b - 55))

    for yy in range(300, 560):
        for xx in range(500, 560):
            r, g, b = px[xx, yy]
            px[xx, yy] = (int(r * 0.92 + 20), int(g * 0.92 + 20), int(b * 0.92 + 20))

    for _ in range(280):
        xx = rng.randint(0, ww - 1)
        yy = rng.randint(0, hh - 1)
        if in_text_band(yy) and 50 <= xx <= 540:
            continue
        v = rng.randint(0, 255)
        px[xx, yy] = (v, v, v)

    img = ImageEnhance.Color(img).enhance(0.82)
    img = ImageEnhance.Contrast(img).enhance(0.98)
    img = ImageEnhance.Brightness(img).enhance(0.95)

    w, h = img.size
    small = img.resize((max(1, w // PHOTOCOPY_DIV), max(1, h // PHOTOCOPY_DIV)), Image.BILINEAR)
    img = small.resize((w, h), Image.BILINEAR)
    img = img.transform(
        (w, h), Image.AFFINE, (1, 0.028, -10, 0.012, 1, -5),
        resample=Image.BICUBIC, fillcolor=bg,
    )
    ghost = img.transform(
        (w, h), Image.AFFINE, (1, 0, 3, 0, 1, 2),
        resample=Image.BICUBIC, fillcolor=bg,
    )
    img = Image.blend(img, ghost, 0.12)
    img = img.filter(ImageFilter.GaussianBlur(radius=BLUR_R))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=JPEG_Q)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    img = img.filter(ImageFilter.SMOOTH)

    outp = FIX / f"{fid}_{kind}.png"
    for old in FIX.glob(f"{fid}_*.png"):
        if old != outp:
            try:
                old.unlink()
            except Exception:
                pass
    img.save(outp)
    return {
        "id": fid, "file": outp.name, "kind": kind, "metric": metric,
        "expected": expected, "lines": lines, "cn_title": cn_title, "stamp": stamp,
        "path": str(outp.relative_to(ROOT)).replace("\\", "/"),
        "hardening": [
            "highlighter_cross", "magnetic_clip", "thermal_fade", "coffee_splash_edge",
            "double_fold_corner", "pencil_scribble", "stapler_puncture", "watermark_diag",
            "phone_shadow", "receipt_skew_stack", "blue_pen_circles", "red_correction_tape",
            "ship_label_edge", "binder_clip_top", "sticky_peel_corner",
            f"jpeg_q{JPEG_Q}", f"photocopy_div{PHOTOCOPY_DIV}", f"blur_{BLUR_R}",
            "text_band_protect", "c272_clarity_floor",
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


def id_disjoint(train_ids, held_ids):
    return len(set(train_ids) & set(held_ids)) == 0


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    PROTO.write_text(PROTOCOL.format(ts=ts(), jpeg_q=JPEG_Q), encoding="utf-8")
    items = []
    for fid, kind, metric, expected, lines, cn, stamp in SPECS:
        items.append(make_fixture(fid, kind, lines, metric, expected, cn, stamp))
    man = {
        "version": "v36h",
        "n": len(items),
        "gate": GATE,
        "theme": "hlx_magclip_thermal_coffee_heldout",
        "clarity_floor": {
            "jpeg_q_min": 58, "jpeg_q": JPEG_Q,
            "photocopy_div_max": 2, "photocopy_div": PHOTOCOPY_DIV,
            "blur_max": 0.5, "blur": BLUR_R,
            "text_band_y": list(TEXT_BAND),
        },
        "items": items,
        "timestamp": ts(),
        "claim": False,
        "gate2_3_untouched": True,
        "gen11": "HOLD",
    }
    J(FIX / "manifest.json", man)

    train_ids, train_amts = [], []
    if (TRAIN_FIX / "manifest.json").is_file():
        tman = json.loads((TRAIN_FIX / "manifest.json").read_text(encoding="utf-8"))
        train_ids = [it["id"] for it in tman.get("items") or []]
        train_amts = [it["expected"] for it in tman.get("items") or []]
    held_ids = [it["id"] for it in items]
    held_amts = [it["expected"] for it in items]
    disjoint = id_disjoint(train_ids, held_ids)
    amt_overlap = sorted(set(train_amts) & set(held_amts))

    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        out = {
            "cycle": "C322", "theme": "vision_v36_heldout", "gate": GATE,
            "timestamp": ts(), "attempted": False, "reason": f"gpu_free={free}",
            "n": len(items), "id_disjoint": disjoint, "amt_overlap": amt_overlap,
            "vl_gate_v36_heldout_claim": False, "pass": False, "claim": False,
            "gate2_3_untouched": True, "gen11": "HOLD",
        }
        J(DOC / "C322_VISION_V36_HELDOUT_SMOKE.json", out)
        print(json.dumps(out, ensure_ascii=False))
        return 1

    from evo.office.vision_backend import RealVlBackend
    from evo.office.vision_ocr import ocr_image
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
            print(json.dumps({
                "id": it["id"], "ok": ok, "got": got, "expected": it["expected"],
            }, ensure_ascii=False), flush=True)
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
    gate_pass = n >= 16 and rate >= GATE and disjoint
    claim = gate_pass
    scope = "r50plus_v36_heldout_hlx_magclip_n>=16_qwen35_2b_clarity_floor" if claim else None
    out = {
        "cycle": "C322",
        "theme": "vision_v36_heldout",
        "gate": GATE,
        "timestamp": ts(),
        "attempted": True,
        "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": rate,
        "gate_pass": gate_pass,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
        "rows": rows,
        "id_disjoint": disjoint,
        "amt_overlap": amt_overlap,
        "vl_gate_v36_heldout_claim": claim,
        "claim_scope": scope,
        "clarity_floor": man["clarity_floor"],
        "gate2_3_untouched": True,
        "gen11": "HOLD",
        "pass": gate_pass,
        "claim": claim,
    }
    J(DOC / "C322_VISION_V36_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if claim:
        J(DOC / "C322b_VISION_GATE_V36_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v36_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v36_heldout_claim": True,
            "rate": rate, "n": n, "n_ok": n_ok, "gate": GATE,
            "claim_scope": scope,
            "id_disjoint": disjoint,
            "gate2_3_untouched": True,
            "gen11": "HOLD",
            "cycle": "C322",
        })
    print(json.dumps({
        "cycle": "C322", "rate": rate, "n_ok": n_ok, "n": n,
        "fail_ids": out["fail_ids"], "disjoint": disjoint,
        "claim": claim, "pass": gate_pass,
    }, ensure_ascii=False))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
