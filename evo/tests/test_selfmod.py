import unittest

import torch
import torch.nn.functional as F

from evo.arch.selfmod import FrequencyMemory, SelfModifyingLM, param_frequency
from evo.arch.train import _recall_fast, _refresh_state, _replay_all, freeze_slowest
from evo.selfplay.heldout import last_number, parse_yes


class SelfModTest(unittest.TestCase):
    def test_freeze_slowest_level(self):
        torch.manual_seed(0)
        model = SelfModifyingLM(
            vocab=20,
            d_model=32,
            n_layers=1,
            n_heads=4,
            d_mem=8,
            max_len=8,
            etas=[0.3, 0.1, 0.02],
            decays=[0.6, 0.9, 0.99],
            bptt=8,
        )
        frozen = freeze_slowest(model, [1, 4, 16])
        self.assertGreater(frozen, 0)
        slow = [param for name, param in model.named_parameters() if ".levels.2." in name]
        fast = [param for name, param in model.named_parameters() if ".levels.0." in name]
        self.assertTrue(slow and all(not param.requires_grad for param in slow))
        self.assertTrue(fast and all(param.requires_grad for param in fast))

    def test_sparse_replay_updates_shared_weights(self):
        torch.manual_seed(0)
        model = SelfModifyingLM(
            vocab=20,
            d_model=32,
            n_layers=1,
            n_heads=4,
            d_mem=8,
            max_len=8,
            etas=[1.0, 0.1],
            decays=[0.5, 0.9],
            bptt=8,
        )
        before_emb = model.emb.weight.detach().clone()
        before_slow = [param.detach().clone() for name, param in model.named_parameters() if ".levels.1." in name]
        opt = torch.optim.AdamW([param for _name, param in model.named_parameters()], lr=0.05)
        _replay_all(model, list(range(16)), 0, 8, 2, torch.device("cpu"), {1: opt}, 1.0)
        self.assertFalse(torch.equal(before_emb, model.emb.weight))
        slow = [param for name, param in model.named_parameters() if ".levels.1." in name]
        self.assertTrue(any(not torch.equal(old, param) for old, param in zip(before_slow, slow)))

    def test_fast_recall_updates_only_the_fast_level(self):
        torch.manual_seed(0)
        model = SelfModifyingLM(
            vocab=20,
            d_model=32,
            n_layers=1,
            n_heads=4,
            d_mem=8,
            max_len=8,
            etas=[1.0, 0.1],
            decays=[0.5, 0.9],
            bptt=8,
            carry=True,
        )
        fast = [(name, param) for name, param in model.named_parameters() if ".levels.0." in name]
        others = [(name, param) for name, param in model.named_parameters() if ".levels.0." not in name]
        before_fast = [(name, param.detach().clone()) for name, param in fast]
        before_other = [(name, param.detach().clone()) for name, param in others]
        opt = torch.optim.AdamW([param for _name, param in model.named_parameters()], lr=0.05)
        _recall_fast(model, list(range(16)), 0, 8, 2, torch.device("cpu"), {1: opt}, 1.0)
        self.assertTrue(any(not torch.equal(old, param) for (_name, old), (_n, param) in zip(before_fast, fast)))
        self.assertTrue(all(torch.equal(old, param) for (_name, old), (_n, param) in zip(before_other, others)))

    def test_refresh_writes_state_and_keeps_weights(self):
        torch.manual_seed(0)
        model = SelfModifyingLM(
            vocab=20,
            d_model=32,
            n_layers=1,
            n_heads=4,
            d_mem=8,
            max_len=8,
            etas=[1.0],
            decays=[1.0],
            bptt=8,
            carry=True,
        )
        before = [param.detach().clone() for param in model.parameters()]
        _refresh_state(model, list(range(16)), 0, 8, 2, torch.device("cpu"))
        for old, new in zip(before, model.parameters()):
            self.assertTrue(torch.equal(old, new))
        self.assertIsNotNone(model.blocks[0].mem.levels[0]._carry)

    def test_carry_survives_until_reset(self):
        torch.manual_seed(0)
        memory = FrequencyMemory(d_model=16, d_mem=8, eta=1.0, decay=1.0, bptt=8, carry=True)
        data = torch.randn(1, 4, 16)
        first = memory(data)
        second = memory(data)
        self.assertFalse(torch.allclose(second[:, 0], torch.zeros_like(second[:, 0]), atol=1e-5))
        memory.reset_state()
        third = memory(data)
        self.assertTrue(torch.allclose(third[:, 0], torch.zeros_like(third[:, 0]), atol=1e-5))
        self.assertEqual(tuple(first.shape), (1, 4, 16))

    def test_frequency_names(self):
        freqs = [1, 4, 16]
        self.assertEqual(param_frequency("blocks.0.mem.levels.2.q.weight", freqs), 16)
        self.assertEqual(param_frequency("blocks.0.attn.qkv.weight", freqs), 1)

    def test_read_is_causal(self):
        torch.manual_seed(0)
        memory = FrequencyMemory(d_model=16, d_mem=8, eta=1.0, decay=1.0, bptt=8)
        y = memory(torch.randn(2, 4, 16))
        self.assertEqual(tuple(y.shape), (2, 4, 16))
        self.assertTrue(torch.isfinite(y).all())
        # Position 0 is read before any write, and the output projection has no bias.
        self.assertTrue(torch.allclose(y[:, 0], torch.zeros_like(y[:, 0]), atol=1e-5))

    def test_short_train_stays_finite(self):
        torch.manual_seed(0)
        model = SelfModifyingLM(
            vocab=40,
            d_model=32,
            n_layers=1,
            n_heads=4,
            d_mem=16,
            max_len=16,
            etas=[0.2],
            decays=[0.9],
            bptt=16,
        )
        opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
        data = torch.randint(0, 40, (4, 16))
        for _ in range(3):
            opt.zero_grad(set_to_none=True)
            logits = model(data[:, :-1])
            loss = F.cross_entropy(logits.reshape(-1, 40), data[:, 1:].reshape(-1))
            self.assertTrue(torch.isfinite(loss))
            loss.backward()
            opt.step()


class HeldoutParseTest(unittest.TestCase):
    def test_number_and_yes(self):
        self.assertEqual(last_number("the answer is 12."), "12")
        self.assertEqual(parse_yes("Yes, I think so"), 1.0)
        self.assertEqual(parse_yes("no"), 0.0)
        self.assertEqual(parse_yes("maybe"), 0.5)
