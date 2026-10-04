@echo off
rem ==========================================================================
rem  Menu for the Hybrid GWO-ABC WSN project (Windows). Run install.bat first.
rem  Double-click for the menu, or run "run.bat <number>" to start one option.
rem ==========================================================================
setlocal EnableExtensions
title Hybrid GWO-ABC WSN
cd /d "%~dp0"
set "VPY=%CD%\.venv\Scripts\python.exe"
if exist "%VPY%" goto :ready
echo  The project is not installed yet: double-click install.bat first.
pause
exit /b 1

:ready
set "OPTION=%~1"
set "DIRECT=%~1"
if defined DIRECT goto :dispatch

:menu
cls
echo ==============================================================
echo   Hybrid GWO-ABC - energy-efficient cluster-head selection
echo ==============================================================
echo    1  Open the simulator window - GUI
echo    2  One simulation of the proposed Hybrid GWO-ABC      ~35 s
echo    3  Compare Random, LEACH, GWO, ABC and Hybrid
echo       on 3 networks                                     ~2 min
echo    4  Run the automatic tests                           ~15 s
echo    5  Main comparison, scenario S1, 20 networks        ~12 min
echo    6  Comparison with the base paper                 ~1 h 20 min
echo    7  Redraw the documentation diagrams                 ~10 s
echo    8  Open the beginner guide in the web browser
echo    9  Open the results folder
echo    0  Exit
echo ==============================================================
choice /c 1234567890 /n /m "  Type a number: "
set "OPTION=%ERRORLEVEL%"
if "%OPTION%"=="10" exit /b 0

:dispatch
if not defined DIRECT if "%OPTION%"=="5" call :confirm "results\scenarios\S1_100nodes"
if not defined DIRECT if "%OPTION%"=="6" call :confirm "results\base_paper"
if "%OPTION%"=="skip" goto :done
if "%OPTION%"=="1" "%VPY%" main.py
if "%OPTION%"=="2" "%VPY%" main.py simulate
if "%OPTION%"=="3" "%VPY%" main.py compare --runs 3
if "%OPTION%"=="4" "%VPY%" -m pytest -q
if "%OPTION%"=="5" "%VPY%" main.py scenarios --only S1_100nodes
if "%OPTION%"=="6" "%VPY%" main.py basepaper
if "%OPTION%"=="7" "%VPY%" main.py diagrams
if "%OPTION%"=="8" start "" "https://github.com/kowshickj-git/Hybrid-Grey-Wolf-Optimizer-GWO-Network/blob/main/docs/00_START_HERE.md"
if "%OPTION%"=="9" start "" "%CD%\results"

:done
if defined DIRECT exit /b %ERRORLEVEL%
echo.
pause
goto :menu

rem  :confirm <folder>  - long experiments re-create saved results; ask first
:confirm
echo.
echo  This re-runs the experiment and replaces the saved results in %~1
echo  (with the same settings and seeds you get the same numbers again).
choice /c YN /m "  Continue"
if errorlevel 2 set "OPTION=skip"
exit /b 0
