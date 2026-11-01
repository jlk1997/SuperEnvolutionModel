"""Command line for the local self-evolution experiments."""

from __future__ import annotations

import argparse
import math
import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault("HF_HOME", str(Path(__file__).resolve().parents[1] / ".cache" / "huggingface"))
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


def _cfg(args):
    from evo.util import load_config

    cfg = load_config(args.config)
    if getattr(args, "model", None):
        cfg["model_name"] = args.model
    return cfg


def cmd_smoke(args) -> None:
    import torch

    from evo.inner_loop import adapt_scratch
    from evo.model import build_model
    from evo.util import set_seed

    cfg = _cfg(args)
    set_seed(cfg["seed"])
    if not torch.cuda.is_available():
        raise SystemExit("CUDA is not available")
    evo = build_model(cfg)
    evo.reset_scratch()
    loss, n_params = adapt_scratch(
        evo,
        "The fictitious alloy brinium melts at 451 degrees.",
        steps=1,
        lr=cfg["inner_lr"],
        max_len=cfg["max_seq_len"],
    )
    if not math.isfinite(loss):
        raise SystemExit(f"smoke failed: non-finite loss {loss}")
    print(
        f"SMOKE_OK loss={loss:.4f} trainable={n_params} vram_mb={evo.vram_mb():.0f} "
        f"4bit={evo.is_4bit} gpu={torch.cuda.get_device_name(0)}",
        flush=True,
    )


def cmd_try(args) -> None:
    from evo.experience import DEMO_FACT, DEMO_QUESTIONS, run_experience

    if bool(args.fact) != bool(args.question):
        raise SystemExit("Pass both --fact and --question, or neither to use the built-in fact.")
    cfg = _cfg(args)
    if args.fact:
        questions = [{"question": args.question, "answers": [args.answer] if args.answer else []}]
        fact = args.fact
    else:
        questions = DEMO_QUESTIONS
        fact = DEMO_FACT
    run_experience(cfg, fact, questions, args.steps, args.lr)


def cmd_exam(args) -> None:
    """Unit gate, then the multi-day exam the phase is scored on."""
    cmd_unit(args)
    print("EXAM_UNIT_OK", flush=True)
    if args.check:
        print("EXAM_CHECK_OK config=" + str(args.config), flush=True)
        return
    from evo.phase4 import run_phase4

    run_phase4(_cfg(args))


