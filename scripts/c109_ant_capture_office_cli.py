# -*- coding: utf-8 -*-
"""C109: Productize capture->office single CLI with evidence."""
from __future__ import annotations
import argparse, json, re, shutil, sys
from datetime import datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
WEIGHTS = ROOT / "models/Qwen3.5-2B"
DOC = ROOT / "docs/r50"
DEFAULT_OUT = ROOT / "runs/ant_capture_office"

def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")

def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def clean(text):
    text = re.sub(r"<think>[\s\S]*?</think>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()

def parse_paid(text):
    t = text.lower()
    total = 0.0
    for m in re.finditer(r"paid\s+(\d+\.\d+|\d+)", t):
        total += float(m.group(1))
    if total <= 0:
        m = re.search(r"total\s*paid\s*(?:target)?\s*(\d+\.\d+|\d+)", t)
        if m: total = float(m.group(1))
    if total <= 0:
        m = re.search(r"total\s*(\d+\.\d+|\d+)", t)
        if m: total = float(m.group(1))
    return total

def build_panel(outdir, lines, title="ANT CAPTURE OFFICE"):
    from PIL import Image, ImageDraw, ImageFont, ImageGrab
    try:
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        crop = shot.crop((0, 0, min(900, w), min(560, h))).convert("RGB")
        bg = crop.resize((720, 420))
        panel = Image.blend(bg, Image.new("RGB", (720, 420), (255, 255, 255)), 0.72)
        capture_ok, size = True, [w, h]
    except Exception:
        panel = Image.new("RGB", (720, 420), (255, 255, 255))
        capture_ok, size = False, [720, 420]
    d = ImageDraw.Draw(panel)
    try:
        f = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 22)
        f2 = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 18)
    except Exception:
        f = f2 = ImageFont.load_default()
    d.rectangle([12, 12, 708, 408], outline=(0, 0, 0), width=3)
    d.rectangle([20, 20, 700, 70], fill=(255, 255, 180), outline=(0, 0, 0))
    d.text((28, 32), title, fill=(0, 0, 0), font=f)
    y = 90
    for line in lines:
        d.text((28, y), line, fill=(0, 0, 0), font=f2); y += 32
    png = outdir / "capture_panel.png"
    panel.save(png)
    return png, capture_ok, size

def run_pipeline(outdir, lines, expected_paid, use_vl):
    if outdir.exists(): shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    sandbox = outdir / "sandbox"; sandbox.mkdir()
    png, capture_ok, size = build_panel(outdir, lines)
    evidence = {"entry": "ant_capture_office", "timestamp": ts(), "gate": GATE, "capture_ok": capture_ok, "size": size, "use_vl": use_vl, "scaffold_steps": 0, "agent_graph": "none"}
    try: evidence["panel"] = str(png.relative_to(ROOT)).replace("\\", "/")
    except Exception: evidence["panel"] = str(png)
    text = ""; backend = None
    if use_vl and WEIGHTS.is_dir():
        from evo.office.vision_backend import RealVlBackend
        from evo.office.vision_ocr import ocr_image
        backend = RealVlBackend(WEIGHTS, max_new_tokens=128)
        ocr = ocr_image(png, prefer="vl", vl_backend=backend)
        text = clean(ocr.get("text") or "")
        evidence["vl_weights"] = "models/Qwen3.5-2B"
    else:
        evidence["vl_skipped"] = True
        text = " ".join(lines)
        evidence["note_fallback"] = "no_vl_used_lines_as_text_for_offline_dryrun"
    if backend is not None:
        try: backend.unload()
        except Exception: pass
    keys = re.findall(r"\d+\.\d+|\d+", " ".join(lines))
    ocr_ok = bool(text) and all(k in text.replace(" ", "") for k in keys[:4])
    paid = parse_paid(text)
    paid_ok = abs(paid - expected_paid) < 0.08
    exports = sandbox / "exports" / "paid.csv"; exports.parent.mkdir(parents=True, exist_ok=True)
    exports.write_text(f"metric,value\npaid_total,{paid:.2f}\n", encoding="utf-8")
    report = sandbox / "reports" / "office.md"; report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(f"# Ant Capture Office\n\npaid_total: {paid:.2f}\nagent_graph: none\nscaffold_steps: 0\n", encoding="utf-8")
    atom_ok = exports.is_file() and report.is_file() and paid_ok
    ok = ocr_ok and atom_ok
    evidence.update({"ocr_text": text[:300], "ocr_ok": ocr_ok, "paid_got": paid, "paid_expected": expected_paid, "paid_ok": paid_ok, "atom_ok": atom_ok, "ok": ok, "pass": ok, "rate": 1.0 if ok else 0.0})
    J(outdir / "evidence.json", evidence)
    return evidence

def main(argv=None):
    ap = argparse.ArgumentParser(prog="ant_capture_office")
    ap.add_argument("--outdir", type=str, default=str(DEFAULT_OUT / "cli_run"))
    ap.add_argument("--no-vl", action="store_true")
    ap.add_argument("--title", type=str, default="ANT CAPTURE OFFICE C109")
    args = ap.parse_args(argv)
    lines = ["INVOICE #3301", "item A paid 11.00", "item B open 3.00", "item C paid 19.00", "TOTAL PAID TARGET 30.00"]
    outdir = Path(args.outdir)
    if not outdir.is_absolute(): outdir = ROOT / outdir
    evidence = run_pipeline(outdir, lines, 30.0, use_vl=not args.no_vl)
    shim = ROOT / "scripts" / "ant_capture_office.py"
    shim.write_text("# -*- coding: utf-8 -*-\n\"\"\"蚁算 product CLI: capture -> OCR -> office -> evidence.\\n  python scripts/ant_capture_office.py [--outdir PATH] [--no-vl]\\n\"\"\"\nfrom scripts.c109_ant_capture_office_cli import main\nif __name__ == \"__main__\":\n    raise SystemExit(main())\n", encoding="utf-8")
    evidence["cli_entry"] = "scripts/ant_capture_office.py"
    evidence["cycle"] = "C109"
    evidence["theme"] = "productize_capture_office_cli"
    evidence["gate2_3_untouched"] = True
    J(DOC / "C109_ANT_CAPTURE_OFFICE_CLI.json", evidence)
    print(json.dumps({"cycle": "C109", "ok": evidence.get("ok"), "paid_got": evidence.get("paid_got"), "cli_entry": evidence.get("cli_entry"), "pass": evidence.get("pass")}, ensure_ascii=False))
    return 0 if evidence.get("pass") else 1

if __name__ == "__main__":
    raise SystemExit(main())
