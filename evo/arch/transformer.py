"""Decoder-only transformer used as the phase-3 baseline."""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class CausalSelfAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        if d_model % n_heads != 0:
            raise ValueError("d_model must be divisible by n_heads")
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.proj = nn.Linear(d_model, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, steps, channels = x.shape
        qkv = self.qkv(x).reshape(batch, steps, 3, self.n_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        query, key, value = qkv[0], qkv[1], qkv[2]
        out = F.scaled_dot_product_attention(query, key, value, is_causal=True)
        out = out.transpose(1, 2).reshape(batch, steps, channels)
        return self.proj(out)


class MLP(nn.Module):
    def __init__(self, d_model: int, d_ff: int):
        super().__init__()
        self.fc = nn.Linear(d_model, d_ff)
        self.proj = nn.Linear(d_ff, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.proj(F.gelu(self.fc(x)))


class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int, d_ff: int):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_heads)
        self.ln2 = nn.LayerNorm(d_model)
        self.mlp = MLP(d_model, d_ff)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.ln1(x))
        x = x + self.mlp(self.ln2(x))
        return x


class TransformerLM(nn.Module):
    def __init__(self, vocab: int, d_model: int, n_layers: int, n_heads: int, d_ff: int, max_len: int):
        super().__init__()
        self.max_len = max_len
        self.emb = nn.Embedding(vocab, d_model)
        self.pos = nn.Embedding(max_len, d_model)
        self.blocks = nn.ModuleList(
            TransformerBlock(d_model, n_heads, d_ff) for _ in range(n_layers)
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
