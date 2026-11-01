"""External exam scaffold (CPU). Names the Stage-2 benches; local wire when data present.

ROADMAP: after real-folder pilot, external exams and fleet share.
fleet.py is frozen — this module stubs harness contracts and may wire benches
to local on-disk fixtures (no download, no VL, no sealed-pack reopen).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from evo.util import repo_path

# Preregistered names only — adapters wire when a local fixture exists.
BENCHES = (
    {"id": "cl_bench", "title": "CL-Bench", "kind": "continual", "status": "stub"},
    {"id": "serve_learn", "title": "ServeLearnBench", "kind": "service", "status": "stub"},
    {"id": "evo_arena", "title": "EvoArena", "kind": "arena", "status": "stub"},
    {"id": "path_bench", "title": "PATH-Bench", "kind": "path", "status": "stub"},
)

# Local-only fixtures (not upstream leaderboards).
LOCAL_CANDIDATES: dict[str, tuple[str, ...]] = {
    "cl_bench": (
        "data/external_fixtures/cl_bench_local.json",
        "data/heldout_math.json",
    ),
    "serve_learn": (
        "data/external_fixtures/serve_learn_local.json",
    ),
    "evo_arena": (
        "data/external_fixtures/evo_arena_local.json",
    ),
    "path_bench": (
        "data/external_fixtures/path_bench_local.json",
    ),
}

KIND_LABEL = {
    "cl_bench": "continual_toy",
    "serve_learn": "service_toy",
    "evo_arena": "arena_toy",
    "path_bench": "path_toy",
}


def discover_local(bench_id: str) -> Path | None:
    """Return first existing local toy path for bench_id; no network."""
    for rel in LOCAL_CANDIDATES.get(bench_id, ()):
        path = repo_path(rel)
        if path.is_file():
            return path
    return None


def discover_cl_bench_local() -> Path | None:
    """Compat alias used by cl_bench score script."""
    return discover_local("cl_bench")


def list_benches() -> list[dict[str, str]]:
    rows = [dict(row) for row in BENCHES]
    for row in rows:
        found = discover_local(row["id"])
        if found is not None:
            row["status"] = "wired_local_fixture"
            row["local_path"] = str(found)
    return rows


def adapter_contract(bench_id: str) -> dict[str, Any]:
    """What a future adapter must expose. No network."""
    known = {row["id"] for row in BENCHES}
    if bench_id not in known:
        return {"ok": False, "error": "unknown_bench", "bench_id": bench_id}
    found = discover_local(bench_id)
    out: dict[str, Any] = {
        "ok": True,
        "bench_id": bench_id,
        "required_methods": ["load_local", "iter_items", "score"],
        "rules": [
            "local files only — no download in-process",
            "Gate 0.6 competence unchanged",
            "never reopen burned sealed office packs",
            "no VL / no Epoch D claim",
            "wired_local_fixture is NOT an upstream leaderboard pass",
        ],
        "wired": found is not None,
    }
    if found is not None:
        out["local_path"] = str(found)
    return out


class LocalQaAdapter:
    """Generic local Q/A toy adapter. upstream_claim always False."""

    def __init__(self, bench_id: str, path: Path | None = None) -> None:
        self.bench_id = bench_id
        self.path = path or discover_local(bench_id)
        self._items: list[dict[str, Any]] = []

    def load_local(self) -> dict[str, Any]:
        if self.path is None or not self.path.is_file():
            return {"ok": False, "error": "missing_local_fixture", "bench_id": self.bench_id}
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(raw, list) or not raw:
            return {"ok": False, "error": "empty_or_bad_fixture", "path": str(self.path)}
        items: list[dict[str, Any]] = []
        for i, row in enumerate(raw):
            if not isinstance(row, dict):
                continue
            q = row.get("question") or row.get("prompt") or row.get("task") or ""
            a = row.get("answer")
            if a is None and "tests" in row:
                a = "code"
            items.append(
                {
                    "id": str(row.get("id") or f"item_{i}"),
                    "task": str(q),
                    "gold": str(a) if a is not None else "",
                    "phase": "train" if i < max(1, len(raw) // 2) else "eval",
                }
            )
        self._items = items
        return {
            "ok": True,
            "bench_id": self.bench_id,
            "path": str(self.path),
            "n": len(items),
            "n_train": sum(1 for x in items if x["phase"] == "train"),
            "n_eval": sum(1 for x in items if x["phase"] == "eval"),
            "upstream_claim": False,
            "kind": KIND_LABEL.get(self.bench_id, "local_toy"),
        }

    def iter_items(self, phase: str | None = None) -> Iterator[dict[str, Any]]:
        if not self._items:
            self.load_local()
        for row in self._items:
            if phase is None or row.get("phase") == phase:
                yield dict(row)

    def score(self, predictions: dict[str, str]) -> dict[str, Any]:
        if not self._items:
            loaded = self.load_local()
            if not loaded.get("ok"):
                return {"ok": False, "error": "not_loaded", "bench_id": self.bench_id}
        eval_items = [x for x in self._items if x.get("phase") == "eval"]
        if not eval_items:
            eval_items = list(self._items)
        hits = 0
        for row in eval_items:
            pred = str(predictions.get(row["id"], "")).strip()
            gold = str(row.get("gold", "")).strip()
            if pred and gold and pred == gold:
                hits += 1
        n = len(eval_items)
        rate = (hits / n) if n else 0.0
        return {
            "ok": True,
            "bench_id": self.bench_id,
            "n": n,
            "hits": hits,
            "rate": rate,
            "gate": "0.6",
            "pass_gate": rate >= 0.6,
            "upstream_claim": False,
            "notes": f"local {KIND_LABEL.get(self.bench_id, 'toy')} score only; not upstream {self.bench_id}",
        }


class ClBenchLocalAdapter(LocalQaAdapter):
    """Continual toy over local Q/A JSON. Not upstream CL-Bench."""

    def __init__(self, path: Path | None = None) -> None:
        super().__init__("cl_bench", path=path)


class ServeLearnLocalAdapter(LocalQaAdapter):
    """Service/reconcile toy. Not upstream ServeLearnBench."""

    def __init__(self, path: Path | None = None) -> None:
        super().__init__("serve_learn", path=path)


class EvoArenaLocalAdapter(LocalQaAdapter):
    """Arena preference toy. Not upstream EvoArena."""

    def __init__(self, path: Path | None = None) -> None:
        super().__init__("evo_arena", path=path)


class PathBenchLocalAdapter(LocalQaAdapter):
    """Multi-hop path toy. Not upstream PATH-Bench."""

    def __init__(self, path: Path | None = None) -> None:
        super().__init__("path_bench", path=path)


ADAPTERS = {
    "cl_bench": ClBenchLocalAdapter,
    "serve_learn": ServeLearnLocalAdapter,
    "evo_arena": EvoArenaLocalAdapter,
    "path_bench": PathBenchLocalAdapter,
}


def _smoke_one(bench_id: str) -> dict[str, Any]:
    cls = ADAPTERS[bench_id]
    adapter = cls()
    loaded = adapter.load_local()
    if not loaded.get("ok"):
        return {"load": loaded, "score": {"ok": False, "error": "not_loaded"}, "wired": False}
    preds = {row["id"]: row["gold"] for row in adapter.iter_items()}
    scored = adapter.score(preds)
    return {"load": loaded, "score": scored, "wired": True}


def run_scaffold_smoke(write_evidence: bool = True) -> dict[str, Any]:
    benches = list_benches()
    contracts = [adapter_contract(row["id"]) for row in benches]
    per_bench: dict[str, Any] = {}
    for bid in ADAPTERS:
        per_bench[bid] = _smoke_one(bid)
    wired_ids = [c["bench_id"] for c in contracts if c.get("wired")]
    # Every wired bench must load+score OK; stubs (no fixture) are allowed but
    # this paper expects all four local fixtures present.
    wired_ok = all(
        per_bench[bid]["load"].get("ok") and per_bench[bid]["score"].get("ok")
        for bid in wired_ids
    )
    passed = (
        len(benches) == 4
        and all(c.get("ok") for c in contracts)
        and set(wired_ids) == set(ADAPTERS)
        and wired_ok
    )
    cl = per_bench["cl_bench"]
    evidence: dict[str, Any] = {
        "kind": "external_scaffold_smoke",
        "gate": "0.6",
        "gpu": False,
        "vl": False,
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "benches": benches,
        "contracts_ok": all(c.get("ok") for c in contracts),
        "wired_ids": wired_ids,
        "per_bench": {
            bid: {
                "wired": per_bench[bid]["wired"],
                "load": per_bench[bid]["load"],
                "score_smoke": per_bench[bid]["score"],
            }
            for bid in ADAPTERS
        },
        "cl_bench_local": cl["load"],
        "cl_bench_score_smoke": cl["score"],
        "none_wired": len(wired_ids) == 0,
        "pass": passed,
        "notes": (
            "CPU scaffold; all four benches wired to local toys under "
            "data/external_fixtures (cl_bench may also use heldout_math). "
            "Not an upstream external exam pass. Fleet module remains frozen."
        ),
        "queue_after_mid_n": [
            "DONE: Gate2 mid-n dual power observational (GPU)",
            "DONE: wire cl_bench / serve_learn / evo_arena / path_bench local toys",
            "fleet drill already exists (frozen) — do not extend",
            "D still blocked without VL weights",
        ],
        "mid_n_done": True,
        "mid_n_evidence": "docs/GATE2_MID_N_OBSERVATIONAL_2026-10-18.json",
        "upstream_claim": False,
    }
    if write_evidence:
        path = repo_path("docs") / "EXTERNAL_SCAFFOLD_2026-10-18.json"
        path.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        evidence["docs_path"] = str(path)
        # Per-bench wire docs
        for bid in ("serve_learn", "evo_arena", "path_bench", "cl_bench"):
            pb = per_bench[bid]
            title = next(r["title"] for r in BENCHES if r["id"] == bid)
            wire_doc = {
                "kind": f"{bid}_local_wire",
                "gate": "0.6",
                "timestamp": evidence["timestamp"],
                "bench_id": bid,
                "local_path": pb["load"].get("path"),
                "load": pb["load"],
                "score_smoke": pb["score"],
                "upstream_claim": False,
                "pass": bool(pb["load"].get("ok") and pb["score"].get("ok")),
                "notes": f"Wired {bid} adapter to local toy. Not upstream {title}.",
            }
            fname = {
                "cl_bench": "CL_BENCH_LOCAL_WIRE_2026-10-18.json",
                "serve_learn": "SERVE_LEARN_LOCAL_WIRE_2026-10-18.json",
                "evo_arena": "EVO_ARENA_LOCAL_WIRE_2026-10-18.json",
                "path_bench": "PATH_BENCH_LOCAL_WIRE_2026-10-18.json",
            }[bid]
            wpath = repo_path("docs") / fname
            wpath.write_text(json.dumps(wire_doc, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
            evidence.setdefault("wire_docs", {})[bid] = str(wpath)
    return evidence


def main() -> None:
    evidence = run_scaffold_smoke()
    print(json.dumps(evidence, ensure_ascii=True), flush=True)
    if not evidence.get("pass"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
