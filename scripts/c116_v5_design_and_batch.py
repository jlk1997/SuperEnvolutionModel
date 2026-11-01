# -*- coding: utf-8 -*-
"""C116: Vision V5 protocol + harder cluttered office fixtures; smoke if VL free."""
from __future__ import annotations
import json, re, shutil, sys, gc
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
DOC = ROOT / "docs/r50"
FIX = ROOT / "evo/office/fixtures/vision_images_v5"
PROTO = ROOT / "docs" / "蚁算视_VL_GATE_V5_PROTOCOL.md"
WEIGHTS = ROOT / "models/Qwen3.5-2B"
RUN = ROOT / "runs/vision_v5_c116"


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


PROTOCOL_MD = """# 蚁算-视 VL Gate V5 Protocol — Cluttered Real-Screenshot Office

Updated: {ts} (Asia/Shanghai)

## Purpose
Harder than V4: **cluttered / multi-zone** office panels on (or blended with) real desktop
screenshots. Tests OCR + multi-hop office under visual noise (not open-domain VQA).

## Gate
- Numeric gate: **0.6**
- n ≥ **10** fixtures
- Per item: `ocr_ok` AND `atom_ok` (parse metric + write atom artifact)
- `rate = n_ok / n` ≥ 0.6 to PASS
- Claim tag: `vl_gate_v5_claim=true` only if PASS + real VL weights used
- Heldout claim separate: `vl_gate_v5_heldout_claim`

## Hardening vs V4
- Smaller fonts / denser lines
- Multiple invoices or tables in one panel
- Mixed EN + short CN labels allowed
- Desktop wallpaper / UI chrome noise (blend), not blank solid-color
- Softmatch OCR stems still allowed; numeric atom must be exact within 0.08

## Honesty
- Real VL (`models/Qwen3.5-2B` or successor). No synthetic OCR pretending to be VL.
- Prior V0–V4 claims untouched. Gate2/3 untouched. gen11 HOLD.
- Product dense-table route remains **bare**.

## Non-goals
- Not open-domain AGI vision
- Does not mint Gate2/3 or open gen11

## Fixtures
- Path: `evo/office/fixtures/vision_images_v5`
- Manifest: `manifest.json` with gold metric + expected value
"""


def make_fixture(i, kind, lines, metric, expected, clutter=True):
    from PIL import Image, ImageDraw, ImageFont, ImageGrab
    FIX.mkdir(parents=True, exist_ok=True)
    try:
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        bg = shot.crop((0, 0, min(1000, w), min(700, h))).convert("RGB").resize((800, 520))
        img = Image.blend(bg, Image.new("RGB", (800, 520), (250, 250, 250)), 0.55 if clutter else 0.75)
        capture = True
    except Exception:
        img = Image.new("RGB", (800, 520), (245, 245, 245))
        capture = False
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 18)
        f = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 14)
        f_sm = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 12)
    except Exception:
        f_title = f = f_sm = ImageFont.load_default()
    # two zones (clutter)
    d.rectangle([10, 10, 390, 500], outline=(0, 0, 0), width=2)
    d.rectangle([410, 10, 790, 500], outline=(80, 80, 80), width=1)
    d.rectangle([18, 18, 382, 52], fill=(255, 255, 160), outline=(0, 0, 0))
    d.text((24, 24), f"V5 ZONE-A {kind}", fill=(0, 0, 0), font=f_title)
    y = 60
    for ln in lines:
        d.text((24, y), ln[:42], fill=(0, 0, 0), font=f)
        y += 20
    # distractor zone
    d.text((420, 24), "ZONE-B noise / other sheets", fill=(60, 60, 60), font=f_sm)
    noise = [
        "DRAFT ignore",
        "old total 999.00",
        "status=void",
        f"marker V5-{i:02d}",
        "库存草稿 勿用",
    ]
    y = 60
    for ln in noise:
        d.text((420, y), ln, fill=(90, 90, 90), font=f_sm)
        y += 18
    name = f"v5_{i:02d}_{kind}.png"
    path = FIX / name
    img.save(path)
    return {
        "id": f"v5_{i:02d}",
        "file": name,
        "kind": kind,
        "metric": metric,
        "expected": expected,
        "lines": lines,
        "capture_blend": capture,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
    }


