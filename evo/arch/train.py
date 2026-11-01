"""Sequential training and test-time evaluation for the two small LMs."""

from __future__ import annotations

import random
import time

import torch
import torch.nn.functional as F

from evo.arch.data import build_corpus, sample_batch, stream
from evo.arch.selfmod import SelfModifyingLM, param_frequency
from evo.arch.transformer import TransformerLM
from evo.util import set_seed


def n_params(model: torch.nn.Module) -> int:
    return sum(param.numel() for param in model.parameters())


def token_nll(model, idx: torch.Tensor) -> torch.Tensor:
    logits = model(idx[:, :-1])
    target = idx[:, 1:]
    return F.cross_entropy(logits.reshape(-1, logits.size(-1)), target.reshape(-1))


@torch.no_grad()
def eval_sentences(model, sentences: list[str], tok, device) -> float:
    model.eval()
    total = 0.0
    count = 0
    for sentence in sentences:
        if hasattr(model, "reset_state"):
            model.reset_state()
        ids = tok.encode(sentence)
        if len(ids) < 2:
            continue
        if len(ids) > model.max_len:
            ids = ids[: model.max_len]
        batch = torch.tensor([ids], device=device)
        loss = token_nll(model, batch)
        tokens = batch.size(1) - 1
        total += float(loss.item()) * tokens
        count += tokens
    return total / max(count, 1)


@torch.no_grad()
def half_nll(model, ids: list[int], device, second: bool) -> float:
    if hasattr(model, "reset_state"):
        model.reset_state()
    model.eval()
    batch = torch.tensor([ids], device=device)
    logits = model(batch[:, :-1])
    mid = batch.size(1) // 2
    if second:
        target = batch[:, mid:]
        pred = logits[:, mid - 1 : mid - 1 + target.size(1), :]
    else:
        target = batch[:, 1:mid]
        pred = logits[:, : target.size(1), :]
    return float(F.cross_entropy(pred.reshape(-1, pred.size(-1)), target.reshape(-1)).item())


