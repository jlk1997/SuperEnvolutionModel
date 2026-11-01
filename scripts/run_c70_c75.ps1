$ErrorActionPreference = "Stop"
Set-Location E:\envolution
$py = ".\.venv\Scripts\python.exe"
Write-Host "=== C70 fixtures ==="
& $py scripts\c70_vision_v2h_style_train_fixtures.py
if ($LASTEXITCODE -ne 0) { throw "c70 failed" }
Write-Host "=== C71 absorb (GPU) ==="
& $py scripts\c71_vision_lora_reabsorb_heldout_style.py
if ($LASTEXITCODE -ne 0) { throw "c71 failed" }
Write-Host "=== C72 retest (GPU) ==="
& $py scripts\c72_vision_lora_vs_bare_retest.py
if ($LASTEXITCODE -ne 0) { throw "c72 failed" }
Write-Host "=== C73 fixtures ==="
& $py scripts\c73_vision_v3_dense_ocr_fixtures.py
if ($LASTEXITCODE -ne 0) { throw "c73 failed" }
Write-Host "=== C73b smoke (GPU) ==="
& $py scripts\c73b_vision_v3_dense_smoke.py
if ($LASTEXITCODE -ne 0) { throw "c73b failed" }
Write-Host "=== C74 replace dual ==="
& $py scripts\c74_replace_dual_strengthen.py
if ($LASTEXITCODE -ne 0) { throw "c74 failed" }
Write-Host "=== C75 docs ==="
& $py scripts\c75_docs_checkpoint.py
if ($LASTEXITCODE -ne 0) { throw "c75 failed" }
Write-Host "=== DONE ==="
git add -A
git status --short
