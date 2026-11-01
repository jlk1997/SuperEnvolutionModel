"""Phase 3 entry: write the architecture comparison into a run directory."""

from __future__ import annotations

import traceback

from evo.arch.train import run_arch
from evo.runlog import Run


def _plot(summary: dict, path) -> bool:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return False
    labels = ["A after A", "A after B", "B after A", "B after B", "TTT 2nd half"]
    fig, ax = plt.subplots(figsize=(8, 4))
    names = [
        name
        for name in (
            "transformer",
            "selfmod",
            "selfmod_locked",
            "selfmod_replay",
            "selfmod_carry",
            "selfmod_recall",
            "selfmod_sparse",
        )
        if name in summary
    ]
    for name in names:
        block = summary[name]
        values = [
            block["after_a"]["nll_a_train"],
            block["after_b"]["nll_a_train"],
            block["after_a"]["nll_b_train"],
            block["after_b"]["nll_b_train"],
            block["ttt_second_half_nll"],
        ]
        ax.plot(labels, values, marker="o", label=name)
    ax.set_ylabel("NLL")
    ax.set_title("Sequential domains and test-time absorption")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return True


def run_phase3(cfg: dict) -> dict:
    run = Run(cfg["runs_root"], cfg.get("run_name", "phase3_arch"), cfg)
    try:
        summary = run_arch(cfg)
        run.save_json("summary.json", summary)
        _plot(summary, run.dir / "arch_nll.png")
        def _forget(name: str):
            block = summary.get(name)
            return None if block is None else block["forgetting_a"]

        run.log(
            {
                "event": "arch_done",
                "transformer_forgetting": _forget("transformer"),
                "selfmod_forgetting": _forget("selfmod"),
                "locked_forgetting": _forget("selfmod_locked"),
                "replay_forgetting": _forget("selfmod_replay"),
                "carry_forgetting": _forget("selfmod_carry"),
                "recall_forgetting": _forget("selfmod_recall"),
                "sparse_forgetting": _forget("selfmod_sparse"),
                "restream_gain": None
                if summary.get("selfmod_carry") is None or not summary["selfmod_carry"].get("restream")
                else summary["selfmod_carry"]["restream"]["gain"],
                "state_hold": None
                if summary.get("selfmod_recall") is None or not summary["selfmod_recall"].get("state_hold")
                else summary["selfmod_recall"]["state_hold"]["hold"],
                "params": summary["params"],
            }
        )
        print(f"[arch] wrote {run.dir}", flush=True)
        return summary
    except Exception:
        (run.dir / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise
