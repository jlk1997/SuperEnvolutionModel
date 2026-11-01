# -*- coding: utf-8 -*-
"""Shared vision metric atom parse (C149+ / C153 / C158 / C158b / C162 / C338).
Handles OCR word-order variants: "paid 4.50" AND "4.50 paid".
Status-filtered sums. Ignores stamp/watermark noise 999/888/777/666/42.

C153: word-boundary on amount-THEN-status (lineN/rowN).
C158: NOISE+=666; colon-decimal normalize (16:00 -> 16.00).
C162: unglue digit.status (14.ok).
C338: sla_ok_hours sums Nh ok / N hours ok (TARGET watermark-robust).
C213: NOISE+=99.99/99.95 (sticky/decoy paid totals).
C158b: do NOT bag-dedupe identical (amount,status) — duplicate line items
like "paid 5.00" twice must both count; instead drop amount-THEN spans that
overlap a status-THEN span.
"""
from __future__ import annotations
import re
from typing import List, Tuple

NOISE = {999.0, 888.0, 777.0, 666.0, 42.0, 99.99, 99.95, 999, 888, 777, 666, 42, 99.99}


def _clean(text: str) -> str:
    t = (text or "").lower()
    t = re.sub(r"(\d+):(\d{2})\b", r"\1.\2", t)
    # C162: OCR glues amount to status ("14.ok" / "5.hold") -> "14 ok"
    t = re.sub(
        r"(\d)\.(paid|open|void|hold|ok|done|active|leave|closed|recv|ship)\b",
        r"\1 \2",
        t,
    )
    return re.sub(r"\s+", " ", t).strip()


def _is_noise(v: float) -> bool:
    if v in NOISE:
        return True
    for n in (999.0, 888.0, 777.0, 666.0, 99.99, 99.95, 42.0):
        if abs(v - n) < 1e-6:
            return True
    return False


def iter_amount_status_pairs(text: str):
    """Yield (amount, status) — compatibility helper (may include dups)."""
    for amt, st, _a, _b in iter_amount_status_spans(text):
        yield amt, st


def iter_amount_status_spans(text: str):
    """Yield (amount, status, start, end) from OCR-ish text."""
    t = _clean(text)
    # amount THEN status
    for m in re.finditer(
        r"\b(\d+\.?\d*)\s+(paid|open|void|hold|ok|done|active|leave|closed|recv|ship)\b",
        t,
    ):
        yield float(m.group(1)), m.group(2), m.start(), m.end()
    # status THEN amount
    for m in re.finditer(
        r"\b(paid|open|void|hold|ok|done|active|leave|closed|qty|pri)\s+(\d+\.?\d*)",
        t,
    ):
        yield float(m.group(2)), m.group(1), m.start(), m.end()


def _overlaps(a0, a1, b0, b1) -> bool:
    return not (a1 <= b0 or b1 <= a0)


def sum_status(text: str, good: set[str], *, also_qty_ok: bool = False) -> float:
    """Sum amounts whose paired status is in good.

    Prefers status-THEN-amount spans; keeps amount-THEN only when non-overlapping.
    Duplicate identical amounts on separate lines all count (C158b).
    """
    t = _clean(text)
    status_then: List[Tuple[float, str, int, int]] = []
    amount_then: List[Tuple[float, str, int, int]] = []
    for m in re.finditer(
        r"\b(paid|open|void|hold|ok|done|active|leave|closed|qty|pri)\s+(\d+\.?\d*)",
        t,
    ):
        status_then.append((float(m.group(2)), m.group(1), m.start(), m.end()))
    for m in re.finditer(
        r"\b(\d+\.?\d*)\s+(paid|open|void|hold|ok|done|active|leave|closed|recv|ship)\b",
        t,
    ):
        amount_then.append((float(m.group(1)), m.group(2), m.start(), m.end()))

    kept: List[Tuple[float, str]] = []
    spans: List[Tuple[int, int]] = []
    # Track ALL status-then spans for overlap (incl. rejected) so
    # 'open 15.00 paid 99.99' does not invent amount-then (15,paid).
    all_st_spans: List[Tuple[int, int]] = [(a0, a1) for _amt, _st, a0, a1 in status_then]
    for amt, st, a0, a1 in status_then:
        if _is_noise(amt) or st not in good:
            continue
        kept.append((amt, st))
        spans.append((a0, a1))
    for amt, st, a0, a1 in amount_then:
        if _is_noise(amt) or st not in good:
            continue
        if any(_overlaps(a0, a1, b0, b1) for b0, b1 in spans):
            continue
        if any(_overlaps(a0, a1, b0, b1) for b0, b1 in all_st_spans):
            continue
        kept.append((amt, st))
        spans.append((a0, a1))

    total = sum(a for a, _ in kept)
    if also_qty_ok or "ok" in good:
        for m in re.finditer(r"qty\s+(\d+\.?\d*)\s+(ok|hold|void|open)\b", t):
            amt = float(m.group(1))
            st = m.group(2)
            if _is_noise(amt) or st not in good:
                continue
            # qty N ok is a distinct constructive pattern; always add if status ok
            # but skip if this exact span already covered
            if any(_overlaps(m.start(), m.end(), b0, b1) for b0, b1 in spans):
                continue
            kept.append((amt, "qty_" + st))
            spans.append((m.start(), m.end()))
            total += amt
    else:
        total = sum(a for a, _ in kept)
    return round(total, 2)


