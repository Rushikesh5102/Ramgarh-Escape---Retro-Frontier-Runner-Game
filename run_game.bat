@echo off
setlocal EnableDelayedExpansion
title Ramgarh Escape - Frontier Runner Game
cd /d "%~dp0"

set "IS_CLI=0"
if not "%~1"=="" set "IS_CLI=1"

:: -------------------------------------------------------------
:: GODOT ENGINE PATH DISCOVERY
:: -------------------------------------------------------------
set "GODOT_EXE=C:\Users\Rushi\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64.exe"
set "GODOT_CONSOLE=C:\Users\Rushi\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe"

if not exist "!GODOT_EXE!" (
    for %%P in (godot.exe godot_console.exe) do (
        for /f "tokens=*" %%F in ('where %%P 2^>nul') do (
            if exist "%%F" set "GODOT_EXE=%%F"
        )
    )
)
if not exist "!GODOT_CONSOLE!" (
    if exist "!GODOT_EXE!" set "GODOT_CONSOLE=!GODOT_EXE!"
)

:: -------------------------------------------------------------
:: COMMAND LINE ARGUMENT HANDLING
:: -------------------------------------------------------------
if /i "%~1"=="--play" goto :play_standalone
if /i "%~1"=="play" goto :play_standalone
if /i "%~1"=="1" goto :play_standalone

if /i "%~1"=="--engine" goto :play_engine
if /i "%~1"=="engine" goto :play_engine
if /i "%~1"=="2" goto :play_engine

if /i "%~1"=="--test" goto :run_tests
if /i "%~1"=="test" goto :run_tests
if /i "%~1"=="3" goto :run_tests

if /i "%~1"=="--export" goto :export_packages
if /i "%~1"=="--build" goto :export_packages
if /i "%~1"=="build" goto :export_packages
if /i "%~1"=="4" goto :export_packages

if /i "%~1"=="--assets" goto :regenerate_assets
if /i "%~1"=="assets" goto :regenerate_assets
if /i "%~1"=="5" goto :regenerate_assets

if /i "%~1"=="--editor" goto :launch_editor
if /i "%~1"=="editor" goto :launch_editor
if /i "%~1"=="6" goto :launch_editor

if /i "%~1"=="--push" goto :git_push
if /i "%~1"=="push" goto :git_push
if /i "%~1"=="7" goto :git_push

if /i "%~1"=="--web" goto :play_web
if /i "%~1"=="web" goto :play_web

:: -------------------------------------------------------------
:: INTERACTIVE COMMAND CENTER MENU
:: -------------------------------------------------------------
:menu
cls
echo ===================================================================
echo             RAMGARH ESCAPE - RETRO FRONTIER RUNNER
echo                Jai ^& Veeru's High-Speed Adventure
echo ===================================================================
echo.
echo   [1] Play Game (Standalone Windows Executable)
echo   [2] Play Game (Direct Godot Engine Mode)
echo   [3] Play Game (Web Browser - GitHub Pages Mode)
echo   [4] Run Automated QA Test Suite (Headless - 107 Tests)
echo   [5] Rebuild Release Packages (Windows ^& Android PCKs)
echo   [6] Regenerate Refined Sprites, Audio ^& Preview Banner
echo   [7] Launch Project in Godot 4 Editor
echo   [8] Sync ^& Push Latest Code to GitHub
echo   [9] Exit
echo.
echo ===================================================================
choice /c 123456789 /t 6 /d 1 /m "Select option (Auto-launches [1] in 6s):"
set "OPT=%ERRORLEVEL%"

if "%OPT%"=="1" goto :play_standalone
if "%OPT%"=="2" goto :play_engine
if "%OPT%"=="3" goto :play_web
if "%OPT%"=="4" goto :run_tests
if "%OPT%"=="5" goto :export_packages
if "%OPT%"=="6" goto :regenerate_assets
if "%OPT%"=="7" goto :launch_editor
if "%OPT%"=="8" goto :git_push
if "%OPT%"=="9" goto :eof
goto :menu

:: -------------------------------------------------------------
:: OPTION 3: PLAY IN WEB BROWSER
:: -------------------------------------------------------------
:play_web
echo.
echo [1/1] Launching Ramgarh Escape in your default web browser...
start "" "%~dp0index.html"
exit /b 0

:: -------------------------------------------------------------
:: OPTION 1: PLAY STANDALONE EXECUTABLE
:: -------------------------------------------------------------
:play_standalone
echo.
echo [1/1] Launching standalone Ramgarh Escape...
cd /d "%~dp0build\windows"
if exist "RamgarhEscape.exe" (
    start "" "RamgarhEscape.exe"
    echo Game launched successfully.
) else if exist "EscapeFromRamgarh.exe" (
    start "" "EscapeFromRamgarh.exe"
    echo Game launched successfully.
) else (
    echo [WARNING] Standalone executable not found in build\windows.
    echo Launching via Godot Engine instead...
    goto :play_engine
)
exit /b 0

