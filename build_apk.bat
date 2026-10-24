@echo off
setlocal EnableDelayedExpansion
title Ramgarh Escape - Android APK Builder
cd /d "%~dp0"

echo ===================================================================
echo             RAMGARH ESCAPE - ANDROID APK BUILDER
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
echo [2/3] Signing APK with Android Debug Keystore...
set "JARSIGNER=C:\Program Files\Java\jdk-24\bin\jarsigner.exe"
set "KEYSTORE=%APPDATA%\Godot\keystores\debug.keystore"

if exist "!JARSIGNER!" (
    if exist "!KEYSTORE!" (
        "!JARSIGNER!" -sigalg SHA256withRSA -digestalg SHA-256 -keystore "!KEYSTORE!" -storepass android "%~dp0build\android\RamgarhEscape.apk" androiddebugkey
        echo APK successfully signed!
    ) else (
        echo [WARNING] debug.keystore not found. APK may be unsigned.
    )
) else (
    echo [WARNING] jarsigner.exe not found. APK may be unsigned.
)

echo.
echo [3/3] Build Complete!
echo.
echo ===================================================================
echo   APK File Location:
echo   %~dp0build\android\RamgarhEscape.apk
echo ===================================================================
echo.
echo Opening folder so you can share it directly...
explorer.exe /select,"%~dp0build\android\RamgarhEscape.apk"

if not "%~1"=="--no-pause" pause
exit /b 0