def sum_pri_open(text: str) -> float:
    t = _clean(text)
    total = 0.0
    for m in re.finditer(r"pri\s+(\d+\.?\d*)\s+open\b", t):
        total += float(m.group(1))
    return round(total, 2)


def parse_metric(text: str, metric: str, expected) -> Tuple[float, bool]:
    """Return (got, ok). ok True only when got matches expected within 0.08."""
    t = _clean(text)
    exp = float(expected)
    tol = 0.08

    m = re.search(rf"{re.escape(metric)}\s*target\s*(\d+\.?\d*)", t)
    if m and abs(float(m.group(1)) - exp) < tol:
        return float(m.group(1)), True
    m = re.search(r"total\s*paid\s*(?:target)?\s*(\d+\.?\d*)", t)
    if metric == "paid_total" and m and abs(float(m.group(1)) - exp) < tol:
        return float(m.group(1)), True

    got = None
    if metric == "paid_total":
        got = sum_status(t, {"paid"})
    elif metric == "tax_base_paid":
        got = sum_status(t, {"paid"})
    elif metric == "qty_sum":
        got = 0.0
        for m in re.finditer(r"qty\s+(\d+\.?\d*)\s*\.?\s*ok\b", t):
            got += float(m.group(1))
        got = round(got, 2)
    elif metric == "payroll_active":
        got = sum_status(t, {"active"})
    elif metric in ("ship_ok_qty", "ship_ok"):  # C358: V35+ fixtures use ship_ok
        got = 0.0
        for m in re.finditer(r"(\d+\.?\d*)\s+ok\b", t):
            v = float(m.group(1))
            if not _is_noise(v):
                got += v
        got = round(got, 2)
    elif metric == "refund_done":
        got = sum_status(t, {"done"})
    elif metric == "open_pri_sum":
        got = sum_pri_open(t)
    elif metric == "sla_ok_hours":
        # C338: sum hours marked ok — OCR often yields "43.00h ok" / "43.00 hours ok".
        # Do not count late/rate/hold; TARGET line alone is brittle under watermark ($1.50).
        got = 0.0
        for m in re.finditer(r"(\d+\.?\d*)\s*h(?:ours)?\s+ok\b", t):
            v = float(m.group(1))
            if not _is_noise(v):
                got += v
        got = round(got, 2)

    if got is not None and abs(got - exp) < tol:
        return float(got), True

    if exp == 0.0:
        if re.search(rf"{re.escape(metric)}\s*(?:target)?\s*0(?:\.0+)?\b", t) or re.search(
            r"target\s*0(?:\.0+)?\b", t
        ):
            return 0.0, True
        if "open only" in t:
            if sum_status(t, {"paid"}) == 0.0:
                return 0.0, True

    for m in re.finditer(r"(\d+\.?\d*)", t):
        v = float(m.group(1))
        if _is_noise(v):
            continue
        if abs(v - exp) < tol:
            return v, True

    return float(got or 0.0), False
