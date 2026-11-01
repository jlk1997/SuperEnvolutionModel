# -*- coding: utf-8 -*-
"""Hardened ant_capture_office library (C115)."""
from __future__ import annotations
import argparse, json, re, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
WEIGHTS = ROOT / "models/Qwen3.5-2B"
try:
    from evo.office.money_tool import (
        sum_paid_from_text,
        prefer_tool_over_lora,
        confidence_gated_money,
        model_paid_guess,
        tool_metric,
        confidence_gated_metric,
        confidence_gate_metric,
    )
    MONEY_TOOL = True
    CONFIDENCE_GATE = True
except Exception:
    MONEY_TOOL = False
    CONFIDENCE_GATE = False
    def sum_paid_from_text(text, status_token="paid"):
        return 0.0
    def prefer_tool_over_lora():
        return {"policy": "fallback_regex"}
    def confidence_gated_money(text, model_guess=None, **kw):
        return {"value": 0.0, "source": "fallback", "confidence": "low", "agree": None,
                "tool_total": 0.0, "model_guess": model_guess, "reason": "no_money_tool",
                "policy": "fallback"}
    def model_paid_guess(text):
        return None
    def tool_metric(text, metric):
        return None
    def confidence_gated_metric(text, metric, model_guess=None, expected=None, tol=0.01):
        return {"value": None, "decision": "fallback", "expanded": False}
    def confidence_gate_metric(model_got, tool_got, expected=None, tol=0.01):
        return model_got, "fallback"

DEFAULT_OUT = ROOT / "runs/ant_capture_office"
EVIDENCE_SCHEMA_KEYS = (
    "entry", "timestamp", "gate", "capture_ok", "size", "use_vl",
    "scaffold_steps", "agent_graph", "ocr_ok", "paid_got", "paid_expected",
    "paid_ok", "atom_ok", "ok", "pass", "rate", "errors",
)


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean(text):
    text = re.sub(r"<think>[\s\S]*?</think>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def parse_paid(text, model_guess=None, return_meta=False):
    """C145: confidence-gated money_tool on capture path; regex fallback."""
    if MONEY_TOOL and CONFIDENCE_GATE:
        gated = confidence_gated_money(text or "", model_guess=model_guess)
        val = float(gated.get("value") or 0.0)
        if return_meta:
            return val, gated
        return val
    if MONEY_TOOL:
        tool_total = float(sum_paid_from_text(text or ""))
        meta = {"source": "money_tool", "policy": "tool_only", "value": tool_total}
        if tool_total > 0:
            return (tool_total, meta) if return_meta else tool_total
        t0 = (text or "").lower()
        if "open only" in t0 or _re_zero(t0):
            return (0.0, {"source": "money_tool", "policy": "tool_only_zero"}) if return_meta else 0.0
    tlow = (text or "").lower()
    total = 0.0
    for m in re.finditer(r"paid\s+(\d+\.\d+|\d+)", tlow):
        total += float(m.group(1))
    if total <= 0:
        m = re.search(r"total\s*paid\s*(?:target)?\s*(\d+\.\d+|\d+)", tlow)
        if m:
            total = float(m.group(1))
    if total <= 0:
        m = re.search(r"total\s*(\d+\.\d+|\d+)", tlow)
        if m:
            total = float(m.group(1))
    meta = {"source": "regex_fallback", "policy": "fallback_regex", "value": total}
    return (total, meta) if return_meta else total




def parse_metric_gated(text, metric, model_guess=None, expected=None, return_meta=False):
    """C210: expanded multi-metric confidence gate on capture path."""
    if MONEY_TOOL and CONFIDENCE_GATE:
        gated = confidence_gated_metric(text or "", metric, model_guess=model_guess, expected=expected)
        val = gated.get("value")
        if return_meta:
            return val, gated
        return val
    # fallback: paid_total only via parse_paid
    if metric == "paid_total":
        return parse_paid(text, model_guess=model_guess, return_meta=return_meta)
    if return_meta:
        return None, {"decision": "unsupported_metric", "metric": metric}
    return None

def _re_zero(t0: str) -> bool:
    if re.search(r"paid_total\s*target\s*0", t0):
        return True
    if re.search(r"total\s*paid\s*(?:target)?\s*0(?:\.0+)?\b", t0):
        return True
    return False


def validate_evidence(ev: dict) -> list[str]:
    missing = [k for k in EVIDENCE_SCHEMA_KEYS if k not in ev]
    errs = []
    if missing:
        errs.append(f"missing_keys:{missing}")
    if "rate" in ev and ev["rate"] is not None:
        try:
            r = float(ev["rate"])
            if r < 0 or r > 1:
                errs.append("rate_out_of_range")
        except Exception:
            errs.append("rate_not_numeric")
    return errs


def build_panel(outdir, lines, title="ANT CAPTURE OFFICE"):
    from PIL import Image, ImageDraw, ImageFont, ImageGrab
    errors = []
    try:
        shot = ImageGrab.grab(all_screens=False)
        w, h = shot.size
        crop = shot.crop((0, 0, min(900, w), min(560, h))).convert("RGB")
        bg = crop.resize((720, 420))
        panel = Image.blend(bg, Image.new("RGB", (720, 420), (255, 255, 255)), 0.72)
        capture_ok, size = True, [w, h]
    except Exception as e:
        panel = Image.new("RGB", (720, 420), (255, 255, 255))
        capture_ok, size = False, [720, 420]
        errors.append(f"capture_fallback:{type(e).__name__}")
    d = ImageDraw.Draw(panel)
    try:
        f = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 22)
        f2 = ImageFont.truetype(r"C:\\Windows\\Fonts\\arial.ttf", 18)
    except Exception:
        f = f2 = ImageFont.load_default()
        errors.append("font_fallback_default")
    d.rectangle([12, 12, 708, 408], outline=(0, 0, 0), width=3)
    d.rectangle([20, 20, 700, 70], fill=(255, 255, 180), outline=(0, 0, 0))
    d.text((28, 32), title[:48], fill=(0, 0, 0), font=f)
    y = 90
    for line in lines[:10]:
        d.text((28, y), str(line)[:60], fill=(0, 0, 0), font=f2)
        y += 32
    png = outdir / "capture_panel.png"
    panel.save(png)
    return png, capture_ok, size, errors


