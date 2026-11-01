"""A phase-3 fast memory beside Qwen's last layer.

The state updates inside the forward pass. It is off while the night optimizer runs.
"""

from __future__ import annotations

import torch
import torch.nn as nn

from evo.arch.selfmod import FrequencyMemory
from evo.model import activate


def _last_decoder(model) -> nn.Module:
    found = None
    for name, module in model.named_modules():
        if name.endswith("layers") and isinstance(module, nn.ModuleList) and len(module) > 0:
            found = module
    if found is None:
        raise RuntimeError("could not find a decoder stack")
    return found[-1]


class FastSidecar:
    def __init__(self, evo, scale: float = 0.02):
        self.evo = evo
        self.scale = scale
        self.mem: FrequencyMemory | None = None
        self.enabled = False
        self.handle = None
        layer = _last_decoder(evo.model)

        def hook(_module, _inputs, output):
            if not self.enabled:
                return output
            hidden = output[0] if isinstance(output, tuple) else output
            if not torch.is_tensor(hidden) or hidden.dim() != 3:
                return output
            if self.mem is None:
                width = int(hidden.shape[-1])
                mem = FrequencyMemory(width, d_mem=32, eta=0.2, decay=0.8, bptt=64, carry=True)
                nn.init.normal_(mem.proj.weight, mean=0.0, std=self.scale)
                self.mem = mem.to(device=hidden.device, dtype=torch.float32)
            with torch.no_grad():
                delta = self.mem(hidden.float())
                rms = hidden.float().pow(2).mean(dim=-1, keepdim=True).sqrt().clamp(min=1e-3)
                delta_rms = delta.pow(2).mean(dim=-1, keepdim=True).sqrt().clamp(min=1e-3)
                delta = delta / delta_rms * rms * self.scale
            updated = hidden + delta.to(dtype=hidden.dtype)
            if isinstance(output, tuple):
                return (updated,) + output[1:]
            return updated

        self.handle = layer.register_forward_hook(hook)

    def on(self) -> None:
        self.enabled = True

    def off(self) -> None:
        self.enabled = False

    def reset(self) -> None:
        if self.mem is not None:
            self.mem.reset_state()

    def absorb(self, text: str, adapter: str | None) -> None:
        """One forward over `text` so the fast state sees it. No optimizer step."""
        if not text.strip():
            return
        self.on()
        try:
            tok = self.evo.tok
            encoded = tok(text, return_tensors="pt", add_special_tokens=False, truncation=True, max_length=256)
            encoded = {key: value.to(self.evo.device) for key, value in encoded.items()}
            with activate(self.evo.model, adapter), torch.no_grad():
                self.evo.model(**encoded)
        finally:
            self.off()

    def close(self) -> None:
        if self.handle is not None:
            self.handle.remove()
            self.handle = None
