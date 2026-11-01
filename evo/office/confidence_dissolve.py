# -*- coding: utf-8 -*-
GATE=0.6
def route_mode(confidence, bare_rate_hist):
    if confidence>=0.8 and bare_rate_hist>=GATE: return "bare"
    if confidence>=0.5: return "light_scaffold"
    return "full_scaffold"
