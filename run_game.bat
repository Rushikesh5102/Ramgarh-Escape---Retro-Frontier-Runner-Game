@echo off
title Ramgarh Escape
echo ========================================================
echo   Launching Ramgarh Escape...
echo ========================================================
cd /d "%~dp0build\windows"
if exist "RamgarhEscape.exe" (
    start "" "RamgarhEscape.exe"
) else (
    start "" "EscapeFromRamgarh.exe"
)
