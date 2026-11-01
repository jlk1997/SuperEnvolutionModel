# -*- coding: utf-8 -*-
from pathlib import Path
import re
p = Path("scripts/c313_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")
# normalize for matching
m = re.search(r'stage = f"""# STAGE_ANT_C313.*?"""\n', t, re.S)
if not m:
    raise SystemExit("no stage block")
new = '''stage = f"""# STAGE_ANT_C313

Updated: {ts()} (Asia/Shanghai)

**C308-C313 STAGE_READY={'YES' if stage_ready else 'NO'}**

## Batch
| Cycle | Theme | Key |
| --- | --- | --- |
| C308 | V34 design | n={c266.get('n')} bamboo/slate/denim/brass/... clarity jpeg_q>=60 |
| C309 | V34 smoke | rate={v34} claim={v34_claim} |
| C310 | V34 heldout | rate={v34h} claim={v34h_claim} |
| C311 | dissolve/cost/shadow | pass={nv_pass} replace={replace.get('mean_ratio')} |
| C312 | capture regression | pass={capture_pass} |
| C313 | scorecard | composite={composite} |

## Iron
Gate **0.6**. Gate2/3 untouched. gen11 HOLD.

## Vision claims (scoped)
- V25: claim={v25_claim} rate={v25}
- V25 heldout: claim={v25h_claim} rate={v25h}
- V26: claim={v26_claim} rate={v26}
- V26 heldout: claim={v26h_claim} rate={v26h}
- V27: claim={v27_claim} rate={v27}
- V27 heldout: claim={v27h_claim} rate={v27h}
- V28: claim={v28s_claim} rate={v28s}
- V28 heldout: claim={v28h_claim} rate={v28h}
- V29: claim={v29s_claim} rate={v29s}
- V29 heldout: claim={v29h_hist_claim} rate={v29h_hist}
- V30: claim={v30_claim} rate={v30}
- V30 heldout: claim={v30h_claim} rate={v30h}
- V31: claim={v31_claim} rate={v31}
- V31 heldout: claim={v31h_claim} rate={v31h}
- V32: claim={v32_claim} rate={v32}
- V32 heldout: claim={v32h_claim} rate={v32h}
- V34: claim={v34_claim} rate={v34}
- V34 heldout: claim={v34h_claim} rate={v34h}
"""
'''
t = t[:m.start()] + new + t[m.end():]
t = t.replace(
    "Stage: C296-C313; V32 CLAIM {v32}; V32 heldout CLAIM {v32h}; nv pass={nv_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}",
    "Stage: C308-C313; V34 CLAIM {v34}; V34 heldout CLAIM {v34h}; nv pass={nv_pass}; capture pass={capture_pass}; composite={composite} STAGE_READY={stage_ready}",
)
t = t.replace(
    "Non-vision C305: pass={nv_pass} rate={conf_rate} (dissolve/shadow); product C299={bool(c299.get('pass'))}/{u2c_rate}; dissolve C293={dissolve_pass}/{shadow_pass}; replace_ratio={replace.get('mean_ratio')}",
    "Non-vision C311: pass={nv_pass} dissolve/shadow; product C299={bool(c299.get('pass'))}/{u2c_rate}; dissolve C311={dissolve_pass}/{shadow_pass}; replace_ratio={replace.get('mean_ratio')}",
)
t = t.replace('f.write(f"\\n## C296-C313 ({ts()})\\n")', 'f.write(f"\\n## C308-C313 ({ts()})\\n")')
compile(t, "c313", "exec")
p.write_text(t, encoding="utf-8")
print("ok", "C308-C313" in t, "C296 | V32 design" not in t)
