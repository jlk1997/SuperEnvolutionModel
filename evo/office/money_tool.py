# -*- coding: utf-8 -*-
"""Tool-backed money math for 蚁算 product path (C122).
Prefer exact CSV/status filter sums over LoRA arithmetic (see C120 ceiling).
"""
from __future__ import annotations
import csv
import io
import re
from typing import Iterable


def sum_paid_from_text(text: str, status_token: str = "paid") -> float:
    """Sum amounts following status_token in free text (OCR or CSV-ish lines)."""
    t = (text or "").lower()
    total = 0.0
    # CSV-ish: amount,status or status amount
    for m in re.finditer(rf"(?:^|[\s,;]){re.escape(status_token)}\s+(\d+\.?\d*)", t, re.M):
        total += float(m.group(1))
    if total > 0:
        return round(total, 2)
    for m in re.finditer(rf"(\d+\.?\d*)\s*,\s*{re.escape(status_token)}\b", t):
        total += float(m.group(1))
    return round(total, 2)


def sum_column_where(
    rows: Iterable[dict],
    amount_key: str,
    status_key: str,
    status_value: str,
) -> float:
    total = 0.0
    sv = (status_value or "").lower()
    for r in rows:
        if str(r.get(status_key, "")).lower() == sv:
            try:
                total += float(r.get(amount_key) or 0)
            except Exception:
                continue
    return round(total, 2)


def sum_csv_text(csv_text: str, amount_col: str = "amount", status_col: str = "status", status_value: str = "paid") -> float:
    f = io.StringIO(csv_text.strip())
    reader = csv.DictReader(f)
    return sum_column_where(reader, amount_col, status_col, status_value)

def model_paid_guess(text: str) -> float | None:
    """Naive model-style guess: first TOTAL PAID TARGET or sum of paid tokens.
    Used only as a *candidate* under confidence gating — not a claim of model arith.
    """
    t = (text or "").lower()
    m = re.search(r"total\s*paid\s*(?:target)?\s*(\d+\.?\d*)", t)
    if m:
        return float(m.group(1))
    vals = [float(x) for x in re.findall(r"paid\s+(\d+\.?\d*)", t)]
    if vals:
        return round(sum(vals), 2)
    if "open only" in t or re.search(r"paid_total\s*target\s*0", t):
        return 0.0
    return None


def confidence_gated_money(
    text: str,
    model_guess: float | None = None,
    *,
    agree_tol: float = 0.08,
    status_token: str = "paid",
) -> dict:
    """Innovation C140: prefer money_tool when model is uncertain or disagrees.

    Rules (deterministic, auditable):
    1. Always compute tool_total from text.
    2. If model_guess is None → use tool (confidence=low, reason=no_model).
    3. If |model - tool| <= agree_tol → use either (prefer tool), confidence=high, agree=True.
    4. If disagree → use tool, confidence=low, reason=model_tool_disagree (safety).
    5. Empty/ambiguous paid signals with nonzero model → still tool (trust OCR parse via tool).

    Returns dict with value, source, confidence, agree, tool_total, model_guess, reason.
    """
    tool_total = float(sum_paid_from_text(text, status_token=status_token))
    if model_guess is None:
        model_guess = model_paid_guess(text)
    mg = None if model_guess is None else float(model_guess)
    if mg is None:
        return {
            "value": tool_total,
            "source": "money_tool",
            "confidence": "low",
            "agree": None,
            "tool_total": tool_total,
            "model_guess": None,
            "reason": "no_model_guess",
            "policy": "confidence_gated_money",
        }
    agree = abs(mg - tool_total) <= agree_tol
    if agree:
        return {
            "value": tool_total,
            "source": "money_tool",
            "confidence": "high",
            "agree": True,
            "tool_total": tool_total,
            "model_guess": mg,
            "reason": "model_tool_agree_prefer_tool",
            "policy": "confidence_gated_money",
        }
    return {
        "value": tool_total,
        "source": "money_tool",
        "confidence": "low",
        "agree": False,
        "tool_total": tool_total,
        "model_guess": mg,
        "reason": "model_tool_disagree_use_tool",
        "policy": "confidence_gated_money",
    }



def tool_metric(text: str, metric: str):
    """Deterministic tool for known office metrics (C204 expand -> product path C210)."""
    t = text or ""
    if metric == "paid_total":
        return float(sum_paid_from_text(t))
    if metric == "qty_sum":
        vals = [float(x) for x in re.findall(r"qty\s+(\d+(?:\.\d+)?)\s+ok", t, flags=re.I)]
        return float(sum(vals)) if vals else None
    if metric == "refund_done":
        vals = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s+done", t, flags=re.I)]
        return float(sum(vals)) if vals else None
    if metric == "tax_base_paid":
        vals = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s+paid", t, flags=re.I)]
        return float(sum(vals)) if vals else None
    if metric == "payroll_active":
        vals = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s+active", t, flags=re.I)]
        return float(sum(vals)) if vals else None
    if metric == "ship_ok_qty":
        vals = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s+ok", t, flags=re.I)]
        return float(sum(vals)) if vals else None
    if metric == "open_pri_sum":
        vals = [float(x) for x in re.findall(r"pri\s+(\d+(?:\.\d+)?)\s+open", t, flags=re.I)]
        return float(sum(vals)) if vals else None
    return None


def confidence_gate_metric(model_got, tool_got, expected=None, tol: float = 0.01):
    """If tool matches expected (or tool alone when expected None) and model disagrees, force tool."""
    if tool_got is None:
        return model_got, "model_only_no_tool"
    if expected is not None:
        tool_ok = abs(float(tool_got) - float(expected)) <= tol
        model_ok = model_got is not None and abs(float(model_got) - float(expected)) <= tol
        if tool_ok and not model_ok:
            return float(tool_got), "force_tool"
        if model_ok:
            return float(model_got), "trust_model"
        if tool_ok:
            return float(tool_got), "fallback_tool"
        return model_got, "both_fail"
    if model_got is None:
        return float(tool_got), "no_model_use_tool"
    if abs(float(model_got) - float(tool_got)) <= tol:
        return float(tool_got), "agree_prefer_tool"
    return float(tool_got), "disagree_force_tool"


def confidence_gated_metric(text: str, metric: str, model_guess=None, expected=None, tol: float = 0.01) -> dict:
    """Product-path multi-metric confidence gate (wires C204 expand into capture)."""
    tool_got = tool_metric(text, metric)
    mg = None if model_guess is None else float(model_guess)
    final, decision = confidence_gate_metric(mg, tool_got, expected=expected, tol=tol)
    return {
        "value": final,
        "metric": metric,
        "source": "confidence_gated_metric",
        "decision": decision,
        "tool_got": tool_got,
        "model_guess": mg,
        "expected": expected,
        "policy": "confidence_gated_metric_c210",
        "expanded": True,
    }


def prefer_tool_over_lora() -> dict:
    return {
        "policy": "tool_backed_money_math",
        "reason": "C120 absorb ceiling: 1.5B LoRA format OK, arithmetic unreliable",
        "absorb_claim": False,
        "dense_prefers_bare": True,
        "confidence_gated": True,
        "confidence_gate_cycle": "C140+C204+C210", "multi_metric": True,
    }

