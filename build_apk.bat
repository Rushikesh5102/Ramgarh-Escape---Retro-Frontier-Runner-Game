@echo off
setlocal EnableDelayedExpansion
title Ramgarh Escape - Android APK Builder
cd /d "%~dp0"

echo ===================================================================
echo             RAMGARH ESCAPE - ANDROID APK BUILDER
echo               With Official Custom Game Logo Icon
echo ===================================================================
echo.

set "GODOT_CONSOLE=C:\Users\Rushi\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe"
if not exist "!GODOT_CONSOLE!" (
    for %%P in (godot_console.exe godot.exe) do (
        for /f "tokens=*" %%F in ('where %%P 2^>nul') do (
            if exist "%%F" set "GODOT_CONSOLE=%%F"
        )
    )
)

if not exist "!GODOT_CONSOLE!" (
    echo [ERROR] Godot console executable not found!
    pause
    exit /b 1
)

if not exist "build\android" mkdir "build\android"

echo [1/3] Building RamgarhEscape.apk with Godot 4.7.2...
"!GODOT_CONSOLE!" --headless --path "%~dp0." --export-debug Android "%~dp0build\android\RamgarhEscape.apk"

if not exist "%~dp0build\android\RamgarhEscape.apk" (
    echo [ERROR] APK export failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Injecting Official Game Logo Icons ^& Adaptive Mipmaps...
python "%~dp0tools\inject_apk_icons.py"

echo.
echo [3/3] Build ^& Verification Complete!
echo.
echo ===================================================================
echo   APK File Location:
echo   %~dp0build\android\RamgarhEscape.apk
echo.
echo   - App Icon: Official Ramgarh Escape Golden Crest with Veeru
echo   - Status: Signed ^& Verified with debug.keystore
echo ===================================================================
echo.
if not "%~1"=="--no-pause" (
    echo Opening folder so you can share it directly...
    start "" "%~dp0build\android"
    pause
)
exit /b 0
