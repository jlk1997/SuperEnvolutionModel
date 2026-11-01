# Reproduce Epoch C product path checks (no exam / Gate2).
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..
$py = ".\.venv\Scripts\python.exe"
Write-Host "=== router unit tests (incl. multi-atom conflict) ==="
& $py -m unittest evo.tests.test_office_router_atoms -v
Write-Host "=== route smoke (CPU) four families ==="
& $py -c @"
from evo.crystal.router import route
for s in ('table','report','file','shell'):
    d = route(s, notes='x', prefer_atom=True)
    assert d['mode']=='atom' and d['atom']==f'office_{s}_uselog', d
    print(s, d['atom'], 'bare', d.get('bare_rate'))
# cross-steal sanity
assert route('table', notes='x')['atom'] != 'office_shell_uselog'
print('cross-family OK')
"@
Write-Host "=== atoms ==="
Get-ChildItem runs\capabilities\office_*_uselog | Select-Object Name
Write-Host "C product path OK (table/report/file/shell). B/exam NOT claimed. Gate 0.6."
