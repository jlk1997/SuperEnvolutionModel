# C4 dissolve diagnosis — why bare=0 (table/report)

Updated: 2026-10-17 14:35 Asia/Shanghai

Gate **0.6** never lowered. No Gate2 from notes_only scaffold.

## Attempts

| ID | Actor | SFT | bare | scaffold | D |
| --- | --- | --- | ---: | ---: | ---: |
| v1 | raw generate(prompt) | night steps=9 on **raw** traces | 0 | 0 | 0 |
| v2 | stream._model_reply + tool_call primer | same raw pairs | 0 | 0 | 0 |
| v3 | events_xml n=3 table | _model_reply steps=9 | 0 | 0 | 0 |
| v4 | events_xml n=8 report (F3j) | epochs=4 steps=32 | **0** | **1.0** | 1.0 |
| v5 | events_xml n=7 table (merged F3i+F3j) | epochs=4 | **RUNNING** | — | — |

## Root cause (falsifiable)

evo.session.trace.trace_text / dump_arm_use_log persist **naked code/cmd strings**.
Office eval requires **XML** <tool_call><function=...> (see format_call / TOOL_CALL_PRIMER).

Evidence from F3i dual.jsonl:
- all 8 ok traces have xml=False
- heads look like python -c "..." / import json... not <tool_call>

So SFT taught the wrong surface form. Held-out episodes never parse tool calls → bare=scaffold=0 even when scaffold notes paste the same naked trace.

Secondary factors (not primary):
- **n small**: table only 3 ok practice pairs (smoke min)
- held-out seeds 9000+ are unseen tasks (correct for C4; not the format bug)

## Fix recipe

1. Rebuild pairs via evo.office.use_log_xml from EventBus tool events → dual_xml.jsonl. **DONE**
2. dissolve_uselog prefers pair_source=events_xml. **DONE**
3. Keep office _model_reply actor at eval. **DONE**
4. Grow n (F3j steps=32) + merge corpora. **DONE** n_ok=23
5. After XML+n↑: report scaffold clears 4/4 but bare stays 0 → **capacity/internalize gap**, not format alone.

## Status

- XML rebuild DONE on F3i + F3j; merged_xml_s0 n_ok=23 (report12/table7/file4).
- v3 table still bare=scaffold=0.
- **v4 report**: bare=0.0 scaffold=1.0 D=1.0 internalized=false adapter kept=false; gate 0.6 not cleared; no Gate2.
- **v5 table merged** detached 2026-10-17 14:35 (gpu_heavy=31488).

## Next C knife after v5

If v5 table bare still <0.6: try report dissolve on merged (n=12) OR longer epochs; keep Gate 0.6; exam ladder frozen; no Gate2.
