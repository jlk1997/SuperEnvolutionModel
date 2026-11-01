# -*- coding: utf-8 -*-
def critique(ok, family, steps):
    if ok and steps<=2: return {"tag":"excellent","action":"promote_signal"}
    if ok: return {"tag":"ok","action":"keep"}
    return {"tag":"fail","action":"crystal_fix_or_demote"}
