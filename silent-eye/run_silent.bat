@echo off
REM Silent-Eye Windows Launcher
REM Author: r4ttles
REM Enhanced Path Checking

echo.
echo ==========================================
echo     SILENT-EYE Advanced Recon Engine
echo             (Windows Edition)
echo ==========================================
echo.

set /p target_ip=Enter Target IP: 
set /p ports_range=Enter Ports (e.g., 1-1024 or 22,80,443): 

echo.
echo [*] Verifying Python Environment...

REM Try 'python' first, then 'py'
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    goto :found
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=py
    goto :found
)

echo [!] CRITICAL ERROR: Neither 'python' nor 'py' found in PATH.
echo [!] Please install Python from python.org and check "Add to PATH".
pause
exit /b 1

:found
echo [+] %PYTHON_CMD% detected. Starting scan...
echo.

%PYTHON_CMD% silent_eye.py -t %target_ip% -p %ports_range%

echo.
echo Scan finished. Check for .json output file.
pause
