"""Test-time fast weights at several timescales.

The fast matrix is written inside the forward pass (TTT / delta rule).
Outer training updates each frequency level on its own schedule (CMS).
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

from evo.arch.transformer import CausalSelfAttention


class FrequencyMemory(nn.Module):
    def __init__(self, d_model: int, d_mem: int, eta: float, decay: float, bptt: int, carry: bool = False):
        super().__init__()
        self.norm = nn.LayerNorm(d_model)
        self.q = nn.Linear(d_model, d_mem, bias=False)
        self.k = nn.Linear(d_model, d_mem, bias=False)
        self.v = nn.Linear(d_model, d_mem, bias=False)
        self.proj = nn.Linear(d_mem, d_model, bias=False)
        self.eta = eta
        self.decay = decay
        self.bptt = bptt
        self.carry = carry
        self._carry = None

    def reset_state(self) -> None:
        self._carry = None

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        hidden = self.norm(x)
        query = F.normalize(self.q(hidden), dim=-1, eps=1e-6)
        key = F.normalize(self.k(hidden), dim=-1, eps=1e-6)
        value = self.v(hidden)
        batch, steps, width = query.shape
        carried = self._carry
        if (
            self.carry
            and carried is not None
            and carried.shape[0] == batch
            and carried.shape[-1] == width
        ):
            state = carried.to(device=query.device, dtype=query.dtype)
        else:
            state = query.new_zeros(batch, width, width)
        reads = []
        for t in range(steps):
            q_t = query[:, t]
            k_t = key[:, t]
            v_t = value[:, t]
            read = torch.bmm(state, q_t.unsqueeze(-1)).squeeze(-1)
            reads.append(read)
            predicted = torch.bmm(state, k_t.unsqueeze(-1)).squeeze(-1)
            error = v_t - predicted
            state = self.decay * state + self.eta * torch.bmm(error.unsqueeze(-1), k_t.unsqueeze(1))
            state = state.clamp(-5.0, 5.0)
            if self.bptt and (t + 1) % self.bptt == 0:
                state = state.detach()
        if self.carry:
            self._carry = state.detach()
        stacked = torch.stack(reads, dim=1)
        return self.proj(stacked)


class ContinuumMemory(nn.Module):
    def __init__(self, d_model: int, d_mem: int, etas: list[float], decays: list[float], bptt: int, carry: bool = False):
        super().__init__()
        self.levels = nn.ModuleList(
            FrequencyMemory(d_model, d_mem, eta, decay, bptt, carry=carry)
            for eta, decay in zip(etas, decays)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        total = 0
        for level in self.levels:
            total = total + level(x)
        return total


class SelfModBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int, d_mem: int, etas, decays, bptt: int, carry: bool = False):
        super().__init__()
        self.ln = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_heads)
        self.mem = ContinuumMemory(d_model, d_mem, etas, decays, bptt, carry=carry)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.ln(x))
        x = x + self.mem(x)
        return x


class SelfModifyingLM(nn.Module):
    def __init__(
        self,
        vocab: int,
        d_model: int,
        n_layers: int,
        n_heads: int,
        d_mem: int,
        max_len: int,
        etas: list[float],
        decays: list[float],
        bptt: int,
        carry: bool = False,
    ):
        super().__init__()
        self.max_len = max_len
        self.emb = nn.Embedding(vocab, d_model)
        self.pos = nn.Embedding(max_len, d_model)
        self.blocks = nn.ModuleList(
            SelfModBlock(d_model, n_heads, d_mem, etas, decays, bptt, carry=carry) for _ in range(n_layers)
        )
        self.ln = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab, bias=False)
        self.head.weight = self.emb.weight

    def forward(self, idx: torch.Tensor) -> torch.Tensor:
        _batch, steps = idx.shape
        if steps > self.max_len:
            raise ValueError(f"sequence length {steps} exceeds max_len {self.max_len}")
        position = torch.arange(steps, device=idx.device)
        x = self.emb(idx) + self.pos(position)[None, :, :]
        for block in self.blocks:
            x = block(x)
        return self.head(self.ln(x))

    def reset_state(self) -> None:
        for module in self.modules():
            if isinstance(module, FrequencyMemory):
                module.reset_state()


def param_frequency(name: str, freqs: list[int]) -> int:
    marker = ".levels."
    if marker in name:
        index = int(name.split(marker, 1)[1].split(".", 1)[0])
        if 0 <= index < len(freqs):
            return int(freqs[index])
    return int(freqs[0])
