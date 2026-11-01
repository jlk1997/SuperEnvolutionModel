"""Local model registry: resolve paths, check real weights, fail fast.

Primary checkpoint is Qwen2.5-1.5B-Instruct under models/. There is no silent
fallback to incomplete Qwen3.5-0.8B (or any other) weights.
"""

from __future__ import annotations

from pathlib import Path

from evo.util import repo_path

PRIMARY = "Qwen2.5-1.5B-Instruct"
# Optional listing only (studio / manual 2B experiments). Never used as silent fallback.
OPTIONAL_2B = "Qwen3.5-2B"


def resolve(name: str | Path | None = None) -> Path:
    """Map a config value, alias, or HF-style id to a local models/ path when possible."""
    if name is None or not str(name).strip():
        return repo_path("models") / PRIMARY
    text = str(name).strip()
    path = Path(text)
    if path.is_absolute():
        return path
    normalized = text.replace("\\", "/")
    if normalized.startswith("models/"):
        return repo_path(normalized)
    # HF hub id like Qwen/Qwen2.5-1.5B-Instruct -> models/<basename> if present
    basename = Path(normalized).name
    under_models = repo_path("models") / basename
    if under_models.is_dir():
        return under_models
    candidate = repo_path(text)
    if candidate.is_dir():
        return candidate
    return under_models


def is_ready(name: str | Path | None = None) -> bool:
    """True when config.json exists and at least one non-empty *.safetensors weight is present.

    Index-only trees (e.g. model.safetensors.index.json without shard files) are not ready.
    """
    root = resolve(name)
    if not root.is_dir() or not (root / "config.json").is_file():
        return False
    for weight in root.glob("*.safetensors"):
        if not weight.is_file():
            continue
        # Real weight shards / single-file dumps; never treat a missing/empty file as ready.
        if weight.stat().st_size > 0:
            return True
    return False


def require_ready(cfg: dict) -> Path:
    """Resolve cfg['model_name'], rewrite it to the local path, or raise.

    Never rewrites to another model family. Clears legacy model_fallback flags.
    """
    raw = cfg.get("model_name")
    root = resolve(raw if raw else None)
    if not is_ready(root):
        primary = repo_path("models") / PRIMARY
        raise RuntimeError(
            f"Model weights not ready at {root}. "
            f"Need config.json and at least one non-empty *.safetensors file "
            f"(index.json alone is not enough). "
            f"Primary expected at {primary} (ready={is_ready(primary)}). "
            f"No silent fallback to Qwen3.5-0.8B or any other checkpoint."
        )
    cfg["model_name"] = str(root)
    cfg.pop("model_fallback", None)
    return root


def list_models() -> list[dict]:
    """Studio listing: primary 1.5B first, optional 2B second."""
    rows = []
    for label, folder in (("1.5B", PRIMARY), ("2B", OPTIONAL_2B)):
        path = resolve(folder)
        rows.append({"id": label, "path": str(path), "ready": is_ready(path), "folder": folder})
    return rows
