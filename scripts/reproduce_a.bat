@echo off
REM Usage: scripts\reproduce_a.bat unit|m0-add|m0-stack|census-dry|census-smoke|studio
setlocal
cd /d "%~dp0\.."
set PY=.venv\Scripts\python.exe
if not exist %PY% set PY=python
if "%1"=="" set TASK=unit
if not "%1"=="" set TASK=%1
if "%TASK%"=="unit" %PY% -m evo unit & goto :eof
if "%TASK%"=="m0-add" %PY% -m evo plast --stage m0 --config configs/evoplast_fit_add.yaml & goto :eof
if "%TASK%"=="m0-stack" %PY% -m evo plast --stage m0 --config configs/evoplast_fit.yaml & goto :eof
if "%TASK%"=="census-dry" %PY% -m evo plast --stage census --config configs/evoplast_census_dry.yaml & goto :eof
if "%TASK%"=="census-smoke" %PY% -m evo plast --stage census --config configs/evoplast_census_smoke.yaml & goto :eof
if "%TASK%"=="studio" %PY% -m evo studio & goto :eof
echo Unknown task %TASK%
exit /b 1
