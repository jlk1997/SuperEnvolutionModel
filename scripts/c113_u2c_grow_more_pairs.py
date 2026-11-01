# -*- coding: utf-8 -*-
"""C113: Grow U2C SFT pairs (same weak office-table domain, more variety)."""
from __future__ import annotations
import csv, json, random, shutil, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
GATE = 0.6
BASE = ROOT / "runs" / "u2c_grow_c113"
DOC = ROOT / "docs" / "r50"
PAIRS_OUT = BASE / "sft_pairs.jsonl"
PRIOR = ROOT / "runs" / "u2c_grow_c103" / "sft_pairs.jsonl"

METRICS = [
    ("paid_total", "paid"),
    ("refund_done", "done"),
    ("qty_sum", "ok"),
    ("tax_base_paid", "paid"),
    ("ship_ok_qty", "ok"),
    ("payroll_active", "active"),
    ("open_pri_sum", "open"),
]

OTHER_STATUS = {
    "paid": ["open", "void", "refund"],
    "done": ["open", "pending"],
    "ok": ["hold", "bad"],
    "active": ["leave", "term"],
    "open": ["closed", "done"],
}


def ts():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def J(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def mk_rows(rng: random.Random, status_ok: str, n_rows: int = 4):
    others = OTHER_STATUS[status_ok]
    rows = []
    for i in range(n_rows):
        st = status_ok if i % 2 == 0 else rng.choice(others)
        if status_ok == "ok":
            amt = float(rng.randint(1, 120))
        elif status_ok == "open":
            amt = float(rng.randint(1, 12))
        else:
            amt = round(rng.uniform(1.0, 900.0), 2)
        rows.append((f"R{i+1}", amt, st))
    return rows


def expected(rows, status_ok: str) -> float:
    return round(sum(float(a) for _, a, st in rows if str(st) == status_ok), 2)


def pair_from(metric: str, status_ok: str, rows, sid: str):
    buf = ["id,amount,status"]
    for r in rows:
        buf.append(f"{r[0]},{r[1]},{r[2]}")
    csv_text = "\n".join(buf) + "\n"
    out = f"{metric}={expected(rows, status_ok):.2f}"
    return {
        "instruction": f"Compute {metric} from CSV",
        "input": csv_text,
        "output": out,
        "atom": f"office_table_u2c_{metric}",
        "sid": sid,
        "status_key": status_ok,
    }


def main():
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)
    rng = random.Random(113)
    pairs = []
    prior_n = 0
    if PRIOR.is_file():
        for line in PRIOR.read_text(encoding="utf-8").splitlines():
            if line.strip():
                o = json.loads(line)
                o["sid"] = o.get("sid") or f"prior_{prior_n}"
                pairs.append(o)
                prior_n += 1
    new_n = 0
    for metric, status_ok in METRICS:
        for k in range(10):
            sid = f"c113_{metric}_{k:02d}"
            rows = mk_rows(rng, status_ok, n_rows=rng.randint(3, 6))
            pairs.append(pair_from(metric, status_ok, rows, sid))
            sb = BASE / "sessions" / sid
            sb.mkdir(parents=True)
            p = sb / "input.csv"
            with p.open("w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh)
                w.writerow(["id", "amount", "status"])
                for r in rows:
                    w.writerow(list(r))
            exp = expected(rows, status_ok)
            (sb / "summary.csv").write_text(f"metric,value\n{metric},{exp:.2f}\n", encoding="utf-8")
            new_n += 1
    with PAIRS_OUT.open("w", encoding="utf-8") as fh:
        for pr in pairs:
            fh.write(json.dumps(pr, ensure_ascii=False) + "\n")
    heldout = []
    by_m = {m: [] for m, _ in METRICS}
    for i, pr in enumerate(pairs):
        atom = pr.get("atom") or ""
        for m, _ in METRICS:
            if atom.endswith(m) and str(pr.get("sid", "")).startswith("c113_"):
                by_m[m].append(i)
    for m, _ in METRICS:
        idxs = by_m[m]
        if idxs:
            heldout.append(idxs[-1])
    extras = []
    for m, _ in METRICS[:2]:
        idxs = by_m[m]
        if len(idxs) >= 2:
            extras.append(idxs[-2])
    heldout = sorted(set(heldout + extras))[:9]
    meta = {
        "cycle": "C113",
        "theme": "u2c_grow_more_pairs_same_domain",
        "gate": GATE,
        "timestamp": ts(),
        "gate2_3_untouched": True,
        "n_pairs_total": len(pairs),
        "n_prior": prior_n,
        "n_new": new_n,
        "pairs_path": str(PAIRS_OUT.relative_to(ROOT)).replace("\\", "/"),
        "heldout_idx": heldout,
        "heldout_n": len(heldout),
        "metrics": [m for m, _ in METRICS],
        "pass": len(pairs) >= 60 and len(heldout) >= 7,
        "claim": False,
        "note": "Grown pairs for C114 absorb push. No training here. No Gate2/3.",
    }
    J(DOC / "C113_U2C_GROW_PAIRS.json", meta)
    J(BASE / "meta.json", meta)
    print(json.dumps({"cycle": "C113", "n_pairs": len(pairs), "heldout_n": len(heldout), "pass": meta["pass"]}, ensure_ascii=False))
    return 0 if meta["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
