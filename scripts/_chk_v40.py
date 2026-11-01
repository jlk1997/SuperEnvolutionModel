from pathlib import Path
for name in ["c346_vision_v40_design_and_batch.py","c347_vision_v40_smoke.py","c348_vision_v40_heldout.py","c349_dissolve_cost_shadow.py","c350_capture_office_regression.py"]:
    s = (Path("scripts")/name).read_text(encoding="utf-8")
    print("===", name)
    print("  v40_", s.count("v40_"), "v39_path", s.count("vision_images_v39"), "C346", s.count("C346"), "C347", s.count("C347"), "C348", s.count("C348"), "C349", s.count("C349"), "C350", s.count("C350"))
    for ln in s.splitlines():
        if ln.startswith("FIX =") or ln.startswith("RUN =") or ln.startswith("PROTO"):
            print(" ", ln[:120])
        if "v40_01" in ln or "v40h_01" in ln or "v39_01" in ln:
            print("  SPEC", ln[:100])