def _match_ff(vocab: int, cfg: dict, target: int) -> int:
    """Binary search MLP width so the transformer has about as many parameters."""
    lo, hi = 256, cfg["d_model"] * 8
    best_ff, best_gap = lo, None
    while lo <= hi:
        mid = max(64, ((lo + hi) // 2 // 64) * 64)
        probe = TransformerLM(vocab, cfg["d_model"], cfg["n_layers"], cfg["n_heads"], mid, cfg["seq_len"])
        count = n_params(probe)
        gap = abs(count - target)
        if best_gap is None or gap < best_gap:
            best_ff, best_gap = mid, gap
        del probe
        if count < target:
            lo = mid + 64
        else:
            hi = mid - 64
    return best_ff


def build_models(cfg: dict, vocab: int, device: torch.device):
    set_seed(cfg["seed"])
    probe = SelfModifyingLM(
        vocab,
        cfg["d_model"],
        cfg["n_layers"],
        cfg["n_heads"],
        cfg["d_mem"],
        cfg["seq_len"],
        cfg["etas"],
        cfg["decays"],
        cfg["bptt"],
    )
    target = n_params(probe)
    d_ff = _match_ff(vocab, cfg, target)
    del probe
    set_seed(cfg["seed"])
    selfmod = SelfModifyingLM(
        vocab,
        cfg["d_model"],
        cfg["n_layers"],
        cfg["n_heads"],
        cfg["d_mem"],
        cfg["seq_len"],
        cfg["etas"],
        cfg["decays"],
        cfg["bptt"],
    ).to(device)
    set_seed(cfg["seed"])
    transformer = TransformerLM(
        vocab, cfg["d_model"], cfg["n_layers"], cfg["n_heads"], d_ff, cfg["seq_len"]
    ).to(device)
    return transformer, selfmod, d_ff


def freeze_slowest(model, freqs: list[int]) -> int:
    """Stop the slowest CMS level from being overwritten by the next domain."""
    levels = [int(freq) for freq in freqs]
    slow = max(levels)
    frozen = 0
    for name, param in model.named_parameters():
        if ".levels." in name and param_frequency(name, levels) == slow:
            param.requires_grad_(False)
            frozen += param.numel()
    return frozen


def _optimizers(model, lr: float, freqs: list[int]):
    groups: dict[int, list] = {int(freq): [] for freq in freqs}
    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        groups[param_frequency(name, freqs)].append(param)
    opts = {}
    for freq, params in groups.items():
        if params:
            opts[freq] = torch.optim.AdamW(params, lr=lr)
    return opts


def _step(opts, step: int, clip: float) -> None:
    for freq, opt in opts.items():
        if step % freq != 0:
            continue
        params = [param for group in opt.param_groups for param in group["params"]]
        for param in params:
            if param.grad is not None:
                param.grad.div_(freq)
        torch.nn.utils.clip_grad_norm_(params, clip)
        opt.step()
        opt.zero_grad(set_to_none=True)


def _refresh_state(model, ids: list[int], cursor: int, seq_len: int, batch_size: int, device) -> int:
    """One no-grad forward on domain A so the fast state is rewritten and the weights stay put."""
    if len(ids) < seq_len:
        return cursor
    if cursor + seq_len > len(ids):
        cursor = 0
    window = ids[cursor : cursor + seq_len]
    rows = [window for _ in range(batch_size)]
    training = model.training
    model.eval()
    with torch.no_grad():
        token_nll(model, torch.tensor(rows, device=device))
    if training:
        model.train()
    return cursor + seq_len


def _recall_window(ids: list[int], cursor: int, seq_len: int, batch_size: int, device):
    if len(ids) < seq_len:
        return None, cursor
    if cursor + seq_len > len(ids):
        cursor = 0
    window = ids[cursor : cursor + seq_len]
    rows = [window for _ in range(batch_size)]
    return torch.tensor(rows, device=device), cursor + seq_len


def _recall_fast(model, ids, cursor, seq_len, batch_size, device, opts, clip: float) -> int:
    """One gradient step on the fastest memory level only. Shared layers keep the B gradient at zero."""
    batch, advanced = _recall_window(ids, cursor, seq_len, batch_size, device)
    if batch is None:
        return cursor
    training = model.training
    model.train()
    for opt in opts.values():
        opt.zero_grad(set_to_none=True)
    loss = token_nll(model, batch)
    loss.backward()
    for name, param in model.named_parameters():
        if param.grad is not None and ".levels.0." not in name:
            param.grad = None
    for opt in opts.values():
        owned = [param for group in opt.param_groups for param in group["params"] if param.grad is not None]
        if not owned:
            opt.zero_grad(set_to_none=True)
            continue
        torch.nn.utils.clip_grad_norm_(owned, clip)
        opt.step()
        opt.zero_grad(set_to_none=True)
    if not training:
        model.eval()
    return advanced


def _replay_all(model, ids, cursor, seq_len, batch_size, device, opts, clip: float) -> int:
    """One gradient step on every weight, using the next domain-A window."""
    batch, advanced = _recall_window(ids, cursor, seq_len, batch_size, device)
    if batch is None:
        return cursor
    training = model.training
    model.train()
    for opt in opts.values():
        opt.zero_grad(set_to_none=True)
    loss = token_nll(model, batch)
    loss.backward()
    for opt in opts.values():
        owned = [param for group in opt.param_groups for param in group["params"] if param.grad is not None]
        if not owned:
            opt.zero_grad(set_to_none=True)
            continue
        torch.nn.utils.clip_grad_norm_(owned, clip)
        opt.step()
        opt.zero_grad(set_to_none=True)
    if not training:
        model.eval()
    return advanced


def _train_domain(model, ids, cfg, device, seed: int, replay_ids=None, recall_ids=None, sparse_ids=None) -> list[dict]:
    opts = _optimizers(model, cfg["arch_lr"], [int(freq) for freq in cfg["freqs"]])
    for opt in opts.values():
        opt.zero_grad(set_to_none=True)
    if hasattr(model, "reset_state"):
        model.reset_state()
    rng = random.Random(seed)
    history = []
    model.train()
    started = time.time()
    recall_every = int(cfg.get("recall_every") or 0)
    replay_every = int(cfg.get("replay_every") or 0)
    cursor = 0
    recalls = 0
    sparse_steps = 0
    for step in range(cfg["steps_per_domain"]):
        rows = sample_batch(ids, cfg["batch_size"], cfg["seq_len"], rng)
        frac = float(cfg.get("replay_frac") or 0.0)
        if replay_ids is not None and frac > 0:
            n_replay = max(1, int(round(cfg["batch_size"] * frac)))
            rows[:n_replay] = sample_batch(replay_ids, n_replay, cfg["seq_len"], rng)
        batch = torch.tensor(rows, device=device)
        loss = token_nll(model, batch)
        loss.backward()
        _step(opts, step, cfg["grad_clip"])
        if recall_ids is not None and recall_every and (step + 1) % recall_every == 0:
            if cfg.get("recall_grad"):
                cursor = _recall_fast(
                    model,
                    recall_ids,
                    cursor,
                    cfg["seq_len"],
                    cfg["batch_size"],
                    device,
                    opts,
                    cfg["grad_clip"],
                )
            else:
                cursor = _refresh_state(
                    model, recall_ids, cursor, cfg["seq_len"], cfg["batch_size"], device
                )
            recalls += 1
        if sparse_ids is not None and replay_every and (step + 1) % replay_every == 0:
            cursor = _replay_all(
                model,
                sparse_ids,
                cursor,
                cfg["seq_len"],
                cfg["batch_size"],
                device,
                opts,
                cfg["grad_clip"],
            )
            sparse_steps += 1
        if step % cfg["log_every"] == 0 or step + 1 == cfg["steps_per_domain"]:
            history.append({"step": step, "loss": float(loss.detach().item())})
            print(
                f"[arch] step={step} loss={history[-1]['loss']:.3f} "
                f"elapsed={time.time() - started:.1f}s",
                flush=True,
            )
    history.append({"seconds": time.time() - started, "recalls": recalls, "sparse_steps": sparse_steps})
    if recalls:
        kind = "fast-grad" if cfg.get("recall_grad") else "state"
        print(f"[arch] {kind} recalls={recalls}", flush=True)
    if sparse_steps:
        print(f"[arch] sparse replays={sparse_steps}", flush=True)
    return history


def _snapshot_nll(model, corpus, device) -> dict:
    tok = corpus["tokenizer"]
    return {
        "nll_a": eval_sentences(model, corpus["a_test"], tok, device),
        "nll_a_train": eval_sentences(model, corpus["a_train"][:24], tok, device),
        "nll_b": eval_sentences(model, corpus["b_test"], tok, device),
        "nll_b_train": eval_sentences(model, corpus["b_train"][:24], tok, device),
    }


def train_one(model, corpus, cfg, device, seed: int, lock_slow: bool = False) -> dict:
    tok = corpus["tokenizer"]
    before = _snapshot_nll(model, corpus, device)
    a_ids = stream(corpus["a_train"], tok)
    b_ids = stream(corpus["b_train"], tok)
    a_hist = _train_domain(model, a_ids, cfg, device, seed)
    after_a = _snapshot_nll(model, corpus, device)
    frozen = freeze_slowest(model, cfg["freqs"]) if lock_slow else 0
    if frozen:
        print(f"[arch] froze slowest memory level params={frozen}", flush=True)
    replay = a_ids if cfg.get("replay_frac") else None
    recall_ids = a_ids if cfg.get("recall_every") else None
    sparse_ids = a_ids if cfg.get("replay_every") else None
    b_hist = _train_domain(
        model,
        b_ids,
        cfg,
        device,
        seed + 1,
        replay_ids=replay,
        recall_ids=recall_ids,
        sparse_ids=sparse_ids,
    )
    state_hold = (
        _state_hold(model, a_ids, device, cfg["seq_len"], cfg["batch_size"])
        if cfg.get("recall_every")
        else None
    )
    after_b = _snapshot_nll(model, corpus, device)
    novel_ids = []
    for sentence in corpus["novel"]:
        novel_ids.extend(tok.encode(sentence))
    while len(novel_ids) < cfg["seq_len"]:
        novel_ids = novel_ids + novel_ids
    novel_ids = novel_ids[: cfg["seq_len"]]
    ttt_first = half_nll(model, novel_ids, device, second=False)
    ttt_second = half_nll(model, novel_ids, device, second=True)
    restream = _restream(model, a_ids, device, cfg["seq_len"]) if cfg.get("carry_state") else None
    return {
        "before": before,
        "after_a": after_a,
        "after_b": after_b,
        "frozen_params": frozen,
        "forgetting_a": after_b["nll_a_train"] - after_a["nll_a_train"],
        "acquisition_b": after_a["nll_b_train"] - after_b["nll_b_train"],
        "ttt_first_half_nll": ttt_first,
        "ttt_second_half_nll": ttt_second,
        "restream": restream,
        "state_hold": state_hold,
        "a_loss": a_hist,
        "b_loss": b_hist,
    }


@torch.no_grad()
def _restream(model, ids: list[int], device, seq_len: int) -> dict | None:
    """Read a domain in order with carried fast weights and no optimizer step."""
    if not hasattr(model, "reset_state"):
        return None
    if len(ids) < seq_len * 2:
        return None
    model.reset_state()
    model.eval()
    losses = []
    start = 0
    while start + seq_len <= len(ids) and len(losses) < 4:
        batch = torch.tensor([ids[start : start + seq_len]], device=device)
        losses.append(float(token_nll(model, batch).item()))
        start += seq_len
    if len(losses) < 2:
        return None
    return {
        "chunks": losses,
        "first": losses[0],
        "last": losses[-1],
        "gain": losses[0] - losses[-1],
    }


@torch.no_grad()
def _state_hold(model, ids: list[int], device, seq_len: int, batch_size: int) -> dict | None:
    """NLL of one domain-A window with the live fast state, then with the state cleared."""
    if not hasattr(model, "reset_state") or len(ids) < seq_len:
        return None
    window = ids[:seq_len]
    batch = torch.tensor([window for _ in range(batch_size)], device=device)
    model.eval()
    carried = float(token_nll(model, batch).item())
    model.reset_state()
    reset = float(token_nll(model, batch).item())
    model.reset_state()
    return {"carried_nll": carried, "reset_nll": reset, "hold": reset - carried}


def run_arch(cfg: dict) -> dict:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.set_float32_matmul_precision("high")
    corpus = build_corpus()
    vocab = corpus["tokenizer"].vocab_size
    if cfg.get("carry_only") or cfg.get("recall_only"):
        set_seed(cfg["seed"])
        carried = SelfModifyingLM(
            vocab,
            cfg["d_model"],
            cfg["n_layers"],
            cfg["n_heads"],
            cfg["d_mem"],
            cfg["seq_len"],
            cfg["etas"],
            cfg["decays"],
            cfg["bptt"],
            carry=True,
        ).to(device)
        label = "recall_only" if cfg.get("recall_only") else "carry_only"
        key = "selfmod_recall" if cfg.get("recall_only") else "selfmod_carry"
        print(f"[arch] {label} device={device} recall_every={cfg.get('recall_every')}", flush=True)
        carried_result = train_one(carried, corpus, cfg, device, cfg["seed"] + 7)
        return {
            "device": str(device),
            "vocab": vocab,
            "params": {key: n_params(carried)},
            "note": (
                "Fast weights persist inside a domain. recall_every runs a no-grad pass over domain A "
                "during domain B, so the state is refreshed and the optimizer still steps only on B. "
                "state_hold is reset NLL minus carried NLL on one A window."
            ),
            key: carried_result,
        }
    if cfg.get("sparse_only"):
        set_seed(cfg["seed"])
        sparse_model = SelfModifyingLM(
            vocab,
            cfg["d_model"],
            cfg["n_layers"],
            cfg["n_heads"],
            cfg["d_mem"],
            cfg["seq_len"],
            cfg["etas"],
            cfg["decays"],
            cfg["bptt"],
        ).to(device)
        print(f"[arch] sparse_only every={cfg.get('replay_every')} device={device}", flush=True)
        sparse_result = train_one(sparse_model, corpus, cfg, device, cfg["seed"] + 7)
        return {
            "device": str(device),
            "vocab": vocab,
            "params": {"selfmod_sparse": n_params(sparse_model)},
            "selfmod_sparse": sparse_result,
            "note": (
                "Every replay_every steps during domain B, one extra update is taken on the next "
                "domain-A window. That step touches every weight. The other steps train on domain B."
            ),
        }
    if cfg.get("replay_only"):
        set_seed(cfg["seed"])
        replay_model = SelfModifyingLM(
            vocab,
            cfg["d_model"],
            cfg["n_layers"],
            cfg["n_heads"],
            cfg["d_mem"],
            cfg["seq_len"],
            cfg["etas"],
            cfg["decays"],
            cfg["bptt"],
        ).to(device)
        print(f"[arch] replay_only frac={cfg.get('replay_frac')} device={device}", flush=True)
        replay_result = train_one(replay_model, corpus, cfg, device, cfg["seed"] + 7)
        return {
            "device": str(device),
            "vocab": vocab,
            "params": {"selfmod_replay": n_params(replay_model)},
            "selfmod_replay": replay_result,
            "note": (
                "During domain B, replay_frac of each batch is drawn from domain A. "
                "The fast state itself is still reset every forward."
            ),
        }
    transformer, selfmod, d_ff = build_models(cfg, vocab, device)
    print(
        f"[arch] device={device} vocab={vocab} transformer={n_params(transformer)} "
        f"selfmod={n_params(selfmod)} d_ff={d_ff}",
        flush=True,
    )
    selfmod.cpu()
    transformer_result = train_one(transformer, corpus, cfg, device, cfg["seed"] + 7)
    transformer.cpu()
    selfmod.to(device)
    selfmod_result = train_one(selfmod, corpus, cfg, device, cfg["seed"] + 7)
    locked_result = None
    if cfg.get("lock_slow"):
        selfmod.cpu()
        set_seed(cfg["seed"])
        locked = SelfModifyingLM(
            vocab,
            cfg["d_model"],
            cfg["n_layers"],
            cfg["n_heads"],
            cfg["d_mem"],
            cfg["seq_len"],
            cfg["etas"],
            cfg["decays"],
            cfg["bptt"],
        ).to(device)
        print("[arch] training selfmod with the slow level locked on domain B", flush=True)
        locked_result = train_one(locked, corpus, cfg, device, cfg["seed"] + 7, lock_slow=True)
    summary = {
        "device": str(device),
        "vocab": vocab,
        "d_ff": d_ff,
        "params": {"transformer": n_params(transformer), "selfmod": n_params(selfmod)},
        "transformer": transformer_result,
        "selfmod": selfmod_result,
        "note": (
            "forgetting_a > 0 means domain A got worse after training on B. "
            "ttt_second_half_nll is loss on the second half of a novel domain "
            "seen in a single forward, with no optimizer step. "
            "selfmod_locked freezes the slowest memory level before domain B."
        ),
    }
    if locked_result is not None:
        summary["selfmod_locked"] = locked_result
        summary["params"]["selfmod_locked"] = n_params(locked)
    return summary