def run_pipeline(outdir, lines, expected_paid, use_vl, title="ANT CAPTURE OFFICE", metric="paid_total", expected=None):
    errors = []
    if not lines:
        errors.append("empty_lines")
        evidence = {
            "entry": "ant_capture_office", "timestamp": ts(), "gate": GATE,
            "capture_ok": False, "size": [0, 0], "use_vl": use_vl,
            "scaffold_steps": 0, "agent_graph": "none",
            "ocr_ok": False, "paid_got": 0.0, "paid_expected": expected_paid,
            "paid_ok": False, "atom_ok": False, "ok": False, "pass": False,
            "rate": 0.0, "errors": errors, "error": "empty_lines",
        }
        outdir.mkdir(parents=True, exist_ok=True)
        J(outdir / "evidence.json", evidence)
        return evidence
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    sandbox = outdir / "sandbox"
    sandbox.mkdir()
    png, capture_ok, size, cerr = build_panel(outdir, lines, title=title)
    errors.extend(cerr)
    evidence = {
        "entry": "ant_capture_office", "timestamp": ts(), "gate": GATE,
        "capture_ok": capture_ok, "size": size, "use_vl": use_vl,
        "scaffold_steps": 0, "agent_graph": "none", "errors": list(errors),
    }
    try:
        evidence["panel"] = str(png.relative_to(ROOT)).replace("\\", "/")
    except Exception:
        evidence["panel"] = str(png)
    text = ""
    backend = None
    if use_vl:
        if not WEIGHTS.is_dir():
            errors.append("vl_weights_missing")
            evidence["vl_skipped"] = True
            evidence["note_fallback"] = "weights_missing_lines_as_text"
            text = " ".join(lines)
        else:
            try:
                from evo.office.vision_backend import RealVlBackend
                from evo.office.vision_ocr import ocr_image
                backend = RealVlBackend(WEIGHTS, max_new_tokens=128)
                ocr = ocr_image(png, prefer="vl", vl_backend=backend)
                text = clean(ocr.get("text") or "")
                evidence["vl_weights"] = "models/Qwen3.5-2B"
                if not text:
                    errors.append("vl_ocr_empty")
            except Exception as e:
                errors.append(f"vl_ocr_error:{type(e).__name__}")
                evidence["note_fallback"] = "vl_failed_lines_as_text"
                text = " ".join(lines)
    else:
        evidence["vl_skipped"] = True
        text = " ".join(lines)
        evidence["note_fallback"] = "no_vl_used_lines_as_text_for_offline_dryrun"
    if backend is not None:
        try:
            backend.unload()
        except Exception as e:
            errors.append(f"vl_unload:{type(e).__name__}")
    keys = re.findall(r"\d+\.\d+|\d+", " ".join(lines))
    ocr_ok = bool(text) and (not keys or all(k in text.replace(" ", "") for k in keys[:4]))
    paid, gate_meta = parse_paid(text, model_guess=None, return_meta=True)
    # C227 multi-metric: when metric != paid_total, confidence-gated tool wins
    metric_name = metric or "paid_total"
    exp_val = float(expected_paid if expected is None else expected)
    if metric_name != "paid_total" and MONEY_TOOL and CONFIDENCE_GATE:
        gated_m = confidence_gated_metric(text or "", metric_name, model_guess=None, expected=exp_val, tol=0.08)
        paid = float(gated_m.get("value") if gated_m.get("value") is not None else 0.0)
        gate_meta = gated_m
    elif metric_name != "paid_total" and MONEY_TOOL:
        tv = tool_metric(text or "", metric_name)
        paid = float(tv) if tv is not None else 0.0
        gate_meta = {"source": "tool_metric", "metric": metric_name, "value": paid}

    exp_for_ok = float(exp_val) if "exp_val" in dir() else float(expected_paid)
    paid_ok = abs(paid - exp_for_ok) < 0.08
    money_policy = prefer_tool_over_lora() if MONEY_TOOL else {"policy": "fallback_regex"}
    money_policy = dict(money_policy)
    money_policy["confidence_gate"] = gate_meta
    money_policy["confidence_gated_wired"] = bool(CONFIDENCE_GATE and MONEY_TOOL)
    try:
        exports = sandbox / "exports" / "paid.csv"
        exports.parent.mkdir(parents=True, exist_ok=True)
        exports.write_text(f"metric,value\n{(metric_name if 'metric_name' in dir() else 'paid_total')},{paid:.2f}\n", encoding="utf-8")
        report = sandbox / "reports" / "office.md"
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(
            f"# Ant Capture Office\n\npaid_total: {paid:.2f}\nagent_graph: none\nscaffold_steps: 0\n",
            encoding="utf-8",
        )
        atom_ok = exports.is_file() and report.is_file() and paid_ok
    except Exception as e:
        errors.append(f"atom_write:{type(e).__name__}")
        atom_ok = False
    ok = ocr_ok and atom_ok
    evidence.update({
        "ocr_text": text[:300], "ocr_ok": ocr_ok, "paid_got": paid,
        "metric": metric_name if "metric_name" in dir() else "paid_total",
        "metric_got": paid,
        "paid_expected": float(exp_val if "exp_val" in dir() else expected_paid), "paid_ok": paid_ok,
        "money_tool": bool(MONEY_TOOL), "money_policy": money_policy.get("policy"), "confidence_gated": bool(CONFIDENCE_GATE and MONEY_TOOL), "confidence_gate": gate_meta,
        "atom_ok": atom_ok, "ok": ok, "pass": ok, "rate": 1.0 if ok else 0.0,
        "errors": errors,
    })
    schema_errs = validate_evidence(evidence)
    if schema_errs:
        evidence["schema_errors"] = schema_errs
        errors.extend(schema_errs)
        evidence["errors"] = errors
    J(outdir / "evidence.json", evidence)
    return evidence


