# Shell family — LM use_log FIXED → dissolve PASS

Updated: 2026-10-17 16:25 Asia/Shanghai

Gate **0.6**. Exam frozen. C product path unchanged (table/report/file) + **shell atom wired**.

## Root cause
1. Model emitted Unix `cp` / `mkdir -p` / `&&` / `/path/to` placeholders.
2. License allowlist only `mkdir,dir,type,copy` — refused `cp` and compounds → 0 ok traces.
3. `practice_bootstrap` only fired on **unparsed** turns; parseable-but-refused cmds never got gold.

## Fix
- `cp→copy` alias; strip `mkdir -p`; refuse abs/`path/to` shell args (`license.py`)
- Primer allowlist + gold example (`stream.py`)
- Bootstrap also on all-calls-license-refused + persistent scripted cursor
- XML: applied-only, skip shell-family python fences, normalize+dedupe cmds

## Evidence
| Run | ok shell practice |
| --- | ---: |
| bootstrap smoke s7 | **4/4** |
| shell_only s8 x24 | **12/12** |
| dissolve v2 merged n=16 | **bare=1.0 D=0.0** (scaffold=0.0) |

Router: `route("shell")` → atom `office_shell_uselog`. No Gate2.
