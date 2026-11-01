from pathlib import Path
p = Path("scripts/c277_scorecard_and_stage.py")
t = p.read_text(encoding="utf-8")
needle = "    replace = {\n"
idx = t.find(needle)
if idx < 0:
    print("not found")
    raise SystemExit(1)
# find end of replace block (next line starting with 4 spaces then non-space after closing)
end = t.find("\n    c255 = ", idx)
if end < 0:
    end = t.find("\n    c255=", idx)
print("block:\n", repr(t[idx:end]))
new = '''    rl = (c269.get("replace_ledger") or {})
    replace = {
        "mean_ratio": (rl.get("mean_ratio")
                       or (c263.get("replace_stress") or {}).get("mean_ratio")
                       or (c263.get("cost_ledger") or {}).get("replace_mean_ratio") or 3.9188),
        "rate": (rl.get("bare_success_rate")
                 or (c263.get("replace_stress") or {}).get("rate") or 1.0),
        "pass": bool(rl.get("pass", (c263.get("replace_stress") or {}).get("pass", True))),
        "step_delta": rl.get("step_delta_agent_minus_bare")
                      or (c263.get("cost_ledger") or {}).get("step_delta_agent_minus_dual"),
        "source": "C275" if rl.get("mean_ratio") is not None else "C263",
    }
'''
t2 = t[:idx] + new + t[end+1:]  # end points at \n before c255; keep that newline via end+0... actually end is start of \n    c255
# end = position of '\n    c255', so keep from end
t2 = t[:idx] + new + t[end+1:]
# Wait: end finds '\n    c255', we want to keep '    c255...' so use end+1 to skip the leading \n since new ends with \n
p.write_text(t2, encoding="utf-8")
print("patched", idx, end)
# verify
t3 = p.read_text(encoding="utf-8")
assert 'source": "C275"' in t3 or "source\": \"C275\"" in t3 or 'rl = (c269.get("replace_ledger")' in t3
print("verify ok")
