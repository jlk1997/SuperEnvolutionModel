# Epoch A reproduce helpers. Usage: .\scripts\reproduce_a.ps1 -Task unit
param(
  [ValidateSet("unit","m0-add","m0-stack","census-dry","census-smoke","studio","all-smoke")]
  [string]$Task = "unit"
)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Py = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Py)) { $Py = "python" }

function Invoke-Evo {
  param([string[]]$EvoArgs)
  & $Py -m evo @EvoArgs
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

switch ($Task) {
  "unit" { Invoke-Evo -EvoArgs @("unit") }
  "m0-add" { Invoke-Evo -EvoArgs @("plast","--stage","m0","--config","configs/evoplast_fit_add.yaml") }
  "m0-stack" { Invoke-Evo -EvoArgs @("plast","--stage","m0","--config","configs/evoplast_fit.yaml") }
  "census-dry" { Invoke-Evo -EvoArgs @("plast","--stage","census","--config","configs/evoplast_census_dry.yaml") }
  "census-smoke" { Invoke-Evo -EvoArgs @("plast","--stage","census","--config","configs/evoplast_census_smoke.yaml") }
  "studio" { Invoke-Evo -EvoArgs @("studio") }
  "all-smoke" {
    Invoke-Evo -EvoArgs @("unit")
    Invoke-Evo -EvoArgs @("plast","--stage","census","--config","configs/evoplast_census_dry.yaml")
    Write-Host "GPU steps: re-run with -Task m0-add or -Task census-smoke"
  }
}
