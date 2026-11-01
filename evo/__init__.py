"""Local weight-level self-evolution experiments.

Phase 1 writes self-edits into LoRA weights and measures retention.
Phase 2 proposes and solves tasks checked by a Python executor.
Phase 3 trains a small transformer against a test-time fast-weight model.
"""

__version__ = "0.1.0"