def cmd_unit(_args) -> None:
    root = Path(__file__).resolve().parents[1]
    suite = unittest.defaultTestLoader.discover(
        str(root / "evo" / "tests"),
        pattern="test_*.py",
        top_level_dir=str(root),
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Local self-evolving model experiments")
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add(name: str, func):
        command = sub.add_parser(name)
        command.add_argument("--config", default=None)
        command.add_argument("--model", default=None)
        command.set_defaults(func=func)
        return command

    smoke = add("smoke", cmd_smoke)
    smoke.set_defaults(config="configs/smoke.yaml")
    add("baselines", lambda args: _run_phase1("baselines", args))
    add("continual", lambda args: _run_phase1("continual", args))
    add("antiforget", lambda args: _run_phase1("antiforget", args))
    add("selfplay", lambda args: __import__("evo.phase2", fromlist=["run_selfplay"]).run_selfplay(_cfg(args)))
    add("arch", lambda args: __import__("evo.phase3", fromlist=["run_phase3"]).run_phase3(_cfg(args)))
    add("live", lambda args: __import__("evo.phase4", fromlist=["run_phase4"]).run_phase4(_cfg(args)))
    add("evolve", lambda args: __import__("evo.evolve", fromlist=["run_evolve"]).run_evolve(_cfg(args)))
    add("stream", lambda args: __import__("evo.live.stream", fromlist=["run_stream"]).run_stream(_cfg(args)))
    add("baseline", lambda args: __import__("evo.live.baseline", fromlist=["write_baseline"]).write_baseline())
    add("probe-base", lambda args: __import__("evo.live.probe_qwen", fromlist=["run_probe"]).run_probe([args.model] if args.model else None))
    add("service", lambda args: __import__("evo.live.service", fromlist=["write_pair"]).write_pair())
    add("office", cmd_office)
    add("rhythm", lambda args: __import__("evo.office.stream", fromlist=["run_office"]).run_office(_rhythm_cfg(args)))
    add("heldout", cmd_heldout)
    add("pilot", lambda args: print(__import__("evo.office.pilot", fromlist=["demo"]).demo(), flush=True))
    shadow = sub.add_parser("shadow-smoke", help="Real-folder shadow mode smoke (CPU; Gate3 judge branch)")
    shadow.add_argument("--root", default=None, help="Designated folder (default: runs/shadow_workspace)")
    shadow.set_defaults(func=cmd_shadow_smoke)
    auto_sm = sub.add_parser("auto-smoke", help="Assist→auto promote smoke (CPU; sandbox only)")
    auto_sm.add_argument("--root", default=None)
    auto_sm.add_argument("--min-n", type=int, default=1)
    auto_sm.set_defaults(func=cmd_auto_smoke)
    crystal_ul = sub.add_parser(
        "crystal-use-log",
        help="C2/C3: grade office use-log pairs and crystallize family atoms (gate 0.6)",
    )
    crystal_ul.add_argument("--use-log", default="runs/use_log/office_use_log_dual_f3i_s0")
    crystal_ul.add_argument("--arm", default="dual")
    crystal_ul.add_argument("--family", action="append", default=None)
    crystal_ul.add_argument("--min-n", type=int, default=2)
    crystal_ul.add_argument("--criterion", type=float, default=0.6)
    
    crystal_ul.set_defaults(func=cmd_crystal_use_log)
    crystal_d = sub.add_parser(
        "crystal-dissolve",
        help="C4/C5 GPU: SFT from use-log + bare/scaffold dissolution (gate 0.6)",
    )
    crystal_d.add_argument("--use-log", default="runs/use_log/office_use_log_dual_f3i_s0")
    crystal_d.add_argument("--family", default="table")
    crystal_d.add_argument("--epochs", type=int, default=2)
    crystal_d.add_argument("--heldout-n", type=int, default=4)
    crystal_d.set_defaults(func=cmd_crystal_dissolve)

    add("fleet", lambda args: print(__import__("evo.live.fleet", fromlist=["run_drill"]).run_drill(), flush=True))
    studio = add("studio", cmd_studio)
    studio.add_argument("--host", default="127.0.0.1")
    studio.add_argument("--port", type=int, default=8765)
    add("bench-base", lambda args: print(__import__("evo.live.bench", fromlist=["run_bench"]).run_bench(args.model), flush=True))
    plast = sub.add_parser("plast", help="Plasticity evolution: reference lives, then the optional model gate")
    plast.add_argument("--config", default="configs/evoplast_all.yaml")
    plast.add_argument(
        "--stage",
        default=None,
        choices=("m0", "m1", "es", "baldwin", "transfer", "all", "life", "evolve", "grow", "stream", "census"),
    )
    plast.add_argument("--model", default=None)
    plast.set_defaults(func=cmd_plast)
    status = sub.add_parser("status", help="Print the scoreboard of the newest run, even if it is still going")
    status.add_argument("--run", default=None, help="metrics.jsonl or a run directory")
    status.set_defaults(func=cmd_status)
    unit = sub.add_parser("unit")
    unit.set_defaults(func=cmd_unit)
    exam = sub.add_parser("exam", help="Close this phase: unit tests, then the scored live run")
    exam.add_argument("--config", default="configs/phase4_exam.yaml")
    exam.add_argument("--model", default=None)
    exam.add_argument("--check", action="store_true", help="Unit tests only, no GPU run")
    exam.set_defaults(func=cmd_exam)
    trial = sub.add_parser("try", help="One self-edit and one executor check on the 0.5B model")
    trial.add_argument("--config", default="configs/smoke.yaml")
    trial.add_argument("--model", default=None)
    trial.add_argument("--fact", default=None)
    trial.add_argument("--question", default=None)
    trial.add_argument("--answer", default=None)
    trial.add_argument("--steps", type=int, default=40)
    trial.add_argument("--lr", type=float, default=5e-4)
    trial.set_defaults(func=cmd_try)

    # Defaults so a bare command still has a config path when the user passed none.
    args = parser.parse_args(argv)
    if args.cmd == "baselines" and not args.config:
        args.config = "configs/phase1_baselines.yaml"
    elif args.cmd == "continual" and not args.config:
        args.config = "configs/phase1_continual.yaml"
    elif args.cmd == "antiforget" and not args.config:
        args.config = "configs/phase1_antiforget.yaml"
    elif args.cmd == "selfplay" and not args.config:
        args.config = "configs/phase2_selfplay.yaml"
    elif args.cmd == "arch" and not args.config:
        args.config = "configs/phase3_arch.yaml"
    elif args.cmd == "live" and not args.config:
        args.config = "configs/phase4_smoke.yaml"
    elif args.cmd == "evolve" and not args.config:
        args.config = "configs/evolve_all.yaml"
    elif args.cmd == "stream" and not args.config:
        args.config = "configs/stream_smoke.yaml"
    elif args.cmd == "smoke" and not args.config:
        args.config = "configs/smoke.yaml"
    elif args.cmd == "office" and not args.config:
        args.config = "configs/office_smoke.yaml"
    elif args.cmd == "rhythm" and not args.config:
        args.config = "configs/office_smoke.yaml"
    elif args.cmd == "heldout" and not args.config:
        args.config = "configs/office_heldout.yaml"
    args.func(args)


def _with_model(cfg: dict):
    from evo.model import build_model, release

    evo = None
    if cfg.get("actor") == "model":
        evo = build_model(cfg)
    return evo, release


def _ready_model(cfg: dict) -> None:
    """Resolve and require local weights via the model registry. Fail fast; no silent fallback."""
    from evo.registry import require_ready

    require_ready(cfg)






def cmd_crystal_dissolve(args) -> None:
    import json
    from evo.office.dissolve_uselog import run_dissolve

    report = run_dissolve(
        args.use_log,
        args.family,
        epochs=int(args.epochs),
        heldout_n=int(args.heldout_n),
    )
    print(json.dumps(report, indent=2, ensure_ascii=True)[:4000], flush=True)


def cmd_crystal_use_log(args) -> None:
    """CPU-side C2/C3 from use_log. Does not lower criterion below 0.6."""
    import json

    from evo.office.from_use_log import run_pipeline

    criterion = float(args.criterion)
    if criterion < 0.6:
        raise SystemExit("criterion may not be lowered below 0.6")
    report = run_pipeline(
        args.use_log,
        families=args.family,
        arm=args.arm,
        criterion=criterion,
        min_n=int(args.min_n),
    )
    print(json.dumps(report, indent=2, ensure_ascii=True)[:4000], flush=True)




def cmd_auto_smoke(args) -> None:
    import json
    from pathlib import Path

    from evo.office.auto_smoke import run_auto_smoke

    root = Path(args.root) if getattr(args, "root", None) else None
    evidence = run_auto_smoke(root=root, write_evidence=True, min_n=int(getattr(args, "min_n", 1) or 1))
    print(json.dumps(evidence, ensure_ascii=True), flush=True)
    if not evidence.get("pass"):
        raise SystemExit(1)


def cmd_shadow_smoke(args) -> None:
    import json
    from pathlib import Path

    from evo.office.shadow_smoke import run_shadow_smoke

    root = Path(args.root) if getattr(args, "root", None) else None
    evidence = run_shadow_smoke(root=root, write_evidence=True)
    print(json.dumps(evidence, ensure_ascii=True), flush=True)
    if not evidence.get("pass"):
        raise SystemExit(1)


def cmd_office(args) -> None:
    import json

    cfg = _cfg(args)
    if cfg.get("actor") == "model":
        _ready_model(cfg)
    evo, release = _with_model(cfg)
    try:
        if cfg.get("calibrate") and evo is not None:
            from evo.office.calibrate import calibrate

            choice = calibrate(evo, cfg)
            cfg["difficulty"] = int(choice["difficulty"])
            print(json.dumps(choice), flush=True)
        result = __import__("evo.office.stream", fromlist=["run_office"]).run_office(cfg, evo)
    finally:
        if evo is not None:
            release(evo)
    print(json.dumps(result["judge"], ensure_ascii=True)[:2000], flush=True)


def cmd_studio(args) -> None:
    from evo.studio.app import serve

    serve(args.host, int(args.port))


def cmd_heldout(args) -> None:
    import json

    cfg = _cfg(args)
    if cfg.get("actor") == "model":
        _ready_model(cfg)
    evo, release = _with_model(cfg)
    try:
        result = __import__("evo.office.heldout_run", fromlist=["run_heldout"]).run_heldout(cfg, evo)
    finally:
        if evo is not None:
            release(evo)
    print(json.dumps(result.get("judge"), ensure_ascii=True)[:2000], flush=True)


def _rhythm_cfg(args):
    cfg = _cfg(args)
    cfg["arms"] = ["dual"]
    cfg["actor"] = cfg.get("actor") or "reference"
    cfg["write_gate"] = False
    return cfg


def cmd_plast(args) -> None:
    import json

    cfg = _cfg(args)
    if args.stage:
        cfg["stage"] = args.stage
    if cfg.get("actor") == "model":
        from evo.registry import require_ready

        require_ready(cfg)
    report = __import__("evo.evolution.runner", fromlist=["run_plast"]).run_plast(cfg)
    m0 = report.get("m0") or {}
    brief = {
        "stage": report.get("stage"),
        "m0_reference": m0.get("passed"),
        "m0_lm": m0.get("lm_passed"),
        "m0": m0.get("passed"),
        "m1": (report.get("m1") or {}).get("passed"),
        "es": (report.get("es") or {}).get("passed"),
        "transfer": (report.get("transfer") or {}).get("heritability"),
    }
    if m0.get("model") is not None:
        model = m0.get("model") or {}
        brief["m0_model_status"] = model.get("status")
        brief["m0_model_passed"] = model.get("passed")
        if model.get("recommendation"):
            brief["m0_lm_recommendation"] = model.get("recommendation")
    for key in ("life", "grow", "evolve", "stream", "census"):
        if key in report:
            block = report[key] or {}
            brief[key] = block.get("passed")
            if key == "census":
                brief["census_status"] = block.get("status")
                brief["census_n_passed"] = block.get("n_passed")
                brief["census_n_cells"] = block.get("n_cells")
    print(json.dumps(brief, ensure_ascii=True), flush=True)


def cmd_status(args) -> None:
    from evo.util import repo_path
    from evo.world.status import latest_metrics, read_status

    target = getattr(args, "run", None)
    if target:
        path = Path(target)
        if path.is_dir():
            path = path / "metrics.jsonl"
    else:
        path = latest_metrics(repo_path("runs"))
    if path is None or not path.is_file():
        raise SystemExit("No metrics.jsonl under runs/ yet.")
    print(read_status(path), flush=True)


def _run_phase1(which: str, args) -> None:
    from evo.phase1 import run_antiforget, run_baselines, run_continual

    cfg = _cfg(args)
    if which == "baselines":
        run_baselines(cfg)
    elif which == "continual":
        run_continual(cfg)
    else:
        run_antiforget(cfg)


if __name__ == "__main__":
    main(sys.argv[1:])