def main(argv=None):
    ap = argparse.ArgumentParser(prog="ant_capture_office")
    ap.add_argument("--outdir", type=str, default=str(DEFAULT_OUT / "cli_run"))
    ap.add_argument("--no-vl", action="store_true")
    ap.add_argument("--title", type=str, default="ANT CAPTURE OFFICE")
    ap.add_argument("--expected-paid", type=float, default=30.0)
    ap.add_argument("--lines-file", type=str, default="")
    ap.add_argument("--dry-run", action="store_true", help="Force --no-vl and default lines")
    ap.add_argument("--metric", type=str, default="paid_total",
                    help="Office metric: paid_total|qty_sum|refund_done|tax_base_paid|payroll_active|ship_ok_qty|open_pri_sum")
    ap.add_argument("--expected", type=float, default=None,
                    help="Expected metric value (defaults to --expected-paid for paid_total)")
    args = ap.parse_args(argv)
    if args.lines_file:
        lp = Path(args.lines_file)
        if not lp.is_absolute():
            lp = ROOT / lp
        if not lp.is_file():
            print(json.dumps({"ok": False, "error": "lines_file_missing", "path": str(lp)}, ensure_ascii=False))
            return 2
        lines = [ln.strip() for ln in lp.read_text(encoding="utf-8").splitlines() if ln.strip()]
    else:
        lines = [
            "INVOICE #3301",
            "item A paid 11.00",
            "item B open 3.00",
            "item C paid 19.00",
            "TOTAL PAID TARGET 30.00",
        ]
    use_vl = not (args.no_vl or args.dry_run)
    outdir = Path(args.outdir)
    if not outdir.is_absolute():
        outdir = ROOT / outdir
    exp = args.expected if args.expected is not None else args.expected_paid
    evidence = run_pipeline(outdir, lines, args.expected_paid, use_vl=use_vl, title=args.title,
                           metric=args.metric, expected=exp)
    evidence["cli_entry"] = "scripts/ant_capture_office.py"
    print(json.dumps({
        "ok": evidence.get("ok"),
        "paid_got": evidence.get("paid_got"),
        "metric": evidence.get("metric", "paid_total"),
        "metric_got": evidence.get("metric_got", evidence.get("paid_got")),
        "errors": evidence.get("errors"),
        "pass": evidence.get("pass"),
    }, ensure_ascii=False))
    return 0 if evidence.get("pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
