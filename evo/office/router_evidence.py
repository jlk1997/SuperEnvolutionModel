# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
@dataclass
class EvidenceChain:
    task: str
    atoms: list = field(default_factory=list)
    why: list = field(default_factory=list)
    def add(self, atom, reason):
        self.atoms.append(atom); self.why.append(reason)
    def ok(self):
        return bool(self.atoms) and len(self.why)>=len(self.atoms)
def explain_family(family: str):
    ev=EvidenceChain(task=f"office_{family}")
    ev.add(f"office_{family}_uselog", f"family={family}; dissolve bare clears gate 0.6")
    return ev
