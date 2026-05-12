@echo off
setlocal

set "TARGET_DIR=C:\ffmpeg\bin"
set "SOURCE_FILE=%~dp0ffmpeg.exe"

if not exist "%SOURCE_FILE%" (
    echo ffmpeg.exe not found next to this script.
    pause
    exit /b 1
)

mkdir "%TARGET_DIR%" 2>nul

copy /y "%SOURCE_FILE%" "%TARGET_DIR%\ffmpeg.exe" >nul 2>&1

if %errorlevel% equ 0 (
    echo ffmpeg.exe copied to %TARGET_DIR%
) else (
    echo Failed to copy ffmpeg.exe
    pause
    exit /b 1
)

setx PATH "%PATH%;C:\ffmpeg\bin" /M >nul 2>&1

echo Done.
pause