:: -------------------------------------------------------------
:: OPTION 2: PLAY DIRECT VIA GODOT ENGINE
:: -------------------------------------------------------------
:play_engine
echo.
echo [1/1] Launching Ramgarh Escape in Godot Engine...
cd /d "%~dp0"
if exist "!GODOT_EXE!" (
    start "" "!GODOT_EXE!" --path "%~dp0."
    echo Game launched in Godot Engine.
) else (
    echo [ERROR] Godot executable not found at: !GODOT_EXE!
    pause
)
exit /b 0

:: -------------------------------------------------------------
:: OPTION 3: RUN AUTOMATED TEST SUITE
:: -------------------------------------------------------------
:run_tests
echo.
echo ===================================================================
echo           RUNNING HEADLESS AUTOMATED TEST SUITE
echo ===================================================================
cd /d "%~dp0"
if exist "!GODOT_CONSOLE!" (
    "!GODOT_CONSOLE!" --headless --path "%~dp0." "res://tests/test_runner.tscn"
) else if exist "!GODOT_EXE!" (
    "!GODOT_EXE!" --headless --path "%~dp0." "res://tests/test_runner.tscn"
) else (
    echo [ERROR] Godot console executable not found.
)
echo.
echo ===================================================================
echo Test run complete.
if "!IS_CLI!"=="1" exit /b %ERRORLEVEL%
pause
goto :menu

:: -------------------------------------------------------------
:: OPTION 4: REBUILD RELEASE PACKAGES
:: -------------------------------------------------------------
:export_packages
echo.
echo ===================================================================
echo          REBUILDING RELEASE DATA PACKAGES (PCK)
echo ===================================================================
cd /d "%~dp0"
if not exist "!GODOT_CONSOLE!" (
    echo [ERROR] Godot console executable not found.
    if "!IS_CLI!"=="1" exit /b 1
    pause
    goto :menu
)
echo [1/2] Exporting Windows Desktop Package (build\windows\RamgarhEscape.pck)...
"!GODOT_CONSOLE!" --headless --path "%~dp0." --export-pack "Windows Desktop" "%~dp0build\windows\RamgarhEscape.pck"
echo [2/2] Exporting Android Package (build\android\RamgarhEscape.pck)...
"!GODOT_CONSOLE!" --headless --path "%~dp0." --export-pack "Android" "%~dp0build\android\RamgarhEscape.pck"
echo.
echo Packages rebuilt successfully!
if "!IS_CLI!"=="1" exit /b %ERRORLEVEL%
pause
goto :menu

:: -------------------------------------------------------------
:: OPTION 5: REGENERATE REFINED ASSETS & SPRITES
:: -------------------------------------------------------------
:regenerate_assets
echo.
echo ===================================================================
echo        REGENERATING REFINED CHARACTER SPRITES & AUDIO
echo ===================================================================
cd /d "%~dp0"
echo [1/5] Generating refined Jai & Veeru sprites with BSA Motorbike...
python tools\generate_refined_player.py
echo [2/5] Generating Basanti sprites, Dhanno tanga, and dialogue avatars...
python tools\generate_girls_and_portraits.py
echo [3/5] Generating Bollywood soundtracks, songs, and dialogue voice FX...
python tools\generate_bollywood_music.py
echo [4/5] Generating core background layers, obstacles, and UI assets...
python tools\generate_all_assets.py
echo [5/5] Generating 1200x630 social preview banner (preview.png)...
python tools\generate_preview_banner.py
echo.
echo All assets regenerated successfully!
if "!IS_CLI!"=="1" exit /b %ERRORLEVEL%
pause
goto :menu

:: -------------------------------------------------------------
:: OPTION 6: LAUNCH GODOT 4 EDITOR
:: -------------------------------------------------------------
:launch_editor
echo.
echo Launching project in Godot 4 Editor...
cd /d "%~dp0"
if exist "!GODOT_EXE!" (
    start "" "!GODOT_EXE!" -e --path "%~dp0."
) else (
    echo [ERROR] Godot executable not found at: !GODOT_EXE!
    if "!IS_CLI!"=="1" exit /b 1
    pause
)
exit /b 0

:: -------------------------------------------------------------
:: OPTION 7: GIT STATUS & PUSH
:: -------------------------------------------------------------
:git_push
echo.
echo ===================================================================
echo               SYNCING & PUSHING TO GITHUB
echo ===================================================================
cd /d "%~dp0"
git status
echo.
if "!IS_CLI!"=="1" (
    set "COMMIT_MSG=%~2"
    if "!COMMIT_MSG!"=="" set "COMMIT_MSG=chore: update project assets and game configuration"
) else (
    set /p COMMIT_MSG="Enter commit message (Press Enter for default): "
    if "!COMMIT_MSG!"=="" set "COMMIT_MSG=chore: update project assets and game configuration"
)
git add .
git commit -m "!COMMIT_MSG!"
git push -u origin main
echo.
echo Push completed!
if "!IS_CLI!"=="1" exit /b %ERRORLEVEL%
pause
goto :menu
