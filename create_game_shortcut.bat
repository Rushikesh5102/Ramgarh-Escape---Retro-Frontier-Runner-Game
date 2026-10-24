@echo off
setlocal EnableDelayedExpansion
title Ramgarh Escape - Create Game Shortcut
cd /d "%~dp0"

echo ===================================================================
echo         RAMGARH ESCAPE - CREATE GAME LOGO SHORTCUT
echo ===================================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\create_shortcuts.ps1"

echo.
echo ===================================================================
echo   Done! Look on your Desktop and inside this folder for:
echo   "Ramgarh Escape" with the official game logo icon.
echo ===================================================================
echo.
if "%~1"=="" pause