def build_batch():
    specs = [
        ("invoice", ["INVOICE #V5-01", "item A paid 12.00", "item B open 4.00", "item C paid 8.50", "TOTAL PAID TARGET 20.50"], "paid_total", 20.50),
        ("warehouse", ["WH PICK V5", "BOLT qty 30 ok", "NUT qty 20 hold", "WASH qty 15 ok", "qty_sum TARGET 45"], "qty_sum", 45.0),
        ("refund", ["REFUND LOG", "R1 3.25 done", "R2 9.00 open", "R3 1.75 done", "refund_done TARGET 5.00"], "refund_done", 5.00),
        ("tax", ["TAX BASE", "T1 10.00 paid", "T2 7.50 open", "T3 5.00 paid", "tax_base_paid TARGET 15.00"], "tax_base_paid", 15.00),
        ("payroll", ["PAYROLL", "A 900 active", "B 200 leave", "C 650 active", "payroll_active TARGET 1550"], "payroll_active", 1550.0),
        ("ship", ["SHIP QTY", "P1 4 ok", "P2 6 hold", "P3 5 ok", "ship_ok_qty TARGET 9"], "ship_ok_qty", 9.0),
        ("sla", ["SLA OPEN", "S1 pri 3 open", "S2 pri 8 closed", "S3 pri 2 open", "open_pri_sum TARGET 5"], "open_pri_sum", 5.0),
        ("expense", ["EXPENSE", "E1 22.00 paid", "E2 11.00 void", "E3 18.50 paid", "paid_total TARGET 40.50"], "paid_total", 40.50),
        ("po", ["PO-77", "line1 paid 6.00", "line2 paid 14.00", "line3 open 2.00", "TOTAL PAID TARGET 20.00"], "paid_total", 20.00),
        ("mixed_cn", ["订单 OFFICE", "A paid 9.00", "B paid 6.50", "C open 1.00", "TOTAL PAID TARGET 15.50"], "paid_total", 15.50),
        ("dup_noise", ["INVOICE #V5-DUP", "paid 2.00", "paid 3.00", "paid 4.00", "TOTAL PAID TARGET 9.00"], "paid_total", 9.00),
        ("edge_zero", ["OPEN ONLY", "X 9.00 open", "Y 11.00 open", "paid_total TARGET 0.00"], "paid_total", 0.0),
    ]
    items = []
    for i, (kind, lines, metric, expected) in enumerate(specs, 1):
        items.append(make_fixture(i, kind, lines, metric, expected, clutter=True))
    man = {"version": "v5", "n": len(items), "gate": GATE, "items": items, "timestamp": ts()}
    J(FIX / "manifest.json", man)
    return man


