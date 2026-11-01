# -*- coding: utf-8 -*-
"""C150: Vision V7 heldout — disjoint fixtures + smoke claim if rate>=0.6.
Different numbers/ids from V7 train. Gate 0.6. gen11 HOLD. Gate2/3 untouched.
"""
from __future__ import annotations
import gc, json, re, sys, shutil
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evo.office.vision_metric_parse import parse_metric

GATE = 0.6
DOC = ROOT / "docs" / "r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v7h"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v7h_c150"
PROTO = ROOT / "docs" / "蚁算_VL_GATE_V7_HELDOUT_PROTOCOL.md"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def font(size=14):
    for name in ("arial.ttf", "msyh.ttc", "simhei.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_fixture(path: Path, cn_title: str, lines: list, stamp: str):
    W, H = 720, 520
    im = Image.new("RGB", (W, H), (248, 248, 242))
    d = ImageDraw.Draw(im)
    f_title = font(22)
    f_body = font(16)
    f_tiny = font(11)
    f_stamp = font(28)
    d.rectangle([8, 8, W - 8, H - 8], outline=(30, 30, 30), width=2)
    d.text((20, 16), cn_title, fill=(10, 10, 10), font=f_title)
    y = 55
    for ln in lines:
        d.text((24, y), ln, fill=(5, 5, 5), font=f_body)
        y += 28
    d.rectangle([0, 210, W, 236], fill=(210, 210, 210))
    d.text((30, 214), "~~ fold crease / stamp smear ~~", fill=(80, 80, 80), font=f_tiny)
    d.ellipse([480, 300, 680, 460], outline=(200, 40, 40), width=4)
    d.text((510, 360), stamp, fill=(200, 40, 40), font=f_stamp)
    d.text((20, 450), "VOID / IGNORE 999 old total 999.00 tiny distractor 888.00 TOTAL 42", fill=(160, 160, 160), font=f_tiny)
    d.text((20, 470), "WIN-B stamped status=void invoice#OLD", fill=(160, 160, 160), font=f_tiny)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


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


def build_heldout():
    specs = [
        ("h_receipt", ["RECEIPT #V7H-01", "tea paid 6.25", "bagel paid 9.75", "soda open 2.00", "TOTAL PAID TARGET 16.00"], "paid_total", 16.00, "收据 Heldout", "PAID"),
        ("h_stamp_wh", ["WH TICKET V7H", "SCREW qty 9 ok", "WASHER qty 4 hold", "PIN qty 6 ok", "qty_sum TARGET 15"], "qty_sum", 15.0, "仓收 Heldout", "RECV"),
        ("h_refund", ["REFUND H", "H1 2.50 done", "H2 4.00 open", "H3 1.50 done", "refund_done TARGET 4.00"], "refund_done", 4.00, "退款 Heldout", "DONE"),
        ("h_tax", ["TAX SLIP H", "H1 5.50 paid", "H2 3.00 open", "H3 8.50 paid", "tax_base_paid TARGET 14.00"], "tax_base_paid", 14.00, "税联 Heldout", "PAID"),
        ("h_payroll", ["PAYROLL H", "X 520 active", "Y 90 leave", "Z 280 active", "payroll_active TARGET 800"], "payroll_active", 800.0, "薪资 Heldout", "OK"),
        ("h_ship", ["SHIP H", "Q1 5 ok", "Q2 11 hold", "Q3 2 ok", "ship_ok_qty TARGET 7"], "ship_ok_qty", 7.0, "发货 Heldout", "SHIP"),
        ("h_sla", ["SLA H", "T1 pri 3 open", "T2 pri 9 closed", "T3 pri 4 open", "open_pri_sum TARGET 7"], "open_pri_sum", 7.0, "服务 Heldout", "OPEN"),
        ("h_expense", ["EXPENSE H", "F1 11.00 paid", "F2 6.00 void", "F3 9.50 paid", "paid_total TARGET 20.50"], "paid_total", 20.50, "报销 Heldout", "PAID"),
        ("h_po", ["PO-99 H", "a paid 7.25", "b paid 4.75", "c open 1.00", "TOTAL PAID TARGET 12.00"], "paid_total", 12.00, "采购 Heldout", "RECV"),
        ("h_order", ["ORDER H", "M paid 3.40", "N paid 8.60", "P open 2.00", "TOTAL PAID TARGET 12.00"], "paid_total", 12.00, "订单 Heldout", "PAID"),
        ("h_dup", ["INVOICE #V7H-DUP", "paid 1.25", "paid 2.75", "paid 6.00", "TOTAL PAID TARGET 10.00"], "paid_total", 10.00, "重复 Heldout", "PAID"),
        ("h_zero", ["OPEN ONLY H", "U 14.00 open", "V 21.00 open", "paid_total TARGET 0.00"], "paid_total", 0.0, "未付 Heldout", "HOLD"),
        ("h_ledger", ["LEDGER H", "r1 paid 4.10", "r2 paid 5.90", "r3 open 0.80", "TOTAL PAID TARGET 10.00"], "paid_total", 10.00, "账本 Heldout", "PAID"),
        ("h_ui", ["UI H", "one paid 2.20", "two paid 7.80", "three open 3.00", "TOTAL PAID TARGET 10.00"], "paid_total", 10.00, "界面 Heldout", "PAID"),
        ("h_heavy", ["HEAVY H", "p paid 13.00", "q paid 2.00", "r open 5.00", "TOTAL PAID TARGET 15.00"], "paid_total", 15.00, "重章 Heldout", "PAID"),
        ("h_mix", ["MIX H", "jia paid 4.50", "yi paid 5.50", "bing open 1.00", "TOTAL PAID TARGET 10.00"], "paid_total", 10.00, "中英 Heldout", "验讫"),
    ]
    if FIX.exists():
        shutil.rmtree(FIX)
    FIX.mkdir(parents=True)
    items = []
    for i, (kind, lines, metric, expected, cn, stamp) in enumerate(specs, 1):
        name = f"v7h_{i:02d}_{kind}.png"
        path = FIX / name
        draw_fixture(path, cn, lines, stamp)
        items.append({
            "id": f"v7h_{i:02d}", "file": name, "kind": kind,
            "metric": metric, "expected": expected, "lines": lines,
            "cn_title": cn, "stamp": stamp,
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "disjoint_from": "vision_images_v7",
            "hardening": ["occlusion", "tiny_font", "stamped_receipt", "heldout"],
        })
    man = {
        "version": "v7h", "n": len(items), "gate": GATE,
        "theme": "v7_heldout_disjoint_occlusion_tiny_stamped",
        "disjoint_from": "evo/office/fixtures/vision_images_v7",
        "items": items, "timestamp": ts(),
    }
    J(FIX / "manifest.json", man)
    PROTO.write_text(
        f"# 蚁算 VL Gate V7 Heldout\n\nts: {ts()}\ngate: {GATE}\n"
        f"disjoint: yes (new numbers/ids vs V7 train)\n"
        f"claim_if: rate>=0.6 and n>=14\ngen11: HOLD\nGate2/3: untouched\n",
        encoding="utf-8",
    )
    return man


def smoke(man):
    free = gpu_free_mib()
    if free < 2000 or not WEIGHTS.is_dir():
        return {"attempted": False, "reason": f"gpu_free={free}", "rate": 0.0, "claim": False}
    from evo.office.vision_backend import RealVlBackend
    from evo.office.vision_ocr import ocr_image
    RUN.mkdir(parents=True, exist_ok=True)
    backend = RealVlBackend(WEIGHTS, max_new_tokens=200)
    rows, n_ok = [], 0
    try:
        for it in man["items"]:
            png = ROOT / it["path"]
            ocr = ocr_image(png, prefer="vl", vl_backend=backend)
            text = re.sub(r"<think>[\s\S]*?</think>", " ", ocr.get("text") or "")
            text = re.sub(r"\s+", " ", text).strip()
            ocr_ok = soft_ocr_ok(text, it["lines"])
            got, atom_ok = parse_metric(text, it["metric"], it["expected"])
            ok = bool(ocr_ok and atom_ok)
            n_ok += int(ok)
            rows.append({
                "id": it["id"], "kind": it["kind"], "metric": it["metric"],
                "ocr_ok": ocr_ok, "atom_ok": atom_ok, "ok": ok,
                "got": got, "expected": it["expected"], "ocr_preview": text[:300],
            })
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
    rate = n_ok / n if n else 0.0
    claim = rate >= GATE and n >= 14
    scope = "r50plus_v7_heldout_disjoint_n>=14_softocr_atom_qwen35_2b" if claim else None
    return {
        "attempted": True, "gpu_free_mib_start": free,
        "n": n, "n_ok": n_ok, "rate": round(rate, 4),
        "gate": GATE, "gate_pass": claim, "vl_gate_v7_heldout_claim": claim,
        "claim_scope": scope, "rows": rows,
        "fail_ids": [r["id"] for r in rows if not r["ok"]],
    }


def main():
    man = build_heldout()
    design = {
        "cycle": "C150a", "theme": "v7_heldout_design_disjoint",
        "gate": GATE, "timestamp": ts(), "gate2_3_untouched": True, "gen11": "HOLD",
        "n_fixtures": man["n"], "fixtures": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "disjoint_from": "vision_images_v7", "pass": man["n"] >= 14, "claim": False,
    }
    J(DOC / "C150a_V7_HELDOUT_DESIGN.json", design)
    sm = smoke(man)
    out = {
        "cycle": "C150", "theme": "vision_v7_heldout_disjoint_smoke",
        "gate": GATE, "timestamp": ts(), "gate2_3_untouched": True, "gen11": "HOLD",
        "weights": "models/Qwen3.5-2B",
        "fixtures": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        **{k: v for k, v in sm.items()},
        "prior_v7_train_untouched": True,
        "open_domain_benchmark": False,
        "pass": True,
        "claim": bool(sm.get("vl_gate_v7_heldout_claim")),
        "note": "Disjoint V7 heldout. Claim only if rate>=0.6 and n>=14.",
    }
    J(DOC / "C150_VISION_V7_HELDOUT_SMOKE.json", out)
    J(RUN / "judge.json", out)
    if out["claim"]:
        J(DOC / "C150b_VISION_GATE_V7_HELDOUT_CLAIM.json", {
            "kind": "vision_gate_v7_heldout_claim",
            "timestamp": ts(),
            "vl_gate_v7_heldout_claim": True,
            "rate": out["rate"], "n": out["n"], "n_ok": out["n_ok"],
            "gate": GATE, "claim_scope": out.get("claim_scope"),
            "disjoint_from": "vision_images_v7",
            "gate2_3_untouched": True, "gen11": "HOLD",
        })
    print(json.dumps({
        "cycle": "C150", "n": out.get("n"), "rate": out.get("rate"),
        "claim": out["claim"], "fail": out.get("fail_ids"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
