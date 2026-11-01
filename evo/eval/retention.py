"""Retention matrix helpers and plots."""

from __future__ import annotations

import csv
from pathlib import Path


def matrix_stats(matrix: list[list[float | None]]) -> dict:
    diagonal = []
    for index, row in enumerate(matrix):
        if index < len(row) and row[index] is not None:
            diagonal.append(row[index])
    final = [value for value in matrix[-1] if value is not None] if matrix else []

    def avg(values):
        return sum(values) / len(values) if values else None

    return {
        "mean_immediate_f1": avg(diagonal),
        "final_retention_f1": avg(final),
    }


def retention_curve(matrix: list[list[float | None]]) -> list[float | None]:
    curve = []
    for row in matrix:
        seen = [value for value in row if value is not None]
        curve.append(sum(seen) / len(seen) if seen else None)
    return curve


def write_matrix_csv(matrix: list[list[float | None]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        for row in matrix:
            writer.writerow(["" if value is None else f"{value:.4f}" for value in row])


def save_heatmap(matrix: list[list[float | None]], path: Path, title: str) -> bool:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return False
    numeric = [[0.0 if value is None else value for value in row] for row in matrix]
    if not numeric:
        return False
    fig, ax = plt.subplots(figsize=(6, 5))
    image = ax.imshow(numeric, vmin=0, vmax=1, cmap="viridis")
    ax.set_xlabel("Passage")
    ax.set_ylabel("After update")
    ax.set_title(title)
    fig.colorbar(image, ax=ax, label="F1")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return True


def save_curves(curves: dict[str, list[float | None]], path: Path, title: str) -> bool:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return False
    fig, ax = plt.subplots(figsize=(7, 4))
    for name, values in curves.items():
        xs = list(range(1, len(values) + 1))
        ys = [0.0 if value is None else value for value in values]
        ax.plot(xs, ys, marker="o", label=name)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Updates")
    ax.set_ylabel("Mean F1 on seen passages")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return True


def save_bars(rows: dict[str, dict], path: Path) -> bool:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return False
    names = list(rows)
    if not names:
        return False
    immediate = [rows[name].get("mean_immediate_f1") or 0 for name in names]
    retention = [rows[name].get("final_retention_f1") or 0 for name in names]
    import numpy as np

    x = np.arange(len(names))
    width = 0.35
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(x - width / 2, immediate, width, label="immediate F1")
    ax.bar(x + width / 2, retention, width, label="final retention F1")
    ax.set_xticks(x, names)
    ax.set_ylim(0, 1)
    ax.set_title("Anti-forgetting ablation")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return True