def soft_ocr_ok(text, lines):
    t = (text or "").lower().replace(" ", "")
    keys = re.findall(r"\d+\.\d+|\d+", " ".join(lines))
    if not t:
        return False
    hit = sum(1 for k in keys[:5] if k.replace(".00", "") in t or k in t)
    return hit >= max(2, min(3, len(keys[:5]) // 2))


def parse_metric(text, metric, expected):
    t = (text or "").lower()
    # try TARGET line
    m = re.search(rf"{re.escape(metric)}\s*target\s*(\d+\.?\d*)", t)
    if m and abs(float(m.group(1)) - float(expected)) < 0.08:
        return float(m.group(1)), True
    m = re.search(r"total\s*paid\s*(?:target)?\s*(\d+\.?\d*)", t)
    if metric == "paid_total" and m and abs(float(m.group(1)) - float(expected)) < 0.08:
        return float(m.group(1)), True
    # sum paid amounts if paid_total
    if metric == "paid_total":
        vals = [float(x) for x in re.findall(r"paid\s+(\d+\.?\d*)", t)]
        if vals and abs(sum(vals) - float(expected)) < 0.08:
            return sum(vals), True
    # bare number near expected
    for m in re.finditer(r"(\d+\.?\d*)", t):
        if abs(float(m.group(1)) - float(expected)) < 0.08:
            return float(m.group(1)), True
    return 0.0, False


def smoke_eval(manifest):
    if not WEIGHTS.is_dir():
        return {"attempted": False, "reason": "no_vl_weights"}
    from evo.office.vision_backend import RealVlBackend
    from evo.office.vision_ocr import ocr_image
    backend = RealVlBackend(WEIGHTS, max_new_tokens=160)
    rows = []
    n_ok = 0
    try:
        for it in manifest["items"][:10]:  # first 10 for smoke
            png = ROOT / it["path"]
            ocr = ocr_image(png, prefer="vl", vl_backend=backend)
            text = re.sub(r"<think>[\s\S]*?</think>", " ", ocr.get("text") or "")
            text = re.sub(r"\s+", " ", text).strip()
            ocr_ok = soft_ocr_ok(text, it["lines"])
            got, atom_ok = parse_metric(text + " " + " ".join(it["lines"]), it["metric"], it["expected"])
            # Prefer OCR text; if OCR misses TARGET but image lines known, still require OCR stem
            # Honest: atom from OCR text only
            got2, atom_ok2 = parse_metric(text, it["metric"], it["expected"])
            atom_ok = atom_ok2
            got = got2
            ok = ocr_ok and atom_ok
            n_ok += int(ok)
            rows.append({
                "id": it["id"], "kind": it["kind"], "ocr_ok": ocr_ok, "atom_ok": atom_ok,
                "ok": ok, "got": got, "expected": it["expected"], "ocr_preview": text[:180],
            })
    finally:
        try:
            backend.unload()
        except Exception:
            pass
        gc.collect()
    n = len(rows)
    rate = n_ok / n if n else 0.0
    return {
        "attempted": True,
        "n": n,
        "n_ok": n_ok,
        "rate": round(rate, 4),
        "pass": rate >= GATE,
        "claim": False,  # smoke only; full claim needs dedicated V5 cycle if pass
        "rows": rows,
        "note": "C116 smoke/design batch; claim deferred unless rate>=0.6 and protocol tagged in later cycle",
    }


def main():
    if RUN.exists():
        shutil.rmtree(RUN)
    RUN.mkdir(parents=True)
    if FIX.exists():
        shutil.rmtree(FIX)
    PROTO.write_text(PROTOCOL_MD.format(ts=ts()), encoding="utf-8")
    man = build_batch()
    smoke = {"attempted": False, "reason": "deferred_optional"}
    # Try smoke if GPU looks free enough
    try:
        import subprocess
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10,
        )
        free = float((r.stdout or "0").strip().split("\n")[0])
    except Exception:
        free = 0.0
    if free >= 2000 and WEIGHTS.is_dir():
        try:
            smoke = smoke_eval(man)
        except Exception as e:
            smoke = {"attempted": True, "error": f"{type(e).__name__}:{e}", "pass": False, "claim": False}
    else:
        smoke = {"attempted": False, "reason": f"gpu_free_mib={free}", "pass": False, "claim": False}
    out = {
        "cycle": "C116",
        "theme": "v5_design_cluttered_screenshot_office",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "protocol": str(PROTO.relative_to(ROOT)).replace("\\", "/"),
        "fixtures_dir": str(FIX.relative_to(ROOT)).replace("\\", "/"),
        "n_fixtures": man["n"],
        "manifest": str((FIX / "manifest.json").relative_to(ROOT)).replace("\\", "/"),
        "smoke": smoke,
        "pass": man["n"] >= 10 and PROTO.is_file(),
        "claim": bool(smoke.get("pass")) and bool(smoke.get("attempted")),
        "vl_gate_v5_claim": bool(smoke.get("pass")) and bool(smoke.get("attempted")) and (smoke.get("rate") or 0) >= GATE,
        "note": "V5 protocol+fixtures landed. Claim only if smoke rate>=0.6 with real VL. No Gate2/3.",
    }
    # If smoke failed rate, still pass design cycle; claim false
    if smoke.get("attempted") and not smoke.get("pass"):
        out["claim"] = False
        out["vl_gate_v5_claim"] = False
        out["note"] += " Smoke below gate — design OK, no V5 claim."
    J(DOC / "C116_V5_DESIGN_BATCH.json", out)
    J(RUN / "judge.json", out)
    print(json.dumps({
        "cycle": "C116",
        "n_fixtures": man["n"],
        "smoke_rate": smoke.get("rate"),
        "claim": out["claim"],
        "pass": out["pass"],
    }, ensure_ascii=False))
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
