from pathlib import Path
p = Path("tools/_boot_v38_c332.py")
lines = p.read_text(encoding="utf-8-sig").splitlines(True)
start = next(i for i,l in enumerate(lines) if l.startswith("def inject_overlay"))
end = next(i for i,l in enumerate(lines) if i>start and l.startswith("def "))
# build regex pattern without broken escapes: \n    # --- V37 overlays.*?\n(?=    img\.save\(buf)
pat = "\\n    # --- V37 overlays.*?\\n(?=    img\\.save\\(buf)"
new_lines = [
    "def inject_overlay(text: str) -> str:\n",
    '    soft = "    buf = io.BytesIO()"\n',
    '    text2 = re.sub(r"' + pat + '", "\\n", text, count=1, flags=re.S)\n',
    "    if soft not in text2:\n",
    '        soft = "    img.save(buf"\n',
    '    if "CEDAR bait" not in text2 and soft in text2:\n',
    '        text2 = text2.replace(soft, V38_OVERLAY + "\\n" + soft, 1)\n',
    "    return text2\n",
    "\n",
]
lines[start:end] = new_lines
text = "".join(lines)
p.write_text(text, encoding="utf-8")
compile(text, str(p), "exec")
print("compiles ok", start, end)
