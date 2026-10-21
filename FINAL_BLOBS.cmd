@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if errorlevel 1 exit /b 1
set "PYTHONUTF8=1"
python analysis/finalize_blobs.py
if errorlevel 1 goto :failed
exit /b 0
:failed
echo FINAL BLOBS FAILED - inspect the preceding error; do not publish
exit /b 1
