# -*- coding: utf-8 -*-
from dataclasses import dataclass
GATE=0.6
@dataclass
class PromoteDecision:
    family: str; current: str; nxt: str|None; reason: str
def decide(family, level, bare_rate, n_success, safety_ok, fail_rate=0.0):
    if fail_rate>0.3 or not safety_ok: return PromoteDecision(family, level, "assist", "demote")
    if level=="assist" and bare_rate>=GATE and n_success>=8 and safety_ok: return PromoteDecision(family, level, "shadow", "up")
    if level=="shadow" and bare_rate>=0.8 and n_success>=20 and safety_ok: return PromoteDecision(family, level, "auto", "up")
    return PromoteDecision(family, level, None, "hold")
