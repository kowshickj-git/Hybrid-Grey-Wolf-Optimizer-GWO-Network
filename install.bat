@echo off
rem ==========================================================================
rem  One-click installer for the Hybrid GWO-ABC WSN project (Windows).
rem  Double-click this file, or run "install.bat /quiet" for no questions.
rem  It does not need MATLAB. Everything is installed inside this folder
rem  (.venv), so other Python projects on the computer are not affected.
rem ==========================================================================
setlocal EnableExtensions
title Hybrid GWO-ABC WSN - installer
cd /d "%~dp0"

set "QUIET="
if /i "%~1"=="/quiet" set "QUIET=1"

echo ============================================================
echo  Hybrid GWO-ABC WSN project - one-click installer
echo ============================================================
echo  Folder: %CD%
echo.

if exist "main.py" goto :find_python
echo [ERROR] main.py was not found next to install.bat.
echo         If you downloaded a ZIP file, extract it first:
echo         right-click the ZIP, choose "Extract All", open the extracted
echo         folder and double-click install.bat there.
goto :fail

rem --------------------------------------------------------------------------
:find_python
echo [1/5] Looking for Python 3.10 or newer ...
set "PY="
call :try_python py -3
if not defined PY call :try_python python
if not defined PY call :try_python "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if not defined PY call :try_python "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PY call :try_python "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not defined PY call :try_python "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if not defined PY call :try_python "%ProgramFiles%\Python313\python.exe"
if not defined PY call :try_python "%ProgramFiles%\Python312\python.exe"
if not defined PY call :try_python "%ProgramFiles%\Python311\python.exe"
if not defined PY call :try_python "%ProgramFiles%\Python310\python.exe"
if defined PY goto :have_python

echo.
echo       Python 3.10 or newer was not found on this computer.
where winget >nul 2>&1
if errorlevel 1 goto :manual_python
if defined QUIET goto :install_python
choice /c YN /m "      Install Python 3.12 now (free, official python.org build via winget)"
if errorlevel 2 goto :manual_python

:install_python
echo       Installing Python 3.12 - this can take a few minutes ...
winget install -e --id Python.Python.3.12 --scope user --silent --accept-package-agreements --accept-source-agreements
call :try_python "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PY call :try_python py -3
if defined PY goto :have_python

:manual_python
echo.
echo       Please install Python yourself, then run install.bat again:
echo         1. Open https://www.python.org/downloads/ and download Python 3.12 for Windows.
echo         2. In the installer TICK "Add python.exe to PATH", then click "Install Now".
echo         3. Double-click install.bat again.
goto :fail

:have_python
%PY% -c "import sys; print('      found Python', sys.version.split()[0], 'at', sys.executable)"
%PY% -c "import tkinter" >nul 2>&1
if not errorlevel 1 goto :make_venv
echo       [warning] Tkinter is missing, so the simulator window - the GUI - will not open.
echo                 Everything else works. To fix it, run the Python installer again,
echo                 choose "Modify" and tick "tcl/tk and IDLE".

rem --------------------------------------------------------------------------
:make_venv
echo.
echo [2/5] Creating a private Python environment in .venv ...
if exist ".venv\Scripts\python.exe" goto :venv_ready
%PY% -m venv .venv
if errorlevel 1 goto :venv_failed
:venv_ready
set "VPY=%CD%\.venv\Scripts\python.exe"
echo       ready: .venv

rem --------------------------------------------------------------------------
echo.
echo [3/5] Installing the libraries: NumPy, pandas, Matplotlib, SciPy, pytest
echo       The first time this downloads about 100 MB and takes a few minutes ...
"%VPY%" -m pip install --upgrade pip --disable-pip-version-check -q
"%VPY%" -m pip install -r requirements.txt --disable-pip-version-check
if errorlevel 1 goto :pip_failed

rem --------------------------------------------------------------------------
echo.
echo [4/5] Checking the installation ...
"%VPY%" -c "import numpy, pandas, matplotlib, scipy; print('      NumPy', numpy.__version__, '- pandas', pandas.__version__, '- Matplotlib', matplotlib.__version__, '- SciPy', scipy.__version__)"
if errorlevel 1 goto :pip_failed

rem --------------------------------------------------------------------------
echo.
echo [5/5] Running the automatic tests - about 15 to 60 seconds ...
set "TESTS=passed"
"%VPY%" -m pytest -q
if errorlevel 1 set "TESTS=FAILED - see docs\07_TROUBLESHOOTING.md, section Tests"

echo.
echo ============================================================
echo  Installation finished.   Automatic tests: %TESTS%
echo ============================================================
echo  What next?
echo    - Double-click run.bat for a menu: open the simulator window,
echo      run a simulation, compare the algorithms, run the tests ...
echo    - Read the beginner guide: docs\00_START_HERE.md
echo ============================================================
if not defined QUIET pause
exit /b 0

rem --------------------------------------------------------------------------
:venv_failed
echo [ERROR] Could not create the .venv folder. Check that you may write to this
echo         folder - do not run it inside the ZIP file or from a read-only drive.
goto :fail

:pip_failed
echo [ERROR] Installing the libraries failed. Check the internet connection and run
echo         install.bat again. Details: docs\07_TROUBLESHOOTING.md, "pip install fails".
goto :fail

:fail
echo.
echo  Installation did not finish. Help: docs\07_TROUBLESHOOTING.md
if not defined QUIET pause
exit /b 1

rem --------------------------------------------------------------------------
rem  :try_python <command>  - sets PY when <command> is Python 3.10 or newer
:try_python
%* -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if not errorlevel 1 set "PY=%*"
exit /b 0
