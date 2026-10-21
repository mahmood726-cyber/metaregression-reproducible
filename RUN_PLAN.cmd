@echo off
echo === Enable local environment
setlocal EnableExtensions
echo === Archive working directory
cd /d "%~dp0"
if errorlevel 1 goto :failed
echo === Python UTF-8
set PYTHONUTF8=1
echo === Disable unrelated pytest plugin auto-loading
set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
echo === Environment from caller; see RUN_PLAN_EXPECTED.md
if defined R_BIN set "PATH=%R_BIN%;%PATH%"
set "R_ENVIRON_USER=NUL"
echo === Default browser
if not defined PW_CHANNEL set "PW_CHANNEL=msedge"
rem PLAYWRIGHT_MODULE and LINKEDOM_MODULE may select existing installations.
rem Otherwise the preflight requires locally resolvable modules.
echo === Dependency and target preflight
python analysis/recut_preflight.py
if errorlevel 1 goto :failed
echo === Verify prepared integrity
python analysis/recut_integrity.py verify
if errorlevel 1 goto :failed
echo === Preserve prior outputs and scratch folders without deletion
python analysis/preserve_recut_attempt.py
if errorlevel 1 goto :failed
echo === Prepare clean stage
python analysis/recut.py prepare
if errorlevel 1 goto :failed
echo === Fresh original browser
python analysis/recut.py original
if errorlevel 1 goto :failed
echo === Original replay gate
python analysis/recut.py compare-original
if errorlevel 1 goto :failed
echo === Original UI
python analysis/recut.py ui
if errorlevel 1 goto :failed
echo === Fresh original R
python bench/launch.py outputs/recut/validate_R.log Rscript validate.R
if errorlevel 1 goto :failed
echo === Extras numeric
python analysis/recut.py numeric
if errorlevel 1 goto :failed
echo === Extras DOM and negative probes
python analysis/recut.py dom
if errorlevel 1 goto :failed
echo === Extras browser
python analysis/recut.py browser
if errorlevel 1 goto :failed
echo === Historical outputs
python analysis/make_outputs.py
if errorlevel 1 goto :failed
echo === Safeguards
python -m pytest -q analysis/test_safeguards.py analysis/test_recut.py
if errorlevel 1 goto :failed
echo === R safeguard plant check on the uncorrupted table
python analysis/check_r_guard_plant.py
if errorlevel 1 goto :failed
echo === Archive verification
python analysis/verify_archive.py
if errorlevel 1 goto :failed
echo === Executed replay gates
python analysis/recut_integrity.py verify --executed
if errorlevel 1 goto :failed
echo === Execution plan complete; allmeta v1.8.0 1cb3f84 replay gates passed
exit /b 0
:failed
echo === FAILED - inspect the preceding command and outputs/recut; do not publish
exit /b 1
