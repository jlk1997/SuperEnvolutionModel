# -*- coding: utf-8 -*-
from dataclasses import dataclass
@dataclass
class RecoveryResult:
    ok: bool; attempts: int; path: list
def recover(primary_ok, fallback_ok):
    path=["try_primary"]
    if primary_ok: return RecoveryResult(True,1,path+["success"])
    path.append("fallback_atom")
    if fallback_ok: return RecoveryResult(True,2,path+["success_fallback"])
    return RecoveryResult(False,2,path+["demote_assist"])
