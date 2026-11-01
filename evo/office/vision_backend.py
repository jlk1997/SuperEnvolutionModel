# -*- coding: utf-8 -*-
"""VisionBackend drop-in for Ant-Vision (蚁算-视).

Synthetic backends for CPU development. RealVlBackend loads local Qwen3.5 VL
weights when inventory unlocks — never invent scores. Optional PEFT adapter.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class VisionObs:
    image_path: Path
    task: str  # caption | ocr | table_cells
    gold: str | None = None


@dataclass
class VisionPred:
    text: str
    backend: str
    synthetic_not_vl: bool
    confidence: float | None = None


class VisionBackend(Protocol):
    name: str
    synthetic_not_vl: bool

    def predict(self, obs: VisionObs) -> VisionPred: ...


class SyntheticFixtureBackend:
    """Reads gold from sidecar .json next to image; not a VL model."""

    name = "synthetic_fixture"
    synthetic_not_vl = True

    def predict(self, obs: VisionObs) -> VisionPred:
        side = obs.image_path.with_suffix(".json")
        if side.is_file():
            import json
            meta = json.loads(side.read_text(encoding="utf-8"))
            key = {"caption": "caption", "ocr": "ocr_text", "table_cells": "cells_csv"}.get(obs.task, "caption")
            text = str(meta.get(key) or meta.get("gold") or "")
        else:
            text = ""
        return VisionPred(text=text, backend=self.name, synthetic_not_vl=True, confidence=1.0)


class NullBackend:
    name = "null"
    synthetic_not_vl = True

    def predict(self, obs: VisionObs) -> VisionPred:
        return VisionPred(text="", backend=self.name, synthetic_not_vl=True, confidence=0.0)


_TASK_PROMPTS = {
    "caption": "Describe this image in one short sentence.",
    "ocr": "Read all visible text in this image. Reply with the text only.",
    "table_cells": "Extract the table as CSV. Reply with CSV only.",
}


class RealVlBackend:
    """Local Qwen3.5 / Qwen3-VL style image-text model. Optional PEFT LoRA."""

    name = "real_vl"
    synthetic_not_vl = False

    def __init__(
        self,
        weights_path: Path | None = None,
        device: str = "cuda",
        max_new_tokens: int = 96,
        adapter_path: Path | None = None,
    ):
        self.weights_path = Path(weights_path) if weights_path else None
        self.adapter_path = Path(adapter_path) if adapter_path else None
        self.device = device
        self.max_new_tokens = max_new_tokens
        self._model = None
        self._processor = None
        if self.adapter_path is not None:
            self.name = "real_vl_lora"

    def _ensure(self) -> None:
        if self._model is not None:
            return
        if self.weights_path is None or not self.weights_path.is_dir():
            raise RuntimeError(f"RealVlBackend: missing weights_path={self.weights_path}")
        import torch
        from transformers import AutoModelForImageTextToText, AutoProcessor

        self._processor = AutoProcessor.from_pretrained(str(self.weights_path), trust_remote_code=True)
        dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        # Windows WDDM: safetensors open(device=cuda) can hit OSError 1455 (pagefile).
        # Load to CPU then .to(cuda) — proven on this box for Qwen3.5-2B.
        self._model = AutoModelForImageTextToText.from_pretrained(
            str(self.weights_path),
            trust_remote_code=True,
            dtype=dtype,
            low_cpu_mem_usage=True,
        )
        if torch.cuda.is_available() and str(self.device).startswith("cuda"):
            self._model = self._model.to("cuda")
        if self.adapter_path is not None and self.adapter_path.is_dir():
            from peft import PeftModel
            self._model = PeftModel.from_pretrained(self._model, str(self.adapter_path))
            self.name = "real_vl_lora"
        self._model.eval()

    def unload(self) -> None:
        self._model = None
        self._processor = None
        try:
            import torch
            import gc
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception:
            pass

    def predict(self, obs: VisionObs) -> VisionPred:
        from PIL import Image
        import torch

        self._ensure()
        assert self._model is not None and self._processor is not None
        img = Image.open(obs.image_path).convert("RGB")
        prompt = _TASK_PROMPTS.get(obs.task, _TASK_PROMPTS["caption"])
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": img},
                    {"type": "text", "text": prompt},
                ],
            }
        ]
        chat = self._processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self._processor(
            text=[chat],
            images=[img],
            return_tensors="pt",
            padding=True,
        )
        _dev = next(self._model.parameters()).device
        inputs = {k: v.to(_dev) if hasattr(v, "to") else v for k, v in inputs.items()}
        with torch.inference_mode():
            out = self._model.generate(**inputs, max_new_tokens=self.max_new_tokens, do_sample=False)
        gen = out[:, inputs["input_ids"].shape[-1] :]
        text = self._processor.batch_decode(gen, skip_special_tokens=True)[0].strip()
        return VisionPred(text=text, backend=self.name, synthetic_not_vl=False, confidence=None)


def select_backend(weights_local: bool = False, weights_path: Path | None = None):
    if weights_local and weights_path is not None:
        return RealVlBackend(weights_path)
    return SyntheticFixtureBackend()
